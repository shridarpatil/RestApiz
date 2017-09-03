==========================
Flask-AutoGenerate-RestApi
==========================


.. image:: https://img.shields.io/pypi/v/RestApiz.svg
        :target: https://pypi.python.org/pypi/RestApiz

.. image:: https://img.shields.io/travis/shridarpatil/RestApiz.svg
        :target: https://travis-ci.org/shridarpatil/RestApiz

.. image:: https://readthedocs.org/projects/RestApiz/badge/?version=latest
        :target: https://RestApiz.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://pyup.io/repos/github/shridarpatil/RestApiz/shield.svg
     :target: https://pyup.io/repos/github/shridarpatil/RestApiz/
     :alt: Updates


Create rest api's dynamically within no time.


* Free software: MIT license
* Documentation: https://RestApiz.readthedocs.io.


Features
--------

* Create Rest like apis without writing tons of lines of code.

# Flask-RestApi
RestApi module is used to create rest apis dynamically

## Installation
```pip install RestApiz```

### Prerequisites
Flask, MySQL

## Getting Started

import RestApi

##Example

- Create rest api table
    - Name:  py_restapi 
    - Fields: id, method, query, url, before_query and after_query
    
- Create table po with fields poid and potext.

POST:
--------
- For POST create entry in rest api table and call rest api as follows

| rest_id  | method | query  | url | before_query | after_query |
| -------- | ------ | ------ | --- | ------------ | ----------- |
| 1  | POST  | po  | insert into po(poid, potext) values(%s, %s)  | validatepost.validate_before:validation | validatepost.validate_after:validation

Url:/postPo

Method:POST

Content-Type:application/json

Body:{"poid":1, "potext":"po text"}
### Note:
```Inserts data into table 'po' ```

GET:
---
- For GET create entry in rest api table and call rest api as follows

| rest_id  | method | query  | url | before_query | after_query |
| -------- | ------ | ------ | --- | ------------ | ----------- |
| 1  | GET  | select * from po where id=:id	  | getPo  | |  |


Url:/getPo?id=1

Method:GET

Body:{"poid":1, "potext":"po text"}

PUT:
----
- For PUT create entry in rest api table and call rest api as follows

| rest_id  | method | query  | url | before_query | after_query |
| -------- | ------ | ------ | --- | ------------ | ----------- |
| 1  | PUT  | update po set potext=:potext where poid=;poid	  | putPo  | |  |

 Url: putPo?poid=1
 
 Method:PUT
 
 Body:{"poid":"Updated using RestApiz"}
 
 DELETE:
----
- For DELETE create entry in rest api table and call rest api as follows

| rest_id  | method | query  | url | before_query | after_query |
| -------- | ------ | ------ | --- | ------------ | ----------- |
| 1  | DELETE  | delete from po where poid=;poid | deletePo  | |  |

 Url: deletePo?poid=1
 
 Method:delete
 
 
```
from flask import Flask
import RestApi

app = Flask(__name__)

RestApi.createApi(app, host='localhost', userName='username', 
                  password='password', database='databasename')

if __name__ == "__main__":
    app.run()
```


Credits
---------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage

