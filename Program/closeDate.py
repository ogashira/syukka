#! python
# -*- coding: cp932 -*-

from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta
import csv
import pandas as pd


class CloseDate:

    def __init__(self):
        
        tokuisaki_file = open('../master/effitA/tokuisaki.csv',encoding='cp932')
        file_reader = csv.reader(tokuisaki_file)
        tokuisaki = list(file_reader)
        tokuisaki_file.close()
        
        del tokuisaki[0:2]

        self.closeDate = {}
        for line in tokuisaki:
            if line[0] >= 'T6000':
                break
            else:
                self.closeDate[line[0]] = line[8]
        #self.closeDate : {'T1060':'31', 'T1070':'20' .......}


    def get_closeDate(self, df_row):
        
        tokuisakiCode = df_row['���Ӑ�R�[�h']
        syukkabi = str(df_row['�o�ח\���'])
        nouki = str(df_row['�[��'])


        syukkabi_Y = syukkabi[0:4] #�o�ד��̔N string
        syukkabi_M = syukkabi[4:6] #�o�ד��̌� string
        syukkabi_D = syukkabi[6:]  #�o�ד��̓� string

        # nouki_M = nouki.split('/')[0]  #�[���̌� string
        # nouki_D = nouki.split('/')[1]  #�[���̓� string
        nouki_M = nouki[4:6]
        nouki_D = nouki[6:]
        nouki_Y = nouki[:4]

        '''
        #nouki_Y�����߂�
        if int(syukkabi_M) == 12 and int(nouki_M) == 1:
            nouki_Y = str(int(syukkabi_Y) + 1)
        else:
            nouki_Y = syukkabi_Y
        '''

        # �o�ד��Ɣ[���̔N���������߂� 
        syukkabi_YMD = syukkabi_Y + '/' + syukkabi_M + '/' + syukkabi_D
        nouki_YMD = nouki_Y + '/' + nouki_M + '/' + nouki_D
        nouki = datetime.strptime(nouki_YMD, '%Y/%m/%d')
        nouki_YMD = nouki.strftime('%Y/%m/%d')  # nouki_YMD���@**/**/** �ɂ���


        close_D = self.closeDate[tokuisakiCode]  #���߂̓�


        # nouki �́@datetaime 
        if close_D == '31':  #���߂�31�Ȃ�[���̌��̖���
            close = (nouki + relativedelta(months=1)).replace(day=1)  \
            - timedelta(days=1)
        elif close_D == '1':  #���߂�1���Ȃ�A
            if nouki_D =='1':
                close = nouki  #�[����1���Ȃ�A�[���Ɠ������A
            else:                   #����ȊO�́A�[���̗�����1��
                close = (nouki + relativedelta(months=1)).replace(day=1) 
        else: 
            #���߂�1���ł�31���ł��Ȃ��ꍇ�́A
            #���ߓ����[�����ȏゾ������A�[���̌��̒��ߓ��A
            if int(close_D) - int(nouki_D) >= 0 :  
                close = nouki.replace(day= int(close_D))
            else:
                #���ߓ��̕���������������A�[���̗����̒��ߓ��B                                   
                close = (nouki + relativedelta(months=1)).replace(day= int(close_D))
                
        week = datetime.strptime(nouki_YMD, '%Y/%m/%d').weekday()
        w_list = ['��','��','��','��','��','�y','��']
        weekDay = w_list[week]
        close = close.strftime('%Y/%m/%d')

        return pd.Series([syukkabi_YMD, nouki_YMD, weekDay, close])



    def get_jikai(self, df_row):
        
        tokuisakiCode = df_row['���Ӑ�R�[�h']
        syukkabi_YMD = str(df_row['�o�ח\���'])
        closeDate_YMD = df_row['closeDate']
        syukkaYoteiSouko = []


        syukkabi_Y = syukkabi_YMD.split('/')[0] #�o�ד��̔N string
        syukkabi_M = syukkabi_YMD.split('/')[1] #�o�ד��̌� string
        syukkabi_D = syukkabi_YMD.split('/')[2]   #�o�ד��̓� string


        close_D = self.closeDate[tokuisakiCode]  #���߂̓�


        
        closeDate = datetime.strptime(closeDate_YMD, '%Y/%m/%d')
        syukkabi = datetime.strptime(syukkabi_YMD, '%Y/%m/%d')
        if close_D == '31':  #���߂�31�Ȃ�o�ד��̌��̖���
            effit_close = (syukkabi + relativedelta(months=1)).replace(day=1)  \
            - timedelta(days=1)
        elif close_D == '1':  #���߂�1���Ȃ�A
            if syukkabi_D =='1':
                effit_close = syukkabi  #�o�ד���1���Ȃ�A�o�ד��Ɠ������A
            else:                   #����ȊO�́A�o�ד��̗�����1��
                effit_close = (syukkabi + relativedelta(months=1)).replace(day=1) 
        else: 
            #���߂�1���ł�31���ł��Ȃ��ꍇ�́A
            #���ߓ����o�ד��ȏゾ������A �o�ד��̌��̒��ߓ��A
            if int(close_D) - int(syukkabi_D) >= 0 :  
                effit_close = syukkabi.replace(day= int(close_D))
            else:
                #���ߓ��̕���������������A�o�ד��̗����̒��ߓ��B                                   
                effit_close = (syukkabi + relativedelta(months=1)).replace(day= int(close_D))
                
        if closeDate != effit_close:
            syukkaYoteiSouko.append('��')

        return syukkaYoteiSouko


