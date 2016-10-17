import sys
from paths import flow_folder
sys.path.insert(0, flow_folder)

from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.python_operator import PythonOperator
from flow.downloaders.utils import lazada_download
from flow.parsers.utils import parse_write
from flow.config import data_feed_path
from flow.utils import get_diff_urls, delete_old_urls, insert_new_urls, download_images, copy_current2previous, feature_extraction


default_args = {
    'owner': 'raja',
    'depends_on_past': False,
    'start_date': datetime(2016,10,1),
    'email':['raja@iqnect.org'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=30),
}

dag = DAG('lazada_singapore', default_args=default_args)

website = 'lazada'
country = 'singapore'
p = data_feed_path + website + country

op_kwargs = {
    'download_file': p + '.txt',
    'current_parsed_csv': p + 'current.csv',
    'previous_parsed_csv': p + 'previous.csv',
    'website': website,
    'country': country,
    "feed_url": "http://lap.lazada.com/datafeed2/download.php?affiliate=69829&country=sg&cat1=%22Fashion%22&cat2=%22Men%22%2C%22Women%22&cat3=%22Clothing%22&price=0&app=0",
    'map': [
        ('image_url', 'picture_url'),
        ('product_url', 'tracking_link'),
        ('unique_url', 'tracking_link')
      ],
    'cats': []
}

t1 = PythonOperator(
    task_id='download_lazada_singapore',
    provide_context=True,
    python_callable=lazada_download,
    op_kwargs=op_kwargs,
    dag=dag)

t2 = PythonOperator(
    task_id='parse_lazada',
    provide_context=True,
    python_callable=parse_write,
    op_kwargs=op_kwargs,
    dag=dag)

t3 = PythonOperator(
    task_id='get_diff_urls',
    provide_context=True,
    python_callable=get_diff_urls,
    op_kwargs=op_kwargs,
    dag=dag)

t4 = PythonOperator(
    task_id='delete_old_urls',
    provide_context=True,
    python_callable=delete_old_urls,
    op_kwargs=op_kwargs,
    dag=dag)

t5 = PythonOperator(
    task_id='insert_new_urls',
    provide_context=True,
    python_callable=insert_new_urls,
    op_kwargs=op_kwargs,
    dag=dag)

t6 = PythonOperator(
    task_id='download_images',
    provide_context=True,
    python_callable=download_images,
    op_kwargs=op_kwargs,
    dag=dag)

t7 = PythonOperator(
    task_id='copy_current2previous',
    provide_context=True,
    python_callable=copy_current2previous,
    op_kwargs=op_kwargs,
    dag=dag)

t8 = PythonOperator(
    task_id='feature_extraction',
    provide_context=True,
    python_callable=feature_extraction,
    op_kwargs=op_kwargs,
    dag=dag)

t2.set_upstream(t1)
t3.set_upstream(t2)
t4.set_upstream(t3)
t5.set_upstream(t3)
t6.set_upstream(t5)
t7.set_upstream(t5)
t8.set_upstream(t6)