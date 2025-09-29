# Struck-online-GEOG676-fall2025

Lab 5 – Python Toolbox in ArcGIS Pro

Course: GEOG 676
Author: Kenneth Struck
Date: September 2025

Overview

This lab converts the workflow from Lab 4 into a Python Toolbox (.pyt) for ArcGIS Pro. The tool, called Garage Building Analysis, buffers parking garage locations and determines which campus buildings fall within the specified buffer distance.

The toolbox allows users to supply input parameters directly through ArcGIS Pro’s geoprocessing interface, making the analysis reusable and interactive.

⚙️ Tool Parameters

When you load Lab5.pyt into ArcGIS Pro, the Garage Building Analysis tool appears with the following parameters:

Workspace Folder – A folder where the output geodatabase (Lab5.gdb) will be created.

Garages CSV – Input CSV file with X/Y (longitude/latitude) coordinates of parking garages.

Campus GDB – Input file geodatabase containing the Structures feature class (buildings).

Buffer Distance (meters) – Distance around each garage to search for nearby buildings.

Output Intersection (derived) – Feature class of buildings within the buffer zones (added to the map automatically).

Workflow Steps

The tool performs the following operations:

Creates Lab5.gdb in the workspace folder.

Reads garage coordinates from the CSV file.

Creates point features in WGS84 and projects them into the campus spatial reference.

Buffers garage points using the user-specified distance.

Copies the Structures feature class from the campus GDB.

Intersects the buffers with campus buildings to find nearby structures.

Exports the intersection results both as a feature class and a CSV file.

Adds the intersection layer to the current ArcGIS Pro map.

Outputs

Geodatabase (Lab5.gdb) containing:

Garages (projected garage points)

Garages_Buffer_<distance>m (buffer polygons)

Structures (copied buildings from campus GDB)

Intersect_<distance>m (intersection result)

CSV file summarizing intersection results, written to the workspace folder.

How to Run

Clone or download this repo.

In ArcGIS Pro, open the Catalog pane → right-click Toolboxes → Add Toolbox → browse to Lab5.pyt.

Open the Garage Building Analysis tool.

Fill in the parameters:

Workspace folder (e.g., GEOG676_Lab5)

Garage CSV (e.g., garages.csv)

Campus GDB (e.g., Campus.gdb)

Buffer distance (e.g., 150)

Run the tool.

View results in the map and open the exported CSV file for tabular results.
