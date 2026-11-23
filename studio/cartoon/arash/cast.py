# Looks of this series' characters, made with chars.spec() (see babak/cast.py for examples). Keep a look fixed once
# a part with it is published.
from chars import spec

# ---- part 1: Arash (a lean archer of about 30: plain undyed wool, an olive cloak, a leather bracer (the cuffs), long dark hair, a light
# beard, a calm face; his great bow), King Manuchehr (tired by the long siege: a greying beard, a gold crown, blue and gold), Afrasiab, king
# of Turan (a black helmet with a red plume, black scale armour, a red cloak; a sharp, smiling face), an Iranian general (bronze helmet,
# blue scales, red cloak), the messenger, a hungry mother and her boy, soldiers of Iran (bronze, blue) and of Turan (black, red)
ARASH = spec(kind="man", skin="tan", hair="long_curly", hair_col="#1e140c", beard="light", beard_col="#1e140c", head="none", garment="tunic",
             col="#8a7656", col2="#66563c", pattern="plain", cloak="#4e5a36", cloak2="#343e22", cloak_hi="#6e7a4e", belt="#5a3a1e", buckle=False,
             cuff="#7a4a24", trim="#a8946e", trousers="#4a3a2a", boots="#3a2414", iris="#3a2214", build=0.96, bs=1.06)
MANUCHEHR = spec(kind="man", skin="light", hair="long_curly", hair_col="#4a423a", beard="full", beard_col="#6a625a", head="crown", crown_h=1.25,
                 jewel="#1c4aa8", jewel2="#b8121c", garment="robe", col="#1e4a7a", col2="#123052", pattern="brocade", cloak="#c9a24a",
                 cloak2="#8a6a22", cloak_hi="#f0d48a", belt=None, sash="#c9a24a", cuff="#f0d48a", trim="#f0d48a", iris="#3a2a1a", build=1.05)
AFRASIAB = spec(kind="man", skin="light", hair="long_curly", hair_col="#140e0a", beard="short", beard_col="#140e0a", head="helmet",
                helm=("#141418", "#3a3a46", "#7a7a8a"), plume="#b3181d", garment="tunic", col="#1c1c22", col2="#0c0c10", pattern="scales",
                scale_col="#8a1a1a", cloak="#7a0e12", cloak2="#4a080a", cloak_hi="#b8202a", belt="#2b190c", buckle=False, cuff="#8a1a1a",
                trim="#c9a24a", iris="#2a1a10", build=1.1)
GENERAL = spec(kind="man", skin="olive", hair="short", hair_col="#1a120c", beard="full", beard_col="#3a2a1e", head="helmet",
               helm=("#5a3c14", "#a8782a", "#ecc66a"), plume="#1e4a8a", garment="tunic", col="#1e4a6a", col2="#123448", pattern="scales",
               scale_col="#8ab0c8", cloak="#7a1a1a", cloak2="#4a0e0e", cloak_hi="#a83a2a", belt="#2b190c", cuff="#c9a24a", trim="#c9a24a",
               iris="#2a1a10", build=1.1)
MESSENGER = spec(kind="man", skin="tan", hair="short", hair_col="#1a120c", beard="short", beard_col="#1a120c", head="turban", head_col="#e8e0cc",
                 garment="robe", col="#2f6a4a", col2="#1e4632", pattern="plain", belt=None, sash="#c9a24a", cuff="#c9a24a", trim="#c9a24a",
                 iris="#2a1a10", build=0.95)
MOTHER = spec(kind="woman", skin="tan", hair="none", beard=None, head="scarf", scarf_col="#5a4632", scarf_edge="#a89878", garment="dress",
              col="#6a5a4a", col2="#4a3e32", pattern="plain", hs=0.95, bs=0.95, belt=None, cuff="#a89878", trim="#a89878", iris="#3a2214")
BOY = spec(kind="boy", skin="tan", hair="boy_curly", hair_col="#1a120c", beard=None, head="none", garment="child", col="#7a8a6a", col2="#5a6a4a",
           pattern="plain", hs=1.1, bs=0.6, belt="#5a4228", buckle=False, cuff="#9aa88a", trim="#9aa88a", trousers="#4a3a2a", iris="#3a2214")
IRAN_SOLDIER = spec(kind="man", skin="tan", hair="short", beard="short", beard_col="#1a120c", head="helmet", helm=("#6a4a22", "#a8782a", "#e0b25a"),
                    plume="#1e4a8a", garment="tunic", col="#3a5a7a", col2="#24405a", pattern="scales", scale_col="#a8bcd0", belt="#2b190c",
                    buckle=False, cuff="#8a7a5a", trim="#8a7a5a", iris="#2a1a10")
