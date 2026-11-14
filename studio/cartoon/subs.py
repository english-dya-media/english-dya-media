import json, sys
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paths import VOICES_DIR
from lines import LINES
DUR = json.load(open(f'{VOICES_DIR}/durations.json'))
TEXT = {l[0]: (l[4], l[5]) for l in LINES}

HEAD = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 0
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Sub,Vazirmatn Medium,46,&H00FFFFFF,&H00FFFFFF,&H00000000,&H64000000,0,0,0,0,100,100,0,0,1,3.2,1.2,8,90,90,0,1
Style: Cap,Cinzel,40,&H00E6F0F6,&H00FFFFFF,&H00000000,&H64000000,0,0,0,0,100,100,2,0,1,2.4,0.8,8,80,80,0,1
Style: Title,Cinzel,150,&H005EB2D9,&H00FFFFFF,&H00100808,&H64000000,1,0,0,0,100,100,12,0,1,3,2,5,60,60,0,1
Style: CTA,Vazirmatn Bold,62,&H00FFFFFF,&H00FFFFFF,&H00000000,&H64000000,1,0,0,0,100,100,0,0,1,3.5,1.5,5,60,60,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

SUB_Y = 1040
RLM = "\u200f"
def rtl(s):
    return RLM + s + RLM

def ts(t):
    h = int(t // 3600); m = int(t % 3600 // 60); s = t % 60
    return f"{h}:{m:02d}:{s:05.2f}"

def sub_events(lines):
    ev = []
    for i, (lid, t) in enumerate(lines):
        end = t + DUR[lid] + 0.45
        if i + 1 < len(lines):
            end = min(end, lines[i + 1][1] - 0.05)
        en, fa = TEXT[lid]
        txt = "{\\an8\\pos(540,%d)\\fad(120,120)}" % SUB_Y + en + "\\N{\\fnVazirmatn Bold\\fs52\\c&H00CFE6F8&}" + rtl(fa)
        ev.append(f"Dialogue: 0,{ts(t)},{ts(end)},Sub,,0,0,0,,{txt}")
    return ev

def caption(t0, t1, en, fa, y=330):
    txt = "{\\an8\\pos(540,%d)\\fad(500,500)}" % y + en + "\\N{\\fnVazirmatn Medium\\fs44\\fsp0}" + rtl(fa)
    return f"Dialogue: 1,{ts(t0)},{ts(t1)},Cap,,0,0,0,,{txt}"

def title(t0, t1, ep_en, ep_fa):
    a = "{\\an5\\pos(540,760)\\fad(600,600)}BABAK"
    b = "{\\an5\\pos(540,900)\\fad(800,600)\\fs44\\b0\\fsp4\\c&H00E6F0F6&}" + ep_en
    c = "{\\an5\\pos(540,975)\\fad(900,600)\\fnVazirmatn Bold\\fs54\\fsp0\\b1\\c&H00CFE6F8&}" + rtl(ep_fa)
    return [f"Dialogue: 2,{ts(t0)},{ts(t1)},Title,,0,0,0,,{a}", f"Dialogue: 2,{ts(t0)},{ts(t1)},Title,,0,0,0,,{b}",
            f"Dialogue: 2,{ts(t0)},{ts(t1)},Title,,0,0,0,,{c}"]

def cta(t0, t1, en="Follow to see the rest", fa="برای دیدن ادامه، فالو کن", nxt=None, y0=640):
    ev = [f"Dialogue: 3,{ts(t0)},{ts(t1)},CTA,,0,0,0,,{{\\an5\\pos(540,{y0})\\fad(300,0)}}{en}",
          f"Dialogue: 3,{ts(t0)},{ts(t1)},CTA,,0,0,0,,{{\\an5\\pos(540,{y0+90})\\fad(300,0)\\fs58}}{rtl(fa)}",
          f"Dialogue: 3,{ts(t0)},{ts(t1)},CTA,,0,0,0,,{{\\an5\\pos(540,{y0+180})\\fad(300,0)\\fs46\\c&H005EB2D9&}}@english_dya"]
    if nxt:
        ev.append(f"Dialogue: 3,{ts(t0)},{ts(t1)},Cap,,0,0,0,,{{\\an5\\pos(540,{y0+300})\\fad(300,0)}}{nxt[0]}\\N{{\\fnVazirmatn Medium\\fs40\\fsp0}}{rtl(nxt[1])}")
    return ev

def label(t0, t1, en, fa):
    return f"Dialogue: 1,{ts(t0)},{ts(t1)},Cap,,0,0,0,,{{\\an8\\pos(540,330)\\fad(300,400)}}{en}\\N{{\\fnVazirmatn Medium\\fs44\\fsp0}}{rtl(fa)}"

def write(path, events):
    open(path, "w", encoding="utf-8").write(HEAD + "\n".join(events) + "\n")
