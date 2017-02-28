'''This module defines a logger class FlowLogger that logs runtime messages(and errors)
to a log file and stdout. It rotates the log file when it reached a configurable
size limit. A FlowLoggerWatcher class is provided to watch the system disk space
and deletes log files whenever necessary'''

import logging
import os
import sys
from flow.config import log_file_path, log_level_file, log_level_stdout, log_file_size_in_bytes


class FlowLogger:
    '''A universal logger class, logs to file and stdout'''

    def __init__(self, site, country):
        self.__logger = site + '.' + country
        self.__logger_format = \
            '[%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d]:\n\t - %(message)s'
        self.__setup()

    def __setup(self):
        'set up loggers'
        flow_logger_levels = {'debug': logging.DEBUG,
                              'info': logging.INFO,
                              'warning': logging.WARNING,
                              'error': logging.ERROR,
                              'critical': logging.CRITICAL}
        self.log_level_f = flow_logger_levels[log_level_file]
        self.log_level_s = flow_logger_levels[log_level_stdout]
        self.formatter = logging.Formatter(self.__logger_format)
        self.logger = logging.getLogger(self.__logger)
        self.logger.setLevel(logging.NOTSET)
        self.__setup_file_logger()
        self.__setup_stdout_logger()

    def __setup_file_logger(self):
        file_handler = logging.handlers.RotatingFileHandler(self.__logger + ".log",
                                                            maxBytes=log_file_size_in_bytes)
        file_handler.setLevel(self.log_level_f)
        file_handler.setFormatter(self.formatter)
        self.logger.addHandler(file_handler)

    def __setup_stdout_logger(self):
        stdout_handler = logging.StreamHandler(sys.stdout)
        stdout_handler.setLevel(self.log_level_s)
        stdout_handler.setFormatter(self.formatter)
        self.logger.addHandler(stdout_handler)

    def __getattr__(self, attrname):
        'route log requests to logger object'
        return getattr(self.logger, attrname)

class FlowLoggerWatcher:
    'Disk watcher class, runs to delete log files if necessary'

    def __call__(self):
        'One pass check disk status, and delete old log files if necessary'
        while self.__disize():
            next_file = self.__nextfile()
            if next_file:
                os.remove(next_file)

    def __disize(self):
        '''If the disk usage exceeds a limit (75%), start to delete
        old log files from the disk'''
        stats = os.statvfs(log_file_path)
        total = stats.f_blocks * stats.f_frsize
        used = (stats.f_blocks - stats.f_bfree) * stats.f_frsize
        if used / total > 0.75:
            return True
        return False

    def __nextfile(self):
        'Get the oldest file in log file directory or None if empty'
        try:
            return min((os.path.join(dirname, filename)
                        for dirname, _, filenames in os.walk(log_file_path)
                        for filename in filenames), key=lambda fn: os.stat(fn).st_mtime)
        except:
            return None
