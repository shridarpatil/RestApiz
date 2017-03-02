# Flask-RestApi
RestApi module is used to create rest apis dynamically

## Getting Started

import RestApi

### Prerequisites
Flask, MySQL

Example 

from flask import Flask
import RestApi

app = Flask(__name__)

RestApi.createApi(app, host="localhost", userName='', password='', database='')
if __name__ == "__main__":
    app.run(debug=True)
