__author__ = 'Amit Mohapatra'

import sys
from os import sep
import logging
import logging.handlers


class Logger(object):
    """
    created a system for log format
    """

    def __init__(self, conf_obj):
        log_file_path = "%s%s%s" % (conf_obj.setup.local_log_path, sep, "sentiment-analysis-app.log")
        log_backup_count = conf_obj.setup.log_backup_count
        log_size_in_bytes = conf_obj.setup.log_size_in_bytes

        log = logging.getLogger('')
        log.setLevel(logging.DEBUG)
        format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', '%a, %d %b %Y %H:%M:%S')

        ch = logging.StreamHandler(sys.stdout)
        ch.setFormatter(format)
        log.addHandler(ch)

        fh = logging.handlers.RotatingFileHandler(log_file_path, maxBytes=log_size_in_bytes,
                                                  backupCount=log_backup_count)
        fh.setFormatter(format)
        log.addHandler(fh)

