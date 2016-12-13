from pymongo import MongoClient

mongo_client = MongoClient()
db = mongo_client['fashion']
db_status_collection = db['db_status']

def get_db_status():
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
        
    print res_dict

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
    return res_list


if __name__ == "__main__":
    print get_db_status()
