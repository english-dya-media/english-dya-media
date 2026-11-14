"""Join a part's scenes and make the final reel: subtitles, header, title and end cards, page name, sound.
python3 assemble.py babak 3   -> build/babak/out/babak_part03.mp4
needs build/babak/scenes/p03_*.mp4 (render.py), build/babak/audio/part03.wav (p03_audio.py), build/babak/out/p03.ass
(p03_subs.py). Card timing comes from <series>/parts.json -> parts.N.cards:
{"title": [start, end], "end": start, "wm_off": "<extra ffmpeg expression in t, or empty>"}"""
import importlib, os, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import series
name = series.from_argv()
from paths import SCENES, AUDIO, OUT
import cards, encode

n = int(sys.argv[1]); tag = f"p{n:02d}"
cfg = series.config()
c = cfg["parts"][str(n)]["cards"]
names = list(importlib.import_module(f"{tag}_scenes").SCENES)
lst = os.path.join(OUT, f"{tag}_list.txt")
open(lst, "w").write("".join(f"file '{SCENES}/{tag}_{s}.mp4'\n" for s in names))
video = os.path.join(OUT, f"{tag}_video.mp4")
subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", video], check=True)
cdir = cards.make(n, os.path.join(OUT, f"{tag}_cards"))
out = os.path.join(OUT, f"{name}_part{n:02d}.mp4")
encode.run(video, os.path.join(AUDIO, f"part{n:02d}.wav"), os.path.join(OUT, f"{tag}.ass"), cdir,
           c["title"][0], c["title"][1], c["end"], out, c.get("wm_off", ""))
d = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", out],
                         capture_output=True, text=True).stdout)
print(out, f"{d:.1f} s", f"{os.path.getsize(out) / 1e6:.1f} MB")
if d >= 170 or os.path.getsize(out) > 95e6:
    raise SystemExit("too long or too big: keep parts under 170 s and files under 95 MB")
