#! python3
# -*- coding: cp932 -*-


import datetime
from datetime import timedelta
from datetime import date
import csv
import os





class Eigyoubi:

    def __init__(self):
        #休日表の取得
        if os.name == 'nt':
            eigyou_file = open(r'//192.168.1.247/共有/受注check/master/order_holiday.csv', encoding = 'cp932')
        else:
            eigyou_file = open(r'../master/selfMade/order_holiday.csv', encoding = 'cp932')
            
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
    

    
    
      
        
        

        

                

    




