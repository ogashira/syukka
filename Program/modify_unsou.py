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
        AH_group = AH.groupby('依頼先')['cans'].sum()

        def get_unsou_cans(unsou):

            try:
                unsou_cans = AH_group.loc[unsou]
            except:
                unsou_cans = 0

            return unsou_cans

        torr_cans = get_unsou_cans('ﾄｰﾙ')
        niigata_cans = get_unsou_cans('新潟')



        def modify_change(row):
            sitei = row['顧客指定運送屋']
            iraisaki = row['依頼先']
            torr = row['ﾄｰﾙ']
            niigata = row['新潟']
            if (niigata_cans >=2 and torr_cans == 1 and iraisaki == 'ﾄｰﾙ' 
                    and niigata != float('inf') and sitei != 'ﾄｰﾙ'): 
                return '新潟'
            if (niigata_cans == 1 and torr_cans >= 2 and iraisaki == '新潟' 
                    and torr != float('inf') and sitei != '新潟'): 
                return 'ﾄｰﾙ'

            return iraisaki

        #ﾄｰﾙが1缶、新潟が2缶以上かつ、顧客指定運送屋にﾄｰﾙが無かったら、
        #ﾄｰﾙを新潟に変更する。その逆は逆をする。
        AH['依頼先'] = AH.apply(modify_change, axis=1)

        #顧客指定運送屋を最優先



        return AH

