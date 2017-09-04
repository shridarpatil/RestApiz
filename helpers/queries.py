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
    "user": {
        "sql": """CREATE TABLE IF NOT EXISTS `rest_api`.`user` (
                  `id` INT(10) NOT NULL AUTO_INCREMENT ,
                  `user_name` VARCHAR(100) NOT NULL ,
                  `password` VARCHAR(100) NOT NULL ,
                  PRIMARY KEY (`id`),
                  UNIQUE `user_ibfk_1` (`user_name`)
              ) ENGINE = InnoDB;
              """
    },
    "role": {
        "sql": """CREATE TABLE IF NOT EXISTS `roles` (
                  `id` INT(10) NOT NULL ,
                  `name` VARCHAR(50) NOT NULL ,
                  PRIMARY KEY (`id`),
                   UNIQUE `role_ibfk_1` (`name`)) ENGINE = InnoDB;"""
    }
}

USERS = {
    "Administrator": {
        "sql": """INSERT INTO `user` (`id`, `user_name`, `password`)
                VALUES ('', 'Administrator','27db7898211c8ccbeb4d5a97d198839a')
            """
    }
}

ROUTES = {
    "login": {
        "sql": """INSERT INTO `py_restapi` (
                `id`, `url`, `method`, `query`, `before_query`, `after_query`)
                VALUES (
                    NULL,
                    'login',
                    'GET',
                    'select id from user where user_name=:user_name and password=:password ',
                    'auth.auth:encrypt_password', ''
                )
              """
    }
}
