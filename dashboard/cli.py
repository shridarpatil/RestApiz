#!/bin/python
# -*- coding: utf-8 -*-

import json
import RestApiz

from flask import Flask, send_file, jsonify


app = Flask(__name__)

@app.route("/admin")
def admin():
    return send_file("/home/RestApi/dashboard/public/index.html")


@app.errorhandler(404)
def page_not_found(e):
    return jsonify({"error":'404.html'}), 404


def main():

    app.run(debug=True, port=60000, host='127.0.1.1')
if __name__ == "__main__":

    app.run(debug=True, port=60000, host='127.0.1.1')
