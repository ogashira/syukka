#! python
# -*- coding: cp932 -*-

import os
import pandas as pd


class UntinKeisanSheet(object):
    '''
    packing����untin_moto���󂯂āA�^���v�Z��Ă�add�񐔂�\������B
    �\��������A��no��add�������̫��ނɕۑ�����Bcreate_folder
    �����̫��ނ̒��ɁAsumi.csv�����݂��Ȃ���� cnt = 1
    sumi.csv�����݂���΁Acnt ��sumi.csv��add���max�Ƃ���
    '''

    def __init__(self, untin_moto):
        
        self.untin_moto = untin_moto
        self.uriage_day = str(untin_moto.loc[0, '�o�ח\���'])
        folder_name = self.uriage_day
        # ̫��ނ����݂��Ȃ���΍��i�o�ח\�����̫��ޖ��j
        if os.path.exists(r'../tmp/{}'.format(folder_name)):
            pass
        else:
            os.mkdir(r'../tmp/{}'.format(folder_name))


            
    def sheet_add_cnt(self):
        folder_name = self.uriage_day
        if os.path.exists(r'../tmp/{}/add_cnt.csv'.format(folder_name)):
            add_cnt = pd.read_csv(r'../tmp/{}/add_cnt.csv'.format(folder_name), 
                                                               encoding='cp932')
            cnt = add_cnt['add'].max()
            moto_add = pd.merge(self.untin_moto, add_cnt, 
                                  on = ['�󒍂m�n', '�󒍍s�m�n'], how = 'left')
            moto_add = moto_add.fillna({'add': cnt+1})
        else:
            cnt = 1
            moto_add = self.untin_moto.copy()
            moto_add['add'] = cnt

        moto_add_after = moto_add[['�󒍂m�n', '�󒍍s�m�n', 'add']]
        moto_add_after.to_csv(r'../tmp/{}/add_cnt.csv'.format(folder_name), 
                                                            encoding = 'cp932')




        return moto_add

    
