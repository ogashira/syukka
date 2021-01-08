#! python
# -*- coding: utf-8 -*-


import pyautogui 
import subprocess 
import time 
import pyperclip
import numpy as np
import pandas as pd
import platform

from recorder import Recorder




class EffitA(object):


    def __init__(self, myfolder):
        self.myfolder = myfolder


    def launch_effitA(self):
        '''
        effitAのメイン画面になった時は必ず、「受注出荷処理」が押されて
        点青の状態になっているようにする。
        '''
        pyautogui.PAUSE = 1

        pf = platform.system()
        if pf == 'Windows':
            subprocess.Popen(r'//192.168.1.245/effit_A/Menu/EMN300I.exe toyo_user' \
                             r',生産C10,1,admin,東洋工業塗料')
        else:
            subprocess.Popen(r'/mnt/effitA/Menu/EMN300I.exe toyo_user' \
                             r',生産C10,1,admin,東洋工業塗料')
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
        
        myclc = pyautogui.locateOnScreen(r'../png_file/effita_png/受注出荷処理_点青.png')
        time.sleep(3)
        if myclc != None:
            clc_cent = pyautogui.center(myclc)
            pyautogui.click(clc_cent)
        else:
            myclc2 = pyautogui.locateOnScreen(r'../png_file/effita_png/受注出荷処理_青.png')
            time.sleep(3)
            if myclc2 != None:
                clc_cent2 = pyautogui.center(myclc2)
                pyautogui.click(clc_cent2)
            else:
                myclc3 = pyautogui.locateOnScreen(r'../png_file/effita_png/受注出荷処理.png')
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
        
        myclc = pyautogui.locateOnScreen(r'../png_file/effita_png/受注出荷処理.png')
        time.sleep(3)
        if myclc != None:
            clc_cent = pyautogui.center(myclc)
            pyautogui.click(clc_cent)
        else:
            myclc2 = pyautogui.locateOnScreen(r'../png_file/effita_png/受注出荷処理_青.png')
            time.sleep(3)
            clc_cent2 = pyautogui.center(myclc2)
            pyautogui.click(clc_cent2)
            time.sleep(1)



    def dl_DBmanager2(self, file_name, *args):
        '''
        csvのダウンロードからfile保存まで行う
        *args: yokujitu または、sengetu, honjitu などのDBmanager2に渡す日付文字列
        fils_name: 運賃計算ｼｰﾄ_改などのfilename。この引数から保存するfile名と
        pyautoguiのpngデータのfile名を指定する。
        '''

        def pattern_untinKeisanSheet(file_name, yokujitu):
            # 運賃計算ｼｰﾄ_改の場合の抽出条件
            pyautogui.typewrite(['tab','tab','delete'])
            pyautogui.typewrite(yokujitu)
            time.sleep(3)


        def pattern_jutyuuDT(file_name, sengetu, honjitu):
            # 受注DTの場合の抽出条件
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
        
        
        # dbmanager2の抽出条件をfile名によって分岐する。
        if file_name == '運賃計算ｼｰﾄ_改':
            pattern_untinKeisanSheet(file_name, args[0])
        elif file_name == '受注DT':
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



        myclc = pyautogui.locateOnScreen(r'../png_file/dbmanager2_png/戻る.png')
        time.sleep(3)
        clc_cent = pyautogui.center(myclc)
        pyautogui.click(clc_cent)
        time.sleep(1)

        myclc = pyautogui.locateOnScreen(r'../png_file/dbmanager2_png/戻る(太字).png')
        time.sleep(3)
        clc_cent = pyautogui.center(myclc)
        pyautogui.click(clc_cent)
        time.sleep(1)



    def dl_zaiko(self):
        # effitA トップ画面の状態から

        myclc = pyautogui.locateOnScreen(r'../png_file/effita_png/現在庫.png')
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

        myclc = pyautogui.locateOnScreen(r'../png_file/effita_png/受注出荷処理.png')
        time.sleep(3)
        if myclc != None:
            clc_cent = pyautogui.center(myclc)
            pyautogui.click(clc_cent)
        else:
            myclc2 = pyautogui.locateOnScreen(r'../png_file/effita_png/受注出荷処理_青.png')
            time.sleep(3)
            clc_cent2 = pyautogui.center(myclc2)
            pyautogui.click(clc_cent2)
            time.sleep(1)


    def launch_uriage_nyuuryoku(self, factory):
        myclc = pyautogui.locateOnScreen(r'../png_file/effita_png/売上入力.png')
        time.sleep(3)
        if myclc != None:
            clc_cent = pyautogui.center(myclc)
            pyautogui.click(clc_cent)
            time.sleep(10)
        else:
            myclc2 = pyautogui.locateOnScreen(r'../png_file/effita_png/売上入力_黒点.png')
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
        myclc = pyautogui.locateOnScreen(r'../png_file/uriage_nyuuryoku/終了.png')
        time.sleep(3)
        clc_cent = pyautogui.center(myclc)
        pyautogui.click(clc_cent)
        time.sleep(1)
        




    def uriage_nyuuryoku(self, untinForUriage):
        pyautogui.PAUSE = 1
        recorder = Recorder(self.myfolder)
        unsou_dic = {'ﾄｰﾙ':'U0001', '新潟':'U0009', '名鉄':'U0002', 
                     '西濃':'U0003', 'ﾄﾅﾐ':'U0004', '福山':'U0006', 
                     '配達':'U0008', '佐川':'U0010', 'ｹｲﾋﾝ':'U0007', 
                     '久留米':'U0005'}
        
        haisou_kubun = {'通常': 1, '土曜配達': 2, '営業所': 3, '曜日違い': 4, '祝日配達': 5}

        souko_dic = {'土気出荷': 'S0021', '本社出荷': 'S0001'}
        
        # close_dateを変更しないリスト（スタンレー得意先コード）
        nonChange_list = ['T1031', 'T1032', 'T1034', 'T1035', 'T1037', 'T1039']


        for i in range(untinForUriage.shape[0]): 
            uriagebi = untinForUriage.loc[i, '出荷予定日']
            tokuisaki_code = untinForUriage.loc[i, '得意先コード']
            nounyuu_code = untinForUriage.loc[i, '納入先コード']
            iraisaki = untinForUriage.loc[i, '依頼先']
            bikou = untinForUriage.loc[i, '備考']
            syukka_yotei_souko = untinForUriage.loc[i, '出荷予定倉庫']
            jutyuu_no = untinForUriage.loc[i, '受注ＮＯ']
            jutyuugyou_no = str(untinForUriage.loc[i, '受注行ＮＯ'])
            tokuisaki_no = untinForUriage.loc[i, '得意先注文ＮＯ']
            jutyuu_hinban = untinForUriage.loc[i, '品番']
            real_hinban = untinForUriage.loc[i, 'hinban']
            nouki = untinForUriage.loc[i, '納期']
            yusyutu = untinForUriage.loc[i, '輸出向先']
            syukka_souko = untinForUriage.loc[i, '出荷']
            week = untinForUriage.loc[i, '曜日']
            close_date = untinForUriage.loc[i, 'closeDate']
            hikiate = untinForUriage.loc[i, 'lot']

            # npNan : 運送対応表に納入先名称が載っていない
            if iraisaki == 'NoCalc' or iraisaki == 'npNan' or iraisaki == 'NoData' or hikiate == {} \
                    or 'short' in hikiate.keys():
                txt = '受注No:{}, 品番:{} の売上入力不可です。' \
                        .format(jutyuu_no, jutyuu_hinban)
                recorder.out_log(txt)
                recorder.out_file(txt)
                continue

            # 登録ボタン押す 
            myclc = pyautogui.locateOnScreen(r'../png_file/uriage_nyuuryoku/登録.png')
            time.sleep(5)
            if myclc != None:
                clc_cent = pyautogui.center(myclc)
                pyautogui.click(clc_cent)
                time.sleep(1)
            else:
                myclc2 = pyautogui.locateOnScreen(r'../png_file/uriage_nyuuryoku/登録_青.png')
                time.sleep(3)
                clc_cent2 = pyautogui.center(myclc2)
                pyautogui.click(clc_cent2)
                time.sleep(1)

            # マウスカーソルを(0, 0)に逃がしておく
            pyautogui.moveRel(0, 20)


            # 売上日
            pyautogui.typewrite(['delete'])
            pyautogui.typewrite(uriagebi)
            pyautogui.typewrite(['enter'])
            # 取引区分  
            pyautogui.typewrite(['delete'])
            pyautogui.typewrite('01')
            #pyperclip.copy('01')
            #pyautogui.hotkey('ctrl', 'v')
            time.sleep(1)
            pyautogui.typewrite(['enter'])
            # 得意先  
            pyautogui.typewrite(['delete'])
            pyautogui.typewrite(tokuisaki_code)
            pyautogui.typewrite(['enter'])
            # 納入先  
            if pd.isnull(nounyuu_code):
                pyautogui.typewrite(['enter'])
            else:
                pyautogui.typewrite(['delete'])
                pyautogui.typewrite(nounyuu_code)
                pyautogui.typewrite(['enter'])
            # 運送業者  
            pyautogui.typewrite(['delete'])
            pyautogui.typewrite(unsou_dic[iraisaki])
            pyautogui.typewrite(['enter'])
            # 配送区分  
            if '営業所' in syukka_yotei_souko: 
                pyautogui.typewrite(['delete'])
                pyautogui.typewrite('3')
                pyautogui.typewrite(['enter'])
                pyautogui.hotkey('shift', 'tab')
            elif '土曜配達' in syukka_yotei_souko:
                pyautogui.typewrite(['delete'])
                pyautogui.typewrite('2')
                pyautogui.typewrite(['enter'])
                pyautogui.hotkey('shift', 'tab')
            elif '曜日' in syukka_yotei_souko:
                pyautogui.typewrite(['delete'])
                pyautogui.typewrite('4')
                pyautogui.typewrite(['enter'])
                pyautogui.hotkey('shift', 'tab')
            else:
                pyautogui.typewrite(['delete'])
                pyautogui.typewrite('1')
                pyautogui.typewrite(['enter'])
                pyautogui.hotkey('shift', 'tab')

            # 請求予定日  
            # 得意先がスタンレーの場合はclose_dateは変更しない
            if tokuisaki_code in nonChange_list:
                pyautogui.typewrite(['enter'])
            else:
                pyautogui.typewrite(['delete'])
                pyautogui.typewrite(close_date)
                pyautogui.typewrite(['enter'])


            # 出荷倉庫  
            pyautogui.typewrite(['delete'])
            pyautogui.typewrite(souko_dic[syukka_souko])
            pyautogui.typewrite(['enter'])
            
            
            
            # 受注No  
            pyautogui.typewrite(['delete'])
            pyautogui.typewrite(jutyuu_no)
            pyautogui.typewrite(['enter'])

            # 受注行No  
            pyautogui.typewrite(['delete'])
            pyautogui.typewrite(jutyuugyou_no)
            pyautogui.typewrite(['enter']) 
             
            myclc = pyautogui.locateOnScreen(r'../png_file/uriage_nyuuryoku/完納済.png')
            time.sleep(8)
            if myclc != None:
                pyautogui.typewrite(['enter'])
                txt = '{}:{}は完納済です'.format(jutyuu_no, jutyuu_hinban)
                recorder.out_log(txt)
                recorder.out_file(txt)
                time.sleep(3)
                continue 

            myclc = pyautogui.locateOnScreen(r'../png_file/uriage_nyuuryoku/登録なし.png')
            time.sleep(5)
            if myclc != None:
                pyautogui.typewrite(['enter'])
                txt = '{}:{}は登録なしです'.format(jutyuu_no, jutyuu_hinban)
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
                
            # ok test中はｷｬﾝｾﾙ
            myclc = pyautogui.locateOnScreen(r'../png_file/uriage_nyuuryoku/ok.png')
            time.sleep(3)
            clc_cent = pyautogui.center(myclc)
            pyautogui.click(clc_cent)

                
        
            

            











