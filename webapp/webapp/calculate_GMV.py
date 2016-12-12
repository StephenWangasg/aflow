from pymongo import MongoClient
from django import db
from django.http import HttpResponse

mongo_client_ = MongoClient()
_db = mongo_client_['fashion']
collection = _db['products']

for site in ['lazada', 'asos', 'farfetch', 'yoox', 'zalora']:
    for location in ['singapore', 'global', 'indonesia', 'malaysia']:
	c1 = collection.find({'site':site, 'location':location, 'extracted':True})
	gmv = 0.0
	count = 0
	for record in c1:
	    gmv += float(record['display_price'])
	    count += 1

	if count > 0:
            print site +','+ location +','+str(count)+','+ str(gmv)
