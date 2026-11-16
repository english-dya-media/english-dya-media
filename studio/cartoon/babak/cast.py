from chars import spec
BABAK = spec(kind="man", hair="long_curly", beard="full", head="helmet", garment="tunic", col="#4a3017", col2="#2d1c0c", pattern="brocade",
             cloak="#a51d1d", strap=True)
BABAK_CAPTIVE = spec(kind="man", hair="long_curly", beard="grey", head="none", garment="robe", col="#c79a3c", col2="#8a6420", pattern="brocade",
                     cloak=None, grey=0.6, belt="#5a3a18", trim="#f0d080")
BABAK_YOUNG = spec(kind="man", hair="long_curly", beard="light", head="none", garment="tunic", col="#5a4632", col2="#3a2a1c", pattern="plain",
                   cloak=None, belt="#2b190c", cuff="#7a6040", trim="#8a6a40")
BABAK_LEADER = spec(kind="man", hair="long_curly", beard="full", head="none", garment="robe", col="#9e1c1c", col2="#6a1010", pattern="brocade",
                    cloak=None, belt="#2b190c", trim="#e0b25a")
BABAK_TEEN = spec(kind="boy", hair="teen_curly", beard=None, head="none", garment="tunic", col="#6a5236", col2="#4a3a26", pattern="plain",
                  hs=1.0, bs=0.86, belt="#3a2414", buckle=False, cuff="#8a7050", trim="#8a7050")
BABAK_BOY = spec(kind="boy", hair="boy_curly", beard=None, head="none", garment="child", col="#7a6a4a", col2="#5a4a32", pattern="plain",
                 hs=1.08, bs=0.62, belt="#4a3420", buckle=False, cuff="#9a8a6a", trim="#9a8a6a", trousers="#4a3a2a")
MAHRU = spec(kind="woman", skin="tan", hair="none", beard=None, head="scarf", scarf_col="#2f3f6e", scarf_edge="#c9a24a", garment="dress",
             col="#5a2f3a", col2="#3a1c24", pattern="plain", hs=0.95, bs=0.95, belt=None, cuff="#c9a24a", trim="#c9a24a")
BANU = spec(kind="woman", skin="light", hair="none", beard=None, head="scarf", scarf_col="#8e1820", scarf_edge="#e0b25a", diadem=True,
            garment="dress", col="#7a1a22", col2="#4a0e14", pattern="brocade", hs=0.95, bs=0.95, belt=None, cuff="#e0b25a", trim="#e0b25a")
JAVIDAN = spec(kind="man", skin="light", hair="short", hair_col="#2b1a12", beard="javidan", beard_col="#2b1a12", head="fur_hat", head_col="#8a7560",
               garment="coat", col="#3e4a3a", col2="#283226", pattern="plain", fur="#9a8268", build=1.18, grey=0.5, belt="#2b190c", cuff="#9a8268", trim="#9a8268")
OLD_CHIEF = spec(kind="old", skin="old", hair="short", hair_col="#d8d2c8", beard="white", head="turban", head_col="#e8e0cc", garment="robe",
                 col="#6a2a1e", col2="#4a1a12", pattern="plain", belt="#3a2414", cuff="#c9a24a", trim="#c9a24a", turban_tail=True)
STABLE_HAND = spec(kind="old", skin="olive", hair="short", hair_col="#bdb6ad", beard="white", head="cap", head_col="#6a5a44", garment="robe",
                   col="#5a5040", col2="#3a3428", pattern="plain", belt="#3a2414", buckle=False, cuff="#7a6a50", trim="#7a6a50")
FATHER = spec(kind="man", skin="olive", hair="short", beard="father", head="turban", head_col="#f0ead8", garment="robe", col="#3a5a6a",
              col2="#24404c", pattern="plain", belt=None, sash="#c9a24a", cuff="#c9a24a", trim="#c9a24a")
