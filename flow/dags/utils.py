import sys
from paths import flow_folder
sys.path.insert(0, flow_folder)
from flow.pipeline import get_diff_urls, delete_old_urls, insert_new_urls, download_images, get_unique_urls_from_db, get_unique_urls_from_csv, update_existing_urls
from datetime import datetime, timedelta
from airflow.operators.python_operator import PythonOperator
import copy

# use the current date minus 2 days as the start date
date_now = datetime.now()-timedelta(days=2)
base_start_date = date_now.replace(hour=15,minute=0,second=0)

# manually set the start date
#base_start_date = datetime(2016,12,5,15,0,0) # 15pm UTC, which is 23pm in singapore

currency_start_date = base_start_date
asos_start_date = base_start_date + timedelta(minutes = 1)
farfetch_start_date = base_start_date + timedelta(minutes = 5)
lazada_start_date = base_start_date + timedelta(minutes = 20)
yoox_start_date = base_start_date + timedelta(minutes = 40)
zalora_start_date = base_start_date + timedelta(hours = 1)
swap_start_date = base_start_date + timedelta(hours = 1)
updatedb_start_date = base_start_date + timedelta(hours = 2)
gmv_start_date = base_start_date + timedelta(minutes = 2)
db_status_start_date = base_start_date + timedelta(minutes = 3)

default_args = {
    'owner': 'iqnect',
    'depends_on_past': False,
    'start_date': base_start_date,
    'email':['sisong@iqnect.org'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=30),
}

currency_args = copy.deepcopy(default_args)
asos_args = copy.deepcopy(default_args)
farfetch_args = copy.deepcopy(default_args)
lazada_args = copy.deepcopy(default_args)
yoox_args = copy.deepcopy(default_args)
zalora_args = copy.deepcopy(default_args)
swap_args = copy.deepcopy(default_args)
updatedb_args = copy.deepcopy(default_args)
gmv_args = copy.deepcopy(default_args)
db_status_args = copy.deepcopy(default_args)

currency_args['start_date'] = currency_start_date
asos_args['start_date'] = asos_start_date
farfetch_args['start_date'] = farfetch_start_date
lazada_args['start_date'] = lazada_start_date
yoox_args['start_date'] = yoox_start_date
zalora_args['start_date'] = zalora_start_date
swap_args['start_date'] = swap_start_date
updatedb_args['start_date'] = updatedb_start_date
gmv_args['start_date'] = gmv_start_date
db_status_args['start_date'] = db_status_start_date

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
