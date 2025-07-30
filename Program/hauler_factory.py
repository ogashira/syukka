#! python
# -*- coding: utf-8 -*-
import csv
import sys
import platform
import pandas as pd
import numpy as np
from typing import List

# サーバー のpython_moduleﾌｫﾙﾀﾞをsys.pathに追加してimport可能にする
shared_folder_path:str = r'/mnt/public/技術課ﾌｫﾙﾀﾞ/200. effit_data/ﾏｽﾀ/運賃計算関係/python_module'
sys.path.append(shared_folder_path)

from i_hauler import IHauler
from torr import Torr
from niigata import Niigata
from keihin import Keihin
from seinou import Seinou


class HaulerFactory :

    def __init__ (self, factory:str) -> None:

        self.factory: str = factory

        self.torr_fare_mtx: List[List[str]] = []
        self.torr_fare_nara_hirosima_mtx: List[List[str]] = []
        self.torr_relay_mtx: List[List[str]] = []
        self.torr_surcharge_mtx: List[List[str]] = []
        self.keihin_fare_mtx: List[List[str]] = []
        self.niigata_fare_mtx: List[List[str]] = []
        self.niigata_relay_mtx: List[List[str]] = []
        self.niigata_surcharge_mtx: List[List[str]] = []
        self.seinou_fare_mtx: List[List[str]] = []
        self.seinou_surcharge_mtx: List[List[str]] = []
        self.seinou_relay_mtx: List[List[str]] = []


        path:str = ''
        if platform.system() == 'Windows':
            path = r'//192.168.1.247/共有/技術課ﾌｫﾙﾀﾞ/200. effit_data/ﾏｽﾀ/運賃計算関係/untin/'
        elif platform.system() == 'Linux':
            path = r'/mnt/public/技術課ﾌｫﾙﾀﾞ/200. effit_data/ﾏｽﾀ/運賃計算関係/untin/'
        elif platform.system() == 'Darwin':
            path = r'/Volumes/共有/技術課ﾌｫﾙﾀﾞ/200. effit_data/ﾏｽﾀ/運賃計算関係/untin/'
        else:
            path = r'./'
        

        if self.factory == 'toke':
            '''
            unsou_file = open(path + 'torr_toke.csv' ,encoding='cp932')
            file_reader = csv.reader(unsou_file)
            self.torr_fare_mtx: List[List[str]] = list(file_reader)
            unsou_file.close()
            '''
            with open(path + 'torr_toke.csv', encoding='cp932') as unsou_file:
                file_reader = csv.reader(unsou_file)
                self.torr_fare_mtx = list(file_reader)

            with open(path + 'torr_toke_nara_hirosima.csv' ,encoding='cp932') as unsou_file:
                file_reader = csv.reader(unsou_file)
                self.torr_fare_nara_hirosima_mtx = list(file_reader)
            
            with open(path + 'torr_tyuukei_toke.csv' ,encoding='cp932') as unsou_file:
                file_reader = csv.reader(unsou_file)
                self.torr_relay_mtx = list(file_reader)

            with open(path + 'torr_surcharge_toke.csv' ,encoding='cp932') as unsou_file:
                file_reader = csv.reader(unsou_file)
                self.torr_surcharge_mtx = list(file_reader)

            with open(path + 'keihin_toke.csv' ,encoding='cp932') as unsou_file:
                file_reader = csv.reader(unsou_file)
                self.keihin_fare_mtx = list(file_reader)

            with open(path + 'niigata_toke.csv' ,encoding='cp932') as unsou_file:
                file_reader = csv.reader(unsou_file)
                self.niigata_fare_mtx = list(file_reader)

            with open(path + 'niigata_tyuukei_toke.csv' ,encoding='cp932') as unsou_file:
                file_reader = csv.reader(unsou_file)
                self.niigata_relay_mtx = list(file_reader)

            with open(path + 'niigata_surcharge_toke.csv' ,encoding='cp932') as unsou_file:
                file_reader = csv.reader(unsou_file)
                self.niigata_surcharge_mtx = list(file_reader)

            with open(path + 'seinou_toke.csv' ,encoding='cp932') as unsou_file:
                file_reader = csv.reader(unsou_file)
                self.seinou_fare_mtx = list(file_reader)

            with open(path + 'seinou_surcharge_toke.csv' ,encoding='cp932') as unsou_file:
                file_reader = csv.reader(unsou_file)
                self.seinou_surcharge_mtx = list(file_reader)

        elif self.factory == 'honsya':
            with open(path + 'torr_honsya.csv' ,encoding='cp932') as unsou_file:
                file_reader = csv.reader(unsou_file)
                self.torr_fare_mtx = list(file_reader)

            with open(path + 'torr_tyuukei_honsya.csv' ,encoding='cp932') as unsou_file:
                file_reader = csv.reader(unsou_file)
                self.torr_relay_mtx = list(file_reader)

            with open(path + 'niigata_honsya.csv' ,encoding='cp932') as unsou_file:
                file_reader = csv.reader(unsou_file)
                self.niigata_fare_mtx = list(file_reader)

            with open(path + 'niigata_tyuukei_honsya.csv' ,encoding='cp932') as unsou_file:
                file_reader = csv.reader(unsou_file)
                self.niigata_relay_mtx = list(file_reader)

            with open(path + 'keihin_honsya.csv' ,encoding='cp932') as unsou_file:
                file_reader = csv.reader(unsou_file)
                self.keihin_fare_mtx = list(file_reader)





    def create_torr(self) -> IHauler:
        torr: IHauler = Torr( self.torr_fare_mtx,
                              self.torr_fare_nara_hirosima_mtx,
                              self.torr_relay_mtx,
                              self.torr_surcharge_mtx)
        return torr

    def create_niigata(self) -> IHauler:
        niigata: IHauler = Niigata( self.niigata_fare_mtx,
                              self.niigata_relay_mtx,
                              self.niigata_surcharge_mtx)
        return niigata
                
    def create_keihin(self) -> IHauler:
        keihin: IHauler = Keihin(self.keihin_fare_mtx)
        return keihin
        
        
    def create_seinou(self) -> IHauler:
        seinou: IHauler = Seinou( self.seinou_fare_mtx,
                                  self.seinou_relay_mtx,
                                  self.seinou_surcharge_mtx
                                )
        return seinou


