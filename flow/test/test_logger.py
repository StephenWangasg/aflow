import os
import logger
import pytest


class TestClass:

    @pytest.fixture(autouse=True)
    def tmpdisk_stat(self, tmpdir_factory):
        self.directory = str(tmpdir_factory.mktemp('logs'))
        self.used = logger.FlowDiskWatcher.used(self.directory)
        self.free = logger.FlowDiskWatcher.free(self.directory)
        self.total = logger.FlowDiskWatcher.total(self.directory)
        self.percentage = self.used / self.total

    def test_logger(self):
        logg = logger.FlowLogger(
            'test-site', 'singapore', self.directory, 'debug', 'debug', 1024)
        for i in range(100000):
            logg.debug(
                '------------Logger Test [%d]------------------------', i)
            logg.info('Logger directory: %s', self.directory)
            logg.warning('Used space: %d MB', self.used / 1024 / 1024)
            logg.error('Free space: %d MB', self.free / 1024 / 1024)
            logg.critical('Total space: %MB', self.total / 1024 / 1024)
            logg.log(10, "Used %.2f\% used", self.percentage * 100)

    def test_watcher(self):
        original = len([name for name in os.listdir(self.directory) if os.path.isfile(
            os.path.join(self.directory, name))])
        assert original > 100
        watcher = logger.FlowLoggerWatcher(
            self.directory, (self.used + 102500) / self.total)
        watcher()
        len1 = len([name for name in os.listdir(self.directory) if os.path.isfile(
            os.path.join(self.directory, name))])
        assert len1 < original
        watcher = logger.FlowLoggerWatcher(
            self.directory, (self.used + 10250) / self.total)
        watcher()
        len2 = len([name for name in os.listdir(self.directory) if os.path.isfile(
            os.path.join(self.directory, name))])
        assert len2 < len1
