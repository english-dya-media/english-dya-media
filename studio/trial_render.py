"""Trial reel (~17-20 s, Instagram "Trial Reel" shown to non-followers): each item is a wrong/basic phrase (struck through,
spoken), then the right/stronger one (spoken) and a one-line Persian note. Two formats, both written with daygen.write_trial():
  mistakes: 3 sentences Persian speakers get wrong ("I am agree." -> "I agree.")
  vocab:    4 basic phrases -> a stronger word ("very tired" -> "exhausted")

python3 trial_render.py content/trial12a.json [--preview]      ->  out/trial12a.mp4
Content: {"tag", "handle", "headline", "head_emoji", "end1", "end2", "items": [{"wrong", "right", "note", "emoji"}], "caption", ...}
"""
import json, os, subprocess, sys
import numpy as np
import soundfile as sf
from kokoro_onnx import Kokoro
from playwright.sync_api import sync_playwright
from render import font_css, CSS, EMO, SFX, build_audio, HERE, W, H, FPS
from music import make_music
from tts import trim

END = 2.2

MCSS = r"""
.adq{direction:rtl;display:flex;align-items:center;gap:16px;background:var(--acc);color:#14162E;font:900 64px/1.3 Vaz;
 padding:10px 40px;border-radius:999px;box-shadow:0 14px 40px rgba(255,212,59,.3);}
.adq img{width:78px;height:78px;}
.sent{display:flex;align-items:center;gap:22px;font:700 76px/1.25 Pop;max-width:1000px;}
.sent img{width:84px;height:84px;flex:none;}
.sent.bad span{position:relative;color:#FFB3C1;}
.sent.bad i{position:absolute;left:-6px;right:-6px;top:54%;height:9px;margin-top:-4px;background:var(--bad);border-radius:5px;transform-origin:left center;}
.sent.good span{color:var(--good);font-size:86px;font-weight:800;}
.note{direction:rtl;max-width:940px;text-align:center;padding:10px 34px 14px;border-radius:28px;background:var(--acc);color:#14162E;font:800 54px/1.45 Vaz;}
.big{direction:rtl;font:900 86px/1.35 Vaz;text-align:center;}
.fbtn{direction:rtl;display:flex;align-items:center;gap:18px;background:#3B82F6;color:#fff;font:900 96px/1.3 Vaz;
 padding:16px 70px;border-radius:40px;box-shadow:0 20px 50px rgba(59,130,246,.45);}
.fbtn img{width:96px;height:96px;}
"""

JS = r"""
const D = __DATA__, TS = __TS__, E = n => '__EMO__/' + n + '.png';
const ez = 'cubic-bezier(.2,.8,.2,1)', bo = 'cubic-bezier(.2,.9,.3,1.3)';
const A = (n, d, dl, f = 'ease-out', it = 1) => `animation:${n} ${d}s ${f} ${dl}s ${it} normal both;`;
const L = (top, inner) => `<div class="line" style="top:${top}px">${inner}</div>`;
function header(active) {
  return L(236, `<div class="handle" dir="ltr">${D.handle}</div>`) +
    L(322, `<div class="adq">${D.headline}<img src="${E(D.head_emoji || 'grimacing_face')}"></div>`) +
    (active >= 0 ? L(470, '<div class="prog">' + D.items.map((_, i) =>
      `<span class="${i === active ? 'on' : (i < active ? 'done' : '')}"></span>`).join('') + '</div>') : '');
}
function scene(i) {
  const it = D.items[i], T = TS[i];
  return header(i) + `<div class="glow" style="top:${760 - 320}px"></div>` +
    `<div class="emowrap" style="top:${760 - 140}px;width:280px;height:280px;margin-left:-140px;${A('bob', 2.4, .4, 'ease-in-out', 'infinite')}">` +
      `<img src="${E(it.emoji)}" style="${A('punch', .35, 0, ez)}"></div>` +
    L(990, `<div class="sent bad" dir="ltr" style="${A('punch', .35, 0, ez)}"><img src="${E('cross_mark')}"><span>${it.wrong}<i style="${A('strike', .25, T.strike)}"></i></span></div>`) +
    L(1140, `<div class="sent good" dir="ltr" style="${A('slideUp', .3, T.right, ez)}"><img src="${E('check_mark_button')}"><span>${it.right}</span></div>`) +
    L(1310, `<div class="note" style="${A('popSmall', .35, T.note, bo)}">${it.note}</div>`);
}
function endScene() {
  return L(236, `<div class="handle" dir="ltr">${D.handle}</div>`) +
    `<div class="glow" style="top:420px;width:900px;height:900px;margin-left:-450px"></div>` +
    L(560, `<div class="big" style="${A('slideUp', .35, 0, ez)}">${D.end1}</div>`) +
    L(700, `<div class="big" style="color:var(--acc);${A('slideUp', .35, .15, ez)}">${D.end2}</div>`) +
    L(900, `<div class="fbtn" style="${A('popSmall', .4, .35, bo)}"><span style="display:inline-block;${A('pulse', .6, .9, 'ease-in-out', 'infinite')}">فالو کن</span><img src="${E('backhand_index_pointing_down')}"></div>`);
}
function fitAll(maxW = 1000) {
  document.querySelectorAll('.line > *').forEach(el => {
    el.style.width = 'max-content'; const w = el.offsetWidth;
    if (w > maxW) { el.style.zoom = (maxW / w).toFixed(3); el.style.margin = '0 auto'; } else el.style.width = '';
  });
}
window.show = async (key) => {
  document.getElementById('stage').innerHTML = key === 'end' ? endScene() : scene(+key);
  await Promise.all([...document.images].map(im => im.decode().catch(() => {})));
  fitAll(); window.seek(0);
};
window.seek = (ms) => { for (const a of document.getAnimations()) { a.pause(); a.currentTime = ms; } };
window.ready = async () => {
  await Promise.all([document.fonts.load('700 60px Pop', 'Ab'), document.fonts.load('800 60px Pop', 'Ab'), document.fonts.load('900 100px Vaz', 'سلام')]);
  return document.fonts.check('900 100px Vaz', 'سلام');
};
"""


