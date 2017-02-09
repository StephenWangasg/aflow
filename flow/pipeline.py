import csv, eventlet, uuid, datetime
from flow.config import collection, feed_images_path, _db
from flow.utils import download_image, get_hashed_st
import pymongo

def get_unique_urls_from_db(**kwargs):
    """
    Query database, return a set of urls.
    """
    return {row['unique_url'] for row in collection.find(
        {'site':kwargs['website'], 'location':kwargs['country']},
        {'unique_url':1})}

def get_unique_urls_from_csv(**kwargs):
    """
    Extract parser csv, return a set of urls.
    """
    new_csv = csv.DictReader(open(kwargs['new_parsed_csv'], 'rb'), delimiter='\t')
    return {row['unique_url'] for row in new_csv}

def get_diff_urls(**kwargs):
    """
    Calculate 3 URL sets:
    delete_urls: to be deleted from database
    new_urls: to be inserted into database
    same_urls: to be updated in the database
    """
    previous_unique_urls = get_unique_urls_from_db(**kwargs)
    new_unique_urls = get_unique_urls_from_csv(**kwargs)

    if new_unique_urls is None or len(new_unique_urls) == 0:
        # when download error happens, no new urls parsed from previous step
        delete_urls = set()
        new_urls = set()
        same_urls = set()
    else: # normal url comparision operation
        delete_urls = previous_unique_urls - new_unique_urls
        new_urls = new_unique_urls - previous_unique_urls
        same_urls = new_unique_urls & previous_unique_urls

    return new_urls, delete_urls, same_urls

def update_insert_delete_urls(**kwargs):
    """
    Update database based on 3 url sets.
    Delete urls in delete_urls set
    Insert urls in new_urls set
    Update urls in same_urls set
    """
    current_parsed_path = kwargs['new_parsed_csv']
    website = kwargs['website']
    country = kwargs['country']
    image_paths = []

    new_urls, delete_urls, same_urls = get_diff_urls(**kwargs)

    for delete_url in delete_urls:
        print 'removing url ', delete_url
        collection.delete_one({'unique_url': delete_url})

    for row in csv.DictReader(open(current_parsed_path, 'rb'), delimiter='\t'):
        if len(new_urls) > 0 and row["unique_url"] in new_urls:
            row.update({'extracted': False, 'location': country, 'site': website})
            row['image_name'] = str(uuid.uuid1()) + '.jpg'
            row['image_path'] = feed_images_path + row['image_name']
            row['hashedId'] = get_hashed_st(row['image_url'])
            try:
                collection.insert(row)
            except pymongo.errors.DuplicateKeyError:
                continue
            image_paths.append((row['image_url'], row['image_path']))
        elif len(same_urls) > 0 and row['unique_url'] in same_urls:
            collection.update_one(
                {'unique_url': row['unique_url']},
                {'$set':{'display_price':row['display_price']}})

    _db['ingestion'].update_one(
        {
            'site': kwargs['website'],
            'location':kwargs['country']
        },
        {
            '$push':{
                'counts':{
                    'date': datetime.datetime.utcnow(),
                    'newCount':len(new_urls),
                    'deleteCount': len(delete_urls),
                    'overlapCount': len(same_urls)
                    }}
        }, upsert=True)

    pool = eventlet.GreenPool()
    for _ in pool.imap(download_image, image_paths[:1000]): pass
