import sys
from paths import flow_folder
sys.path.insert(0, flow_folder)

from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from flow.dags.utils import db_status_args
from flow.utilities.access import Access
from datetime import datetime
import flow.configures.conf as conf


DAG_ = DAG('db_status', default_args=db_status_args)


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

t1 = PythonOperator(
    task_id='db_status',
    provide_context=True,
    python_callable=get_db_status,
    op_kwargs=conf.CONFIGS,
    dag=DAG_)
