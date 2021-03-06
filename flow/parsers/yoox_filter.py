import parser


class YooxFilter(parser.IRowFilter):
    'Yoox filter class'

    def __init__(self, kwargs):
        parser.IRowFilter.__init__(self, kwargs)
        self.cats = [s.lower() for s in self.kwargs['cats']]

    def filter(self, row):
        cats = self.cats
        if not self.check_field(row, ('Category', 'Name', 'Gender')):
            return False
        if not any(word in row['Category'].lower() for word in cats):
            self.kwargs['logger'].debug(
                'Did not find category keywords in (%s)', row['Category'])
            return False
        if any(word.search(row['Name']) for word in parser.INVALID_KEYWORDS_RE):
            self.kwargs['logger'].debug(
                'Invalid keywords in Name field (%s)', row['Name'])
            return False
        if row['Gender'] == 'female' or row['Gender'] == 'male':
            row['gender'] = row['Gender']
        else:
            self.kwargs['logger'].debug('Gender invalid (%s)', row['Gender'])
            return False
        self.update(row, 'Price', 'PriceSale', row['Name'])

        return True
