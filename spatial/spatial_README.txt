SPATIAL LIBRARIES AND DEPENDENCIES
Make sure you have the following python libraries and their dependencies installed:
pandas
geopandas
sqlalchemy
shapely

Geopandas depends on a library called rtree for dealing with spatial indexing.
Rtree, in turn, requires a C spatial index library to work its magic, and I ran
into some issues with this. If the geoprocessing script throws an error saying
"OSError: Could not find libspatialindex_c library file" or something similar, I
was able to fix this by running the following:
conda install -c ioos rtree


SETUP AND FILE TRANSFER
!!!The following instructions assume you have already followed Mike's initial setup
instructions for creating a directory structure, file upload, and postgres database!!!

1. Create a new directory under /data/final_project called "spatial"

2. Transfer the following files to your instance via scp or wget:

create_postgres_crime.sql (https://github.com/mikegruzynski/w205_final_project/tree/master/upload)
Place the file in /data/final_project/python_to_postgres_files/

geodf_processing.py (https://github.com/mikegruzynski/w205_final_project/tree/master/spatial)
Place this file into the /spatial directory you created above.


EXECUTE

1. From root, start the postgres server:
/data/start_postgres.sh

2. Once the server is running:
cd /data/final_project/python_to_postgres_files
psql --username=postgres -d final_project -f create_postgres_crime.sql

3. When this completes, log into postgres:
psql --username=postgres
\connect final_project
\dt

4. You should see two new tables - seattle_crime_raw and seattle_crime
Check them out and make sure they have data in them. Exit postgres.

5. Navigate to /data/final_project/spatial and run the following:
python ./geodf_processing.py

6. The geoprocessing script will run for a while...I have been seeing anywhere
from 15-30 minutes.
IMPORTANT - After completing the spatial join, it will ask you if you want to create
shapefiles. I included this feature so I could check the output in desktop GIS
software, but it's a slow operation, so I gave you guys the option to skip it.
Just enter y or n at the prompt.

7. When the geoprocessing script completes, log back into postgres and check the
tables. There should be a new table named "spjoin."
