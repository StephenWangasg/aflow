import time
from config import segmentation_server, classification_server, imgQ, collection
from requests.exceptions import ConnectionError
from tools import ProductFeature

def redis_to_mongo():
    Features = ProductFeature(segmentation_server, classification_server)
    while True:
        try:
            img_path = imgQ.spop("insertQ")
            features = Features.get_feature(img_path)
            features['extracted'] = True
            collection.update_one({'image_path': img_path}, {'$set': features})
        except (KeyboardInterrupt, SystemExit):
            imgQ.sadd("insertQ", img_path)
            raise
        except TypeError:
            print "sleeping"
            time.sleep(60)
        except ConnectionError as e:
            print e
            imgQ.sadd("insertQ", img_path)
            time.sleep(600)
        except SyntaxError, e:
            print e
            collection.update_one({'image_path': img_path}, {'$set': {'extracted':None}})
            raise
        except Exception as e:
            print e
            imgQ.sadd("insertQ", img_path)
            raise
       

if __name__ == '__main__':
    redis_to_mongo()
