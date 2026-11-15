"""Subtitles and place/year captions of part 3 -> build/babak/out/p03.ass (title/end cards and the header are overlays, see assemble.py)"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import series; series.from_folder(__file__)
from paths import OUT
from subs import sub_events, caption, write
from p03_audio import LINES
ev = sub_events(LINES)
ev.append(caption(0.6, 4.3, "Hashtadsar · June 829", "هشتادسر · ژوئن ۸۲۹"))
ev.append(caption(18.6, 23.4, "Azerbaijan · 816", "آذربایجان · ۸۱۶"))
ev.append(caption(57.4, 61.8, "819", "۸۱۹"))
ev.append(caption(71.0, 75.4, "821", "۸۲۱"))
ev.append(caption(81.8, 84.8, "Bazz · 824", "بذ · ۸۲۴"))
ev.append(caption(93.9, 96.4, "Hashtadsar · June 829", "هشتادسر · ژوئن ۸۲۹"))
write(f"{OUT}/p03.ass", ev)
print(len(ev), "events")
