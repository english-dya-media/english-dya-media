"""Subtitles and place captions of part 5 -> build/leyli/out/p05.ass (title/end cards and the header are overlays, see assemble.py)"""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import series; series.from_folder(__file__)
from paths import OUT
from subs import sub_events, caption, write, ts, SUB_Y, rtl
from p05_audio import LINES, S, END_CARD
TITLE = (S["s2"], S["s3"])


def off_cards(e):
    """end a subtitle before the title card or the end card begins"""
    m = re.match(r"(Dialogue: \d+,)(\d+):(\d+):([\d.]+),(\d+):(\d+):([\d.]+),(.*)", e)
    t0 = int(m[2]) * 3600 + int(m[3]) * 60 + float(m[4]); t1 = int(m[5]) * 3600 + int(m[6]) * 60 + float(m[7])
    for lim in (TITLE[0], END_CARD):
        if t0 < lim < t1:
            t1 = lim - 0.1
    return f"{m[1]}{ts(t0)},{ts(t1)},{m[8]}"


def split_line(pieces):
    """the subtitle of one long line as several: pieces = [(start, end, english, persian)]"""
    out = []
    for t0, t1, en, fa in pieces:
        txt = "{\\an8\\pos(540,%d)\\fad(120,120)}" % SUB_Y + en + "\\N{\\fnVazirmatn Bold\\fs52\\c&H00CFE6F8&}" + rtl(fa)
        out.append(f"Dialogue: 0,{ts(t0)},{ts(t1)},Sub,,0,0,0,,{txt}")
    return out


ev = []
for (lid, t), e in zip(LINES, sub_events(LINES)):
    if lid == "p5s6a":           # the long line in two pieces (the voice pauses after "hunter")
        ev += split_line([(t, t + 2.6, "Back in the desert, Majnun met a hunter.", "در بیابان، مجنون به شکارچی‌ای رسید."),
                          (t + 2.65, t + 5.15, "A gazelle was caught in his trap.", "آهویی در دامش افتاده بود.")])
    else:
        ev.append(off_cards(e))
ev.append(caption(11.8, 15.8, "The desert of Najd", "بیابانِ نجد", y=330))
ev.append(caption(59.0, 62.9, "The camp of the Banu Amir", "اردوگاهِ بنی‌عامر", y=330))
write(f"{OUT}/p05.ass", ev)
print(len(ev), "events")
