# Looks of this series' characters, made with chars.spec() (see babak/cast.py for examples). Keep a look fixed once
# a part with it is published.
from chars import spec

# ---- part 1: Mardas's land (an Arab king of the plains), his son Zahhak, Iblis as a smiling well-wisher
# Zahhak as a young prince: curly hair, a young beard, crimson and gold, a black cloak with a crimson lining
ZAHHAK_PRINCE = spec(kind="man", skin="tan", hair="teen_curly", hair_col="#140e0a", beard="light", beard_col="#140e0a", head="none",
                     garment="tunic", col="#8e1a24", col2="#5a0e16", pattern="brocade", cloak="#17151b", cloak2="#5a0e16", cloak_hi="#3a3440",
                     belt="#2b190c", cuff="#d8a64a", trim="#d8a64a", iris="#3a2214")
# Zahhak as king (the hook; from part 2 on): a dark full beard, a gold crown, black and crimson, two black snakes on his shoulders
ZAHHAK_KING = spec(kind="man", skin="tan", hair="long_curly", hair_col="#120c09", beard="full", beard_col="#120c09", head="crown",
                   garment="robe", col="#141218", col2="#08070a", pattern="brocade", cloak="#6a0c14", cloak2="#3a060c", cloak_hi="#a8202a",
                   belt=None, sash="#a8202a", cuff="#d8a64a", trim="#d8a64a", iris="#3a2214", snakes=True, build=1.05)
# King Mardas: kind and old, white beard, a white head cloth, a white robe under a camel-brown cloak
MARDAS = spec(kind="old", skin="old", hair="short", hair_col="#e0dad0", beard="white", head="kufiya", kufiya_col="#f4f0e8", kufiya_shade="#d2c9b8",
              garment="robe", col="#ece5d6", col2="#c8bea8", pattern="plain", cloak="#8a5a2e", cloak2="#6a4220", cloak_hi="#b88446",
              belt=None, sash="#c9a24a", cuff="#c9a24a", trim="#d8b25a", iris="#3a2a1a")
# Iblis, first disguise: a smiling young well-wisher in green; his amber eyes stay the same in every disguise
IBLIS_FRIEND = spec(kind="man", skin="light", hair="short", hair_col="#1a120c", beard="short", beard_col="#1a120c", head="turban", head_col="#2f6a4a",
                    turban_tail=True, garment="robe", col="#2f6a4a", col2="#1e4632", pattern="plain", belt=None, sash="#c9a24a",
                    cuff="#c9a24a", trim="#c9a24a", iris="#c8981c", build=0.95)
HERDSMAN = spec(kind="man", skin="olive", hair="short", beard="short", beard_col="#2a1a10", head="kufiya", kufiya_col="#efe8dc", kufiya_shade="#cbbfaa",
                kufiya_pat="check", kufiya_pat_col="#a8262a", agal="#2a1e16", garment="robe", col="#8a7556", col2="#5e4e38", pattern="plain",
                belt="#3a2414", buckle=False, cuff="#a8946e", trim="#a8946e")
POOR_BOY = spec(kind="boy", skin="tan", hair="boy_curly", beard=None, head="none", garment="child", col="#6a7f8f", col2="#4a5a68", pattern="plain",
                hs=1.08, bs=0.62, belt="#5a4228", buckle=False, cuff="#8a9aa8", trim="#8a9aa8", trousers="#4a3a2a")
POOR_MOTHER = spec(kind="woman", skin="tan", hair="none", beard=None, head="scarf", scarf_col="#4a3a5a", scarf_edge="#a89878", garment="dress",
                   col="#6a5a4a", col2="#4a3e32", pattern="plain", hs=0.95, bs=0.95, belt=None, cuff="#a89878", trim="#a89878")

# ---- part 2: Zahhak, young and crowned on his father's throne (the snakes grow out of his shoulders at the end of the part);
# Iblis's second disguise: a young cook in white (the same amber eyes)
ZAHHAK_YOUNG_KING = dict(ZAHHAK_PRINCE, head="crown", garment="robe", col="#141218", col2="#08070a", pattern="brocade",
                         cloak="#6a0c14", cloak2="#3a060c", cloak_hi="#a8202a", belt=None, sash="#a8202a", snakes=True)
