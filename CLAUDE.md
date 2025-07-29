# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is an IT research repository focused on geographic information systems (GIS), spatial data analysis, and urban growth modeling. The repository contains:

1. **Taiwanese Geographic Data**: Large-scale topographic and land use datasets from Taiwan
2. **SLEUTH Urban Growth Model**: A cellular automata-based urban growth simulation model
3. **OSM Data Processing**: OpenStreetMap data for Taiwan road networks
4. **GIS Analysis Tools**: Various spatial data processing utilities

## Key Components

### SLEUTH Urban Growth Model (`SLEUTH3.0beta_p01_linux/`)
- **Main executable**: Built by compiling C source files into `grow` executable
- **Build system**: Uses Make with `Makefile` (configured for gcc-14)
- **Input data**: Located in `Input/` directory (GIF format raster data)
- **Scenarios**: Configuration files in `Scenarios/` directory
- **Dependencies**: Requires GD graphics library (included in `GD/` subdirectory)

### Taiwan Geographic Datasets
- **Topographic data**: 25,000:1 and 100,000:1 scale digital elevation models and vector data
- **Land use data**: Historical land cover data from 1904-2015 in NetCDF format
- **Format**: Primarily shapefiles (.shp), NetCDF (.nc), and GRD formats

### OSM Road Network Data
- **Files**: `taiwan-latest.osm.pbf`, `road_taiwan.osm`, `road_taiwan.geojson`  
- **Tools**: `osmconvert` executable for format conversion

## Build Commands

### SLEUTH Model
```bash
cd SLEUTH3.0beta_p01_linux
make clean_all  # Clean all build artifacts
make depend     # Generate dependencies
make            # Build the grow executable
```

### Running SLEUTH
```bash
cd SLEUTH3.0beta_p01_linux
./grow scenario_file_name
```

## Data Processing Workflows

### Land Use Data Analysis
- NetCDF files contain Plant Functional Type (PFT) classifications
- Use the README.txt in `land_use_data/` for classification codes:
  - 01: Forest
  - 02: Grassland  
  - 04: Agriculture
  - 08: Built-up
  - 13: Inland water
  - 26: Bare soil

### OSM Data Processing
- Use `osmconvert` to convert between .osm.pbf and .osm formats
- Road network data available in multiple formats for different analysis needs

## Architecture Notes

- **SLEUTH**: Classic C-based cellular automata model with modular object-oriented design
- **Data**: Multi-scale geographic datasets requiring GIS software for visualization
- **Processing**: Designed for Linux environments with gcc compilation
- **Memory**: SLEUTH requires significant memory for large urban areas - ensure WRITE_MEMORY_MAP=yes in scenario files

## Important Configuration

- SLEUTH requires scenario files to have `WRITE_MEMORY_MAP=yes` for Linux compatibility
- GD graphics library is included and configured for the build system
- All file paths in scenario files should use absolute paths