import os
import sys
import gzip
from ftplib import FTP
from .downloader import IDownloader, ZeroDownloadExcept


class TargetDownloader(IDownloader):
    'Target downloader'

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
            ftp = FTP('products.impactradius.com')
            ftp.login('ps-ftp_189204', 'CwHPeTx2kf')
            ftp.cwd('Target')
            ftp.retrbinary('RETR Target-Product-Feed-Commissioned-Items_IR.txt.gz',
                           open(fgz, 'wb').write)
            ftp.quit()

            with gzip.open(fgz, 'rb') as ifile, open(fil, 'wb') as ofile:
                ofile.write(ifile.read())
                self.kwargs['downloaded'] = 1
            if not self.kwargs['downloaded']:
                raise ZeroDownloadExcept
        except:
            self.kwargs['download_error'] = sys.exc_info()
            self.kwargs.update({'download_result': 0})

    def transform(self):
        pass
