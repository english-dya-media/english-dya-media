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
