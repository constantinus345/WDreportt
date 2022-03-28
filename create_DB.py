#& d:/Python_Code/CursValutar2/Scripts/python.exe d:/Python_Code/CursValutar2/creating_DB.py

import psycopg2
from sqlalchemy import create_engine
import configs 

try:
    conn = psycopg2.connect(
       database=configs.Databasex, user= configs.DB_user , password= configs.DB_password , host= configs.DB_host, port= configs.DB_port
    )
    cur = conn.cursor()
    conn.close()
except Exception as e:
    print(e)
    conn = psycopg2.connect(
       database="postgres", user= configs.DB_user , password= configs.DB_password , host= configs.DB_host, port= configs.DB_port)
    
    cursor = conn.cursor()
    
    conn.autocommit = True
    sql = f'''CREATE database {configs.Databasex}'''
    
    #Creating a database
    cursor.execute(sql)
    print("Database created successfully........")
    conn.commit()
    #Closing the connection
    conn.close()
#Creating a cursor object using the cursor() method

conn = psycopg2.connect(
   database=configs.Databasex, user= configs.DB_user , password= configs.DB_password , host= configs.DB_host, port= configs.DB_port
)
cursor = conn.cursor()

engine = create_engine(f'postgresql://postgres:{configs.DB_password}@localhost:{configs.DB_port}/{configs.Databasex}')


"""
Fetches all tables and if configs.Table_1 is not there, it creates it
Uses ColumnsX schema
"""

cursor.execute("""SELECT table_name FROM information_schema.tables
       WHERE table_schema = 'public'""")
    
try:
   tables = [i[0] for i in cursor.fetchall()] # A list() of tables.
except:
   tables = []

def create_table(Table_name,Column_List):
   if Table_name.lower() not in tables:
      #Creating table as per requirement
      sql =f'''CREATE TABLE {Table_name}({Column_List});'''
      print(repr(sql))
      cursor.execute(sql)
      
      print(f"Table {Table_name} created successfully")
      conn.commit()
   else: 
      print(f"{Table_name} already exists")

create_table(configs.Table_1, configs.Columns_1)
create_table(configs.Table_2, configs.Columns_2)

conn.close()
engine.dispose()