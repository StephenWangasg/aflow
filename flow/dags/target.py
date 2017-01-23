import sys
from paths import flow_folder
sys.path.insert(0, flow_folder)

from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from flow.downloaders.target_downloader import target_download
from flow.parsers.target_parser import parse_write, import_cats
from flow.config import data_feed_path
from flow.dags.utils import target_args, get_sub_dag


dag = DAG('target', default_args=target_args)

website = 'target'
country = 'global'
p = data_feed_path + website + country

op_kwargs = {
    'download_file': p + '.txt',
    'new_parsed_csv': p + 'current.csv',
    'website': website,
    'country': country,
    'map': [
        ('product_name', 'Product Name'),
        ('product_url', 'Product URL'),
        ('image_url', 'Image URL'),
        ('unique_url', 'Image URL')
    ],
}
cats = import_cats(data_feed_path + 'target_cats')
op_kwargs['cats'] = cats

t1 = PythonOperator(
    task_id='download_target',
    provide_context=True,
    python_callable=target_download,
    op_kwargs=op_kwargs,
    dag=dag)


t2 = PythonOperator(
    task_id='parse_target',
    provide_context=True,
    python_callable=parse_write,
    op_kwargs=op_kwargs,
    dag=dag)

t3, t4, t5, t6, t7, t8, t9 = get_sub_dag(op_kwargs, dag)
t1 >> t2 >> t4 >> t5 >> t7 >> t9
t3 >> t5
t5 >> t6
t5 >> t8