IRAN_SOLDIER_2 = dict(IRAN_SOLDIER, skin="olive", beard="full", col="#5a4a3a", col2="#3a2e24", plume="#c9a24a")
IRAN_SOLDIER_3 = dict(IRAN_SOLDIER, skin="light", beard="light", col="#3a5a4a", col2="#24402f", helm=("#5a5a62", "#8a8a96", "#c8c8d0"))
TURAN_SOLDIER = spec(kind="man", skin="light", hair="short", beard="short", beard_col="#120c09", head="helmet", helm=("#141418", "#3a3a44", "#6a6a78"),
                     plume="#8a1a1a", garment="tunic", col="#2a1a1a", col2="#140c0c", pattern="scales", scale_col="#6a3a3a", belt="#2b190c",
                     buckle=False, cuff="#5a2a2a", trim="#8a1a1a", iris="#2a1a10")
TURAN_SOLDIER_2 = dict(TURAN_SOLDIER, skin="tan", beard="full", col="#1c1c22", col2="#0c0c10", plume="#141418")
# Afrasiab's old advisor (a white beard, a dark red robe, a black cap)
ADVISOR = spec(kind="old", skin="old", hair="short", hair_col="#d8d2c8", beard="white", head="cap", head_col="#1e1618", garment="robe",
               col="#5a1a1a", col2="#3a0e0e", pattern="plain", cloak="#1c1a20", cloak2="#0e0d12", cloak_hi="#3a3640", belt=None, sash="#c9a24a",
               cuff="#8a6a3a", trim="#8a6a3a", iris="#3a2a1a", build=0.95)

# ---- part 2: Spandarmad (the guardian of the earth: a woman of soft green light, a pale green veil with a diadem), the old bowyer (white
# beard, a brown cap, a leather apron), the smith (strong, short beard, a dark cap, a long leather apron), Arash's mother (an older village
# woman in a blue scarf), two witnesses of Turan (Afrasiab's officers: black helmets, red plumes), and Arash without his cloak (on the summit)
SPANDARMAD = spec(kind="woman", skin="light", hair="none", beard=None, head="scarf", scarf_col="#cfeecb", scarf_edge="#5ab46a", diadem=True,
                  garment="dress", col="#8fd49a", col2="#5aa86a", pattern="plain", hs=0.95, bs=1.0, belt=None, cuff="#e8f8d8", trim="#e8f8d8",
                  iris="#2a6a4a")
BOWYER = spec(kind="old", skin="old", hair="short", hair_col="#d8d2c8", beard="white", head="cap", head_col="#6a4a2a", garment="robe",
              col="#5a6a4a", col2="#3a4a2e", pattern="plain", apron="#8a6a44", belt="#3a2414", buckle=False, cuff="#8a7a5a", trim="#8a7a5a",
              iris="#3a2a1a", build=0.95)
SMITH = spec(kind="man", skin="olive", hair="short", hair_col="#140e0a", beard="short", beard_col="#140e0a", head="cap", head_col="#2a2420",
             garment="tunic", col="#6a4a3a", col2="#4a3226", pattern="plain", apron="#5a3a22", apron_hem=1010, belt="#2b190c", buckle=False,
             cuff="#4a3226", trim="#4a3226", trousers="#3a2a22", iris="#2a1a10", build=1.12)
ARASH_MOTHER = spec(kind="woman", skin="tan", hair="none", beard=None, head="scarf", scarf_col="#2f4a8a", scarf_edge="#c8d4e8", garment="dress",
                    col="#5a4a6a", col2="#3a3048", pattern="plain", hs=0.95, bs=0.95, belt=None, cuff="#c8d4e8", trim="#c8d4e8", iris="#3a2214",
                    grey=0.4)
WITNESS_A = dict(TURAN_SOLDIER, beard="full", beard_col="#2a1a12", cloak="#5a0e10", cloak2="#3a080a", cloak_hi="#8a1a1a", scale_col="#8a2a2a")
WITNESS_B = dict(TURAN_SOLDIER_2, skin="light", beard="short", beard_col="#120c09", plume="#b3181d", cloak="#3a3a44", cloak2="#1e1e26",
                 cloak_hi="#5a5a68")
ARASH_BARE = dict(ARASH, cloak=None)
