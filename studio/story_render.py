"""Render one story episode as a reel.

  python3 story_render.py content/story_w01.json 1 --preview   # stills at busy moments
  python3 story_render.py content/story_w01.json 1             # full reel -> out/story_w01_e01.mp4
Needs build/story_wXX_eYY/timeline.json from tts_story.py.
"""
import json, os, subprocess, sys
import soundfile as sf
from playwright.sync_api import sync_playwright
from render import font_css, build_audio
from music import make_music

HERE = os.path.dirname(os.path.abspath(__file__))
EMO = "file://" + os.path.join(HERE, "assets", "emoji")
SFX = os.path.join(HERE, "assets", "sfx")
W, H, FPS = 1080, 1920, 30
MYSTERY = [[45, 48, 52, 55], [41, 45, 48, 52], [43, 47, 50, 53], [40, 44, 47, 50]]  # Am7 Fmaj7 G7 E7

CSS = r"""
:root{--ink:#1E1B2E;--paper:#FFFDF8;--acc:#FFD43B;--red:#D7263D;--wood:#E3B27C;--wood2:#C98E56;--cab:#7A5236;--cab2:#5E3D27;}
*{box-sizing:border-box}
html,body{margin:0;width:1080px;height:1920px;overflow:hidden;background:#F4E3CC;font-family:Vaz,sans-serif;}
#wall{position:absolute;left:0;top:0;width:1080px;height:1010px;
 background:
  linear-gradient(180deg,rgba(90,60,30,.10),rgba(90,60,30,0) 35%),
  repeating-linear-gradient(0deg, rgba(120,90,60,.07) 0 3px, transparent 3px 96px),
  repeating-linear-gradient(90deg, rgba(120,90,60,.07) 0 3px, transparent 3px 96px),
  linear-gradient(180deg,#F7E9D6,#F1DCC0);}
#win{position:absolute;left:640px;top:330px;width:330px;height:370px;border-radius:26px;background:#FFFFFF;padding:16px;box-shadow:0 10px 30px rgba(90,60,30,.18);}
#win .sky{position:relative;width:100%;height:100%;border-radius:14px;overflow:hidden;background:linear-gradient(180deg,#8FD3FF,#D9F1FF);}
#win .sky:before,#win .sky:after{content:'';position:absolute;background:#fff;}
#win .sky:before{left:50%;top:0;bottom:0;width:12px;margin-left:-6px;}
#win .sky:after{top:50%;left:0;right:0;height:12px;margin-top:-6px;}
#win .sun{position:absolute;left:40px;top:40px;width:70px;height:70px;border-radius:50%;background:#FFE27A;box-shadow:0 0 40px #FFE27A;}
#shelf{position:absolute;left:110px;top:520px;width:360px;height:22px;border-radius:8px;background:var(--wood2);box-shadow:0 8px 14px rgba(90,60,30,.18);}
.jar{position:absolute;bottom:22px;border-radius:14px 14px 10px 10px;}
#counter{position:absolute;left:0;top:1000px;width:1080px;height:84px;background:linear-gradient(180deg,#EDC48F,var(--wood) 60%,#D9A56C);}
#edge{position:absolute;left:0;top:1084px;width:1080px;height:30px;background:var(--wood2);box-shadow:0 10px 18px rgba(0,0,0,.18);}
#cab{position:absolute;left:0;top:1114px;width:1080px;height:806px;background:linear-gradient(180deg,var(--cab),var(--cab2));}
.door{position:absolute;top:1150px;width:470px;height:720px;border-radius:22px;border:6px solid rgba(255,255,255,.07);}
.knob{position:absolute;top:1260px;width:26px;height:26px;border-radius:50%;background:#E8C27C;box-shadow:0 3px 6px rgba(0,0,0,.3);}
.char{position:absolute;transform-origin:50% 92%;}
.char > img.body{position:absolute;inset:0;width:100%;height:100%;object-fit:contain;filter:drop-shadow(0 18px 18px rgba(80,40,10,.28));}
.shadow{position:absolute;height:34px;border-radius:50%;background:radial-gradient(closest-side,rgba(70,40,10,.35),rgba(70,40,10,0));}
.eye{position:absolute;background:#fff;border-radius:50%;box-shadow:inset 0 -5px 0 rgba(0,0,0,.08),0 3px 6px rgba(0,0,0,.25);overflow:hidden;}
.pupil{position:absolute;width:56%;height:56%;left:22%;top:22%;background:#1B1730;border-radius:50%;}
.pupil:after{content:'';position:absolute;width:34%;height:34%;left:16%;top:14%;background:#fff;border-radius:50%;}
.brow{position:absolute;background:#3B2626;border-radius:99px;}
.mouth{position:absolute;background:#4A1022;border-radius:45% 45% 55% 55% / 35% 35% 65% 65%;overflow:hidden;}
.mouth i{position:absolute;left:20%;right:20%;bottom:-20%;height:55%;background:#F06A8A;border-radius:50%;}
.lip{position:absolute;border:0 solid #4A1022;}
.hat{position:absolute;}
.prop{position:absolute;}
#top{position:absolute;left:0;right:0;top:226px;display:flex;flex-direction:column;align-items:center;gap:6px;z-index:5;}
#top .pill{direction:rtl;background:rgba(30,27,46,.86);color:#fff;font:800 40px/1.35 Vaz;padding:6px 30px;border-radius:999px;display:flex;gap:14px;align-items:center;}
#top .pill b{color:var(--acc);font-weight:800;}
#top .h{font:600 28px Pop;color:rgba(30,27,46,.55);}
#box{position:absolute;left:60px;top:1196px;width:900px;min-height:250px;background:var(--paper);border-radius:36px;border:5px solid #999;
 box-shadow:0 18px 40px rgba(0,0,0,.35);padding:58px 40px 30px;display:flex;flex-direction:column;align-items:center;gap:14px;transform-origin:50% 0;}
#notch{position:absolute;top:-26px;width:44px;height:44px;background:var(--paper);border-left:5px solid #999;border-top:5px solid #999;transform:rotate(45deg);border-radius:8px 0 0 0;}
#name{position:absolute;top:-30px;right:44px;direction:rtl;color:#fff;font:800 34px/1.4 Vaz;padding:4px 24px;border-radius:999px;display:flex;gap:12px;align-items:center;}
#name small{font:600 24px Pop;opacity:.85;}
#en{font:600 50px/1.3 Pop;color:var(--ink);text-align:center;}
#en mark{background:linear-gradient(180deg,transparent 52%,#FFD43B 52%);color:inherit;padding:0 4px;}
#fa{direction:rtl;font:600 42px/1.45 Vaz;color:#5B5670;text-align:center;}
.ov{position:absolute;inset:0;z-index:10;}
#title{background:rgba(24,18,46,.62);}
#poster{position:absolute;left:280px;top:385px;width:520px;height:600px;background:#FFF8E6;border-radius:18px;box-shadow:0 30px 60px rgba(0,0,0,.45);
 display:flex;flex-direction:column;align-items:center;padding-top:26px;}
#poster .m{font:800 96px/1 Pop;color:var(--red);letter-spacing:4px;}
#poster .mf{direction:rtl;font:900 50px/1.3 Vaz;color:var(--red);}
#poster .ph{margin-top:14px;width:330px;height:330px;border-radius:12px;background:linear-gradient(180deg,#E9F4FF,#CFE6FA);display:flex;align-items:center;justify-content:center;}
#poster .ph img{width:270px;height:270px;}
.tape{position:absolute;width:140px;height:40px;background:rgba(255,230,150,.75);}
#hook{position:absolute;left:0;right:0;top:1020px;display:flex;flex-direction:column;align-items:center;gap:4px;}
#hook .f{direction:rtl;font:900 78px/1.35 Vaz;color:#fff;text-shadow:0 6px 24px rgba(0,0,0,.4);}
#hook .e{font:600 44px Pop;color:var(--acc);}
#cliff{background:rgba(15,12,35,.66);display:flex;flex-direction:column;align-items:center;justify-content:center;gap:10px;padding-bottom:300px;}
#cliff .t{direction:rtl;font:900 104px/1.3 Vaz;color:var(--acc);text-shadow:0 8px 30px rgba(0,0,0,.4);}
#cliff .n{direction:rtl;font:700 54px/1.4 Vaz;color:#fff;}
#vocab{background:rgba(15,12,35,.78);display:flex;flex-direction:column;align-items:center;padding-top:330px;gap:26px;}
#vocab .vt{direction:rtl;font:900 66px/1.3 Vaz;color:#fff;}
.vrow{direction:rtl;width:820px;display:flex;align-items:center;justify-content:space-between;background:#FFFDF8;border-radius:26px;padding:16px 34px;}
.vrow .fa{font:800 56px/1.35 Vaz;color:#5B5670;}
.vrow .en{font:700 62px/1.2 Pop;color:var(--ink);direction:ltr;}
#vocab .cta{direction:rtl;margin-top:18px;background:var(--acc);color:#14162E;font:900 54px/1.35 Vaz;padding:12px 40px;border-radius:999px;display:flex;align-items:center;gap:14px;}
#vocab .cta img{width:72px;height:72px;}
#vocab .nx{direction:rtl;font:700 44px/1.4 Vaz;color:rgba(255,255,255,.8);}
"""

