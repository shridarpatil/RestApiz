# -*- coding: utf-8 -*-

"""Generate Rest like apis."""
import json
import sys
import time

from flask import jsonify
from flask import request
from flask import Response

import pymysql.cursors
from werkzeug.serving import BaseRequestHandler
import logging


class CreateService():
    """Create service."""

    def __init__(self, app, host, user, password, db):
        """Initialize."""
        self.app = app
        self.host = host
        self.user = user
        self.password = password
        self.db = db

        self.connection()

    def connection(self):
        """Connect to mysql database."""
        host = self.host
        user = self.user
        password = self.password
        db = self.db

        try:
            conn = pymysql.connect(
                host=host,
                user=user,
                password=password,
                db=db,
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )
            c = conn.cursor()
        except Exception as e:
            raise ValueError(e)

        self.c = c
        self.conn = conn
        self.generate_rest_api()

    def generate_rest_api(self):
        """Generate rest apis."""
        query = "select * from py_restapi"
        c = self.c
        c.execute(query)
        data = c.fetchall()

        for row in data:

            if row['method'].lower() == 'get':
                self.create_get(row['url'], row['method'], row['query'])
            elif row['method'].lower() == 'post':
                self.create_post(row['url'], row['method'], row['query'])
            elif row['method'].lower() == 'put':
                self.create_put(row['url'], row['method'], row['query'])

    def create_get(self, url, method, query):
        """
        Create route for all GET methods.

        :param utl : The route for the get method
        :param method : The rest method
        :param query : sql query
        """
        app = self.app

        def get():
            logging.debug('Running /' + url)
            query_params = request.args
            logging.debug(query_params)
            generated_query = self.generate_query(query_params, query, ':')
            logging.debug('generated_query /' + generated_query)

            c = self.c
            try:
                c.execute(generated_query)
                data = c.fetchall()
            except Exception as e:
                logging.error(e)
                raise InvalidUsage(str(e), status_code=400)

            if not data:
                type = 'Warning'
            else:
                type = 'Info'
            logging.debug('Completed /' + url)
            return Response(
                json.dumps({"success": True, "type": type, "data": data}),
                mimetype='application/json'
            )

        get.methods = [method]
        app.add_url_rule('/' + url, url, get)

    def create_post(self, url, method, query):
        """
        Create route for all POST methods

        :param utl : The route for the get method
        :param method : The rest method
        :param query : sql query
        """
        def post():
            logging.debug('Running /' + url)
            json = request.get_json(force=True)
            values = self.generate_post_query(json, query)
            c = self.c
            conn = self.conn
            try:
                c.execute(query, values)
                id = conn.insert_id()
                conn.commit()
                logging.debug('Completed /' + url)
                return
                return Response(
                    jsonify({"success": True, "type": "Info", "data": id}),
                    mimetype='application/json'
                )
            except Exception as e:
                logging.error(e.message)
                raise InvalidUsage(str(e.message), status_code=400)

        post.methods = [method]
        self.app.add_url_rule('/' + url, url, post)

    def create_put(self, url, method, query):
        """Create route for all PUT methods."""
        # pathBeforeReq = './hello'
        # funcNameBeforeReq = 'hell'

        # pathAfterReq = './hello'
        # funcNameAfterReq = 'hell'

        def put():
            logging.debug('Running /' + url)

            data = request.get_json(force=True)
            query_params = request.args

            # try:

            #   funcBeforeReq = self.generate_function(
            #     pathBeforeReq, funcNameBeforeReq
            # )

            # except TypeError as e:
            #     raise InvalidUsage(
            #         funcName + ' must return query_params, data',
            #         status_code=404
            # )

            # except Exception as e:
            #   raise InvalidUsage(str(e), status_code=404)

            # try:
            #     query_params, data = funcBeforeReq(
            #         InvalidUsage, query_params, data
            #     )

            # except Exception as e:
            #     raise InvalidUsage(
            #         'Error in function '+ funcNameBeforeReq,
            #         status_code=404, payload={'Error': str(e)}
            #     )

            try:
                generated_query = self.generate_query(query_params, query, ':')
                generated_query = self.generate_query(
                    data, generated_query, ';'
                )
                logging.debug('Query : ' + generated_query)
            except Exception as e:
                logging.error(e)
                raise InvalidUsage(str(e), status_code=404)

            # values = self.generate_post_query(json, query)

            c = self.c
            conn = self.conn
            try:
                c.execute(generated_query)
                conn.commit()
            except Exception as e:
                logging.error(e)
                raise InvalidUsage(str(e), status_code=400)

            # try:

            #     funcAfterReq = self.generate_function(
            #         pathAfterReq, funcNameAfterReq
            #     )

            # except TypeError as e:
            #     raise InvalidUsage(
            #         funcName + ' must return query_params, data',
            #         status_code=404
            #     )

            # except Exception as e:
            #     raise InvalidUsage(str(e), status_code=404)

            # try:
            #     query_params = funcAfterReq(InvalidUsage, query_params, data)

            # except Exception as e:
            #     raise InvalidUsage(
            #         'Error in function '+ funcNameBeforeReq,
            #         status_code=404, payload={'Error':str(e)}
            #     )

            logging.debug('Completed /' + url)
            return Response(
                jsonify({"success": True, "type": "Info", "data": []}),
                mimetype='application/json'
            )

        put.methods = [method]
        self.app.add_url_rule('/' + url, url, put)

    def generate_post_query(self, data, query):
        """Create insert query."""
        start_pt = query.find('(') + 1
        end_pt = query.find(')')
        params = query[start_pt:end_pt].split(',')
        values = []
        try:
            for param in params:
                values.append(data[param.replace(' ', '')])
        except Exception as e:
            logging.error(e.message)
            raise InvalidUsage(str(e.message), status_code=400)

        return values

    def generate_query(self, params, query, symbol):
        """Create GET, PUT, DELETE query."""
        q_symbol = symbol
        q_colon = query.find(q_symbol)
        if q_colon != -1:
            q_space = query.find(" ", q_colon)
            if q_space == -1:
                q_space = len(query)

            q_colon += 1

            param = query[q_colon:q_space]
            params_replace_text = ""
            if symbol == ";":
                if type(params[param]) == str:
                    params_replace_text = "'" + str(params[param]) + "'"
                else:
                    params_replace_text = params[param]
            else:

                params_replace_text = params[param]
            query = query.replace(q_symbol + param, params_replace_text)
            query = self.generate_query(params, query, q_symbol)
        return query

    def generate_function(self, path, function_name):
        """Generate function."""
        sys.path.insert(0, path)
        module_before_req = __import__(function_name)

        return getattr(module_before_req, function_name)


