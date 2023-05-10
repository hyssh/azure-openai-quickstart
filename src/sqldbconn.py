import os
import dotenv
import pyodbc

dotenv.load_dotenv()

def get_connx():
    """
    Connect to SQL database
    Have variables in .env file
    
    SQL_SERVER= 
    SQL_DATABASE=
    SQL_USERNAME=
    SQL_PASSWORD=
    """
    # connect to database
    server = os.getenv("SQL_SERVER")
    database = os.getenv("SQL_DATABASE")
    username = os.getenv("SQL_USERNAME")
    password = os.getenv("SQL_PASSWORD")
    driver= '{ODBC Driver 18 for SQL Server}'
    return pyodbc.connect('Driver='+driver+';Server=tcp:'+server+',1433;Database='+database+';Uid='+username+';Pwd='+ password+';Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')

def get_data(query: str):
    cnxn = get_connx()
    # execute query using the given query variable
    cursor = cnxn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    # close the connection
    cnxn.close()
    return results

