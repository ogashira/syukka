#! python
# -*- coding: cp932 -*-

import csv
import pandas as pd
import numpy as np



class Untin_honsya :

    def __init__ (self):
        #self.weight = weight
        #self.deli_name = deli_name

        unsou_file = open(r'../master/untin/torr_honsya.csv',encoding='cp932')
        file_reader = csv.reader(unsou_file)
        self.torr = list(file_reader)
        unsou_file.close()
        
        unsou_file = open(r'../master/untin/torr_tyuukei_honsya.csv'
                          ,encoding='cp932')
        file_reader = csv.reader(unsou_file)
        self.torr_tyuukei= list(file_reader)
        unsou_file.close()

        unsou_file = open(r'../master/untin/keihin_honsya.csv',encoding='cp932')
        file_reader = csv.reader(unsou_file)
        self.keihin= list(file_reader)
        unsou_file.close()

        unsou_file = open(r'../master/untin/niigata_honsya.csv',encoding='cp932')
        file_reader = csv.reader(unsou_file)
        self.niigata= list(file_reader)
        unsou_file.close()

        unsou_file = open(r'../master/untin/niigata_tyuukei_honsya.csv'
                          ,encoding='cp932')
        file_reader = csv.reader(unsou_file)
        self.niigata_tyuukei= list(file_reader)
        unsou_file.close()

        unsou_file = open(r'../master/untin/tonami_new_honsya.csv'
                          ,encoding='cp932')
        file_reader = csv.reader(unsou_file)
        self.tonami_new = list(file_reader)
        unsou_file.close()

        unsou_file = open(r'../master/untin/tonami_old_honsya.csv'
                          ,encoding='cp932')
        file_reader = csv.reader(unsou_file)
        self.tonami_old = list(file_reader)
        unsou_file.close()

        unsou_file = open(r'../master/untin/kurume_honsya.csv',encoding='cp932')
        file_reader = csv.reader(unsou_file)
        self.kurume = list(file_reader)
        unsou_file.close()



    def get_torr(self,dist,weight,YN,address,tyuukei):
		
        '''
		#�ǂ���̉^���\���g�����H �{�Ђł͍L���A�ޗǂ̉^���\�͖���
        if '�L����'in address or '�ޗǌ�' in address:
            untin_mtx = self.torr_nara_hirosima
        else:
            untin_mtx = self.torr
       ''' 
    
        #�g�[���̉^�������߂�
        if YN == '-':
            return float('inf')
        
        #��{����std_fare�����߂�
        dist_idx = 0
        for i  in range(len(self.torr[0])-1,0,-1): 
            if float(self.torr[0][i].replace(',','')) >= dist : 
                dist_idx = i
                break
        std_fare = float('inf')
        if dist_idx== 0:
            std_fare = float('inf')
        else:
            for i in range(len(self.torr)-1,0,-1):
                if float(self.torr[i][0]) >= weight :
                    std_fare = self.torr[i][dist_idx].replace(',', '')
                    break
        
        #���p���������߂�
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

        #��{����std_fare�����߂�
        dist_idx = 0
        for i in range(len(self.niigata[0])-1, 0, -1):
            if float(self.niigata[0][i].replace(',','')) >= dist :
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
       
        #���p���������߂�
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
        #keihin = '���m','���l','-', �Ȃ� 
        if keihin == '-':
            return float('inf')
            
        #��{����std_fare�����߂�
        weight_idx = 0
        for i in range(len(self.keihin[0])-1, 0, -1):
            #���݂����͏d�ʂ������\��
            if float(self.keihin[0][i].replace(',','')) > weight : 
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
        '-'�Ȃ�΍s���Ȃ����疳����A100�ȉ��̐��l�Ȃ�Ώd�ʂ��|����B
        ����ȊO�̐��l�͂��̂܂܉^���B
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
        
        if designation != '���':
            return 0

        tonami_new = 0
        for i in range(len(self.tonami_new)-1, 0, -1):
            if float(self.tonami_new[i][0]) >= weight :
                #�R���}������P�[�X������̂�...
                tonami_new_price = self.tonami_new[i][1].replace(',', '')
                break                        
        tonami_old = 0
        for i in range(len(self.tonami_old)-1, 0, -1):
            if float(self.tonami_old[i][0]) >= weight :
                tonami_old_price = self.tonami_old[i][1].replace(',', '')
                break
        tonami_diff = float(tonami_new_price) - float(tonami_old_price)
        return tonami_diff
            

    def get_kurume(self, dist_YN, weight): 
        #�v���Ẳ^�������߂�
        if dist_YN == '-':
            return float('inf')
        
        #��{����std_fare�����߂�
        dist_idx = 0
        for i  in range(len(self.kurume[0])-1,0,-1): 
            if float(self.kurume[0][i].replace(',','')) >= float(dist_YN) : 
                dist_idx = i
                break
        std_fare = float('inf')
        if dist_idx== 0:
            std_fare = float('inf')
        else:
            for i in range(len(self.kurume)-1,0,-1):
                if float(self.kurume[i][0]) >= weight :
                    std_fare = self.kurume[i][dist_idx].replace(',', '')
                    break
        return std_fare


	#apply��df�̍s���󂯎��
    def get_untin(self, df_row):
        nounyuusaki = df_row['�[���於�̂P']
        weight = df_row['weight']
        address = df_row['�Z���P']
        torr_dist = df_row['İً���']
        torr_tyuukei = df_row['İْ��p��']
        torr_YN = df_row['İٍs���s���Ȃ�']
        niigata_dist = df_row['�V������']
        niigata_tyuukei = df_row['�V�����p��']
        niigata_YN = df_row['�V���s���s���Ȃ�']
        keihin = df_row['���݌�']
        designation = df_row['�ڋq�w��^����']
        kurume_distYN = df_row['�v���ċ���']

        if address != 'NoCalc' and address is not np.nan:
            torr_fare = self.get_torr(torr_dist,weight,torr_YN,address
                                      ,torr_tyuukei)

            niigata_fare = self.get_niigata(niigata_dist, weight, niigata_YN
                                            , address, niigata_tyuukei)

            keihin_fare = self.get_keihin(keihin, weight)

            kurume_fare = self.get_kurume(kurume_distYN, weight)

            tonami_diff = self.get_tonami_diff(designation,weight) 
        else:
            torr_fare = 0
            niigata_fare = 0
            keihin_fare = 0
            kurume_fare = 0
            tonami_diff = 0


        return pd.Series([torr_fare,niigata_fare, keihin_fare ,kurume_fare
                         , tonami_diff])


