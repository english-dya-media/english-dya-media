"""Metricool items for Rostam & Sohrab parts (two a day: 18:00 and 20:00 Tehran).

python3 plan_parts.py <part> [<part> ...]   -> JSON list of {"date", "label", "info"} for createScheduledPost
Each part's entry in parts.json needs: title_fa, date (Tehran calendar day), slot ("18:00" or "20:00"),
media (branch/path), cover_ms, summary (lines), words ([emoji, english, pronunciation in Persian letters, meaning]).
"""
import json, os, sys
from datetime import datetime
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import youtube                  # every part also goes to YouTube as a Short, in the same Metricool post
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
    nxt = cfg["parts"].get(str(n + 1), {}).get("title_fa") or (cfg["titles"].get(str(n + 1)) or [None])[0]
    if nxt:
        when = "امشب ساعت ۸" if p.get("slot", "20:00") == "18:00" else "فردا ساعت ۶ عصر"
        lines.append(f"قسمت {str(n + 1).translate(FA)} «{nxt}» {when} 🌙")
        lines.append("فالو کن که بقیه‌ی داستانو از دست ندی 🤍")
    else:
        lines.append("پایان داستان رستم و سهراب 🤍 اگه دوست داشتی برای دوستت بفرست")
        when = "امشب ساعت ۸" if p.get("slot", "20:00") == "18:00" else "فردا ساعت ۶ عصر"
        lines.append(f"داستان بعدی: بابک خرمدین 🔥 قسمت اول {when}، فالو کن که از دستش ندی 🤍")
    lines += ["", cfg["hashtags"]]
    return "\n".join(lines)


def item(cfg, n):
    p = cfg["parts"][str(n)]
    hh, mm = map(int, p.get("slot", "20:00").split(":"))
    y, mo, d = map(int, p["date"].split("-"))
    t = datetime(y, mo, d, hh, mm, tzinfo=ZoneInfo("Asia/Tehran")).astimezone(ZoneInfo("Europe/Rome"))
    info = {"autoPublish": True, "descendants": [], "draft": False, "firstCommentText": "", "hasNotReadNotes": False,
            "media": [RAW + p["media"]], "mediaAltText": [], "providers": [{"network": "instagram"}, {"network": "youtube"}],
            "youtubeData": youtube.yt("rostam", p, True, n)[0],
            "publicationDate": {"dateTime": t.strftime("%Y-%m-%dT%H:%M:%S"), "timezone": "Europe/Rome"},
            "shortener": False, "smartLinkData": {"ids": []}, "text": caption(cfg, n),
            "videoCoverMilliseconds": p.get("cover_ms", 15000),
            "instagramData": {"type": "REEL", "collaborators": [], "isAiGenerated": True, "showReelOnFeed": True}}
    return {"date": t.isoformat(), "label": f"rostam part {n}", "info": json.dumps(info, ensure_ascii=False)}


if __name__ == "__main__":
    cfg = json.load(open(os.path.join(HERE, "parts.json"), encoding="utf-8"))
    json.dump([item(cfg, int(a)) for a in sys.argv[1:]], sys.stdout, ensure_ascii=False, indent=1)
