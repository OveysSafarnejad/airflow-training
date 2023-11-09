import csv
import logging
from datetime import timedelta
from tempfile import NamedTemporaryFile

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.utils.dates import days_ago

dag_args = {
    'owner': 'safarnejad',
    'email': ['safarnejad.ho@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 5,
    'retry_delay': timedelta(minutes=1),
}


# params from airflow docs - macros
# the execution date as YYYYMMDD (ds_nodash)
# the next execution date as YYYYMMDD if exists, else None (next_ds_nodash)
def load_data_to_file(ds_nodash, next_ds_nodash) -> None:
    hook = PostgresHook(
        postgres_conn_id='orders-pg-conn'
    )
    cursor = hook.get_conn().cursor()
    cursor.execute(
        "SELECT * FROM public.order WHERE date >= %s AND date < %s;",
        (ds_nodash, next_ds_nodash)
    )
    with NamedTemporaryFile('w', suffix=f"{ds_nodash}") as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow([row[0] for row in cursor.description])
        csv_writer.writerows(cursor)
        f.flush()
        cursor.close()
        logging.info('Saved orders to temporary file %s file.', f.name)

        s3_hook = S3Hook(aws_conn_id='minio-s3')
        s3_hook.load_file(
            bucket_name='airflow',
            filename=f.name,
            key=f"orders/{ds_nodash}.txt",
            replace=True
        )
        logging.info(f"file orders/{ds_nodash}.txt has been pushed to S3")


with DAG(
        dag_id='sql_hook_to_s3_v2',
        default_args=dag_args,
        start_date=days_ago(0),
        schedule_interval="@daily"
) as dag:
    load_data_from_pg_to_s3 = PythonOperator(
        task_id='load_data_from_pg_to_s3',
        python_callable=load_data_to_file,
    )

    load_data_from_pg_to_s3
