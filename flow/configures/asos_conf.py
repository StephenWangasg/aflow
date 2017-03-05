'''Configurations for asos global'''

import os
import flow.configures.conf as conf

OP_KWARGS = {
    'site': 'asos',
    'country': 'global',
    'affiliate_name': 'ASOS',
    'feed_url': 'ftp://iQNECT:n39PzPcw@aftp.linksynergy.com/41970_3301502_mp.txt.gz',
    'download_file': os.path.join(conf.DOWNLOAD_CONFIGS['download_path'], 'asos.global.txt'),
    'parsed_file': os.path.join(conf.DOWNLOAD_CONFIGS['download_path'], 'asos.global.csv'),
    'prepend_header': ('product_id', 'product_name', 'sku', 'primary_cat',
                       'secondary_cat', 'product_url', 'image_url', 'c8', 'c9',
                       'c10', 'c11', 'c12', 'sale_price', 'retail_price', 'c15',
                       'c16', 'c17', 'c18', 'c19', 'c20', 'c21', 'c22', 'c23',
                       'c24', 'c25', 'currency', 'c27', 'c28', 'c29', 'c30', 'c31',
                       'c32', 'c33', 'c34', 'c35', 'c36', 'c37', 'c38'),
    'cats': (
        ('All-In-One', 'Knitwear', 'Mens', 'Tops', 'Trousers', 'Womens', 'Mens Jackets',
         'Womens Jackets', 'Womens Coats', 'Mens Coats'),
        ('Caps', 'Wallets', 'Gloves', 'Hats', 'Bags', 'Accessories', 'Hair', 'Shoes',
         'Sandals', 'Trainers', 'Gifts', 'Sunglasses', 'Underwear', 'Swimming', 'Bikinis',
         'Swimsuits', 'Swimwear', 'Socks', 'Accessories', 'Backpacks', 'Jewelry', 'Luggage',
         'Lingerie/Underwear', 'Belts', 'Bracelets', 'Earrings', 'Necklaces', 'Jewellery',
         'Lipsticks', 'Conditioners', 'Mens Clothing Other', 'Mens Bracelets', 'Other Gifts')
    ),
    'maps': (
        ('product_name', 'product_name'),
        ('currency', 'currency'),
        ('product_url', 'product_url'),
        ('image_url', 'image_url'),
        ('unique_url', 'image_url')
    ),
}

conf.update(OP_KWARGS)

