#!/bin/python
# -*- coding: utf-8 -*-

"""Return route roles."""


def route_roles(cursor, connection, end_point):
    """
    Return route roles.

    :param cursor: database cursor object
    :param connection: database connection object
    :param end_point: user end_point
    """
    cursor.execute(
        """
         SELECT a.`role_id` FROM `route_access_roles` as a
            JOIN py_restapi as p on p.id = a.route_id
            WHERE  p.route_name = '{}'
        """.format(end_point)
    )
    return cursor.fetchall()
