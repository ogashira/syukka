#! python
# -*- coding: utf-8 -*-

import pandas as pd
import datetime
import numpy as np
import pickle
from recorder import *


class UriageSumi(object):

    def __init__ (self, myfolder):

        self.myfolder = myfolder

        uriage_sumi = pd.read_csv(
                r'../master/effitA/uriage_sumi.csv', 
                skiprows = 1,
                encoding='cp932'
        )
        uriage_sumi = uriage_sumi.rename(
                columns = {
                    '売上日':'出荷予定日',
                    '運送業者':'依頼先',
                    '自由使用区分１':'配送区分',
                    '請求予定年月日':'closeDate',
                    '管理個数':'受注数量',
                    '管理単位':'受注単位',
                    '振替元品番':'hinban',
                    '振替元数量':'cans',
                    'ロットＮＯ':'lot',
                }
        )
        # uriage_sumiの備考のNaNを処理する。2021/2/11 
        uriage_sumi = uriage_sumi.fillna({'備考':'noData'})

        uriage_sumi['出荷予定日'] = uriage_sumi['出荷予定日'].map(
                lambda x : '{}/{}/{}'.format(str(x)[:4],str(x)[4:6],str(x)[6:])
        )
        uriage_sumi['closeDate'] = uriage_sumi['closeDate'].map(
                lambda x : '{}/{}/{}'.format(str(x)[:4],str(x)[4:6],str(x)[6:])
        )
        uriage_sumi['納期'] = uriage_sumi['納期'].map(
                lambda x : '{}/{}/{}'.format(str(x)[:4],str(x)[4:6],str(x)[6:])
        )

        self.uriage_sumi = uriage_sumi[uriage_sumi['得意先コード'] < 'T6000']


    def get_uriage_sumi(self):
        '''
        self.uriage_sumiに'lot_dic'列を追加して{lot:cans}の辞書を得る
        次に、self.uriage_sumiは複数LOTの場合はLOTごとに行があるので、
        重複する受注no、受注行noで、{lot:cans, lot:cans} の形にまとめて１行にする。
        '''

        def get_dic_lot (row):
            # {lot:cans}の形にする
            dic_lot = {}
            lot = row['lot']
            if pd.isnull(row['hinban']):
                cans = row['受注数量']
            else:
                cans = row['cans']
            dic_lot[lot] = cans
            return dic_lot

        uriage_sumi = self.uriage_sumi.copy()
        uriage_sumi['dic_lot'] = uriage_sumi.apply(get_dic_lot, axis=1)

        uriage_sumi = uriage_sumi.sort_values(['受注ＮＯ', '受注行ＮＯ'])
        uriage_sumi = uriage_sumi.reset_index()

        # dic_lotを{'21011201H': 15, '21011501H': 3}の形にする
        # 受注数量も削除する分を残す分に加える。
        for i in range(len(uriage_sumi)-1):
            JNo = uriage_sumi.loc[i, '受注ＮＯ']
            JGNo = uriage_sumi.loc[i, '受注行ＮＯ']
            dic_lot = uriage_sumi.loc[i, 'dic_lot']
            Jsuu = uriage_sumi.loc[i, '受注数量']
            j = 1
            while uriage_sumi.loc[i+j, '受注ＮＯ'] == JNo and (
                    uriage_sumi.loc[i+j, '受注行ＮＯ'] == JGNo):
                add_dic_lot = uriage_sumi.loc[i+j, 'dic_lot']
                add_lot = [k for k, v in add_dic_lot.items()][0]
                add_cans = [v for k, v in add_dic_lot.items()][0]
                add_Jsuu = uriage_sumi.loc[i+j, '受注数量']

                dic_lot[add_lot] = add_cans
                Jsuu = Jsuu + add_Jsuu

                # .locではエラーになる。辞書やﾘｽﾄを代入するときは.atを使う
                # .locでは複数選択の意味があるので単一セルしか選択できない.atを使う
                uriage_sumi.at[i, 'dic_lot'] = dic_lot
                uriage_sumi.loc[i, '受注数量'] = Jsuu

                uriage_sumi.loc[i+j, '得意先注文ＮＯ'] = 'del'

                # i+jが最終行であったらwhileを抜ける
                if i + j == len(uriage_sumi)-1:
                    break

                j += 1

        uriage_sumi2 = uriage_sumi.loc[uriage_sumi['得意先注文ＮＯ'] != 'del', :]

        return uriage_sumi2



    def get_output_sumi(self, output):
        uriage_sumi = self.get_uriage_sumi()

        output_sumi = pd.merge(output, uriage_sumi, on =['受注ＮＯ', '受注行ＮＯ'], how = 'left')

        return output_sumi




    def check_sumi(self, UU_sumi):

        # data.pickleからﾀﾞｳﾝﾛｰﾄﾞ
        with open(r'./data.pickle', 'rb') as f:
            data_loaded = pickle.load(f)

        unsou_dic = data_loaded['unsou_dic'] 
        haisou_kubun = data_loaded['haisou_kubun']
        souko_dic = data_loaded['souko_dic']



        def kubun_hantei(syukka_yotei_souko):
            
            if '営業所' in syukka_yotei_souko: 
                return 3
            elif '土曜配達' in syukka_yotei_souko:
                return 2
            elif '曜日' in syukka_yotei_souko:
                return 4
            else:
                return 1


        # UU_sumi2の総合判定する 
        def final_hantei(df_row):
            txt = ''
            syukkabi = df_row['出荷日']
            tokuisaki = df_row['得意先']
            unsou = df_row['運送']
            kubun = df_row['配送区分']
            closeDate = df_row['締め日']
            souko = df_row['出荷場所']
            hinban = df_row['品番']
            suu = df_row['数量']
            lot = df_row['lot']

            if pd.isnull(syukkabi):
                pass
            else:
                txt= txt + '出荷日,' if syukkabi == 'ng' else txt
                txt= txt + '得意先,' if tokuisaki == 'ng' else txt
                txt= txt + '運送,' if unsou == 'ng' else txt
                txt= txt + '配送区分,' if kubun == 'ng' else txt
                txt= txt + '締め日,' if closeDate == 'ng' else txt
                txt= txt + '出荷場所,' if souko == 'ng' else txt
                txt= txt + '品番,' if hinban == 'ng' else txt
                txt= txt + '数量,' if suu == 'ng' else txt
                txt= txt + 'lot,' if lot == 'ng' else txt
                
                txt = 'ALL OK' if txt == '' else txt + '-> NG'

            return txt


            



        def check(df_row):

            syukkabi = np.nan
            tokuisaki = np.nan
            unsou = np.nan
            kubun = np.nan
            closeDate = np.nan
            souko = np.nan
            hinban = np.nan
            suuryou = np.nan
            lot = np.nan

            if  not pd.isnull(df_row['売上ＮＯ']):
                UU_syukkabi = df_row['出荷予定日_x']
                sumi_syukkabi = df_row['出荷予定日_y']
                UU_tokuisaki = df_row['得意先コード_x']
                sumi_tokuisaki = df_row['得意先コード_y']
                UU_unsou = unsou_dic[df_row['依頼先_x']]
                sumi_unsou = df_row['依頼先_y']
                UU_kubun = kubun_hantei(df_row['出荷予定倉庫'])
                sumi_kubun = df_row['配送区分']
                UU_closeDate = df_row['closeDate_x']
                sumi_closeDate = df_row['closeDate_y']
                UU_souko = souko_dic[df_row['出荷']]
                sumi_souko = df_row['出庫元倉庫']
                UU_hinban = df_row['品番_x']
                sumi_hinban = df_row['品番_y']
                UU_suuryou = df_row['受注数量_x']
                sumi_suuryou = df_row['受注数量_y']
                UU_lot = df_row['lot_x']
                sumi_lot = df_row['dic_lot']

                syukkabi = 'ok' if UU_syukkabi == sumi_syukkabi else 'ng'
                tokuisaki = 'ok' if UU_tokuisaki == sumi_tokuisaki else 'ng'
                unsou = 'ok' if UU_unsou == sumi_unsou else 'ng' 
                kubun = 'ok' if UU_kubun == sumi_kubun else 'ng' 
                closeDate = 'ok' if UU_closeDate == sumi_closeDate else 'ng' 
                souko = 'ok' if UU_souko == sumi_souko else 'ng' 
                hinban = 'ok' if UU_hinban == sumi_hinban else 'ng' 
                suuryou = 'ok' if UU_suuryou == sumi_suuryou else 'ng'
                lot = 'ok' if UU_lot == sumi_lot else 'ng'

            return pd.Series([syukkabi, tokuisaki, unsou, kubun, closeDate, 
                              souko, hinban, suuryou, lot])

        UU_sumi[['出荷日','得意先','運送','配送区分','締め日','出荷場所','品番',
                 '数量', 'lot']] = UU_sumi.apply(check, axis=1)
        
        UU_sumi2 = UU_sumi[['受注ＮＯ', '受注行ＮＯ', '出荷日','得意先','運送',
                            '配送区分','締め日','出荷場所','品番', '数量', 'lot'
        ]]


        UU_sumi3 = UU_sumi2.copy()
        UU_sumi3.loc[:,'総合判定'] = UU_sumi3.apply(final_hantei, axis=1)
        


        recorder = Recorder(self.myfolder)
        txt = '売上入力後のﾁｪｯｸ >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'
        recorder.out_log(txt, '\n')
        recorder.out_log(UU_sumi3, '\n')
        recorder.out_file(txt, '\n')
        recorder.out_file(UU_sumi3, '\n')


