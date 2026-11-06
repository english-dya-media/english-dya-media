"""Render a day's reel (MP4) and stories (JPEG) from content/dayXX.json.

  python3 render.py content/day01.json --preview   # a few still frames to check layout
  python3 render.py content/day01.json             # full reel + stories into out/
"""
import base64, json, os, subprocess, sys
from playwright.sync_api import sync_playwright
from music import make_music
import soundfile as sf

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(HERE, "assets", "fonts")
EMO = "file://" + os.path.join(HERE, "assets", "emoji")
SFX = os.path.join(HERE, "assets", "sfx")
W, H, FPS = 1080, 1920, 30

HOOK, WORD, END = 2.4, 5.2, 3.0
T = dict(emoji=0.10, word=0.30, tts1=0.75, wrong=1.25, strike=1.45, silent=1.85,
         right=2.35, meaning=2.65, repeat=3.05, tts2=3.15)


def font_css():
    faces = [("Vaz", "Vazirmatn.woff2", "100 900"),
             ("Pop", "poppins-latin-600-normal.woff2", "600"),
             ("Pop", "poppins-latin-700-normal.woff2", "700"),
             ("Pop", "poppins-latin-800-normal.woff2", "800"),
             ("NotoL", "noto-sans-latin-500-normal.woff2", "500"),
             ("NotoX", "noto-sans-latin-ext-500-normal.woff2", "500")]
    out = []
    for fam, fn, wt in faces:
        b = base64.b64encode(open(os.path.join(FONTS, fn), "rb").read()).decode()
        out.append("@font-face{font-family:%s;src:url(data:font/woff2;base64,%s) format('woff2');"
                   "font-weight:%s;font-display:block;}" % (fam, b, wt))
    return "\n".join(out)


