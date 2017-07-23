# Drop previous incarnation of seattle crime table
DROP TABLE seattle_crime;

# Create crime table from most recent data
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
  nvl(initial_type_group, event_clearance_group)            AS initial_type_group,
  latitude,
  longitude,
  zonebeat,
  substr(nvl(at_scene_time, event_clearance_date), 7, 4)    AS at_scene_year, 
  substr(nvl(at_scene_time, event_clearance_date), 1, 2)    AS at_scene_month, 
  substr(nvl(at_scene_time, event_clearance_date), 4, 2)    AS at_scene_day,
  substr(nvl(at_scene_time, event_clearance_date), 13)      AS at_scene_time,
  substr(nvl(at_scene_time, event_clearance_date), -2, 2)   AS at_scene_am_pm,
  nvl(at_scene_time, event_clearance_date)                  AS at_scene_date_time,
  substr(nvl(event_clearance_date, at_scene_time), 7, 4)    AS event_clearance_year, 
  substr(nvl(event_clearance_date, at_scene_time), 1, 2)    AS event_clearance_month, 
  substr(nvl(event_clearance_date, at_scene_time), 4, 2)    AS event_clearance_day,
  substr(nvl(event_clearance_date, at_scene_time), 13)      AS event_clearance_time,
  substr(nvl(event_clearance_date, at_scene_time), -2, 2)   AS event_clearance_am_pm,
  nvl(event_clearance_date, at_scene_time)                  AS event_clearance_date_time,
  IF(nvl(event_clearance_group, initial_type_group) 
      IN ('THREATS, HARASSMENT', 'ROBBERY', 'ASSAULTS',
          'DRIVE BY (NO INJURY)'), TRUE, FALSE)             AS is_violent,
  CASE
    WHEN (nvl(event_clearance_group, initial_type_group) IN ('THREATS, HARASSMENT', 'ROBBERY', 'ASSAULTS',
                                         'DRIVE BY (NO INJURY', 'HOMICIDE'))
      THEN 3
    WHEN (nvl(event_clearance_group, initial_type_group) 
               IN ('AUTO THEFTS', 'BURGLARY', 'DISTURBANCES',
                   'MENTAL HEALTH', 'OTHER PROPERTY', 'BURGLARY',
                   'PERSON DOWN/INJURY', 'NARCOTICS COMPLAINTS',
                   'DISTURBANCES', 'LEWD CONDUCT', 'PROSTITUTION',
                   'WEAPONS CALLS', 'RECKLESS BURNING', 'HARBOR CALLS',
                   'OTHER VICE', 'VICE CALLS') AND
           event_clearance_subgroup NOT IN ('AUTO RECOVERIES'))
       THEN 1
    ELSE 0 
    END                                                      AS risk_factor,
  IF(nvl(event_clearance_group, initial_type_group) 
     IN ('FRAUD CALLS', 'FALSE ALARMS'), TRUE, FALSE)        AS is_false_alarm,
  nvl(event_clearance_group, initial_type_group)             AS event_clearance_group,
  event_clearance_subgroup                                   AS event_clearance_subgroup
FROM seattle_crime_raw 
;
