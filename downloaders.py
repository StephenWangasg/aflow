import requests, csv, gzip
import email, imaplib
from parsers import parse_csv
from config import data_feed_path
from tools import download_http_file


def lazada(download_file_path, country_item):
    download_http_file(country_item['feed_url'], download_file_path)


def yoox(download_file_path, country_item):
    affiliate_name = country_item["affiliate_name"]
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


def zalora(download_file_path, country_item):
    search_word = country_item['search_word']
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


def download_and_parse(website, country, country_item, feed_item):
    p = data_feed_path + website + country
    download_path = p + '.txt'
    st = website + '(download_path, country_item)'
    eval(st)
    current_parsed_path = p + 'current.csv'
    parse_csv(download_path, current_parsed_path, website, country, feed_item['map'], feed_item['cats'])
    return current_parsed_path, p + 'previous.csv'


if __name__ == '__main__':
    pass
