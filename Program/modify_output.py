#! python
# -*- coding: utf-8 -*-


import pandas as pd
import pickle

"""
PH_tokeとPH_honsyaをconcatしてから、uriage_sumiをmergeする。
uriage_sumiの結果に合せてから、土気と本社に分ける。
売上入力の修正で出荷工場が変わる事も考えられるから。
"""

class ModifyOutput(object):

    def __init__(self):

        """
        unsou_dic = {'ﾄｰﾙ':'U0001', '新潟':'U0009' ......}
        これを、key, value をひっくり返す
        dic_unsou = {'U0001':'ﾄｰﾙ', '新潟':'U0009',........}
        """

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




    def modify_PH(self, PH_concat_sumi):

        def modify_kubun(row):
            haisou = row['配送区分']
            yotei_souko = row['出荷予定倉庫']
            cans = row['cans_y']
            cans_x = row['cans_x']
            hinban = row['品番']
            hinban_furikae = row['hinban_y']
            jutyuu_suuryou = row['受注数量_y']
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

            hinban_result = None
            cans_result = None

            if not pd.isnull(uriageNo):

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

                if pd.isnull(hinban_furikae):
                    hinban_result = hinban
                    cans_result = jutyuu_suuryou
                else:
                    hinban_result = hinban_furikae
                    cans_result = cans

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


        # 運送屋のmodify
        # PH_concat_sumi['依頼先_x'] = PH_concat_sumi['依頼先_y'].map(
                                                                # self.dic_unsou)
        # 出荷倉庫のmodify
        # PH_concat_sumi['出荷'] = PH_concat_sumi['出庫元倉庫'].map(
                                                                # self.dic_souko)
        # 出荷予定倉庫のmodify(list)
        PH_concat_sumi[['依頼先_x', 'cans_x', '得意先コード_x', 
            '納入先コード_x', 'hinban_x', '受注数量_x', '受注単位_x', 
            '得意先注文ＮＯ_x', '備考_x', '出荷', '出荷予定倉庫', '納期_x', 
            'closeDate_x']] = PH_concat_sumi.apply(modify_kubun, axis = 1)

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

        
        """
        remake_PH = remake_PH.drop(columns = '依頼先_y')

        remake_PH = remake_PH.rename(columns = {'依頼先_x':'依頼先'})

        return remake_PH



        """
