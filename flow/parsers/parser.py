
import sys
import csv
from datetime import datetime
from flow.utilities.base import CBase

KEYS = ['product_name', 'price', 'disc_price', 'display_price',
        'currency', 'product_url', 'image_url', 'unique_url']

INVALID_KEYWORDS = [
    'bathing', 'laptop', 'brief', 'maternity', 'costume', 'keyboard',
    'wrap', 'bra', 'belt', 'tanga', 'panty', 'nightwear', 'sandal',
    'usb', 'leg warmer', 'sock', 'add', 't-back', 'g-string', 'iphone',
    'robe', 'hat', 'toe', 'swim', 'shawl', 'watch', 'shapewear', 'adult',
    'child', 'baby', 'monokini', 'stocking', 'ipad', 'corset', 'girdle',
    'swimsuit', 'bag', 'bikini', 'lingerie', 'nipple', 'night', 'sleep',
    'shoe', 'clamp', 'waist trainer', 'boots', 'sleeping', 'nail', 'poncho',
    'shrug', 'tube', 'swimwear', 'one-piece', 'PC', 'kimono', 'finger',
    'babies', 'panties', 'ipad cover', 'sleepwear', 'beach wear', 'thong',
    'silicone', 'qyt', 'leg support', 'wrap-around',
    'Cyber Women Flare Sleeve Lace Patchwork Stretch Pleated Hem Plus Blouse',
    'macbook', 'kid', 'box', 'cincher', 'underwear', 'mask', 'beachwear',
    'one piece', 'camera', 'pajama', 'bandeau', 'trimmer', 'pencil case',
    'stickers', 'hip flask', 'water bottle', 'foulard', 'hardware', 'hair',
    'hairbrush', 'toni & guy', 'shot glasses', 'body wash', 'shave gel',
    'backpack', 'frisbee', 'book', 'pomade', 'poster', 'cooler', 'beard',
    'wax', 'game', 'blood', 'headphones', 'bandana', 'scarf', 'shaver',
    'table', 'wireless', 'example', 'mosquito', 'mug', 'stainless steel',
    'handlebar', 'bicycle', 'motorbike', 'gloves', 'portable', 'bike',
    'paintball', 'alluminum', 'paddles', 'fishing', 'goggles', 'yoga'
]

INVALID_KEYWORDS = [keyword.lower() for keyword in INVALID_KEYWORDS]


class IRowFilter(CBase):
    'row filter base class'

    def __init__(self, kwargs):
        CBase.__init__(self)
        self.kwargs = kwargs
        self.ensure_logger(kwargs)

    def filter(self, row):
        '''filters(validates) a row from downloaded file,
        return True if the row contains valid data, False othereise'''
        raise NotImplementedError('subclass must override filter()!')


class Parser:
    'Parser class exposes the parse function'

    def __init__(self, rowfilter):
        self.filter = rowfilter
        self.kwargs = self.filter.kwargs

    def parse(self):
        '''parse the content of downloaded file,
        rows will be filtered, valid rows are written
        into a new csv file'''
        try:
            total_entries, invalid_entries = 0, 0
            start_time = datetime.now()
            self.kwargs['logger'].info(
                'Start parsing at %s', start_time.strftime("%X,%B %d,%Y"))
            dl_file = self.kwargs['download_file']
            ps_file = self.kwargs['parsed_file']
            with open(dl_file, 'rb') as ifile, open(ps_file, 'wb') as ofile:
                reader = csv.DictReader(ifile, delimiter=',', quotechar='"')
                writer = csv.writer(ofile, delimiter='\t', quotechar='"')
                writer.writerow(KEYS)
                for row in reader:
                    total_entries += 1
                    result = self.filter.filter(row)
                    if result:
                        writer.writerow([row[key] for key in KEYS])
                    else:
                        invalid_entries += 1
            self.kwargs['logger'].info('Parser summary:')
            self.kwargs['logger'].info('Valid: %d, Invalid: %d, Total: %d',
                                       total_entries - invalid_entries,
                                       invalid_entries, total_entries)
        except:
            self.kwargs['logger'].error('Parse error', exc_info=sys.exc_info())
            raise

        end_time = datetime.now()
        self.kwargs['logger'].info('Finish parsing at %s, duration %d sec',
                                   end_time.strftime("%X,%B %d,%Y"),
                                   (end_time - start_time).total_seconds())
