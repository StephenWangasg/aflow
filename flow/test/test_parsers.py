'test filter classes'

import os
import unittest
import shutil
from flow.parsers.parser import Parser
from flow.parsers.raukuten_filter import RaukutenFilter
from flow.parsers.lazada_filter import LazadaFilter
from flow.parsers.zalora_filter import ZaloraFilter
import flow.configures.asos_conf as asos_conf
import flow.configures.lazada_conf as lazada_conf
import flow.configures.zalora_conf as zalora_conf
import flow.test.arguments as test


class TestParser(unittest.TestCase):
    '''TestParser class'''

    def setUp(self):
        self.parser_dir = os.path.join(test.TESTARGS['tmpdir'], 'parsers')
        self.log_dir = os.path.join(self.parser_dir, 'logs')

        if not os.path.isdir(self.parser_dir):
            os.mkdir(self.parser_dir)
        if not os.path.isdir(self.log_dir):
            os.mkdir(self.log_dir)

    def test_raukuten_filter(self):
        'test raukuten filter'
        kwargs = asos_conf.OP_KWARGS.copy()
        # copy downloaded file test/data/asos.global.txt
        filename = kwargs['site'] + '.' + kwargs['country'] + '.txt'
        filepath0 = os.path.join(test.TESTARGS['testdir'], 'data', filename)
        filepath1 = os.path.join(self.parser_dir, filename)
        shutil.copyfile(filepath0, filepath1)
        kwargs.update({'log_path': self.log_dir,
                       'download_path': self.parser_dir,
                       'download_file': filepath1,
                       'log_level_file': 'debug',
                       'log_level_stdout': 'debug',
                       'log_file_size_in_bytes': 0x100000})

        self.assertIsNone(Parser(RaukutenFilter(kwargs)).parse())

    def test_lazada_filter(self):
        'test lazada filter'
        kwargs = lazada_conf.OP_KWARGS.copy()
        kwargs['country'] = 'singapore'
        # copy downloaded file test/data/lazada.singapore.txt
        filename = kwargs['site'] + '.' + kwargs['country'] + '.txt'
        filepath0 = os.path.join(test.TESTARGS['testdir'], 'data', filename)
        filepath1 = os.path.join(self.parser_dir, filename)
        shutil.copyfile(filepath0, filepath1)
        kwargs.update({'log_path': self.log_dir,
                       'download_path': self.parser_dir,
                       'download_file': filepath1,
                       'log_level_file': 'debug',
                       'log_level_stdout': 'debug',
                       'log_file_size_in_bytes': 0x100000})

        self.assertIsNone(Parser(LazadaFilter(kwargs)).parse())

    def test_zalora_filter(self):
        'test zalora filter'
        kwargs = zalora_conf.OP_KWARGS.copy()
        kwargs['country'] = 'singapore'
        # copy downloaded file test/data/zalora.singapore.txt
        filename = kwargs['site'] + '.' + kwargs['country'] + '.txt'
        filepath0 = os.path.join(test.TESTARGS['testdir'], 'data', filename)
        filepath1 = os.path.join(self.parser_dir, filename)
        shutil.copyfile(filepath0, filepath1)
        kwargs.update({'log_path': self.log_dir,
                       'download_path': self.parser_dir,
                       'download_file': filepath1,
                       'log_level_file': 'debug',
                       'log_level_stdout': 'debug',
                       'log_file_size_in_bytes': 0x100000})

        self.assertIsNone(Parser(ZaloraFilter(kwargs)).parse())
