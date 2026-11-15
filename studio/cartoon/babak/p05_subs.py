"""Subtitles and place/year captions of part 5 -> build/babak/out/p05.ass (title/end cards and the header are overlays, see assemble.py)"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import series; series.from_folder(__file__)
from paths import OUT
from subs import sub_events, caption, write
from p05_audio import LINES
ev = sub_events(LINES)
ev.append(caption(0.4, 4.0, "Afshin's camp · 835", "اردوگاه افشین · ۸۳۵"))
ev.append(caption(31.0, 34.6, "Barzand · 835", "برزند · ۸۳۵"))
ev.append(caption(52.8, 56.6, "Bazz", "دژ بذ"))
write(f"{OUT}/p05.ass", ev)
print(len(ev), "events")
