#! python
# -*- coding: utf-8 -*-

from sql_express import *




class HinkanSheet(object):

    def __init__(self, HS_nonExistent_coa):
        sql = SqlExpress()
        self.nonExistent_coa = HS_nonExistent_coa
        
        nonExistent_coa_lot = [] # get_hinken_dataに渡す
        nonExistent_coa_hinban = [] # get_spec_dataに渡す
        for row in self.nonExistent_coa:
            if row[4] == '営業':
                nonExistent_coa_lot.append(row[0])
                nonExistent_coa_hinban.append(row[3])

        self.hinken_data = sql.get_hinken_data(nonExistent_coa_lot)

        self.spec_data = pd.read_excel(r'//192.168.1.247/Guest/品質検査管理ｼｰﾄ2017.xlsm', 'ﾌｫｰﾏｯﾄ用ﾃﾞｰﾀ', engine='openpyxl')
        self.spec_data = self.spec_data.fillna('-')
        #print(self.spec_data.head(100)) 
