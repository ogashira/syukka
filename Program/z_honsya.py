#! python
# -*- coding: utf-8 -*-

import pprint
import pyodbc
import pandas as pd






driver = '{SQL Server}'
server = '192.168.1.245\SQL2016'
database = '東洋工業塗料'
uid = 'sa'
pwd = 'toyo-mjsys'


# 2021/2/26変換できない文字ℓなどをテキストﾌｧｲﾙなどに書き込むときに
# エラーが出て半日悩んだ。この関数で変換できない文字を？に変換して解決。
# 変換できない文字を無視する場合は、
# replaceの代わりにignoreを使う
def henkan(str_text):
    if type(str_text) == str:
        str_text = str_text.encode('cp932','replace')
        #このままだと出力時に\x90D\x93cのようになって読めないので直す
        str_text = str_text.decode('cp932')
    return str_text





cnxn = pyodbc.connect('DRIVER=' + driver + 
                      ';SERVER=' + server + 
                      ';DATABASE=' + database +
                      ';UID=' + uid +
                      ';PWD=' + pwd + 
                      ';CHARSET = cp932'
                     )

cursor = cnxn.cursor()

sqlQuery = ("SELECT ZaiHinCD AS '品番', ZaiBuCD AS '倉庫',"
            " ZaiLotNo AS 'ロットNo', ZaiZaiSuG AS '在庫数量（現在）'" 
            " From dbo.BZAIKO"
            " WHERE (ZaiBuCD = 'S0001'"
            " OR ZaiBuCD = 'S0021'"
            " OR ZaiBuCD = 'S0031')"
            " AND ZaiZaiSuG > 0"
            " AND ZaiHinCD NOT LIKE '%-EX'"
            )
df = pd.read_sql(sqlQuery, cnxn)
df = df.groupby(['品番','倉庫','ロットNo'],as_index=False).sum()
df = df.sort_values(by=['品番', '倉庫', 'ロットNo'])

#df = df.reset_index(drop = True)

cursor.close()
cnxn.close()

# henkanに渡して、変換できない文字ℓなどを？に変換する。    
df = df.applymap(henkan)
df.to_csv(r'./z.csv',encoding='cp932')


print(df)
