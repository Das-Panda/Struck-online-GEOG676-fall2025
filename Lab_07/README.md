GEOG676 - Lab 7: Raster Analysis

Author: Kenneth Struck
Course: GEOG 676 – Advanced Geospatial Programming (Texas A&M University)
Date: October 2025

🛰️ Overview

This lab demonstrates raster analysis using satellite and elevation data for the Chicago, Illinois region. The analysis integrates Landsat 9 multispectral imagery and an SRTM 1 Arc-Second DEM to produce:

A composite raster image (Bands 4, 3, 2 for true color)

A hillshade raster showing terrain illumination

A slope raster indicating surface steepness in degrees

All processing was performed in ArcGIS Pro using ArcPy and the Spatial Analyst extension.

📂 Data Sources
Dataset	Source	Description
Landsat 9 OLI/TIRS Collection 2 Level-1	USGS EarthExplorer	Multispectral satellite imagery (Path 023, Row 031, 2024-09-26) used to create RGB composite
SRTM 1 Arc-Second Global DEM	USGS EarthExplorer	Digital Elevation Model providing surface height data for hillshade and slope analyses

⚙️ Processing Steps

Downloaded Landsat 9 Bands (B2, B3, B4) and DEM in GeoTIFF format.

Set the project workspace in ArcPy to the GEOG676_Lab7 folder.

Created an RGB composite raster using Bands 4, 3, and 2 to produce a true-color image.

Generated a hillshade raster using the DEM with an azimuth of 315° and altitude of 45°.

Calculated slope in degrees from the same DEM.

Exported all final products as GeoTIFF files and verified them visually in ArcGIS Pro.

🗺️ Outputs
File	Description
Chicago_Composite.tif	RGB composite raster (True Color)
Chicago_Hillshade.tif	Hillshade raster based on DEM
Chicago_Slope.tif	Slope raster (degrees)
Lab7_RasterAnalysis_Final.py	Python script automating the full process

🖼️ Visual Results
🌆 Composite Raster (Bands 4-3-2)


Displays natural color imagery of the Chicago metropolitan area using Landsat 9 data.

🏔️ Hillshade Raster


Shaded relief image emphasizing terrain features derived from the SRTM DEM.

📈 Slope Raster


Visualizes slope steepness — lighter areas indicate steeper terrain, while darker areas are flatter.

🧠 Key Takeaways

Landsat and SRTM data can be effectively combined for multi-layered raster analysis.

ArcPy simplifies repetitive workflows for imagery and terrain processing.

Composite, hillshade, and slope rasters provide complementary visual and analytical insights into surface features.

✅ Deliverables

GitHub Repository: Includes all Python code and raster outputs.

Canvas Submission: Contains screenshots of the composite, hillshade, and slope rasters.
