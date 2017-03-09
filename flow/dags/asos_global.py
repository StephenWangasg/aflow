'asos global DAG definition'

from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from utils import get_sub_dag, get_task_id
from flow.configures.conf import get_dag_args
from flow.configures.asos_conf import OP_KWARGS
from flow.downloaders.downloader import DownloaderDirector
from flow.downloaders.raukuten_downloader import RaukutenDownloader
from flow.parsers.parser import Parser
from flow.parsers.raukuten_filter import RaukutenFilter


ASOS_GLOBAL_DAG = DAG('asos_global', default_args=get_dag_args('asos.global'))

TASK1 = PythonOperator(
    task_id=get_task_id('download', OP_KWARGS),
    provide_context=True,
    python_callable=lambda **kwargs: DownloaderDirector.construct(
        RaukutenDownloader(kwargs)),
    op_kwargs=OP_KWARGS,
    dag=ASOS_GLOBAL_DAG)

TASK2 = PythonOperator(
    task_id=get_task_id('parse', OP_KWARGS),
    provide_context=True,
    python_callable=lambda **kwargs: Parser(RaukutenFilter(kwargs)).parse(),
    op_kwargs=OP_KWARGS,
    dag=ASOS_GLOBAL_DAG)

TASK3 = get_sub_dag(OP_KWARGS, ASOS_GLOBAL_DAG)

TASK1 >> TASK2 >> TASK3