JS = r"""
const S = __STORY__, EP = __EP__, TL = __TL__, E = n => '__EMO__/' + n + '.png';
const $ = (h) => { const d = document.createElement('div'); d.innerHTML = h.trim(); return d.firstChild; };
const clamp = (x, a, b) => Math.max(a, Math.min(b, x));
const ease = (x) => 1 - Math.pow(1 - clamp(x, 0, 1), 3);
const back = (x) => { x = clamp(x, 0, 1); const c = 1.9; return 1 + (c + 1) * Math.pow(x - 1, 3) + c * Math.pow(x - 1, 2); };
const POS = { teapot: { cx: 290, size: 440, bottom: 1084 }, mug: { cx: 792, size: 420, bottom: 1084 } };
const LOOK = { teapot: 1, mug: -1 };
const chars = {};
function buildChar(key) {
  const c = S.characters[key], p = POS[key], s = p.size;
  const root = $(`<div class="char" style="left:${p.cx - s / 2}px;top:${p.bottom - s}px;width:${s}px;height:${s}px"></div>`);
  root.appendChild($(`<img class="body" src="${E(c.img)}">`));
  const ew = c.eye * s, eh = ew * 1.18;
  const eyes = c.eyes.map(([x, y]) => {
    const e = $(`<div class="eye" style="left:${x * s - ew / 2}px;top:${y * s - eh / 2}px;width:${ew}px;height:${eh}px"><div class="pupil"></div></div>`);
    root.appendChild(e); return e;
  });
  const brows = c.eyes.map(([x, y]) => {
    const b = $(`<div class="brow" style="left:${x * s - ew * 0.55}px;top:${y * s - eh * 0.98}px;width:${ew * 1.1}px;height:${ew * 0.2}px"></div>`);
    root.appendChild(b); return b;
  });
  const mw = c.mw * s;
  const mouth = $(`<div class="mouth"><i></i></div>`); root.appendChild(mouth);
  const lip = $(`<div class="lip"></div>`); root.appendChild(lip);
  if (c.hat) root.appendChild($(`<img class="hat" src="${E('top_hat')}" style="left:${0.2 * s}px;top:${-0.24 * s}px;width:${0.56 * s}px;height:${0.56 * s}px;transform:rotate(-10deg)">`));
  const shadow = $(`<div class="shadow" style="left:${p.cx - s * 0.36}px;top:${p.bottom - 26}px;width:${s * 0.72}px"></div>`);
  document.getElementById('scene').appendChild(shadow);
  document.getElementById('scene').appendChild(root);
  chars[key] = { root, eyes, brows, mouth, lip, ew, eh, mw, s, c, p, phase: key === 'teapot' ? 0.4 : 1.7, period: key === 'teapot' ? 3.3 : 3.9 };
}
function build() {
  const sc = document.getElementById('scene');
  sc.innerHTML = `<div id="wall"></div><div id="win"><div class="sky"><div class="sun"></div></div></div>
    <div id="shelf"><div class="jar" style="left:40px;width:70px;height:96px;background:#9FD8C3"></div>
    <div class="jar" style="left:130px;width:58px;height:74px;background:#F4B9A7"></div><div class="jar" style="left:210px;width:84px;height:112px;background:#C9D7F2"></div></div>
    <div id="counter"></div><div id="edge"></div><div id="cab"></div>
    <div class="door" style="left:40px"></div><div class="door" style="left:570px"></div>
    <div class="knob" style="left:470px"></div><div class="knob" style="left:584px"></div>`;
  ['teapot', 'mug'].forEach(buildChar);
  sc.appendChild($(`<img class="prop" id="glass" src="${E('magnifying_glass_tilted_left')}" style="width:170px;height:170px">`));
  for (let k = 0; k < 3; k++) {
    sc.appendChild($(`<div class="prop fp" style="left:${462 + k * 80}px;top:${1030 + (k % 2) * 18}px;width:66px;height:30px;border-radius:50%;background:rgba(120,190,255,.65);box-shadow:0 0 0 3px rgba(255,255,255,.6) inset"></div>`));
    sc.appendChild($(`<img class="prop fb" src="${E('bubbles')}" style="left:${460 + k * 80}px;top:${962 + (k % 2) * 18}px;width:72px;height:72px">`));
  }
  sc.appendChild($(`<img class="prop" id="shock" src="${E('exclamation_question_mark')}" style="left:226px;top:500px;width:130px;height:130px">`));
  const L = EP.lines;
  document.getElementById('topf').innerHTML = `${S.series_fa}<b>· ${EP.part_fa}</b>`;
  document.getElementById('toph').textContent = `${S.series_en} · @english_dya`;
  document.getElementById('poster').innerHTML = `<div class="tape" style="left:-30px;top:-10px;transform:rotate(-30deg)"></div><div class="tape" style="right:-30px;top:-10px;transform:rotate(30deg)"></div>
    <div class="m">MISSING</div><div class="mf">گمشده</div><div class="ph"><img src="${E('spoon')}"></div>`;
  document.getElementById('hook').innerHTML = `<div class="f">${EP.hook_fa}</div><div class="e">${EP.hook_en}</div>`;
  document.getElementById('cliff').innerHTML = `<div class="t">${EP.tbc_fa}</div><div class="n">${EP.next_fa}</div>`;
  document.getElementById('vocab').innerHTML = `<div class="vt">${EP.vocab_title}</div>` +
    EP.vocab.map(([en, fa]) => `<div class="vrow"><span class="fa">${fa}</span><span class="en">${en}</span></div>`).join('') +
    `<div class="cta">${EP.cta_fa}<img src="${E('backhand_index_pointing_down')}"></div><div class="nx">${EP.next_fa}</div>`;
}
const MOODS = {
  calm:      { brow: [-4, 4, 0], lip: 'smile', o: 0 },
  worried:   { brow: [-16, 16, -0.08], lip: 'frown', o: 0 },
  thinking:  { brow: [-12, 3, -0.06], lip: 'flat', o: 0, look: [0.12, -0.16] },
  surprised: { brow: [-6, 6, -0.3], lip: 'o', o: 0.45, big: 1.12 },
  shocked:   { brow: [-8, 8, -0.32], lip: 'o', o: 0.6, big: 1.15 },
};
let lastSeg = -2;
function setBox(i) {
  const box = document.getElementById('box');
  if (i < 0) { box.style.display = 'none'; return; }
  box.style.display = 'flex';
  const ln = EP.lines[i], c = S.characters[ln.who];
  box.style.borderColor = c.color;
  const notch = document.getElementById('notch');
  notch.style.borderColor = c.color; notch.style.left = (POS[ln.who].cx - 60 - 22) + 'px';
  const nm = document.getElementById('name');
  nm.style.background = c.color; nm.innerHTML = `${c.name_fa}<small>${c.name_en}</small>`;
  nm.style.right = ln.who === 'teapot' ? 'auto' : '44px'; nm.style.left = ln.who === 'teapot' ? '44px' : 'auto';
  document.getElementById('en').innerHTML = ln.en.replace(/\*(.+?)\*/g, '<mark>$1</mark>');
  document.getElementById('fa').textContent = ln.fa;
}
window.setT = (ms) => {
  const t = ms / 1000, L = TL.lines;
  // which line segment is on screen
  let seg = -1;
  for (const ln of L) if (t >= ln.seg_start && t < ln.seg_end) seg = ln.i;
  if (t >= L[L.length - 1].seg_end && t < TL.cliff) seg = L.length - 1;
  if (t < TL.title || t >= TL.cliff) seg = -1;
  if (seg !== lastSeg) { setBox(seg); lastSeg = seg; }
  if (seg >= 0) { const k = clamp((t - L[seg].seg_start) / 0.18, 0, 1); document.getElementById('box').style.transform = `scale(${0.94 + 0.06 * back(k)})`; }
  // latest mood per character
  for (const key of Object.keys(chars)) {
    const ch = chars[key];
    let mood = 'calm', open = 0, speaking = false, look = null, lineStart = 0;
    for (const ln of L) { if (ln.who === key && t >= ln.seg_start) { mood = ln.mood; look = ln.look || null; lineStart = ln.start; } }
    if (key === 'teapot' && t < (L.find(l => l.who === 'teapot') || {seg_start: 0}).seg_start) mood = 'worried';
    const cur = L.find(ln => t >= ln.start && t < ln.end && ln.who === key);
    if (cur) { speaking = true; const f = Math.floor((t - cur.start) * TL.fps); open = cur.env[Math.min(f, cur.env.length - 1)] || 0; }
    const M = MOODS[mood] || MOODS.calm;
    const someoneElse = L.some(ln => t >= ln.start && t < ln.end && ln.who !== key);
    // body
    const idle = 1 + 0.01 * Math.sin(2 * Math.PI * 0.6 * t + ch.phase * 3);
    let ty = 0, sc = idle, rot = 0;
    if (speaking) { ty = -14 * open; sc = idle * (1.03 + 0.03 * open); rot = Math.sin(t * 7) * 1.6 * open; }
    if (mood === 'shocked' && t >= lineStart - 0.4) { const k = clamp((t - (lineStart - 0.4)) / 0.35, 0, 1); ty -= 40 * Math.sin(Math.PI * k); }
    ch.root.style.transform = `translateY(${ty}px) rotate(${rot}deg) scale(${sc})`;
    ch.root.style.filter = someoneElse ? 'brightness(.9) saturate(.9)' : 'none';
    // eyes
    const blink = !M.big && ((t + ch.phase) % ch.period) < 0.13;
    const big = M.big || 1;
    let lx = LOOK[key] * 0.13, ly = 0.05;
    if (M.look) { lx = M.look[0]; ly = M.look[1]; }
    if (look === 'down') { lx = LOOK[key] * 0.08; ly = 0.22; }
    if (someoneElse) { lx = LOOK[key] * 0.16; ly = 0.04; }
    ch.eyes.forEach(e => {
      e.style.transform = `scale(${big}, ${blink ? 0.1 : big})`;
      e.firstChild.style.transform = `translate(${lx * 100}%, ${ly * 100}%) scale(${M.big ? 0.85 : 1})`;
    });
    // brows
    ch.brows.forEach((b, j) => { b.style.transform = `translateY(${M.brow[2] * ch.eh}px) rotate(${M.brow[j]}deg)`; });
    // mouth
    const [mx, my] = ch.c.mouth, s = ch.s, mw = ch.mw;
    let o = Math.max(open, M.o);
    const showOpen = o > 0.08 || M.lip === 'o';
    if (showOpen) {
      const round = M.lip === 'o' && !speaking;
      const w = round ? mw * 0.55 : mw * (1 - 0.3 * open);
      const h = round ? mw * 0.62 : mw * (0.18 + 0.62 * o);
      Object.assign(ch.mouth.style, { display: 'block', left: (mx * s - w / 2) + 'px', top: (my * s - h * 0.35) + 'px', width: w + 'px', height: h + 'px',
        borderRadius: round ? '50%' : '45% 45% 55% 55% / 35% 35% 65% 65%' });
      ch.lip.style.display = 'none';
    } else {
      ch.mouth.style.display = 'none';
      const lw = mw * (M.lip === 'flat' ? 0.6 : 0.85), lh = mw * 0.32, bw = Math.max(5, mw * 0.08);
      const st = { display: 'block', left: (mx * s - lw / 2) + 'px', width: lw + 'px', height: lh + 'px', borderWidth: '0', borderRadius: '0' };
      if (M.lip === 'smile') Object.assign(st, { top: (my * s - lh * 0.6) + 'px', borderBottomWidth: bw + 'px', borderRadius: `0 0 ${lw}px ${lw}px / 0 0 ${lh}px ${lh}px` });
      else if (M.lip === 'frown') Object.assign(st, { top: (my * s) + 'px', borderTopWidth: bw + 'px', borderRadius: `${lw}px ${lw}px 0 0 / ${lh}px ${lh}px 0 0` });
      else Object.assign(st, { top: (my * s) + 'px', height: bw + 'px', background: '#4A1022', borderRadius: bw + 'px' });
      if (M.lip !== 'flat') st.background = 'transparent';
      Object.assign(ch.lip.style, st);
    }
  }
  // props
  const lnBy = (p) => L.find(l => l.prop === p);
  const g = lnBy('glass'), fpl = lnBy('footprints'), sh = lnBy('shock');
  const glass = document.getElementById('glass');
  if (g && t >= g.seg_start && t < TL.cliff) {
    const k = back((t - g.seg_start) / 0.4);
    let x = 575, y = 720, r = -10 + Math.sin(t * 3) * 6;
    if (fpl && t >= fpl.seg_start) { const m = ease((t - fpl.seg_start) / 0.6); x = 575 - 110 * m; y = 720 + 190 * m; r = -25 * m + Math.sin(t * 3) * 4; }
    glass.style.display = 'block'; glass.style.left = x + 'px'; glass.style.top = y + 'px';
    glass.style.transform = `rotate(${r}deg) scale(${k})`;
  } else glass.style.display = 'none';
  document.querySelectorAll('.fp,.fb').forEach((el, j) => {
    const k = Math.floor(j / 2);
    if (fpl && t >= fpl.seg_start + k * 0.22) { const q = back((t - fpl.seg_start - k * 0.22) / 0.3); el.style.display = 'block'; el.style.transform = `scale(${q})`; }
    else el.style.display = 'none';
  });
  const shock = document.getElementById('shock');
  if (sh && t >= sh.seg_start && t < TL.cliff + 0.6) { const q = back((t - sh.seg_start) / 0.35); shock.style.display = 'block'; shock.style.transform = `scale(${q}) rotate(${Math.sin(t * 9) * 8}deg)`; }
  else shock.style.display = 'none';
  // overlays
  const ti = document.getElementById('title');
  if (t < TL.title) {
    const out = clamp((t - (TL.title - 0.45)) / 0.45, 0, 1);
    ti.style.display = 'block'; ti.style.opacity = 1 - out;
    const pin = t < 0.35 ? 1.08 - 0.08 * ease(t / 0.35) : 1;
    document.getElementById('poster').style.transform = `translateY(${-260 * ease(out)}px) rotate(${-3 + 2 * Math.sin(t * 2.2)}deg) scale(${pin * (1 - 0.3 * out)})`;
  } else ti.style.display = 'none';
  const cl = document.getElementById('cliff');
  if (t >= TL.cliff && t < TL.vocab) { cl.style.display = 'flex'; cl.style.opacity = ease((t - TL.cliff) / 0.3); cl.firstChild.style.transform = `scale(${0.85 + 0.15 * back((t - TL.cliff) / 0.4)})`; }
  else cl.style.display = 'none';
  const vo = document.getElementById('vocab');
  if (t >= TL.vocab) {
    vo.style.display = 'flex'; vo.style.opacity = ease((t - TL.vocab) / 0.3);
    vo.querySelectorAll('.vrow').forEach((r, j) => { const q = ease((t - TL.vocab - 0.25 - j * 0.25) / 0.35); r.style.opacity = q; r.style.transform = `translateY(${30 * (1 - q)}px)`; });
    const cta = vo.querySelector('.cta'); const q = back((t - TL.vocab - 1.2) / 0.4); cta.style.transform = `scale(${q})`;
  } else vo.style.display = 'none';
};
window.ready = async () => {
  build();
  await Promise.all([document.fonts.load('600 50px Pop', 'Ab'), document.fonts.load('800 40px Pop', 'Ab'), document.fonts.load('900 60px Vaz', 'سلام'), document.fonts.load('600 40px Vaz', 'سلام')]);
  await Promise.all([...document.images].map(im => im.decode().catch(() => {})));
  window.setT(0);
  return document.fonts.check('600 50px Pop') && document.fonts.check('900 60px Vaz', 'سلام');
};
"""

