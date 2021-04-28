#! python
# -*- coding: utf-8 -*-

import pandas as pd

UU_toke = pd.DataFrame(index = [], columns=['a','b','sumi'])
UU_honsya = pd.DataFrame(index = [], columns=['a','b','sumi'])

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#UU_toke.loc[0, 'sumi'] = '済'
#UU_toke.loc[0, 'sumi'] = '済'
#UU_honsya.loc[0, 'sumi'] = '済'
#UU_honsya.loc[1, 'sumi'] = '済'
#UU_honsya.loc[2, 'sumi'] = '-済'





#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

sumi_toke = list(UU_toke.loc[:, 'sumi'])
sumi_honsya = list(UU_honsya.loc[:, 'sumi'])

len_sumi_toke = len(sumi_toke)
sumi_toke_count = sumi_toke.count('済')
len_honsya_toke = len(sumi_honsya)
sumi_honsya_count = sumi_honsya.count('済')

print(r'len(sumi_toke): {}, sumi_toke.count(済) :{}'.format(len_sumi_toke,sumi_toke_count))
print(r'len(sumi_honsya): {}, sumi_honsya.count(済) :{}'.format(len_honsya_toke,sumi_honsya_count))

if not (UU_toke.empty or len(sumi_toke)==  sumi_toke.count('済')):
    print('effitA実行')
else:
    print('pass effitA')
    

