import email, imaplib, gzip
from pprint import pprint


def zalora_from_email(**kwargs):
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

def download_zalora_singapore(**kwargs):
    zalora_from_email(kwargs['download_file'],{
          "name": "singapore",
          "search_word": "ZALORA_SG-Product_Feed.txt.g"
        })

def download_zalora_malaysia(**kwargs):
    zalora_from_email('/home/raja/Downloads/feeds1/zaloramalaysia.txt',{
          "name": "malaysia",
          "search_word": "ZALORA_MY-Product_Feed.txt.g"
        })