# ===============================================================
# GEOG676 - Lab 7: Raster Analysis
# Author: Kenneth Struck
# Date: October 2025
# Description:
#   Combines Landsat 9 bands (4,3,2) into a composite raster
#   and performs hillshade and slope analysis using DEM data.
# ===============================================================

import arcpy
import os
from arcpy.sa import *

# --- Workspace setup ---
proj_dir = r"C:\Users\kenne\Documents\ArcGIS\Projects\GEOG676_Lab7"
gdb = os.path.join(proj_dir, "GEOG676_Lab7.gdb")
arcpy.env.workspace = gdb
arcpy.env.overwriteOutput = True

print("Initializing workspace...")
arcpy.CheckOutExtension("Spatial")

# --- Input rasters ---
# These are the actual Landsat 9 band file names from your extracted download
band4 = os.path.join(proj_dir, "LC09_L1TP_023031_20240926_20240926_02_T1_B4.TIF")  # Red
band3 = os.path.join(proj_dir, "LC09_L1TP_023031_20240926_20240926_02_T1_B3.TIF")  # Green
band2 = os.path.join(proj_dir, "LC09_L1TP_023031_20240926_20240926_02_T1_B2.TIF")  # Blue

# DEM (Digital Elevation Model)
dem = os.path.join(proj_dir, "DEM_Chicago.tif")

# --- Verify inputs ---
inputs = [band4, band3, band2, dem]
for f in inputs:
    if not os.path.exists(f):
        print(f"⚠️  Missing: {f}")
        raise FileNotFoundError("One or more input rasters are missing!")

print("✅ All input rasters located successfully.\n")

# --- Output file paths ---
composite_out = os.path.join(proj_dir, "Chicago_Composite.tif")
hillshade_out = os.path.join(proj_dir, "Chicago_Hillshade.tif")
slope_out = os.path.join(proj_dir, "Chicago_Slope.tif")

# --- Step 1: Create composite raster ---
print("Creating RGB composite (Bands 4, 3, 2)...")
arcpy.management.CompositeBands([band4, band3, band2], composite_out)
print(f"✅ Composite created: {composite_out}\n")

# --- Step 2: Create Hillshade raster ---
print("Creating Hillshade from DEM...")
hillshade = Hillshade(dem, azimuth=315, altitude=45)
hillshade.save(hillshade_out)
print(f"✅ Hillshade created: {hillshade_out}\n")

# --- Step 3: Create Slope raster ---
print("Creating Slope raster from DEM...")
slope = Slope(dem, "DEGREE")
slope.save(slope_out)
print(f"✅ Slope raster created: {slope_out}\n")

# --- Cleanup ---
arcpy.CheckInExtension("Spatial")
print("✅ Lab 7 complete! All rasters saved to GEOG676_Lab7 folder.")
