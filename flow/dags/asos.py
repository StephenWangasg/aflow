import sys
from paths import flow_folder
sys.path.insert(0, flow_folder)

from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.python_operator import PythonOperator
from flow.downloaders.utils import raukuten_download
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

dag = DAG('asos', default_args=default_args)

website = 'asos'
country = 'global'
p = data_feed_path + website + country

op_kwargs = {
    'download_file': p + '.txt',
    'current_parsed_csv': p + 'current.csv',
    'previous_parsed_csv': p + 'previous.csv',
    'website': website,
    'country': country,
    "affiliate_name": "ASOS",
    "feed_url": "ftp://iQNECT:n39PzPcw@aftp.linksynergy.com/37863_3301502_mp.txt.gz",
    "prepend_header": "product_id|product_name|sku|primary_cat|secondary_cat|product_url|image_url|c8|c9|c10|c11|c12|sale_price|retail_price|c15|c16|c17|c18|c19|c20|c21|c22|c23|c24|c25|currency|c27|c28|c29|c30|c31|c32|c33|c34|c35|c36|c37|c38\n",

    "cats": [
        'All-In-One', 'Knitwear', 'Mens', 'Tops', 'Trousers', 'Womens', 'Mens Jackets', 'Womens Jackets', 'Womens Coats', 'Mens Coats', '|',
        'Caps', 'Wallets', 'Gloves', 'Hats', 'Bags', 'Accessories', 'Hair', 'Shoes', 'Sandals', 'Trainers', 'Gifts',
        'Sunglasses', 'Underwear', 'Swimming', 'Bikinis', 'Swimsuits', 'Swimwear', 'Socks', 'Accessories', 'Backpacks', 'Jewelry', 'Luggage',
        'Lingerie/Underwear', 'Belts', 'Bracelets', 'Earrings', 'Necklaces', 'Jewellery', 'Lipsticks', 'Conditioners'
        ],
    'map': [
        ('product_name', 'product_name'),
        ('currency', 'currency'),
        ('product_url', 'product_url'),
        ('image_url', 'image_url'),
        ('unique_url', 'image_url')
        ]
}

t1 = PythonOperator(
    task_id='download_asos',
    provide_context=True,
    python_callable=raukuten_download,
    op_kwargs=op_kwargs,
    dag=dag)

t2 = PythonOperator(
    task_id='parse_asos',
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