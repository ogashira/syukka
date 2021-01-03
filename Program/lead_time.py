#! python
# -*- coding: cp932 -*-

import csv
from datetime import datetime
import pandas as pd
import os

class LeadTime(object):

    def __init__(self):

        # �z�B�����ް��̎擾
        if os.name == 'nt':
            nounyuusaki_file = open(r'//192.168.1.247/���L/��check/master/order_nounyuusaki.csv', encoding = 'cp932')
        else:    
            nounyuusaki_file = open(r'../master/selfMade/order_nounyuusaki.csv', encoding = 'cp932')

        file_reader = csv.reader(nounyuusaki_file)
        nounyuusaki_l = list(file_reader)
        nounyuusaki_file.close()


        #�񎟌�ؽĂɂ���
        self.nounyuusaki = []
        for row in nounyuusaki_l:
            rows = []
            rows.append(row[0])       # ���Ӑ�R�[�h
            rows.append(row[1])       # �[����R�[�h
            rows.append(row[3])       # �z�B����
            rows.append(row[5])       # �[���於��
            self.nounyuusaki.append(rows)

        # 0��:�N����,1��:���m�x��, 2��:�^�����x��
        if os.name == 'nt':
            eigyou_file = open(r'//192.168.1.247/���L/��check/master/order_holiday.csv', encoding = 'cp932')
        else:
            eigyou_file = open(r'../master/selfMade/order_holiday.csv', encoding = 'cp932')

        file_reader = csv.reader(eigyou_file)
        header = next(file_reader)
        self.unsou_eigyoubi = list(file_reader)
        eigyou_file.close()


        # **/**/** �̌`�ɂ���
        for row in self.unsou_eigyoubi:
            time_data = datetime.strptime(row[0], '%Y/%m/%d')
            row[0] = time_data.strftime('%Y/%m/%d') 
            del row[1]  # �Q��ڂ̗j���͍폜����B




    def get_youbi(self, df_row):

        tokui_code = df_row['���Ӑ�R�[�h']
        nounyuu_code = df_row['�[����R�[�h']
        syukkabi = df_row['�o�ח\���']
        nouki = df_row['�[��']
        syukkayotei = df_row['�o�ח\��q��']


        # �z�B���������߂�
        nissuu = 0
        for line in self.nounyuusaki:
            if (
            line[0] == tokui_code  and line[1] == nounyuu_code
            ) or (
            line[0] == tokui_code and line[1] == '' and pd.isnull(nounyuu_code)
            ):
                nissuu = int(line[2])

        # �[������k���ďo�ד������߂�B
        # �^�����x���͔z�B�����ɐ����Ȃ��B�o�ד������m�x����������k���ē��m�c�Ɠ��܂�
        # �߂�B�o�ד����o�ח\���������i�傫���j��������u�j���Ⴂ�v�Ƃ���B
        # 0��:�N����,1��:���m�x��, 2��:�^�����x��

        for i in range(len(self.unsou_eigyoubi)):
            if self.unsou_eigyoubi[i][0]== syukkabi:
                syukka_idx = i                          #�o�ד��\�����index
            if self.unsou_eigyoubi[i][0] == nouki:
                nouki_idx = i                           #�[����index
                break
                

        while nissuu > 0 :
            if self.unsou_eigyoubi[nouki_idx][2] == '�x':
                nouki_idx -= 1
            else:
                nouki_idx -= 1
                nissuu -= 1
        while self.unsou_eigyoubi[nouki_idx][1] == '�x':
                nouki_idx -= 1

        calc_syukka_idx = nouki_idx               #�[������v�Z�����o�ׂ��ׂ�����idx


        if syukka_idx < calc_syukka_idx :
            syukkayotei.append('�j��')

        return syukkayotei
        




        

