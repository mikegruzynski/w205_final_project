Instructions for starting crime pipeline.

1. Identify or create the directory where crime files will be based.
2. Copy create_postgres_crime.sql and run_crime_update.sh
3. make run_crime_update.sh executable:

   chmod 755 run_crime_update.sh
   
4. The create_postgres_crime.sql includes a copy command which assumes SUPERUSER privilege. If user
   doesn't already have this, run the following as postgres:
   
   psql:  ALTER USER <user_to_use> SUPERUSER;
   
5. You should be able to run the run_crime_update.sh file now:

./run_crime_update.sh <full_path_to_crime_directory> <database_to_create_table> <user_to_use>

e.g.

./run_crime_update.sh /home/w205/crime crime_db w205

