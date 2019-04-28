"""
BCAA Assignment Airflow DAG
Created by : Omid Poostforoosh

This DAG runs a built docker container image called:
       arxiv_cron
The container feeds the latest papers from:
       http://export.arxiv.org/rss/cs
into cloud base postgreSQL database, hosted on:
        isilo.db.elephantsql.com
The number of papers can be set in the arxiv_cron.py with variable "n"
This DAG is a daily basis job which runs everyday at 07:00 AM UTC
"""

import airflow
from datetime import datetime, timedelta
from airflow.models import DAG
from airflow.operators.bash_operator import BashOperator

default_args = {
            'owner': 'omid',
            'depends_on_past': False,
            'email': ['bcaa_support@bcaa.com'],
            'email_on_failure': True,
            'email_on_retry': False,
            'retries': 1,
            'retry_delay': timedelta(minutes=5),
            }

dag = DAG(
        'bcaa_assignment',
        default_args=default_args,
        start_date = datetime(2019, 4, 28, 7, 0),
        schedule_interval="0 7 * * *")

bcaa_assignment = BashOperator(
                    task_id = "arxiv_cron_task",
                    bash_command = "docker run arxiv_cron",
                    dag=dag)
