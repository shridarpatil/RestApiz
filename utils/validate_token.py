#!/bin/python
# -*- coding: utf-8 -*-

"""Print."""
from .exceptions import InvalidUsage


def validate_token(cursor, connection, token, endpoint):
    """Validate Token"""
    if endpoint != 'login':
        if token is None:
            raise InvalidUsage("No token", 403)
        cursor.execute(
            """
            select exists(select id from user where token='{}') as token
            """.format(token)
        )
        if cursor.fetchone()['token'] == 0:
            raise InvalidUsage("Invalid Token")