SAM_BOY = spec(kind="boy", skin="olive", hair="short", beard=None, head="cap", head_col="#c23a2a", garment="child", col="#d8c8a0", col2="#b0a07a",
               pattern="plain", hs=1.08, bs=0.62, belt="#6a4a2a", buckle=False, cuff="#b0a07a", trim="#b0a07a", trousers="#5a4a3a")
SERVANT = spec(kind="man", skin="olive", hair="short", beard="short", beard_col="#2a1a10", head="cap", head_col="#5a4a3a", garment="robe",
               col="#5a4a3a", col2="#3a3026", pattern="plain", belt="#2b190c", buckle=False, cuff="#7a6a50", trim="#7a6a50")
JAVIDAN_ILL = spec(kind="man", skin="light", hair="short", hair_col="#3a2a20", beard="javidan", beard_col="#2b1a12", head="none", garment="tunic",
                   col="#d8d0c0", col2="#b0a890", pattern="plain", build=1.1, grey=0.6, belt=None, cuff="#c8c0b0", trim="#c8c0b0")
SOLDIER = spec(kind="man", skin="olive", hair="short", beard="short", beard_col="#1a120c", head="cap", head_col="#5a5a60", garment="tunic",
               col="#4a4a52", col2="#2a2a30", pattern="plain", belt="#2b190c", buckle=False, cuff="#6a6a70", trim="#6a6a70")

# ---- part 3 (episode 2): 816-829. Red = Babak's people, black = the caliph's men.
STEEL = ("#2a2c34", "#5c606c", "#a8aebb")
BABAK_816 = dict(BABAK_LEADER, cloak="#a51d1d")
YOUNG_SOLDIER = spec(kind="man", skin="olive", hair="short", beard="light", beard_col="#1a120c", head="turban", head_col="#16161b",
                     garment="tunic", col="#2a2a31", col2="#16161a", pattern="plain", belt="#2b190c", buckle=False, cuff="#40404a", trim="#40404a")
OFFICER = spec(kind="man", skin="tan", hair="short", beard="short", beard_col="#2a2420", grey=0.4, head="helmet", helm=STEEL, plume="#141418",
               garment="coat", col="#24242c", col2="#111116", pattern="scales", scale_col="#7a7e8a", belt="#2b190c", cuff="#3a3a44", trim="#8a8e9a")
TAX_COLLECTOR = spec(kind="man", skin="light", hair="short", beard="father", beard_col="#1a1410", head="turban", head_col="#121216",
                     garment="robe", col="#1e1e25", col2="#0e0e12", pattern="plain", build=1.22, belt=None, sash="#c9a24a", cuff="#c9a24a", trim="#c9a24a")
GUARD = spec(kind="man", skin="olive", hair="short", beard="full", beard_col="#14100c", head="turban", head_col="#141418",
             garment="tunic", col="#2c2c33", col2="#16161a", pattern="plain", belt="#2b190c", buckle=False, cuff="#3a3a42", trim="#3a3a42")
FARMER = spec(kind="old", skin="old", hair="short", hair_col="#bdb6ad", beard="grey", beard_col="#6a6058", grey=0.7, head="cap", head_col="#7a6a50",
              garment="robe", col="#6a5a40", col2="#4a3e2c", pattern="plain", belt="#3a2414", buckle=False, cuff="#8a7a5a", trim="#8a7a5a")
COMMANDER = spec(kind="man", skin="tan", hair="short", beard="full", beard_col="#20140c", head="cap", head_col="#5a1a14",
                 garment="tunic", col="#8a221a", col2="#5a1410", pattern="plain", belt="#2b190c", cuff="#c9a24a", trim="#c9a24a", strap=True)
AHMAD = spec(kind="man", skin="light", hair="short", beard="full", beard_col="#1a1410", head="helmet", helm=STEEL, plume="#141418",
             garment="coat", col="#3a3c46", col2="#22242c", pattern="scales", scale_col="#d8b25a", belt="#2b190c", cuff="#c9a24a", trim="#e0b25a", build=1.08)
