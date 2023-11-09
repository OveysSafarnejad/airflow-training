from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator


dag_args = {
    'owner': 'safarnejad',
    'retries': 1,
    'retry_delay': timedelta(minutes=2),
}

with DAG(
    dag_id='bash_operator_dag',
    description='this is my first dag',
    start_date=datetime(2023, 11, 5),
    default_args=dag_args,
    schedule_interval='@daily'
) as dag:

    task_a = BashOperator(
        task_id='task_a',
        bash_command="pwd",
        dag=dag
    )

    task_b = BashOperator(
        task_id='task_b',
        # bash_command="cp /opt/airflow/dags/consolidate_data.jpg
        # /opt/airflow/dags/consolidate.jpg",
        bash_command="echo Hello!",
        dag=dag
    )

    task_c = BashOperator(
        task_id='task_c',
        bash_command="ls -la",
        dag=dag
    )

    task_a.set_downstream(task_b)
    task_b.set_downstream(task_c)