IBLIS_COOK = spec(kind="man", skin="light", hair="short", hair_col="#1a120c", beard="light", beard_col="#1a120c", head="cap", head_col="#f2eee6",
                  garment="tunic", col="#ece6da", col2="#c8bea8", pattern="plain", belt="#8a6a40", buckle=False, cuff="#d8cfbe", trim="#d8cfbe",
                  trousers="#5a4a3a", iris="#c8981c", build=0.95)
COURTIER = spec(kind="man", skin="tan", hair="short", beard="full", beard_col="#1a120c", head="kufiya", kufiya_col="#f2eee6", agal="#17161a",
                garment="robe", col="#3a5a6a", col2="#24404c", pattern="plain", belt=None, sash="#c9a24a", cuff="#c9a24a", trim="#c9a24a")
COURTIER2 = dict(COURTIER, beard="white", kind="old", skin="old", col="#6a4a2a", col2="#4a321c", kufiya_pat="check", kufiya_pat_col="#a8262a")
COURTIER3 = dict(COURTIER, beard="short", col="#5a2a3a", col2="#3a1a24", head="turban", head_col="#e8e0cc", skin="olive")

# ---- part 3: Iblis's third disguise: a doctor in grey with a leather bag (the same amber eyes); the court doctors; King Jamshid on his
# jewelled throne (long white beard, a tall crown, lapis blue and gold) and his nobles; a noble rider of Iran; Zahhak's guards;
# Arnavaz and Shahrnaz, princesses of Jamshid's house, in pale silk
IBLIS_DOCTOR = spec(kind="man", skin="light", hair="short", hair_col="#1a120c", beard="short", beard_col="#2a221c", head="turban", head_col="#45454f",
                    garment="robe", col="#6e6e78", col2="#4a4a54", pattern="plain", belt=None, sash="#34343c", cuff="#9a9aa4", trim="#9a9aa4",
                    iris="#c8981c", build=0.95)
DOCTOR_A = spec(kind="old", skin="old", hair="short", hair_col="#d8d2c8", beard="white", head="turban", head_col="#f2eee6", garment="robe",
                col="#2a3a6a", col2="#1a2648", pattern="plain", belt=None, sash="#c9a24a", cuff="#c9a24a", trim="#c9a24a", iris="#3a2a1a")
DOCTOR_B = spec(kind="man", skin="olive", hair="short", beard="full", beard_col="#6a625a", head="turban", head_col="#e8dcc0", garment="robe",
                col="#6a4a2a", col2="#4a321c", pattern="plain", belt="#3a2414", buckle=False, cuff="#a8946e", trim="#a8946e", iris="#2a1a10")
DOCTOR_C = spec(kind="old", skin="tan", hair="short", hair_col="#d8d2c8", beard="white", head="kufiya", kufiya_col="#efe8dc", kufiya_shade="#cbbfaa",
                agal="#2a1e16", garment="robe", col="#3a5a3a", col2="#24402a", pattern="plain", belt=None, sash="#8a6a3a", cuff="#c9b07a", trim="#c9b07a")
JAMSHID = spec(kind="old", skin="old", hair="long_curly", hair_col="#bdb6ac", beard="white", head="crown", crown_h=1.7, jewel="#1c4aa8", jewel2="#b8121c",
               garment="robe", col="#1e3a7a", col2="#132654", pattern="brocade", cloak="#c9a24a", cloak2="#8a6a22", cloak_hi="#f6dc8a",
               belt=None, sash="#c9a24a", cuff="#f0d48a", trim="#f0d48a", iris="#3a2a1a", build=1.08)
IRAN_NOBLE = spec(kind="man", skin="light", hair="long_curly", hair_col="#1a120c", beard="full", beard_col="#1a120c", head="helmet",
                  helm=("#5a3c14", "#a8782a", "#ecc66a"), plume="#1e4a8a", garment="tunic", col="#1e4a6a", col2="#123448", pattern="scales",
                  cloak="#7a1a1a", cloak2="#4a0e0e", cloak_hi="#a83a2a", belt="#2b190c", cuff="#c9a24a", trim="#c9a24a", iris="#2a1a10")
