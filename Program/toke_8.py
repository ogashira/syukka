#! python
# -*- coding: cp932 -*-


from packing import *
from ajust_untin import *
from gyoumu import *

pd.set_option('display.unicode.east_asian_width', True)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', None)

class Toke:

    def __init__(self, myfolder):


        self.myfolder = myfolder
        packing = Packing()
        
        self.toke_moto = packing.get_toke_moto()
        if self.toke_moto.empty:
            self.toke_untin = self.toke_moto
            self.allHauler = self.toke_moto
            self.packingHinban = self.toke_moto
            self.untinForUriage = self.toke_moto
            self.sorting = self.toke_moto
        else:
            self.toke_untin = packing.get_untin_toke()
            
            ajust_toke = Ajust_toke(self.myfolder)
            
            self.allHauler = ajust_toke.get_allHauler(self.toke_moto, 
                    self.toke_untin)
            self.packingHinban = ajust_toke.get_packingHinban(self.toke_moto, 
                    self.allHauler)
            self.untinForUriage = ajust_toke.get_untinForUriage(self.toke_moto,
                    self.allHauler)

            # untinForUriage縺ｫpackingHinban縺ｮ'蜃ｺ闕ｷ莠亥ｮ壼�れる>>>>>>>>>
            # この時点でuntinForUriageから出荷予定倉庫を削除して、packingHinbanの
            # 出荷予定倉庫を結合するので、robot_logで表示される出荷予定倉庫は
            # 入れ替え前のものとなる。
            merge_data = self.packingHinban[['受注ＮＯ', '受注行ＮＯ', 
                                                             '出荷予定倉庫']]
            UU = self.untinForUriage.drop(columns = '出荷予定倉庫')
            
            self.untinForUriage = pd.merge(UU, merge_data, on= ['受注ＮＯ', 
                                                    '受注行ＮＯ'], how = 'left')



            
            #untinForUriageをいったん保存
            filePath_eigyou = '{}/{}営業_uriage.xlsx'.format(self.myfolder, '土気')
            self.untinForUriage.to_excel(filePath_eigyou)

            

            gyoumu = Gyoumu(self.myfolder)

            # sortingを作って、エクセルで保存
            self.sorting = gyoumu.get_sorting(self.packingHinban, self.myfolder, '土気')
            filePath_gyoumu = '{}/{}業務_packing.xlsx'.format(self.myfolder, '土気')
            
            # sortingのスタイル調整して再保存
            gyoumu.get_excel_style(filePath_gyoumu)
            # untinForUriageのスタイル調整して再保存
            gyoumu.get_excel_style(filePath_eigyou)



            del gyoumu



            self.packingCoa = ajust_toke.get_packingCoa(self.packingHinban, 
                    self.untinForUriage)
            
            del ajust_toke


        
        del packing




    #元データ(toke)を取得する
    def get_toke_moto(self):
        return self.toke_moto

    #運賃データ(toke)を取得する
    def get_toke_untin(self):
        return self.toke_untin

    #全運賃表を取得する
    def get_allHauler(self):
        return self.allHauler

    #仕分け表の元を取得する
    def get_packingHinban(self):
        return self.packingHinban

    # 仕分け表を取得する
    def get_sorting(self):
        return self.sorting
    

    #売上入力用ﾃﾞｰﾀを取得する
    def get_untinForUriage(self):
        return self.untinForUriage

    # 成績表用仕分け表を取得する
    def get_packingCoa(self):
        return self.packingCoa



