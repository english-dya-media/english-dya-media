"""Episode narration: script.json -> one WAV per line + episode WAV + timeline.

usage: python3 -I voices_ep.py <cast.json> <script.json> <out_dir>
out_dir gets: lines/NNN.wav, episode.wav, timeline.json
Timeline holds every scene (start/end) and line (start/end, verse_start).
"""
import sys, json, os, re, wave
import numpy as np
import sherpa_onnx

K = os.path.join(os.path.dirname(os.path.abspath(__file__)), "voice", "kokoro-multi-lang-v1_0")
NAMES = ("af_alloy,af_aoede,af_bella,af_heart,af_jessica,af_kore,af_nicole,af_nova,"
         "af_river,af_sarah,af_sky,am_adam,am_echo,am_eric,am_fenrir,am_liam,am_michael,"
         "am_onyx,am_puck,am_santa,bf_alice,bf_emma,bf_isabella,bf_lily,bm_daniel,bm_fable,"
         "bm_george,bm_lewis").split(",")
SID = {n: i for i, n in enumerate(NAMES)}
SR = 24000
_eng = {}

def engine(accent):
    if accent not in _eng:
        lex = f"{K}/lexicon-gb-en.txt" if accent == "gb" else f"{K}/lexicon-us-en.txt"
        cfg = sherpa_onnx.OfflineTtsConfig(
            model=sherpa_onnx.OfflineTtsModelConfig(
                kokoro=sherpa_onnx.OfflineTtsKokoroModelConfig(
                    model=f"{K}/model.onnx", voices=f"{K}/voices.bin", tokens=f"{K}/tokens.txt",
                    lexicon=lex, data_dir=f"{K}/espeak-ng-data", dict_dir=f"{K}/dict",
                    lang="en" if accent == "gb" else "en-us"),
                provider="cpu", num_threads=2),
            max_num_sentences=1)
        _eng[accent] = sherpa_onnx.OfflineTts(cfg)
    return _eng[accent]

def write_wav(path, x):
    pcm = (np.clip(x, -1, 1) * 32767).astype(np.int16)
    with wave.open(path, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())

cast = json.load(open(sys.argv[1], encoding="utf-8"))
script = json.load(open(sys.argv[2], encoding="utf-8"))
out = sys.argv[3]
os.makedirs(f"{out}/lines", exist_ok=True)
say = cast.get("_say", {})

def spoken(text):
    for k in sorted(say, key=len, reverse=True):
        text = re.sub(rf"\b{re.escape(k)}\b", say[k], text)
    return text

chunks, t = [], 0.0
def add(x):
    global t
    chunks.append(x); t += len(x) / SR
def silence(sec):
    add(np.zeros(int(round(sec * SR)), dtype=np.float32))

timeline = {"scenes": []}
silence(0.5)
n = 0
for sc in script["scenes"]:
    s = {"id": sc["id"], "start": round(t, 3), "lines": []}
    if sc.get("card"):
        silence(sc["dur"])
    for ln in sc["lines"]:
        n += 1
        vstart = None
        if ln.get("verse"):
            vstart = round(t, 3)
            silence(ln.get("pre", 1.5))
        c = cast[ln["role"]]
        cache = f"{out}/lines/{n:03d}.wav"
        eng = engine("gb" if c["voice"].startswith("b") else "us")
        a = eng.generate(spoken(ln["en"]), sid=SID[c["voice"]], speed=c.get("speed", 1.0))
        x = np.asarray(a.samples, dtype=np.float32)
        if x.size == 0:
            sys.exit(f"empty audio: {ln['en']}")
        write_wav(cache, x)
        st = round(t, 3)
        add(x)
        s["lines"].append({"n": n, "role": ln["role"], "start": st, "end": round(t, 3),
                           "verse_start": vstart})
        silence(ln.get("pause", 0.5))
        print(f"{n:03d} {ln['role']:<14} {len(x)/SR:5.1f}s", flush=True)
    s["end"] = round(t, 3)
    timeline["scenes"].append(s)

silence(0.5)
write_wav(f"{out}/episode.wav", np.concatenate(chunks))
timeline["duration"] = round(t, 3)
json.dump(timeline, open(f"{out}/timeline.json", "w", encoding="utf-8"), indent=1)
print(f"TOTAL {t/60:.2f} min, {n} lines")
