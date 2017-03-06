'test downloader classes'

import os
import unittest
from flow.downloaders.downloader import DownloaderDirector
from flow.downloaders.raukuten_downloader import RaukutenDownloader
from flow.downloaders.lazada_downloader import LazadaDownloader
from flow.downloaders.zalora_downloader import ZaloraDownloader
import flow.configures.asos_conf as asos_conf
import flow.configures.lazada_conf as lazada_conf
import flow.configures.zalora_conf as zalora_conf
import flow.test.arguments as test


class TestDownloader(unittest.TestCase):
    '''TestDownloader class'''

    def setUp(self):
        self.download_dir = os.path.join(test.TESTARGS['tmpdir'], 'downloads')
        self.log_dir = os.path.join(self.download_dir, 'logs')

        if not os.path.isdir(self.download_dir):
            os.mkdir(self.download_dir)
        if not os.path.isdir(self.log_dir):
            os.mkdir(self.log_dir)

    def test_raukuten_downloader(self):
        'test raukuten downloader'
        kwargs = asos_conf.OP_KWARGS.copy()
        kwargs.update({'log_path': self.log_dir,
                       'download_path': self.download_dir,
                       'download_file': os.path.join(
                           self.download_dir,
                           (kwargs['site'] + '.' + kwargs['country'] + '.txt')),
                       'log_level_file': 'debug',
                       'log_level_stdout': 'info',
                       'log_file_size_in_bytes': 0x100000})

        downloader = RaukutenDownloader(kwargs)
        self.assertIsNone(DownloaderDirector.construct(downloader))

    def test_lazada_downloader(self):
        'test lazada downloader'
        kwargs = lazada_conf.OP_KWARGS.copy()
        kwargs['country'] = 'singapore'
        kwargs.update({'log_path': self.log_dir,
                       'download_path': self.download_dir,
                       'download_file': os.path.join(
                           self.download_dir,
                           (kwargs['site'] + '.' + kwargs['country'] + '.txt')),
                       'feed_url': 'http://lap.lazada.com/datafeed2/download.php?affiliate=69829&country=sg&cat1=%22Fashion%22&cat2=%22Men%22%2C%22Women%22&cat3=%22Clothing%22&price=0&app=0',
                       'log_level_file': 'debug',
                       'log_level_stdout': 'debug',
                       'log_file_size_in_bytes': 0x100000})

        downloader = LazadaDownloader(kwargs)
        self.assertIsNone(DownloaderDirector.construct(downloader))


    def test_zalora_downloader(self):
        'test zalora downloader'
        kwargs = zalora_conf.OP_KWARGS.copy()
        kwargs['country'] = 'singapore'
        kwargs.update({'log_path': self.log_dir,
                       'download_path': self.download_dir,
                       'download_file': os.path.join(
                           self.download_dir,
                           (kwargs['site'] + '.' + kwargs['country'] + '.txt')),
                       'search_word': 'ZALORA_SG-Product_Feed.txt.g',
                       'log_level_file': 'debug',
                       'log_level_stdout': 'debug',
                       'log_file_size_in_bytes': 0x100000})

        downloader = ZaloraDownloader(kwargs)
        self.assertIsNone(DownloaderDirector.construct(downloader))

