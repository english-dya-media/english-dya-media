"""Final encode of a part: subtitles (ASS) + header on every frame + title card + end card + moving page name + audio.
python3 encode.py VIDEO AUDIO ASS CARDS_DIR TITLE_START TITLE_END END_START OUT [EXTRA_WM_OFF]
EXTRA_WM_OFF: extra ffmpeg expression in t where the page name hides (e.g. 'between(t,49.3,55.5)' under a caption)."""
import os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(HERE, "fonts")
VBR = float(os.environ.get("VBR", "3.0"))   # video Mbit/s: ~50 MB for 2:10 (GitHub takes files < 100 MB)


def run(video, audio, ass, cards, t0, t1, e0, out, extra=""):
    t0, t1, e0 = float(t0), float(t1), float(e0)
    off = f"between(t,{t0},{t1})+gte(t,{e0})" + (f"+{extra}" if extra else "")
    wm = (f"drawtext=text='@english_dya':fontfile={FONTS}/Vazirmatn-Medium.ttf:fontsize=30:fontcolor=white:"
          "shadowcolor=black@0.6:shadowx=2:shadowy=2:alpha='0.45*clip(min(mod(t,20),20-mod(t,20))/0.5,0,1)':"
          "x='if(eq(mod(floor(t/20),4),0)+eq(mod(floor(t/20),4),3),90+2*mod(t,20),w-tw-130-2*mod(t,20))':"
          "y='if(eq(mod(floor(t/20),4),0)+eq(mod(floor(t/20),4),2),300,860)':"
          f"enable='not({off})'")
    fin = f"fade=t=in:st={t0}:d=0.35:alpha=1," if t0 > 0 else ""
    fc = (f"[0:v]subtitles={ass}:fontsdir={FONTS}[s];[2:v]format=rgba[h];"
          f"[3:v]format=rgba,{fin}fade=t=out:st={t1 - 0.4}:d=0.4:alpha=1[ti];"
          f"[4:v]format=rgba,fade=t=in:st={e0}:d=0.4:alpha=1[en];"
          f"[s][ti]overlay=0:0:enable='between(t,{t0},{t1})':shortest=1[a];"
          f"[a][en]overlay=0:0:enable='gte(t,{e0})'[b];[b][h]overlay=0:0[c];[c]{wm}[v]")
    tmp = out[:-4] + ".part.mp4"
    cmd = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", video, "-i", audio,
           "-framerate", "30", "-loop", "1", "-i", f"{cards}/header.png",
           "-framerate", "30", "-loop", "1", "-i", f"{cards}/title.png",
           "-framerate", "30", "-loop", "1", "-i", f"{cards}/end.png",
           "-filter_complex", fc, "-map", "[v]", "-map", "1:a", "-shortest",
           "-c:v", "libx264", "-preset", "medium", "-b:v", f"{VBR}M", "-maxrate", f"{VBR * 1.5:.1f}M", "-bufsize", f"{VBR * 3:.1f}M", "-pix_fmt", "yuv420p",
           "-profile:v", "high", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", tmp]
    subprocess.run(cmd, check=True)
    os.replace(tmp, out)


if __name__ == "__main__":
    run(*sys.argv[1:9], *(sys.argv[9:10] or [""]))
