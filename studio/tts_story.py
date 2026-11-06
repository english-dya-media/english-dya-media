"""Voices + timeline for one story episode.

python3 tts_story.py content/story_w01.json 1
-> build/story_wXX_eYY/line_N.wav, timeline.json (start times, durations, mouth envelopes at 30 fps)
"""
import json, os, re, sys
import numpy as np
import soundfile as sf
from kokoro_onnx import Kokoro

HERE = os.path.dirname(os.path.abspath(__file__))
FPS = 30
TITLE, LEAD, GAP, CLIFF, VOCAB = 2.6, 0.15, 0.5, 1.8, 4.8


def trim(x, sr, thresh=0.01, pad=0.05):
    idx = np.where(np.abs(x) > thresh)[0]
    if len(idx) == 0:
        return x
    x = x[max(0, idx[0] - int(pad * sr)): min(len(x), idx[-1] + int(pad * sr))].copy()
    f = int(0.01 * sr)
    x[:f] *= np.linspace(0, 1, f); x[-f:] *= np.linspace(1, 0, f)
    return x


def envelope(x, sr):
    hop = sr // FPS
    n = int(np.ceil(len(x) / hop))
    rms = np.array([np.sqrt(np.mean(x[i * hop:(i + 1) * hop] ** 2) + 1e-12) for i in range(n)])
    ref = np.percentile(rms, 90) + 1e-9
    v = np.clip((rms - 0.02 * ref / 0.3) / ref, 0, 1)
    out, cur = [], 0.0
    for a in v:  # quick attack, slower release
        cur = a if a > cur else cur * 0.55 + a * 0.45
        out.append(round(float(cur), 3))
    return out


def main(path, ep_no):
    s = json.load(open(path))
    ep = next(e for e in s["episodes"] if e["ep"] == ep_no)
    out = os.path.join(HERE, "build", f"story_w{s['week']:02d}_e{ep_no:02d}")
    os.makedirs(out, exist_ok=True)
    k = Kokoro(os.path.join(HERE, "voice", "kokoro-v1.0.onnx"), os.path.join(HERE, "voice", "voices-v1.0.bin"))
    t = TITLE
    lines = []
    for i, ln in enumerate(ep["lines"]):
        c = s["characters"][ln["who"]]
        text = re.sub(r"\*", "", ln["en"])
        x, sr = k.create(text, voice=c["voice"], speed=c.get("speed", 1.0), lang=c.get("lang", "en-us"))
        x = trim(np.asarray(x, dtype=np.float32), sr)
        x = x / (np.max(np.abs(x)) + 1e-9) * 0.89
        wav = os.path.join(out, f"line_{i}.wav")
        sf.write(wav, x, sr)
        dur = len(x) / sr
        start = t + LEAD
        lines.append(dict(ln, i=i, start=round(start, 3), dur=round(dur, 3), end=round(start + dur, 3),
                          seg_start=round(t, 3), seg_end=round(start + dur + GAP, 3), wav=wav, env=envelope(x, sr)))
        print(f"line {i} {ln['who']:7s} {dur:5.2f}s  start {start:5.2f}  {text}")
        t = start + dur + GAP
    cliff = t
    vocab = cliff + CLIFF
    total = round(vocab + VOCAB, 3)
    json.dump(dict(fps=FPS, title=TITLE, cliff=round(cliff, 3), vocab=round(vocab, 3), total=total, lines=lines),
              open(os.path.join(out, "timeline.json"), "w"), indent=0)
    print("cliff", round(cliff, 2), "vocab", round(vocab, 2), "total", total)


if __name__ == "__main__":
    main(sys.argv[1], int(sys.argv[2]))
