from datetime import datetime, timedelta

from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator


dag_args = {
    'owner': 'safarnejad',
    'retries': 1,
    'retry_delay': timedelta(minutes=2),
}

with DAG(
    dag_id='postgres_conn_dag',
    description='this is my first dag',
    start_date=datetime(2023, 11, 6),
    default_args=dag_args,
    schedule_interval='0 0 * * *'
) as dag:

    '''
    Its important to create a connection before create and runnig dag
    (in this example required connection is postgres connection.)
    it can be created through Admin > Connections in airflow admin panel
    '''
    task_a = PostgresOperator(
        task_id='task_a',
        postgres_conn_id='postgres-test',
        sql="""
            create table  if not exists dag_runs(
                dt date,
                dag_id character varying,
                primary key (dt, dag_id)
            )
        """,
        dag=dag
    )

    task_a