MUHAMMAD = spec(kind="man", skin="tan", hair="short", beard="full", beard_col="#120c08", grey=0.25, head="helmet", helm=STEEL, plume="#0c0c10",
                garment="coat", col="#1e1e24", col2="#0e0e12", pattern="scales", scale_col="#8a8e9a", belt="#2b190c", cuff="#5a5e6a", trim="#a8aebb",
                cloak="#1a1a20", cloak2="#0a0a0e", cloak_hi="#4a4a58", build=1.12)
FIGHTER = spec(kind="man", skin="olive", hair="short", beard="short", beard_col="#1a120c", head="cap", head_col="#6a1a14",
               garment="tunic", col="#9a2a1e", col2="#6a1a12", pattern="plain", belt="#2b190c", buckle=False, cuff="#7a3a2a", trim="#7a3a2a")
FIGHTER2 = dict(FIGHTER, beard="full", skin="tan", head="scarf", scarf_col="#7a1414", scarf_edge="#c9a24a", kind="man", hair="none")
VILLAGE_W = spec(kind="woman", skin="tan", hair="none", beard=None, head="scarf", scarf_col="#5a3a2a", scarf_edge="#c9a24a", garment="dress",
                 col="#6a4a3a", col2="#3a2a1e", pattern="plain", hs=0.95, bs=0.95, belt=None, cuff="#c9a24a", trim="#c9a24a")

# ---- part 4 (episode 2): 829-835
MAMUN = spec(kind="old", skin="light", hair="short", hair_col="#bdb6ad", beard="grey", beard_col="#8a847c", grey=0.7, head="cap", head_col="#16161a",
             garment="robe", col="#1c1c22", col2="#0e0e12", pattern="plain", belt=None, cuff="#c9a24a", trim="#c9a24a")
MUTASIM = spec(kind="man", skin="tan", hair="short", beard="full", beard_col="#120c08", head="turban", head_col="#121216", turban_tail=True,
               garment="robe", col="#18181e", col2="#0a0a0e", pattern="brocade", build=1.22, belt=None, sash="#c9a24a", cuff="#c9a24a", trim="#e0b25a")
AFSHIN = spec(kind="man", skin="light", hair="short", beard="short", beard_col="#120c08", head="fur_hat", head_col="#3a2a20",
              garment="coat", col="#2e4a4a", col2="#1a2e2e", pattern="scales", scale_col="#c9a24a", fur="#4a3a2a", build=0.95,
              belt="#2b190c", cuff="#c9a24a", trim="#e0b25a")
DANCER_W = dict(VILLAGE_W, col="#9a1c1c", col2="#5a0e0e", scarf_col="#7a1414", scarf_edge="#e0b25a")

# ---- part 5 (episode 3): 835-836, the spy and the silver trap
SPY = spec(kind="man", skin="olive", hair="short", hair_col="#1a120c", beard="light", beard_col="#1a120c", head="cap", head_col="#2f6a5e",
           garment="tunic", col="#7a5a34", col2="#4a3620", pattern="plain", build=0.92, belt="#2b190c", buckle=False, cuff="#9a7a4a", trim="#9a7a4a")
SCOUT = spec(kind="man", skin="tan", hair="short", hair_col="#1a120c", beard="short", beard_col="#20140c", head="turban", head_col="#8a1a14", turban_tail=True,
             garment="tunic", col="#7a2a1a", col2="#4a1a10", pattern="plain", belt="#2b190c", buckle=False, cuff="#9a4a2a", trim="#9a4a2a")
DRUMMER = spec(kind="man", skin="tan", hair="short", beard="full", beard_col="#14100c", head="turban", head_col="#141418",
               garment="tunic", col="#26262c", col2="#121216", pattern="plain", build=1.15, belt="#5a3a1a", buckle=False, cuff="#3a3a42", trim="#c9a24a")

# ---- part 6 (episode 3): 836-837, the fall of Bazz
ABDULLAH = spec(kind="man", hair="long_curly", beard="short", beard_col="#17100c", head="none", garment="tunic", col="#8a221a", col2="#5a1410",
                pattern="scales", scale_col="#4a2a14", belt="#2b190c", cuff="#7a5a34", trim="#c9a24a", strap=True)
