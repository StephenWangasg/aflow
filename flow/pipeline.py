import csv, eventlet, uuid, hashlib, urllib2, shutil, datetime
from flow.config import collection, feed_images_path, _db
from config import segmentation_server, classification_server
from flow.utils import ProductFeature, download_image, get_hashed_st

ingestion_collection = _db['ingestion']

def delete_old_urls(**kwargs):
    ti = kwargs['ti']
    delete_urls = ti.xcom_pull(key='delete_urls', task_ids='get_diff_urls')
    for delete_url in list(delete_urls):
        collection.remove({'unique_url': delete_url})


def download_images(**kwargs):
    ti = kwargs['ti']
    image_paths = ti.xcom_pull(key='image_paths', task_ids='insert_new_urls')
    pool = eventlet.GreenPool()
    for _ in pool.imap(download_image, image_paths[:1000]):
        pass


def insert_new_urls(**kwargs):
    current_parsed_path = kwargs['new_parsed_csv']
    website = kwargs['website']
    country = kwargs['country']
    ti = kwargs['ti']
    new_urls = ti.xcom_pull(key='new_urls', task_ids='get_diff_urls')
#    new_urls = set(list(new_urls)[:200])  # remove
    image_paths = []
    if len(new_urls) > 0:
        for row in csv.DictReader(open(current_parsed_path, 'rb'), delimiter='\t'):
            url = row["unique_url"]
            if url in new_urls:
                row.update({'extracted': False, 'location': country, 'site': website})
                row['image_name'] = str(uuid.uuid1()) + '.jpg'
                row['image_path'] = feed_images_path + row['image_name']
                row['hashedId'] = get_hashed_st(row['image_url'])
                collection.insert(row)
                image_paths.append((row['image_url'], row['image_path']))
    kwargs['ti'].xcom_push(key='image_paths', value=image_paths)


def get_unique_urls_from_db(**kwargs):
    website = kwargs['website']
    country = kwargs['country']
    previous_unique_urls = set()
    for row in collection.find({'site':website, 'location':country},{'unique_url':1}):
        previous_unique_urls.add(row['unique_url'])
    kwargs['ti'].xcom_push(key='previous_unique_urls', value=previous_unique_urls)


def get_unique_urls_from_csv(**kwargs):
    new_parsed_path = kwargs['new_parsed_csv']
    new_csv = csv.DictReader(open(new_parsed_path, 'rb'), delimiter='\t')
    new_unique_urls = set([_['unique_url'] for _ in new_csv])
    kwargs['ti'].xcom_push(key='new_unique_urls', value=new_unique_urls)


def get_diff_urls(**kwargs):
    ti = kwargs['ti']
    new_unique_urls = ti.xcom_pull(key='new_unique_urls', task_ids='get_unique_urls_from_csv')
    previous_unique_urls = ti.xcom_pull(key='previous_unique_urls', task_ids='get_unique_urls_from_db')
    delete_urls = previous_unique_urls - new_unique_urls
    new_urls = new_unique_urls - previous_unique_urls
    ingestion_collection.update_one(
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
                    'overlapCount': len(new_unique_urls & previous_unique_urls)
                }
            }
        },
        upsert=True)
    kwargs['ti'].xcom_push(key='delete_urls', value=delete_urls)
    kwargs['ti'].xcom_push(key='new_urls', value=new_urls)