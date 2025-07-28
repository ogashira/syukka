#! python
# -*- coding: utf-8 -*-

import jaconv
import csv
import pandas as pd
import numpy as np
import re
import sys
import os
import platform
from unsoutaiou import *
from untin_toke import *
from untin_honsya import *
from toyo_untin import *
from untin_keisan_sheet import *
from sql_query import *




class Packing :
	
    def __init__(self, uriagebi, sengetu):
        pf = platform.system()
        if pf == 'Windows':
            mypath = (r'//192.168.1.247/共有/技術課ﾌｫﾙﾀﾞ/200. effit_data/ﾏｽﾀ/'\
                      r'hinban.csv') 
        elif pf == 'Linux':
            mypath = (r'/mnt/public/技術課ﾌｫﾙﾀﾞ/200. effit_data/ﾏｽﾀ/hinban.csv')
        else:
            mypath = r'../master/hinban.csv'

        hinban_file = open(mypath, encoding='cp932')

        file_reader = csv.reader(hinban_file)
        header = next(file_reader)
        hinban = list(file_reader)
        hinban_file.close()
        
        #self.tanjuu = [品番、品名、単重]
        self.tanjuu = []
        for line in hinban:
        	lines = [ line[0], line[7], line[41] ]
        	self.tanjuu.append(lines)
        
        #運賃計算ｼｰﾄ_改の元ｼｰﾄ

        if pf == 'Windows' or pf == 'Linux':
            sql = SqlQuery(uriagebi, sengetu)
            self.untin_moto = sql.get_untin_keisan_sheet()
            self.untin_moto = self.untin_moto.apply(
                    lambda col: col.map(lambda x : np.nan if x == ' ' else x))
            # self.untin_moto['備考.1'] = self.untin_moto['備考.1'].map(
                                                             # lambda x : float(x))
            # self.untin_moto = pd.read_csv(r'../master/effitA/運賃計算ｼｰﾄ_改.csv',
                                                     # encoding='cp932',skiprows=1)
        else:
            self.untin_moto = pd.read_csv(r'../master/effitA/運賃計算ｼｰﾄ_改.csv',
                                                    encoding='cp932',skiprows=1)
        if self.untin_moto.shape[0] == 0 :
            print('運賃計算ｼｰﾄ_改.csv にﾃﾞｰﾀがありません。終了します。')
            sys.exit()
        
        

        # 2021/2/16納入先コードが全てNANになるとなぜかエラーになる
        # unsoutaiou.add_addressでエラーになる？　理由はわからないが
        # fillna で対策した。unsoutaiou_toke,honsyaでも同様にfillnaした
        self.untin_moto = self.untin_moto.fillna({'納入先コード': ''})


        self.untin_moto = self.untin_moto.fillna({'備考':'noData'})
        self.untin_moto = self.untin_moto.sort_values(by=['得意先コード', 
                                                          '納入先名称１'])
        
        
        #ｱﾄﾛﾝﾍﾟｰﾙ缶使用の品番（缶の重さ3kg）
        AT_file = open(r'../master/selfMade/AT_un_pl.csv', encoding='cp932')
        file_reader = csv.reader(AT_file)

        self.AT_un_pl = []
        for row in file_reader: #一次元ﾘｽﾄにするため
            self.AT_un_pl.append(''.join(row))

        AT_file.close()
            
        #文字列中の-1-を-に、文字列最後の-1を削除する。
        def change_hinban(hinban):
            chg_hinban = re.sub('-1-','-',hinban)
            chg_hinban = re.sub('-1$','',chg_hinban)
            return chg_hinban
            
        
        #単位がCNの品番の-EX-THIを-EXにする
        def change_hinban_mukesaki(hinban):
            chg_hinban = re.sub('-EX-.*$','-EX', hinban)
            return chg_hinban

        
        # In[43]:
        
        
        #ﾘｽﾄtanjuuを使って、品番から入れ目を求める
        def get_ireme(hinban):
            ireme = 0
            for line in self.tanjuu:
                if line[0] == hinban :
                    ireme = float(line[2])/ 1000
                    break
            return ireme
        
        
        #品名を小文字、半角にしてから(15KG)の　15を取り出し 　'ireme2'とする。
        def get_ireme2(hinmei):
            # 大文字を小文字に変換
            hinmei = hinmei.lower() 
            #全角を半角にする(数字も記号も)
            hinmei = jaconv.z2h(hinmei,digit=True,ascii=True) 
            
            result = re.search(r'(\d+\.?\d*kg)', hinmei) 
            if result:
                hinmei2 = result.group()
                result2 = re.search(r'(\d+\.?\d*)', hinmei2)
                hinmei3 = result2.group()
                hinmei3 = float(hinmei3)
            else:
                hinmei3 = None
            
            return hinmei3
        

        
        #un_ATは3kg,200g(ｶﾞﾗｽ瓶)は0.3kg、1kg以下は0.2kg,
        #6kg以下は0.5kg, -R-EXは1kg, 品番中に-EX-,最後に-EX は２kg
        #それ以外は1kg
        def get_can_weight (row):
            ireme = row['ireme']
            hinban = row['hinban']
            if hinban in self.AT_un_pl:
                can_weight = 3
            elif ireme == 0.2 :
                can_weight = 0.3
            elif ireme <= 1.0 :
                can_weight = 0.2
            elif 1.0 < ireme < 6:
                can_weight = 0.5
            elif re.search('-R-EX', str(hinban)):
                can_weight = 1
            elif re.search('-EX$|-EX-', str(hinban)):
                can_weight = 2
            else: can_weight = 1
            
            return can_weight

        
        #大阪顧客は削除する
        self.moto_h = self.untin_moto.loc[self.untin_moto['得意先コード'] 
                <= 'T6000',:] 
        if self.moto_h.shape[0] == 0 :
            print('本社・土気出荷がありません。終了します。')
            sys.exit()

        # 東新油脂は削除する
        moto_h01 = self.moto_h.loc[self.moto_h['得意先コード'] != 'T0011', :]
        moto_h01 =  moto_h01.reset_index(drop=True)
        if moto_h01.shape[0] == 0 :
            print('本社・土気出荷がありません。終了します。')
            sys.exit()
        
        moto_h = moto_h01.copy()

        # UntinKeisanSheetに渡して、sheet_add_cntにする>>>>>>>>>>>>>>>>>>>>>>
        UKS = UntinKeisanSheet(moto_h, uriagebi, sengetu)
        moto_h = UKS.sheet_add_cnt()

        # 更に、sheet_add_sumi に渡して、入力済を識別する
        moto_h2 = UKS.sheet_add_sumi(moto_h)

        del UKS
        #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<



        moto_honsya = moto_h2.copy()
        #単位KGの場合、-1- →- , -1(最後)→消す
        moto_honsya.loc[moto_honsya['受注単位']=='KG','hinban'] = \
                moto_honsya['品番'].map(change_hinban)
        moto_honsya.loc[moto_honsya['受注単位']=='CN','hinban'] = \
                moto_honsya['品番'].map(change_hinban_mukesaki)
        
        moto_honsya.loc[:,'ireme']= moto_honsya['hinban'].map(get_ireme)
        
        #999998など入れ目が0の場合は、品名から入れ目を求める
        moto_honsya.loc[moto_honsya['ireme']==0, 'ireme'] \
            = moto_honsya['品名'].map(get_ireme2)



        moto_honsya.loc[moto_honsya['受注単位']== 'KG','cans'] \
                = moto_honsya['受注数量']/ moto_honsya['ireme']
        moto_honsya.loc[moto_honsya['受注単位']== 'CN','cans'] \
                = moto_honsya['受注数量']
        moto_honsya.loc[moto_honsya['受注単位']== 'BI','cans'] \
                = moto_honsya['受注数量']
        #applyでdataframごと関数に渡す。関数の中で複数列を評価する。
        moto_honsya['can_weight'] = moto_honsya.apply(get_can_weight,axis=1)
        
        #重量を求める
        moto_honsya['weight'] = (moto_honsya['ireme'] \
                + moto_honsya['can_weight']) * moto_honsya['cans']
        
        #備考から、納期8/3　の部分だけを抜き出す
        #moto_honsya['納期'] = moto_honsya.loc[:,'備考'].str.extract \
                #(r'([1-9][0-2]?/[1-9][0-9]?)')


        #備考から、本社出荷、を抜き出す
        moto_honsya['出荷'] = moto_honsya.loc[:,'備考'].str.extract \
                (r'(本社出荷)')

        

        
        moto_honsya = moto_honsya.fillna({'出荷':''})
        # この時点で出荷の列に入っているデータは、本社出荷、空白文字



        moto_honsya= moto_honsya.rename(columns= {'備考.1':'受注時運賃n缶'})


        # 出荷予定倉庫の列を[]にする。このやり方でないとうまくいかなかった。
        moto_honsya['出荷予定倉庫'] = moto_honsya.apply(lambda x: [], axis=1) 
        
        #東洋運賃を計算追加する
        toyo_untin = Toyo_untin(moto_honsya)
        moto_honsya = toyo_untin.get_toyoUntin()
        del toyo_untin

        # 土気出荷、空白はtoke_motoに　本社出荷、大阪直送はhonsya_motoに分ける 
        self.toke_moto = moto_honsya[moto_honsya['出荷'] == '']
        self.honsya_moto = moto_honsya[moto_honsya['出荷'] == '本社出荷']


        self.moto_honsya = moto_honsya.copy()
        #moto_honsyaは大阪顧客を除いた本社、土気出荷分の元データ


    def get_NoCalc(self, row):
        bikou = row['備考']
        add1 = row['住所１']
        if '営業持参' in bikou or '大阪直送' in bikou:
            return 'NoCalc'
        else:
            return add1


    def get_honsya_moto(self):
        """
        honsya_moto = self.moto_honsya[self.moto_honsya['備考'].str.match \
                (r'^.*(本社出荷|大阪直送).*$',na=True)]
        honsya_moto = honsya_moto.fillna({'出荷':''})
        """
        honsya_moto = self.honsya_moto.copy() 
        honsya_moto['出荷'] = '本社出荷' # 全て本社出荷にする

        unsoutaiou_honsya = Unsoutaiou_honsya()
        honsyaMoto = unsoutaiou_honsya.add_address(honsya_moto)
        del unsoutaiou_honsya

        #大阪直送、営業持参の場合は運賃計算しないように「住所１」を
        #「NoCalc」に変更しておく
        # honsyaMoto.loc[honsyaMoto['備考'] =='営業持参','住所１'] = 'NoCalc'
        if not honsyaMoto.empty:
            honsyaMoto['住所１'] = honsyaMoto.apply(self.get_NoCalc, axis=1)

        return honsyaMoto


    def get_toke_moto(self):
        """
        toke_moto = self.moto_honsya[self.moto_honsya['備考'].str.match\
                (r'^(?!.*本社出荷).*$', na=True)]
        toke_moto = toke_moto.fillna({'出荷':''})
        toke_moto['出荷'] = toke_moto['出荷'].map(lambda x : '土気出荷' 
                                                      if x == ''  else x ) 
        """
        
        toke_moto = self.toke_moto.copy() 
        toke_moto['出荷'] = '土気出荷' # 全て土気出荷にする。


        unsoutaiou_toke = Unsoutaiou_toke()
        tokeMoto = unsoutaiou_toke.add_address(toke_moto)
        del unsoutaiou_toke



        #大阪直送、営業持参の場合は運賃計算しないように「住所１」を
        #「NoCalc」に変更しておく
        # tokeMoto.loc[tokeMoto['出荷'] =='営業持参','住所１'] = 'NoCalc'
        if not tokeMoto.empty:
            tokeMoto['住所１'] = tokeMoto.apply(self.get_NoCalc, axis=1)


        return tokeMoto


    def get_untin_toke(self):
        toke_moto = self.get_toke_moto()
        

        if toke_moto.shape[0] == 0: 
            pass
        else:

            tokeMoto_gr = toke_moto.groupby('住所１',as_index=False) \
                    [['weight', 'cans']].sum()


            '''
            toke_moto_dup = toke_moto.drop_duplicates(['住所１']) 
            tokeMoto_gr = pd.merge(
                    tokeMoto_gr, toke_moto_dup, on='住所１', how='left'
            )
            '''

            '''
            20240226 bug  修正
            出荷の全てがサンプル999998で顧客の情報がない T0000の場合、住所１の情報が
            一つもない場合は、tokeMoto_grのdataFrameがemptyになってしまいエラーになってしまう
            (tokeMoto_add_unsoutaiou = unsoutaiou_toke.add_unsoutaiou(tokeMoto_gr)
            でエラーになるので、tokeMoto_grがemptyの時は空のデータフレームを作成するように
            修正した。
            '''
            if tokeMoto_gr.shape[0] == 0:
                tokeMoto_gr = pd.DataFrame(columns=['住所１', 'weight', 'cans'], index = [0])


            
            unsoutaiou_toke = Unsoutaiou_toke()
            tokeMoto_add_unsoutaiou = unsoutaiou_toke.add_unsoutaiou(tokeMoto_gr)

            
            del unsoutaiou_toke

            untin_toke = Untin_toke()
            #applyでdfごと指定すれば、各行ごと関数に渡せる。複数の戻り値は、
            #Seriesにして返す。関数はUnsou_tokeｸﾗｽのget_untinﾒｿｯﾄﾞ。
            tokeMoto_add_unsoutaiou[['ﾄｰﾙ','新潟','ｹｲﾋﾝ','西濃']] =  \
                    tokeMoto_add_unsoutaiou.apply(untin_toke.get_untin, axis=1)


            del untin_toke
        
        
        return tokeMoto_add_unsoutaiou

		

    def get_untin_honsya(self):
        honsya_moto = self.get_honsya_moto()

        
        if honsya_moto.shape[0] == 0:
            pass
        else:
            honsyaMoto_gr = honsya_moto.groupby('住所１',as_index=False) \
                    [['weight','cans']].sum()
            
            #honsya_motoが持っている「得意先コード」、「納入先コード」をくっつける
            # honsya_moto_code = honsya_moto[['納入先名称１','得意先コード',
                                            #'納入先コード']]
            #ダブりを無くしておく必須
            # honsya_moto_code = honsya_moto_code.drop_duplicates(['納入先名称１']) 
            # honsyaMoto = pd.merge(honsyaMoto, honsya_moto_code, how='left', 
                                  # on='納入先名称１')


            '''
            20240226 bug  修正
            出荷の全てがサンプル999998で顧客の情報がない T0000の場合、住所１の情報が
            一つもない場合は、honsyaMoto_grのdataFrameがemptyになってしまいエラーになってしまう
            (honsyaMoto_add_unsoutaiou = unsoutaiou_honsya.add_unsoutaiou(honsyaMoto_gr)
            でエラーになるので、honsyaMoto_grがemptyの時は空のデータフレームを作成するように
            修正した。
            '''
            if honsyaMoto_gr.shape[0] == 0:
                honsyaMoto_gr = pd.DataFrame(columns=['住所１', 'weight', 'cans'], index = [0])



            
            unsoutaiou_honsya = Unsoutaiou_honsya()
            honsyaMoto_add_unsoutaiou = unsoutaiou_honsya.add_unsoutaiou(honsyaMoto_gr)



            del unsoutaiou_honsya

            untin_honsya = Untin_honsya()
            #applyでdfごと指定すれば、各行ごと関数に渡せる。複数の戻り値は、
            #Seriesにして返す。関数はUnsou_tokeｸﾗｽのget_untinﾒｿｯﾄﾞ。
            honsyaMoto_add_unsoutaiou[['ﾄｰﾙ','新潟','ｹｲﾋﾝ']] \
                    = honsyaMoto_add_unsoutaiou.apply(untin_honsya.get_untin, axis=1)


            del untin_honsya

        return honsyaMoto_add_unsoutaiou

