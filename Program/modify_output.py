#! python
# -*- coding: utf-8 -*-


import pandas as pd
import pickle

from uriage_sumi import *


"""
PH_tokeとPH_honsyaをconcatしてから、uriage_sumiをmergeする。
uriage_sumiの結果に合せてから、土気と本社に分ける。
売上入力の修正で出荷工場が変わる事も考えられるから。
"""

class ModifyOutput(object):

    def __init__(self, myfolder, uriagebi, sengetu):

        """
        unsou_dic = {'ﾄｰﾙ':'U0001', '新潟':'U0009' ......}
        これを、key, value をひっくり返す
        dic_unsou = {'U0001':'ﾄｰﾙ', '新潟':'U0009',........}
        """
        
        self.myfolder = myfolder
        self.uriagebi = uriagebi
        self.sengetu = sengetu


        def k_v_change(data_dic):
            change_dic = {} 
            for k, v in data_dic.items():
                change_dic[v] = k
            return change_dic

        with open(r'./data.pickle', 'rb') as f:
            data_loaded = pickle.load(f)
        
        unsou_dic = data_loaded['unsou_dic']
        self.dic_unsou = k_v_change(unsou_dic)

        souko_dic = data_loaded['souko_dic']
        self.dic_souko = k_v_change(souko_dic)



    
    def toke_honsya_concat_sumi(self, toke, honsya):
        """
        PH_toke,PH_honsyaまたはUU_toke,UU_honsyaをconcatして
        uriage_sumiをmergeする
        """
        if len(toke.index)!= 0 and len(honsya.index)!= 0 :
            toke_honsya_concat = pd.concat([toke, honsya])
        elif len(toke.index) != 0 and len(honsya.index) == 0:
            toke_honsya_concat = toke
        elif len(toke.index) == 0 and len(honsya.index) != 0:
            toke_honsya_concat = honsya

        us = UriageSumi(self.myfolder, self.uriagebi, self.sengetu)
        concat_sumi = us.get_output_sumi(toke_honsya_concat)
        del us

        return concat_sumi
        

    def uriageSumi_check_sumi(self, UU_toke, UU_honsya):
        concat_sumi = self.toke_honsya_concat_sumi(UU_toke, UU_honsya)
        us = UriageSumi(self.myfolder, self.uriagebi, self.sengetu)
        us.check_sumi(concat_sumi)
        del us

        



    def modify_kubun(self, haisou, yotei_souko):
        if haisou == 1:
            if '曜日' in yotei_souko:
                yotei_souko.remove('曜日')
            if '土曜配達' in yotei_souko:
                yotei_souko.remove('土曜配達')
            if '営業所' in yotei_souko:
                yotei_souko.remove('営業所')
        if haisou == 4:
            if '曜日' not in yotei_souko:
                yotei_souko.append('曜日')
            if '土曜配達' in yotei_souko:
                yotei_souko.remove('土曜配達')
            if '営業所' in yotei_souko:
                yotei_souko.remove('営業所')
        if haisou == 2:
            if '曜日' in yotei_souko:
                yotei_souko.remove('曜日')
            if '土曜配達' not in a:
                yotei_souko.append('土曜配達')
            if '営業所' in yotei_souko:
                yotei_souko.remove('営業所')
        if haisou ==3:
            if '営業所' not in yotei_souko:
                yotei_souko.append('営業所')
            if '土曜配達' in yotei_souko:
                yotei_souko.remove('土曜配達')
            if '曜日' in yotei_souko:
                yotei_souko.remove('曜日')

        return yotei_souko



    def get_modified_PH(self, PH_toke, PH_honsya):

        def modify_PH(row):
            haisou = row['配送区分']
            yotei_souko = row['出荷予定倉庫']
            cans_x = row['cans_x']
            cans_y = row['cans_y']
            hinban_kanji = row['品番']
            hinban_y = row['hinban_y']
            uriageNo = row['売上ＮＯ']
            irai_x = row['依頼先_x']
            irai_y = row['依頼先_y']
            syukka = row['出荷']
            motosouko = row['出庫元倉庫']
            tokui_code_x = row['得意先コード_x']
            tokui_code_y = row['得意先コード_y']
            nounyuu_code_x = row['納入先コード_x']
            nounyuu_code_y = row['納入先コード_y']
            hinban_x = row['hinban_x']
            jutyuu_suuryou_x = row['受注数量_x']
            jutyuu_suuryou_y = row['受注数量_y']
            jutyuu_tani_x = row['受注単位_x']
            jutyuu_tani_y = row['受注単位_y']
            tokui_no_x = row['得意先注文ＮＯ_x']
            tokui_no_y = row['得意先注文ＮＯ_y']
            bikou_x = row['備考_x']
            bikou_y = row['備考_y']
            nouki_x = row['納期_x']
            nouki_y = row['納期_y']
            closeDate_x = row['closeDate_x']
            closeDate_y = row['closeDate_y']
            dic_lot = row['dic_lot']

            hinban_result = None
            cans_result = 0

            if not pd.isnull(uriageNo):

                yotei_souko = self.modify_kubun(haisou, yotei_souko)

                if pd.isnull(hinban_y):
                    hinban_result = hinban_kanji
                else:
                    hinban_result = hinban_y

                for v in dic_lot.values():
                    cans_result += int(v)

                #  営業持参などで売上入力がnanの場合を考慮する
                if pd.isnull(irai_y):
                    irai_x = 'NoData'
                else:
                    irai_x = self.dic_unsou[irai_y]
                cans_x = cans_result
                tokui_code_x = tokui_code_y
                nounyuu_code_x = nounyuu_code_y
                hinban_x = hinban_result
                jutyuu_suuryou_x = jutyuu_suuryou_y
                jutyuu_tani_x = jutyuu_tani_y
                tokui_no_x = tokui_no_y
                bikou_x = bikou_y
                syukka = self.dic_souko[motosouko]
                nouki_x = nouki_y
                closeDate_x = closeDate_y

                 
              

            return pd.Series([irai_x, cans_x, tokui_code_x, nounyuu_code_x, 
                hinban_x, jutyuu_suuryou_x, jutyuu_tani_x, tokui_no_x, bikou_x, 
                syukka, yotei_souko, nouki_x, closeDate_x])



        PH_concat_sumi = self.toke_honsya_concat_sumi(PH_toke, PH_honsya)


        PH_concat_sumi[['依頼先_x', 'cans_x', '得意先コード_x', 
            '納入先コード_x', 'hinban_x', '受注数量_x', '受注単位_x', 
            '得意先注文ＮＯ_x', '備考_x', '出荷', '出荷予定倉庫', '納期_x', 
            'closeDate_x']] = PH_concat_sumi.apply(modify_PH, axis = 1)

        modified_PH = PH_concat_sumi[['出荷予定日_x', '依頼先_x', 'cans_x', 
            'weight', '得意先コード_x', '納入先コード_x', '納入先名称１', 
            'hinban_x', '品名', '受注数量_x', '受注単位_x', 
            '得意先注文ＮＯ_x', '備考_x', '出荷', '出荷予定倉庫', '輸出向先', 
            '納期_x', '受注ＮＯ', '受注行ＮＯ', 'add', '曜日', 'closeDate_x']]

        modified_PH = modified_PH.rename(columns={'出荷予定日_x':'出荷予定日', 
            '依頼先_x':'依頼先', 'cans_x':'cans', 
           '得意先コード_x':'得意先コード', '納入先コード_x':'納入先コード', 
            'hinban_x':'hinban', '受注数量_x':'受注数量', 
            '受注単位_x':'受注単位', '得意先注文ＮＯ_x':'得意先注文ＮＯ', 
            '備考_x':'備考', '納期_x':'納期', 'closeDate_x':'closeDate'})


        return modified_PH

    

    def get_modified_UU(self, UU_toke, UU_honsya):
        
        def modify_UU(row):
            tokui_code_x = row['得意先コード_x']
            tokui_code_y = row['得意先コード_y']
            nounyuu_code_x = row['納入先コード_x']
            nounyuu_code_y = row['納入先コード_y']
            irai_x = row['依頼先_x']
            irai_y = row['依頼先_y']
            bikou_x = row['備考_x']
            bikou_y = row['備考_y']
            tokui_no_x = row['得意先注文ＮＯ_x']
            tokui_no_y = row['得意先注文ＮＯ_y']
            hinban_kanji_x = row['品番_x']
            hinban_kanji_y = row['品番_y']
            jutyuu_suuryou_x = row['受注数量_x']
            jutyuu_suuryou_y = row['受注数量_y']
            hinban_x = row['hinban_x']
            hinban_y = row['hinban_y']
            cans_x = row['cans_x']
            cans_y = row['cans_y']
            nouki_x = row['納期_x']
            nouki_y = row['納期_y']
            syukka = row['出荷']
            motosouko = row['出庫元倉庫']
            closeDate_x = row['closeDate_x']
            closeDate_y = row['closeDate_y']
            lot_x = row['lot_x']
            dic_lot = row['dic_lot']
            yotei_souko = row['出荷予定倉庫']
            haisou = row['配送区分']
            uriageNo = row['売上ＮＯ']

            hinban_result = None
            cans_result = 0

            if not pd.isnull(uriageNo):

                yotei_souko = self.modify_kubun(haisou, yotei_souko)

                if pd.isnull(hinban_y):
                    hinban_result = hinban_kanji_y
                else:
                    hinban_result = hinban_y

                for v in dic_lot.values():
                    cans_result += int(v)

                tokui_code_x = tokui_code_y
                nounyuu_code_x = nounyuu_code_y

                #  営業持参などで売上入力がnanの場合を考慮する
                if pd.isnull(irai_y):
                    irai_x = 'NoData'
                else:
                    irai_x = self.dic_unsou[irai_y]

                bikou_x = bikou_y
                tokui_no_x = tokui_no_y
                hinban_kanji_x = hinban_kanji_y
                jutyuu_suuryou_x = jutyuu_suuryou_y
                hinban_x = hinban_result
                cans_x = cans_result
                nouki_x = nouki_y
                syukka = self.dic_souko[motosouko]
                closeDate_x = closeDate_y
                lot_x = dic_lot

            
            return pd.Series([tokui_code_x, nounyuu_code_x, irai_x, bikou_x,
                tokui_no_x, hinban_kanji_x, jutyuu_suuryou_x, hinban_x, cans_x,
                nouki_x, syukka, closeDate_x, lot_x, yotei_souko])


        UU_concat_sumi = self.toke_honsya_concat_sumi(UU_toke, UU_honsya)

        UU_concat_sumi[['得意先コード_x','納入先コード_x','依頼先_x', '備考_x',
            '得意先注文ＮＯ_x', '品番_x', '受注数量_x', 'hinban_x', 'cans_x',
            '納期_x', '出荷', 'closeDate_x', 'lot_x', '出荷予定倉庫'
            ]] = UU_concat_sumi.apply(modify_UU, axis = 1)

        modified_UU = UU_concat_sumi[['出荷予定日_x', '得意先コード_x',
            '納入先コード_x','依頼先_x', '備考_x', '受注ＮＯ', '受注行ＮＯ',
            '得意先注文ＮＯ_x', '品番_x', '受注数量_x', 'hinban_x', 'cans_x',
            '納期_x', 'toyo_untin', '輸出向先', '出荷', 'add', 'sumi',  '曜日',
            'closeDate_x', 'lot_x', '出荷予定倉庫'
            ]]

        modified_UU = modified_UU.rename(
            columns={
                '出荷予定日_x':'出荷予定日', '得意先コード_x':'得意先コード', 
                '納入先コード_x':'納入先コード','依頼先_x':'依頼先', 
                '備考_x':'備考', '得意先注文ＮＯ_x':'得意先注文ＮＯ', 
                '品番_x':'品番', '受注数量_x':'受注数量', 'hinban_x':'hinban', 
                'cans_x':'cans','納期_x':'納期','closeDate_x':'closeDate', 
                'lot_x':'lot'
            }
        )


        return modified_UU

        

