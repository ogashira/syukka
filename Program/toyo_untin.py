#! python
# -*- coding: utf-8 -*-

import csv
import pandas as pd

class Toyo_untin:

    def __init__(self, moto):
        self.moto = moto

        f = open(r'../master/untin/toyo_untin_tyuukei_ari.csv'
                 , encoding='cp932')
        file_reader = csv.reader(f)
        self.toyoUntinTyuukeiAri = list(file_reader)
        f.close()
    
        f = open(r'../master/untin/toyo_untin_tyuukei_nasi.csv'
                 , encoding='cp932')
        file_reader = csv.reader(f)
        self.toyoUntinTyuukeiNasi= list(file_reader)
        f.close()

        f = open(r'../master/untin/toyo_untin_seikyuusaki.csv'
                 , encoding='cp932')
        file_reader = csv.reader(f)
        toyoUntinSeikyuuSaki= list(file_reader)
        f.close()

        self.seikyuu = {}
        for line in toyoUntinSeikyuuSaki:
            self.seikyuu[(line[0],line[2])] = [line[13],line[14]]
            

    def get_toyoUntin(self):
        
        def calc_ncan(code,name):
            ncan = self.moto.loc[(self.moto['得意先コード']== code) 
                    & (self.moto['納入先名称１']==name),'cans'].sum()


            return ncan
            
            



        def get_untin(df_row):
            code = df_row['得意先コード']
            name = df_row['納入先名称１']
            ncan_jutyuu = df_row['受注時運賃n缶']
            cans = df_row['cans']
            ireme = df_row['ireme']
            key_tpl = (code, name)
            ncan_tuika = 0
            untin = 0




            if key_tpl in self.seikyuu:
                ncan_tuika = calc_ncan(code,name)
                ncan = max(ncan_tuika, float(ncan_jutyuu))
                toyo_dist = int(self.seikyuu[key_tpl][0])
                toyo_tyuukei = int(self.seikyuu[key_tpl][1])
                
                if toyo_tyuukei > 0:
                    untinMtx = self.toyoUntinTyuukeiAri
                else:
                    untinMtx = self.toyoUntinTyuukeiNasi
                
                dist_idx = 0
                for i  in range(len(untinMtx[0])-1,0,-1): 
                    if int(untinMtx[0][i].replace(',','')) >= toyo_dist : 
                        dist_idx = i
                        break
                tanka = 0
                if dist_idx== 0:
                    tanka = 0
                else:
                    for i in range(len(untinMtx)-1,0,-1):
                        if int(untinMtx[i][0]) >= ncan :
                            tanka = untinMtx[i][dist_idx].replace(',', '')
                            break
                     
                untin = int(tanka) * int(cans) * float(ireme)
                

            return pd.Series([ncan_tuika, untin])


        
        c_moto = self.moto.copy()
        c_moto[['追加後運賃n缶','toyo_untin']] = c_moto.apply(get_untin, axis=1)

        return c_moto
