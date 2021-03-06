# BCAA Assignment

A repo containing three methods for representing BCAA business intelligence assignment.
Each method includes a containerized data processor created by Docker.
For the first and second approaches, docker images are already built and provided in [Docker hub](https://hub.docker.com/r/omidp/bcaa_assignment). Teammates can easily pull the image from docker hub and run it. That's it. It's all they need to do.

This repo also includes a Jupyter notebook which points at the database and pull a sample of data.


#  Dockers Highlights
## postgreSQL
A simple database has been implemented in a free could base postgreSQL platform called [ElephantSQL](elephantsql.com).
Credentials are provided in `creds.py`

## Approach 1
In this method, a python script `arxiv_cron.py` captures data from [arxiv.org](http://arxiv.org/rss/cs) and load it into postgreSQL. An Apache Airflow DAG schedules the job for a periodic basis `arxiv_cron_dag.py`. This DAG is a daily basis job which runs everyday at 07:00 AM __UTC__. This setting can be easily changed by editing __schedule_interval__ parameter. 

### Requirements (Assuming they are already installed on your machines)
- [Docker](https://docs.docker.com/install/)
- [Apache Airflow](https://airflow.apache.org/installation.html)
- [Jupyter Notebook](https://jupyter.readthedocs.io/en/latest/install.html)

docker commands:
```
docker pull omidp/bcaa_assignment:part1
```
```
docker image ls
docker run <created image id>
```


## Approach 2
The container image in this method can be pulled and run independently without any installation. Python file `arxiv_scheduler.py` creates a thread which automatically runs based on a scheduled interval.  

### Requirements (Assuming they are already installed on your machines)
- [Docker](https://docs.docker.com/install/)
- [Jupyter Notebook](https://jupyter.readthedocs.io/en/latest/install.html)

docker commands:
```
docker pull omidp/bcaa_assignment:part2_scheduled_container
```
```
docker image ls
docker run <created image id>
```

## Approach 3
This data pipeline has been provided to demonstrate the knowledge of AWS. The python script `arxiv_s3.py` captures data from [arxiv.org](http://arxiv.org/rss/cs) and load it into Redshift. This data pipeline uses Amazon Simple Storage Service (S3) to store csv files.


### Requirements (Assuming they are already installed on your machines)
- [Docker](https://docs.docker.com/install/)
- [Jupyter Notebook](https://jupyter.readthedocs.io/en/latest/install.html)
- Amazon Web Services (Including Redshift and S3 buckets)

# Credentials Files
For the first and second methods, credentials stored in `creds.py` which are located right beside the main script.   

For approach number 3, we need the Amazon Web Service platform which cannot be established for this assignment. However, scripts are fully tested and codes can be run successfully with inserting a proper  AWS credential.

# Jupyter Notebook
Includes all blocks for:
- importing packages
- connecting to postgreSQL database
- presenting a sample of data

```
./jupyter notebook
```
When the notebook pages loaded in the browser click on `arxiv.ipynb` then run all cells
