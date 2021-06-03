#! python
# -*- coding: utf-8 -*-


from modify_output import *
from toke import *
from honsya import *
from kenpin import *
from eigyoubi import *
from sql_server import *
from coa import *
from recorder import *

import platform
import pprint


MYFOLDER = r'C:/Users/oga/Documents/syukka/Program'

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

toke = Toke(MYFOLDER, uriagebi, sengetu)
honsya = Honsya(MYFOLDER, uriagebi, sengetu)

UU_toke = toke.get_untinForUriage()
UU_honsya = honsya.get_untinForUriage()

PH_toke = toke.get_packingHinban()

PH_honsya = honsya.get_packingHinban()

#effitAを立ち上げるかどうかの判定>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

sumi_toke = list(UU_toke.loc[:, 'sumi'])
sumi_honsya = list(UU_honsya.loc[:, 'sumi'])

if not  (
        (UU_toke.empty and UU_honsya.empty) 
        or  (
            len(sumi_toke) == sumi_toke.count('済') and
            len(sumi_honsya) == sumi_honsya.count('済')
            )   
        ):
    print('\n\neffitAを立ち上げる\n\n')
else:
    print('\n\neffitAを立ち上げない\n\n')
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

pf = platform.system()
if pf == 'Windows':
    sql = SqlServer(uriagebi, sengetu)
    uriage_sumi = sql.get_uriage_sumi()
else:
    uriage_sumi = pd.read_csv(
            r'../master/effitA/uriage_sumi.csv', 
            skiprows = 1,
            encoding='cp932'
    )

# 売上入力のチェック
if not (UU_toke.empty and UU_honsya.empty) and not uriage_sumi.empty:
    modify = ModifyOutput(MYFOLDER, uriagebi, sengetu)
    modify.uriageSumi_check_sumi(UU_toke, UU_honsya)
    modified_UU = modify.get_modified_UU(UU_toke, UU_honsya)
    modified_PH = modify.get_modified_PH(PH_toke, PH_honsya)

    del modify


    # PH,UUを土気、本社に分ける
    modi_PH_toke = modified_PH.loc[modified_PH['出荷'] == '土気出荷', :]
    modi_PH_honsya = modified_PH.loc[modified_PH['出荷'] == '本社出荷', :]

    modi_UU_toke = modified_UU.loc[modified_UU['出荷'] == '土気出荷', :]
    modi_UU_honsya = modified_UU.loc[modified_UU['出荷'] == '本社出荷', :]
else:
    modi_PH_toke = PH_toke
    modi_PH_honsya = PH_honsya
    modi_UU_toke = UU_toke
    modi_UU_honsya = UU_honsya


gyoumu = Gyoumu(MYFOLDER)

# sortingを作って、エクセルで保存
if len(modi_PH_toke.index) != 0 :
    sorting = gyoumu.get_sorting(modi_PH_toke, MYFOLDER, '土気')
    filePath_gyoumu_toke = '{}/{}業務_packing.xlsx'.format(MYFOLDER, '土気')

if len(modi_PH_honsya) != 0:
    sorting = gyoumu.get_sorting(modi_PH_honsya, MYFOLDER, '本社')
    filePath_gyoumu_honsya = '{}/{}業務_packing.xlsx'.format(MYFOLDER, '本社')

# sortingのスタイル調整して再保存
if len(modi_PH_toke.index) != 0:
    gyoumu.get_excel_style(filePath_gyoumu_toke)
if len(modi_PH_honsya.index) != 0:
    gyoumu.get_excel_style(filePath_gyoumu_honsya)

# kenpin,出荷実績照会作成
if not UU_toke.empty:
    kenpin_toke = Kenpin('toke', modi_PH_toke, modi_UU_toke, MYFOLDER)
    kenpin_toke.create_kenpin()
    kenpin_toke.get_syukka_jisseki_syoukai()
    del kenpin_toke
    
if not UU_honsya.empty:
    kenpin_honsya = Kenpin('honsya', modi_PH_honsya, modi_UU_honsya,
                                                            MYFOLDER)
    kenpin_honsya.create_kenpin()
    kenpin_honsya.get_syukka_jisseki_syoukai()
    del kenpin_honsya

del gyoumu

recorder = Recorder(MYFOLDER)
txt = ('\n**売上入力、業務用fileは作成は終了しました。*** \n\n'
            '検査成績書を探し、無ければ発行します。\n\n')

recorder.out_log(txt)
recorder.out_file(txt)

# ここからCOA作成>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
