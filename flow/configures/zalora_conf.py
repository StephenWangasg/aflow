'''Configurations for zalora(Singapore, Malaysia)
please update the country specific setting in respective DAG'''

import conf

OP_KWARGS = {
    'site': 'zalora',
    'country': '**UPDATE-ME**',
    'download_file': '**UPDATE-ME**',
    'parsed_file': '**UPDATE-ME**',
    'search_word': '**UPDATE-ME**',
    'maps': (
        ('product_name', 'NAME'),
        ('currency', 'CURRENCY'),
        ('product_url', 'BUYURL'),
        ('image_url', 'IMAGEURL'),
        ('unique_url', 'IMAGEURL')
    ),
    'cats': (
        "Men>Clothing>T-Shirts",
        "Men>Clothing>Polo Shirts",
        "Men>International Brands>Clothing",
        "Men>Clothing>Shirts",
        "Men>Clothing>Pants",
        "Men>Clothing>Outerwear",
        "Men>Clothing>Jeans",
        "Men>Clothing>Shorts",
        "Men>Clothing>Men\"s Clothing",
        "Men>Sports>Clothing",
        "Women>Clothing>Playsuits & Jumpsuits",
        "Women>Clothing>Dresses",
        "Women>Clothing>Tops",
        "Women>Clothing>Skirts",
        "Women>Clothing>Outerwear",
        "Women>Clothing>Shorts",
        "Women>International Brands>Clothing",
        "Women>Clothing>Pants & Leggings",
        "Women>Korean Fashion>Clothing",
        "Women>Sports>Clothing",
        "Women>Clothing>Jeans",
        "Women>Clothing>Women\"s Clothing",
        "Women>Clothing>Plus Size",
        "Women>International Brands>Sports",
        "Women>Florals>Clothing",
        "Women>Form-fitting>Clothing",
        "Women>Rock Chic>Clothing",
        "Women>Girl Boss>Clothing"
    )
}

conf.update(OP_KWARGS)
