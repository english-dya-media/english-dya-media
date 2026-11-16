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

# ------------------------------------------------------------------ PART 5 (Babak, episode 3): Afshin's tent, the forts, the camp at Barzand, the watch fires,
# the war room at Bazz, the silver road, the woods at night, the ravine
def pine(x, y, h, col="#2e4a32", dark="#1e3424", trunk="#3a2618"):
    """a layered pine, base of the trunk at (x, y)"""
    out = f'<rect x="{x - h * 0.03:.0f}" y="{y - h * 0.18:.0f}" width="{h * 0.06:.0f}" height="{h * 0.18:.0f}" fill="{trunk}"/>'
    for k in range(4):
        top = y - h + k * h * 0.2; bot = y - h * 0.12 - (3 - k) * h * 0.13; w = h * (0.16 + 0.07 * k)
        out += (f'<path d="M {x:.0f} {top:.0f} L {x + w:.0f} {bot:.0f} C {x + w * 0.4:.0f} {bot - h * 0.03:.0f}, {x - w * 0.4:.0f} {bot - h * 0.03:.0f}, {x - w:.0f} {bot:.0f} Z" fill="{col}"/>'
                f'<path d="M {x:.0f} {top:.0f} L {x - w:.0f} {bot:.0f} C {x - w * 0.5:.0f} {bot - h * 0.02:.0f}, {x - w * 0.2:.0f} {bot - h * 0.03:.0f}, {x:.0f} {bot - h * 0.04:.0f} Z" fill="{dark}" opacity="0.8"/>')
    return out

def oak(x, y, h, seed=0, col="#3e5a2e", dark="#2a4020", hi="#5a7a3a", trunk="#3a2618"):
    """a round leafy tree, base of the trunk at (x, y)"""
    r = random.Random(seed)
    out = f'<path d="M {x - h * 0.05:.0f} {y:.0f} L {x - h * 0.03:.0f} {y - h * 0.5:.0f} L {x + h * 0.03:.0f} {y - h * 0.5:.0f} L {x + h * 0.05:.0f} {y:.0f} Z" fill="{trunk}"/>'
    for k in range(9):
        cx = x + r.uniform(-0.28, 0.28) * h; cy = y - h * 0.62 + r.uniform(-0.25, 0.18) * h; rr = h * r.uniform(0.16, 0.24)
        out += f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{rr:.0f}" fill="{col}"/>'
    for k in range(4):
        cx = x + r.uniform(-0.25, 0.25) * h; cy = y - h * 0.52 + r.uniform(-0.1, 0.12) * h; rr = h * r.uniform(0.12, 0.18)
        out += f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{rr:.0f}" fill="{dark}" opacity="0.7"/>'
    for k in range(3):
        cx = x + r.uniform(-0.1, 0.28) * h; cy = y - h * 0.78 + r.uniform(-0.08, 0.08) * h; rr = h * r.uniform(0.08, 0.12)
        out += f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{rr:.0f}" fill="{hi}" opacity="0.6"/>'
    return out

def oil_lamp(x, y, chain=300):
    """a hanging brass oil lamp (flame at about (x, y - 14)) with its glow"""
    return (f'<path d="M {x} {y - chain} L {x} {y - 30}" stroke="#6a5030" stroke-width="3"/>'
            f'<circle cx="{x}" cy="{y - 10}" r="110" fill="#ffb060" opacity="0.30" filter="url(#b20)"/>'
            f'<path d="M {x - 34} {y - 4} C {x - 30} {y + 22}, {x + 30} {y + 22}, {x + 34} {y - 4} Z" fill="#b9832f" stroke="#2a1608" stroke-width="3"/>'
            f'<path d="M {x - 34} {y - 4} L {x + 34} {y - 4} L {x + 22} {y - 26} L {x - 22} {y - 26} Z" fill="#8a5a22" stroke="#2a1608" stroke-width="3"/>'
            f'<path d="M {x} {y - 40} C {x - 8} {y - 30}, {x - 6} {y - 24}, {x} {y - 22} C {x + 6} {y - 24}, {x + 8} {y - 30}, {x} {y - 40} Z" fill="#fff0b0"/>')

def command_tent():
    """Afshin's command tent at night: canvas, two hanging oil lamps (x 250 and 840, flame y ≈ 610), spears on a rack (left),
    a black banner (right), a carpet; people stand at feet y 1380-1650"""
    s = ("<defs>" + FILTERS + lg("cv", [(0, "#3a2e22", 1), (0.6, "#4a3a2a", 1), (1, "#2a2018", 1)]) +
         rg("l1", 250, 640, 700, [(0, "#ffb060", 0.42), (0.5, "#8a4a20", 0.12), (1, "#000", 0)]) +
         rg("l2", 840, 620, 700, [(0, "#ffb060", 0.42), (0.5, "#8a4a20", 0.12), (1, "#000", 0)]) +
         lg("cp", [(0, "#4a1410", 1), (1, "#2a0a08", 1)]) + "</defs>")
    s += f'<rect width="{W}" height="{H}" fill="url(#cv)"/>'
    for k in range(10):
        x = -40 + k * 125
        s += f'<path d="M {x} 0 C {x + 16} 500, {x - 8} 1000, {x + 8} 1330" stroke="#140e08" stroke-width="5" fill="none" opacity="0.5"/>'
        s += f'<path d="M {x + 50} 0 C {x + 66} 500, {x + 42} 1000, {x + 58} 1330" stroke="#7a6248" stroke-width="3" fill="none" opacity="0.2"/>'
    s += '<path d="M 0 0 L 1080 0 L 1080 190 C 700 290, 380 290, 0 190 Z" fill="#140e08" opacity="0.8"/>'
    s += '<path d="M 0 250 C 380 330, 700 330, 1080 250" stroke="#8a6a3a" stroke-width="6" fill="none" opacity="0.5"/>'
    # spear rack (left)
    for k in range(4):
        x = 70 + k * 34
        s += f'<path d="M {x} 1330 L {x + 14} 640" stroke="#3a2414" stroke-width="9"/><path d="M {x + 14} 600 l 10 44 l -20 0 Z" fill="#a8aebb" stroke="#1b0f0a" stroke-width="2"/>'
    s += '<rect x="40" y="1080" width="170" height="16" fill="#3a2414"/><rect x="40" y="1300" width="170" height="20" fill="#3a2414"/>'
    # black banner on a stand (right)
    s += ('<rect x="960" y="520" width="12" height="810" fill="#2a1a10"/><circle cx="966" cy="512" r="12" fill="#c9a24a" stroke="#1b0f0a" stroke-width="2"/>'
          '<path d="M 972 540 L 1080 552 L 1080 820 L 972 800 Z" fill="#101014" stroke="#000" stroke-width="2"/>'
          '<path d="M 972 570 L 1080 580" stroke="#c9a24a" stroke-width="5" opacity="0.7"/>')
    # a low chest with a scroll (back right)
    s += ('<rect x="700" y="1210" width="200" height="110" rx="8" fill="#4a2a14" stroke="#140a04" stroke-width="4"/>'
          '<path d="M 700 1250 L 900 1250" stroke="#c9a24a" stroke-width="6"/>'
          '<rect x="740" y="1186" width="110" height="26" rx="12" fill="#e2d2a8" stroke="#3a2a14" stroke-width="3"/>')
    s += '<rect x="0" y="1320" width="1080" height="600" fill="#24180e"/><path d="M 0 1320 L 1080 1320" stroke="#3a2a1a" stroke-width="6"/>'
    s += ('<path d="M 160 1400 L 920 1400 L 1060 1900 L 20 1900 Z" fill="url(#cp)" stroke="#140404" stroke-width="4"/>'
          '<path d="M 200 1430 L 880 1430 L 1000 1860 L 80 1860 Z" fill="none" stroke="#b9832f" stroke-width="8" opacity="0.8"/>'
          '<path d="M 330 1540 L 750 1540 L 800 1740 L 280 1740 Z" fill="none" stroke="#b9832f" stroke-width="5" opacity="0.5"/>')
    s += oil_lamp(250, 640, 640) + oil_lamp(840, 620, 620)
    s += f'<rect width="{W}" height="{H}" fill="url(#l1)"/><rect width="{W}" height="{H}" fill="url(#l2)"/>'
    return svg_render(s)

def fort_road():
    """835: a ruined stone fort on the road between Zanjan and Ardabil, clear morning; the wall's broken top (x 470-820, y ≈ 1000)
    is rebuilt in the scene; workers walk at feet y 1380-1600"""
    s = ("<defs>" + FILTERS + lg("sky", [(0, "#3f72b4", 1), (0.38, "#9cc2de", 1), (0.55, "#f0dcb6", 1)]) +
         lg("gr", [(0, "#b08c60", 1), (1, "#76583a", 1)]) + lg("st", [(0, "#a88a68", 1), (1, "#7a604a", 1)]) + "</defs>")
    s += f'<rect width="{W}" height="{H}" fill="url(#sky)"/>' + clouds(W, 141, [300, 410, 520], "#ffffff", "#fff8e8", 0.6)
    s += f'<path d="{ridge(W, 880, 300, 142, rough=0.55)}" fill="#8e98b8"/><path d="{ridge(W, 1000, 170, 143, rough=0.45)}" fill="#a0866a"/>'
    s += f'<rect x="0" y="820" width="{W}" height="260" fill="#f0e0c0" opacity="0.3" filter="url(#b40)"/>'
    s += f'<path d="M -40 1180 C 300 1150, 800 1150, 1120 1175 L 1120 2000 L -40 2000 Z" fill="url(#gr)"/>'
    # the road
    s += '<path d="M 1120 1240 C 800 1260, 500 1300, 380 1400 C 260 1500, 220 1700, 200 1920 L 520 1920 C 520 1700, 560 1520, 660 1430 C 780 1330, 960 1290, 1120 1280 Z" fill="#c8a87a" opacity="0.7"/>'
    # the fort: a broken tower and a wall
    s += ('<path d="M 120 1250 L 120 760 L 150 740 L 180 760 L 210 730 L 250 770 L 290 745 L 330 780 L 330 1250 Z" fill="url(#st)" stroke="#2a1a10" stroke-width="4"/>'
          '<path d="M 120 760 L 330 780 L 330 1250 L 290 1250 L 290 800 Z" fill="#5a4432" opacity="0.4"/>'
          '<rect x="200" y="880" width="40" height="70" fill="#2a1a10"/>'
          '<path d="M 330 1250 L 330 900 L 470 900 L 470 1000 L 520 1010 L 560 1060 L 620 1040 L 680 1090 L 740 1050 L 820 1080 L 820 980 L 960 980 L 960 1250 Z" '
          'fill="url(#st)" stroke="#2a1a10" stroke-width="4"/>')
    r = random.Random(144)
    for k in range(80):                       # stone courses
        x = r.uniform(130, 950); y = r.uniform(780, 1240)
        if 470 < x < 820 and y < 1090:
            continue
        s += f'<rect x="{x:.0f}" y="{y:.0f}" width="{r.uniform(40, 80):.0f}" height="{r.uniform(22, 34):.0f}" rx="4" fill="#5a4432" opacity="0.25"/>'
    s += "".join(f'<rect x="{x}" y="870" width="26" height="30" fill="#9a7c5c" stroke="#2a1a10" stroke-width="3"/>' for x in (340, 390, 440, 830, 880, 930))
    for i, (x, y, rr) in enumerate([(560, 1280, 34), (610, 1300, 26), (520, 1310, 30), (900, 1300, 40), (950, 1320, 28), (380, 1300, 30)]):
        s += boulder(x, y, rr, 150 + i, "#9a7c5c", "#5a4432", "#c8aa86")
    s += ('<path d="M 840 1250 L 840 900 M 900 1250 L 900 900 M 830 960 L 910 960 M 830 1060 L 910 1060 M 830 1160 L 910 1160" stroke="#5a3a1c" stroke-width="9"/>')
    s += grass_tufts(145, 1200, 1900, 26, "#7a6a3a", "#a89a5a")
    return svg_render(s)

