"""
The JSON requests to the BIM server API

Created: 2018-01-01
"""

def getLoginRequest(username, password):

	loginRequest = {
	  "request": {
	    "interface": "AuthInterface", 
	    "method": "login", 
	    "parameters": {
	      "username": username,
	      "password": password
	    }
	  }
	}

	return loginRequest;