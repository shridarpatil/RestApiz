#!/usr/bin/env flask
# -*- coding: utf-8 -*-

import json
import os

from RestApiz import RestApiz

from flask import Flask
from flask import jsonify


app = Flask(__name__)

with open('dbConfig.json') as data_file:
    data = json.load(data_file)


def create_api(app):
    RestApiz.create_api(app,
        host=data["databaseHostName"],
        user_name=data['databaseUserName'],
        password=data['databasePassword'],
        database=data['databaseName']
    )


@app.route("/admin")
def admin():
    return send_file("public/index.html")


@app.errorhandler(404)
def page_not_found(e):
    return jsonify({"error":'404.html'}), 404


if __name__ == "__main__":
    create_api(app)
    app.run(debug=os.getenv("debug_mode", False), port=60001, host='127.0.1.1')
    app.run(debug=os.getenv("debug_mode", False), port=60000, host='127.0.1.1')
    # app.run(debug=False, request_handler=RestApiz.RequestHandler, port=3000)