def army_camp():
    """835: Afshin's great camp at Barzand: rows of dark tents to the mountains, black banners, smoke (people at feet y 1400-1700)"""
    s = ("<defs>" + FILTERS + lg("sky", [(0, "#5a7aa8", 1), (0.4, "#b4c4d4", 1), (0.56, "#ecdcc0", 1)]) + lg("gr", [(0, "#a8885e", 1), (1, "#6e5236", 1)]) + "</defs>")
    s += f'<rect width="{W}" height="{H}" fill="url(#sky)"/>' + clouds(W, 151, [320, 430], "#ffffff", "#fff4e4", 0.5)
    s += f'<path d="{ridge(W, 900, 320, 152, rough=0.55)}" fill="#9aa2bc"/><path d="{ridge(W, 980, 160, 153, rough=0.4)}" fill="#8a8a8e"/>'
    s += f'<path d="M -40 1000 C 300 985, 800 985, 1120 995 L 1120 2000 L -40 2000 Z" fill="url(#gr)"/>'
    s += f'<rect x="0" y="930" width="{W}" height="180" fill="#e8dcc8" opacity="0.4" filter="url(#b20)"/>'
    r = random.Random(154)
    rows = [(1015, 0.22, 26), (1050, 0.3, 20), (1100, 0.42, 14), (1170, 0.6, 10), (1270, 0.85, 7)]
    for y, sc, n in rows:
        xs = sorted(r.uniform(-60, 1140) for _ in range(n))
        for x in xs:
            w = 180 * sc * r.uniform(0.85, 1.15); h = 130 * sc * r.uniform(0.9, 1.1)
            col = r.choice(["#2a2a30", "#34343a", "#3e3a36", "#4a3e30", "#26262c"])
            s += (f'<path d="M {x - w / 2:.0f} {y:.0f} L {x:.0f} {y - h:.0f} L {x + w / 2:.0f} {y:.0f} Z" fill="{col}" stroke="#141418" stroke-width="{max(1.5, 4 * sc):.1f}"/>'
                  f'<path d="M {x:.0f} {y - h:.0f} L {x - w * 0.08:.0f} {y:.0f} L {x + w * 0.08:.0f} {y:.0f} Z" fill="#0a0a0c" opacity="0.7"/>'
                  f'<path d="M {x:.0f} {y - h:.0f} L {x + w / 2:.0f} {y:.0f} L {x + w * 0.2:.0f} {y:.0f} Z" fill="#000" opacity="0.2"/>')
            if r.random() < 0.18:
                s += (f'<rect x="{x - 2 * sc:.0f}" y="{y - h - 160 * sc:.0f}" width="{max(2, 6 * sc):.0f}" height="{160 * sc:.0f}" fill="#2a1a10"/>'
                      f'<path d="M {x + 3 * sc:.0f} {y - h - 156 * sc:.0f} l {70 * sc:.0f} {8 * sc:.0f} l {-6 * sc:.0f} {36 * sc:.0f} l {6 * sc:.0f} {36 * sc:.0f} l {-70 * sc:.0f} {-8 * sc:.0f} Z" fill="#101014"/>')
    for k in range(70):
        x = r.uniform(-20, 1100); y = r.uniform(1300, 1900); sc = 0.4 + (y - 1300) / 600
        s += f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{r.uniform(6, 16) * sc:.0f}" ry="{r.uniform(4, 8) * sc:.0f}" fill="#5a4430" opacity="0.55"/>'
    s += grass_tufts(155, 1300, 1900, 18, "#7a6a3a", "#a89a5a")
    return svg_render(s)

def ridges_dusk():
    """watch fires along the ridges at dusk: layered dark ridges against an orange-violet sky; fire points in RIDGE_FIRES"""
    s = ("<defs>" + FILTERS + lg("sky", [(0, "#141a3a", 1), (0.3, "#3a2e5a", 1), (0.48, "#a84e4a", 1), (0.58, "#f09a5a", 1), (0.66, "#ffd08a", 1)]) + "</defs>")
    s += f'<rect width="{W}" height="{H}" fill="url(#sky)"/>' + stars(161, 90, 600)
    s += clouds(W, 162, [700, 800, 880], "#e07a6a", "#ffb08a", 0.5)
    layers = [(1080, 200, 163, "#4a3a5a"), (1200, 240, 164, "#33283e"), (1380, 260, 165, "#211a28"), (1600, 240, 166, "#120e16")]
    for base, amp, seed, col in layers:
        s += f'<path d="{ridge(W, base, amp, seed, rough=0.5)}" fill="{col}"/>'
    s += f'<rect x="0" y="960" width="{W}" height="200" fill="#ffb080" opacity="0.18" filter="url(#b40)"/>'
    for x, y, a in RIDGE_FIRES:
        s += f'<circle cx="{x}" cy="{y}" r="{26 * a:.0f}" fill="#ff9a40" opacity="0.35" filter="url(#b12)"/><circle cx="{x}" cy="{y}" r="{4 * a:.1f}" fill="#ffe0a0"/>'
    return svg_render(s)

def _ridge_y(base, amp, seed, x, n=40, rough=0.5):
    r = random.Random(seed); ys = []; y = 0
    for i in range(n + 1):
        y = y * 0.6 + r.uniform(-1, 1); ys.append(y)
    i = max(0, min(n - 1, int(x / W * n))); f = x / W * n - i
    yy = lambda i: base - amp * (0.5 + 0.5 * math.sin(i * 0.37 + seed)) - amp * rough * ys[i]
    return yy(i) * (1 - f) + yy(i + 1) * f

RIDGE_FIRES = [(x, round(_ridge_y(b, a, sd, x)) + 6, s) for (b, a, sd, s) in [(1200, 240, 164, 1.0), (1380, 260, 165, 1.5)] for x in (90, 300, 520, 740, 960)]

def war_room():
    """Bazz at night: stone walls, a hanging lamp (x 540, flame y ≈ 520), a red banner, a window with the moon; the table is drawn in the scene"""
    s = ("<defs>" + FILTERS + lg("wall", [(0, "#2a1c14", 1), (1, "#4a3222", 1)]) +
         rg("lamp", 540, 560, 900, [(0, "#ffb060", 0.5), (0.5, "#a05a28", 0.16), (1, "#000", 0)]) + "</defs>")
    s += f'<rect width="{W}" height="{H}" fill="url(#wall)"/>'
    r = random.Random(171)
    for row in range(30):
        y = 120 + row * 44; off = 0 if row % 2 else 50
        for k in range(-1, 12):
            x = off + k * 100 + r.uniform(-6, 6)
            s += f'<rect x="{x:.0f}" y="{y}" width="{r.uniform(84, 96):.0f}" height="38" rx="6" fill="#1a100a" opacity="{r.uniform(0.18, 0.35):.2f}"/>'
    s += ('<path d="M 820 400 L 820 760 L 960 760 L 960 400 Q 890 320, 820 400 Z" fill="#0e1430" stroke="#140a06" stroke-width="12"/>'
          '<circle cx="905" cy="470" r="26" fill="#f4f0e0"/><circle cx="905" cy="470" r="70" fill="#c8d0ff" opacity="0.15" filter="url(#b20)"/>'
          '<path d="M 890 400 L 890 760" stroke="#140a06" stroke-width="8"/>')
    s += ('<rect x="110" y="300" width="10" height="560" fill="#2a1a10"/><path d="M 120 310 L 330 330 L 320 620 L 230 580 L 130 620 Z" fill="#9a1418" stroke="#2a0606" stroke-width="3"/>'
          '<path d="M 120 340 L 328 358" stroke="#e0b25a" stroke-width="6" opacity="0.8"/>')
    s += '<rect x="0" y="1180" width="1080" height="740" fill="#1e140e"/><path d="M 0 1180 L 1080 1180" stroke="#3a2a1a" stroke-width="6"/>'
    s += oil_lamp(540, 520, 520)
    s += f'<rect width="{W}" height="{H}" fill="url(#lamp)"/>'
    return svg_render(s)

def table_map():
    """top-down: an old wooden table with a map scratched into it (mountains, a river, Bazz in the middle at (540, 980))"""
    s = "<defs>" + FILTERS + rg("lt", 520, 900, 1100, [(0, "#a06a3a", 1), (0.6, "#6a4222", 1), (1, "#2e1a0c", 1)]) + "</defs>"
    s += f'<rect width="{W}" height="{H}" fill="url(#lt)"/>'
    r = random.Random(181)
    for k in range(11):
        y = k * 180 + r.uniform(-10, 10)
        s += f'<path d="M 0 {y:.0f} L 1080 {y + r.uniform(-8, 8):.0f}" stroke="#1e1006" stroke-width="7" opacity="0.7"/>'
        for j in range(6):
            yy = y + r.uniform(20, 160); x0 = r.uniform(-100, 900)
            s += f'<path d="M {x0:.0f} {yy:.0f} q {r.uniform(100, 200):.0f} {r.uniform(-8, 8):.0f} {r.uniform(250, 420):.0f} {r.uniform(-6, 6):.0f}" stroke="#3a2010" stroke-width="2.5" fill="none" opacity="0.45"/>'
    for x, y, sz in [(260, 700, 70), (380, 620, 60), (760, 680, 80), (860, 820, 60), (250, 1250, 70), (800, 1300, 75), (420, 1420, 55), (680, 1460, 60), (180, 980, 55), (900, 1060, 60)]:
        s += f'<path d="M {x - sz} {y + sz * 0.5:.0f} L {x} {y - sz * 0.6:.0f} L {x + sz} {y + sz * 0.5:.0f}" stroke="#e8c898" stroke-width="5" fill="none" opacity="0.75" stroke-linejoin="round"/>'
    s += '<path d="M 60 560 C 200 700, 300 760, 330 900 C 360 1040, 300 1200, 420 1320 C 520 1420, 700 1500, 1020 1560" stroke="#e8c898" stroke-width="4" fill="none" stroke-dasharray="14 10" opacity="0.6"/>'
    s += '<path d="M 500 1000 L 500 940 L 520 940 L 520 955 L 540 955 L 540 940 L 560 940 L 560 955 L 580 955 L 580 940 L 600 940 L 600 1000 Z" fill="none" stroke="#f0d0a0" stroke-width="5" opacity="0.85" transform="translate(-10,0)"/>'
    return svg_render(s)

