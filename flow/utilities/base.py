'''base class for downloader, parser filter, manager'''

import os
import errno
from flow.utilities.logger import FlowLogger


class CBase:
    '''CBase for downloader, parser filter, manager'''

    def __init__(self, kwargs):
        self.kwargs = kwargs
        self.__ensure_logger()
        self.__ensure_download_files()

    def __ensure_logger(self):
        'Ensure logger is properly created if not already'
        kwargs = self.kwargs
        kwargs['log_file_ext'] = ('.log' if 'log_file_ext' not in kwargs
                                  else kwargs['log_file_ext'])
        kwargs['log_level_file'] = ('info' if 'log_level_file' not in kwargs
                                    else kwargs['log_level_file'])
        kwargs['log_level_stdout'] = ('info' if 'log_level_stdout' not in kwargs
                                      else kwargs['log_level_stdout'])
        kwargs['log_file_size_in_bytes'] = (0x500000
                                            if 'log_file_size_in_bytes' not in kwargs
                                            else kwargs['log_file_size_in_bytes'])
        kwargs['log_file_count'] = (10 if 'log_file_count' not in kwargs
                                    else kwargs['log_file_count'])
        kwargs['logger'] = (FlowLogger(kwargs['site'], kwargs['country'],
                                       kwargs['log_path'],
                                       kwargs['log_file_ext'],
                                       kwargs['log_level_file'],
                                       kwargs['log_level_stdout'],
                                       kwargs['log_file_size_in_bytes'],
                                       kwargs['log_file_count'])
                            if 'logger' not in kwargs
                            else kwargs['logger'])

    def __ensure_download_files(self):
        'ensure download directory is created, and file parameters are set'
        kwargs = self.kwargs
        try:
            os.makedirs(kwargs['download_path'])
        except OSError as err:
            if err.errno != errno.EEXIST:
                raise
        if 'download_file' not in kwargs:
            kwargs['download_file'] = os.path.join(
                kwargs['download_path'],
                kwargs['site'] + '.' + kwargs['country'] + '.txt')
        if 'parsed_file' not in kwargs:
            kwargs['parsed_file'] = os.path.join(
                kwargs['download_path'],
                kwargs['site'] + '.' + kwargs['country'] + '.csv')
