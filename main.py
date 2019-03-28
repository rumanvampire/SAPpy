import webapp2

import json

from google.appengine.api import urlfetch

class SlackDemo(webapp2.RequestHandler):

    def post(self):

        sap_url = ‘<your-sap-gateway>/ZSLACK_DEMO_SRV/RfcDestinationSet‘

        json_suffix = ‘?$format=json’

        authorization = ‘Basic <your-basic-credentials>’

        slack_token = ‘<your-slack-token>’

        request_token = self.request.get(‘token’)

        if slack_token != request_token:

            self.response.headers[‘Content-Type’] = ‘text/plain’

            self.response.write(‘Invalid token.’)

            return

        text = self.request.get(‘text’)

        details = {}

        if text.find(‘shout’) > -1:

            details[‘response_type’] = ‘in_channel’

            response_text = ”

        if text.find(‘test’) > -1:

            rfc_destination = text.split()[-1]

            request_url = sap_url + “(‘” + rfc_destination + “‘)” + json_suffix

            headers = {}

            headers[‘Authorization’] = authorization

            response_tmp = urlfetch.fetch(url=request_url,

                              headers=headers,

                              method=urlfetch.GET)

            response_info = json.loads(response_tmp.content)

            response_text += ‘Sensor sweep indicates the following:\n’

            response_text += response_info[‘d’][‘Destination’] + ‘ – ‘

            response_text += response_info[‘d’][‘ConnectionStatus’] + ‘ – ‘

            response_text += str(response_info[‘d’][‘ConnectionTime’]) + ‘ ms response’

        else:

            response_text += “I’m sorry, Captain, but my neural nets can’t process your command.”

        details[‘text’] = response_text

        json_response = json.dumps(details)

        self.response.headers[‘Content-Type’] = ‘application/json’

        self.response.write(json_response)

app = webapp2.WSGIApplication([

    (‘/slackdemo’, SlackDemo),

], debug=True)

