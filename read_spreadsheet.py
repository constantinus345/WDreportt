import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import configs
import sys
from datetime import datetime

import psycopg2
from sqlalchemy import create_engine

sheet_key= configs.sheet_key
JSON_Creds= configs.JSON_Creds

engine = create_engine(f"""postgresql://postgres:{configs.DB_password}\
@localhost:{configs.DB_port}/{configs.Databasex}""")

def list_of_sheets(sheet_key=sheet_key, JSON_Creds= JSON_Creds, sheetsorids="sheets"):
    scope = ['https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(JSON_Creds, scope)
    gc = gspread.authorize(credentials)


    wks= gc.open_by_key(sheet_key)
    worksheet_list_classes = wks.worksheets()
    #Could't figure out how to extract sheet_name and ids from class, hence this artifice with string

    worksheet_list_names = [str(x).split("'")[1] for x in worksheet_list_classes]
    worksheet_list_ids = [int(str(x).split(":")[-1][:-1]) for x in worksheet_list_classes]
    if sheetsorids == "ids":
        return worksheet_list_ids
    return  worksheet_list_names

#print(list_of_sheets(sheetsorids="ids"))
#print(list_of_sheets())


def df_sheet(sheetname, sheet_key=sheet_key, JSON_Creds= JSON_Creds):
    scope = ['https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(JSON_Creds, scope)
    gc = gspread.authorize(credentials)


    doc = gc.open_by_key(sheet_key)

    sheet = doc.worksheet(sheetname)

    dataframe = pd.DataFrame(sheet.get_all_records())
    #dataframe = pd.DataFrame(sheet.get_values())

    return dataframe

def write_spreadsheet_to_excel_periodically(Sheet="Suspect or fake profiles"):

    datenow= datetime.now().strftime("%m-%d-%Y")
    dfx= df_sheet("Suspect or fake profiles")
    print(datenow)
    print(dfx.columns.tolist())
    dfx.drop('', axis=1, inplace= True)
    print(dfx.columns.tolist())
    Sheet="Suspect or fake profiles"
    dfx.to_excel(f"{configs.Excel_Location}/{Sheet}_{datenow}.xlsx")
    with engine.connect() as conn:
        dfx.to_sql(f'{configs.Table_1}', con=conn, if_exists="replace",index=False)

def  read_all_table_profiles(Table=f"{configs.Table_1}"):
    SQLq= f"""SELECT * FROM public.{configs.Table_1}"""
    with engine.connect() as conn:
        dfx = pd.read_sql(SQLq, con=conn)
    return dfx

def  read_all_table_workallocation(Table=f"{configs.Table_2}"):
    Table=f"{configs.Table_2}"
    SQLq= f"""SELECT * FROM public.{Table}"""
    with engine.connect() as conn:
        dfx = pd.read_sql(SQLq, con=conn)
    return dfx

File_Name= sys.argv[0]

if __name__ == "__main__":
    print("Executing the main")
else: 
    print(f"Imported {File_Name}")

"""
for shs in list_of_sheets():
    try:
        print(f"Sheet {shs} columns:\n {list(df_sheet(shs))}\n{'_'*60}\n")
    except Exception as e:
        print(shs," - ",e)"""

