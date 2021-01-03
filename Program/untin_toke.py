#! python
# -*- coding: cp932 -*-

import csv
import pandas as pd
import numpy as np
#from unsoutaiou import *


class Untin_toke :

    def __init__ (self):
        #self.weight = weight
        #self.deli_name = deli_name

        unsou_file = open(r'../master/untin/torr_toke.csv',encoding='cp932')
        file_reader = csv.reader(unsou_file)
        self.torr = list(file_reader)
        unsou_file.close()
        
        unsou_file = open(r'../master/untin/torr_toke_nara_hirosima.csv'
                          ,encoding='cp932')
        file_reader = csv.reader(unsou_file)
        self.torr_nara_hirosima = list(file_reader)
        unsou_file.close()
        
        unsou_file = open(r'../master/untin/torr_tyuukei_toke.csv'
                          ,encoding='cp932')
        file_reader = csv.reader(unsou_file)
        self.torr_tyuukei= list(file_reader)
        unsou_file.close()

        unsou_file = open(r'../master/untin/keihin_toke.csv',encoding='cp932')
        file_reader = csv.reader(unsou_file)
        self.keihin= list(file_reader)
        unsou_file.close()

        unsou_file = open(r'../master/untin/niigata_toke.csv',encoding='cp932')
        file_reader = csv.reader(unsou_file)
        self.niigata= list(file_reader)
        unsou_file.close()

        unsou_file = open(r'../master/untin/niigata_tyuukei_toke.csv'
                          ,encoding='cp932')
        file_reader = csv.reader(unsou_file)
        self.niigata_tyuukei= list(file_reader)
        unsou_file.close()

        unsou_file = open(r'../master/untin/tonami_new_toke.csv'
                          ,encoding='cp932')
        file_reader = csv.reader(unsou_file)
        self.tonami_new = list(file_reader)
        unsou_file.close()

        unsou_file = open(r'../master/untin/tonami_old_toke.csv'
                          ,encoding='cp932')
        file_reader = csv.reader(unsou_file)
        self.tonami_old = list(file_reader)
        unsou_file.close()



    def get_torr(self,dist,weight,YN,address,tyuukei):
		
		#どちらの運賃表を使うか？
        if '広島県'in address or '奈良県' in address:
            untin_mtx = self.torr_nara_hirosima
        else:
            untin_mtx = self.torr
        
    
        #トールの運賃を求める
        if YN == '-':
            return float('inf')
        
        #基本料金std_fareを求める
        dist_idx = 0
        for i  in range(len(untin_mtx[0])-1,0,-1): 
            if float(untin_mtx[0][i].replace(',', '')) >= dist : 
                dist_idx = i
                break
        std_fare = float('inf')
        if dist_idx== 0:
            std_fare = float('inf')
        else:
            for i in range(len(untin_mtx)-1,0,-1):
                if float(untin_mtx[i][0]) >= weight :
                    std_fare = untin_mtx[i][dist_idx].replace(',', '')
                    break
        
        #中継料金を求める
        if tyuukei == 0:
            tyuukei_fare = 0
        else:
            for i in range(len(self.torr_tyuukei)-1,0,-1):
                if float(self.torr_tyuukei[i][0]) >=weight :
                    tyuukei_fare = self.torr_tyuukei[i][1].replace(',', '')
                    tyuukei_fare = float(tyuukei_fare) * float(tyuukei)
                    break
        

        return float(std_fare) + float(tyuukei_fare)



    def get_niigata(self, dist, weight, YN, address, tyuukei) :

        if YN == '-':
            return float('inf')

        #基本料金std_fareを求める
        dist_idx = 0
        for i in range(len(self.niigata[0])-1, 0, -1):
            if float(self.niigata[0][i].replace(',', '')) >= dist :
                dist_idx = i
                break
        std_fare = float('inf')
        if dist_idx == 0:
            std_fare = float('inf')
        else:
            for i in range(len(self.niigata)-1, 0, -1):
                if float(self.niigata[i][0]) >= weight :
                    std_fare = self.niigata[i][dist_idx].replace(',', '')
                    break
       
        #中継料金を求める
        if tyuukei == 0:
            tyuukei_fare = 0
        else:
            for i in range(len(self.niigata_tyuukei)-1,0,-1):
                if float(self.niigata_tyuukei[i][0]) >=weight :
                    tyuukei_fare = self.niigata_tyuukei[i][1].replace(',', '')
                    tyuukei_fare = float(tyuukei_fare) * float(tyuukei)
                    break

        return float(std_fare) + float(tyuukei_fare)
                
        
        
    def get_keihin(self, keihin, weight):
        #keihin = '愛知','横浜','-', など 
        if keihin == '-':
            return float('inf')
            
        #基本料金std_fareを求める
        weight_idx = 0
        for i in range(len(self.keihin[0])-1, 0, -1):
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
        '''
        if std_fare == '-':
            keihin_fare = float('inf')
        else:
            if float(std_fare) < 100:
                keihin_fare = float(std_fare) * weight
            else:
                keihin_fare = float(std_fare)

        return keihin_fare



    def get_tonami_diff(self, designation, weight):
        
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

        if address != 'NoCalc' and address is not np.nan:
            torr_fare = self.get_torr(torr_dist,weight,torr_YN,address
                                      ,torr_tyuukei)

            niigata_fare = self.get_niigata(niigata_dist, weight, niigata_YN
                                      , address, niigata_tyuukei)

            keihin_fare = self.get_keihin(keihin, weight)

            tonami_diff = self.get_tonami_diff(designation,weight) 
        else:
            torr_fare = 0
            niigata_fare = 0
            keihin_fare = 0
            tonami_diff = 0

        return pd.Series([torr_fare,niigata_fare, keihin_fare, tonami_diff])















