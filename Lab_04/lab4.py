# -*- coding: utf-8 -*-
"""
GEOG 676 - Lab 4
Author: Kenneth Struck
"""

import os, csv
import arcpy

# -----------------------------
# FOLDER SETUP
# -----------------------------
BASE_DIR = r"C:\Users\kenne\Desktop\GEOG676_Lab4"
GARAGES_CSV = os.path.join(BASE_DIR, "garages.csv")
CAMPUS_GDB = os.path.join(BASE_DIR, "Campus.gdb")
STRUCTURES_FC = os.path.join(CAMPUS_GDB, "Structures")

OUT_GDB = os.path.join(BASE_DIR, "Homework04.gdb")

arcpy.env.overwriteOutput = True

# -----------------------------
# HELPER FUNCTIONS
# -----------------------------
def ensure_gdb(path_gdb):
    """Create output GDB if it doesn’t exist"""
    if not arcpy.Exists(path_gdb):
        arcpy.management.CreateFileGDB(os.path.dirname(path_gdb),
                                       os.path.basename(path_gdb))
    return path_gdb

def detect_xy_fields(csv_path):
    """Find X/Y or Lon/Lat fields in garages.csv"""
    with open(csv_path, newline="", encoding="utf-8") as f:
        header = next(csv.reader(f))
    header_lc = [h.lower() for h in header]
    # common guesses
    x_candidates = ["x", "lon", "longitude"]
    y_candidates = ["y", "lat", "latitude"]

    x_field = next((h for h in header if h.lower() in x_candidates), None)
    y_field = next((h for h in header if h.lower() in y_candidates), None)

    if not x_field or not y_field:
        raise RuntimeError("Could not detect XY fields. Please rename headers in garages.csv to X,Y or Lon,Lat")
    return x_field, y_field

# -----------------------------
# MAIN WORKFLOW
# -----------------------------
print("=== Lab 4 workflow starting ===")

# 1) Create GDB
ensure_gdb(OUT_GDB)

# 2) Find XY fields in garages.csv
x_field, y_field = detect_xy_fields(GARAGES_CSV)
print(f"Detected fields → X: {x_field}, Y: {y_field}")

# 3) Garages CSV is in WGS84 (lat/long)
csv_sr = arcpy.SpatialReference(4326)  # EPSG:4326 (WGS 84)

# 4) Create garages feature class in WGS84
GARAGES_FC = os.path.join(OUT_GDB, "Garages_WGS84")
arcpy.management.XYTableToPoint(GARAGES_CSV, GARAGES_FC, x_field, y_field, coordinate_system=csv_sr)

# 5) Project garages into Structures CRS
STRUCTURES_SR = arcpy.Describe(STRUCTURES_FC).spatialReference
GARAGES_PROJECTED = os.path.join(OUT_GDB, "Garages")
arcpy.management.Project(GARAGES_FC, GARAGES_PROJECTED, STRUCTURES_SR)

# 6) Copy Structures into GDB
STRUCTURES_COPY = os.path.join(OUT_GDB, "Structures")
arcpy.management.CopyFeatures(STRUCTURES_FC, STRUCTURES_COPY)

# 7) Buffer garages (hardcoded to 150m for Pro Python Window)
buf_dist = "150"
GARAGES_BUFFER = os.path.join(OUT_GDB, f"Garages_Buffer_{buf_dist}m")
arcpy.analysis.Buffer(GARAGES_PROJECTED, GARAGES_BUFFER, f"{buf_dist} Meters", dissolve_option="ALL")

# 8) Intersect buffers + structures
INTERSECT_FC = os.path.join(OUT_GDB, f"Intersect_{buf_dist}m")
arcpy.analysis.Intersect([GARAGES_BUFFER, STRUCTURES_COPY], INTERSECT_FC)

# 9) Export to CSV
CSV_OUT = os.path.join(BASE_DIR, f"Intersection_{buf_dist}m.csv")
fields = [f.name for f in arcpy.ListFields(INTERSECT_FC) if f.type not in ("Geometry", "Raster")]

with open(CSV_OUT, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(fields)
    with arcpy.da.SearchCursor(INTERSECT_FC, fields) as cursor:
        for row in cursor:
            writer.writerow(row)

print("=== Done! ===")
print(f"GDB created: {OUT_GDB}")
print(f"Results table: {CSV_OUT}")
