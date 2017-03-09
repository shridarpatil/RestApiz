#!/usr/bin/python
import json
from flask import jsonify, request, g
import pymysql.cursors
import sys, time
from werkzeug.serving import BaseRequestHandler
import logging
from flask import render_template

class createService():
	def __init__(self, app, host, user, password, db):
		self.app = app
		self.host = host
		self.user = user
		self.password = password
		self.db = db

		self.connection()		
		pass
	
	def connection(self):
		
		host = self.host
		user = self.user
		password = self.password
		db = self.db
		
		try:		
			conn = pymysql.connect(host=host,
	                          user = user,
	                          password = password,
				                    db = db,
				                    charset='utf8mb4',
		                        cursorclass=pymysql.cursors.DictCursor)
			c = conn.cursor()
		except Exception, e:
			raise ValueError(e)
		self.c = c
		self.conn = conn
		self.generateRestApi()

	def generateRestApi(self):
		query = "select * from py_restapi"
		c =  self.c
		c.execute(query)
		data = c.fetchall()

		for row in data:

			if row['method'].lower() == 'get':
				self.createGet(row['url'], row['method'], row['query'])
			elif row['method'].lower() == 'post':
				self.createPost(row['url'], row['method'], row['query'])
			elif row['method'].lower() == 'put':
				self.createPut(row['url'], row['method'], row['query'])

	

	def createGet(self, url, method, query):

		app = self.app
		def get():
			logging.debug('Running /' + url)
			queryParams = request.args
			generatedQuery = self.generateQuery(queryParams, query, ':')

			c = self.c
			try:
				c.execute(generatedQuery)
				data = c.fetchall()
			except Exception, e:
				logging.error(e)
				raise InvalidUsage(str(e), status_code=400)
			
			if not data:
				type = 'Warning'
			else:
				type = 'Info'
			logging.debug('Completed /' + url)
			return json.dumps({"success":True, "type":type, "data" : data})
		
		get.methods = [method]
		app.add_url_rule('/' + url, url, get)
		pass

	def createPost(self, url, method, query):
		app = self.app

		def post():
			logging.debug('Running /' + url)
			json = request.get_json(force=True)
			values = self.generatePostQuery(json, query)
			c = self.c
			conn = self.conn
			try:
				c.execute(query, values)
				id = conn.insert_id()
				conn.commit()
				logging.debug('Completed /' + url)
				return jsonify({"success":True, "type":"Info", "data" : id})
			except Exception, e:
				logging.error(e)
				raise InvalidUsage(str(e), status_code=400)
			
			
		post.methods = [method]
		self.app.add_url_rule('/' + url, url, 
                      post)
		pass

	def createPut(self, url, method, query):
		app = self.app
		
		# pathBeforeReq = './hello'
		# funcNameBeforeReq = 'hell'

		# pathAfterReq = './hello'
		# funcNameAfterReq = 'hell'
		
		def put():
			logging.debug('Running /' + url)
			
			data = request.get_json(force=True)
			queryParams = request.args


			# try:

			# 	funcBeforeReq = self.generateFunc(pathBeforeReq, funcNameBeforeReq)

			# except TypeError, e:
			# 	raise InvalidUsage(funcName + ' must return queryParams, data', status_code=404)
			
			# except Exception, e:
			# 	raise InvalidUsage(str(e), status_code=404)

			# try:
			# 	queryParams, data = funcBeforeReq(InvalidUsage, queryParams, data)

			# except Exception, e:
			# 	raise InvalidUsage('Error in function '+ funcNameBeforeReq, status_code=404, payload={'Error':str(e)})

			 
			

			try:
				generatedQuery = self.generateQuery(queryParams, query, ':')
				generatedQuery = self.generateQuery(data, generatedQuery, ';')
				logging.debug('Query : ' + generatedQuery)
			except Exception, e:
				logging.error(e)
				raise InvalidUsage(str(e), status_code=404)
			
			# values = self.generatePostQuery(json, query)

			c = self.c
			conn = self.conn
			try:
				c.execute(generatedQuery)
				conn.commit()
			except Exception, e:
				logging.error(e)
				raise InvalidUsage(str(e), status_code=400)

			# try:

			# 	funcAfterReq = self.generateFunc(pathAfterReq, funcNameAfterReq)

			# except TypeError, e:
			# 	raise InvalidUsage(funcName + ' must return queryParams, data', status_code=404)
			
			# except Exception, e:
			# 	raise InvalidUsage(str(e), status_code=404)

			# try:
			# 	queryParams = funcAfterReq(InvalidUsage, queryParams, data)

			# except Exception, e:
			# 	raise InvalidUsage('Error in function '+ funcNameBeforeReq, status_code=404, payload={'Error':str(e)})

			
			
			logging.debug('Completed /' + url)
			return jsonify({"success":True, "type":"Info", "data" : []})


		put.methods = [method]
		self.app.add_url_rule('/' + url, url, 
                      put)
		pass


	def generatePostQuery(self, data, query):
		startPt = query.find('(') + 1
		endPt = query.find(')')
		params = query[startPt:endPt].split(',')
		values = []
		try:
			for param in params:
				values.append(data[param.replace(' ', '')])
		except Exception, e:
			logging.error(e)
			raise InvalidUsage(str(e), status_code=400)

		
		return values


	def generateQuery(self, params, query, symbol):
			
		qSymbol = symbol
		qColon = query.find(qSymbol)
		if qColon!=-1:
			qSpace = query.find(" ",qColon)
			if qSpace==-1:
				qSpace = len(query)

			qColon += 1

			param = query[qColon:qSpace]
			paramsReplaceText = ""
			if symbol==";":
				#if type(params[param]) == "string":
				paramsReplaceText = "'"+str(params[param])+"'"
				#else:
				#	paramsReplaceText = params[param]				
			else:
				
				paramsReplaceText = params[param]
			query = query.replace(qSymbol+param, paramsReplaceText)
			query = self.generateQuery(params, query, qSymbol)
		return query

	def generateFunc(self, path, funcName):

			sys.path.insert(0, path)
			moduleBeforeReq = __import__(funcName)

			return getattr(moduleBeforeReq, funcName)


