-- This script loads the Seattle.gov crime data as a raw table int hive

-- If seattle_crime_raw already exists, drop table so it can be refreshed.

DROP TABLE seattle_crime_raw;

-- Refresh the seattle_crime_raw data with latest file
CREATE EXTERNAL TABLE seattle_crime_raw
(at_scene_time               timestamp,
 cad_cdw_id                  int,
 cad_event_number            int,
 census_tract                string,
 district_sector             string,
 event_clearance_code        int,
 event_clearance_date        timestamp,
 event_clearance_description string,
 event_clearance_group       string,
 event_clearance_subgroup    string,
 general_offense_number      int,
 hundred_block_location      string,
 incident_location           string,
 initial_type_description    string,
 initial_type_group          string,
 latitude                    float,
 longitude                   float,
 zonebeat                    string)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES (
 "separatorChar" = ",",
 "quoteChar" = '"',
 "escapeChar" = '\\'
)
STORED AS TEXTFILE
LOCATION '/user/w205/final_project/crime_data';
