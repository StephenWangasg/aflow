import sys
from paths import flow_folder
sys.path.insert(0, flow_folder)

from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.python_operator import PythonOperator
from flow.db_transfer import get_current_set, empty_aero_set, create_annoy_for_categories, create_annoy_for_filters, restart_server, mongo2aero


default_args = {
    'owner': 'raja',
    'depends_on_past': False,
    'start_date': datetime(2016,10,1),
    'email':['raja@iqnect.org'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0,
    'retry_delay': timedelta(minutes=30),
}

dag = DAG('update_db', default_args=default_args)

t1 = PythonOperator(
    task_id='get_current_set',
    provide_context=True,
    python_callable=get_current_set,
    dag=dag)

t2 = PythonOperator(
    task_id='empty_aero_set',
    provide_context=True,
    python_callable=empty_aero_set,
    dag=dag)

t3 = PythonOperator(
    task_id='mongo2aero',
    provide_context=True,
    python_callable=mongo2aero,
    dag=dag)

t4 = PythonOperator(
    task_id='create_annoy_for_categories',
    provide_context=True,
    python_callable=create_annoy_for_categories,
    dag=dag)

t5 = PythonOperator(
    task_id='create_annoy_for_filters',
    provide_context=True,
    python_callable=create_annoy_for_filters,
    dag=dag)

t6 = PythonOperator(
    task_id='restart_server',
    provide_context=True,
    python_callable=restart_server,
    dag=dag)

t2.set_upstream(t1)
t3.set_upstream(t2)
t4.set_upstream(t3)
t5.set_upstream(t4)
t6.set_upstream(t5)