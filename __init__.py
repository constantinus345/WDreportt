#d:/Python_Code/WDreportt/Scripts/python.exe d:/Python_Code/WDreportt/__init__.py

from flask import Flask,request,json
import configs
import requests
from getResponse import getResponse
from mongo_log_conversations import Insert_Telegram_Interaction as insert_mongo
import sys
from mongoerror import json_processing


app = Flask(__name__)

@app.route('/')
def hello():
    return 'Webhooks with Python- Report MD.'



bot_link= f"https://api.telegram.org/bot{configs.Telegram_Key}/"
url= f"{bot_link}sendMessage"




@app.route('/',methods=['POST', 'GET'])
def githubIssue():
    try:
        json_data = request.json
        print(type(json_data))
        print(json_data)


        json_processing((json_data))

        #insert_mongo(json_data)
        #print(json_data)
    except:
        print("Some error on reading data")

    try:
        Person_fname = json_data['message']['from']['first_name']
        Person_text = json_data['message']['text']
        print(f"{Person_fname} searched {Person_text}")
    except:
        print("PNAME")
        pass

    try:
        user_input = json_data['message']['text']
        
    except:
        print("UINPUT")
        user_input = "notvalid"

    try:
        chat_id = json_data['message']['from']['id']
    except:
        chat_id = 1307289323

    bot_output = getResponse(user_input)

    r= requests.post(url=url, params = {'chat_id':chat_id, 'text': bot_output, 'parse_mode': 'HTML'})

    return json_data

if __name__ == '__main__':
    app.run(debug=True,host='127.0.0.1', port=8443)
    #https://fc9bf52ae64d.ngrok.io
    #app.run(debug=True,host='https://fc9bf52ae64d.ngrok.io')