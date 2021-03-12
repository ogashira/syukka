#! python
# -*- coding: utf-8 -*-

import glob
import shutil
import pandas as pd

class Coa(object):


    def __init__(self):
        pass



    def get_packingCoa(self, modi_PH, modi_UU):
        """
        modi_PH_tokeまたはmodi_PH_honsya, modi_UU_tokeまたはmodi_UU_honsya
        を与えて、土気分、本社分のpackingCoaを作る
        """
        
        lot_data = modi_UU[['受注ＮＯ', '受注行ＮＯ', 'lot']]
        packingCoa = pd.merge(modi_PH, lot_data, on =['受注ＮＯ', '受注行ＮＯ'] 
                , how = 'left')

        packingCoa = packingCoa[[
            '出荷予定日', '得意先コード', '納入先コード', '納入先名称１', 
            'hinban', '出荷', '受注ＮＯ', '受注行ＮＯ', 'lot', '出荷予定倉庫'
        ]]
        return packingCoa

        











    def find_coa(self):

        directory = r'//192.168.1.247/共有/営業課ﾌｫﾙﾀﾞ/testreport/櫻田/'
        path = directory + '*20102951T*.pdf'
        files = glob.glob(path)
        print(len(files))
        for file in files:
            try:
                new_file_path = './'
                shutil.copy(file, new_file_path)

            except FileNotFoundError:
                print('File Not Found!')


