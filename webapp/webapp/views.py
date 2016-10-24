from pymongo import MongoClient
from django import db
from django.http import HttpResponse

mongo_client_ = MongoClient()
_db = mongo_client_['fashion']
collection = _db['products']


def send_response(response):
    response["Access-Control-Allow-Origin"] = '*'
    response["Access-Control-Allow-Headers"] = 'accept,content-type'
    db.reset_queries()
    return response


def get_db_status(request):
    h = "<html><body>"
    h += '<table border="1"><tr>'
    h += '<th>Site </th>'
    h += '<th>Location </th>'
    h += '<th>Count </th>'
    h += '<th>Feature extracted </th>'
    h += '<th>To be extracted </th>'
    h += '<th>Not proper image URL </th>'
    h += '<th>404 on image URL </th>'
    h += '<th>Timeout for download </th>'
    h += '<th>Server error </th></tr>'

    for site in ['lazada', 'asos', 'farfetch', 'yoox', 'zalora']:
        for location in ['singapore', 'global', 'indonesia', 'malaysia']:
            h += "<tr><th>%s </th>" % site
            h += "<th> %s </th>" % location
            h += "<th> %s </th>" % collection.find({'site':site, 'location':location}).count()
            h += "<th> %s </th>" % collection.find({'site':site, 'location':location, "extracted":True}).count()
            h += "<th> %s </th>" % collection.find({'site':site, 'location':location, "extracted":False}).count()
            h += "<th> %s </th>" % collection.find({'site':site, 'location':location, 'extracted': 'download_error_url'}).count()
            h += "<th> %s </th>" % collection.find({'site':site, 'location':location, 'extracted': 'download_error_url_404'}).count()
            h += "<th> %s </th>" % collection.find({'site':site, 'location':location, 'extracted': 'download_error_url_timeout'}).count()
            h += "<th> %s </th></tr>" % collection.find({'site':site, 'location':location, 'extracted': 'server_error'}).count()
    h += "<tr><th>%s </th>" % "total"
    h += "<th> %s </th>" % "count"
    h += "<th> %s </th>" % collection.find().count()
    h += "<th> %s </th>" % collection.find({"extracted": True}).count()
    h += "<th> %s </th>" % collection.find({"extracted": False}).count()
    h += "<th> %s </th>" % collection.find( {'extracted': 'download_error_url'}).count()
    h += "<th> %s </th>" % collection.find({'extracted': 'download_error_url_404'}).count()
    h += "<th> %s </th>" % collection.find({'extracted': 'download_error_url_timeout'}).count()
    h += "<th> %s </th></tr>" % collection.find({'extracted': 'server_error'}).count()

    h += "</table></body></html>"
    return send_response(HttpResponse(h))