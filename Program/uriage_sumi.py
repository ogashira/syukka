#! python
# -*- coding: cp932 -*-

import pandas as pd
import datetime


class UriageSumi(object):
    
    def __init__ (self):

        uriage_sumi = pd.read_csv(
                r'../master/effitA/uriage_sumi.csv', 
                skiprows = 1,
                encoding='cp932'
        )
        uriage_sumi = uriage_sumi.rename(
                columns = {
                    '�����':'�o�ח\���',
                    '�^���Ǝ�':'�˗���',
                    '���R�g�p�敪�P':'�z���敪',
                    '�����\��N����':'closeDate',
                    '�Ǘ���':'�󒍐���',
                    '�Ǘ��P��':'�󒍒P��',
                    '�U�֌��i��':'hinban',
                    '�U�֌�����':'cans',
                    '���b�g�m�n':'lot',
                }
        )

        uriage_sumi['�o�ח\���'] = uriage_sumi['�o�ח\���'].map(
                lambda x : '{}/{}/{}'.format(str(x)[:4],str(x)[4:6],str(x)[6:])
        )
        uriage_sumi['closeDate'] = uriage_sumi['closeDate'].map(
                lambda x : '{}/{}/{}'.format(str(x)[:4],str(x)[4:6],str(x)[6:])
        )
        uriage_sumi['�[��'] = uriage_sumi['�[��'].map(
                lambda x : '{}/{}/{}'.format(str(x)[:4],str(x)[4:6],str(x)[6:])
        )

        self.uriage_sumi = uriage_sumi[uriage_sumi['���Ӑ�R�[�h'] < 'T6000']


    def get_uriage_sumi(self):
        '''
        self.uriage_sumi��'lot_dic'���ǉ�����{lot:cans}�̎����𓾂�
        ���ɁAself.uriage_sumi�͕���LOT�̏ꍇ��LOT���Ƃɍs������̂ŁA
        �d�������no�A�󒍍sno�ŁA{lot:cans, lot:cans} �̌`�ɂ܂Ƃ߂ĂP�s�ɂ���B
        '''

        def get_dic_lot (row):
            # {lot:cans}�̌`�ɂ���
            dic_lot = {}
            lot = row['lot']
            if pd.isnull(row['hinban']):
                cans = row['�󒍐���']
            else:
                cans = row['cans']
            dic_lot[lot] = cans
            return dic_lot

        uriage_sumi = self.uriage_sumi.copy()
        uriage_sumi['dic_lot'] = uriage_sumi.apply(get_dic_lot, axis=1)
        
        uriage_sumi = uriage_sumi.sort_values(['�󒍂m�n', '�󒍍s�m�n'])
        uriage_sumi = uriage_sumi.reset_index()

        
        for i in range(len(uriage_sumi)-1):
            JNo = uriage_sumi.loc[i, '�󒍂m�n']
            JGNo = uriage_sumi.loc[i, '�󒍍s�m�n']
            dic_lot = uriage_sumi.loc[i, 'dic_lot']
            j = 1
            while uriage_sumi.loc[i+j, '�󒍂m�n'] == JNo and (
                    uriage_sumi.loc[i+j, '�󒍍s�m�n'] == JGNo):
                add_dic_lot = uriage_sumi.loc[i+j, 'dic_lot']
                add_lot = [k for k, v in add_dic_lot.items()][0]
                add_cans = [v for k, v in add_dic_lot.items()][0]
                
                dic_lot[add_lot] = add_cans
                
                # .loc�ł̓G���[�ɂȂ�B������ؽĂ�������Ƃ���.at���g��
                # .loc�ł͕����I���̈Ӗ�������̂ŒP��Z�������I���ł��Ȃ�.at���g��
                uriage_sumi.at[i, 'dic_lot'] = dic_lot

                uriage_sumi.loc[i+j, '���Ӑ撍���m�n'] = 'del'

                # i+j���ŏI�s�ł�������while�𔲂���
                if i + j == len(uriage_sumi)-1:
                    break

                j += 1

        uriage_sumi2 = uriage_sumi.loc[uriage_sumi['���Ӑ撍���m�n'] != 'del', :]
                
        return uriage_sumi2


    def uriage_check(self, untinForUriage):

        uriage_sumi = self.get_uriage_sumi()
        UU = untinForUriage

        check_df = pd.merge(UU, uriage_sumi, on =['�󒍂m�n', '�󒍍s�m�n'], how = 'left')

        return check_df
