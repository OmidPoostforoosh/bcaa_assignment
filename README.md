# bcaa_assignment

A repo containing three methods for representing BCAA business intelligence Assignment.
Each method includes a containerized data processor created by Docker.
Docker images are already build and provided in [Docker hub](https://hub.docker.com/r/omidp/bcaa_assignment) for the first and second approaches:


```
docker pull omidp/bcaa_assignment:part1
docker pull omidp/bcaa_assignment:part2_scheduled_container
```

#  Dockers Highlights
- Choose an absolute `start_date` when instantiating a DAG. It's tempting to do something like `start_date = datetime.now()` but this will mess things up in the future.
- If you need a task run at a specific time, use a cron-style schedule interval instead of the Airflow style. Using `@daily` _will_ get your task run, but the timing is not exactly strict.
- On VANAIRLV01, DAGs run in __UTC Time__. So if you want something to run at 3 AM PST, it must be schedule for 10 AM on the Airflow server. (Note: this was not the case on the old Airflow server, but it may not be worth looking into solving this particular issue.)
- Some other really good best practices can be found [here](https://gtoonstra.github.io/etl-with-airflow/principles.html). IMO, one of the most important concepts here is _idempotency_. From the best practices doc: "The result of a DAG run should always have idempotency characteristics. This means that when you run a process multiple times with the same parameters (even on different days), the outcome is exactly the same. You do not end up with multiple copies of the same data in your environment or other undesirable side effects." It's very easy to trigger DAGs multiple times, and you don't want your data messed up if the DAG accidentally triggers.

# Credentials Files
Some DAGs require credentials to access external systems. These files are not included in the repository to avoid accidentally checking in credentials.

The format of the currently used credentials files are as follows:
- Info Portal Postgres database
`postgres_creds.py` :
```
username = ''
password = ''
host = '192.168.32.171'
dbname = 'poc_db'
port = '5499'
```
- Data Warehouse
`redshift_creds.py`:
```
username = ""
password = ""
cluster = "o2ebrands-bi.cnomrdbyfyea.ca-central-1"
db_name = "o2enexus"
```
- BI Email Account
`imap_creds.py` :
```
imap_username = ''
imap_password = ''
```
- OBE Production Server
`obe_mysql_creds.py` :
```
instance_ip = '173.194.248.216'
database_name = 'obe_v8'
user = ''
password = ''
portal = '3306'
```
- Vonigo API
`vonigo_creds.py` :
```
username = ''
raw_password = ''
```

# Airflow Debugging / Useful Commands
Note : Airflow root on VANAIRVL01 is `~/airflow`. Assume all files referenced are in the Airflow root unless otherwise specified.
### Problem: Airflow webserver is not loading
The PID for the webserver is in the file `airflow-webserver.pid`. Check that the process is running by running the command ``ps -ef | grep `cat airflow-webserver.pid` ``. You should see output like
```
junktion 44028 47529  1 11:27 ?        00:00:02 [ready] gunicorn: worker [airflow-webserver]
junktion 44126 47529  1 11:28 ?        00:00:02 [ready] gunicorn: worker [airflow-webserver]
junktion 44215 47529  2 11:29 ?        00:00:02 [ready] gunicorn: worker [airflow-webserver]
junktion 44287 47529  3 11:30 ?        00:00:02 [ready] gunicorn: worker [airflow-webserver]
junktion 44450 47529 12 11:31 ?        00:00:01 gunicorn: worker [airflow-webserver]
junktion 44492 44430  0 11:32 pts/19   00:00:00 grep --color=auto 47529
junktion 47529     1  0 Jul25 ?        00:02:18 gunicorn: master [airflow-webserver]
```
If the webserver is not running, you should only see one line (for the `grep`) process.

If the webserver is not running, you can start it with the command `airflow webserver -p 8080 -D`. This will run the webserver on port 8080 as a daemon.

There are also log files for the webserver (`airflow-webserver.log`, `airflow-webserver.err`, `airflow-webserver.out`) for additional debugging.

### Problem: DAGs aren't running
Perhaps the scheduler is down. The PID for the scheduler is in the file `airflow-scheduler.pid`. Check that the process is running by running the command ``ps -ef | grep `cat airflow-scheduler.pid` ``. You should see output like
```
junktion 45628     1  3 11:45 ?        00:00:10 /usr/bin/python3 /home/junktion/.local/bin/airflow scheduler -D
junktion 46450 44430  0 11:51 pts/19   00:00:00 grep --color=auto 45628
```
If the webserver is not running, you should only see one line (for the `grep`) process.

If the scheduler is not running, you can start it with the command `airflow scheduler -D`. This will run the scheduler as a daemon. It is a _very_ good idea to restart the scheduler every so often (possible TODO: write a cron job to restart the scheduler).

There are also log files for the webserver (`airflow-scheduler.log`, `airflow-scheduler.err`, `airflow-scheduler.out`) for additional debugging.

### Problem: tasks are failing.
Have a look at the log file for the task.
Access from the frontend: Navigate to `Browse` -> `Task Instances` in the header. Click on the `Task Id` of the failed task, and go to the `Log` tab.
Access from the backend: In the Airflow root, log files are located in the `logs` folder and are laid out as `logs/<DAG name>/<task name>/<timestamp of run>`.

### Problem: DAGs are messed up (there are too many inactive DAGs that are still showing up, or some other state issue).
There is no way easy or obvious way to remove DAGs from the webserver frontend (which is kinda weird). DAGs are stored in Airflow's meta database located in `airflow.db`. If you reset this database, all of the DAGs in the `dags` folder will be reloaded. You can reset the database using the command `airflow resetdb`. __WARNING__ : You will lose all information from previous runs by performing this action. This is especially annoying if you don't update the `start_time`s on your DAGs (it will backfill from the start date as though they have never run).
