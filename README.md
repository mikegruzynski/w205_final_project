# w205_final_project
https://sites.google.com/s/0B6PWth7pPGaLRW1tYUFNZmNRaFk/p/0B6PWth7pPGaLSFdLYWdxdmhSMTg/edit?pli=1&authuser=1


STEP BY STEP:
1. Log into AWS and Launch New Instance
    - Go To Community AMI and search for UCB W205 SPRING 2016
    - choose m3.large
    - Hit Next Configure: Instance Details
    - add: Protect against accidental termination
    - Next: add Storage
    - change /dev/sda1 from 30 to 100 gb
    - Hit Next Add Tags
    - Add another tag
    - key: w205_final_project_key value: w205_final_project_value
    - Next Configure Security Group
    - Port Range: 4040, 7180, 8080, 8088, 50070, 10000 ALL WITH 0.0.0.0/0, ::/0 as last colunmn
    - Hit next review
    - Hit Launch
    - Then change top to Create a new key pair: name it w205_final and HIT DOWNLOAD KEY PAIR

2. Connect to AWS EC2 instance

3. open up /data
    - chmod a+rwx /data

4. Figure out name of data volume
    - fdisk -l
	
5. get setup script and make it executable and run
    - wget https://s3.amazonaws.com/ucbdatasciencew205/setup_ucb_complete_plus_postgres.sh
    - chmod +x ./setup_ucb_complete_plus_postgres.sh
    - ./setup_ucb_complete_plus_postgres.sh <FROM ABOVE THE DATA VOLUME>
    - mine command : ./setup_ucb_complete_plus_postgres.sh /dev/xvda1
    - hit eneter to continue

6. set up text file system
    - su - w205
    - cd /data
    - mkdir /final_project
    - cd /final_project
    - mkdir /raw_data
    - cd /raw_data
    - mkdir /bus
    - mkdir /crime
    - mkdir /weather
    - mkdir /shapes
    - mkdir /geospatial

7. Bring data into AWS from PC
    - Go into launch folder where you keep the .pem file (key to AWS INSTANCE)
    - root@ec2-54-205-222-199.compute-1.amazonaws.com addressfound on the pop up window from when you hit connect on AWS EC2 under Example:
    - load the files with:
    - scp -i "w205_final.pem" ../raw_data/Froutes.txt  root@ec2-54-205-222-199.compute-1.amazonaws.com:/data/final_project/raw_data/bus
    - scp -i "w205_final.pem" ../raw_data/Fstops.txt  root@ec2-54-205-222-199.compute-1.amazonaws.com:/data/final_project/raw_data/bus
    - scp -i "w205_final.pem" ../raw_data/Ftrips.txt  root@ec2-54-205-222-199.compute-1.amazonaws.com:/data/final_project/raw_data/bus
    - scp -i "w205_final.pem" ../raw_data/stop_times.txt  root@ec2-54-205-222-199.compute-1.amazonaws.com:/data/final_project/raw_data/bus
    - scp -i "w205_final.pem" ../raw_data/Seattle_Police_Department_911_Incident_Response.csv  root@ec2-54-205-222-199.compute-1.amazonaws.com:/data/final_project/raw_data/crime
    - scp -i "w205_final.pem" ../raw_data/weather.txt  root@ec2-54-205-222-199.compute-1.amazonaws.com:/data/final_project/raw_data/weather

8. Make no header files
    - cd /data/final_project/raw_data/bus
    - tail -n +2 Froutes.txt > Froutes_noH.txt
    - tail -n +2 Fstops.txt > Fstops_noH.txt
    - tail -n +2 Ftrips.txt > Ftrips_noH.txt
    - tail -n +2 stop_times.txt > stop_times_noH.txt
    - cd /data/final_project/raw_data/weather
    - tail -n +2 weather.txt > weather_noH.txt
    - cd /data/final_project/raw_data/crime
    - tail -n +2 Seattle_Police_Department_911_Incident_Response.txt > Seattle_Police_Department_911_Incident_Response_noH.txt
	
