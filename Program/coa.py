#! python
# -*- coding: utf-8 -*-

import glob
import shutil
import pandas as pd
from add_data import AddData


class Coa(object):


    def __init__(self, modi_PH, modi_UU):
        self.modi_PH = modi_PH
        self.modi_UU = modi_UU


    def get_packingCoa(self):
        """
        modi_PH_tokeまたはmodi_PH_honsya, modi_UU_tokeまたはmodi_UU_honsya
        を与えて、土気分、本社分のpackingCoaを作る
        """
        
        lot_data = self.modi_UU[['受注ＮＯ', '受注行ＮＯ', 'lot']]
        packingCoa = pd.merge(self.modi_PH, lot_data, 
                            on =['受注ＮＯ', '受注行ＮＯ'] , how = 'left')

        packingCoa = packingCoa[[
            '出荷予定日', '得意先コード', '納入先コード', '納入先名称１', 
            'hinban', '出荷', '受注ＮＯ', '受注行ＮＯ', 'lot', '出荷予定倉庫'
        ]]
        return packingCoa

        
    def get_coa_list(self):
        ad = AddData()
        coa_list = ad.coa_list
        del ad
        return coa_list


    def get_packingCoa_list(self):

        packingCoa = self.get_packingCoa()
        packingCoa = packingCoa.fillna({'納入先コード':''})
        coa_list = self.get_coa_list()
        del coa_list[:2]

        #packingCoa['出荷予定倉庫'].map(lambda x : x.append('成'))
        #packingCoa['lot'].map(lambda x :  x['21031200H'] = 15)

        """
        packingCoa_listを作る。
        packingCoa(dataframe)から成のある行を抜き出し、
        [['lot','tokuiCD', 'nonyuCD', 'hinban']....]にする
        lotが２つ以上ある場合も対応して表示する
        """
        packingCoa_list = []
        for i in range(len(packingCoa)):
            yoteisouko = packingCoa.loc[i,'出荷予定倉庫']
            lot = packingCoa.loc[i,'lot']
            tokuiCD = packingCoa.loc[i,'得意先コード']
            nonyuCD = packingCoa.loc[i,'納入先コード']
            hinban = packingCoa.loc[i,'hinban']

            if '成' in yoteisouko:
                for k in lot.keys():
                    list_row = []
                    list_row.append(k)
                    list_row.append(tokuiCD)
                    list_row.append(nonyuCD)
                    list_row.append(hinban)

                    packingCoa_list.append(list_row)

        """
        packingCoaﾘｽﾄにcoa_listの作成部署、成績書formatをくっつける
        """
        for row in packingCoa_list:
            for add_row in coa_list:
                if (row[1] == add_row[0] and row[2] == add_row[1] 
                                                      and row[3] == add_row[3]):
                    row.append(add_row[5])
                    row.append(add_row[6])

                    



        return packingCoa_list









    def find_coa(self):

        directory = r'//192.168.1.247/共有/営業課ﾌｫﾙﾀﾞ/testreport/櫻田/'
        path = directory + '*20120801H*伊坂(美光ABなし).pdf'
        files = glob.glob(path)
        print(len(files))
        for file in files:
            try:
                new_file_path = './'
                shutil.copy(file, new_file_path)

            except FileNotFoundError:
                print('File Not Found!')


