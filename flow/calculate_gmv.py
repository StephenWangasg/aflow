from datetime import datetime
from pymongo import MongoClient

websites = ['lazada', 'asos', 'farfetch', 'yoox', 'zalora', 'swap', 'flipkart', 'target', 'luisaviaroma']
countries = ['singapore', 'global', 'indonesia', 'malaysia', 'india']

mongo_client = MongoClient()
db = mongo_client['fashion']
products = db['products']
gmvs = db['gmvs']


def calculate_gmv_single(site, location):
    records = products.find({'site':site, 'location':location, 'extracted':True})
    gmv = 0.0
    count = 0
    currency = None
    for record in records:
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


def calculate_gmv(**kwargs):
    for site in websites:
        for location in countries:
            calculate_gmv_single(site, location)

if __name__ == "__main__":
    #calculate_gmv()
    calculate_gmv_single('swap', 'singapore')
