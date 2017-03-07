
import sys
import csv
import urlparse
import httplib2
import requests
from .downloader import IDownloader, ZeroDownloadExcept


class YooxDownloader(IDownloader):
    'Yoox downloader'

    def __init__(self, kwargs):
        IDownloader.__init__(self, kwargs)

    def download(self):
        try:
            self.kwargs['download_result'] = 1
            self.kwargs['downloaded'] = 0
            fil = self.kwargs['download_file']

            affiliate_name = self.kwargs["affiliate_name"]
            feed_list_url = "http://dashboard.commissionfactory.com/Affiliate/Creatives/DataFeeds/j$PXsIK0g7Sc7c7lgOaU55Wgh@yZ4ZHnh@CJo9$kyeultKH2s@$Rh8xW/"

            with open(fil + '.csv', 'w') as feed_list_url_file:
                feed_list_url_file.write(requests.get(feed_list_url).text)

            with open(fil + '.csv', 'rt') as fcsv:
                reader = csv.reader(fcsv, delimiter=',')
                for row in reader:
                    if affiliate_name == row[1]:
                        feed_url = row[8]
                        headers = {
                            'Accept': 'application/json',
                            'Content-Type': 'application/json; charset=UTF-8'}
                        target = urlparse.urlparse(feed_url)
                        hclient = httplib2.Http()
                        _, content = hclient.request(
                            target.geturl(), 'GET', '', headers)
                        with open(fil, 'wb') as data_feed_file:
                            data_feed_file.write(content)
                            self.kwargs['downloaded'] = 1
                        break

            if not self.kwargs['downloaded']:
                raise ZeroDownloadExcept

        except:
            self.kwargs['download_error'] = sys.exc_info()
            self.kwargs.update({'download_result': 0})

    def transform(self):
        pass
