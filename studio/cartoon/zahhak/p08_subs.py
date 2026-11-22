"""Subtitles and place captions of part 8 -> build/zahhak/out/p08.ass (title/end cards and the header are overlays, see assemble.py)"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import series; series.from_folder(__file__)
from paths import OUT
from subs import sub_events, caption, write
from p08_audio import LINES
ev = sub_events(LINES)
ev.append(caption(135.6, 140.2, "The Arvand river · the Tigris", "رود اروند · دجله", y=330))
write(f"{OUT}/p08.ass", ev)
print(len(ev), "events")
