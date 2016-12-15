import sys
from paths import flow_folder
sys.path.insert(0, flow_folder)

from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from flow.dags.utils import db_status_args
from flow.get_db_status import get_db_status

dag = DAG('db_status', default_args=db_status_args)

t1 = PythonOperator(
    task_id='db_status',
    provide_context=True,
    python_callable=get_db_status,
    dag=dag)

