import os
import sys
from paths import flow_folder
sys.path.insert(0, flow_folder)

from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from flow.downloaders.utils import raukuten_download
from flow.parsers.utils import parse_write
from flow.config import CONFIGS, DOWNLOAD_CONFIGS
from flow.dags.utils import asos_args, get_sub_dag

from flow.downloaders.downloader import DownloaderDirector
from flow.downloaders.raukuten_downloader import RaukutenDownloader
from flow.parsers.parser import Parser
from flow.configures.asos_conf import OP_KWARGS

DAG_ = DAG('asos', default_args=asos_args)

t1 = PythonOperator(
    task_id='download_asos',
    provide_context=True,
    python_callable=lambda **kwargs: DownloaderDirector.construct(
        RaukutenDownloader(OP_KWARGS)),
    op_kwargs=OP_KWARGS,
    dag=DAG_)

t2 = PythonOperator(
    task_id='parse_asos',
    provide_context=True,
    python_callable=lambda **kwargs: Parser(kwargs).parse(),
    op_kwargs=OP_KWARGS,
    dag=DAG_)

t3 = get_sub_dag(OP_KWARGS, DAG_)

t1 >> t2 >> t3
