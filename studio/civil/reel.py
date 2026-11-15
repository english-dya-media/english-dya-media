"""Render a civil-engineering reel: content/cNNN.json -> out/cNNN.mp4 (1080x1920, 30 fps, AAC).

  python3 reel.py content/c001.json             # full render
  python3 reel.py content/c001.json --audio     # redo only the sound (after a full render)
  python3 reel.py content/c001.json --preview   # stills every ~1.6 s + build/<tag>/sheet.jpg (contact sheet)
                                                #   and a layout check (text wider than the safe area, low content)
Layout: badge, hook (Persian + English), diagram, bottom captions; quiz reels add 4 options, a countdown and the
reveal. Then a 2.6 s follow card. Music: original bed from ../music.py; sounds from ../assets/sfx.
"""
import base64, html as H_, json, os, re, subprocess, sys
from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
STUDIO = os.path.dirname(HERE)
sys.path.insert(0, STUDIO)
sys.path.insert(0, HERE)
from music import make_music          # noqa: E402
from kit import KINDS, fa, A, BO, EZ  # noqa: E402

FONTS = os.path.join(STUDIO, "assets", "fonts")
EMO = "file://" + os.path.join(STUDIO, "assets", "emoji")
SFX = os.path.join(STUDIO, "assets", "sfx")
W, H, FPS, END = 1080, 1920, 30, 2.6
SAFE_BOTTOM = 1500        # Instagram's caption/buttons cover what is below
PROG = [[45, 48, 52, 55], [41, 45, 48, 52], [48, 52, 55, 59], [43, 47, 50, 55]]   # Am7 Fmaj7 Cmaj7 G


def font_css():
    faces = [("Vaz", "Vazirmatn.woff2", "100 900"), ("Pop", "poppins-latin-500-normal.woff2", "500"),
             ("Pop", "poppins-latin-600-normal.woff2", "600"), ("Pop", "poppins-latin-700-normal.woff2", "700"),
             ("Pop", "poppins-latin-800-normal.woff2", "800"), ("Mono", "jetbrains-mono-latin-500-normal.woff2", "500"),
             ("Mono", "jetbrains-mono-latin-700-normal.woff2", "700")]
    out = []
    for fam, fn, wt in faces:
        b = base64.b64encode(open(os.path.join(FONTS, fn), "rb").read()).decode()
        out.append("@font-face{font-family:%s;src:url(data:font/woff2;base64,%s) format('woff2');font-weight:%s;font-display:block;}" % (fam, b, wt))
    return "\n".join(out)


