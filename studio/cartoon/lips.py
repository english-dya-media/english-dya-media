"""Lip-sync envelopes (loudness + brightness at 30 fps) for every voice line -> build/<series>/lips/<id>.json
python3 lips.py babak   (voices.py runs it too)"""
import glob, json, os, sys, wave
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import series
if __name__ == "__main__":
    series.from_argv()
from paths import VOICES_DIR, LIPS


def main():
    for path in sorted(glob.glob(f"{VOICES_DIR}/*.wav")):
        lid = os.path.basename(path)[:-4]
        w = wave.open(path); sr = w.getframerate()
        x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
        if w.getnchannels() > 1:
            x = x.reshape(-1, w.getnchannels()).mean(1)
        hop = sr // 30; n = len(x) // hop
        db, cen = [], []
        for i in range(n):
            seg = x[i * hop:(i + 1) * hop]
            db.append(float(20 * np.log10(np.sqrt((seg ** 2).mean() + 1e-9))))
            sp = np.abs(np.fft.rfft(seg * np.hanning(len(seg)))); f = np.fft.rfftfreq(len(seg), 1 / sr)
            cen.append(float((sp * f).sum() / (sp.sum() + 1e-9)))
        json.dump({"db": db, "cen": cen}, open(f"{LIPS}/{lid}.json", "w"))
    print("lips ok")


if __name__ == "__main__":
    main()
