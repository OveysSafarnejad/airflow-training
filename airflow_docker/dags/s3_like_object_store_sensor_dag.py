"""
To test this dag I need to create an s3 like object storage (minio) on my local machine.
    ```
        mkdir -p ~/minio/data

        docker run \
            -p 9000:9000 \
            -p 9090:9090 \
            -v ~/minio/data:/data \
            -e "MINIO_ROOT_USER=|| username ||" \
            -e "MINIO_ROOT_PASSWORD=|| password ||" \
            quay.io/minio/minio server /data --console-address ":9090"
    ```
then I have to create an amazon web services connection through
airflow consule > admin > connections with following items:
    {
        "aws_access_key_id": "",
        "aws_secret_acess_key": "",
        "host": "http://host.docker.internal:9000"
    }

"""

from datetime import datetime, timedelta

from airflow import DAG
from airflow.providers.amazon.aws.sensors.s3 import S3KeySensor


default_args = {
    'owner': 'safarnejad',
    'retries': 5,
    'retry_delay': timedelta(minutes=10)
}


with DAG(
    dag_id='s3_like_object_store_sensor_dag',
    start_date=datetime(2023, 11, 7),
    schedule_interval='@daily',
    default_args=default_args
) as dag:

    task_a = S3KeySensor(
        task_id='task_a',
        bucket_name='airflow',
        bucket_key='requirements.txt',
        aws_conn_id='minio-s3',
        mode='poke',
        poke_interval=5,  # interval between pokes
        timeout=30  # task will failafter the timeout
    )
