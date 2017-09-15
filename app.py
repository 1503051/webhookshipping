#!/usr/bin/env python

import urllib
import json
import os

from flask import Flask
from flask import request
from flask import make_response
from flask_pymongo import PyMongo

# Flask app should start in global layout
app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'hrvisual'
app.config['MONGO_URI'] = 'mongodb://140.110.143.203:27017/hrvisual'

mongo = PyMongo(app)

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = makeWebhookResult(req)
    
    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def makeWebhookResult(req):
    if req.get("result").get("action") != "branchcontact":
        return {}
    result = req.get("result")
    parameters = result.get("parameters")
    
    contact = {'Narl':'02-6630-0151', 'Ndl':'03-5726100', 'Nchc':'03-5776085', 'Cic':'03-7777777', '1503051':'0911111111'}    
    speech ="unknow"
    
    branch = parameters.get("branch")
    if branch is not None:        
        speech = "The contact information for " + branch + " is " + contact[branch]
   
    anytxt = parameters.get("any")
    if anytxt is not None:
        speech = "The contact information for " + anytxt + " is " + contact[anytxt]
    
    
    star = mongo.db.stars
    s = star.find_one({'emp_number' : '1503051'})
    if s:
        speech = {'emp_number' : s['emp_number'], 'distance' : s['distance']}
    else:
        speech = "No such emp_number"
    
    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        # "data": data,
        # "contextOut": [],
        "source": "apiai-onlinestore-shipping"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(debug=True, port=port, host='0.0.0.0')
