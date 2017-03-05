'''base class for downloader, parser filter, manager'''

from flow.utilities.logger import FlowLogger


class CBase:
    '''CBase for downloader and parser filter'''

    def __init__(self):
        pass

    def ensure_logger(self, kwargs):
        'Ensure logger is properly created if not already'
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
                                       kwargs['log_level_file'],
                                       kwargs['log_level_stdout'],
                                       kwargs['log_file_size_in_bytes'],
                                       kwargs['log_file_count'])
                            if 'logger' not in kwargs
                            else kwargs['logger'])
