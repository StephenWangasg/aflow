import csv
import gzip
import socket
import sys
import urllib
from abc import ABCMeta, abstractmethod
from datetime import datetime


class IParser:
    __metaclass__ = ABCMeta

    @abstractmethod
    def parse(self):
        pass

def parse_write(**kwargs):
    inputfile = kwargs['download_file']
    outputfile = kwargs['new_parsed_csv']
    map = kwargs['map']
    cats = kwargs['cats']
    website = kwargs['website']
    with open(inputfile, 'rb') as infile, open(outputfile, 'wb') as output_file:
        reader = csv.DictReader(infile)
        writer = csv.writer(output_file, delimiter='\t', quotechar="\"")
        writer.writerow(keys)
        for row in reader:
            parsed_row =  eval(website+'(row, map, cats)')
            if type(parsed_row) == dict:
                filtered_row = [parsed_row[your_key] for your_key in keys]
                writer.writerow(filtered_row)

