"""Painted backgrounds (SVG -> PNG, cached)."""
import math, os, random
from PIL import Image, ImageFilter
from film import svg_render, W, H
from paths import BG as BGDIR

def cached(name, fn, blur=0):
    path = f"{BGDIR}/{name}.png"
    if not os.path.exists(path):
        im = fn()
        if blur:
            im = im.filter(ImageFilter.GaussianBlur(blur))
        im.save(path)
    return Image.open(path).convert("RGBA")

# ------------------------------------------------------------------ helpers
FILTERS = ('<filter id="b3"><feGaussianBlur stdDeviation="3"/></filter><filter id="b6"><feGaussianBlur stdDeviation="6"/></filter>'
           '<filter id="b12"><feGaussianBlur stdDeviation="12"/></filter><filter id="b20"><feGaussianBlur stdDeviation="20"/></filter>'
           '<filter id="b40"><feGaussianBlur stdDeviation="40"/></filter>')

def lg(id_, stops, vertical=True):
    a = 'x1="0" y1="0" x2="0" y2="1"' if vertical else 'x1="0" y1="0" x2="1" y2="0"'
    return f'<linearGradient id="{id_}" {a}>' + "".join(f'<stop offset="{o}" stop-color="{c}" stop-opacity="{op}"/>' for o, c, op in stops) + '</linearGradient>'

def rg(id_, cx, cy, r, stops):
    return (f'<radialGradient id="{id_}" cx="{cx}" cy="{cy}" r="{r}" gradientUnits="userSpaceOnUse">' +
            "".join(f'<stop offset="{o}" stop-color="{c}" stop-opacity="{op}"/>' for o, c, op in stops) + '</radialGradient>')

def ridge(w, base, amp, seed, n=40, rough=0.35, x0=0):
    r = random.Random(seed); ys = []; y = 0
    for i in range(n + 1):
        y = y * 0.6 + r.uniform(-1, 1); ys.append(y)
    pts = [(x0 + w * i / n, base - amp * (0.5 + 0.5 * math.sin(i * 0.37 + seed)) - amp * rough * ys[i]) for i in range(n + 1)]
    return f"M {x0} {base+3000} L " + " L ".join(f"{x:.0f} {y:.0f}" for x, y in pts) + f" L {x0+w} {base+3000} Z"

def hill(w, base, amp, seed, n=12, x0=0):
    r = random.Random(seed)
    pts = [(x0 + w * i / n, base - amp * (0.5 + 0.5 * math.sin(i * 0.8 + seed)) + r.uniform(-amp * 0.15, amp * 0.15)) for i in range(n + 1)]
    d = f"M {x0} {base+3000} L {pts[0][0]:.0f} {pts[0][1]:.0f} "
    for i in range(1, len(pts)):
        (xa, ya), (xb, yb) = pts[i - 1], pts[i]
        d += f"Q {xa + (xb-xa)/2:.0f} {min(ya, yb) - 10:.0f} {xb:.0f} {yb:.0f} "
    return d + f"L {x0+w} {base+3000} Z"

def clouds(w, seed, ys, col="#f7a58a", hi="#ffd2a0", op=0.55):
    r = random.Random(seed); out = ""
    for y in ys:
        x = r.uniform(-200, w)
        for k in range(3):
            L = r.uniform(260, 520); hh = r.uniform(10, 24)
            out += (f'<path d="M {x:.0f} {y:.0f} C {x+L*0.3:.0f} {y-hh:.0f}, {x+L*0.7:.0f} {y-hh*1.3:.0f}, {x+L:.0f} {y:.0f} '
                    f'C {x+L*0.6:.0f} {y+hh*0.6:.0f}, {x+L*0.3:.0f} {y+hh*0.5:.0f}, {x:.0f} {y:.0f} Z" fill="{col}" opacity="{op}" filter="url(#b6)"/>'
                    f'<path d="M {x+L*0.1:.0f} {y+hh*0.25:.0f} C {x+L*0.4:.0f} {y+hh*0.5:.0f}, {x+L*0.7:.0f} {y+hh*0.4:.0f}, {x+L*0.95:.0f} {y+hh*0.1:.0f}" '
                    f'stroke="{hi}" stroke-width="4" fill="none" opacity="0.7" filter="url(#b6)"/>')
            x += L * r.uniform(0.6, 1.1); y += r.uniform(-14, 14)
    return out

def puffy(cx, cy, w, h, seed, col, shade):
    r = random.Random(seed); out = ""
    for i in range(9):
        x = cx + r.uniform(-w / 2, w / 2); y = cy + r.uniform(-h / 3, h / 3); rr = r.uniform(h * 0.35, h * 0.6)
        out += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{rr:.0f}" fill="{col}"/>'
    out += f'<ellipse cx="{cx}" cy="{cy + h * 0.35:.0f}" rx="{w * 0.55:.0f}" ry="{h * 0.25:.0f}" fill="{shade}" opacity="0.6"/>'
    return f'<g filter="url(#b3)">{out}</g>'

def stars(seed, n, y1, w=W):
    r = random.Random(seed)
    return "".join(f'<circle cx="{r.uniform(0, w):.0f}" cy="{r.uniform(0, y1):.0f}" r="{r.uniform(0.8, 2.4):.1f}" fill="#fff" opacity="{r.uniform(0.4, 1):.2f}"/>' for _ in range(n))

def poplar(x, y, h, col="#4a6a3a", dark="#33502a"):
    return (f'<rect x="{x-5}" y="{y-h*0.25:.0f}" width="10" height="{h*0.25:.0f}" fill="#4a3424"/>'
            f'<path d="M {x} {y-h:.0f} C {x+h*0.16:.0f} {y-h*0.7:.0f}, {x+h*0.14:.0f} {y-h*0.3:.0f}, {x} {y-h*0.18:.0f} C {x-h*0.14:.0f} {y-h*0.3:.0f}, {x-h*0.16:.0f} {y-h*0.7:.0f}, {x} {y-h:.0f} Z" fill="{col}"/>'
            f'<path d="M {x} {y-h:.0f} C {x-h*0.16:.0f} {y-h*0.7:.0f}, {x-h*0.14:.0f} {y-h*0.3:.0f}, {x} {y-h*0.18:.0f} Z" fill="{dark}" opacity="0.7"/>')

