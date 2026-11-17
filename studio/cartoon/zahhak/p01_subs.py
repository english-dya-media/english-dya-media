"""Subtitles and place captions of part 1 -> build/zahhak/out/p01.ass (title/end cards and the header are overlays, see assemble.py)"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import series; series.from_folder(__file__)
from paths import OUT
from subs import sub_events, caption, write
from p01_audio import LINES
ev = sub_events(LINES)
ev.append(caption(15.0, 20.6, "Land of the Arabs · in the days of Jamshid", "سرزمین تازیان · روزگار جمشید"))
write(f"{OUT}/p01.ass", ev)
print(len(ev), "events")
