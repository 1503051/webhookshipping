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
    if req.get("result").get("action") != "shippingcost":
        return {}
    result = req.get("result")
    parameters = result.get("parameters")
    zone = parameters.get("shipping-zone")
    cost = {'Europe':'Grace Cheng #725', 'North America':'Dahlong Yang #252', 'South America':'Customer #7585', 'Asia':'400', 'Africa':'500', 'India':'600'}    
    speech = "The cost of shipping to " + zone + " is " + cost[zone]
    #speech = "The cost of shipping to " + zone + " is " + str(cost[zone]) + " euros."
    
    #name=parameters.get("given-name")    
    #contact ={'Grace':'Grace Cheng/1503051 #7585', 'Dahlong':'Dahlong Yang/0203134 #252', 'Customer':'Miss Fu/1403047 #7580'}    
    #speech = "The phone ext for  " + zone + " is " + str(contact[name])

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
