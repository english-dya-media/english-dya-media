"""Quote reel (~6-8 s): a short English quote on a generated landscape, then its Persian meaning, over calm music
(no voice: the owner wants music only). The key words, their meanings and the "follow" line go in the caption only,
so the video stays clean for people to re-share to their stories. Made for the late-night slot.

python3 quote_render.py content/quote12.json [--preview]      ->  out/quote12.mp4
Content (written by daygen.write_quote): {"tag", "en", "fa", "author", "words": [{"en", "fa"}],
  "scene": {"palette", "seed", "figure", "trees", "sea"}, "handle", "cta", "caption", ...}
Palettes: dusk, night, sunset, mist, mono, rose, forest. The scene is drawn from the seed, so it never repeats.
"""
import base64, json, os, re, subprocess, sys
import numpy as np
import soundfile as sf
from playwright.sync_api import sync_playwright
from render import font_css, HERE, W, H, FPS, FONTS
from music import make_music

HOLD = 4.0                               # seconds on screen after the Persian appears
PROGS = [[[45, 48, 52, 55], [41, 45, 48, 52], [48, 52, 55, 59], [43, 47, 50, 55]],   # Am7 Fmaj7 Cmaj7 G
         [[41, 45, 48, 52], [43, 47, 50, 55], [40, 43, 47, 50], [45, 48, 52, 55]],   # Fmaj7 G Em7 Am7
         [[48, 52, 55, 59], [40, 43, 47, 50], [41, 45, 48, 52], [43, 47, 50, 55]],   # Cmaj7 Em7 Fmaj7 G
         [[38, 41, 45, 48], [43, 47, 50, 53], [48, 52, 55, 59], [45, 48, 52, 55]]]   # Dm7 G7 Cmaj7 Am7
PATTERNS = [[0, 2, 1, 3, 2, 1, 3, 2], [0, 1, 2, 3, 2, 3, 1, 2], [0, 2, 3, 2, 1, 2, 3, 1], [3, 2, 1, 0, 1, 2, 3, 2]]


def music_bed(total, out, day):
    """Soft music-box arpeggio over a pad, with a stereo room (convolution reverb); a different chord loop per day."""
    dry = out[:-4] + "_dry.wav"
    make_music(total + 0.5, [], dry, bpm=62, level_db=-20.0, prog=PROGS[day % 4], pluck_decay=0.9,
               pattern=PATTERNS[day % 4], pad_gain=0.6)
    x, sr = sf.read(dry)
    x = x.mean(1) if x.ndim > 1 else x
    rng, n = np.random.default_rng(day), int(2.4 * sr)
    t = np.arange(n) / sr
    chans = []
    for _ in range(2):
        ir = rng.standard_normal(n) * np.exp(-t / 0.85)
        ir[: int(.012 * sr)] *= np.linspace(0, 1, int(.012 * sr))
        N = 1 << (len(x) + n - 2).bit_length()
        y = np.fft.irfft(np.fft.rfft(x, N) * np.fft.rfft(ir, N), N)[: len(x)]
        y *= np.sqrt(np.mean(x ** 2)) / (np.sqrt(np.mean(y ** 2)) + 1e-9)
        chans.append(0.68 * x + 0.42 * y)
    st = np.stack(chans, 1)[: int(total * sr)]
    fo = int(1.4 * sr)
    st[-fo:] *= np.linspace(1, 0, fo)[:, None]
    st *= 10 ** (-17 / 20) / (np.sqrt(np.mean(st ** 2)) + 1e-9)
    sf.write(out, np.clip(st, -0.97, 0.97).astype(np.float32), sr)
    return out


def serif_css():
    faces = [("Play", "playfair-display-latin-500-italic.woff2", "500", "italic"),
             ("Play", "playfair-display-latin-600-italic.woff2", "600", "italic"),
             ("Corm", "cormorant-garamond-latin-500-italic.woff2", "500", "italic"),
             ("Corm", "cormorant-garamond-latin-600-italic.woff2", "600", "italic"),
             ("Lora", "lora-latin-400-normal.woff2", "400", "normal"),
             ("Lora", "lora-latin-500-normal.woff2", "500", "normal")]
    out = []
    for fam, fn, wt, st in faces:
        b = base64.b64encode(open(os.path.join(FONTS, fn), "rb").read()).decode()
        out.append("@font-face{font-family:%s;src:url(data:font/woff2;base64,%s) format('woff2');font-weight:%s;"
                   "font-style:%s;font-display:block;}" % (fam, b, wt, st))
    return "\n".join(out)


