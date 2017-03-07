'Configuration for swap us'

import os
import conf

OP_KWARGS = {
    'site': 'swap',
    'country': 'us',
    'download_file': os.path.join(conf.DOWNLOAD_CONFIGS['download_path'], 'swap.us.txt'),
    'parsed_file': os.path.join(conf.DOWNLOAD_CONFIGS['download_path'], 'swap.us.csv'),
    'search_word': 'Swap_com-Swap_com_Product_Catalog.txt.g',
    'cats': (
        "Men's Apparel > Men's Fashion",
        "Women's Apparel > Women's Fashion",
    ),
    'maps': (
        ('product_name', 'NAME'),
        ('currency', 'CURRENCY'),
        ('product_url', 'BUYURL'),
        ('image_url', 'IMAGEURL'),
        ('unique_url', 'IMAGEURL')
    )
}

conf.update(OP_KWARGS)
