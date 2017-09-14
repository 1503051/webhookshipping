#!/usr/bin/env python

import urllib
import json
import os

from flask import Flask
from flask import request
from flask import make_response

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
    if req.get("result").get("action") != "branchcost":
        return {}
    result = req.get("result")
    parameters = result.get("parameters")
    branch = parameters.get("branch")
    contact = {'Europe':'Grace Cheng #725', 'North America':'Dahlong Yang #252', 'South America':'Customer #7585', 'Asia':'400', 'Africa':'500', 'India':'600'}    
    speech = "The cost of shipping to " + branch + " is " + contact[branch]
    
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