QCSS = r"""
*{box-sizing:border-box}
html,body{margin:0;width:1080px;height:1920px;overflow:hidden;background:#000;}
#scene{position:absolute;inset:0;overflow:hidden}
#cv{position:absolute;left:0;top:0;width:1080px;height:1920px;transform-origin:50% 42%;}
#shade{position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,.30) 0%,rgba(0,0,0,0) 13%,rgba(0,0,0,0) 20%,
  rgba(0,0,0,.26) 36%,rgba(0,0,0,.26) 62%,rgba(0,0,0,0) 76%,rgba(0,0,0,.30) 100%);}
.handle{position:absolute;top:160px;left:0;right:0;text-align:center;font:600 32px Pop;color:rgba(255,255,255,.72);letter-spacing:1.5px}
.block{position:absolute;left:84px;right:84px;top:60px;height:1300px;display:flex;flex-direction:column;align-items:center;
  justify-content:center;gap:30px;text-align:center}
.en{font-family:QSERIF;font-style:italic;font-weight:500;color:#fff;line-height:1.3;text-wrap:balance;
  text-shadow:0 2px 26px rgba(0,0,0,.6),0 0 2px rgba(0,0,0,.4)}
.en .k{display:inline}
.au{font:500 30px/1.2 Lora;letter-spacing:3px;color:rgba(255,255,255,.78);text-transform:uppercase;margin-top:-6px}
.sep{width:96px;height:2px;background:rgba(255,255,255,.6);border-radius:2px;transform-origin:center}
.fa{direction:rtl;font:400 47px/1.8 Vaz;color:#F7ECDB;text-wrap:balance;text-shadow:0 2px 18px rgba(0,0,0,.65)}
.kws{display:flex;gap:16px;flex-wrap:wrap;justify-content:center;margin-top:6px}
.kw{display:inline-flex;gap:14px;align-items:center;padding:10px 28px 12px;border-radius:999px;background:rgba(8,8,18,.42);
  border:1.5px solid rgba(255,255,255,.30);font:500 38px/1.3 Lora;color:#fff;direction:ltr}
.kw .f{direction:rtl;font:500 37px/1.3 Vaz;color:#FFDCA8}
.cta{direction:rtl;font:500 34px/1.4 Vaz;color:rgba(255,255,255,.88);text-shadow:0 2px 14px rgba(0,0,0,.7);margin-top:10px}
@keyframes kb{from{transform:scale(1)}to{transform:scale(1.075)}}
@keyframes qin{from{opacity:.55;filter:blur(2px);transform:translateY(10px)}to{opacity:1;filter:none;transform:none}}
@keyframes up{from{opacity:0;transform:translateY(22px)}to{opacity:1;transform:none}}
@keyframes fade{from{opacity:0}to{opacity:1}}
@keyframes grow{from{transform:scaleX(0)}to{transform:scaleX(1)}}
@keyframes kOn{from{color:#fff}to{color:#FFD9A0}}
"""