FOREST = {"day": dict(sky=[(0, "#4a7cb8", 1), (0.4, "#a8c8de", 1), (0.55, "#eedcb8", 1)], far="#8e9ab8", mid="#6a7a5a", slope="#7a6a48", slope_d="#5a4a32",
                      road="#c4a478", road_d="#9a7e58", tree="#3e5a2e", tree_d="#2a4020", hi="#5a7a3a", pine="#2e4a32", pine_d="#1e3424", haze="#f0e4c8"),
          "night": dict(sky=[(0, "#04060e", 1), (0.45, "#101a34", 1), (0.6, "#1c2444", 1)], far="#1e2440", mid="#151c2a", slope="#1c1e26", slope_d="#121418",
                        road="#4a4e5e", road_d="#30323e", tree="#14201a", tree_d="#0c1410", hi="#24342a", pine="#101a16", pine_d="#0a100c", haze="#4a5a8a"),
          # Babak 7: an autumn valley in Armenia, the morning of the hunt
          "autumn": dict(sky=[(0, "#5a86bc", 1), (0.38, "#b4cce0", 1), (0.55, "#f6e2c2", 1)], far="#9a98b4", mid="#8e7a48", slope="#9c7c46", slope_d="#6c5230",
                         road="#cbab7a", road_d="#9c8058", tree="#c2662a", tree_d="#8a3c1a", hi="#e8aa3c", pine="#2e4a32", pine_d="#1e3424", haze="#fae8c8")}

def forest_road(pal="day"):
    """a road along a wooded mountainside (road band at feet y 1300-1420); trees above and below; night: moon and stars"""
    P = FOREST[pal]
    s = "<defs>" + FILTERS + lg("sky", P["sky"]) + lg("sl", [(0, P["slope"], 1), (1, P["slope_d"], 1)]) + "</defs>"
    s += f'<rect width="{W}" height="{H}" fill="url(#sky)"/>'
    if pal == "night":
        s += stars(191, 220, 900) + '<circle cx="820" cy="380" r="44" fill="#f4f0e0"/><circle cx="820" cy="380" r="150" fill="#c8d0ff" opacity="0.12" filter="url(#b40)"/>'
    else:
        s += clouds(W, 192, [330, 440], "#ffffff", "#fff8e8", 0.6)
    s += f'<path d="{ridge(W, 900, 300, 193, rough=0.5)}" fill="{P["far"]}"/>'
    s += f'<rect x="0" y="820" width="{W}" height="220" fill="{P["haze"]}" opacity="0.25" filter="url(#b40)"/>'
    s += f'<path d="M -40 2000 L -40 1020 C 200 960, 500 1000, 700 950 C 860 915, 1000 950, 1120 930 L 1120 2000 Z" fill="{P["mid"]}"/>'
    r = random.Random(194)
    for k in range(16):           # far pines along the upper slope
        x = r.uniform(-20, 1100); y = 1000 - 40 * math.sin(x / 300) + r.uniform(0, 140)
        s += pine(x, y, r.uniform(110, 170), P["pine"], P["pine_d"])
    s += f'<path d="M -40 2000 L -40 1260 C 300 1240, 800 1250, 1120 1235 L 1120 2000 Z" fill="url(#sl)"/>'
    s += f'<path d="M -40 1290 C 300 1270, 800 1280, 1120 1265 L 1120 1440 C 800 1450, 300 1445, -40 1460 Z" fill="{P["road"]}"/>'
    s += f'<path d="M -40 1290 C 300 1270, 800 1280, 1120 1265" stroke="{P["road_d"]}" stroke-width="8" fill="none" opacity="0.6"/>'
    s += f'<path d="M -40 1380 C 300 1370, 800 1378, 1120 1360" stroke="{P["road_d"]}" stroke-width="5" fill="none" opacity="0.35"/>'
    for k in range(40):
        x = r.uniform(-20, 1100); y = r.uniform(1290, 1450)
        s += f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{r.uniform(5, 12):.0f}" ry="{r.uniform(3, 6):.0f}" fill="{P["road_d"]}" opacity="0.6"/>'
    for i, (x, y, rr) in enumerate([(60, 1250, 40), (1020, 1240, 50), (980, 1500, 60), (90, 1520, 70)]):
        s += boulder(x, y, rr, 195 + i, P["slope"], P["slope_d"], P["road"] if pal == "day" else "#5a6070")
    for i, (x, h) in enumerate([(-30, 560), (1110, 600), (980, 470), (120, 430)]):    # big trees in front of the lower slope (edges)
        s += oak(x, 1700 + 40 * (i % 2), h, 196 + i, P["tree"], P["tree_d"], P["hi"])
    s += grass_tufts(197, 1460, 1900, 22, P["tree_d"], P["hi"])
    return svg_render(s)

def leaves_fg(pal="day"):
    """foreground foliage framing the frame (scouts watching from the trees): a trunk at the left, leaves at the top,
    the right edge and a thick bush across the bottom (from y ≈ 1180)"""
    P = FOREST[pal]
    r = random.Random(201)
    s = "<defs>" + FILTERS + "</defs>"
    s += '<path d="M -40 2000 L -40 -40 L 120 -40 C 130 600, 150 1300, 190 2000 Z" fill="#2a1a10"/><path d="M 120 -40 C 130 600, 150 1300, 190 2000" stroke="#4a3220" stroke-width="10" fill="none"/>'
    def leaf(x, y, a, L, col):
        return (f'<g transform="translate({x:.0f},{y:.0f}) rotate({a:.0f})"><path d="M {-L / 2:.0f} 0 C {-L / 4:.0f} {-L * 0.32:.0f}, {L / 4:.0f} {-L * 0.32:.0f}, {L / 2:.0f} 0 '
                f'C {L / 4:.0f} {L * 0.32:.0f}, {-L / 4:.0f} {L * 0.32:.0f}, {-L / 2:.0f} 0 Z" fill="{col}" stroke="#0e160a" stroke-width="3"/>'
                f'<path d="M {-L / 2:.0f} 0 L {L / 2:.0f} 0" stroke="#0e160a" stroke-width="2" opacity="0.5"/></g>')
    clusters = [(80, 120, 26, 200, 130), (520, 20, 22, 380, 90), (1000, 160, 22, 150, 160), (1050, 700, 12, 90, 160)]
    for cx, cy, n, rx, ry in clusters:
        for k in range(n):
            s += leaf(cx + r.uniform(-1, 1) * rx, cy + r.uniform(-1, 1) * ry, r.uniform(0, 180), r.uniform(120, 200), r.choice([P["tree"], P["tree_d"], P["hi"]]))
    bush = "M -40 2000 L -40 1260 " + " ".join(f"Q {x - 45:.0f} {1170 + r.uniform(-40, 30):.0f} {x:.0f} {1230 + r.uniform(-30, 30):.0f}" for x in range(60, 1200, 90)) + " L 1120 2000 Z"
    s += f'<path d="{bush}" fill="{P["tree_d"]}"/>'
    for k in range(70):
        x = r.uniform(-40, 1120); y = r.uniform(1170, 1950)
        s += leaf(x, y, r.uniform(0, 180), r.uniform(130, 210), r.choice([P["tree"], P["tree_d"], P["hi"], P["tree"]]))
    return svg_render(s).filter(ImageFilter.GaussianBlur(1.5))

def woods_night():
    """a camp in the woods at night: stars, a thin moon, trunks and dark canopy; ground at y 1300+ (the fire is drawn in the scene)"""
    s = ("<defs>" + FILTERS + lg("sky", [(0, "#04060e", 1), (0.5, "#0e1630", 1), (0.7, "#18203a", 1)]) +
         rg("fire", 540, 1400, 760, [(0, "#ff9a40", 0.32), (0.5, "#a04a20", 0.12), (1, "#000", 0)]) + "</defs>")
    s += f'<rect width="{W}" height="{H}" fill="url(#sky)"/>' + stars(211, 200, 1000)
    s += '<path d="M 300 300 C 270 330, 270 380, 300 410 C 280 380, 282 330, 300 300 Z" fill="#f0ecd8"/>'
    s += f'<path d="{ridge(W, 1150, 160, 212)}" fill="#141a2c"/>'
    r = random.Random(213)
    for k in range(12):
        x = r.uniform(-40, 1120); y = r.uniform(1240, 1320)
        s += pine(x, y, r.uniform(380, 620), "#0c1410", "#080c0a", "#140c08")
    s += '<rect x="0" y="1300" width="1080" height="620" fill="#16100c"/>'
    for i, (x, y, rr) in enumerate([(120, 1330, 60), (960, 1320, 70), (300, 1310, 40)]):
        s += boulder(x, y, rr, 214 + i, "#2a2a30", "#16161a", "#4a4440")
    s += f'<rect width="{W}" height="{H}" fill="url(#fire)"/>'
    return svg_render(s)

RAVINE = {"night": dict(sky=[(0, "#060a18", 1), (1, "#1a2448", 1)], wall="#2a2c3a", wall_d="#16161e", wall_l="#5a6488", floor="#24242c", floor_d="#141418", lit=0.0),
          "dawn": dict(sky=[(0, "#6a7ab0", 1), (0.6, "#e8a890", 1), (1, "#ffd8a8", 1)], wall="#7a5a48", wall_d="#3e2c26", wall_l="#f0a878", floor="#6a5446", floor_d="#3e3028", lit=1.0)}

def ravine(pal="night"):
    """a narrow ravine: steep walls left and right, a strip of sky, a stony floor (people at feet y 1400-1700)"""
    P = RAVINE[pal]
    s = ("<defs>" + FILTERS + lg("sky", P["sky"]) + lg("fl", [(0, P["floor"], 1), (1, P["floor_d"], 1)]) +
         lg("wl", [(0, P["wall_l"], 1), (0.25, P["wall"], 1), (1, P["wall_d"], 1)]) + lg("wr", [(0, P["wall"], 1), (1, P["wall_d"], 1)]) + "</defs>")
    s += f'<rect width="{W}" height="{H}" fill="url(#sky)"/>'
    if pal == "night":
        s += stars(221, 60, 700)
    s += f'<path d="M 300 2000 L 300 900 L 380 700 L 470 760 L 560 620 L 650 720 L 760 660 L 780 2000 Z" fill="{P["wall_d"]}" opacity="0.9"/>'
    s += f'<path d="M -40 2000 L -40 -40 L 260 -40 L 300 300 L 250 600 L 330 900 L 290 1200 L 380 1420 L 330 2000 Z" fill="url(#wl)"/>'
    s += f'<path d="M 1120 2000 L 1120 -40 L 820 -40 L 780 260 L 850 560 L 760 880 L 820 1150 L 700 1420 L 760 2000 Z" fill="url(#wr)"/>'
    s += f'<path d="M 260 -40 L 300 300 L 250 600 L 330 900 L 290 1200 L 380 1420" stroke="{P["wall_l"]}" stroke-width="10" fill="none" opacity="{0.4 + 0.4 * P["lit"]:.2f}" stroke-linejoin="round"/>'
    s += _strata(222, -40, 300, 0, 1900, 30, "#000", 0.25, 5, slope=0.1) + _strata(223, 780, 1120, 0, 1900, 30, "#000", 0.25, 5, slope=-0.1)
    s += _cracks(224, 0, 260, 0, 1700, 10, "#000", 0.35) + _cracks(225, 820, 1080, 0, 1700, 10, "#000", 0.35)
    s += f'<path d="M -40 1440 C 200 1400, 500 1380, 700 1400 C 900 1420, 1000 1430, 1120 1450 L 1120 2000 L -40 2000 Z" fill="url(#fl)"/>'
    for i, (x, y, rr) in enumerate([(130, 1460, 80), (930, 1470, 90), (560, 1420, 30), (420, 1440, 24), (700, 1880, 120), (260, 1860, 100)]):
        s += boulder(x, y, rr, 226 + i, P["wall"], P["wall_d"], P["wall_l"])
    if pal == "dawn":
        s += '<path d="M 560 620 L 650 720 L 760 660 L 780 900 L 300 900 L 380 700 L 470 760 Z" fill="#ffd0a0" opacity="0.25" filter="url(#b20)"/>'
    return svg_render(s)

