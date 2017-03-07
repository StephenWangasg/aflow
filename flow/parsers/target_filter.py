
import parser


class TargetFilter(parser.IRowFilter):
    'target filter class'

    def filter(self, row):
        cats = [s.lower() for s in self.kwargs['cats']]
        if not any(word in row['Category'].lower() for word in cats):
            self.kwargs['logger'].debug(
                'Did not find category keywords in (%s)', row['Category'])
            return False
        if any(word.lower() in row['Product Name'].lower() for word in parser.INVALID_KEYWORDS):
            self.kwargs['logger'].debug(
                'Invalid keywords in Product Name field (%s)', row['Product Name'])
            return False
        prod_name = row['Product Name']
        if 'Women' in prod_name:
            row['gender'] = 'female'
        elif 'Men' in prod_name:
            row['gender'] = 'male'
        elif 'Girls' in prod_name:
            self.kwargs['logger'].debug(
                'Girls found in Product Name field (%s)', prod_name)
            return False
        elif 'Boys' in prod_name:
            self.kwargs['logger'].debug(
                'Boys found in Product Name field (%s)', prod_name)
            return False
        else:
            row['gender'] = -1
        row['currency'] = 'USD'

        self.update(row, row['Original Price'], row['Current Price'], prod_name)

        return True
