"""YouTube Shorts versions of our Instagram videos (owner's request, 14 Nov 2026: everything posted on Instagram
also goes to YouTube; stories can't, they are images). The channel is connected to the same Metricool brand.

yt(kind, content, ai) -> (youtubeData dict, description suffix) used by plan.py and rostam/plan_parts.py.
kind: "reel" (dayNN.json), "trial" (trialNN.json), "quote" (quoteNN.json), "rostam" (parts.json entry + number),
"promo" (dict with "title").
"""
FA = str.maketrans("0123456789", "۰۱۲۳۴۵۶۷۸۹")
BASE_TAGS = ["english", "learn english", "english vocabulary", "english pronunciation", "زبان انگلیسی",
             "آموزش زبان انگلیسی", "لغت انگلیسی", "تلفظ انگلیسی", "یادگیری زبان انگلیسی", "shorts"]
KIND_TAGS = {
    "quote": ["english quotes", "جملات انگلیسی", "متن انگلیسی با ترجمه", "جملات انگیزشی", "quotes"],
    "trial": ["مکالمه انگلیسی", "اشتباهات رایج انگلیسی", "english mistakes", "speak english"],
    "rostam": ["رستم و سهراب", "شاهنامه", "فردوسی", "Shahnameh", "Rostam and Sohrab", "Ferdowsi", "انیمیشن"],
}
DESC_TAIL = "\n\n📲 اینستاگرام: @english_dya"


def _fit(head, extra, tail=" #shorts", limit=100):
    """head + ' | ' + as many extras as fit + tail, at most `limit` characters."""
    t, used = head, []
    for e in extra:
        cand = f"{head} | {', '.join(used + [e])}"
        if len(cand) + len(tail) <= limit:
            used.append(e)
            t = cand
    if len(t) + len(tail) > limit:
        t = t[: limit - len(tail) - 1].rstrip() + "…"
    return t + tail


def title(kind, c, n=None):
    first = c.get("caption", "").split("\n")[0].strip() if isinstance(c, dict) else ""
    if kind == "reel":
        return _fit(first, [w["en"] for w in c["words"]])
    if kind == "trial":
        return _fit(first, [it["right"].rstrip(".!") for it in c["items"]])
    if kind == "quote":
        q = c["en"] + (f" — {c['author']}" if c.get("author") else "")
        return _fit(q + " 🤍", [])
    if kind == "rostam":
        return _fit(f"رستم و سهراب، قسمت {str(n).translate(FA)}: {c['title_fa']} 🎬", ["Shahnameh in English"])
    return _fit(c["title"], [])


def tags(kind, c):
    t = BASE_TAGS + KIND_TAGS.get(kind, [])
    if kind == "reel":
        t += [w["en"] for w in c["words"]]
    elif kind == "trial":
        t += [it["right"].rstrip(".") for it in c["items"]]
    elif kind == "rostam":
        t += [w[1] for w in c.get("words", [])]
    out, total = [], 0
    for x in dict.fromkeys(t):                       # YouTube allows 500 characters of tags in all
        if total + len(x) + 1 > 480:
            break
        out.append(x)
        total += len(x) + 1
    return out


def desc(text):
    """The Instagram caption, worded for YouTube: subscribe instead of follow, plus a pointer to the Instagram page."""
    return text.replace("فالو کن", "سابسکرایب کن") + DESC_TAIL


def yt(kind, c, ai, n=None):
    data = {"title": title(kind, c, n), "type": "short", "privacy": "public", "tags": tags(kind, c),
            "category": "EDUCATION", "madeForKids": False, "isAiGeneratedContent": bool(ai)}
    return data, DESC_TAIL
