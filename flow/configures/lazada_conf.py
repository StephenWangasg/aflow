'''Configurations for lazada(Singapore, Indonesia, Malaysia)
please update the country specific setting in respective DAG'''

import conf

OP_KWARGS = {
    'site': 'lazada',
    'country': '**UPDATE-ME**',
    'download_file': '**UPDATE-ME**',
    'parsed_file': '**UPDATE-ME**',
    'feed_url': '**UPDATE-ME**',
    'maps': (
        ('image_url', 'picture_url'),
        ('product_url', 'tracking_link'),
        ('unique_url', 'picture_url')
    ),
}

conf.update(OP_KWARGS)