def ravine_up():
    """looking up from the ravine at dawn: the rim (y ≈ 700-760) against the morning sky; walls rise on both sides"""
    s = ("<defs>" + FILTERS + lg("sky", [(0, "#3a5a9a", 1), (0.25, "#9aa8d0", 1), (0.38, "#f4b8a0", 1), (0.46, "#ffe0b0", 1)]) +
         lg("wall", [(0, "#c88a64", 1), (0.3, "#8a5a40", 1), (1, "#2e1e18", 1)]) + "</defs>")
    s += f'<rect width="{W}" height="{H}" fill="url(#sky)"/>' + clouds(W, 231, [260, 360, 470], "#ffd0c0", "#fff0e0", 0.55)
    rim = [(-40, 760), (80, 730), (200, 750), (330, 712), (460, 730), (600, 706), (740, 726), (880, 702), (1000, 730), (1120, 715)]
    s += '<path d="M -40 2000 L ' + " L ".join(f"{x} {y}" for x, y in rim) + ' L 1120 2000 Z" fill="url(#wall)"/>'
    s += '<path d="M ' + " L ".join(f"{x} {y}" for x, y in rim) + '" stroke="#ffd8a8" stroke-width="8" fill="none" opacity="0.8"/>'
    r = random.Random(232)
    for _ in range(40):
        y = r.uniform(760, 1900); x = r.uniform(-40, 1080); L = r.uniform(80, 240)
        s += f'<path d="M {x:.0f} {y:.0f} q {L / 2:.0f} {-(y - 700) * 0.02:.0f} {L:.0f} {-(y - 700) * 0.05:.0f}" stroke="#3a2418" stroke-width="{3 + (y - 700) / 300:.1f}" fill="none" opacity="0.35"/>'
    s += _cracks(233, 0, 1080, 780, 1800, 16, "#2a160c", 0.4)
    s += '<path d="M -40 2000 L -40 -40 L 100 -40 L 140 400 L 80 800 L 150 1200 L 70 1600 L 110 2000 Z" fill="#2a1a12"/>'
    s += '<path d="M 1120 2000 L 1120 -40 L 990 -40 L 960 300 L 1020 700 L 950 1100 L 1030 1500 L 990 2000 Z" fill="#33201a"/>'
    s += f'<rect x="0" y="1200" width="{W}" height="720" fill="#000" opacity="0.25"/>'
    return svg_render(s)

# ------------------------------------------------------------------ PART 6 (Babak, episode 3): the side gate, the walls of Bazz, the forest stream, the field, Sahl's gate
def side_gate_night():
    """Bazz at night: a high stone wall with a small side gate (arch x 330-520, sill y 1360), a torch, the moon (rider leaves at feet y 1400-1600)"""
    s = ("<defs>" + FILTERS + lg("sky", [(0, "#04060f", 1), (0.5, "#111a36", 1), (0.7, "#1c2442", 1)]) + lg("wl", [(0, "#2e2a30", 1), (1, "#1a171c", 1)]) +
         rg("tq", 600, 1120, 420, [(0, "#ffb060", 0.45), (0.5, "#a05a28", 0.12), (1, "#000", 0)]) + "</defs>")
    s += f'<rect width="{W}" height="{H}" fill="url(#sky)"/>' + stars(241, 160, 700)
    s += '<circle cx="860" cy="330" r="40" fill="#f4f0e0"/><circle cx="860" cy="330" r="140" fill="#c8d0ff" opacity="0.12" filter="url(#b40)"/>'
    s += '<path d="M -40 1440 L -40 640 L 1120 600 L 1120 1440 Z" fill="url(#wl)"/>'
    s += "".join(f'<rect x="{-30 + i * 72}" y="{598 - 2 * i if i < 16 else 566}" width="44" height="46" fill="#2e2a30"/>' for i in range(16))
    r = random.Random(242)
    for row in range(18):
        y = 660 + row * 44; off = 0 if row % 2 else 46
        for k in range(-1, 13):
            x = off + k * 92 + r.uniform(-5, 5)
            s += f'<rect x="{x:.0f}" y="{y}" width="{r.uniform(76, 88):.0f}" height="38" rx="5" fill="#0e0c10" opacity="{r.uniform(0.25, 0.45):.2f}"/>'
    s += ('<path d="M 320 1440 L 320 1130 Q 425 1010, 530 1130 L 530 1440 Z" fill="#0a080c" stroke="#3a3440" stroke-width="10"/>'
          '<path d="M 300 1440 L 300 1120 Q 425 985, 550 1120 L 550 1440" fill="none" stroke="#4a4450" stroke-width="8"/>')
    s += '<rect x="592" y="1080" width="14" height="90" fill="#3a2414"/>'
    s += '<rect x="0" y="1440" width="1080" height="480" fill="#16141a"/><path d="M -40 1440 L 1120 1440" stroke="#2e2a32" stroke-width="8"/>'
    s += f'<rect width="{W}" height="{H}" fill="url(#tq)"/>'
    return svg_render(s)

def wall_outside(pal="day"):
    """the outer wall of Bazz seen from below: crenellated top at y ≈ 820, stone face to the bottom; smoky summer sky (ladders drawn in the scene)"""
    s = ("<defs>" + FILTERS + lg("sky", [(0, "#4a5a7a", 1), (0.35, "#a0a4b0", 1), (0.5, "#e8c8a0", 1)]) + lg("wl", [(0, "#9a7a5c", 1), (1, "#5a4232", 1)]) + "</defs>")
    s += f'<rect width="{W}" height="{H}" fill="url(#sky)"/>' + clouds(W, 251, [300, 420], "#e8e0d8", "#ffffff", 0.5)
    s += '<path d="M -40 1920 L -40 860 L 1120 820 L 1120 1920 Z" fill="url(#wl)"/>'
    s += "".join(f'<rect x="{-30 + i * 74}" y="{806 - 1.4 * i:.0f}" width="46" height="62" fill="#9a7a5c" stroke="#3a2a1c" stroke-width="3"/>' for i in range(16))
    r = random.Random(252)
    for row in range(24):
        y = 880 + row * 44; off = 0 if row % 2 else 50
        for k in range(-1, 12):
            x = off + k * 100 + r.uniform(-6, 6)
            s += f'<rect x="{x:.0f}" y="{y}" width="{r.uniform(84, 96):.0f}" height="38" rx="5" fill="#3a2a1c" opacity="{r.uniform(0.18, 0.32):.2f}"/>'
    s += _cracks(253, 0, 1080, 880, 1800, 14, "#2a1a10", 0.4)
    s += f'<rect x="0" y="1500" width="{W}" height="420" fill="#000" opacity="0.18"/>'
    return svg_render(s)

def forest_stream():
    """a dense forest by a mountain stream, cool morning: tall pines, a stream across the lower middle (y 1330-1480), mossy stones; people stand at y 1500-1700"""
    s = ("<defs>" + FILTERS + lg("sky", [(0, "#7a9ab8", 1), (0.5, "#c8d8d8", 1)]) + lg("gr", [(0, "#4a5a34", 1), (1, "#2e3a22", 1)]) +
         lg("wt", [(0, "#5a8aa0", 1), (1, "#2e5a70", 1)]) + "</defs>")
    s += f'<rect width="{W}" height="{H}" fill="url(#sky)"/>'
    r = random.Random(261)
    for k in range(14):
        x = r.uniform(-60, 1140); s += pine(x, r.uniform(1150, 1220), r.uniform(700, 900), "#4a6a5a", "#3a5a4a", "#3a2a1e")
    s += f'<rect x="0" y="700" width="{W}" height="500" fill="#e0e8e8" opacity="0.35" filter="url(#b40)"/>'
    for k in range(9):
        x = r.uniform(-60, 1140); s += pine(x, r.uniform(1260, 1320), r.uniform(900, 1150), "#2e4a32", "#1e3424", "#3a2618")
    s += '<path d="M -40 1260 C 300 1240, 800 1250, 1120 1255 L 1120 2000 L -40 2000 Z" fill="url(#gr)"/>'
    s += '<path d="M -40 1350 C 300 1320, 700 1340, 1120 1325 L 1120 1450 C 700 1470, 300 1460, -40 1490 Z" fill="url(#wt)"/>'
    for k in range(12):
        x = r.uniform(0, 1080); y = r.uniform(1350, 1460)
        s += f'<path d="M {x:.0f} {y:.0f} q 30 -8 60 0" stroke="#c8e0e8" stroke-width="4" fill="none" opacity="0.6"/>'
    for i, (x, y, rr) in enumerate([(160, 1350, 50), (900, 1340, 60), (520, 1470, 44), (80, 1500, 70), (1000, 1490, 80)]):
        s += boulder(x, y, rr, 262 + i, "#6a7a6a", "#3a4a3a", "#a8b8a0")
    s += grass_tufts(263, 1500, 1900, 26, "#3e5a2a", "#7a9a4a")
    for i, (x, h) in enumerate([(-40, 1500), (1120, 1550)]):
        s += f'<rect x="{x - 50}" y="0" width="100" height="1920" fill="#2a1c12"/>'
    return svg_render(s)

def field_dawn():
    """the edge of the forest at dawn: a ploughed field (furrows), a low hill on the right (rider at y ≈ 1010), the forest edge on the left"""
    s = ("<defs>" + FILTERS + lg("sky", [(0, "#5a6a9a", 1), (0.3, "#c8a0a0", 1), (0.48, "#ffd0a0", 1)]) + lg("fd", [(0, "#8a6a4a", 1), (1, "#5a4030", 1)]) + "</defs>")
    s += f'<rect width="{W}" height="{H}" fill="url(#sky)"/>' + clouds(W, 271, [380, 480, 600], "#ffc8b0", "#fff0e0", 0.55)
    s += '<circle cx="760" cy="960" r="70" fill="#fff0c8" opacity="0.9"/><circle cx="760" cy="960" r="260" fill="#ffd8a0" opacity="0.25" filter="url(#b40)"/>'
    s += f'<path d="{ridge(W, 1080, 140, 272, rough=0.4)}" fill="#8a7a9a"/>'
    s += '<path d="M 520 1200 C 700 1040, 900 1000, 1120 1030 L 1120 1300 L 520 1300 Z" fill="#6a6a4a"/>'
    s += '<path d="M -40 1200 C 300 1180, 800 1170, 1120 1200 L 1120 2000 L -40 2000 Z" fill="url(#fd)"/>'
    for k in range(16):
        y = 1210 + k * k * 3.2
        s += f'<path d="M -40 {y:.0f} C 300 {y - 10:.0f}, 800 {y - 14:.0f}, 1120 {y + 2:.0f}" stroke="#4a3424" stroke-width="{2 + k * 0.6:.1f}" fill="none" opacity="0.55"/>'
    r = random.Random(273)
    for k in range(10):
        s += pine(r.uniform(-80, 220), r.uniform(1220, 1280), r.uniform(500, 760), "#2e4032", "#1e2c24", "#2a1c12")
    return svg_render(s)

