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
    effita.dl_DBmanager2('運賃計算ｼｰﾄ_改', yokujitu)
    recorder.out_log('運賃計算ｼｰﾄ_改をダウンロード、保存しました', '\n')
    effita.dl_DBmanager2('受注DT', sengetu, honjitu)
    recorder.out_log('受注DTをダウンロード、保存しました','\n')
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
    modify = ModifyOutput()
    modified_PH = modify.modify_PH(PH_concat_sumi)
    

    # 業務用packing(sorting)を作る
    
    """
    2021/1/15 uriage_sumi から修正したpackingHinbanを作る。
    GyoumuｸﾗｽにpackingHinban,myfolder,factoryを渡して、
    sortingしてから、excelの体裁整える
    """
    remake_PH = RemakePackingHinban(packingHinban_toke, uriage_sumi)

    """
    以下は、toke.pyに記述してあったその部分のcode 
    gyoumu = Gyoumu(self.myfolder)

    sortingを作って、エクセルで保存
    self.sorting = gyoumu.get_sorting(self.packingHinban, self.myfolder, '土気')
    filePath_gyoumu = '{}/{}業務_packing.xlsx'.format(self.myfolder, '土気')
    
    sortingのスタイル調整して再保存
    gyoumu.get_excel_style(filePath_gyoumu)
    untinForUriageのスタイル調整して再保存



    del gyoumu
    """
    





    # kenpin,出荷実績照会作成
    if not untinForUriage_toke.empty:
        kenpin_toke = Kenpin('toke', packingHinban_toke, untinForUriage_toke, myfolder)
        kenpin_toke.create_kenpin()
        kenpin_toke.get_syukka_jisseki_syoukai()
        del kenpin_toke
        
    if not untinForUriage_honsya.empty:
        kenpin_honsya = Kenpin('honsya', packingHinban_honsya, untinForUriage_honsya, myfolder)
        kenpin_honsya.create_kenpin()
        kenpin_honsya.get_syukka_jisseki_syoukai()
        del kenpin_honsya
    
    txt = '\n *********売上入力の記録********** \n'
    recorder.out_log( txt)
    recorder.out_file(txt)


    import line
