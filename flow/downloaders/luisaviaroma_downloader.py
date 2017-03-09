import gzip

# from ftplib import FTP


# def extract_file(download_file_path):
#     with gzip.open(download_file_path + '.gz', 'rb') as in_file, open(download_file_path, 'wb') as out_file:
#         out_file.write(in_file.read())


# def luisaviaroma_download(**kwargs):
#     download_file_path = kwargs['download_file']

#     ftp = FTP('datatransfer.cj.com')     # connect to host, default port
#     ftp.login('4616059', 'JZ$TYXPJ')
#     ftp.cwd('outgoing/productcatalog/187926')
    
#     print 'Downloading archive...'
#     ftp.retrbinary('RETR LUISAVIAROMA_COM-Complete_Singapore.txt.gz', open(download_file_path + '.gz', 'wb').write)
#     ftp.quit()

#     # File has been downloaded, unzip it
#     print 'Extracting...'
#     extract_file(download_file_path)


# if __name__ == "__main__":
#     #print "target"
#     luisaviaroma_download(download_file='/images/models/feeds/luisaviaromaglobal.txt')
#     #extract_file('/images/models/feeds/targetglobal.txt')
