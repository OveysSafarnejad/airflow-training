source .ven/bin/activate
export AIRFLOW_HOME=/Users/audioworkstation/Documents/WORKSPACE/LEARNING/Airflow-Training
airflow db init
airflow scheduler
airflow webserver -p 9000