def armenia_gate():
    """night in the mountains of Armenia: a stone fortress gate (opening x 400-680, sill y 1380) with torches on both sides"""
    s = ("<defs>" + FILTERS + lg("sky", [(0, "#04060f", 1), (0.6, "#141a34", 1)]) + lg("st", [(0, "#4a4248", 1), (1, "#2a2428", 1)]) +
         rg("tl", 330, 1020, 380, [(0, "#ffb060", 0.5), (1, "#000", 0)]) + rg("tr", 750, 1020, 380, [(0, "#ffb060", 0.5), (1, "#000", 0)]) +
         rg("inside", 540, 1250, 300, [(0, "#ffb870", 0.6), (1, "#000", 0)]) + "</defs>")
    s += f'<rect width="{W}" height="{H}" fill="url(#sky)"/>' + stars(281, 180, 700)
    s += f'<path d="{ridge(W, 900, 300, 282, rough=0.6)}" fill="#141a2c"/>'
    s += '<path d="M 60 1400 L 60 560 L 100 520 L 140 560 L 140 600 L 940 600 L 940 560 L 980 520 L 1020 560 L 1020 1400 Z" fill="url(#st)" stroke="#120e12" stroke-width="5"/>'
    s += "".join(f'<rect x="{150 + i * 64}" y="568" width="38" height="36" fill="#3a3238"/>' for i in range(13))
    r = random.Random(283)
    for row in range(17):
        y = 620 + row * 46; off = 0 if row % 2 else 50
        for k in range(0, 10):
            x = 70 + off + k * 100 + r.uniform(-6, 6)
            if 390 < x < 690 and y > 1000:
                continue
            s += f'<rect x="{x:.0f}" y="{y}" width="{r.uniform(80, 92):.0f}" height="40" rx="5" fill="#1a1418" opacity="{r.uniform(0.25, 0.4):.2f}"/>'
    s += '<path d="M 390 1400 L 390 1110 Q 540 960, 690 1110 L 690 1400 Z" fill="url(#inside)" stroke="#120e12" stroke-width="10"/>'
    s += '<path d="M 370 1110 Q 540 940, 710 1110" stroke="#5a5058" stroke-width="16" fill="none"/>'
    for x in (330, 750):
        s += f'<rect x="{x - 6}" y="1020" width="12" height="110" fill="#3a2414"/>'
    s += '<rect x="0" y="1400" width="1080" height="520" fill="#1a1618"/><path d="M 380 1400 L 700 1400 L 820 1920 L 260 1920 Z" fill="#3a2e28" opacity="0.6"/>'
    s += f'<rect width="{W}" height="{H}" fill="url(#tl)"/><rect width="{W}" height="{H}" fill="url(#tr)"/>'
    return svg_render(s)


# ------------------------------------------------------------------ PART 7 (Babak, episode 4 half 1): Sahl's castle, Samarra's palace
def sahl_room():
    """Sahl's hall at night (Armenia, 837): stone walls, a carved cross-stone, a blue-and-gold hanging, an arched window with the moon (left),
    a hanging oil lamp (flame x 760, y ≈ 520) and a table with a candle at the right (table top y 1250); floor from y 1330"""
    s = ("<defs>" + FILTERS + lg("wall", [(0, "#241a16", 1), (1, "#46322a", 1)]) +
         rg("lamp", 760, 600, 950, [(0, "#ffb060", 0.5), (0.5, "#a05a28", 0.16), (1, "#000", 0)]) +
         rg("cand", 900, 1150, 420, [(0, "#ffc070", 0.45), (1, "#000", 0)]) + lg("rug", [(0, "#24365a", 1), (1, "#16223a", 1)]) + "</defs>")
    s += f'<rect width="{W}" height="{H}" fill="url(#wall)"/>'
    r = random.Random(701)
    for row in range(29):
        y = 130 + row * 42; off = 0 if row % 2 else 55
        for k in range(-1, 12):
            x = off + k * 110 + r.uniform(-6, 6)
            s += f'<rect x="{x:.0f}" y="{y}" width="{r.uniform(92, 104):.0f}" height="36" rx="6" fill="#140c08" opacity="{r.uniform(0.18, 0.34):.2f}"/>'
    s += '<rect x="0" y="0" width="1080" height="120" fill="#120a06"/>' + "".join(f'<rect x="{x}" y="90" width="70" height="60" fill="#2a1a10" stroke="#0a0604" stroke-width="3"/>' for x in (60, 330, 600, 870))
    # the window with the moon
    s += ('<clipPath id="win7"><path d="M 90 980 L 90 560 Q 190 420, 290 560 L 290 980 Z"/></clipPath>'
          '<path d="M 90 980 L 90 560 Q 190 420, 290 560 L 290 980 Z" fill="#0c1430" stroke="#120a06" stroke-width="14"/>' + '<g clip-path="url(#win7)">' + stars(702, 60, 980, 300) + '</g>' +
          '<circle cx="215" cy="640" r="30" fill="#f4f0e0"/><circle cx="228" cy="632" r="26" fill="#0c1430"/>'
          '<circle cx="200" cy="650" r="90" fill="#c8d0ff" opacity="0.12" filter="url(#b20)"/>'
          '<path d="M 190 500 L 190 980 M 90 760 L 290 760" stroke="#120a06" stroke-width="10"/>'
          '<path d="M 80 990 L 300 990" stroke="#3a2a20" stroke-width="18"/>')
    # carved cross-stone (khachkar)
    s += ('<rect x="430" y="540" width="200" height="330" rx="10" fill="#7a6a5e" stroke="#2a1e18" stroke-width="6"/>'
          '<rect x="446" y="556" width="168" height="298" rx="6" fill="none" stroke="#5a4a40" stroke-width="5"/>'
          '<path d="M 530 590 L 530 760 M 482 640 L 578 640" stroke="#4a3a30" stroke-width="22" stroke-linecap="round"/>'
          '<path d="M 530 590 l -16 -14 M 530 590 l 16 -14 M 482 640 l -14 -16 M 482 640 l -14 16 M 578 640 l 14 -16 M 578 640 l 14 16" stroke="#4a3a30" stroke-width="9" stroke-linecap="round"/>'
          '<circle cx="530" cy="810" r="28" fill="none" stroke="#4a3a30" stroke-width="8"/><circle cx="530" cy="810" r="9" fill="#4a3a30"/>')
    # blue-and-gold hanging (Sahl's colours)
    s += ('<rect x="866" y="300" width="12" height="40" fill="#2a1a10"/><path d="M 800 340 L 960 340 L 960 820 L 880 780 L 800 820 Z" fill="#24466a" stroke="#0e1a2a" stroke-width="5"/>'
          '<path d="M 812 360 L 948 360 M 812 760 L 948 760" stroke="#e0b25a" stroke-width="8"/>'
          + "".join(f'<path d="M {880} {430 + k * 80} l 22 26 l -22 26 l -22 -26 Z" fill="#e0b25a" opacity="0.7"/>' for k in range(4)))
    # floor, rug, table with a candle
    s += '<rect x="0" y="1330" width="1080" height="590" fill="#22160e"/><path d="M 0 1330 L 1080 1330" stroke="#3a281a" stroke-width="6"/>'
    s += '<path d="M 160 1420 L 920 1420 L 1060 1920 L 20 1920 Z" fill="url(#rug)"/><path d="M 190 1440 L 890 1440 L 1020 1900 L 60 1900 Z" fill="none" stroke="#c9a24a" stroke-width="7"/>'
    s += ('<rect x="700" y="1250" width="380" height="34" rx="6" fill="#4a2e1a" stroke="#1a0e06" stroke-width="5"/>'
          '<rect x="730" y="1284" width="24" height="120" fill="#3a2414"/><rect x="1030" y="1284" width="24" height="120" fill="#3a2414"/>'
          '<rect x="884" y="1176" width="30" height="74" rx="4" fill="#efe2c4" stroke="#2a1a10" stroke-width="3"/><rect x="872" y="1244" width="54" height="10" rx="3" fill="#b9832f"/>'
          '<path d="M 899 1176 C 889 1160, 893 1146, 899 1132 C 905 1146, 909 1160, 899 1176 Z" fill="#ffe8a0"/>')
    s += oil_lamp(760, 520, 400)
    s += f'<rect width="{W}" height="{H}" fill="url(#lamp)"/><rect width="{W}" height="{H}" fill="url(#cand)"/>'
    return svg_render(s)

