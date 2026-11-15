"""Build the Metricool post list for civil reels (one Instagram reel per day).

  python3 plan.py dates c004 c010 2026-11-20      # give c004..c010 consecutive dates from 2026-11-20 (only
                                                  #   files without a date; writes them back)
  python3 plan.py posts <media base url> c004 c010 > build/plan.json

<media base url> e.g. https://raw.githubusercontent.com/english-dya-media/english-dya-media/media-civil-2026-11-20/media
Each item: {"date": "<ISO, Rome offset>", "label": "c004 reel (site)", "info": "<JSON string for createScheduledPost>"}
Slots in the content files are Tehran time and are converted here (Italy's daylight saving is handled).
"""
import json, os, sys
from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo

HERE = os.path.dirname(os.path.abspath(__file__))
TEHRAN, BRAND_TZ = ZoneInfo("Asia/Tehran"), "Europe/Rome"


def tags(first, last):
    a, b = int(first[1:]), int(last[1:])
    return [f"c{n:03d}" for n in range(a, b + 1)]


def load(tag):
    return json.load(open(os.path.join(HERE, "content", f"{tag}.json"), encoding="utf-8"))


def when(day_iso, hhmm):
    y, mo, d = map(int, day_iso.split("-"))
    h, mi = map(int, hhmm.split(":"))
    return datetime(y, mo, d, h, mi, tzinfo=TEHRAN).astimezone(ZoneInfo(BRAND_TZ))


def dates(first, last, start):
    day = date.fromisoformat(start)
    for t in tags(first, last):
        p = os.path.join(HERE, "content", f"{t}.json")
        d = load(t)
        if not d.get("date"):
            d["date"] = day.isoformat()
            json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print(t, d["date"], d["slot"], d["kind"], d.get("topic", ""))
        day = date.fromisoformat(d["date"]) + timedelta(days=1)


def posts(base, first, last):
    base, out = base.rstrip("/"), []
    for t in tags(first, last):
        d = load(t)
        if not d.get("date"):
            raise SystemExit(f"{t} has no date: run `plan.py dates` first")
        when_ = when(d["date"], d["slot"])
        info = {"autoPublish": True, "descendants": [], "draft": False, "firstCommentText": "", "hasNotReadNotes": False,
                "media": [f"{base}/{t}.mp4"], "mediaAltText": [], "providers": [{"network": "instagram"}],
                "publicationDate": {"dateTime": when_.strftime("%Y-%m-%dT%H:%M:%S"), "timezone": BRAND_TZ},
                "shortener": False, "smartLinkData": {"ids": []}, "text": d["caption"],
                "videoCoverMilliseconds": int(d.get("cover", 1.6) * 1000),
                "instagramData": {"type": "REEL", "collaborators": [], "showReelOnFeed": True, "isAiGenerated": False}}
        out.append({"date": when_.isoformat(), "label": f"{t} reel ({d['kind']})", "info": json.dumps(info, ensure_ascii=True)})
    json.dump(out, sys.stdout, ensure_ascii=False, indent=0)


if __name__ == "__main__":
    a = sys.argv[1:]
    if a and a[0] == "dates":
        dates(a[1], a[2], a[3])
    elif a and a[0] == "posts":
        posts(a[1], a[2], a[3])
    else:
        raise SystemExit(__doc__)
