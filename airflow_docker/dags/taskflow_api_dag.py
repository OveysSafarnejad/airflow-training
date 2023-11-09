from datetime import datetime, timedelta

from airflow.decorators import dag, task


dag_args = {
    'owner': 'safarnejad',
    'retries': 2,
    'retry_delay': timedelta(minutes=1),
}


@dag(
    dag_id='taskflow_api_dag',
    default_args=dag_args,
    start_date=datetime(2023, 11, 4),
    schedule_interval='@daily'
)
def example_taskflow_dag():

    @task(multiple_outputs=True)
    def get_name():
        return {
            'first_name': 'Oveys',
            'last_name': 'Safarnejad'
        }

    @task()
    def get_age():
        return 30

    @task()
    def greetings(first_name, last_name, age):
        print(f"Hello, My name is {first_name} {last_name}  \
                and I'm {age} years old ;)")

    name_dict = get_name()
    age = get_age()
    greetings(
        first_name=name_dict['first_name'],
        last_name=name_dict['last_name'],
        age=age
    )


greet_lag = example_taskflow_dag()