def palace_court():
    """the caliph's palace in Samarra, an inner court on a winter morning (838): a great gate in the back wall at the left (opening x 80-470,
    y 320-1080; through it the street and the crowd), an arcade in the middle, a palace door at the right (opening x 890-1030), black
    banners, palms above the wall; paved ground from y 1080 (people stand at y 1120-1300, the elephant at about y 1150)"""
    B = 1080
    s = ("<defs>" + FILTERS + lg("sky", [(0, "#7a8cb8", 1), (0.6, "#e8c8b0", 1), (1, "#f6dcc0", 1)]) + lg("wl", [(0, "#d2aa82", 1), (1, "#b08664", 1)]) +
         lg("street", [(0, "#fff0d8", 1), (1, "#e2c49a", 1)]) + lg("pave", [(0, "#b49274", 1), (1, "#6e5442", 1)]) + "</defs>")
    s += f'<rect width="{W}" height="{H}" fill="url(#sky)"/>' + clouds(W, 711, [120, 200], "#ffffff", "#fff4e8", 0.5)
    for px, ph in [(640, 300), (770, 360), (1010, 330)]:          # palms behind the wall
        s += f'<path d="M {px} 420 C {px - 10} {420 - ph * 0.5}, {px + 10} {420 - ph * 0.8}, {px} {420 - ph}" stroke="#4a3a2a" stroke-width="14" fill="none"/>'
        for a in range(0, 360, 40):
            ang = math.radians(a); L = 105
            s += f'<path d="M {px} {420 - ph} q {math.cos(ang) * L * 0.5:.0f} {math.sin(ang) * L * 0.3 - 26:.0f} {math.cos(ang) * L:.0f} {math.sin(ang) * L * 0.5 + 18:.0f}" stroke="#3e5a34" stroke-width="13" fill="none" stroke-linecap="round"/>'
    s += f'<rect x="0" y="380" width="1080" height="{B - 380}" fill="url(#wl)"/>' + "".join(f'<rect x="{i * 54}" y="352" width="34" height="32" fill="#c8a07a"/>' for i in range(21))
    s += f'<path d="M 0 420 L 1080 420" stroke="#9a7254" stroke-width="6"/><path d="M 0 {B - 18} L 1080 {B - 18}" stroke="#8a6448" stroke-width="10"/>'
    # gate tower and the great gate (left)
    s += f'<rect x="30" y="240" width="480" height="{B - 240}" fill="#c49a74" stroke="#7a5638" stroke-width="5"/>' + "".join(f'<rect x="{34 + i * 60}" y="210" width="38" height="34" fill="#c49a74" stroke="#7a5638" stroke-width="3"/>' for i in range(8))
    arch = f"M 80 {B} L 80 520 Q 80 360, 275 320 Q 470 360, 470 520 L 470 {B} Z"
    s += f'<path d="{arch}" fill="url(#street)"/>'
    r = random.Random(712)
    crowd = ""
    for row, (y, sc, cols) in enumerate([(930, 0.8, ["#7a6a8a", "#8a6a5a", "#6a7a8a"]), (1000, 1.0, ["#5a4a5a", "#6a4a3a", "#4a5a6a", "#7a3a2a"]), (1075, 1.25, ["#3a2a30", "#4a3428", "#2a3440", "#5a2a20"])]):
        for k in range(14):
            x = 70 + k * 30 + r.uniform(-8, 8); col = r.choice(cols)
            crowd += (f'<path d="M {x - 22 * sc:.0f} {y + 40:.0f} C {x - 22 * sc:.0f} {y - 10 * sc:.0f}, {x + 22 * sc:.0f} {y - 10 * sc:.0f}, {x + 22 * sc:.0f} {y + 40:.0f} Z" fill="{col}"/>'
                      f'<circle cx="{x:.0f}" cy="{y - 24 * sc:.0f}" r="{13 * sc:.0f}" fill="{col}"/>')
            if r.random() < 0.35:
                crowd += f'<path d="M {x + 8 * sc:.0f} {y - 6 * sc:.0f} L {x + 20 * sc:.0f} {y - 62 * sc:.0f}" stroke="{col}" stroke-width="{7 * sc:.0f}" stroke-linecap="round"/>'
    s += f'<clipPath id="gclip7"><path d="{arch}"/></clipPath><g clip-path="url(#gclip7)">{crowd}</g>'
    s += f'<path d="{arch[:-2]}" fill="none" stroke="#6a4a30" stroke-width="16"/>'
    s += f'<path d="M 56 {B} L 56 510 Q 56 330, 275 288 Q 494 330, 494 510 L 494 {B}" fill="none" stroke="#e8c8a0" stroke-width="10" opacity="0.8"/>'
    for x in (560, 700):                                           # arcade
        s += (f'<path d="M {x} {B - 18} L {x} 700 Q {x + 55} 600, {x + 110} 700 L {x + 110} {B - 18} Z" fill="#7a5640" stroke="#6a4a34" stroke-width="5"/>'
              f'<path d="M {x + 10} {B - 18} L {x + 10} 710 Q {x + 55} 630, {x + 100} 710" fill="none" stroke="#e8c8a0" stroke-width="5" opacity="0.7"/>')
    s += (f'<rect x="860" y="640" width="200" height="{B - 640}" fill="#b08664" stroke="#7a5638" stroke-width="5"/>'      # palace door (right)
          f'<path d="M 890 {B} L 890 790 Q 960 700, 1030 790 L 1030 {B} Z" fill="#2a1a12" stroke="#6a4a30" stroke-width="8"/>')
    for fx in (140, 410):                                          # black flags on the gate tower
        s += (f'<rect x="{fx - 4}" y="80" width="8" height="134" fill="#2a1a12"/>'
              f'<path d="M {fx + 4} 86 L {fx + 120} 98 L {fx + 112} 150 L {fx + 120} 202 L {fx + 4} 190 Z" fill="#141216" stroke="#060406" stroke-width="2"/>')
    for bx, by, h in [(630, 440, 170), (990, 440, 170)]:     # black banners hanging on the walls
        s += (f'<rect x="{bx - 46}" y="{by - 8}" width="92" height="10" rx="4" fill="#2a1a12"/>'
              f'<path d="M {bx - 40} {by} L {bx + 40} {by} L {bx + 40} {by + h} L {bx} {by + h - 34} L {bx - 40} {by + h} Z" fill="#141216" stroke="#060406" stroke-width="2"/>'
              f'<path d="M {bx - 32} {by + 22} L {bx + 32} {by + 22}" stroke="#c9a24a" stroke-width="5" opacity="0.8"/>')
    s += f'<rect x="0" y="{B}" width="1080" height="{H - B}" fill="url(#pave)"/>'
    for k in range(12):
        y = B + k * k * 6 + k * 12
        s += f'<path d="M 0 {y} L 1080 {y}" stroke="#5a4434" stroke-width="{2 + k * 0.4:.1f}" opacity="0.5"/>'
    for k in range(-9, 10):
        s += f'<path d="M {540 + k * 60} {B} L {540 + k * 230} 1920" stroke="#5a4434" stroke-width="2.5" opacity="0.45"/>'
    s += f'<rect x="0" y="{B}" width="1080" height="60" fill="#000" opacity="0.12" filter="url(#b12)"/>'
    return svg_render(s)

def bare_tree(x, y, h, seed=0, col="#2a2026"):
    """a leafless winter tree (base at x, y)"""
    r = random.Random(seed)
    s = f'<path d="M {x - h * 0.04:.0f} {y} L {x - h * 0.02:.0f} {y - h * 0.55:.0f} L {x + h * 0.02:.0f} {y - h * 0.55:.0f} L {x + h * 0.04:.0f} {y} Z" fill="{col}"/>'
    def br(x0, y0, ang, L, w, d):
        nonlocal s
        if d == 0 or L < 8:
            return
        x1 = x0 + math.sin(math.radians(ang)) * L; y1 = y0 - math.cos(math.radians(ang)) * L
        s += f'<path d="M {x0:.0f} {y0:.0f} L {x1:.0f} {y1:.0f}" stroke="{col}" stroke-width="{w:.1f}" stroke-linecap="round"/>'
        for da in (-28 - r.uniform(0, 14), 24 + r.uniform(0, 14)):
            br(x1, y1, ang + da, L * r.uniform(0.62, 0.74), w * 0.62, d - 1)
    br(x, y - h * 0.5, -6, h * 0.3, h * 0.05, 5)
    return s

def winter_road():
    """January 838: a road across a snowy plain under a grey sky (road band at y 1030-1110, riders' feet at about y 1080), far snowy mountains,
    bare trees; snow drifts in the foreground from y 1350"""
    s = ("<defs>" + FILTERS + lg("sky", [(0, "#6e7888", 1), (0.45, "#b6bec8", 1), (0.62, "#e2e6ec", 1)]) + lg("sn", [(0, "#eef2f8", 1), (1, "#c2cad8", 1)]) + "</defs>")
    s += f'<rect width="{W}" height="{H}" fill="url(#sky)"/>'
    s += f'<path d="{ridge(W, 800, 300, 731, rough=0.6)}" fill="#cdd4de"/><path d="{ridge(W, 800, 300, 731, rough=0.6)}" fill="#7a8498" opacity="0.3" transform="translate(26,0)"/>'
    s += f'<path d="{ridge(W, 930, 110, 732, rough=0.4)}" fill="#e2e6ee"/>'
    s += f'<rect x="0" y="780" width="{W}" height="260" fill="#ffffff" opacity="0.35" filter="url(#b40)"/>'
    s += '<path d="M -40 980 C 300 960, 800 970, 1120 985 L 1120 2000 L -40 2000 Z" fill="url(#sn)"/>'
    for x, y, h in [(90, 1000, 260), (300, 985, 170), (860, 990, 210), (1010, 1000, 300)]:
        s += bare_tree(x, y, h, seed=733 + x)
    s += '<path d="M -40 1040 C 300 1025, 800 1030, 1120 1045 L 1120 1112 C 800 1100, 300 1098, -40 1115 Z" fill="#c6c0bc"/>'
    s += '<path d="M -40 1060 C 300 1048, 800 1052, 1120 1066 M -40 1092 C 300 1082, 800 1086, 1120 1098" stroke="#a49c98" stroke-width="5" fill="none" opacity="0.6"/>'
    r = random.Random(734)
    for k in range(50):
        x = r.uniform(-20, 1100); y = r.uniform(1040, 1110)
        s += f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{r.uniform(5, 10):.0f}" ry="{r.uniform(2, 4):.0f}" fill="#8a8480" opacity="0.5"/>'
    s += '<path d="M -40 1380 C 200 1340, 420 1370, 640 1345 C 820 1325, 980 1350, 1120 1340 L 1120 2000 L -40 2000 Z" fill="#f4f6fa"/>'
    s += '<path d="M -40 1380 C 200 1340, 420 1370, 640 1345 C 820 1325, 980 1350, 1120 1340" stroke="#ffffff" stroke-width="8" fill="none"/>'
    s += '<path d="M -40 1640 C 260 1600, 600 1630, 1120 1610 L 1120 2000 L -40 2000 Z" fill="#e4e8f0"/>'
    return svg_render(s)

