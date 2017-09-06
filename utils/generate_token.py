#!/bin/python
# -*- coding: utf-8 -*-

"""Print."""

import uuid
import hashlib


def generate_token():
    """Validate Token"""
    return hashlib.sha1(str(uuid.uuid4()) + "salt").hexdigest()
