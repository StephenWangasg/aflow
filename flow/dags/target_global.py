'target global DAG definition'

from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from utils import get_sub_dag, get_task_id
from flow.configures.conf import get_dag_args
from flow.configures.target_conf import OP_KWARGS
from flow.downloaders.downloader import DownloaderDirector
from flow.downloaders.target_downloader import TargetDownloader
from flow.parsers.parser import Parser
from flow.parsers.target_filter import TargetFilter
TARGET_GLOBAL_DAG = DAG(
    'target_global', default_args=get_dag_args('target.global'))

TARGET_GLOBAL_KWARGS = OP_KWARGS.copy()
TARGET_GLOBAL_KWARGS['download_file_csv_dialect']['delimiter'] = '\t'

TASK1 = PythonOperator(
    task_id=get_task_id('download', TARGET_GLOBAL_KWARGS),
    provide_context=True,
    python_callable=lambda **kwargs: DownloaderDirector.construct(
        TargetDownloader(kwargs)),
    op_kwargs=TARGET_GLOBAL_KWARGS,
    dag=TARGET_GLOBAL_DAG)


TASK2 = PythonOperator(
    task_id=get_task_id('parse', TARGET_GLOBAL_KWARGS),
    provide_context=True,
    python_callable=lambda **kwargs: Parser(TargetFilter(kwargs)).parse(),
    op_kwargs=TARGET_GLOBAL_KWARGS,
    dag=TARGET_GLOBAL_DAG)

TASK3 = get_sub_dag(TARGET_GLOBAL_KWARGS, TARGET_GLOBAL_DAG)

TASK1 >> TASK2 >> TASK3
