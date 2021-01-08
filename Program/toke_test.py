#! python
# -*- coding: utf-8 -*-

import os
from toke import *

pd.set_option('display.unicode.east_asian_width', True)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', None)

dt_now = datetime.now().strftime('%Y%m%d_%H%M%S')
myfolder = r'./01出荷OutPut/' + dt_now
os.makedirs(myfolder)
toke = Toke(myfolder)

packingHinban = toke.get_packingHinban()
print(packingHinban)

untinForUriage = toke.get_untinForUriage()
print(untinForUriage)


