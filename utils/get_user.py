#!/bin/python
# -*- coding: utf-8 -*-

"""Return user data."""
from .exceptions import InvalidUsage


def user(cursor, connection, token):
    """
    Return user_id and user name.

    :param cursor: database cursor object
    :param connection: database connection object
    :param token: user token
    :param endpoint: route name
    """
    if token is None:
        raise InvalidUsage("No token", 403)
    cursor.execute(
        """
         select id, user_name from user where token='{}'
        """.format(token)
    )
    return cursor.fetchone()
