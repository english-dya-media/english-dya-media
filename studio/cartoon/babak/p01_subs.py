"""Subtitles and place captions of part 1 -> build/out/p01.ass (title/end cards and the header are overlays, see assemble.py)"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import series; series.from_folder(__file__)
from paths import OUT
from subs import sub_events, caption, write
from p01_audio import LINES
ev = sub_events(LINES)
ev.append(caption(0.8, 3.25, "Samarra · 838", "سامرا · ۸۳۸"))
ev.append(caption(22.0, 27.0, "Belalabad, Azerbaijan · c. 805", "بلال‌آباد، آذربایجان · حدود ۸۰۵"))
ev.append(caption(89.6, 93.6, "Tabriz", "تبریز"))
write(f"{OUT}/p01.ass", ev)
print(len(ev), "events")
