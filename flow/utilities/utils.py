import hashlib
import urllib2


def get_hashed_st(st):
    m = hashlib.md5()
    m.update(st)
    hashed_st = m.hexdigest()
    return hashed_st


def download_image_from_url(url, image_path):
    img_data = urllib2.urlopen(url, timeout=30).read()
    with open(image_path, 'wb') as image_file:
        print 'write file ', image_path
        image_file.write(img_data)


def download_image(url_path):
    url, path = url_path
    try:
        print 'download image ', url_path
        download_image_from_url(url, path)
    except (KeyboardInterrupt, SystemExit):
        raise
    except Exception:
        pass
