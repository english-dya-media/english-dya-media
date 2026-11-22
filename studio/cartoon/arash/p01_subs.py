"""Subtitles and place captions of part 1 -> build/arash/out/p01.ass (title/end cards and the header are overlays, see assemble.py)"""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import series; series.from_folder(__file__)
from paths import OUT
from subs import sub_events, caption, write, ts
from p01_audio import LINES, S, END_CARD
TITLE = (S["s2"], S["s3"])


def off_cards(e):
    """end a subtitle before the title card or the end card begins"""
    m = re.match(r"(Dialogue: \d+,)(\d+):(\d+):([\d.]+),(\d+):(\d+):([\d.]+),(.*)", e)
    t0 = int(m[2]) * 3600 + int(m[3]) * 60 + float(m[4]); t1 = int(m[5]) * 3600 + int(m[6]) * 60 + float(m[7])
    for lim in (TITLE[0], END_CARD):
        if t0 < lim < t1:
            t1 = lim - 0.1
    return f"{m[1]}{ts(t0)},{ts(t1)},{m[8]}"


ev = [off_cards(e) for e in sub_events(LINES)]
ev.append(caption(12.6, 17.0, "Tabaristan · northern Iran", "تبرستان · مازندرانِ امروز", y=330))
ev.append(caption(57.6, 61.4, "The camp of Turan", "اردوی توران", y=330))
write(f"{OUT}/p01.ass", ev)
print(len(ev), "events")