MESSENGER = spec(kind="man", skin="olive", hair="short", hair_col="#1a120c", beard="full", beard_col="#20160e", head="cap", head_col="#5a2a1a",
                 garment="tunic", col="#8a4a2a", col2="#5a2e1a", pattern="plain", belt="#2b190c", buckle=False, cuff="#7a5a3a", trim="#7a5a3a")
SAHL = spec(kind="old", skin="light", hair="short", hair_col="#8a827a", beard="grey", beard_col="#9a948c", grey=0.6, head="fur_hat", head_col="#4a3226",
            garment="robe", col="#24466a", col2="#142a44", pattern="brocade", fur="#d8c8a8", belt=None, sash="#c9a24a", cuff="#c9a24a", trim="#e0b25a", build=1.08)
BUGHA = spec(kind="man", skin="tan", hair="short", beard="full", beard_col="#120c08", grey=0.3, head="helmet", helm=STEEL, plume="#0c0c10",
             garment="coat", col="#1e1e24", col2="#0e0e12", pattern="scales", scale_col="#8a8e9a", belt="#2b190c", cuff="#5a5e6a", trim="#a8aebb",
             cloak="#1a1a20", cloak2="#0a0a0e", cloak_hi="#4a4a58", build=1.1)
PLOUGHMAN = dict(FARMER, head_col="#8a7a5a", col="#7a6a4a")

# ---- part 7 (episode 4): 837-838, the betrayal. Babak greys a little with every step towards Samarra (part 1's captive look).
BABAK_GUEST = dict(BABAK, head="none", grey=0.2)                                   # Sahl's guest: no helmet, his red cloak
BABAK_SLEEP = dict(BABAK_GUEST, cloak=None)
BABAK_CHAINED = dict(BABAK, head="none", grey=0.4, pattern="plain", col="#5a4632", col2="#3a2a1c", strap=False,
                     cloak="#6a4a34", cloak2="#4a3424", cloak_hi="#8a6a4a")       # a prisoner on the winter road
ABDULLAH_CHAINED = dict(ABDULLAH, strap=False, pattern="plain", col="#6a2a1e", col2="#4a1a12")
STEWARD = spec(kind="man", skin="light", hair="short", hair_col="#2a1a12", beard="short", beard_col="#2a1a12", head="cap", head_col="#3a4a2a",
               garment="robe", col="#4a5a3a", col2="#2a3a22", pattern="plain", belt=None, sash="#8a6a3a", cuff="#c9a24a", trim="#c9a24a", build=0.95)
NIGHT_RIDER = spec(kind="man", skin="olive", hair="short", hair_col="#1a120c", beard="short", beard_col="#1a120c", head="cap", head_col="#2a2a30",
                   garment="tunic", col="#3a3a44", col2="#22222a", pattern="plain", belt="#2b190c", buckle=False, cuff="#4a4a52", trim="#4a4a52",
                   cloak="#26262e", cloak2="#141418", cloak_hi="#4a4a58")
PRINCE = spec(kind="man", skin="tan", hair="short", beard="short", beard_col="#120c08", head="turban", head_col="#121216", turban_tail=True,
              garment="robe", col="#1e1e26", col2="#0e0e12", pattern="brocade", belt=None, sash="#c9a24a", cuff="#c9a24a", trim="#e0b25a")   # Harun, the caliph's son
OFFICIAL = dict(TAX_COLLECTOR, build=1.05)
OFFICIAL2 = dict(TAX_COLLECTOR, build=1.0, beard="full", skin="tan", head_col="#f0ead8", col="#2a2a33", sash="#8a2a2a")
PALACE_SERVANT = dict(SERVANT, head="turban", head_col="#f0ead8", col="#e2dccb", col2="#bdb5a0", cuff="#c9a24a", trim="#c9a24a", beard="light")
PALACE_SERVANT2 = dict(PALACE_SERVANT, skin="tan", beard="short", head="cap", head_col="#121216")
