import csv

from data import invalid_words, keys
from  __builtin__ import any as b_any

valid = lambda st: any(ext in st for ext in invalid_words)

# def import_cats(filename):
#     with open(filename, 'rb') as f:
#         cats = f.read().splitlines()
#         return cats
#     return None 


def get_prices(price, price2):
    try:
        p1 = float(price)
    except ValueError:
        p1 = 0.0
    try:
        p2 = float(price2)
    except ValueError:
        p2 = 0.0
    disp_price = p2 if (p1 > p2 and p2!=0.0) else p1
    return {'price': str(p1), 'disc_price': str(p2), 'display_price': str(disp_price)}


def update_map_price(row, map_, price_key, price2_key):
    mapped = dict([(key, row[value]) for key, value in map_])
    row.update(mapped)
    prices = get_prices(row[price_key], row[price2_key])
    row.update(prices)
    return row


def target_parse(row, map_, cats):
    if not b_any((row['Category'] == x or row['Category'].startswith(x)) for x in cats):
        return
    if valid(row['Product Name'].lower()):
        return
    prod_name = row['Product Name']
    if 'Women' in prod_name:
        row['gender'] = 'female'
    elif 'Men' in prod_name:
        row['gender'] = 'male'
    elif 'Girls' in prod_name:
        return
    elif 'Boys' in prod_name:
        return
    else:
        row['gender'] = -1
    row['currency'] = 'USD'
    return update_map_price(row, map_, 'Original Price', 'Current Price')


def parse_write(**kwargs):
    inputfile = kwargs['download_file']
    outputfile = kwargs['new_parsed_csv']
    map = kwargs['map']
    cats = kwargs['cats']
    website = kwargs['website']
    with open(inputfile, 'rb') as infile, open(outputfile, 'wb') as output_file:
        reader = csv.DictReader(infile, delimiter='\t', quotechar="\"")
        writer = csv.writer(output_file, delimiter='\t', quotechar="\"")
        writer.writerow(keys)
        for row in reader:
            parsed_row =  target_parse(row, map, cats)
            if type(parsed_row) == dict:
                print parsed_row['Product Name']
                filtered_row = [parsed_row[your_key] for your_key in keys]
                writer.writerow(filtered_row)


if __name__ == "__main__":
    data_feed_path = '/images/models/feeds/'

    website = 'target'
    country = 'global'
    p = data_feed_path + website + country

    op_kwargs = {
        'download_file': p + '.txt',
        'new_parsed_csv': p + 'current.csv',
        'website': website,
        'country': country,
        'map': [
            ('product_name', 'Product Name'),
            #('currency', 'Currency'),
            ('product_url', 'Product URL'),
            ('image_url', 'Image URL'),
            ('unique_url', 'Image URL')
        ],
    }

    cats = import_cats(data_feed_path + 'target_cats')
    op_kwargs['cats'] = cats
    parse_write(**op_kwargs)
