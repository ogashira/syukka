#! python
# -*- coding: utf-8 -*-

import os
import pandas as pd


class UntinKeisanSheet(object):
    '''
    packingからuntin_motoを受けて、運賃計算ｼｰﾄにadd回数を表示する。
    表示したら、受注noとaddを所定のﾌｫﾙﾀﾞに保存する。create_folder
    所定のﾌｫﾙﾀﾞの中に、sumi.csvが存在しなければ cnt = 1
    sumi.csvが存在すれば、cnt はsumi.csvのadd列のmaxとする
    '''

    def __init__(self, untin_moto):
        
        self.untin_moto = untin_moto
        self.uriage_day = str(untin_moto.loc[0, '出荷予定日'])
        folder_name = self.uriage_day
        # ﾌｫﾙﾀﾞが存在しなければ作る（出荷予定日のﾌｫﾙﾀﾞ名）
        if os.path.exists(r'../tmp/{}'.format(folder_name)):
            pass
        else:
            os.mkdir(r'../tmp/{}'.format(folder_name))


            
    def sheet_add_cnt(self):
        folder_name = self.uriage_day
        if os.path.exists(r'../tmp/{}/add_cnt.csv'.format(folder_name)):
            add_cnt = pd.read_csv(r'../tmp/{}/add_cnt.csv'.format(folder_name), 
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
        moto_add_after = moto_add_after.drop_duplicates(['受注ＮＯ', '受注行ＮＯ'])
        moto_add_after.to_csv(r'../tmp/{}/add_cnt.csv'.format(folder_name), 
                                                            encoding = 'cp932')

        return moto_add


    def sheet_add_sumi(self, moto):
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
        

        


