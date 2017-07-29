# Flask-RestApi
RestApi module is used to create rest apis dynamically

## Getting Started

import RestApi

### Prerequisites
Flask, MySQL

Example

- Create rest api table
    - Name:  py_restapi 
    - Fields: id, method, query and url
    
- Create table po with fields poid and potext.
- For POST create entry in rest api table and call rest api as follows

| rest_id  | method | query  | url |
| ------------- | ------------- | ------------- | ------------- |
| 1  | POST  | po  | postPo  |

Url:/postPo

Method:POST

Content-Type:application/json

Body:{"poid":1, "potext":"po text"}


- For GET create entry in rest api table and call rest api as follows

| rest_id  | method | query  | url |
| ------------- | ------------- | ------------- | ------------- |
| 1  | GET  | select * from po where id=:id	  | getPo  |


Url:/getPo?id=1

Method:GET

Body:{"poid":1, "potext":"po text"}

 
```
from flask import Flask
import RestApi

app = Flask(__name__)

RestApi.createApi(app, host='localhost', userName='username', 
                  password='password', database='databasename')

if __name__ == "__main__":
    app.run()
```