CSS = r"""
:root{--ink:#E8F3FF;--dim:#8FB3D9;--acc:#FFD43B;--red:#FF5C7A;--blue:#4FC3F7;--green:#2EE59D;--en:#9BD4FF;}
*{box-sizing:border-box}
html,body{margin:0;width:1080px;height:1920px;overflow:hidden;background:#071A33;}
body{font-family:Vaz,sans-serif;color:var(--ink);}
#bg{position:absolute;inset:0;background:
 radial-gradient(900px 820px at 50% 40%, #154781 0%, rgba(21,71,129,0) 70%),
 radial-gradient(700px 600px at 92% 94%, rgba(255,212,59,.10), rgba(255,212,59,0) 70%),
 radial-gradient(600px 500px at 6% 8%, rgba(79,195,247,.10), rgba(79,195,247,0) 70%),
 linear-gradient(180deg,#0C2B52 0%,#071A33 100%);}
#grid{position:absolute;inset:0;
 background-image:linear-gradient(rgba(143,179,217,.15) 2px,transparent 2px),linear-gradient(90deg,rgba(143,179,217,.15) 2px,transparent 2px),
  linear-gradient(rgba(143,179,217,.065) 1px,transparent 1px),linear-gradient(90deg,rgba(143,179,217,.065) 1px,transparent 1px);
 background-size:180px 180px,180px 180px,36px 36px,36px 36px;background-position:-1px -1px;
 -webkit-mask:radial-gradient(1200px 1600px at 50% 45%,#000 35%,rgba(0,0,0,.3) 100%);}
#stage{position:absolute;inset:0;}
#col{position:absolute;top:186px;height:1304px;left:0;right:40px;display:flex;flex-direction:column;align-items:center;}
.badge{direction:rtl;display:flex;align-items:center;gap:14px;padding:6px 26px 6px 20px;border-radius:999px;
 background:rgba(255,212,59,.12);border:2px solid rgba(255,212,59,.55);}
.badge img{width:50px;height:50px;}
.badge .bfa{font:800 38px/1.3 Vaz;color:var(--acc);}
.badge .ben{font:600 26px Pop;color:#FFE58A;direction:ltr;}
.badge .num{font:700 26px Pop;color:#0B2545;background:var(--acc);border-radius:999px;padding:1px 14px;direction:ltr;}
.hook{margin-top:20px;display:flex;flex-direction:column;align-items:center;gap:4px;text-align:center;max-width:960px;}
.hfa{direction:rtl;font:900 64px/1.36 Vaz;color:#fff;text-shadow:0 8px 30px rgba(0,0,0,.35);}
.hen{direction:ltr;font:600 36px/1.3 Pop;color:var(--en);}
.qfa{direction:rtl;font:900 56px/1.4 Vaz;color:#fff;text-shadow:0 8px 30px rgba(0,0,0,.35);max-width:930px;text-wrap:balance;}
.qen{direction:ltr;font:600 32px/1.3 Pop;color:var(--en);max-width:930px;text-wrap:balance;}
.sub{margin-top:6px;direction:rtl;font:600 32px/1.4 Vaz;color:var(--dim);}
.suben{direction:ltr;font:500 25px/1.3 Pop;color:var(--dim);}
.dia{position:relative;flex:1 1 auto;width:920px;display:flex;align-items:center;justify-content:center;}
.dia > svg{display:block;overflow:visible;}
.halo{paint-order:stroke;stroke:#0A2140;stroke-width:12px;stroke-linejoin:round;}
.tb{transform-box:fill-box;transform-origin:center;}
.gu{transform-box:fill-box;transform-origin:50% 100%;}
.steps{position:relative;flex:none;margin-top:12px;width:100%;height:250px;}
.step{position:absolute;top:0;left:0;right:0;display:flex;justify-content:center;}
.panel{max-width:880px;display:flex;flex-direction:column;align-items:center;gap:2px;padding:14px 38px 16px;border-radius:30px;
 background:rgba(5,18,38,.80);border:2px solid rgba(143,211,255,.28);box-shadow:0 18px 40px rgba(0,0,0,.35);text-align:center;}
.sfa{direction:rtl;font:800 50px/1.45 Vaz;color:#fff;max-width:800px;text-wrap:balance;}
.sfa b{color:var(--acc);font-weight:900;}
.sen{direction:ltr;font:600 32px/1.35 Pop;color:var(--en);max-width:800px;text-wrap:balance;}
.sen b{color:var(--acc);}
.emo{width:1.05em;height:1.05em;vertical-align:-.18em;margin:0 .08em;}
.arw{width:1.1em;height:.6em;vertical-align:.02em;margin:0 .15em;overflow:visible;}
.tk{gap:10px;padding:18px 40px 20px;}
.tkrow{direction:rtl;display:flex;align-items:center;gap:20px;font:900 54px/1.3 Vaz;}
.tkrow .en{direction:ltr;font:600 30px Pop;color:var(--en);margin-right:18px;}
.fx{direction:ltr;font:700 46px/1.35 Mono;color:var(--acc);letter-spacing:.5px;}
.fx sup{font-size:.62em;}
/* quiz */
.opts{position:relative;flex:none;margin-top:12px;width:840px;height:430px;}
.opt{position:absolute;left:0;right:0;height:94px;display:flex;align-items:center;gap:20px;direction:rtl;padding:0 26px 0 30px;
 border-radius:26px;background:rgba(5,18,38,.80);border:3px solid rgba(143,211,255,.30);}
.opt .let{flex:none;width:66px;height:66px;border-radius:50%;display:flex;align-items:center;justify-content:center;
 background:rgba(255,212,59,.16);border:2px solid rgba(255,212,59,.6);font:900 32px Vaz;color:var(--acc);}
.opt .ofa{font:900 50px/1.3 Vaz;color:#fff;flex:1;}
.opt .oen{direction:ltr;font:700 36px Pop;color:var(--en);}
.opt img{width:58px;height:58px;}
.qsteps{position:absolute;top:116px;left:-20px;right:-20px;height:310px;}
.timer{position:absolute;right:0;top:calc(50% - 150px);width:220px;display:flex;flex-direction:column;align-items:center;gap:6px;}
.ring{position:relative;width:180px;height:180px;}
.ring svg{position:absolute;inset:0;}
.tn{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;font:900 92px Vaz;color:#fff;}
.tcap{direction:rtl;font:800 30px/1.3 Vaz;color:var(--acc);white-space:nowrap;text-align:center;}
.tcap2{direction:ltr;font:600 22px Pop;color:var(--en);white-space:nowrap;}
/* follow card */
.line{position:absolute;left:0;right:40px;display:flex;justify-content:center;}
.handle{padding:8px 30px;border-radius:999px;background:rgba(255,255,255,.08);border:2px solid rgba(255,255,255,.16);font:600 34px Pop;color:#E7EAFF;}
.e1{direction:rtl;font:900 82px/1.3 Vaz;text-align:center;}
.e2{direction:ltr;font:600 40px/1.3 Pop;color:var(--en);text-align:center;}
.fbtn{direction:rtl;display:flex;align-items:center;gap:18px;background:#3B82F6;color:#fff;font:900 92px/1.3 Vaz;
 padding:14px 66px;border-radius:40px;box-shadow:0 20px 50px rgba(59,130,246,.45);}
.fbtn img{width:92px;height:92px;}
.e3{direction:rtl;display:flex;align-items:center;gap:12px;font:700 46px/1.35 Vaz;color:var(--dim);}
.e3 img{width:58px;height:58px;}
.glow{position:absolute;left:50%;width:760px;height:760px;margin-left:-380px;border-radius:50%;
 background:radial-gradient(closest-side,rgba(79,195,247,.35),rgba(79,195,247,0));}
@keyframes fadeIn{from{opacity:0}to{opacity:1}}
@keyframes fadeOut{from{opacity:1}to{opacity:0}}
@keyframes popIn{0%{opacity:0;transform:scale(.55)}100%{opacity:1;transform:scale(1)}}
@keyframes punch{0%{opacity:0;transform:scale(1.22)}100%{opacity:1;transform:scale(1)}}
@keyframes slideUp{from{opacity:0;transform:translateY(36px)}to{opacity:1;transform:translateY(0)}}
@keyframes dropIn{from{opacity:0;transform:translateY(-60px)}to{opacity:1;transform:translateY(0)}}
@keyframes growUp{from{transform:scaleY(0)}to{transform:scaleY(1)}}
@keyframes drawIn{0%{stroke-dashoffset:1;opacity:0}1%{opacity:1}100%{stroke-dashoffset:0;opacity:1}}
@keyframes ringDown{from{stroke-dashoffset:0}to{stroke-dashoffset:-1}}
@keyframes dim18{to{opacity:.18}} @keyframes dim25{to{opacity:.25}} @keyframes dim35{to{opacity:.35}} @keyframes dim0{to{opacity:0}}
@keyframes pulse{0%,100%{transform:scale(1)}50%{transform:scale(1.07)}}
@keyframes bobY{0%,100%{transform:translateY(0)}50%{transform:translateY(-14px)}}
@keyframes toY{to{transform:translateY(var(--dy))}}
@keyframes okFlash{0%{background:rgba(5,18,38,.80);border-color:rgba(143,211,255,.30)}35%{background:rgba(46,229,157,.55)}
 100%{background:rgba(46,229,157,.20);border-color:#2EE59D}}
"""

