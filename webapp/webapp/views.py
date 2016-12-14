import csv
import redis
import ast

from flow import config


from pymongo import MongoClient
from django import db
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET
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


@require_GET
def get_db_status(request):
    return render(request, 'db_status.html', {
        'title': 'DB Status',
        'result': query_db_status(),
    })


@require_GET
def export_db_status(request):
    response = HttpResponse(content_type='text/csv')
    filename = 'db_status_' + datetime.now().isoformat()
    response['Content-Disposition'] = 'attachment; filename="' + filename + '.csv"'

    writer = csv.writer(response)
    writer.writerow([
        'Site', 
        'Location', 
        'Count', 
        'Feature extracted', 
        'To be extracted',
        'Not proper image URL',
        '404 on image URL',
        'Timeout for download',
        'Server error',])

    records = query_db_status()
    for r in records:
        if r['total'] > 0:
            writer.writerow([
                r['site'], 
                r['location'], 
                r['total'], 
                r['True'],
                r['False'],
                r['download_error_url'],
                r['download_error_url_404'],
                r['download_error_url_timeout'],
                r['server_error'],
            ])

    return response

@require_GET
def get_gmvs(request):
    return render(request, 'gmvs.html', {
        'title': 'GMVs',
        'records': query_gmvs(),
    })


@require_GET
def export_gmvs(request):
    response = HttpResponse(content_type='text/csv')
    filename = 'gmvs_' + datetime.now().isoformat()
    response['Content-Disposition'] = 'attachment; filename="' + filename + '.csv"'

    writer = csv.writer(response)
    writer.writerow(['Site', 'Location', 'Count', 'GMV (Default currency)', 'GMV (USD)',])

    records = query_gmvs()
    for r in records:
        if r['count'] > 0:
            writer.writerow([r['site'], r['location'], r['count'], r['gmv'], r['usd'],])

    return response


def query_db_status():
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

    res_list.sort(cmp=compare_res_dict)

    # Calculate total
    count_total = 0
    count_extracted = 0
    count_not_extracted = 0
    count_download_error_url = 0
    count_download_error_url_404 = 0
    count_download_error_url_timeout = 0
    count_server_error = 0

    for r in res_list:
        count_total += r['total']
        count_extracted += r['True']
        count_not_extracted += r['False']
        count_download_error_url += r['download_error_url']
        count_download_error_url_404 += r['download_error_url_404']
        count_download_error_url_timeout += r['download_error_url_timeout']
        count_server_error += r['server_error']

    res_list.append({
        'site': 'Total',
        'location': '',
        'total': count_total,
        'True': count_extracted,
        'False': count_not_extracted,
        'download_error_url': count_download_error_url,
        'download_error_url_404': count_download_error_url_404,
        'download_error_url_timeout': count_download_error_url_timeout,
        'server_error': count_server_error,
    })

    return res_list


def query_gmvs():
    currency_cache = redis.StrictRedis(host=config.query_server['host'], port=6379, db=0)
    exist = currency_cache.get('currencies')
    conversions = ast.literal_eval(exist)

    records = gmv_collection.find()
    res_list = []
    # Calculate GMV in USD
    for r in records:
        key = r['currency'] + 'USD' 
        mult = conversions[key]
        res = {
            'site': r['site'],
            'location': r['location'],
            'count': r['count'],
            'currency': r['currency'],
            'gmv': r['gmv'],
            'usd': r['gmv'] * mult,
        }
        res_list.append(res)

    res_list.sort(cmp=compare_res_dict)
       
    # Calculate total
    count_total = 0
    gmv_total = 0.0
    for r in res_list:
        count_total += r['count']
        gmv_total += r['usd']
    res_list.append({
        'site': 'Total',
        'location': '',
        'count': count_total,
        'gmv': '',
        'usd': gmv_total,
    })
    return res_list

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
