"""Metricool items for Rostam & Sohrab parts (one a day at 20:00 Tehran).

python3 plan_parts.py <part> [<part> ...]   -> JSON list of {"date", "label", "info"} for createScheduledPost
Each part's entry in parts.json needs: title_fa, date (Tehran calendar day), media (branch/path), cover_ms,
summary (lines), words ([emoji, english, pronunciation in Persian letters, meaning]).
"""
import json, os, sys
from datetime import datetime
from zoneinfo import ZoneInfo

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = "https://raw.githubusercontent.com/english-dya-media/english-dya-media/"
FA = str.maketrans("0123456789", "۰۱۲۳۴۵۶۷۸۹")


def caption(cfg, n):
    p = cfg["parts"][str(n)]
    lines = [f"🎬 قسمت {str(n).translate(FA)} از داستان رستم و سهراب | {p['title_fa']}", ""]
    lines += p["summary"] + ["", "📚 لغت‌های این قسمت:"]
    lines += [f"{e} {en} = {pr} ({fa})" for e, en, pr, fa in p["words"]]
    lines += ["", cfg["source"], ""]
    nxt = cfg["titles"].get(str(n + 1)) or (cfg["parts"].get(str(n + 1), {}).get("title_fa"),)
    if nxt and nxt[0]:
        lines.append(f"قسمت {str(n + 1).translate(FA)} «{nxt[0]}» فردا ساعت ۸ شب 🌙")
        lines.append("فالو کن که بقیه‌ی داستانو از دست ندی 🤍")
    else:
        lines.append("پایان داستان رستم و سهراب 🤍 اگه دوست داشتی برای دوستت بفرست")
    lines += ["", cfg["hashtags"]]
    return "\n".join(lines)


def item(cfg, n):
    p = cfg["parts"][str(n)]
    hh, mm = map(int, cfg["slot_tehran"].split(":"))
    y, mo, d = map(int, p["date"].split("-"))
    t = datetime(y, mo, d, hh, mm, tzinfo=ZoneInfo("Asia/Tehran")).astimezone(ZoneInfo("Europe/Rome"))
    info = {"autoPublish": True, "descendants": [], "draft": False, "firstCommentText": "", "hasNotReadNotes": False,
            "media": [RAW + p["media"]], "mediaAltText": [], "providers": [{"network": "instagram"}],
            "publicationDate": {"dateTime": t.strftime("%Y-%m-%dT%H:%M:%S"), "timezone": "Europe/Rome"},
            "shortener": False, "smartLinkData": {"ids": []}, "text": caption(cfg, n),
            "videoCoverMilliseconds": p.get("cover_ms", 15000),
            "instagramData": {"type": "REEL", "collaborators": [], "isAiGenerated": True, "showReelOnFeed": True}}
    return {"date": t.isoformat(), "label": f"rostam part {n}", "info": json.dumps(info, ensure_ascii=False)}


if __name__ == "__main__":
    cfg = json.load(open(os.path.join(HERE, "parts.json"), encoding="utf-8"))
    json.dump([item(cfg, int(a)) for a in sys.argv[1:]], sys.stdout, ensure_ascii=False, indent=1)
