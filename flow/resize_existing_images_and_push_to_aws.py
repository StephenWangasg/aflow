import time, os
from flow.config import segmentation_server, classification_server, collection, feed_images_path
from requests.exceptions import ConnectionError
from flow.utils import ProductFeature, download_image_from_url, push2aws
import urllib2, socket
from PIL import Image
 
def _feature_extraction():
    thumbnail_size = 1000,1000
    thumbnail_quality = 80
    count = 0
    succeeded = 0
    while True:
        try:
	    count += 1
            product = collection.find_and_modify(query={'resized': False, 'extracted':True}, update={"$set": {'resized': "processing"}},
                                       upsert=False, full_response=True)['value']
            if product is None:
		time.sleep(1)
		continue
	
	    img_path = product['image_path']
	    img_url = product['image_url']
	    thumbnail_path = img_path + '_thumbnail.jpg'
	    img_name_with_ext = product['image_name']
	    img_name, _ = os.path.splitext(img_name_with_ext)
	    try:
		# create thumbnail
		image = Image.open(img_path)
		image.thumbnail(thumbnail_size, Image.ANTIALIAS)
		image.save(thumbnail_path, "JPEG", quality=thumbnail_quality)
        	# upload to aws
		thumbnail_url = push2aws(thumbnail_path, img_name)
	        collection.update_one({'image_path': img_path}, {'$set': {'image_url_old': img_url, 'image_url': thumbnail_url, 'resized':True}})
                succeeded +=1
            except IOError:
                collection.update_one({'image_path':img_path},{'$set':{'resized':"IOError"}})
	    except Exception as e:
		print "image resizing error"
		print e
                
#		collection.update_one({'image_path': img_path}, {'$set': {'resized':"error", 'push2awsError':None}})
                raise

        except (KeyboardInterrupt, SystemExit):
            raise
        except Exception as e:
            print e
            raise
            print img_path
        print count, succeeded

def revert2old():
    for p in collection.find({'extracted':True},{'image_path':1, 'image_url_old':1, 'resized':1}):
        if p.has_key('resized')  and p.has_key('image_url_old') and p['resized']:
            collection.update_one({'image_path': p['image_path']}, {'$set': {'image_url': p['image_url_old'], 'resized':False}})
            print 'd'
if __name__ == '__main__':
    _feature_extraction()
    #revert2old()
