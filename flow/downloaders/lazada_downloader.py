
import sys
import urlparse
import httplib2
from flow.downloaders.downloader import IDownloader, ZeroDownloadExcept


class LazadaDownloader(IDownloader):
    'Lazada downloader'

    def __init__(self, kwargs):
        IDownloader.__init__(self, kwargs)

    def download(self):
        try:
            self.kwargs['download_result'] = 1
            self.kwargs['downloaded'] = 0
            headers = {
                'Accept': 'application/json',
                'Content-Type': 'application/json; charset=UTF-8'
            }
            target = urlparse.urlparse(self.kwargs['feed_url'])
            hclient = httplib2.Http()
            _, content = hclient.request(target.geturl(), 'GET', '', headers)
            with open(self.kwargs['download_file'], 'wb') as data_feed_file:
                data_feed_file.write(content)
                self.kwargs['downloaded'] = 1
            if not self.kwargs['downloaded']:
                raise ZeroDownloadExcept
        except:
            self.kwargs['download_error'] = sys.exc_info()
            self.kwargs.update({'download_result': 0})

    def transform(self):
        pass
