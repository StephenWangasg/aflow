
import csv
import gzip
import socket
import sys
import urllib
from abc import ABCMeta, abstractmethod
from datetime import datetime


# from flow.config import data_feed_path


def download_http_file(url, file_path):
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json; charset=UTF-8'
    }
    target = urlparse(url)
    method = 'GET'
    body = ''
    hclient = http.Http()
    _, content = hclient.request(target.geturl(), method, body, headers)
    with open(file_path, 'wb') as data_feed_file:
        data_feed_file.write(content)


class IDownloader:
    __metaclass__ = ABCMeta

    @abstractmethod
    def download(self):
        pass

    @abstractmethod
    def transform(self):
        pass

    @staticmethod
    def join_filename(dir_path, site, country, ext='.txt'):
        return dir_path + "/" + site + country + ext


class ZeroDownloadExcept(Exception):
    'Raised exception when zero valid product is detected'
    pass


class RaukutenDownloader(IDownloader):

    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.kwargs['download_file'] = IDownloader.join_filename(kwargs['download_path'],
                                                                 kwargs['site'], kwargs[
                                                                     'country'],
                                                                 ".txt" if "ext" not in kwargs else kwargs["ext"])
        self.kwargs['download_file_gz'] = IDownloader.join_filename(kwargs['download_path'],
                                                                    kwargs['site'], kwargs['country'], '.gz')

    def download(self):
        try:
            self.kwargs['download_result'] = 1
            socket.setdefaulttimeout(3600)
            urllib.urlretrieve(self.kwargs['feed_url'], self.kwargs[
                               'download_file_gz'])
        except:
            self.kwargs['download_error'] = sys.exc_info()
            self.kwargs.update({'download_result': 0})
        finally:
            socket.setdefaulttimeout(None)

    def transform(self):
        try:
            self.kwargs['download_result'] = 1
            unique_image_urls = []
            duplic_image_urls = {}
            total_entries, invalid_entries = 0, 0
            gz_file = self.kwargs['download_file_gz']
            dl_file = self.kwargs['download_file']
            with gzip.open(gz_file, 'rb') as ifile, open(dl_file, 'w') as ofile:
                ifile.next()
                reader = csv.DictReader(ifile, fieldnames=self.kwargs[
                                        'prepend_header'], delimiter='|')
                writer = csv.DictWriter(ofile, fieldnames=self.kwargs['prepend_header'], delimiter=',',
                                        quotechar='"')
                writer.writeheader()
                for row in reader:
                    uid = row['image_url']
                    total_entries += 1
                    if uid and uid not in unique_image_urls:
                        unique_image_urls.append(uid)
                        writer.writerow(row)
                    elif uid and uid not in duplic_image_urls:
                        duplic_image_urls[uid] = 1
                        self.kwargs['logger'].debug(
                            'Duplicate image url %s is omitted', uid)
                    elif uid:
                        duplic_image_urls[uid] += 1
                        self.kwargs['logger'].debug(
                            '%d duplications of image url %s detected', duplic_image_urls[uid], uid)
                    else:
                        invalid_entries += 1

            self.kwargs['logger'].info('Downloader summary:')
            self.kwargs['logger'].info('Valid: %d, Duplicates: %d, Invalid: %d, Total: %d', len(
                unique_image_urls), len(duplic_image_urls), invalid_entries, total_entries)
            if duplic_image_urls:
                mkey = max(duplic_image_urls,
                           key=lambda k: duplic_image_urls[k])
                self.kwargs['logger'].info(
                    'Most duplicated(%d): %s', duplic_image_urls[mkey], mkey)
            if not unique_image_urls:
                raise ZeroDownloadExcept
        except:
            self.kwargs['download_error'] = sys.exc_info()
            self.kwargs.update({'download_result': 0})


class DownloaderDirector:
    'Download director'
    @staticmethod
    def construct(downloader):
        '''a static method drives the download procedure:
        download the feeds from the downloader's given url,
        followed by transform, a step intended to transform
        the downloaded file into a defined format.
        Logs are added around each step'''

        # step 1: download feed
        start_time = datetime.now()
        downloader.kwargs['logger'].info(
            'Start downloading at %s', start_time.strftime("%X,%B %d,%Y"))
        downloader.download()
        if not downloader.kwargs['download_result']:
            downloader.kwargs['logger'].error(
                'Download error', exc_info=downloader.kwargs['download_error'])
            return 0
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
            return 0
        end_time = datetime.now()
        downloader.kwargs['logger'].info('Finish transforming at %s, duration %d sec',
                                         end_time.strftime("%X,%B %d,%Y"),
                                         (end_time - start_time).total_seconds())
        return 1