CSS = r"""
:root{--bad:#FF5C7A;--good:#2EE59D;--acc:#FFD43B;--txt:#F8FAFC;--mut:#AAB4F8;}
*{box-sizing:border-box}
html,body{margin:0;width:1080px;height:1920px;overflow:hidden;background:#0A0D22;}
body{font-family:Vaz,sans-serif;color:var(--txt);}
#bg{position:absolute;inset:0;
 background:
  radial-gradient(760px 640px at 86% 88%, rgba(255,212,59,.13), rgba(255,212,59,0) 70%),
  radial-gradient(700px 600px at 8% 72%, rgba(46,229,157,.10), rgba(46,229,157,0) 70%),
  radial-gradient(1000px 900px at 50% 30%, #252A7E 0%, rgba(37,42,126,0) 72%),
  linear-gradient(180deg,#10143A 0%,#0A0D22 100%);}
#dots{position:absolute;inset:0;background-image:radial-gradient(rgba(255,255,255,.07) 2px, transparent 2px);
 background-size:40px 40px;-webkit-mask:linear-gradient(180deg,#000 0%,rgba(0,0,0,.25) 60%,transparent 100%);}
#stage{position:absolute;inset:0;}
.line{position:absolute;left:0;right:0;display:flex;justify-content:center;}
.handle{padding:8px 30px;border-radius:999px;background:rgba(255,255,255,.08);border:2px solid rgba(255,255,255,.14);
 font:600 34px Pop;letter-spacing:.5px;color:#E7EAFF;}
.prog{display:flex;flex-direction:row-reverse;gap:14px;}
.prog span{width:22px;height:22px;border-radius:11px;background:rgba(255,255,255,.18);}
.prog span.done{background:rgba(255,212,59,.55);} .prog span.on{width:64px;background:var(--acc);}
.glow{position:absolute;left:50%;width:640px;height:640px;margin-left:-320px;border-radius:50%;
 background:radial-gradient(closest-side, rgba(120,128,255,.55), rgba(120,128,255,0));}
.ring{position:absolute;left:50%;border-radius:50%;
 background:conic-gradient(from 0deg, rgba(255,212,59,0), rgba(255,212,59,.65), rgba(46,229,157,.55), rgba(255,212,59,0) 70%);
 -webkit-mask:radial-gradient(farthest-side, transparent calc(100% - 7px), #000 calc(100% - 6px));}
.emowrap{position:absolute;left:50%;}
.emowrap img{width:100%;height:100%;object-fit:contain;filter:drop-shadow(0 26px 40px rgba(0,0,0,.45));}
.en{font-family:Pop;font-weight:800;line-height:1.05;letter-spacing:1px;color:#fff;text-shadow:0 8px 30px rgba(0,0,0,.35);}
.sil{position:relative;display:inline-block;}
.sbar{position:absolute;left:-10%;right:-10%;top:52%;height:13px;margin-top:-6px;background:var(--bad);border-radius:7px;transform-origin:left center;}
.pill{direction:rtl;display:flex;align-items:center;gap:12px;padding:6px 26px;border-radius:999px;white-space:nowrap;}
.spill{background:rgba(255,92,122,.14);border:2px solid rgba(255,92,122,.6);font:600 40px/1.35 Vaz;}
.spill b{font:800 42px Pop;color:var(--bad);padding:0 6px;}
.pill img{width:50px;height:50px;}
.row{direction:rtl;display:flex;align-items:center;gap:18px;white-space:nowrap;}
.row > img{width:64px;height:64px;}
.wrong .lbl{font:600 40px Vaz;color:var(--mut);}
.wrong .w{position:relative;font:800 60px/1.3 Vaz;color:#FFB3C1;}
.wbar{position:absolute;right:-8px;left:-8px;top:54%;height:8px;margin-top:-4px;background:var(--bad);border-radius:4px;transform-origin:right center;}
.right .r{font:900 92px/1.2 Vaz;color:var(--good);}
.right .ipa{font:500 54px NotoL,NotoX,'DejaVu Sans',sans-serif;color:#CFE9FF;margin-right:8px;}
.mean{direction:rtl;padding:6px 36px 10px;border-radius:24px;background:var(--acc);color:#14162E;font:700 56px/1.35 Vaz;
 box-shadow:0 12px 30px rgba(255,212,59,.22);white-space:nowrap;}
.mean b{font-weight:900;}
.rep{border:2px solid rgba(255,255,255,.35);font:600 40px/1.35 Vaz;background:rgba(255,255,255,.06);}
.hook{position:absolute;left:0;right:0;text-align:center;direction:rtl;}
.h1{font:800 96px/1.3 Vaz;} .h2{font:900 138px/1.3 Vaz;}
.h3{font:800 96px/1.3 Vaz;display:flex;justify-content:center;align-items:center;gap:22px;}
.h3 img{width:118px;height:118px;}
.hl{position:relative;z-index:0;padding:0 20px;display:inline-block;}
.hl i{position:absolute;inset:14% -2% 6% -2%;background:var(--bad);border-radius:20px;z-index:-1;transform:skewX(-8deg);transform-origin:right center;}
.hrow{gap:38px;flex-direction:row-reverse;} .hrow img{width:168px;height:168px;filter:drop-shadow(0 16px 26px rgba(0,0,0,.4));}
.hsub{border:3px solid var(--acc);color:var(--acc);font:700 48px/1.35 Vaz;padding:8px 34px;}
.hsub img{width:60px;height:60px;}
.e1{direction:rtl;font:900 84px/1.3 Vaz;text-align:center;}
.e2{direction:rtl;display:flex;align-items:center;gap:16px;font:800 72px/1.3 Vaz;color:var(--acc);}
.e2 img{width:96px;height:96px;}
.e3{direction:rtl;font:600 48px/1.35 Vaz;color:var(--mut);display:flex;align-items:center;gap:12px;}
.e3 img{width:58px;height:58px;}
/* stories */
.kick{background:var(--acc);color:#14162E;font:800 52px/1.35 Vaz;padding:8px 36px;}
.kick img{width:64px;height:64px;}
.tiles{direction:ltr;display:flex;gap:12px;}
.tiles span{width:112px;height:144px;border-radius:22px;display:flex;align-items:center;justify-content:center;
 background:rgba(255,255,255,.08);border:2px solid rgba(255,255,255,.22);font:800 96px Pop;color:#fff;}
.q{direction:rtl;width:920px;text-align:center;font:900 78px/1.35 Vaz;}
.hint{border:2px solid rgba(170,180,248,.5);color:var(--mut);font:600 44px/1.35 Vaz;}
.cta{background:var(--acc);color:#14162E;font:900 60px/1.35 Vaz;padding:12px 44px;box-shadow:0 16px 40px rgba(255,212,59,.3);}
.cta img{width:80px;height:80px;}
.chev{position:absolute;left:50%;width:56px;height:56px;margin-left:-28px;border-right:9px solid var(--acc);border-bottom:9px solid var(--acc);transform:rotate(45deg);border-radius:4px;}
.t1{direction:rtl;font:800 92px/1.3 Vaz;text-align:center;}
.t2{direction:rtl;font:900 104px/1.3 Vaz;text-align:center;}
.body{direction:rtl;width:880px;text-align:center;font:600 54px/1.55 Vaz;color:#D5DAFF;}
.bubble{direction:rtl;background:#fff;color:#14162E;border-radius:44px 44px 44px 12px;padding:14px 40px;font:700 50px/1.35 Vaz;
 display:flex;gap:14px;align-items:center;box-shadow:0 16px 40px rgba(0,0,0,.35);}
.bubble b{font:700 52px Pop;color:#3B3FD8;}
.mk{position:relative;display:inline-block;}
.ubar{position:absolute;left:-4%;right:-4%;bottom:-4px;height:12px;background:var(--acc);border-radius:6px;transform-origin:left center;}
.gpill{background:rgba(255,212,59,.12);border:2px solid rgba(255,212,59,.6);font:600 40px/1.35 Vaz;}
.gpill b{font:800 42px Pop;color:var(--acc);padding:0 6px;}
.ttl{direction:rtl;font:900 112px/1.25 Vaz;color:var(--acc);}
.wcard{background:#fff;color:#14162E;border-radius:36px;padding:14px 56px 22px;display:flex;flex-direction:column;align-items:center;box-shadow:0 20px 50px rgba(0,0,0,.35);}
.wcard .w{font-family:Pop;font-weight:800;line-height:1.15;}
.wcard .p{font:500 50px NotoL,NotoX,'DejaVu Sans',sans-serif;color:#4A4F86;}
.opts{display:flex;flex-direction:column;gap:22px;width:820px;}
.opt{direction:rtl;display:flex;align-items:center;gap:28px;background:rgba(255,255,255,.07);border:2px solid rgba(255,255,255,.22);border-radius:28px;padding:14px 26px;font:800 64px/1.3 Vaz;}
.opt b{flex:none;width:104px;height:104px;border-radius:52px;background:var(--acc);color:#14162E;display:flex;align-items:center;justify-content:center;font:900 42px Vaz;}
.bigw{font-family:Pop;font-weight:800;line-height:1.1;color:#fff;text-shadow:0 8px 30px rgba(0,0,0,.35);}
@keyframes glowOn{to{color:var(--acc);text-shadow:0 0 28px rgba(255,212,59,.55)}}
@keyframes popIn{0%{transform:scale(.2) rotate(-10deg);opacity:0}60%{transform:scale(1.1) rotate(3deg);opacity:1}100%{transform:scale(1) rotate(0)}}
@keyframes popSmall{0%{transform:scale(.6);opacity:0}70%{transform:scale(1.05);opacity:1}100%{transform:scale(1);opacity:1}}
@keyframes slideUp{from{transform:translateY(46px);opacity:0}to{transform:none;opacity:1}}
@keyframes fadeIn{from{opacity:0}to{opacity:1}}
@keyframes strike{from{transform:scaleX(0)}to{transform:scaleX(1)}}
@keyframes silentFade{to{color:rgba(255,92,122,.6)}}
@keyframes pulse{0%,100%{transform:scale(1)}50%{transform:scale(1.09)}}
@keyframes punch{from{transform:scale(1.12)}to{transform:scale(1)}}
@keyframes bob{0%,100%{transform:translateY(0)}50%{transform:translateY(-14px)}}
@keyframes spin{to{transform:rotate(360deg)}}
@keyframes hlGrow{from{transform:skewX(-8deg) scaleX(0)}to{transform:skewX(-8deg) scaleX(1)}}
"""

