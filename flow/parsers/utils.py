from flow.parsers.data import invalid_words, keys
import csv
from  __builtin__ import any as b_any


valid = lambda st: any(ext in st for ext in invalid_words)

def zalora(row, map_, cats):
    if not b_any((row['KEYWORDS'] == x or row['KEYWORDS'].startswith(x)) for x in cats):
        return
    if valid(row['NAME'].lower()):
        return
    if row['KEYWORDS'].startswith('Women'):
        row['gender'] = 'female'
    elif row['KEYWORDS'].startswith('Men'):
        row['gender'] = 'male'
    else:
        return
    return update_map_price(row, map_, 'PRICE', 'SALEPRICE')

def get_prices(price, price2):
    try:
        p1 = float(price)
    except ValueError:
        p1 = 0.0
    try:
        p2 = float(price2)
    except ValueError:
        p2 = 0.0
    disp_price = p2 if p1 > p2 else p1
    return {'price': str(p1), 'disc_price': str(p2), 'display_price': str(disp_price)}


def update_map_price(row, map_, price_key, price2_key):
    mapped = dict([(key, row[value]) for key, value in map_])
    row.update(mapped)
    prices = get_prices(row[price_key], row[price2_key])
    row.update(prices)
    return row


def parse_write(**kwargs):
    inputfile = kwargs['download_file']
    outputfile = kwargs['current_parsed_csv']
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