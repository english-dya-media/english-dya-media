"""Subtitles and place captions of part 6 -> build/zahhak/out/p06.ass (title/end cards and the header are overlays, see assemble.py)"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import series; series.from_folder(__file__)
from paths import OUT
from subs import sub_events, caption, write
from p06_audio import LINES
ev = sub_events(LINES)
ev.append(caption(70.4, 75.6, "Mount Alborz", "کوه البرز", y=330))
ev.append(caption(100.8, 105.6, "Sixteen years later", "شانزده سال بعد", y=330))
write(f"{OUT}/p06.ass", ev)
print(len(ev), "events")
