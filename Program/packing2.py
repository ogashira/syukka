#! python
# -*- coding: cp932 -*-

import jaconv
import csv
import pandas as pd
import numpy as np
import re
import sys
from unsoutaiou import *
from untin_toke import *
from untin_honsya import *
from toyo_untin import *


class Packing :
	
    def __init__(self):
        hinban_file = open(r'//192.168.1.247/���L/�Z�p��̫���/200. effit_data/'
                           r'Ͻ�/hinban.csv', encoding='cp932')
        # hinban_file = open(r'../master/hinban.csv', encoding='cp932')
        file_reader = csv.reader(hinban_file)
        header = next(file_reader)
        hinban = list(file_reader)
        hinban_file.close()
        
        #self.tanjuu = [�i�ԁA�i���A�P�d]
        self.tanjuu = []
        for line in hinban:
        	lines = [ line[0], line[7], line[41] ]
        	self.tanjuu.append(lines)
        
        #�^���v�Z���_���̌����
        self.untin_moto = pd.read_csv(r'../master/effitA/�^���v�Z���_��.csv',
                                      encoding='cp932',skiprows=1)
        if self.untin_moto.shape[0] == 0 :
            print('�^���v�Z���_��.csv ���ް�������܂���B�I�����܂��B')
            sys.exit()

        self.untin_moto = self.untin_moto.sort_values(by=['���Ӑ�R�[�h', 
                                                          '�[���於�̂P'])
        
        
        #�����߰يʎg�p�̕i�ԁi�ʂ̏d��3kg�j
        AT_file = open(r'../master/selfMade/AT_un_pl.csv', encoding='cp932')
        file_reader = csv.reader(AT_file)

        self.AT_un_pl = []
        for row in file_reader: #�ꎟ��ؽĂɂ��邽��
            self.AT_un_pl.append(''.join(row))

        AT_file.close()
            
        #�����񒆂�-1-��-�ɁA������Ō��-1���폜����B
        def change_hinban(hinban):
            chg_hinban = re.sub('-1-','-',hinban)
            chg_hinban = re.sub('-1$','',chg_hinban)
            return chg_hinban
            
        
        #�P�ʂ�CN�̕i�Ԃ�-EX-THI��-EX�ɂ���
        def change_hinban_mukesaki(hinban):
            chg_hinban = re.sub('-EX-.*$','-EX', hinban)
            return chg_hinban

        
        # In[43]:
        
        
        #ؽ�tanjuu���g���āA�i�Ԃ������ڂ����߂�
        def get_ireme(hinban):
            ireme = 0
            for line in self.tanjuu:
                if line[0] == hinban :
                    ireme = float(line[2])/ 1000
                    break
            return ireme
        
        
        #�i�����������A���p�ɂ��Ă���(15KG)�́@15�����o�� �@'ireme2'�Ƃ���B
        def get_ireme2(hinmei):
            # �啶�����������ɕϊ�
            hinmei = hinmei.lower() 
            #�S�p�𔼊p�ɂ���(�������L����)
            hinmei = jaconv.z2h(hinmei,digit=True,ascii=True) 
            
            result = re.search(r'(\d+\.?\d*kg)', hinmei) 
            if result:
                hinmei2 = result.group()
                result2 = re.search(r'(\d+\.?\d*)', hinmei2)
                hinmei3 = result2.group()
                hinmei3 = float(hinmei3)
            else:
                hinmei3 = None
            
            return hinmei3
        

        
        #un_AT��3kg,200g(��׽�r)��0.3kg�A1kg�ȉ���0.2kg,
        #6kg�ȉ���0.5kg, -R-EX��1kg, �i�Ԓ���-EX-,�Ō��-EX �͂Qkg
        #����ȊO��1kg
        def get_can_weight (row):
            ireme = row['ireme']
            hinban = row['hinban']
            if hinban in self.AT_un_pl:
                can_weight = 3
            elif ireme == 0.2 :
                can_weight = 0.3
            elif ireme <= 1.0 :
                can_weight = 0.2
            elif 1.0 < ireme < 6:
                can_weight = 0.5
            elif re.search('-R-EX', hinban):
                can_weight = 1
            elif re.search('-EX$|-EX-', hinban):
                can_weight = 2
            else: can_weight = 1
            
            return can_weight

        
        #���ڋq�͍폜����
        moto_h = self.untin_moto.loc[self.untin_moto['���Ӑ�R�[�h'] 
                <= 'T6000',:] 
        if moto_h.shape[0] == 0 :
            print('�{�ЁE�y�C�o�ׂ�����܂���B�I�����܂��B')
            sys.exit()


        moto_honsya = moto_h.copy()
        #�P��KG�̏ꍇ�A-1- ��- , -1(�Ō�)������
        moto_honsya.loc[moto_honsya['�󒍒P��']=='KG','hinban'] = \
                moto_honsya['�i��'].map(change_hinban)
        moto_honsya.loc[moto_honsya['�󒍒P��']=='CN','hinban'] = \
                moto_honsya['�i��'].map(change_hinban_mukesaki)
        
        moto_honsya.loc[:,'ireme']= moto_honsya['hinban'].map(get_ireme)
        
        #999998�ȂǓ���ڂ�0�̏ꍇ�́A�i���������ڂ����߂�
        moto_honsya.loc[moto_honsya['ireme']==0, 'ireme'] \
            = moto_honsya['�i��'].map(get_ireme2)



        moto_honsya.loc[moto_honsya['�󒍒P��']== 'KG','cans'] \
                = moto_honsya['�󒍐���']/ moto_honsya['ireme']
        moto_honsya.loc[moto_honsya['�󒍒P��']== 'CN','cans'] \
                = moto_honsya['�󒍐���']
        #apply��datafram���Ɗ֐��ɓn���B�֐��̒��ŕ������]������B
        moto_honsya['can_weight'] = moto_honsya.apply(get_can_weight,axis=1)
        
        #�d�ʂ����߂�
        moto_honsya['weight'] = (moto_honsya['ireme'] \
                + moto_honsya['can_weight']) * moto_honsya['cans']
        
        #���l����A�[��8/3�@�̕��������𔲂��o��
        moto_honsya['�[��'] = moto_honsya.loc[:,'���l'].str.extract \
                (r'([1-9][0-2]?/[1-9][0-9]?)')

        #���l����y�C�o�ׁA�{�Џo�ׁA��㒼���@�𔲂��o��
        moto_honsya['�o��'] = moto_honsya.loc[:,'���l'].str.extract \
                (r'(�y�C�o��|�{�Џo��|��㒼��|�c�Ǝ��Q)')

        #��㒼���A�c�Ǝ��Q�̏ꍇ�͉^���v�Z���Ȃ��悤�Ɂu�[���於�̂P�v��
        #�unoCalc�v�ɕύX���Ă���
        moto_honsya.loc[(moto_honsya['�o��']=='��㒼��')|(moto_honsya['�o��']
            =='�c�Ǝ��Q'),'�[���於�̂P'] = 'noCalc'
        
        moto_honsya= moto_honsya.rename(columns= {'���l.1':'�󒍎��^��n��'})

        # �o�ח\��q�ɂ̗��[]�ɂ���B���̂����łȂ��Ƃ��܂������Ȃ������B
        moto_honsya['�o�ח\��q��'] = moto_honsya.apply(lambda x: [], axis=1) 
        
        #���m�^�����v�Z�ǉ�����
        toyo_untin = Toyo_untin(moto_honsya)
        moto_honsya = toyo_untin.get_toyoUntin()
        del toyo_untin

        

        self.moto_honsya = moto_honsya.copy()
        #moto_honsya�͑��ڋq���������{�ЁA�y�C�o�ו��̌��f�[�^




    def get_honsya_moto(self):
        honsya_moto = self.moto_honsya[self.moto_honsya['���l'].str.match \
                (r'^.*�{�Џo��.*$',na=True)]
        return honsya_moto

    def get_toke_moto(self):
        toke_moto = self.moto_honsya[self.moto_honsya['���l'].str.match\
                (r'^(?!.*�{�Џo��).*$', na=True)]
        toke_moto = toke_moto.fillna({'�o��':''})
        toke_moto['�o��'] = toke_moto['�o��'].map(lambda x : '�y�C�o��' 
                                                      if x == ''  else x ) 
        return toke_moto


    def get_untin_toke(self):
        toke_moto = self.get_toke_moto()

        if toke_moto.shape[0] == 0: 
            pass
        else:
            tokeMoto = toke_moto.groupby('�[���於�̂P',as_index=False) \
                    [['weight','cans']].sum()

            #toke_moto�������Ă���u���Ӑ�R�[�h�v�A�u�[����R�[�h�v����������
            toke_moto_code = toke_moto[['�[���於�̂P','���Ӑ�R�[�h',
                                        '�[����R�[�h']]
            #�_�u��𖳂����Ă����K�{
            toke_moto_code = toke_moto_code.drop_duplicates(['�[���於�̂P']) 
            tokeMoto = pd.merge(tokeMoto, toke_moto_code, how='left', 
                                on='�[���於�̂P')
            
            unsoutaiou_toke = Unsoutaiou_toke()
            tokeMoto_add_unsoutaiou = unsoutaiou_toke.add_unsoutaiou(tokeMoto)
            


            del unsoutaiou_toke

            untin_toke = Untin_toke()
            #apply��df���Ǝw�肷��΁A�e�s���Ɗ֐��ɓn����B�����̖߂�l�́A
            #Series�ɂ��ĕԂ��B�֐���Unsou_toke�׽��get_untinҿ��ށB
            tokeMoto_add_unsoutaiou[['İ�','�V��','����','��Ѝ��z']] =  \
                    tokeMoto_add_unsoutaiou.apply(untin_toke.get_untin, axis=1)

            del untin_toke
        
        return tokeMoto_add_unsoutaiou

		

    def get_untin_honsya(self):
        honsya_moto = self.get_honsya_moto()
        
        if honsya_moto.shape[0] == 0:
            pass
        else:
            honsyaMoto = honsya_moto.groupby('�[���於�̂P',as_index=False) \
                    [['weight','cans']].sum()
            
            #honsya_moto�������Ă���u���Ӑ�R�[�h�v�A�u�[����R�[�h�v����������
            honsya_moto_code = honsya_moto[['�[���於�̂P','���Ӑ�R�[�h',
                                            '�[����R�[�h']]
            #�_�u��𖳂����Ă����K�{
            honsya_moto_code = honsya_moto_code.drop_duplicates(['�[���於�̂P']) 
            honsyaMoto = pd.merge(honsyaMoto, honsya_moto_code, how='left', 
                                  on='�[���於�̂P')
            
            unsoutaiou_honsya = Unsoutaiou_honsya()
            honsyaMoto_add_unsoutaiou = unsoutaiou_honsya.add_unsoutaiou(honsyaMoto)

            del unsoutaiou_honsya

            untin_honsya = Untin_honsya()
            #apply��df���Ǝw�肷��΁A�e�s���Ɗ֐��ɓn����B�����̖߂�l�́A
            #Series�ɂ��ĕԂ��B�֐���Unsou_toke�׽��get_untinҿ��ށB
            honsyaMoto_add_unsoutaiou[['İ�','�V��','����','�v����','��Ѝ��z']] \
                    = honsyaMoto_add_unsoutaiou.apply(untin_honsya.get_untin, axis=1)

            del untin_honsya

        return honsyaMoto_add_unsoutaiou

