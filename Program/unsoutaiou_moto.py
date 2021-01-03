#! python
# -*- coding: cp932 -*-
import csv
import pandas as pd



class Unsoutaiou_toke :
    
    # [���Ə�����,����溰��,����於��1,�X�֔ԍ� ,�X�֔ԍ�2,�Z��1,İً���,�?
    #  İٍs���s���Ȃ�,�V������,�V�����p��,�V���s���s���Ȃ�,����,�ڋq�w��^����
    #  ,�A�o������,���Ӑ溰��,�[���溰��]
    
    def __init__(self):
        # dl_df = pd.read_csv(
        # r'\\192.168.1.247\���L\�o����̫���\�^���v�Z�֌W\unsoutaiou_toke.csv', 
        # encoding='cp932'
        # )
        dl_df = pd.read_csv(
                r'../master/untin/unsoutaiou_toke.csv',encoding='cp932'
        )


        self.unsoutaiou = dl_df.rename(columns={'����於�̂P':'�[���於�̂P'})

    def add_unsoutaiou(self, df):
        dup_unsoutaiou = self.unsoutaiou.drop_duplicates(['�[���於�̂P'])
        add_unsoutaiou = pd.merge(df,dup_unsoutaiou, on='�[���於�̂P'
                                  , how='left')
        return add_unsoutaiou
        
                

    




class Unsoutaiou_honsya :
    

    # [���Ə�����,����溰��,����於��1,�X�֔ԍ� ,�X�֔ԍ�2,�Z��1,İً�
    #  İٍs���s���Ȃ�,�V������,�V�����p��,�V���s���s���Ȃ�,����,�ڋq�w��^����,
    #  �A�o������,���Ӑ溰��,�[���溰��,�v���ċ���] �y�C�ɂ͋v���ċ������Ȃ��B

    def __init__(self):
        # dl_df = pd.read_csv(
        # r'\\192.168.1.247\���L\�o����̫���\�^���v�Z�֌W\unsoutaiou_honsya.csv', 
        # encoding='cp932'
        # )

        dl_df = pd.read_csv(
                r'../master/untin/unsoutaiou_honsya.csv',encoding='cp932'
        )

        self.unsoutaiou = dl_df.rename(columns={'����於�̂P':'�[���於�̂P'})

    def add_unsoutaiou(self, df):
        dup_unsoutaiou = self.unsoutaiou.drop_duplicates(['�[���於�̂P'])
        add_unsoutaiou = pd.merge(df, dup_unsoutaiou, on='�[���於�̂P'
                                  , how='left')
        return add_unsoutaiou