JS = r"""
const D = __DATA__, T = __T__, E = n => '__EMO__/' + n + '.png';
const ez = 'cubic-bezier(.2,.8,.2,1)', bo = 'cubic-bezier(.2,.9,.3,1.3)';
const A = (n, d, dl, f = 'ease-out', it = 1) => `animation:${n} ${d}s ${f} ${dl}s ${it} normal both;`;
const L = (top, inner) => `<div class="line" style="top:${top}px">${inner}</div>`;
function header(active) {
  let h = L(236, `<div class="handle" dir="ltr">${D.handle}</div>`);
  if (active >= 0) h += L(318, '<div class="prog">' + [0,1,2,3].map(i =>
      `<span class="${i === active ? 'on' : (i < active ? 'done' : '')}"></span>`).join('') + '</div>');
  return h;
}
function halo(cy, size) {
  return `<div class="glow" style="top:${cy - 320}px"></div>` +
    `<div class="ring" style="top:${cy - size/2 - 34}px;width:${size + 68}px;height:${size + 68}px;margin-left:-${size/2 + 34}px;${A('spin', 7, 0, 'linear', 'infinite')}"></div>`;
}
function emo(name, cy, size, delay, idle = true) {
  const wrap = `top:${cy - size/2}px;width:${size}px;height:${size}px;margin-left:-${size/2}px;` +
    (idle ? A('bob', 2.6, delay + 0.6, 'ease-in-out', 'infinite') : '');
  return `<div class="emowrap" style="${wrap}"><img src="${E(name)}" style="${A('popIn', .55, delay, bo)}"></div>`;
}
function hookScene() {
  const h = D.hook;
  const row = D.words.map((w, k) => `<img src="${E(w.emoji)}" style="${A('popIn', .45, .25 + k * .15, bo)}">`).join('');
  return header(-1) + `<div class="glow" style="top:300px;width:900px;height:900px;margin-left:-450px"></div>` +
    `<div class="hook" style="top:470px;${A('punch', .45, 0, ez)}">
       <div class="h1">${h.l1}</div>
       <div class="h2">${h.l2a} <span class="hl"><i style="${A('hlGrow', .3, .05, ez)}"></i>${h.l2b}</span></div>
       <div class="h3">${h.l3}<img src="${E(h.l3emoji)}"></div></div>` +
    L(1010, `<div class="hrow line" style="position:static">${row}</div>`) +
    L(1236, `<div class="pill hsub" style="${A('slideUp', .4, .9, ez)}">${h.sub}<img src="${E(h.subemoji)}"></div>`);
}
function wordScene(i) {
  const w = D.words[i];
  const marks = w.mark || w.silent || [], glow = w.mark_style === 'glow';
  const letters = [...w.en].map((ch, j) => !marks.includes(j) ? ch : glow
    ? `<span class="mk" style="${A('glowOn', .3, T.silent)}">${ch}<i class="ubar" style="${A('strike', .3, T.silent, ez)}"></i></span>`
    : `<span class="sil" style="${A('silentFade', .3, T.silent)}">${ch}<i class="sbar" style="${A('strike', .3, T.silent, ez)}"></i></span>`).join('');
  const n = w.en.length, fs = n <= 6 ? 150 : n <= 9 ? 128 : n <= 11 ? 112 : 100;
  const tip = w.tip ? w.tip.replace('{EN}', `<b dir="ltr">${w.tip_en}</b>`) : D.labels.silent.replace('{L}', `<b dir="ltr">${w.letter}</b>`);
  const tipEmo = w.tip_emoji || (glow ? 'light_bulb' : 'shushing_face');
  return header(i) + halo(580, 360) + emo(w.emoji, 580, 360, T.emoji) +
    L(792 + (150 - fs) / 2, `<div class="en" dir="ltr" style="font-size:${fs}px;${A('slideUp', .45, T.word, ez)}">${letters}</div>`) +
    L(966, `<div class="pill ${glow ? 'gpill' : 'spill'}" style="${A('slideUp', .35, T.silent, ez)}">${tip}<img src="${E(tipEmo)}"></div>`) +
    L(1058, `<div class="row wrong" style="${A('slideUp', .35, T.wrong, ez)}"><img src="${E('cross_mark')}"><span class="lbl">${D.labels.wrong}:</span>` +
            `<span class="w">${w.wrong}<i class="wbar" style="${A('strike', .3, T.strike)}"></i></span></div>`) +
    L(1140, `<div class="row right" style="${A('slideUp', .4, T.right, ez)}"><img src="${E('check_mark_button')}"><span class="r">${w.right}</span><span class="ipa" dir="ltr">${w.ipa}</span></div>`) +
    L(1268, `<div class="mean" style="${A('popSmall', .4, T.meaning, bo)}">${D.labels.meaning}: <b>${w.fa}</b></div>`) +
    L(1376, `<div style="${A('fadeIn', .3, T.repeat)}"><div class="pill rep" style="${A('pulse', .5, T.tts2, 'ease-in-out', 2)}">` +
            `<img src="${E('speaker_high_volume')}"><span>${D.labels.repeat}</span></div></div>`);
}
function endScene() {
  const e = D.end;
  return header(-1) + halo(600, 300) + emo(e.emoji, 600, 300, .1) +
    L(800, `<div class="e1" style="${A('slideUp', .4, .35, ez)}">${e.e1}</div>`) +
    L(938, `<div class="e2" style="${A('slideUp', .4, .65, ez)}"><span>${e.e2}</span><img src="${E('backhand_index_pointing_down')}" style="${A('bob', .7, 1.0, 'ease-in-out', 'infinite')}"></div>`) +
    L(1080, `<div class="e3" style="${A('fadeIn', .4, 1.0)}">${e.e3}<img src="${E('sparkles')}"></div>`);
}
function ctaBlock(text) {
  return L(1440, `<div class="pill cta">${text}<img src="${E('backhand_index_pointing_down')}"></div>`) +
    `<div class="chev" style="top:1572px"></div><div class="chev" style="top:1612px;opacity:.55"></div>`;
}
function storyQuiz(s) {
  const n = s.word.length, tw = Math.min(112, Math.floor((960 - (n - 1) * 12) / n));
  const tiles = [...s.word].map(c => `<span style="width:${tw}px;height:${Math.round(tw * 1.29)}px;font-size:${Math.round(tw * .86)}px">${c}</span>`).join('');
  return L(290, `<div class="pill kick"><img src="${E(s.kicker_emoji)}">${s.kicker}</div>`) +
    halo(630, 340) + emo(s.emoji, 630, 340, 0, false) +
    L(870, `<div class="tiles">${tiles}</div>`) +
    L(1060, `<div class="q">${s.q.replace(/\n/g, '<br>')}</div>`) +
    L(1296, `<div class="pill hint">${s.hint}</div>`) + ctaBlock(s.cta);
}
function storyAsk(s) {
  return halo(560, 300) + emo(s.emoji, 560, 300, 0, false) +
    L(760, `<div class="t1">${s.t1}</div>`) +
    L(872, `<div class="t2">${s.t2a} <span class="hl"><i></i>${s.t2b}</span></div>`) +
    L(1060, `<div class="body">${s.body.replace(/\n/g, '<br>')}</div>`) +
    L(1262, `<div class="bubble"><span>${s.example_label}</span><b dir="ltr">${s.example}</b></div>`) + ctaBlock(s.cta);
}
function storyRecall(s) {
  const n = s.word.length, fs = n <= 6 ? 150 : n <= 9 ? 124 : 100;
  return L(290, `<div class="pill kick"><img src="${E(s.kicker_emoji)}">${s.kicker}</div>`) +
    halo(530, 220) + emo(s.emoji || 'brain', 530, 220, 0, false) +
    L(672, `<div class="ttl">${s.title}</div>`) +
    L(830, `<div class="wcard"><span class="w" dir="ltr" style="font-size:${fs}px">${s.word}</span><span class="p" dir="ltr">${s.ipa}</span></div>`) +
    L(1130, `<div class="q">${s.q}</div>`) +
    L(1282, `<div class="pill hint">${s.hint}</div>`) + ctaBlock(s.cta);
}
function storyMcq(s) {
  const n = s.word.length, fs = n <= 6 ? 150 : n <= 9 ? 128 : 104;
  const tags = ['الف', 'ب', 'ج'];
  const opts = s.options.map((o, k) => `<div class="opt"><b>${tags[k]}</b><span>${o}</span></div>`).join('');
  return L(290, `<div class="pill kick"><img src="${E(s.kicker_emoji)}">${s.kicker}</div>`) +
    L(430, `<div class="bigw" dir="ltr" style="font-size:${fs}px">${s.word}</div>`) +
    L(610, `<div class="q">${s.q}</div>`) +
    L(756, `<div class="opts">${opts}</div>`) +
    L(1268, `<div class="pill hint">${s.hint}</div>`) + ctaBlock(s.cta);
}
function fitAll(maxW = 1000) {
  const fitted = [];
  document.querySelectorAll('.line > *, .hook > *').forEach(el => {
    el.style.zoom = '';
    const prevW = el.style.width;
    el.style.width = 'max-content';
    const w = el.offsetWidth;
    if (w > maxW) {
      el.style.zoom = (maxW / w).toFixed(3);
      el.style.marginLeft = el.style.marginRight = 'auto';
      fitted.push(el.textContent.trim().slice(0, 40) + ' @' + w + 'px');
    } else {
      el.style.width = prevW;
    }
  });
  return fitted;
}
window.show = async (key) => {
  const st = document.getElementById('stage');
  st.innerHTML = key === 'hook' ? hookScene() : key === 'end' ? endScene()
    : String(key).startsWith('story') ? ({quiz: storyQuiz, ask: storyAsk, recall: storyRecall, mcq: storyMcq})[D.stories[+key.slice(5)].kind](D.stories[+key.slice(5)])
    : wordScene(+key);
  document.body.offsetHeight;
  await Promise.all([...document.images].map(im => im.decode().catch(() => {})));
  const fitted = fitAll();
  window.seek(0);
  return fitted;
};
window.seek = (ms) => { for (const a of document.getAnimations()) { a.pause(); a.currentTime = ms; } };
window.ready = async () => {
  await Promise.all([document.fonts.load('800 100px Pop', 'Ab'), document.fonts.load('600 40px Pop', 'Ab'),
    document.fonts.load('900 100px Vaz', 'سلام'), document.fonts.load('500 50px NotoL', 'ab'),
    document.fonts.load('500 50px NotoX', 'ˈɪəæɛ')]);
  await document.fonts.ready;
  return [document.fonts.check('800 100px Pop'), document.fonts.check('900 100px Vaz', 'سلام'), document.fonts.check('500 50px NotoX', 'ˈɪə')];
};
"""


