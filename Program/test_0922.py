from untin_toke import *
from untin_honsya import *

untin_toke = Untin_toke()
untin_honsya = Untin_honsya()
torr_fare = untin_honsya.get_torr(500,630,"", 2)
niigata_fare = untin_honsya.get_niigata(500,630,"",1)
keihin_fare = untin_honsya.get_keihin("愛知", 1500)

print(torr_fare)
print(niigata_fare)
print(keihin_fare)

