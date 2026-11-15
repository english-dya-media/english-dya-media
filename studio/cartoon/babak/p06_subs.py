"""Subtitles and place/year captions of part 6 -> build/babak/out/p06.ass (title/end cards and the header are overlays, see assemble.py)"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import series; series.from_folder(__file__)
from paths import OUT
from subs import sub_events, caption, write
from p06_audio import LINES
ev = sub_events(LINES)
ev.append(caption(36.9, 40.8, "Bazz · 15 August 837", "بذ · ۱۵ اوت ۸۳۷"))
ev.append(caption(112.4, 115.8, "Armenia · 837", "ارمنستان · ۸۳۷"))
write(f"{OUT}/p06.ass", ev)
print(len(ev), "events")
