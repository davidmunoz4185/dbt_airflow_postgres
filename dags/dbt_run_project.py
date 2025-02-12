from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.dummy import DummyOperator
from datetime import datetime, timedelta
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 5, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dbt_project_dir = "/opt/airflow/dbt/jaffle_shop"
dbt_profiles_dir = "/opt/airflow/dbt/jaffle_shop"

dag = DAG('dbt_build_project', default_args=default_args, schedule_interval=None)
start_task = DummyOperator(task_id='start_task', dag=dag)
end_task = DummyOperator(task_id='end_task', dag=dag)

# Define dbt tasks using BashOperator
dbt_task = BashOperator(
    task_id='dbt_build_project_task',
    bash_command=f"""
        dbt build \
        --project-dir {dbt_project_dir} \
        --profiles-dir {dbt_profiles_dir} \
        --target pro
    """,
    dag=dag
)

# Set task dependencies
start_task >> dbt_task >> end_task