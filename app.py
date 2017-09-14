# !/usr/bin/env python
import json
from flask import Flask, request, make_response, jsonify
from forecast import Forecast, validate_params

APP = Flask(__name__)
LOG = APP.logger


@APP.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    try:
        action = req.get('result').get('action')
    except AttributeError:
        return 'json error'

    if action == 'shippingcost':
        res = weather(req)
    else:
        LOG.error('Unexpected action.')

    print 'Action: ' + action
    print 'Response: ' + res

    return make_response(jsonify({'speech': res, 'displayText': res}))


def weather(req):
    result = req.get("result")
    parameters = result.get("parameters")
    zone = parameters.get("Shipping-zone")

    cost = {'Europe':100, 'North America':200, 'South America':300, 'Asia':400, 'Africa':500, 'India':600}

    speech = "The cost of shipping to " + zone + " is " + str(cost[zone]) + " euros."

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
    APP.run(debug=True, host='0.0.0.0')
