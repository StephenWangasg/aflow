import sys
from paths import flow_folder
sys.path.insert(0, flow_folder)

from airflow import DAG
from airflow.operators.python_operator import PythonOperator
import requests, redis
from flow.config import query_server
from flow.dags.utils import currency_args

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

dag = DAG('price_conversion', default_args=currency_args)

t1 = PythonOperator(
    task_id='update_currency_conversion',
    provide_context=True,
    python_callable=cache_currency,
    dag=dag)
