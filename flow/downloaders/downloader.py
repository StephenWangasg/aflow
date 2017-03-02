
from abc import ABCMeta, abstractmethod
from datetime import datetime

class IDownloader:
    'downloader abstract base class'
    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    @abstractmethod
    def download(self):
        'download feed'
        pass

    @abstractmethod
    def transform(self):
        '''preliminarily filtering downloaded file,
        remove duplicates, for example'''
        pass

    @staticmethod
    def join_filename(dir_path, site, country, ext='.txt'):
        'A simple help function to generate file name'
        return dir_path + "/" + site + country + ext


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
        start_time = datetime.now()
        downloader.kwargs['logger'].info(
            'Start downloading at %s', start_time.strftime("%X,%B %d,%Y"))
        downloader.download()
        if not downloader.kwargs['download_result']:
            downloader.kwargs['logger'].error(
                'Download error', exc_info=downloader.kwargs['download_error'])
            raise downloader.kwargs['download_error'][1]
        end_time = datetime.now()
        downloader.kwargs['logger'].info('Finish downloading at %s, duration %d sec',
                                         end_time.strftime("%X,%B %d,%Y"),
                                         (end_time - start_time).total_seconds())

        # step 2: transform the content
        start_time = datetime.now()
        downloader.kwargs['logger'].info(
            'Start transforming at %s', start_time.strftime("%X,%B %d,%Y"))
        downloader.transform()
        if not downloader.kwargs['download_result']:
            downloader.kwargs['logger'].error(
                'Transform error', exc_info=downloader.kwargs['download_error'])
            raise downloader.kwargs['download_error'][1]
        end_time = datetime.now()
        downloader.kwargs['logger'].info('Finish transforming at %s, duration %d sec',
                                         end_time.strftime("%X,%B %d,%Y"),
                                         (end_time - start_time).total_seconds())
