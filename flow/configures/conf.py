'''minimal configurations for all feeds'''

from datetime import datetime, timedelta


CONFIGS = {
    'log_path': '/images/models/logs/',
    # 'disable', 'debug', 'info', 'warning', 'error' or 'critical'
    'log_level_file': 'debug',
    'log_level_stdout': 'disable',
    'log_file_size_in_bytes': 0x500000,  # 5MB
    'log_file_count': 10,  # see below
    'mongo_host': 'localhost',
    'mongo_port': 27017,
    'query_host': '172.31.2.224',
    'query_port': 8000,
    'query_port_redis': 6379,
    'segmentation_host': '172.31.21.193',
    'segmentation_port': 8000,
    'classification_host': '172.31.15.49',
    'classification_port': 8000,
    'aerospike': {'hosts': [('172.31.25.128', 3000)], 'policies': {
        'timeout': 5000}},
    'model_path': '/images/models/',
    'download_path': '/images/models/feeds/',
    'feed_images_path': '/images/models/feed_images/',
    'attribute_tree': 'attribute_tree.json',
    'extraction_threads': 4,
    # How the downloaded file is formated?
    'download_file_csv_dialect': {'delimiter': ',',
                                  'quotechar': '"',
                                  'escapechar': None,
                                  'doublequote': True,
                                  'skipinitialspace': False,
                                  'lineterminator': '\r\n', },
}

CATEGORIES = {
    "tShirts": ['color', 'pattern', "neck", "slLen"],
    "shirts": ['color', 'pattern', "neck", "slLen"],
    "leggings": ['color', 'pattern', "length"],
    "downJackets": ['color', 'pattern', "neck"],
    "dresses": ['color', 'pattern', "fit", "neck", "sil", "slLen", "dressLen"],
    "skirts": ['color', 'pattern', "dressLen", "sil"],
    "shorts": ['color', 'pattern', "fit", "length"],
    "polo": ['color', 'pattern', "neck", "slLen"],
    "jeans": ['color', 'pattern', "fit"],
    "pullovers": ['color', 'pattern', "neck", "slLen"],
    "tankTops": ['color', 'pattern', "neck"],
    "cardigans": ['color', 'pattern', "neck", "slLen"],
    "hoodies": ['color', 'pattern', "neck", "slLen"],
    "trench": ['color', 'pattern', "neck", "slLen"],
    "casualPants": ['color', 'pattern', "fit", "length"],
    "camis": ['color', 'pattern'],
    "blazers": ['color', 'pattern', "slLen"],
    "rompers": ['color', 'pattern', "fit"],
    "suitPants": ['color']
}

# use the current date minus 2 days as the start date
DATE_NOW = datetime.utcnow() - timedelta(days=2)
BASETARTATE = DATE_NOW.replace(hour=15, minute=0, second=0)

DAG_CONFIGS = {
    'owner': 'iqnect',
    'depends_on_past': False,
    'start_date': BASETARTATE,
    'email': ['sisong@iqnect.org'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
    'catchup': False,
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
    'feature': 45,
    'updatedb': 180,
    'db_status': 200,
    'gmv': 220,
}

WEBSITES = ['lazada', 'asos', 'farfetch', 'zalora',
            'swap', 'flipkart', 'target', 'luisaviaroma']

COUNTRIES = ['singapore', 'global', 'indonesia', 'malaysia', 'india', 'us']

STATUSES = [True, False, 'download_error_url', 'download_error_url_404',
            'download_error_url_timeout', 'server_error']

LAYER = 'FC8'
LAYER_DIMENSION = 25

ATTRIBUTE_LENGTH = {'color': 25, 'dressLen': 3, 'fit': 3, 'gender': 2,
                    'length': 3, 'neck': 8, 'pattern': 8, 'sil': 9, 'slLen': 3, 'subCat': 19}

ATTRIBUTE_MAP = {"color": "color", "black": "black", "blue": "blue", "white": "white",
                 "red": "red", "grey": "grey", "beige": "beige", "darkBlue": "darkBlue",
                 "green": "green", "lightBlue": "lightBlue", "pink": "pink", "purple": "purple",
                 "yellow": "yellow", "darkGreen": "darkGreen", "brown": "brown", "orange": "orange",
                 "darkGrey": "darkGrey", "darkRed": "darkRed", "rose": "rose", "gold": "gold",
                 "silver": "silver", "lightGrey": "lightGrey", "lightGreen": "lightGreen",
                 "melonRed": "watermelonRed", "camel": "camel", "lakeBlue": "lakeBlue",
                 "dressLen": "dressLength", "knee": "kneeLength", "full": "full", "mini": "mini",
                 "fit": "fit", "slim": "slim", "loose": "loose", "straight": "straight",
                 "gender": "gender", "m": "male", "f": "female", "length": "bottomLength",
                 "short": "short", "neck": "neckLine", "o": "oNeck", "v": "vNeck",
                 "turtle": "turtleNeck", "slash": "slashNeck", "strapless": "strapless",
                 "turnDown": "turnDownCollar", "hooded": "hooded", "stand": "standCollar",
                 "pattern": "pattern", "solid": "solid", "print": "print", "plaid": "plaid",
                 "striped": "striped", "floral": "floral", "polkaDot": "polkaDot",
                 "leopard": "leopard", "camouflage": "camouflage", "sil": "silhouette",
                 "aLine": "aLine", "sheath": "sheath", "pleated": "pleated",
                 "ballGown": "ballGown", "pencil": "pencil", "asymmetrical": "asymmetrical",
                 "fitFlare": "fitAndFlare", "trumpet": "trumpetAndMermaid",
                 "slLen": "sleeveLength", "half": "half", "sleeveless": "sleeveless",
                 "subCat": "category", "tShirts": "tShirts", "shirts": "shirts",
                 "leggings": "leggings", "downJackets": "downJackets", "dresses": "dresses",
                 "skirts": "skirts", "shorts": "shorts", "polo": "polo", "jeans": "jeans",
                 "pullovers": "pullovers", "tankTops": "tankTops", "cardigans": "cardigans",
                 "hoodies": "hoodies", "trench": "trench", "casualPants": "casualPants",
                 "camis": "camis", "blazers": "blazers", "rompers": "jumpSuitsandRompers",
                 "suitPants": "suitPants"}


def update(op_kwargs):
    'merge minimal configurations into feeds operational conf'
    op_kwargs.update(CONFIGS)


def get_dag_args(deltime):
    'DAG arguments'
    args = DAG_CONFIGS.copy()
    args['start_date'] = BASETARTATE + timedelta(
        minutes=DAG_TIMEDELTA[deltime])
    return args


#'log_file_count': The maximum number of logs for one task.
# A task is either a downloader, parser or manager.
# Each task initially uses a log file in the form 'A.B.C'
# where 'A' is site name('lazada')
#'B' is country name('singapore)
#'C' is task name('download')
# All logs are saved in 'log_path'
# If the file grows larger than 'log_file_size_in_bytes',
# it is renamed to 'A.B.C.1', and new logs are saved in
#'A.B.C' again. When 'A.B.C' grows larger again, 'A.B.C.1'
# is renamed to 'A.B.C.2'. This renaming iterates until
#'A.B.C.{log_file_count}', then oldest log is purged.
