'test logger and watcher class'

import os
import fractions
import unittest
import flow.utilities.logger as logger
import flow.test.arguments as test


class TestLogger(unittest.TestCase):
    '''TestLogger class'''

    def setUp(self):
        self.log_dir = os.path.join(test.TESTARGS['tmpdir'], 'logs')
        if not os.path.isdir(self.log_dir):
            os.mkdir(self.log_dir)
        self.used = logger.FlowDiskWatcher.used(self.log_dir)
        self.free = logger.FlowDiskWatcher.free(self.log_dir)
        self.total = logger.FlowDiskWatcher.total(self.log_dir)
        self.percentage = fractions.Fraction(self.used, self.total)
        if test.TESTARGS['no_logger']:
            self.skipTest('logger test is disabled')

    def log(self):
        'test logger, generate ~500 log files, each 1024 bytes'
        logg = logger.FlowLogger('website', 'country',
                                 self.log_dir, '.log', 'debug', 'debug', 1024, 500)
        for i in range(1000):
            logg.debug(
                '------------Logger Test [%d]-------------', i)
            logg.info('Logger directory: %s', self.log_dir)
            used_size = self.used / 1024 / 1024
            used_unit = "MB" if used_size < 1024 else "GB"
            used_size = used_size if used_size < 1024 else used_size / 1024
            free_size = self.free / 1024 / 1024
            free_unit = "MB" if free_size < 1024 else "GB"
            free_size = free_size if free_size < 1024 else free_size / 1024
            logg.warning('Used space: %d %s' % (used_size, used_unit))
            logg.error('Free space: %d %s' % (free_size, free_unit))
            logg.critical('Total space: %d GB' %
                          (self.total / 1024 / 1024 / 1024))
            logg.log(10, "Used %4.2f %%" % float(self.percentage * 100))

    def test_watcher(self):
        'test wathcer class, delete all log files'
        self.log()
        original = len([name for name in os.listdir(self.log_dir) if os.path.isfile(
            os.path.join(self.log_dir, name))])
        self.assertTrue(500 <= original <= 501)
        watcher = logger.FlowLoggerWatcher(
            self.log_dir, float(self.used + 1024 * 300) / self.total)
        watcher()
        len1 = len([name for name in os.listdir(self.log_dir) if os.path.isfile(
            os.path.join(self.log_dir, name))])
        self.assertTrue(len1 < original)
        if len1:
            watcher = logger.FlowLoggerWatcher(
                self.log_dir, float(self.percentage))
            watcher()
            len2 = len([name for name in os.listdir(self.log_dir) if os.path.isfile(
                os.path.join(self.log_dir, name))])
            self.assertTrue(len2 <= len1)
