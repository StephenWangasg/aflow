'yoox singapore DAG definition'

from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from utils import get_sub_dag, get_task_id
from flow.configures import conf
from flow.configures.yoox_conf import OP_KWARGS
from flow.downloaders.downloader import DownloaderDirector
from flow.downloaders.yoox_downloader import YooxDownloader
from flow.parsers.parser import Parser
from flow.parsers.yoox_filter import YooxFilter

YOOX_SINGAPORE_DAG = DAG(
    'yoox_singapore', default_args=conf.get_dag_args('yoox.singapore'))

YOOX_SINGAPORE_KWARGS = OP_KWARGS.copy()
YOOX_SINGAPORE_KWARGS['country'] = 'singapore'
YOOX_SINGAPORE_KWARGS['affiliate_name'] = 'YOOX.com Singapore'

TASK1 = PythonOperator(
    task_id=get_task_id('download', YOOX_SINGAPORE_KWARGS),
    provide_context=True,
    python_callable=lambda **kwargs: DownloaderDirector.construct(
        YooxDownloader(kwargs)),
    op_kwargs=YOOX_SINGAPORE_KWARGS,
    dag=YOOX_SINGAPORE_DAG)

TASK2 = PythonOperator(
    task_id=get_task_id('parse', YOOX_SINGAPORE_KWARGS),
    provide_context=True,
    python_callable=lambda **kwargs: Parser(YooxFilter(kwargs)).parse(),
    op_kwargs=YOOX_SINGAPORE_KWARGS,
    dag=YOOX_SINGAPORE_DAG)

TASK3 = get_sub_dag(YOOX_SINGAPORE_KWARGS, YOOX_SINGAPORE_DAG)

TASK1 >> TASK2 >> TASK3
