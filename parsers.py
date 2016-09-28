import csv
from  __builtin__ import any as b_any
from config import invalid_words


valid = lambda st: any(ext in st for ext in invalid_words)


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


def parse_csv(inputfile, outputfile, website, country, map_, cats):
    keys = ['product_name', 'gender', 'price', 'disc_price', 'display_price', 'currency', 'product_url', 'image_url', 'unique_url']
    with open(inputfile, 'rb') as infile, open(outputfile, 'wb') as output_file:
        reader = csv.DictReader(infile)
        writer = csv.writer(output_file, delimiter='\t', quotechar="\"")
        writer.writerow(keys)
        for row in reader:
            parsed_row = eval(website+'(row, map_, cats)')
            if type(parsed_row) == dict:
                filtered_row = [parsed_row[your_key] for your_key in keys]
                writer.writerow(filtered_row)


if __name__ == '__main__':
    pass
