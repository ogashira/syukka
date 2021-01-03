#! python
# -*- coding: cp932 -*-


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
myfolder = r'//192.168.1.247/���L/�c�Ɖ�̫���/01�o��OutPut/' + dt_now
os.makedirs(myfolder)


with open('result.txt', 'w') as result:
    print(dt_now +'\n', file= result)


def start():
    recorder = Recorder(myfolder)

    effita = EffitA(myfolder)
    effita.launch_effitA()
    effita.launch_DBmanager2()
    effita.dl_DBmanager2('�^���v�Z���_��', yokujitu)
    recorder.out_log('�^���v�Z���_�����_�E�����[�h�A�ۑ����܂���', '\n')
    effita.dl_DBmanager2('��DT', sengetu, honjitu)
    recorder.out_log('��DT���_�E�����[�h�A�ۑ����܂���','\n')
    effita.close_DBmanager2()
    effita.dl_zaiko()
    recorder.out_log('���݌ɂ��_�E�����[�h�A�ۑ����܂���','\n')

    toke = Toke(myfolder)
    packingHinban_toke = toke.get_packingHinban()
    untinForUriage_toke = toke.get_untinForUriage()

    honsya = Honsya(myfolder)
    packingHinban_honsya = honsya.get_packingHinban()
    untinForUriage_honsya = honsya.get_untinForUriage()

    import line


    del toke
    del honsya


    # kenpin,�o�׎��яƉ�쐬
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
    
    txt = '\n *********������͂̋L�^********** \n'
    recorder.out_log( txt)
    recorder.out_file(txt)


    
    # ������͎��{
    if not untinForUriage_toke.empty:
        effita.launch_uriage_nyuuryoku('toke')
        effita.uriage_nyuuryoku(untinForUriage_toke)
        effita.close_uriage_nyuuryoku()
    
    if not untinForUriage_honsya.empty:
        effita.launch_uriage_nyuuryoku('honsya')
        effita.uriage_nyuuryoku(untinForUriage_honsya)
        effita.close_uriage_nyuuryoku()

        
    effita.close_effitA()    
    
    txt = '������͏I�����܂���'
    recorder.out_log(txt, '\n')
    recorder.out_file(txt, '\n')
    



