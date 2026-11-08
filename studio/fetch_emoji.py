"""Download the Fluent 3D emoji images (MIT licence, github.com/microsoft/fluentui-emoji) that the
content files need, into assets/emoji/<key>.png. A key is the Fluent file stem, e.g. "money_with_wings".

python3 fetch_emoji.py            # everything referenced by content/day*.json, content/trial*.json + renderer basics
python3 fetch_emoji.py ewe crown  # specific keys
Exit code 1 if any key could not be found (pick another emoji for it).
"""
import glob, json, os, sys, urllib.parse, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "assets", "emoji")
BASE_URL = "https://raw.githubusercontent.com/microsoft/fluentui-emoji/main/assets/"
# folders whose capitalisation can't be derived from the key
SPECIAL = {}  # the folder is normally the key with spaces and a capital first letter ("Dna", "Globe showing europe-africa")
BASICS = ["check_mark_button", "cross_mark", "speaker_high_volume", "shushing_face", "light_bulb",
          "backhand_index_pointing_down", "sparkles", "thinking_face", "brain", "stopwatch", "speech_balloon",
          "grimacing_face", "smiling_face_with_sunglasses"]


def needed():
    keys = set(BASICS)
    for p in glob.glob(os.path.join(HERE, "content", "day*.json")):
        d = json.load(open(p))
        keys |= {d["hook"].get("l3emoji"), d["hook"].get("subemoji"), d["end"].get("emoji")}
        for w in d["words"]:
            keys |= {w.get("emoji"), w.get("tip_emoji")}
        for s in d["stories"]:
            keys |= {s.get("emoji"), s.get("kicker_emoji")}
    for p in glob.glob(os.path.join(HERE, "content", "trial*.json")):
        d = json.load(open(p))
        keys |= {d.get("head_emoji")} | {it.get("emoji") for it in d["items"]}
    return sorted(k for k in keys if k)


def fetch(key):
    path = os.path.join(OUT, key + ".png")
    if os.path.exists(path):
        return True
    folder = SPECIAL.get(key) or (key.replace("_", " ")[0].upper() + key.replace("_", " ")[1:])
    for rel in (f"{folder}/3D/{key}_3d.png", f"{folder}/Default/3D/{key}_3d_default.png"):
        url = BASE_URL + urllib.parse.quote(rel)
        try:
            data = urllib.request.urlopen(url, timeout=30).read()
            open(path, "wb").write(data)
            return True
        except Exception:
            continue
    return False


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    keys = sys.argv[1:] or needed()
    missing = [k for k in keys if not fetch(k)]
    print(f"{len(keys) - len(missing)}/{len(keys)} emoji ready")
    if missing:
        print("NOT FOUND:", ", ".join(missing))
        sys.exit(1)
