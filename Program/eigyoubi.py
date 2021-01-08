#! python3
# -*- coding: utf-8 -*-


import datetime
from datetime import timedelta
from datetime import date
import csv
import os
import platform





class Eigyoubi:

    def __init__(self):
        #休日表の取得
        pf = platform.system()
        if pf == 'Windows':
            mypath = r'//192.168.1.247/共有/受注check/master/order_holiday.csv'
        elif pf == 'Linux':
            mypath = r'/mnt/public/受注check/master/order_holiday.csv'
        else:
            mypath = r'../master/selfMade/order_holiday.csv'
        eigyou_file = open(mypath, encoding = 'cp932')
            
        file_reader = csv.reader(eigyou_file)
        header = next(file_reader)
        eigyoubi_l = list(file_reader)
        eigyou_file.close()


        #二次元ﾘｽﾄにする
        self.eigyoubi = []
        for row in eigyoubi_l:
            if row[2] == '休':
                continue
            else:           
                time_data = datetime.datetime.strptime(row[0], '%Y/%m/%d')
                self.eigyoubi.append(time_data.strftime('%Y%m%d')) 


        self.honjitu = datetime.datetime.now()
        self.honjitu = self.honjitu.strftime('%Y%m%d')
        self.honjitu_idx = self.eigyoubi.index(self.honjitu)

        sengetu = datetime.datetime.today() - timedelta(days = 60)
        self.sengetu = sengetu.strftime('%Y%m%d')
    

    def get_honjitu(self):
        return self.honjitu


    def get_zenjitu(self):
        self.zenjitu = self.eigyoubi[self.honjitu_idx - 1]
        return self.zenjitu


    def get_zenkai(self):
        self.zenkai = self.eigyoubi[self.honjitu_idx - 3]
        return self.zenkai


    def get_yokujitu(self):
        self.yokujitu = self.eigyoubi[self.honjitu_idx + 1]
        return self.yokujitu

    def get_sengetu(self):
        return self.sengetu
    

    
    
      
        
        

        

                

    




