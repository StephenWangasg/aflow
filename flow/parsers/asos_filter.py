import parser


class AsosFilter(parser.IRowFilter):
    'ASOS filter class'

    def filter(self, row):
        cats1, cats2 = self.kwargs['cats']
        cats1 = [s.lower() for s in cats1]
        cats2 = [s.lower() for s in cats2]
        if row['primary_cat'].lower() not in cats1:
            self.kwargs['logger'].debug(
                'primary_cat %s not in primary category', row['primary_cat'])
            return False
        prod_name = row['product_name'].lower()
        if not prod_name:
            self.kwargs['logger'].warning(
                'product_name not defined for %s', row['image_url'])
            return False
        if any(word in prod_name for word in parser.INVALID_KEYWORDS):
            self.kwargs['logger'].debug('Invalid keywords in product name (%s)', prod_name)
            return False
        secondarycat = row['secondary_cat'].lower()
        if any(word in secondarycat for word in cats2):
            self.kwargs['logger'].debug('secondary cat (%s) invalid', secondarycat)
            return False
        row['gender'] = -1 if 'gender' not in row else row['gender']
        row.update({key: row[value] for (key, value) in self.kwargs['maps']})

        rt_price = row['retail_price']
        sl_price = row['sale_price']
        try:
            rt_price = float(rt_price)
        except ValueError:
            rt_price = 0.0
        try:
            sl_price = float(sl_price)
        except ValueError:
            sl_price = 0.0
        disp_price = sl_price if rt_price > sl_price != 0.0 else rt_price
        if rt_price == sl_price == 0:
            self.kwargs['logger'].warning(
                '%s(%s) retail and sale price both 0', prod_name, row['image_url'])
        row.update({'price': str(rt_price), 'disc_price': str(
            sl_price), 'display_price': str(disp_price)})

        return True
