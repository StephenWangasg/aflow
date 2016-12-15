import sys
from paths import flow_folder
sys.path.insert(0, flow_folder)

from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from flow.dags.utils import gmv_args
from flow.calculate_gmv import calculate_gmv

dag = DAG('calculate_gmv', default_args=gmv_args)

t1 = PythonOperator(
    task_id='calculate_gmv',
    provide_context=True,
    python_callable=calculate_gmv,
    dag=dag)

