"""Subtitles and place captions of part 2 -> build/out/p02.ass"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import series; series.from_folder(__file__)
from paths import OUT
from subs import sub_events, caption, write
from p02_audio import LINES
ev = sub_events(LINES)
ev.append(caption(49.8, 55.0, "Bazz Fortress · Azerbaijan", "دژ بذ · آذربایجان", y=280))
write(f"{OUT}/p02.ass", ev)
print(len(ev), "events")
