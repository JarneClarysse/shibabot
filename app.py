# -*- coding: utf-8 -*-
import os
import sys
import json
import random
from processing import procesText
from datetime import datetime

import requests
from flask import Flask, request

app = Flask(__name__)
answerList = ["whaf?","Whaf was that?","Given command does not exist.","For a list of commands type help"]

@app.route('/', methods=['GET'])
def verify():
    log("starting up")

    # when the endpoint is registered as a webhook, it must echo back
    # the 'hub.challenge' value it receives in the query arguments
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == os.environ["VERIFY_TOKEN"]:
            return "Verification token mismatch", 403
            return request.args["hub.challenge"], 200

            return "Hello world", 200


@app.route('/', methods=['POST'])
def webhook():
    print("webhook entered")
    # endpoint for processing incoming messaging events
    data = request.get_json()
    log(data)  # you may not want to log every incoming message in production, but it's good for testing
    
    if data["object"] == "page":

        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:

                if messaging_event.get("message"):  # someone sent us a message
                    answer = answerList[random.randint(0,len(answerList)-1)]

                    sender_id = messaging_event["sender"]["id"]        # the facebook ID of the person sending you the message
                    
                    recipient_id = messaging_event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID
                    
                    if 'text' in messaging_event["message"]:
                        message_text = messaging_event["message"]["text"]  # the message's text
                        message_text= commandCheck(message_text.lower())
                        if (isinstance(message_text,list)):
                            answer = procesText(answer, message_text[0], message_text[1])

                        else:
                            answer = procesText(answer, message_text, None)

                        if (isinstance(answer,list)):

                            if (answer[0]==True ):
                                send_picture(sender_id, answer[1])

                            elif(answer[0]==False):

                                send_sound(sender_id, answer[1])
                            else:    
                                for reply in answer:
                                    send_message(sender_id, reply)

                        else:
                            send_message(sender_id, answer)

                if messaging_event.get("delivery"):  # delivery confirmation
                    pass

                if messaging_event.get("optin"):  # optin confirmation
                    pass

                if messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message
                    pass

                return "ok", 200
        else:
            return "OK"

def send_message(recipient_id, message_text):

   # log("sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_text))

    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
        }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message_text
            }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        #log(r.text)

def send_picture(recipient_id, image_url):

    log("sending message to {recipient}: {text}".format(recipient=recipient_id, text=image_url))

    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {"id": recipient_id},
        "message": {
            "attachment": {
                "type": "image",
                "payload": {
                    "url": image_url
                }
            }}
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
       
def send_sound(recipient_id, sound_url):

    log("sending message to {recipient}: {text}".format(recipient=recipient_id, text=sound_url))

    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {"id": recipient_id},
        "message": {
            "attachment": {
                "type": "audio",
                "payload": {
                    "url": sound_url
                }
            }}
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)

def log(msg, *args, **kwargs):  # simple wrapper for logging to stdout on heroku
    try:
        if type(msg) is dict:
            msg = json.dumps(msg)
        else:
            print(msg)
            msg = unicode(msg).format(*args, **kwargs)
            print u"{}: {}".format(datetime.now(), msg)
    except UnicodeEncodeError:
        pass  # squash logging errors in case of non-ascii text
        sys.stdout.flush()


        if __name__ == '__main__':
            app.run(debug=True)

def commandCheck(message):
    messages = message.split(' ')
    if (len(messages)==2):
        if(messages[0]=="weather"):
            return messages
        
        return message
    else: 
        return message



