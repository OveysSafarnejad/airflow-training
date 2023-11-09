from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator


def check_version() -> None:
    import sklearn
    print(f"sklearn version: {sklearn.__version__}")


dag_args = {
    'owner': 'safarnejad',
    'retries': 2,
    'retry_delay': timedelta(minutes=1),
}

with DAG(
    dag_id='package_dag',
    description='A simple dag with python operators',
    start_date=datetime(2023, 11, 7),
    schedule_interval='@daily',
    default_args=dag_args
):
    task_a = PythonOperator(
        task_id='task_a',
        python_callable=check_version
    )

    task_a
