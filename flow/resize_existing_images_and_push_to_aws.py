import time, os
from flow.config import segmentation_server, classification_server, collection, feed_images_path
from requests.exceptions import ConnectionError
from flow.utils import ProductFeature, download_image_from_url, push2aws
import urllib2, socket
from PIL import Image
 
def _feature_extraction(segmentation_server, classification_server):
    Features = ProductFeature(segmentation_server, classification_server)
    thumbnail_size = 500,500

    # add resized field, default is False
    count = 0
    succeeded = 0
    while True:
        try:
	    count += 1
            product = collection.find_and_modify(query={'resized': {'$exists': False}, 'extracted':True}, update={"$set": {'resized': "processing"}},
                                       upsert=False, full_response=True)['value']
            #            product = collection.find_one({'extracted': False}, {'image_path': 1, 'image_url': 1})
            img_path = product['image_path']
	    img_url = product['image_url']
	    thumbnail_path = img_path + '_thumbnail.jpg'

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

	    img_name_with_ext = product['image_name']
	    img_name, img_ext = os.path.splitext(img_name_with_ext)
	    thumbnail_url = ''
	    try:
		# create thumbnail
		image = Image.open(img_path)
		image.thumbnail(thumbnail_size, Image.ANTIALIAS)
		image.save(thumbnail_path, "JPEG")
        	# upload to aws
		thumbnail_url = push2aws(thumbnail_path, img_name)
	        collection.update_one({'image_path': img_path}, {'$set': {'image_url_old': img_url, 'img_url': thumbnail_url, 'resized':True}})
	    except Exception as e:
		print "image resizing error"
		print e
		continue

	    succeeded = 1
	    if count % 100 == 0:
		print 'processed', count, 'succeeded', succeeded
		print 'thumbnail_url:', thumbnail_url

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
    print 'processed', count, 'succeeded', succeeded


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
