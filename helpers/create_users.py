#!/bin/python
# -*- coding: utf-8 -*-

"""Create Users."""
import pymysql

from .queries import USERS


def create_admin_user(cursor, conn):
    """
    Create Admin user.

    :param cursor: databse cursor
    :param conn: database conn
    """
    for user_name, value in USERS.iteritems():
        print("Creating User: {}".format(user_name))
        try:
            cursor.execute(value['sql'])
        except pymysql.err.IntegrityError:
            pass
        conn.commit()
