"""Where things are. The series (a folder next to this file: babak, zahhak, …) comes from the SERIES environment
variable; entry scripts set it from their first argument (see series_from_argv), series scripts from their folder."""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SERIES = os.environ.get("SERIES", "")
SDIR = os.path.join(HERE, SERIES) if SERIES else ""
if SDIR:
    if not os.path.isdir(SDIR):
        raise SystemExit(f"no series folder {SDIR}")
    if SDIR not in sys.path:
        sys.path.insert(0, SDIR)                     # cast.py, lines.py, pNN_*.py of the series
FONTS = os.path.join(HERE, "fonts")
BG = os.path.join(HERE, "build", "bg")               # painted backgrounds, shared by all series
PIPER = os.path.join(HERE, "build", "piper")         # voice model, shared
BUILD = os.path.join(HERE, "build", SERIES or "_")
VOICES_DIR = os.path.join(BUILD, "voices")           # one wav per line id + durations.json
LIPS = os.path.join(BUILD, "lips")                   # lip-sync envelopes per line id
SCENES = os.path.join(BUILD, "scenes")               # one mp4 per scene
AUDIO = os.path.join(BUILD, "audio")                 # mixed soundtrack per part
OUT = os.path.join(BUILD, "out")                     # subtitles, cards and final parts
for _d in (BG, PIPER, VOICES_DIR, LIPS, SCENES, AUDIO, OUT):
    os.makedirs(_d, exist_ok=True)
