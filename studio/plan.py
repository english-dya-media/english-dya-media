"""Build the Metricool post list (reel + stories per day) for a range of days.

python3 plan.py <media base url> <first day> <last day> > build/plan.json
e.g. python3 plan.py https://raw.githubusercontent.com/english-dya-media/english-dya-media/media-2026-11-07/media 5 11

Each item: {"date": "<ISO with Rome offset>", "label": "...", "info": "<JSON string for createScheduledPost>"}
Slots in the content files are Tehran time; they are converted here, so daylight-saving changes in Italy are handled.
"""
import json, os, sys
from datetime import datetime
from zoneinfo import ZoneInfo

HERE = os.path.dirname(os.path.abspath(__file__))
TEHRAN, BRAND_TZ = ZoneInfo("Asia/Tehran"), "Europe/Rome"


def when(day_iso, hhmm):
    y, mo, d = map(int, day_iso.split("-"))
    h, mi = map(int, hhmm.split(":"))
    return datetime(y, mo, d, h, mi, tzinfo=TEHRAN).astimezone(ZoneInfo(BRAND_TZ))


def item(label, url, t, kind, text=""):
    ig = {"type": kind, "collaborators": [], "isAiGenerated": kind == "REEL"}
    info = {"autoPublish": True, "descendants": [], "draft": False, "firstCommentText": "", "hasNotReadNotes": False,
            "media": [url], "mediaAltText": [], "providers": [{"network": "instagram"}],
            "publicationDate": {"dateTime": t.strftime("%Y-%m-%dT%H:%M:%S"), "timezone": BRAND_TZ},
            "shortener": False, "smartLinkData": {"ids": []}, "text": text, "instagramData": ig}
    if kind == "REEL":
        info["videoCoverMilliseconds"] = 1500
        ig["showReelOnFeed"] = True
    return {"date": t.isoformat(), "label": label, "info": json.dumps(info, ensure_ascii=True)}


def main(base, first, last):
    base = base.rstrip("/")
    out = []
    for n in range(first, last + 1):
        d = json.load(open(os.path.join(HERE, "content", f"day{n:02d}.json")))
        tag = f"day{n:02d}"
        out.append(item(f"{tag} reel", f"{base}/{tag}_reel.mp4", when(d["date"], d.get("reel_slot", "21:00")), "REEL", d["caption"]))
        for k, s in enumerate(d["stories"]):
            out.append(item(f"{tag} story{k + 1} ({s['kind']})", f"{base}/{tag}_story{k + 1}.jpg", when(d["date"], s["slot"]), "STORY"))
    out.sort(key=lambda x: x["date"])
    json.dump(out, sys.stdout, ensure_ascii=False, indent=0)


if __name__ == "__main__":
    main(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))
