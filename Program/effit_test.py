#! python
# -*- coding: utf-8 -*-

import platform
import sys

from effitA import EffitA
from eigyoubi import Eigyoubi
from toke import *
from honsya import *
from recorder import Recorder
from kenpin import *
from uriage_sumi import *
from remake_packingHinban import *


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
elif pf == 'Linux':
    myfolder = r'/mnt/public/営業課ﾌｫﾙﾀﾞ/01出荷OutPut/' + dt_now
else:
    print('ご使用のマシンではserverに入れません')
    sys.exit()

    
os.makedirs(myfolder)


with open('result.txt', 'w') as result:
    print(dt_now +'\n', file= result)



recorder = Recorder(myfolder)

effita = EffitA(myfolder)
effita.launch_effitA()

toke = Toke(myfolder)
packingHinban_toke = toke.get_packingHinban()
untinForUriage_toke = toke.get_untinForUriage()

honsya = Honsya(myfolder)
packingHinban_honsya = honsya.get_packingHinban()
untinForUriage_honsya = honsya.get_untinForUriage()


del toke
del honsya


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


# 売上入力のﾁｪｯｸ
us = UriageSumi(myfolder)
uriage_sumi = us.get_uriage_sumi()

if not untinForUriage_toke.empty:
    UU_sumi_toke = us.get_UU_sumi(untinForUriage_toke)
    us.check_sumi(UU_sumi_toke)

if not untinForUriage_honsya.empty:
    UU_sumi_honsya = us.get_UU_sumi(untinForUriage_honsya)
    us.check_sumi(UU_sumi_honsya)

del us


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



