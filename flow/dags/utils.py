import sys
from paths import flow_folder
sys.path.insert(0, flow_folder)
from flow.pipeline import get_diff_urls, delete_old_urls, insert_new_urls, download_images, get_unique_urls_from_db, get_unique_urls_from_csv, update_existing_urls
from datetime import datetime, timedelta
from airflow.operators.python_operator import PythonOperator


default_args = {
    'owner': 'raja',
    'depends_on_past': False,
    'start_date': datetime(2016,11,02),
    'email':['raja@iqnect.org'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=30),
}


def get_sub_dag(op_kwargs, dag):

    t3 = PythonOperator(
        task_id='get_unique_urls_from_db',
        provide_context=True,
        python_callable=get_unique_urls_from_db,
        op_kwargs=op_kwargs,
        dag=dag)

    t4 = PythonOperator(
        task_id='get_unique_urls_from_csv',
        provide_context=True,
        python_callable=get_unique_urls_from_csv,
        op_kwargs=op_kwargs,
        dag=dag)

    t5 = PythonOperator(
        task_id='get_diff_urls',
        provide_context=True,
        python_callable=get_diff_urls,
        op_kwargs=op_kwargs,
        dag=dag)

    t6 = PythonOperator(
        task_id='delete_old_urls',
        provide_context=True,
        python_callable=delete_old_urls,
        op_kwargs=op_kwargs,
        dag=dag)

    t7 = PythonOperator(
        task_id='insert_new_urls',
        provide_context=True,
        python_callable=insert_new_urls,
        op_kwargs=op_kwargs,
        dag=dag)

    t8 = PythonOperator(
        task_id='update_existing_urls',
        provide_context=True,
        python_callable=update_existing_urls,
        op_kwargs=op_kwargs,
        dag=dag)

    t9 = PythonOperator(
        task_id='download_images',
        provide_context=True,
        python_callable=download_images,
        op_kwargs=op_kwargs,
        dag=dag)

    return t3, t4, t5, t6, t7, t8, t9