JS = r"""
const S = __SCENES__;
window.show = async (k) => {
  document.getElementById('stage').innerHTML = S[k];
  await Promise.all([...document.images].map(im => im.decode().catch(() => {})));
  fitAll(); window.seek(0); return true;
};
window.seek = (ms) => {
  for (const a of document.getAnimations()) { a.pause(); a.currentTime = ms; }
  document.querySelectorAll('#stage svg').forEach(s => { try { s.pauseAnimations(); s.setCurrentTime(ms / 1000); } catch (e) {} });
  const t = ms / 1000;
  document.querySelectorAll('[data-count]').forEach(el => {
    const [t0, t1, a, b, pf] = JSON.parse(el.dataset.count);
    const k = Math.max(0, Math.min(1, (t - t0) / (t1 - t0)));
    let v = String(Math.round(a + (b - a) * k));
    if (pf) v = v.replace(/\d/g, d => '۰۱۲۳۴۵۶۷۸۹'[d]);
    el.textContent = v;
  });
};
function fitAll() {   // shrink single lines that are wider than their limit
  document.querySelectorAll('.fit').forEach(el => {
    const max = +(el.dataset.max || 960);
    el.style.zoom = ''; el.style.whiteSpace = 'nowrap';
    const w = el.scrollWidth;
    if (w > max) el.style.zoom = (max / w).toFixed(3);
  });
}
window.layout = () => {   // for --preview: what sticks out
  const bad = [];
  document.querySelectorAll('.panel, .opt').forEach(el => { const r = el.getBoundingClientRect();
    if (r.bottom > __SAFE__) bad.push('ends at y=' + Math.round(r.bottom) + ': ' + el.textContent.slice(0, 40)); });
  const dia = document.querySelector('.dia'), sv = dia && dia.querySelector(':scope > svg');
  if (sv && sv.getBoundingClientRect().height > dia.getBoundingClientRect().height + 1) bad.push('diagram taller than the space left for it');
  document.querySelectorAll('.fit').forEach(el => { if (el.style.zoom && +el.style.zoom < .86) bad.push('shrunk ' + el.style.zoom + ': ' + el.textContent.slice(0, 50)); });
  return bad;
};
window.ready = async () => {
  await Promise.all([document.fonts.load('900 60px Vaz', 'سلام'), document.fonts.load('600 40px Pop', 'Ab'),
                     document.fonts.load('700 40px Pop', 'Ab'), document.fonts.load('700 40px Mono', 'Ab')]);
  return document.fonts.check('900 60px Vaz', 'سلام');
};
"""

