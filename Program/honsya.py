#! python
# -*- coding: cp932 -*-


from packing import *
from ajust_untin import *
from gyoumu import *

pd.set_option('display.unicode.east_asian_width', True)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', None)

class Honsya:

    def __init__(self, myfolder):


        self.myfolder = myfolder
        packing = Packing()
        
        self.honsya_moto = packing.get_honsya_moto()
        if self.honsya_moto.empty:
            self.honsya_untin = self.honsya_moto
            self.allHauler = self.honsya_moto
            self.packingHinban = self.honsya_moto
            self.untinForUriage = self.honsya_moto
            self.sorting = self.honsya_moto
        else:
            self.honsya_untin = packing.get_untin_honsya()

            ajust_honsya = Ajust_honsya(self.myfolder)

            self.allHauler = ajust_honsya.get_allHauler(self.honsya_moto, 
                                                        self.honsya_untin)
            self.packingHinban = ajust_honsya.get_packingHinban(self.honsya_moto, 
                    self.allHauler)
            self.untinForUriage = ajust_honsya.get_untinForUriage(self.honsya_moto, 
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
            filePath_eigyou = '{}/{}�c��_uriage.xlsx'.format(self.myfolder, '�{��')
            self.untinForUriage.to_excel(filePath_eigyou)
            


            gyoumu = Gyoumu(self.myfolder)

            # sorting������āA�G�N�Z���ŕۑ�
            self.sorting = gyoumu.get_sorting(self.packingHinban, self.myfolder, '�{��')
            filePath_gyoumu = '{}/{}�Ɩ�_packing.xlsx'.format(self.myfolder, '�{��')

            # sorting�̃X�^�C���������čĕۑ�
            gyoumu.get_excel_style(filePath_gyoumu)
            # untinForUriage�̃X�^�C���������čĕۑ�
            gyoumu.get_excel_style(filePath_eigyou)



            del gyoumu
        


            self.packingCoa = ajust_honsya.get_packingCoa(self.packingHinban, 
                    self.untinForUriage)
            
            del ajust_honsya



        del packing


    #���f�[�^(honsya)���擾����
    def get_honsya_moto(self):
        return self.honsya_moto

    #�^���f�[�^(honsya)���擾����
    def get_honsya_untin(self):
        return self.honsya_untin

    #�S�^���\���擾����
    def get_allHauler(self):
        return self.allHauler

    #�d�����\�̌����擾����
    def get_packingHinban(self):
        return self.packingHinban

    # �d�����\���擾����
    def get_sorting(self):
        return self.sorting

    # ������͗p�ް����擾����
    def get_untinForUriage(self):
        return self.untinForUriage


    # ���ѕ\�p�d�����\���擾����
    def get_packingCoa(self):
        return self.packingCoa


