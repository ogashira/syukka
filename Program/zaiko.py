#! python
# -*- coding: utf-8 -*-

import jaconv, csv, openpyxl
import os
import platform
from datetime import datetime, date, timedelta
from recorder import *

'''
売上処理のための在庫の引き当て（LOT）を行う
輸出製品の場合は、輸出塗料連絡表のlotを引き当てる。
しかし、輸出塗料連絡表には品番、品名が無いので、現在庫ﾃﾞｰﾀにある
品番のlotを調べて、どれが輸出塗料連絡表のオーダーNoのLOTなのかを調べて引き当てる。
国内受注製品は、一致する缶数のLOTから引き当てる。同時に同数の缶数が一致した場合
は、製造日が受注日よりも後ならばどちらでもよい。
見込み品の場合は、古いLOTから引き当てる。
'''




class Zaiko:

    def __init__ (self, myfolder):

        self.myfolder = myfolder


     
    #輸出塗料連絡表の取得
        pf = platform.system()
        if pf == 'Windows':
            mypath = r'//192.168.1.247/Guest/輸出塗料連絡表.xlsx'
        elif pf == 'Linux':
            mypath = r'/mnt/guest/輸出塗料連絡表.xlsx'
        else:
            mypath = r'../master/輸出塗料連絡表.xlsx'

        wb = openpyxl.load_workbook(mypath, data_only=True)

        ws = wb['輸出塗料連絡表']
        
        # シートを保護したときのパスワードをセット
        ws.protection.password = 'gijutu'
        
        # シートの保護を解除
        ws.protection.disable()

        #二次元ﾘｽﾄにする
        yusyutuRenraku = []
        for row in ws.rows:
            rows = []
            for cell in row:
                rows.append(cell.value)
            yusyutuRenraku.append(rows)
        
        #orderNo_lot = {'VNN3044:{20090501H : 3, 20091852T: 5,...},.....} の形にする
        orderNo_lot = {}
        lot_cans = {}
        for line in yusyutuRenraku:
            if line[3]== None :
                continue
            else:
                #小文字を大文字にする
                orderNo = str(line[3]).upper() 
                #全角を半角にする(数字も記号も)
                orderNo = jaconv.z2h(orderNo,digit=True,ascii=True) 
                #空白を除去
                orderNo = orderNo.replace(' ','') 
                orderNo = orderNo.replace('　','')
                lot = str(line[5]).upper()
                lot = jaconv.z2h(lot,digit=True,ascii=True)
                

                if orderNo in orderNo_lot:
                    lot_cans = orderNo_lot[orderNo]
                    lot_cans[lot] = line[7]
                    orderNo_lot[orderNo] = lot_cans
                else:
                    orderNo_lot[orderNo] = {lot:line[7]}


        self.yusyutuRenrakuLot = orderNo_lot
        '''
        {VNN3044:{20090501H: 3, 20091852T: 5....}, VNN3055:{..},....}
        '''


    # 現在庫ﾃﾞｰﾀの取得 
        zaiko = pd.read_csv(r'../master/effitA/zaiko.csv',encoding='cp932')
        zaiko = zaiko.loc[(zaiko['倉庫']=='大阪倉庫')|(zaiko['倉庫']=='本社倉庫')
                          |(zaiko['倉庫']=='土気倉庫'), ['品番','ロットNo',
                          '在庫数量（現在）','倉庫']]
        zaiko = zaiko.fillna("")
        
        genzaiko_d = zaiko.to_dict(orient='split') #dataframe を辞書にする
        genzaiko_l = genzaiko_d['data'] # 辞書からkey=data(二次元ﾘｽﾄ部分）を取り出す
        genzaiko_l = sorted(genzaiko_l, key=lambda x: x[1]) #LOTでソート
        self.genzaiko_l = sorted(genzaiko_l, key=lambda x: x[0]) #更に、品番でソート

        '''
        [['S10-E-C', '20052603H', '3', '本社倉庫'],
        ['S10-E-C', '20071405H', '15', '本社倉庫'],
        ['S10-P3', '20071331H', '4', '大阪倉庫'],
        ['S11-PT04S-T', '20091451T', '60', '土気倉庫'],
        ['S11-PT04S-T-R-EX', '20091454T', '8', '土気倉庫'],......]
        '''

    # 受注見込み製品ﾃﾞｰﾀの取得
        JM_file = open('../master/selfMade/受注見込みﾘｽﾄ.csv',encoding='cp932')
        file_reader = csv.reader(JM_file)
        JM = list(file_reader)
        JM_file.close()

        self.JM_data = {}
        for line in JM:
            hinban = line[0]
            JorM = line[1]
            self.JM_data[hinban] = JorM


    # 受注DT.csv の取得
        JDT = pd.read_csv(r'../master/effitA/受注DT.csv', skiprows = 1
                          , encoding = 'cp932')
        JDT = JDT.drop_duplicates(['受注ＮＯ'])
        JDT = JDT.loc[:,['受注ＮＯ','受注日']]
        self.JDT_d = dict(zip(JDT['受注ＮＯ'], JDT['受注日']))
    
 

