#!/bin/python
# -*- coding: utf-8 -*-

"""Print."""
from .exceptions import InvalidUsage
from flask import request


def update_token(cursor, connection, token, new_token):
    """Validate Token"""
    if request.endpoint == 'login':
        args = request.args.to_dict()
        user_name = args['user_name']
        query = """
                    UPDATE `user` set token='{}' where user_name='{}'
                """.format(new_token, user_name)
    else:
        query = """
                    UPDATE `user` set token='{}' where token = '{}'
                """.format(new_token, token)
    try:
        cursor.execute(query)
    except Exception as e:
        raise InvalidUsage(
            'Query Error check logs for details', status_code=400
        )
    try:
        connection.commit()
    except Warning as e:
        raise e