JS = r"""
const D = __DATA__, T = __T__, W = 1080, H = 1920;
const PAL = {
  dusk:   {sky: ['#0b1026', '#2e2c5e', '#d99a9a'], far: '#6c5f90', near: '#0d0e22', fog: '#d99a9a', glow: '#ffd6a8', disc: 1, stars: 1, hz: 1180},
  night:  {sky: ['#02050d', '#0b1b36', '#2c5376'], far: '#2e4c6a', near: '#03060d', fog: '#2c5376', glow: '#e3ecff', disc: 1, stars: 1, hz: 1170},
  sunset: {sky: ['#1b0f2e', '#7a3550', '#f29c5c'], far: '#8a4a5a', near: '#150a16', fog: '#f29c5c', glow: '#ffd27a', disc: 1, stars: 0, hz: 1210},
  mist:   {sky: ['#0f2a30', '#3e6d72', '#c9dbd2'], far: '#7f9e9c', near: '#0a181a', fog: '#c9dbd2', glow: '#fff4da', disc: 0, stars: 0, hz: 1180},
  mono:   {sky: ['#0c0c0e', '#2b2c30', '#8d8f94'], far: '#5c5e63', near: '#070708', fog: '#8d8f94', glow: '#ececec', disc: 1, stars: 0, hz: 1170},
  rose:   {sky: ['#1a1230', '#5e4275', '#eab3b8'], far: '#86668f', near: '#150e20', fog: '#eab3b8', glow: '#ffe3d8', disc: 1, stars: 1, hz: 1190},
  forest: {sky: ['#0a1712', '#2c5242', '#a9c8b2'], far: '#5d7f6d', near: '#050e0a', fog: '#a9c8b2', glow: '#f6ffe9', disc: 0, stars: 0, hz: 1160},
};
const ez = 'cubic-bezier(.2,.8,.2,1)';
const A = (n, d, dl, f = 'ease-out') => `animation:${n} ${d}s ${f} ${dl}s 1 normal both;`;
function rng32(a) { return function () { a |= 0; a = a + 0x6D2B79F5 | 0; let t = Math.imul(a ^ a >>> 15, 1 | a);
  t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; }
function noise(r) { const p = []; for (let i = 0; i < 512; i++) p.push(r());
  return x => { const i = Math.floor(x), f = x - i, a = p[i & 511], b = p[(i + 1) & 511], u = f * f * (3 - 2 * f); return a + (b - a) * u; }; }
const hex = c => [1, 3, 5].map(i => parseInt(c.slice(i, i + 2), 16));
const rgba = (c, a) => `rgba(${hex(c).join(',')},${a})`;
const mix = (c1, c2, t) => { const a = hex(c1), b = hex(c2); return `rgb(${a.map((v, i) => Math.round(v + (b[i] - v) * t)).join(',')})`; };

function trees(ctx, r, top, col) {
  ctx.fillStyle = col;
  for (let i = 0; i < top.length; i += 2 + Math.floor(r() * 4)) {
    const [x, y] = top[i], h = 34 + r() * 74, w = h * .3;
    for (let s = 0; s < 3; s++) { const ty = y - h * s / 3.2, tw = w * (1 - s / 4);
      ctx.beginPath(); ctx.moveTo(x - tw, ty + 3); ctx.lineTo(x, ty - h * .5); ctx.lineTo(x + tw, ty + 3); ctx.fill(); }
    ctx.fillRect(x - 2, y - 4, 4, 10);
  }
}
function figure(ctx, top, col) {
  const i = Math.round(top.length * (D.scene.figure_x || .64)), [x, y] = top[i];
  ctx.save(); ctx.fillStyle = col; ctx.translate(x, y + 3); const s = 1.08; ctx.scale(s, s);
  ctx.beginPath(); ctx.arc(0, -93, 9, 0, 7); ctx.fill(); ctx.fillRect(-3.5, -87, 7, 9);
  ctx.beginPath(); ctx.moveTo(-12, -80); ctx.quadraticCurveTo(0, -85, 12, -80); ctx.lineTo(14, -44); ctx.lineTo(9, -42);
  ctx.lineTo(7.5, 0); ctx.lineTo(2, 0); ctx.lineTo(0, -36); ctx.lineTo(-2, 0); ctx.lineTo(-7.5, 0); ctx.lineTo(-9, -42);
  ctx.lineTo(-14, -44); ctx.closePath(); ctx.fill(); ctx.restore();
}
function ridge(ctx, r, base, amp, period, col) {
  const nz = noise(r), top = [];
  ctx.fillStyle = col; ctx.beginPath(); ctx.moveTo(0, H);
  for (let x = -6; x <= W + 12; x += 6) {
    let y = 0, a = 1, f = 1 / period, tot = 0;
    for (let o = 0; o < 5; o++) { y += a * nz(x * f + o * 37.1 + 11); tot += a; a *= .5; f *= 2.07; }
    const yy = base - amp * (y / tot - .35); ctx.lineTo(x, yy); top.push([x, yy]);
  }
  ctx.lineTo(W, H); ctx.closePath(); ctx.fill();
  return top;
}
function drawScene(cv) {
  const sc = D.scene, P = PAL[sc.palette] || PAL.dusk, r = rng32(sc.seed || 7), ctx = cv.getContext('2d'), HZ = P.hz;
  let g = ctx.createLinearGradient(0, 0, 0, HZ + 160);
  g.addColorStop(0, P.sky[0]); g.addColorStop(.55, P.sky[1]); g.addColorStop(1, P.sky[2]);
  ctx.fillStyle = g; ctx.fillRect(0, 0, W, H);
  if (P.stars) for (let i = 0; i < 360; i++) { const y = Math.pow(r(), 1.6) * HZ * .85, x = r() * W;
    ctx.globalAlpha = (.2 + .8 * r()) * (1 - y / HZ); ctx.fillStyle = '#fff'; ctx.beginPath(); ctx.arc(x, y, .5 + r() * 1.4, 0, 7); ctx.fill(); }
  ctx.globalAlpha = 1;
  const sx = W * (.2 + .6 * r()), sy = HZ - 45 - r() * 55;          // low, near the horizon: never behind the text
  g = ctx.createRadialGradient(sx, sy, 0, sx, sy, 680);
  g.addColorStop(0, rgba(P.glow, .55)); g.addColorStop(.3, rgba(P.glow, .17)); g.addColorStop(1, rgba(P.glow, 0));
  ctx.fillStyle = g; ctx.fillRect(0, 0, W, H);
  if (P.disc) { ctx.save(); ctx.fillStyle = rgba(P.glow, .96); ctx.shadowColor = rgba(P.glow, .95); ctx.shadowBlur = 70;
    ctx.beginPath(); ctx.arc(sx, sy, 56, 0, 7); ctx.fill(); ctx.restore(); }
  ctx.filter = 'blur(26px)';
  for (let i = 0; i < 8; i++) { ctx.fillStyle = rgba(P.glow, .05 + .07 * r());
    ctx.beginPath(); ctx.ellipse(r() * W, HZ - 80 - r() * 760, 260 + r() * 560, 14 + r() * 30, 0, 0, 7); ctx.fill(); }
  ctx.filter = 'none';
  if (sc.sea) {
    ridge(ctx, r, HZ + 10, 120, 300, mix(P.far, P.near, .25));
    g = ctx.createLinearGradient(0, HZ + 40, 0, H);
    g.addColorStop(0, mix(P.sky[2], P.near, .45)); g.addColorStop(1, P.near);
    ctx.fillStyle = g; ctx.fillRect(0, HZ + 40, W, H - HZ - 40);
    ctx.filter = 'blur(1.6px)';
    for (let y = HZ + 46; y < H; y += 4 + r() * 6) {
      const d = (y - HZ) / (H - HZ), w = 20 + (40 + d * 380) * r(), a = .5 * (1 - d) * (.3 + .7 * r());
      ctx.fillStyle = rgba(P.glow, a); ctx.fillRect(sx - w / 2 + (r() - .5) * 90 * d, y, w, 2 + d * 3);
    }
    ctx.filter = 'none';
    const shore = ridge(ctx, r, H - 150, 90, 260, P.near);
    if (sc.figure) figure(ctx, shore, P.near);
  } else {
    const N = 5;
    for (let k = 0; k < N; k++) {
      const t = k / (N - 1), col = mix(P.far, P.near, Math.pow(t, .75));
      const top = ridge(ctx, r, HZ + 40 + t * 500, 250 - t * 90, 400 - t * 130, col);
      if (sc.trees && k >= N - 2) trees(ctx, r, top, col);
      if (sc.figure && k === N - 1) figure(ctx, top, col);
      if (k < N - 1) { const fy = HZ + 100 + t * 500; g = ctx.createLinearGradient(0, fy - 260, 0, fy + 160);
        g.addColorStop(0, rgba(P.fog, 0)); g.addColorStop(.7, rgba(P.fog, .24 - t * .13)); g.addColorStop(1, rgba(P.fog, 0));
        ctx.fillStyle = g; ctx.fillRect(0, fy - 260, W, 420); }
    }
  }
  const gc = document.createElement('canvas'); gc.width = 540; gc.height = 960;
  const c2 = gc.getContext('2d'), im = c2.createImageData(540, 960);
  for (let i = 0; i < im.data.length; i += 4) { const v = 128 + (r() - .5) * 130; im.data[i] = im.data[i + 1] = im.data[i + 2] = v; im.data[i + 3] = 255; }
  c2.putImageData(im, 0, 0); ctx.globalCompositeOperation = 'overlay'; ctx.globalAlpha = .16; ctx.drawImage(gc, 0, 0, W, H);
  ctx.globalAlpha = 1; ctx.globalCompositeOperation = 'source-over';
  g = ctx.createRadialGradient(W / 2, H * .45, H * .25, W / 2, H * .45, H * .75);
  g.addColorStop(0, 'rgba(0,0,0,0)'); g.addColorStop(1, 'rgba(0,0,0,.55)'); ctx.fillStyle = g; ctx.fillRect(0, 0, W, H);
}
function esc(s) { return s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'); }
function quoteHtml() {
  let q = D.en;
  for (const w of D.words) q = q.replace(new RegExp('\\b(' + esc(w.en) + ')\\b', 'i'), `<span class="k" style="${A('kOn', .5, T.fa + .5)}">$1</span>`);
  return q;
}
function build() {
  const n = D.en.length, fs = n <= 40 ? 80 : n <= 70 ? 70 : n <= 100 ? 62 : 56;
  return `<div id="scene"><canvas id="cv" width="1080" height="1920" style="${A('kb', T.total, 0, 'linear')}"></canvas></div><div id="shade"></div>` +
    `<div class="handle" dir="ltr">${D.handle}</div><div class="block">` +
    `<div class="en" style="font-size:${fs}px;${A('qin', .7, 0, ez)}">“${quoteHtml()}”</div>` +
    (D.author ? `<div class="au" style="${A('fade', .5, .35)}">— ${D.author}</div>` : '') +
    `<div class="sep" style="${A('grow', .45, T.fa - .25, ez)}"></div>` +
    `<div class="fa" style="${A('up', .6, T.fa, ez)}">${D.fa}</div></div>`;     // no follow line: people re-share it to their stories
}
function fitAll(maxW = 912) {
  document.querySelectorAll('.block > *').forEach(el => { if (el.scrollWidth > maxW) el.style.zoom = (maxW / el.scrollWidth).toFixed(3); });
}
window.show = async () => {
  document.getElementById('stage').innerHTML = build(); drawScene(document.getElementById('cv'));
  fitAll(); window.seek(0);
  const b = document.querySelector('.block').getBoundingClientRect(), kids = [...document.querySelectorAll('.block > *')];
  return {top: Math.round(kids[0].getBoundingClientRect().top), bottom: Math.round(kids[kids.length - 1].getBoundingClientRect().bottom)};
};
window.seek = (ms) => { for (const a of document.getAnimations()) { a.pause(); a.currentTime = ms; } };
window.ready = async () => {
  await Promise.all([document.fonts.load('italic 500 60px QSERIF', 'Ab'), document.fonts.load('400 50px Vaz', 'سلام'),
                     document.fonts.load('500 40px Lora', 'Ab'), document.fonts.load('600 30px Pop', '@a')]);
  return document.fonts.check('italic 500 60px QSERIF', 'Ab');
};
"""


