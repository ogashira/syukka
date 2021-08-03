#! python
# -*- coding: utf-8 -*-


class ModifyUnsou(object):

    def __init__(self):
        pass

    def get_modified_AH(self, AH):
        """ 
        運送屋の調整を行う
        新潟とﾄｰﾙが１缶の場合は新潟にするなど
        AHはallHaulerの略
        """
        #顧客指定運送屋をﾘｽﾄにしておく
        list_sitei = list(AH['顧客指定運送屋'])

        AH_group = AH.groupby('依頼先')['cans'].sum()

        def get_unsou_cans(unsou):

            try:
                unsou_cans = AH_group.loc[unsou]
            except:
                unsou_cans = 0

            return unsou_cans

        torr_cans = get_unsou_cans('ﾄｰﾙ')
        niigata_cans = get_unsou_cans('新潟')

        #ﾄｰﾙが1缶、新潟が2缶以上かつ、顧客指定運送屋にﾄｰﾙが無かったら、
        #ﾄｰﾙを新潟に変更する。その逆は逆をする。
        if niigata_cans >= 2 and torr_cans == 1 and 'ﾄｰﾙ' not in list_sitei:
            AH['依頼先'] = AH['依頼先'].map(lambda x : '新潟' if x == 'ﾄｰﾙ' else x)
        elif niigata_cans == 1 and torr_cans >= 2 and '新潟' not in list_sitei:
            AH['依頼先'] = AH['依頼先'].map(lambda x : 'ﾄｰﾙ' if x == '新潟' else x)

        return AH

