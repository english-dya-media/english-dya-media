"""Subtitles and place captions of part 9 -> build/zahhak/out/p09.ass (title/end cards and the header are overlays, see assemble.py)"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import series; series.from_folder(__file__)
from paths import OUT
from subs import sub_events, caption, write
from p09_audio import LINES
ev = sub_events(LINES)
ev.append(caption(35.9, 40.4, "Gang Dezhhukht · Zahhak's palace", "گنگ‌دژهوخت · کاخ ضحاک", y=330))
ev.append(caption(107.0, 111.6, "Zahhak's camp in India", "اردوی ضحاک در هندوستان", y=330))
write(f"{OUT}/p09.ass", ev)
print(len(ev), "events")
