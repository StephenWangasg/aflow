'''This module defines a logger class FlowLogger that logs runtime messages(and errors)
to a log file and stdout. It rotates the log file when it reached a configurable
size limit. A FlowLoggerWatcher class is provided to watch the system disk space
and deletes log files whenever necessary'''

import os
import sys
import errno
import logging.handlers


class FlowLogger:
    '''A universal logger class, logs to file and stdout'''

    def __init__(self, site, country, log_file_path, log_file_ext='.log',
                 log_level_file='debug', log_level_stdout='debug',
                 log_file_size_in_bytes=0x3200000, log_file_count=10):
        self.log_file_path = log_file_path
        self.log_file_ext = log_file_ext
        self.log_level_file = log_level_file
        self.log_level_stdout = log_level_stdout
        self.log_file_size_in_bytes = log_file_size_in_bytes
        self.log_file_count = log_file_count
        self.__logger = site + '.' + country
        self.__logger_format = \
            '[%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d]: - %(message)s'
        self.__setup()

    def __setup(self):
        'set up loggers'
        flow_logger_levels = {'debug': logging.DEBUG,
                              'info': logging.INFO,
                              'warning': logging.WARNING,
                              'error': logging.ERROR,
                              'critical': logging.CRITICAL}
        self.log_level_f = flow_logger_levels[self.log_level_file]
        self.log_level_s = flow_logger_levels[self.log_level_stdout]
        self.formatter = logging.Formatter(self.__logger_format)
        self.logger = logging.getLogger(self.__logger)
        self.logger.propagate = False
        self.logger.setLevel(logging.DEBUG)
        self.__setup_file_logger()
        self.__setup_stdout_logger()

    def __setup_file_logger(self):
        try:
            os.makedirs(self.log_file_path)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
        file_handler = logging.handlers.RotatingFileHandler(
            os.path.join(self.log_file_path,
                         self.__logger + self.log_file_ext),
            maxBytes=self.log_file_size_in_bytes,
            backupCount=self.log_file_count)
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


class FlowDiskWatcher:
    'Utility class watch disk usage'

    def __init__(self):
        pass

    @staticmethod
    def free(watch_dir):
        stats = os.statvfs(watch_dir)
        return stats.f_bavail * stats.f_frsize

    @staticmethod
    def used(watch_dir):
        stats = os.statvfs(watch_dir)
        return (stats.f_blocks - stats.f_bfree) * stats.f_frsize

    @staticmethod
    def total(watch_dir):
        stats = os.statvfs(watch_dir)
        return stats.f_blocks * stats.f_frsize


class FlowLoggerWatcher:
    'Disk watcher class, runs to delete log files if necessary'

    def __init__(self, log_file_path, percentage_limit=0.75):
        self.log_file_path = log_file_path
        self.percentage_limit = percentage_limit

    def __call__(self):
        'One pass check disk status, and delete old log files if necessary'
        while self.__disize():
            next_file = self.__nextfile()
            if next_file:
                os.remove(next_file)
            else:
                break

    def __disize(self):
        '''If the disk usage exceeds a limit, start to delete
        old log files from the disk'''
        total = FlowDiskWatcher.total(self.log_file_path)
        used = FlowDiskWatcher.used(self.log_file_path)
        percentage = float(used) / total
        if percentage > self.percentage_limit:
            return True
        return False

    def __nextfile(self):
        'Get the oldest file in log file directory or None if empty'
        try:
            return min((os.path.join(dirname, filename)
                        for dirname, _, filenames in os.walk(self.log_file_path)
                        for filename in filenames), key=lambda fn: os.stat(fn).st_mtime)
        except:
            return None
