import os
import json

data_feed_path = '/images/models/feeds/'

def flipkart_parse():
    files = []
    for i in os.listdir(data_feed_path):
        if os.path.isfile(os.path.join(data_feed_path, i)) and i.startswith('flipkartsingapore'):
            files.append(i)

    for f in files:
        with open (data_feed_path + f, 'r') as json_file:
            #print json_file.read()
            data = json.loads(json_file.read()) 
            print data  


if __name__ == '__main__':
    flipkart_parse()
