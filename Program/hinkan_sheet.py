#! python
# -*- coding: utf-8 -*-

from sql_express import *

import win32com.client
import time




class HinkanSheet(object):

    def __init__(self, HS_nonExistent_coa):
        """
        HS_nonExistent_coaはnonExistent_coaの中の品管ｼｰﾄ分のみ
        """
        sql = SqlExpress()
        self.nonExistent_coa = HS_nonExistent_coa
        
        nonExistent_coa_lot = [] # get_hinken_dataに渡す
        nonExistent_coa_hinban = [] # spec_dataに渡す
        for row in self.nonExistent_coa:
            if row[4] == '営業':
                nonExistent_coa_lot.append(row[0])
                nonExistent_coa_hinban.append(row[3])

        self.hinken_data = sql.get_hinken_data(nonExistent_coa_lot)

        self.spec_data = pd.read_excel(r'//192.168.1.247/Guest/'
                r'品質検査管理ｼｰﾄ2017.xlsm', 'ﾌｫｰﾏｯﾄ用ﾃﾞｰﾀ', engine='openpyxl')
        self.spec_data = self.spec_data.fillna('-')
       
        # isinを使ってﾘｽﾄに存在する品番のみを取得する
        self.spec_data = self.spec_data[self.spec_data['入力名']
                                                .isin(nonExistent_coa_hinban)] 
        self.spec_data = self.spec_data.iloc[:,:111 ] # 92列までを取得



    def coa_data_copy(self, ws_work, ws_format, ws_inn, lot, hinban):
        """
        品管ｼｰﾄのworkに、品質試験ﾃﾞｰﾀとﾌｫｰﾏｯﾄ用ﾃﾞｰﾀ(spec)を転記する
        """
        # spec_dataの情報を得る
        """
        locで得たデータはSeriesなので、それのiloc[0]がリテラルのデータとなる
        """

        # 検査ngなどで、成績書が作成できなかったらfalseを返す
        bool_success = True

        coaName          = self.spec_data.loc[
                            self.spec_data['入力名']== hinban, '成績書名'].iloc[0]
        spec_vis1        = self.spec_data.loc[
                           self.spec_data['入力名']== hinban, '粘度規格'].iloc[0]
        spec_vis2        = self.spec_data.loc[
                           self.spec_data['入力名']== hinban, '粘度規格2'].iloc[0]
        spec_vis3        = self.spec_data.loc[
                           self.spec_data['入力名']== hinban, '粘度規格3'].iloc[0]
        spec_sg1         = self.spec_data.loc[
                           self.spec_data['入力名']== hinban, '比重規格'].iloc[0]
        spec_sg2         = self.spec_data.loc[
                           self.spec_data['入力名']== hinban, '比重規格2'].iloc[0]
        spec_sg3         = self.spec_data.loc[
                           self.spec_data['入力名']== hinban, '比重規格3'].iloc[0]
        spec_nv1         = self.spec_data.loc[
                           self.spec_data['入力名']== hinban, '加残規格'].iloc[0]
        spec_nv2         = self.spec_data.loc[
                           self.spec_data['入力名']== hinban, '加残規格2'].iloc[0]
        spec_nv3         = self.spec_data.loc[
                           self.spec_data['入力名']== hinban, '加残規格3'].iloc[0]
        spec_haze1       = self.spec_data.loc[
                               self.spec_data['入力名']== hinban, 'Haze1'].iloc[0]
        spec_haze2       = self.spec_data.loc[
                               self.spec_data['入力名']== hinban, 'Haze2'].iloc[0]
        spec_haze3       = self.spec_data.loc[
                               self.spec_data['入力名']== hinban, 'Haze3'].iloc[0]
        spec_dltaE1      = self.spec_data.loc[
                                self.spec_data['入力名']== hinban, 'ΔE1'].iloc[0]
        spec_dltaE2      = self.spec_data.loc[
                                self.spec_data['入力名']== hinban, 'ΔE2'].iloc[0]
        spec_dltaE3      = self.spec_data.loc[
                                self.spec_data['入力名']== hinban, 'ΔE3'].iloc[0]
        spec_nendo      = self.spec_data.loc[
                                self.spec_data['入力名']== hinban, '粘度'].iloc[0]
        spec_hijuu      = self.spec_data.loc[
                                self.spec_data['入力名']== hinban, '比重'].iloc[0]
        spec_kazan      = self.spec_data.loc[
                                self.spec_data['入力名']== hinban, '加残'].iloc[0]
        judg_eki         = self.spec_data.loc[
                              self.spec_data['入力名']== hinban, '液外KS'].iloc[0]
        spec_eki         = self.spec_data.loc[
                          self.spec_data['入力名']== hinban, '液外規格KS'].iloc[0]
        judg_sagyou      = self.spec_data.loc[
                             self.spec_data['入力名']== hinban, '作業性S'].iloc[0]
        spec_sagyou      = self.spec_data.loc[
                         self.spec_data['入力名']== hinban, '作業性規格S'].iloc[0]
        judg_app         = self.spec_data.loc[
                              self.spec_data['入力名']== hinban, '外観KS'].iloc[0]
        spec_app         = self.spec_data.loc[
                          self.spec_data['入力名']== hinban, '外観規格KS'].iloc[0]
        judg_adh         = self.spec_data.loc[
                              self.spec_data['入力名']== hinban, '付着KS'].iloc[0]
        spec_adh         = self.spec_data.loc[
                          self.spec_data['入力名']== hinban, '付着規格KS'].iloc[0]
        judg_vacu        = self.spec_data.loc[
                              self.spec_data['入力名']== hinban, '蒸着KS'].iloc[0]
        spec_vacu        = self.spec_data.loc[
                          self.spec_data['入力名']== hinban, '蒸着規格KS'].iloc[0]
        judg_heat        = self.spec_data.loc[
                              self.spec_data['入力名']== hinban, '耐熱KS'].iloc[0]
        spec_heat        = self.spec_data.loc[
                          self.spec_data['入力名']== hinban, '耐熱規格KS'].iloc[0]
        judg_water       = self.spec_data.loc[
                              self.spec_data['入力名']== hinban, '耐水KS'].iloc[0]
        spec_water       = self.spec_data.loc[
                          self.spec_data['入力名']== hinban, '耐水規格KS'].iloc[0]
        judg_humi        = self.spec_data.loc[
                               self.spec_data['入力名']== hinban, '耐湿K'].iloc[0]
        spec_humi        = self.spec_data.loc[
                           self.spec_data['入力名']== hinban, '耐湿規格K'].iloc[0]
        judg_save        = self.spec_data.loc[
                               self.spec_data['入力名']== hinban, '保存S'].iloc[0]
        spec_save        = self.spec_data.loc[
                           self.spec_data['入力名']== hinban, '保存規格S'].iloc[0]
        judg_overct      = self.spec_data.loc[
                        self.spec_data['入力名']== hinban, 'ﾄｯﾌﾟ上塗り性'].iloc[0]
        spec_overct      = self.spec_data.loc[
                    self.spec_data['入力名']== hinban, 'ﾄｯﾌﾟ上塗り性規格'].iloc[0]
        spec_2eki        = self.spec_data.loc[
                                self.spec_data['入力名']== hinban, '２液'].iloc[0]
        # hinken_dataの情報を得る
        data_tanjuu      = self.hinken_data.loc[
                    self.hinken_data['ﾛｯﾄNo'] == lot, '単重'].iloc[0]
        data_suu         = self.hinken_data.loc[
                    self.hinken_data['ﾛｯﾄNo'] == lot, '管理良品数量'].iloc[0]
        data_hantei      = self.hinken_data.loc[
                            self.hinken_data['ﾛｯﾄNo'] == lot, '判定'].iloc[0]
        data_tantou      = self.hinken_data.loc[
                        self.hinken_data['ﾛｯﾄNo'] == lot, 'tantou'].iloc[0]
        data_vis         = self.hinken_data.loc[
                           self.hinken_data['ﾛｯﾄNo'] == lot, '粘度1'].iloc[0]
        data_sg          = self.hinken_data.loc[
                           self.hinken_data['ﾛｯﾄNo'] == lot, '比重1'].iloc[0]
        data_nv         = self.hinken_data.loc[
                       self.hinken_data['ﾛｯﾄNo'] == lot, '加熱残分1'].iloc[0]
        data_haze         = self.hinken_data.loc[
                            self.hinken_data['ﾛｯﾄNo'] == lot, 'Haze'].iloc[0]
        data_dltaE        = self.hinken_data.loc[
                             self.hinken_data['ﾛｯﾄNo'] == lot, 'ΔE'].iloc[0]


        if data_hantei == '合格':
                             
            # sheets("work")に転記する spec_data
            ws_work.Range("A2").Value = hinban
            ws_work.Range("D2").Value = coaName
            ws_work.Range("F2").Value = spec_vis1
            ws_work.Range("G2").Value = spec_vis2
            ws_work.Range("H2").Value = spec_vis3
            ws_work.Range("I2").Value = spec_sg1
            ws_work.Range("J2").Value = spec_sg2
            ws_work.Range("K2").Value = spec_sg3
            ws_work.Range("L2").Value = spec_nv1
            ws_work.Range("M2").Value = spec_nv2
            ws_work.Range("N2").Value = spec_nv3
            ws_work.Range("O2").Value = spec_haze1
            ws_work.Range("P2").Value = spec_haze2
            ws_work.Range("Q2").Value = spec_haze3
            ws_work.Range("R2").Value = spec_dltaE1
            ws_work.Range("S2").Value = spec_dltaE2

            ws_work.Range("AS2").Value = spec_nendo
            ws_work.Range("AT2").Value = spec_hijuu
            ws_work.Range("AU2").Value = spec_kazan

            ws_work.Range("BF2").Value = judg_eki
            ws_work.Range("BG2").Value = spec_eki
            ws_work.Range("BL2").Value = judg_sagyou
            ws_work.Range("BM2").Value = spec_sagyou
            ws_work.Range("BN2").Value = judg_app
            ws_work.Range("BO2").Value = spec_app
            ws_work.Range("BP2").Value = judg_adh
            ws_work.Range("BQ2").Value = spec_adh
            ws_work.Range("BR2").Value = judg_vacu
            ws_work.Range("BS2").Value = spec_vacu
            ws_work.Range("BT2").Value = judg_heat
            ws_work.Range("BU2").Value = spec_heat
            ws_work.Range("BV2").Value = judg_water
            ws_work.Range("BW2").Value = spec_water
            ws_work.Range("BX2").Value = judg_humi
            ws_work.Range("BY2").Value = spec_humi
            ws_work.Range("BZ2").Value = judg_save
            ws_work.Range("CA2").Value = spec_save
            ws_work.Range("CJ2").Value = judg_overct
            ws_work.Range("CK2").Value = spec_overct
            ws_work.Range("DF2").Value = spec_2eki
            
            # sheets("work")に転記する hinken_data
            ws_work.Range("A7").Value = hinban
            ws_work.Range("B7").Value = lot
            ws_work.Range("C7").Value = data_tanjuu
            ws_work.Range("D7").Value = data_suu
            ws_work.Range("K7").Value = data_hantei
            ws_work.Range("L7").Value = data_tantou
            ws_work.Range("M7").Value = data_vis
            ws_work.Range("P7").Value = data_sg
            ws_work.Range("S7").Value = data_nv
            ws_work.Range("V7").Value = data_haze
            ws_work.Range("W7").Value = data_dltaE

            self.shape_copy(ws_format, ws_inn, data_tantou)
        else:
            bool_success = False


        return bool_success



    def shape_copy(self, ws_format, ws_inn, data_tantou):

        def press_inn(inn, col):
            ws_inn.Activate()
            ws_inn.Shapes(inn).Copy()
            ws_format.Activate()
            if ws_format.Name == '一般品':
                ws_format.Range(col + "25").Activate()
                ws_format.Paste()
                ws_format.Shapes(inn).Left = ws_format.Range(col + "25").Left + 15
                ws_format.Shapes(inn).Top = ws_format.Range(col + "25").Top + 8
            elif ws_format.Name == '秦野':
                ws_format.Range(col + "24").Activate() 
                ws_format.Paste()
                ws_format.Shapes(inn).Left = ws_format.Range(col + "24").Left + 15
                ws_format.Shapes(inn).Top = ws_format.Range(col + "24").Top + 8



        if data_tantou == '和泉':
            tantou_inn = "Picture 7"
            kensa_inn = "Picture 8"
        elif data_tantou == '荒添':
            tantou_inn = "Picture 11"
            kensa_inn = "Picture 8"
        elif data_tantou == '嘉規':
            tantou_inn = "Picture 15"
            kensa_inn = "Picture 8"
        elif data_tantou == '丸山':
            tantou_inn = "Picture 6"
            kensa_inn = "Picture 8"
        elif data_tantou == '徳武':
            tantou_inn = "Picture 19"
            kensa_inn = "Picture 8"
        elif data_tantou == '吉田':
            tantou_inn = "Picture 18"
            kensa_inn = "Picture 8"
        elif data_tantou == '鈴木':
            tantou_inn = "Picture 8"
            kensa_inn = "Picture 7"
        elif data_tantou == '村山':
            tantou_inn = "Picture 17"
            kensa_inn = "Picture 8"
        elif data_tantou == '井上':
            tantou_inn = "Picture 16"
            kensa_inn = "Picture 8"
        elif data_tantou == '石崎':
            tantou_inn = "Picture 13"
            kensa_inn = "Picture 8"
        elif data_tantou == '尾頭':
            tantou_inn = "Picture 9"
            kensa_inn = "Picture 8"
        else:
            tantou_inn = "Picture 3"
            kensa_inn = "Picture 8"

        press_inn(tantou_inn, "F")
        press_inn(kensa_inn, "H")
        


    def HS_create_coa(self, coa_folder):
        """
        HS_nonExistent_coaを基にcoaを作る。作れなかったcoaがあったら、
        HS_nonCreate_coaのリストを返す
        """
        HS_nonCreate_coa = []


        EXCEL_PATH = r'//192.168.1.247/Guest/品質検査管理ｼｰﾄ2017.xlsm'


        xlapp = win32com.client.Dispatch("Excel.Application")    # Excelの起動
        xlapp.DisplayAlerts = True
        # xlapp.Visible = False

        # UpdateLinks = Falseを指定しないと「読み取り専用で開きますか」の
        # メッセージが出て止まってしまう。なぜかわからない。
        wb = xlapp.Workbooks.Open(EXCEL_PATH, 
                    UpdateLinks = False, ReadOnly = True)   # Excelファイルを開く
        # time.sleep(20)

        ws_work = wb.Worksheets('work')
        ws_hinken = wb.Worksheets('品質試験ﾃﾞｰﾀ')
        ws_inn = wb.Worksheets('印')


        for row in self.nonExistent_coa:
            lot        = row[0]
            hinban     = row[3]
            tantou     = row[4]
            coa_format = row[5]
            
            if coa_format == '一般品':
                sheet_format = '一般品'
            else:
                sheet_format = '秦野'

            
            ws_format = wb.Worksheets(sheet_format)
            ws_format.Visible = -1 # Vidible=-1, Hidden=0
            ws_format.Activate()

            # coa_data_copyを実行すれば、returnなくてもws_workに転記されるはず
            bool_success = self.coa_data_copy(ws_work, ws_format, ws_inn,  
                                                                 lot, hinban)
            # bool_successがfalseならば、HS_nonCreate_coaにappendして、次のroopへ行く
            if not bool_success:
                row.append('Did not pass')
                HS_nonCreate_coa.append(row)
                continue
               
                

            # pdfに変換　絶対パスが必要
            """
            try.expectで例外が出たら、HS_nonCreate_coaにrowを追加する。
            """
            try:
                ws_format.ExportAsFixedFormat(Type = 0, Quality = 0, 
                                Filename = '{}/{}_{}_{}.pdf'
                                .format(coa_folder,hinban, lot, coa_format))
            except Exception as ex:
                print('*****************成績書作成エラー*******************')
                print('{}({})のcoaが作成できませんでした'.format(hinban, lot))
                HS_nonCreate_coa.append(row)


        ws_hinken.Activate()
        wb.Close(SaveChanges = False)    # 開いたエクセルを閉じる
        xlapp.Quit()    # Excelを終了
        

        return HS_nonCreate_coa
        
