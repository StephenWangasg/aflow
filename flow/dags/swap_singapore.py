import sys
from paths import flow_folder
sys.path.insert(0, flow_folder)

from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from flow.downloaders.utils import swap_download
from flow.parsers.utils import parse_write
from flow.config import data_feed_path
from flow.dags.utils import swap_args, get_sub_dag


dag = DAG('swap_singapore', default_args=swap_args)

website = 'swap'
country = 'singapore'
p = data_feed_path + website + country

op_kwargs = {
    'download_file': p + '.txt',
    'new_parsed_csv': p + 'current.csv',
    'website': website,
    'country': country,
    "search_word": "Swap_com-Swap_com_Product_Catalog.txt.g",
    'map': [
        ('product_name', 'NAME'),
        ('currency', 'CURRENCY'),
        ('product_url', 'BUYURL'),
        ('image_url', 'IMAGEURL'),
        ('unique_url', 'IMAGEURL')
    ],
    'cats': [
        "Men's Apparel > Men's Fashion",
        "Women's Apparel > Women's Fashion",
    ]
}

t1 = PythonOperator(
    task_id='download_swap_singapore',
    provide_context=True,
    python_callable=swap_download,
    op_kwargs=op_kwargs,
    dag=dag)


t2 = PythonOperator(
    task_id='parse_swap_singapore',
    provide_context=True,
    python_callable=parse_write,
    op_kwargs=op_kwargs,
    dag=dag)

t3, t4, t5, t6, t7, t8, t9 = get_sub_dag(op_kwargs, dag)
t1 >> t2 >> t4 >> t5 >> t7 >> t9
t3 >> t5
t5 >> t6
t5 >> t8
