#!/bin/bash
export $CRIME_DIR = "$HOME/w205/crime"
export $HDFS_CRIME_DIR = "/user/w205"

# 
mkdir -p $CRIME_DIR

#Get Crime data file
wget -O $CRIME_DIR/crime.csv https://data.seattle.gov/d/3k2p-39jp?category=Public-Safety&view_name=Seattle-Police-Department-911-Incident-Response

#Create directory for hdfs
hdfs dfs -mkdir $HDFS_CRIME_DIR/crime_data/

# Uploads data files to HDFS, with each file having its specific directory
hdfs dfs -put $CRIME_DIR/crime.csv $HDFS_CRIME_DIR/crime_data/
