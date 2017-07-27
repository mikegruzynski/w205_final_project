#Code adapted from https://glenbambrick.com/2016/01/09/csv-to-shapefile-with-pyshp/

#Importing necessary libraries
import shapefile, csv, urllib
from pyproj import Proj, transform

#Function to assign spatial projection
def get_prj(epsg_code):
    wkt = urllib.urlopen("http://spatialreference.org/ref/epsg/{0}/prettywkt/".format(epsg_code))
    remove_spaces = wkt.read().replace(" ","")
    output = remove_spaces.replace("\n", "")
    return output

#Create Point shapefile for transit stops
stops_shp = shapefile.Writer(shapefile.POINT)
stops_shp.autoBalance = 1

#Establish shapefile fields and data types
stops_shp.field("STOP_ID", "C")
stops_shp.field("STOP_NAME", "C")
stops_shp.field("STOP_LAT", "C")
stops_shp.field("STOP_LON", "C")
stops_shp.field("ZONE_ID", "C")

#Counter for checking the total number of records
counter = 1

#Data is provided in lat/long coordinates, but it must be reprojected into a local
#projection system to calculate on-the-ground distances and buffers.
#Lat/long can be represented by the WGS84 coordinate system (EPSG code 4326).
#For this analysis, we will use the NAD83 Washington State Plane (EPSG code 2285).
prj1 = Proj(init='epsg:4326')
prj2 = Proj(init='epsg:2285')


#Access source data in csv format, skipping the headers
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

        counter += 1

    print str(counter) + " features added to shapefile."

#Save shapefile
stops_shp.save("./shp/transit_stops")

#Create spatial projection file
prj = open("./shp/transit_stops.prj", "w")
prj.write(get_prj("2285"))
prj.close()
