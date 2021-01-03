#! python
# -*- coding: cp932 -*-

import pandas as pd
import numpy as np
from closeDate import *
from zaiko import *
from add_data import *
from recorder import *
from lead_time import *


pd.set_option('display.max_columns', None)



class Ajust_toke:

    def __init__ (self, myfolder):
        self.myfolder = myfolder

    def get_allHauler(self, moto, untin):

        def best_hauler(row):
            nounyuusaki = row['納入先名称１']
            sitei = row['顧客指定運送屋']
            address = row['住所１']
            torr = row['ﾄｰﾙ']
            niigata = row['新潟']
            keihin = row['ｹｲﾋﾝ']

            dic = {'ﾄｰﾙ':float(torr), '新潟':float(niigata), 'ｹｲﾋﾝ':float(keihin)}
            
            #顧客指定運送屋がある場合はソレ、無い場合は最安値の運送屋を選ぶ
            #最安値が２つ以上ある場合を考慮して、リスト内包表記で求める。
            if address == 'NoCalc':
                best_hauler = ['配達']
            elif address is np.nan:
                best_hauler = ['npNan']
            elif sitei != '無し' and sitei != '無':
                best_hauler = [sitei]
            else:
                best_hauler = [kv[0] for kv in dic.items() if kv[1] == 
                               min(dic.values())]
            
            return best_hauler


        syukkabi = moto.iloc[0,5]

        untin['依頼先'] = untin.apply(best_hauler, axis=1) 
        untin['出荷予定日'] = syukkabi

        allHauler = untin[['出荷予定日','住所１','納入先名称１','得意先コード',
                           '納入先コード','weight','cans','ﾄｰﾙ','新潟','ｹｲﾋﾝ',
                           'ﾄﾅﾐ差額','依頼先','輸出向先']]



        # 依頼先のlistをリテラルにしておく
        allHauler2 = allHauler.copy()
        allHauler2.loc[:,'依頼先'] = allHauler2['依頼先'].map(lambda x : x[0])
        allHauler_sort = allHauler2.sort_values('依頼先')

        return allHauler_sort


    def get_packingHinban(self, moto, allHauler):
        
        allHauler = allHauler[['住所１','依頼先','輸出向先']]
        moto_addHinban = pd.merge(moto, allHauler, how= 'left', on='住所１')
        packingHinban = moto_addHinban[['出荷予定日','依頼先','cans','weight',
                                        '得意先コード','納入先コード',
                                        '納入先名称１', 'hinban', '品名','受注数量',
                                        '受注単位','得意先注文ＮＯ','備考','出荷',
                                        '出荷予定倉庫','輸出向先','納期', '受注ＮＯ',
                                        '受注行ＮＯ','add']]
        
        # 運送屋（依頼先）がNaNの場合はNo dataにする>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

        packingHinban = packingHinban.fillna({'依頼先':'NoData'})

        

        # 次回請求を求める>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        closeDate = CloseDate()

        packingHinban2 = packingHinban.copy() 
        packingHinban2[['出荷予定日','納期','曜日','closeDate']] = \
        packingHinban2.apply(closeDate.get_closeDate, axis=1)

        packingHinban3 = packingHinban2.copy()
        packingHinban3.loc[:,'出荷予定倉庫'] = packingHinban3.apply(
            closeDate.get_jikai, axis = 1)


        # 成、指を求める<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

        add_data = AddData()
        
        packingHinban3.loc[:,'出荷予定倉庫'] = packingHinban3.apply(
                  add_data.get_coa, axis = 1)

        
        del add_data
        # 曜日違いを求める<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

        lead_time = LeadTime()

        packingHinban3.loc[:,'出荷予定倉庫'] = packingHinban3.apply(
                lead_time.get_youbi, axis = 1)

        del lead_time
        #  土曜配達を判定<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

        def get_dohai(df_row):
            syukka_souko = df_row['出荷予定倉庫']
            week = df_row['曜日']

            if week == '土':
                syukka_souko.append('土曜配達')
            return syukka_souko


        packingHinban3.loc[:, '出荷予定倉庫'] = packingHinban3.apply(
                get_dohai, axis = 1)
        


        #  営業所止めを判定<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

        def get_siten_tome(df_row):
            syukka_souko = df_row['出荷予定倉庫']
            bikou = df_row['備考']

            if bikou.find('支店止め') >= 0 or bikou.find('支店どめ') >= 0 or \
                bikou.find('営業所止め') >= 0 or bikou.find('営業所どめ') >= 0 :
                syukka_souko.append('営業所')
            return syukka_souko


        packingHinban3.loc[:, '出荷予定倉庫'] = packingHinban3.apply(
                get_siten_tome, axis = 1)



        return packingHinban3

        
    def get_untinForUriage(self, moto, allHauler):
        allHauler = allHauler[['住所１','依頼先','輸出向先']]
        moto_addHauler = pd.merge(moto, allHauler, how= 'left', on='住所１')
        untinForUriage = moto_addHauler[['出荷予定日','得意先コード','納入先コード',
                                         '依頼先','備考','出荷予定倉庫','受注ＮＯ',
                                         '受注行ＮＯ','得意先注文ＮＯ','品番','hinban',
                                         'cans','納期', 'toyo_untin','輸出向先','出荷','add']]


        # 運送屋（依頼先）がNaNの場合はNo dataにする>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

        untinForUriage = untinForUriage.fillna({'依頼先':'NoData'})

        # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

        closeDate = CloseDate()

        untinForUriage2 = untinForUriage.copy() 
        untinForUriage2[['出荷予定日','納期','曜日','closeDate']] = \
        untinForUriage2.apply(closeDate.get_closeDate, axis=1)

        del closeDate

        # 曜日違いを求める<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

        lead_time = LeadTime()

        untinForUriage2.loc[:,'出荷予定倉庫'] = untinForUriage2.apply(
                lead_time.get_youbi, axis = 1)

        del lead_time
        # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
        
        zaiko = Zaiko(self.myfolder)
        recorder = Recorder(self.myfolder)
        
        txt ='売上処理入力用ﾃﾞｰﾀ（土気）' 
        recorder.out_log(txt, '\n')
        recorder.out_file(txt, '\n')

        untinForUriage2['lot'] = untinForUriage2.apply(zaiko.get_lot, axis=1)
        
        recorder.out_log('')
        recorder.out_file('')
        recorder.out_log(untinForUriage2, '\n')
        recorder.out_file(untinForUriage2, '\n')

        del zaiko
        del recorder



        return untinForUriage2


    def get_packingCoa(self, packingHinban, untinForUriage):
        lot_data = untinForUriage[['受注ＮＯ', '受注行ＮＯ', 'lot']]
        packingCoa = pd.merge(packingHinban, lot_data, on =['受注ＮＯ', '受注行ＮＯ'] 
                , how = 'left')

        packingCoa = packingCoa[[
            '出荷予定日', '得意先コード', '納入先コード', '納入先名称１', 
            'hinban', '出荷', '受注ＮＯ', '受注行ＮＯ', 'lot'
        ]]

        return packingCoa
        




