# read the shapefiles
import fiona
from shapely.geometry import shape
polygons = [pol for pol in fiona.open('./shp/transit_stops_buffer.shp')]
points = [pt for pt in fiona.open('./shp/crime_incidents.shp')]

#Create the R-tree index and store the features in it (bounding box)
from rtree import index
idx = index.Index()
for pos, poly in enumerate(polygons):
    idx.insert(pos, shape(poly['geometry']).bounds)

#Iterate through the points
for i,pt in enumerate(points):
    point = shape(pt['geometry'])
    # iterate through spatial index
    for j in idx.intersection(point.coords[0]):
        if point.within(shape(polygons[j]['geometry'])):
            points[i]['properties']['STOP_ID'] = polygons[j]['properties']['STOP_ID']

schema = fiona.open('./shp/crime_incidents.shp').schema
with fiona.open('./shp/spjoin.shp', 'w', 'ESRI Shapefile', schema) as output:
    for i in points:
        if points[i]['properties']['STOP_ID'] != u'None':
            output.write(i)
