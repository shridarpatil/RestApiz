#!/bin/python
# -*- coding: utf-8 -*-

"""Create tables."""

TABLES = {
    "py_restapi": {
        "sql": """CREATE TABLE IF NOT EXISTS `py_restapi` (
                  `id` int(11) NOT NULL PRIMARY KEY AUTO_INCREMENT,
                  `route_name` varchar(255) NOT NULL UNIQUE,
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
                  `token` VARCHAR(100) NOT NULL ,
                  PRIMARY KEY (`id`),
                  UNIQUE `user_ibfk_1` (`user_name`)
              ) ENGINE = InnoDB;
              """
    },
    "role": {
        "sql": """CREATE TABLE IF NOT EXISTS `roles` (
                  `id` INT(10) NOT NULL AUTO_INCREMENT ,
                  `name` VARCHAR(50) NOT NULL ,
                  PRIMARY KEY (`id`),
                   UNIQUE `role_ibfk_1` (`name`)) ENGINE = InnoDB;"""
    },
    "user_roles": {
        "sql": """CREATE TABLE IF NOT EXISTS `user_roles` (
                  `id` INT NOT NULL AUTO_INCREMENT ,
                  `user_id` INT NOT NULL ,
                  `role_id` INT NOT NULL ,
                  PRIMARY KEY (`id`),
                  INDEX `ibfk_user_roles_1` (`user_id`),
                  INDEX `ibfk_user_roles_2` (`role_id`)
                ) ENGINE = InnoDB;"""
    },
    "route_access_roles": {
        "sql": """CREATE TABLE IF NOT EXISTS `route_access_roles` (
                 `id` INT(10) NOT NULL AUTO_INCREMENT ,
                 `route_id` INT(10) NOT NULL ,
                 `role_id` INT(10) NOT NULL ,
                 PRIMARY KEY (`id`),
                 INDEX `ibfk_route_access_roles_1` (`route_id`),
                 INDEX `ibfk_route_access_2` (`role_id`)
              ) ENGINE = InnoDB;
              """
    }
}

USERS = {
    "Administrator": {
        "sql": """INSERT INTO `user` (`user_name`, `password`)
                VALUES ('Administrator','r00t')
            """
    }
}

ROUTES = {
    "login": {
        "sql": """INSERT INTO `py_restapi` (
                `id`, `route_name`, `method`, `query`, `before_query`, `after_query`)
                VALUES (
                    NULL,
                    'login',
                    'GET',
                    'select id from user where user_name=:user_name and password=:password ',
                    '', ''
                )
              """
    }
}

UPDATE_TABLE_STRUCTURE = {
    "Foreign key constraints": {
        "sql": [
            """ALTER TABLE `user_roles`
              ADD CONSTRAINT `ibfk_user_roles_1` FOREIGN KEY (`user_id`)
              REFERENCES `user`(`id`) ON DELETE RESTRICT ON UPDATE RESTRICT;
            """,

            """ALTER TABLE `user_roles`
              ADD CONSTRAINT `ibfk_user_roles_2` FOREIGN KEY (`role_id`)
              REFERENCES `roles`(`id`)
              ON DELETE RESTRICT ON UPDATE RESTRICT;""",

            """ALTER TABLE `route_access_roles`
              ADD CONSTRAINT `ibfk_route_access_roles_roles_1` FOREIGN KEY (`route_id`)
              REFERENCES `py_restapi`(`id`) ON DELETE RESTRICT ON UPDATE RESTRICT;
            """,

            """ALTER TABLE `route_access_roles`
              ADD CONSTRAINT `ibfk_route_access_roles_roles_2` FOREIGN KEY (`role_id`)
              REFERENCES `roles`(`id`) ON DELETE RESTRICT ON UPDATE RESTRICT;
            """,
            """ALTER TABLE `user` CHANGE `token` `token` VARCHAR(100) CHARACTER
            SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL;"""
        ]
    }
}
