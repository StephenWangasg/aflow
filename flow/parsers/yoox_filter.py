import parser


class YooxFilter(parser.IRowFilter):
    'Yoox filter class'

    def filter(self, row):
        cats = [s.lower() for s in self.kwargs['cats']]
        if not any(word in row['Category'].lower() for word in cats):
            self.kwargs['logger'].debug(
                'Did not find category keywords in (%s)', row['Category'])
            return False
        if any(word.lower() in row['Name'].lower for word in parser.INVALID_KEYWORDS):
            self.kwargs['logger'].debug(
                'Invalid keywords in Name field (%s)', row['Name'])
            return False
        if row['Gender'] == 'female' or row['Gender'] == 'male':
            row['gender'] = row['Gender']
        else:
            self.kwargs['logger'].debug('Gender invalid (%s)', row['Gender'])
            return False
        self.update(row, row['Price'], row['PriceSale'], row['Name'])

        return True
