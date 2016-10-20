import csv, eventlet, uuid, hashlib, urllib2, shutil
from flow.config import collection, feed_images_path
from config import segmentation_server, classification_server
from flow.utils import ProductFeature, download_image, get_hashed_st


def delete_old_urls(**kwargs):
    ti = kwargs['ti']
    delete_urls = ti.xcom_pull(key='delete_urls', task_ids='get_diff_urls')
    for delete_url in list(delete_urls):
        collection.remove({'unique_url': delete_url})


def download_images(**kwargs):
    ti = kwargs['ti']
    image_paths = ti.xcom_pull(key='image_paths', task_ids='insert_new_urls')
    pool = eventlet.GreenPool()
    for _ in pool.imap(download_image, image_paths):
        pass


def insert_new_urls(**kwargs):
    current_parsed_path = kwargs['current_parsed_csv']
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


def copy_current2previous(**kwargs):
    current_parsed_path = kwargs['current_parsed_csv']
    previous_parsed_path = kwargs['previous_parsed_csv']
    shutil.copyfile(current_parsed_path, previous_parsed_path)


def get_diff_urls(**kwargs):
    current_parsed_path = kwargs['current_parsed_csv']
    previous_parsed_path = kwargs['previous_parsed_csv']
    current_csv = csv.DictReader(open(current_parsed_path, 'rb'), delimiter='\t')
    current_product_urls = [_['unique_url'] for _ in current_csv]
    try:
        previous_csv = csv.DictReader(open(previous_parsed_path, 'rb'), delimiter='\t')
        previous_product_urls = [_['unique_url'] for _ in previous_csv]
    except IOError:
        previous_product_urls = []
    delete_urls = set(previous_product_urls) - set(current_product_urls)
    new_urls = set(current_product_urls) - set(previous_product_urls)
    kwargs['ti'].xcom_push(key='delete_urls', value=delete_urls)
    kwargs['ti'].xcom_push(key='new_urls', value=new_urls)


def feature_extraction(**kwargs):
    ti = kwargs['ti']
    image_paths = ti.xcom_pull(key='image_paths', task_ids='insert_new_urls')
    Features = ProductFeature(segmentation_server, classification_server)
    for (_, img_path) in image_paths:
        try:
            features = Features.get_feature(img_path)
            features['extracted'] = True
            collection.update_one({'image_path': img_path}, {'$set': features})
        except (KeyboardInterrupt, SystemExit):
            raise
        except Exception as e:
            print e
            raise
