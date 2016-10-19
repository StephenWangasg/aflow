import sys
from paths import flow_folder
sys.path.insert(0, flow_folder)

from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.python_operator import PythonOperator
import requests, redis
from flow.config import query_server


def get_current_rates():
    sources = ['USD', 'AUD', 'GBP', 'SGD', 'MYR', 'IDR']
    conversions = {}
    for source in sources:
        payload = {
            'access_key': '68ed2e50d616f09954f0906bfe509904',
            'source': source,
            'currencies': 'USD,SGD,MYR,IDR'
        }
        r = requests.get('http://apilayer.net/api/live', params=payload)
        conversions.update(r.json()['quotes'])
    return conversions


def cache_currency(**kwargs):
    currency_cache = redis.StrictRedis(host=query_server['host'], port=6379, db=0)
    conversions = get_current_rates()
    currency_cache.set('currencies', str(conversions))
    print conversions



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

dag = DAG('update_db', default_args=default_args)

t1 = PythonOperator(
    task_id='update_currency_conversion',
    provide_context=True,
    python_callable=cache_currency,
    dag=dag)
