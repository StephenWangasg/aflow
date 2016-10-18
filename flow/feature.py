import time, os
from flow.config import segmentation_server, classification_server, collection, feed_images_path
from requests.exceptions import ConnectionError
from flow.utils import ProductFeature, download_image_from_url

def redis_to_mongo():
    Features = ProductFeature(segmentation_server, classification_server)
    while True:
        try:
            product = collection.find_one({'extracted': False}, {'image_path': 1, 'image_url': 1})
            img_path = product['image_path']
            if not os.path.isfile(img_path):
                try:
                    download_image_from_url(product['image_url'], img_path)
                except (KeyboardInterrupt, SystemExit):
                    raise
                except Exception as e:
                    print e
                    raise
            features = Features.get_feature(img_path)
            features['extracted'] = True
            collection.update_one({'image_path': img_path}, {'$set': features})
        except (KeyboardInterrupt, SystemExit):
            raise
        except ConnectionError as e:
            print e
            time.sleep(600)
        except SyntaxError, e:
            print e
            collection.update_one({'image_path': img_path}, {'$set': {'extracted':None}})
            raise
        except Exception as e:
            print e
            raise
def change_paths():
    for row in collection.find({},{'image_path':1, 'image_name':1}):
        if 'new_models' in row['image_path']:
            img_path = feed_images_path + row['image_name']
            print img_path
#            break
            collection.update_one({'image_name': row['image_name']}, {'$set': {'image_path':img_path}})

if __name__ == '__main__':
#    redis_to_mongo()
    change_paths()
