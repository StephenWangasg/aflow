
import os
import sys
import gzip
import email
import imaplib
from flow.downloaders.downloader import IDownloader, ZeroDownloadExcept


class ZaloraDownloader(IDownloader):
    'Zalora downloader'

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
            search_word = self.kwargs['search_word']
            user = "zaloraiq@gmail.com"
            pwd = "Iqnect@123"
            maplib = imaplib.IMAP4_SSL("imap.gmail.com")
            maplib.login(user, pwd)
            maplib.select("[Gmail]/All Mail")
            _, items = maplib.search(None, "ALL")
            items = items[0].split()
            for emailid in reversed(items):
                _, data = maplib.fetch(emailid, "(RFC822)")
                email_body = data[0][1]
                mail = email.message_from_string(email_body)
                if mail.get_content_maintype() != 'multipart' or (search_word not in email_body):
                    continue
                for part in mail.walk():
                    if part.get_content_maintype() == 'multipart' or (
                            part.get('Content-Disposition') is None):
                        continue
                    with open(fgz, 'wb') as file_gz:
                        file_gz.write(part.get_payload(decode=True))
                    with gzip.open(fgz, 'rb') as ifile, open(fil, 'wb') as ofile:
                        ofile.write(ifile.read())
                        self.kwargs['downloaded'] = 1
                    return

            if not self.kwargs['downloaded']:
                raise ZeroDownloadExcept

        except:
            self.kwargs['download_error'] = sys.exc_info()
            self.kwargs.update({'download_result': 0})

    def transform(self):
        pass