def build_html(d, path):
    js = (JS.replace("__DATA__", json.dumps(d, ensure_ascii=False))
            .replace("__T__", json.dumps(T)).replace("__EMO__", EMO))
    html = ("<!doctype html><html lang='fa'><head><meta charset='utf-8'><style>" + font_css() + CSS +
            "</style></head><body><div id='bg'></div><div id='dots'></div><div id='stage'></div><script>" +
            js + "</script></body></html>")
    open(path, "w", encoding="utf-8").write(html)


def open_page(p, html):
    exe = "/usr/bin/google-chrome" if os.path.exists("/usr/bin/google-chrome") else None
    b = p.chromium.launch(executable_path=exe,
                          args=["--no-sandbox", "--disable-gpu", "--font-render-hinting=none", "--hide-scrollbars"])
    pg = b.new_page(viewport={"width": W, "height": H}, device_scale_factor=1)
    pg.goto("file://" + html)
    print("fonts ok:", pg.evaluate("ready()"))
    return b, pg


def encode_scene(pg, key, dur, path):
    fitted = pg.evaluate(f"show({json.dumps(key)})")
    if fitted:
        print(f"  shrunk to fit in scene {key}: {fitted}")
    tmp = path[:-4] + ".part.mp4"
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "image2pipe", "-framerate", str(FPS), "-c:v", "mjpeg", "-i", "-",
           "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-bf", "0", "-g", "60", "-pix_fmt", "yuv420p",
           "-r", str(FPS), "-video_track_timescale", "15360", tmp]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for f in range(round(dur * FPS)):
        pg.evaluate(f"seek({f * 1000 / FPS})")
        proc.stdin.write(pg.screenshot(type="jpeg", quality=92))
    proc.stdin.close()
    if proc.wait() != 0:
        raise SystemExit(f"ffmpeg failed on scene {key}")
    os.replace(tmp, path)