def flat_house(x, y, w, h, wall="#b08866", shade="#8a6648", roof="#6a4a34", door=True, window=True, lit=False, snow=False):
    out = (f'<rect x="{x}" y="{y-h}" width="{w}" height="{h}" fill="{wall}" stroke="#3a2418" stroke-width="2"/>'
           f'<rect x="{x}" y="{y-h}" width="{w*0.25:.0f}" height="{h}" fill="{shade}" opacity="0.6"/>'
           f'<rect x="{x-6}" y="{y-h-12}" width="{w+12}" height="14" fill="{roof}" stroke="#3a2418" stroke-width="2"/>')
    for k in range(int(w // 34)):
        out += f'<rect x="{x + 10 + k*34}" y="{y-h-4}" width="8" height="8" fill="#3a2418"/>'
    if door:
        out += f'<rect x="{x + w*0.55:.0f}" y="{y - h*0.62:.0f}" width="{w*0.22:.0f}" height="{h*0.62:.0f}" fill="#4a2e1c" stroke="#2a180e" stroke-width="2"/>'
    if window:
        wc = "#ffc46a" if lit else "#2a1c14"
        out += f'<rect x="{x + w*0.18:.0f}" y="{y - h*0.7:.0f}" width="{w*0.16:.0f}" height="{h*0.2:.0f}" fill="{wc}" stroke="#2a180e" stroke-width="2"/>'
    if snow:
        out += f'<path d="M {x-8} {y-h-12} C {x+w*0.3:.0f} {y-h-26}, {x+w*0.7:.0f} {y-h-24}, {x+w+8} {y-h-12} Z" fill="#eef2f8"/>'
    return out

def grass_tufts(seed, y0, y1, n, col="#3e5a2a", hi="#7a9a4a", w=W):
    r = random.Random(seed); out = ""
    for _ in range(n):
        x = r.uniform(-20, w + 20); y = r.uniform(y0, y1); s = 0.5 + (y - y0) / max(1, (y1 - y0)) * 1.2
        for k in range(5):
            dx = r.uniform(-14, 14) * s; hgt = r.uniform(26, 60) * s
            out += f'<path d="M {x+dx:.0f} {y:.0f} q {r.uniform(-8,8)*s:.0f} {-hgt/2:.0f} {r.uniform(-14,14)*s:.0f} {-hgt:.0f}" stroke="{col if k%2 else hi}" stroke-width="{2.5*s:.1f}" fill="none" stroke-linecap="round"/>'
    return out

# ------------------------------------------------------------------ PART 1
def samarra_wide():
    s = ("<defs>" + FILTERS + lg("sky", [(0, "#2b2a5e", 1), (0.3, "#6a4a7e", 1), (0.48, "#d8786a", 1), (0.56, "#f7b06a", 1), (0.62, "#ffd090", 1)]) +
         rg("sun", 300, 1040, 600, [(0, "#fff0c0", 0.95), (0.25, "#ffb060", 0.45), (1, "#ff8040", 0)]) + lg("street", [(0, "#b48a62", 1), (1, "#6e4e36", 1)]) + "</defs>")
    s += f'<rect width="{W}" height="{H}" fill="url(#sky)"/>' + clouds(W, 4, [380, 520, 650, 760], "#e8909a", "#ffd0a0") + f'<rect width="{W}" height="{H}" fill="url(#sun)"/>'
    s += '<circle cx="300" cy="1040" r="64" fill="#fff2d0"/>'
    # far city: domes and flat roofs
    r = random.Random(7)
    far = ""
    x = -20
    while x < W:
        w = r.uniform(60, 140); h = r.uniform(80, 200)
        far += f'<rect x="{x:.0f}" y="{1060-h:.0f}" width="{w:.0f}" height="{h+200:.0f}" fill="#7a4a5e"/>'
        if r.random() < 0.3:
            far += f'<path d="M {x+w*0.15:.0f} {1060-h:.0f} Q {x+w/2:.0f} {1060-h-w*0.7:.0f} {x+w*0.85:.0f} {1060-h:.0f} Z" fill="#7a4a5e"/>'
        x += w + r.uniform(-10, 10)
    s += far + '<rect x="0" y="900" width="1080" height="300" fill="#f0a070" opacity="0.25" filter="url(#b40)"/>'
    # palms
    for px, ph in [(90, 380), (980, 420), (1040, 300)]:
        s += f'<path d="M {px} 1120 C {px-10} {1120-ph*0.5}, {px+10} {1120-ph*0.8}, {px} {1120-ph}" stroke="#3a2430" stroke-width="16" fill="none"/>'
        for a in range(0, 360, 45):
            ang = math.radians(a); L = 110
            s += f'<path d="M {px} {1120-ph} q {math.cos(ang)*L*0.5:.0f} {math.sin(ang)*L*0.3-30:.0f} {math.cos(ang)*L:.0f} {math.sin(ang)*L*0.5+20:.0f}" stroke="#3a2430" stroke-width="14" fill="none" stroke-linecap="round"/>'
    # city wall + gate
    s += '<rect x="0" y="880" width="1080" height="320" fill="#a07858"/><rect x="0" y="880" width="1080" height="320" fill="#5a3a40" opacity="0.35"/>'
    for i in range(24):
        s += f'<rect x="{i*48}" y="856" width="30" height="30" fill="#a07858"/><rect x="{i*48}" y="856" width="30" height="30" fill="#5a3a40" opacity="0.35"/>'
    s += ('<rect x="560" y="760" width="300" height="440" fill="#946c4e"/><rect x="560" y="760" width="300" height="440" fill="#5a3a40" opacity="0.3"/>'
          '<path d="M 640 1200 L 640 960 Q 710 870, 780 960 L 780 1200 Z" fill="#2a1a20"/>'
          '<path d="M 650 1200 L 650 965 Q 710 885, 770 965 L 770 1200" fill="none" stroke="#c9a070" stroke-width="6"/>')
    for i in range(7):
        s += f'<rect x="{560 + i*44}" y="736" width="28" height="28" fill="#946c4e"/>'
    for bx in (590, 830, 120, 400):
        s += f'<rect x="{bx}" y="{700 if bx in (590, 830) else 790}" width="6" height="200" fill="#2a1a1a"/><path d="M {bx+6} {706 if bx in (590,830) else 796} l 80 10 l -6 60 l 6 60 l -80 -10 Z" fill="#141014"/>'
    # street + far-side crowd zone shading
    s += '<rect x="0" y="1180" width="1080" height="740" fill="url(#street)"/>'
    s += '<rect x="0" y="1180" width="1080" height="40" fill="#000" opacity="0.18"/>'
    return svg_render(s)

def samarra_close():
    s = ("<defs>" + FILTERS + lg("sky", [(0, "#3a2e66", 1), (0.35, "#8a5272", 1), (0.6, "#e88c6a", 1), (0.8, "#ffc888", 1)]) + "</defs>")
    s += f'<rect width="{W}" height="{H}" fill="url(#sky)"/>' + clouds(W, 9, [420, 600, 760, 900], "#f0a0a0", "#ffd8b0", 0.7)
    s += '<circle cx="220" cy="1250" r="140" fill="#ffe0a8" opacity="0.8" filter="url(#b20)"/>'
    s += '<rect x="0" y="1300" width="1080" height="700" fill="#8a5a50"/>'
    return svg_render(s)

def title_bg():
    s = ("<defs>" + FILTERS + lg("sky", [(0, "#0a0608", 1), (0.5, "#2a0a0a", 1), (0.75, "#5a1410", 1), (1, "#1a0806", 1)]) +
         rg("glow", 540, 1180, 700, [(0, "#ff5a2a", 0.7), (0.4, "#a01a10", 0.35), (1, "#200000", 0)]) + "</defs>")
    s += f'<rect width="{W}" height="{H}" fill="url(#sky)"/><rect width="{W}" height="{H}" fill="url(#glow)"/>'
    s += f'<path d="{ridge(W, 1300, 160, 31)}" fill="#120808"/>'
    s += ('<path d="M 430 1180 L 430 1060 L 470 1060 L 470 1030 L 520 1030 L 520 1000 L 560 1000 L 560 1030 L 610 1030 L 610 1060 L 650 1060 L 650 1180 Z" fill="#0a0404"/>'
          '<path d="M 330 1340 L 430 1180 L 650 1180 L 760 1340 Z" fill="#0a0404"/>')
    return svg_render(s)

def belalabad_wide():
    s = ("<defs>" + FILTERS + lg("sky", [(0, "#4a7ab8", 1), (0.35, "#9cc0d8", 1), (0.5, "#f2d6a8", 1)]) +
         lg("slope", [(0, "#7a9a4a", 1), (1, "#4a6a2e", 1)]) + lg("haze", [(0, "#f5e0b8", 0), (1, "#f5e0b8", 0.7)]) + "</defs>")
    s += f'<rect width="{W}" height="{H}" fill="url(#sky)"/>' + clouds(W, 2, [300, 430, 560], "#ffffff", "#fff8e8", 0.65)
    s += f'<path d="{ridge(W, 760, 220, 3, rough=0.5)}" fill="#8a94b4"/>'
    s += '<path d="M 140 560 L 210 600 L 260 590 L 300 640 L 180 640 Z" fill="#ffffff" opacity="0.8"/>'
    s += f'<rect x="0" y="560" width="{W}" height="300" fill="url(#haze)" opacity="0.6"/>'
    s += f'<path d="{hill(W, 880, 160, 5)}" fill="#6a8a54"/>'
    s += f'<rect x="0" y="760" width="{W}" height="220" fill="url(#haze)" opacity="0.35"/>'
    # village on the far slope
    r = random.Random(11)
    for i in range(14):
        x = 420 + r.uniform(0, 560); y = 860 + r.uniform(-40, 70)
        s += flat_house(int(x), int(y), int(r.uniform(60, 100)), int(r.uniform(44, 70)))
    for x in (380, 400, 980, 1010, 600):
        s += poplar(x, 900 + (x % 40), 160)
    # main slope (cows + boy walk here)
    s += f'<path d="M -50 1130 C 200 1060, 520 1040, 1130 1000 L 1130 2000 L -50 2000 Z" fill="url(#slope)"/>'
    s += '<path d="M -50 1130 C 200 1060, 520 1040, 1130 1000" stroke="#a8c070" stroke-width="6" fill="none" opacity="0.6"/>'
    s += '<path d="M 980 1012 C 820 1100, 560 1180, 300 1320 C 200 1380, 120 1460, 60 1600" stroke="#b49a6a" stroke-width="34" fill="none" opacity="0.8"/>'
    s += grass_tufts(4, 1060, 1900, 120)
    s += f'<rect x="0" y="1500" width="{W}" height="420" fill="#2a3a1a" opacity="0.35"/>'
    return svg_render(s)

def house_door():
    s = ("<defs>" + FILTERS + lg("sky", [(0, "#6a8ac0", 1), (0.6, "#f2c890", 1)]) + lg("wall", [(0, "#c49a70", 1), (1, "#9a7050", 1)]) + "</defs>")
    s += f'<rect width="{W}" height="{H}" fill="url(#sky)"/>'
    s += f'<path d="{hill(W, 1000, 220, 8)}" fill="#7a9a5a" filter="url(#b6)"/>'
    s += '<rect x="0" y="380" width="760" height="1100" fill="url(#wall)" stroke="#3a2418" stroke-width="4"/>'
    r = random.Random(5)
    for i in range(60):
        x = r.uniform(10, 720); y = r.uniform(400, 1440)
        s += f'<rect x="{x:.0f}" y="{y:.0f}" width="{r.uniform(40,90):.0f}" height="{r.uniform(20,34):.0f}" rx="8" fill="#8a6446" opacity="0.35"/>'
    s += '<rect x="-10" y="360" width="790" height="34" fill="#6a4a34" stroke="#3a2418" stroke-width="3"/>'
    for k in range(12):
        s += f'<rect x="{20 + k*64}" y="352" width="20" height="18" fill="#3a2418"/>'
    s += ('<rect x="300" y="640" width="300" height="760" fill="#3a2214" stroke="#1e110a" stroke-width="5"/>'
          '<rect x="320" y="660" width="260" height="740" fill="#5a3620"/>'
          + "".join(f'<rect x="{324 + k*52}" y="664" width="44" height="732" fill="#6a4228" stroke="#3a2214" stroke-width="2"/>' for k in range(5)) +
          '<circle cx="550" cy="1040" r="10" fill="#c9a24a"/>'
          '<path d="M 60 560 L 60 680 M 110 560 L 110 700 M 160 560 L 160 660" stroke="#5a7a3a" stroke-width="10"/>'
          '<ellipse cx="160" cy="1390" rx="80" ry="22" fill="#000" opacity="0.2"/>'
          '<path d="M 110 1390 C 90 1300, 110 1240, 160 1230 C 210 1240, 230 1300, 210 1390 Z" fill="#b0603a" stroke="#4a2414" stroke-width="3"/>')
    s += '<rect x="0" y="1400" width="1080" height="520" fill="#8a7a5a"/><rect x="0" y="1400" width="1080" height="30" fill="#000" opacity="0.2"/>'
    s += grass_tufts(9, 1430, 1900, 40, "#5a6a3a", "#8a9a5a")
    return svg_render(s)

def tree_hill():
    s = ("<defs>" + FILTERS + lg("sky", [(0, "#6a9ac8", 1), (0.45, "#f0d8a0", 1), (0.6, "#ffc878", 1)]) + lg("field", [(0, "#d8b860", 1), (1, "#9a7a3a", 1)]) +
         rg("sun", 900, 900, 600, [(0, "#fff4d0", 0.9), (0.3, "#ffd080", 0.4), (1, "#ffb060", 0)]) + "</defs>")
    s += f'<rect width="{W}" height="{H}" fill="url(#sky)"/>' + clouds(W, 6, [380, 520], "#ffffff", "#fff8e0", 0.6) + f'<rect width="{W}" height="{H}" fill="url(#sun)"/>'
    s += f'<path d="{ridge(W, 960, 140, 12)}" fill="#a8a4c0"/><path d="{hill(W, 1040, 120, 13)}" fill="#a8a060"/>'
    s += f'<path d="M -40 1260 C 200 1150, 600 1110, 1120 1160 L 1120 2000 L -40 2000 Z" fill="url(#field)"/>'
    s += '<path d="M 1000 1900 C 900 1600, 700 1400, 560 1230" stroke="#c8a870" stroke-width="40" fill="none" opacity="0.7"/>'
    r = random.Random(3)
    for i in range(140):
        x = r.uniform(-20, 1100); y = r.uniform(1200, 1900); sc = 0.5 + (y - 1200) / 700
        s += f'<path d="M {x:.0f} {y:.0f} q {r.uniform(-6,6)*sc:.0f} {-20*sc:.0f} {r.uniform(-4,10)*sc:.0f} {-48*sc:.0f}" stroke="#e8c870" stroke-width="{3*sc:.1f}" fill="none"/>'
    return svg_render(s)

def big_tree(scale=1.0):
    """big plane tree, transparent layer; trunk base at (0,0) in its own coords"""
    s = ('<path d="M -50 0 C -40 -160, -60 -300, -30 -420 L 30 -420 C 50 -300, 40 -160, 60 0 Z" fill="#5a3e2a" stroke="#2a1a10" stroke-width="4"/>'
         '<path d="M -50 0 C -40 -160, -60 -300, -30 -420 L -6 -420 C -14 -300, -20 -160, -10 0 Z" fill="#3a2818" opacity="0.6"/>'
         '<path d="M -30 -380 C -120 -440, -200 -470, -260 -520 M 20 -390 C 100 -450, 200 -480, 260 -540 M 0 -420 C 0 -500, 10 -560, 0 -640" stroke="#5a3e2a" stroke-width="26" fill="none" stroke-linecap="round"/>')
    r = random.Random(21)
    blobs = [(x, y, rr) for x, y, rr in ((r.uniform(-360, 360), r.uniform(-880, -440), r.uniform(80, 150)) for _ in range(46))]
    for col, dy, k in (("#2e4a1c", 18, 1.0), ("#3e6224", 0, 0.92), ("#55803a", -16, 0.7), ("#78a24a", -30, 0.42)):
        for x, y, rr in blobs:
            if k < 0.9 and (y > -560 + r.uniform(-60, 60) or x < -200 + r.uniform(-60, 60)):
                continue
            s += f'<circle cx="{x + (8 if k < 1 else 0):.0f}" cy="{y + dy:.0f}" r="{rr * k:.0f}" fill="{col}"/>'
    s += '<path d="M -40 -420 C -20 -470, 30 -470, 50 -420" stroke="#1e2e12" stroke-width="30" opacity="0.4" fill="none"/>'
    return f'<g transform="scale({scale})">{s}</g>'

def ground_close():
    """close ground under the tree: blurred far landscape + near grassy ground"""
    th = Image.open(f"{BGDIR}/tree_hill.png").convert("RGBA") if os.path.exists(f"{BGDIR}/tree_hill.png") else tree_hill()
    far = th.crop((200, 700, 880, 1300)).resize((W, 960), Image.BICUBIC).filter(ImageFilter.GaussianBlur(10))
    base = Image.new("RGBA", (W, H)); base.paste(far, (0, 0))
    s = ("<defs>" + FILTERS + lg("g", [(0, "#c8a858", 1), (0.4, "#a8883e", 1), (1, "#6a5a26", 1)]) + "</defs>")
    s += f'<path d="M 0 820 C 300 780, 700 800, 1080 790 L 1080 1920 L 0 1920 Z" fill="url(#g)"/>'
    r = random.Random(8)
    for i in range(260):
        x = r.uniform(-20, 1100); y = r.uniform(820, 1900); sc = 0.6 + (y - 820) / 900
        s += f'<path d="M {x:.0f} {y:.0f} q {r.uniform(-8,8)*sc:.0f} {-22*sc:.0f} {r.uniform(-6,12)*sc:.0f} {-54*sc:.0f}" stroke="#{r.choice(["e8c870","c8a850","8a7a30"])}" stroke-width="{3*sc:.1f}" fill="none" stroke-linecap="round"/>'
    for i in range(30):
        x = r.uniform(0, 1080); y = r.uniform(900, 1900)
        s += f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{r.uniform(40,120):.0f}" ry="{r.uniform(10,26):.0f}" fill="#fff4c0" opacity="0.18" filter="url(#b6)"/>'
    top = svg_render(s)
    base.alpha_composite(top)
    return base

def stable():
    s = ("<defs>" + FILTERS + lg("wall", [(0, "#4a3020", 1), (1, "#2a1a10", 1)]) + "</defs>")
    s += f'<rect width="{W}" height="{H}" fill="url(#wall)"/>'
    for k in range(12):
        s += f'<rect x="{k*94}" y="0" width="86" height="1300" fill="#5a3a24" stroke="#2a1a10" stroke-width="3"/>'
    s += '<rect x="0" y="380" width="1080" height="40" fill="#3a2414"/><rect x="0" y="820" width="1080" height="34" fill="#3a2414"/>'
    for k in range(3):
        x = 180 + k * 300
        s += f'<path d="M {x} 0 L {x+40} 0 L {x+260} 1300 L {x+140} 1300 Z" fill="#ffe4a8" opacity="0.12" filter="url(#b12)"/>'
    s += '<rect x="0" y="1300" width="1080" height="620" fill="#6a5030"/>'
    r = random.Random(4)
    for i in range(160):
        x = r.uniform(0, 1080); y = r.uniform(1300, 1900)
        s += f'<path d="M {x:.0f} {y:.0f} l {r.uniform(-30,30):.0f} {r.uniform(-8,8):.0f}" stroke="#c8a860" stroke-width="3" opacity="0.7"/>'
    s += '<path d="M 760 1300 C 780 1180, 880 1150, 1000 1170 C 1060 1180, 1090 1240, 1090 1300 Z" fill="#c8a050" stroke="#6a4a20" stroke-width="3"/>'
    s += '<rect x="0" y="900" width="1080" height="18" fill="#2a1a10" opacity="0.6"/>'
    return svg_render(s)

def night_fire():
    s = ("<defs>" + FILTERS + lg("sky", [(0, "#070a1e", 1), (0.6, "#1a2244", 1), (1, "#2a2a40", 1)]) + "</defs>")
    s += f'<rect width="{W}" height="{H}" fill="url(#sky)"/>' + stars(3, 220, 1000)
    s += '<path d="M 0 300 C 300 260, 700 380, 1080 320" stroke="#c8d0ff" stroke-width="80" opacity="0.05" filter="url(#b40)" fill="none"/>'
    s += f'<path d="{ridge(W, 1080, 160, 17)}" fill="#141a2e"/><path d="{hill(W, 1180, 80, 19)}" fill="#0e1220"/>'
    s += '<rect x="0" y="1200" width="1080" height="720" fill="#1a1612"/>'
    s += '<ellipse cx="540" cy="1260" rx="420" ry="90" fill="#ff9a40" opacity="0.18" filter="url(#b40)"/>'
    return svg_render(s)

def bazaar():
    s = ("<defs>" + FILTERS + lg("air", [(0, "#3a2416", 1), (1, "#7a5232", 1)]) + "</defs>")
    s += f'<rect width="{W}" height="{H}" fill="url(#air)"/>'
    vx, vy = 540, 930
    for k in range(9, 0, -1):
        f = k / 9
        w = 60 + 1100 * f ** 1.6; h = 120 + 1500 * f ** 1.6
        x0 = vx - w / 2; y0 = vy - h * 0.62
        col = 110 + int(90 * f)
        s += (f'<path d="M {x0:.0f} {y0+h:.0f} L {x0:.0f} {y0+h*0.35:.0f} Q {vx:.0f} {y0-h*0.08:.0f} {x0+w:.0f} {y0+h*0.35:.0f} L {x0+w:.0f} {y0+h:.0f} '
              f'L {x0+w+60*f:.0f} {y0+h:.0f} L {x0+w+60*f:.0f} {y0+h*0.2:.0f} L {x0-60*f:.0f} {y0+h*0.2:.0f} L {x0-60*f:.0f} {y0+h:.0f} Z" '
              f'fill="rgb({col},{int(col*0.72)},{int(col*0.5)})" stroke="#2a180e" stroke-width="{2+2*f:.1f}"/>')
        s += f'<ellipse cx="{vx}" cy="{y0+h*0.12:.0f}" rx="{w*0.06:.0f}" ry="{h*0.02:.0f}" fill="#fff0c0" opacity="0.8"/>'
        s += f'<path d="M {vx-w*0.03:.0f} {y0+h*0.12:.0f} L {vx+w*0.03:.0f} {y0+h*0.12:.0f} L {vx+w*0.12:.0f} {y0+h:.0f} L {vx-w*0.12:.0f} {y0+h:.0f} Z" fill="#ffe8b0" opacity="0.06"/>'
    r = random.Random(6)
    for side in (-1, 1):
        for k in range(6):
            f = 0.35 + k * 0.13
            x = vx + side * (120 + 420 * f ** 1.5); y = vy + 30 + 700 * f ** 1.5
            ww = 90 * f ** 1.2 * 2.2; hh = 160 * f ** 1.2 * 2
            cols = ["#a8342a", "#3a6a8a", "#c8962a", "#5a7a3a", "#8a4a7a"]
            s += f'<rect x="{x-ww/2:.0f}" y="{y-hh:.0f}" width="{ww:.0f}" height="{hh:.0f}" fill="#2a180e" opacity="0.8"/>'
            for j in range(4):
                s += f'<rect x="{x-ww/2+j*ww/4:.0f}" y="{y-hh:.0f}" width="{ww/4-2:.0f}" height="{hh*0.6:.0f}" fill="{r.choice(cols)}" opacity="0.9"/>'
            s += f'<ellipse cx="{x:.0f}" cy="{y-hh-20*f:.0f}" rx="{14*f:.0f}" ry="{18*f:.0f}" fill="#ffc060"/>'
    s += '<rect x="0" y="1400" width="1080" height="520" fill="#6a4a30"/>'
    return svg_render(s)

def village_winter_dusk():
    s = ("<defs>" + FILTERS + lg("sky", [(0, "#2a3a6a", 1), (0.5, "#8a7aa0", 1), (0.62, "#e8a890", 1)]) + "</defs>")
    s += f'<rect width="{W}" height="{H}" fill="url(#sky)"/>' + clouds(W, 8, [420, 560], "#c8a8c0", "#f0d0d0", 0.5)
    s += f'<path d="{ridge(W, 900, 200, 33, rough=0.5)}" fill="#8a90b0"/><path d="{ridge(W, 900, 200, 33, rough=0.5)}" fill="#eef2fa" opacity="0.5" transform="translate(0,-6)"/>'
    s += f'<path d="{hill(W, 1040, 120, 35)}" fill="#c8d0e0"/>'
    r = random.Random(12)
    for i in range(9):
        x = 100 + i * 110 + r.uniform(-20, 20); y = 1060 + r.uniform(-20, 40)
        s += flat_house(int(x), int(y), int(r.uniform(70, 100)), int(r.uniform(50, 70)), wall="#8a7a7a", shade="#6a5a62", roof="#5a4a50", lit=(i in (2, 5, 7)), snow=True)
    s += '<path d="M -40 1300 C 300 1220, 700 1180, 1120 1200 L 1120 2000 L -40 2000 Z" fill="#dfe6f2"/>'
    s += '<path d="M 540 1240 C 520 1400, 400 1600, 300 1920" stroke="#b8c0d4" stroke-width="60" fill="none" opacity="0.6"/>'
    return svg_render(s)

def blizzard():
    s = ("<defs>" + FILTERS + lg("sky", [(0, "#0a1020", 1), (0.6, "#1e2a46", 1), (1, "#3a4a66", 1)]) + "</defs>")
    s += f'<rect width="{W}" height="{H}" fill="url(#sky)"/>'
    s += f'<path d="{ridge(W, 980, 260, 41, rough=0.6)}" fill="#2a3450"/><path d="{ridge(W, 980, 260, 41, rough=0.6)}" fill="#c8d4e8" opacity="0.25"/>'
    s += f'<path d="M -40 1280 C 300 1200, 700 1180, 1120 1230 L 1120 2000 L -40 2000 Z" fill="#9aa8c0"/>'
    s += '<rect x="0" y="900" width="1080" height="600" fill="#c8d4e8" opacity="0.25" filter="url(#b40)"/>'
    return svg_render(s)

def interior():
    s = ("<defs>" + FILTERS + lg("wall", [(0, "#3a2418", 1), (1, "#5a3a24", 1)]) +
         rg("fire", 230, 1200, 760, [(0, "#ffb060", 0.6), (0.4, "#c86a30", 0.25), (1, "#000", 0)]) + "</defs>")
    s += f'<rect width="{W}" height="{H}" fill="url(#wall)"/>'
    r = random.Random(14)
    for i in range(70):
        x = r.uniform(0, 1080); y = r.uniform(200, 1300)
        s += f'<rect x="{x:.0f}" y="{y:.0f}" width="{r.uniform(50,110):.0f}" height="{r.uniform(26,40):.0f}" rx="8" fill="#2a1a10" opacity="0.3"/>'
    s += '<rect x="0" y="160" width="1080" height="44" fill="#2a180e"/>' + "".join(f'<rect x="{x}" y="120" width="40" height="120" fill="#24140a"/>' for x in (80, 380, 680, 980))
    # hearth (left)
    s += ('<path d="M 60 1320 L 60 940 Q 230 820, 400 940 L 400 1320 Z" fill="#6a5a50" stroke="#2a1a10" stroke-width="5"/>'
          '<path d="M 110 1320 L 110 1000 Q 230 910, 350 1000 L 350 1320 Z" fill="#140a06"/>'
          '<rect x="40" y="920" width="380" height="30" fill="#5a4a40" stroke="#2a1a10" stroke-width="4"/>')
    # door (right)
    s += ('<rect x="760" y="640" width="260" height="680" fill="#2a1a10"/>'
          '<rect x="780" y="660" width="220" height="660" fill="#5a3620" stroke="#2a180e" stroke-width="4"/>'
          + "".join(f'<rect x="{784 + k*44}" y="664" width="38" height="652" fill="#6a4228" stroke="#3a2214" stroke-width="2"/>' for k in range(5)) +
          '<rect x="780" y="760" width="220" height="16" fill="#3a2214"/><rect x="780" y="1180" width="220" height="16" fill="#3a2214"/>'
          '<circle cx="808" cy="990" r="10" fill="#c9a24a"/>')
    # shelf, pots, window
    s += ('<rect x="470" y="700" width="230" height="14" fill="#4a2e1a"/>'
          '<path d="M 490 700 C 480 650, 500 630, 520 628 C 545 630, 560 650, 548 700 Z" fill="#a85a30" stroke="#3a1a0a" stroke-width="3"/>'
          '<path d="M 580 700 C 574 664, 590 650, 610 650 C 630 650, 644 664, 636 700 Z" fill="#7a6a4a" stroke="#3a1a0a" stroke-width="3"/>'
          '<rect x="470" y="400" width="150" height="180" fill="#1a2440" stroke="#2a180e" stroke-width="8"/><path d="M 545 400 L 545 580 M 470 490 L 620 490" stroke="#2a180e" stroke-width="6"/>')
    s += '<rect x="0" y="1320" width="1080" height="600" fill="#4a3020"/>'
    s += ('<path d="M 180 1480 L 900 1480 L 1000 1860 L 80 1860 Z" fill="#7a1e1e" stroke="#2a0a0a" stroke-width="4"/>'
          '<path d="M 230 1520 L 860 1520 L 940 1820 L 140 1820 Z" fill="none" stroke="#d8a64a" stroke-width="10"/>'
          '<path d="M 400 1600 L 680 1600 L 720 1740 L 360 1740 Z" fill="#2a3a6a" opacity="0.8"/>')
    s += f'<rect width="{W}" height="{H}" fill="url(#fire)"/>'
    return svg_render(s)

def doorway():
    """inside looking out through the open door into the blizzard night"""
    s = ("<defs>" + FILTERS + lg("night", [(0, "#0e1830", 1), (1, "#3a4a6a", 1)]) + lg("wall", [(0, "#3a2418", 1), (1, "#4a2e1c", 1)]) +
         rg("warm", 540, 1500, 900, [(0, "#ffa050", 0.35), (1, "#000", 0)]) + "</defs>")
    s += f'<rect width="{W}" height="{H}" fill="url(#wall)"/>'
    s += '<rect x="250" y="420" width="580" height="1100" fill="url(#night)"/>'
    s += f'<g><clipPath id="dc"><rect x="250" y="420" width="580" height="1100"/></clipPath><g clip-path="url(#dc)">'
    s += f'<path d="{ridge(W, 1100, 200, 51)}" fill="#24304a"/><path d="M 0 1300 C 400 1250, 700 1260, 1080 1240 L 1080 1600 L 0 1600 Z" fill="#aab6cc"/>'
    s += '</g></g>'
    s += '<rect x="230" y="400" width="620" height="22" fill="#2a180e"/><rect x="230" y="400" width="22" height="1120" fill="#2a180e"/><rect x="828" y="400" width="22" height="1120" fill="#2a180e"/>'
    s += '<path d="M 830 420 L 1010 380 L 1010 1560 L 830 1520 Z" fill="#5a3620" stroke="#2a180e" stroke-width="4"/>'
    s += "".join(f'<path d="M {840 + k*34} {416 - k*8} L {840 + k*34} {1524 + k*8}" stroke="#3a2214" stroke-width="3"/>' for k in range(5))
    s += '<rect x="0" y="1520" width="1080" height="400" fill="#3e2818"/><path d="M 250 1520 L 830 1520 L 900 1620 L 180 1620 Z" fill="#c8d4e8" opacity="0.5"/>'
    s += f'<rect width="{W}" height="{H}" fill="url(#warm)"/>'
    return svg_render(s)

def grass_fg(seed=3, y0=1480, col=("#5a4a1a", "#7a6a2a", "#9a8a3a")):
    r = random.Random(seed); out = ""
    for i in range(320):
        x = r.uniform(-30, W + 30); hgt = r.uniform(280, 640); y = H + 20
        bend = r.uniform(-60, 60)
        out += (f'<path d="M {x-7:.0f} {y} Q {x+bend*0.4:.0f} {y-hgt*0.6:.0f} {x+bend:.0f} {y-hgt:.0f} Q {x+bend*0.4+4:.0f} {y-hgt*0.6:.0f} {x+7:.0f} {y} Z" '
                f'fill="{r.choice(col)}"/>')
    return svg_render(out).filter(ImageFilter.GaussianBlur(2.5))

# ------------------------------------------------------------------ PART 2
def night_stable_snow():
    s = ("<defs>" + FILTERS + lg("sky", [(0, "#060a18", 1), (0.6, "#16203c", 1), (1, "#2a3450", 1)]) +
         rg("win", 230, 820, 420, [(0, "#ffb060", 0.55), (1, "#000", 0)]) + "</defs>")
    s += f'<rect width="{W}" height="{H}" fill="url(#sky)"/>' + stars(9, 120, 700)
    s += f'<path d="{ridge(W, 900, 180, 61)}" fill="#1c2640"/>'
    s += '<rect x="-20" y="520" width="440" height="780" fill="#4a3a3a" stroke="#1a1010" stroke-width="4"/><rect x="-20" y="500" width="460" height="30" fill="#3a2a2a"/>'
    s += '<path d="M -20 500 C 100 480, 300 480, 440 500 L 440 520 L -20 520 Z" fill="#e8eef8"/>'
    s += '<rect x="180" y="760" width="110" height="120" fill="#ffc46a" stroke="#1a1010" stroke-width="6"/><path d="M 235 760 L 235 880 M 180 820 L 290 820" stroke="#1a1010" stroke-width="5"/>'
    s += f'<rect width="{W}" height="{H}" fill="url(#win)"/>'
    # lean-to shelter for the horses
    s += ('<path d="M 520 640 L 1100 600 L 1100 640 L 520 690 Z" fill="#4a3220" stroke="#1a1008" stroke-width="4"/>'
          '<path d="M 520 630 L 1100 590 L 1100 606 L 520 650 Z" fill="#e8eef8"/>'
          '<rect x="540" y="680" width="20" height="640" fill="#3a2414"/><rect x="1040" y="640" width="20" height="680" fill="#3a2414"/>'
          '<rect x="560" y="690" width="480" height="630" fill="#1a1410" opacity="0.65"/>')
    s += '<path d="M -40 1290 C 300 1250, 700 1250, 1120 1270 L 1120 2000 L -40 2000 Z" fill="#b8c4d8"/>'
    s += '<path d="M 640 1300 C 720 1260, 860 1250, 980 1280 L 990 1320 L 630 1320 Z" fill="#c8a050" stroke="#6a4a20" stroke-width="3"/>'
    return svg_render(s)

def dawn_house():
    s = ("<defs>" + FILTERS + lg("sky", [(0, "#3a4a80", 1), (0.35, "#b88aa8", 1), (0.5, "#f6b89a", 1), (0.58, "#ffd8b0", 1)]) +
         rg("sun", 820, 1000, 600, [(0, "#fff0d8", 0.85), (0.3, "#ffc8a0", 0.35), (1, "#ff9a80", 0)]) + "</defs>")
    s += f'<rect width="{W}" height="{H}" fill="url(#sky)"/>' + clouds(W, 5, [420, 560, 700], "#f0b0b8", "#ffe0d0", 0.6) + f'<rect width="{W}" height="{H}" fill="url(#sun)"/>'
    s += f'<path d="{ridge(W, 1040, 220, 71, rough=0.5)}" fill="#8a7aa0"/><path d="{ridge(W, 1040, 220, 71, rough=0.5)}" fill="#fff" opacity="0.35" transform="translate(0,-5)"/>'
    s += f'<path d="{hill(W, 1150, 110, 73)}" fill="#c8c0d8"/>'
    s += ('<rect x="-20" y="560" width="400" height="760" fill="#7a6a6e" stroke="#2a1a1e" stroke-width="4"/>'
          '<path d="M -20 560 C 100 540, 280 540, 400 560 L 400 580 L -20 580 Z" fill="#f2f4fa"/>'
          '<rect x="150" y="900" width="150" height="420" fill="#4a2e1c" stroke="#2a180e" stroke-width="4"/>')
    s += '<path d="M -40 1300 C 300 1270, 700 1270, 1120 1290 L 1120 2000 L -40 2000 Z" fill="#e6e8f2"/>'
    s += '<path d="M 400 1310 C 600 1400, 800 1600, 900 1920" stroke="#c8c8dc" stroke-width="70" fill="none" opacity="0.7"/>'
    return svg_render(s)

def bazz(palette="dusk"):
    if palette == "dusk":
        sky = lg("sky", [(0, "#283a78", 1), (0.3, "#9a8ac0", 1), (0.47, "#f6b88e", 1), (0.55, "#ffdcb0", 1)])
        sun = (240, 1120); mtn, lit = "#2e2638", "#5e4a68"
    else:
        sky = lg("sky", [(0, "#1e2250", 1), (0.32, "#7a4a74", 1), (0.5, "#f09a6a", 1), (0.6, "#ffd29a", 1)])
        sun = (860, 1240); mtn, lit = "#2a1e2c", "#6a4458"
    s = "<defs>" + FILTERS + sky + rg("sun", sun[0], sun[1], 620, [(0, "#fff2d0", 0.9), (0.25, "#ffc890", 0.45), (1, "#ff9a70", 0)]) + "</defs>"
    s += f'<rect width="{W}" height="{H}" fill="url(#sky)"/>' + clouds(W, 15, [360, 480, 600], "#f0b0b0", "#ffe0c8", 0.55) + f'<rect width="{W}" height="{H}" fill="url(#sun)"/>'
    s += f'<circle cx="{sun[0]}" cy="{sun[1]}" r="70" fill="#fff4dc"/>'
    s += f'<path d="{ridge(W, 1280, 200, 81)}" fill="#9a88a8"/>'
    base = 1000
    peak = ("M 120 1920 L 150 1500 L 260 1330 L 330 1200 L 380 1100 L 410 1000 L 440 880 L 470 780 L 780 780 L 820 860 L 870 960 L 940 1040 L 990 1010 "
            "L 1040 1100 L 1100 1250 L 1140 1920 Z")
    face = "M 120 1920 L 150 1500 L 260 1330 L 330 1200 L 380 1100 L 410 1000 L 440 880 L 470 780 L 560 1100 L 610 1500 L 640 1920 Z"
    s += f'<path d="{peak}" fill="{mtn}"/><path d="{face}" fill="{lit}" opacity="0.8"/>'
    s += '<path d="M 300 1290 L 440 1220 L 380 1150 L 470 1080 L 430 1010 L 490 940 L 455 870 L 480 810 L 520 780" stroke="#d8c0c8" stroke-width="4" fill="none" opacity="0.45"/>'
    walls = ('<rect x="480" y="680" width="290" height="104" fill="#1e1a26"/><rect x="450" y="610" width="70" height="174" fill="#1e1a26"/>'
             '<rect x="730" y="630" width="70" height="154" fill="#1e1a26"/><rect x="590" y="580" width="80" height="204" fill="#1e1a26"/>')
    walls += "".join(f'<rect x="{480+i*24}" y="668" width="12" height="14" fill="#1e1a26"/>' for i in range(12))
    walls += "".join(f'<rect x="{x}" y="{y}" width="12" height="14" fill="#1e1a26"/>' for x, y in [(450, 598), (476, 598), (504, 598), (590, 568), (614, 568), (640, 568), (660, 568), (730, 618), (756, 618), (786, 618)])
    walls += "".join(f'<rect x="{x}" y="{y}" width="9" height="13" fill="#ffb25e"/>' for x, y in [(480, 650), (620, 620), (650, 700), (760, 670), (540, 720)])
    s += walls
    s += f'<rect x="0" y="1050" width="{W}" height="900" fill="#fff" opacity="0.15" filter="url(#b40)"/>'
    return svg_render(s)

def cloud_sea(top, seed, w=W + 600, hi="#fff8f2", mid="#ead9de", lo="#c9c0d6"):
    r = random.Random(seed)
    parts = [f'<defs>{FILTERS}' + lg("cg", [(0, mid, 1), (1, lo, 1)]) + f'<radialGradient id="cb" cx="0.38" cy="0.3" r="0.8"><stop offset="0" stop-color="{hi}"/><stop offset="1" stop-color="{mid}"/></radialGradient></defs>',
             f'<rect x="0" y="{top + 70}" width="{w}" height="{H - top}" fill="url(#cg)"/>']
    for row in range(3):
        y = top + row * 60; x = -160
        while x < w + 160:
            rx = r.uniform(60, 150) * (1 + row * 0.3); ry = rx * r.uniform(0.42, 0.6)
            parts.append(f'<ellipse cx="{x:.0f}" cy="{y + r.uniform(-14, 18):.0f}" rx="{rx:.0f}" ry="{ry:.0f}" fill="url(#cb)"/>')
            x += rx * r.uniform(0.9, 1.4)
    doc = f'<g filter="url(#b3)">' + "".join(parts) + '</g>'
    from film import svg_render as sr
    return sr(doc, w, H)

def fog_battle():
    s = ("<defs>" + FILTERS + lg("sky", [(0, "#6a7480", 1), (0.6, "#9aa2a8", 1), (1, "#5a6066", 1)]) + "</defs>")
    s += f'<rect width="{W}" height="{H}" fill="url(#sky)"/>'
    s += f'<path d="{ridge(W, 1080, 120, 91)}" fill="#7a8088" opacity="0.7"/>'
    s += '<path d="M -40 1260 C 300 1230, 700 1240, 1120 1220 L 1120 2000 L -40 2000 Z" fill="#3e4246"/>'
    s += f'<rect x="0" y="1000" width="{W}" height="400" fill="#c8d0d6" opacity="0.4" filter="url(#b40)"/>'
    return svg_render(s)

def bedroom():
    s = ("<defs>" + FILTERS + lg("wall", [(0, "#24160e", 1), (1, "#3a2416", 1)]) +
         rg("candle", 820, 1060, 820, [(0, "#ffb060", 0.55), (0.5, "#a05a28", 0.2), (1, "#000", 0)]) + "</defs>")
    s += f'<rect width="{W}" height="{H}" fill="url(#wall)"/>'
    r = random.Random(17)
    for i in range(50):
        x = r.uniform(0, 1080); y = r.uniform(200, 1300)
        s += f'<rect x="{x:.0f}" y="{y:.0f}" width="{r.uniform(50,110):.0f}" height="{r.uniform(26,40):.0f}" rx="8" fill="#140a06" opacity="0.35"/>'
    s += ('<rect x="60" y="520" width="230" height="760" fill="#120a06"/><rect x="80" y="540" width="190" height="740" fill="#3a4a6a" opacity="0.5"/>'
          '<rect x="0" y="1280" width="1080" height="640" fill="#2a1a10"/>'
          '<rect x="300" y="1120" width="640" height="200" rx="14" fill="#4a2e1a" stroke="#1a0e06" stroke-width="5"/>'
          '<rect x="860" y="1060" width="40" height="230" fill="#3a2414"/><rect x="845" y="1050" width="70" height="16" fill="#5a3a20"/>')
    s += f'<rect width="{W}" height="{H}" fill="url(#candle)"/>'
    return svg_render(s)

def courtyard():
    s = ("<defs>" + FILTERS + lg("sky", [(0, "#e8b88a", 1), (0.5, "#f2c890", 1), (1, "#d89a68", 1)]) + lg("st", [(0, "#8a5e3c", 1), (1, "#5a3a24", 1)]) + "</defs>")
    s += f'<rect width="{W}" height="{H}" fill="url(#sky)"/>'
    s += '<rect x="0" y="520" width="1080" height="560" fill="url(#st)"/>' + "".join(f'<rect x="{i*48}" y="496" width="30" height="30" fill="#8a5e3c"/>' for i in range(24))
    s += ('<rect x="330" y="300" width="420" height="780" fill="#7a5034" stroke="#2a180e" stroke-width="4"/>'
          + "".join(f'<rect x="{330+i*44}" y="276" width="28" height="30" fill="#7a5034"/>' for i in range(10)) +
          '<path d="M 450 1080 L 450 760 Q 540 660, 630 760 L 630 1080 Z" fill="#2a1a10"/>'
          '<rect x="380" y="380" width="8" height="200" fill="#2a1a10"/><path d="M 388 386 l 110 14 l -8 70 l 8 70 l -110 -14 Z" fill="#a0161c"/>'
          '<rect x="700" y="380" width="8" height="200" fill="#2a1a10"/><path d="M 708 386 l 110 14 l -8 70 l 8 70 l -110 -14 Z" fill="#a0161c"/>')
    for i in range(5):
        y = 1080 + i * 46
        s += f'<rect x="{300 - i*60}" y="{y}" width="{480 + i*120}" height="46" fill="#{0x9a - i*8:02x}{0x6c - i*6:02x}{0x48 - i*4:02x}" stroke="#2a180e" stroke-width="2"/>'
    s += '<rect x="0" y="1310" width="1080" height="610" fill="#7a5638"/>'
    return svg_render(s)

def throne_hall():
    s = ("<defs>" + FILTERS + lg("dark", [(0, "#08070a", 1), (1, "#16121a", 1)]) + "</defs>")
    s += f'<rect width="{W}" height="{H}" fill="url(#dark)"/>'
    for x in (90, 300, 780, 990):
        s += f'<rect x="{x-40}" y="200" width="80" height="1150" fill="#1c1820"/><rect x="{x-50}" y="1300" width="100" height="50" fill="#24202a"/><rect x="{x-50}" y="190" width="100" height="40" fill="#24202a"/>'
    s += '<path d="M 470 0 L 610 0 L 760 1350 L 320 1350 Z" fill="#f2e4c8" opacity="0.10" filter="url(#b20)"/>'
    s += '<rect x="0" y="1350" width="1080" height="570" fill="#0e0c10"/><rect x="380" y="1300" width="320" height="50" fill="#2a2430"/><rect x="420" y="1250" width="240" height="50" fill="#322a38"/>'
    s += ('<path d="M 440 1250 L 440 860 Q 540 770, 640 860 L 640 1250 Z M 410 1060 L 670 1060 L 670 1130 L 410 1130 Z" fill="#060508" stroke="#c8a860" stroke-width="5"/>'
          '<circle cx="540" cy="840" r="16" fill="#c8a860"/>')
    return svg_render(s)

# ------------------------------------------------------------------ PART 3 (Babak, episode 2): the pass, the village, the snow, the ridge
def _strata(seed, x0, x1, y0, y1, n, col, op=0.35, w=3, slope=0.0):
    r = random.Random(seed); out = ""
    for _ in range(n):
        y = r.uniform(y0, y1); x = r.uniform(x0, x1); L = r.uniform(60, 240)
        out += f'<path d="M {x:.0f} {y:.0f} q {L*0.5:.0f} {r.uniform(-12,12) + slope*L*0.5:.0f} {L:.0f} {r.uniform(-8,8) + slope*L:.0f}" stroke="{col}" stroke-width="{w}" fill="none" opacity="{op}" stroke-linecap="round"/>'
    return out

def _cracks(seed, x0, x1, y0, y1, n, col="#3a2216", op=0.45):
    r = random.Random(seed); out = ""
    for _ in range(n):
        x = r.uniform(x0, x1); y = r.uniform(y0, y1); d = f"M {x:.0f} {y:.0f}"
        for k in range(r.randint(2, 4)):
            x += r.uniform(-30, 30); y += r.uniform(30, 90); d += f" L {x:.0f} {y:.0f}"
        out += f'<path d="{d}" stroke="{col}" stroke-width="{r.uniform(2,4):.1f}" fill="none" opacity="{op}" stroke-linejoin="round"/>'
    return out

def boulder(x, y, r, seed=0, col="#7e6a58", dark="#4a3c30", lit="#b0987e", rot=0.0):
    """an angular rock with lit and shaded facets, centre (x, y); transparent SVG"""
    rr = random.Random(seed); n = 8; pts = []
    for i in range(n):
        a = -math.pi / 2 + i / n * 2 * math.pi + rr.uniform(-0.18, 0.18)
        k = r * rr.uniform(0.84, 1.1)
        pts.append((x + math.cos(a) * k * 1.15, min(y + r * 0.72, y + math.sin(a) * k * 0.88)))
    cx, cy = x + r * rr.uniform(-0.25, 0.1), y - r * rr.uniform(0.0, 0.25)
    poly = lambda q: "M " + " L ".join(f"{a:.1f} {b:.1f}" for a, b in q) + " Z"
    sw = max(2.0, r * 0.045)
    out = f'<g transform="rotate({rot:.1f},{x:.1f},{y:.1f})" stroke-linejoin="round">'
    out += f'<path d="{poly(pts)}" fill="{col}" stroke="#1b0f0a" stroke-width="{sw:.1f}"/>'
    out += f'<path d="{poly([pts[-2], pts[-1], pts[0], pts[1], (cx, cy)])}" fill="{lit}" opacity="0.85"/>'
    out += f'<path d="{poly([pts[2], pts[3], pts[4], pts[5], (cx, cy)])}" fill="{dark}" opacity="0.75"/>'
    out += f'<path d="M {cx:.1f} {cy:.1f} L {pts[2][0]:.1f} {pts[2][1]:.1f} M {cx:.1f} {cy:.1f} L {pts[5][0]:.1f} {pts[5][1]:.1f} M {cx:.1f} {cy:.1f} L {pts[-2][0]:.1f} {pts[-2][1]:.1f}" stroke="#1b0f0a" stroke-width="{sw*0.6:.1f}" opacity="0.5"/>'
    return out + '</g>'

GORGE = {"noon": dict(sky=[(0, "#4f82c4", 1), (0.45, "#a2c4e0", 1), (0.7, "#f2e2c2", 1)], far="#98a2c0", wall="#b47c4c", wall_d="#7a4e32",
                      wall_l="#e6ae78", floor="#c29c6e", floor_d="#8a6a4a", haze="#f6e6ca"),
         "dust": dict(sky=[(0, "#7a6e66", 1), (0.45, "#c2a688", 1), (0.7, "#e6c8a0", 1)], far="#a89080", wall="#9a6a46", wall_d="#64402a",
                      wall_l="#cc9668", floor="#a88660", floor_d="#7a5a40", haze="#ead2b2")}

def gorge_floor(pal="noon"):
    """the floor of the narrow pass and its back wall; people walk across at feet y 1260-1520. Near side walls: gorge_walls()."""
    P = GORGE[pal]
    s = ("<defs>" + FILTERS + lg("sky", P["sky"]) + lg("fl", [(0, P["floor"], 1), (1, P["floor_d"], 1)]) +
         lg("hz", [(0, P["haze"], 0), (1, P["haze"], 0.85)]) + lg("bw", [(0, P["wall_l"], 1), (0.5, P["wall"], 1), (1, P["wall_d"], 1)]) + "</defs>")
    s += f'<rect width="{W}" height="{H}" fill="url(#sky)"/>' + clouds(W, 31, [250, 360], "#ffffff", "#fff8e8", 0.55)
    s += f'<path d="{ridge(W, 700, 150, 33, rough=0.5)}" fill="{P["far"]}"/><rect x="0" y="520" width="{W}" height="330" fill="url(#hz)" opacity="0.75"/>'
    back = "M -40 2000 L -40 690 L 110 640 L 210 700 L 330 590 L 430 650 L 520 560 L 640 625 L 730 585 L 850 665 L 960 600 L 1120 690 L 1120 2000 Z"
    s += f'<path d="{back}" fill="url(#bw)"/><path d="{back}" fill="{P["haze"]}" opacity="0.22"/>'
    s += _strata(34, -40, 1100, 690, 1190, 46, P["wall_d"], 0.35, 4) + _strata(35, -40, 1100, 650, 1150, 24, P["wall_l"], 0.4, 3)
    s += _cracks(36, 0, 1080, 650, 1060, 16, P["wall_d"], 0.4)
    for i, (x, y, r) in enumerate([(120, 1205, 46), (930, 1200, 52), (1010, 1215, 34), (60, 1222, 28)]):
        s += boulder(x, y, r, 300 + i, P["wall"], P["wall_d"], P["wall_l"])
    s += f'<path d="M -40 1235 C 200 1205, 800 1200, 1120 1228 L 1120 2000 L -40 2000 Z" fill="url(#fl)"/>'
    s += f'<path d="M -40 1235 C 200 1205, 800 1200, 1120 1228" stroke="{P["wall_d"]}" stroke-width="10" fill="none" opacity="0.45"/>'
    s += f'<path d="M -40 1420 C 300 1380, 700 1390, 1120 1430" stroke="{P["floor"]}" stroke-width="90" fill="none" opacity="0.5"/>'
    r = random.Random(37)
    for _ in range(80):
        x = r.uniform(-20, 1100); y = r.uniform(1245, 1900); sc = 0.4 + (y - 1245) / 655 * 1.4
        s += f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{r.uniform(8,22)*sc:.0f}" ry="{r.uniform(5,11)*sc:.0f}" fill="{P["floor_d"]}" opacity="0.7"/>'
    s += grass_tufts(38, 1245, 1900, 40, "#7a6a3a", "#a89a5a")
    s += f'<rect x="0" y="1560" width="{W}" height="360" fill="#000" opacity="0.12"/>'
    return svg_render(s)

def gorge_walls(pal="noon"):
    """near side walls of the pass, an fg layer (transparent in the middle)"""
    P = GORGE[pal]
    L = "M -60 -60 L 210 -60 L 180 220 L 225 430 L 165 720 L 200 930 L 140 1180 L 175 1420 L 110 1700 L 150 2000 L -60 2000 Z"
    R = "M 1140 -60 L 880 -60 L 905 250 L 860 480 L 925 770 L 885 1010 L 950 1260 L 915 1510 L 985 1760 L 965 2000 L 1140 2000 Z"
    s = "<defs>" + FILTERS + "</defs>"
    s += f'<path d="{L}" fill="{P["wall_d"]}"/><path d="{R}" fill="{P["wall"]}"/><path d="{R}" fill="#000" opacity="0.22"/>'
    s += f'<path d="M 210 -60 L 180 220 L 225 430 L 165 720 L 200 930 L 140 1180 L 175 1420 L 110 1700 L 150 2000" stroke="{P["wall_l"]}" stroke-width="12" fill="none" opacity="0.75" stroke-linejoin="round"/>'
    s += f'<path d="M 880 -60 L 905 250 L 860 480 L 925 770 L 885 1010 L 950 1260 L 915 1510 L 985 1760 L 965 2000" stroke="{P["wall_l"]}" stroke-width="8" fill="none" opacity="0.5" stroke-linejoin="round"/>'
    s += _strata(41, -60, 150, 0, 1900, 26, "#000", 0.25, 5) + _strata(42, 920, 1120, 0, 1900, 26, "#000", 0.22, 5)
    s += _cracks(43, -20, 150, 0, 1800, 9, "#2a160c", 0.5) + _cracks(44, 930, 1100, 0, 1800, 9, "#2a160c", 0.4)
    return svg_render(s)

def cliff_up():
    """looking up at the far wall of the pass: its rim with rocks against a hot sky (rim y≈600-700)"""
    s = ("<defs>" + FILTERS + lg("sky", [(0, "#2d5ca6", 1), (0.22, "#6a9ad2", 1), (0.36, "#d8e6ee", 1)]) +
         lg("wall", [(0, "#d49a64", 1), (0.35, "#a8703f", 1), (1, "#4e3220", 1)]) + "</defs>")
    s += f'<rect width="{W}" height="{H}" fill="url(#sky)"/>' + clouds(W, 51, [200, 330, 450], "#ffffff", "#fffaf0", 0.65)
    rim = [(-40, 700), (60, 660), (140, 690), (230, 610), (330, 650), (420, 600), (500, 640), (600, 590), (690, 630), (780, 575), (880, 640), (980, 600), (1120, 650)]
    wall = "M -40 2000 L " + " L ".join(f"{x} {y}" for x, y in rim) + " L 1120 2000 Z"
    s += f'<path d="{wall}" fill="url(#wall)"/>'
    r = random.Random(52)
    for _ in range(40):   # strata converge upward (we look up)
        y = r.uniform(700, 1900); x = r.uniform(-40, 1080); L = r.uniform(80, 260)
        s += f'<path d="M {x:.0f} {y:.0f} q {L/2:.0f} {-(y-600)*0.02:.0f} {L:.0f} {-(y-600)*0.05:.0f}" stroke="#5a3a22" stroke-width="{3 + (y-600)/300:.1f}" fill="none" opacity="0.35"/>'
    s += _cracks(53, 0, 1080, 700, 1800, 18, "#3a2216", 0.4)
    for i, (x, y, rr) in enumerate([(70, 650, 48), (250, 596, 60), (420, 586, 46), (700, 586, 58), (830, 566, 64), (960, 612, 44), (1050, 590, 54)]):
        s += boulder(x, y, rr, 60 + i, "#6a4c36", "#3a2818", "#c89a6a")
    s += '<path d="M -40 2000 L -40 -40 L 120 -40 L 150 300 L 90 700 L 130 1100 L 60 1500 L 100 2000 Z" fill="#3a2416"/>'
    s += '<path d="M 1120 2000 L 1120 -40 L 980 -40 L 950 260 L 1010 640 L 960 1000 L 1030 1400 L 990 2000 Z" fill="#4a2e1c"/>'
    s += f'<rect x="0" y="1300" width="{W}" height="620" fill="#000" opacity="0.18"/>'
    return svg_render(s)

def ridge_view():
    """on the ridge above the pass: afternoon sky, far ranges, the far rim of the gorge and the deep cut; near rocks (y 1250+)"""
    s = ("<defs>" + FILTERS + lg("sky", [(0, "#3a6aae", 1), (0.35, "#9cc0dc", 1), (0.52, "#f4dcb4", 1)]) +
         rg("sun", 880, 760, 520, [(0, "#fff4d8", 0.8), (0.3, "#ffd8a0", 0.35), (1, "#ffb070", 0)]) +
         lg("cut", [(0, "#4a3428", 1), (1, "#1e140e", 1)]) + lg("near", [(0, "#a8784c", 1), (1, "#6a4a30", 1)]) + "</defs>")
    s += f'<rect width="{W}" height="{H}" fill="url(#sky)"/>' + clouds(W, 61, [330, 450, 560], "#ffffff", "#fff4e0", 0.6) + f'<rect width="{W}" height="{H}" fill="url(#sun)"/>'
    s += f'<path d="{ridge(W, 900, 200, 62, rough=0.5)}" fill="#a2a6c2"/><path d="{ridge(W, 980, 150, 63, rough=0.4)}" fill="#8e8aa6"/>'
    s += f'<rect x="0" y="760" width="{W}" height="300" fill="#f4e0c0" opacity="0.35" filter="url(#b40)"/>'
    far = "M -40 2000 L -40 1040 L 120 1010 L 260 1050 L 400 1000 L 560 1045 L 700 1005 L 860 1050 L 1000 1015 L 1120 1040 L 1120 2000 Z"
    s += f'<path d="{far}" fill="#c08e5e"/>' + _strata(64, -40, 1100, 1040, 1180, 22, "#7a5234", 0.4, 3)
    s += '<path d="M -40 1150 C 300 1170, 700 1160, 1120 1150 L 1120 1320 L -40 1320 Z" fill="url(#cut)"/>'
    s += '<path d="M -40 1150 C 300 1170, 700 1160, 1120 1150" stroke="#e6b47e" stroke-width="5" fill="none" opacity="0.6"/>'
    near = "M -40 2000 L -40 1300 C 200 1270, 500 1290, 760 1265 C 900 1255, 1020 1270, 1120 1280 L 1120 2000 Z"
    s += f'<path d="{near}" fill="url(#near)"/>' + _strata(65, -40, 1100, 1300, 1900, 30, "#4a3020", 0.35, 4) + _cracks(66, 0, 1080, 1320, 1850, 12, "#3a2216", 0.4)
    s += grass_tufts(67, 1300, 1900, 26, "#6a6a3a", "#a09a5a")
    return svg_render(s)

def gorge_down():
    """looking down from the ridge into the pass: sunlit far wall, deep shadowed floor (column walks at y 1050-1250)"""
    s = ("<defs>" + FILTERS + lg("fw", [(0, "#d8a26a", 1), (1, "#8a5a36", 1)]) + lg("fl", [(0, "#8a6a4c", 1), (1, "#5a4232", 1)]) +
         lg("nw", [(0, "#5a3a24", 1), (1, "#2a1a10", 1)]) + "</defs>")
    s += f'<rect width="{W}" height="{H}" fill="#6a4a32"/>'
    s += '<path d="M -40 -40 L 1120 -40 L 1120 760 C 800 820, 300 840, -40 860 Z" fill="url(#fw)"/>'
    s += _strata(71, -40, 1100, 0, 820, 40, "#6a4428", 0.35, 5, slope=0.08) + _cracks(72, 0, 1080, 0, 760, 18, "#4a2c18", 0.45)
    s += '<path d="M -40 860 C 300 840, 800 820, 1120 760 L 1120 1350 C 800 1320, 300 1330, -40 1360 Z" fill="url(#fl)"/>'
    s += '<path d="M -40 1080 C 300 1060, 800 1050, 1120 1030" stroke="#a88a66" stroke-width="70" fill="none" opacity="0.45"/>'
    r = random.Random(73)
    for _ in range(60):
        x = r.uniform(-20, 1100); y = r.uniform(880, 1320)
        s += f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{r.uniform(5,14):.0f}" ry="{r.uniform(3,7):.0f}" fill="#4a3424" opacity="0.6"/>'
    s += '<path d="M -40 1360 C 300 1330, 800 1320, 1120 1350 L 1120 2000 L -40 2000 Z" fill="url(#nw)"/>'
    s += _strata(74, -40, 1100, 1380, 1900, 26, "#000", 0.3, 5)
    s += f'<rect x="0" y="840" width="{W}" height="520" fill="#000" opacity="0.18"/>'
    return svg_render(s)

def village_square():
    """816: the square of a mountain village, overcast autumn day; a muddy patch in front (people stand at y 1400-1650)"""
    s = ("<defs>" + FILTERS + lg("sky", [(0, "#5a6e90", 1), (0.4, "#a6b4c4", 1), (0.6, "#e0d8c8", 1)]) +
         lg("gr", [(0, "#a48660", 1), (1, "#6e5438", 1)]) + "</defs>")
    s += f'<rect width="{W}" height="{H}" fill="url(#sky)"/>' + clouds(W, 81, [280, 380, 480, 580], "#eef0f4", "#ffffff", 0.7)
    s += f'<path d="{ridge(W, 820, 260, 82, rough=0.55)}" fill="#8a92ac"/>'
    s += f'<path d="{hill(W, 960, 140, 83)}" fill="#7a8a5e"/><rect x="0" y="860" width="{W}" height="200" fill="#e8e0d0" opacity="0.3" filter="url(#b20)"/>'
    for x in (90, 130, 960, 1000):
        s += poplar(x, 1080, 230, "#7a7a3a", "#5a5a2a")
    r = random.Random(84)
    for i in range(7):   # back row of houses
        x = -20 + i * 160 + r.uniform(-20, 20); y = 1130 + r.uniform(-10, 10)
        s += flat_house(int(x), int(y), int(r.uniform(120, 160)), int(r.uniform(90, 130)), "#b4906a", "#8a6a4a", "#6a4a34")
    s += flat_house(-60, 1290, 300, 300, "#bc9a74", "#94704e", "#6e4e36", window=True) + flat_house(820, 1300, 320, 310, "#b8946e", "#8e6c4c", "#6a4a32")
    s += '<rect x="250" y="1080" width="12" height="230" fill="#4a3424"/><path d="M 262 1088 l 70 8 l -6 40 l 6 40 l -70 -8 Z" fill="#5a4a3a" opacity="0.0"/>'
    s += f'<path d="M -40 1260 C 300 1240, 800 1240, 1120 1265 L 1120 2000 L -40 2000 Z" fill="url(#gr)"/>'
    s += '<ellipse cx="330" cy="1690" rx="300" ry="70" fill="#4a3624" opacity="0.85"/><ellipse cx="310" cy="1680" rx="220" ry="42" fill="#7a8494" opacity="0.35"/>'
    s += '<path d="M 600 1300 C 640 1500, 700 1700, 720 1920 M 680 1300 C 740 1500, 820 1700, 860 1920" stroke="#5a4430" stroke-width="10" fill="none" opacity="0.35"/>'
    for _ in range(70):
        x = r.uniform(-20, 1100); y = r.uniform(1280, 1900); sc = 0.4 + (y - 1280) / 620
        s += f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{r.uniform(6,16)*sc:.0f}" ry="{r.uniform(4,8)*sc:.0f}" fill="#5a4430" opacity="0.6"/>'
    s += grass_tufts(85, 1270, 1900, 24, "#6a6a3a", "#9a9a5a")
    return svg_render(s)

def snow_pass():
    """819: deep snow in a high pass on a grey day (riders at feet y 1350-1450, legs hidden by snow_fg)"""
    s = ("<defs>" + FILTERS + lg("sky", [(0, "#6a7488", 1), (0.5, "#b0b8c6", 1), (0.7, "#dde2ea", 1)]) + lg("sn", [(0, "#eef2f8", 1), (1, "#c4ccdc", 1)]) + "</defs>")
    s += f'<rect width="{W}" height="{H}" fill="url(#sky)"/>'
    s += f'<path d="{ridge(W, 900, 380, 91, rough=0.6)}" fill="#d8dee8"/><path d="{ridge(W, 900, 380, 91, rough=0.6)}" fill="#7a8498" opacity="0.35" transform="translate(30,0)"/>'
    s += f'<path d="{ridge(W, 1050, 220, 92, rough=0.5)}" fill="#e6eaf2"/>'
    r = random.Random(93)
    for _ in range(26):
        x = r.uniform(0, 1080); y = r.uniform(820, 1100)
        s += f'<path d="M {x:.0f} {y:.0f} l {r.uniform(-30,30):.0f} {r.uniform(40,120):.0f}" stroke="#8a94a8" stroke-width="5" opacity="0.4"/>'
    s += f'<rect x="0" y="900" width="{W}" height="300" fill="#ffffff" opacity="0.35" filter="url(#b40)"/>'
    s += '<path d="M -40 1250 C 300 1210, 800 1220, 1120 1240 L 1120 2000 L -40 2000 Z" fill="url(#sn)"/>'
    s += '<path d="M -40 1380 C 300 1350, 700 1360, 1120 1390" stroke="#b4bccc" stroke-width="40" fill="none" opacity="0.5"/>'
    return svg_render(s)

def snow_fg():
    """snow drifts in front of the riders (fg layer)"""
    s = "<defs>" + FILTERS + lg("sn", [(0, "#f6f8fc", 1), (1, "#d4dae6", 1)]) + "</defs>"
    s += '<path d="M -40 1440 C 120 1400, 260 1430, 420 1405 C 600 1380, 760 1420, 920 1395 C 1000 1385, 1060 1400, 1120 1410 L 1120 2000 L -40 2000 Z" fill="url(#sn)"/>'
    s += '<path d="M -40 1440 C 120 1400, 260 1430, 420 1405 C 600 1380, 760 1420, 920 1395 C 1000 1385, 1060 1400, 1120 1410" stroke="#ffffff" stroke-width="8" fill="none"/>'
    s += '<path d="M -40 1620 C 200 1580, 500 1610, 800 1590 C 950 1580, 1050 1600, 1120 1610 L 1120 2000 L -40 2000 Z" fill="#e2e8f2"/>'
    return svg_render(s)

def camp_rocks():
    """Babak's camp in the mountains, clear day: tents, red banners, flat earth to draw on (people stand at y 1450-1650)"""
    s = ("<defs>" + FILTERS + lg("sky", [(0, "#4a7ab8", 1), (0.4, "#a4c4dc", 1), (0.55, "#f0dcb8", 1)]) + lg("gr", [(0, "#b08c62", 1), (1, "#76583a", 1)]) + "</defs>")
    s += f'<rect width="{W}" height="{H}" fill="url(#sky)"/>' + clouds(W, 101, [300, 420, 520], "#ffffff", "#fff8e8", 0.6)
    s += f'<path d="{ridge(W, 900, 300, 102, rough=0.55)}" fill="#8e98b8"/>'
    s += f'<path d="{ridge(W, 1080, 200, 103, rough=0.5)}" fill="#9a7a5a"/>' + _strata(104, -40, 1100, 950, 1150, 16, "#6a4a30", 0.35, 3)
    for x, y, w_, h_, col in [(70, 1250, 230, 170, "#8a2a1e"), (760, 1240, 260, 190, "#7a2418"), (430, 1200, 180, 120, "#9a3424")]:
        s += (f'<path d="M {x} {y} L {x + w_/2} {y - h_} L {x + w_} {y} Z" fill="{col}" stroke="#2a1008" stroke-width="4"/>'
              f'<path d="M {x + w_/2} {y - h_} L {x + w_*0.42} {y} L {x + w_*0.58} {y} Z" fill="#2a1008" opacity="0.6"/>'
              f'<path d="M {x + w_/2} {y - h_} L {x + w_} {y} L {x + w_*0.75} {y} Z" fill="#000" opacity="0.18"/>')
    for x in (330, 690):
        s += f'<rect x="{x}" y="900" width="8" height="330" fill="#3a2414"/><path d="M {x+8} 906 l 100 12 l -8 60 l 8 60 l -100 -12 Z" fill="#b5161b" stroke="#2a0a0a" stroke-width="2"/>'
    s += f'<path d="M -40 1250 C 300 1230, 800 1235, 1120 1250 L 1120 2000 L -40 2000 Z" fill="url(#gr)"/>'
    r = random.Random(105)
    for _ in range(60):
        x = r.uniform(-20, 1100); y = r.uniform(1260, 1900); sc = 0.4 + (y - 1260) / 640
        s += f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{r.uniform(6,16)*sc:.0f}" ry="{r.uniform(4,8)*sc:.0f}" fill="#5a4430" opacity="0.55"/>'
    s += grass_tufts(106, 1260, 1900, 20, "#7a6a3a", "#a89a5a")
    return svg_render(s)

def map_dirt():
    """top-down packed earth with pebbles (the map is drawn on it in the scene)"""
    s = "<defs>" + FILTERS + rg("lt", 540, 800, 1200, [(0, "#c8a478", 1), (1, "#8a6a48", 1)]) + "</defs>"
    s += f'<rect width="{W}" height="{H}" fill="url(#lt)"/>'
    r = random.Random(111)
    for _ in range(260):
        x = r.uniform(0, 1080); y = r.uniform(0, 1920); rr = r.uniform(3, 14)
        s += f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{rr:.1f}" ry="{rr*0.7:.1f}" fill="{r.choice(["#6a5038", "#9a7a56", "#d8bc94", "#5a4230"])}" opacity="{r.uniform(0.4, 0.8):.2f}"/>'
    for _ in range(40):
        x = r.uniform(0, 1080); y = r.uniform(0, 1920)
        s += f'<path d="M {x:.0f} {y:.0f} q {r.uniform(-40,40):.0f} {r.uniform(-10,10):.0f} {r.uniform(-80,80):.0f} {r.uniform(-20,20):.0f}" stroke="#7a5c3e" stroke-width="2" fill="none" opacity="0.4"/>'
    return svg_render(s)

def ledge_fg(top=1060, seed=121):
    """the rim of the pass seen from the air above the gorge: a rocky ledge across the frame (fg layer)"""
    r = random.Random(seed)
    s = "<defs>" + FILTERS + lg("lf", [(0, "#8a6040", 1), (0.25, "#5a3c26", 1), (1, "#2a1a10", 1)]) + "</defs>"
    pts = [(-60, top + 40)]
    x = -60
    while x < 1140:
        x += r.uniform(50, 110); pts.append((x, top + r.uniform(-30, 40)))
    d = "M -60 2000 L " + " L ".join(f"{a:.0f} {b:.0f}" for a, b in pts) + " L 1140 2000 Z"
    s += f'<path d="{d}" fill="url(#lf)" stroke="#1b0f0a" stroke-width="4" stroke-linejoin="round"/>'
    s += '<path d="M ' + " L ".join(f"{a:.0f} {b + 8:.0f}" for a, b in pts) + '" stroke="#d8a878" stroke-width="7" fill="none" opacity="0.6" stroke-linejoin="round"/>'
    s += _strata(seed + 1, -60, 1100, top + 80, 1900, 34, "#000", 0.3, 6) + _cracks(seed + 2, 0, 1080, top + 60, 1800, 14, "#140a04", 0.5)
    return svg_render(s)

# ------------------------------------------------------------------ PART 4 (Babak, episode 2): the stream, the feast, the tent, Baghdad, the fires on the plain
def stream_bg():
    """a mountain stream at the floor of the pass (water y 1240-1560), stones, dust in the air"""
    s = ("<defs>" + FILTERS + lg("sky", [(0, "#8a8070", 1), (0.5, "#c8b090", 1)]) + lg("wt", [(0, "#4a6a7a", 1), (1, "#2a4a5a", 1)]) +
         lg("bank", [(0, "#9a7650", 1), (1, "#6a4c32", 1)]) + "</defs>")
    s += f'<rect width="{W}" height="{H}" fill="url(#sky)"/>'
    back = "M -40 1300 L -40 520 L 140 470 L 260 540 L 420 440 L 560 520 L 700 430 L 860 500 L 1120 450 L 1120 1300 Z"
    s += f'<path d="{back}" fill="#8a6446"/>' + _strata(131, -40, 1100, 500, 1150, 40, "#5a3c26", 0.35, 4) + _cracks(132, 0, 1080, 480, 1100, 14, "#4a2c18", 0.4)
    s += f'<rect x="0" y="600" width="{W}" height="700" fill="#d8c0a0" opacity="0.35" filter="url(#b40)"/>'
    s += '<path d="M -40 1180 C 300 1150, 700 1160, 1120 1170 L 1120 1260 L -40 1260 Z" fill="url(#bank)"/>'
    s += '<path d="M -40 1240 C 300 1225, 700 1235, 1120 1230 L 1120 1580 C 700 1600, 300 1590, -40 1600 Z" fill="url(#wt)"/>'
    s += '<path d="M -40 1560 C 300 1590, 700 1600, 1120 1570 L 1120 2000 L -40 2000 Z" fill="url(#bank)"/>'
    for i, (x, y, r) in enumerate([(120, 1250, 40), (880, 1245, 52), (300, 1575, 70), (760, 1590, 90), (1010, 1600, 60), (60, 1620, 50)]):
        s += boulder(x, y, r, 140 + i, "#7a6a5a", "#3a3028", "#b0a088")
    s += grass_tufts(133, 1600, 1900, 20, "#6a6a3a", "#9a9a5a")
    return svg_render(s)

def feast_night():
    """Bazz at night: the fortress against the stars, torches on the walls, ground lit by a big fire (y 1250+)"""
    s = ("<defs>" + FILTERS + lg("sky", [(0, "#060818", 1), (0.6, "#161c3a", 1), (1, "#24223a", 1)]) +
         rg("fire", 540, 1300, 700, [(0, "#ff9a40", 0.45), (0.5, "#a04a20", 0.15), (1, "#000000", 0)]) + "</defs>")
    s += f'<rect width="{W}" height="{H}" fill="url(#sky)"/>' + stars(41, 260, 900)
    s += f'<path d="{ridge(W, 1000, 220, 42)}" fill="#12162a"/>'
    s += ('<path d="M 60 1260 L 60 760 L 40 760 L 40 720 L 70 720 L 70 740 L 100 740 L 100 720 L 130 720 L 130 740 L 160 740 L 160 720 L 190 720 L 190 760 L 170 760 L 170 1260 Z" fill="#0c0a14"/>'
          '<path d="M 880 1260 L 880 700 L 860 700 L 860 660 L 890 660 L 890 680 L 920 680 L 920 660 L 950 660 L 950 680 L 980 680 L 980 660 L 1010 660 L 1010 700 L 990 700 L 990 1260 Z" fill="#0c0a14"/>'
          '<rect x="160" y="900" width="730" height="360" fill="#100e1a"/>' + "".join(f'<rect x="{160 + i * 46}" y="878" width="26" height="26" fill="#100e1a"/>' for i in range(16)))
    for x, y in [(115, 800), (935, 740), (330, 930), (720, 930)]:
        s += f'<circle cx="{x}" cy="{y}" r="60" fill="#ffb060" opacity="0.35" filter="url(#b20)"/><circle cx="{x}" cy="{y}" r="9" fill="#ffe0a0"/>'
    s += '<rect x="0" y="1240" width="1080" height="680" fill="#1e1610"/>'
    s += f'<rect width="{W}" height="{H}" fill="url(#fire)"/>'
    return svg_render(s)

def tent_interior():
    """a dim military tent at night: canvas walls, a pole, a lamp on a stand (x 860), a low bed (y 1150-1350)"""
    s = ("<defs>" + FILTERS + lg("cv", [(0, "#4a3a2a", 1), (1, "#2a2018", 1)]) +
         rg("lamp", 860, 900, 900, [(0, "#ffb060", 0.5), (0.5, "#8a4a20", 0.15), (1, "#000", 0)]) + "</defs>")
    s += f'<rect width="{W}" height="{H}" fill="url(#cv)"/>'
    for k in range(9):
        x = -60 + k * 150
        s += f'<path d="M {x} 0 C {x + 20} 600, {x - 10} 1100, {x + 10} 1300" stroke="#1a140e" stroke-width="5" fill="none" opacity="0.5"/>'
        s += f'<path d="M {x + 60} 0 C {x + 80} 600, {x + 50} 1100, {x + 70} 1300" stroke="#6a5440" stroke-width="3" fill="none" opacity="0.25"/>'
    s += '<path d="M 0 0 L 1080 0 L 1080 160 C 700 260, 380 260, 0 160 Z" fill="#1e1610" opacity="0.8"/>'
    s += '<rect x="520" y="0" width="34" height="1320" fill="#3a2414" stroke="#140a04" stroke-width="3"/>'
    s += '<rect x="0" y="1300" width="1080" height="620" fill="#2a1e14"/><path d="M 0 1300 L 1080 1300" stroke="#4a3624" stroke-width="6"/>'
    s += ('<rect x="60" y="1360" width="960" height="40" fill="#5a2a1e" opacity="0.6"/>'
          '<rect x="140" y="1180" width="700" height="140" rx="16" fill="#4a2e1a" stroke="#140a04" stroke-width="5"/>')
    s += ('<rect x="852" y="760" width="16" height="560" fill="#3a2a1a"/><path d="M 820 1320 L 900 1320 L 880 1290 L 840 1290 Z" fill="#3a2a1a"/>'
          '<path d="M 830 760 L 890 760 L 870 735 L 850 735 Z" fill="#8a6a3a" stroke="#1b0f0a" stroke-width="3"/>')
    s += f'<rect width="{W}" height="{H}" fill="url(#lamp)"/>'
    return svg_render(s)

def gold_hall():
    """the caliph's golden hall in Baghdad: arches, lamps, carpet, a raised throne (seat at x 540, y 1150)"""
    s = ("<defs>" + FILTERS + lg("wall", [(0, "#3a2414", 1), (0.6, "#6a4420", 1), (1, "#4a2e18", 1)]) +
         rg("glow", 540, 900, 900, [(0, "#ffd890", 0.45), (0.6, "#c88a3a", 0.12), (1, "#000", 0)]) + lg("cp", [(0, "#7a1a14", 1), (1, "#4a0e0a", 1)]) + "</defs>")
    s += f'<rect width="{W}" height="{H}" fill="url(#wall)"/>'
    for x in (-60, 260, 580, 900):
        s += (f'<path d="M {x + 20} 1280 L {x + 20} 520 Q {x + 120} 330, {x + 220} 520 L {x + 220} 1280 Z" fill="#2a180c" stroke="#d8a64a" stroke-width="10"/>'
              f'<path d="M {x + 40} 1280 L {x + 40} 540 Q {x + 120} 380, {x + 200} 540 L {x + 200} 1280" fill="none" stroke="#8a6020" stroke-width="4"/>')
        s += "".join(f'<path d="M {x + 120} {600 + k * 120} l 20 30 l -20 30 l -20 -30 Z" fill="#d8a64a" opacity="0.5"/>' for k in range(5))
    for x in (230, 550, 870):
        s += f'<rect x="{x - 26}" y="200" width="52" height="1080" fill="#5a3a1a" stroke="#d8a64a" stroke-width="5"/><rect x="{x - 40}" y="180" width="80" height="34" fill="#d8a64a"/>'
    for x, y in [(160, 420), (920, 420), (540, 300)]:
        s += f'<path d="M {x} 0 L {x} {y - 40}" stroke="#8a6020" stroke-width="3"/><circle cx="{x}" cy="{y}" r="70" fill="#ffd080" opacity="0.35" filter="url(#b20)"/><path d="M {x - 26} {y - 30} L {x + 26} {y - 30} L {x + 18} {y + 20} L {x - 18} {y + 20} Z" fill="#d8a64a" stroke="#3a2010" stroke-width="3"/>'
    s += '<rect x="0" y="1270" width="1080" height="650" fill="#3a2010"/>'
    s += '<path d="M 300 1280 L 780 1280 L 1000 1920 L 80 1920 Z" fill="url(#cp)"/><path d="M 330 1300 L 750 1300 L 950 1900 L 130 1900 Z" fill="none" stroke="#d8a64a" stroke-width="8"/>'
    s += ('<rect x="330" y="1150" width="420" height="130" fill="#6a4420" stroke="#d8a64a" stroke-width="6"/>'
          '<rect x="280" y="1240" width="520" height="60" fill="#7a5028" stroke="#d8a64a" stroke-width="6"/>')
    s += f'<rect width="{W}" height="{H}" fill="url(#glow)"/>'
    return svg_render(s)

def night_plain():
    """seen from the walls of Bazz at night: the plain far below, a line of enemy campfires to the horizon"""
    s = ("<defs>" + FILTERS + lg("sky", [(0, "#04060f", 1), (0.5, "#121a36", 1), (0.62, "#262a48", 1)]) + lg("pl", [(0, "#14182a", 1), (1, "#080a12", 1)]) + "</defs>")
    s += f'<rect width="{W}" height="{H}" fill="url(#sky)"/>' + stars(51, 300, 1000)
    s += '<circle cx="820" cy="420" r="46" fill="#f4f0e0"/><circle cx="820" cy="420" r="140" fill="#c8d0ff" opacity="0.12" filter="url(#b40)"/>'
    s += f'<path d="{ridge(W, 1100, 120, 52)}" fill="#1a1e36"/>'
    s += '<rect x="0" y="1080" width="1080" height="840" fill="url(#pl)"/>'
    r = random.Random(53)
    for k in range(70):          # the campfires: a band from near-left to the far horizon
        u = k / 69
        x = lerp_(-40, 1100, u) + r.uniform(-30, 30); y = lerp_(1700, 1110, u ** 0.6) + r.uniform(-14, 14)
        sz = lerp_(10, 2.2, u ** 0.5)
        s += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{sz * 5:.1f}" fill="#ff9a40" opacity="0.18" filter="url(#b6)"/><circle cx="{x:.0f}" cy="{y:.0f}" r="{sz:.1f}" fill="#ffd080"/>'
    s += '<rect x="0" y="1080" width="1080" height="60" fill="#3a3a5a" opacity="0.3" filter="url(#b20)"/>'
    return svg_render(s)

def lerp_(a, b, u):
    return a + (b - a) * u

def night_sky_wall():
    """night sky with the moon, for the wall shots (wall_fg darkened goes in front)"""
    s = "<defs>" + FILTERS + lg("sky", [(0, "#05070f", 1), (0.55, "#141c3a", 1), (0.75, "#2a2c4a", 1)]) + "</defs>"
    s += f'<rect width="{W}" height="{H}" fill="url(#sky)"/>' + stars(61, 280, 1100)
    s += '<circle cx="250" cy="520" r="54" fill="#f4f0e0"/><circle cx="250" cy="520" r="170" fill="#c8d0ff" opacity="0.12" filter="url(#b40)"/>'
    s += f'<path d="{ridge(W, 1150, 140, 62)}" fill="#161a30"/>'
    r = random.Random(63)
    for k in range(40):
        x = r.uniform(0, 1080); y = r.uniform(1120, 1240)
        s += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="2.2" fill="#ffd080"/><circle cx="{x:.0f}" cy="{y:.0f}" r="10" fill="#ff9a40" opacity="0.2" filter="url(#b6)"/>'
    return svg_render(s)
