from pymongo import MongoClient
import redis
import os

data_feed_path = '/images/models/feeds/'
feed_images_path = '/images/models/feed_images/'
model_path = '/images/models/'

if not os.path.exists(data_feed_path):
    os.makedirs(data_feed_path)

if not os.path.exists(feed_images_path):
    os.makedirs(feed_images_path)

if not os.path.exists(model_path):
    os.makedirs(model_path)

# IP and port numbers
mongo_config = {'host': '127.0.0.1', 'port': 27017}
redis_config  = {'host': '127.0.0.1', 'port': 6379}
segmentation_server = {'host': '172.31.2.224', 'port': '8000'}
classification_server = {'host': '172.31.15.49', 'port': '8000'}
query_server = {'host': '172.31.22.177', 'port': '8000'}
aerospike_config = {'hosts': [ ('172.31.25.128', 3000) ],'policies': {'timeout': 5000 }}

# Connections
mongo_client_ = MongoClient(mongo_config['host'], mongo_config['port'])
_db = mongo_client_['fashion']
collection = _db['products']