BODY = """<div id="scene"></div>
<div id="top"><div class="pill" id="topf"></div><div class="h" id="toph"></div></div>
<div id="box"><div id="notch"></div><div id="name"></div><div id="en"></div><div id="fa"></div></div>
<div class="ov" id="title"><div id="poster"></div><div id="hook"></div></div>
<div class="ov" id="cliff"></div><div class="ov" id="vocab"></div>"""


def main(story_path, ep_no, preview=False):
    s = json.load(open(story_path))
    ep = next(e for e in s["episodes"] if e["ep"] == ep_no)
    tag = f"story_w{s['week']:02d}_e{ep_no:02d}"
    bdir = os.path.join(HERE, "build", tag)
    tl = json.load(open(os.path.join(bdir, "timeline.json")))
    js = (JS.replace("__STORY__", json.dumps(s, ensure_ascii=False)).replace("__EP__", json.dumps(ep, ensure_ascii=False))
            .replace("__TL__", json.dumps(tl)).replace("__EMO__", EMO))
    html = os.path.join(bdir, "story.html")
    open(html, "w", encoding="utf-8").write("<!doctype html><html lang='fa'><head><meta charset='utf-8'><style>" + font_css() + CSS +
                                             "</style></head><body>" + BODY + "<script>" + js + "</script></body></html>")
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--no-sandbox", "--disable-gpu", "--font-render-hinting=none"])
        pg = b.new_page(viewport={"width": W, "height": H}, device_scale_factor=1)
        pg.goto("file://" + html)
        print("fonts ok:", pg.evaluate("ready()"))
        L = tl["lines"]
        if preview:
            moments = [("title", 1.2), ("l0", L[0]["start"] + 0.6), ("l3", L[3]["start"] + 1.0), ("l4", L[4]["start"] + 1.2),
                       ("l5", L[5]["start"] + 0.5), ("cliff", tl["cliff"] + 0.8), ("vocab", tl["vocab"] + 2.5)]
            for name, t in moments:
                pg.evaluate(f"setT({t * 1000})")
                pg.screenshot(path=os.path.join(bdir, f"prev_{name}.jpg"), type="jpeg", quality=85)
            b.close(); print("previews in", bdir); return
        os.makedirs(os.path.join(HERE, "out"), exist_ok=True)
        video = os.path.join(bdir, "video.mp4"); tmp = video[:-4] + ".part.mp4"
        cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "image2pipe", "-framerate", str(FPS), "-c:v", "mjpeg", "-i", "-",
               "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-bf", "0", "-g", "60", "-pix_fmt", "yuv420p", "-r", str(FPS), tmp]
        proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
        for f in range(round(tl["total"] * FPS)):
            pg.evaluate(f"setT({f * 1000 / FPS})")
            proc.stdin.write(pg.screenshot(type="jpeg", quality=92))
        proc.stdin.close()
        if proc.wait() != 0:
            raise SystemExit("ffmpeg failed")
        os.replace(tmp, video)
        b.close()
    # sound
    ev = [(0.05, f"{SFX}/pop.wav", 0.35), (tl["title"] - 0.45, f"{SFX}/whoosh.wav", 0.35)]
    for ln in L:
        ev.append((ln["start"], ln["wav"], 1.0))
        if ln.get("prop") == "glass": ev.append((ln["seg_start"] + 0.05, f"{SFX}/tick.wav", 0.35))
        if ln.get("prop") == "footprints": ev += [(ln["seg_start"] + k * 0.22, f"{SFX}/pop.wav", 0.28) for k in range(3)]
        if ln.get("prop") == "shock": ev.append((ln["seg_start"], f"{SFX}/boop.wav", 0.4))
    ev += [(tl["cliff"], f"{SFX}/sting.wav", 0.7), (tl["vocab"], f"{SFX}/ding.wav", 0.3)]
    ev += [(tl["vocab"] + 0.25 + j * 0.25, f"{SFX}/tick.wav", 0.3) for j in range(len(ep["vocab"]))]
    voice = [(ln["start"], ln["end"]) for ln in L]
    music = make_music(tl["total"], voice + [(tl["cliff"], tl["cliff"] + 1.6)], os.path.join(bdir, "music.wav"), bpm=92, level_db=-28.0,
                       prog=MYSTERY, pluck_decay=0.12, pattern=[0, 2, 1, 3, 0, 2, 3, 1], pad_gain=0.55)
    ev.insert(0, (0.0, music, 1.0))
    wav = os.path.join(bdir, "audio.wav")
    build_audio(ev, tl["total"], wav)
    out = os.path.join(HERE, "out", f"{tag}.mp4"); tmp = out[:-4] + ".part.mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", video, "-i", wav, "-map", "0:v", "-map", "1:a", "-c:v", "copy",
                    "-c:a", "aac", "-b:a", "160k", "-ar", "44100", "-ac", "2", "-shortest", "-movflags", "+faststart", "-use_editlist", "0", tmp], check=True)
    os.replace(tmp, out)
    print("episode:", out, tl["total"], "s")


if __name__ == "__main__":
    main(sys.argv[1], int(sys.argv[2]), preview="--preview" in sys.argv)
