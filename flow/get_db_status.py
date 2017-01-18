from pymongo import MongoClient
from datetime import datetime

mongo_client = MongoClient()
db = mongo_client['fashion']
collection = db['products']
db_collection = db['db_status']

SITES = ['lazada', 'asos', 'farfetch', 'yoox', 'zalora', 'swap', 'flipkart']
LOCATIONS = ['global', 'singapore', 'indonesia', 'malaysia', 'india']
STATUSES = [True, False, 'download_error_url','download_error_url_404','download_error_url_timeout','server_error']


def get_db_status(**kwargs):
    for site in SITES:
        for location in LOCATIONS:
            total = collection.count({'site': site, 'location': location})
            # Save to mongodb
            entry = db_collection.update_one(
                {'site': site, 'location': location, 'status': 'total'}, 
                {'$set': {
                    'count': total,
                    'last_modified': datetime.now(),
                }}, 
                upsert=True
            )

            #count.append((site, location, None, collection.count({'site': site, 'location': location})))
            for status in STATUSES:
                count = collection.count({'site': site, 'location': location, 'extracted': status})
                # Save to mongodb
                entry = db_collection.update_one(
                    {'site': site, 'location': location, 'status': status},
                    {'$set': {
                        'count': count,
                        'last_modified': datetime.now(),
                    }}, 
                    upsert=True
                )

                #count.append((site, location, status, collection.count({'site': site, 'location': location, 'extracted': status})))


if __name__ == "__main__":
    get_db_status()
    #cursor = db_collection.find({'count':{'$gt':0}})
    #for c in cursor:
    #    print c

