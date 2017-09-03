# -*- coding: utf-8 -*-

"""Generate Rest like apis."""
# import json
import sys
import time

from flask import jsonify
from flask import request

import logging
import pymysql

from utils.import_from import import_func
from utils.response import generate_response_body
from werkzeug.serving import BaseRequestHandler


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
                self.create_get(row)
            elif row['method'].lower() == 'post':
                self.create_post(row)
            elif row['method'].lower() == 'put':
                self.create_put(row)

    def create_get(self, metadta):
        """
        Create route for all GET methods.

        :param utl : The route for the get method
        :param method : The rest method
        :param query : sql query
        """
        url = metadta['url']
        method = metadta['method']
        query = metadta['query']

        def get():
            logging.debug('Running /' + url)

            bag = {
                "request_body": request.args,
                "response_body": {},
            }

            generated_query = self.generate_query(
                bag['request_body'], query, ':'
            )
            logging.debug('generated_query /' + generated_query)

            c = self.c
            try:
                c.execute(generated_query)
                data = c.fetchall()
            except Exception as e:
                logging.error(e)
                raise InvalidUsage(str(e), status_code=400)

            if not data:
                response_type = 'Warning'
            else:
                response_type = 'Info'

            generate_response_body(
                bag['response_body'], 'success',
                response_type, data, 'Success'
            )
            logging.debug('Completed /' + url)
            return jsonify({"success": True, "type": type, "data": data})

        get.methods = [method]
        self.app.add_url_rule('/' + url, url, get)

    def create_post(self, metadta):
        """
        Create route for all POST methods

        :param utl : The route for the get method
        :param method : The rest method
        :param query : sql query
        """
        url = metadta['url']
        method = metadta['method']
        query = metadta['query']

        def post():
            logging.debug('Running /' + url)
            bag = {
                "request_body": request.get_json(force=True),
                "response_body": {},
            }

            values = self.generate_post_query(bag['request_body'], query)
            c = self.c
            conn = self.conn
            try:
                c.execute(query, values)
            except Exception as e:
                logging.error(e.message)
                raise InvalidUsage(str(e.message), status_code=400)

            id = conn.insert_id()
            conn.commit()

            logging.debug('Completed /' + url)

            generate_response_body(
                bag['response_body'], 'success',
                'info', id, 'Inserted successfully'
            )
            return jsonify(bag['response_body'])

        post.methods = [method]
        self.app.add_url_rule('/' + url, url, post)

    def create_put(self, metadta):
        """Create route for all PUT methods."""
        url = metadta['url']
        method = metadta['method']
        query = metadta['query']

        before_query = metadta['before_query']
        after_query = metadta['after_query']

        def put():
            logging.debug('Running /' + url)

            bag = {
                "request_body": request.get_json(force=True),
                "query_params": request.args,
                "response_body": {},
            }

            if before_query != '':
                before_query_func = import_func(before_query)
                before_query_func(bag)
            try:
                generated_query = self.generate_query(
                    bag['query_params'], query, ':'
                )
                generated_query = self.generate_query(
                    bag['request_body'], generated_query, ';'
                )
                logging.info('Query : {}'.format(generated_query))
            except Exception as e:
                logging.error(e)
                raise InvalidUsage(str(e), status_code=400)

            # values = self.generate_post_query(json, query)

            c = self.c
            conn = self.conn
            try:
                c.execute(generated_query)
            except Exception as e:
                logging.error(e)
                raise InvalidUsage(str(e), status_code=400)
            try:
                conn.commit()
            except Warning as e:
                raise e

            if after_query != '':
                after_query_func = import_func(after_query)
                after_query_func(bag)

            logging.debug('Completed /' + url)

            generate_response_body(
                bag['response_body'], 'success',
                'info', [], 'Updated successfully'
            )
            return jsonify(bag['response_body'])

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
                if isinstance(params[param], unicode):
                    params[param] = params[param].encode('utf-8', 'replace')

                if isinstance(params[param], str):
                    params_replace_text = "'" + str(params[param]) + "'"
                else:
                    params_replace_text = params[param]
            else:

                params_replace_text = params[param]
            logging.debug(params_replace_text)
            try:
                query = query.replace(q_symbol + param, params_replace_text)
            except TypeError:
                query = query.replace(
                    q_symbol + param, str(params_replace_text)
                )
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
