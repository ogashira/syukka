#! python
# -*- coding: cp932 -*-

import pandas as pd
import openpyxl
import unicodedata
from openpyxl.styles.borders import Border, Side
from openpyxl.styles.fonts import Font
from openpyxl.utils import get_column_letter
import jaconv
from recorder import *

class Gyoumu:

    def __init__ (self, myfolder):
        self.myfolder = myfolder



    def get_sorting(self, P_H, myfolder, factory):


        def get_dupli(packingHinban):

            '''�A�o�ƍ����ɂ킯�Ă���dupli��concat����
            y���Ȃ��ꍇ���dataframe���o���A�����concat����ƁA
            dupli��boolean��float�ɂȂ��Ă��܂��BTrue��1, False��0
            �����ŁAconcat�̌�ɁAdupli���ް���bool�ɃL���X�g����B'''
        
            
            def moji_henkan(moji): 
                moji = jaconv.z2h(moji,digit=True,ascii=True) 
                moji = moji.replace(' ', '')
                moji = moji.replace('�@', '')
                moji = moji.upper()
                return moji




            PH_domestic = packingHinban.loc[packingHinban['�A�o����'] \
                != 'y',:].copy()
            PH_export = packingHinban.loc[packingHinban['�A�o����'] \
                == 'y', :].copy()
            
            #������dupli ���l���̕����𔼊p�������󔒖����ɂ���B
            PH_domestic.loc[:,'mojiHenkan'] = PH_domestic['���l'].map(moji_henkan)
            PH_domestic['dupli'] = PH_domestic.duplicated(subset=['�[���於�̂P', 'mojiHenkan'],keep='first')
            #�A�o��dupli
            PH_export['dupli'] = PH_export.duplicated(subset=['���Ӑ撍���m�n'] \
                                                      ,keep='first')
            
            #concat��index��reset
            PH_con = pd.concat([PH_domestic, PH_export], sort=True)
            PH_con.loc[:,'dupli'] = PH_con.loc[:, 'dupli'].map(lambda x: bool(x))

            PH_con = PH_con.sort_values(['���Ӑ�R�[�h', 'mojiHenkan'])

            PH_con.reset_index(inplace=True, drop=True)
            
            return PH_con


        packingHinban = P_H.sort_values(['���Ӑ�R�[�h', '���l'])


        #packingHinban��dupli��ǉ�(dupli�͎d�����̖ڈ��A�d���̖ڈ�)
        packingHinban = get_dupli(packingHinban)


        '''
        dataframe�̍s���P�s���������āAlist�ɓ����B
        ��������dataframe��index�͂��ꂼ��Ⴄ���Ƃɒ��ӂ���B
        index �P�ڂ�0�A�Q�ڂ�1�A�R�ڂ͂Q.....�ƂȂ��Ă���B
        '''
        df_list = []
        for i in range(len(packingHinban)):
            #copy�������̂�append���Ȃ��ƌ�X�A������ƂȂ���warning���ł�B����1
            # ��1 �ŁAdf_list2[i]��copy���ĘA�����������邱�Ƃ��ł���
            df = packingHinban.iloc[i : i + 1].copy()
            df_list.append(df)


        '''
        duplicated��df��keep = 'first'�ɂ����̂ŁA�ŏ���dupli�͕K��false�ɂȂ�B
        dupli��false�������牺��j��roop�ɂ͂���Broop�ł́A����dupli��true�Ȃ�΁A
        df��concat��������B
        false���o�����_��roop�𔲂���i��roop�𑱂���B
        i��roop�́Adupli��true�̎��͉������Ȃ��B
        '''
        df_list2 = df_list.copy()
        if len(df_list2) == 1:
            df_list2[0].loc[:,'���d��'] = df_list2[0].loc[:,'weight'].sum()
        else:        
            for i in range(len(df_list2)):
                #index�����ꂼ��Ⴄ�̂ŁAloc[i, 'supli'] �ɂ���
                if df_list2[i].loc[i, 'dupli'] == False:
                    j = i + 1
                    for j in range(j,len(df_list2)):
                        if df_list2[j].loc[j,'dupli'] == True:
                            df_list2[i] = pd.concat([df_list2[i], df_list2[j]])
                            df_list2[i].loc[:,'dupli'] = 'concat'
                        else:
                            break
                    # ��1 ������warning���ł�
                    df_list2[i].loc[:,'���d��'] = df_list2[i].loc[:,'weight'].sum()


        #dupli��False�܂���concat�̂��̂�����list3�ɓ����B
        df_list3 = []
        
        for i in range(len(df_list2)):
            if df_list2[i].loc[i, 'dupli'] != True:
                df_list3.append(df_list2[i])



        df_col = df_list3[0].columns

        df_kara = pd.DataFrame(index=[], columns=df_col)
        df_kara.loc['a'] = '<' * 5

        result = df_kara.copy()
        for line in df_list3:
            result = pd.concat([result, line])
            result = pd.concat([result, df_kara])



        result = result[['�˗���','cans','���d��','���Ӑ�R�[�h','�[����R�[�h',
                         '�[���於�̂P', '�i��','���Ӑ撍���m�n','���l','�o��',
                         '�o�ח\��q��','add']]




        recorder = Recorder(self.myfolder)
        
        txt = '�Ɩ��o�׏����p�ް��i{}�j'.format(factory)
        recorder.out_log('')
        recorder.out_file('')
        recorder.out_log(txt, '\n')
        recorder.out_log(result, '\n')
        recorder.out_file(txt, '\n')
        recorder.out_file(result, '\n')

        #packingHinban��excel�`����filePath�ɕۑ�����B
        filePath = '{}/{}�Ɩ�_packing.xlsx'.format(myfolder, factory)
        result.to_excel(filePath, index = False)
        #recorder.out_csv(result, filePath)

        del recorder


        return result


    def get_excel_style(self, filePath):
        wb =  openpyxl.load_workbook(filePath)
        ws = wb['Sheet1']
        
        max_col = ws.max_column
        max_row = ws.max_row

        def get_east_asian_width_count(text):
            # �S�p�p����'F',�S�p���Ȃ�'W', ���ꕶ����'A'���Ԃ�B 
            count = 0
            for c in text:
                if unicodedata.east_asian_width(c) in 'FWA':
                    count += 1.7
                else:
                    count += 1
            return count

        i = 2
        while True:
            if ws.cell(i, 1).value == None:
                break
            if ws.cell(i, 1).value == '<<<<<':
                ws.delete_rows(i)
                
                for j in range(1, max_col+1):
                    border = Border(top = Side(style='medium', color='000000'))
                    ws.cell(i, j).border = border
                
                # �P�s�폜����������-1����
                i -= 1 

            i += 1

        # column�̕����������𒲐�����
        for col in ws.columns:
            max_length = 0
            column = col[0].column
        
            for cell in col:
                if cell.row == 1:
                    continue
                cell.font = Font(size=10)
                count = get_east_asian_width_count(str(cell.value))

                if count > max_length:
                    max_length = count
        
            adjusted_width = (max_length + 0) * 1.1
            ws.column_dimensions[get_column_letter(column)].width = adjusted_width
            # ws.column_dimensions[column].width = adjusted_width
            


        for i in range(max_row + 1):
            ws.row_dimensions[i].height = 20

        # ����ݒ�
        ws.page_setup.orientation = ws.ORIENTATION_LANDSCAPE
        ws.page_setup.fitToWidth = 1
        ws.page_setup.fitToHeight = 0
        ws.sheet_properties.pageSetUpPr.fitToPage = True
        ws.page_setup.paperSize = ws.PAPERSIZE_A4
        ws.page_margins.left = 0.2
        ws.page_margins.right = 0.2
        ws.page_margins.top = 0.8
        ws.page_margins.bottom = 0.8
            
        wb.save(filePath)

        
