import sys
from paths import flow_folder
sys.path.insert(0, flow_folder)

from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from flow.downloaders.utils import lazada_download
from flow.parsers.utils import parse_write
from flow.config import data_feed_path
from flow.dags.utils import lazada_args, get_sub_dag

dag = DAG('lazada_singapore', default_args=lazada_args)

website = 'lazada'
country = 'singapore'
p = data_feed_path + website + country

op_kwargs = {
    'download_file': p + '.txt',
    'new_parsed_csv': p + 'current.csv',
    'website': website,
    'country': country,
    "feed_url": "http://lap.lazada.com/datafeed2/download.php?affiliate=69829&country=sg&cat1=%22Fashion%22&cat2=%22Men%22%2C%22Women%22&cat3=%22Clothing%22&price=0&app=0",
    'map': [
        ('image_url', 'picture_url'),
        ('product_url', 'tracking_link'),
        ('unique_url', 'picture_url')
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
    task_id='parse_lazada_singapore',
    provide_context=True,
    python_callable=parse_write,
    op_kwargs=op_kwargs,
    dag=dag)

t3 = get_sub_dag(op_kwargs, dag)

t1 >> t2 >> t3
