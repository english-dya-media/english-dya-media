"""Subtitles and place captions of part 3 -> build/arash/out/p03.ass (title/end cards and the header are overlays, see assemble.py)"""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import series; series.from_folder(__file__)
from paths import OUT
from subs import sub_events, caption, write, ts
from p03_audio import LINES, S, END_CARD
TITLE = (S["s2"], S["s3"])


def off_cards(e):
    """end a subtitle before the title card or the end card begins"""
    m = re.match(r"(Dialogue: \d+,)(\d+):(\d+):([\d.]+),(\d+):(\d+):([\d.]+),(.*)", e)
    t0 = int(m[2]) * 3600 + int(m[3]) * 60 + float(m[4]); t1 = int(m[5]) * 3600 + int(m[6]) * 60 + float(m[7])
    for lim in (TITLE[0], END_CARD):
        if t0 < lim < t1:
            t1 = lim - 0.1
    return f"{m[1]}{ts(t0)},{ts(t1)},{m[8]}"


def split_line(lid, pieces):
    """replace the subtitle of one long line by several: pieces = [(start, end, english, persian)]"""
    from subs import SUB_Y, rtl
    out = []
    for t0, t1, en, fa in pieces:
        txt = "{\\an8\\pos(540,%d)\\fad(120,120)}" % SUB_Y + en + "\\N{\\fnVazirmatn Bold\\fs52\\c&H00CFE6F8&}" + rtl(fa)
        out.append(f"Dialogue: 0,{ts(t0)},{ts(t1)},Sub,,0,0,0,,{txt}")
    return out


ev = []
for (lid, t), e in zip(LINES, sub_events(LINES)):
    if lid == "p3s6d":           # the long Tirgan line in two pieces (the voice pauses after "water")
        ev += split_line(lid, [(t, t + 3.62, "Every year on Tirgan, people splash water…", "هر سال در جشنِ تیرگان، مردم آب می‌پاشند…"),
                               (t + 3.67, t + 5.65, "…and remember Arash.", "…و آرش را به یاد می‌آورند.")])
    else:
        ev.append(off_cards(e))
ev.append(caption(12.8, 16.6, "Mount Damavand · sunrise", "کوهِ دماوند · طلوعِ خورشید", y=330))
ev.append(caption(80.6, 85.0, "The Jeyhun River · Khorasan", "رودِ جیحون · خراسان", y=330))
ev.append(caption(123.3, 127.8, "Tirgan · the 13th day of Tir", "جشنِ تیرگان · سیزدهمِ تیرماه", y=330))
write(f"{OUT}/p03.ass", ev)
print(len(ev), "events")
