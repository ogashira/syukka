#! python
# -*- coding: utf-8 -*-

from toke import *
from honsya import *
from kenpin import *


toke = Toke('./')
honsya = Honsya('./')

untinForUriage_toke = toke.get_untinForUriage()
packingHinban_toke = toke.get_packingHinban()

untinForUriage_honsya = honsya.get_untinForUriage()
packingHinban_honsya = honsya.get_packingHinban()


if not untinForUriage_toke.empty:
    kenpin_toke = Kenpin('toke', packingHinban_toke, untinForUriage_toke)
    kenpin_toke.create_kenpin()

if not untinForUriage_honsya.empty:
    kenpin_honsya = Kenpin('honsya', packingHinban_honsya, untinForUriage_honsya)
    kenpin_honsya.create_kenpin()


