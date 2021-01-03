#! python
# -*- coding: cp932 -*-

import jaconv, csv, openpyxl
from datetime import datetime, date, timedelta
from recorder import *

'''
���㏈���̂��߂̍݌ɂ̈������āiLOT�j���s��
�A�o���i�̏ꍇ�́A�A�o�h���A���\��lot���������Ă�B
�������A�A�o�h���A���\�ɂ͕i�ԁA�i���������̂ŁA���݌��ް��ɂ���
�i�Ԃ�lot�𒲂ׂāA�ǂꂪ�A�o�h���A���\�̃I�[�_�[No��LOT�Ȃ̂��𒲂ׂĈ������Ă�B
�����󒍐��i�́A��v����ʐ���LOT����������Ă�B�����ɓ����̊ʐ�����v�����ꍇ
�́A���������󒍓�������Ȃ�΂ǂ���ł��悢�B
�����ݕi�̏ꍇ�́A�Â�LOT����������Ă�B
'''




class Zaiko:

    def __init__ (self, myfolder):

        self.myfolder = myfolder


     
    #�A�o�h���A���\�̎擾
        wb = openpyxl.load_workbook(
            r'//192.168.1.247/Guest/�A�o�h���A���\.xlsx', data_only=True
        )
        # wb = openpyxl.load_workbook(
           # r'../master/�A�o�h���A���\.xlsx', data_only=True
        # )
        ws = wb['�A�o�h���A���\']
        
        # �V�[�g��ی삵���Ƃ��̃p�X���[�h���Z�b�g
        ws.protection.password = 'gijutu'
        
        # �V�[�g�̕ی������
        ws.protection.disable()

        #�񎟌�ؽĂɂ���
        yusyutuRenraku = []
        for row in ws.rows:
            rows = []
            for cell in row:
                rows.append(cell.value)
            yusyutuRenraku.append(rows)
        
        #orderNo_lot = {'VNN3044:{20090501H : 3, 20091852T: 5,...},.....} �̌`�ɂ���
        orderNo_lot = {}
        lot_cans = {}
        for line in yusyutuRenraku:
            if line[3]== None :
                continue
            else:
                #��������啶���ɂ���
                orderNo = str(line[3]).upper() 
                #�S�p�𔼊p�ɂ���(�������L����)
                orderNo = jaconv.z2h(orderNo,digit=True,ascii=True) 
                #�󔒂�����
                orderNo = orderNo.replace(' ','') 
                orderNo = orderNo.replace('�@','')
                lot = str(line[5]).upper()
                lot = jaconv.z2h(lot,digit=True,ascii=True)
                

                if orderNo in orderNo_lot:
                    lot_cans = orderNo_lot[orderNo]
                    lot_cans[lot] = line[7]
                    orderNo_lot[orderNo] = lot_cans
                else:
                    orderNo_lot[orderNo] = {lot:line[7]}


        self.yusyutuRenrakuLot = orderNo_lot
        '''
        {VNN3044:{20090501H: 3, 20091852T: 5....}, VNN3055:{..},....}
        '''


    # ���݌��ް��̎擾 
        zaiko = pd.read_csv(r'../master/effitA/zaiko.csv',encoding='cp932')
        zaiko = zaiko.loc[(zaiko['�q��']=='���q��')|(zaiko['�q��']=='�{�Бq��')
                          |(zaiko['�q��']=='�y�C�q��'), ['�i��','���b�gNo',
                          '�݌ɐ��ʁi���݁j','�q��']]
        zaiko = zaiko.fillna("")
        
        genzaiko_d = zaiko.to_dict(orient='split') #dataframe �������ɂ���
        genzaiko_l = genzaiko_d['data'] # ��������key=data(�񎟌�ؽĕ����j�����o��
        genzaiko_l = sorted(genzaiko_l, key=lambda x: x[1]) #LOT�Ń\�[�g
        self.genzaiko_l = sorted(genzaiko_l, key=lambda x: x[0]) #�X�ɁA�i�ԂŃ\�[�g

        '''
        [['S10-E-C', '20052603H', '3', '�{�Бq��'],
        ['S10-E-C', '20071405H', '15', '�{�Бq��'],
        ['S10-P3', '20071331H', '4', '���q��'],
        ['S11-PT04S-T', '20091451T', '60', '�y�C�q��'],
        ['S11-PT04S-T-R-EX', '20091454T', '8', '�y�C�q��'],......]
        '''

    # �󒍌����ݐ��i�ް��̎擾
        JM_file = open('../master/selfMade/�󒍌�����ؽ�.csv',encoding='cp932')
        file_reader = csv.reader(JM_file)
        JM = list(file_reader)
        JM_file.close()

        self.JM_data = {}
        for line in JM:
            hinban = line[0]
            JorM = line[1]
            self.JM_data[hinban] = JorM


    # ��DT.csv �̎擾
        JDT = pd.read_csv(r'../master/effitA/��DT.csv', skiprows = 1
                          , encoding = 'cp932')
        JDT = JDT.drop_duplicates(['�󒍂m�n'])
        JDT = JDT.loc[:,['�󒍂m�n','�󒍓�']]
        self.JDT_d = dict(zip(JDT['�󒍂m�n'], JDT['�󒍓�']))
    
 

# �� method



    def get_lot(self,df_row):
        '''lot�̈������Ă��s���B
        �A�o���悪y�Ȃ��defpattern_y�ŏ���,����ȊO�͂��ꂼ��������
        '''

        recorder = Recorder(self.myfolder)
        
        #pattern�����肷��֐�
        def get_pattern(hinban):
            if self.JM_data.get(hinban, '-') =='�󒍐��i':
                return 'J'
            elif self.JM_data.get(hinban, '-') == '�����ݐ��i':
                return 'M'
            else:
                return '-'

        #�݌ɂ������֐�
        def zaiko_minus(k, cans):
            for line in self.genzaiko_l:
                if line[1] == k:
                    line[2] = float(line[2]) - cans


        def pattern_y(hinban,cans,orderNo, syukka_souko, lot) :
            '''
            �A�o�h���A���\�̕i�ԁAlot�����݌ɂɂȂ�������A���b�Z�[�W���o�����A
            {}�̂܂�program�͐i�s����B
            ���݌ɂ��^���v�Z�V�[�g�̏o�׊ʐ���������Ȃ�������A���b�Z�[�W��
            �o���A{'short':0}��program�͐i�s����B
            �A�o�h���A���\�̏o�׊ʐ��͖�������i���Ă��Ȃ��j
            �o�בq�ɂƍ݌ɑq�ɂ��s��v�̏ꍇ�A{'short':0}�����Ĕ��㗧�ĂȂ�
            '''
            yusyutu = self.yusyutuRenrakuLot.get(orderNo, {})
            # {20090501H : 3, 20091852T : 5....}
            for line in self.genzaiko_l:
                if line[0] == hinban:
                    zaiko_lot = line[1]
                    zaiko_cans = float(line[2])
                    zaiko_souko = line[3]
                    yusyutu_cans = float(yusyutu.get(zaiko_lot, 0))

                    if zaiko_lot in yusyutu:
                        if zaiko_souko[:2] == syukka_souko[:2]:
                            if zaiko_cans >= yusyutu_cans:
                                lot[zaiko_lot] =  yusyutu_cans
                                zaiko_minus(zaiko_lot, yusyutu_cans)
                            else:
                                txt = '�A�o���i{}��{}�̍݌ɂ�����܂���'\
                                                      .format(hinban,zaiko_lot)
                                recorder.out_log(txt)
                                recorder.out_file(txt)
                                lot = {'short':0}
                                break                 
                            
            if lot == {}:
                txt = '�A�o���i{}���A�o�h���A���\�ɂȂ����A�o�ח\��q�ɂƈႤ�q�ɂɂ���܂�'.format(hinban)
                recorder.out_log(txt)
                recorder.out_file(txt,'\n')
                 

            if 'short' not in lot and lot != {}:
                total = 0
                for v in lot.values():
                    total += int(v)
                if total != int(cans):#���̏o�׊ʐ���total���r���Ă���
                    recorder.out_log('�E�A�o���i(' + hinban + ')�̍݌ɂ������܂���B')
                    recorder.out_file('�E�A�o���i(' + hinban + ')�̍݌ɂ������܂���B')
                    lot['short'] = 0



                        
            
            return lot



        def pattern_J(hinban,cans,JNo, syukka_souko, lot):
            #�r���̍݌Ɉ������ĂŁAcans�͕ω�����̂ŏo�׊ʐ���syukka_cans�Ƃ��Ď���Ă���
            syukka_cans = cans
            dt_now = datetime.now()
            mytoday = dt_now.strftime('%Y%m%d')
            J_date = str(self.JDT_d.get(JNo, mytoday))
            J_date = J_date[:4] + '/' + J_date[4:6] + '/' + J_date[6:]
            J_date = datetime.strptime(J_date, '%Y/%m/%d')
            J_zaiko = {}

            #if�Ɉ���������Ȃ���187�s�̂Ƃ���Œ�`����Ă��Ȃ��ăG���[�ɂȂ邩��B
            zaiko_souko = ''
            zaiko_lot = ''
            for line in self.genzaiko_l:   
                if line[0] == hinban:
                    zaiko_hinban = line[0]
                    zaiko_lot = line[1]
                    zaiko_cans = line[2]
                    zaiko_souko = line[3]
                    zaiko_date = '20' + zaiko_lot[:2] + '/' + zaiko_lot[2:4] \
                        + '/' + zaiko_lot[4:6]
                    zaiko_date = datetime.strptime(zaiko_date, '%Y/%m/%d')
                    if zaiko_date - J_date >= timedelta(0) \
                            and zaiko_souko[:2] == syukka_souko[:2]:
                        J_zaiko[zaiko_lot] = zaiko_cans
                        
            #�������k�n�s�Ń\�[�g����ƃ��X�g�ɂȂ�̂ŁA�܂������ɂ���B
            J_zaiko = sorted(J_zaiko.items())
            J_zaiko = dict(J_zaiko)
            
            #�ʐ����݌ɂƏo�׊ʐ��Ƃ҂������v����LOT���������Ă�
            for k, v in J_zaiko.items():
                if float(v) == cans:
                    lot[k] = cans
                    zaiko_minus(k, cans)
                    break
            else:
                for k, v in J_zaiko.items(): #�݌ɂ��o�׊ʐ��ȏ��LOT���������Ă�
                    if float(v) >= cans:
                        lot[k] = cans
                        zaiko_minus(k, cans)
                        break

            # if zaiko_souko[:2] != syukka_souko[:2]:
            #     lot['short'] = 0 
            #     recorder.out_log('�E�o�ׂ���q�ɂƍ݌ɂ�����q�ɂ���v���Ă܂���(' \
            #                      + hinban + ':' + zaiko_lot + ')')
            #     recorder.out_file('�E�o�ׂ���q�ɂƍ݌ɂ�����q�ɂ���v���Ă܂���(' \
            #                       + hinban + ':' + zaiko_lot + ')')
            
            if lot == {}:
                recorder.out_log('�E�󒍐��i(' + hinban + ')��LOT���������Ăł�' \
                                 '�܂���B')
                recorder.out_file('�E�󒍐��i(' + hinban + ')��LOT���������Ă�' \
                                  '���܂���B')
            else:
                total = 0
                for v in lot.values():
                    total += int(v)
                if total < int(syukka_cans):#���̏o�׊ʐ���total���r���Ă���
                    recorder.out_log('�E�󒍐��i(' + hinban + ')�̍݌ɂ�����܂���B')
                    recorder.out_file('�E�󒍐��i(' + hinban + ')�̍݌ɂ�����܂���B')
                    lot['short'] = 0

            return lot



        def pattern_M(hinban,cans, syukka_souko, lot):
            M_zaiko = []
            #�r���̍݌Ɉ������ĂŁAcans�͕ω�����̂ŏo�׊ʐ���syukka_cans�Ƃ��Ď���Ă���
            syukka_cans = cans
            if syukka_souko == '��㒼��':
                for line in self.genzaiko_l:   
                    if line[0] == hinban and line[3] == '�ړ��q��' and float(line[2]) > 0 :
                        add_l = []
                        add_l.append(line[1])
                        add_l.append(line[2])
                        add_l.append(line[3])
                        M_zaiko.append(add_l)
            elif syukka_souko == '�y�C�o��':
                for line in self.genzaiko_l:   
                    if line[0] == hinban and line[3] == '�y�C�q��' and float(line[2]) > 0  :
                        add_l = []
                        add_l.append(line[1])
                        add_l.append(line[2])
                        add_l.append(line[3])
                        M_zaiko.append(add_l)
            elif syukka_souko == '�{�Џo��':
                for line in self.genzaiko_l:   
                    if line[0] == hinban and line[3] == '�{�Бq��' and float(line[2]) > 0  :
                        add_l = []
                        add_l.append(line[1])
                        add_l.append(line[2])
                        add_l.append(line[3])
                        M_zaiko.append(add_l)
                        
            #�Q����ؽĂ�LOT�Ń\�[�g����B
            M_zaiko = sorted(M_zaiko)
            
            #LOT�̈������āAcans�͂O�ɂȂ�܂Ō����Ă���
            for i in range(len(M_zaiko)):
                if float(cans) > float(M_zaiko[i][1]):
                    tmp = float(M_zaiko[i][1])
                    M_zaiko[i][1] = 0
                    cans = float(cans) - tmp
                    lot[M_zaiko[i][0]] = tmp
                    zaiko_minus(M_zaiko[i][0], tmp)
                else:
                    M_zaiko[i][1] = float(M_zaiko[i][1]) - float(cans)
                    lot[M_zaiko[i][0]] = float(cans)
                    zaiko_minus(M_zaiko[i][0], float(cans))
                    #cans = 0        
                    break
        
            if lot == {}:
                recorder.out_log('�E�����ݐ��i(' + hinban + ')��LOT���������Ăł��܂���B')
                recorder.out_file('�E�����ݐ��i(' + hinban + ')��LOT���������Ăł��܂���B')
            else:
                total = 0
                for v in lot.values():
                    total += int(v)
                if total < int(syukka_cans):#���̏o�׊ʐ���total���r���Ă���
                    recorder.out_log('�E�����ݐ��i(' + hinban + ')�̍݌ɂ�����܂���B')
                    recorder.out_file('�E�����ݐ��i(' + hinban + ')�̍݌ɂ�����܂���B')
                    lot['short'] =0


            return lot


        #�� �����܂�method���̊֐�



        hinban = df_row['hinban']
        cans = df_row['cans']
        yusyutu = df_row['�A�o����']
        orderNo = df_row['���Ӑ撍���m�n']
        JNo = df_row['�󒍂m�n']
        syukka_souko = df_row['�o��']
        lot = {}
        if yusyutu == 'y':
            lot = pattern_y(hinban, cans, orderNo, syukka_souko, lot)
        else:
            pattern = '-'
            pattern = get_pattern(hinban)
            if pattern == 'J':
                lot = pattern_J(hinban,cans,JNo, syukka_souko, lot)
                # JNo�͎󒍓������߂邽�߂ɕK�v�B�󒍐��i�̐������͎󒍓������オ�K�{�Ȃ��߁B
            elif pattern == 'M':
                lot = pattern_M(hinban,cans, syukka_souko, lot)
            else:
                recorder.out_log('�E�󒍌�����ؽ�.csv�ɐ��i���ް�������܂���(' + hinban + ')')
                recorder.out_file('�E�󒍌�����ؽ�.csv�ɐ��i���ް�������܂���(' + hinban + ')' )
                
        return lot