class Ajust_honsya:


    def __init__ (self, myfolder):
        self.myfolder = myfolder


    def get_allHauler(self, moto, untin):

        def best_hauler(row):
            nounyuusaki = row['納入先名称１']
            sitei = row['顧客指定運送屋']
            address = row['住所１']
            torr = row['ﾄｰﾙ']
            niigata = row['新潟']
            keihin = row['ｹｲﾋﾝ']
            kurume = row['久留米']


            dic = {'ﾄｰﾙ':float(torr), '新潟':float(niigata), 'ｹｲﾋﾝ':float(keihin), '久留米':float(kurume)}
            
            #顧客指定運送屋がある場合はソレ、無い場合は最安値の運送屋を選ぶ
            #最安値が２つ以上ある場合を考慮して、リスト内包表記で求める。
            if address == 'NoCalc':
                best_hauler = ['NoCalc']
            elif address is np.nan:
                best_hauler = ['npNan']
            elif sitei != '無し':
                best_hauler = [sitei]
            else:
                best_hauler = [kv[0] for kv in dic.items() if kv[1] 
                               == min(dic.values())]
            
            return best_hauler


        syukkabi = moto.iloc[0,5]

        untin['依頼先'] = untin.apply(best_hauler, axis=1) 
        untin['出荷予定日'] = syukkabi

        allHauler = untin[['出荷予定日','住所１','納入先名称１','得意先コード',
                           '納入先コード','weight','cans','ﾄｰﾙ','新潟','ｹｲﾋﾝ',
                           '久留米','ﾄﾅﾐ差額','依頼先','輸出向先']]

        # 依頼先のlistをリテラルにしておく
        allHauler2 = allHauler.copy()
        allHauler2.loc[:,'依頼先'] = allHauler2['依頼先'].map(lambda x : x[0])
        allHauler_sort = allHauler2.sort_values('依頼先')


        return allHauler_sort




    def get_packingHinban(self, moto, allHauler):
        
        allHauler = allHauler[['住所１','依頼先','輸出向先']]
        moto_addHinban = pd.merge(moto, allHauler, how= 'left', on='住所１')
        packingHinban = moto_addHinban[['出荷予定日', '依頼先','cans','weight','得意先コード',
                                        '納入先コード','納入先名称１', 'hinban', '品名',
                                        '受注数量','受注単位','得意先注文ＮＯ',
                                        '備考','出荷','出荷予定倉庫','輸出向先',
                                        '納期', '受注ＮＯ', '受注行ＮＯ','add']]


        # 運送屋（依頼先）がNaNの場合はNo dataにする>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

        packingHinban = packingHinban.fillna({'依頼先':'NoData'})


        # 次回請求を求める>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        closeDate = CloseDate()

        packingHinban2 = packingHinban.copy() 
        packingHinban2[['出荷予定日','納期','曜日','closeDate']] = \
        packingHinban2.apply(closeDate.get_closeDate, axis=1)

        packingHinban3 = packingHinban2.copy()
        packingHinban3.loc[:,'出荷予定倉庫'] = packingHinban3.apply(
            closeDate.get_jikai, axis = 1)

        # 成、指を求める<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

        add_data = AddData()
        
        packingHinban3.loc[:,'出荷予定倉庫'] = packingHinban3.apply(
                  add_data.get_coa, axis = 1)

        
        del add_data
        #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
        # 曜日違いを求める<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

        lead_time = LeadTime()

        packingHinban3.loc[:,'出荷予定倉庫'] = packingHinban3.apply(
                lead_time.get_youbi, axis = 1)

        del lead_time
        # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
        #  土曜配達を判定<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

        def get_dohai(df_row):
            syukka_souko = df_row['出荷予定倉庫']
            week = df_row['曜日']

            if week == '土':
                syukka_souko.append('土曜配達')
            return syukka_souko

        packingHinban3.loc[:, '出荷予定倉庫'] = packingHinban3.apply(
                get_dohai, axis = 1)

        
        #  営業所止めを判定<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

        def get_siten_tome(df_row):
            syukka_souko = df_row['出荷予定倉庫']
            bikou = df_row['備考']

            if bikou.find('支店止め') >= 0 or bikou.find('支店どめ') >= 0 or \
                bikou.find('営業所止め') >= 0 or bikou.find('営業所どめ') >= 0 :
                syukka_souko.append('営業所')
            return syukka_souko


        packingHinban3.loc[:, '出荷予定倉庫'] = packingHinban3.apply(
                get_siten_tome, axis = 1)
        



        return packingHinban3



    def get_untinForUriage(self,moto, allHauler):
        allHauler = allHauler[['住所１','依頼先','輸出向先']]
        moto_addHauler = pd.merge(moto, allHauler, how= 'left', on='住所１')
        untinForUriage = moto_addHauler[['出荷予定日','得意先コード',
                                         '納入先コード','依頼先','備考',
                                         '出荷予定倉庫','受注ＮＯ','受注行ＮＯ',
                                         '得意先注文ＮＯ','品番','hinban',
                                         'cans','納期', 'toyo_untin', '輸出向先','出荷','add']]

        # 運送屋（依頼先）がNaNの場合はNo dataにする>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

        untinForUriage = untinForUriage.fillna({'依頼先':'NoData'})

        # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<


        closeDate = CloseDate()

        untinForUriage2 = untinForUriage.copy() 
        untinForUriage2[['出荷予定日','納期','曜日','closeDate']] = \
                untinForUriage2.apply(closeDate.get_closeDate, axis=1)

        del closeDate

        # 曜日違いを求める<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

        lead_time = LeadTime()

        untinForUriage2.loc[:,'出荷予定倉庫'] = untinForUriage2.apply(
                lead_time.get_youbi, axis = 1)

        del lead_time
        # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

        zaiko = Zaiko(self.myfolder)
        recorder = Recorder(self.myfolder)

        txt ='売上処理入力用ﾃﾞｰﾀ（本社）' 
        recorder.out_log(txt, '\n')
        recorder.out_file(txt, '\n')

        untinForUriage2['lot'] = untinForUriage2.apply(zaiko.get_lot, axis=1)
        
        recorder.out_log('')
        recorder.out_file('')
        recorder.out_log(untinForUriage2, '\n')
        recorder.out_file(untinForUriage2, '\n')

        del zaiko
        del recorder
        

        return untinForUriage2



    def get_packingCoa(self, packingHinban, untinForUriage):
        lot_data = untinForUriage[['受注ＮＯ', '受注行ＮＯ', 'lot']]
        packingCoa = pd.merge(packingHinban, lot_data, on =['受注ＮＯ', '受注行ＮＯ'] 
                , how = 'left')

        packingCoa = packingCoa[[
            '出荷予定日', '得意先コード', '納入先コード', '納入先名称１', 
            'hinban', '出荷', '受注ＮＯ', '受注行ＮＯ', 'lot'
        ]]

        return packingCoa
