import sys
from paths import flow_folder
sys.path.insert(0, flow_folder)

from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.python_operator import PythonOperator
from flow.downloaders.utils import yoox_download
from flow.parsers.utils import parse_write
from flow.config import data_feed_path
from flow.pipeline import get_diff_urls, delete_old_urls, insert_new_urls, download_images, copy_current2previous, feature_extraction


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

dag = DAG('yoox_singapore', default_args=default_args)

website = 'yoox'
country = 'singapore'
p = data_feed_path + website + country

op_kwargs = {
    'download_file': p + '.txt',
    'current_parsed_csv': p + 'current.csv',
    'previous_parsed_csv': p + 'previous.csv',
    'website': website,
    'country': country,
    "affiliate_name": "YOOX.com Singapore",
    'map': [
        ('product_name', 'Name'),
        ('currency', 'Currency'),
        ('product_url', 'Url'),
        ('image_url', 'Image'),
        ('unique_url', 'Url')
      ],
    'cats': [
        "Apparel & Accessories > Clothing > Outerwear > Coats & Jackets",
        "Apparel & Accessories > Clothing > Shirts & Tops",
        "Apparel & Accessories > Clothing > One-Pieces",
        "Apparel & Accessories > Clothing > Skirts",
        "Apparel & Accessories > Clothing > Shorts",
        "Apparel & Accessories > Clothing > Pants",
        "Apparel & Accessories > Clothing",
        "Apparel & Accessories > Clothing > Uniforms",
        "Apparel & Accessories > Clothing > Suits",
        "Apparel & Accessories > Clothing > Outerwear",
        "Apparel & Accessories > Clothing > Outerwear > Snow Pants & Suits",
        "Apparel & Accessories > Clothing > One-Pieces > Jumpsuits & Rompers"
      ]
}

t1 = PythonOperator(
    task_id='download_yoox_singapore',
    provide_context=True,
    python_callable=yoox_download,
    op_kwargs=op_kwargs,
    dag=dag)

t2 = PythonOperator(
    task_id='parse_yoox',
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