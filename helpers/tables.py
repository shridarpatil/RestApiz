#!/bin/python
# -*- coding: utf-8 -*-

"""Create tables."""

TABLES = {
    "py_restapi": {
        "sql": """CREATE TABLE IF NOT EXISTS `py_restapi` (
                  `id` int(11) NOT NULL PRIMARY KEY AUTO_INCREMENT,
                  `url` varchar(255) NOT NULL UNIQUE,
                  `method` enum('GET','POST','PUT','DELETE') NOT NULL,
                  `query` varchar(255) NOT NULL,
                  `before_query` varchar(255) NOT NULL,
                  `after_query` varchar(255) NOT NULL
                ) ENGINE=InnoDB DEFAULT CHARSET=latin1"""
    },
    "test_py_restapi": {
        "sql": """CREATE TABLE IF NOT EXISTS `py_restapi` (
                  `id` int(11) NOT NULL PRIMARY KEY AUTO_INCREMENT,
                  `url` varchar(255) NOT NULL UNIQUE,
                  `method` enum('GET','POST','PUT','DELETE') NOT NULL,
                  `query` varchar(255) NOT NULL,
                  `before_query` varchar(255) NOT NULL,
                  `after_query` varchar(255) NOT NULL
                ) ENGINE=InnoDB DEFAULT CHARSET=latin1"""
    }
}
