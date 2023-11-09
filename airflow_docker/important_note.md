## What if I want to have some external python packages in my airflow server?

there are two ways.
1. Extending base airflow docker image
    1.1 create a requirements file
    1.2 create a docker file 

    1.3 build docker file with my tag
    1.4 edit docker-compose file base image
    or
    1.3' edit docker compose :   
        # image: ${AIRFLOW_IMAGE_NAME:-apache/airflow:2.7.2}
        build: .
    1.4' docker compose up -d --build
    https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html#special-case-adding-dependencies-via-requirements-txt-file

    * each time I want to add a dependency, I have to 
    edit requirements > build image > restart airflow server


(Does not worked for me)
2. Customizing airflow image
    2.1 download airflow github source (airflow directory is
        airflow'ssource code)
    2.2 add requirements.txt file into airflow/docker-context-files
    2.3 docker build . --build-arg AIRFLOW_VERSION='2.7.3' --tag customized-airflow:latest

    2.4 docker compose up -d --no-deps --build airflow-webserver airflow-scheduler