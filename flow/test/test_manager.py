'''test manager class'''

import os
import unittest
import shutil
import flow.configures.asos_conf as asos_conf
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

    def test_manager(self):
        'test manager class'

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

        manager = Manager(kwargs)
        manager.update_insert_delete_urls()

        counts = manager.kwargs['accessor'].products.count()

        ind = 0
        for prod in manager.kwargs['accessor'].products.find():
            if ind > counts // 2:
                break
            manager.kwargs['accessor'].products.delete_one(prod)
            ind += 1

        news, dels, upds = manager.update_insert_delete_urls()

        self.assertTrue(news == ind)
        self.assertTrue(dels == 0)
        self.assertTrue(upds == counts - ind)
