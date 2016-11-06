# -*- coding: utf-8 -*-
import os
import json
import datetime
import logging

LOGGER = logging.getLogger("DataAccess")

class DataAccess(object):
    """
    A ver simple data access module.
    It stores all data in a folder. For each day, it saves a json file like
    "2016-11-04.json".

    """
    def __init__(self, path):
        self.path = path
        if not os.path.exists(path):
            os.mkdir(path)

    def list_logs(self):
        """
        List all logs. Sorted reversely by file name.
        """
        filenames = sorted(os.listdir(self.path), reverse=True)
        return [x.split('.')[0] for x in filenames]

    def read_log(self, date):
        """
        Get a log by its date
        :param dateime.date date: the date
        :return dict: log data parsed from the json file
        """
        filename = os.path.join(self.path, "{0}.json".format(date))
        LOGGER.debug("Loading log {0}".format(filename))
        if os.path.exists(filename):
            return json.load(open(filename))
        LOGGER.warn("Failed to load log for {0}".format(date))
        return None

    def write_log(self, log):
        """
        Write a log to disk.
        :param dict log: log information
        :param datetime.date date: date of the log. If none, it's today
                                   in local time zone
        """
        filename = os.path.join(self.path, "{0}.json".format(log['date']))
        with open(filename, 'w') as f:
            json.dump(log, f, indent=4, sort_keys=True)
