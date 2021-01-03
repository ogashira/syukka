#! python
# -*- coding: cp932 -*-


import pyautogui 
import subprocess 
import time 
import pyperclip
import numpy as np
import pandas as pd

from recorder import Recorder




class EffitA(object):


    def __init__(self, myfolder):
        self.myfolder = myfolder


    def launch_effitA(self):
        '''
        effitA�̃��C����ʂɂȂ������͕K���A�u�󒍏o�׏����v���������
        �_�̏�ԂɂȂ��Ă���悤�ɂ���B
        '''
        pyautogui.PAUSE = 1
        subprocess.Popen(r'//192.168.1.245/effit_A/Menu/EMN300I.exe toyo_user' \
                         r',���YC10,1,admin,���m�H�Ɠh��')
        time.sleep(10)
        
        pyautogui.typewrite('honsya')
        pyautogui.typewrite(['enter'])
        pyautogui.typewrite('tajiri')
        pyautogui.typewrite(['enter', 'enter'])
        
        time.sleep(3)
        
        myclc = pyautogui.locateOnScreen \
            (r'../png_file/effita_png/caps_error.png')
        time.sleep(3)
        
        if myclc != None:
            pyautogui.typewrite(['capslock'])
            pyautogui.typewrite(['enter'])
            pyautogui.typewrite(['tab','tab'])
            pyautogui.typewrite('honsya')
            pyautogui.typewrite(['enter'])
            pyautogui.typewrite('tajiri')
            pyautogui.typewrite(['enter', 'enter'])  
        
        time.sleep(3)
        
        myclc = pyautogui.locateOnScreen(r'../png_file/effita_png/�󒍏o�׏���_�_��.png')
        time.sleep(3)
        if myclc != None:
            clc_cent = pyautogui.center(myclc)
            pyautogui.click(clc_cent)
        else:
            myclc2 = pyautogui.locateOnScreen(r'../png_file/effita_png/�󒍏o�׏���_��.png')
            time.sleep(3)
            if myclc2 != None:
                clc_cent2 = pyautogui.center(myclc2)
                pyautogui.click(clc_cent2)
            else:
                myclc3 = pyautogui.locateOnScreen(r'../png_file/effita_png/�󒍏o�׏���.png')
                time.sleep(3)
                if myclc3 != None:
                    clc_cent3 = pyautogui.center(myclc3)
                    pyautogui.click(clc_cent3)
    

    def close_effitA(self):
        myclc = pyautogui.locateOnScreen(r'../png_file/effita_png/syuuryou.png')
        time.sleep(3)
        clc_cent = pyautogui.center(myclc)
        pyautogui.click(clc_cent)
        time.sleep(1)
        

    def launch_DBmanager2(self):
        myclc = pyautogui.locateOnScreen \
            (r'../png_file/effita_png/system_kanri.png')
        time.sleep(3)
        clc_cent = pyautogui.center(myclc)
        pyautogui.click(clc_cent)
        time.sleep(5)
        
        myclc = pyautogui.locateOnScreen \
            (r'../png_file/dbmanager2_png/dbmanager2.png')
        time.sleep(3)
        clc_cent = pyautogui.center(myclc)
        pyautogui.click(clc_cent)
        time.sleep(10)


    def close_DBmanager2(self):
        myclc = pyautogui.locateOnScreen(r'../png_file/dbmanager2_png/csv_syuuryou.png')
        time.sleep(5)
        clc_cent = pyautogui.center(myclc)
        pyautogui.click(clc_cent)
        time.sleep(1)
        
        myclc = pyautogui.locateOnScreen(r'../png_file/effita_png/�󒍏o�׏���.png')
        time.sleep(3)
        if myclc != None:
            clc_cent = pyautogui.center(myclc)
            pyautogui.click(clc_cent)
        else:
            myclc2 = pyautogui.locateOnScreen(r'../png_file/effita_png/�󒍏o�׏���_��.png')
            time.sleep(3)
            clc_cent2 = pyautogui.center(myclc2)
            pyautogui.click(clc_cent2)
            time.sleep(1)



    def dl_DBmanager2(self, file_name, *args):
        '''
        csv�̃_�E�����[�h����file�ۑ��܂ōs��
        *args: yokujitu �܂��́Asengetu, honjitu �Ȃǂ�DBmanager2�ɓn�����t������
        fils_name: �^���v�Z���_���Ȃǂ�filename�B���̈�������ۑ�����file����
        pyautogui��png�f�[�^��file�����w�肷��B
        '''

        def pattern_untinKeisanSheet(file_name, yokujitu):
            # �^���v�Z���_���̏ꍇ�̒��o����
            pyautogui.typewrite(['tab','tab','delete'])
            pyautogui.typewrite(yokujitu)
            time.sleep(3)


        def pattern_jutyuuDT(file_name, sengetu, honjitu):
            # ��DT�̏ꍇ�̒��o����
            pyautogui.typewrite(['tab','tab','delete'])
            pyautogui.typewrite(sengetu) 
            pyautogui.typewrite(['tab','tab','tab','tab','tab','tab','delete'])
            pyautogui.typewrite(honjitu)
            time.sleep(3)



        
        
        myclc = pyautogui.locateOnScreen \
            (r'../png_file/dbmanager2_png/hozonsagyou_yobidasi.png')
        time.sleep(10)
        clc_cent = pyautogui.center(myclc)
        pyautogui.click(clc_cent)
        time.sleep(5)
        
        myclc = pyautogui.locateOnScreen \
                (r'../png_file/dbmanager2_png/{}.png'.format(file_name))
        time.sleep(3)
        clc_cent = pyautogui.center(myclc)
        pyautogui.click(clc_cent)
        time.sleep(1)

        myclc = pyautogui.locateOnScreen \
            (r'../png_file/dbmanager2_png/sentaku.png')
        time.sleep(3)
        clc_cent = pyautogui.center(myclc)
        pyautogui.click(clc_cent)
        time.sleep(1)
        
        myclc = pyautogui.locateOnScreen \
            (r'../png_file/dbmanager2_png/sentaku_ok.png')
        time.sleep(3)
        clc_cent = pyautogui.center(myclc)
        pyautogui.click(clc_cent)
        time.sleep(1)
        
        myclc = pyautogui.locateOnScreen \
            (r'../png_file/dbmanager2_png/tugihe.png')
        time.sleep(3)
        clc_cent = pyautogui.center(myclc)
        pyautogui.click(clc_cent)
        time.sleep(20)
        
        
        # dbmanager2�̒��o������file���ɂ���ĕ��򂷂�B
        if file_name == '�^���v�Z���_��':
            pattern_untinKeisanSheet(file_name, args[0])
        elif file_name == '��DT':
            pattern_jutyuuDT(file_name, args[0], args[1])


        
        myclc = pyautogui.locateOnScreen \
            (r'../png_file/dbmanager2_png/jikkou.png')
        time.sleep(3)
        clc_cent = pyautogui.center(myclc)
        pyautogui.click(clc_cent)
        time.sleep(5)
        
        pyautogui.typewrite('y')
        time.sleep(5)
        
        myclc = pyautogui.locateOnScreen \
            (r'../png_file/dbmanager2_png/csv_syuturyoku.png')
        time.sleep(3)
        clc_cent = pyautogui.center(myclc)
        pyautogui.click(clc_cent)
        time.sleep(1)


        pyautogui.typewrite(['delete'])
        pyperclip.copy(r'C:\Users\toyo\Documents\syukka' \
                       r'\master\effitA\{}.csv'.format(file_name))
        # pyperclip.copy(r'C:\Users\toyo\Documents\syukka' \
                       # r'\program\{}.csv'.format(file_name))
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(1)
        pyautogui.typewrite(['enter'])
        pyautogui.typewrite(['y'])
        pyautogui.typewrite(['enter'])
        time.sleep(1)



        myclc = pyautogui.locateOnScreen(r'../png_file/dbmanager2_png/�߂�.png')
        time.sleep(3)
        clc_cent = pyautogui.center(myclc)
        pyautogui.click(clc_cent)
        time.sleep(1)

        myclc = pyautogui.locateOnScreen(r'../png_file/dbmanager2_png/�߂�(����).png')
        time.sleep(3)
        clc_cent = pyautogui.center(myclc)
        pyautogui.click(clc_cent)
        time.sleep(1)



    def dl_zaiko(self):
        # effitA �g�b�v��ʂ̏�Ԃ���

        myclc = pyautogui.locateOnScreen(r'../png_file/effita_png/���݌�.png')
        time.sleep(3)
        clc_cent = pyautogui.center(myclc)
        pyautogui.click(clc_cent)
        time.sleep(5)


        pyautogui.typewrite('@0001')
        pyautogui.typewrite(['enter','enter'])
        time.sleep(5)
        pyautogui.typewrite(['up','tab','tab','tab','tab','tab','tab','tab',
                             'right','tab','tab','tab','tab','tab','enter'])
        time.sleep(3)
        pyautogui.typewrite(['delete'])
        pyautogui.typewrite(r'C:\Users\toyo\Documents\syukka\master\effitA\zaiko.csv')
        time.sleep(1)
        pyautogui.typewrite(['enter'])
        pyautogui.typewrite(['y'])
        pyautogui.typewrite(['enter'])
        time.sleep(2)
        pyautogui.typewrite(['tab','tab','tab','tab','tab','tab','tab','enter'])

        myclc = pyautogui.locateOnScreen(r'../png_file/effita_png/�󒍏o�׏���.png')
        time.sleep(3)
        if myclc != None:
            clc_cent = pyautogui.center(myclc)
            pyautogui.click(clc_cent)
        else:
            myclc2 = pyautogui.locateOnScreen(r'../png_file/effita_png/�󒍏o�׏���_��.png')
            time.sleep(3)
            clc_cent2 = pyautogui.center(myclc2)
            pyautogui.click(clc_cent2)
            time.sleep(1)


    def launch_uriage_nyuuryoku(self, factory):
        myclc = pyautogui.locateOnScreen(r'../png_file/effita_png/�������.png')
        time.sleep(3)
        if myclc != None:
            clc_cent = pyautogui.center(myclc)
            pyautogui.click(clc_cent)
            time.sleep(10)
        else:
            myclc2 = pyautogui.locateOnScreen(r'../png_file/effita_png/�������_���_.png')
            time.sleep(3)
            clc_cent2 = pyautogui.center(myclc2)
            pyautogui.click(clc_cent2)
            time.sleep(10)


        if factory == 'toke':
            pyautogui.typewrite('@0002')
        else:
            pyautogui.typewrite('@0001')
        pyautogui.typewrite(['enter','enter'])
        time.sleep(7)



    def close_uriage_nyuuryoku(self):
        myclc = pyautogui.locateOnScreen(r'../png_file/uriage_nyuuryoku/�I��.png')
        time.sleep(3)
        clc_cent = pyautogui.center(myclc)
        pyautogui.click(clc_cent)
        time.sleep(1)
        




    def uriage_nyuuryoku(self, untinForUriage):
        pyautogui.PAUSE = 1
        recorder = Recorder(self.myfolder)
        unsou_dic = {'İ�':'U0001', '�V��':'U0009', '���S':'U0002', 
                     '���Z':'U0003', '���':'U0004', '���R':'U0006', 
                     '�z�B':'U0008', '����':'U0010', '����':'U0007', 
                     '�v����':'U0005'}
        
        haisou_kubun = {'�ʏ�': 1, '�y�j�z�B': 2, '�c�Ə�': 3, '�j���Ⴂ': 4, '�j���z�B': 5}

        souko_dic = {'�y�C�o��': 'S0021', '�{�Џo��': 'S0001'}
        
        # close_date��ύX���Ȃ����X�g�i�X�^�����[���Ӑ�R�[�h�j
        nonChange_list = ['T1031', 'T1032', 'T1034', 'T1035', 'T1037', 'T1039']


        for i in range(untinForUriage.shape[0]): 
            uriagebi = untinForUriage.loc[i, '�o�ח\���']
            tokuisaki_code = untinForUriage.loc[i, '���Ӑ�R�[�h']
            nounyuu_code = untinForUriage.loc[i, '�[����R�[�h']
            iraisaki = untinForUriage.loc[i, '�˗���']
            bikou = untinForUriage.loc[i, '���l']
            syukka_yotei_souko = untinForUriage.loc[i, '�o�ח\��q��']
            jutyuu_no = untinForUriage.loc[i, '�󒍂m�n']
            jutyuugyou_no = str(untinForUriage.loc[i, '�󒍍s�m�n'])
            tokuisaki_no = untinForUriage.loc[i, '���Ӑ撍���m�n']
            jutyuu_hinban = untinForUriage.loc[i, '�i��']
            real_hinban = untinForUriage.loc[i, 'hinban']
            nouki = untinForUriage.loc[i, '�[��']
            yusyutu = untinForUriage.loc[i, '�A�o����']
            syukka_souko = untinForUriage.loc[i, '�o��']
            week = untinForUriage.loc[i, '�j��']
            close_date = untinForUriage.loc[i, 'closeDate']
            hikiate = untinForUriage.loc[i, 'lot']

            # npNan : �^���Ή��\�ɔ[���於�̂��ڂ��Ă��Ȃ�
            if iraisaki == 'NoCalc' or iraisaki == 'npNan' or iraisaki == 'NoData' or hikiate == {} \
                    or 'short' in hikiate.keys():
                txt = '��No:{}, �i��:{} �̔�����͕s�ł��B' \
                        .format(jutyuu_no, jutyuu_hinban)
                recorder.out_log(txt)
                recorder.out_file(txt)
                continue

            # �o�^�{�^������ 
            myclc = pyautogui.locateOnScreen(r'../png_file/uriage_nyuuryoku/�o�^.png')
            time.sleep(5)
            if myclc != None:
                clc_cent = pyautogui.center(myclc)
                pyautogui.click(clc_cent)
                time.sleep(1)
            else:
                myclc2 = pyautogui.locateOnScreen(r'../png_file/uriage_nyuuryoku/�o�^_��.png')
                time.sleep(3)
                clc_cent2 = pyautogui.center(myclc2)
                pyautogui.click(clc_cent2)
                time.sleep(1)

            # �}�E�X�J�[�\����(0, 0)�ɓ������Ă���
            pyautogui.moveRel(0, 20)


            # �����
            pyautogui.typewrite(['delete'])
            pyautogui.typewrite(uriagebi)
            pyautogui.typewrite(['enter'])
            # ����敪  
            pyautogui.typewrite(['delete'])
            pyautogui.typewrite('01')
            #pyperclip.copy('01')
            #pyautogui.hotkey('ctrl', 'v')
            time.sleep(1)
            pyautogui.typewrite(['enter'])
            # ���Ӑ�  
            pyautogui.typewrite(['delete'])
            pyautogui.typewrite(tokuisaki_code)
            pyautogui.typewrite(['enter'])
            # �[����  
            if pd.isnull(nounyuu_code):
                pyautogui.typewrite(['enter'])
            else:
                pyautogui.typewrite(['delete'])
                pyautogui.typewrite(nounyuu_code)
                pyautogui.typewrite(['enter'])
            # �^���Ǝ�  
            pyautogui.typewrite(['delete'])
            pyautogui.typewrite(unsou_dic[iraisaki])
            pyautogui.typewrite(['enter'])
            # �z���敪  
            if '�c�Ə�' in syukka_yotei_souko: 
                pyautogui.typewrite(['delete'])
                pyautogui.typewrite('3')
                pyautogui.typewrite(['enter'])
                pyautogui.hotkey('shift', 'tab')
            elif '�y�j�z�B' in syukka_yotei_souko:
                pyautogui.typewrite(['delete'])
                pyautogui.typewrite('2')
                pyautogui.typewrite(['enter'])
                pyautogui.hotkey('shift', 'tab')
            elif '�j��' in syukka_yotei_souko:
                pyautogui.typewrite(['delete'])
                pyautogui.typewrite('4')
                pyautogui.typewrite(['enter'])
                pyautogui.hotkey('shift', 'tab')
            else:
                pyautogui.typewrite(['delete'])
                pyautogui.typewrite('1')
                pyautogui.typewrite(['enter'])
                pyautogui.hotkey('shift', 'tab')

            # �����\���  
            # ���Ӑ悪�X�^�����[�̏ꍇ��close_date�͕ύX���Ȃ�
            if tokuisaki_code in nonChange_list:
                pyautogui.typewrite(['enter'])
            else:
                pyautogui.typewrite(['delete'])
                pyautogui.typewrite(close_date)
                pyautogui.typewrite(['enter'])


            # �o�בq��  
            pyautogui.typewrite(['delete'])
            pyautogui.typewrite(souko_dic[syukka_souko])
            pyautogui.typewrite(['enter'])
            
            
            
            # ��No  
            pyautogui.typewrite(['delete'])
            pyautogui.typewrite(jutyuu_no)
            pyautogui.typewrite(['enter'])

            # �󒍍sNo  
            pyautogui.typewrite(['delete'])
            pyautogui.typewrite(jutyuugyou_no)
            pyautogui.typewrite(['enter']) 
             
            myclc = pyautogui.locateOnScreen(r'../png_file/uriage_nyuuryoku/���[��.png')
            time.sleep(8)
            if myclc != None:
                pyautogui.typewrite(['enter'])
                txt = '{}:{}�͊��[�ςł�'.format(jutyuu_no, jutyuu_hinban)
                recorder.out_log(txt)
                recorder.out_file(txt)
                time.sleep(3)
                continue 

            myclc = pyautogui.locateOnScreen(r'../png_file/uriage_nyuuryoku/�o�^�Ȃ�.png')
            time.sleep(5)
            if myclc != None:
                pyautogui.typewrite(['enter'])
                txt = '{}:{}�͓o�^�Ȃ��ł�'.format(jutyuu_no, jutyuu_hinban)
                recorder.out_log(txt)
                recorder.out_file(txt)
                time.sleep(3)
                continue 

            # lot             
            pyautogui.typewrite(['enter', 'enter', 'enter', 'enter', 
                                 'enter', 'enter', 'enter']) 
            for lot, cans in hikiate.items():
                pyautogui.typewrite(lot)
                pyautogui.typewrite(['delete'])
                pyautogui.typewrite(['enter'])
                pyautogui.typewrite(str(cans))
                pyautogui.typewrite(['delete'])
                pyautogui.typewrite(['enter'])
                time.sleep(3)
                
            # ok test���ͷ�ݾ�
            myclc = pyautogui.locateOnScreen(r'../png_file/uriage_nyuuryoku/ok.png')
            time.sleep(3)
            clc_cent = pyautogui.center(myclc)
            pyautogui.click(clc_cent)

                
        
            

            











