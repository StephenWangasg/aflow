'swap us DAG definition'

from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from utils import get_sub_dag, get_task_id
from flow.configures.conf import get_dag_args
from flow.configures.swap_conf import OP_KWARGS
from flow.downloaders.downloader import DownloaderDirector
from flow.downloaders.swap_downloader import SwapDownloader
from flow.parsers.parser import Parser
from flow.parsers.swap_filter import SwapFilter

SWAP_US_DAG = DAG('swap_us', default_args=get_dag_args('swap.us'))

TASK1 = PythonOperator(
    task_id=get_task_id('download', OP_KWARGS),
    provide_context=True,
    python_callable=lambda **kwargs: DownloaderDirector.construct(
        SwapDownloader(kwargs)),
    op_kwargs=OP_KWARGS,
    dag=SWAP_US_DAG)


TASK2 = PythonOperator(
    task_id=get_task_id('parse', OP_KWARGS),
    provide_context=True,
    python_callable=lambda **kwargs: Parser(SwapFilter(kwargs)).parse(),
    op_kwargs=OP_KWARGS,
    dag=SWAP_US_DAG)

TASK3 = get_sub_dag(OP_KWARGS, SWAP_US_DAG)

TASK1 >> TASK2 >> TASK3
