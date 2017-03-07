import os
import sys
from paths import flow_folder
sys.path.insert(0, flow_folder)

from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from flow.dags.utils import get_sub_dag
from flow.configures.conf import get_dag_args
from flow.configures.asos_conf import OP_KWARGS
from flow.downloaders.downloader import DownloaderDirector
from flow.downloaders.raukuten_downloader import RaukutenDownloader
from flow.parsers.parser import Parser
from flow.parsers.raukuten_filter import RaukutenFilter

ASOS_DAG = DAG('asos', default_args=get_dag_args('asos.global'))

t1 = PythonOperator(
    task_id='download_asos',
    provide_context=True,
    python_callable=lambda **kwargs: DownloaderDirector.construct(
        RaukutenDownloader(kwargs)),
    op_kwargs=OP_KWARGS,
    dag=ASOS_DAG)

t2 = PythonOperator(
    task_id='parse_asos',
    provide_context=True,
    python_callable=lambda **kwargs: Parser(RaukutenFilter(kwargs)).parse(),
    op_kwargs=OP_KWARGS,
    dag=ASOS_DAG)

t3 = get_sub_dag(OP_KWARGS, ASOS_DAG)

t1 >> t2 >> t3
