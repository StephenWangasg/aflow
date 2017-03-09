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

    exit_now = False

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

    def download(self, image_url, image_path):
        try:
            if os.path.isfile(image_path):
                return True
            kwargs = self.kwargs
            accessor = self.accessor
            kwargs['logger'].debug('Download (%s) -> (%s)', image_url, image_path)
            download_image_from_url(image_url, image_path)
            return True
        except (ValueError, httplib.HTTPException):
            kwargs['logger'].error(
                'download value error (%s)', image_url, exc_info=True)
            accessor.products.update_one({'image_path': image_path}, {
                '$set': {'extracted': 'download_error_url'}})
        except urllib2.HTTPError:
            kwargs['logger'].error(
                'download Http error (%s)', image_url, exc_info=True)
            accessor.products.update_one({'image_path': image_path}, {
                '$set': {'extracted': 'download_error_url_404'}})
        except socket.timeout:
            kwargs['logger'].error(
                'download timeout (%s)', image_url, exc_info=True)
            accessor.products.update_one({'image_path': image_path}, {
                '$set': {'extracted': 'download_error_url_timeout'}})
        except:
            kwargs['logger'].error(
                'download error (%s)', image_url, exc_info=True)
            accessor.products.update_one({'image_path': image_path}, {
                '$set': {'extracted': 'download_error_other'},
                '$inc': {'error_count': 1}})
        return False

    def run(self, tid, exit_on_error=False):
        'iterating the mongodb extract features for all images'
        kwargs = self.kwargs
        accessor = self.accessor
        log_path = os.path.join(kwargs['log_path'], 'feature' + str(tid))
        kwargs['logger'] = FlowLogger('extract', 'feature', log_path,
                                      '', 'debug', 'disable', 0xF00000, 20)
        thumbnail_size = 1000, 1000
        thumbnail_quality = 80
        while not FeatureExtractor.exit_now:
            try:
                product = accessor.products.find_one_and_update({'extracted': False},{
                    '$set': {'extracted': "processing"}})

                if not product:
                    product = accessor.products.find_one_and_update({'error_count':1},{ 
                        '$set': {'extracted': 'processing'}})

                if not product:
                    product = accessor.products.find_one_and_update({'error_count':2},{
                        '$set': {'extracted': 'processing'}})
                
                if not product:
                    kwargs['logger'].info('No record to process. Sleeping 5 minutes')
                    time.sleep(300)
                    continue

                if not self.download(product['image_url'], product['image_path']):
                    continue

                image_path=product['image_path']
                img_name_with_ext = product['image_name']
                img_name, _ = os.path.splitext(img_name_with_ext)
                thumbnail_path = image_path + '_thumbnail.jpg'
                try:
                    accessor.products.update_one({'image_path':image_path},{
                        '$set': {'resized': 'processing'}})
                    image = Image.open(image_path)
                    image.thumbnail(thumbnail_size, Image.ANTIALIAS)
                    image.save(thumbnail_path, "JPEG", quality=thumbnail_quality)
                    thumbnail_url = push2aws(thumbnail_path, img_name)
                    accessor.products.update_one({'image_path': image_path},{
                        '$set': {'image_url_old': product['image_url'],
                                 'image_url': thumbnail_url, 'resized': True}})
                except:
                    kwargs['logger'].error(
                        'resize error (%s)', product['image_url'], exc_info=True)
                    accessor.products.update_one({'image_path': image_path},{
                        '$set': {'resized': "IOError", 'extracted': 'resize error'}})
                    continue

                features = ProductFeature(kwargs).get_feature(image_path)
                features['extracted'] = True
                accessor.products.update_one({'image_path': image_path}, {'$set': features})

                if os.path.isfile(image_path):
                    os.remove(image_path)

                if os.path.isfile(thumbnail_path):
                    os.remove(thumbnail_path)
            except:
                kwargs['logger'].error(
                    'extract error {%s}',  product['image_url'], exc_info=True)
                accessor.products.update_one({'image_path': image_path}, {
                    '$set': {'extracted': 'server_error'}})
                if exit_on_error:
                    raise

    def extract(self):
        'Entrance function for feature extraction'
        threads = set()
        for num in range(self.kwargs['extraction_threads'] - 1):
            threads.add(FeatureExtractor.EThread(self, num + 1))
        for thread in threads:
            thread.start()
        while True:
            try:
                self.run(self.kwargs['extraction_threads'], True)
            except (KeyboardInterrupt, SystemExit):
                FeatureExtractor.exit_now=True
                for thread in threads:
                    thread.join()
                break
            except:
                pass
        self.kwargs['logger'].warning('Feature extractor is exiting...')

TASK1 = PythonOperator(
    task_id=get_task_id('extract', conf.CONFIGS),
    provide_context=True,
    python_callable=lambda **kwargs: FeatureExtractor(kwargs).extract(),
    op_kwargs=conf.CONFIGS,
    dag=FEATURE_EXTRACTION_DAG)
