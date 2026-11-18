"""Subtitles and place captions of part 5 -> build/zahhak/out/p05.ass (title/end cards and the header are overlays, see assemble.py)"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import series; series.from_folder(__file__)
from paths import OUT
from subs import sub_events, caption, write
from p05_audio import LINES
ev = sub_events(LINES)
ev.append(caption(32.0, 37.4, "Mount Damavand", "کوه دماوند", y=330))
ev.append(caption(61.3, 64.9, "The fourth day", "روز چهارم", y=280))
write(f"{OUT}/p05.ass", ev)
print(len(ev), "events")
