"""Subtitles and place captions of part 4 -> build/zahhak/out/p04.ass (title/end cards and the header are overlays, see assemble.py)"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import series; series.from_folder(__file__)
from paths import OUT
from subs import sub_events, caption, write
from p04_audio import LINES
ev = sub_events(LINES)
ev.append(caption(12.6, 16.6, "A thousand years of Zahhak", "هزار سال پادشاهی ضحاک", y=330))
ev.append(caption(93.0, 97.0, "The far mountains", "کوه‌های دوردست"))
write(f"{OUT}/p04.ass", ev)
print(len(ev), "events")
