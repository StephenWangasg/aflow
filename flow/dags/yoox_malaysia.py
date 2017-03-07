'yoox malaysia DAG definition'

import os
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from .utils import get_sub_dag, get_task_id
from ..configures import conf
from ..configures.yoox_conf import OP_KWARGS
from ..downloaders.downloader import DownloaderDirector
from ..downloaders.yoox_downloader import YooxDownloader
from ..parsers.parser import Parser
from ..parsers.yoox_filter import YooxFilter

YOOX_MALAYSIA_DAG = DAG(
    'yoox_malaysia', default_args=conf.get_dag_args('yoox.malaysia'))

YOOX_MALAYSIA_KWARGS = OP_KWARGS.copy()
YOOX_MALAYSIA_KWARGS['country'] = 'malaysia'
YOOX_MALAYSIA_KWARGS['download_file'] = os.path.join(
    conf.DOWNLOAD_CONFIGS['download_path'], 'yoox.malaysia.txt')
YOOX_MALAYSIA_KWARGS['parsed_file'] = os.path.join(
    conf.DOWNLOAD_CONFIGS['download_path'], 'yoox.malaysia.csv')
YOOX_MALAYSIA_KWARGS['affiliate_name'] = 'YOOX.com Malaysia'

TASK1 = PythonOperator(
    task_id=get_task_id('download', YOOX_MALAYSIA_KWARGS),
    provide_context=True,
    python_callable=lambda **kwargs: DownloaderDirector.construct(
        YooxDownloader(kwargs)),
    op_kwargs=YOOX_MALAYSIA_KWARGS,
    dag=YOOX_MALAYSIA_DAG)

TASK2 = PythonOperator(
    task_id=get_task_id('parse', YOOX_MALAYSIA_KWARGS),
    provide_context=True,
    python_callable=lambda **kwargs: Parser(YooxFilter(kwargs)).parse(),
    op_kwargs=YOOX_MALAYSIA_KWARGS,
    dag=YOOX_MALAYSIA_DAG)

TASK3 = get_sub_dag(YOOX_MALAYSIA_KWARGS, YOOX_MALAYSIA_DAG)

TASK1 >> TASK2 >> TASK3

