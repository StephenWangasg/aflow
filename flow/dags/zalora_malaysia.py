'zalora malaysia DAG definition'

import os
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from .utils import get_sub_dag, get_task_id
from ..configures import conf
from ..configures.zalora_conf import OP_KWARGS
from ..downloaders.downloader import DownloaderDirector
from ..downloaders.zalora_downloader import ZaloraDownloader
from ..parsers.parser import Parser
from ..parsers.zalora_filter import ZaloraFilter

ZALORA_MALAYSIA_DAG = DAG(
    'zalora_malaysia', default_args=conf.get_dag_args('zalora.malaysia'))

ZALORA_MALAYSIA_KWARGS = OP_KWARGS.copy()
ZALORA_MALAYSIA_KWARGS['country'] = 'malaysia'
ZALORA_MALAYSIA_KWARGS['download_file'] = os.path.join(
    conf.DOWNLOAD_CONFIGS['download_path'], 'zalora.malaysia.txt')
ZALORA_MALAYSIA_KWARGS['parsed_file'] = os.path.join(
    conf.DOWNLOAD_CONFIGS['download_path'], 'zalora.malaysia.csv')
ZALORA_MALAYSIA_KWARGS['search_word'] = 'ZALORA_MY-Product_Feed.txt.g'

TASK1 = PythonOperator(
    task_id=get_task_id('download', ZALORA_MALAYSIA_KWARGS),
    provide_context=True,
    python_callable=lambda **kwargs: DownloaderDirector.construct(
        ZaloraDownloader(kwargs)),
    op_kwargs=ZALORA_MALAYSIA_KWARGS,
    dag=ZALORA_MALAYSIA_DAG)

TASK2 = PythonOperator(
    task_id=get_task_id('parse', ZALORA_MALAYSIA_KWARGS),
    provide_context=True,
    python_callable=lambda **kwargs: Parser(ZaloraFilter(kwargs)).parse(),
    op_kwargs=ZALORA_MALAYSIA_KWARGS,
    dag=ZALORA_MALAYSIA_DAG)

TASK3 = get_sub_dag(ZALORA_MALAYSIA_KWARGS, ZALORA_MALAYSIA_DAG)

TASK1 >> TASK2 >> TASK3
