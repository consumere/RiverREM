#!/usr/bin/env python
"""
Script to generate REM from DEM via pixi task
Usage: pixi run make-rem <path_to_dem.tif>
"""
import sys
from riverrem.REMMaker import REMMaker

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: pixi run make-rem <path_to_dem.tif>")
        sys.exit(1)

    dem_path = sys.argv[1]
    print(f"Generating REM from: {dem_path}")

    rem_maker = REMMaker(dem=dem_path, out_dir='./')
    rem_path = rem_maker.make_rem()

    print(f"\n✓ REM created: {rem_path}")
