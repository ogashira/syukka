#! python
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
from hauler_factory import HaulerFactory


class Untin_toke :

    def __init__ (self) -> None:

        hauler_factory: HaulerFactory = HaulerFactory('toke')
        self.torr:IHauler =hauler_factory.create_torr()
        self.niigata:IHauler= hauler_factory.create_niigata()
        self.keihin:IHauler = hauler_factory.create_keihin()
        self.seinou:IHauler = hauler_factory.create_seinou()



	#applyでdfの行を受け取る
    def get_untin(self, df_row):
        nounyuusaki = df_row['納入先名称１']
        weight = df_row['weight']
        address = df_row['住所１']
        torr_dist = df_row['ﾄｰﾙ距離']
        torr_tyuukei = df_row['ﾄｰﾙ中継回数']
        torr_YN = df_row['ﾄｰﾙ行く行かない']
        niigata_dist = df_row['新潟距離']
        niigata_tyuukei = df_row['新潟中継回数']
        niigata_YN = df_row['新潟行く行かない']
        keihin = df_row['ｹｲﾋﾝ向']
        designation = df_row['顧客指定運送屋']
        seinou_dist = df_row['西濃距離']

        if address != 'NoCalc' and address is not np.nan:
            torr_fare:float = self.torr.calc_fare(
                            torr_dist,
                            weight,
                            torr_YN,
                            torr_tyuukei,
                            address
                            )

            niigata_fare:float = self.niigata.calc_fare(
                            niigata_dist,
                            weight,
                            niigata_YN,
                            niigata_tyuukei
                            )  

            #ケイヒンの運賃表は横軸が重量、縦軸が行先（横浜、静岡..など）
            #dictは0(使用しない)とし、縦軸の行先を仮引数addressに設定する
            keihin_fare:float = self.keihin.calc_fare(
                            0,
                            weight,
                            YN = keihin,
                            )

            seinou_fare:float = self.seinou.calc_fare(
                            seinou_dist,
                            weight
                            )
        else:
            torr_fare = 0
            niigata_fare = 0
            keihin_fare = 0
            seinou_fare = 0

        return pd.Series([torr_fare,niigata_fare, keihin_fare, seinou_fare])

