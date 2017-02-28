
from flow.config import data_feed_path

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
        writer = csv.DictWriter(f2, delimiter=',', quotechar="\"", fieldnames=columns)
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


class Downloader:
    "Base downloader class"
    def __init__(self, **kwargs):
        dfp = data_feed_path if 'data_feed_path' not in kwargs else kwargs['data_feed_path']
        self.args = kwargs
        self.site = kwargs['website']
        self.country = kwargs['country']
        self.__file = dfp + self.site + self.country + kwargs.get('ext', '.txt')

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

