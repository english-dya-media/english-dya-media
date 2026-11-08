"""Daily growth log for @english_dya (+5,000 followers a month is the owner's goal).

The daily check copies what it pulled from Metricool into a JSON file and runs
    python3 growth/update.py build/today.json        (no argument: just print the report)
JSON: {"days":  [{"date": "2026-11-07", "followers": 64712, "gained": 7, "lost": 16, "reach": 457}, ...],
       "reels": [{"published_utc": "20261107173200", "url": "https://www.instagram.com/reel/.../", "tag": "day05",
                  "kind": "reel" | "trial" | "promo", "reach": 264, "views": 317, "likes": 1, "comments": 0, "saves": 0,
                  "shares": 0, "watch": 3.387, "view_rate": 22.3}, ...]}
Use null for a number Metricool didn't return; rows are upserted (same date / same url), nulls never overwrite a value.
"""
import calendar, csv, json, os, sys
from datetime import date, timedelta

HERE = os.path.dirname(os.path.abspath(__file__))
DAYS, REELS = os.path.join(HERE, "days.csv"), os.path.join(HERE, "reels.csv")
DCOLS = ["date", "followers", "gained", "lost", "reach"]
RCOLS = ["published_utc", "url", "tag", "kind", "reach", "views", "likes", "comments", "saves", "shares", "watch", "view_rate"]
GOAL = 5000


def load(path, key):
    return {r[key]: r for r in csv.DictReader(open(path))} if os.path.exists(path) else {}


def save(path, cols, rows, key):
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for r in sorted(rows.values(), key=key):
            w.writerow({c: r.get(c, "") for c in cols})


def num(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def upsert(table, key, rows):
    for r in rows:
        old = table.get(str(r[key]), {})
        old.update({k: v for k, v in r.items() if v is not None and v != ""})
        table[str(r[key])] = old


def report(days, reels):
    f = sorted((d, num(r["followers"])) for d, r in days.items() if num(r.get("followers")) is not None)
    if not f:
        return print("no follower data yet")
    last_d, last_f = f[-1]
    ld = date.fromisoformat(last_d)
    first_this = date(ld.year, ld.month, 1)
    prev = [x for x in f if date.fromisoformat(x[0]) < first_this]
    base_d, base_f = prev[-1] if prev else [x for x in f if date.fromisoformat(x[0]) >= first_this][0]
    mtd = last_f - base_f
    left = calendar.monthrange(ld.year, ld.month)[1] - ld.day
    week = [x for x in f if date.fromisoformat(x[0]) >= ld - timedelta(days=7)]
    pace = (week[-1][1] - week[0][1]) / max(1, (date.fromisoformat(week[-1][0]) - date.fromisoformat(week[0][0])).days) if len(week) > 1 else None
    print(f"followers {last_f:,.0f} on {last_d}" + (f" ({last_f - f[-2][1]:+,.0f} vs {f[-2][0]})" if len(f) > 1 else ""))
    print(f"{ld:%B}: {mtd:+,.0f} since {base_d} | goal +{GOAL:,} | needed from now: "
          f"{(GOAL - mtd) / max(1, left):+,.0f}/day for {left} days")
    if pace is not None:
        print(f"last 7 days: {pace:+.1f}/day -> month projection {mtd + pace * left:+,.0f}")
    gl = [(d, num(r.get("gained")), num(r.get("lost"))) for d, r in sorted(days.items())[-7:]]
    print("follows/unfollows:", ", ".join(f"{d[5:]} +{g:.0f}/-{l:.0f}" for d, g, l in gl if g is not None and l is not None))
    cut = (ld - timedelta(days=14)).strftime("%Y%m%d")
    rec = [r for r in reels.values() if r.get("published_utc", "") >= cut]
    rec.sort(key=lambda r: -(num(r.get("views")) or 0))
    if rec:
        print("reels, last 14 days (by views):")
        for r in rec:
            print(f"  {r['published_utc'][:8]} {r.get('tag', '?'):>9} {r.get('kind', '?'):<6} views {num(r.get('views')) or 0:>7,.0f}"
                  f"  reach {num(r.get('reach')) or 0:>7,.0f}  view-rate {num(r.get('view_rate')) or 0:4.1f}%"
                  f"  watch {num(r.get('watch')) or 0:4.1f}s  saves {num(r.get('saves')) or 0:3.0f}  shares {num(r.get('shares')) or 0:3.0f}")
        for kind in sorted({r.get("kind", "?") for r in rec}):
            k = [r for r in rec if r.get("kind") == kind]
            print(f"  avg {kind}: {sum(num(r.get('views')) or 0 for r in k) / len(k):,.0f} views over {len(k)}")


def main(path=None):
    days, reels = load(DAYS, "date"), load(REELS, "url")
    if path:
        new = json.load(open(path))
        upsert(days, "date", new.get("days", []))
        upsert(reels, "url", new.get("reels", []))
        save(DAYS, DCOLS, days, key=lambda r: r["date"])
        save(REELS, RCOLS, reels, key=lambda r: r.get("published_utc", ""))
    report(days, reels)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else None)
