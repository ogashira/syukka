#! python
# -*- coding: cp932 -*-
import csv
import pandas as pd



class Unsoutaiou_toke :
    
    # [事業所ｺｰﾄﾞ,相手先ｺｰﾄﾞ,相手先名称1,郵便番号 ,郵便番号2,住所1,ﾄｰﾙ距離,ﾄ?
    #  ﾄｰﾙ行く行かない,新潟距離,新潟中継回数,新潟行く行かない,ｹｲﾋﾝ,顧客指定運送屋
    #  ,輸出向け先,得意先ｺｰﾄﾞ,納入先ｺｰﾄﾞ]
    
    def __init__(self):
        # dl_df = pd.read_csv(
        # r'\\192.168.1.247\共有\経理課ﾌｫﾙﾀﾞ\運賃計算関係\unsoutaiou_toke.csv', 
        # encoding='cp932'
        # )
        dl_df = pd.read_csv(
                r'../master/untin/unsoutaiou_toke.csv',encoding='cp932'
        )


        self.unsoutaiou = dl_df.rename(columns={'相手先名称１':'納入先名称１'})

    def add_unsoutaiou(self, df):
        dup_unsoutaiou = self.unsoutaiou.drop_duplicates(['納入先名称１'])
        add_unsoutaiou = pd.merge(df,dup_unsoutaiou, on='納入先名称１'
                                  , how='left')
        return add_unsoutaiou
        
                

    




class Unsoutaiou_honsya :
    

    # [事業所ｺｰﾄﾞ,相手先ｺｰﾄﾞ,相手先名称1,郵便番号 ,郵便番号2,住所1,ﾄｰﾙ距
    #  ﾄｰﾙ行く行かない,新潟距離,新潟中継回数,新潟行く行かない,ｹｲﾋﾝ,顧客指定運送屋,
    #  輸出向け先,得意先ｺｰﾄﾞ,納入先ｺｰﾄﾞ,久留米距離] 土気には久留米距離がない。

    def __init__(self):
        # dl_df = pd.read_csv(
        # r'\\192.168.1.247\共有\経理課ﾌｫﾙﾀﾞ\運賃計算関係\unsoutaiou_honsya.csv', 
        # encoding='cp932'
        # )

        dl_df = pd.read_csv(
                r'../master/untin/unsoutaiou_honsya.csv',encoding='cp932'
        )

        self.unsoutaiou = dl_df.rename(columns={'相手先名称１':'納入先名称１'})

    def add_unsoutaiou(self, df):
        dup_unsoutaiou = self.unsoutaiou.drop_duplicates(['納入先名称１'])
        add_unsoutaiou = pd.merge(df, dup_unsoutaiou, on='納入先名称１'
                                  , how='left')
        return add_unsoutaiou
