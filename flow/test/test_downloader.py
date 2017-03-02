'test downloader class'

import pytest
from flow.logger import FlowLogger
from flow.downloaders.downloader import DownloaderDirector, RaukutenDownloader


@pytest.fixture(scope='module')
def download_stat(tmpdir_factory):
    'pytest fixture function'
    directory = str(tmpdir_factory.mktemp('download', False))
    return {'directory': directory}


def test_raukuten_downloader(download_stat):
    'test raukuten downloader'
    kwargs = {'download_path': download_stat['directory'],
              'site': 'asos', 'country': 'global',
              'feed_url': 'ftp://iQNECT:n39PzPcw@aftp.linksynergy.com/41970_3301502_mp.txt.gz',
              'prepend_header': ('product_id', 'product_name', 'sku', 'primary_cat',
                                 'secondary_cat', 'product_url', 'image_url', 'c8', 'c9',
                                 'c10', 'c11', 'c12', 'sale_price', 'retail_price', 'c15',
                                 'c16', 'c17', 'c18', 'c19', 'c20', 'c21', 'c22', 'c23',
                                 'c24', 'c25', 'currency', 'c27', 'c28', 'c29', 'c30', 'c31',
                                 'c32', 'c33', 'c34', 'c35', 'c36', 'c37', 'c38'),
              'logger':
              FlowLogger('asos', 'global', download_stat['directory'], 'debug', 'critical'), }

    try:
        downloader = RaukutenDownloader(kwargs)
        DownloaderDirector.construct(downloader)
    except:
        assert 0
