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

# ---- part 2: Leyli as a young woman (the same indigo veil with silver coins, braids and red dress), the old elder of the Banu Amir (white
# beard, a red-checked head cloth, a brown robe), the ruler (a white turban with a jewel, a green robe with gold, a dark red cloak), Leyli's
# angry kinsman (short black beard, a grey head cloth, a dark blue robe), the messenger (young, a white head cloth, a sand-coloured tunic),
# the servants who carry the gifts, and the pilgrims in white at the Kaaba
LEYLI_W = spec(kind="woman", skin="light", hair="none", hair_col="#0e0908", beard=None, head="scarf", scarf_col="#2a2a6e", scarf_edge="#b6a2d8",
               coins=True, braids=True, braid_tie="#c4202a", garment="dress", col="#b8242a", col2="#7a141a", pattern="plain", hs=0.95, bs=0.95,
               belt=None, cuff="#2a2a6e", trim="#e4e6ea", boots="#5a3a22", iris="#1a0e08")
ELDER = spec(kind="old", skin="old", hair="short", hair_col="#d8d2c8", beard="white", head="kufiya", kufiya_col="#f0ece4", kufiya_shade="#cfc6b6",
             kufiya_pat="check", kufiya_pat_col="#a8262a", agal="#17161a", garment="robe", col="#7a5a3a", col2="#5a4028", pattern="plain",
             belt=None, sash="#3a2a1a", cuff="#c8b088", trim="#c8b088", iris="#3a2a1a", build=0.98)
RULER = spec(kind="man", skin="light", hair="short", hair_col="#1a120c", beard="full", beard_col="#2a1e14", head="turban", head_col="#f4efe2",
             turban_tail=True, garment="robe", col="#2a5a3a", col2="#1a3a26", pattern="brocade", cloak="#6a1a1e", cloak2="#4a0e12",
             cloak_hi="#c9a24a", belt=None, sash="#c9a24a", cuff="#c9a24a", trim="#c9a24a", iris="#2a1a10", build=1.12)
KINSMAN = spec(kind="man", skin="olive", hair="short", hair_col="#120c08", beard="short", beard_col="#120c08", head="kufiya", kufiya_col="#8a8a90",
               kufiya_shade="#6a6a70", agal="#17161a", garment="robe", col="#26365a", col2="#18243e", pattern="plain", belt=None, sash="#5a3a22",
               cuff="#8a7a5a", trim="#8a7a5a", iris="#1a0e08", build=1.02)
MESSENGER = spec(kind="man", skin="tan", hair="short", hair_col="#1a120c", beard="light", beard_col="#1a120c", head="kufiya", kufiya_col="#f2eee6",
                 kufiya_shade="#cfc6b6", agal="#17161a", garment="tunic", col="#c8a878", col2="#a08458", pattern="plain", belt="#5a3a22",
                 buckle=False, cuff="#e8dcc0", trim="#e8dcc0", trousers="#8a7a5a", boots="#5a3a22", iris="#2a170c", build=0.95)
SERVANT_A = spec(kind="man", skin="tan", hair="short", hair_col="#1a120c", beard="short", beard_col="#1a120c", head="cap", head_col="#e8e0cc",
                 garment="tunic", col="#6a7a8a", col2="#4a5a6a", pattern="plain", belt="#3a2a1a", buckle=False, cuff="#c8c0b0", trim="#c8c0b0",
                 trousers="#4a3a2a", boots="#3a2414", iris="#2a170c")
SERVANT_B = dict(SERVANT_A, skin="olive", beard="full", col="#8a5a3a", col2="#6a4028", head_col="#c8b08a")

