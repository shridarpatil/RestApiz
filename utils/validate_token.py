#!/bin/python
# -*- coding: utf-8 -*-

"""Validate token."""
from .exceptions import InvalidUsage


def validate_token(cursor, connection, token, endpoint):
    """
    Validate Token.

    :param cursor: database cursor object
    :param connection: database connection object
    :param token: user token
    :param endpoint: route name
    """
    if endpoint != 'login':
        if token is None:
            raise InvalidUsage("No token", 403)
        cursor.execute(
            """
            select exists(select id from user where token='{}') as token
            """.format(token)
        )
        if cursor.fetchone()['token'] == 0:
            raise InvalidUsage("Invalid Token", status_code=403)
