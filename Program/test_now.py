#! python
# -*- coding: utf-8 -*-


from uriage_sumi import *
from modify_output import *
from toke import *
from honsya import *



toke = Toke('./')
honsya = Honsya('./')

UU_toke = toke.get_untinForUriage()
UU_honsya = honsya.get_untinForUriage()

PH_toke = toke.get_packingHinban()

PH_honsya = honsya.get_packingHinban()


us = UriageSumi('./')

uriage_sumi = us.get_uriage_sumi()

UU_concat = pd.concat([UU_toke, UU_honsya])

PH_concat = pd.concat([PH_toke, PH_honsya])

PH_concat_sumi = us.get_output_sumi(PH_concat, uriage_sumi)

UU_concat_sumi = us.get_output_sumi(UU_concat, uriage_sumi)


modify = ModifyOutput()

modified_PH = modify.modify_PH(PH_concat_sumi)

print(modified_PH)
