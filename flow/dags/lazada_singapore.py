'lazada singapore DAG definition'

from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from utils import get_sub_dag, get_task_id
from flow.configures import conf
from flow.configures.lazada_conf import OP_KWARGS
from flow.downloaders.downloader import DownloaderDirector
from flow.downloaders.lazada_downloader import LazadaDownloader
from flow.parsers.parser import Parser
from flow.parsers.lazada_filter import LazadaFilter

LAZADA_SINGAPORE_DAG = DAG(
    'lazada_singapore', default_args=conf.get_dag_args('lazada.singapore'))

LAZADA_SINGAPORE_KWARGS = OP_KWARGS.copy()
LAZADA_SINGAPORE_KWARGS['country'] = 'singapore'
LAZADA_SINGAPORE_KWARGS['feed_url'] = \
    'http://lap.lazada.com/datafeed2/download.php?affiliate=69829&country=sg&cat1=%22Fashion%22&cat2=%22Men%22%2C%22Women%22&cat3=%22Clothing%22&price=0&app=0'

TASK1 = PythonOperator(
    task_id=get_task_id('download', LAZADA_SINGAPORE_KWARGS),
    provide_context=True,
    python_callable=lambda **kwargs: DownloaderDirector.construct(
        LazadaDownloader(kwargs)),
    op_kwargs=LAZADA_SINGAPORE_KWARGS,
    dag=LAZADA_SINGAPORE_DAG)

TASK2 = PythonOperator(
    task_id=get_task_id('parse', LAZADA_SINGAPORE_KWARGS),
    provide_context=True,
    python_callable=lambda **kwargs: Parser(LazadaFilter(kwargs)).parse(),
    op_kwargs=LAZADA_SINGAPORE_KWARGS,
    dag=LAZADA_SINGAPORE_DAG)

TASK3 = get_sub_dag(LAZADA_SINGAPORE_KWARGS, LAZADA_SINGAPORE_DAG)

TASK1 >> TASK2 >> TASK3
