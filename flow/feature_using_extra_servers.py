import time, os
from flow.config import segmentation_server, classification_server, collection, feed_images_path
from requests.exceptions import ConnectionError
from flow.utils import ProductFeature, download_image_from_url, push2aws
import urllib2, socket
from httplib import BadStatusLine
from PIL import Image

def _feature_extraction(segmentation_server, classification_server):
    Features = ProductFeature(segmentation_server, classification_server)
    thumbnail_size = 1000,1000
    thumbnail_quality = 80
    while True:
        try:
            product = collection.find_and_modify(
                query={'extracted': False}, 
                update={"$set": {'extracted': "processing", 'resized': 'processing'}},
                upsert=False, 
                full_response=True)['value']

            if product is None:
                print 'No record to process. Sleeping 5 seconds'
                time.sleep(5)
                continue

            img_path = product['image_path']
            print img_path
            if not os.path.isfile(img_path):
                try:
                    download_image_from_url(product['image_url'], img_path)
                except (KeyboardInterrupt, SystemExit):
                    raise
                except ValueError, BadStatusLine:
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
	    
	    img_name_with_ext = product['image_name']
	    img_name, _ = os.path.splitext(img_name_with_ext)
	    thumbnail_path = img_path + '_thumbnail.jpg'
	    try:
		image = Image.open(img_path)
	    	image.thumbnail(thumbnail_size, Image.ANTIALIAS)
	    	image.save(thumbnail_path, "JPEG", quality=thumbnail_quality)
	    	thumbnail_url = push2aws(thumbnail_path, img_name)
		collection.update_one(
                    {'image_path': img_path}, 
                    {'$set': {'image_url_old': product['image_url'], 'image_url': thumbnail_url, 'resized':True}})
	    except IOError:
                print "io erroe while pushing 2 aws"
                collection.update_one(
                    {'image_path':img_path},
                    {'$set':{'resized':"IOError", 'extracted':'resize error'}})
                continue
            except Exception as e:
                print e
                raise

	    features = Features.get_feature(img_path)
            features['extracted'] = True
            collection.update_one({'image_path': img_path}, {'$set': features})

        except (KeyboardInterrupt, SystemExit):
            raise
        except SyntaxError, e:
            collection.update_one({'image_path': img_path}, {'$set': {'extracted': 'server_error'}})
            print "server error"
        except Exception as e:
            print e
            raise


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


if __name__ == '__main__':
    extract_feature()