def main(path, preview=False, serif="Play"):
    d = json.load(open(path))
    bdir = os.path.join(HERE, "build", d["tag"]); os.makedirs(bdir, exist_ok=True)
    fa_t = min(4.0, max(2.2, 0.6 + 0.045 * len(d["en"])))          # time to read the English first
    T = dict(fa=round(fa_t, 2), total=round(fa_t + HOLD, 2))
    html = os.path.join(bdir, "q.html")
    js = JS.replace("__DATA__", json.dumps(d, ensure_ascii=False)).replace("__T__", json.dumps(T)).replace("QSERIF", serif)
    open(html, "w", encoding="utf-8").write("<!doctype html><html lang='fa'><head><meta charset='utf-8'><style>" + font_css() + serif_css() +
        QCSS.replace("QSERIF", serif) + "</style></head><body><div id='stage'></div><script>" + js + "</script></body></html>")
    with sync_playwright() as p:
        exe = "/usr/bin/google-chrome" if os.path.exists("/usr/bin/google-chrome") else None
        b = p.chromium.launch(executable_path=exe, args=["--no-sandbox", "--disable-gpu", "--font-render-hinting=none"])
        pg = b.new_page(viewport={"width": W, "height": H}); pg.goto("file://" + html); print("fonts ok:", pg.evaluate("ready()"))
        box = pg.evaluate("show()"); print("text block y:", box)
        if preview:
            for t in (0.0, T["total"] - 0.1):
                pg.evaluate(f"seek({t * 1000})"); pg.screenshot(path=os.path.join(bdir, f"prev_{t:g}.jpg"), type="jpeg", quality=88)
            b.close(); print("previews in", bdir, "| total", T["total"], "s"); return
        video = os.path.join(bdir, "video.mp4"); tmp = video[:-4] + ".part.mp4"
        proc = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "image2pipe", "-framerate", str(FPS), "-c:v", "mjpeg", "-i", "-",
                                 "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p", "-r", str(FPS), tmp], stdin=subprocess.PIPE)
        for f in range(round(T["total"] * FPS)):
            pg.evaluate(f"seek({f * 1000 / FPS})"); proc.stdin.write(pg.screenshot(type="jpeg", quality=92))
        proc.stdin.close()
        if proc.wait() != 0: raise SystemExit("ffmpeg failed")
        os.replace(tmp, video); b.close()
    total = T["total"]
    wav = music_bed(total, os.path.join(bdir, "music.wav"), d.get("day", 0))
    out = os.path.join(HERE, "out", f"{d['tag']}.mp4"); tmp = out[:-4] + ".part.mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", video, "-i", wav, "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac",
                    "-b:a", "160k", "-ar", "44100", "-ac", "2", "-shortest", "-movflags", "+faststart", tmp], check=True)
    os.replace(tmp, out); print("quote reel:", out, total, "s")


if __name__ == "__main__":
    a = sys.argv[1:]
    main(a[0], preview="--preview" in a, serif=a[a.index("--serif") + 1] if "--serif" in a else "Play")
