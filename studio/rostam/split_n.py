"""Cut a finished long render into several short parts (each < 3 min) for posting.

  python3 -I split_n.py spec.json

spec: {"full": "<long render.mp4>", "ep": "<episode dir with audio/>", "out": "<dir>", "first_part": 1,
       "cuts": ["S06c", "S14b", "S21"],                 # scene ids where parts 2.. start
       "titles": [[en, fa], ...],                         # one per part, plus the part after the last
       "retitle": true}                                   # redraw the first part's TITLE card as "PART N · title"
Every part gets the header «قسمت N از داستان رستم و سهراب»; a part that starts mid-episode gets ~1 s of fresh
frames (no crossfade from the previous shot); every part ends on a fresh end card naming the next part.
Output: <out>/rostam_partNN.mp4
"""
import json, os, subprocess, sys, wave
from multiprocessing import Pool, Process
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import render
from render import W, H, FPS, part_header

ENC = ["-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p", "-r", str(FPS)]
LEAD = 0.15          # a part that starts mid-episode starts this much before its first shot (silence)
FRESH = 0.8          # seconds of fresh frames at such a start (covers the 0.6 s crossfade)
CARD = 6.0


def scene_frames(ctx):
    n, out = 0, {}
    for s in ctx.scenes:
        out[s["id"]] = (n, s)
        n += round((s["end"] - s["start"]) * FPS)
    return out, n


def enc_main(args):
    src, a, b, hdr, out = args
    fc = (f"[0:v]trim=start_frame={a}:end_frame={b},setpts=PTS-STARTPTS[v];"
          f"[v][1:v]overlay=0:0:eof_action=repeat[o]")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", src, "-i", hdr, "-filter_complex", fc,
                    "-map", "[o]", "-an"] + ENC + [out + ".part.mp4"], check=True)
    os.replace(out + ".part.mp4", out)


def enc_fresh(ctx, frames, hdr, out):
    ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
                           "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-"] + ENC + [out + ".part.mp4"],
                          stdin=subprocess.PIPE)
    for sc, t in frames:
        im = ctx.frame(sc, t).convert("RGBA")
        im.alpha_composite(hdr)
        ff.stdin.write(im.convert("RGB").tobytes())
    ff.stdin.close()
    if ff.wait() != 0:
        sys.exit("ffmpeg failed: " + out)
    os.replace(out + ".part.mp4", out)


def plan(spec, ctx):
    """List, per part, its video pieces ("main" frame ranges of the long render, or "fresh" frame lists)
    and its audio span."""
    fr, total = scene_frames(ctx)
    ids = [s["id"] for s in ctx.scenes]
    cuts = spec["cuts"]
    n0 = spec["first_part"]
    parts = []
    for i in range(len(cuts) + 1):
        k = n0 + i
        pieces = []
        if i == 0:
            a_t0, f0 = 0.0, 0
            if spec.get("retitle") and "TITLE" in fr:
                ft, st = fr["TITLE"]
                nt = round((st["end"] - st["start"]) * FPS)
                pieces.append(("main", 0, ft))
                pieces.append(("fresh", "title", [(st, st["start"] + j / FPS) for j in range(nt)]))
                f0 = ft + nt
        else:
            f, sc = fr[cuts[i - 1]]
            a_t0 = sc["start"] - LEAD
            nf = round((LEAD + FRESH) * FPS)
            first = dict(sc, idx=0)
            pieces.append(("fresh", "start", [(first, a_t0 + j / FPS) for j in range(nf)]))
            f0 = f + round((a_t0 + nf / FPS - sc["start"]) * FPS)
        if i < len(cuts):
            fe, sc_next = fr[cuts[i]]
            prev = ctx.scenes[ids.index(cuts[i]) - 1]
            pieces.append(("main", f0, fe))
            t0 = fe / FPS
            card = dict(prev, card="end", start=t0, end=t0 + CARD, items=[], idx=0)
            pieces.append(("fresh", "end", [(card, t0 + j / FPS) for j in range(round(CARD * FPS))]))
            a_t1, pad = fe / FPS, CARD
        else:
            fe, send = fr["END"]
            pieces.append(("main", f0, fe))
            pieces.append(("fresh", "end", [(send, send["start"] + j / FPS) for j in range(total - fe)]))
            a_t1, pad = None, 0.0
        parts.append({"k": k, "pieces": pieces, "audio": (a_t0, a_t1, pad)})
    return parts


