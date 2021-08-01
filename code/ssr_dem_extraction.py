"""
Script to extract digital elevation model for ssr stations

Jane Ye
"""

from qgis import processing

# Set DEM and lake input layers for joining
SSR_layer_str = 'SSRLakes_DEMHYDRO_ML_3deg_210718_ssrpoints'
DEM_layer_str = 'DEM_CanadaEuropeAsia_15arcsec'

# Run sample raster values to get DEM values at points in the lake layer
DEMSSR_out = processing.run("qgis:rastersampling",
                            {'INPUT': SSR_layer_str,
                             'RASTERCOPY': DEM_layer_str,
                             'COLUMN_PREFIX': 'SSRDEM',
                             'OUTPUT': r'C:\Users\janey\Documents\11. S20\Ecohydro_Solar Radiation Lakes\GIS\Shapefiles\SSRLakesML_210718\SSRLakesML_3deg_210718.shp'
                             })

