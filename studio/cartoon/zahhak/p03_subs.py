"""Subtitles and place captions of part 3 -> build/zahhak/out/p03.ass (title/end cards and the header are overlays, see assemble.py)"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import series; series.from_folder(__file__)
from paths import OUT
from subs import sub_events, caption, write
from p03_audio import LINES
ev = sub_events(LINES)
ev.append(caption(72.6, 76.8, "Iran · King Jamshid's palace", "ایران · کاخ جمشید شاه"))
ev.append(caption(108.8, 112.8, "To the Arab lands", "به سوی سرزمین تازیان"))
write(f"{OUT}/p03.ass", ev)
print(len(ev), "events")
