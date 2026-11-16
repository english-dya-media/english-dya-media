"""Subtitles and place/year captions of part 7 -> build/babak/out/p07.ass (title/end cards and the header are overlays, see assemble.py)"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import series; series.from_folder(__file__)
from paths import OUT
from subs import sub_events, caption, write
from p07_audio import LINES
ev = sub_events(LINES)
ev.append(caption(0.4, 4.6, "Sahl's castle · Armenia", "قلعه‌ی سهل · ارمنستان"))
ev.append(caption(19.0, 23.4, "15 September 837", "۱۵ سپتامبر ۸۳۷"))
ev.append(caption(62.1, 66.3, "Samarra · 4 January 838", "سامرا · ۴ ژانویه ۸۳۸"))
write(f"{OUT}/p07.ass", ev)
print(len(ev), "events")
