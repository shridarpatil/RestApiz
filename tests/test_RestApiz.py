#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `RestApiz` package."""

import json
import pytest

from RestApiz import RestApiz  # noqa

from flask import Flask
from flask_cors import CORS

app = Flask(__name__)

CORS(app)

with open('tests/dbConfig.json') as data_file:
    data = json.load(data_file)


@pytest.fixture
def response():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    # import requests
    # return requests.get('https://github.com/audreyr/cookiecutter-pypackage')


def test_content(response):
    """Sample pytest test function with the pytest fixture as an argument."""
    # from bs4 import BeautifulSoup
    # assert 'GitHub' in BeautifulSoup(response.content).title.string
    # RestApiz.create_api(
    #     app,
    #     host=data["databaseHostName"],
    #     user_name=data['databaseUserName'],
    #     password=data['databasePassword'],
    #     database=data['databaseName']
    # )
