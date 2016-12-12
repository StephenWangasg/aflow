import sys
from paths import flow_folder
sys.path.insert(0, flow_folder)

from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from flow.downloaders.utils import zalora_download
from flow.parsers.utils import parse_write
from flow.config import data_feed_path
from flow.dags.utils import zalora_args, get_sub_dag


dag = DAG('zalora_singapore', default_args=zalora_args)

website = 'zalora'
country = 'singapore'
p = data_feed_path + website + country

op_kwargs = {
    'download_file': p + '.txt',
    'new_parsed_csv': p + 'current.csv',
    'website': website,
    'country': country,
    "search_word": "ZALORA_SG-Product_Feed.txt.g",
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
    task_id='download_zalora_singapore',
    provide_context=True,
    python_callable=zalora_download,
    op_kwargs=op_kwargs,
    dag=dag)

t2 = PythonOperator(
    task_id='parse_zalora_singapore',
    provide_context=True,
    python_callable=parse_write,
    op_kwargs=op_kwargs,
    dag=dag)

t3, t4, t5, t6, t7, t8, t9 = get_sub_dag(op_kwargs, dag)
t1 >> t2 >> t4 >> t5 >> t7 >> t9
t3 >> t5
t5 >> t6
t5 >> t8
