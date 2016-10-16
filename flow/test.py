import sys

sys.path.insert(0, '/home/raja/dev/fashion-ingestion')
from airflow import DAG
from datetime import datetime, timedelta

from airflow.operators.python_operator import PythonOperator
from flow.downloaders.zalora import zalora_singapore
from flow.parsers.zalora import parse_csv
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

dag = DAG('ingest', schedule_interval=timedelta(hours=12), default_args=default_args)

t1 = PythonOperator(
    task_id='zalora_download',
    provide_context=True,
    python_callable=zalora_singapore,
    dag=dag)

t2 = PythonOperator(
    task_id='zalora_parser',
    provide_context=True,
    python_callable=parse_csv,
    dag=dag)

t2.set_upstream(t1)