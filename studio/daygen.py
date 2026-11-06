"""Shared building blocks for daily vocab content. A week file (weeks/weekNN.py) imports this
and calls write_day() once per day; this writes content/dayNN.json in the format render.py reads.

Day N is published on DAY1 + (N-1) days (day 1 = Tue 3 Nov 2026). Times are Tehran time.
"""
import json, os, re
from datetime import date, timedelta

HERE = os.path.dirname(os.path.abspath(__file__))
ZW = "‌"
DAY1 = date(2026, 11, 3)
HANDLE = "@english_dya"

LABELS = {"wrong": "اشتباه رایج", "silent": "حرف {L} خونده نمیشه", "meaning": "معنی", "repeat": "با من تکرار کن"}
END = {"emoji": "thinking_face", "e1": f"تو کدومو اشتباه می{ZW}گفتی؟", "e2": "تو کامنت بنویس",
       "e3": f"برای لغت{ZW}های روزانه فالو کن"}
CTA1 = f"تو کدومشو اشتباه می{ZW}گفتی؟ تو کامنت بنویس 👇"
CTA2 = "سیو کن که یادت بمونه 📌"
TAGS = (f"#زبان_انگلیسی #آموزش_زبان_انگلیسی #لغت_انگلیسی #تلفظ_انگلیسی #یادگیری_زبان #لغت_روز "
        f"#زبان_انگلیسی_آسان")

REEL_SLOT = "21:00"
RECALL = dict(kind="recall", kicker="از ریلز دیروز", kicker_emoji="brain", emoji="thinking_face", title="یادته؟",
              q="معنی این کلمه چیه؟", hint="بدون نگاه کردن به ریلز!", cta="معنیشو ریپلای کن", slot="10:00")
QUIZ = dict(kind="quiz", kicker=f"تست ۵ ثانیه{ZW}ای", kicker_emoji="stopwatch",
            q="کدوم حرف این کلمه\nخونده نمیشه؟", hint="راهنما: فقط یه حرف!", cta="جوابتو ریپلای کن", slot="13:00")
MCQ = dict(kind="mcq", kicker="از ریلز دیروز", kicker_emoji="brain", q="یعنی چی؟",
           hint="فقط حرفشو بفرست: الف، ب یا ج", cta="جوابتو ریپلای کن", slot="17:00")
ASK = dict(kind="ask", emoji="speech_balloon", example_label="مثلاً:", cta="ریپلای کن", slot="22:00")


def SIL(letter):
    """A silent letter: struck through in red."""
    return dict(tip="حرف {EN} خونده نمیشه", tip_en=letter)


def GLOW(tip, tip_en, tip_emoji="light_bulb"):
    """Highlighted letters (stress, vowel, ending), glowing yellow."""
    return dict(mark_style="glow", tip=tip, tip_en=tip_en, tip_emoji=tip_emoji)


def day_date(n):
    return DAY1 + timedelta(days=n - 1)


def load_day(n):
    p = os.path.join(HERE, "content", f"day{n:02d}.json")
    return json.load(open(p)) if os.path.exists(p) else None


def used_words():
    out = set()
    for f in sorted(os.listdir(os.path.join(HERE, "content"))):
        if re.match(r"day\d+\.json$", f):
            d = json.load(open(os.path.join(HERE, "content", f)))
            out |= {w["en"].lower() for w in d["words"]}
            out |= {s["word"].lower() for s in d["stories"] if s["kind"] == "quiz"}
    return out


def check(d, prev):
    """Catch mistakes before anything is rendered."""
    err = []
    h = d["hook"]
    if len(h["l2a"] + h["l2b"]) > 15: err.append(f"hook line 2 too long ({len(h['l2a'] + h['l2b'])} > 15 chars)")
    if len(h["l1"]) > 18: err.append("hook line 1 too long")
    if len(d["words"]) != 4: err.append("need exactly 4 words")
    for w in d["words"]:
        marks = w.get("mark", w.get("silent", []))
        if not marks or max(marks) >= len(w["en"]): err.append(f"{w['en']}: bad mark indices")
        if w.get("mark_style") != "glow" and "tip_en" in w and len(w["tip_en"]) == 1 and len(marks) == 1:
            if w["en"][marks[0]].lower() != w["tip_en"].lower():
                err.append(f"{w['en']}: marked letter '{w['en'][marks[0]]}' != tip '{w['tip_en']}'")
        if len(w["en"]) > 12: err.append(f"{w['en']}: longer than 12 letters")
        if len(w["fa"]) > 18: err.append(f"{w['en']}: meaning too long")
        for k in ("emoji", "ipa", "wrong", "right", "fa", "uni", "tts"):
            if not w.get(k): err.append(f"{w['en']}: missing {k}")
    kinds = [s["kind"] for s in d["stories"]]
    for s in d["stories"]:
        if s["kind"] in ("recall", "mcq") and prev:
            if s["word"].lower() not in {w["en"].lower() for w in prev["words"]}:
                err.append(f"{s['kind']} word '{s['word']}' is not from the previous day's reel")
        if s["kind"] == "mcq":
            if len(s["options"]) != 3 or not 0 <= s["answer"] < 3: err.append("mcq needs 3 options and an answer index")
        if s["kind"] == "quiz" and "answer" in s and len(s["answer"]) == 1 and s["answer"].lower() not in s["word"].lower():
            err.append(f"quiz answer '{s['answer']}' not in '{s['word']}'")
        if s["kind"] == "ask" and len(s["t2a"] + s["t2b"]) > 20: err.append("ask line 2 too long")
    if prev and kinds != ["recall", "quiz", "mcq", "ask"]: err.append(f"stories should be recall, quiz, mcq, ask (got {kinds})")
    return err


def write_day(day, hook, words, cap, stories):
    for w in words:
        w.setdefault("tts", w["en"])
    lines = [cap[0], cap[1], ""] + [f"{w['uni']} {w['en']} = {w['right']} ({w['fa']})" for w in words] + \
            ["", CTA1, CTA2, "", TAGS]
    d = dict(day=day, date=day_date(day).isoformat(), handle=HANDLE, labels=LABELS, end=END, hook=hook,
             words=words, stories=stories, reel_slot=REEL_SLOT, caption="\n".join(lines))
    prev = load_day(day - 1)
    errs = check(d, prev)
    if errs:
        raise SystemExit(f"day{day:02d}: " + "; ".join(errs))
    json.dump(d, open(os.path.join(HERE, "content", f"day{day:02d}.json"), "w"), ensure_ascii=False, indent=1)
    print(f"day{day:02d} {d['date']}: " + ", ".join(w["en"] for w in words) + "  | stories: " +
          ", ".join(s.get("word", s.get("example", "")) for s in stories))
