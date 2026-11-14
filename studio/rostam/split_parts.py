"""Split the finished episode into two ~5-minute parts with a header line
«قسمت X از داستان رستم و سهراب» burnt in at the top.

Part 1: start .. end of S14, then a fresh end card (next part).
Part 2: fresh first frames of S14b (no crossfade), the rest of the
episode, and a fresh end card (next: Tahmineh).

  python3 -I split_parts.py <ep_dir> <full.mp4> <part_no_first> <out_dir>
"""
import os, subprocess, sys, wave
from multiprocessing import Process
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import render
from render import W, H, FPS, font, FAB, RTL, GOLD, CREAM, FA_DIGITS

ENC = ["-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p", "-r", str(FPS)]


def header(n):
    """Header line for part n, film-style: cream text, gold diamonds, soft shadow."""
    txt = f"قسمت {str(n).translate(FA_DIGITS)} از داستان رستم و سهراب"
    f = font(FAB, 46)
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    y = 218
    tw = f.getlength(txt, **RTL)
    d.text((W / 2, y), txt, font=f, fill=CREAM + (255,), anchor="mm", **RTL)
    for sgn in (-1, 1):
        x = W / 2 + sgn * (tw / 2 + 30)
        d.regular_polygon((x, y + 4, 7), 4, fill=GOLD + (235,))
    a = im.getchannel("A").filter(ImageFilter.GaussianBlur(8))
    out = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    out.putalpha(a.point(lambda v: min(200, int(v * 1.8))))
    out.alpha_composite(im)
    return out


def encode_main(src, start_frame, end_frame, hdr_png, out):
    fc = (f"[0:v]trim=start_frame={start_frame}:end_frame={end_frame},setpts=PTS-STARTPTS[v];"
          f"[v][1:v]overlay=0:0:eof_action=repeat[o]")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", src, "-i", hdr_png, "-filter_complex", fc,
                    "-map", "[o]", "-an"] + ENC + [out + ".part.mp4"], check=True)
    os.replace(out + ".part.mp4", out)


def encode_fresh(ctx, frames, hdr, out):
    """frames: list of (scene dict, time). Composite with the header and encode."""
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


def audio_cut(wav, t0, t1, pad, out):
    w = wave.open(wav)
    sr, ch, sw = w.getframerate(), w.getnchannels(), w.getsampwidth()
    x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).copy()
    seg = x[int(t0 * sr) * ch:int(t1 * sr) * ch]
    fade = int(0.02 * sr)
    seg[:fade] = (seg[:fade] * np.linspace(0, 1, fade)).astype(np.int16)
    seg = np.concatenate([seg, np.zeros(int(pad * sr) * ch, np.int16)])
    o = wave.open(out, "wb")
    o.setnchannels(ch)
    o.setsampwidth(sw)
    o.setframerate(sr)
    o.writeframes(seg.tobytes())
    o.close()


def mux(parts, wav, out):
    lst = out + ".txt"
    with open(lst, "w") as f:
        for p in parts:
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


def scene_frames(ctx):
    n, out = 0, {}
    for s in ctx.scenes:
        out[s["id"]] = (n, s)
        n += round((s["end"] - s["start"]) * FPS)
    return out, n


def fresh_jobs(ep, n1, work):
    """Render the three short fresh segments in one process."""
    ctx = render.Ctx(ep, os.path.join(ep, "images"))
    fr, total = scene_frames(ctx)
    k14b, s14b = fr["S14b"]
    kend, send = fr["END"]
    s14 = dict(fr["S14"][1])
    h1, h2 = header(n1), header(n1 + 1)
    # part 1 end card over the riders' plain
    ctx.script.update({"next_label": "NEXT PART", "next_en": "THE STOLEN HORSE", "next_fa": "ربودن رخش"})
    ctx._ov.clear()
    t0 = k14b / FPS
    end1 = dict(s14, card="end", start=t0, end=t0 + 6.0, idx=0)
    encode_fresh(ctx, [(end1, t0 + i / FPS) for i in range(6 * FPS)], h1, f"{work}/p1_end.mp4")
    # part 2 opening: S14b without the crossfade from S14
    st = dict(s14b, idx=0)
    encode_fresh(ctx, [(st, 289.0 + i / FPS) for i in range(24)], h2, f"{work}/p2_start.mp4")
    # part 2 end card (next: Tahmineh)
    ctx.script.update({"next_label": "NEXT PART", "next_en": "TAHMINEH", "next_fa": "تهمینه"})
    ctx._ov.clear()
    encode_fresh(ctx, [(send, send["start"] + i / FPS) for i in range(total - kend)], h2, f"{work}/p2_end.mp4")


def main():
    ep, full, n1, out_dir = sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4]
    work = os.path.join(out_dir, "work")
    os.makedirs(work, exist_ok=True)
    ctx = render.Ctx(ep, os.path.join(ep, "images"))
    fr, total = scene_frames(ctx)
    k14b = fr["S14b"][0]
    kend = fr["END"][0]
    header(n1).save(f"{work}/h1.png")
    header(n1 + 1).save(f"{work}/h2.png")
    k2 = k14b + round((289.0 + 24 / FPS - fr["S14b"][1]["start"]) * FPS)
    jobs = [Process(target=encode_main, args=(full, 0, k14b, f"{work}/h1.png", f"{work}/p1_main.mp4")),
            Process(target=encode_main, args=(full, k2, kend, f"{work}/h2.png", f"{work}/p2_main.mp4")),
            Process(target=fresh_jobs, args=(ep, n1, work))]
    for j in jobs:
        j.start()
    for j in jobs:
        j.join()
        if j.exitcode:
            sys.exit("a job failed")
    wav = os.path.join(ep, "audio", "episode.wav")
    audio_cut(wav, 0.0, k14b / FPS, 6.0, f"{work}/a1.wav")
    w = wave.open(wav)
    audio_cut(wav, 289.0, w.getnframes() / w.getframerate(), 0.0, f"{work}/a2.wav")
    mux([f"{work}/p1_main.mp4", f"{work}/p1_end.mp4"], f"{work}/a1.wav",
        os.path.join(out_dir, f"rostam_sohrab_part{n1}.mp4"))
    mux([f"{work}/p2_start.mp4", f"{work}/p2_main.mp4", f"{work}/p2_end.mp4"], f"{work}/a2.wav",
        os.path.join(out_dir, f"rostam_sohrab_part{n1 + 1}.mp4"))
    print("done")


if __name__ == "__main__":
    main()
