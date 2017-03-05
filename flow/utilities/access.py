'''One-stop access to servers.'''

from pymongo import MongoClient


class Access:
    '''An entry class for accessing the various servers'''

    def __init__(self, kwargs):
        self.kwargs = kwargs
        self.defined = False
        self.loopup = {}

    def __ensure_mongo(self):
        if not self.defined:
            client = MongoClient(
                self.kwargs['mongo_host'], self.kwargs['mongo_port'])
            self.loopup = {
                'mongo': client,
                'fashion': client['fashion'],
                'products': client['fashion']['products'],
                'ingestion': client['fashion']['ingestion'],
            }
            self.defined = True

    def __getattr__(self, attrname):
        self.__ensure_mongo()
        if attrname in self.loopup:
            return self.loopup[attrname]
        else:
            raise AttributeError(attrname)
