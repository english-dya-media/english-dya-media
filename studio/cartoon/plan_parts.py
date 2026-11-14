"""Captions, slots and Metricool items for the cartoon story series (two parts a day, 18:00 and 20:00 Tehran,
series after series in the order of queue.json, starting after Rostam & Sohrab's last part).

python3 plan_parts.py status                          -> every series: parts made / scheduled, what comes next
python3 plan_parts.py <series> <part> [<part> …]      -> JSON list of {"date", "label", "info"} for createScheduledPost
python3 plan_parts.py slots "<YYYY-MM-DD HH:MM>" <n>  -> the next n Tehran slots after that Tehran time (never < 2 h from now)
A part's entry in <series>/parts.json needs: title_fa, date (Tehran day), slot ("18:00"/"20:00"), media (branch/path),
cover_ms, summary (2 lines), words ([emoji, english, pronunciation in Persian letters, meaning]); optional episode/source.
"""
import json, os, sys
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import series

RAW = "https://raw.githubusercontent.com/english-dya-media/english-dya-media/"
FA = str.maketrans("0123456789", "۰۱۲۳۴۵۶۷۸۹")
TEH, ROME = ZoneInfo("Asia/Tehran"), ZoneInfo("Europe/Rome")
SLOTS = ("18:00", "20:00")


def next_series(name):
    q = series.queue()["order"]
    i = q.index(name)
    return series.config(q[i + 1]) if i + 1 < len(q) else None


def caption(name, cfg, n):
    p = cfg["parts"][str(n)]
    lines = [f"🎬 قسمت {str(n).translate(FA)} از داستان {cfg['series_fa']} | {p['title_fa']}", ""]
    lines += p["summary"] + ["", "📚 لغت‌های این قسمت:"]
    lines += [f"{e} {en} = {pr} ({fa})" for e, en, pr, fa in p["words"]]
    src = p.get("source") or cfg.get("sources", {}).get(str(p.get("episode", ""))) or cfg["source"]
    lines += ["", src, ""]
    when = "امشب ساعت ۸" if p.get("slot", "20:00") == "18:00" else "فردا ساعت ۶ عصر"
    nxt = (cfg["titles"].get(str(n + 1)) or [None])[0]
    if nxt:
        lines.append(f"قسمت {str(n + 1).translate(FA)} «{nxt}» {when} 🌙")
        lines.append("فالو کن که بقیه‌ی داستانو از دست ندی 🤍")
    else:
        lines.append(f"پایان داستان {cfg['series_fa']} 🤍 اگه دوست داشتی برای دوستت بفرست")
        ns = next_series(name)
        if ns:
            lines.append(f"داستان بعدی: {ns['series_fa']} 🔥 قسمت اول {when}، فالو کن که از دستش ندی 🤍")
        else:
            lines.append("برای داستان‌های بعدی فالو کن 🤍")
    lines += ["", cfg["hashtags"]]
    return "\n".join(lines)


def item(name, cfg, n):
    p = cfg["parts"].get(str(n)) or {}
    if not (p.get("media") and p.get("date") and p.get("slot")):
        raise SystemExit(f"{name} part {n}: needs media, date and slot in {name}/parts.json first "
                         "(free slots: python3 plan_parts.py slots …)")
    hh, mm = map(int, p["slot"].split(":"))
    y, mo, d = map(int, p["date"].split("-"))
    t = datetime(y, mo, d, hh, mm, tzinfo=TEH).astimezone(ROME)
    info = {"autoPublish": True, "descendants": [], "draft": False, "firstCommentText": "", "hasNotReadNotes": False,
            "media": [RAW + p["media"]], "mediaAltText": [], "providers": [{"network": "instagram"}],
            "publicationDate": {"dateTime": t.strftime("%Y-%m-%dT%H:%M:%S"), "timezone": "Europe/Rome"},
            "shortener": False, "smartLinkData": {"ids": []}, "text": caption(name, cfg, n),
            "videoCoverMilliseconds": p.get("cover_ms", 15000),
            "instagramData": {"type": "REEL", "collaborators": [], "isAiGenerated": True, "showReelOnFeed": True}}
    return {"date": t.isoformat(), "label": f"{name} part {n}", "info": json.dumps(info, ensure_ascii=False)}


def slots(after, count):
    """next Tehran slots strictly after `after` (Tehran wall time), at least 2 h from now"""
    a = datetime.strptime(after, "%Y-%m-%d %H:%M").replace(tzinfo=TEH)
    soon = datetime.now(TEH) + timedelta(hours=2)
    out, day = [], a.date()
    while len(out) < count:
        for s in SLOTS:
            hh, mm = map(int, s.split(":"))
            t = datetime(day.year, day.month, day.day, hh, mm, tzinfo=TEH)
            if t > a and t >= soon and len(out) < count:
                out.append({"date": day.isoformat(), "slot": s, "rome": t.astimezone(ROME).strftime("%Y-%m-%d %H:%M")})
        day += timedelta(days=1)
    return out


def status():
    rows, to_make, to_sched = [], None, None
    for name in series.queue()["order"]:
        c = series.config(name)
        total = len(c["titles"])
        made = [int(k) for k, v in c["parts"].items() if v.get("media")]
        sched = [int(k) for k, v in c["parts"].items() if v.get("date")]
        last = max(sched) if sched else 0
        rows.append({"series": name, "parts": total, "made": sorted(made), "scheduled": sorted(sched),
                     "last_slot": (lambda p: f"{p['date']} {p['slot']}" if p else None)(c["parts"].get(str(last)))})
        nm = next((k for k in range(1, total + 1) if k not in made), None)
        if to_make is None and nm:
            to_make = {"series": name, "part": nm}
        ns = next((k for k in range(1, total + 1) if k not in sched), None)
        if to_sched is None and ns:
            to_sched = {"series": name, "part": ns, "made": ns in made}
    return {"series": rows, "next_to_make": to_make, "next_to_schedule": to_sched}


if __name__ == "__main__":
    if sys.argv[1] == "slots":
        json.dump(slots(sys.argv[2], int(sys.argv[3])), sys.stdout, indent=1)
    elif sys.argv[1] == "status":
        json.dump(status(), sys.stdout, ensure_ascii=False, indent=1)
    else:
        name = sys.argv[1]
        cfg = series.config(name)
        json.dump([item(name, cfg, int(a)) for a in sys.argv[2:]], sys.stdout, ensure_ascii=False, indent=1)
