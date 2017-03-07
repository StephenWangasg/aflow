'''Configurations for yoox(Singapore, Malaysia)
please update the country specific setting in respective DAG'''

import conf

OP_KWARGS = {
    'site': 'yoox',
    'country': '**UPDATE-ME**',
    'download_file': '**UPDATE-ME**',
    'parsed_file': '**UPDATE-ME**',
    'affiliate_name': '**UPDATE-ME**',
    'cats': (
        "Apparel & Accessories > Clothing > Outerwear > Coats & Jackets",
        "Apparel & Accessories > Clothing > Shirts & Tops",
        "Apparel & Accessories > Clothing > One-Pieces",
        "Apparel & Accessories > Clothing > Skirts",
        "Apparel & Accessories > Clothing > Shorts",
        "Apparel & Accessories > Clothing > Pants",
        "Apparel & Accessories > Clothing",
        "Apparel & Accessories > Clothing > Uniforms",
        "Apparel & Accessories > Clothing > Suits",
        "Apparel & Accessories > Clothing > Outerwear",
        "Apparel & Accessories > Clothing > Outerwear > Snow Pants & Suits",
        "Apparel & Accessories > Clothing > One-Pieces > Jumpsuits & Rompers"
    ),
    'maps': (
        ('product_name', 'Name'),
        ('currency', 'Currency'),
        ('product_url', 'Url'),
        ('image_url', 'Image'),
        ('unique_url', 'Url')
    ),
}

conf.update(OP_KWARGS)
