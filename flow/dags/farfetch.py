import sys
from paths import flow_folder
sys.path.insert(0, flow_folder)

from airflow import DAG
from airflow.operators.python_operator import PythonOperator

from flow.downloaders.downloader import DownloaderDirector
from flow.downloaders.raukuten_downloader import RaukutenDownloader
from flow.parsers.parser import Parser
from flow.dags.utils import farfetch_args, get_sub_dag
from flow.configures.farfetch_conf import OP_KWARGS

DAG_ = DAG('farfetch', default_args=farfetch_args)

t1 = PythonOperator(
    task_id='download_farfetch',
    provide_context=True,
    python_callable=lambda **kwargs: DownloaderDirector.construct(
        RaukutenDownloader(kwargs)),
    op_kwargs=OP_KWARGS,
    dag=DAG_)

t2 = PythonOperator(
    task_id='parse_farfetch',
    provide_context=True,
    python_callable=parse_write,
    op_kwargs=op_kwargs,
    dag=dag)

t3 = get_sub_dag(op_kwargs, dag)

t1 >> t2 >> t3