ARROW = {"←": '<svg class="arw" viewBox="0 0 44 24"><path d="M42 12H6M15 3L4 12l11 9" fill="none" stroke="currentColor" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/></svg>',
         "→": '<svg class="arw" viewBox="0 0 44 24"><path d="M2 12h36M29 3l11 9-11 9" fill="none" stroke="currentColor" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/></svg>'}


def rich(s):
    """Text -> HTML: :emoji_key: -> Fluent image, arrows -> drawn arrows. Other HTML (<b>, <sup>) passes through."""
    img = lambda k: f'<img class="emo" src="{EMO}/{k}.png">'
    s = re.sub(r"([^\s<>]+)\s+:([a-z0-9_]+):", lambda m: f'<span style="white-space:nowrap">{m.group(1)} {img(m.group(2))}</span>', s)
    s = re.sub(r":([a-z0-9_]+):\s+([^\s<>]+)", lambda m: f'<span style="white-space:nowrap">{img(m.group(1))} {m.group(2)}</span>', s)
    s = re.sub(r":([a-z0-9_]+):", lambda m: img(m.group(1)), s)
    for k, v in ARROW.items():
        s = s.replace(k, v)
    return s


def emoji_keys(d):
    blob = json.dumps(d, ensure_ascii=False)
    return sorted(set(re.findall(r":([a-z0-9_]+):", blob)) | {KINDS[d["kind"]][2], "construction_worker", "backhand_index_pointing_down",
                                                          "pushpin", "check_mark_button"})


def badge(d):
    bfa, ben, emo = KINDS[d["kind"]]
    return (f'<div class="badge" style="{A(("popIn", .35, 0, BO))}"><img src="{EMO}/{emo}.png"><span class="bfa">{bfa}</span>'
            f'<span class="ben">{ben}</span><span class="num">#{d["n"]}</span></div>')


