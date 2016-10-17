import sys
from paths import flow_folder
sys.path.insert(0, flow_folder)

from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.python_operator import PythonOperator
from flow.downloaders.utils import zalora_download
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

dag = DAG('zalora_malaysia', default_args=default_args)

website = 'zalora'
country = 'malaysia'
p = data_feed_path + website + country

op_kwargs = {
    'download_file': p + '.txt',
    'current_parsed_csv': p + 'current.csv',
    'previous_parsed_csv': p + 'previous.csv',
    'website': website,
    'country': country,
    "search_word": "ZALORA_MY-Product_Feed.txt.g",
    'map': [
        ('product_name', 'NAME'),
        ('currency', 'CURRENCY'),
        ('product_url', 'BUYURL'),
        ('image_url', 'IMAGEURL'),
        ('unique_url', 'IMAGEURL')
      ],
    'cats': [
        "Men>Clothing>T-Shirts",
        "Men>Clothing>Polo Shirts",
        "Men>International Brands>Clothing",
        "Men>Clothing>Shirts",
        "Men>Clothing>Pants",
        "Men>Clothing>Outerwear",
        "Men>Clothing>Jeans",
        "Men>Clothing>Shorts",
        "Men>Clothing>Men\"s Clothing",
        "Men>Sports>Clothing",
        "Women>Clothing>Playsuits & Jumpsuits",
        "Women>Clothing>Dresses",
        "Women>Clothing>Tops",
        "Women>Clothing>Skirts",
        "Women>Clothing>Outerwear",
        "Women>Clothing>Shorts",
        "Women>International Brands>Clothing",
        "Women>Clothing>Pants & Leggings",
        "Women>Korean Fashion>Clothing",
        "Women>Sports>Clothing",
        "Women>Clothing>Jeans",
        "Women>Clothing>Women\"s Clothing",
        "Women>Clothing>Plus Size",
        "Women>International Brands>Sports",
        "Women>Florals>Clothing",
        "Women>Form-fitting>Clothing",
        "Women>Rock Chic>Clothing",
        "Women>Girl Boss>Clothing"
      ]
}

t1 = PythonOperator(
    task_id='download_zalora_malaysia',
    python_callable=zalora_download,
    op_kwargs=op_kwargs,
    dag=dag)

t2 = PythonOperator(
    task_id='parse_zalora_malaysia',
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