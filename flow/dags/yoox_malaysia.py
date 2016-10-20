import sys
from paths import flow_folder
sys.path.insert(0, flow_folder)

from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from flow.downloaders.utils import yoox_download
from flow.parsers.utils import parse_write
from flow.config import data_feed_path
from flow.dags.utils import default_args, get_sub_dag

dag = DAG('yoox_malaysia', default_args=default_args)

website = 'yoox'
country = 'malaysia'
p = data_feed_path + website + country

op_kwargs = {
    'download_file': p + '.txt',
    'new_parsed_csv': p + 'current.csv',
    'website': website,
    'country': country,
    "affiliate_name": "YOOX.com Malaysia",
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
    task_id='download_yoox_malaysia',
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

t3, t4, t5, t6, t7, t8, t9 = get_sub_dag(op_kwargs, dag)
t1 >> t2 >> t4 >> t5 >> t7 >> t8 >> t9
t3 >> t5
t5 >> t6