class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        rv['success'] = 'False'
        rv['type'] = 'Error'
        return rv


def createApi(app, host=None, userName=None, password=None, database=None):

	if host==None:
		logging.error('host not found')
		raise ValueError('host not found')

	if userName==None:
		logging.error('userName not found')
		raise ValueError('userName not found')

	if password==None:
		logging.error('password not found')
		raise ValueError('password not found')

	if database==None:
		logging.error('database not found')
		raise ValueError('database not found')

	logging.getLogger('Rest Api')
	logging.basicConfig(filename='RestApi.log',level=logging.DEBUG, format='Rest-Api %(asctime)s [%(levelname)-5.5s] %(message)s')

	@app.errorhandler(InvalidUsage)
	def handle_invalid_usage(error):
	    response = jsonify(error.to_dict())
	    response.status_code = error.status_code
	    return response
	@app.before_request
	def before_request():
		
		logClient(request)
		
	createServices = createService(app, host, userName, password, database)
	print """
			______          _      ___        _ 
			| ___ \        | |    / _ \      (_)
			| |_/ /___  ___| |_  / /_\ \_ __  _ 
			|    // _ \/ __| __| |  _  | '_ \| |
			| |\ \  __/\__ \ |_  | | | | |_) | |
			\_| \_\___||___/\__| \_| |_/ .__/|_|
			                           | |      
			                           |_|       

"""
	return True

class logClient(object):
	"""docstring for logClient"""
	def __init__(self, arg):
		super(logClient, self).__init__()
		self.arg = arg
		self.logClient()

	def logClient(self):
		logging.info('Client-IP: ' + self.arg.remote_addr)
		logging.info('User-Agent: ' + self.arg.headers.get('User-Agent'))
		pass
		
class RequestHandler(BaseRequestHandler):
    """Extend werkzeug request handler to suit our needs."""
    def handle(self):
        self.fancyStarted = time.time()
        rv = super(RequestHandler, self).handle()
        return rv

    def send_response(self, *args, **kw):
        self.fancyProcessed = time.time()
        super(RequestHandler, self).send_response(*args, **kw)

    def log_request(self, code='-', size='-'):
        duration = int((self.fancyProcessed - self.fancyStarted) * 1000)
        self.log('info', '"{0}" {1} {2} [{3}ms]'.format(self.requestline, code, size, duration))


version = '0.0.3'
