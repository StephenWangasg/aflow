import time, os
from flow.config import segmentation_server, classification_server, collection, feed_images_path
from requests.exceptions import ConnectionError
from flow.utils import ProductFeature, download_image_from_url
import urllib2, socket

def _feature_extraction(segmentation_server, classification_server):
    Features = ProductFeature(segmentation_server, classification_server)
    while True:
        try:
            product = collection.find_and_modify(query={'extracted': False}, update={"$set": {'extracted': "processing"}},
                                       upsert=False, full_response=True)['value']
            #            product = collection.find_one({'extracted': False}, {'image_path': 1, 'image_url': 1})
            img_path = product['image_path']
            print img_path
            if not os.path.isfile(img_path):
                try:
                    download_image_from_url(product['image_url'], img_path)
                except (KeyboardInterrupt, SystemExit):
                    raise
                except ValueError:
                    print "value error"
                    collection.update_one({'image_path': img_path}, {'$set': {'extracted': 'download_error_url'}})
                    continue
                except urllib2.HTTPError:
                    print "404 erroe "
                    collection.update_one({'image_path': img_path}, {'$set': {'extracted': 'download_error_url_404'}})
                    continue
                except socket.timeout:
                    print "timeout error"
                    collection.update_one({'image_path': img_path},
                                          {'$set': {'extracted': 'download_error_url_timeout'}})
                    continue
                except Exception as e:
                    print e
                    raise
            features = Features.get_feature(img_path)
            features['extracted'] = True
            collection.update_one({'image_path': img_path}, {'$set': features})
        except (KeyboardInterrupt, SystemExit):
            raise
            #        except ConnectionError as e:
            #            print e
            #            time.sleep(600)
        except SyntaxError, e:
            print os.path.getsize(img_path) > 0
            collection.update_one({'image_path': img_path}, {'$set': {'extracted': 'server_error'}})
            print "server error"
        except Exception as e:
            print e
            raise
            print img_path


def feature_extraction(**kwargs):
    segmentation_server = kwargs['segmentation_server']
    classification_server = kwargs['classification_server']
    _feature_extraction(segmentation_server, classification_server)

def extract_feature():
    seg = raw_input("segmentation server : ")
    clas = raw_input("classification server : ")
    segmentation_server = {'host': seg, 'port': '8000'}
    classification_server = {'host': clas, 'port': '8000'}
    _feature_extraction(segmentation_server, classification_server)

def change_paths():
    for row in collection.find({},{'image_path':1, 'image_name':1}):
        if 'new_models' in row['image_path']:
            img_path = feed_images_path + row['image_name']
#            break
            collection.update_one({'image_name': row['image_name']}, {'$set': {'image_path':img_path}})

if __name__ == '__main__':
    #extract_feature()
    _feature_extraction(segmentation_server, classification_server)
    #change_paths()