def audio_events(d, bdir):
    ev = [(0.0, f"{SFX}/whoosh.wav", 0.35)] + [(0.25 + k * .15, f"{SFX}/pop.wav", 0.30) for k in range(len(d["words"]))]
    t0 = HOOK
    for i in range(len(d["words"])):
        ev += [(t0, f"{SFX}/whoosh.wav", 0.30), (t0 + T["emoji"], f"{SFX}/pop.wav", 0.32),
               (t0 + T["tts1"], f"{bdir}/tts_{i}_normal.wav", 1.0), (t0 + T["wrong"], f"{SFX}/boop.wav", 0.30),
               (t0 + T["silent"], f"{SFX}/tick.wav", 0.30), (t0 + T["right"], f"{SFX}/ding.wav", 0.28),
               (t0 + T["tts2"], f"{bdir}/tts_{i}_slow.wav", 1.0)]
        t0 += WORD
    ev += [(t0, f"{SFX}/whoosh.wav", 0.30), (t0 + 0.1, f"{SFX}/pop.wav", 0.32), (t0 + 0.65, f"{SFX}/ding.wav", 0.22)]
    total = t0 + END
    voice = [(t, t + sf.info(f).duration) for t, f, _ in ev if "/tts_" in f]
    ev.insert(0, (0.0, make_music(total, voice, os.path.join(bdir, "music.wav")), 1.0))
    return ev, total


