#! python
# -*- coding: utf-8 -*-

from sql_express import *

import win32com.client
import time




class HinkanSheet(object):

    def __init__(self, HS_nonExistent_coa):
        sql = SqlExpress()
        self.nonExistent_coa = HS_nonExistent_coa
        
        nonExistent_coa_lot = [] # get_hinken_dataに渡す
        nonExistent_coa_hinban = [] # get_spec_dataに渡す
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
        self.spec_data = self.spec_data.iloc[:,:89 ] # 89列までを取得

        print(self.spec_data)
        print(self.hinken_data)


    def coa_data_copy(self, ws_format, lot, hinban):
        """
        品管ｼｰﾄのworkに、品質試験ﾃﾞｰﾀとﾌｫｰﾏｯﾄ用ﾃﾞｰﾀ(spec)を転記する
        """
        # spec_dataの情報を得る
        """
        locで得たデータはSeriesなので、それのiloc[0]がリテラルのデータとなる
        """
        coaName          = self.spec_data.loc[
                            self.spec_data['入力名']== hinban, '成績書名'].iloc[0]
        spec_vis1        = self.spec_data.loc[
                           self.spec_data['入力名']== hinban, '粘度規格1'].iloc[0]
        spec_vis2        = self.spec_data.loc[
                           self.spec_data['入力名']== hinban, '粘度規格2'].iloc[0]
        spec_vis3        = self.spec_data.loc[
                           self.spec_data['入力名']== hinban, '粘度規格3'].iloc[0]
        spec_sg1         = self.spec_data.loc[
                           self.spec_data['入力名']== hinban, '比重規格1'].iloc[0]
        spec_sg2         = self.spec_data.loc[
                           self.spec_data['入力名']== hinban, '比重規格2'].iloc[0]
        spec_sg3         = self.spec_data.loc[
                           self.spec_data['入力名']== hinban, '比重規格3'].iloc[0]
        spec_nv1         = self.spec_data.loc[
                           self.spec_data['入力名']== hinban, '加残規格1'].iloc[0]
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
        judg_eki         = self.spec_data.loc[
                              self.spec_data['入力名']== hinban, '液外KS'].iloc[0]
        spec_eki         = self.spec_data.loc[
                          self.spec_data['入力名']== hinban, '液外規格KS'].iloc[0]
        judg_sagyou      = self.spec_data.loc[
                             self.spec_data['入力名']== hinban, '作業性S'].iloc[0]
        spec_sagyo       = self.spec_data.loc[
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
        # hinken_dataの情報を得る
        data_suu         = self.hinken_data.loc[
                    self.hinken_data['ロットＮＯ'] == lot, '管理良品数量'].iloc[0]
        data_hantei      = self.hinken_data.loc[
                            self.hinken_data['ロットＮＯ'] == lot, '判定'].iloc[0]
        data_tantou      = self.hinken_data.loc[
                        self.hinken_data['ロットＮＯ'] == lot, '検査担当'].iloc[0]
        data_vis         = self.hinken_data.loc[
                           self.hinken_data['ロットＮＯ'] == lot, '粘度1'].iloc[0]
        data_sg          = self.hinken_data.loc[
                           self.hinken_data['ロットＮＯ'] == lot, '比重1'].iloc[0]
        data_nv         = self.hinken_data.loc[
                       self.hinken_data['ロットＮＯ'] == lot, '加熱残分1'].iloc[0]
        data_haze         = self.hinken_data.loc[
                            self.hinken_data['ロットＮＯ'] == lot, 'Haze'].iloc[0]
        data_dltaE        = self.hinken_data.loc[
                             self.hinken_data['ロットＮＯ'] == lot, 'ΔE'].iloc[0]
        
        



    def HS_create_coa(self, coa_folder):
        """
        HS_nonExistent_coaを基にcoaを作る。作れなかったcoaがあったら、
        HS_nonCreate_coaのリストを返す
        """
        HS_nonCreate_coa = []


        EXCEL_PATH = r'//192.168.1.247/Guest/品質検査管理ｼｰﾄ2017.xlsm'


        xlapp = win32com.client.Dispatch("Excel.Application")    # Excelの起動
        xlapp.DisplayAlerts = False
        # xlapp.Visible = True
        wb = xlapp.Workbooks.Open(EXCEL_PATH, ReadOnly=1)    # Excelファイルを開く
        # time.sleep(20)

        ws_work = wb.Worksheets('work')
        ws_hinken = wb.Worksheets('品質試験ﾃﾞｰﾀ')


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

            # coa_data_copyを実行すれば、returnなくてもws_formatに転記されるはず
            self.coa_data_copy(ws_format, lot, hinban)

            # pdfに変換　絶対パスが必要
            ws_format.ExportAsFixedFormat(Type = 0, Quality = 0, 
                                Filename = coa_folder + r"/" + hinban + r".pdf")

        ws_hinken.Activate()
        wb.Close(SaveChanges = False)    # 開いたエクセルを閉じる
        xlapp.Quit()    # Excelを終了
        

        return HS_nonCreate_coa
        