def fresh_worker(spec, parts, work):
    ctx = render.Ctx(spec["ep"], None)
    titles = spec["titles"]
    for i, p in enumerate(parts):
        hdr = part_header(p["k"])
        for j, piece in enumerate(p["pieces"]):
            if piece[0] != "fresh":
                continue
            ctx._ov.clear()
            nxt = titles[i + 1] if i + 1 < len(titles) else titles[-1]
            ctx.script.update({"part": p["k"], "title_en": titles[i][0], "title_fa": titles[i][1],
                               "next_label": "NEXT PART", "next_en": nxt[0], "next_fa": nxt[1]})
            enc_fresh(ctx, piece[2], hdr, f"{work}/p{p['k']:02d}_{j}.mp4")


def audio(wav, t0, t1, pad, out):
    w = wave.open(wav)
    sr, ch, sw = w.getframerate(), w.getnchannels(), w.getsampwidth()
    x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).copy()
    seg = x[int(t0 * sr) * ch:(int(t1 * sr) * ch if t1 is not None else len(x))]
    fade = int(0.02 * sr)
    seg[:fade] = (seg[:fade] * np.linspace(0, 1, fade)).astype(np.int16)
    seg = np.concatenate([seg, np.zeros(int(pad * sr) * ch, np.int16)])
    o = wave.open(out, "wb")
    o.setnchannels(ch)
    o.setsampwidth(sw)
    o.setframerate(sr)
    o.writeframes(seg.tobytes())
    o.close()


def mux(pieces, wav, out):
    lst = out + ".txt"
    with open(lst, "w") as f:
        for p in pieces:
            f.write(f"file '{os.path.abspath(p)}'\n")
    vid = out + ".v.mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", vid],
                   check=True)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", vid, "-i", wav, "-map", "0:v", "-map", "1:a",
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "160k", "-ar", "48000", "-ac", "2", "-shortest",
                    "-movflags", "+faststart", out + ".part.mp4"], check=True)
    os.replace(out + ".part.mp4", out)
    os.remove(vid)
    os.remove(lst)


def main():
    spec = json.load(open(sys.argv[1], encoding="utf-8"))
    out = spec["out"]
    work = os.path.join(out, "work")
    os.makedirs(work, exist_ok=True)
    ctx = render.Ctx(spec["ep"], None)
    parts = plan(spec, ctx)
    jobs = []
    for p in parts:
        hp = f"{work}/h{p['k']:02d}.png"
        part_header(p["k"]).save(hp)
        for j, piece in enumerate(p["pieces"]):
            if piece[0] == "main" and piece[2] > piece[1]:
                jobs.append((spec["full"], piece[1], piece[2], hp, f"{work}/p{p['k']:02d}_{j}.mp4"))
    fw = Process(target=fresh_worker, args=(spec, parts, work))
    fw.start()
    with Pool(2) as pool:
        pool.map(enc_main, jobs, chunksize=1)
    fw.join()
    if fw.exitcode:
        sys.exit("fresh frames failed")
    wav = os.path.join(spec["ep"], "audio", "episode.wav")
    for p in parts:
        k = p["k"]
        files = [f"{work}/p{k:02d}_{j}.mp4" for j, pc in enumerate(p["pieces"])
                 if pc[0] == "fresh" or pc[2] > pc[1]]
        audio(wav, *p["audio"], f"{work}/a{k:02d}.wav")
        mux(files, f"{work}/a{k:02d}.wav", os.path.join(out, f"rostam_part{k:02d}.mp4"))
        print("part", k, "done", flush=True)


if __name__ == "__main__":
    main()
