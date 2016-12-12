import httplib2 as http
from urlparse import urlparse
import socket, urllib, csv, gzip, os
import requests
import email, imaplib


def download_http_file(url, file_path):
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json; charset=UTF-8'
    }
    target = urlparse(url)
    method = 'GET'
    body = ''
    h = http.Http()
    response, content = h.request(target.geturl(), method, body, headers)
    data_feed_file = open(file_path, "w")
    data_feed_file.write(content)
    data_feed_file.close()
    return


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
    return url

def lazada_download(**kwargs):
    download_file_path = kwargs['download_file']
    feed_url = kwargs['feed_url']
    download_http_file(feed_url, download_file_path)
    return feed_url

def yoox_download(**kwargs):
    download_file_path = kwargs['download_file']
    affiliate_name = kwargs["affiliate_name"]
    feed_list_url = "http://dashboard.commissionfactory.com/Affiliate/Creatives/DataFeeds/j$PXsIK0g7Sc7c7lgOaU55Wgh@yZ4ZHnh@CJo9$kyeultKH2s@$Rh8xW/"

    r = requests.get(feed_list_url)
    all_affiliate_names = r.text
    feed_list_url_file = open(download_file_path + ".csv", "w")
    feed_list_url_file.write(all_affiliate_names)
    feed_list_url_file.close()

    with open(download_file_path + '.csv', 'rt') as f:
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            if affiliate_name == row[1]:
                feed_url = row[8]
                download_http_file(feed_url, download_file_path)
                break

    return feed_list_url


def zalora_download(**kwargs):
    download_file_path = kwargs['download_file']
    search_word = kwargs['search_word']
    user = "zaloraiq@gmail.com"
    pwd = "Iqnect@123"
    m = imaplib.IMAP4_SSL("imap.gmail.com")
    m.login(user, pwd)
    m.select("[Gmail]/All Mail")
    resp, items = m.search(None, "ALL")
    items = items[0].split()
    for emailid in reversed(items):
        resp, data = m.fetch(emailid, "(RFC822)")
        email_body = data[0][1]
        mail = email.message_from_string(email_body)
        if mail.get_content_maintype() != 'multipart' or (search_word not in email_body):
            continue
        for part in mail.walk():
            if part.get_content_maintype() == 'multipart' or (part.get('Content-Disposition') is None):
                continue
            with open(download_file_path + '.gz', 'wb') as f:
                f.write(part.get_payload(decode=True))
            with gzip.open(download_file_path + '.gz', 'rb') as in_file, open(download_file_path, 'wb') as out_file:
                out_file.write(in_file.read())
            return
