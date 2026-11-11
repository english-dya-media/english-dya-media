"""Build the Metricool post list (reel + trial reels + quote reel + stories per day) for a range of days.

python3 plan.py <media base url> <first day> <last day> [--only reel|trial|quote|story] > build/plan.json
e.g. python3 plan.py https://raw.githubusercontent.com/english-dya-media/english-dya-media/media-2026-11-14/media 12 18

Each item: {"date": "<ISO with Rome offset>", "label": "...", "info": "<JSON string for createScheduledPost>"}
Slots in the content files are Tehran time; they are converted here, so daylight-saving changes in Italy are handled.
"""
import glob, json, os, sys
from datetime import datetime
from zoneinfo import ZoneInfo

HERE = os.path.dirname(os.path.abspath(__file__))
TEHRAN, BRAND_TZ = ZoneInfo("Asia/Tehran"), "Europe/Rome"
V2_FROM_DAY = 12          # daily reels from day 12 use the fast-opening layout (render.py v2, cover at 2.5 s)
TRIAL_COVER_MS = 3000
QUOTE_TAIL_MS = 600       # quote reels: cover near the end, when the Persian and the key words are on screen


def when(day_iso, hhmm):
    y, mo, d = map(int, day_iso.split("-"))
    h, mi = map(int, hhmm.split(":"))
    return datetime(y, mo, d, h, mi, tzinfo=TEHRAN).astimezone(ZoneInfo(BRAND_TZ))


def item(label, url, t, kind, text="", cover=1500, ai=None):
    # AI label: reels with the synthetic voice. Quote reels (graphics + music, no voice) are not labelled.
    ig = {"type": kind, "collaborators": [], "isAiGenerated": kind in ("REEL", "TRIAL_REEL") if ai is None else ai}
    info = {"autoPublish": True, "descendants": [], "draft": False, "firstCommentText": "", "hasNotReadNotes": False,
            "media": [url], "mediaAltText": [], "providers": [{"network": "instagram"}],
            "publicationDate": {"dateTime": t.strftime("%Y-%m-%dT%H:%M:%S"), "timezone": BRAND_TZ},
            "shortener": False, "smartLinkData": {"ids": []}, "text": text, "instagramData": ig}
    if kind in ("REEL", "TRIAL_REEL"):
        info["videoCoverMilliseconds"] = cover
        ig["showReelOnFeed"] = True
    return {"date": t.isoformat(), "label": label, "info": json.dumps(info, ensure_ascii=True)}


def main(base, first, last, only=None):
    base = base.rstrip("/")
    out = []
    for n in range(first, last + 1):
        d = json.load(open(os.path.join(HERE, "content", f"day{n:02d}.json")))
        tag = f"day{n:02d}"
        out.append(item(f"{tag} reel", f"{base}/{tag}_reel.mp4", when(d["date"], d.get("reel_slot", "21:00")), "REEL", d["caption"],
                        2500 if n >= V2_FROM_DAY else 1500))
        for k, s in enumerate(d["stories"]):
            out.append(item(f"{tag} story{k + 1} ({s['kind']})", f"{base}/{tag}_story{k + 1}.jpg", when(d["date"], s["slot"]), "STORY"))
        for tp in sorted(glob.glob(os.path.join(HERE, "content", f"trial{n:02d}*.json"))):
            t = json.load(open(tp))
            out.append(item(f"{tag} trial reel {t['tag']} ({t['kind']})", f"{base}/{t['tag']}.mp4", when(t["date"], t["slot"]), "TRIAL_REEL",
                            t["caption"], TRIAL_COVER_MS))
        qp = os.path.join(HERE, "content", f"quote{n:02d}.json")
        qv = os.path.join(HERE, "out", f"quote{n:02d}.mp4")
        if os.path.exists(qp):
            q = json.load(open(qp))
            dur = float(os.popen(f"ffprobe -v error -show_entries format=duration -of csv=p=0 {qv}").read() or 8) if os.path.exists(qv) else 8.0
            out.append(item(f"{tag} quote reel", f"{base}/quote{n:02d}.mp4", when(q["date"], q["slot"]), "REEL", q["caption"],
                            max(1000, int(dur * 1000) - QUOTE_TAIL_MS), ai=False))
    if only:
        out = [x for x in out if f" {only}" in x["label"] and (only != "reel" or "trial" not in x["label"])]
    out.sort(key=lambda x: x["date"])
    json.dump(out, sys.stdout, ensure_ascii=False, indent=0)


if __name__ == "__main__":
    a = sys.argv[1:]
    only = a[a.index("--only") + 1] if "--only" in a else None
    main(a[0], int(a[1]), int(a[2]), only)
