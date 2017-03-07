'db_status'

from datetime import datetime
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from .utils import get_task_id
from ..configures import conf
from ..utilities.access import Access


DB_STATUS_DAG = DAG('db_status', default_args=conf.get_dag_args('db_status'))


def get_db_status_single(site, location, accessor):
    'update db status for a single site'
    total = accessor.products.count({'site': site, 'location': location})
    # Save to mongodb
    accessor.db_status.update_one(
        {'site': site, 'location': location, 'status': 'total'},
        {'$set': {
            'count': total,
            'last_modified': datetime.now(),
        }},
        upsert=True
    )

    for status in conf.STATUSES:
        count = accessor.products.count(
            {'site': site, 'location': location, 'extracted': status})
        # Save to mongodb
        accessor.db_status.update_one(
            {'site': site, 'location': location, 'status': status},
            {'$set': {
                'count': count,
                'last_modified': datetime.now(),
            }},
            upsert=True
        )


def get_db_status(**kwargs):
    'update db status all sites'
    accessor = Access(kwargs)
    for site in conf.WEBSITES:
        for location in conf.COUNTRIES:
            get_db_status_single(site, location, accessor)

TASK1 = PythonOperator(
    task_id=get_task_id('db_status', conf.CONFIGS),
    provide_context=True,
    python_callable=get_db_status,
    op_kwargs=conf.CONFIGS,
    dag=DB_STATUS_DAG)
