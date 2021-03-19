#! python
# -*- coding: utf-8 -*-

import glob
import shutil
import pandas as pd
from add_data import AddData
from recorder import *
from hinkan_sheet import *


class Coa(object):


    def __init__(self, modi_PH, modi_UU, myfolder):
        self.modi_PH = modi_PH
        self.modi_UU = modi_UU
        self.myfolder = myfolder


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



    def copy_coa(self, coa_folder, packingCoa_list):
        """
        copy出来なかったcoaを返す
        """
        nonExistent_coa = []

        # 工場名を取得
        factory = coa_folder[-2 :]

        directory = r'//192.168.1.247/共有/営業課ﾌｫﾙﾀﾞ/testreport/櫻田/'
        for row in packingCoa_list:
            if row[5] != 'ﾒﾀﾙ':
                path = directory + '*' + row[0] + '*' + row[5] + '.pdf'
            else:
                path = directory + '*' + row[0] + '*' + '.pdf'

            files = glob.glob(path)
            if len(files) > 0:
                for file in files:
                    shutil.copy(file, coa_folder)
                    break
            else:
                nonExistent_coa.append(row)

        recorder = Recorder(self.myfolder)
        txt = ('{}分の検査成績書を所定のﾌｫﾙﾀﾞ―にｺﾋﾟｰしました。\n'.format(factory))
        recorder.out_log(txt)
        recorder.out_file(txt)
        if nonExistent_coa == []:
            txt = ('{}分の検査成績書は全て完了です。\n'.format(factory))
            recorder.out_log(txt)
            recorder.out_file(txt)
        else:
            txt = ('{}分の検査成績書の以下が見つかりません。\n'.format(factory))
            recorder.out_log(txt)
            recorder.out_file(txt)
            recorder.out_log(nonExistent_coa, '\n\n')
            recorder.out_file(nonExistent_coa, '\n\n')

        return nonExistent_coa

    
    def get_HS_nonExistent_coa(self, nonExistent_coa):
        """品管ｼｰﾄ分のnonExistent_coaを求める"""
        HS_nonExistent_coa = []
        for row in nonExistent_coa:
            if row[5] != 'ﾒﾀﾙ':
                HS_nonExistent_coa.append(row)
        return HS_nonExistent_coa



    def get_MHS_nonExistent_coa(self, nonExistent_coa):
        """ﾒﾀﾙ品管ｼｰﾄ分のnonExistent_coaを求める"""
        MHS_nonExistent_coa = []
        for row in nonExistent_coa:
            if row[5] == 'ﾒﾀﾙ':
                MHS_nonExistent_coa.append(row)
        return MHS_nonExistent_coa


    def create_coa(self, nonExistent_coa):
        HS_nonExistent_coa = self.get_HS_nonExistent_coa(nonExistent_coa)
        MHS_nonExistent_coa = self.get_MHS_nonExistent_coa(nonExistent_coa)

        nonCreate_coa = [] 
        if HS_nonExistent_coa != [] :
            HS = HinkanSheet(HS_nonExistent_coa)

        if MHS_nonExistent_coa != []:
            pass


        return nonCreate_coa
