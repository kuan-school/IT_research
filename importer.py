import os

# --- 1. CONFIGURATION ---
# IMPORTANT: Replace the items in this list with your actual folder names.
location_codes = ['96232NE','96232SW','96232SE','96221NE','96221NW','97233NW','97233SW','97233SE','97224NW'] 

# IMPORTANT: Set the ABSOLUTE path to the directory containing your '112_terrain_data' and '113_terrain_data' folders.
# Example for macOS: "/Users/your_username/Documents/GIS_Data"
# DO NOT use a relative path like './'.
base_project_path = "/Users/morris/IT_research" 
# --- END OF CONFIGURATION ---


# --- 2. SCRIPT LOGIC (No changes needed below) ---
# Get the current QGIS project instance
project = QgsProject.instance()

# List of the main year directories to check
year_dirs = ['112_terrain_data', '113_terrain_data']

print("--- Starting Script ---")

# Loop through each main year directory
for year_dir in year_dirs:
    # Loop through each location code you provided
    for code in location_codes:
        # Construct the full, absolute path to the shapefile
        shp_path = os.path.join(
            base_project_path,
            year_dir,
            'images',
            code,
            '向量25K', # This folder name contains Chinese characters
            'ContourL.shp'
        )

        # Check if the shapefile actually exists at that path
        if os.path.exists(shp_path):
            # Create a unique and descriptive layer name, e.g., "112_Contour_9522"
            layer_name = f"{year_dir.split('_')[0]}_Contour_{code}"

            # Create the vector layer object
            layer = QgsVectorLayer(shp_path, layer_name, "ogr")

            # Check if the layer was loaded successfully
            if not layer.isValid():
                print(f"❌ Layer failed to load: {shp_path}")
            else:
                # Add the valid layer to the current QGIS project
                project.addMapLayer(layer)
                print(f"✅ Successfully added layer: {layer_name}")
        else:
            # Inform the user if a specific file was not found
            print(f"⚠️ File not found, skipping: {shp_path}")

print("--- Script Finished ---")