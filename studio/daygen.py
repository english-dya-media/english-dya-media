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


# Trial reels (Instagram "Trial Reel": shown to non-followers first; our main lever for new followers).
# Two a day from day 12 (Tehran time): "a" = vocab at 15:00, "b" = mistakes at 19:00. Rendered by trial_render.py.
TRIAL_SLOT = "19:00"
TRIAL_KINDS = {
    # 3 sentences Persian speakers get wrong: wrong -> right + a one-line why
    "mistakes": dict(n=3, headline=f"تو هم این{ZW}جوری می{ZW}گی؟", head_emoji="grimacing_face",
                     end1="هر روز انگلیسی یاد بگیر", end2="بدون اشتباه!", slot="19:00",
                     tags="#زبان_انگلیسی #آموزش_زبان_انگلیسی #گرامر_انگلیسی #اشتباهات_رایج #مکالمه_انگلیسی"),
    # 4 basic phrases -> the stronger word (very tired -> exhausted) + its Persian meaning
    "vocab": dict(n=4, headline=f"حرفه{ZW}ای{ZW}تر حرف بزن", head_emoji="smiling_face_with_sunglasses",
                  end1=f"هر روز کلمه{ZW}ی جدید یاد بگیر", end2=f"حرفه{ZW}ای{ZW}تر حرف بزن", slot="15:00",
                  tags="#زبان_انگلیسی #آموزش_زبان_انگلیسی #لغت_انگلیسی #یادگیری_زبان #مکالمه_انگلیسی"),
}


def used_trial_items(skip=None):
    out = set()
    for f in sorted(os.listdir(os.path.join(HERE, "content"))):
        if re.match(r"trial\d+[a-z]?\.json$", f) and f != skip:
            out |= {it["right"].lower() for it in json.load(open(os.path.join(HERE, "content", f)))["items"]}
    return out


def write_trial(day, kind, items, cap, suffix="", slot=None, headline=None, head_emoji=None):
    """content/trialNN<suffix>.json, one trial reel. cap = (line 1, line 2) of the caption; hashtags are added.
    From day 12: write_trial(N, "vocab", ..., suffix="a") and write_trial(N, "mistakes", ..., suffix="b")."""
    k = TRIAL_KINDS[kind]
    fn = f"trial{day:02d}{suffix}.json"
    seen, err = used_trial_items(skip=fn), []
    if len(items) != k["n"]: err.append(f"{kind} needs {k['n']} items")
    for it in items:
        for f in ("wrong", "right", "note", "emoji"):
            if not it.get(f): err.append(f"item missing {f}")
        if max(len(it.get("wrong", "")), len(it.get("right", ""))) > 22: err.append(f"'{it.get('wrong')}' / '{it.get('right')}': > 22 chars")
        if len(it.get("note", "")) > 36: err.append(f"note too long: {it.get('note')}")
        if it.get("right", "").lower() in seen: err.append(f"'{it['right']}' was already used in a trial reel")
    if err:
        raise SystemExit(f"trial{day:02d}: " + "; ".join(err))
    d = dict(tag=fn[:-5], kind=kind, day=day, date=day_date(day).isoformat(), slot=slot or k["slot"], handle=HANDLE,
             headline=headline or k["headline"], head_emoji=head_emoji or k["head_emoji"], end1=k["end1"], end2=k["end2"],
             items=items, caption=f"{cap[0]}\n{cap[1]}\n\n{k['tags']}")
    json.dump(d, open(os.path.join(HERE, "content", fn), "w"), ensure_ascii=False, indent=1)
    print(f"{d['tag']} {d['date']} {d['slot']} ({kind}): " + ", ".join(it["right"] for it in items))


# Quote reels: one a day at 23:00 Tehran (late-night scrolling). Rendered by quote_render.py.
QUOTE_SLOT = "23:00"
QUOTE_TAGS = "#جملات_انگلیسی #متن_انگلیسی_با_ترجمه #جملات_انگیزشی #زبان_انگلیسی #آموزش_زبان_انگلیسی #quotes"
QUOTE_CTA = f"هر شب یه جمله{ZW}ی انگلیسی با معنی 🤍 فالو کن"
PALETTES = ["night", "sunset", "mist", "dusk", "mono", "rose", "forest"]
# A different topic every day; the same topic may come back only after a week.
QUOTE_TOPICS = ["peace of mind", "trying again", "self-belief", "patience", "hard work", "friendship", "love",
                "family", "time", "kindness", "hope", "change", "happiness", "rest", "courage", "gratitude",
                "being alone", "dreams", "people", "letting go", "success", "mistakes", "the future", "honesty"]


def used_quotes(skip=None):
    out = set()
    for f in sorted(os.listdir(os.path.join(HERE, "content"))):
        if re.match(r"quote\d+\.json$", f) and f != skip:
            out.add(re.sub(r"[^a-z ]", "", json.load(open(os.path.join(HERE, "content", f)))["en"].lower()))
    return out


def recent_topics(day, back=6):
    out = {}
    for n in range(day - back, day):
        p = os.path.join(HERE, "content", f"quote{n:02d}.json")
        if os.path.exists(p):
            out[n] = json.load(open(p)).get("topic")
    return out


def write_quote(day, en, fa, words, share, topic, author=None, palette=None, figure=False, trees=False, sea=False):
    """content/quoteNN.json. words = [(english, persian), ...] (1-2 key words that appear in the quote);
    share = the caption's last line (a send/save prompt); topic = one of QUOTE_TOPICS, different every day."""
    fn = f"quote{day:02d}.json"
    err = []
    if topic not in QUOTE_TOPICS: err.append(f"topic '{topic}' is not in QUOTE_TOPICS")
    used = {n: t for n, t in recent_topics(day).items() if t == topic}
    if used: err.append(f"topic '{topic}' was used on day {min(used)}; pick another one")
    if len(en) > 110: err.append(f"quote longer than 110 characters ({len(en)})")
    if len(fa) > 120: err.append(f"Persian longer than 120 characters ({len(fa)})")
    if not 1 <= len(words) <= 2: err.append("give 1 or 2 key words")
    for w, m in words:
        if not re.search(r"\b" + re.escape(w) + r"\b", en, re.I): err.append(f"key word '{w}' is not in the quote")
        if len(w) + len(m) > 34: err.append(f"key word chip too long: {w} = {m}")
    if re.sub(r"[^a-z ]", "", en.lower()) in used_quotes(skip=fn): err.append("this quote was already used")
    if err:
        raise SystemExit(f"quote{day:02d}: " + "; ".join(err))
    pal = palette or PALETTES[day % len(PALETTES)]
    cap = f"“{en}”" + (f" — {author}" if author else "") + f"\n{fa}\n\n" + "\n".join(f"📌 {w} = {m}" for w, m in words)
    d = dict(tag=fn[:-5], day=day, date=day_date(day).isoformat(), slot=QUOTE_SLOT, handle=HANDLE, topic=topic, en=en, fa=fa, author=author,
             words=[dict(en=w, fa=m) for w, m in words], cta=QUOTE_CTA,
             scene=dict(palette=pal, seed=day * 7919 + 13, figure=figure, trees=trees or pal == "forest", sea=sea),
             caption=f"{cap}\n\n{share}\n{QUOTE_CTA}\n\n{QUOTE_TAGS}")
    json.dump(d, open(os.path.join(HERE, "content", fn), "w"), ensure_ascii=False, indent=1)
    print(f"{d['tag']} {d['date']} {d['slot']} [{topic}] ({pal}): {en}")


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