9. make python data to clean up data and clean data dir
    - cd /data/final_project
    - mkdir python_clean_files
    - mkdir clean_data
    - cd clean_data
    - mkdir bus
    - mkdir weather
    - cd /bus
    - cp ../../raw_data/bus/Fstops_noH.txt  .
    - cd ../weather
    - cp ../../raw_data/weather/weather_noH.txt .
    - cd ../crime
    - cp ../../raw_data/weather/Seattle_Police_Department_911_Incident_Response_noH.txt .
	
10. bring python script up to AWS and make executable for cleaning data
    - on pc side (launch command from dir with launch .pem file
    - scp -i "w205_final.pem" ../python_clean_files/bus_route_stops_clean.py  root@ec2-54-205-222-199.compute-1.amazonaws.com:/data/final_project/python_clean_files
    - on AWS instance
    - chmod +x bus_route_stops_clean.py
	- cd /data/final_project/python_clean_files
	- /home/w205/spark15/bin/spark-submit bus_route_stops_clean.py
	
11. bring python scripts up to aws and make executable for converting txt to postgres
    - cd /data/final_project
    - mkdir python_to_postgres_files
    - cd python_to_postgres_files
    - cd ..
    - mkdir /python_extract_postgres_files
    - on pc side (launch command from dir with launch .pem file
    - scp -i "w205_final.pem" ../python_to_postgres_files/bus_route_stop_to_postgres.py  root@ec2-54-205-222-199.compute-1.amazonaws.com:/data/final_project/python_to_postgres_files
    - scp -i "w205_final.pem" ../python_to_postgres_files/bus_stop_to_postgres.py  root@ec2-54-205-222-199.compute-1.amazonaws.com:/data/final_project/python_to_postgres_files
    - scp -i "w205_final.pem" ../python_to_postgres_files/test.py  root@ec2-54-205-222-199.compute-1.amazonaws.com:/data/final_project/python_extract_postgres_files
    - scp -i "w205_final.pem" ../python_to_postgres_files/weather.py  root@ec2-54-205-222-199.compute-1.amazonaws.com:/data/final_project/python_to_postgres_files

12. pip install python packages and python anacondas
    - wget https://repo.continuum.io/archive/Anaconda2-4.1.1-Linux-x86_64.sh
    - chmod +x *.sh
    -  ./Anaconda2-4.1.1-Linux-x86_64.sh
    - /root/anaconda2/bin/pip install psycopg2==2.6.2
    - /root/anaconda2/bin/pip install geopandas
    - sudo yum install geos-devel

13. Create postgres database and dataframes
    - input below in AWS command prompt:
    - psql --username=postgres
    - CREATE DATABASE final_project;
    - \connect final_project;
    - and now for the data frames:
	
CREATE TABLE weather_seattle (
cal_date DATE NOT NULL,
temp_high_degF INT NOT NULL,
temp_high_avg INT NOT NULL,
temp_high_low INT NOT NULL,
visiblity_mi_high INT NOT NULL,
visiblity_mi_avg INT NOT NULL,
visiblity_mi_low INT NOT NULL,
wind_mph_high INT NOT NULL,
wind_mph_avg INT NOT NULL,
wind_mph_low INT NOT NULL,
precipitation_in_sum REAL NOT NULL,
events TEXT NOT NULL
);

CREATE TABLE bus_stop_seattle (
stop_id BIGINT NOT NULL,
stop_name TEXT NOT NULL,
stop_lat DOUBLE PRECISION NOT NULL,
stop_lon DOUBLE PRECISION NOT NULL
);

CREATE TABLE bus_route_stop_seattle (
route_short_name TEXT NOT NULL,
stop_name TEXT NOT NULL,
stop_id BIGINT NOT NULL,
stop_lat DOUBLE PRECISION NOT NULL,
stop_lon DOUBLE PRECISION NOT NULL
);

    - check if it is there: \l (for database) and \dt (for the dataframes)

13. run python postgres scripts:
    - ctrl + d twice to get out of postgres
    - cd /data/final_project/python_to_postgres_files
    - chmod +x *.py	
    - python bus_route_stop_to_postgres.py
    - python bus_stop_to_postgres.py
    - python weather.py
    - cd /data/final_project/python_extract_postgres_files
    - /root/anaconda2/bin/python test.py


