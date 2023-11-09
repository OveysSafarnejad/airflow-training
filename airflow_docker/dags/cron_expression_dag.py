'''
    A cron  expression is a string comprising 5 fileds
    seprated by space that represents a set of time, like:
    '* 14 1 * *' -> minute hour dayofmonth month dayofweek

    cron builtins equivalent for dags are:
    None
    @once
    @hourly     -> 0 * * * *
    @daily      -> 0 0 * * *
    @weekly     -> 0 0 * * 0
    @monthly    -> 0 0 1 * *
    @yearly     -> 0 0 1 1 *

    check https://crontab.guru
    Do you know the meaning of "15 16-23/2 * * 2,4"
'''

from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator


dag_args = {
    'owner': 'safarnejad',
    'retries': 1,
    'retry_delay': timedelta(minutes=2),
}

with DAG(
    dag_id='cron_expression_dag',
    description='this is my first dag',
    start_date=datetime(2023, 11, 5),
    default_args=dag_args,
    schedule_interval='* 12 * * *'
) as dag:

    task_a = BashOperator(
        task_id='task_a',
        bash_command="echo Hello!",
        dag=dag
    )
