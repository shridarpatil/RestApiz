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
