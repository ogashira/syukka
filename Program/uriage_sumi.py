#! python
# -*- coding: utf-8 -*-

import pandas as pd
import datetime


class UriageSumi(object):

    def __init__ (self):

        uriage_sumi = pd.read_csv(
                r'../master/effitA/uriage_sumi.csv', 
                skiprows = 1,
                encoding='cp932'
        )
        uriage_sumi = uriage_sumi.rename(
                columns = {
                    '売上日':'出荷予定日',
                    '運送業者':'依頼先',
                    '自由使用区分１':'配送区分',
                    '請求予定年月日':'closeDate',
                    '管理個数':'受注数量',
                    '管理単位':'受注単位',
                    '振替元品番':'hinban',
                    '振替元数量':'cans',
                    'ロットＮＯ':'lot',
                }
        )

        uriage_sumi['出荷予定日'] = uriage_sumi['出荷予定日'].map(
                lambda x : '{}/{}/{}'.format(str(x)[:4],str(x)[4:6],str(x)[6:])
        )
        uriage_sumi['closeDate'] = uriage_sumi['closeDate'].map(
                lambda x : '{}/{}/{}'.format(str(x)[:4],str(x)[4:6],str(x)[6:])
        )
        uriage_sumi['納期'] = uriage_sumi['納期'].map(
                lambda x : '{}/{}/{}'.format(str(x)[:4],str(x)[4:6],str(x)[6:])
        )

        self.uriage_sumi = uriage_sumi[uriage_sumi['得意先コード'] < 'T6000']


    def get_uriage_sumi(self):
        '''
        self.uriage_sumiに'lot_dic'列を追加して{lot:cans}の辞書を得る
        次に、self.uriage_sumiは複数LOTの場合はLOTごとに行があるので、
        重複する受注no、受注行noで、{lot:cans, lot:cans} の形にまとめて１行にする。
        '''

        def get_dic_lot (row):
            # {lot:cans}の形にする
            dic_lot = {}
            lot = row['lot']
            if pd.isnull(row['hinban']):
                cans = row['受注数量']
            else:
                cans = row['cans']
            dic_lot[lot] = cans
            return dic_lot

        uriage_sumi = self.uriage_sumi.copy()
        uriage_sumi['dic_lot'] = uriage_sumi.apply(get_dic_lot, axis=1)

        uriage_sumi = uriage_sumi.sort_values(['受注ＮＯ', '受注行ＮＯ'])
        uriage_sumi = uriage_sumi.reset_index()


        for i in range(len(uriage_sumi)-1):
            JNo = uriage_sumi.loc[i, '受注ＮＯ']
            JGNo = uriage_sumi.loc[i, '受注行ＮＯ']
            dic_lot = uriage_sumi.loc[i, 'dic_lot']
            j = 1
            while uriage_sumi.loc[i+j, '受注ＮＯ'] == JNo and (
                    uriage_sumi.loc[i+j, '受注行ＮＯ'] == JGNo):
                add_dic_lot = uriage_sumi.loc[i+j, 'dic_lot']
                add_lot = [k for k, v in add_dic_lot.items()][0]
                add_cans = [v for k, v in add_dic_lot.items()][0]

                dic_lot[add_lot] = add_cans

                # .locではエラーになる。辞書やﾘｽﾄを代入するときは.atを使う
                # .locでは複数選択の意味があるので単一セルしか選択できない.atを使う
                uriage_sumi.at[i, 'dic_lot'] = dic_lot

                uriage_sumi.loc[i+j, '得意先注文ＮＯ'] = 'del'

                # i+jが最終行であったらwhileを抜ける
                if i + j == len(uriage_sumi)-1:
                    break

                j += 1

        uriage_sumi2 = uriage_sumi.loc[uriage_sumi['得意先注文ＮＯ'] != 'del', :]

        return uriage_sumi2


    def get_UU_sumi(self, untinForUriage):

        uriage_sumi = self.get_uriage_sumi()
        UU = untinForUriage

        UU_sumi = pd.merge(UU, uriage_sumi, on =['受注ＮＯ', '受注行ＮＯ'], how = 'left')

        return UU_sumi

'''
    def check_sumi(self, UU_sumi):
        
        def check(df_row):
'''
