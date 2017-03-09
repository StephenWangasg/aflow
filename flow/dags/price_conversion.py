# 'price conversion'

# import redis
# import requests
# from airflow import DAG
# from airflow.operators.python_operator import PythonOperator
# from utils import get_task_id
# from flow.configures import conf

# PRICE_CONVERSION_DAG = DAG(
#     'price_conversion', default_args=conf.get_dag_args('currency'))


# def get_current_rates():
#     'get current rates'
#     sources = ['USD', 'AUD', 'GBP', 'SGD', 'MYR', 'IDR']
#     conversions = {}
#     for source in sources:
#         payload = {
#             'access_key': '68ed2e50d616f09954f0906bfe509904',
#             'source': source,
#             'currencies': 'USD,SGD,MYR,IDR'
#         }
#         ret = requests.get('http://apilayer.net/api/live', params=payload)
#         conversions.update(ret.json()['quotes'])
#     return conversions


# def cache_currency(**kwargs):
#     'cache currency'
#     currency_cache = redis.StrictRedis(host=kwargs['query_host'],
#                                        port=kwargs['query_port_redis'], db=0)
#     conversions = get_current_rates()
#     currency_cache.set('currencies', str(conversions))

# TASK1 = PythonOperator(
#     task_id=get_task_id('cache_currency', conf.CONFIGS),
#     provide_context=True,
#     python_callable=cache_currency,
#     op_kwargs=conf.CONFIGS,
#     dag=PRICE_CONVERSION_DAG)