# ------------------------------------------------------------------ PART 8 (Babak, episode 4 half 2): the courtyard, after, today
def court_dusk():
    """Samarra, the caliph's great courtyard at dusk (838): the back wall with an arcade; in the middle a raised seat under a black canopy
    (seat cushion top y 852, x 432-648; platform y 900; steps down to the ground at y 1080, x 300-780); black banners at x 250 and 830;
    torch brackets at (170, 720) and (910, 720) (the scene draws the flames); paved ground from y 1080 (people stand at y 1100-1450)"""
    B = 1080
    s = ("<defs>" + FILTERS + lg("sky", [(0, "#14122a", 1), (0.1, "#2a2246", 1), (0.19, "#6a3a58", 1), (0.25, "#c0645a", 1), (0.3, "#ee9a62", 1)]) +
         lg("wl", [(0, "#7a5038", 1), (1, "#4a2e20", 1)]) + lg("pave", [(0, "#6e4c36", 1), (0.5, "#4a3224", 1), (1, "#22160e", 1)]) +
         rg("tl", 170, 720, 560, [(0, "#ffb060", 0.42), (0.45, "#c0602a", 0.14), (1, "#000", 0)]) +
         rg("tr", 910, 720, 560, [(0, "#ffb060", 0.42), (0.45, "#c0602a", 0.14), (1, "#000", 0)]) +
         lg("cnp", [(0, "#1e1c24", 1), (1, "#0c0b10", 1)]) + "</defs>")
    s += f'<rect width="{W}" height="{H}" fill="url(#sky)"/>' + stars(801, 40, 300) + clouds(W, 802, [330, 420], "#d87a6a", "#f0a87a", 0.4)
    for px, ph in [(90, 300), (330, 250), (760, 280), (1000, 330)]:            # palms behind the wall
        s += f'<path d="M {px} 440 C {px - 10} {440 - ph * 0.5}, {px + 10} {440 - ph * 0.8}, {px} {440 - ph}" stroke="#1e1420" stroke-width="14" fill="none"/>'
        for a in range(0, 360, 40):
            ang = math.radians(a); L = 100
            s += f'<path d="M {px} {440 - ph} q {math.cos(ang) * L * 0.5:.0f} {math.sin(ang) * L * 0.3 - 26:.0f} {math.cos(ang) * L:.0f} {math.sin(ang) * L * 0.5 + 18:.0f}" stroke="#1e1420" stroke-width="13" fill="none" stroke-linecap="round"/>'
    s += f'<rect x="0" y="400" width="{W}" height="{B - 400}" fill="url(#wl)"/>' + "".join(f'<rect x="{i * 54}" y="372" width="34" height="32" fill="#6a442e"/>' for i in range(21))
    s += f'<path d="M 0 440 L {W} 440" stroke="#3a2418" stroke-width="6"/><path d="M 0 {B - 16} L {W} {B - 16}" stroke="#3a2418" stroke-width="10"/>'
    for x in (30, 180, 760, 910):                                            # the arcade
        s += (f'<path d="M {x} {B - 16} L {x} 800 Q {x + 70} 700, {x + 140} 800 L {x + 140} {B - 16} Z" fill="#1c100a" stroke="#3a2418" stroke-width="5"/>'
              f'<path d="M {x + 10} {B - 16} L {x + 10} 810 Q {x + 70} 722, {x + 130} 810" fill="none" stroke="#c89a6a" stroke-width="4" opacity="0.45"/>')
    for bx in (250, 830):                                                   # black banners on the wall
        s += (f'<rect x="{bx - 56}" y="436" width="112" height="12" rx="5" fill="#2a1a12"/>'
              f'<path d="M {bx - 48} 446 L {bx + 48} 446 L {bx + 48} 700 L {bx} 662 L {bx - 48} 700 Z" fill="#121216" stroke="#060406" stroke-width="2"/>'
              f'<path d="M {bx - 40} 476 L {bx + 40} 476 M {bx - 40} 640 L {bx + 40} 640" stroke="#c9a24a" stroke-width="5" opacity="0.8"/>')
    for tx in (170, 910):                                                   # torch brackets
        s += (f'<path d="M {tx - 14} 724 L {tx + 14} 724 L {tx + 8} 790 L {tx - 8} 790 Z" fill="#2a2024" stroke="#0e0a0c" stroke-width="3"/>'
              f'<path d="M {tx} 790 L {tx} 830 M {tx - 22} 830 L {tx + 22} 830" stroke="#2a2024" stroke-width="8"/>')
    # the raised seat: steps, platform, cushion and back, under a black canopy on four poles
    for k, (x0, x1, y0) in enumerate([(300, 780, 1030), (340, 740, 980), (380, 700, 930)]):
        s += (f'<rect x="{x0}" y="{y0}" width="{x1 - x0}" height="50" fill="#{0x7a - 10 * k:02x}{0x58 - 7 * k:02x}{0x40 - 5 * k:02x}" stroke="#2a180e" stroke-width="3"/>'
              f'<rect x="{x0}" y="{y0}" width="{x1 - x0}" height="8" fill="#c8a070" opacity="0.35"/>')
    s += '<rect x="400" y="900" width="280" height="32" fill="#3a2418" stroke="#1a0e08" stroke-width="3"/>'
    s += ('<rect x="440" y="690" width="200" height="170" rx="10" fill="#121216" stroke="#c9a24a" stroke-width="6"/>'
          '<rect x="430" y="850" width="220" height="52" rx="12" fill="#5a1418" stroke="#1a0606" stroke-width="3"/>'
          '<path d="M 434 862 L 646 862" stroke="#c9a24a" stroke-width="5"/>')
    for px in (395, 685):
        s += f'<rect x="{px - 7}" y="500" width="14" height="430" fill="#2a1a12" stroke="#120a06" stroke-width="2"/><circle cx="{px}" cy="496" r="12" fill="#c9a24a"/>'
    s += '<path d="M 368 520 L 540 452 L 712 520 L 712 548 L 368 548 Z" fill="url(#cnp)" stroke="#060406" stroke-width="3"/>'
    s += "".join(f'<path d="M {x} 548 q 13 26 26 0" fill="#121216" stroke="#c9a24a" stroke-width="3"/>' for x in range(368, 712, 26))
    s += '<path d="M 368 548 L 712 548" stroke="#c9a24a" stroke-width="6"/>'
    s += f'<rect x="0" y="{B}" width="{W}" height="{H - B}" fill="url(#pave)"/>'
    for k in range(12):
        y = B + k * k * 6 + k * 12
        s += f'<path d="M 0 {y} L {W} {y}" stroke="#2a1a12" stroke-width="{2 + k * 0.4:.1f}" opacity="0.5"/>'
    for k in range(-9, 10):
        s += f'<path d="M {540 + k * 60} {B} L {540 + k * 230} 1920" stroke="#2a1a12" stroke-width="2.5" opacity="0.45"/>'
    s += f'<rect width="{W}" height="{H}" fill="url(#tl)"/><rect width="{W}" height="{H}" fill="url(#tr)"/>'
    s += f'<rect x="0" y="{B}" width="{W}" height="60" fill="#000" opacity="0.18" filter="url(#b12)"/>'
    return svg_render(s)

def shadow_wall():
    """a plastered wall of the courtyard, lit by a torch at the right (the scene throws shadows on it, x 150-900, y 300-1500); ground from y 1560"""
    s = ("<defs>" + FILTERS + lg("wl", [(0, "#8a6244", 1), (1, "#5a3c28", 1)]) +
         rg("tl", 1000, 820, 1150, [(0, "#ffc070", 0.5), (0.4, "#d07a3a", 0.2), (1, "#000", 0)]) + "</defs>")
    s += f'<rect width="{W}" height="{H}" fill="url(#wl)"/>'
    r = random.Random(811)
    for row in range(14):
        y = 150 + row * 105
        s += f'<path d="M 0 {y} L {W} {y}" stroke="#4a3020" stroke-width="3" opacity="0.35"/>'
        off = (row % 2) * 90
        for x in range(-90 + off, W, 180):
            s += f'<path d="M {x} {y} L {x} {y + 105}" stroke="#4a3020" stroke-width="3" opacity="0.3"/>'
    for _ in range(30):
        x = r.uniform(0, W); y = r.uniform(150, 1550)
        s += f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{r.uniform(20, 70):.0f}" ry="{r.uniform(8, 20):.0f}" fill="#3a2418" opacity="0.12"/>'
    s += '<rect x="0" y="0" width="110" height="1560" fill="#2a1a10" opacity="0.7"/><rect x="104" y="0" width="12" height="1560" fill="#c89a6a" opacity="0.25"/>'
    s += f'<rect x="0" y="1560" width="{W}" height="{H - 1560}" fill="#24160e"/><path d="M 0 1560 L {W} 1560" stroke="#120a06" stroke-width="8"/>'
    s += f'<rect width="{W}" height="{H}" fill="url(#tl)"/>'
    return svg_render(s)

def samarra_dawn():
    """the plain outside Samarra at dawn (838): a grey-rose sky, the city far away on the horizon (y 1010), a bare hill on the right with
    a tall wooden post on top (x 760, from y 905 up to 470); bare ground in front"""
    s = ("<defs>" + FILTERS + lg("sky", [(0, "#3e4058", 1), (0.25, "#76708a", 1), (0.42, "#c8a0a0", 1), (0.53, "#ecc0a2", 1)]) +
         lg("hl", [(0, "#4a3a3c", 1), (1, "#241a1c", 1)]) + lg("gr", [(0, "#6a5a56", 1), (1, "#2e2422", 1)]) + "</defs>")
    s += f'<rect width="{W}" height="{H}" fill="url(#sky)"/>' + clouds(W, 821, [420, 560, 700, 820], "#a88a96", "#d8b4b0", 0.5)
    s += '<circle cx="280" cy="1000" r="150" fill="#ffe0c8" opacity="0.35" filter="url(#b40)"/><circle cx="280" cy="1000" r="40" fill="#fff0e0" opacity="0.6"/>'
    r = random.Random(822)
    x = -20; far = ""
    while x < W:
        w = r.uniform(50, 120); h = r.uniform(30, 90)
        far += f'<rect x="{x:.0f}" y="{1010 - h:.0f}" width="{w:.0f}" height="{h + 60:.0f}" fill="#6a5a6e"/>'
        if r.random() < 0.3:
            far += f'<path d="M {x + w * 0.2:.0f} {1010 - h:.0f} Q {x + w / 2:.0f} {1010 - h - w * 0.6:.0f} {x + w * 0.8:.0f} {1010 - h:.0f} Z" fill="#6a5a6e"/>'
        x += w + r.uniform(-8, 8)
    s += far + '<rect x="0" y="960" width="1080" height="120" fill="#e8c0aa" opacity="0.35" filter="url(#b20)"/>'
    s += '<path d="M -40 1050 C 300 1040, 700 1050, 1120 1040 L 1120 2000 L -40 2000 Z" fill="url(#gr)"/>'
    s += '<path d="M 280 1500 C 420 1250, 600 920, 760 900 C 900 885, 1020 960, 1120 1040 L 1120 2000 L 280 2000 Z" fill="url(#hl)"/>'
    s += '<path d="M 420 1300 C 560 1080, 680 935, 760 916" stroke="#8a7070" stroke-width="5" fill="none" opacity="0.4"/>'
    s += '<path d="M 751 905 L 755 470 L 765 470 L 769 905 Z" fill="#160e10"/><path d="M 748 905 L 772 905 L 776 920 L 744 920 Z" fill="#160e10"/>'
    s += grass_tufts(823, 1100, 1900, 50, "#3a2e2a", "#5a4a42")
    return svg_render(s)

def tigris_dawn():
    """Baghdad on the Tigris at dawn: on the far bank the round city's wall and the green dome (y 860-1000), palms; the wide river
    (y 1000-1480) with the sunlight on the water; reeds on the near bank (from y 1480)"""
    s = ("<defs>" + FILTERS + lg("sky", [(0, "#4a5a7e", 1), (0.3, "#9a98b4", 1), (0.46, "#eab89a", 1), (0.52, "#f8d4ae", 1)]) +
         lg("rv", [(0, "#d8b4a4", 1), (0.4, "#8a8296", 1), (1, "#3a3a50", 1)]) + "</defs>")
    s += f'<rect width="{W}" height="{H}" fill="url(#sky)"/>' + clouds(W, 831, [380, 520, 640], "#c8a0b0", "#f0c8b0", 0.45)
    s += '<circle cx="760" cy="960" r="200" fill="#fff0d0" opacity="0.35" filter="url(#b40)"/><circle cx="760" cy="960" r="46" fill="#fff4e0"/>'
    s += '<rect x="0" y="930" width="1080" height="80" fill="#5e5068"/>' + "".join(f'<rect x="{i * 46}" y="912" width="28" height="22" fill="#5e5068"/>' for i in range(24))
    for x in (120, 300, 860, 1000):
        s += f'<rect x="{x - 22}" y="880" width="44" height="130" fill="#56485e"/>'
    s += ('<rect x="470" y="850" width="140" height="90" fill="#4e4458"/><path d="M 470 850 Q 540 740, 610 850 Z" fill="#3a6a5a"/>'
          '<path d="M 540 742 L 540 712" stroke="#3a6a5a" stroke-width="6"/><circle cx="540" cy="708" r="7" fill="#c9a24a"/>')
    for px, ph in [(60, 210), (200, 170), (390, 190), (700, 160), (950, 200)]:
        s += f'<path d="M {px} 1000 C {px - 8} {1000 - ph * 0.5}, {px + 8} {1000 - ph * 0.8}, {px} {1000 - ph}" stroke="#3a3040" stroke-width="10" fill="none"/>'
        for a in range(0, 360, 45):
            ang = math.radians(a); L = 70
            s += f'<path d="M {px} {1000 - ph} q {math.cos(ang) * L * 0.5:.0f} {math.sin(ang) * L * 0.3 - 18:.0f} {math.cos(ang) * L:.0f} {math.sin(ang) * L * 0.5 + 12:.0f}" stroke="#3a3040" stroke-width="9" fill="none" stroke-linecap="round"/>'
    s += '<path d="M 976 1000 L 978 905 L 984 905 L 986 1000 Z" fill="#2a2030" opacity="0.8"/>'
    s += '<rect x="0" y="1000" width="1080" height="500" fill="url(#rv)"/>'
    r = random.Random(832)
    for k in range(70):
        y = r.uniform(1010, 1480); w = r.uniform(20, 120) * (0.6 + (y - 1000) / 500)
        x = 760 + r.gauss(0, 40 + (y - 1000) * 0.25)
        s += f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{w:.0f}" ry="{2 + (y - 1000) / 160:.1f}" fill="#fff0d0" opacity="{r.uniform(0.25, 0.7):.2f}"/>'
    for k in range(40):
        y = r.uniform(1010, 1480); x = r.uniform(0, W)
        s += f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{r.uniform(30, 90):.0f}" ry="2" fill="#e8d0c8" opacity="0.18"/>'
    s += '<rect x="0" y="990" width="1080" height="40" fill="#f0d8c8" opacity="0.4" filter="url(#b12)"/>'
    s += '<path d="M -40 1500 C 200 1470, 500 1490, 760 1475 C 900 1468, 1020 1480, 1120 1470 L 1120 2000 L -40 2000 Z" fill="#3a3428"/>'
    for k in range(60):
        x = r.uniform(-20, 1100); h = r.uniform(90, 260); lean = r.uniform(-30, 30)
        s += f'<path d="M {x:.0f} {1500 + r.uniform(0, 60):.0f} q {lean * 0.4:.0f} {-h * 0.5:.0f} {lean:.0f} {-h:.0f}" stroke="#2a2a1e" stroke-width="{r.uniform(4, 8):.1f}" fill="none" stroke-linecap="round"/>'
    return svg_render(s)

