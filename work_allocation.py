import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import configs
import sys
from datetime import datetime

import psycopg2
from sqlalchemy import create_engine
import random

from read_spreadsheet import read_all_table_profiles, read_all_table_workallocation, engine
import configs


"""
1.Checks the database for shady profiles
2. Selects a random link
3. Checks if the link selected was previouslu allocated to the Telegram User
3.1. Selects a [TelegramID, link] pair that does not exist, inserts it into 
/the database and returns the pair as list
"""
def give_work_link_name(Telegram_ID):
    dfx= read_all_table_profiles()
    dfx = dfx.drop_duplicates(subset= "Link", keep="last")
    #print(dfx.columns.tolist())
    #print(len(dfx))
    df_work = read_all_table_workallocation()
    #print(len(df_work))
    #print(df_work)
    df_work_columns_list = df_work.columns.tolist()
    #print(df_work_columns_list)
    links= dfx['Link'].tolist()

    for x in range(len(dfx)):
        link_random = random.choice(links)
        #print(x,"  ",len(links))
        #print(link_random)
        index_link = dfx['Link'].tolist().index(link_random)
        links = [x for x in links if x!= link_random]
        #print(index_link)
        #boolean- checks if [Telegram_ID, link_random] combination already allocated
        #print(type(df_work["telegramid"][0]))
        Work_Check= ((df_work["telegramid"]== Telegram_ID) & (df_work["link_report"]== link_random)).any()
        #print(Work_Check)
        #print(Telegram_ID, link_random)
        if Work_Check == True:
            continue    
        else:
            #print(datetime.now())
            df_work_one = pd.DataFrame( columns= df_work_columns_list)
            df_work_one.loc[0]=[datetime.now(), Telegram_ID, link_random]
            #print(df_work_one.loc[0])
            with engine.connect() as conn:
                df_work_one.to_sql(f'{configs.Table_2}', con=conn, if_exists="append",index=False)
            break
    
    name = dfx['Name of profile'][index_link]
    comments= dfx['Authentic profile/ comments'][index_link]
    #print(name)
    return [link_random, name, comments]

#print(give_work_link_name(configs.Telegram_ID_C))

#print(give_work_link_name(801734855))