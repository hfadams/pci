"""
Script for pairing lake and solar radiation stations in QGIS

Jane Ye
"""

from qgis.core import QgsDistanceArea
from qgis import processing

# Set SSR and lake input layers for joining
lake_layer_str = 'incominglakes'
ssr_layer_str = 'ssr_stns'

# Run join attributes by nearest
joinnearest_out = processing.run("native:joinbynearest",
                                 {'INPUT': lake_layer_str,
                                  'INPUT_2': ssr_layer_str,
                                  'FIELDS_TO_COPY': 'Station na;ID;ID Type;Latitude;Longitude',
                                  'DISCARD_NONMATCHING': True,
                                  'PREFIX': 'SSR',
                                  'NEIGHBORS': 1,
                                  'MAX_DISTANCE': 3,
                                  'OUTPUT': r'../../data/SSRLakesPairedML_3deg_210718.shp'}
                                 )

joined_layer = iface.addVectorLayer(joinnearest_out['OUTPUT'], '', 'ogr')

# Calculate distance between points in output layer
# Initiate data provider class object to use "add attribute" class function
pv = joined_layer.dataProvider()
pv.addAttributes([QgsField('GeoDistKm', QVariant.Double)])
joined_layer.updateFields()

# Initiate distance calculator class object to use "measure line" class function
d = QgsDistanceArea()
d.setEllipsoid('WGS84')

# Define function to call measureLine and get distance
def get_distance(lon1, lat1, lon2, lat2):
    point1 = QgsPointXY(lon1, lat1)
    point2 = QgsPointXY(lon2, lat2)
    distance = d.measureLine([point1, point2])
    return (distance / 1000)

# Populate new field
with edit(joined_layer):
    for f in joined_layer.getFeatures():
        f.setAttribute(f.fieldNameIndex('GeoDistKm'),
                       get_distance(f['long'], f['lat'], f['SSRLongitu'], f['SSRLatitud']))
        joined_layer.updateFeature(f)
