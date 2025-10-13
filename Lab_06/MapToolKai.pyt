# ==============================================================
# GEOG676 - Lab 6: Map Generation Toolbox
# Author: Kenneth Struck
# Instructor: Dr. Hong Kai
# Description:
#     This Python Toolbox creates either a Unique Value or Graduated
#     Color map in ArcGIS Pro using arcpy.mp. It includes a progressor
#     that updates the user on each processing step.
# ==============================================================

import arcpy
import time

class Toolbox(object):
    def __init__(self):
        self.label = "Map Generation Toolbox"
        self.alias = "mapgen"
        self.tools = [GenerateMap]


class GenerateMap(object):
    def __init__(self):
        self.label = "Generate Map"
        self.description = "Generates a Unique Value or Graduated Color map using arcpy.mp."
        self.canRunInBackground = False

    def getParameterInfo(self):
        params = []

        # 0 - Input feature layer
        p0 = arcpy.Parameter(
            displayName="Input Feature Layer",
            name="in_layer",
            datatype="GPFeatureLayer",
            parameterType="Required",
            direction="Input"
        )

        # 1 - Classification field
        p1 = arcpy.Parameter(
            displayName="Classification Field",
            name="class_field",
            datatype="Field",
            parameterType="Required",
            direction="Input"
        )
        p1.parameterDependencies = ["in_layer"]

        # 2 - Symbology type
        p2 = arcpy.Parameter(
            displayName="Symbology Type",
            name="sym_type",
            datatype="GPString",
            parameterType="Required",
            direction="Input"
        )
        p2.filter.list = ["Unique", "Graduated"]
        p2.value = "Unique"

        # 3 - Number of classes
        p3 = arcpy.Parameter(
            displayName="Number of Classes (Graduated only)",
            name="n_classes",
            datatype="GPLong",
            parameterType="Optional",
            direction="Input"
        )
        p3.value = 5

        # 4 - Color ramp
        p4 = arcpy.Parameter(
            displayName="Color Ramp Name",
            name="color_ramp",
            datatype="GPString",
            parameterType="Optional",
            direction="Input"
        )
        p4.value = "Spectral"

        params = [p0, p1, p2, p3, p4]
        return params


    def execute(self, parameters, messages):
        in_layer = parameters[0].valueAsText
        class_field = parameters[1].valueAsText
        sym_type = parameters[2].valueAsText
        n_classes = parameters[3].value
        color_ramp_name = parameters[4].valueAsText

        arcpy.SetProgressor("step", "Initializing map generation...", 0, 100, 20)
        arcpy.AddMessage("Starting map generation process...")

        aprx = arcpy.mp.ArcGISProject("CURRENT")
        m = aprx.listMaps()[0]

        # --- Robust layer lookup fix ---
        # ArcGIS sometimes uses full paths or altered names for layers
        layer_name = in_layer.split("\\")[-1].split("/")[-1]  # strip path
        layer_name = layer_name.split(".")[-1] if "." in layer_name else layer_name
        lyr_list = [
            lyr for lyr in m.listLayers()
            if layer_name.lower() in lyr.name.lower()
        ]

        if not lyr_list:
            all_layers = [lyr.name for lyr in m.listLayers()]
            raise arcpy.ExecuteError(
                f"Layer '{layer_name}' not found in the current map.\n"
                f"Layers available: {', '.join(all_layers)}.\n"
                f"Make sure '{layer_name}' is added and visible in the Contents pane."
            )

        lyr = lyr_list[0]
        sym = lyr.symbology

        # --- Apply symbology ---
        arcpy.SetProgressorLabel("Applying renderer type...")
        arcpy.SetProgressorPosition(40)
        time.sleep(0.3)

        if sym_type == "Unique":
            sym.updateRenderer("UniqueValueRenderer")
            sym.renderer.fields = [class_field]

            ramps = aprx.listColorRamps(color_ramp_name)
            if ramps:
                sym.renderer.colorRamp = ramps[0]
            else:
                arcpy.AddWarning(f"Color ramp '{color_ramp_name}' not found, using default.")
            arcpy.AddMessage(f"Applied Unique Value Renderer using {class_field}")

        elif sym_type == "Graduated":
            sym.updateRenderer("GraduatedColorsRenderer")
            sym.renderer.classificationField = class_field
            sym.renderer.breakCount = n_classes or 5

            ramps = aprx.listColorRamps(color_ramp_name)
            if ramps:
                sym.renderer.colorRamp = ramps[0]
            else:
                arcpy.AddWarning(f"Color ramp '{color_ramp_name}' not found, using default.")
            arcpy.AddMessage(f"Applied Graduated Color Renderer using {class_field}")

        else:
            raise arcpy.ExecuteError(f"Invalid symbology type '{sym_type}'.")

        arcpy.SetProgressorLabel("Finalizing symbology...")
        arcpy.SetProgressorPosition(70)
        time.sleep(0.3)

        lyr.symbology = sym

        # --- Save project ---
        try:
            m.clearSelection()
            aprx.save()
            arcpy.AddMessage("Symbology applied successfully and project saved.")
        except Exception as e:
            arcpy.AddWarning(f"Project save skipped or failed: {e}")

        arcpy.SetProgressorLabel("Finishing up...")
        arcpy.SetProgressorPosition(100)
        arcpy.ResetProgressor()
        arcpy.AddMessage("Map generation completed successfully.")