class InvalidUsage(Exception):
    """Invalid Usage."""

    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        """Initialise."""
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        """To dict."""
        rv = dict(self.payload or ())
        rv['message'] = self.message
        rv['success'] = 'False'
        rv['type'] = 'Error'
        return rv


def create_api(app, host=None, user_name=None, password=None, database=None):
    """Create Api."""
    if host is None:
        logging.error('host not found')
        raise ValueError('host not found')

    if user_name is None:
        logging.error('user_name not found')
        raise ValueError('user_name not found')

    if password is None:
        logging.error('password not found')
        raise ValueError('password not found')

    if database is None:
        logging.error('database not found')
        raise ValueError('database not found')

    logging.getLogger('Rest Api')
    logging.basicConfig(
        filename='RestApi.log', level=logging.DEBUG,
        format='Rest-Api %(asctime)s [%(levelname)-5.5s] %(message)s'
    )

    @app.errorhandler(InvalidUsage)
    def handle_invalid_usage(error):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response

    @app.before_request
    def before_request():

        LogClient(request)

    CreateService(app, host, user_name, password, database)
    print("""
            ______          _      ___        _
            | ___ \        | |    / _ \      (_)
            | |_/ /___  ___| |_  / /_\ \_ __  _
            |    // _ \/ __| __| |  _  | '_ \| |
            | |\ \  __/\__ \ |_  | | | | |_) | |
            \_| \_\___||___/\__| \_| |_/ .__/|_|
                                       | |
                                       |_|

    """)
    return True


class LogClient(object):
    """Docstring for LogClient."""

    def __init__(self, arg):
        """Initialise."""
        super(LogClient, self).__init__()
        self.arg = arg
        self.log_client()

    def log_client(self):
        """Log client."""
        logging.info('Client-IP: ' + self.arg.remote_addr)
        logging.info('User-Agent: ' + self.arg.headers.get('User-Agent'))


class RequestHandler(BaseRequestHandler):
    """Extend werkzeug request handler to suit our needs."""

    def handle(self):
        """Handle."""
        self.fancyStarted = time.time()
        rv = super(RequestHandler, self).handle()
        return rv

    def send_response(self, *args, **kw):
        """Send response."""
        self.fancyProcessed = time.time()
        super(RequestHandler, self).send_response(*args, **kw)

    def log_request(self, code='-', size='-'):
        """Log request."""
        duration = int((self.fancyProcessed - self.fancyStarted) * 1000)
        self.log('info', '"{0}" {1} {2} [{3}ms]'.format(
            self.requestline, code, size, duration)
        )
