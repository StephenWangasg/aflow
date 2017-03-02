import os
import sys
from paths import flow_folder
sys.path.insert(0, flow_folder)

from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from flow.downloaders.utils import raukuten_download
from flow.parsers.utils import parse_write
from flow.config import CONFIGS, DOWNLOAD_CONFIGS
from flow.dags.utils import asos_args, get_sub_dag

from flow.logger import FlowLogger
from flow.downloaders.downloader import DownloaderDirector
from flow.downloaders.raukuten_downloader import RaukutenDownloader
from flow.parsers.parser import Parser
from flow.parsers.asos_filter import AsosFilter

DAG_ = DAG('asos', default_args=asos_args)

OP_KWARGS = {
    'site': 'asos',
    'country': 'global',
    'affiliate_name': 'ASOS',
    'feed_url': 'ftp://iQNECT:n39PzPcw@aftp.linksynergy.com/41970_3301502_mp.txt.gz',
    'download_file': os.path.join(DOWNLOAD_CONFIGS['download_path'], 'asos.global.txt'),
    'parsed_file': os.path.join(DOWNLOAD_CONFIGS['download_path'], 'asos.global.csv'),
    'logger': FlowLogger('asos', 'global', CONFIGS['log_path'], 'debug'),
    'prepend_header': ('product_id', 'product_name', 'sku', 'primary_cat',
                       'secondary_cat', 'product_url', 'image_url', 'c8', 'c9',
                       'c10', 'c11', 'c12', 'sale_price', 'retail_price', 'c15',
                       'c16', 'c17', 'c18', 'c19', 'c20', 'c21', 'c22', 'c23',
                       'c24', 'c25', 'currency', 'c27', 'c28', 'c29', 'c30', 'c31',
                       'c32', 'c33', 'c34', 'c35', 'c36', 'c37', 'c38'),
    'cats': (
        ('All-In-One', 'Knitwear', 'Mens', 'Tops', 'Trousers', 'Womens', 'Mens Jackets',
         'Womens Jackets', 'Womens Coats', 'Mens Coats'),
        ('Caps', 'Wallets', 'Gloves', 'Hats', 'Bags', 'Accessories', 'Hair', 'Shoes',
         'Sandals', 'Trainers', 'Gifts', 'Sunglasses', 'Underwear', 'Swimming', 'Bikinis',
         'Swimsuits', 'Swimwear', 'Socks', 'Accessories', 'Backpacks', 'Jewelry', 'Luggage',
         'Lingerie/Underwear', 'Belts', 'Bracelets', 'Earrings', 'Necklaces', 'Jewellery',
         'Lipsticks', 'Conditioners', 'Mens Clothing Other', 'Mens Bracelets', 'Other Gifts')
    ),
    'maps': (
        ('product_name', 'product_name'),
        ('currency', 'currency'),
        ('product_url', 'product_url'),
        ('image_url', 'image_url'),
        ('unique_url', 'image_url')
    ),
    'row_filter': AsosFilter
}

OP_KWARGS.update(CONFIGS)
OP_KWARGS.update(DOWNLOAD_CONFIGS)

t1 = PythonOperator(
    task_id='download_asos',
    provide_context=True,
    python_callable=lambda **kwargs: DownloaderDirector.construct(
        RaukutenDownloader(OP_KWARGS)),
    op_kwargs=OP_KWARGS,
    dag=DAG_)

t2 = PythonOperator(
    task_id='parse_asos',
    provide_context=True,
    python_callable=lambda **kwargs: Parser(kwargs).parse(),
    op_kwargs=OP_KWARGS,
    dag=DAG_)

t3 = get_sub_dag(OP_KWARGS, DAG_)

t1 >> t2 >> t3
