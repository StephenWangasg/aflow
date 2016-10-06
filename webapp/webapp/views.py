import requests
from django.http import JsonResponse
import redis, ast
from datetime import datetime
currency_cache = redis.StrictRedis(host='localhost', port=6379, db=0)
from django import db

def send_response(response):
    response["Access-Control-Allow-Origin"] = '*'
    response["Access-Control-Allow-Headers"] = 'accept,content-type'
    db.reset_queries()
    return response


def get_current_rates():
    sources = ['USD', 'AUD', 'GBP']
    conversions = {}
    for source in sources:
        payload = {
            'access_key': '68ed2e50d616f09954f0906bfe509904',
            'source': source,
            'currencies': 'USD,SGD,MYR,IDR'
        }
        r = requests.get('http://apilayer.net/api/live', params=payload)
        conversions.update(r.json()['quotes'])
    return conversions


def cache_currency_with_time():
    conversions = get_current_rates()
    t = str(datetime.now())
    currency_cache.set('currencies', str(conversions))
    currency_cache.set('currency_time', t)
    return conversions


def get_currency_conversion(request):
    cached_time = currency_cache.get('currency_time')

    if (cached_time == 'None') or cached_time == None:
        conversions = cache_currency_with_time()
    else:
        cached_time = currency_cache.get('currency_time')
        cached_time = datetime.strptime(cached_time, '%Y-%m-%d %H:%M:%S.%f')
        elapsed_time = datetime.now() - cached_time
        if divmod(elapsed_time.total_seconds(), 60*24)[0]>24.0:
            conversions = cache_currency_with_time()
        else:
            exist = currency_cache.get('currencies')
            conversions = ast.literal_eval(exist)
    return send_response(JsonResponse({'conversions': conversions}))
