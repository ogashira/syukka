#! python
# -*- coding: utf-8 -*-

import platform

from effitA import EffitA
from eigyoubi import Eigyoubi
from toke import *
from honsya import *
from recorder import Recorder
from kenpin import *
from uriage_sumi import *
from modify_output import *
from kenpin import *




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
yokujitu = eigyoubi.get_yokujitu()
honjitu = eigyoubi.get_honjitu()
sengetu = eigyoubi.get_sengetu()
del eigyoubi


dt_now = datetime.now().strftime('%Y%m%d_%H%M%S')

pf = platform.system()
if pf == 'Windows':
    myfolder = r'//192.168.1.247/共有/営業課ﾌｫﾙﾀﾞ/01出荷OutPut/' + dt_now
else:
    myfolder = r'/mnt/public/営業課ﾌｫﾙﾀﾞ/01出荷OutPut/' + dt_now
os.makedirs(myfolder)


with open('result.txt', 'w') as result:
    print(dt_now +'\n', file= result)


recorder = Recorder(myfolder)

effita = EffitA(myfolder)
effita.launch_effitA()

toke = Toke(myfolder)
PH_toke = toke.get_packingHinban()
UU_toke = toke.get_untinForUriage()

honsya = Honsya(myfolder)
PH_honsya = honsya.get_packingHinban()
UU_honsya = honsya.get_untinForUriage()



del toke
del honsya


txt = '\n *********売上入力の記録********** \n'
recorder.out_log( txt)
recorder.out_file(txt)


# 売上入力実施
if not UU_toke.empty:
    effita.launch_uriage_nyuuryoku('toke')
    effita.uriage_nyuuryoku(UU_toke)
    effita.close_uriage_nyuuryoku()

if not UU_honsya.empty:
    effita.launch_uriage_nyuuryoku('honsya')
    effita.uriage_nyuuryoku(UU_honsya)
    effita.close_uriage_nyuuryoku()

    
effita.close_effitA()    

txt = '売上入力終了しました'
recorder.out_log(txt, '\n')
recorder.out_file(txt, '\n')


# 売上入力のﾁｪｯｸ
"""
UU_tokeとUU_honsyaをconcatしてからﾁｪｯｸに渡す。
出荷倉庫が変更されている可能性もあるため。
ﾁｪｯｸ後に出荷倉庫をuriage_sumiに合わせてから、再び、
toke と honsyaに分ける
PHの方もﾁｪｯｸはしないがconcat->uriage_sumiをmerge->
uriage_sumiに合わせてから->土気と本社に分ける
"""
us = UriageSumi(myfolder)
uriage_sumi = us.get_uriage_sumi()

UU_concat = pd.concat([UU_toke, UU_honsya])
PH_concat = pd.concat([PH_toke, PH_honsya])



if not UU_concat.empty:
    UU_concat_sumi= us.get_output_sumi(UU_concat, uriage_sumi)
    # UU_concatを渡して売上入力のﾁｪｯｸを行う。
    us.check_sumi(UU_concat_sumi)

if not PH_concat.empty:
    PH_concat_sumi = us.get_output_sumi(PH_concat, uriage_sumi)

del us


# PHを修正する。uriage_sumiに合わせる。 
modify = ModifyOutput(myfolder, uriagebi, sengetu)
modified_PH = modify.get_modified_PH(PH_concat_sumi)
# UUを修正する。uriage_sumiに合わせる。
modified_UU = modify.get_modified_UU(UU_concat_sumi)
del modify
del PH_concat_sumi
del UU_concat_sumi


# PH,UUを土気、本社に分ける
modi_PH_toke = modified_PH.loc[modified_PH['出荷'] == '土気出荷', :]
modi_PH_honsya = modified_PH.loc[modified_PH['出荷'] == '本社出荷', :]

modi_UU_toke = modified_UU.loc[modified_UU['出荷'] == '土気出荷', :]
modi_UU_honsya = modified_UU.loc[modified_UU['出荷'] == '本社出荷', :]



# sortingを作って、エクセルで保存

gyoumu = Gyoumu(myfolder)
sorting = gyoumu.get_sorting(modi_PH_toke, myfolder, '土気')
sorting = gyoumu.get_sorting(modi_PH_honsya, myfolder, '本社')
filePath_gyoumu_toke = '{}/{}業務_packing.xlsx'.format(myfolder, '土気')
filePath_gyoumu_honsya = '{}/{}業務_packing.xlsx'.format(myfolder, '本社')

# sortingのスタイル調整して再保存
gyoumu.get_excel_style(filePath_gyoumu_toke)
gyoumu.get_excel_style(filePath_gyoumu_honsya)

del gyoumu



# kenpin,出荷実績照会作成
if not UU_toke.empty:
    kenpin_toke = Kenpin('toke', modi_PH_toke, modi_UU_toke, myfolder)
    kenpin_toke.create_kenpin()
    kenpin_toke.get_syukka_jisseki_syoukai()
    del kenpin_toke
    
if not UU_honsya.empty:
    kenpin_honsya = Kenpin('honsya', modi_PH_honsya, modi_UU_honsya,
                                                            myfolder)
    kenpin_honsya.create_kenpin()
    kenpin_honsya.get_syukka_jisseki_syoukai()
    del kenpin_honsya



import line
