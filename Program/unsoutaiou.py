#! python
# -*- coding: utf-8 -*-
import csv
import pandas as pd
import os
import platform



class Unsoutaiou_toke :
    
    # [事業所ｺｰﾄﾞ,相手先ｺｰﾄﾞ,相手先名称1,郵便番号 ,郵便番号2,住所1,ﾄｰﾙ距離,ﾄ?
    #  ﾄｰﾙ行く行かない,新潟距離,新潟中継回数,新潟行く行かない,ｹｲﾋﾝ,顧客指定運送屋
    #  ,輸出向け先,得意先ｺｰﾄﾞ,納入先ｺｰﾄﾞ]
    
    def __init__(self):
        pf = platform.system()
        if pf == 'Windows':
            mypath = (r'//192.168.1.247/共有/経理課ﾌｫﾙﾀﾞ/運賃計算関係/unsoutaiou_toke.csv')
        elif pf == 'Linux':
            mypath = (r'/mnt/public/経理課ﾌｫﾙﾀﾞ/運賃計算関係/unsoutaiou_toke.csv')
        else:
            mypath = r'../master/untin/unsoutaiou_toke.csv'
    

        dl_df = pd.read_csv(mypath, encoding='cp932')


        self.unsoutaiou = dl_df.rename(
                columns={'相手先名称１':'納入先名称１','ｹｲﾋﾝ':'ｹｲﾋﾝ向'}
        )




        # 2021/2/16 納入先コードが全てNaNだとエラーになる？だからfillnaした
        self.unsoutaiou = self.unsoutaiou.fillna({'納入先コード': ''})

    def add_unsoutaiou(self, df):
        dup_unsoutaiou = self.unsoutaiou.drop_duplicates(['住所１'])

        add_unsoutaiou = pd.merge(
                df,dup_unsoutaiou, on='住所１', 
                how='left'
        )

        return add_unsoutaiou

    
    def add_address(self, df):
        """
        unsoutaiou = self.unsoutaiou[[
            '得意先コード','納入先コード','納入先名称１','住所１']]    

        dup_unsoutaiou = unsoutaiou.drop_duplicates(['得意先コード',
                                                '納入先コード','納入先名称１'])
        add_address = pd.merge(
                df, dup_unsoutaiou, 
                on=['得意先コード','納入先コード','納入先名称１'],
                how = 'left'
        )
        """

        unsoutaiou = self.unsoutaiou[[
            '相手先コード１', '納入先名称１','住所１','納入先コード']]    

        unsoutaiou = unsoutaiou.rename(
                columns={'相手先コード１':'得意先コード'}
        )

        dup_unsoutaiou = unsoutaiou.drop_duplicates(['得意先コード',
                                                '納入先名称１','納入先コード'])
        add_address = pd.merge(
                df, dup_unsoutaiou, 
                on=['得意先コード','納入先名称１','納入先コード'],
                how = 'left'
        )

        return add_address
    
        
                

    




class Unsoutaiou_honsya :
    

    # [事業所ｺｰﾄﾞ,相手先ｺｰﾄﾞ,相手先名称1,郵便番号 ,郵便番号2,住所1,ﾄｰﾙ距
    #  ﾄｰﾙ行く行かない,新潟距離,新潟中継回数,新潟行く行かない,ｹｲﾋﾝ,顧客指定運送屋,
    #  輸出向け先,得意先ｺｰﾄﾞ,納入先ｺｰﾄﾞ,久留米距離] 土気には久留米距離がない。

    def __init__(self):
        pf = platform.system()
        if pf == 'Windows':
            mypath = (r'//192.168.1.247/共有/経理課ﾌｫﾙﾀﾞ/運賃計算関係/unsoutaiou_honsya.csv')
        elif pf == 'Linux':
            mypath = (r'/mnt/public/経理課ﾌｫﾙﾀﾞ/運賃計算関係/unsoutaiou_honsya.csv')
        else:
            mypath = r'../master/untin/unsoutaiou_honsya.csv'
    

        dl_df = pd.read_csv(mypath, encoding='cp932')

        self.unsoutaiou = dl_df.rename(
                columns={'相手先名称１':'納入先名称１','ｹｲﾋﾝ':'ｹｲﾋﾝ向'}
        )

        # 2021/2/16 納入先コードが全てNaNだとエラーになる？だからfillnaした
        self.unsoutaiou = self.unsoutaiou.fillna({'納入先コード': ''})

    def add_unsoutaiou(self, df):
        dup_unsoutaiou = self.unsoutaiou.drop_duplicates(['住所１'])
        add_unsoutaiou = pd.merge(
                df, dup_unsoutaiou, on='住所１',
                how='left'
        )
        return add_unsoutaiou



    def add_address(self, df):
        """
        unsoutaiou = self.unsoutaiou[[
            '得意先コード','納入先コード','納入先名称１','住所１']]    
        dup_unsoutaiou = unsoutaiou.drop_duplicates(['得意先コード',
                                                '納入先コード','納入先名称１'])
        add_address = pd.merge(
                df, dup_unsoutaiou, 
                on=['得意先コード','納入先コード','納入先名称１'],
                how = 'left'
        )
        """
        
        unsoutaiou = self.unsoutaiou[[
            '相手先コード１', '納入先名称１','住所１','納入先コード']]    

        unsoutaiou = unsoutaiou.rename(
                columns={'相手先コード１':'得意先コード'}
        )

        dup_unsoutaiou = unsoutaiou.drop_duplicates(['得意先コード',
                                                '納入先名称１','納入先コード'])
        add_address = pd.merge(
                df, dup_unsoutaiou, 
                on=['得意先コード','納入先名称１','納入先コード'],
                how = 'left'
                )

        return add_address










