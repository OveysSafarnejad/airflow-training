from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator


def push_xcoms(ti) -> None:
    # Max XCOM size is 48KB
    ti.xcom_push(
        key='first_name',
        value='Oveys'
    )

    ti.xcom_push(
        key='last_name',
        value='Safarnejad'
    )

    ti.xcom_push(
        key='age',
        value=30
    )


def greeting(ti) -> None:
    first_name = ti.xcom_pull(task_ids='task_a', key='first_name')
    last_name = ti.xcom_pull(task_ids='task_a', key='last_name')
    age = ti.xcom_pull(task_ids='task_a', key='age')
    print(f"My name is {first_name} {last_name} and I'm {age} years old.")


dag_args = {
    'owner': 'safarnejad',
    'retries': 2,
    'retry_delay': timedelta(minutes=1),
}

with DAG(
    dag_id='python_op_dag',
    description='A simple dag with python operators',
    start_date=datetime(2023, 11, 4),
    schedule_interval='@daily',
    default_args=dag_args
):
    task_a = PythonOperator(
        task_id='task_a',
        python_callable=push_xcoms
    )

    task_b = PythonOperator(
        task_id='task_b',
        python_callable=greeting
    )

    task_a >> task_b
