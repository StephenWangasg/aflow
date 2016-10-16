from  __builtin__ import any as b_any
from flow.parsers.utils import valid, update_map_price

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



