#! python
# -*- coding: utf-8 -*-

import csv
import pandas as pd
import numpy as np
#from unsoutaiou import *


class Untin_toke :

    def __init__ (self):
        #self.weight = weight
        #self.deli_name = deli_name

        unsou_file = open(r'//192.168.1.247/共有/技術課ﾌｫﾙﾀﾞ/200. effit_data/ﾏｽﾀ/運賃計算関係/untin/torr_toke.csv' ,encoding='cp932')
        file_reader = csv.reader(unsou_file)
        self.torr: list[list[str]] = list(file_reader)
        unsou_file.close()
        
        unsou_file = open(r'//192.168.1.247/共有/技術課ﾌｫﾙﾀﾞ/200. effit_data/ﾏｽﾀ/運賃計算関係/untin/torr_toke_nara_hirosima.csv' ,encoding='cp932')
        file_reader = csv.reader(unsou_file)
        self.torr_nara_hirosima: list[list[str]] = list(file_reader)
        unsou_file.close()
        
        unsou_file = open(r'//192.168.1.247/共有/技術課ﾌｫﾙﾀﾞ/200. effit_data/ﾏｽﾀ/運賃計算関係/untin/torr_tyuukei_toke.csv' ,encoding='cp932')
        file_reader = csv.reader(unsou_file)
        self.torr_tyuukei: list[list[str]]= list(file_reader)
        unsou_file.close()

        unsou_file = open(r'//192.168.1.247/共有/技術課ﾌｫﾙﾀﾞ/200. effit_data/ﾏｽﾀ/運賃計算関係/untin/torr_surcharge_toke.csv' ,encoding='cp932')
        file_reader = csv.reader(unsou_file)
        self.torr_surcharge: list[list[str]]= list(file_reader)
        unsou_file.close()

        unsou_file = open(r'//192.168.1.247/共有/技術課ﾌｫﾙﾀﾞ/200. effit_data/ﾏｽﾀ/運賃計算関係/untin/keihin_toke.csv' ,encoding='cp932')
        file_reader = csv.reader(unsou_file)
        self.keihin: list[list[str]]= list(file_reader)
        unsou_file.close()

        unsou_file = open(r'//192.168.1.247/共有/技術課ﾌｫﾙﾀﾞ/200. effit_data/ﾏｽﾀ/運賃計算関係/untin/niigata_toke.csv' ,encoding='cp932')
        file_reader = csv.reader(unsou_file)
        self.niigata: list[list[str]]= list(file_reader)
        unsou_file.close()

        unsou_file = open(r'//192.168.1.247/共有/技術課ﾌｫﾙﾀﾞ/200. effit_data/ﾏｽﾀ/運賃計算関係/untin/niigata_tyuukei_toke.csv' ,encoding='cp932')
        file_reader = csv.reader(unsou_file)
        self.niigata_tyuukei: list[list[str]]= list(file_reader)
        unsou_file.close()

        unsou_file = open(r'//192.168.1.247/共有/技術課ﾌｫﾙﾀﾞ/200. effit_data/ﾏｽﾀ/運賃計算関係/untin/niigata_surcharge_toke.csv' ,encoding='cp932')
        file_reader = csv.reader(unsou_file)
        self.niigata_surcharge: list[list[str]]= list(file_reader)
        unsou_file.close()

        unsou_file = open(r'//192.168.1.247/共有/技術課ﾌｫﾙﾀﾞ/200. effit_data/ﾏｽﾀ/運賃計算関係/untin/seinou_toke.csv' ,encoding='cp932')
        file_reader = csv.reader(unsou_file)
        self.seinou: list[list[str]]= list(file_reader)
        unsou_file.close()

        unsou_file = open(r'//192.168.1.247/共有/技術課ﾌｫﾙﾀﾞ/200. effit_data/ﾏｽﾀ/運賃計算関係/untin/seinou_surcharge_toke.csv' ,encoding='cp932')
        file_reader = csv.reader(unsou_file)
        self.seinou_surcharge: list[list[str]]= list(file_reader)
        unsou_file.close()


    def get_torr(self, dist: int, weight: float, YN: str, address: str, tyuukei: int)-> float:
		
        HOKEN_FARE: float = 100.0

		#縺ｩ縺｡繧峨表を使うか？
        if '広島県' in address or '奈良県' in address:
            untin_mtx = self.torr_nara_hirosima
        else:
            untin_mtx = self.torr
        
    
        #トールの運賃を求める
        if YN == '-':
            return float('inf')
        
        #基本料金std_fareを求める
        dist_idx: int = 0
        weight_idx: int = 0
        for i  in range(len(untin_mtx[0])-1,0,-1): 
            if float(untin_mtx[0][i].replace(',', '')) >= dist : 
                dist_idx = i
                break
        for i  in range(len(untin_mtx)-1,0,-1): 
            if float(untin_mtx[i][0].replace(',', '')) >= weight : 
                weight_idx = i
                break
        std_fare = float('inf')
        if dist_idx!= 0 and weight_idx!= 0:
            std_fare = float(untin_mtx[weight_idx][dist_idx].replace(',', ''))
        
        #surcharge surcharge_fareを求める
        dist_idx: int = 0
        weight_idx: int = 0
        for i  in range(len(self.torr_surcharge[0])-1,0,-1): 
            if float(self.torr_surcharge[0][i].replace(',', '')) >= dist : 
                dist_idx = i
                break
        for i  in range(len(self.torr_surcharge)-1,0,-1): 
            if float(self.torr_surcharge[i][0].replace(',', '')) >= weight : 
                weight_idx = i
                break
        surcharge_fare: float = float('inf')
        if dist_idx!= 0 and weight_idx!= 0:
            surcharge_fare = float(self.torr_surcharge[weight_idx][dist_idx].replace(',', ''))

        #中継料金を求める
        tyuukei_fare: float= 0.0
        for i in range(len(self.torr_tyuukei)-1,0,-1):
            if float(self.torr_tyuukei[i][0]) >=weight :
                tyuukei_fare = float(self.torr_tyuukei[i][1].replace(',', '')) * float(tyuukei)
                break

        

        return std_fare + tyuukei_fare + surcharge_fare + HOKEN_FARE



    def get_niigata(self, dist, weight, YN, tyuukei) :

        if YN == '-':
            return float('inf')

        #基本料金std_fareを求める
        dist_idx: int = 0
        weight_idx: int = 0
        for i  in range(len(self.niigata[0])-1,0,-1): 
            if float(self.niigata[0][i].replace(',', '')) >= dist : 
                dist_idx = i
                break
        for i  in range(len(self.niigata)-1,0,-1): 
            if float(self.niigata[i][0].replace(',', '')) >= weight : 
                weight_idx = i
                break
        std_fare = float('inf')
        if dist_idx!= 0 and weight_idx!= 0:
            std_fare = float(self.niigata[weight_idx][dist_idx].replace(',', ''))

        # サーチャージを求める
        dist_idx: int = 0
        weight_idx: int = 0
        for i  in range(len(self.niigata_surcharge[0])-1,0,-1): 
            if float(self.niigata_surcharge[0][i].replace(',', '')) >= dist : 
                dist_idx = i
                break
        for i  in range(len(self.niigata_surcharge)-1,0,-1): 
            if float(self.niigata_surcharge[i][0].replace(',', '')) >= weight : 
                weight_idx = i
                break
        surcharge_fare = float('inf')
        if dist_idx!= 0 and weight_idx!= 0:
            surcharge_fare = float(self.niigata_surcharge[weight_idx][dist_idx].replace(',', ''))
       
        #中継料金を求める
        tyuukei_fare: float= 0.0
        for i in range(len(self.niigata_tyuukei)-1,0,-1):
            if float(self.niigata_tyuukei[i][0]) >=weight :
                tyuukei_fare = float(self.niigata_tyuukei[i][1].replace(',', '')) * float(tyuukei)
                break

        return std_fare + surcharge_fare + tyuukei_fare
                
        
        
    def get_keihin(self, keihin, weight):
        #keihin = '愛知','横浜','-', など 
        if keihin == '-':
            return float('inf')
            
        #基本料金std_fareを求める
        weight_idx = 0
        for i in range(len(self.keihin[0])-1, 0, -1): # 6~1まで。0は実行しない
            if float(self.keihin[0][i]) > weight : #ｹｲﾋﾝだけは重量が未満表示
                weight_idx = i
                break
        std_fare = float('inf')
        if weight_idx == 0:
            std_fare = float('inf')
        else:
            for i in range(len(self.keihin)-1, 0, -1):
                if self.keihin[i][0] == keihin :
                    std_fare = self.keihin[i][weight_idx].replace(',', '')
                    break
        '''
        '-'ならば行かないから無限大、100以下の数値ならば重量を掛ける。
        それ以外の数値はそのまま運賃。
        2025/5/21ケイヒン運賃表が更新。全て運賃が記載されているので、
        重量を乗算する必要なくなった。
        '''
        if std_fare == '-':
            keihin_fare = float('inf')
        else:
            keihin_fare = float(std_fare)

        return keihin_fare


    def get_seinou(self,dist,weight):
		
        HOKEN_FARE = 300

    
        #西濃運賃を求める
        if dist == '-':
            return float('inf')
        
        #基本料金std_fareを求める
        dist_idx: int = 0
        weight_idx: int = 0
        for i  in range(len(self.seinou[0])-1,0,-1): 
            if float(self.seinou[0][i].replace(',', '')) >= dist : 
                dist_idx = i
                break
        for i  in range(len(self.seinou)-1,0,-1): 
            if float(self.seinou[i][0].replace(',', '')) >= weight : 
                weight_idx = i
                break
        std_fare = float('inf')
        if dist_idx!= 0 and weight_idx!= 0:
            std_fare = float(self.seinou[weight_idx][dist_idx].replace(',', ''))

        # サーチャージを求める
        dist_idx: int = 0
        weight_idx: int = 0
        for i  in range(len(self.seinou_surcharge[0])-1,0,-1): 
            if float(self.seinou_surcharge[0][i].replace(',', '')) >= dist : 
                dist_idx = i
                break
        for i  in range(len(self.seinou_surcharge)-1,0,-1): 
            if float(self.seinou_surcharge[i][0].replace(',', '')) >= weight : 
                weight_idx = i
                break
        surcharge_fare = float('inf')
        if dist_idx!= 0 and weight_idx!= 0:
            surcharge_fare = float(self.seinou_surcharge[weight_idx][dist_idx].replace(',', ''))
       
        #中継料金を求める
        tyuukei_fare: float= 0.0

        return std_fare + surcharge_fare + tyuukei_fare + HOKEN_FARE


    def get_tonami_diff(self, designation, weight):
        '''
        使っていない
        '''
        
        if designation != 'ﾄﾅﾐ':
            return 0

        tonami_new = 0
        for i in range(len(self.tonami_new)-1, 0, -1):
            if float(self.tonami_new[i][0]) >= weight :
                tonami_new_price = self.tonami_new[i][1].replace(',', '')
                break                        #コンマがあるケースがあるので...
        tonami_old = 0
        for i in range(len(self.tonami_old)-1, 0, -1):
            if float(self.tonami_old[i][0]) >= weight :
                tonami_old_price = self.tonami_old[i][1].replace(',', '')
                break
        tonami_diff = float(tonami_new_price) - float(tonami_old_price)
        return tonami_diff
            




	#applyでdfの行を受け取る
    def get_untin(self, df_row):
        nounyuusaki = df_row['納入先名称１']
        weight = df_row['weight']
        address = df_row['住所１']
        torr_dist = df_row['ﾄｰﾙ距離']
        torr_tyuukei = df_row['ﾄｰﾙ中継回数']
        torr_YN = df_row['ﾄｰﾙ行く行かない']
        niigata_dist = df_row['新潟距離']
        niigata_tyuukei = df_row['新潟中継回数']
        niigata_YN = df_row['新潟行く行かない']
        keihin = df_row['ｹｲﾋﾝ向']
        designation = df_row['顧客指定運送屋']
        seinou_dist = df_row['西濃距離']

        if address != 'NoCalc' and address is not np.nan:
            torr_fare = self.get_torr(torr_dist,weight,torr_YN,address
                                      ,torr_tyuukei)

            niigata_fare = self.get_niigata(niigata_dist, weight, niigata_YN
                                      , niigata_tyuukei)

            keihin_fare = self.get_keihin(keihin, weight)

            seinou_fare = self.get_seinou(seinou_dist, weight)
        else:
            torr_fare = 0
            niigata_fare = 0
            keihin_fare = 0
            seinou_fare = 0

        return pd.Series([torr_fare,niigata_fare, keihin_fare, seinou_fare])















