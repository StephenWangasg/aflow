import os
import sys
import gzip
from ftplib import FTP
from .downloader import IDownloader, ZeroDownloadExcept


class SwapDownloader(IDownloader):
    'Swap downloader'

    def __init__(self, kwargs):
        IDownloader.__init__(self, kwargs)
        self.kwargs['download_file_gz'] = os.path.join(
            kwargs['download_path'],
            kwargs['site'] + '.' + kwargs['country'] + '.gz')

    def download(self):
        try:
            self.kwargs['download_result'] = 1
            self.kwargs['downloaded'] = 0
            fil = self.kwargs['download_file']
            fgz = self.kwargs['download_file_gz']
            ftp = FTP('datatransfer.cj.com')
            ftp.login('4616059', 'JZ$TYXPJ')
            ftp.cwd('outgoing/productcatalog/187926')
            ftp.retrbinary('RETR Swap_com-Swap_com_Product_Catalog.txt.gz',
                           open(fgz, 'wb').write)
            ftp.quit()
            with gzip.open(fgz, 'rb') as ifile, open(fil, 'wb') as ofile:
                self.kwargs['downloaded'] = 1
                ofile.write(ifile.read())
            if not self.kwargs['downloaded']:
                raise ZeroDownloadExcept
        except:
            self.kwargs['download_error'] = sys.exc_info()
            self.kwargs.update({'download_result': 0})

    def transform(self):
        pass
