'''Configurations for farfetch global'''

import conf

OP_KWARGS = {
    'site': 'farfetch',
    'country': 'global',
    'affiliate_name': 'FarFetch',
    'feed_url': 'ftp://iQNECT:n39PzPcw@aftp.linksynergy.com/35653_3301502_mp.txt.gz',
    'prepend_header': ('product_id', 'product_name', 'sku', 'primary_cat',
                       'secondary_cat', 'product_url', 'image_url', 'c8', 'c9',
                       'c10', 'c11', 'c12', 'sale_price', 'retail_price', 'c15',
                       'c16', 'c17', 'c18', 'c19', 'c20', 'c21', 'c22', 'c23',
                       'c24', 'c25', 'currency', 'c27', 'c28', 'c29', 'c30', 'c31',
                       'c32', 'c33', 'gender', 'c35', 'c36', 'c37', 'c38'),
    'cats': (
        ('Clothing & Accessories'),
        ('Accessories', 'Accessory', 'Anklets', 'Backpacks', 'Bags', 'Belts', 'Boots', 'Bikinis',
         'Bracelets', 'Bras', 'Brogues', 'Ballerinas', 'Biometric', 'Bath', 'Conditioner',
         'Candles', 'Bedding', 'Barware', 'Artwork', 'Ashtrays', 'Buckles', 'Braces', 'Bridal',
         'Brooches', 'Card', 'Clips', 'Claw', 'Baby', 'Capes', 'Caps', 'Charms', 'Conditioners',
         'Crib', 'Earrings', 'Espadrilles', 'Eye', 'Face', 'Facial', 'Flip Flops', 'Gifts',
         'Gloves', 'Gloves', 'Holdalls', 'Hi-Tops', 'Hair', 'Hair', 'Handbags', 'Hats',
         'Headbands', 'Headwear', 'Jewellery', 'Jewelry', 'Loafers', 'Lip', 'Lotion',
         'Lingerie', 'Underwear', 'Lipsticks', 'Luggage', 'Key Chains', 'Kimono', 'Mittens',
         'Necklaces', 'Mules', 'Pumps', 'Neckties', 'Night', 'Oxfords', 'Phone', 'Makeup',
         'Purses', 'Pendants', 'Pins', 'Rings', 'Pre-Walker', 'Sandals', 'Slippers', 'Sandals',
         'Scarves', 'Snoods', 'Shoes', 'Socks', 'Shoelaces', 'Sneakers', 'Skin', 'Shampoo',
         'Vision', 'Shaving', 'Sunglasses', 'Swimming', 'Swimsuits', 'Swimwear', 'Toe', 'Toddler',
         'Trainers', 'Underwear', 'Wallets', 'Warmers', 'Watches')
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
