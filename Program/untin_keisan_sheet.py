#! python
# -*- coding: utf-8 -*-

import os
import pandas as pd
import platform
from sql_query import *
import numpy as np


class UntinKeisanSheet(object):
    '''
    packingからuntin_motoを受けて、運賃計算ｼｰﾄにadd回数を表示する。
    表示したら、受注noとaddを所定のﾌｫﾙﾀﾞに保存する。create_folder
    所定のﾌｫﾙﾀﾞの中に、sumi.csvが存在しなければ cnt = 1
    sumi.csvが存在すれば、cnt はsumi.csvのadd列のmaxとする
    '''

    def __init__(self, untin_moto, uriagebi, sengetu):
        
        self.uriagebi = uriagebi
        self.sengetu = sengetu
        self.untin_moto = untin_moto
        self.uriage_day = str(untin_moto.loc[0, '出荷予定日'])
        folder_name = self.uriage_day
        self.folder_path = ''
        if platform.system() == 'Windows':
            self.folder_path = r'//192.168.1.247/共有/営業課ﾌｫﾙﾀﾞ/01出荷OutPut/addCount/'
        elif platform.system() == 'Linux':
            self.folder_path = r'/mnt/public/営業課ﾌｫﾙﾀﾞ/01出荷OutPut/addCount/'
        else:
            self.folder_path = r'./'


        # ﾌｫﾙﾀﾞが存在しなければ作る（出荷予定日のﾌｫﾙﾀﾞ名）
        if os.path.exists(self.folder_path + '{}'.format(folder_name)):
            pass
        else:
            os.mkdir(self.folder_path + '{}'.format(folder_name))

# \\192.168.1.247\共有\営業課ﾌｫﾙﾀﾞ\01出荷OutPut\addCount
            
    def sheet_add_cnt(self):
        folder_name = self.uriage_day
        if os.path.exists(self.folder_path + '{}/add_cnt.csv'.format(folder_name)):
            add_cnt = pd.read_csv(self.folder_path + '{}/add_cnt.csv'.format(folder_name), 
                                                               encoding='cp932')
            cnt = add_cnt['add'].max()
            moto_add = pd.merge(self.untin_moto, add_cnt, 
                                  on = ['受注ＮＯ', '受注行ＮＯ'], how = 'left')
            moto_add = moto_add.fillna({'add': cnt+1})
        else:
            cnt = 1
            moto_add = self.untin_moto.copy()
            moto_add['add'] = cnt

        moto_add_after = moto_add[['受注ＮＯ', '受注行ＮＯ', 'add']]
        moto_add_after = moto_add_after.drop_duplicates(subset= ['受注ＮＯ', '受注行ＮＯ'])
        moto_add_after.to_csv(self.folder_path + '/{}/add_cnt.csv'.format(folder_name), 
                                                            encoding = 'cp932')

        return moto_add


    def sheet_add_sumi(self, moto):
        pf = platform.system()
        if pf == 'Windows' or pf == 'Linux':
            sql = SqlQuery(self.uriagebi, self.sengetu)
            uriage_mae = sql.get_uriage_sumi()
            uriage_mae = uriage_mae.apply(
                    lambda col: col.map(lambda x : np.nan if x == ' ' else x))
            del sql
        else:
            uriage_mae = pd.read_csv(
                r'../master/effitA/uriage_mae.csv',
                skiprows = 1,
                encoding= 'cp932'
            )
        uriage_mae = uriage_mae.drop_duplicates(['売上ＮＯ', '売上行ＮＯ'])
        uriage_mae = uriage_mae[['受注ＮＯ', '受注行ＮＯ']]
        uriage_mae['sumi'] = '済'

        moto_sumi = pd.merge(moto, uriage_mae, on = ['受注ＮＯ', '受注行ＮＯ'],
                             how = 'left')
        return moto_sumi
        

        


