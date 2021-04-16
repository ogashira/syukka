#! python
# -*- coding: utf-8 -*-

import win32com.client
import time
import pandas as pd



class MetalHinkanSheet(object):

    def __init__(self, MHS_nonExistent_coa, coa_folder):
        """
        MHS_nonExistent_coaはnonExistent_coaの中のﾒﾀﾙ品管ｼｰﾄ分のみ
        """
        """AB試験があるIK-50のリスト"""
        self.AB_JUDGE_LIST = ['S7-IK50-M', 'S7-IK50-4-M']

        self.nonExistent_coa = MHS_nonExistent_coa
        self.coa_folder = coa_folder
        
        nonExistent_coa_lot = [] #get_hinken_dataに渡す
        nonExistent_coa_hinban = [] #spec_dataに渡す
        for row in self.nonExistent_coa:
            if row[4] == '営業':
                nonExistent_coa_lot.append(row[0])
                nonExistent_coa_hinban.append(row[3])


        """
        pandasのread_excelを使う。内部ではopenpyxlが動いているらしい"""
        xlpath = r'//192.168.1.247/Guest/ﾒﾀﾙ品管ｼｰﾄ.xlsm'
        xlsx = pd.ExcelFile(xlpath, engine='openpyxl')

        alltest_data = pd.read_excel(xlsx, 'test_db', skiprows = 1)
        sheet_data = pd.read_excel(xlsx, 'sheet_db', skiprows = 1)
        allspec_data = pd.read_excel(xlsx, 'spec_db')


        

        allspec_data = allspec_data.fillna('-')
       
        """isinを使ってﾘｽﾄに存在する品番のみを取得する"""
        self.spec_data = allspec_data[allspec_data['品番']
                                                .isin(nonExistent_coa_hinban)] 
        """isinを使ってﾘｽﾄに存在するlotのみを取得する"""
        self.test_data = alltest_data[alltest_data['\nLOT']
                                                .isin(nonExistent_coa_lot)] 
        """sheet_dataは品番:シート名の辞書にする"""
        self.sheet_dic = dict(zip(sheet_data['品番'], sheet_data['シート名'])) 

        """品番にik-50がある場合は、過去LOTのデータを作っておく"""
        isExist = False
        for IK50 in self.AB_JUDGE_LIST:
            if IK50 in nonExistent_coa_hinban:
                isExist = True
                break
        if isExist:
            self.ik50_df = alltest_data[alltest_data['\n品番']
                                                .isin(self.AB_JUDGE_LIST)]
        else: #空のDataFrame
            self.ik50_df = pd.DataFrame(index = [], 
                                            columns = alltest_data.columns)
    

        
    def judge_test_type(self, this_time_lot):
        """
        IK50がA試験かB試験かを判定する。
        ik-50のﾃﾞｰﾀﾌﾚｰﾑからlotのﾘｽﾄを作ってindexから前回LOTを求める
        """
        ik50lot_l = list(self.ik50_df.loc[:, '\nLOt'])
        ik50lot_l.sort()

        this_time_idx = ik50lot_l.index(this_time_lot)
        last_time_idx = this_time_idx - 1
        
        """
        indexが0未満の場合は前回LOTが無いので、'No lot last time'を返して終了
        それ以外は前回LOTを求める"""
        if last_time_idx < 0:
            test_type = 'No lot last time'
            return test_type
        else:
            last_time_lot = ik50lot_l[last_time_idx]

        this_time_year = r'20{}'.format(this_time_lot[:2])
        this_time_month = this_time_lot[2:4]
        last_time_year = r'20{}'.format(last_time_lot[:2])
        last_time_month = last_time_lot[2:4]

        interval_month = (((int(this_time_year) - int(last_time_year)) * 12 
                               + int(this_time_month)) - int(last_time_month))

        if ((this_time_month == '12' or this_time_month == '06') 
            and interval_month == 0):
            test_type = 'A'
        elif ((this_time_month == '11' or this_time_mont == '05')
            and interval_month <= 5):
            test_type = 'A'
        elif ((this_time_month == '10' or this_time_mont == '04')
            and interval_month <= 4):
            test_type = 'A'
        elif ((this_time_month == '09' or this_time_mont == '03')
            and interval_month <= 3):
            test_type = 'A'
        elif ((this_time_month == '08' or this_time_mont == '02')
            and interval_month <= 2):
            test_type = 'A'
        elif ((this_time_month == '07' or this_time_mont == '01')
            and interval_month <= 1):
            test_type = 'A'
        else:
            test_type = 'B'
        return test_type

        """
        (MHS.spec_data.columns
        ['品番', '品名',,, '', '', '',
        '配合後の\n粘度 min', '配合後の\n粘度 max', '', '',
        '配合後の\n加熱残分 min', '配合後の\n加熱残分 max', '中心光度 min', '中心光度 max', '中心光度 結果',
        '', '', '', '', '配合後の容器の中での状態 規格',
        '配合後の容器の中での状態 結果', '作業性 規格', '作業性 結果', '', '', '',
        '', '', '', '耐熱後\n正反射低下', '耐温水性 規格', '耐温水性 結果',
        '', '', '耐湿後\n正反射低下', '', '', '有効期限',
        '', 'Unnamed: 40']



        MHS.test_data.columns
        ['発行', '', '\n品番', '品名', '\nLOT', '', '', '', '',
        '', '', '', '配合後の\n粘度', '', '', '',
        '配合後の\n加熱残分', '中心光度\n1', '中心光度\n2', '中心光度\n3', '中心光度\n4', '中心光度\n5',
        '耐熱後\n 正反射', '耐湿後\n正反射', '薄塗り\n全反射', '薄塗り\n拡散', '薄塗り\n正反射', 'n=1\n全反射',
        'n=1\n拡散', '', 'n=2\n全反射', 'n=2\n拡散', '', 'n=3\n全反射',
        'n=3\n拡散', '', '厚塗り\n全反射', '厚塗り\n拡散', '厚塗り\n正反射', '温度', '湿度',
        '天気', 'その他\n情報', '容器の中での状態', '配合後の容器の中での状態', '作業性', '塗膜の外観', '付着性',
        '耐熱性', '耐熱後\n付着性', '耐温水性', '耐湿性', '耐湿後\n付着性', '冷熱ｻｲｸﾙ', '備考'])
        """



    def coa_data_copy(self, ws_work, ws_format, row, MHS_nonCreate_coa):
        """
        品管ｼｰﾄのworkに、品質試験ﾃﾞｰﾀとﾌｫｰﾏｯﾄ用ﾃﾞｰﾀ(spec)を転記する
        """
        # spec_dataの情報を得る
        """
        locで得たデータはSeriesなので、それのiloc[0]がリテラルのデータとなる
        """

        hinban = row[3]
        lot = row[0]


        coaName         = self.spec_data.loc[self.spec_data['品番']== hinban,  
                                                           '成績書表記'].iloc[0]
        spec_sg_min     = self.spec_data.loc[self.spec_data['品番']== hinban,  
                                                             '比重 min'].iloc[0]
        spec_sg_max     = self.spec_data.loc[self.spec_data['品番']== hinban,  
                                                             '比重 max'].iloc[0]
        spec_vis_min    = self.spec_data.loc[self.spec_data['品番']== hinban,  
                                                             '粘度 min'].iloc[0]
        spec_vis_max    = self.spec_data.loc[self.spec_data['品番']== hinban,  
                                                             '粘度 max'].iloc[0]
        spec_nv_min     = self.spec_data.loc[self.spec_data['品番']== hinban,  
                                                         '加熱残分 min'].iloc[0]
        spec_nv_max     = self.spec_data.loc[self.spec_data['品番']== hinban,  
                                                         '加熱残分 max'].iloc[0]
        spec_ref_min    = self.spec_data.loc[self.spec_data['品番']== hinban,  
                                                         '正反射率 min'].iloc[0]
        spec_ref_max    = self.spec_data.loc[self.spec_data['品番']== hinban,  
                                                         '正反射率 max'].iloc[0]
        spec_eki        = self.spec_data.loc[self.spec_data['品番']== hinban,  
                                                '容器の中での状態 規格'].iloc[0]
        judge_eki       = self.spec_data.loc[self.spec_data['品番']== hinban,  
                                                '容器の中での状態 結果'].iloc[0]
        spec_app        = self.spec_data.loc[self.spec_data['品番']== hinban,  
                                                      '塗膜の外観 規格'].iloc[0]
        judge_app       = self.spec_data.loc[self.spec_data['品番']== hinban,  
                                                      '塗膜の外観 結果'].iloc[0]
        spec_adh        = self.spec_data.loc[self.spec_data['品番']== hinban,  
                                                          '付着性 規格'].iloc[0]
        judge_adh       = self.spec_data.loc[self.spec_data['品番']== hinban,  
                                                          '付着性 結果'].iloc[0]
        spec_heat       = self.spec_data.loc[self.spec_data['品番']== hinban,  
                                                          '耐熱性 規格'].iloc[0]
        judge_heat      = self.spec_data.loc[self.spec_data['品番']== hinban,  
                                                          '耐熱性 結果'].iloc[0]
        spec_humi       = self.spec_data.loc[self.spec_data['品番']== hinban,  
                                                          '耐湿性 規格'].iloc[0]
        judge_humi      = self.spec_data.loc[self.spec_data['品番']== hinban,  
                                                          '耐湿性 結果'].iloc[0]
        spec_cycl       = self.spec_data.loc[self.spec_data['品番']== hinban,  
                                                        '冷熱ｻｲｸﾙ 規格'].iloc[0]
        judge_cycl      = self.spec_data.loc[self.spec_data['品番']== hinban,  
                                                        '冷熱ｻｲｸﾙ 結果'].iloc[0]
        spec_ireme      = self.spec_data.loc[self.spec_data['品番']== hinban,  
                                                               '入れ目'].iloc[0]
        # test_dataの情報を得る
        data_hantei     = self.test_data.loc[self.test_data['\nLOT'] == lot,
                                                                 '判定'].iloc[0]
        data_suu        = self.test_data.loc[self.test_data['\nLOT'] == lot,
                                                                 '缶数'].iloc[0]
        data_sg1        = self.test_data.loc[self.test_data['\nLOT'] == lot,
                                                              '比重\n1'].iloc[0]
        data_sg2        = self.test_data.loc[self.test_data['\nLOT'] == lot,
                                                              '比重\n2'].iloc[0]
        data_sg3        = self.test_data.loc[self.test_data['\nLOT'] == lot,
                                                              '比重\n3'].iloc[0]
        data_vis1       = self.test_data.loc[self.test_data['\nLOT'] == lot,
                                                              '粘度\n1'].iloc[0]
        data_vis2       = self.test_data.loc[self.test_data['\nLOT'] == lot,
                                                              '粘度\n2'].iloc[0]
        data_vis3       = self.test_data.loc[self.test_data['\nLOT'] == lot,
                                                              '粘度\n3'].iloc[0]
        data_nv1        = self.test_data.loc[self.test_data['\nLOT'] == lot,
                                                            '加熱残分1'].iloc[0]
        data_nv2        = self.test_data.loc[self.test_data['\nLOT'] == lot,
                                                            '加熱残分2'].iloc[0]
        data_nv3        = self.test_data.loc[self.test_data['\nLOT'] == lot,
                                                            '加熱残分3'].iloc[0]
        data_ref1       = self.test_data.loc[self.test_data['\nLOT'] == lot,
                                                          'n=1\n正反射'].iloc[0]
        data_ref2       = self.test_data.loc[self.test_data['\nLOT'] == lot,
                                                          'n=2\n正反射'].iloc[0]
        data_ref3       = self.test_data.loc[self.test_data['\nLOT'] == lot,
                                                          'n=3\n正反射'].iloc[0]


        if data_hantei == '合格' or data_hantei == '合格-済':
            # sheets("work")に転記するspec_data
            ws_work.Range("C14").Value = coaName
            ws_work.Range("D14").Value = spec_sg_min
            ws_work.Range("E14").Value = spec_sg_max
            ws_work.Range("F14").Value = spec_vis_min
            ws_work.Range("G14").Value = spec_vis_max
            ws_work.Range("J14").Value = spec_nv_min
            ws_work.Range("K14").Value = spec_nv_max
            ws_work.Range("Q14").Value = spec_ref_min
            ws_work.Range("R14").Value = spec_ref_max
            ws_work.Range("S14").Value = spec_eki
            ws_work.Range("T14").Value = judge_eki
            ws_work.Range("Y14").Value = spec_app
            ws_work.Range("Z14").Value = judge_app
            ws_work.Range("AA14").Value = spec_adh
            ws_work.Range("AB14").Value = judge_adh
            ws_work.Range("AC14").Value = spec_heat
            ws_work.Range("AD14").Value = judge_heat
            ws_work.Range("AH14").Value = spec_humi
            ws_work.Range("AI14").Value = judge_humi
            ws_work.Range("AK14").Value = spec_cycl
            ws_work.Range("AL14").Value = judge_cycl
            ws_work.Range("AN14").Value = spec_ireme
            
            # sheets("work")に転記するtest_data
            ws_work.Range("F20").Value = data_suu
            ws_work.Range("G20").Value = data_sg1
            ws_work.Range("H20").Value = data_sg2
            ws_work.Range("I20").Value = data_sg3
            ws_work.Range("J20").Value = data_vis1
            ws_work.Range("K20").Value = data_vis2
            ws_work.Range("L20").Value = data_vis3
            ws_work.Range("N20").Value = data_nv1
            ws_work.Range("O20").Value = data_nv2
            ws_work.Range("P20").Value = data_nv3
            ws_work.Range("AD20").Value = data_ref1
            ws_work.Range("AG20").Value = data_ref2
            ws_work.Range("AJ20").Value = data_ref3
            
            MHS_nonCreate_coa = self.create_pdf(row, ws_format, MHS_nonCreate_coa)
        else:
            row.append('Did not pass')
            MHS_nonCreate_coa.append(row)


            
            

        return MHS_nonCreate_coa







    def MHS_create_coa(self):
        """
        MHS_nonExistent_coaを基にcoaを作る。作れなかったcoaがあったら、
        MHS_nonCreate_coaのリストを返す
        """
        MHS_nonCreate_coa = []


        EXCEL_PATH = r'//192.168.1.247/Guest/ﾒﾀﾙ品管ｼｰﾄ.xlsm'


        xlapp = win32com.client.Dispatch("Excel.Application")  #Excelの起動
        xlapp.DisplayAlerts = True

        """UpdateLinks = Falseを指定しないと「読み取り専用で開きますか」の
        メッセージが出て止まってしまう。なぜかわからない。"""
        wb = xlapp.Workbooks.Open(EXCEL_PATH, 
                    UpdateLinks = False, ReadOnly = True)

        ws_work = wb.Worksheets('work')
        ws_test = wb.Worksheets('test_db') #book閉じる時にｱｸﾃｨﾌﾞにするｼｰﾄ


        for row in self.nonExistent_coa:
            lot        = row[0]
            hinban     = row[3]
            tantou     = row[4]
            coa_format = row[5]
            
            sheet_format = self.sheet_dic[hinban]
            
            ws_format = wb.Worksheets(sheet_format)
            ws_format.Visible = -1   #Vidible=-1, Hidden=0
            ws_format.Activate()
            
            """IK-50の検査AB判定"""
            test_type = 'A'
            if hinban in self.AB_JUDGE_LIST:
                test_type = self.judge_test_type(lot)

            """coa_data_copyを実行すれば、returnなくてもws_workに転記されるはず
            coa_data_copyの中でshape_copyを呼び出して印をする"""
            MHS_nonCreate_coa = self.coa_data_copy(ws_work, ws_format, 
                                                          row, MHS_nonCreate_coa)



        ws_test.Activate()
        wb.Close(SaveChanges = False)    # 開いたエクセルを閉じる
        xlapp.Quit()    # Excelを終了
        

        return MHS_nonCreate_coa



    
    def create_pdf(self, row, ws_format, MHS_nonCreate_coa):

        # pdfに変換　絶対パスが必要
        """
        try.expectで例外が出たら、MHS_nonCreate_coaにrowを追加する。
        """
        lot = row[0]
        hinban = row[3]
        coa_format = row[5]

        sheet_format = self.sheet_dic[hinban]
        try:
            ws_format.ExportAsFixedFormat(Type = 0, Quality = 0, 
                            Filename = '{}/{}_{}_{}.pdf'
                            .format(self.coa_folder,hinban, lot, sheet_format))
        except Exception as ex:
            print('*****************成績書作成エラー*******************')
            print('{}({})のcoaが作成できませんでした'.format(hinban, lot))
            row.append('pdf error')
            MHS_nonCreate_coa.append(row)
        finally:
            return MHS_nonCreate_coa

