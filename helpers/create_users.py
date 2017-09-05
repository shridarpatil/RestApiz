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
    print(""" \033[32m
===================================================
                Creating User
===================================================
          \033[0m""")
    for user_name, value in USERS.iteritems():
        print("User: {}".format(user_name))
        try:
            cursor.execute(value['sql'])
        except pymysql.err.IntegrityError:
            pass
        conn.commit()
