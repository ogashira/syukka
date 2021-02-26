#! python
# -*- coding: utf-8 -*-

import platform

from effitA import EffitA
from eigyoubi import Eigyoubi
from toke import *
from honsya import *
from recorder import Recorder
from kenpin import *
from modify_output import *




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


def start():
    recorder = Recorder(myfolder)

    effita = EffitA(myfolder)
    effita.launch_effitA()
    effita.launch_DBmanager2()
    effita.dl_DBmanager2('運賃計算ｼｰﾄ_改', uriagebi)
    recorder.out_log('運賃計算ｼｰﾄ_改をダウンロード、保存しました', '\n')
    effita.dl_DBmanager2('受注DT', sengetu, honjitu)
    recorder.out_log('受注DTをダウンロード、保存しました','\n')
    effita.dl_DBmanager2('uriage_mae', uriagebi)
    recorder.out_log('売上済をダウンロード、保存しました','\n')
    effita.close_DBmanager2()
    effita.dl_zaiko()
    recorder.out_log('現在庫をダウンロード、保存しました','\n')

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


    # sumi列の値をリストにする
    sumi_toke = list(UU_toke.loc[:, 'sumi'])
    sumi_honsya = list(UU_honsya.loc[:, 'sumi'])

    # 売上入力実施 UU_tokeが空ではなく、sumiが全部'済 'でなかったら実行
    if not UU_toke.empty and len(sumi_toke) > sumi_toke.count('済'):
        effita.launch_uriage_nyuuryoku('toke')
        effita.uriage_nyuuryoku(UU_toke)
        effita.close_uriage_nyuuryoku()
    
    if not UU_honsya.empty and len(sumi_honsya) > sumi_honsya.count('済'):
        effita.launch_uriage_nyuuryoku('honsya')
        effita.uriage_nyuuryoku(UU_honsya)
        effita.close_uriage_nyuuryoku()

    
    txt = '売上入力終了しました'
    recorder.out_log(txt, '\n')
    recorder.out_file(txt, '\n')

    # 売上済(uriage_sumi)ダウンロード
    effita.launch_DBmanager2()
    effita.dl_DBmanager2('uriage_sumi', uriagebi)
    recorder.out_log('売上済をダウンロード、保存しました','\n')
    effita.close_DBmanager2()


    # effitAを閉じる
    effita.close_effitA()



    # 売上入力のﾁｪｯｸ
    """
    UU_tokeとUU_honsyaをconcatしてからﾁｪｯｸに渡す。
    出荷倉庫が変更されている可能性もあるため。
    ﾁｪｯｸ後に出荷倉庫をuriage_sumiに合わせてから、再び、
    toke と honsyaに分ける
    PHの方もﾁｪｯｸはしないがconcat->uriage_sumiをmerge->
    uriage_sumiに合わせてから->土気と本社に分ける
    """



    if not (UU_toke.empty and UU_honsya.empty):
        modify = ModifyOutput(myfolder, uriagebi, sengetu)
        modify.uriageSumi_check_sumi(UU_toke, UU_honsya)
        modified_UU = modify.get_modified_UU(UU_toke, UU_honsya)
        modified_PH = modify.get_modified_PH(PH_toke, PH_honsya)

        del modify


    # PH,UUを土気、本社に分ける
    modi_PH_toke = modified_PH.loc[modified_PH['出荷'] == '土気出荷', :]
    modi_PH_honsya = modified_PH.loc[modified_PH['出荷'] == '本社出荷', :]
    
    modi_UU_toke = modified_UU.loc[modified_UU['出荷'] == '土気出荷', :]
    modi_UU_honsya = modified_UU.loc[modified_UU['出荷'] == '本社出荷', :]
    

    # sortingを作って、エクセルで保存
    
    gyoumu = Gyoumu(myfolder)
    if len(modi_PH_toke.index) != 0:
        sorting = gyoumu.get_sorting(modi_PH_toke, myfolder, '土気')
        filePath_gyoumu_toke = '{}/{}業務_packing.xlsx'.format(myfolder, '土気')
    if len(modi_PH_honsya.index) != 0:
        sorting = gyoumu.get_sorting(modi_PH_honsya, myfolder, '本社')
        filePath_gyoumu_honsya = '{}/{}業務_packing.xlsx'.format(myfolder, '本社')

    # sortingのスタイル調整して再保存
    if len(modi_PH_toke.index) != 0:
        gyoumu.get_excel_style(filePath_gyoumu_toke)
    if len(modi_PH_honsya.index) != 0:
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