# ↓ method



    def get_lot(self,df_row):
        '''lotの引き当てを行う。
        輸出向先がyならばdefpattern_yで処理,それ以外はそれぞれのﾊﾟﾀｰﾝ
        '''

        recorder = Recorder(self.myfolder)
        
        #patternを決定する関数
        def get_pattern(hinban):
            if self.JM_data.get(hinban, '-') =='受注製品':
                return 'J'
            elif self.JM_data.get(hinban, '-') == '見込み製品':
                return 'M'
            else:
                return '-'

        #在庫を引く関数
        def zaiko_minus(k, cans):
            for line in self.genzaiko_l:
                if line[1] == k:
                    line[2] = float(line[2]) - cans


        def pattern_y(hinban,cans,orderNo, syukka_souko, lot) :
            '''
            輸出塗料連絡表の品番、lotが現在庫になかったら、メッセージを出すが、
            {}のままprogramは進行する。
            現在庫が運賃計算シートの出荷缶数よりも足りなかったら、メッセージを
            出し、{'short':0}でprogramは進行する。
            輸出塗料連絡表の出荷缶数は無視する（見ていない）
            出荷倉庫と在庫倉庫が不一致の場合、{'short':0}だして売上立てない
            '''
            yusyutu = self.yusyutuRenrakuLot.get(orderNo, {})
            # {20090501H : 3, 20091852T : 5....}
            for line in self.genzaiko_l:
                if line[0] == hinban:
                    zaiko_lot = line[1]
                    zaiko_cans = float(line[2])
                    zaiko_souko = line[3]
                    yusyutu_cans = float(yusyutu.get(zaiko_lot, 0))

                    if zaiko_lot in yusyutu:
                        if zaiko_souko[:2] == syukka_souko[:2]:
                            if zaiko_cans >= yusyutu_cans:
                                lot[zaiko_lot] =  yusyutu_cans
                                zaiko_minus(zaiko_lot, yusyutu_cans)
                            else:
                                txt = '輸出製品{}の{}の在庫が足りません'\
                                                      .format(hinban,zaiko_lot)
                                recorder.out_log(txt)
                                recorder.out_file(txt)
                                lot = {'short':0}
                                break                 
                            
            if lot == {}:
                txt = '輸出製品{}が輸出塗料連絡表にないか、出荷予定倉庫と違う倉庫にあります'.format(hinban)
                recorder.out_log(txt)
                recorder.out_file(txt,'\n')
                 

            if 'short' not in lot and lot != {}:
                total = 0
                for v in lot.values():
                    total += int(v)
                if total != int(cans):#元の出荷缶数とtotalを比較している
                    recorder.out_log('・輸出製品(' + str(hinban) + ')の在庫が合いません。')
                    recorder.out_file('・輸出製品(' + str(hinban) + ')の在庫が合いません。')
                    lot['short'] = 0



                        
            
            return lot



        def pattern_J(hinban,cans,JNo, syukka_souko, lot):
            #途中の在庫引き当てで、cansは変化するので出荷缶数をsyukka_cansとして取っておく
            syukka_cans = cans
            dt_now = datetime.now()
            mytoday = dt_now.strftime('%Y%m%d')
            J_date = str(self.JDT_d.get(JNo, mytoday))
            J_date = J_date[:4] + '/' + J_date[4:6] + '/' + J_date[6:]
            J_date = datetime.strptime(J_date, '%Y/%m/%d')
            J_zaiko = {}

            #ifに引っかからないと187行のところで定義されていなくてエラーになるから。
            zaiko_souko = ''
            zaiko_lot = ''
            for line in self.genzaiko_l:   
                if line[0] == hinban:
                    zaiko_hinban = line[0]
                    zaiko_lot = line[1]
                    zaiko_cans = line[2]
                    zaiko_souko = line[3]
                    zaiko_date = '20' + zaiko_lot[:2] + '/' + zaiko_lot[2:4] \
                        + '/' + zaiko_lot[4:6]
                    zaiko_date = datetime.strptime(zaiko_date, '%Y/%m/%d')
                    if zaiko_date - J_date >= timedelta(0) \
                            and zaiko_souko[:2] == syukka_souko[:2]:
                        J_zaiko[zaiko_lot] = zaiko_cans
                        
            #辞書をＬＯＴでソートするとリストになるので、また辞書にする。
            J_zaiko = sorted(J_zaiko.items())
            J_zaiko = dict(J_zaiko)
            
            #缶数が在庫と出荷缶数とぴったり一致するLOTを引き当てる
            for k, v in J_zaiko.items():
                if float(v) == cans:
                    lot[k] = cans
                    zaiko_minus(k, cans)
                    break
            else:
                for k, v in J_zaiko.items(): #在庫が出荷缶数以上のLOTを引き当てる
                    if float(v) >= cans:
                        lot[k] = cans
                        zaiko_minus(k, cans)
                        break

            # if zaiko_souko[:2] != syukka_souko[:2]:
            #     lot['short'] = 0 
            #     recorder.out_log('・出荷する倉庫と在庫がある倉庫が一致してません(' \
            #                      + hinban + ':' + zaiko_lot + ')')
            #     recorder.out_file('・出荷する倉庫と在庫がある倉庫が一致してません(' \
            #                       + hinban + ':' + zaiko_lot + ')')
            
            if lot == {}:
                recorder.out_log('・受注製品(' + str(hinban) + ')のLOTが引き当てでき' \
                                 'ません。')
                recorder.out_file('・受注製品(' + str(hinban) + ')のLOTが引き当てで' \
                                  'きません。')
            else:
                total = 0
                for v in lot.values():
                    total += int(v)
                if total < int(syukka_cans):#元の出荷缶数とtotalを比較している
                    recorder.out_log('・受注製品(' + str(hinban) + ')の在庫が足りません。')
                    recorder.out_file('・受注製品(' + str(hinban) + ')の在庫が足りません。')
                    lot['short'] = 0

            return lot



        def pattern_M(hinban,cans, syukka_souko, lot):
            M_zaiko = []
            #途中の在庫引き当てで、cansは変化するので出荷缶数をsyukka_cansとして取っておく
            syukka_cans = cans
            if syukka_souko == '大阪直送':
                for line in self.genzaiko_l:   
                    if line[0] == hinban and line[3] == '移動倉庫' and float(line[2]) > 0 :
                        add_l = []
                        add_l.append(line[1])
                        add_l.append(line[2])
                        add_l.append(line[3])
                        M_zaiko.append(add_l)
            elif syukka_souko == '土気出荷':
                for line in self.genzaiko_l:   
                    if line[0] == hinban and line[3] == '土気倉庫' and float(line[2]) > 0  :
                        add_l = []
                        add_l.append(line[1])
                        add_l.append(line[2])
                        add_l.append(line[3])
                        M_zaiko.append(add_l)
            elif syukka_souko == '本社出荷':
                for line in self.genzaiko_l:   
                    if line[0] == hinban and line[3] == '本社倉庫' and float(line[2]) > 0  :
                        add_l = []
                        add_l.append(line[1])
                        add_l.append(line[2])
                        add_l.append(line[3])
                        M_zaiko.append(add_l)
                        
            #２次元ﾘｽﾄをLOTでソートする。
            M_zaiko = sorted(M_zaiko)
            
            #LOTの引き当て、cansは０になるまで減っていく
            for i in range(len(M_zaiko)):
                if float(cans) > float(M_zaiko[i][1]):
                    tmp = float(M_zaiko[i][1])
                    M_zaiko[i][1] = 0
                    cans = float(cans) - tmp
                    lot[M_zaiko[i][0]] = tmp
                    zaiko_minus(M_zaiko[i][0], tmp)
                else:
                    M_zaiko[i][1] = float(M_zaiko[i][1]) - float(cans)
                    lot[M_zaiko[i][0]] = float(cans)
                    zaiko_minus(M_zaiko[i][0], float(cans))
                    #cans = 0        
                    break
        
            if lot == {}:
                recorder.out_log('・見込み製品(' + str(hinban) + ')のLOTが引き当てできません。')
                recorder.out_file('・見込み製品(' + str(hinban) + ')のLOTが引き当てできません。')
            else:
                total = 0
                for v in lot.values():
                    total += int(v)
                if total < int(syukka_cans):#元の出荷缶数とtotalを比較している
                    recorder.out_log('・見込み製品(' + str(hinban) + ')の在庫が足りません。')
                    recorder.out_file('・見込み製品(' + str(hinban) + ')の在庫が足りません。')
                    lot['short'] =0


            return lot


        #↑ ここまでmethod内の関数



        hinban = df_row['hinban']
        cans = df_row['cans']
        yusyutu = df_row['輸出向先']
        orderNo = df_row['得意先注文ＮＯ']
        JNo = df_row['受注ＮＯ']
        syukka_souko = df_row['出荷']
        lot = {}
        if yusyutu == 'y':
            lot = pattern_y(hinban, cans, orderNo, syukka_souko, lot)
        else:
            pattern = '-'
            pattern = get_pattern(hinban)
            if pattern == 'J':
                lot = pattern_J(hinban,cans,JNo, syukka_souko, lot)
                # JNoは受注日を求めるために必要。受注製品の製造日は受注日よりも後が必須なため。
            elif pattern == 'M':
                lot = pattern_M(hinban,cans, syukka_souko, lot)
            else:
                recorder.out_log('・受注見込みﾘｽﾄ.csvに製品のﾃﾞｰﾀがありません(' + str(hinban) + ')')
                recorder.out_file('・受注見込みﾘｽﾄ.csvに製品のﾃﾞｰﾀがありません(' + str(hinban) + ')' )
                
        return lot






