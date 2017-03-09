'lazada malaysia DAG definition'

from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from utils import get_sub_dag, get_task_id
from flow.configures import conf
from flow.configures.lazada_conf import OP_KWARGS
from flow.downloaders.downloader import DownloaderDirector
from flow.downloaders.lazada_downloader import LazadaDownloader
from flow.parsers.parser import Parser
from flow.parsers.lazada_filter import LazadaFilter

LAZADA_MALAYSIA_DAG = DAG(
    'lazada_malaysia', default_args=conf.get_dag_args('lazada.malaysia'))

LAZADA_MALAYSIA_KWARGS = OP_KWARGS.copy()

LAZADA_MALAYSIA_KWARGS['country'] = 'malaysia'
LAZADA_MALAYSIA_KWARGS['feed_url'] = \
    'http://lap.lazada.com/datafeed2/download.php?affiliate=69829&country=my&cat1=%22Fashion%22&cat2=%22Women%22%2C%22Men%22&cat3=%22Clothing%22&price=0&app=0'  #DO NOT ADD comma(,) here

TASK1 = PythonOperator(
    task_id=get_task_id('download', LAZADA_MALAYSIA_KWARGS),
    provide_context=True,
    python_callable=lambda **kwargs: DownloaderDirector.construct(
        LazadaDownloader(kwargs)),
    op_kwargs=LAZADA_MALAYSIA_KWARGS,
    dag=LAZADA_MALAYSIA_DAG)

TASK2 = PythonOperator(
    task_id=get_task_id('parse', LAZADA_MALAYSIA_KWARGS),
    provide_context=True,
    python_callable=lambda **kwargs: Parser(LazadaFilter(kwargs)).parse(),
    op_kwargs=LAZADA_MALAYSIA_KWARGS,
    dag=LAZADA_MALAYSIA_DAG)

TASK3 = get_sub_dag(LAZADA_MALAYSIA_KWARGS, LAZADA_MALAYSIA_DAG)

TASK1 >> TASK2 >> TASK3