def steps_html(steps, end, top_cls="step"):
    out = []
    for i, s in enumerate(steps):
        t1 = steps[i + 1]["t"] if i + 1 < len(steps) else None
        anim = [("slideUp", .35, s["t"])]
        if t1 is not None:
            anim.append(("fadeOut", .22, t1 - .22, "ease-in", "forwards"))
        inner = rich(s["html"]) if "html" in s else (
            f'<div class="panel"><div class="sfa">{rich(s["fa"])}</div>'
            f'<div class="sen">{rich(s["en"])}</div></div>')
        out.append(f'<div class="{top_cls}" style="{A(*anim)}">{inner}</div>')
    return "".join(out)


def main_scene(d):
    svg = f'<svg viewBox="0 0 920 {d["svg_h"]}" width="920" height="{d["svg_h"]}">{d["svg"]}</svg>'
    if d["kind"] != "quiz":
        return (f'<div id="col">{badge(d)}'
                f'<div class="hook" style="{A(("punch", .4, 0))}"><div class="hfa fit">{rich(d["hook_fa"])}</div>'
                f'<div class="hen fit">{rich(d["hook_en"])}</div></div>'
                f'<div class="dia">{svg}</div><div class="steps">{steps_html(d["steps"], d["dur"])}</div></div>')
    tc, think, tr, ans = d["t_count"], d["think"], d["t_reveal"], d["answer"]
    letters = ["الف", "ب", "ج", "د"]
    opts = ""
    for i, (f, e) in enumerate(d["options"]):
        top = i * 112
        anim = [("slideUp", .3, d["t_opts"] + i * .18)]
        if i == ans:
            anim += [("okFlash", .7, tr, "ease-out", "forwards"), ("toY", .5, tr + .35, EZ, "forwards")]
            check = f'<img src="{EMO}/check_mark_button.png" style="{A(("popIn", .35, tr + .1, BO))}">'
        else:
            anim += [("fadeOut", .3, tr, "ease-in", "forwards")]
            check = ""
        opts += (f'<div class="opt" style="top:{top}px;--dy:{-top}px;{A(*anim)}"><span class="let">{letters[i]}</span>'
                 f'<span class="ofa">{rich(f)}</span>{check}<span class="oen">{rich(e)}</span></div>')
    nums = ""
    for k in range(think):
        t0 = tc + k
        an = [("punch", .25, t0)] + ([("fadeOut", .15, t0 + .85, "ease-in", "forwards")] if k < think - 1 else [])
        nums += f'<div class="tn" style="{A(*an)}">{fa(think - k)}</div>'
    timer = (f'<div class="timer" style="{A(("popIn", .35, tc - .2, BO), ("fadeOut", .3, tr, "ease-in", "forwards"))}">'
             f'<div class="ring"><svg viewBox="0 0 180 180" width="180" height="180">'
             f'<circle cx="90" cy="90" r="78" fill="rgba(5,18,38,.8)" stroke="rgba(255,255,255,.16)" stroke-width="12"/>'
             f'<circle cx="90" cy="90" r="78" fill="none" stroke="#FFD43B" stroke-width="12" stroke-linecap="round" pathLength="1" '
             f'transform="rotate(-90 90 90)" style="stroke-dasharray:1;{A(("ringDown", think, tc, "linear"))}"/></svg>{nums}</div>'
             f'<div class="tcap">{rich("جوابتو کامنت کن :backhand_index_pointing_down:")}</div><div class="tcap2">comment your answer</div></div>')
    return (f'<div id="col">{badge(d)}'
            f'<div class="hook" style="{A(("punch", .4, 0))}"><div class="qfa">{rich(d["hook_fa"])}</div>'
            f'<div class="qen">{rich(d["hook_en"])}</div>'
            f'<div class="sub" style="{A(("fadeIn", .4, .5))}">{rich(d["sub_fa"])}</div>'
            f'<div class="suben" style="{A(("fadeIn", .4, .6))}">{rich(d["sub_en"])}</div></div>'
            f'<div class="dia">{svg}{timer}</div>'
            f'<div class="opts">{opts}<div class="qsteps">{steps_html(d["steps"], d["dur"])}</div></div></div>')


