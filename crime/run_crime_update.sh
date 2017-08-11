#!/bin/bash
# Usage: ./run_crime_update.sh <crime_files_directory> <database_name> <user/role>
export CRIME_DIR = "$1"

# ensure directory exists, ignore error if it already exists
mkdir -p $CRIME_DIR 2>/dev/null

#Get Crime data file, rename it as SeattleCrimeData.csv
wget -O $CRIME_DIR/SeattleCrimeData.csv https://data.seattle.gov/d/3k2p-39jp?category=Public-Safety&view_name=Seattle-Police-Department-911-Incident-Response

#Run .sql script to update crime table in postgres
psql -d $2 -u $3 create_postgres_crime.sql
