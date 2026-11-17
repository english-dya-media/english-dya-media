"""Subtitles and place captions of part 2 -> build/zahhak/out/p02.ass (title/end cards and the header are overlays, see assemble.py)"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import series; series.from_folder(__file__)
from paths import OUT
from subs import sub_events, caption, write
from p02_audio import LINES
ev = sub_events(LINES)
ev.append(caption(16.6, 20.4, "The palace of the Arab kings", "کاخ پادشاهان تازی"))
for t0, en, fa in ((44.5, "Day 1", "روز اول"), (53.1, "Day 2", "روز دوم"), (59.1, "Day 3", "روز سوم"), (61.7, "Day 4", "روز چهارم")):
    ev.append(caption(t0, t0 + 2.4, en, fa))
write(f"{OUT}/p02.ass", ev)
print(len(ev), "events")
