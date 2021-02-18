#! python

import pprint
import pyodbc
import pandas as pd

driver = '{SQL Server}'
server = 'PC750\SQLEXPRESS'
database = 'hinkan_sheet'
trusted_connection = 'yes'

cnxn = pyodbc.connect('DRIVER=' + driver + ';SERVER=' + server + ';DATABASE=' 
        + database + ';PORT=1433;Trusted_Connection=' + trusted_connection +';')
cursor = cnxn.cursor()

sqlQuery = "SELECT 粘度1 FROM dbo.hinken_data where 品番 = 'S6-UV361-U'"
df = pd.read_sql(sqlQuery, cnxn)

print(df)
# cursor.execute("SELECT * FROM dbo.hinken_data")
# rows = cursor.fetchall()
# pprint.pprint(rows)

cursor.close()
cnxn.close()
