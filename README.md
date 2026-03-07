# spatial-flood-risk-analysis
LULC Classification and Flood Vulnerability Analysis of Malappuram District (2018–2024) using Sentinel-2 and CART Machine Learning
# Spatial Flood Risk Analysis: Malappuram District (2018–2024)

## Project Overview

This study uses **Sentinel-2 MSI Level-2A** imagery and the **CART (Classification and Regression Tree)** algorithm to analyze land-use changes following the 2018 Kerala floods. We specifically identified a "Hydrological Shift" where **512.49 km²** transitioned into high-risk saturated zones. This project combines remote sensing, Python-based classification, and GIS-based statistical analysis.

## 📁 Repository Structure

* **[Final Project Report](https://www.google.com/search?q=./Group%252013%2520Final%2520Report.docx):** Full comprehensive documentation of methodology, results, and flood-risk conclusions.
* **[/scripts](https://www.google.com/search?q=./malappuram_cart_classification_2024.py):** Google Earth Engine Python script for CART classification.
* **[/Maps](https://www.google.com/search?q=./Maps/):** High-resolution classification results (including [2024 Classified Map](https://www.google.com/search?q=./Maps/Map4_2024_Classified.png)).
* **[/Data](https://www.google.com/search?q=./Malapuram%2520Traininpoints/):** Training point shapefiles used for model calibration.
* **[Output Statistics](https://www.google.com/search?q=./OUTPUT_HTML_FILE.csv):** Pixel counts and area calculations extracted via QGIS.

## 💾 Large Data Access (GeoTIFF)

Due to GitHub's file size limits (over 41MB), the raw high-resolution GeoTIFF rasters are hosted externally:

* **[Download Raw .tif Rasters (2018 & 2024)](https://drive.google.com/drive/folders/13d-R1bNFMPGukvrqfEHvV1RQfb9UMwlw?usp=sharing)**

## 📊 Key Results

| Metric | 2018 (Baseline) | 2024 (Current) |
| --- | --- | --- |
| **Urban Pixel Count** | 40,338,109 | See `OUTPUT_HTML_FILE.csv` |
| **Validation Accuracy** | ~74% | Robust Kappa Coefficient |

## 🌍 Alignment with UN SDGs

* **SDG 11: Sustainable Cities & Communities** – Implementing risk-informed zoning based on flood-saturated zones.
* **SDG 13: Climate Action** – Monitoring environmental changes post-extreme weather events.
* **SDG 15: Life on Land** – Tracking forest recovery and land degradation in the Western Ghats region.

