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

dag = DAG('dbt_build_models_bq', default_args=default_args, schedule_interval=None)
start_task = DummyOperator(task_id='start_task', dag=dag)
end_task = DummyOperator(task_id='end_task', dag=dag)

# Define dbt tasks using BashOperator
dbt_seed_customers = BashOperator(
    task_id='dbt_seed_customers',
    bash_command=f"""
        dbt build -s jaffle_shop_customers \
        --project-dir {dbt_project_dir} \
        --profiles-dir {dbt_profiles_dir} \
        --target bigquery
    """,
    dag=dag
)

dbt_seed_orders = BashOperator(
    task_id='dbt_seed_orders',
    bash_command=f"""
        dbt build -s jaffle_shop_orders \
        --project-dir {dbt_project_dir} \
        --profiles-dir {dbt_profiles_dir} \
        --target bigquery
    """,
    dag=dag
)

dbt_seed_payments = BashOperator(
    task_id='dbt_seed_payments',
    bash_command=f"""
        dbt build -s stripe_payments \
        --project-dir {dbt_project_dir} \
        --profiles-dir {dbt_profiles_dir} \
        --target bigquery
    """,
    dag=dag
)

dbt_stg_customers = BashOperator(
    task_id='dbt_stg_customers',
    bash_command=f"""
        dbt build -s stg_jaffle_shop__customers \
        --project-dir {dbt_project_dir} \
        --profiles-dir {dbt_profiles_dir} \
        --target bigquery
    """,
    dag=dag
)

dbt_stg_orders = BashOperator(
    task_id='dbt_stg_orders',
    bash_command=f"""
        dbt build -s stg_jaffle_shop__orders \
        --project-dir {dbt_project_dir} \
        --profiles-dir {dbt_profiles_dir} \
        --target bigquery
    """,
    dag=dag
)

dbt_stg_payments = BashOperator(
    task_id='dbt_stg_payments',
    bash_command=f"""
        dbt build -s stg_stripe__payments \
        --project-dir {dbt_project_dir} \
        --profiles-dir {dbt_profiles_dir} \
        --target bigquery
    """,
    dag=dag
)

dbt_legacy_model = BashOperator(
    task_id='dbt_legacy_model',
    bash_command=f"""
        dbt build -s customer_orders \
        --project-dir {dbt_project_dir} \
        --profiles-dir {dbt_profiles_dir} \
        --target bigquery
    """,
    dag=dag
)

dbt_int_model = BashOperator(
    task_id='dbt_int_model',
    bash_command=f"""
        dbt build -s int_orders \
        --project-dir {dbt_project_dir} \
        --profiles-dir {dbt_profiles_dir} \
        --target bigquery
    """,
    dag=dag
)

dbt_fct_model = BashOperator(
    task_id='dbt_fct_model',
    bash_command=f"""
        dbt build -s fct_customer_orders \
        --project-dir {dbt_project_dir} \
        --profiles-dir {dbt_profiles_dir} \
        --target bigquery
    """,
    dag=dag
)

# Set task dependencies
seed_list = [dbt_seed_customers, dbt_seed_orders, dbt_seed_payments]
stg_list = [dbt_stg_customers, dbt_stg_orders, dbt_stg_payments]
int_list = [dbt_stg_orders, dbt_stg_payments]
fct_list = [dbt_stg_customers, dbt_int_model]

dbt_seed_customers >> dbt_stg_customers
dbt_seed_orders >> dbt_stg_orders
dbt_seed_payments >> dbt_stg_payments

start_task >> seed_list
start_task >> dbt_legacy_model
int_list >> dbt_int_model
fct_list >> dbt_fct_model
dbt_fct_model >> end_task
dbt_legacy_model >> end_task