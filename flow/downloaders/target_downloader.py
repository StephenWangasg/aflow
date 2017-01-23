import gzip

from ftplib import FTP


def extract_file(download_file_path):
    with gzip.open(download_file_path + '.gz', 'rb') as in_file, open(download_file_path, 'wb') as out_file:
        out_file.write(in_file.read())


def target_download(**kwargs):
    download_file_path = kwargs['download_file']

    ftp = FTP('products.impactradius.com')     # connect to host, default port
    ftp.login('ps-ftp_189204', 'CwHPeTx2kf')
    ftp.cwd('Target') 
    #ftp.retrlines('LIST')
    print 'Downloading archive...'
    ftp.retrbinary('RETR Target-Product-Feed-Commissioned-Items_IR.txt.gz', open(download_file_path + '.gz', 'wb').write)
    ftp.quit()

    # File has been downloaded, unzip it
    print 'Extracting...'
    extract_file(download_file_path)


if __name__ == "__main__":
    #print "target"
    target_download(download_file='/images/models/feeds/targetglobal.txt')
    #extract_file('/images/models/feeds/targetglobal.txt')
