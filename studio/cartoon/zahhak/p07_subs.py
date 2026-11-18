"""Subtitles and place captions of part 7 -> build/zahhak/out/p07.ass (title/end cards and the header are overlays, see assemble.py)"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import series; series.from_folder(__file__)
from paths import OUT
from subs import sub_events, caption, write
from p07_audio import LINES
ev = sub_events(LINES)
ev.append(caption(48.8, 53.4, "Zahhak's palace", "کاخ ضحاک", y=330))
ev.append(caption(129.8, 134.4, "The city market", "بازار شهر", y=330))
write(f"{OUT}/p07.ass", ev)
print(len(ev), "events")
