from pymongo import MongoClient

mongo_client = MongoClient()
db = mongo_client['fashion']
collection = db['products']

p = collection.find_one()
print p['display_price'], p['currency']
