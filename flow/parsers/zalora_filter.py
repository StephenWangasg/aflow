import parser


class ZaloraFilter(parser.IRowFilter):
    'zalora filter class'

    def __init__(self, kwargs):
        parser.IRowFilter.__init__(self, kwargs)
        self.cats = [s.lower() for s in self.kwargs['cats']]

    def filter(self, row):
        cats = self.cats
        if not any(word in row['KEYWORDS'].lower() for word in cats):
            self.kwargs['logger'].debug('Did not find category keywords in (%s)', row['KEYWORDS'])
            return False
        if any(word in row['NAME'].lower() for word in parser.INVALID_KEYWORDS):
            self.kwargs['logger'].debug('Invalid keywords in NAME field (%s)', row['NAME'])
            return False
        if row['KEYWORDS'].startswith('Women'):
            row['gender'] = 'female'
        elif row['KEYWORDS'].startswith('Men'):
            row['gender'] = 'male'
        else:
            self.kwargs['logger'].debug('KEYWORDS(%s) contains invalid value', row['KEYWORDS'])
            return False

        self.update(row, row['PRICE'], row['SALEPRICE'], row['NAME'])

        return True

