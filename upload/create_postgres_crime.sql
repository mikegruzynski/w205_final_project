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

drop table seattle_crime;

CREATE TABLE seattle_crime
        AS
        SELECT
          cad_cdw_id,
          cad_event_number,
          census_tract,
          district_sector,
          event_clearance_code,
          general_offense_number,
          event_clearance_description,
          hundred_block_location,
          incident_location,
          initial_type_description,
          coalesce(initial_type_group, event_clearance_group)            AS initial_type_group,
          latitude,
          longitude,
          zonebeat,
          substring(cast(coalesce(at_scene_time, event_clearance_date)  as text) from 7 for 4)    AS at_scene_year,
          substring(cast(coalesce(at_scene_time, event_clearance_date) as text) from 1 for 2)    AS at_scene_month,
          substring(cast(coalesce(at_scene_time, event_clearance_date) as text) from 4 for 2)    AS at_scene_day,
          substring(cast(coalesce(at_scene_time, event_clearance_date) as text) from 13)      AS at_scene_time,
          substring(cast(coalesce(at_scene_time, event_clearance_date) as text) from -2 for 2)   AS at_scene_am_pm,
          coalesce(at_scene_time, event_clearance_date)                  AS at_scene_date_time,
          substring(cast(coalesce(event_clearance_date, at_scene_time) as text) from  7  for 4)    AS event_clearance_year,
          substring(cast(coalesce(event_clearance_date, at_scene_time) as text) from  1  for 2)    AS event_clearance_month,
          substring(cast(coalesce(event_clearance_date, at_scene_time) as text) from 4  for 2)    AS event_clearance_day,
          substring(cast(coalesce(event_clearance_date, at_scene_time) as text) from  13)      AS event_clearance_time,
          substring(cast(coalesce(event_clearance_date, at_scene_time) as text) from  -2 for 2)   AS event_clearance_am_pm,
          coalesce(event_clearance_date, at_scene_time)                  AS event_clearance_date_time,
          CASE
            WHEN coalesce(event_clearance_group, initial_type_group) IN
                          ('THREATS, HARASSMENT', 'ROBBERY', 'ASSAULTS', 'DRIVE BY (NO INJURY)') 
                 THEN TRUE
           ELSE FALSE
           END AS is_violent,
          CASE
              WHEN (coalesce(event_clearance_group, initial_type_group)
             IN ('FRAUD CALLS', 'FALSE ALARMS'))
                         THEN TRUE
               ELSE
                          FALSE
              END AS is_false_alarm,
          coalesce(event_clearance_group, initial_type_group)             AS event_clearance_group,
          event_clearance_subgroup                                   AS event_clearance_subgroup
        FROM seattle_crime_raw
WHERE coalesce(event_clearance_group, initial_type_group) NOT IN ('FRAUD CALLS', 'FALSE ALARMS')
        ;

