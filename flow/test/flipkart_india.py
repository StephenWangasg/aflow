import sys
from paths import flow_folder
sys.path.insert(0, flow_folder)

from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from flow.downloaders.flipkart_downloader import flipkart_download
from flow.config import data_feed_path
from flow.dags.utils import flipkart_args, get_sub_dag

dag = DAG('flipkart_india', default_args=flipkart_args)

website = 'flipkart'
country = 'india'
p = data_feed_path + website + country

query_args = {
    'api_listing': 'https://affiliate-api.flipkart.net/affiliate/api/', 
    'affiliate_id': 'salesiqne', 
    'affiliate_token': '5d2d66375e7c4e13b0affc5b431529af', 
    'data_feed_path': data_feed_path, 
    'website': website, 
    'country': country, 
    'categories': [
        'mens_clothing', 
        'womens_clothing',
    ],
}

op_kwargs = {
    'new_parsed_csv': p + 'current.csv',
    'website': website,
    'country': country,
}

t1 = PythonOperator(
    task_id='query_flipkart_india',
    provide_context=True,
    python_callable=flipkart_download,
    op_kwargs=query_args,
    dag=dag)

t3, t4, t5, t6, t7, t8, t9 = get_sub_dag(op_kwargs, dag)
t1 >> t4 >> t5 >> t7 >> t9
t3 >> t5
t5 >> t6
t5 >> t8
