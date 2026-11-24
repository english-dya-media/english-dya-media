# Looks of this series' characters, made with chars.spec() (see babak/cast.py for examples). Keep a look fixed once
# a part with it is published.
from chars import spec

# ---- part 1: Qays as a boy of about 12 (black curls, an off-white shirt with an indigo sash and trim, brown sandals), Leyli as a girl of
# about 12 (an indigo veil with a row of silver coins over the forehead, two black braids over the shoulders, a red dress with indigo
# cuffs, dark eyes), Qays's father the chief of the Banu Amir (grey beard, a white head cloth with a black cord, a cream robe under a
# brown cloak with gold edges), the old teacher of the tent school (white beard, white turban, a grey-blue robe), Leyli's mother (a dark
# veil, an indigo dress), Leyli's father (black beard, a black head cloth with a dark red check, a black robe under a dark red cloak),
# their classmates, and Majnun as a thin young man in the hook (long wild hair, a light beard, a torn white shirt, bare feet)
QAYS = spec(kind="boy", skin="tan", hair="boy_curly", hair_col="#120c0a", beard=None, head="none", garment="child", col="#ece4d2", col2="#c4b8a0",
            pattern="plain", hs=1.1, bs=0.62, belt=None, sash="#2a3e86", cuff="#d8ccb2", trim="#2a3e86", trousers="#d8ceb8", boots="#6a4626",
            iris="#2a170c")
LEYLI = spec(kind="boy", skin="light", hair="none", hair_col="#0e0908", beard=None, head="scarf", scarf_col="#2a2a6e", scarf_edge="#b6a2d8",
             coins=True, braids=True, braid_tie="#c4202a", lashes=True, garment="dress", col="#b8242a", col2="#7a141a", pattern="plain",
             hs=1.08, bs=0.64, belt=None, cuff="#2a2a6e", trim="#e4e6ea", boots="#5a3a22", iris="#1a0e08")
CHIEF = spec(kind="old", skin="tan", hair="short", hair_col="#8a8680", beard="full", beard_col="#a6a198", head="kufiya", kufiya_col="#f4f0e8",
             kufiya_shade="#d2cabc", agal="#17161a", garment="robe", col="#e8dcc2", col2="#c2b292", pattern="plain", cloak="#5a3a22",
             cloak2="#3a2414", cloak_hi="#c9a24a", belt=None, sash=None, cuff="#c9a24a", trim="#c9a24a", iris="#3a2214", build=1.04)
TEACHER = spec(kind="old", skin="old", hair="short", hair_col="#d8d2c8", beard="white", head="turban", head_col="#f0ead8", garment="robe",
               col="#56687a", col2="#3a4a5a", pattern="plain", belt=None, sash="#8a6a3a", cuff="#c8c0a8", trim="#c8c0a8", iris="#3a2a1a",
               build=0.96)
MOTHER = spec(kind="woman", skin="light", hair="none", beard=None, head="scarf", scarf_col="#1e1a2a", scarf_edge="#8a7aa0", garment="dress",
              col="#3a2e5a", col2="#262040", pattern="plain", hs=0.95, bs=0.95, belt=None, cuff="#c8c0d8", trim="#c8c0d8", iris="#2a1a10")
LEYLI_FATHER = spec(kind="man", skin="olive", hair="short", hair_col="#0e0a08", beard="full", beard_col="#0e0a08", head="kufiya",
                    kufiya_col="#26242c", kufiya_shade="#141318", kufiya_pat="check", kufiya_pat_col="#6a1a1e", agal="#0a0a0c",
                    garment="robe", col="#26262c", col2="#141418", pattern="plain", cloak="#5a1416", cloak2="#360a0c", cloak_hi="#c9a24a",
                    belt=None, sash=None, cuff="#c9a24a", trim="#c9a24a", iris="#1a0e08", build=1.08)
MAJNUN = spec(kind="man", skin="tan", hair="long_curly", hair_col="#120c0a", beard="light", beard_col="#120c0a", head="none",
              garment="robe", col="#e6e0d2", col2="#b4ac9c", pattern="plain", rags=True, patch="#c8b896", belt=None, sash=None,
              cuff="#d8d0c0", trim="#d8d0c0", trousers="#c98a5e", boots="#b07a52", iris="#2a170c", build=0.86)
# classmates (children of the tribes) and the boys of the camp
GIRL_A = spec(kind="boy", skin="tan", hair="none", beard=None, head="scarf", scarf_col="#3a7a52", scarf_edge="#f0d890", garment="dress",
              col="#d8782a", col2="#a4521a", pattern="plain", hs=1.08, bs=0.62, belt=None, cuff="#f0d890", trim="#f0d890", iris="#2a170c")
GIRL_B = spec(kind="boy", skin="olive", hair="none", beard=None, head="scarf", scarf_col="#7a3a6a", scarf_edge="#f0c8d8", garment="dress",
              col="#2e6a8a", col2="#1e4a62", pattern="plain", hs=1.08, bs=0.6, belt=None, cuff="#f0c8d8", trim="#f0c8d8", iris="#2a170c")
BOY_A = spec(kind="boy", skin="olive", hair="short", hair_col="#140e0a", beard=None, head="cap", head_col="#f0ead8", garment="child",
             col="#8a6a3a", col2="#6a4e28", pattern="plain", hs=1.1, bs=0.6, belt="#4a3420", buckle=False, cuff="#c8b088", trim="#c8b088",
             trousers="#5a4a3a", boots="#4a3020", iris="#2a170c")
BOY_B = spec(kind="boy", skin="tan", hair="boy_curly", hair_col="#1a120c", beard=None, head="none", garment="child", col="#5a7a3a",
             col2="#3e5a28", pattern="plain", hs=1.1, bs=0.58, belt="#4a3420", buckle=False, cuff="#b8c890", trim="#b8c890",
             trousers="#4a3a2a", boots="#4a3020", iris="#2a170c")
BOY_C = spec(kind="boy", skin="light", hair="short", hair_col="#2a1a10", beard=None, head="cap", head_col="#7a2a2a", garment="child",
             col="#6a5a8a", col2="#4a3e66", pattern="plain", hs=1.1, bs=0.6, belt="#4a3420", buckle=False, cuff="#c8c0e0", trim="#c8c0e0",
             trousers="#3a3a4a", boots="#3a2818", iris="#2a170c")
# women of the camp who pass the talk on (part 1, scene 5)
GOSSIP_A = spec(kind="woman", skin="tan", hair="none", beard=None, head="scarf", scarf_col="#5a2a2a", scarf_edge="#d8b080", garment="dress",
                col="#7a4a2a", col2="#5a321a", pattern="plain", hs=0.95, bs=0.95, belt=None, cuff="#d8b080", trim="#d8b080", iris="#2a1a10")
GOSSIP_B = spec(kind="woman", skin="olive", hair="none", beard=None, head="scarf", scarf_col="#2a4a5a", scarf_edge="#c8d8e0", garment="dress",
                col="#4a5a3a", col2="#323e26", pattern="plain", hs=0.95, bs=0.95, belt=None, cuff="#c8d8e0", trim="#c8d8e0", iris="#2a1a10",
                grey=0.3)
