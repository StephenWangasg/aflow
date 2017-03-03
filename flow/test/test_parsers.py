'test filter classes'

import os
import pytest
from flow.utilities.logger import FlowLogger
from flow.downloaders.downloader import DownloaderDirector
from flow.downloaders.raukuten_downloader import RaukutenDownloader
import flow.configures.asos_conf as asos_conf


@pytest.fixture(scope='module')
def parse_stat(tmpdir_factory):
    'pytest fixture function'
    download_dir = str(tmpdir_factory.mktemp('download', False))
    log_dir = str(tmpdir_factory.mktemp('log', False))
    return {'download': download_dir, 'log': log_dir}


def test_raukuten_downloader(download_stat):
    'test raukuten downloader'
    kwargs = asos_conf.OP_KWARGS.copy()
    kwargs.update({'log_path': download_stat['log'],
                   'download_path': download_stat['download'],
                   'download_file': os.path.join(
                       download_stat['download'],
                       (kwargs['site'] + '.' + kwargs['country'] + '.txt')),
                   'logger': FlowLogger(kwargs['site'], kwargs['country'],
                                        download_stat['log'], 'debug', 'critical')})

    try:
        downloader = RaukutenDownloader(kwargs)
        DownloaderDirector.construct(downloader)
    except:
        assert 0
