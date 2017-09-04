#!/bin/python
# -*- coding: utf-8 -*-

"""Create tables."""
import pymysql

from tables import TABLES


def create_tables(cursor, conn):
    """
    Create tables.

    :param cursor: databse cursor
    :param conn: database conn
    """
    sql_notes(0, cursor)
    for table_name, value in TABLES.iteritems():
        print "Creating table : {}".format(table_name)
        try:
            cursor.execute(value['sql'])
        except Exception as e:
            raise e
        except pymysql.Warning as e:
            print e

        conn.commit()
    sql_notes(1, cursor)


def sql_notes(status, cursor):
    """Temporarily cahn the "Table already exists" warning."""
    cursor.execute("SET sql_notes = {};".format(status))
