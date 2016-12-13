from pymongo import MongoClient

mongo_client = MongoClient()
db = mongo_client['fashion']
gmvs = db['gmvs']

records = gmvs.find()
for r in records:
    print r

