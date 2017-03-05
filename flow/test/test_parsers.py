'test filter classes'

import os
import unittest
import shutil
from flow.parsers.parser import Parser
from flow.parsers.asos_filter import AsosFilter
import flow.configures.asos_conf as asos_conf
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

    def test_asos_filter(self):
        'test asos filter'
        kwargs = asos_conf.OP_KWARGS.copy()
        # copy downloaded file test/data/asos.global.txt
        filename = kwargs['site'] + '.' + kwargs['country'] + '.txt'
        filepath0 = os.path.join(test.TESTARGS['testdir'], 'data', filename)
        filepath1 = os.path.join(self.parser_dir, filename)
        filepath2 = os.path.join(self.parser_dir,
                                 kwargs['site'] + '.' + kwargs['country'] + '.csv')
        shutil.copyfile(filepath0, filepath1)
        kwargs.update({'log_path': self.log_dir,
                       'download_path': self.parser_dir,
                       'download_file': filepath1,
                       'parsed_file': filepath2,
                       'log_level_file': 'debug',
                       'log_level_stdout': 'debug',
                       'log_file_size_in_bytes': 0x100000})

        self.assertIsNone(Parser(AsosFilter(kwargs)).parse())
