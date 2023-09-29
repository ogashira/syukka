#! python
# -*- coding: utf-8 -*-

from packing import *
from ajust_untin import *
from recorder import *
from eigyoubi import *




while True:
    try:
        uriagebi = input('売上日を入力してください(例: 20201204) :')
        if (
        len(uriagebi) == 8 and
        2020 <= int(uriagebi[:4]) <= 2100 and
        1 <= int(uriagebi[4:6]) <= 12 and
        1 <= int(uriagebi[6:]) <= 31
        ):
            break
    except:
        pass
    print('正しい年月日を入力してください(例: 20200930)')


pd.set_option('display.unicode.east_asian_width', True)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', None)


eigyoubi = Eigyoubi()
sengetu = eigyoubi.get_sengetu()
del eigyoubi

myfolder = r'C:/Users/toyo-pc12/Documents/Untin.csv'

packing = Packing(uriagebi, sengetu)

toke_moto = packing.get_toke_moto()
if toke_moto.empty:
    toke_untin = toke_moto
    AH_toke = toke_moto
    PH_toke = toke_moto
    #UU_toke = toke_moto
else:
    toke_untin =packing.get_untin_toke()
    ajust_toke = Ajust_toke(myfolder, uriagebi, sengetu)
    AH_toke = ajust_toke.get_allHauler(toke_moto, toke_untin)
    PH_toke = ajust_toke.get_packingHinban(toke_moto, AH_toke)
    #UU_toke = ajust_toke.get_untinForUriage(toke_moto,AH_toke)

    
honsya_moto = packing.get_honsya_moto()
if honsya_moto.empty:
    honsya_untin = honsya_moto
    AH_honsya = honsya_moto
    PH_honsya = honsya_moto
    #UU_honsya = honsya_moto
else:
    honsya_untin =packing.get_untin_honsya()
    ajust_honsya = Ajust_honsya(myfolder, uriagebi, sengetu)
    AH_honsya = ajust_honsya.get_allHauler(honsya_moto, honsya_untin)
    PH_honsya = ajust_honsya.get_packingHinban(honsya_moto, AH_honsya)
    #UU_honsya = ajust_honsya.get_untinForUriage(honsya_moto,AH_honsya)


recorder = Recorder(myfolder)
recorder.out_log('')
recorder.out_log(PH_toke, '\n')
recorder.out_log(PH_honsya, '\n')

con_df = pd.concat([PH_toke, PH_honsya])

recorder.out_csv(con_df, myfolder)

