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
