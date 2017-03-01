
import sys
from flow.config import data_feed_path

from abc import ABCMeta, abstractmethod
from datetime import datetime


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


def raukuten_download(**kwargs):
    download_file_path = kwargs['download_file']
    header = kwargs['prepend_header']
    url = kwargs['feed_url']
    tmp_file_path = download_file_path + '.tmp.txt'
    tmp_file_path2 = download_file_path + '.tmp2.txt'
    try:
        socket.setdefaulttimeout(3600)
        urllib.urlretrieve(url, download_file_path + '.gz')
        socket.setdefaulttimeout(None)
    except:
        socket.setdefaulttimeout(None)
    with gzip.open(download_file_path + '.gz', 'rb') as in_file, open(tmp_file_path, 'wb') as out_file:
        out_file.write(in_file.read())
    with file(tmp_file_path, 'r') as original:
        original.next()
        with file(tmp_file_path2, 'w') as modified:
            modified.write(header)
            for row in original:
                modified.write(row)
    uniqueIDs = {}
    with open(tmp_file_path2) as f, open(download_file_path, 'w') as f2:
        reader = csv.DictReader(f, delimiter='|')
        columns = reader.fieldnames
        writer = csv.DictWriter(
            f2, delimiter=',', quotechar="\"", fieldnames=columns)
        writer.writeheader()
        for row in reader:
            uid = row['image_url']
            if uid not in uniqueIDs:
                uniqueIDs[uid] = 0
                writer.writerow(row)
    if os.path.exists(tmp_file_path):
        os.remove(tmp_file_path)
    if os.path.exists(tmp_file_path2):
        os.remove(tmp_file_path2)


class IDownloader:
    __metaclass__ = ABCMeta

    @abstractmethod
    def download(self):
        pass

    @abstractmethod
    def pre_process(self):
        pass

    @abstractmethod
    def post_process(self):
        pass

    @staticmethod
    def download_file(dir_path, site, country, ext='.txt'):
        return dir_path + site + country + ext


class RaukutenDownloader(IDownloader):

    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.kwargs['download_file'] = IDownloader.download_file(kwargs['download_path'],
                                                                 kwargs['site'], kwargs['country'], ".txt" if "ext" not in kwargs else kwargs["ext"])
        self.kwargs['download_file_gz'] = IDownloader.download_file(kwargs['download_path'],
                                                                    kwargs['site'], kwargs['country'], '.gz')

    def download(self):
        try:
            self.kwargs['download_result'] = 1
            socket.setdefaulttimeout(3600)
            urllib.urlretrieve(self.kwargs['feed_url'], self.kwargs['download_file_gz'])
        except:
            self.kwargs['download_error'] = sys.exc_info()
            self.kwargs.update({'download_result': 0})
        finally:
            socket.setdefaulttimeout(None)

    def pre_process(self):

    def post_process(self):
        


class DonwloaderDirector:

    @staticmethod
    def construct(downloader):
        start_time = datetime.now()
        self.kwargs['logger'].info(
            'Start downloading at %s', start_time.strftime("%X,%B %d,%Y"))
        downloader.download()
        if not downloader.kwargs['download_result']:
            downloader.kwargs['logger'].error(
                'Download error', exc_info=downloader.kwargs['download_error'])
            return 0
        end_time = datetime.now()
        self.kwargs['logger'].info('Finish downloading at %s, duration %d sec', end_time.strftime("%X,%B %d,%Y"),
                                   (end_time - start_time).total_seconds())

        start_time = datetime.now()
        self.kwargs['logger'].info(
            'Start pre-processing at %s', start_time.strftime("%X,%B %d,%Y"))
        downloader.pre_process()
        if not downloader.kwargs['download_result']:
            downloader.kwargs['logger'].error(
                'Pre-process error', exc_info=downloader.kwargs['download_error'])
            return 0
        end_time = datetime.now()
        self.kwargs['logger'].info('Finish pre-processing at %s, duration %d sec', end_time.strftime("%X,%B %d,%Y"),
                                   (end_time - start_time).total_seconds())

        start_time = datetime.now()
        self.kwargs['logger'].info(
            'Start post-processing at %s', start_time.strftime("%X,%B %d,%Y"))
        downloader.post_process()
        if not downloader.kwargs['download_result']:
            downloader.kwargs['logger'].error(
                'Post-process error', exc_info=downloader.kwargs['download_error'])
            return 0
        end_time = datetime.now()
        self.kwargs['logger'].info('Finish post-processing at %s, duration %d sec', end_time.strftime("%X,%B %d,%Y"),
                                   (end_time - start_time).total_seconds())
        return 1


class Downloader:
    "Base downloader class"

    def __init__(self, **kwargs):
        dfp = data_feed_path if 'data_feed_path' not in kwargs else kwargs[
            'data_feed_path']
        self.args = kwargs
        self.site = kwargs['website']
        self.country = kwargs['country']
        self.__file = dfp + self.site + \
            self.country + kwargs.get('ext', '.txt')

    def download(self):
        'Main download function'
        try:
            retrieve(self)
            extract(self)
            process(self)
        except IOError:

    def downloaded_file(self):
        'Path of downloaded file'
        return self.__file


class HttpDownloader(Downloader):
    'Http Downloader'


class FtpDownloader(Downloader):
    'FTP downloader'
    pass


class EmailDownloader(Downloader):
    'Email downloader'
    pass
