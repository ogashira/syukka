#! python
# -*- coding: cp932 -*-

import openpyxl
import pandas as pd
import os

class AddData(object):

    def __init__(self):

    #�A�o�h���A���\�̎擾
        if os.name == 'nt':
            wb = openpyxl.load_workbook(
                r'//192.168.1.247/���L/�c�Ɖ�̫���/�N�c/������/���㏈��(����ے��p)/' \
                r'�o�׎��Y�t���X�g(20200731���_�ŐV��).xlsx', data_only=True
            )
        else:
            wb = openpyxl.load_workbook(
               r'../master/�o�׎��Y�t���X�g(20200731���_�ŐV��).xlsx', data_only=True
            )
        ws = wb['���ѕ\']
        
        #�񎟌�ؽĂɂ���
        self.coa_list = []
        for row in ws.rows:
            rows = []
            for cell in row:
                rows.append(cell.value)
            self.coa_list.append(rows)


        ws = wb['�w��`�[']
        
        #�񎟌�ؽĂɂ���
        self.sitei_denpyou = []
        for row in ws.rows:
            rows = []
            for cell in row:
                rows.append(cell.value)
            self.sitei_denpyou.append(rows)


    def get_coa(self, df_row):
        tokui_code = df_row['���Ӑ�R�[�h']
        nounyuu_code = df_row['�[����R�[�h']
        hinban =  df_row['hinban']

        if pd.isnull(nounyuu_code):
            nounyuu_code = None

        yoteisouko_list = df_row['�o�ח\��q��']

        for line in self.coa_list:
            if tokui_code == line[0] and nounyuu_code == line[1] and hinban == line[3]:
                yoteisouko_list.append('��')
                break


        for line in self.sitei_denpyou:
            if tokui_code == line[0] and nounyuu_code == line[1]:
                yoteisouko_list.append('�w')
                break


        return yoteisouko_list

