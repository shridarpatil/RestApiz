#!/bin/python
# -*- coding: utf-8 -*-

"""Log client details"""

import logging


class LogClient(object):
    """Docstring for LogClient."""

    def __init__(self, arg):
        """Initialise."""
        super(LogClient, self).__init__()
        self.arg = arg
        self.log_client()

    def log_client(self):
        """Log client."""
        logging.info('Client-IP: ' + self.arg.remote_addr)
        logging.info('User-Agent: ' + self.arg.headers.get('User-Agent'))
