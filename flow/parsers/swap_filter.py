
import parser


class SwapFilter(parser.IRowFilter):
    'swap filter class'
    def __init__(self, kwargs):
        parser.IRowFilter.__init__(self, kwargs)
        self.cats = [s.lower() for s in self.kwargs['cats']]

    def filter(self, row):
        cats = self.cats
        if not any(word in row['ADVERTISERCATEGORY'].lower() for word in cats):
            self.kwargs['logger'].debug(
                'Did not find category keywords in (%s)', row['ADVERTISERCATEGORY'])
            return False
        if any(word in row['NAME'].lower() for word in parser.INVALID_KEYWORDS):
            self.kwargs['logger'].debug(
                'Invalid keywords in NAME field (%s)', row['NAME'])
            return False
        if row['ADVERTISERCATEGORY'].startswith('Women'):
            row['gender'] = 'female'
        elif row['ADVERTISERCATEGORY'].startswith('Men'):
            row['gender'] = 'male'
        else:
            self.kwargs['logger'].debug(
                'ADVERTISERCATEGORY(%s) contains invalid value', row['ADVERTISERCATEGORY'])
            return False

        self.update(row, row['PRICE'], row['SALEPRICE'], row['NAME'])

        return True
