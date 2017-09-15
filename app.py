#!/usr/bin/env python

import urllib
import json
import os

from flask import Flask
from flask import request
from flask import make_response
from pymongo import MongoClient

# Flask app should start in global layout
app = Flask(__name__)


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
    
    
    client = MongoClient()
    #client = MongoClient("localhost", 27017)
    client = MongoClient("mongodb://140.110.143.203:27017/")
    db = client.hrvisual
    collection = db.ORG_DEPT_EMP_2017
    result=collection.find({"emp_number":"1503051"})[0]
    for obj in result:
        speech=obj['emp_name']
    
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