def end_scene(d):
    hd = d.get("handle")
    out = ""
    if hd:
        out += f'<div class="line" style="top:300px;{A(("fadeIn", .3, 0))}"><div class="handle" dir="ltr">{hd}</div></div>'
    out += (f'<div class="glow" style="top:330px"></div>'
            f'<div class="line" style="top:430px"><img src="{EMO}/construction_worker.png" style="width:230px;height:230px;'
            f'{A(("popIn", .4, 0, BO), ("bobY", 1.6, .5, "ease-in-out", "both", "infinite"))}"></div>'
            f'<div class="line" style="top:700px"><div class="e1" style="{A(("slideUp", .35, .1))}">هر روز یه درس عمران</div></div>'
            f'<div class="line" style="top:818px"><div class="e2" style="{A(("slideUp", .35, .22))}">One civil engineering lesson every day</div></div>'
            f'<div class="line" style="top:930px"><div class="fbtn" style="{A(("popIn", .4, .4, BO))}">'
            f'<span style="display:inline-block;{A(("pulse", .6, .9, "ease-in-out", "both", "infinite"))}">فالو کن</span>'
            f'<img src="{EMO}/backhand_index_pointing_down.png"></div></div>'
            f'<div class="line" style="top:1130px"><div class="e3" style="{A(("fadeIn", .35, .7))}">'
            f'<img src="{EMO}/pushpin.png">سیو کن که یادت بمونه</div></div>')
    return out


def build_audio(events, total, out):
    inputs, fl = [], []
    for k, (t, f, vol) in enumerate(events):
        inputs += ["-i", f]
        fl.append(f"[{k}:a]aresample=44100,aformat=sample_fmts=fltp:channel_layouts=mono,volume={vol},adelay={int(t * 1000)}:all=1[a{k}]")
    fl.append("".join(f"[a{k}]" for k in range(len(events))) +
              f"amix=inputs={len(events)}:normalize=0:duration=longest,apad=whole_dur={total},atrim=0:{total},alimiter=limit=0.95,"
              f"loudnorm=I=-16:TP=-1.5:LRA=11[out]")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *inputs, "-filter_complex", ";".join(fl),
                    "-map", "[out]", "-ac", "2", "-ar", "44100", out], check=True)


def page(p, html):
    exe = "/usr/bin/google-chrome" if os.path.exists("/usr/bin/google-chrome") else None
    b = p.chromium.launch(executable_path=exe, args=["--no-sandbox", "--disable-gpu", "--font-render-hinting=none"])
    pg = b.new_page(viewport={"width": W, "height": H})
    pg.goto("file://" + html)
    if not pg.evaluate("ready()"):
        raise SystemExit("fonts did not load")
    return b, pg


