#!/bin/python
# -*- coding: utf-8 -*-

"""Create tables."""

import hashlib


def test(a):
    """Test"""
    print(a)


def encrypt_password(data):
    """Encrypt password."""
    password = data['query_params']['password']
    data['query_params']['password'] = hashlib.md5(
        password.encode('utf-8')
    ).hexdigest()
