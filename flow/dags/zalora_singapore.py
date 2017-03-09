'zalora singapore DAG definition'

from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from utils import get_sub_dag, get_task_id
from flow.configures import conf
from flow.configures.zalora_conf import OP_KWARGS
from flow.downloaders.downloader import DownloaderDirector
from flow.downloaders.zalora_downloader import ZaloraDownloader
from flow.parsers.parser import Parser
from flow.parsers.zalora_filter import ZaloraFilter

ZALORA_SINGAPORE_DAG = DAG(
    'zalora_singapore', default_args=conf.get_dag_args('zalora.singapore'))

ZALORA_SINGAPORE_KWARGS = OP_KWARGS.copy()
ZALORA_SINGAPORE_KWARGS['country'] = 'singapore'
ZALORA_SINGAPORE_KWARGS['search_word'] = 'ZALORA_SG-Product_Feed.txt.g'

TASK1 = PythonOperator(
    task_id=get_task_id('download', ZALORA_SINGAPORE_KWARGS),
    provide_context=True,
    python_callable=lambda **kwargs: DownloaderDirector.construct(
        ZaloraDownloader(kwargs)),
    op_kwargs=ZALORA_SINGAPORE_KWARGS,
    dag=ZALORA_SINGAPORE_DAG)

TASK2 = PythonOperator(
    task_id=get_task_id('parse', ZALORA_SINGAPORE_KWARGS),
    provide_context=True,
    python_callable=lambda **kwargs: Parser(ZaloraFilter(kwargs)).parse(),
    op_kwargs=ZALORA_SINGAPORE_KWARGS,
    dag=ZALORA_SINGAPORE_DAG)

TASK3 = get_sub_dag(ZALORA_SINGAPORE_KWARGS, ZALORA_SINGAPORE_DAG)

TASK1 >> TASK2 >> TASK3
