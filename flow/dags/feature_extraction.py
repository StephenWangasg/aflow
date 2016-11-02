import sys
from paths import flow_folder
sys.path.insert(0, flow_folder)

from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from flow.dags.utils import default_args
from flow.config import classification_server, segmentation_server
from flow.feature import feature_extraction
'''
dag = DAG('feature_extraction', default_args=default_args)


op_kwargs = {
    'segmentation_server': segmentation_server,
    'classification_server': classification_server
}

t1 = PythonOperator(
    task_id='feature_extraction',
    provide_context=True,
    python_callable=feature_extraction,
    op_kwargs=op_kwargs,
    dag=dag)

t2 = PythonOperator(
    task_id='feature_extraction',
    provide_context=True,
    python_callable=feature_extraction,
    op_kwargs=op_kwargs,
    dag=dag)
'''

