import os
import traceback
import json
import requests

from flask import Flask, request

from messages import get_message, search_keyword

token = os.environ.get('ACCESS_TOKEN')

app = Flask(__name__)



def send_attachment(sender, type, payload):
    return {
        "recipient": {
            "id": sender
        },
        "message": {
            "attachment": {
                "type": type,
                "payload": payload,
            }
        }
    }


def send_text(sender, text):
    return {
        "recipient": {
            "id": sender
        },
        "message": {
            "text": text
        }
    }


def send_message(payload):
    requests.post('https://graph.facebook.com/v2.6/me/messages/?access_token=' + token, json=payload)


def send_hr_info(sender, **kwargs):

    r = requests.get(hr_text)
    response = r.json()

    print(response)

    if 'cod' in response:
        if response['cod'] != 200:
            return 'error'

                        

    payload = send_attachment(sender,
                              'template',
                              {
                                  "template_type": "list",
                                  "top_element_style": "large",
                                  "elements": elements,
                                  "buttons": [
                                      {
                                          "title": "Weather",
                                          "type": "postback",
                                          "payload": "do_it_again"
                                      }

                                  ]
                              })

    payload1 = send_attachment(sender,
                              'template',
                              {
                                 "template_type":"button",
                                 "text":"What do you want to do next?",
                                 "buttons":[
                                    {
                                        "type":"web_url",
                                        "url":"https://www.tesco.com",
                                        "title":"Show Website"
                                    },
                                    {
                                        "type":"postback",
                                        "title":"weather",
                                        "payload":"do_it_again"
                                    }
                                    ]
                                   })



    send_message(payload)
    return None


@app.route('/', methods=['GET', 'POST'])
def webhook():
    if request.method == 'POST':
        try:
            data = json.loads(request.data.decode())
            sender = data['entry'][0]['messaging'][0]['sender']['id']

            print(data)

            if 'message' in data['entry'][0]['messaging'][0]:
                message = data['entry'][0]['messaging'][0]['message']
                text = message['text']
                query = 'q={}'.format(text)
                
                url = 'http://ec2-54-229-26-32.eu-west-1.compute.amazonaws.com:5000/parse?'\
                '{}'.format(query)
	                                                  
                chat_message = search_keyword(text)

                if chat_message:
                    
                    
                    
                    
                    
                    
                    # if found keyword, reply with chat stuff
                    message = send_text(sender, chat_message)
                    send_message(message)
                else:
                    message = send_text(sender, get_message('i_do_not_know'))
                    send_message(message)

        except Exception as e:
            print(traceback.format_exc())
    elif request.method == 'GET':
        if request.args.get('hub.verify_token') == os.environ.get('VERIFY_TOKEN'):
            return request.args.get('hub.challenge')
        return "Wrong Verify Token"
    return "Nothing"

if __name__ == '__main__':
    app.run(debug=True)
