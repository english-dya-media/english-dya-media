"""Generate pronunciation clips for a day's words with Kokoro (local, offline).

Usage: python3 tts.py content/day01.json
Writes build/dayXX/tts_<i>_normal.wav and tts_<i>_slow.wav (+ durations json).
"""
import json, sys, os
import numpy as np
import soundfile as sf
from kokoro_onnx import Kokoro

HERE = os.path.dirname(os.path.abspath(__file__))
VOICE = "af_heart"


def trim(samples, sr, thresh=0.01, pad=0.04):
    a = np.abs(samples)
    idx = np.where(a > thresh)[0]
    if len(idx) == 0:
        return samples
    s = max(0, idx[0] - int(pad * sr))
    e = min(len(samples), idx[-1] + int(pad * sr))
    out = samples[s:e].copy()
    # short fades to avoid clicks
    f = int(0.008 * sr)
    out[:f] *= np.linspace(0, 1, f)
    out[-f:] *= np.linspace(1, 0, f)
    return out


def main(day_json):
    d = json.load(open(day_json))
    outdir = os.path.join(HERE, "build", f"day{d['day']:02d}")
    os.makedirs(outdir, exist_ok=True)
    k = Kokoro(os.path.join(HERE, "voice", "kokoro-v1.0.onnx"),
               os.path.join(HERE, "voice", "voices-v1.0.bin"))
    info = {}
    for i, w in enumerate(d["words"]):
        text = w["tts"]
        try:
            ph = k.tokenizer.phonemize(text, "en-us")
        except Exception as ex:  # tokenizer API differences
            ph = f"? ({ex})"
        for tag, speed in (("normal", 0.95), ("slow", 0.75)):
            if w.get("ph"):
                samples, sr = k.create(w["ph"], voice=VOICE, speed=speed, lang="en-us", is_phonemes=True)
            else:
                samples, sr = k.create(text, voice=VOICE, speed=speed, lang="en-us")
            samples = trim(np.asarray(samples, dtype=np.float32), sr)
            samples = samples / (np.max(np.abs(samples)) + 1e-9) * 0.89  # peak -1 dBFS
            path = os.path.join(outdir, f"tts_{i}_{tag}.wav")
            sf.write(path, samples, sr)
            info[f"{i}_{tag}"] = round(len(samples) / sr, 3)
        print(f"{text:12s} phonemes={ph}  normal={info[f'{i}_normal']}s slow={info[f'{i}_slow']}s")
    json.dump(info, open(os.path.join(outdir, "tts_durations.json"), "w"), indent=1)


if __name__ == "__main__":
    main(sys.argv[1])
