# BCAA Assignment

A repo containing three methods for representing BCAA business intelligence assignment.
Each method includes a containerized data processor created by Docker.
For the first and second approaches, docker images are already built and provided in [Docker hub](https://hub.docker.com/r/omidp/bcaa_assignment)
Teammates can easily pull the image from docker hub and run it.

How to pull image from docker hub:
```
docker pull omidp/bcaa_assignment:part1
docker pull omidp/bcaa_assignment:part2_scheduled_container
```
This repo also includes a Jupyter notebook which points at the database and pull a sample of data.
Each folder contains separated readme.md file which explains the approach particularly.

#  Dockers Highlights
## Approach 1
In this method, a python script `arxiv_cron.py` captures data from [arxiv.org](at http://arxiv.org/rss/cs.) and load it into postgreSQL. An Apache Airflow DAG schedules the job for a periodic basis `arxiv_cron_dag.py`

## Approach 2
The container image in this method can be pulled and run independently without any installation. Python file `arxiv_scheduler.py` creates a thread which automatically runs based on a scheduled interval.  

## Approach 3
This data pipeline has been provided to demonstrate the knowledge of AWS. The python script `arxiv_s3.py` captures data from [arxiv.org](at http://arxiv.org/rss/cs.) and load it into Redshift. This data pipeline uses Amazon Simple Storage Service (S3) to store csv files.

# Credentials Files
For the first and second methods, credentials stored in `creds.py` which are located right beside the main script.   

For approach number 3, we need the Amazon Web Service platform which cannot be established for this assignment. However, scripts are fully tested and codes can be run successfully with inserting a proper  AWS credentials.
