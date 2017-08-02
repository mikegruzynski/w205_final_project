drop table seattle_crime_raw;

create table seattle_crime_raw (
 cad_cdw_id                  varchar(100),
 cad_event_number            bigint,
 general_offense_number      varchar(100),
 event_clearance_code        varchar(100),
 event_clearance_description varchar(500),
 event_clearance_subgroup    varchar(100),
 event_clearance_group          varchar(100),
 event_clearance_date        timestamp,
  hundred_block_location          varchar(100),
 district_sector             varchar(100),
 zonebeat                   varchar(100),
 census_tract                varchar(100),
 latitude                    float,
 longitude                   float,
 incident_location                     varchar(100),
 initial_type_description           varchar(500),
 initial_type_subgroup             varchar(100),
 initial_type_group                    varchar(100),
 at_scene_time                         timestamp);

COPY seattle_crime_raw FROM '/tmp/SeattleCrimeData.csv' CSV HEADER QUOTE '"';
