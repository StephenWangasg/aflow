import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import csv
import json
import requests

from config import data_feed_path
from parsers.data import keys

cats = [
    'mens_clothing', 
    'womens_clothing', 
]


def load_data_from_url(data_feed_url, affiliate_id, affiliate_token, csv_writer, page):
    data_feed = requests.get(data_feed_url, headers={
        'Fk-Affiliate-Id': affiliate_id,
        'Fk-Affiliate-Token': affiliate_token,
    })
    data = data_feed.json()
    products = data['productInfoList']
    for prod in products:
        base_info = prod['productBaseInfoV1']
        prod_name = base_info['title']
        prod_url = base_info['productUrl']
        img_urls = base_info['imageUrls']              
        if img_urls:
            if '800x800' in img_urls:
                img_url = img_urls['800x800']
            else:
                img_url = img_urls['400x400']
        else:
            continue
        uniq_url = img_url
        flipkart_price = base_info['flipkartSellingPrice']
        if flipkart_price:
            price = base_info['flipkartSellingPrice']['amount']
            currency = base_info['flipkartSellingPrice']['currency']
        else:
            continue
           
        if 'flipkartSpecialPrice' in base_info and base_info['flipkartSpecialPrice']:
            disc_price = base_info['flipkartSpecialPrice']['amount']
        else:
            disc_price = 0
        display_price = base_info['flipkartSellingPrice']['amount']
        csv_writer.writerow([prod_name, price, disc_price, display_price, currency, prod_url, img_url, uniq_url])

    if 'nextUrl' in data:
        next_url = data['nextUrl']                   
        print page + 1, ':',  next_url
        load_data_from_url(next_url, affiliate_id, affiliate_token, csv_writer, page + 1)
    else:
        print 'Ended', page     


def flipkart_download(**kwargs):
    affiliate_id = kwargs['affiliate_id']
    affiliate_token = kwargs['affiliate_token']
    api_listing_url = kwargs['api_listing'] + affiliate_id + '.json'
    data_feed_path = kwargs['data_feed_path']
    website = kwargs['website']
    country = kwargs['country']
    categories = kwargs['categories']
    # Get the API listing
    r = requests.get(api_listing_url)
    j = r.json()
    api_listings = j['apiGroups']['affiliate']['apiListings']
    with open(data_feed_path + website + country + 'current.csv', 'wb') as output:
        csv_writer = csv.writer(output, delimiter='\t', quotechar="\"")
        csv_writer.writerow(keys)
        for c in api_listings:
            if c in categories:
                var = api_listings[c]['availableVariants']
                for v in var:
                    if v.startswith('v1'):
                        data_feed_url = var[v]['get'] + '&inStock=true'
                        load_data_from_url(data_feed_url, affiliate_id, affiliate_token, csv_writer, 1)
                    # Save to file
                    #with open(data_feed_path + website + country + c + '.json', 'w') as f:
                    #    json.dump(data, f)


if __name__ == '__main__':
    data_feed_path='/images/models/feeds/'

    # Disable all warnings
    requests.packages.urllib3.disable_warnings()

    flipkart_download(api_listing='https://affiliate-api.flipkart.net/affiliate/api/', affiliate_id='salesiqne', affiliate_token='5d2d66375e7c4e13b0affc5b431529af', data_feed_path=data_feed_path, website='flipkart', country='india', categories=cats)
