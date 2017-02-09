import sys
from paths import flow_folder
sys.path.insert(0, flow_folder)
from flow.pipeline import update_insert_delete_urls
from datetime import datetime, timedelta
from airflow.operators.python_operator import PythonOperator
import copy

# use the current date minus 2 days as the start date
date_now = datetime.now()-timedelta(days=2)
base_start_date = date_now.replace(hour=15,minute=0,second=0)

# manually set the start date
# base_start_date = datetime(2017,1,1,0,0,0)

currency_start_date = base_start_date
asos_start_date = base_start_date + timedelta(minutes = 1)
farfetch_start_date = base_start_date + timedelta(minutes = 5)
lazada_start_date = base_start_date + timedelta(minutes = 20)
yoox_start_date = base_start_date + timedelta(minutes = 40)
zalora_start_date = base_start_date + timedelta(hours = 1)
swap_start_date = base_start_date + timedelta(minutes = 80)
flipkart_start_date = base_start_date + timedelta(minutes = 100)
target_start_date = base_start_date + timedelta(hours = 2)
updatedb_start_date = base_start_date + timedelta(hours = 3)
gmv_start_date = base_start_date + timedelta(minutes = 200)
db_status_start_date = base_start_date + timedelta(minutes = 200)

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
flipkart_args = copy.deepcopy(default_args)
target_args = copy.deepcopy(default_args)
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
flipkart_args['start_date'] = flipkart_start_date
target_args['start_date'] = target_start_date
updatedb_args['start_date'] = updatedb_start_date
gmv_args['start_date'] = gmv_start_date
db_status_args['start_date'] = db_status_start_date

def get_sub_dag(op_kwargs, dag):
    '''
    The common sub dag for all feeds
    '''
    return PythonOperator(
        task_id='update_insert_delete_urls',
        provide_context=True,
        python_callable=update_insert_delete_urls,
        op_kwargs=op_kwargs,
        dag=dag)

