#act "/Users/apfel/micromamba/envs/rem_env"

#bash
#fn="/Users/apfel/pCloud Drive/wasim/merit_v2/saale50_Elevation.tif"
#gdal_translate -of GTiff -a_srs EPSG:25832 "$fn" output_dem_epsg25832.tif
#gdal_translate -of GTiff -a_srs EPSG:4326 "$fn" output_dem.tif

#%%
#fn="/Users/apfel/pCloud Drive/wasim/rcm200/v12/rcm.tif"

#fn="/Users/apfel/pCloud Drive/wasim/rcm200/v4/dhk.tif"
#fn="/Users/apfel/pCloud Drive/wasim/merit_v2/filled_dem.tif"
#fn="/Users/apfel/pCloud Drive/wasim/brend/in3/fab.tif"
#fn="/Users/apfel/pCloud Drive/pCloud Backup/cris-macbookpro62/Dokumente/merit_v3/dem.tif"

fn="output_dem.tif"

fn="swissalti3d_2019_2640-1167_0.5_2056_5728.tif"

from riverrem.REMMaker import REMMaker
# provide the DEM file path and desired output directory
rem_maker = REMMaker(dem=fn,out_dir="out")
# create an REM
rem_maker.make_rem()
# create an REM visualization with the given colormap
rem_maker.make_rem_viz(cmap='topo')
