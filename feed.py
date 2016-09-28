import csv, sys, shutil, uuid, eventlet
from downloaders import download_and_parse
from config import feed_list, data_feed_path, feed_images_path
from tools import download_image, get_hashed_st, scheduler
from config import collection, imgQ
csv.field_size_limit(sys.maxsize)


def run_feed_list():
    for feed_item in feed_list:
        website = feed_item['website']
        for country_item in feed_item['countries']:
            country = country_item['name']
            print country, website
            current_parsed_path, previous_parsed_path = download_and_parse(website, country, country_item, feed_item)
            current_csv = csv.DictReader(open(current_parsed_path, 'rb'), delimiter='\t')
            current_product_urls = [_['unique_url'] for _ in current_csv]

            try:
                previous_csv = csv.DictReader(open(previous_parsed_path, 'rb'), delimiter='\t')
                previous_product_urls = [_['unique_url'] for _ in previous_csv]
            except IOError:
                previous_product_urls = []

            delete_urls = set(previous_product_urls) - set(current_product_urls)
            new_urls = set(current_product_urls) - set(previous_product_urls)
            print "To delete : ", len(delete_urls), " To insert : ", len(new_urls)

            for delete_url in list(delete_urls):
                    collection.remove({'unique_url': delete_url})

            # new_urls = set(list(new_urls)[:200])#remove
            if len(new_urls) > 0:
                mapped_rows, image_paths = [], []

                for row in csv.DictReader(open(current_parsed_path, 'rb'), delimiter='\t'):
                    url = row["unique_url"]
                    if url in new_urls:
                        row.update({'extracted': False, 'location': country, 'site': website})
                        row['image_name'] = str(uuid.uuid1()) + '.jpg'
                        row['image_path'] = feed_images_path + row['image_name']
                        row['hashedId'] = get_hashed_st(row['image_url'])
                        mapped_rows.append(row)
                        image_paths.append((row['image_url'], row['image_path']))

                pool = eventlet.GreenPool()
                for _ in pool.imap(download_image, image_paths):
                    pass
                for row in mapped_rows:
                    collection.insert(row)
                    imgQ.sadd("insertQ", row["image_path"])

            shutil.copyfile(current_parsed_path, previous_parsed_path)


def run_daily():
    for _ in scheduler(4):
        run_feed_list()


if __name__ == '__main__':
    run_feed_list()
    pass
