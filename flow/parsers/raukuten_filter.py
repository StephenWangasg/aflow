import parser


class RaukutenFilter(parser.IRowFilter):
    'Raukuten filter class'

    def filter(self, row):
        cats1, cats2 = self.kwargs['cats']
        cats1 = [s.lower() for s in cats1]
        cats2 = [s.lower() for s in cats2]
        if row['primary_cat'].lower() not in cats1:
            self.kwargs['logger'].debug(
                'primary_cat (%s) not in primary category', row['primary_cat'])
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
        secondarycat = row['secondary_cat'].lower()
        if any(word in secondarycat for word in cats2):
            self.kwargs['logger'].debug(
                'secondary cat (%s) invalid', secondarycat)
            return False
        row['gender'] = -1 if 'gender' not in row else row['gender']

        self.update(row, row['retail_price'], row['sale_price'], prod_name)

        return True