def build_audio(events, total, out):
    inputs, fl = [], []
    for k, (t, f, vol) in enumerate(events):
        inputs += ["-i", f]
        fl.append(f"[{k}:a]aresample=44100,aformat=sample_fmts=fltp:channel_layouts=mono,volume={vol},adelay={int(t * 1000)}:all=1[a{k}]")
    fl.append("".join(f"[a{k}]" for k in range(len(events))) +
              f"amix=inputs={len(events)}:normalize=0:duration=longest,apad=whole_dur={total},atrim=0:{total},alimiter=limit=0.95[out]")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *inputs, "-filter_complex", ";".join(fl),
                    "-map", "[out]", "-ac", "2", "-ar", "44100", out], check=True)


def main(day_json, preview=False, audio_only=False, stories_only=False, fit_check=False):
    d = json.load(open(day_json))
    tag = f"day{d['day']:02d}"
    bdir = os.path.join(HERE, "build", tag)
    odir = os.path.join(HERE, "out")
    os.makedirs(bdir, exist_ok=True); os.makedirs(odir, exist_ok=True)
    html = os.path.join(bdir, "reel.html")
    build_html(d, html)
    if audio_only:
        return mux(d, bdir, odir, tag)
    with sync_playwright() as p:
        b, pg = open_page(p, html)
        if stories_only:
            for k in range(len(d["stories"])):
                fitted = pg.evaluate(f"show('story{k}')"); pg.evaluate("seek(10000)")
                if fitted:
                    print(f"  shrunk to fit in story {k + 1}: {fitted}")
                pg.screenshot(path=os.path.join(odir, f"{tag}_story{k + 1}.jpg"), type="jpeg", quality=95)
            b.close(); print("stories done"); return
        if fit_check:
            keys = ["hook"] + list(range(len(d["words"]))) + ["end"] + [f"story{k}" for k in range(len(d["stories"]))]
            for key in keys:
                fitted = pg.evaluate(f"show({json.dumps(key)})")
                if fitted:
                    print(f"  {tag} {key}: {fitted}")
            b.close(); return
        if preview:
            for key, t in [("hook", 1.3), (0, 4.9), (3, 4.9)] + [(f"story{k}", 10) for k in range(len(d["stories"]))]:
                pg.evaluate(f"show({json.dumps(key)})"); pg.evaluate(f"seek({t * 1000})")
                pg.screenshot(path=os.path.join(bdir, f"preview_{key}.jpg"), type="jpeg", quality=88)
            print("previews in", bdir)
            b.close(); return
        for k in range(len(d["stories"])):
            fitted = pg.evaluate(f"show('story{k}')"); pg.evaluate("seek(10000)")
            if fitted:
                print(f"  shrunk to fit in story {k + 1}: {fitted}")
            pg.screenshot(path=os.path.join(odir, f"{tag}_story{k + 1}.jpg"), type="jpeg", quality=95)
        scenes = [("hook", HOOK)] + [(i, WORD) for i in range(len(d["words"]))] + [("end", END)]
        files = []
        for n, (key, dur) in enumerate(scenes):
            fp = os.path.join(bdir, f"scene{n:02d}.mp4")
            encode_scene(pg, key, dur, fp); files.append(fp); print("scene", key, "done")
        b.close()
    mux(d, bdir, odir, tag, files)


def mux(d, bdir, odir, tag, files=None):
    if files:
        lst = os.path.join(bdir, "list.txt")
        open(lst, "w").write("".join(f"file '{f}'\n" for f in files))
    video = os.path.join(bdir, "video.mp4")
    if files:
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", video], check=True)
    ev, total = audio_events(d, bdir)
    wav = os.path.join(bdir, "audio.wav")
    build_audio(ev, total, wav)
    out = os.path.join(odir, f"{tag}_reel.mp4")
    tmp = out[:-4] + ".part.mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", video, "-i", wav, "-map", "0:v", "-map", "1:a",
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "160k", "-ar", "44100", "-ac", "2", "-shortest",
                    "-movflags", "+faststart", "-use_editlist", "0", tmp], check=True)
    os.replace(tmp, out)
    print("reel:", out, "duration", total)


if __name__ == "__main__":
    main(sys.argv[1], preview="--preview" in sys.argv, audio_only="--audio-only" in sys.argv,
         stories_only="--stories" in sys.argv, fit_check="--fit-check" in sys.argv)
