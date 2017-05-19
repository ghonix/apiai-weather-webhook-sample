#!/usr/bin/env python

from __future__ import print_function
from future.standard_library import install_aliases
install_aliases()

from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

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

    res = processRequest(req)

    res = json.dumps(res, indent=4)
    # print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def processRequest(req):
    parameters = req.get("result").get("parameters")

    # baseurl = "https://query.yahooapis.com/v1/public/yql?"
    # yql_query = makeYqlQuery(req)
    # if yql_query is None:
    #     return {}
    # yql_url = baseurl + urlencode({'q': yql_query}) + "&format=json"
    # result = urlopen(yql_url).read()
    # data = json.loads(result)
    res = makeWebhookResult("I think you should try the %s %s %s that I found on example.com" \
        % (','.join((parameters.get("protein"))),
        ', '.join(parameters.get("vegetable")),
        parameters.get("dish-type")))
    return res

def makeWebhookResult(data):
    # print(json.dumps(item, indent=4))

    speech = data
    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        # "data": data,
        # "contextOut": [],
        "source": "apiai-weather-webhook-sample"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=True, port=port, host='0.0.0.0')
