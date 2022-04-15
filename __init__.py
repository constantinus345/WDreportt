#cd "D:\Python_Code\WDreportt" ; Scripts\activate
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
    except:
        print("Some error on reading data")

    try:
        #Person_fname = json_data['message']['from']['first_name']
        Person_lang = json_data['message']['from']['language_code']
        #print(f"{Person_fname} searched {Person_text}, lang= {Person_lang}")
    except:
        Person_lang = "en"
        print("PNAME ERROR")

    try:
        if "text" in json_data['message']:
            user_input = json_data['message']['text']
        elif "photo" in json_data['message']:
            user_input= "photo"
        else:
            user_input = "notvalid"

    except:
        user_input = "notvalid"
        #print("UINPUT")

    try:
        Telegram_ID = json_data['message']['from']['id']
    except:
        print("chat_id")
        Telegram_ID = 1307289323

    bot_output = getResponse(user_input=user_input, Telegram_ID=Telegram_ID, lang_response= Person_lang)
    print(bot_output)
    print(user_input)
    r= requests.post(url=url, params = {'chat_id':Telegram_ID, 'text': bot_output, 'parse_mode': 'HTML'})

    return json_data

if __name__ == '__main__':
    app.run(debug=True,host='127.0.0.1', port=8443)
    #https://fc9bf52ae64d.ngrok.io
    #app.run(debug=True,host='https://fc9bf52ae64d.ngrok.io')