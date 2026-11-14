"""English voices with Piper (libritts-high, one speaker id per role; see VOICES in lines.py).
python3 voices.py babak 3        -> build/babak/voices/<line id>.wav for every line of part 3 (48 kHz mono),
                                   durations.json and lip-sync data
python3 voices.py babak all      -> every line
python3 voices.py babak 3 p3s2a,p3s2b   -> only these lines (to redo one take)"""
import json, os, subprocess, sys, wave
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import series
if __name__ == "__main__":
    series.from_argv()
from paths import VOICES_DIR, PIPER
from lines import LINES, VOICES

MODEL = os.path.join(PIPER, "en-us-libritts-high.onnx")


def synth(voice, text, spk, length, path):
    from piper import SynthesisConfig
    cfg = SynthesisConfig(speaker_id=spk, length_scale=length, noise_scale=0.667, noise_w_scale=0.8)
    with wave.open(path, "wb") as w:
        voice.synthesize_wav(text, w, syn_config=cfg)


def main(which, only=None):
    from piper import PiperVoice
    voice = PiperVoice.load(MODEL)
    durs_path = os.path.join(VOICES_DIR, "durations.json")
    durs = json.load(open(durs_path)) if os.path.exists(durs_path) else {}
    for lid, part, scene, spk, en, fa, tts in LINES:
        if (which != "all" and part != int(which)) or (only and lid not in only):
            continue
        sid, length, semis, vol = VOICES[spk]
        raw = os.path.join(VOICES_DIR, f"{lid}.raw.wav")
        synth(voice, tts or en, sid, length, raw)
        with wave.open(raw) as w:
            sr = w.getframerate()
        f = 2 ** (semis / 12)
        af = []
        if semis:
            af.append(f"asetrate={sr}*{f:.5f},aresample={sr},atempo={1 / f:.5f}")
        if spk.endswith("_W"):
            af.append("lowpass=f=3800")
        af += [f"volume={vol}", "silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.05",
               "areverse", "silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.08", "areverse", "aresample=48000"]
        out = os.path.join(VOICES_DIR, f"{lid}.wav")
        subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", raw, "-af", ",".join(af), "-ac", "1", "-ar", "48000",
                        "-c:a", "pcm_s16le", out], check=True)
        os.remove(raw)
        with wave.open(out) as w:
            durs[lid] = round(w.getnframes() / w.getframerate(), 3)
        print(lid, spk, durs[lid], flush=True)
    json.dump(durs, open(durs_path, "w"), indent=1)
    import lips
    lips.main()


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "all", sys.argv[2].split(",") if len(sys.argv) > 2 else None)
