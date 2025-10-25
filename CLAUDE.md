# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

RiverREM is a Python package for automatically generating River Relative Elevation Model (REM) visualizations from Digital Elevation Models (DEMs). The package queries OpenStreetMap for river centerlines, samples elevation along those centerlines, and interpolates elevation differences across the DEM extent to create striking visualizations of floodplain topography.

## Core Architecture

### Main Components

1. **REMMaker** (`riverrem/REMMaker.py`): Main class that orchestrates REM creation
   - Queries OSM API via osmnx to retrieve river centerline geometries
   - Rasterizes centerlines and samples DEM elevations along river paths
   - Uses KDTree-based inverse distance weighting (IDW) interpolation to estimate river elevation across entire DEM
   - Detrends the DEM by subtracting interpolated river elevations to create the REM
   - Key parameters:
     - `k`: Number of nearest neighbors for IDW interpolation (auto-estimated based on river sinuosity if not provided)
     - `interp_pts`: Maximum interpolation points (default 1000)
     - `eps`: Error tolerance for approximate KD tree query (default 0.1)
     - `workers`: Number of CPU threads for parallel processing

2. **RasterViz** (`riverrem/RasterViz.py`): Visualization class for creating DEM derivatives
   - Produces hillshade, slope, aspect, roughness, and color-relief maps
   - Uses GDAL (via Python bindings or shell commands) for raster processing
   - Blends hillshade with color-relief to create final visualizations
   - Supports logarithmic colormap scaling for REMs (emphasizes near-river elevations)

### Data Flow

1. User provides DEM raster path
2. REMMaker extracts spatial metadata (projection, extent, cell size, bounding box)
3. OSM river centerlines are queried and filtered (longest river in domain is selected)
4. Centerline is converted to points and rasterized
5. DEM elevations sampled along centerline
6. KDTree built from centerline coordinates
7. IDW interpolation spreads river elevations across DEM extent
8. REM = DEM - interpolated_river_elevation
9. RasterViz creates color-relief from REM and hillshade from original DEM
10. Final visualization blends the two products

### Key Design Decisions

- **Sinuosity-based k estimation**: More sinuous rivers require more nearest neighbors to avoid interpolation artifacts
- **Chunked processing**: Large DEMs are processed in chunks to manage memory usage (`chunk_size` parameter)
- **OSM caching**: River centerlines cached in `./.osm_cache` directory
- **Cache directory**: Intermediate products stored in `./.cache` and cleaned up automatically

## Development Commands

### Environment Setup

Using conda/mamba (recommended):
```bash
conda env create -n rem_env --file environment.yml
conda activate rem_env
```

Using pixi (recommended for this repository):
```bash
pixi install
pixi shell
```

### Quick Start with Pixi Tasks

The repository includes convenient pixi tasks for common operations:

**Generate REM from DEM:**
```bash
pixi run make-rem <path_to_dem.tif>
```

**Generate REM visualization with PNG output:**
```bash
# With defaults (topo colormap, 300 DPI)
pixi run make-viz <path_to_dem.tif>

# With custom colormap
pixi run make-viz <path_to_dem.tif> mako_r

# With custom colormap and DPI
pixi run make-viz <path_to_dem.tif> topo 600
```

### Installation

From source:
```bash
python setup.py install
```

### Running Tests

The repository includes basic test scripts rather than a full test suite:

```bash
# Test with local DEM file
python tests/test_local.py

# Test with remote DEM URL
python tests/test_url.py
```

### Command-Line Usage

REMMaker can be run as CLI tool:
```bash
python riverrem/REMMaker.py [-centerline_shp path] [-cmap mako_r] [-z 4] \
    [-blend_percent 25] [-interp_pts 1000] [-k auto] [-eps 0.1] \
    [-workers 4] /path/to/dem.tif
```

RasterViz can also be run standalone:
```bash
python riverrem/RasterViz.py viz_type [-z 1] [-alt 45] [-azim 315] \
    [-multidirectional] [-cmap topo] [-make_png] [-make_kmz] /path/to/dem.tif
```

Where `viz_type` is one of: `hillshade`, `slope`, `aspect`, `roughness`, `color-relief`, `hillshade-color`

## Key Dependencies

- **GDAL** (>=3.7, <3.9): Raster I/O and processing
- **osmnx** (>=1.3, <2.0): OpenStreetMap API queries
- **scipy**: KDTree for spatial interpolation
- **numpy** (<2.0): Array operations
- **geopandas**, **shapely** (>=2.0): Vector geometry handling
- **seaborn**, **cmocean**: Colormap support

## Common Pitfalls

1. **Numpy 2.x compatibility**: The code requires numpy <2.0 due to shapely compatibility issues. If you encounter `TypeError: ufunc 'create_collection' not supported`, ensure numpy <2.0 is installed. The pixi.toml enforces this constraint.

2. **Missing river centerlines**: If OSM doesn't have river data for the area, users must either:
   - Add centerlines to OSM at https://www.openstreetmap.org/edit
   - Provide custom centerline shapefile via `centerline_shp` parameter
   - Clear OSM cache (`./.osm_cache`) after updating OSM

3. **Interpolation artifacts**: Linear breaks in REM coloring indicate insufficient `k` value. Increase `k` or let auto-estimation handle it.

4. **River name requirement**: OSM rivers must have `name` tag or they'll be filtered out.

5. **CRS metadata**: Input DEMs must have valid coordinate system metadata or processing will fail.

6. **NoData values**: If DEM lacks NoData value, the code assumes 0 and prints a warning.

7. **Large DEM areas**: If the DEM area is much larger than the configured OSM query area, osmnx will automatically subdivide the query. This may take significant time.

## Output Files

- `{dem_name}_REM.tif`: Raw REM raster (DEM minus interpolated river elevation)
- `{dem_name}_hillshade-color.tif`: Final blended visualization
- `{dem_name}_river_pts.shp`: Sampled points along river centerline
- Optional: `.png` and `.kmz` versions for web display and Google Earth

## Package Version

Current version: 1.1.2 (per setup.py)
