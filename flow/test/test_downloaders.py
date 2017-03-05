'test downloader classes'

import os
import unittest
from flow.downloaders.downloader import DownloaderDirector
from flow.downloaders.raukuten_downloader import RaukutenDownloader
import flow.configures.asos_conf as asos_conf
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
