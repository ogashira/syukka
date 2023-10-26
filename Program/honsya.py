#! python
# -*- coding: utf-8 -*-


from packing import *
from ajust_untin import *
from gyoumu import *

pd.set_option('display.unicode.east_asian_width', True)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', None)

class Honsya:
    """
    allHaulerの得意先コード、納入先コードはunsoutaiou_honsyaのデータの
    右端の値。これらは、allHaulerで表示されるが、その後の計算では
    使用されないため、間違っていいても問題ない。
    """

    def __init__(self, myfolder, uriagebi, sengetu):


        self.myfolder = myfolder
        self.uriagebi = uriagebi
        self.sengetu = sengetu
        packing = Packing(uriagebi, sengetu)
        
        self.honsya_moto = packing.get_honsya_moto()
        if self.honsya_moto.empty:
            self.honsya_untin = self.honsya_moto
            self.allHauler = self.honsya_moto
            self.packingHinban = self.honsya_moto
            self.untinForUriage = self.honsya_moto
            self.sorting = self.honsya_moto
        else:
            self.honsya_untin = packing.get_untin_honsya()

            ajust_honsya = Ajust_honsya(self.myfolder,self.uriagebi, self.sengetu)

            self.allHauler = ajust_honsya.get_allHauler(self.honsya_moto, 
                                                        self.honsya_untin)
            self.packingHinban = ajust_honsya.get_packingHinban(self.honsya_moto, 
                    self.allHauler)
            self.untinForUriage = ajust_honsya.get_untinForUriage(self.honsya_moto, 
                    self.allHauler)
            
            # untinForUriageにpackingHinbanの'出荷予定倉庫'を取り入れる>>>>>>>>>
            # この時点でuntinForUriageから出荷予定倉庫を削除して、packingHinbanの
            # 出荷予定倉庫を結合するので、robot_logで表示される出荷予定倉庫は
            # 入れ替え前のものとなる。
            """
            2021/2/26 robot_logの表示をこの時点で行うように変更した。
            ajust_untinからrecorder.out_log,recorder.out_fileをここに
            移動した。
            """
            merge_data = self.packingHinban[['受注ＮＯ', '受注行ＮＯ', 
                                                             '出荷予定倉庫']]
            UU = self.untinForUriage.drop(columns = '出荷予定倉庫')
            
            self.untinForUriage = pd.merge(UU, merge_data, on= ['受注ＮＯ', 
                                                    '受注行ＮＯ'], how = 'left')

            recorder = Recorder(self.myfolder)




            txt ='運賃計算結果一覧（本社）' 
            recorder.out_log(txt, '\n')
            recorder.out_file(txt, '\n')

            recorder.out_log(self.allHauler, '\n')
            recorder.out_file(self.allHauler, '\n')
            recorder.out_log('')
            recorder.out_file('')

            txt ='売上処理入力用ﾃﾞｰﾀ（本社）' 
            recorder.out_log(txt, '\n')
            recorder.out_file(txt, '\n')

            recorder.out_log(self.untinForUriage, '\n')
            recorder.out_file(self.untinForUriage, '\n')
            del recorder

            
            #untinForUriageをいったん保存
            filePath_eigyou = '{}/{}営業_uriage.xlsx'.format(self.myfolder, '本社')
            self.untinForUriage.to_excel(filePath_eigyou)
            


            gyoumu = Gyoumu(self.myfolder)

            # sortingを作って、エクセルで保存
            # self.sorting = gyoumu.get_sorting(self.packingHinban, self.myfolder, '本社')
            # filePath_gyoumu = '{}/{}業務_packing.xlsx'.format(self.myfolder, '本社')

            # sortingのスタイル調整して再保存
            # gyoumu.get_excel_style(filePath_gyoumu)
            # untinForUriageのスタイル調整して再保存
            gyoumu.get_excel_style(filePath_eigyou)


            del gyoumu
        

            del ajust_honsya


        del packing


    #元データ(honsya)を取得する
    def get_honsya_moto(self):
        return self.honsya_moto

    #運賃データ(honsya)を取得する
    def get_honsya_untin(self):
        return self.honsya_untin

    #全運賃表を取得する
    def get_allHauler(self):
        return self.allHauler

    #仕分け表の元を取得する
    def get_packingHinban(self):
        return self.packingHinban

    # 仕分け表を取得する
    # def get_sorting(self):
        # return self.sorting

    # 売上入力用ﾃﾞｰﾀを取得する
    def get_untinForUriage(self):
        return self.untinForUriage


    """
    # 成績表用仕分け表を取得する
    def get_packingCoa(self):
        return self.packingCoa
    """


