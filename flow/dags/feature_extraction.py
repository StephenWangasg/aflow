'feature extraction'

import time
import os
import sys
import urllib2
import socket
import httplib
import threading
from PIL import Image
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from utils import get_task_id
from flow.configures import conf
from flow.utilities.access import Access
from flow.utilities.logger import FlowLogger
from flow.utilities.utils import download_image_from_url, push2aws, ProductFeature


FEATURE_EXTRACTION_ARGS = conf.get_dag_args('feature')
FEATURE_EXTRACTION_ARGS['schedule_interval'] = '@once'
FEATURE_EXTRACTION_DAG = DAG(
    'feature_extraction', default_args=FEATURE_EXTRACTION_ARGS)


class FeatureExtractor:
    'feature extraction class'

    class EThread(threading.Thread):
        'an feature extraction thread'

        def __init__(self, extractor, id):
            threading.Thread.__init__(self)
            self.thread_id = id
            self.extractor = extractor

        def run(self):
            self.extractor.run(self.thread_id)

    def __init__(self, kwargs):
        self.kwargs = kwargs
        self.accessor = Access(kwargs)

    def run(self, tid):
        'iterating the mongodb extract features for all images'
        kwargs = self.kwargs
        accessor = self.accessor
        log_path = os.path.join(kwargs['log_path'], 'feature' + str(tid))
        kwargs['logger'] = FlowLogger('extract', 'feature', log_path,
                                      '', 'debug', 'disable', 0xF00000, 20)
        thumbnail_size = 1000, 1000
        thumbnail_quality = 80
        while True:
            try:
                product = accessor.products.find_and_modify(
                    query={'extracted': False},
                    update={"$set": {'extracted': "processing",
                                     'resized': 'processing'}},
                    upsert=False,
                    full_response=True)['value']

                if not product:
                    kwargs['logger'].info(
                        'No record to process. Sleeping 5 minutes')
                    time.sleep(300)
                    continue

                img_path = product['image_path']
                kwargs['logger'].debug(img_path)
                if not os.path.isfile(img_path):
                    try:
                        download_image_from_url(product['image_url'], img_path)
                    except (ValueError, httplib.HTTPException):
                        kwargs['logger'].error(
                            'value error (%s)', product['image_url'])
                        accessor.products.update_one({'image_path': img_path}, {
                            '$set': {'extracted': 'download_error_url'}})
                        continue
                    except urllib2.HTTPError:
                        kwargs['logger'].error(
                            'Http error (%s)', product['image_url'])
                        accessor.products.update_one({'image_path': img_path}, {
                            '$set': {'extracted': 'download_error_url_404'}})
                        continue
                    except socket.timeout:
                        kwargs['logger'].error(
                            'timeout (%s)', product['image_url'])
                        accessor.products.update_one(
                            {'image_path': img_path},
                            {'$set': {'extracted': 'download_error_url_timeout'}})
                        continue
                    except:
                        raise

                img_name_with_ext = product['image_name']
                img_name, _ = os.path.splitext(img_name_with_ext)
                thumbnail_path = img_path + '_thumbnail.jpg'
                try:
                    image = Image.open(img_path)
                    image.thumbnail(thumbnail_size, Image.ANTIALIAS)
                    image.save(thumbnail_path, "JPEG",
                               quality=thumbnail_quality)
                    thumbnail_url = push2aws(thumbnail_path, img_name)
                    accessor.products.update_one(
                        {'image_path': img_path},
                        {'$set': {'image_url_old': product['image_url'],
                                  'image_url': thumbnail_url, 'resized': True}})
                except IOError:
                    kwargs['logger'].error(
                        'io error {} - {}'.format(sys.exc_info(), product['image_url']))
                    accessor.products.update_one(
                        {'image_path': img_path},
                        {'$set': {'resized': "IOError", 'extracted': 'resize error'}})
                    continue
                except:
                    raise

                features = ProductFeature(kwargs).get_feature(img_path)
                features['extracted'] = True
                accessor.products.update_one(
                    {'image_path': img_path}, {'$set': features})

                if os.path.isfile(img_path):
                    os.remove(img_path)

                if os.path.isfile(thumbnail_path):
                    os.remove(thumbnail_path)
            except SyntaxError:
                kwargs['logger'].error(
                    'syntax error {} - {}'.format(sys.exc_info(), product['image_url']))
                accessor.products.update_one({'image_path': img_path}, {
                    '$set': {'extracted': 'server_error'}})
            except:
                kwargs['logger'].error(
                    'error {} - {}'.format(sys.exc_info(), product['image_url']))
                raise

    def extract(self):
        'Entrance function for feature extraction'
        threads = set()
        for num in range(self.kwargs['extraction_threads'] - 1):
            threads.add(FeatureExtractor.EThread(self, num + 1))
        for thread in threads:
            thread.start()
        self.run(self.kwargs['extraction_threads'])

TASK1 = PythonOperator(
    task_id=get_task_id('extract', conf.CONFIGS),
    provide_context=True,
    python_callable=lambda **kwargs: FeatureExtractor(kwargs).extract(),
    op_kwargs=conf.CONFIGS,
    dag=FEATURE_EXTRACTION_DAG)
