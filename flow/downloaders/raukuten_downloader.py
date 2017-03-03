
import csv
import gzip
import os
import socket
import sys
import urllib
from flow.downloaders.downloader import IDownloader, ZeroDownloadExcept
from flow.utilities.logger import FlowLogger


class RaukutenDownloader(IDownloader):
    'Raukuten downloader'

    def __init__(self, kwargs):
        IDownloader.__init__(self)
        self.kwargs = kwargs
        self.kwargs['download_file_gz'] = os.path.join(
            kwargs['download_path'],
            kwargs['site'] + '.' + kwargs['country'] + '.gz')


    def download(self):
        try:
            self.kwargs['download_result'] = 1
            socket.setdefaulttimeout(3600)
            urllib.urlretrieve(self.kwargs['feed_url'],
                               self.kwargs['download_file_gz'])
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
            with gzip.open(gz_file, 'rb') as ifile, open(dl_file, 'wb') as ofile:
                ifile.next()
                reader = csv.DictReader(
                    ifile, fieldnames=self.kwargs['prepend_header'],
                    delimiter='|')
                writer = csv.DictWriter(
                    ofile, fieldnames=self.kwargs['prepend_header'],
                    delimiter=',', quotechar='"')
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
