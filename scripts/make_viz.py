#!/usr/bin/env python
"""
Script to generate REM visualization with PNG output
Usage: pixi run make-viz <path_to_dem.tif> [colormap] [dpi]
Default colormap: topo
Default DPI: 300
"""
import sys
import os
from riverrem.REMMaker import REMMaker
from PIL import Image

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: pixi run make-viz <path_to_dem.tif> [colormap] [dpi]")
        print("Example: pixi run make-viz dem.tif topo 300")
        sys.exit(1)

    dem_path = sys.argv[1]
    cmap = sys.argv[2] if len(sys.argv) > 2 else 'topo'
    dpi = int(sys.argv[3]) if len(sys.argv) > 3 else 300

    print(f"Generating REM visualization from: {dem_path}")
    print(f"Colormap: {cmap}")
    print(f"DPI: {dpi}")

    rem_maker = REMMaker(dem=dem_path, out_dir='./')
    viz_path = rem_maker.make_rem_viz(cmap=cmap, make_png=True, z=4, blend_percent=25)

    # Set DPI metadata for PNG output
    dem_name = os.path.basename(dem_path).split('.')[0]
    png_path = f"./{dem_name}_hillshade-color.png"

    if os.path.exists(png_path):
        # Open and resave with DPI metadata
        img = Image.open(png_path)
        img.save(png_path, dpi=(dpi, dpi))
        print(f"\n✓ Visualization created: {viz_path}")
        print(f"✓ PNG created: {png_path} (DPI: {dpi})")
    else:
        print(f"\n✓ Visualization created: {viz_path}")
        print(f"Note: PNG not found at expected path: {png_path}")
