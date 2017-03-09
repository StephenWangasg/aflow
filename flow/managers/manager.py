'''MongoDB manager'''

import os
import csv
import uuid
import datetime
import pymongo
import flow.utilities.utils as utils
from flow.utilities.access import Access
from flow.utilities.base import CBase


class Manager(CBase):
    '''Manage the url'''

    @staticmethod
    def get_unique_urls_from_db(kwargs):
        '''Query database, return a set of urls.'''
        return {row['unique_url'] for row in kwargs['accessor'].products.find(
            {'site': kwargs['site'], 'location': kwargs['country']}, {'unique_url': 1})}

    @staticmethod
    def get_unique_urls_from_csv(kwargs):
        '''Extract parser csv, return a set of urls.'''
        new_csv = csv.DictReader(
            open(kwargs['parsed_file'], 'rb'), delimiter='\t', quotechar='"')
        return {row['unique_url'] for row in new_csv}

    @staticmethod
    def get_diff_urls(kwargs):
        '''
        Calculate 3 URL sets:
        delete_urls: to be deleted from database
        new_urls: to be inserted into database
        same_urls: to be updated in the database
        '''
        previous_unique_urls = Manager.get_unique_urls_from_db(kwargs)
        new_unique_urls = Manager.get_unique_urls_from_csv(kwargs)

        if len(new_unique_urls) == 0:
            # when download error happens, no new urls parsed from previous
            # step
            delete_urls = set()
            new_urls = set()
            same_urls = set()
        else:  # normal url comparision operation
            delete_urls = previous_unique_urls - new_unique_urls
            new_urls = new_unique_urls - previous_unique_urls
            same_urls = new_unique_urls & previous_unique_urls

        return new_urls, delete_urls, same_urls

    def __init__(self, kwargs):
        kwargs['log_file_ext'] = '.manage'
        CBase.__init__(self, kwargs)
        self.kwargs['accessor'] = Access(kwargs)

    def update_insert_delete_urls(self):
        '''
        Update database based on 3 url sets.
        Delete urls in delete_urls set
        Insert urls in new_urls set
        Update urls in same_urls set
        '''
        start_time = datetime.datetime.utcnow()
        self.kwargs['logger'].info('Start updating Mongodb (update/insert/delete) urls at %s',
                                   start_time.strftime("%X,%B %d,%Y"))
        current_parsed_path = self.kwargs['parsed_file']
        website = self.kwargs['site']
        country = self.kwargs['country']
        feed = self.kwargs['feed_images_path']
        if not os.path.isdir(feed):
            os.mkdir(feed)
        image_paths = []

        new_urls, delete_urls, same_urls = self.get_diff_urls(self.kwargs)

        for delete_url in delete_urls:
            self.kwargs['logger'].info(
                'remove url from mongodb: (%s)', delete_url)
            self.kwargs['accessor'].products.delete_one(
                {'unique_url': delete_url})

        for row in csv.DictReader(open(current_parsed_path, 'rb'), delimiter='\t', quotechar='"'):
            if len(new_urls) > 0 and row['unique_url'] in new_urls:
                row.update(
                    {'extracted': False, 'location': country, 'site': website})
                row['image_name'] = str(uuid.uuid1()) + '.jpg'
                row['image_path'] = os.path.join(feed, row['image_name'])
                row['hashedId'] = utils.get_hashed_st(row['image_url'])
                try:
                    self.kwargs['accessor'].products.insert(row)
                except pymongo.errors.DuplicateKeyError:
                    self.kwargs['logger'].warning(
                        'insert new product (%s) into mongodb error: DuplicateKeyError',
                        row['unique_url'])
                    continue
                self.kwargs['logger'].debug(
                    'insert url into mongodb: (%s)', row['unique_url'])
                image_paths.append((row['image_url'], row['image_path']))
            elif len(same_urls) > 0 and row['unique_url'] in same_urls:
                self.kwargs['accessor'].products.update_one(
                    {'unique_url': row['unique_url']},
                    {'$set': {'display_price': row['display_price']}})
                self.kwargs['logger'].debug(
                    'update mongodb url: (%s)', row['unique_url'])

        new_urls_len = len(new_urls)
        delete_urls_len = len(delete_urls)
        same_urls_len = len(same_urls)
        self.kwargs['accessor'].ingestion.update_one(
            {
                'site': website,
                'location': country
            },
            {
                '$push': {
                    'counts': {
                        'date': datetime.datetime.utcnow(),
                        'newCount': new_urls_len,
                        'deleteCount': delete_urls_len,
                        'overlapCount': same_urls_len
                    }}
            }, upsert=True)

        self.kwargs['logger'].info('Manager summary:')
        self.kwargs['logger'].info('New: %d, Delete: %d, Update: %d',
                                   new_urls_len, delete_urls_len, same_urls_len)
        end_time = datetime.datetime.utcnow()
        self.kwargs['logger'].info('Finish updating mongodb at %s, duration %d sec',
                                   end_time.strftime("%X,%B %d,%Y"),
                                   (end_time - start_time).total_seconds())
        return new_urls_len, delete_urls_len, same_urls_len
#         # pool = eventlet.GreenPool()
#         # for _ in pool.imap(utils.download_image, image_paths[:10]):
#         #     pass
