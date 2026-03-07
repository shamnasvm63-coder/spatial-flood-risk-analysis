# coding=utf-8
import ee
from ee_plugin import Map
from datetime import datetime

# ==========================================
# 1. CLOUD MASKING FUNCTION (Sentinel-2)
# ==========================================
def maskS2clouds(image):
    qa = image.select('QA60')
    # Bits 10 and 11 are clouds and cirrus, respectively.
    cloudBitMask = 1 << 10
    cirrusBitMask = 1 << 11
    # Ensure both flags are zero for clear conditions
    mask = qa.bitwiseAnd(cloudBitMask).eq(0).And(qa.bitwiseAnd(cirrusBitMask).eq(0))
    return image.updateMask(mask).divide(10000)

# ==========================================
# 2. SELECT AREA OF INTEREST (AOI)
# ==========================================
Administrative_Units = ee.FeatureCollection("FAO/GAUL/2015/level2")
# Filtering for Malappuram District, Kerala
aoi = Administrative_Units.filter(ee.Filter.eq('ADM2_NAME', "Malappuram"))

# ==========================================
# 3. LOAD & PROCESS SENTINEL-2 (2024)
# ==========================================
start_date = '2024-01-01'
end_date = '2024-06-30'

# Load collection and apply cloud mask
S2_collection = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED') \
    .filterDate(start_date, end_date) \
    .filterBounds(aoi) \
    .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20)) \
    .map(maskS2clouds)

# Create a Median Reducer composite to remove transient shadows
median_image = S2_collection.median().clip(aoi)

# Calculate NDVI (Normalized Difference Vegetation Index)
ndvi = median_image.normalizedDifference(['B8', 'B4']).rename('NDVI')

# Final band selection for CART prediction (Including Moisture and Vegetation bands)
bands = ['B2', 'B3', 'B4', 'B8', 'B11', 'B12', 'NDVI']
input_data = median_image.addBands(ndvi).select(bands)

# ==========================================
# 4. LOAD TRAINING DATA & SAMPLE REGIONS
# ==========================================
# Path to your GEE Asset (Ensure this path is correct in your GEE account)
training_data = ee.FeatureCollection("projects/psychic-mason-479416-q2/assets/Training_Points_Malappuram")
label = 'id' 

# Extract spectral values at the training point locations
trainingImage = input_data.sampleRegions(
    **{'collection': training_data, 'properties': [label], 'scale': 10}
)

# Split 80% Training / 20% Validation (As per academic standards)
training_random = trainingImage.randomColumn()
trainingSet = training_random.filter(ee.Filter.lessThan('random', 0.8))
validationSet = training_random.filter(ee.Filter.greaterThanOrEquals('random', 0.8))

# ==========================================
# 5. TRAIN CART CLASSIFIER & CLASSIFY
# ==========================================
# CART Classifier configured for your LULC classes
trainedClassifier = ee.Classifier.smileCart().train(trainingSet, label, bands)
rawClassified = input_data.classify(trainedClassifier)

# ==========================================
# 6. POST-CLASSIFICATION: SIEVE FILTER (Noise Reduction)
# ==========================================
# Removes "salt-and-pepper" noise using an 8-pixel threshold (~800m2)
# This ensures the map highlights landscape-level changes
sievedImage = rawClassified.connectedPixelCount(8, True) \
    .reproject('EPSG:4326', None, 10) \
    .where(rawClassified.connectedPixelCount(8, true).lt(8), 
           rawClassified.focal_mode(1, 'square', 'pixels', 1))

# ==========================================
# 7. VISUALIZATION & MAP OUTPUT
# ==========================================
# Palette: 0: Urban (Gray), 1: Forest (Green), 2: Water (Blue), 3: Agriculture (Yellow)
land_cover_palette = ['#929595', '#3d9554', '#538ae4', '#f1c40f']

Map.centerObject(aoi, 10)
Map.addLayer(sievedImage, {'palette': land_cover_palette, 'min': 0, 'max': 3}, 'LULC_2024_Malappuram_Final')

# ==========================================
# 8. ACCURACY ASSESSMENT
# ==========================================
print('--- RESULTS: MALAPPURAM 2024 ---')

# Training Accuracy
trainAccuracy = trainedClassifier.confusionMatrix()
print('Training Overall Accuracy:', trainAccuracy.accuracy().getInfo())

# Validation Accuracy (Independent Test)
validationSetClassified = validationSet.classify(trainedClassifier)
valAccuracy = validationSetClassified.errorMatrix(label, 'classification')
print('Validation Accuracy (Mean Value):', valAccuracy.accuracy().getInfo())
print('Validation Error Matrix:', valAccuracy.getInfo())

# ==========================================
# 9. EXPORT TO GOOGLE DRIVE
# ==========================================
task_config = {
    'region': aoi.geometry().bounds(),
    'crs': 'EPSG:4326',
    'fileFormat': 'GeoTIFF',
    'scale': 10,  # 10m Sentinel-2 Resolution
    'fileNamePrefix': "Malappuram_LULC_2024_Final",
    'image': sievedImage,
    'description': 'Export_LULC_Final_' + datetime.now().strftime("%Y%m%d"),
    'maxPixels': 1e13
}

task = ee.batch.Export.image.toDrive(**task_config)
task.start()
print('Export Task Started. Check the "Tasks" tab in GEE to confirm.')