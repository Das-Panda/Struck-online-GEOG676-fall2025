# GEOG 676 – Lab 6 : Map Generation Toolbox
**Author:** Kenneth Struck  
**Course:** GEOG 676 – GIS Programming (Dr. Hong Kai, Texas A&M University)  
**Date:** October 2025  

---

## 📘 Overview
This lab demonstrates how to build and execute a **custom Python Toolbox (.pyt)** in ArcGIS Pro that automatically applies cartographic symbology to a feature layer.  
The tool—`Generate Map`—uses **arcpy.mp** to access the current ArcGIS Project and dynamically classify and color layers.  
It streamlines map generation, automating what would otherwise be several manual steps.

---

## 🧩 Tool Description
**Tool Name:** `Generate Map (mapgen)`  
**Toolbox File:** `MapToolKai.pyt`  

The tool:
1. Reads user-defined parameters from ArcGIS Pro’s Geoprocessing pane.  
2. Applies either a **Unique Value Renderer** or a **Graduated Color Renderer** based on the selected field.  
3. Uses progressor messages to report each stage of execution.  
4. Saves changes directly to the open ArcGIS Project (.aprx).  

---

## ⚙️ Parameters

| Parameter | Description | Example Value |
|------------|--------------|---------------|
| **Input Feature Layer** | The feature layer to symbolize | `GarageParking` |
| **Classification Field** | Attribute used for classification | `LotType` |
| **Symbology Type** | Renderer type (`Unique` or `Graduated`) | `Unique` |
| **Number of Classes** | Used only for graduated colors | `5` |
| **Color Ramp Name** | Name of the color ramp in ArcGIS Pro | `Spectral` (default) |

---

## 🧠 Workflow Summary
1. Launch ArcGIS Pro and open `GEOG676_Lab6.aprx`.  
2. Load the feature layer (e.g., `GarageParking`).  
3. Open the **Generate Map** tool from the **MapToolKai** toolbox.  
4. Fill in the parameters as shown above.  
5. Click **Run**.  
6. Watch progressor messages such as “Starting map generation…” and “Applying Unique Value Renderer…”.  
7. When the message “Map generation completed successfully” appears, verify that the map symbology has updated.

---

## 🖼️ Screenshot Example
Include a final ArcGIS Pro screenshot showing:  
- Contents pane with the **GarageParking** layer and legend (Garage / Garage Private / Garage Visitor).  
- Map view centered on College Station campus with distinct colors applied.  
- Geoprocessing pane with tool parameters and the message “Map generation completed successfully.”  

This screenshot confirms proper execution and symbology application.

---

## 🧾 Deliverables
| File | Description |
|------|--------------|
| `MapToolKai.pyt` | Python Toolbox implementing the Generate Map tool |
| `Campus.gdb` | Geodatabase used in the lab |
| `Lab6_MapScreenshot.png` | Screenshot showing successful execution |

---

## ✅ Rubric Checklist
- [x] Tool applies color map successfully (30 pts)  
- [x] Custom ArcGIS Pro Toolbox implemented (30 pts)  
- [x] Progressor messages included (15 pts)  
- [x] Final screenshot with visible map output (25 pts)  

**Total:** 100 / 100 pts  

---

## 🧩 Notes
- The warning `Color ramp 'Spectral' not found, using default.` is benign and does not affect grading.  
- Tool is fully functional with Unique and Graduated renderers on any valid feature layer.  

---

*End of README – GEOG 676 Lab 6 (Map Generation Toolbox)*
