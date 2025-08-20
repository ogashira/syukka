#! python
# -*- coding: utf-8 -*-
import sys
import platform
import pandas as pd
import numpy as np
from untin_mtx_loader import TorrUntinMtxLoader
from untin_mtx_loader import NiigataUntinMtxLoader
from untin_mtx_loader import KeihinUntinMtxLoader
from untin_mtx_loader import SeinouUntinMtxLoader

# サーバー のpython_moduleﾌｫﾙﾀﾞをsys.pathに追加してimport可能にする
shared_folder_path:str = r'./'
if platform.system() == 'Linux':
    shared_folder_path = r'/mnt/public/技術課ﾌｫﾙﾀﾞ/200. effit_data/ﾏｽﾀ/運賃計算関係/python_module'
elif platform.system() == 'Windows':
    shared_folder_path = r'//192.168.1.247/共有/技術課ﾌｫﾙﾀﾞ/200. effit_data/ﾏｽﾀ/運賃計算関係/python_module'
else:
    shared_folder_path = r'./'

sys.path.append(shared_folder_path)

from i_hauler import IHauler
from torr import Torr
from niigata import Niigata
from keihin import Keihin
from seinou import Seinou


class HaulerFactory :


    @staticmethod
    def create_torr(factory: str) -> IHauler:
        torr_untin_mtx_loader = TorrUntinMtxLoader(factory)
        torr: IHauler = Torr( torr_untin_mtx_loader.torr_fare_mtx,
                              torr_untin_mtx_loader.torr_fare_nara_hirosima_mtx,
                              torr_untin_mtx_loader.torr_relay_mtx,
                              torr_untin_mtx_loader.torr_surcharge_mtx)
        return torr


    @staticmethod
    def create_niigata(factory: str) -> IHauler:
        niigata_untin_mtx_loader = NiigataUntinMtxLoader(factory)
        niigata: IHauler = Niigata( niigata_untin_mtx_loader.niigata_fare_mtx,
                              niigata_untin_mtx_loader.niigata_relay_mtx,
                              niigata_untin_mtx_loader.niigata_surcharge_mtx)
        return niigata
                

    @staticmethod
    def create_keihin(factory: str) -> IHauler:
        keihin_untin_mtx_loader = KeihinUntinMtxLoader(factory)
        keihin: IHauler = Keihin(keihin_untin_mtx_loader.keihin_fare_mtx)
        return keihin
        
        
    @staticmethod
    def create_seinou(factory: str) -> IHauler:
        seinou_untin_mtx_loader = SeinouUntinMtxLoader(factory)
        seinou: IHauler = Seinou( seinou_untin_mtx_loader.seinou_fare_mtx,
                                  seinou_untin_mtx_loader.seinou_relay_mtx,
                                  seinou_untin_mtx_loader.seinou_surcharge_mtx
                                )
        return seinou