def sheet(paths, out, cols=4, w=270):
    from PIL import Image, ImageDraw
    hh = int(w * H / W)
    rows = (len(paths) + cols - 1) // cols
    im = Image.new("RGB", (cols * w + (cols + 1) * 8, rows * (hh + 30) + 8), "#222")
    dr = ImageDraw.Draw(im)
    for i, (p, lab) in enumerate(paths):
        x, y = 8 + (i % cols) * (w + 8), 8 + (i // cols) * (hh + 30)
        im.paste(Image.open(p).resize((w, hh)), (x, y + 22))
        dr.text((x + 4, y + 4), lab, fill="#fff")
    im.save(out, quality=88)


def main(path, preview=False, audio_only=False):
    d = json.load(open(path, encoding="utf-8"))
    tag = d["tag"]
    bdir = os.path.join(HERE, "build", tag); odir = os.path.join(HERE, "out")
    os.makedirs(bdir, exist_ok=True); os.makedirs(odir, exist_ok=True)
    missing = [k for k in emoji_keys(d) if not os.path.exists(os.path.join(STUDIO, "assets", "emoji", k + ".png"))]
    if missing:
        subprocess.run([sys.executable, os.path.join(STUDIO, "fetch_emoji.py"), *missing], check=True)
    scenes = {"main": main_scene(d), "end": end_scene(d)}
    html = os.path.join(bdir, "reel.html")
    open(html, "w", encoding="utf-8").write(
        "<!doctype html><html lang='fa'><head><meta charset='utf-8'><style>" + font_css() + CSS + "</style></head><body>"
        "<div id='bg'></div><div id='grid'></div><div id='stage'></div><script>"
        + JS.replace("__SCENES__", json.dumps(scenes, ensure_ascii=False)).replace("__SAFE__", str(SAFE_BOTTOM)) + "</script></body></html>")
    total = d["dur"] + END
    video = os.path.join(bdir, "video.mp4")
    if audio_only and os.path.exists(video):
        return mux(d, bdir, odir, video, total)
    with sync_playwright() as p:
        b, pg = page(p, html)
        if preview:
            pg.evaluate("show('main')")
            pg.evaluate(f"seek({d['dur'] * 1000 - 50})")
            issues = pg.evaluate("layout()")
            times = [x / 10 for x in range(3, int(d["dur"] * 10), 16)] + [d["dur"] - .05]
            shots = []
            for t in times:
                pg.evaluate(f"seek({t * 1000})")
                f = os.path.join(bdir, f"prev_{t:05.2f}.jpg"); pg.screenshot(path=f, type="jpeg", quality=85)
                shots.append((f, f"{t:.1f}s"))
            pg.evaluate("show('end')"); pg.evaluate("seek(1500)")
            f = os.path.join(bdir, "prev_end.jpg"); pg.screenshot(path=f, type="jpeg", quality=85); shots.append((f, "end"))
            b.close()
            sheet(shots, os.path.join(bdir, "sheet.jpg"))
            print("layout:", "ok" if not issues else issues)
            print("sheet:", os.path.join(bdir, "sheet.jpg"))
            return
        tmp = video[:-4] + ".part.mp4"
        proc = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "image2pipe", "-framerate", str(FPS), "-c:v", "mjpeg", "-i", "-",
                                 "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-pix_fmt", "yuv420p", "-r", str(FPS), tmp],
                                stdin=subprocess.PIPE)
        for key, dur in (("main", d["dur"]), ("end", END)):
            pg.evaluate(f"show('{key}')")
            for f in range(round(dur * FPS)):
                pg.evaluate(f"seek({f * 1000 / FPS})")
                proc.stdin.write(pg.screenshot(type="jpeg", quality=92))
        proc.stdin.close()
        if proc.wait() != 0:
            raise SystemExit("ffmpeg failed")
        os.replace(tmp, video); b.close()
    mux(d, bdir, odir, video, total)


def mux(d, bdir, odir, video, total):
    tag = d["tag"]
    ev = [(0.0, make_music(total, [], os.path.join(bdir, "music.wav"), bpm=100, level_db=-21.0, prog=PROG, pluck_decay=.3), 1.0),
          (0.0, f"{SFX}/whoosh.wav", .35)]
    ev += [(t, f"{SFX}/{name}.wav", gain) for t, name, gain in d["sfx"]]
    if d["kind"] == "quiz":
        ev += [(d["t_count"] + k, f"{SFX}/tick.wav", .5) for k in range(d["think"])]
        ev += [(d["t_reveal"], f"{SFX}/ding.wav", .45)]
    ev += [(d["dur"], f"{SFX}/whoosh.wav", .3), (d["dur"] + .4, f"{SFX}/pop.wav", .35)]
    wav = os.path.join(bdir, "audio.wav"); build_audio(ev, total, wav)
    out = os.path.join(odir, f"{tag}.mp4"); tmp = out[:-4] + ".part.mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", video, "-i", wav, "-map", "0:v", "-map", "1:a", "-c:v", "copy",
                    "-c:a", "aac", "-b:a", "160k", "-ar", "44100", "-ac", "2", "-shortest", "-movflags", "+faststart", tmp], check=True)
    os.replace(tmp, out)
    print("reel:", out, round(total, 2), "s")


if __name__ == "__main__":
    main(sys.argv[1], preview="--preview" in sys.argv, audio_only="--audio" in sys.argv)
