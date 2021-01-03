#! python
# -*- coding: cp932 -*-

import pandas as pd
import numpy as np
from closeDate import *
from zaiko import *
from add_data import *
from recorder import *
from lead_time import *


pd.set_option('display.max_columns', None)



class Ajust_toke:

    def __init__ (self, myfolder):
        self.myfolder = myfolder

    def get_allHauler(self, moto, untin):

        def best_hauler(row):
            nounyuusaki = row['�[���於�̂P']
            sitei = row['�ڋq�w��^����']
            address = row['�Z���P']
            torr = row['İ�']
            niigata = row['�V��']
            keihin = row['����']

            dic = {'İ�':float(torr), '�V��':float(niigata), '����':float(keihin)}
            
            #�ڋq�w��^����������ꍇ�̓\���A�����ꍇ�͍ň��l�̉^������I��
            #�ň��l���Q�ȏ゠��ꍇ���l�����āA���X�g����\�L�ŋ��߂�B
            if address == 'NoCalc':
                best_hauler = ['�z�B']
            elif address is np.nan:
                best_hauler = ['npNan']
            elif sitei != '����' and sitei != '��':
                best_hauler = [sitei]
            else:
                best_hauler = [kv[0] for kv in dic.items() if kv[1] == 
                               min(dic.values())]
            
            return best_hauler


        syukkabi = moto.iloc[0,5]

        untin['�˗���'] = untin.apply(best_hauler, axis=1) 
        untin['�o�ח\���'] = syukkabi

        allHauler = untin[['�o�ח\���','�Z���P','�[���於�̂P','���Ӑ�R�[�h',
                           '�[����R�[�h','weight','cans','İ�','�V��','����',
                           '��Ѝ��z','�˗���','�A�o����']]



        # �˗����list�����e�����ɂ��Ă���
        allHauler2 = allHauler.copy()
        allHauler2.loc[:,'�˗���'] = allHauler2['�˗���'].map(lambda x : x[0])
        allHauler_sort = allHauler2.sort_values('�˗���')

        return allHauler_sort


    def get_packingHinban(self, moto, allHauler):
        
        allHauler = allHauler[['�Z���P','�˗���','�A�o����']]
        moto_addHinban = pd.merge(moto, allHauler, how= 'left', on='�Z���P')
        packingHinban = moto_addHinban[['�o�ח\���','�˗���','cans','weight',
                                        '���Ӑ�R�[�h','�[����R�[�h',
                                        '�[���於�̂P', 'hinban', '�i��','�󒍐���',
                                        '�󒍒P��','���Ӑ撍���m�n','���l','�o��',
                                        '�o�ח\��q��','�A�o����','�[��', '�󒍂m�n',
                                        '�󒍍s�m�n','add']]
        
        # �^�����i�˗���j��NaN�̏ꍇ��No data�ɂ���>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

        packingHinban = packingHinban.fillna({'�˗���':'NoData'})

        

        # ���񐿋������߂�>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        closeDate = CloseDate()

        packingHinban2 = packingHinban.copy() 
        packingHinban2[['�o�ח\���','�[��','�j��','closeDate']] = \
        packingHinban2.apply(closeDate.get_closeDate, axis=1)

        packingHinban3 = packingHinban2.copy()
        packingHinban3.loc[:,'�o�ח\��q��'] = packingHinban3.apply(
            closeDate.get_jikai, axis = 1)


        # ���A�w�����߂�<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

        add_data = AddData()
        
        packingHinban3.loc[:,'�o�ח\��q��'] = packingHinban3.apply(
                  add_data.get_coa, axis = 1)

        
        del add_data
        # �j���Ⴂ�����߂�<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

        lead_time = LeadTime()

        packingHinban3.loc[:,'�o�ח\��q��'] = packingHinban3.apply(
                lead_time.get_youbi, axis = 1)

        del lead_time
        #  �y�j�z�B�𔻒�<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

        def get_dohai(df_row):
            syukka_souko = df_row['�o�ח\��q��']
            week = df_row['�j��']

            if week == '�y':
                syukka_souko.append('�y�j�z�B')
            return syukka_souko


        packingHinban3.loc[:, '�o�ח\��q��'] = packingHinban3.apply(
                get_dohai, axis = 1)
        


        #  �c�Ə��~�߂𔻒�<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

        def get_siten_tome(df_row):
            syukka_souko = df_row['�o�ח\��q��']
            bikou = df_row['���l']

            if bikou.find('�x�X�~��') >= 0 or bikou.find('�x�X�ǂ�') >= 0 or \
                bikou.find('�c�Ə��~��') >= 0 or bikou.find('�c�Ə��ǂ�') >= 0 :
                syukka_souko.append('�c�Ə�')
            return syukka_souko


        packingHinban3.loc[:, '�o�ח\��q��'] = packingHinban3.apply(
                get_siten_tome, axis = 1)



        return packingHinban3

        
    def get_untinForUriage(self, moto, allHauler):
        allHauler = allHauler[['�Z���P','�˗���','�A�o����']]
        moto_addHauler = pd.merge(moto, allHauler, how= 'left', on='�Z���P')
        untinForUriage = moto_addHauler[['�o�ח\���','���Ӑ�R�[�h','�[����R�[�h',
                                         '�˗���','���l','�o�ח\��q��','�󒍂m�n',
                                         '�󒍍s�m�n','���Ӑ撍���m�n','�i��','hinban',
                                         'cans','�[��', 'toyo_untin','�A�o����','�o��','add']]


        # �^�����i�˗���j��NaN�̏ꍇ��No data�ɂ���>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

        untinForUriage = untinForUriage.fillna({'�˗���':'NoData'})

        # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

        closeDate = CloseDate()

        untinForUriage2 = untinForUriage.copy() 
        untinForUriage2[['�o�ח\���','�[��','�j��','closeDate']] = \
        untinForUriage2.apply(closeDate.get_closeDate, axis=1)

        del closeDate

        # �j���Ⴂ�����߂�<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

        lead_time = LeadTime()

        untinForUriage2.loc[:,'�o�ח\��q��'] = untinForUriage2.apply(
                lead_time.get_youbi, axis = 1)

        del lead_time
        # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
        
        zaiko = Zaiko(self.myfolder)
        recorder = Recorder(self.myfolder)
        
        txt ='���㏈�����͗p�ް��i�y�C�j' 
        recorder.out_log(txt, '\n')
        recorder.out_file(txt, '\n')

        untinForUriage2['lot'] = untinForUriage2.apply(zaiko.get_lot, axis=1)
        
        recorder.out_log('')
        recorder.out_file('')
        recorder.out_log(untinForUriage2, '\n')
        recorder.out_file(untinForUriage2, '\n')

        del zaiko
        del recorder



        return untinForUriage2


    def get_packingCoa(self, packingHinban, untinForUriage):
        lot_data = untinForUriage[['�󒍂m�n', '�󒍍s�m�n', 'lot']]
        packingCoa = pd.merge(packingHinban, lot_data, on =['�󒍂m�n', '�󒍍s�m�n'] 
                , how = 'left')

        packingCoa = packingCoa[[
            '�o�ח\���', '���Ӑ�R�[�h', '�[����R�[�h', '�[���於�̂P', 
            'hinban', '�o��', '�󒍂m�n', '�󒍍s�m�n', 'lot'
        ]]

        return packingCoa
        




