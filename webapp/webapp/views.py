from pymongo import MongoClient
from django import db
from django.http import HttpResponse
from django.shortcuts import render
from datetime import datetime

mongo_client_ = MongoClient()
_db = mongo_client_['fashion']
collection = _db['products']
gmv_collection = _db['gmvs']
db_status_collection = _db['db_status']


def send_response(response):
    response["Access-Control-Allow-Origin"] = '*'
    response["Access-Control-Allow-Headers"] = 'accept,content-type'
    db.reset_queries()
    return response


def get_db_status(request):
    records = db_status_collection.find()
    res_dict = {}
    for r in records:
        site = r['site']
        location = r['location']
        if site not in res_dict:
            res_dict[site] = {}
        if location not in res_dict[site]:
            res_dict[site][location] = {}
        res_dict[site][location][str(r['status'])] = r['count']


    res_list = []
    for site, site_dict in res_dict.iteritems():
        for location, location_dict in site_dict.iteritems():
            res = {
                'site': site,
                'location': location,
            }
            for status, count in location_dict.iteritems():
                res[status] = count
            res_list.append(res)

    def compare_res_dict(dict1, dict2):
        if dict1['site'] < dict2['site']:
            return -1
        elif dict1['site'] > dict2['site']:
            return 1
        else:
            if dict1['location'] < dict2['location']:
                return -1
            elif dict1['location'] > dict2['location']:
                return 1
            else: 
                return 0
    res_list.sort(cmp=compare_res_dict)

    return render(request, 'db_status.html', {
        'title': 'DB Status',
        'result': res_list,

    })


def get_gmvs(request):
    records = gmv_collection.find()

    return render(request, 'gmvs.html', {
        'title': 'GMVs',
        'records': records,

    })
