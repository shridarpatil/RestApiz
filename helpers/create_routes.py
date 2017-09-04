#!/bin/python
# -*- coding: utf-8 -*-

"""Create Users."""
import pymysql

from .queries import ROUTES


def create_routes(cursor, conn):
    """
    Create Admin user.

    :param cursor: databse cursor
    :param conn: database conn
    """
    for user_name, value in ROUTES.iteritems():
        print("Creating Route: {}".format(user_name))
        try:
            cursor.execute(value['sql'])
        except pymysql.err.IntegrityError:
            pass
        conn.commit()
