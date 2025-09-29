# -*- coding: utf-8 -*-
"""
Lab 5 – Python Toolbox
Author: Your Name
GEOG 676
"""

import arcpy
import os
import csv


class Toolbox(object):
    def __init__(self):
        """Define the toolbox (name, description, tools)"""
        self.label = "Lab 5 Toolbox"
        self.alias = "lab5"
        self.tools = [GarageAnalysis]


class GarageAnalysis(object):
    def __init__(self):
        """Define the tool (name, description)."""
        self.label = "Garage Building Analysis"
        self.description = "Buffers garage points and intersects them with buildings."
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""

        # 1. Output workspace folder
        p0 = arcpy.Parameter(
            displayName="Workspace Folder",
            name="workspace_folder",
            datatype="DEFolder",
            parameterType="Required",
            direction="Input")

        # 2. Garages CSV file
        p1 = arcpy.Parameter(
            displayName="Garages CSV",
            name="garages_csv",
            datatype="DEFile",
            parameterType="Required",
            direction="Input")

        # 3. Campus GDB
        p2 = arcpy.Parameter(
            displayName="Campus GDB",
            name="campus_gdb",
            datatype="DEWorkspace",
            parameterType="Required",
            direction="Input")

        # 4. Buffer distance
        p3 = arcpy.Parameter(
            displayName="Buffer Distance (meters)",
            name="buffer_distance",
            datatype="GPLong",
            parameterType="Required",
            direction="Input")

        # 5. Derived output (the intersection result)
        p4 = arcpy.Parameter(
            displayName="Output Intersection",
            name="output_intersection",
            datatype="DEFeatureClass",
            parameterType="Derived",
            direction="Output")

        return [p0, p1, p2, p3, p4]

    def execute(self, parameters, messages):
        """Main execution code"""

        # Unpack params
        workspace = parameters[0].valueAsText
        garages_csv = parameters[1].valueAsText
        campus_gdb = parameters[2].valueAsText
        buffer_dist = parameters[3].valueAsText

        # Setup output GDB
        out_gdb = os.path.join(workspace, "Lab5.gdb")
        if not arcpy.Exists(out_gdb):
            arcpy.management.CreateFileGDB(workspace, "Lab5.gdb")

        arcpy.env.workspace = out_gdb
        arcpy.env.overwriteOutput = True

        # Locate structures feature class inside campus GDB
        structures_fc = os.path.join(campus_gdb, "Structures")

        # Detect XY fields in CSV
        with open(garages_csv, newline="", encoding="utf-8") as f:
            header = next(csv.reader(f))
        x_candidates = ["x", "lon", "longitude"]
        y_candidates = ["y", "lat", "latitude"]
        x_field = next((h for h in header if h.lower() in x_candidates), None)
        y_field = next((h for h in header if h.lower() in y_candidates), None)
        if not x_field or not y_field:
            raise RuntimeError("CSV must have X/Y or Lon/Lat fields")

        # Create garages feature class in WGS84
        sr_wgs84 = arcpy.SpatialReference(4326)
        garages_fc = os.path.join(out_gdb, "Garages_WGS84")
        arcpy.management.XYTableToPoint(garages_csv, garages_fc,
                                        x_field, y_field,
                                        coordinate_system=sr_wgs84)

        # Project garages into Structures CRS
        structures_sr = arcpy.Describe(structures_fc).spatialReference
        garages_proj = os.path.join(out_gdb, "Garages")
        arcpy.management.Project(garages_fc, garages_proj, structures_sr)

        # Copy structures
        structures_copy = os.path.join(out_gdb, "Structures")
        arcpy.management.CopyFeatures(structures_fc, structures_copy)

        # Buffer garages
        buf_fc = os.path.join(out_gdb, f"Garages_Buffer_{buffer_dist}m")
        arcpy.analysis.Buffer(garages_proj, buf_fc, f"{buffer_dist} Meters", dissolve_option="ALL")

        # Intersect buffers + structures
        inter_fc = os.path.join(out_gdb, f"Intersect_{buffer_dist}m")
        arcpy.analysis.Intersect([buf_fc, structures_copy], inter_fc)

        # Export results table as CSV
        csv_out = os.path.join(workspace, f"Intersection_{buffer_dist}m.csv")
        fields = [f.name for f in arcpy.ListFields(inter_fc) if f.type not in ("Geometry", "Raster")]
        with open(csv_out, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(fields)
            with arcpy.da.SearchCursor(inter_fc, fields) as cursor:
                for row in cursor:
                    writer.writerow(row)

        # Set derived output so ArcGIS adds the layer automatically
        parameters[4].value = inter_fc

        arcpy.AddMessage(f"Workflow complete. Outputs in: {out_gdb}")
        arcpy.AddMessage(f"CSV export: {csv_out}")
