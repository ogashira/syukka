#! python
# -*- coding: utf-8 -*-


from modify_output import *
from toke import *
from honsya import *
from kenpin import *




toke = Toke('./')
honsya = Honsya('./')

UU_toke = toke.get_untinForUriage()
UU_honsya = honsya.get_untinForUriage()

PH_toke = toke.get_packingHinban()

PH_honsya = honsya.get_packingHinban()






# 売上入力のチェック
if not (UU_toke.empty and UU_honsya.empty):
    modify = ModifyOutput('./')
    modify.uriageSumi_check_sumi(UU_toke, UU_honsya)
    modified_UU = modify.get_modified_UU(UU_toke, UU_honsya)
    modified_PH = modify.get_modified_PH(PH_toke, PH_honsya)

    del modify



# PH,UUを土気、本社に分ける
modi_PH_toke = modified_PH.loc[modified_PH['出荷'] == '土気出荷', :]
modi_PH_honsya = modified_PH.loc[modified_PH['出荷'] == '本社出荷', :]

modi_UU_toke = modified_UU.loc[modified_UU['出荷'] == '土気出荷', :]
modi_UU_honsya = modified_UU.loc[modified_UU['出荷'] == '本社出荷', :]


gyoumu = Gyoumu('./')

# sortingを作って、エクセルで保存
if len(modi_PH_toke.index) != 0 :
    sorting = gyoumu.get_sorting(modi_PH_toke, './', '土気')
    filePath_gyoumu_toke = '{}/{}業務_packing.xlsx'.format('./', '土気')

if len(modi_PH_honsya) != 0:
    sorting = gyoumu.get_sorting(modi_PH_honsya, './', '本社')
    filePath_gyoumu_honsya = '{}/{}業務_packing.xlsx'.format('./', '本社')

# sortingのスタイル調整して再保存
if len(modi_PH_toke.index) != 0:
    gyoumu.get_excel_style(filePath_gyoumu_toke)
if len(modi_PH_honsya.index) != 0:
    gyoumu.get_excel_style(filePath_gyoumu_honsya)

# kenpin,出荷実績照会作成
if not UU_toke.empty:
    kenpin_toke = Kenpin('toke', modi_PH_toke, modi_UU_toke, './')
    kenpin_toke.create_kenpin()
    kenpin_toke.get_syukka_jisseki_syoukai()
    del kenpin_toke
    
if not UU_honsya.empty:
    kenpin_honsya = Kenpin('honsya', modi_PH_honsya, modi_UU_honsya,
                                                            './')
    kenpin_honsya.create_kenpin()
    kenpin_honsya.get_syukka_jisseki_syoukai()
    del kenpin_honsya

del gyoumu