NOBLE_1 = spec(kind="man", skin="light", hair="short", beard="full", beard_col="#2a1a10", head="turban", head_col="#f2eee6", garment="robe",
               col="#1f6a6a", col2="#124646", pattern="brocade", belt=None, sash="#c9a24a", cuff="#c9a24a", trim="#c9a24a")
NOBLE_2 = spec(kind="old", skin="old", hair="short", hair_col="#d8d2c8", beard="white", head="cap", head_col="#8a1a24", garment="robe",
               col="#b8642a", col2="#7a3e16", pattern="plain", belt=None, sash="#5a1a1a", cuff="#e0b25a", trim="#e0b25a")
NOBLE_3 = dict(IRAN_NOBLE, plume="#b3181d", col="#4a3a6a", col2="#2a2048", cloak="#1e4a3a", cloak2="#123026", cloak_hi="#2e6a52", beard="short")
ZGUARD = spec(kind="man", skin="tan", hair="short", beard="short", beard_col="#120c09", head="helmet", helm=("#141418", "#3a3a44", "#6a6a78"),
              plume="#6a0c14", garment="tunic", col="#17151b", col2="#08070a", pattern="scales", scale_col="#6a6a78", belt="#2b190c", buckle=False,
              cuff="#3a3a44", trim="#6a0c14")
ARNAVAZ = spec(kind="woman", skin="light", hair="none", beard=None, head="scarf", scarf_col="#dfe6f2", scarf_edge="#c9a24a", diadem=True,
               garment="dress", col="#9fb4d6", col2="#7088b0", pattern="plain", hs=0.95, bs=0.95, belt=None, cuff="#c9a24a", trim="#c9a24a", iris="#3a2a1a")
SHAHRNAZ = dict(ARNAVAZ, scarf_col="#f4e2e8", col="#d8a8b8", col2="#a87888", iris="#4a2a17")

# ---- part 4: Armayel and Garmayel, two good men of the city (at home in their robes; in the king's kitchen with a white apron over the
# robe: not all in white like Iblis the cook); two young men taken to the palace; the king at night without his crown
ARMAYEL = spec(kind="man", skin="olive", hair="short", hair_col="#1a120c", beard="full", beard_col="#2a1a10", head="cap", head_col="#5a3a22",
               garment="robe", col="#7a5a3a", col2="#5a4028", pattern="plain", belt="#3a2414", buckle=False, cuff="#a8946e", trim="#a8946e",
               iris="#3a2214", build=1.05)
GARMAYEL = spec(kind="man", skin="light", hair="short", hair_col="#3a2a1e", beard="short", beard_col="#4a3a2a", head="turban", head_col="#e8dcc0",
                garment="robe", col="#3a5a6a", col2="#24404c", pattern="plain", belt="#2b190c", buckle=False, cuff="#8aa0aa", trim="#8aa0aa",
                iris="#2a4a3a", build=0.95)
ARMAYEL_COOK = dict(ARMAYEL, apron="#ece6da", head_col="#ece6da")
GARMAYEL_COOK = dict(GARMAYEL, apron="#ece6da")
YOUNG_MAN = spec(kind="man", skin="tan", hair="teen_curly", hair_col="#1a120c", beard="light", beard_col="#1a120c", head="none", garment="tunic",
                 col="#6a7f8f", col2="#4a5a68", pattern="plain", belt="#5a4228", buckle=False, cuff="#8a9aa8", trim="#8a9aa8", trousers="#4a3a2a", iris="#3a2214")
YOUNG_MAN_2 = dict(YOUNG_MAN, hair="short", skin="olive", col="#8a6a3a", col2="#6a4a2a", cuff="#b89a6a", trim="#b89a6a")
ZAHHAK_NIGHT = dict(ZAHHAK_KING, head="none", cloak=None, col="#2a1e2a", col2="#1a121a", pattern="plain", sash="#6a0c14")

