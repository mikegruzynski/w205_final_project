#Code adapted from https://glenbambrick.com/2016/01/09/csv-to-shapefile-with-pyshp/ and
#https://macwright.org/2012/10/31/gis-with-python-shapely-fiona.html

#Importing necessary libraries
import shapefile, csv, urllib, fiona
from pyproj import Proj, transform
from shapely.geometry import Point, mapping, shape


#Function to assign spatial projection
def get_prj(epsg_code):
    wkt = urllib.urlopen("http://spatialreference.org/ref/epsg/{0}/prettywkt/".format(epsg_code))
    remove_spaces = wkt.read().replace(" ","")
    output = remove_spaces.replace("\n", "")
    return output

#Function to compute circular spatial buffer around points
def buffer(shp_name, dist):
    with fiona.open("./shp/" + shp_name + ".shp", "r") as input:
        schema = input.schema.copy()
        schema['geometry'] = 'Polygon'
        #keys = schema['properties'].keys()
        #keystring = ''
        #for key in keys:
            #keystring = keystring + "'" + key + "'" + ": point['properties'][" + "'" + key + "'" + "], "
        with fiona.open("./shp/" + shp_name + "_buffer.shp", 'w', 'ESRI Shapefile', schema) as output:
            print 'Buffering ' + shp_name + '...'
            buff_counter = 1
            for i in input:
                output.write({
                'properties': i['properties'],
                'geometry': mapping(shape(i['geometry']).buffer(dist))
                })
                buff_counter += 1
            print 'Buffering complete - ' + str(buff_counter) + ' features added to shapefile.'
    print 'Projecting shapefile...'
    buff_prj = open('./shp/' + shp_name + '_buffer.prj', "w")
    buff_prj.write(get_prj("2285"))
    buff_prj.close()
    print 'Projection complete.'

#Create Point shapefile for transit stops
stops_shp = shapefile.Writer(shapefile.POINT)
stops_shp.autoBalance = 1

#Establish transit point shapefile fields and data types
stops_shp.field("STOP_ID", "C")
stops_shp.field("STOP_NAME", "C")
stops_shp.field("STOP_LAT", "C")
stops_shp.field("STOP_LON", "C")
stops_shp.field("ZONE_ID", "C")

#Create Point shapefile for crime incidents
crime_shp = shapefile.Writer(shapefile.POINT)
crime_shp.autoBalance = 1

#Establish crime point shapefile fields and data types
crime_shp.field("CAD_ID", "C")
crime_shp.field("CAD_EVENT", "C")
crime_shp.field("OFFENSE_NUM", "C")
crime_shp.field("EVENT_DESC", "C")
crime_shp.field("EVENT_SUBGROUP", "C")
crime_shp.field("EVENT_GROUP", "C")
crime_shp.field("EVENT_DATE", "C")
crime_shp.field("LATITUDE", "C")
crime_shp.field("LONGITUDE", "C")

#Counters for checking the total number of records
transit_counter = 1
crime_counter = 1

#Data is provided in lat/long coordinates, but it must be reprojected into a local
#projection system to calculate on-the-ground distances and buffers.
#Lat/long can be represented by the WGS84 coordinate system (EPSG code 4326).
#For this analysis, we will use the NAD83 Washington State Plane (EPSG code 2285).
prj1 = Proj(init='epsg:4326')
prj2 = Proj(init='epsg:2285')

#Access transit stop source data in csv format, skipping the headers
with open('./src/stops.csv', 'rb') as stop_file:
    stop_read = csv.reader(stop_file, delimiter = ',')
    next(stop_read, None)

    #Loop through the csv data and read the attribute data to variables
    for row in stop_read:
        stop_id = row[0]
        stop_name = row[2]
        stop_lat = row[4]
        stop_lon = row[5]
        zone_id = row[6]

        #Reproject lat/long coordinates into WA State Plane
        x_meters, y_meters = transform(prj1, prj2, stop_lon, stop_lat)
        x_ft = x_meters * 3.28084
        y_ft = y_meters * 3.28084

        #Establish spatial location of point geometry and add attribute data to shapefile
        stops_shp.point(float(x_ft), float(y_ft))
        stops_shp.record(stop_id, stop_name, stop_lat, stop_lon, zone_id)

        transit_counter += 1

    print str(transit_counter) + " features added to transit point shapefile."

#Save transit points shapefile
stops_shp.save("./shp/transit_stops")

#Access crime source data in csv format, skipping the headers
with open('./src/crimes_test.csv', 'rb') as crime_file:
    crime_read = csv.reader(crime_file, delimiter = ',')
    next(crime_read, None)

    #Loop through the csv data and read the attribute data to variables
    for row in crime_read:
        cad_id = row[0]
        cad_event = row[1]
        offense_num = row[2]
        event_desc = row[4]
        event_subgrp = row[5]
        event_grp = row[6]
        event_date = row[7]
        crime_lon = row[12]
        crime_lat = row[13]

        #Reproject lat/long coordinates into WA State Plane
        x_meters, y_meters = transform(prj1, prj2, crime_lon, crime_lat)
        x_ft = x_meters * 3.28084
        y_ft = y_meters * 3.28084

        #Establish spatial location of point geometry and add attribute data to shapefile
        crime_shp.point(float(x_ft), float(y_ft))
        crime_shp.record(cad_id, cad_event, offense_num, event_desc, event_subgrp, event_grp, event_date, crime_lat, crime_lon)

        crime_counter += 1

    print str(crime_counter) + " features added to crime point shapefile."

#Save shapefile
crime_shp.save("./shp/crime_incidents")


#Create spatial projection files
transit_prj = open("./shp/transit_stops.prj", "w")
transit_prj.write(get_prj("2285"))
transit_prj.close()

crime_prj = open("./shp/crime_incidents.prj", "w")
crime_prj.write(get_prj("2285"))
crime_prj.close()

#Buffer transit stops for later spatial analysis
buffer('transit_stops', 250)
