'''minimal configurations for all feeds'''

from datetime import datetime, timedelta

CONFIGS = {
    'log_path': '/images/models/logs/',
    'mongo_host': 'localhost',
    'mongo_port': 27017,
    'query_host': '172.31.22.177',
    'query_port': 8000,
    'query_port_redis': 6379
}

DOWNLOAD_CONFIGS = {
    'download_path': '/images/models/feeds/',
    'feed_images_path': '/images/models/feed_images/',
}

# use the current date minus 2 days as the start date
DATE_NOW = datetime.now() - timedelta(days=2)
BASETARTATE = DATE_NOW.replace(hour=15, minute=0, second=0)

DAG_CONFIGS = {
    'owner': 'iqnect',
    'depends_on_past': False,
    'start_date': BASETARTATE,
    'email': ['sisong@iqnect.org'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=30),
}

DAG_TIMEDELTA = {
    'currency': 0,
    'asos.global': 1,
    'farfetch.global': 5,
    'lazada.singapore': 10,
    'lazada.indonesia': 15,
    'lazada.malaysia': 20,
    'swap.us': 25,
    'target.global': 30,
    'zalora.singapore': 35,
    'zalora.malaysia': 40,
    'yoox.singapore': 45,
    'yoox.malaysia': 50,
    'updatedb': 100,
    'gmv': 120,
    'db_status': 200
}

WEBSITES = ['lazada', 'asos', 'farfetch', 'yoox', 'zalora',
            'swap', 'flipkart', 'target', 'luisaviaroma']

COUNTRIES = ['singapore', 'global', 'indonesia', 'malaysia', 'india']

STATUSES = [True, False, 'download_error_url', 'download_error_url_404',
            'download_error_url_timeout', 'server_error']


def update(op_kwargs):
    'merge minimal configurations into feeds operational conf'
    op_kwargs.update(CONFIGS)
    op_kwargs.update(DOWNLOAD_CONFIGS)


def get_dag_args(deltime):
    'DAG arguments'
    args = DAG_CONFIGS.copy()
    args['start_date'] = BASETARTATE + timedelta(
        minutes=DAG_TIMEDELTA[deltime])
    return args
