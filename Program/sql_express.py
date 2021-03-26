#! python
# -*- coding: utf-8 -*-

import pprint
import pyodbc
import pandas as pd



class SqlExpress(object):

    def __init__(self):

        self.driver = '{SQL Server}'
        self.server = 'PC750\SQLEXPRESS'
        self.database = 'hinkan_sheet'
        self.trusted_connection = 'yes'


    def get_hinken_data(self, nonExistent_coa_lot):

        cnxn = pyodbc.connect('DRIVER=' + self.driver + 
                              ';SERVER=' + self.server + 
                              ';DATABASE=' + self.database + 
                              ';PORT=1433'
                              ';Trusted_Connection=' + self.trusted_connection +';'
                              )

        cursor = cnxn.cursor()

        lots = "ロットＮＯ = '1111111H'"
        for lot in nonExistent_coa_lot:
            if lots == "ロットＮＯ = '1111111H'":
                lots = "ロットＮＯ = " + '\'' + lot + '\''
            else:
                lots = lots + " OR ロットＮＯ = " + '\'' + lot + '\''

        # lots = "ロットＮＯ = '21031201H' OR ロットＮＯ = '21031231H'"

        sqlQuery = ("SELECT *"
                    " FROM dbo.hinken_data"
                    " LEFT JOIN dbo.tantousya_data"
                    " ON hinken_data.品番 = tantousya_data.hinban"
                    " WHERE " + lots
                   )
        df = pd.read_sql(sqlQuery, cnxn)

        cursor.close()
        cnxn.close()

        return df


