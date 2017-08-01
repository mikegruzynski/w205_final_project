from pyspark.sql.types import *
import csv

# Creates an RDD based on the .csv of crime data, removes header line
crime_data_raw = sc.textFile("crime_data/SeattleCrimeData.csv")
crime_data_header = crime_data_raw.filter(lambda x: "Longitude" in x)
crime_data_noheader = crime_data_raw.subtract(crime_data_header)
crime_data_rdd = crime_data_noheader.mapPartitions(lambda x: csv.reader(x))

# Creates a schema object that contains the column names for the csv
crime_schema_string = "cad_cdw_id,cad_event_number,general_offense_number,event_clearance_code,event_clearance_description,event_clearance_subgroup,event_clearance_group,event_clearance_date,hundred_block_location,district_sector,zone_beat,census_tract,longitude,latitude,incident_location,initial_type_description,initial_type_subgroup,initial_type_group,at_scene_time"
fields = [StructField(field_name, StringType(), True) for field_name in crime_schema_string.split(',')]
schema = StructType(fields)

# Creates a table, attaches schema
crime_data = sqlContext.createDataFrame(crime_data_rdd, schema)
crime_data.registerTempTable("crime_data_table")

# Creates a dataframe with false, fraud calls removed. Adds additional columns for filtering
crime_data_df = sqlContext.sql("SELECT cad_event_number, event_clearance_code, general_offense_number, event_clearance_description, latitude, longitude, substr(nvl(at_scene_time, event_clearance_date), 7, 4)    AS at_scene_year, substr(nvl(at_scene_time, event_clearance_date), 1, 2)    AS at_scene_month, substr(nvl(at_scene_time, event_clearance_date), 4, 2) AS at_scene_day, substr(nvl(at_scene_time, event_clearance_date), 13)      AS at_scene_time, substr(nvl(at_scene_time, event_clearance_date), -2, 2)   AS at_scene_am_pm, nvl(at_scene_time, event_clearance_date)                  AS at_scene_date_time, substr(nvl(event_clearance_date, at_scene_time), 7, 4)    AS event_clearance_year, substr(nvl(event_clearance_date, at_scene_time), 1, 2) AS event_clearance_month, substr(nvl(event_clearance_date, at_scene_time), 4, 2)    AS event_clearance_day, substr(nvl(event_clearance_date, at_scene_time), 13)      AS event_clearance_time, substr(nvl(event_clearance_date, at_scene_time), -2, 2)   AS event_clearance_am_pm, nvl(event_clearance_date, at_scene_time)                  AS event_clearance_date_time, IF(event_clearance_group IN ('THREATS, HARASSMENT', 'ROBBERY', 'ASSAULTS', 'DRIVE BY (NO INJURY)'), TRUE, FALSE) AS is_violent, CASE WHEN (event_clearance_group IN ('THREATS, HARASSMENT', 'ROBBERY', 'ASSAULTS', 'DRIVE BY (NO INJURY', 'HOMICIDE')) THEN 3 WHEN (event_clearance_group  IN ('AUTO THEFTS', 'BURGLARY', 'DISTURBANCES','MENTAL HEALTH', 'OTHER PROPERTY', 'BURGLARY','PERSON DOWN/INJURY', 'NARCOTICS COMPLAINTS','DISTURBANCES', 'LEWD CONDUCT', 'PROSTITUTION','WEAPONS CALLS', 'RECKLESS BURNING', 'HARBOR CALLS','OTHER VICE', 'VICE CALLS') AND event_clearance_subgroup NOT IN ('AUTO RECOVERIES')) THEN 1 ELSE 0 END AS risk_factor, IF(event_clearance_group IN ('FRAUD CALLS', 'FALSE ALARMS'), TRUE, FALSE) AS is_false_alarm, event_clearance_group AS event_clearance_group, event_clearance_subgroup   FROM crime_data_table where event_clearance_group NOT IN ('FRAUD CALLS', 'FALSE ALARMS')")

