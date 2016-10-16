import sys
sys.path.insert(0, '/home/raja/dev/fashion-ingestion')

from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.python_operator import PythonOperator
from flow.downloaders.zalora import download_zalora_malaysia
from flow.parsers.zalora import parse_zalora_malaysia

default_args = {
    'owner': 'raja',
    'depends_on_past': False,
    'start_date': datetime(2016,10,1),
    'email':['raja@iqnect.org'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=30),
}

dag = DAG('zalora_malaysia', default_args=default_args)

t1 = PythonOperator(
    task_id='download_zalora_malaysia',
    provide_context=True,
    python_callable=download_zalora_malaysia,
    dag=dag)

t2 = PythonOperator(
    task_id='parse_zalora_malaysia',
    provide_context=True,
    python_callable=parse_zalora_malaysia,
    dag=dag)

t2.set_upstream(t1)