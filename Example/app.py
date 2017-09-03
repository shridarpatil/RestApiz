#!/bin/python
# -*- coding: utf-8 -*-

import json
from RestApiz import RestApiz

from flask import Flask, send_file, jsonify


app = Flask(__name__)



with open('dbConfig.json') as data_file:
    data = json.load(data_file)


class SimpleMiddleWare(object):
    """Simple WSGI middleware."""

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        print 'something you want done in every http request'
        print environ
        print start_response
        return self.app(environ, start_response)

# app.wsgi_app = SimpleMiddleWare(app.wsgi_app)


def create_api(app):
    RestApiz.create_api(
        app,
        host=data["databaseHostName"],
        user_name=data['databaseUserName'],
        password=data['databasePassword'],
        database=data['databaseName']
    )


@app.route("/admin")
def admin():
    return send_file("public/index.html")


@app.route("/reloadmetada")
def reload():
    print data
    create_api(app)
    return 'success'

@app.errorhandler(404)
def page_not_found(e):
    return jsonify({"error":'404.html'}), 404

@app.route('/ro')
def routes():
    routes = []
    for rule in app.url_map.iter_rules():

        if "GET" in rule.methods:
            url = rule.rule
            routes.append(url)

    return "routes" + str(routes)


if __name__ == "__main__":
    create_api(app)
    app.run(debug=True, port=60000, host='127.0.1.1', threaded=True)
    # app.run(debug=False, request_handler=RestApiz.RequestHandler, port=3000)
