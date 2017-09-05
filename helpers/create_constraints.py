#!/bin/python
# -*- coding: utf-8 -*-

"""Create Users."""
import pymysql

from .queries import UPDATE_TABLE_STRUCTURE


def create_foreign_key_constraints(cursor, conn):
    """
    Create Admin user.

    :param cursor: databse cursor
    :param conn: database conn
    """
    print("""\033[32m
===================================================
                Updating Tables
===================================================
          \033[0m """)
    for constraint, value in UPDATE_TABLE_STRUCTURE.iteritems():
        print("Updating : {}".format(constraint))
        for sql in value['sql']:
            try:
                cursor.execute(sql)
            except pymysql.err.IntegrityError:
                pass
            except pymysql.err.InternalError:
                pass
            conn.commit()