class Ajust_honsya:


    def __init__ (self, myfolder):
        self.myfolder = myfolder


    def get_allHauler(self, moto, untin):

        def best_hauler(row):
            nounyuusaki = row['�[���於�̂P']
            sitei = row['�ڋq�w��^����']
            address = row['�Z���P']
            torr = row['İ�']
            niigata = row['�V��']
            keihin = row['����']
            kurume = row['�v����']


            dic = {'İ�':float(torr), '�V��':float(niigata), '����':float(keihin), '�v����':float(kurume)}
            
            #�ڋq�w��^����������ꍇ�̓\���A�����ꍇ�͍ň��l�̉^������I��
            #�ň��l���Q�ȏ゠��ꍇ���l�����āA���X�g����\�L�ŋ��߂�B
            if address == 'NoCalc':
                best_hauler = ['NoCalc']
            elif address is np.nan:
                best_hauler = ['npNan']
            elif sitei != '����':
                best_hauler = [sitei]
            else:
                best_hauler = [kv[0] for kv in dic.items() if kv[1] 
                               == min(dic.values())]
            
            return best_hauler


        syukkabi = moto.iloc[0,5]

        untin['�˗���'] = untin.apply(best_hauler, axis=1) 
        untin['�o�ח\���'] = syukkabi

        allHauler = untin[['�o�ח\���','�Z���P','�[���於�̂P','���Ӑ�R�[�h',
                           '�[����R�[�h','weight','cans','İ�','�V��','����',
                           '�v����','��Ѝ��z','�˗���','�A�o����']]

        # �˗����list�����e�����ɂ��Ă���
        allHauler2 = allHauler.copy()
        allHauler2.loc[:,'�˗���'] = allHauler2['�˗���'].map(lambda x : x[0])
        allHauler_sort = allHauler2.sort_values('�˗���')


        return allHauler_sort




    def get_packingHinban(self, moto, allHauler):
        
        allHauler = allHauler[['�Z���P','�˗���','�A�o����']]
        moto_addHinban = pd.merge(moto, allHauler, how= 'left', on='�Z���P')
        packingHinban = moto_addHinban[['�o�ח\���', '�˗���','cans','weight','���Ӑ�R�[�h',
                                        '�[����R�[�h','�[���於�̂P', 'hinban', '�i��',
                                        '�󒍐���','�󒍒P��','���Ӑ撍���m�n',
                                        '���l','�o��','�o�ח\��q��','�A�o����',
                                        '�[��', '�󒍂m�n', '�󒍍s�m�n','add']]


        # �^�����i�˗���j��NaN�̏ꍇ��No data�ɂ���>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

        packingHinban = packingHinban.fillna({'�˗���':'NoData'})


        # ���񐿋������߂�>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        closeDate = CloseDate()

        packingHinban2 = packingHinban.copy() 
        packingHinban2[['�o�ח\���','�[��','�j��','closeDate']] = \
        packingHinban2.apply(closeDate.get_closeDate, axis=1)

        packingHinban3 = packingHinban2.copy()
        packingHinban3.loc[:,'�o�ח\��q��'] = packingHinban3.apply(
            closeDate.get_jikai, axis = 1)

        # ���A�w�����߂�<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

        add_data = AddData()
        
        packingHinban3.loc[:,'�o�ח\��q��'] = packingHinban3.apply(
                  add_data.get_coa, axis = 1)

        
        del add_data
        #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
        # �j���Ⴂ�����߂�<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

        lead_time = LeadTime()

        packingHinban3.loc[:,'�o�ח\��q��'] = packingHinban3.apply(
                lead_time.get_youbi, axis = 1)

        del lead_time
        # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
        #  �y�j�z�B�𔻒�<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

        def get_dohai(df_row):
            syukka_souko = df_row['�o�ח\��q��']
            week = df_row['�j��']

            if week == '�y':
                syukka_souko.append('�y�j�z�B')
            return syukka_souko

        packingHinban3.loc[:, '�o�ח\��q��'] = packingHinban3.apply(
                get_dohai, axis = 1)

        
        #  �c�Ə��~�߂𔻒�<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

        def get_siten_tome(df_row):
            syukka_souko = df_row['�o�ח\��q��']
            bikou = df_row['���l']

            if bikou.find('�x�X�~��') >= 0 or bikou.find('�x�X�ǂ�') >= 0 or \
                bikou.find('�c�Ə��~��') >= 0 or bikou.find('�c�Ə��ǂ�') >= 0 :
                syukka_souko.append('�c�Ə�')
            return syukka_souko


        packingHinban3.loc[:, '�o�ח\��q��'] = packingHinban3.apply(
                get_siten_tome, axis = 1)
        



        return packingHinban3



    def get_untinForUriage(self,moto, allHauler):
        allHauler = allHauler[['�Z���P','�˗���','�A�o����']]
        moto_addHauler = pd.merge(moto, allHauler, how= 'left', on='�Z���P')
        untinForUriage = moto_addHauler[['�o�ח\���','���Ӑ�R�[�h',
                                         '�[����R�[�h','�˗���','���l',
                                         '�o�ח\��q��','�󒍂m�n','�󒍍s�m�n',
                                         '���Ӑ撍���m�n','�i��','hinban',
                                         'cans','�[��', 'toyo_untin', '�A�o����','�o��','add']]

        # �^�����i�˗���j��NaN�̏ꍇ��No data�ɂ���>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

        untinForUriage = untinForUriage.fillna({'�˗���':'NoData'})

        # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<


        closeDate = CloseDate()

        untinForUriage2 = untinForUriage.copy() 
        untinForUriage2[['�o�ח\���','�[��','�j��','closeDate']] = \
                untinForUriage2.apply(closeDate.get_closeDate, axis=1)

        del closeDate

        # �j���Ⴂ�����߂�<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

        lead_time = LeadTime()

        untinForUriage2.loc[:,'�o�ח\��q��'] = untinForUriage2.apply(
                lead_time.get_youbi, axis = 1)

        del lead_time
        # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

        zaiko = Zaiko(self.myfolder)
        recorder = Recorder(self.myfolder)

        txt ='���㏈�����͗p�ް��i�{�Ёj' 
        recorder.out_log(txt, '\n')
        recorder.out_file(txt, '\n')

        untinForUriage2['lot'] = untinForUriage2.apply(zaiko.get_lot, axis=1)
        
        recorder.out_log('')
        recorder.out_file('')
        recorder.out_log(untinForUriage2, '\n')
        recorder.out_file(untinForUriage2, '\n')

        del zaiko
        del recorder
        

        return untinForUriage2



    def get_packingCoa(self, packingHinban, untinForUriage):
        lot_data = untinForUriage[['�󒍂m�n', '�󒍍s�m�n', 'lot']]
        packingCoa = pd.merge(packingHinban, lot_data, on =['�󒍂m�n', '�󒍍s�m�n'] 
                , how = 'left')

        packingCoa = packingCoa[[
            '�o�ח\���', '���Ӑ�R�[�h', '�[����R�[�h', '�[���於�̂P', 
            'hinban', '�o��', '�󒍂m�n', '�󒍍s�m�n', 'lot'
        ]]

        return packingCoa
