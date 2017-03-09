import parser


class LazadaFilter(parser.IRowFilter):
    'lazada filter class'

    def filter(self, row):
        if row['Category lv3'] != 'Clothing':
            self.kwargs['logger'].debug(
                'Category lv3 (%s) not Clothing.', row['Category lv3'])
            return False
        prod_name = row['product_name'].lower()
        if not prod_name:
            self.kwargs['logger'].warning(
                'product_name not defined for (%s)', row['image_url'])
            return False
        if any(word in prod_name for word in parser.INVALID_KEYWORDS):
            self.kwargs['logger'].debug(
                'Invalid keywords in product name (%s)', prod_name)
            return False
        if row['Category lv2'] == 'Women':
            row['gender'] = 'female'
        elif row['Category lv2'] == 'Men':
            row['gender'] = 'male'
        else:
            self.kwargs['logger'].debug('Category lv2 (%s) is invalid value.', row['Category lv2'])
            return False

        self.update(row, row['sale_price'], row['discounted_price'], prod_name)

        return True

