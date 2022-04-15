import telegram
import requests
import configs
import json
import pymongo
import sys
from time import sleep, time
from bson.json_util import dumps
import pandas as pd
from random import uniform as rdmf
import re
from datetime import datetime
import pandas as pd
import other_func
import os

engine= configs.engine

def days_since_timestamp(TS): 

    TS= 1649058329
    Day_sec= 24*60*60
    Days_since_unixts = round((time() - TS)/Day_sec,2)
    return Days_since_unixts



"""def Limit_ok (Telegram_Id, Days, Limit):


    Mongo_client = pymongo.MongoClient(configs.MongoT_Client)
    Mongo_mydb = Mongo_client[configs.MongoT_Database]
    #Important: In MongoDB, a database is not created until it gets content!
    Mongo_mycol = Mongo_mydb[configs.MongoT_Collection]
    after_unix_date= int(time() - 24*3600*Days)
    myquery_lat = {"$and": [{"message.date" : {"$gt": after_unix_date}},
                    {"message.text" : {'$regex' : '^ok$', '$options' : 'i'}},{'message.from.id': {'$in': [ Telegram_Id]}} ]}

    myquery_rus = {"$and": [{"message.date" : {"$gt": after_unix_date}}, 
                    {"message.text" : {'$regex' : '^Ок$', '$options' : 'i'}},{'message.from.id': {'$in': [ Telegram_Id]}}]}


    mydoc = Mongo_mycol.count_documents(myquery_lat) + Mongo_mycol.count_documents(myquery_rus)
    over_limit = True if mydoc > Limit else False
    return over_limit
"""
def  Limit_ok(Telegram_Id, Days, Limit):
    """
    Limits how many oks an user can get. A hyper-active user may be a malicious one, 
    Seeking to extract the database
    """
    SQLq= f"""SELECT *
            FROM worktracker
            WHERE tstamp > (CURRENT_DATE - INTERVAL '{Days} days')
            AND telegramid = '{Telegram_Id}'"""
    with engine.connect() as conn:
        dfx = pd.read_sql(SQLq, con=conn)
    
    over_limit = True if len(dfx) > Limit else False
    
    return over_limit

#print(True and False)
#print(Limit_ok(1307289323, 30, 10000))

def exists(obj, chain):
    _key = chain.pop(0)
    if _key in obj:
        return exists(obj[_key], chain) if chain else obj[_key]


#Not finished
def T_Mongo_Picture_Log(doc):
    Folder= configs.Folder_temp_images
    """
    
    """
    Mongo_client = pymongo.MongoClient(configs.MongoT_Client)
    Mongo_mydb = Mongo_client[configs.MongoT_Database]
    #Important: In MongoDB, a database is not created until it gets content!
    Mongo_mycol = Mongo_mydb[configs.MongoT_Collection]
    #myquery = { "$and": [{"message.date" : {"$gt": after_unix_date}}, {"message.from.id" : Telegram_Id}]}
    #docs = Mongo_mycol.find().sort("_id",-1).limit(50)
    try: 

        doc_file_ID = doc["message"]["photo"][-1]["file_id"]
        doc_Telegram_ID = doc["message"]["from"]["id"]
        doc_date = doc["message"]["date"]
        doc_file_size = doc["message"]["photo"][-1]["file_size"]

        url = f"https://api.telegram.org/bot{configs.Telegram_Key}/getFile?file_id={doc_file_ID}"
        url_response_str= requests.get(url).text
        url_response_json = json.loads(url_response_str)
        #print(url_response_json)
        
        #print(url_response_json)
        url_photo_path = url_response_json["result"]["file_path"]
        #print(url_photo_path)
        url_file_1Hour = f"https://api.telegram.org/file/bot{configs.Telegram_Key}/{url_photo_path}"
        #print(url_file_1Hour)
        img_data = requests.get(url_file_1Hour).content
        
        imagex_path = f"{Folder}/{doc_date}_date_{doc_Telegram_ID}_id.png"
        with open(imagex_path, 'wb') as handler:
            handler.write(img_data)

    except Exception as e:
        print(e)
    return imagex_path


def Mongo_toExcel(Folder_Excel, after_unix_date): 
    """
    Text between two links/images is considered one blob
    """
    Folder_Excel = configs.Folder_Excel
    Mongo_client = pymongo.MongoClient(configs.MongoT_Client)
    Mongo_mydb = Mongo_client[configs.MongoT_Database]
    #Important: In MongoDB, a database is not created until it gets content!
    Mongo_mycol = Mongo_mydb[configs.MongoT_Collection]

    myquery = { "$and": [{"message.date" : {"$gt": after_unix_date}},
                        {"message.from.id": {"$nin": [1307289323, 1981887561, 1874743001]}}]}
    #myquery = { "$and": [{"message.date" : {"$gt": after_unix_date}}]}
    docs = Mongo_mycol.find(myquery)
    
    Cols_Names = ["TelegramID", "Unix date", "Data mesaj", "Numele utilizatorului", "Text tg", "Linkuri", "Text poza", "Poza nume"]

    dfx = pd.DataFrame(columns= Cols_Names)
    #print(len(dfx))

    for doc in docs:
        #print(dumps(doc, indent=4, sort_keys=True))
        doc = json.loads(dumps(doc))
        
        User_Telegram_ID = doc["message"]["from"]["id"]
        User_date = doc["message"]["date"]
        User_date_str = datetime.utcfromtimestamp(int(User_date)).strftime('%Y-%m-%d %H:%M:%S')
        User_FName = exists(doc, ['message', 'from', 'first_name']) if not None else ""
        User_LName = exists(doc, ['message', 'from', 'last_name']) if not None else ""
        User_Full_Name = str(User_FName) +" "+ str(User_LName)
        #print(User_Full_Name)

        User_Text = exists(doc, ['message', 'text'])
        #print("User_Text = ", User_Text)
        if User_Text is not None:
            urls_list = re.findall('(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', User_Text)
            urls_string = " , ".join(urls_list)
        else:
            urls_string = " "

        User_PicCaption = exists(doc, ['message', 'caption']) if not None else ""
        #print("User_PicCaption = ", User_PicCaption)
        User_Pic = exists(doc, ['message', 'photo'])

        if User_Pic is not None:
            User_Pic_Path= T_Mongo_Picture_Log(doc).split("/")[-1]
            print(User_Pic_Path)
        else:
            User_Pic_Path = ""

        Cols_Values = [User_Telegram_ID, User_date,User_date_str, User_Full_Name, User_Text,urls_string, User_PicCaption, User_Pic_Path]

        dfx.loc[len(dfx)] =Cols_Values

    datestr_after_unix_date = datetime.utcfromtimestamp(int(after_unix_date)).strftime('_%Y-%m-%d__%H-%M-%S')
    dfx.to_excel(f"{Folder_Excel}/{after_unix_date}__{datestr_after_unix_date}.xlsx")
    other_func.move_files(configs.Folder_temp_images, configs.Folder_shared_images)

def maxdate_path(Folder_Excel):
    Folder_Excel= configs.Folder_Excel
    Excel_Files= [ int(x.split("_")[0])  for x in os.listdir(Folder_Excel)]
    print(Excel_Files)
    print(max(Excel_Files))

if __name__ == "__main__":
    print(f"Executing the main {sys.argv[0]}")
else: 
    print(f"Imported {sys.argv[0]}")