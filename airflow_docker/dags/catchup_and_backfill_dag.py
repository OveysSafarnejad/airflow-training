from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator


dag_args = {
    'owner': 'safarnejad',
    'retries': 1,
    'retry_delay': timedelta(minutes=2),
}

with DAG(
    dag_id='catchup_and_backfill_dag',
    description='this is my first dag',
    start_date=datetime(2023, 10, 1),
    default_args=dag_args,
    schedule_interval='@daily',
    catchup=False  # Older tasks also should be run
) as dag:

    task_a = BashOperator(
        task_id='task_a',
        bash_command="echo Hello World.",
        dag=dag
    )


'''
    If we set catchup = False
    then we have to run
    ```
        airflow dags backfill -s 2023-10-1 -e 2023-11-5 \
            catchup_and_backfill_dag
    ```
    to run previous tasks.
'''
