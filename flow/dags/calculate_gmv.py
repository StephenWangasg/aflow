
'calculate gmv'

from datetime import datetime
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from .utils import get_task_id
from ..configures import conf
from ..utilities.access import Access


CALCULATE_GMV_DAG = DAG('calculate_gmv', default_args=conf.get_dag_args('gmv'))


def calculate_gmv_single(site, location, accessor):
    '''calculate gmv for a single website'''
    records = accessor.products.find(
        {'site': site, 'location': location, 'extracted': True})
    gmv = 0.0
    count = 0
    currency = None
    for record in records:
        gmv += float(record['display_price'])
        count += 1
        if not currency:
            currency = record['currency']

    if count > 0:
        # Save to mongodb
        accessor.gmvs.update_one(
            {'site': site, 'location': location},
            {'$set': {
                'count': count,
                'gmv': gmv,
                'currency': currency,
                'last_modified': datetime.utcnow(),
            }},
            upsert=True
        )


def calculate_gmv(**kwargs):
    '''calculate gmv for each website'''
    accessor = Access(kwargs)
    for site in conf.WEBSITES:
        for location in conf.COUNTRIES:
            calculate_gmv_single(site, location, accessor)

TASK1 = PythonOperator(
    task_id=get_task_id('calculate_gmv', conf.CONFIGS),
    provide_context=True,
    python_callable=calculate_gmv,
    op_kwargs=conf.CONFIGS,
    dag=CALCULATE_GMV_DAG)
