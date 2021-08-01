"""
Script for extracting lake digital elevation model (DEM)

Jane Ye
"""

from qgis import processing

# Set DEM and lake input layers for joining
lake_layer_str = 'SSRLakesPairedML_1deg_210718'
DEM_layer_str = 'DEM_CanadaEuropeAsia_15arcsec'
hydrolakes_layer_str = 'HydroLAKES_polys_v10'

# define output path
output_path = r'C:\Users\janey\Documents\11. S20\Ecohydro_Solar Radiation Lakes\GIS\Shapefiles\SSRLakesDEMHydrolakesML_210718\SSRLakes_DEMHYDRO_ML_1deg_210718.shp'

# Run sample raster values to get DEM values at points in the lake layer
DEMlakes_out = processing.run("qgis:rastersampling",
                              {'INPUT': lake_layer_str,
                               'RASTERCOPY': DEM_layer_str,
                               'COLUMN_PREFIX': 'DEM',
                               'OUTPUT': 'TEMPORARY_OUTPUT'
                               })


HYDROlakes_out = processing.run("qgis:joinattributesbylocation",
                                {'INPUT': DEMlakes_out['OUTPUT'],
                                 'JOIN': hydrolakes_layer_str,
                                 'JOIN_FIELDS': ['Lake_area', 'Vol_total', 'Depth_avg'],
                                 'METHOD': 0,
                                 'PREFIX': 'HYDRO',
                                 'OUTPUT': output_path
                                 })
