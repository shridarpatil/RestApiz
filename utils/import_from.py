#!/bin/python
# -*- coding: utf-8 -*-

"""Dynamically import function"""


import os
from utils.exceptions import ResourceNotFound


def import_func(path):
    """
    Import an attribute, function or class from a module.

    :attr path: A path descriptor in the form of
                'pkg.module.submodule:attribute'
    :type path: str
    """
    path_parts = path.split(':')
    if len(path_parts) != 2:
        raise ImportError(
            "Path must be in the form of pkg.module.submodule:attribute"
        )
    folders = path_parts[0].split('.')[:-1]
    file_path = ''
    for folder_name in folders:
        file_path += '{}/'.format(folder_name)
        init_file = "{}/__init__.py".format(file_path)
        if not os.path.isfile(init_file):
            try:
                open("{}__init__.py".format(file_path), "w+").close()
            except IOError as e:
                ResourceNotFound("No such directory: '{}'".format(file_path))

    try:
        module = __import__(path_parts[0], fromlist=path_parts[1])
    except AttributeError as e:
        raise e
    return getattr(module, path_parts[1])
