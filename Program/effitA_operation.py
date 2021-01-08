#! python
# -*- coding: utf-8 -*-

import platform

from effitA import EffitA
from eigyoubi import Eigyoubi
from toke import *
from honsya import *
from recorder import Recorder
from kenpin import *



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
    packingHinban_toke = toke.get_packingHinban()
    untinForUriage_toke = toke.get_untinForUriage()

    honsya = Honsya(myfolder)
    packingHinban_honsya = honsya.get_packingHinban()
    untinForUriage_honsya = honsya.get_untinForUriage()

    import line


    del toke
    del honsya


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


    
    # 売上入力実施
    if not untinForUriage_toke.empty:
        effita.launch_uriage_nyuuryoku('toke')
        effita.uriage_nyuuryoku(untinForUriage_toke)
        effita.close_uriage_nyuuryoku()
    
    if not untinForUriage_honsya.empty:
        effita.launch_uriage_nyuuryoku('honsya')
        effita.uriage_nyuuryoku(untinForUriage_honsya)
        effita.close_uriage_nyuuryoku()

        
    effita.close_effitA()    
    
    txt = '売上入力終了しました'
    recorder.out_log(txt, '\n')
    recorder.out_file(txt, '\n')
    



