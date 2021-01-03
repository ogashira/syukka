#! python
# -*- coding: cp932 -*-


from packing import *
from ajust_untin import *
from gyoumu import *

pd.set_option('display.unicode.east_asian_width', True)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', None)

class Toke:

    def __init__(self, myfolder):


        self.myfolder = myfolder
        packing = Packing()
        
        self.toke_moto = packing.get_toke_moto()
        if self.toke_moto.empty:
            self.toke_untin = self.toke_moto
            self.allHauler = self.toke_moto
            self.packingHinban = self.toke_moto
            self.untinForUriage = self.toke_moto
            self.sorting = self.toke_moto
        else:
            self.toke_untin = packing.get_untin_toke()
            
            ajust_toke = Ajust_toke(self.myfolder)
            
            self.allHauler = ajust_toke.get_allHauler(self.toke_moto, 
                    self.toke_untin)
            self.packingHinban = ajust_toke.get_packingHinban(self.toke_moto, 
                    self.allHauler)
            self.untinForUriage = ajust_toke.get_untinForUriage(self.toke_moto,
                    self.allHauler)

            # untinForUriage��packingHinban��'�o�ח\��q��'���������>>>>>>>>>
            # ���̎��_��untinForUriage����o�ח\��q�ɂ��폜���āApackingHinban��
            # �o�ח\��q�ɂ���������̂ŁArobot_log�ŕ\�������o�ח\��q�ɂ�
            # ����ւ��O�̂��̂ƂȂ�B
            merge_data = self.packingHinban[['�󒍂m�n', '�󒍍s�m�n', 
                                                             '�o�ח\��q��']]
            UU = self.untinForUriage.drop(columns = '�o�ח\��q��')
            
            self.untinForUriage = pd.merge(UU, merge_data, on= ['�󒍂m�n', 
                                                    '�󒍍s�m�n'], how = 'left')



            
            #untinForUriage����������ۑ�
            filePath_eigyou = '{}/{}�c��_uriage.xlsx'.format(self.myfolder, '�y�C')
            self.untinForUriage.to_excel(filePath_eigyou)

            

            gyoumu = Gyoumu(self.myfolder)

            # sorting������āA�G�N�Z���ŕۑ�
            self.sorting = gyoumu.get_sorting(self.packingHinban, self.myfolder, '�y�C')
            filePath_gyoumu = '{}/{}�Ɩ�_packing.xlsx'.format(self.myfolder, '�y�C')
            
            # sorting�̃X�^�C���������čĕۑ�
            gyoumu.get_excel_style(filePath_gyoumu)
            # untinForUriage�̃X�^�C���������čĕۑ�
            gyoumu.get_excel_style(filePath_eigyou)



            del gyoumu



            self.packingCoa = ajust_toke.get_packingCoa(self.packingHinban, 
                    self.untinForUriage)
            
            del ajust_toke


        
        del packing




    #���f�[�^(toke)���擾����
    def get_toke_moto(self):
        return self.toke_moto

    #�^���f�[�^(toke)���擾����
    def get_toke_untin(self):
        return self.toke_untin

    #�S�^���\���擾����
    def get_allHauler(self):
        return self.allHauler

    #�d�����\�̌����擾����
    def get_packingHinban(self):
        return self.packingHinban

    # �d�����\���擾����
    def get_sorting(self):
        return self.sorting
    

    #������͗p�ް����擾����
    def get_untinForUriage(self):
        return self.untinForUriage

    # ���ѕ\�p�d�����\���擾����
    def get_packingCoa(self):
        return self.packingCoa



