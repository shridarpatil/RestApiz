#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Generate response body."""


def generate_response_body(
    response_body, success,
    response_type, data, message
):
    """Generate response_body."""
    response_body['success'] = success
    response_body['type'] = response_type
    response_body['data'] = data
    response_body['message'] = message
