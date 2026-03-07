# spatial-flood-risk-analysis
LULC Classification and Flood Vulnerability Analysis of Malappuram District (2018–2024) using Sentinel-2 and CART Machine Learning
# Spatial Flood Risk Analysis: Malappuram District (2018–2024)

## Project Overview
This study uses **Sentinel-2 MSI Level-2A** imagery and the **CART (Classification and Regression Tree)** algorithm to analyze land-use changes following the 2018 Kerala floods. We specifically identified a "Hydrological Shift" where 512.49 km² transitioned into high-risk saturated zones.

## 📁 Repository Structure
* **[/scripts](./malappuram_cart_classification_2024.py):** Google Earth Engine Python script for CART classification.
* **[/Maps](./Maps/):** High-resolution classification results (including [2024 Classified Map](./Maps/Map4_2024_Classified.png)).
* **[/Data](./Malapuram%20Traininpoints/):** Training point shapefiles used for model calibration.
* **[Output Statistics](./OUTPUT_HTML_FILE.csv):** Pixel counts and area calculations extracted via QGIS.

## 💾 Large Data Access (GeoTIFF)
Due to GitHub's file size limits, the raw high-resolution rasters are hosted on Google Drive:
* **[Download Raw .tif Rasters (2018 & 2024)](https://drive.google.com/drive/folders/13d-R1bNFMPGukvrqfEHvV1RQfb9UMwlw?usp=sharing)**

## 📊 Key Results
| Metric | 2018 (Baseline) | 2024 (Current) |
| :--- | :--- | :--- |
| **Urban Pixel Count** | 40,338,109 | *See CSV for delta* |
| **Validation Accuracy** | ~74% | Robust Kappa |

## Alignment with UN SDGs
* **SDG 11:** Sustainable Cities (Risk-informed zoning).
* **SDG 15:** Life on Land (Forest recovery in the Western Ghats).
