#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Exceptions to be raised by every other sub-package"""


__all__ = ['RestApixBaseException', 'ResourceNotFound']


class RestApixBaseException(Exception):
    """Base exception for crux utils."""

    pass


class ResourceNotFound(RestApixBaseException):
    """Resource not found exception"""

    pass


class DuplicateEntry(RestApixBaseException):
    """Mysql DuplicateEntry Error"""

    pass


class InvalidUsage(Exception):
    """Invalid Usage."""

    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        """Initialise."""
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        """To dict."""
        response = dict(self.payload or ())
        response['message'] = self.message
        response['success'] = False
        response['type'] = 'Error'
        return response
