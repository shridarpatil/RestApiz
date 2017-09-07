#!/bin/python
# -*- coding: utf-8 -*-

"""Return user roles."""


def user_roles(cursor, connection, id):
    """
    Return user roles.

    :param cursor: database cursor object
    :param connection: database connection object
    :param id: user id
    """
    cursor.execute(
        """
         SELECT `role_id` FROM `user_roles` WHERE `user_id` = {}
        """.format(id)
    )
    return cursor.fetchall()
