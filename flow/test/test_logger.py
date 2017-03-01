'test logger and watcher class'

import os
import fractions
import logger
import pytest

@pytest.fixture(scope='module')
def tmpdisk_stat(tmpdir_factory):
    'pytest fixture function'
    directory = str(tmpdir_factory.mktemp('logs', False))
    used = logger.FlowDiskWatcher.used(directory)
    free = logger.FlowDiskWatcher.free(directory)
    total = logger.FlowDiskWatcher.total(directory)
    return {'directory': directory,
            'used': used,
            'free': free,
            'total': total,
            'percentage': fractions.Fraction(used, total)}


def test_logger(tmpdisk_stat):
    'test logger, generate ~500 log files, each 1024 bytes'
    logg = logger.FlowLogger(
        'test-site', 'singapore', tmpdisk_stat['directory'], 'debug', 'debug', 1024, 500)
    for i in range(1000):
        logg.debug(
            '------------Logger Test [%d]-------------', i)
        logg.info('Logger directory: %s', tmpdisk_stat['directory'])
        used_size = tmpdisk_stat['used'] / 1024 / 1024
        used_unit = "MB" if used_size < 1024 else "GB"
        used_size = used_size if used_size < 1024 else used_size / 1024
        free_size = tmpdisk_stat['free'] / 1024 / 1024
        free_unit = "MB" if free_size < 1024 else "GB"
        free_size = free_size if free_size < 1024 else free_size / 1024
        logg.warning('Used space: %d %s' % (used_size, used_unit))
        logg.error('Free space: %d %s' % (free_size, free_unit))
        logg.critical('Total space: %d GB' %
                      (tmpdisk_stat['total'] / 1024 / 1024 / 1024))
        logg.log(10, "Used %4.2f %%" %
                 float(tmpdisk_stat['percentage'] * 100))


def test_watcher(tmpdisk_stat):
    'test wathcer class, delete all log files'
    original = len([name for name in os.listdir(tmpdisk_stat['directory']) if os.path.isfile(
        os.path.join(tmpdisk_stat['directory'], name))])
    assert original == 501 or original == 500
    watcher = logger.FlowLoggerWatcher(
        tmpdisk_stat['directory'], float(tmpdisk_stat['used'] + 1024 * 300) / tmpdisk_stat['total'])
    watcher()
    len1 = len([name for name in os.listdir(tmpdisk_stat['directory']) if os.path.isfile(
        os.path.join(tmpdisk_stat['directory'], name))])
    assert len1 < original
    if len1:
        watcher = logger.FlowLoggerWatcher(
            tmpdisk_stat['directory'], float(tmpdisk_stat['percentage']))
        watcher()
        len2 = len([name for name in os.listdir(tmpdisk_stat['directory']) if os.path.isfile(
            os.path.join(tmpdisk_stat['directory'], name))])
        assert len2 <= len1
