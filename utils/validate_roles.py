#!/bin/python
# -*- coding: utf-8 -*-

"""Validate roles."""
from .exceptions import InvalidUsage
from .get_user_roles import user_roles
from .get_route_access_roles import route_roles
from .get_user import user


def validate_roles(cursor, connection, token, endpoint):
    """
    Validate Roles.

    :param cursor: database cursor object
    :param connection: database connection object
    :param token: user token
    :param endpoint: route name
    """
    user_data = user(cursor, connection, token)
    if endpoint != 'login' and user_data['user_name'] != 'Administrator':
        route_access_roles = route_roles(cursor, connection, endpoint)
        if route_access_roles:
            user_access_roles = user_roles(cursor, connection, user_data['id'])
            if user_access_roles:
                for route_role in user_access_roles:
                    for user_role in user_access_roles:
                        if route_role['role_id'] == user_role['role_id']:
                            pass
                        else:
                            raise InvalidUsage("No access", status_code=403)
            else:
                raise InvalidUsage("No access", status_code=403)
