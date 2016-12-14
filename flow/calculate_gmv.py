from datetime import datetime
from pymongo import MongoClient

mongo_client = MongoClient()
db = mongo_client['fashion']
products = db['products']
gmvs = db['gmvs']


def calculate_gmv(**kwargs):
    for site in ['lazada', 'asos', 'farfetch', 'yoox', 'zalora']:
        for location in ['singapore', 'global', 'indonesia', 'malaysia']:
	    c1 = products.find({'site':site, 'location':location, 'extracted':True})
	    gmv = 0.0
	    count = 0
            currency = None
	    for record in c1:
	        gmv += float(record['display_price'])
	        count += 1
                if not currency:
                    currency = record['currency']

	    if count > 0:
                print site + ',' + location + ',' + str(count) + ',' + str(gmv) + ',' + currency
                # Save to mongodb
                entry = gmvs.update_one(
                    {'site': site, 'location': location}, 
                    {'$set': {
                        'count': count,
                        'gmv': gmv,
                        'currency': currency,
                        'last_modified': datetime.now(),
                    }}, 
                    upsert=True
                )


if __name__ == "__main__":
    calculate_gmv()
