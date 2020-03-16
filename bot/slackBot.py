from urllib import request, parse
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from io import BytesIO
import sys
sys.path.append('../')
from framework.model.extractmodel import ExtractionModel

from pprint import pprint

'''
{
    "channel": "C1H9RESGL",
    "text": "Text here for notifications",
	"blocks": [
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "This is a mrkdwn section block :ghost: *this is bold*, and ~this is crossed out~, and <https://google.com|this is a link>"
			}
		}
	]
}
'''
def createBlockMessage(str):
    subDict = {}
    subDict["type"] = "mrkdwn"
    subDict["text"] = str

    dict = {}
    dict["type"] = "section"
    dict["text"] = subDict

    response = {}
    arr = []
    arr.append(dict)
    response["channel"] = "#random"
    response["text"] = "ACK"
    response["blocks"] = arr

    return response


def sendMessage(msg):
    url = "https://hooks.slack.com/services/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"
    # post = { "text": "{0}".format(msg) }
    post = msg
    jsoned = json.dumps(post)
    encoded_data = jsoned.encode('ascii')
    headers = { 'Content-Type': 'application/json' }

    try:
        req = request.Request(url, data=encoded_data, headers=headers)
        resp = request.urlopen(req)
    except Exception as em:
        print("EXCEPTION: " + str(em))

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Hello, world!')

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        json_data = json.loads(body.decode('utf-8'))
        self.send_response(200)
        self.end_headers()

        if json_data["type"] == "url_verification":
            response = BytesIO()
            response.write(b'This is POST request. ')
            response.write(b'Received: ')
            response.write(body)
            self.wfile.write(response.getvalue())

        if json_data["event"]["type"] == "message":
            if json_data["event"]["text"] != "ACK":
                movie_model = ExtractionModel("movie", "movie3")
                extraction = movie_model.extract(json_data["event"]["text"])
                print()
                print("---MODEL OUTPUT---")
                print(extraction)
                str = ""
                keys = []
                for k in extraction:
                    keys.append(k)
                print("\n---KEYS---")
                print(keys)
                print("\n\n")
                for i in range(len(keys)-1):
                    if extraction[keys[i]] != 'O':
                        entity = extraction[keys[i]].split('-')[1]
                        if (i < len(keys) - 2) and (extraction[keys[i+1]] != 'O'):
                            next_entity = extraction[keys[i+1]].split('-')[1]
                        else:
                            str += ('*'+keys[i]+'* '+'`'+entity+'` ')
                            continue
                        if entity == next_entity:
                            str += ('*'+keys[i]+'* ')
                        else:
                            str += ('*'+keys[i]+'* '+'`'+entity+'` ')
                    else:
                        str += (keys[i] + ' ')
                response = createBlockMessage(str)
                pprint(response)
                sendMessage(response)

        # print(body)


httpd = HTTPServer(('localhost', 8000), SimpleHTTPRequestHandler)
httpd.serve_forever()
