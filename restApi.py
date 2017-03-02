#!/usr/bin/python
import json
from flask import jsonify, request
import pymysql.cursors
import sys

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

			queryParams = request.args
			generatedQuery = self.generateQuery(queryParams, query, ':')

			c = self.c
			try:
				c.execute(generatedQuery)
				data = c.fetchall()
			except Exception, e:
				raise InvalidUsage(str(e), status_code=400)
			
			if not data:
				type = 'Warning'
			else:
				type = 'Info'

			return json.dumps({"success":True, "type":type, "data" : data})
		
		get.methods = [method]
		app.add_url_rule('/' + url, url, get)
		pass

	def createPost(self, url, method, query):
		app = self.app

		def post():
			json = request.get_json(force=True)
			values = self.generatePostQuery(json, query)
			c = self.c
			conn = self.conn
			try:
				c.execute(query, values)
				id = conn.insert_id()
				conn.commit()
				return jsonify({"success":True, "type":"Info", "data" : id})
			except Exception, e:
				raise InvalidUsage(str(e), status_code=400)
			
			
		post.methods = [method]
		self.app.add_url_rule('/' + url, url, 
                      post)
		pass

	def createPut(self, url, method, query):
		app = self.app
		
		def put():
			
			json = request.get_json(force=True)
			queryParams = request.args

			try:
				generatedQuery = self.generateQuery(queryParams, query, ':')
				generatedQuery = self.generateQuery(json, generatedQuery, ';')
			
			except Exception, e:
				raise InvalidUsage(str(e), status_code=404)
			
			# values = self.generatePostQuery(json, query)

			c = self.c
			conn = self.conn
			try:
				c.execute(generatedQuery)
				id = conn.insert_id()
				conn.commit()
				return jsonify({"success":True, "type":"Info", "data" : []})
			except Exception, e:
				raise InvalidUsage(str(e), status_code=400)
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
		raise ValueError('host not found')

	if userName==None:
		raise ValueError('userName not found')

	if password==None:
		raise ValueError('password not found')

	if database==None:
		raise ValueError('database not found')

	@app.errorhandler(InvalidUsage)
	def handle_invalid_usage(error):
	    response = jsonify(error.to_dict())
	    response.status_code = error.status_code
	    return response
	
	createServices = createService(app, host, userName, password, database)
	print """
//////////  //////////  ///////////   ///////////////
//      //  //          //                  ||
//      //  //          //                  ||
//     //   //          //                  ||
////////    //////////  ///////////         ||
///         //                   //         ||
// //       //                   //         ||
//   //     //                   //         ||
//    //    //////////  //////////          ||		
	"""
	return True

version = '0.0.1'