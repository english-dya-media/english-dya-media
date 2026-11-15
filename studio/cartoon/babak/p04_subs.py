"""Subtitles and place/year captions of part 4 -> build/babak/out/p04.ass (title/end cards and the header are overlays, see assemble.py)"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import series; series.from_folder(__file__)
from paths import OUT
from subs import sub_events, caption, write
from p04_audio import LINES
ev = sub_events(LINES)
ev.append(caption(0.4, 3.2, "Hashtadsar · June 829", "هشتادسر · ژوئن ۸۲۹"))
ev.append(caption(26.0, 30.0, "Bazz · 829", "بذ · ۸۲۹"))
ev.append(caption(50.6, 54.4, "Byzantine frontier · 833", "مرز بیزانس · ۸۳۳"))
ev.append(caption(66.4, 70.6, "Baghdad · 835", "بغداد · ۸۳۵"))
ev.append(caption(89.8, 93.8, "Bazz · 835", "بذ · ۸۳۵"))
write(f"{OUT}/p04.ass", ev)
print(len(ev), "events")
