import hashlib, time, requests, ast
import httplib2 as http
from urlparse import urlparse
from eventlet.green import urllib2


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
        pass
    return


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


def get_hashed_st(st):
    m = hashlib.md5()
    m.update(st)
    hashed_st = m.hexdigest()
    return hashed_st


def scheduler(start_to_run_time_hour,
              checking_interval=300,
              sleep_time_after_working=3600):
    while True:
        hour_now = int(time.strftime("%H"))
        if hour_now == start_to_run_time_hour:
            yield True
            time.sleep(sleep_time_after_working)
        else:
            time.sleep(checking_interval)


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


if __name__ == '__main__':
    pass