def main(path, preview=False):
    d = json.load(open(path))
    bdir = os.path.join(HERE, "build", d["tag"]); os.makedirs(bdir, exist_ok=True)
    k = Kokoro(os.path.join(HERE, "voice", "kokoro-v1.0.onnx"), os.path.join(HERE, "voice", "voices-v1.0.bin"))
    clips, ts, durs = [], [], []
    for i, it in enumerate(d["items"]):
        pair = {}
        for tag in ("wrong", "right"):
            x, sr = k.create(it[tag], voice="af_heart", speed=0.95, lang="en-us")
            x = trim(np.asarray(x, dtype=np.float32), sr); x = x / (np.max(np.abs(x)) + 1e-9) * 0.89
            p = os.path.join(bdir, f"s{i}_{tag}.wav"); sf.write(p, x, sr); pair[tag] = (p, len(x) / sr)
        strike = .15 + pair["wrong"][1] + .1
        right = strike + .35
        note = right + pair["right"][1] + .1
        ts.append(dict(strike=round(strike, 2), right=round(right, 2), note=round(note, 2)))
        durs.append(round(note + 2.3, 2)); clips.append(pair)
    html = os.path.join(bdir, "m.html")
    js = JS.replace("__DATA__", json.dumps(d, ensure_ascii=False)).replace("__TS__", json.dumps(ts)).replace("__EMO__", EMO)
    open(html, "w", encoding="utf-8").write("<!doctype html><html lang='fa'><head><meta charset='utf-8'><style>" + font_css() + CSS + MCSS +
        "</style></head><body><div id='bg'></div><div id='dots'></div><div id='stage'></div><script>" + js + "</script></body></html>")
    scenes = [(i, durs[i]) for i in range(len(d["items"]))] + [("end", END)]
    with sync_playwright() as p:
        exe = "/usr/bin/google-chrome" if os.path.exists("/usr/bin/google-chrome") else None
        b = p.chromium.launch(executable_path=exe, args=["--no-sandbox", "--disable-gpu", "--font-render-hinting=none"])
        pg = b.new_page(viewport={"width": W, "height": H}); pg.goto("file://" + html); print("fonts ok:", pg.evaluate("ready()"))
        if preview:
            for key, t in ((0, 0.0), (0, 9.0), (2, 9.0), ("end", 1.5)):
                pg.evaluate(f"show({json.dumps(key)})"); pg.evaluate(f"seek({t * 1000})")
                pg.screenshot(path=os.path.join(bdir, f"prev_{key}_{t}.jpg"), type="jpeg", quality=85)
            b.close(); print("previews in", bdir); return
        video = os.path.join(bdir, "video.mp4"); tmp = video[:-4] + ".part.mp4"
        proc = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "image2pipe", "-framerate", str(FPS), "-c:v", "mjpeg", "-i", "-",
                                 "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p", "-r", str(FPS), tmp], stdin=subprocess.PIPE)
        for key, dur in scenes:
            pg.evaluate(f"show({json.dumps(key)})")
            for f in range(round(dur * FPS)):
                pg.evaluate(f"seek({f * 1000 / FPS})"); proc.stdin.write(pg.screenshot(type="jpeg", quality=92))
        proc.stdin.close()
        if proc.wait() != 0: raise SystemExit("ffmpeg failed")
        os.replace(tmp, video); b.close()
    ev, t0, vr = [], 0.0, []
    for i, pair in enumerate(clips):
        T = ts[i]
        ev += [(t0, f"{SFX}/whoosh.wav", 0.25), (t0 + .15, pair["wrong"][0], 1.0), (t0 + T["strike"], f"{SFX}/boop.wav", 0.45),
               (t0 + T["right"], pair["right"][0], 1.0), (t0 + T["right"], f"{SFX}/ding.wav", 0.25), (t0 + T["note"], f"{SFX}/pop.wav", 0.25)]
        vr += [(t0 + .15, t0 + .15 + pair["wrong"][1]), (t0 + T["right"], t0 + T["right"] + pair["right"][1])]
        t0 += durs[i]
    ev += [(t0, f"{SFX}/whoosh.wav", 0.3), (t0 + .35, f"{SFX}/pop.wav", 0.35)]
    total = t0 + END
    ev.insert(0, (0.0, make_music(total, vr, os.path.join(bdir, "music.wav"), bpm=104, level_db=-26.0), 1.0))
    wav = os.path.join(bdir, "audio.wav"); build_audio(ev, total, wav)
    out = os.path.join(HERE, "out", f"{d['tag']}.mp4"); tmp = out[:-4] + ".part.mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", video, "-i", wav, "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac",
                    "-b:a", "160k", "-ar", "44100", "-ac", "2", "-shortest", "-movflags", "+faststart", tmp], check=True)
    os.replace(tmp, out); print("trial reel:", out, round(total, 2), "s")


if __name__ == "__main__":
    main(sys.argv[1], preview="--preview" in sys.argv)
