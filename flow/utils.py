import hashlib, urllib2
import requests, ast


def get_hashed_st(st):
    m = hashlib.md5()
    m.update(st)
    hashed_st = m.hexdigest()
    return hashed_st


def download_image(url_path):
    url, path = url_path
    try:
        img_data = urllib2.urlopen(url, timeout=30).read()
        with open(path, 'wb') as f:
            f.write(img_data)
    except (KeyboardInterrupt, SystemExit):
        raise
    except Exception as e:
        print '"', url, '"',  e
    return


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
        print box
        attributes = self.classifier.get_attributes(query_img_path, box)
        return attributes