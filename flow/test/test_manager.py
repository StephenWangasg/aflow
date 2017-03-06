'''test manager class'''

import os
import unittest
import shutil
import flow.configures.asos_conf as asos_conf
import flow.configures.lazada_conf as lazada_conf
import flow.configures.zalora_conf as zalora_conf
import flow.test.arguments as test
from flow.managers.manager import Manager

class TestManager(unittest.TestCase):
    '''TestManager class'''

    def setUp(self):
        self.manager_dir = os.path.join(test.TESTARGS['tmpdir'], 'manager')
        self.log_dir = os.path.join(self.manager_dir, 'logs')

        if not os.path.isdir(self.manager_dir):
            os.mkdir(self.manager_dir)
        if not os.path.isdir(self.log_dir):
            os.mkdir(self.log_dir)

    def process(self, kwargs):
        'process'
        manager = Manager(kwargs)
        manager.kwargs['accessor'].products.delete_many(
            {'site': kwargs['site'], 'location': kwargs['country']})

        manager.update_insert_delete_urls()

        counts = manager.kwargs['accessor'].products.count(
            {'site': kwargs['site'], 'location': kwargs['country']})

        ind = 0
        for prod in manager.kwargs['accessor'].products.find(
                {'site': kwargs['site'], 'location': kwargs['country']}):
            if ind > (counts // 2):
                break
            manager.kwargs['accessor'].products.delete_one(prod)
            ind += 1

        news, dels, upds = manager.update_insert_delete_urls()

        self.assertTrue(news == ind)
        self.assertTrue(dels == 0)
        self.assertTrue(upds == counts - ind)

    def test_manager_asos_global(self):
        'test manager class with asos global data'

        kwargs = asos_conf.OP_KWARGS.copy()
        # copy parsed csv test/data/asos.global.csv
        filename = kwargs['site'] + '.' + kwargs['country'] + '.csv'
        filepath0 = os.path.join(test.TESTARGS['testdir'], 'data', filename)
        filepath1 = os.path.join(self.manager_dir, filename)

        shutil.copyfile(filepath0, filepath1)
        kwargs.update({'log_path': self.log_dir,
                       'parsed_file': filepath1,
                       'feed_images_path': os.path.join(self.manager_dir, 'feed_images'),
                       'mongo_host': 'localhost',
                       'mongo_port': 27017,
                       'log_level_stdout': 'info'})

        self.process(kwargs)

    def test_manager_lazada_singapore(self):
        'test manager class with lazada singapore data'

        kwargs = lazada_conf.OP_KWARGS.copy()
        kwargs['country'] = 'singapore'
        # copy parsed csv test/data/lazada.singapore.csv
        filename = kwargs['site'] + '.' + kwargs['country'] + '.csv'
        filepath0 = os.path.join(test.TESTARGS['testdir'], 'data', filename)
        filepath1 = os.path.join(self.manager_dir, filename)

        shutil.copyfile(filepath0, filepath1)
        kwargs.update({'log_path': self.log_dir,
                       'parsed_file': filepath1,
                       'feed_images_path': os.path.join(self.manager_dir, 'feed_images'),
                       'mongo_host': 'localhost',
                       'mongo_port': 27017,
                       'log_level_stdout': 'info'})

        self.process(kwargs)

    def test_manager_zalora_singapore(self):
        'test manager class with zalora singapore data'

        kwargs = zalora_conf.OP_KWARGS.copy()
        kwargs['country'] = 'singapore'
        # copy parsed csv test/data/zalora.singapore.csv
        filename = kwargs['site'] + '.' + kwargs['country'] + '.csv'
        filepath0 = os.path.join(test.TESTARGS['testdir'], 'data', filename)
        filepath1 = os.path.join(self.manager_dir, filename)

        shutil.copyfile(filepath0, filepath1)
        kwargs.update({'log_path': self.log_dir,
                       'parsed_file': filepath1,
                       'feed_images_path': os.path.join(self.manager_dir, 'feed_images'),
                       'mongo_host': 'localhost',
                       'mongo_port': 27017,
                       'log_level_stdout': 'info'})

        self.process(kwargs)

