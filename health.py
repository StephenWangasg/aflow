import csv, sys, shutil, uuid, eventlet, os
from downloaders import download_and_parse
from config import feed_list, data_feed_path, feed_images_path
from tools import download_image, get_hasded_st, scheduler
from config import collection, imgQ
csv.field_size_limit(sys.maxsize)
from collections import Counter


def is_db_sync_with_latest_feed():
    total_parsed_count = 0
    for feed_item in feed_list:
        website = feed_item['website']
        for country_item in feed_item['countries']:
            country = country_item['name']
#            print country, website
            current_parsed_path = data_feed_path + website + country + 'current.csv'
            current_csv = csv.DictReader(open(current_parsed_path, 'rb'), delimiter='\t')
            current_product_urls = [_['unique_url'] for _ in current_csv]
            total_parsed_count += len(current_product_urls)
            parsed_urls = set(current_product_urls)
            db_urls = set()
            for product in collection.find({},{'site':1,'location':1,'unique_url':1}):
                if product['site'] == website and product['location'] == country:
                    db_urls.add(product['unique_url'])
            if len(parsed_urls^db_urls) != 0:
                return False
    return total_parsed_count == collection.find().count()


def count_images_downloaded():
    db_images_count = collection.find().count()-0
    count = Counter()
    for product in collection.find({}, {'image_path':1, 'site':1, 'location':1}).limit(db_images_count):
        if not os.path.isfile(product['image_path']):
            count[product['site']+product['location']] += 1
    print db_images_count, count


def download_other_images():
    image_paths = []
    for row in collection.find({'extracted':False}, {'image_path': 1, 'image_url': 1}):
        if not os.path.isfile(row['image_path']):
            image_paths.append((row['image_url'], row['image_path']))
    print len(image_paths)
    pool = eventlet.GreenPool()
    for _ in pool.imap(download_image, image_paths):
        pass



def delete_redis():
    while True:
        product_id = imgQ.spop("insertQ")
        print product_id
        if product_id is None:
            break


def insert_redis():
    for product in collection.find({'extracted': False}, {'image_path': 1}):
        if os.path.isfile(product['image_path']):
            imgQ.sadd("insertQ", product["image_path"])


if __name__ == '__main__':

    # print "Is db in sync with latest feeds ? ", is_db_sync_with_latest_feed()
    count_images_downloaded()
    download_other_images()
    count_images_downloaded()
