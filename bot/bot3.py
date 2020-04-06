import json
import urllib
from http.server import HTTPServer, BaseHTTPRequestHandler
from io import BytesIO
import os
import sys
from urllib.parse import *
sys.path.append('../')
from framework.model.extractmodel import ExtractionModel
from pprint import pprint
from flask import Flask, request, Response

app = Flask(__name__)

def switch_model(model_str):
    modelgrp = model_str.split("|")
    model_group = modelgrp[0]
    model_name = modelgrp[1]


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


def createModelList(models):
    outer = {}
    inner_blocks = []

    sendMessage(createBlockMessage("*Generating list of of models...*"))

    for model in models:
        trained_models = os.listdir("../framework/model/models/" + model)
        inner_dict = {}
        inner_dict["type"] = "section"

        text_dict = {}
        inner_text_dict = {}
        inner_text_dict["type"] = "mrkdwn"
        inner_text_dict["text"] = "\t*" + model + "*\n _Dataset description_ \n Trained models: \n"

        for trained_model in trained_models:
            inner_text_dict["text"] += "\t{}\n".format(trained_model)

        inner_dict["text"] = inner_text_dict
        inner_blocks.append(inner_dict)
        inner_blocks.append({"type": "divider"})

    select_block = {}
    select_block["type"] = "section"
    select_block["text"] = {
        "text": "Select a model",
        "type": "mrkdwn"
    }
    inner_select = {}
    inner_select["action_id"] = "select_model"
    inner_select["type"] = "static_select"
    inner_select["placeholder"] = {
        "type": "plain_text",
        "text": "Select"
    }

    options_dicts = []
    for model in models:
        trained_models = os.listdir("../framework/model/models/" + model)
        options_dicts.append({
            "text": {
                "type": "plain_text",
                "text": "----- {} -----".format(model)
            },
            "value": "none"
        })
        for trained_model in trained_models:
            options_dicts.append({
                "text": {
                    "type": "plain_text",
                    "text": trained_model
                },
                "value": model + "|" +trained_model
            })

    inner_select["options"] = options_dicts
    select_block["accessory"] = inner_select
    inner_blocks.append(select_block)
            
    outer["blocks"] = inner_blocks
    #outer["channel"] = "#random"
    return outer
        


def sendMessage(msg):
    #url = "https://hooks.slack.com/services/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"
    #url = "https://hooks.slack.com/services/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"
    url = "https://hooks.slack.com/services/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"
    # post = { "text": "{0}".format(msg) }
    post = msg
    jsoned = json.dumps(post)
    encoded_data = jsoned.encode('ascii')
    headers = { 'Content-Type': 'application/json' }

    try:
        req = urllib.request.Request(url, data=encoded_data, headers=headers)
        resp = urllib.request.urlopen(req)
    except Exception as em:
        print("EXCEPTION: " + str(em))

def do_bot_command(text):
    if "!load" in text:
        pass
    elif "!list" in text or "!models" in text:
        model_list = os.listdir("../framework/model/models")
        msg = createModelList(model_list)
        print(msg)
        sendMessage(msg)
    elif "!help" in text:
        pass

@app.route("/", methods=['POST', 'GET'])
def handler():
    if request.method == 'GET':
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Hello, world!')
    elif request.method == 'POST':
        content_length = int(request.headers.get('Content-Length'))
        #print(content_length)
        sendMessage(createBlockMessage("crazy how broken this is3"))
        #body = self.rfile.read(content_length)
        # print(request)
        return "" 
        if b'payload' in body:
            body = unquote(str(body),encoding='utf-8')
            body= body.replace("payload=", "")
            body = body.replace("b'", "")
            body = body[:-1]
            json_data = json.loads(body)
            selected_model = json_data["actions"][0]["selected_option"]["value"]
            switch_model(selected_model.split("|"))
        else:
            #print(body)
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
                #print("---- Test -----")
                #print(json_data["event"]["text"][0])
                if json_data["event"]["text"][0] != "!":
                    model = ExtractionModel(model_group, model_name)
                    extraction =model.extract(json_data["event"]["text"])
                    print()
                    print("---MODEL OUTPUT---")
                    print(extraction)
                    str_k = ""
                    keys = []
                    for k in extraction:
                        keys.append(k)
                    print("\n---KEYS---")
                    print(keys)
                    print("\n\n")
                    for i in range(len(keys)-1):
                        print(i)
                        if extraction[keys[i]][0] != 'O':
                            entity = extraction[keys[i]][0].split('-')[1]
                            if (i < len(keys) - 2) and (extraction[keys[i+1]][0] != 'O'):
                                next_entity = extraction[keys[i+1]][0].split('-')[1]
                            else:
                                str_k += ('*'+keys[i]+'* '+'`'+entity+'` ')
                                continue
                            if entity == next_entity:
                                str_k += ('*'+keys[i]+'* ')
                            else:
                                str_k += ('*'+keys[i]+'* '+'`'+entity+'` ')
                        else:
                            str_k += (keys[i] + ' ')
                    response = createBlockMessage(str_k)
                    pprint(response)
                    sendMessage(response)
                else:
                    do_bot_command(json_data["event"]["text"])


app.run(debug=True, host='localhost', port=8001)
