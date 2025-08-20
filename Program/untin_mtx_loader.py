from typing import List
import csv
import platform


class untinMtxLoader:
    def __init__(self, factory: str) -> None:
        self.factory: str = factory

        self.path:str = ''
        if platform.system() == 'Windows':
            self.path = r'//192.168.1.247/共有/技術課ﾌｫﾙﾀﾞ/200. effit_data/ﾏｽﾀ/運賃計算関係/untin/'
        elif platform.system() == 'Linux':
            self.path = r'/mnt/public/技術課ﾌｫﾙﾀﾞ/200. effit_data/ﾏｽﾀ/運賃計算関係/untin/'
        elif platform.system() == 'Darwin':
            self.path = r'/Volumes/共有/技術課ﾌｫﾙﾀﾞ/200. effit_data/ﾏｽﾀ/運賃計算関係/untin/'
        else:
            self.path = r'./'
        

class TorrUntinMtxLoader(untinMtxLoader):
    def __init__(self, factory: str) -> None:
        super().__init__(factory)

        self.torr_fare_mtx: List[List[str]] = []
        self.torr_fare_nara_hirosima_mtx: List[List[str]] = []
        self.torr_relay_mtx: List[List[str]] = []
        self.torr_surcharge_mtx: List[List[str]] = []

        if self.factory == 'toke':
            with open(self.path + 'torr_toke.csv', encoding='cp932') as unsou_file:
                file_reader = csv.reader(unsou_file)
                self.torr_fare_mtx = list(file_reader)

            with open(self.path + 'torr_toke_nara_hirosima.csv' ,encoding='cp932') as unsou_file:
                file_reader = csv.reader(unsou_file)
                self.torr_fare_nara_hirosima_mtx = list(file_reader)
            
            with open(self.path + 'torr_tyuukei_toke.csv' ,encoding='cp932') as unsou_file:
                file_reader = csv.reader(unsou_file)
                self.torr_relay_mtx = list(file_reader)

            with open(self.path + 'torr_surcharge_toke.csv' ,encoding='cp932') as unsou_file:
                file_reader = csv.reader(unsou_file)
                self.torr_surcharge_mtx = list(file_reader)

        elif self.factory == 'honsya':
            with open(self.path + 'torr_honsya.csv' ,encoding='cp932') as unsou_file:
                file_reader = csv.reader(unsou_file)
                self.torr_fare_mtx = list(file_reader)

            with open(self.path + 'torr_tyuukei_honsya.csv' ,encoding='cp932') as unsou_file:
                file_reader = csv.reader(unsou_file)
                self.torr_relay_mtx = list(file_reader)


class NiigataUntinMtxLoader(untinMtxLoader):
    def __init__(self, factory)-> None:
        super().__init__(factory)

        self.niigata_fare_mtx: List[List[str]] = []
        self.niigata_relay_mtx: List[List[str]] = []
        self.niigata_surcharge_mtx: List[List[str]] = []

        if self.factory == 'toke':
            with open(self.path + 'niigata_toke.csv' ,encoding='cp932') as unsou_file:
                file_reader = csv.reader(unsou_file)
                self.niigata_fare_mtx = list(file_reader)

            with open(self.path + 'niigata_tyuukei_toke.csv' ,encoding='cp932') as unsou_file:
                file_reader = csv.reader(unsou_file)
                self.niigata_relay_mtx = list(file_reader)

            with open(self.path + 'niigata_surcharge_toke.csv' ,encoding='cp932') as unsou_file:
                file_reader = csv.reader(unsou_file)
                self.niigata_surcharge_mtx = list(file_reader)
        elif self.factory == 'honsya':
            with open(self.path + 'niigata_honsya.csv' ,encoding='cp932') as unsou_file:
                file_reader = csv.reader(unsou_file)
                self.niigata_fare_mtx = list(file_reader)

            with open(self.path + 'niigata_tyuukei_honsya.csv' ,encoding='cp932') as unsou_file:
                file_reader = csv.reader(unsou_file)
                self.niigata_relay_mtx = list(file_reader)


class KeihinUntinMtxLoader(untinMtxLoader):
    def __init__(self, factory)-> None:
        super().__init__(factory)

        self.keihin_fare_mtx: List[List[str]] = []
        if self.factory == 'toke':
            with open(self.path + 'keihin_toke.csv' ,encoding='cp932') as unsou_file:
                file_reader = csv.reader(unsou_file)
                self.keihin_fare_mtx = list(file_reader)
        elif self.factory == 'honsya':
            with open(self.path + 'keihin_honsya.csv' ,encoding='cp932') as unsou_file:
                file_reader = csv.reader(unsou_file)
                self.keihin_fare_mtx = list(file_reader)


class SeinouUntinMtxLoader(untinMtxLoader):
    def __init__(self, factory)-> None:
        super().__init__(factory)

        self.seinou_fare_mtx: List[List[str]] = []
        self.seinou_surcharge_mtx: List[List[str]] = []
        self.seinou_relay_mtx: List[List[str]] = []
        if self.factory == 'toke':
            with open(self.path + 'seinou_toke.csv' ,encoding='cp932') as unsou_file:
                file_reader = csv.reader(unsou_file)
                self.seinou_fare_mtx = list(file_reader)

            with open(self.path + 'seinou_surcharge_toke.csv' ,encoding='cp932') as unsou_file:
                file_reader = csv.reader(unsou_file)
                self.seinou_surcharge_mtx = list(file_reader)
        elif self.factory == 'honsya':
            pass

