from data import invalid_words, keys
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


def swap(row, map_, cats):
    if not b_any((row['ADVERTISERCATEGORY'] == x or row['ADVERTISERCATEGORY'].startswith(x)) for x in cats):
        return
    if valid(row['NAME'].lower()):
        return
    if row['ADVERTISERCATEGORY'].startswith('Women'):
        row['gender'] = 'female'
    elif row['ADVERTISERCATEGORY'].startswith('Men'):
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
    disp_price = p2 if (p1 > p2 and p2!=0.0) else p1
    return {'price': str(p1), 'disc_price': str(p2), 'display_price': str(disp_price)}


def update_map_price(row, map_, price_key, price2_key):
    mapped = dict([(key, row[value]) for key, value in map_])
    row.update(mapped)
    prices = get_prices(row[price_key], row[price2_key])
    row.update(prices)
    return row


def yoox(row, map_, cats):
    if not b_any(row['Category'] == x for x in cats):
        return
    if valid(row['Name'].lower()):
        return
    if row['Gender'] == 'female' or row['Gender'] == 'male':
        row['gender'] = row['Gender']
    else:
        return
    return update_map_price(row, map_, 'Price', 'PriceSale')


def lazada(row, map_, cats=None):
    if row['Category lv3'] != 'Clothing':
        return
    if valid(row['product_name'].lower()):
        return
    if row['Category lv2'] == 'Women':
        row['gender'] = 'female'
    elif row['Category lv2'] == 'Men':
        row['gender'] = 'male'
    else:
        return
    return update_map_price(row, map_, 'sale_price', 'discounted_price')


def splitCats(cats, sep='|'):
    cats1 = []
    cats2 = []
    currentCats = cats1
    for c in cats:
        if c == '|':
            currentCats = cats2
        else:
            currentCats.append(c)
    return cats1, cats2


def asos(row, map_, cats):
    cats1, invalidSecondaryCatWords = splitCats(cats, '|')
    if not b_any(row['primary_cat'] == x for x in cats1):
        return
    if valid(row['product_name'].lower()):
        return
    if 'gender' not in row: row['gender'] = -1
    secondaryCategory = row['secondary_cat']
    if b_any(w in secondaryCategory for w in invalidSecondaryCatWords):
        return
    return update_map_price(row, map_, 'retail_price', 'sale_price')


def farfetch(row, map_, cats):
    cats1, invalidSecondaryCatWords = splitCats(cats, '|')
    if not b_any(row['primary_cat'] == x for x in cats1):
        return
    if valid(row['product_name'].lower()):
        return
    if 'gender' not in row: row['gender'] = -1
    secondaryCategory = row['secondary_cat']
    if secondaryCategory.strip() == '' or b_any(w in secondaryCategory for w in invalidSecondaryCatWords):
        return
    return update_map_price(row, map_, 'retail_price', 'sale_price')


def target(row, map_, cats):
    print row
    if not b_any((row['Category'] == x or row['Category'].startswith(x)) for x in cats):
        return
    if valid(row['Product Name'].lower()):
        return
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
        reader = csv.DictReader(infile)
        writer = csv.writer(output_file, delimiter='\t', quotechar="\"")
        writer.writerow(keys)
        for row in reader:
            parsed_row =  eval(website+'(row, map, cats)')
            if type(parsed_row) == dict:
                filtered_row = [parsed_row[your_key] for your_key in keys]
                writer.writerow(filtered_row)


if __name__ == "__main__":
    data_feed_path = '/images/models/feeds/'

    website = 'target'
    country = 'global'
    p = data_feed_path + website + country

    op_args = {
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
    with open('target_cats', 'rb') as f:
        cats = f.read().splitlines()
    op_args['cats'] = cats
    parse_write(**op_args)

