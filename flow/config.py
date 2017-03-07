from pymongo import MongoClient
import os

CONFIGS = {
    'log_path': '/home/stephen/tmp/images/models/logs/',
}

DOWNLOAD_CONFIGS = {
    'download_path': '/home/stephen/tmp/images/models/feeds/',

}
model_path = '/home/stephen/tmp/images/models/'
data_feed_path = '/home/stephen/tmp/images/models/feeds/'
feed_images_path = '/home/stephen/tmp/images/models/feed_images/'
log_file_path = '/home/stephen/tmp/images/logs/'

for my_file in (model_path,
                data_feed_path,
                feed_images_path,
                log_file_path):
    if not os.path.exists(my_file):
        os.makedirs(my_file)


# Log level options: 'debug', 'info', 'warning', 'error', 'critical'
log_level_file = 'info'
log_level_stdout = 'debug'
log_file_size_in_bytes = 0x3200000 #50MB

# IP and port numbers
mongo_config = {'host': '127.0.0.1', 'port': 27017}
redis_config = {'host': '127.0.0.1', 'port': 6379}
segmentation_server = {'host': '172.31.2.224', 'port': '8000'}
classification_server = {'host': '172.31.15.49', 'port': '8000'}
query_server = {'host': '172.31.22.177', 'port': '8000'}
aerospike_config = {'hosts': [('172.31.25.128', 3000)], 'policies': {
    'timeout': 5000}}

# Connections
mongo_client_ = MongoClient(mongo_config['host'], mongo_config['port'])
_db = mongo_client_['fashion']
collection = _db['products']