def tower_night():
    """840: the narrow tower prison at Samarra, at night: a tall round brick tower (x 330-750) with an arched door at its foot (opening x 450-630,
    y 800-1180), torch brackets beside the door at (410, 880) and (670, 880) (the scene draws the flames), the moon; ground from y 1180"""
    G = 1180
    s = ("<defs>" + FILTERS + lg("sky", [(0, "#04060e", 1), (0.5, "#121834", 1), (0.7, "#1e2650", 1)]) +
         lg("tw", [(0, "#241c22", 1), (0.35, "#4a3c40", 1), (0.7, "#5a4a4a", 1), (1, "#2a2024", 1)], vertical=False) +
         rg("tg", 540, 900, 520, [(0, "#ff9a50", 0.35), (0.5, "#a04a20", 0.12), (1, "#000", 0)]) + "</defs>")
    s += f'<rect width="{W}" height="{H}" fill="url(#sky)"/>' + stars(841, 140, 1000)
    s += '<circle cx="880" cy="420" r="160" fill="#c8d0f0" opacity="0.18" filter="url(#b40)"/><circle cx="880" cy="420" r="52" fill="#f2ecd8"/><circle cx="866" cy="408" r="10" fill="#d8d0bc" opacity="0.6"/>'
    s += f'<rect x="0" y="980" width="{W}" height="{G - 980}" fill="#1a1620"/>' + "".join(f'<rect x="{i * 50}" y="962" width="30" height="22" fill="#1a1620"/>' for i in range(22))
    s += f'<rect x="330" y="120" width="420" height="{G - 120}" fill="url(#tw)"/>'
    s += "".join(f'<rect x="{330 + i * 60}" y="86" width="36" height="40" fill="#3a2e34"/>' for i in range(7))
    for row in range(26):
        y = 160 + row * 40
        s += f'<path d="M 330 {y} L 750 {y}" stroke="#1a1216" stroke-width="2.5" opacity="0.45"/>'
        for x in range(330 + (row % 2) * 30, 750, 60):
            s += f'<path d="M {x} {y} L {x} {y + 40}" stroke="#1a1216" stroke-width="2" opacity="0.35"/>'
    s += '<rect x="528" y="300" width="24" height="110" rx="10" fill="#06060a"/><rect x="528" y="560" width="24" height="90" rx="10" fill="#06060a"/>'
    s += f'<path d="M 450 {G} L 450 880 Q 540 780, 630 880 L 630 {G} Z" fill="#060406"/>'
    s += f'<path d="M 436 {G} L 436 878 Q 540 760, 644 878 L 644 {G}" fill="none" stroke="#6a5048" stroke-width="12"/>'
    for tx in (410, 670):
        s += (f'<path d="M {tx - 12} 884 L {tx + 12} 884 L {tx + 7} 940 L {tx - 7} 940 Z" fill="#2a2024" stroke="#0e0a0c" stroke-width="3"/>'
              f'<path d="M {tx} 940 L {tx} 972" stroke="#2a2024" stroke-width="7"/>')
    s += f'<rect x="0" y="{G}" width="{W}" height="{H - G}" fill="#151014"/><path d="M 380 {G} L 700 {G} L 860 1920 L 220 1920 Z" fill="#2a2024" opacity="0.6"/>'
    s += f'<rect width="{W}" height="{H}" fill="url(#tg)"/>'
    return svg_render(s)

def prison_cell():
    """inside the tower prison: a narrow dark room of brick, a high slit window (x 515-545, y 380-560) with a moonbeam falling to the floor;
    floor from y 1300 (a prisoner sits at about x 420-660)"""
    s = ("<defs>" + FILTERS + lg("wl", [(0, "#0c0a10", 1), (1, "#1c161a", 1)]) +
         lg("bm", [(0, "#b8ccf0", 0.22), (1, "#b8ccf0", 0.04)]) + "</defs>")
    s += f'<rect width="{W}" height="{H}" fill="url(#wl)"/>'
    for row in range(30):
        y = 120 + row * 42
        s += f'<path d="M 0 {y} L {W} {y}" stroke="#2a2228" stroke-width="2.5" opacity="0.5"/>'
        for x in range((row % 2) * 40, W, 80):
            s += f'<path d="M {x} {y} L {x} {y + 42}" stroke="#2a2228" stroke-width="2" opacity="0.4"/>'
    s += '<rect x="0" y="0" width="200" height="1300" fill="#000" opacity="0.45" filter="url(#b40)"/><rect x="880" y="0" width="200" height="1300" fill="#000" opacity="0.45" filter="url(#b40)"/>'
    s += '<rect x="508" y="372" width="44" height="196" rx="16" fill="#2a2a34"/><rect x="515" y="380" width="30" height="180" rx="12" fill="#8ea4cc"/>'
    s += '<circle cx="530" cy="470" r="90" fill="#b8ccf0" opacity="0.18" filter="url(#b20)"/>'
    s += '<path d="M 515 560 L 545 560 L 720 1330 L 360 1330 Z" fill="url(#bm)" filter="url(#b12)"/>'
    s += f'<rect x="0" y="1300" width="{W}" height="{H - 1300}" fill="#120e12"/><path d="M 0 1300 L {W} 1300" stroke="#060406" stroke-width="6"/>'
    s += '<ellipse cx="540" cy="1340" rx="200" ry="34" fill="#b8ccf0" opacity="0.10" filter="url(#b12)"/>'
    r = random.Random(851)
    for _ in range(70):
        x = r.uniform(100, 980); y = r.uniform(1310, 1500); a = r.uniform(-0.6, 0.6); L = r.uniform(18, 46)
        s += f'<path d="M {x:.0f} {y:.0f} l {L * math.cos(a):.0f} {L * math.sin(a):.0f}" stroke="#6a5a3a" stroke-width="3" opacity="0.35"/>'
    return svg_render(s)

def bazz_ruins():
    """Babak Castle today, near Kaleybar: the peak of bazz() in the morning sun, its walls in ruins (broken walls, a half tower with an arched
    window, rubble), the old trail; the scene adds the sea of clouds below (cloud_sea) and the wind"""
    s = ("<defs>" + FILTERS + lg("sky", [(0, "#2e5ea8", 1), (0.3, "#86b0da", 1), (0.48, "#f2dcc4", 1), (0.56, "#ffe6c8", 1)]) +
         rg("sun", 860, 1150, 640, [(0, "#fff6dc", 0.95), (0.25, "#ffd8a0", 0.45), (1, "#ffb080", 0)]) + "</defs>")
    s += f'<rect width="{W}" height="{H}" fill="url(#sky)"/>' + clouds(W, 861, [330, 450, 560], "#ffffff", "#ffffff", 0.45) + f'<rect width="{W}" height="{H}" fill="url(#sun)"/>'
    s += '<circle cx="860" cy="1150" r="66" fill="#fff8e6"/>'
    s += f'<path d="{ridge(W, 1280, 200, 81)}" fill="#a8b2c6"/>'
    peak = ("M 120 1920 L 150 1500 L 260 1330 L 330 1200 L 380 1100 L 410 1000 L 440 880 L 470 780 L 780 780 L 820 860 L 870 960 L 940 1040 L 990 1010 "
            "L 1040 1100 L 1100 1250 L 1140 1920 Z")
    face = "M 120 1920 L 150 1500 L 260 1330 L 330 1200 L 380 1100 L 410 1000 L 440 880 L 470 780 L 560 1100 L 610 1500 L 640 1920 Z"
    s += f'<path d="{peak}" fill="#4a4054"/><path d="{face}" fill="#8a7684" opacity="0.8"/>'
    s += '<path d="M 300 1290 L 440 1220 L 380 1150 L 470 1080 L 430 1010 L 490 940 L 455 870 L 480 810 L 520 780" stroke="#e8d8d0" stroke-width="4" fill="none" opacity="0.4"/>'
    ruin = ('<path d="M 476 784 L 476 700 L 492 690 L 500 712 L 516 694 L 530 716 L 530 784 Z" fill="#3e3442"/>'
            '<path d="M 560 784 L 560 616 L 578 600 L 596 622 L 610 596 L 628 640 L 640 632 L 640 784 Z" fill="#463a48"/>'
            '<path d="M 588 784 L 588 700 Q 600 676, 612 700 L 612 784 Z" fill="#1a1420"/><path d="M 590 660 Q 600 640, 610 660 L 610 676 L 590 676 Z" fill="#ffe8c8" opacity="0.8"/>'
            '<path d="M 666 784 L 666 726 L 684 718 L 692 736 L 712 722 L 724 744 L 740 734 L 744 784 Z" fill="#3e3442"/>'
            '<path d="M 752 784 L 752 750 L 770 744 L 776 784 Z" fill="#3e3442"/>')
    s += ruin + '<path d="M 560 616 L 578 600 L 596 622 L 610 596 L 628 640 L 640 632" stroke="#c8a8a0" stroke-width="3" fill="none" opacity="0.7"/>'
    r = random.Random(862)
    for _ in range(26):
        x = r.uniform(470, 790); y = r.uniform(776, 792); w = r.uniform(6, 16)
        s += f'<path d="M {x:.0f} {y:.0f} l {w:.0f} {-w * 0.4:.0f} l {w * 0.6:.0f} {w * 0.5:.0f} Z" fill="#3a3040"/>'
    s += f'<rect x="0" y="1050" width="{W}" height="900" fill="#fff" opacity="0.15" filter="url(#b40)"/>'
    return svg_render(s)
