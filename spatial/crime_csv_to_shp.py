#Code adapted from https://glenbambrick.com/2016/01/09/csv-to-shapefile-with-pyshp/

#Importing necessary libraries
import shapefile, csv, urllib

#Function to assign spatial projection
def get_prj(epsg_code):
    wkt = urllib.urlopen("http://spatialreference.org/ref/epsg/{0}/prettywkt/".format(epsg_code))
    remove_spaces = wkt.read().replace(" ","")
    output = remove_spaces.replace("\n", "")
    return output

#Create Point shapefile for transit stops
crime_shp = shapefile.Writer(shapefile.POINT)
crime_shp.autoBalance = 1

#Establish shapefile fields and data types
crime_shp.field("CAD_ID", "C")
crime_shp.field("CAD_EVENT", "C")
crime_shp.field("OFFENSE_NUM", "C")
crime_shp.field("EVENT_DESC", "C")
crime_shp.field("EVENT_SUBGROUP", "C")
crime_shp.field("EVENT_GROUP", "C")
crime_shp.field("EVENT_DATE", "C")
crime_shp.field("LATITUDE", "C")
crime_shp.field("LONGITUDE", "C")

#Counter for checking the total number of records
counter = 1

#Access source data in csv format, skipping the headers
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

        #Establish spatial location of point geometry and add attribute data to shapefile
        crime_shp.point(float(crime_lon), float(crime_lat))
        crime_shp.record(cad_id, cad_event, offense_num, event_desc, event_subgrp, event_grp, event_date, crime_lat, crime_lon)

        counter += 1

    print str(counter) + " features added to shapefile."

#Save shapefile
crime_shp.save("./shp/crime_incidents")

#Create spatial projection file
prj = open("./shp/crime_incidents.prj", "w")
prj.write(get_prj("4326"))
prj.close()
