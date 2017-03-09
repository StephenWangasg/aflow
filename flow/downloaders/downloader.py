'''Donwloader base interface: IDownloader
and DownloaderDirector class'''

import os
import errno
from datetime import datetime
from flow.utilities.base import CBase


class IDownloader(CBase):
    'downloader base class'

    def __init__(self, kwargs):
        kwargs['log_file_ext'] = '.download'
        CBase.__init__(self, kwargs)

    def download(self):
        'download feed'
        raise NotImplementedError('subclass must override download()!')

    def transform(self):
        '''preliminarily filtering downloaded file,
        remove duplicates, for example'''
        raise NotImplementedError('subclass must override transform()!')


class ZeroDownloadExcept(Exception):
    'Raised exception when zero valid product is detected'
    pass


class DownloaderDirector:
    'Download director'

    def __init__(self):
        pass

    @staticmethod
    def construct(downloader):
        '''a static method drives the download procedure:
        download the feeds from the downloader's given url,
        followed by transform, a step performs an initial
        filtering of the downloaded content.
        Logs are added around each step'''

        # step 1: download feed
        start_time = datetime.utcnow()
        downloader.kwargs['logger'].info(
            'Start downloading at %s', start_time.strftime("%X,%B %d,%Y"))
        downloader.download()
        if not downloader.kwargs['download_result']:
            downloader.kwargs['logger'].error(
                'Download error', exc_info=downloader.kwargs['download_error'])
            raise downloader.kwargs['download_error'][1]
        end_time = datetime.utcnow()
        downloader.kwargs['logger'].info('Finish downloading at %s, duration %d sec',
                                         end_time.strftime("%X,%B %d,%Y"),
                                         (end_time - start_time).total_seconds())

        # step 2: transform the content
        start_time = datetime.utcnow()
        downloader.kwargs['logger'].info(
            'Start transforming at %s', start_time.strftime("%X,%B %d,%Y"))
        downloader.transform()
        if not downloader.kwargs['download_result']:
            downloader.kwargs['logger'].error(
                'Transform error', exc_info=downloader.kwargs['download_error'])
            raise downloader.kwargs['download_error'][1]
        end_time = datetime.utcnow()
        downloader.kwargs['logger'].info('Finish transforming at %s, duration %d sec',
                                         end_time.strftime("%X,%B %d,%Y"),
                                         (end_time - start_time).total_seconds())
