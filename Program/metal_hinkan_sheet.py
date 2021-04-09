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
        
        nonExistent_coa_lot = [] """get_hinken_dataに渡す"""
        nonExistent_coa_hinban = [] """spec_dataに渡す"""
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
        else: """空のDataFrame"""
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
MHS.spec_data.columns
['品番', '品名', '成績書表記', '比重 min', '比重 max', '粘度 min', '粘度 max',
'配合後の\n粘度 min', '配合後の\n粘度 max', '加熱残分 min', '加熱残分 max',
'配合後の\n加熱残分 min', '配合後の\n加熱残分 max', '中心光度 min', '中心光度 max', '中心光度 結果',
'正反射率 min', '正反射率 max', '容器の中での状態 規格', '容器の中での状態 結果', '配合後の容器の中での状態 規格',
'配合後の容器の中での状態 結果', '作業性 規格', '作業性 結果', '塗膜の外観 規格', '塗膜の外観 結果', '付着性 規格',
'付着性 結果', '耐熱性 規格', '耐熱性 結果', '耐熱後\n正反射低下', '耐温水性 規格', '耐温水性 結果',
'耐湿性 規格', '耐湿性 結果', '耐湿後\n正反射低下', '冷熱ｻｲｸﾙ 規格', '冷熱ｻｲｸﾙ 結果', '有効期限',
'入れ目', 'Unnamed: 40']



MHS.test_data.columns
['発行', '判定', '\n品番', '品名', '\nLOT', '缶数', '比重\n1', '比重\n2', '比重\n3',
'粘度\n1', '粘度\n2', '粘度\n3', '配合後の\n粘度', '加熱残分1', '加熱残分2', '加熱残分3',
'配合後の\n加熱残分', '中心光度\n1', '中心光度\n2', '中心光度\n3', '中心光度\n4', '中心光度\n5',
'耐熱後\n 正反射', '耐湿後\n正反射', '薄塗り\n全反射', '薄塗り\n拡散', '薄塗り\n正反射', 'n=1\n全反射',
'n=1\n拡散', 'n=1\n正反射', 'n=2\n全反射', 'n=2\n拡散', 'n=2\n正反射', 'n=3\n全反射',
'n=3\n拡散', 'n=3\n正反射', '厚塗り\n全反射', '厚塗り\n拡散', '厚塗り\n正反射', '温度', '湿度',
'天気', 'その他\n情報', '容器の中での状態', '配合後の容器の中での状態', '作業性', '塗膜の外観', '付着性',
'耐熱性', '耐熱後\n付着性', '耐温水性', '耐湿性', '耐湿後\n付着性', '冷熱ｻｲｸﾙ', '備考']
"""




    def coa_data_copy(self, ws_work, ws_format, ws_inn, row, HS_nonCreate_coa):
        """
        品管ｼｰﾄのworkに、品質試験ﾃﾞｰﾀとﾌｫｰﾏｯﾄ用ﾃﾞｰﾀ(spec)を転記する
        """
        # spec_dataの情報を得る
        """
        locで得たデータはSeriesなので、それのiloc[0]がリテラルのデータとなる
        """

        hinban = row[3]
        lot = row[0]









        return MHS_nonCreate_coa







    def HS_create_coa(self):
        """
        MHS_nonExistent_coaを基にcoaを作る。作れなかったcoaがあったら、
        MHS_nonCreate_coaのリストを返す
        """
        MHS_nonCreate_coa = []


        EXCEL_PATH = r'//192.168.1.247/Guest/ﾒﾀﾙ品管ｼｰﾄ.xlsm'


        xlapp = win32com.client.Dispatch("Excel.Application")  """Excelの起動"""
        xlapp.DisplayAlerts = True

        """UpdateLinks = Falseを指定しないと「読み取り専用で開きますか」の
        メッセージが出て止まってしまう。なぜかわからない。"""
        wb = xlapp.Workbooks.Open(EXCEL_PATH, 
                    UpdateLinks = False, ReadOnly = True)

        ws_work = wb.Worksheets('work')
        ws_test = wb.Worksheets('test_db') """book閉じる時にｱｸﾃｨﾌﾞにするｼｰﾄ"""


        for row in self.nonExistent_coa:
            lot        = row[0]
            hinban     = row[3]
            tantou     = row[4]
            coa_format = row[5]
            
            sheet_format = self.sheet_dic[hinban]
            
            ws_format = wb.Worksheets(sheet_format)
            ws_format.Visible = -1   """Vidible=-1, Hidden=0"""
            ws_format.Activate()
            
            """IK-50の検査AB判定"""
            test_type = 'A'
            if hinban in self.AB_JUDGE_LIST:
                test_type = self.judge_test_type(lot)

            """coa_data_copyを実行すれば、returnなくてもws_workに転記されるはず
            coa_data_copyの中でshape_copyを呼び出して印をする"""
            MHS_nonCreate_coa = self.coa_data_copy(ws_work, ws_format, ws_inn, 
                                                          row, HS_nonCreate_coa)



        ws_test.Activate()
        wb.Close(SaveChanges = False)    # 開いたエクセルを閉じる
        xlapp.Quit()    # Excelを終了
        

        return MHS_nonCreate_coa