# ---- part 5: Zirak, the old mobed who dares to speak, and the other wise men (white robes, white caps and turbans); Faranak (a dark
# scarf, deep red) and Abtin (of the old royal line, in hiding: a plain green-grey robe and a brown travelling cloak); the three warriors
# of the dream are drawn as glowing silhouettes, so only their outline matters (helmets, plumes, cloaks, the youngest taller)
ZIRAK = spec(kind="old", skin="old", hair="short", hair_col="#e8e2d8", beard="white", head="turban", head_col="#f6f2ea", garment="robe",
             col="#efe9dc", col2="#cfc5b0", pattern="plain", cloak="#e2dacb", cloak2="#bdb19a", cloak_hi="#fffaf0", belt=None, sash="#d8ccb0",
             cuff="#d8cfbe", trim="#c9a24a", iris="#3a2a1a", build=0.95)
MOBED_1 = spec(kind="old", skin="tan", hair="short", hair_col="#d8d2c8", beard="full", beard_col="#9a928a", head="cap", head_col="#f2eee6",
               garment="robe", col="#e8e1d2", col2="#c4b9a2", pattern="plain", belt=None, sash="#c9b98e", cuff="#d8cfbe", trim="#b8a47a", iris="#3a2a1a")
MOBED_2 = spec(kind="man", skin="olive", hair="short", hair_col="#2a1a10", beard="full", beard_col="#2a1a10", head="turban", head_col="#e8dcc0",
               garment="robe", col="#e2d8c4", col2="#bfb196", pattern="plain", belt=None, sash="#b89a5a", cuff="#d0c4a8", trim="#b89a5a", iris="#2a1a10")
MOBED_3 = spec(kind="old", skin="light", hair="short", hair_col="#cfc8be", beard="short", beard_col="#8a8278", head="cap", head_col="#ddd6c8",
               garment="robe", col="#dcd5c6", col2="#b8ae9a", pattern="plain", belt=None, sash="#a8987a", cuff="#cfc6b4", trim="#a8987a", iris="#3a2a1a")
MOBED_4 = dict(MOBED_2, skin="tan", beard="short", beard_col="#4a3a2a", head="cap", head_col="#f0ece2", col="#ece6d8", col2="#c8bea8")
FARANAK = spec(kind="woman", skin="light", hair="none", beard=None, head="scarf", scarf_col="#23264a", scarf_edge="#c9a24a", garment="dress",
               col="#7a2234", col2="#561424", pattern="plain", hs=0.95, bs=0.95, belt=None, cuff="#c9a24a", trim="#c9a24a", iris="#3a2a1a")
ABTIN = spec(kind="man", skin="light", hair="long_curly", hair_col="#2a1a10", beard="full", beard_col="#2a1a10", head="none", garment="robe",
             col="#3e5a4a", col2="#28402f", pattern="plain", cloak="#6a4a2e", cloak2="#4a3220", cloak_hi="#8a6a42", belt="#3a2414", buckle=False,
             cuff="#a8946e", trim="#a8946e", iris="#3a2214", build=1.0)
DREAM_ELDER = spec(kind="man", skin="tan", hair="long_curly", beard="full", head="helmet", helm=("#2a2a30", "#4a4a54", "#6a6a78"), plume="#6a0c14",
                   garment="tunic", col="#2a2a30", col2="#141418", pattern="scales", cloak="#2a1a1a", cloak2="#140c0c", cloak_hi="#3a2a2a",
                   belt="#2b190c", cuff="#3a3a44", trim="#3a3a44", build=1.08)
DREAM_YOUNG = spec(kind="man", skin="light", hair="long_curly", beard="light", head="helmet", helm=("#2a2a30", "#4a4a54", "#6a6a78"), plume="#c9a24a",
                   garment="tunic", col="#2a2a30", col2="#141418", pattern="scales", cloak="#2a1a1a", cloak2="#140c0c", cloak_hi="#3a2a2a",
                   belt="#c9a24a", cuff="#3a3a44", trim="#3a3a44", build=1.0, bs=1.1)
