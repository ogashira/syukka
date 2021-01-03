#! python
# -*- coding: cp932 -*-

import pandas as pd
import numpy as np
import re
import csv
import barcode
from barcode.writer import ImageWriter
import openpyxl
from openpyxl.styles.borders import Border, Side
from openpyxl.styles.fonts import Font
from openpyxl.utils import get_column_letter
from openpyxl.workbook import Workbook
import unicodedata



class Kenpin(object):

    def __init__(self, factory, packingHinban, untinForUriage, myfolder):
        
        if factory == 'toke':
            self.kenpin_folder = r'\\192.168.3.204\effitA_HT\���M�f�[�^\kenpin.csv' 
            self.syukka_koujou = '�o�׍H��F@0002 �y�C�H��'
            self.factory = '�y�C'
        elif factory == 'honsya':
            self.kenpin_folder = r'C:\effitA_HT\���M�f�[�^\kenpin.csv'
            self.syukka_koujou = '�o�׍H��F@0001 �{�ЍH��'
            self.factory = '�{��'
        else:
            self.kenpin_folder = r'./kenpin_mac.csv'
            self.syukka_koujou = 'mac : @0000 fromMac'
            self.factory = 'Mac'

        self.packingHinban = packingHinban

        self.untinForUriage = untinForUriage

        self.myfolder = myfolder




    def get_kenpin(self):
        
        def get_kubun(df_row):
            iraisaki = df_row['�˗���']
            yotei_souko = df_row['�o�ח\��q��_y']
            syukkabi = df_row['�o�ח\���']
            cans = df_row['cans']
            unsou = unsou_dic[iraisaki][0]
            unsou_code = unsou_dic[iraisaki][1]
            if '�c�Ə�' in yotei_souko:
                kubun = '�c�Ə�'
                kubun_no = 3
            elif '�y�j�z�B' in yotei_souko:
                kubun = '�y�j�z�B'
                kubun_no = 2
            elif '�j��' in yotei_souko:
                kubun = '�j���Ⴂ'
                kubun_no = 4
            elif '�j���z�B' in yotei_souko:
                kubun = '�j���z�B'
                kubun_no = 5
            else:
                kubun = '�ʏ�'
                kubun_no = 1
                
            cans = int(cans)
            syukkabi = syukkabi.replace('/', '')
            
            return pd.Series([unsou, unsou_code, kubun, kubun_no, cans, syukkabi])



        unsou_dic = {'İ�':['�g�[��','U0001'], '�V��':['�V���^�A','U0009'], 
                '���S':['���S','U0002'], '���Z':['���Z','U0003'], 
                '���':['�g�i�~','U0004'], '���R':['���R','U0006'], 
                '�z�B':['�z�B','U0008'], '����':['����}��','U0010'], 
                '����':['�P�C�q��','U0007'], '�v����':['�v����','U0005'],
                'npNan':['npNan','npNan'], 'NoData':['NoData', 'NoData'],
                'NoCalc':['NoCalc','NoCalc']}
        
        haisou_kubun = {
        '�ʏ�': 1, '�y�j�z�B': 2, '�c�Ə�': 3, '�j���Ⴂ': 4, '�j���z�B': 5
        }



        merg_data = self.packingHinban[
        ['�󒍂m�n','�󒍍s�m�n','�󒍐���','�o�ח\��q��', '�i��','�󒍒P��', 
        '�[���於�̂P']
        ]

        kenpin = pd.merge(self.untinForUriage, merg_data, 
                on=['�󒍂m�n','�󒍍s�m�n'], how = 'left')
        
        kenpin[['unsou','unsou_code','kubun','kubun_no','cans',
            '�o�ח\���']]  = kenpin.apply(get_kubun, axis = 1)

        kenpin = kenpin[
        ['���Ӑ�R�[�h','�[����R�[�h','unsou_code','unsou','kubun_no','kubun',
        '�o�ח\���','hinban','�i��','lot','cans','�󒍐���','�󒍒P��',
        '�[���於�̂P','�A�o����', '���Ӑ撍���m�n', '���l','add']
        ]

        # lot�������łQ�ȏ�̂��̂����e�����ɂ��āA�s�𑝂₷�B>>>>>>>>>>>>>>>
        
        # df_list��kenpin���P�s�������
        df_list = []
        for i in range(len(kenpin)):
            df = kenpin.iloc[[i]]
            df_list.append(df)
        
        # lot��key��value��cans�Ǝ󒍐��ʂɓ���Ȃ���A��߰��
        # df_list2�ɓ���Ă���
        df_list2 = []    
        for df in df_list:
            lots = df.iloc[0,9]
            if lots == {}:
                lots = {'short':0}
            for k, v in lots.items():
                df2 = df.copy()
                cans = df2.loc[:, 'cans']
                kg = df2.loc[:,'�󒍐���']
                ratio = kg/cans
                # lot���Q��ވȏ゠�����ꍇ��cans��kg���v�Z����B
                df2.loc[:,'lot'] = k
                if k != 'short':
                    df2.loc[:, 'cans'] = int(v)
                    df2.loc[:, '�󒍐���'] = int(v * ratio)
                else:
                    df2.loc[:,'lot'] = None
                    
                df_list2.append(df2)
        
        df_col = df_list2[0].columns
        
        df_kara = pd.DataFrame(index=[], columns=df_col)
        for line in df_list2:
            df_kara = pd.concat([df_kara, line])
        
        
        df_kara2 = df_kara.sort_values(['unsou_code', 'kubun_no'])

        return df_kara2


    def create_kenpin(self):

        df_kara2 = self.get_kenpin()
        df_kara2 = df_kara2.loc[(df_kara2['�A�o����'] != 'y') & (df_kara2['hinban'] != '999998'), :]
        df_kara2 = df_kara2[['unsou_code','unsou','kubun_no','kubun','�o�ח\���','hinban','�i��','lot','cans','�󒍐���']]
        
        try:
            df_kara2.to_csv(self.kenpin_folder, index=False, header = False , encoding='cp932')
        except Exception as ex:
            print('************kenpin.csv�쐬�G���[****************')
            print('Folder��������Ȃ��̂ŁA{}��kenpin.csv��myfolder�ɕ��荞�݂܂�'.format(self.factory))
            df_kara2.to_csv(self.myfolder + '/kenpin_' + self.factory + '.csv', index=False, header = False , encoding='cp932')





    def get_syukka_jisseki_syoukai(self):
        

        # ����旪���ް��̎擾
        # nounyuusaki = pd.read_csv(r'//192.168.1.247/���L/��check/master/order_nounyuusaki.csv', encoding = 'cp932')
        nounyuusaki = pd.read_csv(r'../master/selfMade/order_nounyuusaki.csv', encoding = 'cp932')

        #merge�p�f�[�^�ɉ��H����
        merge_data = nounyuusaki[['�����R�[�h�P','�����R�[�h�Q','����旪��']]
        merge_data = merge_data.rename(
        columns = {'�����R�[�h�P':'���Ӑ�R�[�h', '�����R�[�h�Q':'�[����R�[�h', '����旪��':'�[���於'}
        )

        # merge_data��NaN���󕶎��ɂ��Ă����B�������Ȃ���merge���ł��Ȃ��B
        merge_data = merge_data.fillna('')
        
        kenpin_moto = self.get_kenpin()
        kenpin_moto = kenpin_moto.fillna('')
        
        kenpin_merge = pd.merge(kenpin_moto, merge_data, on = ['���Ӑ�R�[�h', '�[����R�[�h'], how = 'left')

        # unsou_code��kubun_no�̃^�v����set�ɓ���ďd�����Ȃ����B>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        # {(U0009, 1), (U0009, 4), (U0005, 1)......}
        unsou_set = set()
        for i in range(len(kenpin_merge)):
            unsou_code = kenpin_merge.iloc[i, 2]
            kubun_no = kenpin_merge.iloc[i, 4]

            t = (unsou_code, kubun_no)
            unsou_set.add(t)
        # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

        i = 0
        wb = openpyxl.Workbook()
        for unsou_code, kubun_no in unsou_set:

            kenpin_split = kenpin_merge.loc[(kenpin_merge['unsou_code']== unsou_code) & (kenpin_merge['kubun_no'] == kubun_no),:]
            unsou = kenpin_split.iloc[0,3]
            kubun = kenpin_split.iloc[0,5]

            unsou_gyousya = '�^���ƎҁF{} {}     �z���敪�F{} {}'.format(unsou_code, unsou, kubun_no, kubun)

            sheet_name = '{}_{}'.format(unsou, kubun)
            barcode_str = unsou_code + str(kubun_no)

            # ��U�o�[�R�[�h��png�ŕۑ� 
            code39 = barcode.get_barcode_class('code39')
            barcode_img = code39(barcode_str, writer=ImageWriter(), add_checksum = False)
            barcode_img.save(r'./barcode_{}'.format(i))
            
            ws_new = wb.create_sheet(title = sheet_name,index= i)
            ws = wb[sheet_name]

            ws.sheet_view.showGridLines = False  # �g��������
            ws['E1'].value = '�o�׎��яƉ�'
            ws['A2'].value = self.syukka_koujou
            ws['A3'].value = unsou_gyousya

            

            kenpin_split = kenpin_split[['�o�ח\���','�[���於','�i��','lot','�󒍐���',
                '�󒍒P��','���Ӑ撍���m�n','cans','���l','�A�o����','add']]
            syukka_jisseki_syoukai = kenpin_split.rename(
            columns = {'�o�ח\���':'�����','lot':'ۯ�No.','�󒍐���':'���㐔��',
            '�󒍒P��':'�P��','���Ӑ撍���m�n':'����No.','cans':'�ʐ�'}
            )

            side = Side(style='thin', color='000000')
            border = Border(top=side, bottom=side, left=side, right=side)

            ws.cell(4 , 1).value = '�s'
            ws.cell(4 , 1).border = border
            ws.cell(4 , 2).value = '�����'
            ws.cell(4 , 2).border = border
            ws.cell(4 , 3).value = '�[���於'
            ws.cell(4 , 3).border = border
            ws.cell(4 , 4).value = '�i��'
            ws.cell(4 , 4).border = border
            ws.cell(4 , 5).value = 'ۯ�No.'
            ws.cell(4 , 5).border= border
            ws.cell(4 , 6).value = '���㐔��'
            ws.cell(4 , 6).border = border
            ws.cell(4 , 7).value = '�P��'
            ws.cell(4 , 7).border = border
            ws.cell(4 , 8).value = '����No.'
            ws.cell(4 , 8).border = border
            ws.cell(4 , 9).value = '�ʐ�'
            ws.cell(4 , 9).border = border
            ws.cell(4 , 10).value = '���l'
            ws.cell(4 , 10).border = border
            ws.cell(4 , 11).value = 'y'
            ws.cell(4 , 11).border = border
            ws.cell(4 , 12).value = 'add'
            ws.cell(4 , 12).border = border



            for j in range(len(syukka_jisseki_syoukai)):
                for k in range(len(syukka_jisseki_syoukai.columns)):
                    ws.cell(j+5, 1).value = j + 1
                    ws.cell(j+5, 1).border = border 
                    ws.cell(j+5, k+2).value = syukka_jisseki_syoukai.iloc[j, k]
                    ws.cell(j+5, k+2).border = border
            
            
            def get_east_asian_width_count(text):
                # �S�p�p����'F',�S�p���Ȃ�'W', ���ꕶ����'A'���Ԃ�B 
                count = 0
                for c in text:
                    if unicodedata.east_asian_width(c) in 'FWA':
                        count += 1.7
                    else:
                        count += 1
                return count


            # column�̕����������𒲐�����
            for col in ws.columns:
                max_length = 0
                column = col[0].column
            
                for cell in col:
                    if cell.row < 4: # �R�s�ڂ܂ł�autofit�����Ȃ��B
                        continue
                    cell.font = Font(size=10)
                    count = get_east_asian_width_count(str(cell.value))

                    if count > max_length:
                        max_length = count
            
                adjusted_width = (max_length + 0) * 1.1
                ws.column_dimensions[get_column_letter(column)].width = adjusted_width
                # ws.column_dimensions[column].width = adjusted_width

            # ws�Ƀo�[�R�[�h��\��t��
            img = barcode_img
            img = openpyxl.drawing.image.Image(r'./barcode_{}.png'.format(i))
            img.width = 72*3.5
            img.height = 25*2.5
            ws.add_image(img, 'H1')
            
            ws.row_dimensions[1].height = 23
            for j in range(2, ws.max_row + 1):
                ws.row_dimensions[j].height = 18

             
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

            i += 1

        wb.save('{}/�o�׎��яƉ�_{}.xlsx'.format(self.myfolder, self.factory))

        
        '''
        2020/12/18 �������񂩂�̈˗�
        �o�׎��яƉ�̹��ݕւ̂݁A�����ƗA�o�ż�Ă𕪂���
        �A�o�̏ꍇ�͍ŏI���'y'�������Ă��邩�炻��Ŏ��ʂ���
        '''
        

