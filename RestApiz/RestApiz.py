#!/bin/python
# -*- coding: utf-8 -*-

"""Generate Rest like apis."""
# import json
import time

from flask import jsonify
from flask import request

import logging as log
import pymysql

from utils.echo import echo
from utils.exceptions import InvalidUsage
from utils.import_from import import_func
from utils.log_client import LogClient
from utils.response import generate_response_body
from helpers.create_tables import create_tables
from helpers.create_routes import create_routes
from helpers.create_users import create_admin_user
from werkzeug.serving import BaseRequestHandler


class CreateService():
    """Create service."""

    def __init__(self):
        """Initialize."""

    def db_connect(self, host, user, password, db):
        """Connect to mysql database."""
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

        return c, conn

    def generate_rest_api(self, app, c, conn):
        """Generate rest apis."""
        self.app = app
        self.c = c
        self.conn = conn

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

        before_query = metadta['before_query']
        after_query = metadta['after_query']

        def get():
            log.debug('Running /' + url)

            bag = {
                "query_params": request.args.to_dict(),
                "response_body": {},
            }

            if before_query != '':
                before_query_func = import_func(before_query)
                before_query_func(bag)

            generated_query = self.generate_query(
                bag['query_params'], query, ':'
            )
            log.debug('Query :' + generated_query)

            c = self.c
            try:
                c.execute(generated_query)
                data = c.fetchall()
            except Exception as e:
                log.error(e)
                raise InvalidUsage(str(e), status_code=400)

            if after_query != '':
                after_query_func = import_func(after_query)
                after_query_func(bag)

            if not data:
                response_type = 'Warning'
                message = "resource not found"
            else:
                response_type = 'Info'
                message = "resource found successfully"

            generate_response_body(
                bag['response_body'], 'success',
                response_type, data, message
            )
            log.debug('Completed /' + url)
            return jsonify(bag['response_body']), 200

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

        before_query = metadta['before_query']
        after_query = metadta['after_query']

        def post():
            log.debug('Running /' + url)
            bag = {
                "request_body": request.get_json(force=True),
                "response_body": {},
            }

            values = self.generate_post_query(bag['request_body'], query)
            c = self.c
            conn = self.conn

            if before_query != '':
                before_query_func = import_func(before_query)
                before_query_func(bag)

            try:
                c.execute(query, values)
            except Exception as e:
                log.error(e.message)
                raise InvalidUsage(str(e.message), status_code=400)

            id = conn.insert_id()
            conn.commit()

            bag['response_body'] = id

            if after_query != '':
                after_query_func = import_func(after_query)
                after_query_func(bag)

            generate_response_body(
                bag['response_body'], 'success',
                'info', id, 'resource updated successfully'
            )

            log.debug('Completed /' + url)

            return jsonify(bag['response_body']), 201

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
            log.debug('Running /' + url)

            bag = {
                "request_body": request.get_json(force=True),
                "query_params": request.args.to_dict(),
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
                log.info('Query : {}'.format(generated_query))
            except Exception as e:
                log.error(e)
                raise InvalidUsage(str(e), status_code=400)

            # values = self.generate_post_query(json, query)

            c = self.c
            conn = self.conn
            try:
                c.execute(generated_query)
            except Exception as e:
                log.error(e)
                raise InvalidUsage(
                    'Query Error check logs for details', status_code=400
                )
            try:
                conn.commit()
            except Warning as e:
                raise e

            if after_query != '':
                after_query_func = import_func(after_query)
                after_query_func(bag)

            log.debug('Completed /' + url)

            generate_response_body(
                bag['response_body'], 'success',
                'info', [], 'resource updated successfully'
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
            log.error(e.message)
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
            # if symbol == ";":
            if isinstance(params[param], unicode):
                params[param] = params[param].encode('utf-8', 'replace')

            if isinstance(params[param], str):
                params_replace_text = "'" + str(params[param]) + "'"
            else:
                params_replace_text = params[param]
            # else:

            #     params_replace_text = params[param]

            try:
                query = query.replace(q_symbol + param, params_replace_text)
            except TypeError:
                query = query.replace(
                    q_symbol + param, str(params_replace_text)
                )
            query = self.generate_query(params, query, q_symbol)
        return query


def create_api(app, host=None, user_name=None, password=None, database=None):
    """Create Api."""
    if host is None:
        log.error('host not found')
        raise ValueError('host not found')

    if user_name is None:
        log.error('user_name not found')
        raise ValueError('user_name not found')

    if password is None:
        log.error('password not found')
        raise ValueError('password not found')

    if database is None:
        log.error('database not found')
        raise ValueError('database not found')

    log.getLogger('Rest Api')
    log.basicConfig(
        filename='RestApi.log', level=log.DEBUG,
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
        log.debug(request.headers.get('token'))
        log.debug(request.endpoint)

    apis = CreateService()
    cursor, connection = apis.db_connect(host, user_name, password, database)

    create_tables(cursor, connection)
    create_admin_user(cursor, connection)
    create_routes(cursor, connection)

    apis.generate_rest_api(app, cursor, connection)

    echo()


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