# ---- part 3: Nawfal (a big, broad Arab chief with a full brown beard: a steel helmet with a green plume, steel scale armour over a green
# tunic, a white cloak with gold edges; he rides a big grey horse with a green blanket), his warriors (steel helmets, green plumes, green
# and white tunics), the warrior who speaks to Majnun (a short beard, a brown cloak), the men of Leyli's tribe (black head cloths with a
# dark red check, black and dark red robes), Leyli's father after the defeat (the same, his head cloth and cloak grey with dust), and Ibn
# Salam (a rich young man: a neat black beard, a white turban, a saffron silk robe with gold, a deep blue cloak)
STEEL = ("#2a2c34", "#5c606c", "#a8aebb")
NAWFAL = spec(kind="man", skin="olive", hair="short", hair_col="#2a1a10", beard="full", beard_col="#3a2414", head="helmet", helm=STEEL,
              plume="#1e7a44", garment="tunic", col="#2a6a42", col2="#1a4a2c", pattern="scales", scale_col="#b4bcc4", cloak="#ece6d8",
              cloak2="#c4bca8", cloak_hi="#c9a24a", belt="#5a3a1e", buckle=True, cuff="#c9a24a", trim="#c9a24a", trousers="#3a2e24",
              boots="#3a2414", iris="#2a1a10", build=1.18)
NAWFAL_MAN = spec(kind="man", skin="tan", hair="short", beard="short", beard_col="#1a120c", head="helmet", helm=STEEL, plume="#1e7a44",
                  garment="tunic", col="#2a6a42", col2="#1a4a2c", pattern="scales", scale_col="#a8b0b8", belt="#3a2a1a", buckle=False,
                  cuff="#e8e0cc", trim="#e8e0cc", trousers="#4a3a2a", boots="#3a2414", iris="#2a1a10")
NAWFAL_MAN_2 = dict(NAWFAL_MAN, skin="olive", beard="full", col="#e4dcc8", col2="#bcb29c", scale_col="#8a9aa4", trim="#2a6a42", cuff="#2a6a42")
NAWFAL_MAN_3 = dict(NAWFAL_MAN, skin="light", beard="light", col="#3a7a52", col2="#24543a", plume="#e8e0cc")
WARRIOR = dict(NAWFAL_MAN, skin="tan", beard="short", beard_col="#20160e", cloak="#6a4a2a", cloak2="#4a3018", cloak_hi="#8a6a3a",
               col="#2a6a42", col2="#1a4a2c", build=1.05)
TRIBE_MAN = spec(kind="man", skin="olive", hair="short", hair_col="#120c08", beard="short", beard_col="#120c08", head="kufiya",
                 kufiya_col="#26242c", kufiya_shade="#141318", kufiya_pat="check", kufiya_pat_col="#6a1a1e", agal="#0a0a0c", garment="tunic",
                 col="#3a1416", col2="#220a0c", pattern="plain", belt="#1a1210", buckle=False, cuff="#6a1a1e", trim="#6a1a1e", trousers="#2a2224",
                 boots="#1e1410", iris="#1a0e08")
TRIBE_MAN_2 = dict(TRIBE_MAN, skin="tan", beard="full", col="#26262c", col2="#141418", kufiya_col="#5a1416", kufiya_shade="#360a0c",
                   kufiya_pat=None)
TRIBE_MAN_3 = dict(TRIBE_MAN, skin="light", beard="light", col="#5a1a1c", col2="#3a0e10")
LEYLI_FATHER_DUST = dict(LEYLI_FATHER, kufiya_col="#6a625c", kufiya_shade="#4a4440", kufiya_pat_col="#7a5a50", col="#4e4a48", col2="#2e2c2c",
                         cloak="#6a4a42", cloak2="#4a322e", cloak_hi="#9a8a6a", grey=0.25)
IBN_SALAM = spec(kind="man", skin="light", hair="short", hair_col="#140e0a", beard="light", beard_col="#140e0a", head="turban",
                 head_col="#f6f0e2", turban_tail=True, garment="robe", col="#d0802a", col2="#9a5414", pattern="brocade", cloak="#22407a",
                 cloak2="#162a52", cloak_hi="#c9a24a", belt=None, sash="#c9a24a", cuff="#c9a24a", trim="#c9a24a", iris="#2a1a10", build=0.98)
