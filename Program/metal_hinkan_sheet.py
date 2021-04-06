#! python
# -*- coding: utf-8 -*-

import win32com.client
import time



class MetalHinkanSheet(object):

    def __init__(self, MHS_nonExistent_coa):
        """
        MHS_nonExistent_coaはnonExistent_coaの中のﾒﾀﾙ品管ｼｰﾄ分のみ
        """
        self.nonExistent_coa = MHS_nonExistent_coa
        
        nonExistent_coa_lot = [] # get_hinken_dataに渡す
        nonExistent_coa_hinban = [] # spec_dataに渡す
        for row in self.nonExistent_coa:
            if row[4] == '営業':
                nonExistent_coa_lot.append(row[0])
                nonExistent_coa_hinban.append(row[3])

        self.hinken_data = sql.get_hinken_data(nonExistent_coa_lot)

        self.spec_data = pd.read_excel(r'//192.168.1.247/Guest/'
                r'品質検査管理ｼｰﾄ2017.xlsm', 'ﾌｫｰﾏｯﾄ用ﾃﾞｰﾀ', engine='openpyxl')
        self.spec_data = self.spec_data.fillna('-')
       
        # isinを使ってﾘｽﾄに存在する品番のみを取得する
        self.spec_data = self.spec_data[self.spec_data['入力名']
                                                .isin(nonExistent_coa_hinban)] 
        self.spec_data = self.spec_data.iloc[:,:111 ] # 92列までを取得

