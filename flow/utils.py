import hashlib, urllib2
import requests, ast
from boto.s3.connection import S3Connection
from boto.s3.key import Key

def get_hashed_st(st):
    m = hashlib.md5()
    m.update(st)
    hashed_st = m.hexdigest()
    return hashed_st

def download_image_from_url(url, image_path):
    img_data = urllib2.urlopen(url, timeout=30).read()
    with open(image_path, 'wb') as f:
        f.write(img_data)


def download_image(url_path):
    url, path = url_path
    try:
        download_image_from_url(url, path)
    except (KeyboardInterrupt, SystemExit):
        raise
    except Exception as e:
        pass


class Server:
    def __init__(self, _ip, port):
        self.IP = _ip
        self.port = port

    def return_response(self, st):
        query_url = 'http://' + self.IP + ':' + self.port + st
        response = requests.request("GET", query_url).text
        return ast.literal_eval(response)


class SegmentationServer(Server):
    def __init__(self, _ip, port):
        Server.__init__(self, _ip, port)

    def get_detections(self, img_path):
        st = '/segment?img_path=' + img_path
        return self.return_response(st)


class ClassificationServer(Server):
    def __init__(self, _ip, port):
        Server.__init__(self, _ip, port)

    def get_attributes(self, img_path, box):
        st = '/classify?img_path=' + img_path + '&x1=' + str(box['x1'])+ '&x2=' + str(box['x2'])+ '&y1=' + str(box['y1'])+ '&y2=' + str(box['y2'])
        return self.return_response(st)


class ProductFeature:
    def __init__(self, segmentation_server, classification_server):
        self.segmentor = SegmentationServer(segmentation_server['host'], segmentation_server['port'])
        self.classifier = ClassificationServer(classification_server['host'], classification_server['port'])

    def get_feature(self, query_img_path):
        s1 = self.segmentor.get_detections(query_img_path)
        box = s1['detections'][0]['coord']
        attributes = self.classifier.get_attributes(query_img_path, box)
        return attributes

def push2aws(img_path, name):
    aws_access_key_id = 'AKIAIYWYKOG2DF5UHXNA'
    aws_secret_access_key = '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'
    conn = S3Connection(aws_access_key_id, aws_secret_access_key)
    b = conn.get_bucket('iqfashion')
    k = Key(b)
    k.key = name+'.jpg'
    k.set_contents_from_filename(img_path)
    k.set_acl("public-read")
    return 'https://s3.amazonaws.com/iqfashion/'+name+'.jpg'
