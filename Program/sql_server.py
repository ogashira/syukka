#! python

import pprint
import pyodbc
import pandas as pd




driver = '{SQL Server}'
server = '192.168.1.245\SQL2016'
database = '東洋工業塗料'
uid = 'sa'
pwd = 'toyo-mjsys'

cnxn = pyodbc.connect('DRIVER=' + driver + 
                      ';SERVER=' + server + 
                      ';DATABASE=' + database +
                      ';UID=' + uid +
                      ';PWD=' + pwd +
                      ';CHARSET = cp932'
                     )

cursor = cnxn.cursor()

sqlQuery = ("SELECT RJYUCD.RjcTokCD, RJYUCD.RjcNonyuCD, RJYUCH.RjcTokNam1," 
            " RJYUCH.RjcNonyuNam1, RJYUCH.RjcNonyuNam2, RJYUCD.RjcSKDay,"
            " RJYUCD.RjcHinCD, RJYUCD.RjcHinNam, RJYUCD.RjcJcSu, RJYUCD.RjcTniCD,"
            " RJYUCD.RjcCMNo, RJYUCD.RjcJCNo, RJYUCD.RjcJGNo, RJYUCD.RjcMBiko,"
            " RJYUCD.RjcSokoCD, RJYUCH.RjcHBiko, RJYUCD.RjcNODay"
            " From dbo.RJYUCD"
            " LEFT JOIN dbo.RJYUCH"
            " ON RJYUCD.RjcJCNo = RJYUCH.RjcJCNo"
            " WHERE RJYUCD.RjcSKDay = '20210219'")
df = pd.read_sql(sqlQuery, cnxn)
df = df.rename(columns={'RjcTokCD': '得意先コード', 'RjcNonyuCD': '納入先コード', 
                        'RjcTokNam1': '得意先名称１','RjcNonyuNam1': '納入先名称１', 
                        'RjcNonyuNam2': '納入先名称２', 'RjcSKDay': '出荷予定日', 
                        'RjcHinCD': '品番', 'RjcHinNam':'品名', 'RjcJcSu':'受注数量', 
                        'RjcTniCD':'受注単位','RjcCMNo': '得意先注文ＮＯ', 
                        'RjcJCNo': '受注ＮＯ', 'RjcJGNo': '受注行ＮＯ', 
                        'RjcMBiko': '備考', 'RjcSokoCD': '出荷予定倉庫', 
                        'RjcHBiko': '備考.1', 'RjcNODay': '納期'})



print(df)

cursor.close()
cnxn.close()
def get_df():
    return df

