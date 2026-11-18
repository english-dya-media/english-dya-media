"""Painted backgrounds of Zahhak & Fereydun (SVG -> PNG; cache them with bgs.cached("zh_<name>", zbg.<name>)).
Part 1: Zahhak's throne hall (hook), Mardas's palace on the plain, its gate, the horse yard, a strip of plain for riding,
the palace garden at night / before dawn, the palace wall with Zahhak's window."""
import math, random
from film import svg_render, W, H
from bgs import FILTERS, lg, rg, ridge, clouds, stars, grass_tufts

GOLD, GOLD_D, GOLD_L = "#c9a24a", "#7a5a22", "#f0d48a"


def serpent_emblem(x, y, s=1.0, col=GOLD, dark=GOLD_D):
    """Zahhak's sign: two gold serpents rising on both sides of a disc, heads turned to each other; centre (x, y)"""
    out = f'<g transform="translate({x},{y}) scale({s})">'
    for sd in (-1, 1):
        d = f"M {sd * 10} 70 C {sd * 70} 40, {sd * 70} -10, {sd * 36} -30 C {sd * 10} -46, {sd * 18} -76, {sd * 46} -78"
        out += (f'<path d="{d}" stroke="{dark}" stroke-width="20" fill="none" stroke-linecap="round"/>'
                f'<path d="{d}" stroke="{col}" stroke-width="13" fill="none" stroke-linecap="round"/>'
                f'<path d="M {sd * 40} -90 C {sd * 20} -92, {sd * 8} -80, {sd * 10} -70 C {sd * 18} -64, {sd * 34} -66, {sd * 46} -72 Z" fill="{col}" stroke="{dark}" stroke-width="3"/>'
                f'<circle cx="{sd * 22}" cy="-80" r="3" fill="#a8121c"/>')
    out += (f'<circle cx="0" cy="12" r="20" fill="{col}" stroke="{dark}" stroke-width="4"/><circle cx="0" cy="12" r="8" fill="#a8121c"/>'
            f'<path d="M -60 84 L 60 84" stroke="{col}" stroke-width="6" stroke-linecap="round"/>')
    return out + '</g>'


def palm(x, y, h, col="#2a3a24", lean=0.0, n=9, frond=None):
    """a date palm, base of the trunk at (x, y)"""
    fr = frond or h * 0.36
    tx, ty = x + lean * h, y - h
    out = (f'<path d="M {x - 9} {y} C {x - 6 + lean * h * 0.3:.0f} {y - h * 0.5:.0f}, {tx - 6:.0f} {ty + h * 0.3:.0f}, {tx - 4:.0f} {ty:.0f} '
           f'L {tx + 4:.0f} {ty:.0f} C {tx + 6:.0f} {ty + h * 0.3:.0f}, {x + 6 + lean * h * 0.3:.0f} {y - h * 0.5:.0f}, {x + 9} {y} Z" fill="{col}"/>')
    for k in range(n):
        a = math.radians(-170 + k * (160 / (n - 1)))
        ex, ey = tx + math.cos(a) * fr, ty + math.sin(a) * fr * 0.55 + fr * 0.28
        cx_, cy_ = tx + math.cos(a) * fr * 0.5, ty + math.sin(a) * fr * 0.5 - fr * 0.18
        out += (f'<path d="M {tx:.0f} {ty:.0f} Q {cx_:.0f} {cy_:.0f} {ex:.0f} {ey:.0f}" stroke="{col}" stroke-width="{max(3, fr * 0.09):.1f}" fill="none" stroke-linecap="round"/>')
    return out


def cypress(x, y, h, col="#14241e", dark="#0a1610", rim=None, w=0.13):
    """a slender cypress, base at (x, y); rim: colour of a moonlit right edge"""
    out = (f'<path d="M {x} {y - h:.0f} C {x + h * w:.0f} {y - h * 0.72:.0f}, {x + h * w * 1.05:.0f} {y - h * 0.25:.0f}, {x + h * w * 0.35:.0f} {y - h * 0.04:.0f} '
           f'L {x - h * w * 0.35:.0f} {y - h * 0.04:.0f} C {x - h * w * 1.05:.0f} {y - h * 0.25:.0f}, {x - h * w:.0f} {y - h * 0.72:.0f}, {x} {y - h:.0f} Z" fill="{col}"/>'
           f'<path d="M {x} {y - h:.0f} C {x - h * w:.0f} {y - h * 0.72:.0f}, {x - h * w * 1.05:.0f} {y - h * 0.25:.0f}, {x - h * w * 0.35:.0f} {y - h * 0.04:.0f} L {x} {y - h * 0.06:.0f} Z" fill="{dark}" opacity="0.7"/>'
           f'<rect x="{x - h * 0.012 - 2:.0f}" y="{y - h * 0.06:.0f}" width="{h * 0.024 + 4:.0f}" height="{h * 0.06:.0f}" fill="#20160e"/>')
    if rim:
        out += (f'<path d="M {x + 2} {y - h * 0.97:.0f} C {x + h * w * 0.95:.0f} {y - h * 0.7:.0f}, {x + h * w:.0f} {y - h * 0.3:.0f}, {x + h * w * 0.4:.0f} {y - h * 0.08:.0f}" '
                f'stroke="{rim}" stroke-width="{max(2, h * 0.012):.1f}" fill="none" opacity="0.55"/>')
    return out


# ------------------------------------------------------------------ the hook: Zahhak's hall at night
def hall():
    """Zahhak's throne hall at night: black stone and gold; columns at x 80 and 1000 with torch brackets (flames at about (80, 606) and
    (1000, 606), drawn by the scene); black serpent banners; a raised black throne (cushion top y 990, x 380-700) under a carved alcove;
    steps from y 1180 to the floor at y 1310; people stand at y 1330-1750"""
    s = ("<defs>" + FILTERS + lg("hw", [(0, "#060508", 1), (0.45, "#141118", 1), (1, "#0b090d", 1)]) +
         lg("hf", [(0, "#1c1820", 1), (1, "#040305", 1)]) + lg("cush", [(0, "#8a1420", 1), (1, "#4a0810", 1)]) +
         rg("tl", 80, 600, 560, [(0, "#ffae5a", 0.34), (0.45, "#a0502a", 0.10), (1, "#000", 0)]) +
         rg("tr", 1000, 600, 560, [(0, "#ffae5a", 0.34), (0.45, "#a0502a", 0.10), (1, "#000", 0)]) + "</defs>")
    s += f'<rect width="{W}" height="{H}" fill="url(#hw)"/>'
    for k in range(9):                                                       # stone courses
        y = 240 + k * 120
        s += f'<path d="M 0 {y} L {W} {y}" stroke="#000" stroke-width="3" opacity="0.35"/>'
    s += f'<path d="M 230 1180 L 230 600 Q 540 250, 850 600 L 850 1180 Z" fill="#040306" stroke="{GOLD_D}" stroke-width="8"/>'
    s += f'<path d="M 254 1180 L 254 610 Q 540 290, 826 610 L 826 1180" fill="none" stroke="{GOLD}" stroke-width="3" opacity="0.55"/>'
    s += serpent_emblem(540, 300, 1.25)
    for bx in (180, 900):                                                    # black banners with the gold sign
        s += (f'<rect x="{bx - 46}" y="250" width="92" height="10" rx="4" fill="#2a2018"/>'
              f'<path d="M {bx - 40} 258 L {bx + 40} 258 L {bx + 40} 760 L {bx} 720 L {bx - 40} 760 Z" fill="#0e0d12" stroke="#000" stroke-width="2"/>'
              f'<path d="M {bx - 32} 290 L {bx + 32} 290 M {bx - 32} 690 L {bx + 32} 690" stroke="{GOLD}" stroke-width="4" opacity="0.8"/>' +
              serpent_emblem(bx, 470, 0.42))
    for x in (80, 1000):                                                     # columns and torch brackets
        s += (f'<rect x="{x - 46}" y="150" width="92" height="1160" fill="#15121a" stroke="#020203" stroke-width="3"/>'
              f'<rect x="{x - 46 + (60 if x > 540 else 0)}" y="150" width="32" height="1160" fill="#2e2834" opacity="0.55"/>'
              f'<rect x="{x - 60}" y="130" width="120" height="40" fill="#1e1a22" stroke="{GOLD_D}" stroke-width="3"/>'
              f'<rect x="{x - 60}" y="1280" width="120" height="40" fill="#1e1a22" stroke="{GOLD_D}" stroke-width="3"/>'
              f'<path d="M {x - 46} 420 L {x + 46} 420 M {x - 46} 1020 L {x + 46} 1020" stroke="{GOLD}" stroke-width="6" opacity="0.8"/>'
              f'<path d="M {x - 18} 640 L {x + 18} 640 L {x + 11} 712 L {x - 11} 712 Z" fill="#2a2024" stroke="#0e0a0c" stroke-width="3"/>'
              f'<path d="M {x - 26} 640 L {x + 26} 640" stroke="{GOLD_D}" stroke-width="6"/>')
    for k, (x0, x1, y0) in enumerate([(220, 860, 1270), (260, 820, 1225), (300, 780, 1180)]):   # steps
        s += (f'<rect x="{x0}" y="{y0}" width="{x1 - x0}" height="{50 if k else 42}" fill="#{0x1e - 3 * k:02x}{0x1a - 3 * k:02x}{0x22 - 3 * k:02x}" stroke="#040305" stroke-width="3"/>'
              f'<path d="M {x0} {y0 + 2} L {x1} {y0 + 2}" stroke="{GOLD}" stroke-width="4" opacity="0.75"/>')
    s += (f'<path d="M 400 1000 L 400 720 Q 540 560, 680 720 L 680 1000 Z" fill="#0a090d" stroke="{GOLD}" stroke-width="7"/>'      # throne back
          f'<path d="M 424 990 L 424 730 Q 540 600, 656 730 L 656 990" fill="none" stroke="{GOLD_D}" stroke-width="3"/>' +
          serpent_emblem(540, 690, 0.55) +
          f'<rect x="370" y="1040" width="340" height="140" fill="#0e0c11" stroke="{GOLD_D}" stroke-width="4"/>'
          f'<path d="M 386 1070 L 694 1070 M 386 1150 L 694 1150" stroke="{GOLD}" stroke-width="3" opacity="0.7"/>'
          f'<rect x="380" y="988" width="320" height="58" rx="18" fill="url(#cush)" stroke="#1a0206" stroke-width="3"/>'
          f'<path d="M 392 1000 L 688 1000" stroke="{GOLD}" stroke-width="4" opacity="0.8"/>'
          f'<rect x="352" y="900" width="40" height="150" rx="8" fill="#141118" stroke="{GOLD_D}" stroke-width="3"/>'
          f'<rect x="688" y="900" width="40" height="150" rx="8" fill="#141118" stroke="{GOLD_D}" stroke-width="3"/>'
          f'<circle cx="372" cy="894" r="15" fill="{GOLD}" stroke="#3a2a10" stroke-width="3"/><circle cx="708" cy="894" r="15" fill="{GOLD}" stroke="#3a2a10" stroke-width="3"/>')
    s += f'<rect x="0" y="1310" width="{W}" height="{H - 1310}" fill="url(#hf)"/>'
    for k in range(10):
        y = 1310 + k * k * 7 + k * 14
        s += f'<path d="M 0 {y} L {W} {y}" stroke="#000" stroke-width="{2 + k * 0.4:.1f}" opacity="0.5"/>'
    for k in range(-8, 9):
        s += f'<path d="M {540 + k * 70} 1310 L {540 + k * 240} 1920" stroke="#000" stroke-width="2.5" opacity="0.45"/>'
    s += ('<ellipse cx="80" cy="1500" rx="130" ry="260" fill="#ffae5a" opacity="0.10" filter="url(#b40)"/>'
          '<ellipse cx="1000" cy="1500" rx="130" ry="260" fill="#ffae5a" opacity="0.10" filter="url(#b40)"/>'
          '<ellipse cx="540" cy="1420" rx="300" ry="60" fill="#c9a24a" opacity="0.06" filter="url(#b20)"/>')
    s += f'<rect width="{W}" height="{H}" fill="url(#tl)"/><rect width="{W}" height="{H}" fill="url(#tr)"/>'
    return svg_render(s)


def hall_close():
    """close on the throne: its tall black back with a gold frame and the serpent sign (y 430) fills the frame; torch brackets at the
    edges (flames at about (40, 700) and (1040, 700), drawn by the scene); the king sits with his neck at about (540, 1010)"""
    s = ("<defs>" + FILTERS + lg("hw", [(0, "#07060a", 1), (1, "#110e14", 1)]) +
         rg("tl", 40, 700, 700, [(0, "#ffae5a", 0.42), (0.5, "#a0502a", 0.12), (1, "#000", 0)]) +
         rg("tr", 1040, 700, 700, [(0, "#ffae5a", 0.36), (0.5, "#a0502a", 0.10), (1, "#000", 0)]) + "</defs>")
    s += f'<rect width="{W}" height="{H}" fill="url(#hw)"/>'
    s += f'<path d="M 150 1920 L 150 760 Q 540 250, 930 760 L 930 1920 Z" fill="#09080c" stroke="{GOLD}" stroke-width="12"/>'
    s += f'<path d="M 190 1920 L 190 780 Q 540 320, 890 780 L 890 1920" fill="none" stroke="{GOLD_D}" stroke-width="4"/>'
    s += "".join(f'<circle cx="{x}" cy="{y}" r="6" fill="{GOLD}" opacity="0.8"/>' for x, y in
                 [(150, 900), (150, 1100), (150, 1300), (150, 1500), (930, 900), (930, 1100), (930, 1300), (930, 1500)])
    s += serpent_emblem(540, 440, 1.3)
    for x in (40, 1040):
        s += (f'<path d="M {x - 22} 740 L {x + 22} 740 L {x + 14} 830 L {x - 14} 830 Z" fill="#2a2024" stroke="#0e0a0c" stroke-width="3"/>'
              f'<path d="M {x - 32} 740 L {x + 32} 740" stroke="{GOLD_D}" stroke-width="7"/>')
    s += f'<rect width="{W}" height="{H}" fill="url(#tl)"/><rect width="{W}" height="{H}" fill="url(#tr)"/>'
    return svg_render(s)


# ------------------------------------------------------------------ Mardas's land
def _palace(x0=400, dy=-170):
    """Mardas's palace (white walls, a tiled gate, a dome, a tower), base line y 1192 + dy"""
    s = ""
    for px, ph, lean in [(470, 300, -0.05), (560, 250, 0.04), (700, 230, -0.03), (1000, 320, 0.05), (1060, 260, -0.04)]:
        s += palm(px, 960, ph, col="#5a7448", lean=lean)
    s += ('<path d="M 820 860 Q 900 700, 980 860 Z" fill="#7cb8b6" stroke="#4a7a78" stroke-width="3"/>'
          '<path d="M 846 852 Q 880 760, 914 724" stroke="#d8f0ec" stroke-width="8" fill="none" opacity="0.6"/>'
          '<circle cx="900" cy="704" r="9" fill="#c9a24a"/><rect x="810" y="856" width="180" height="70" fill="#eadfc4" stroke="#8a7050" stroke-width="3"/>')
    s += f'<rect x="{x0}" y="930" width="{W - x0 + 20}" height="262" fill="#ece0c2" stroke="#8a7050" stroke-width="3"/>'
    s += f'<rect x="{x0}" y="930" width="{W - x0 + 20}" height="262" fill="url(#pshade)"/>'
    s += "".join(f'<rect x="{x}" y="912" width="24" height="22" fill="#e2d4b2" stroke="#8a7050" stroke-width="2"/>' for x in range(x0 + 6, W + 20, 46))
    s += ('<rect x="410" y="800" width="84" height="392" fill="#e6d8b8" stroke="#8a7050" stroke-width="3"/>'
          '<rect x="410" y="800" width="26" height="392" fill="#c8b48e" opacity="0.6"/>'
          + "".join(f'<rect x="{x}" y="782" width="18" height="22" fill="#e2d4b2" stroke="#8a7050" stroke-width="2"/>' for x in (412, 444, 474)) +
          '<path d="M 440 880 L 440 850 Q 452 834, 464 850 L 464 880 Z" fill="#3a2a20"/>')
    s += ('<path d="M 590 1192 L 590 1040 Q 680 950, 770 1040 L 770 1192 Z" fill="#2f8a96" stroke="#1e5a62" stroke-width="3"/>'
          '<path d="M 612 1192 L 612 1050 Q 680 984, 748 1050 L 748 1192 Z" fill="#5a4030"/>'
          '<path d="M 612 1192 L 612 1050 Q 680 984, 748 1050" fill="none" stroke="#f0e6cc" stroke-width="3" stroke-dasharray="8 6"/>')
    for wx in (530, 860, 960):
        s += f'<path d="M {wx - 16} 1080 L {wx - 16} 1040 Q {wx} 1018, {wx + 16} 1040 L {wx + 16} 1080 Z" fill="#4a3a2c" stroke="#8a7050" stroke-width="2"/>'
    return f'<g transform="translate(0,{dy})">{s}</g>'


def plain():
    """Mardas's palace on the plain, morning: the palace right of centre (gate opening x 612-748, sill y 1022), palms, far hills;
    the plain from the horizon (y 900); herds at feet y 1000-1100 (far) or 1150-1300 (near), people at y 1350-1750; the sun low at the left"""
    s = ("<defs>" + FILTERS + lg("ps", [(0, "#86aed0", 1), (0.26, "#b8cfdc", 1), (0.44, "#f2e6c8", 1), (0.5, "#f8dcaa", 1)]) +
         lg("pg", [(0, "#e8cf98", 1), (0.35, "#d8b67c", 1), (1, "#a47c48", 1)]) +
         lg("pshade", [(0, "#ffffff", 0.0), (0.6, "#000000", 0.0), (1, "#6a4a2a", 0.25)], vertical=False) +
         rg("sun", 210, 680, 560, [(0, "#fffbe8", 0.95), (0.12, "#ffeec0", 0.6), (1, "#ffe0a0", 0)]) + "</defs>")
    s += f'<rect width="{W}" height="{H}" fill="url(#ps)"/><rect width="{W}" height="{H}" fill="url(#sun)"/>'
    s += '<circle cx="210" cy="680" r="44" fill="#fffaf0"/>'
    s += clouds(W, 31, [330, 420, 520], col="#ffffff", hi="#fff6e0", op=0.45)
    s += f'<path d="{ridge(W, 902, 110, 7, n=30, rough=0.3)}" fill="#b4a2ae" opacity="0.55"/>'
    s += f'<path d="{ridge(W, 910, 60, 12, n=30, rough=0.4)}" fill="#c8b09c" opacity="0.65"/>'
    s += f'<rect x="0" y="880" width="{W}" height="40" fill="#f6e4c0" opacity="0.6" filter="url(#b12)"/>'
    s += f'<rect x="0" y="900" width="{W}" height="{H - 900}" fill="url(#pg)"/>'
    for px, ph, lean in [(60, 230, 0.06), (130, 180, -0.05), (300, 140, 0.03)]:
        s += palm(px, 950, ph, col="#6a7a52", lean=lean)
    s += _palace()
    s += ('<path d="M 612 1022 L 748 1022 C 770 1300, 840 1600, 1000 1920 L 260 1920 C 400 1650, 560 1300, 612 1022 Z" fill="#ecd6a4" opacity="0.65"/>'
          '<path d="M 640 1030 C 600 1350, 480 1650, 380 1920 M 720 1030 C 740 1350, 820 1650, 900 1920" stroke="#c4a06a" stroke-width="5" fill="none" opacity="0.6"/>')
    s += grass_tufts(33, 950, 1900, 52, col="#8a8a4a", hi="#b0a860")
    r = random.Random(34)
    for _ in range(30):
        x = r.uniform(0, W); y = r.uniform(940, 1900); sc = 0.4 + (y - 940) / 800
        s += f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{10 * sc:.1f}" ry="{5 * sc:.1f}" fill="#9a7a50" opacity="0.7"/>'
    return svg_render(s)


def gate():
    """the gate of Mardas's palace, close, morning: a tiled arch (opening x 250-830, apex y 360, ground y 1520) onto a bright inner
    court; a raised stone bench along the wall at the right (top y 1470, x 560-1080, front down to y 1700) with big clay jars at
    x 940 and 1040; the boy and his mother stand at feet y 1700-1760 on the left"""
    s = ("<defs>" + FILTERS + lg("wl", [(0, "#efe4c8", 1), (1, "#d4c09a", 1)]) + lg("court", [(0, "#fdf6e4", 1), (1, "#f2dfb4", 1)]) +
         lg("gr", [(0, "#cfb07c", 1), (1, "#9a7648", 1)]) + lg("bench", [(0, "#d8c8a6", 1), (1, "#a89068", 1)]) + "</defs>")
    s += f'<rect width="{W}" height="{H}" fill="url(#wl)"/>'
    s += '<path d="M 250 1520 L 250 700 Q 540 140, 830 700 L 830 1520 Z" fill="url(#court)"/>'
    for px, ph, lean in [(330, 520, 0.04), (470, 600, -0.03), (690, 560, 0.05), (790, 480, -0.04)]:
        s += f'<g opacity="0.55">{palm(px, 1300, ph, col="#8aa478", lean=lean)}</g>'
    s += ('<path d="M 250 1300 L 830 1300 L 830 1520 L 250 1520 Z" fill="#efe2c2"/>'
          '<path d="M 300 1180 L 300 1300 M 420 1180 L 420 1300 M 660 1180 L 660 1300 M 780 1180 L 780 1300" stroke="#d4c09a" stroke-width="16"/>'
          '<path d="M 280 1180 L 800 1180" stroke="#d8c8a2" stroke-width="12"/>')
    s += ('<path d="M 210 1520 L 210 700 Q 540 70, 870 700 L 870 1520 L 830 1520 L 830 700 Q 540 140, 250 700 L 250 1520 Z" fill="#2f8a96" stroke="#1e5a62" stroke-width="4"/>'
          '<path d="M 230 1520 L 230 700 Q 540 104, 850 700 L 850 1520" fill="none" stroke="#f0e6cc" stroke-width="5" stroke-dasharray="14 10"/>'
          '<path d="M 170 1520 L 170 700 Q 540 0, 910 700 L 910 1520" fill="none" stroke="#b8a478" stroke-width="6"/>')
    s += "".join(f'<circle cx="{540 + 330 * math.cos(math.radians(a)):.0f}" cy="{700 - 600 * math.sin(math.radians(a)):.0f}" r="9" fill="#e8b84e" stroke="#7a5a22" stroke-width="2"/>'
                 for a in range(15, 170, 15))
    for k in range(14):
        y = 300 + k * 92
        s += f'<path d="M 0 {y} L 170 {y} M 910 {y} L {W} {y}" stroke="#c0aa82" stroke-width="2" opacity="0.6"/>'
    s += f'<rect x="0" y="1520" width="{W}" height="{H - 1520}" fill="url(#gr)"/>'
    for k in range(8):
        y = 1520 + k * k * 8 + k * 12
        s += f'<path d="M 0 {y} L {W} {y}" stroke="#8a6a40" stroke-width="2" opacity="0.35"/>'
    s += ('<rect x="560" y="1470" width="540" height="240" fill="url(#bench)" stroke="#6a5436" stroke-width="4"/>'
          '<rect x="550" y="1452" width="560" height="26" rx="6" fill="#e6d8b6" stroke="#6a5436" stroke-width="4"/>'
          '<path d="M 580 1560 L 1080 1560 M 580 1640 L 1080 1640" stroke="#8a7450" stroke-width="2" opacity="0.5"/>')
    for jx, jh in ((940, 300), (1046, 340)):
        s += (f'<path d="M {jx - 56} {1460 - jh} L {jx + 56} {1460 - jh} C {jx + 110} {1460 - jh * 0.7}, {jx + 100} {1460 - jh * 0.1}, {jx + 40} 1460 '
              f'L {jx - 40} 1460 C {jx - 100} {1460 - jh * 0.1}, {jx - 110} {1460 - jh * 0.7}, {jx - 56} {1460 - jh} Z" fill="#b8693c" stroke="#5a2e18" stroke-width="4"/>'
              f'<rect x="{jx - 62}" y="{1448 - jh}" width="124" height="20" rx="6" fill="#9a5230" stroke="#5a2e18" stroke-width="3"/>'
              f'<ellipse cx="{jx}" cy="{1452 - jh}" rx="52" ry="8" fill="#f8f4ea"/>'
              f'<path d="M {jx - 70} {1460 - jh * 0.55} C {jx - 20} {1460 - jh * 0.48}, {jx + 20} {1460 - jh * 0.48}, {jx + 70} {1460 - jh * 0.55}" stroke="#f0dcb0" stroke-width="5" fill="none"/>'
              f'<path d="M {jx - 50} {1460 - jh * 0.85} C {jx - 70} {1460 - jh * 0.6}, {jx - 66} {1460 - jh * 0.3}, {jx - 40} {1460 - jh * 0.12}" stroke="#d88a58" stroke-width="10" fill="none" opacity="0.5"/>')
    s += '<rect x="0" y="1500" width="1080" height="40" fill="#000" opacity="0.12" filter="url(#b12)"/>'
    return svg_render(s)


# ------------------------------------------------------------------ the horse yard and the plain
def yard():
    """Zahhak's horse yard at sunrise: a long stable at the left (posts, reed roof), palms, the sun rising at the right behind the
    palms; a fence across the yard (posts y 1250-1400) with an opening at x 830-970; sand; people and horses stand at y 1520-1760"""
    s = ("<defs>" + FILTERS + lg("ys", [(0, "#8aa0c4", 1), (0.35, "#e8b8a0", 1), (0.55, "#f8d49c", 1), (0.6, "#fbe2b0", 1)]) +
         lg("yg", [(0, "#e6c48c", 1), (0.5, "#cfa46c", 1), (1, "#9c7444", 1)]) +
         rg("ysun", 900, 980, 620, [(0, "#fffbe4", 1), (0.1, "#ffe6a8", 0.7), (1, "#ffcf90", 0)]) + "</defs>")
    s += f'<rect width="{W}" height="{H}" fill="url(#ys)"/><rect width="{W}" height="{H}" fill="url(#ysun)"/>'
    s += '<circle cx="900" cy="990" r="52" fill="#fffaf0"/>'
    s += clouds(W, 41, [520, 640, 760], col="#ffd8c0", hi="#fff0d8", op=0.5)
    s += f'<path d="{ridge(W, 1100, 70, 9, n=30, rough=0.3)}" fill="#c4a0a0" opacity="0.5"/>'
    s += f'<rect x="0" y="1100" width="{W}" height="{H - 1100}" fill="url(#yg)"/>'
    for px, ph, lean in [(700, 430, -0.04), (790, 360, 0.05), (1010, 470, -0.03), (1070, 380, 0.04)]:
        s += palm(px, 1170, ph, col="#4a5a3a", lean=lean)
    s += ('<rect x="-20" y="900" width="650" height="330" fill="#d2a874" stroke="#6a4a2a" stroke-width="3"/>'
          '<rect x="-20" y="900" width="650" height="330" fill="#7a5030" opacity="0.15"/>'
          '<path d="M -40 900 L 660 900 L 690 860 L -40 850 Z" fill="#b89a5c" stroke="#6a4a2a" stroke-width="3"/>'
          + "".join(f'<path d="M {x} 856 L {x - 6} 900" stroke="#8a6a3a" stroke-width="2" opacity="0.7"/>' for x in range(-30, 680, 14)) +
          "".join(f'<rect x="{x}" y="960" width="90" height="270" fill="#3a2418"/><rect x="{x}" y="960" width="90" height="16" fill="#1a100a" opacity="0.6"/>' for x in (30, 230, 430)) +
          "".join(f'<rect x="{x}" y="900" width="18" height="330" fill="#7a5432" stroke="#3a2414" stroke-width="2"/>' for x in (0, 150, 200, 350, 400, 550, 600)))
    for hx in (75, 275, 475):                                                # horse heads in the stalls
        s += (f'<path d="M {hx - 10} 1070 C {hx - 6} 1030, {hx + 20} 1010, {hx + 40} 1020 C {hx + 60} 1040, {hx + 66} 1080, {hx + 48} 1090 '
              f'C {hx + 30} 1090, {hx + 20} 1080, {hx + 12} 1100 L {hx - 10} 1130 Z" fill="#5a3a24" opacity="0.85"/>')
    for x in list(range(-10, 830, 120)) + [970, 1090]:                     # the fence
        s += f'<rect x="{x - 9}" y="1250" width="18" height="150" fill="#7a5432" stroke="#3a2414" stroke-width="2"/>'
    for y in (1282, 1338):
        s += (f'<rect x="-20" y="{y}" width="850" height="14" fill="#8a6440" stroke="#3a2414" stroke-width="2"/>'
              f'<rect x="970" y="{y}" width="130" height="14" fill="#8a6440" stroke="#3a2414" stroke-width="2"/>')
    s += ('<path d="M 30 1690 C 40 1590, 220 1570, 260 1690 Z" fill="#d8b860" stroke="#8a6a2a" stroke-width="3"/>'
          + "".join(f'<path d="M {x} 1690 l {random.Random(x).uniform(-10, 10):.0f} -{random.Random(x + 1).uniform(30, 90):.0f}" stroke="#b89a40" stroke-width="3"/>' for x in range(50, 250, 12)))
    s += grass_tufts(43, 1420, 1880, 18, col="#9a8a4a", hi="#c0aa60")
    r = random.Random(44)
    for _ in range(30):                                                       # hoof prints
        x = r.uniform(0, W); y = r.uniform(1420, 1900); sc = 0.5 + (y - 1400) / 600
        s += f'<path d="M {x - 8 * sc:.0f} {y:.0f} a {8 * sc:.1f} {5 * sc:.1f} 0 1 1 {16 * sc:.1f} 0" stroke="#9a7444" stroke-width="{2 * sc:.1f}" fill="none" opacity="0.6"/>'
    return svg_render(s)


def ride_strip():
    """a long strip of the plain for a tracking shot (3600 x 1920: crop a moving window): morning sky, far hills, palms, scrub;
    the rider's ground at y 1450-1560"""
    WW = 3600
    s = ("<defs>" + FILTERS + lg("rs", [(0, "#7ea8cc", 1), (0.4, "#c4d6de", 1), (0.6, "#f4e2bc", 1)]) +
         lg("rg_", [(0, "#e4c88e", 1), (0.5, "#d0aa70", 1), (1, "#a07848", 1)]) + "</defs>")
    s += f'<rect width="{WW}" height="{H}" fill="url(#rs)"/>'
    s += clouds(WW, 51, [380, 520, 640], col="#ffffff", hi="#fff6e0", op=0.4)
    s += f'<path d="{ridge(WW, 1110, 150, 3, n=60, rough=0.3)}" fill="#b0a0b4" opacity="0.5"/>'
    s += f'<path d="{ridge(WW, 1125, 70, 5, n=70, rough=0.45)}" fill="#c6ae98" opacity="0.7"/>'
    s += f'<rect x="0" y="1110" width="{WW}" height="{H - 1110}" fill="url(#rg_)"/>'
    r = random.Random(52)
    for k in range(16):
        x = r.uniform(0, WW); ph = r.uniform(150, 260)
        s += palm(x, 1160 + r.uniform(0, 30), ph, col="#6a7650", lean=r.uniform(-0.06, 0.06))
    for k in range(40):                                                       # scrub
        x = r.uniform(0, WW); y = r.uniform(1180, 1880); sc = 0.4 + (y - 1180) / 700
        s += f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{36 * sc:.0f}" ry="{14 * sc:.0f}" fill="#8a8648" opacity="0.8"/><ellipse cx="{x - 8 * sc:.0f}" cy="{y - 6 * sc:.0f}" rx="{20 * sc:.0f}" ry="{8 * sc:.0f}" fill="#aaa45a"/>'
    s += grass_tufts(53, 1150, 1900, 120, col="#8a8a4a", hi="#b0a860", w=WW)
    for k in range(60):
        x = r.uniform(0, WW); y = r.uniform(1150, 1900); sc = 0.4 + (y - 1150) / 700
        s += f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{9 * sc:.1f}" ry="{5 * sc:.1f}" fill="#9a7a50" opacity="0.7"/>'
    return svg_render(s, WW, H)


# ------------------------------------------------------------------ the garden at night
def _garden_sky(pal):
    if pal == "night":
        sky = lg("gs", [(0, "#070a1a", 1), (0.3, "#111a34", 1), (0.48, "#22304e", 1)])
        moon = (820, 330, 50, 1.0)
    else:
        sky = lg("gs", [(0, "#0e1428", 1), (0.28, "#24304e", 1), (0.42, "#5a5a7a", 1), (0.5, "#a08ca0", 1)])
        moon = (900, 520, 40, 0.55)
    return sky, moon


def garden(pal="night"):
    """Mardas's garden: the palace behind its garden wall (wall top y 830, base y 1100) with an arched door (x 500-580, y 945-1100) at the
    end of a straight path (x 500-580 at y 1100 widening to x 330-750 at y 1920), cypresses in rows, rose beds, the moon; a lit window
    high in the palace at (300, 690). The pit is dug at (540, 1480). pal "night" | "predawn" """
    sky, (mx, my, mr, ma) = _garden_sky(pal)
    rim = "#9ab4e0" if pal == "night" else "#b8b0d0"
    s = ("<defs>" + FILTERS + sky + lg("gw", [(0, "#2a3048", 1), (1, "#161a2a", 1)]) + lg("gp", [(0, "#4a5068", 1), (1, "#2a2e40", 1)]) +
         lg("gb", [(0, "#101a18", 1), (1, "#060a0a", 1)]) +
         rg("mg", mx, my, 420, [(0, "#dfe8ff", 0.55 * ma), (0.25, "#8aa0d0", 0.18 * ma), (1, "#000", 0)]) + "</defs>")
    s += f'<rect width="{W}" height="{H}" fill="url(#gs)"/><rect width="{W}" height="{H}" fill="url(#mg)"/>'
    s += stars(61, 90 if pal == "night" else 30, 820)
    s += f'<circle cx="{mx}" cy="{my}" r="{mr}" fill="#f4f0e2" opacity="{ma}"/><circle cx="{mx - 12}" cy="{my - 8}" r="{mr * 0.24:.0f}" fill="#d8d2c0" opacity="{0.5 * ma:.2f}"/>'
    if pal != "night":
        s += f'<rect x="0" y="700" width="{W}" height="200" fill="#e0a0a0" opacity="0.18" filter="url(#b40)"/>'
    s += ('<rect x="120" y="560" width="420" height="300" fill="#262a40"/><rect x="120" y="560" width="420" height="300" fill="#000" opacity="0.15"/>'
          + "".join(f'<rect x="{x}" y="540" width="26" height="24" fill="#262a40"/>' for x in range(126, 540, 48)) +
          '<path d="M 640 860 L 640 700 Q 760 560, 880 700 L 880 860 Z" fill="#242840"/><rect x="630" y="840" width="260" height="30" fill="#262a40"/>')
    for wx, lit in ((200, False), (300, True), (400, False)):
        s += f'<path d="M {wx - 22} 740 L {wx - 22} 690 Q {wx} 664, {wx + 22} 690 L {wx + 22} 740 Z" fill="{"#e8a050" if lit else "#0c0e18"}" opacity="{0.85 if lit else 1}"/>'
    s += '<circle cx="300" cy="710" r="70" fill="#ffb060" opacity="0.18" filter="url(#b20)"/>'
    for px, ph, lean in [(80, 380, 0.04), (590, 330, -0.05), (960, 400, 0.04)]:
        s += palm(px, 860, ph, col="#0c1420", lean=lean)
    s += f'<rect x="0" y="830" width="{W}" height="270" fill="url(#gw)"/>'
    s += "".join(f'<rect x="{x}" y="812" width="30" height="22" fill="#2a3048"/>' for x in range(4, W, 54))
    s += f'<path d="M 0 834 L {W} 834" stroke="{rim}" stroke-width="3" opacity="0.35"/>'
    s += ('<path d="M 492 1100 L 492 970 Q 540 920, 588 970 L 588 1100 Z" fill="#3a3248" stroke="#5a5a78" stroke-width="3"/>'
          '<path d="M 500 1100 L 500 974 Q 540 934, 580 974 L 580 1100 Z" fill="#2a1a14"/>'
          '<path d="M 540 940 L 540 1100" stroke="#1a100c" stroke-width="3"/><circle cx="530" cy="1030" r="4" fill="#8a7a50"/><circle cx="550" cy="1030" r="4" fill="#8a7a50"/>')
    s += f'<rect x="0" y="1100" width="{W}" height="{H - 1100}" fill="url(#gb)"/>'
    s += '<path d="M 500 1100 L 580 1100 L 750 1920 L 330 1920 Z" fill="url(#gp)"/>'
    for k in range(14):                                                        # paving joints
        u = (k / 14) ** 1.7; y = 1100 + 820 * u
        xl = 500 - 170 * u; xr = 580 + 170 * u
        s += f'<path d="M {xl:.0f} {y:.0f} L {xr:.0f} {y:.0f}" stroke="#1a1c28" stroke-width="{1.5 + 3 * u:.1f}" opacity="0.6"/>'
    s += f'<path d="M 540 1100 L 540 1920" stroke="#1a1c28" stroke-width="3" opacity="0.4"/>'
    s += f'<path d="M 500 1100 L 330 1920 M 580 1100 L 750 1920" stroke="#5a607a" stroke-width="4" opacity="0.7"/>'
    r = random.Random(62)
    for side in (-1, 1):                                                      # rose beds
        for k in range(46):
            u = r.uniform(0, 1) ** 1.5; y = 1110 + 800 * u
            x = 540 + side * (60 + 190 * u + r.uniform(20, 300) * (0.3 + u))
            sc = 0.4 + 1.6 * u
            s += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{14 * sc:.1f}" fill="#16281e"/>'
            if r.random() < 0.5:
                s += f'<circle cx="{x + 4 * sc:.0f}" cy="{y - 6 * sc:.0f}" r="{4 * sc:.1f}" fill="#7a3a50" opacity="0.8"/>'
    for (x, y, h) in [(330, 1150, 260), (220, 1270, 430), (80, 1470, 720), (750, 1150, 260), (860, 1270, 430), (1000, 1470, 720)]:
        s += cypress(x, y, h, rim=rim)
    s += cypress(-60, 1900, 1180, col="#0a120e", dark="#040806", rim=rim) + cypress(1150, 1900, 1180, col="#0a120e", dark="#040806", rim=rim)
    return svg_render(s)


def garden_close(pal="night"):
    """close on the path near the pit, at night, seen from a little above: the garden wall behind (top y 520, base y 760) under the
    moon; the path from the wall (x 420-660 at y 760) to the bottom (x 60-1020); rose beds and cypresses at both sides.
    The pit is dug at (540, 960); a person standing at it has the feet at about y 975 (scale 0.36)"""
    sky, (mx, my, mr, ma) = _garden_sky(pal)
    rim = "#9ab4e0" if pal == "night" else "#b8b0d0"
    s = ("<defs>" + FILTERS + sky + lg("gw", [(0, "#2a3048", 1), (1, "#161a2a", 1)]) + lg("gp", [(0, "#4a5068", 1), (1, "#242838", 1)]) +
         lg("gb", [(0, "#101a18", 1), (1, "#060a0a", 1)]) +
         rg("mg", 760, 300, 420, [(0, "#dfe8ff", 0.5 * ma), (0.25, "#8aa0d0", 0.16 * ma), (1, "#000", 0)]) + "</defs>")
    s += f'<rect width="{W}" height="{H}" fill="url(#gs)"/><rect width="{W}" height="{H}" fill="url(#mg)"/>'
    s += stars(71, 60, 520)
    s += f'<circle cx="760" cy="300" r="56" fill="#f4f0e2" opacity="{ma}"/><circle cx="746" cy="290" r="13" fill="#d8d2c0" opacity="{0.5 * ma:.2f}"/>'
    for px, ph, lean in [(150, 360, 0.04), (930, 400, -0.04)]:
        s += palm(px, 540, ph, col="#0c1420", lean=lean)
    s += f'<rect x="0" y="520" width="{W}" height="240" fill="url(#gw)"/>'
    s += "".join(f'<rect x="{x}" y="500" width="34" height="24" fill="#2a3048"/>' for x in range(0, W, 60))
    s += f'<path d="M 0 524 L {W} 524" stroke="{rim}" stroke-width="3" opacity="0.3"/>'
    s += f'<rect x="0" y="760" width="{W}" height="{H - 760}" fill="url(#gb)"/>'
    s += '<path d="M 420 760 L 660 760 L 1020 1920 L 60 1920 Z" fill="url(#gp)"/>'
    for k in range(16):
        u = (k / 16) ** 1.5; y = 760 + 1160 * u
        s += f'<path d="M {420 - 360 * u:.0f} {y:.0f} L {660 + 360 * u:.0f} {y:.0f}" stroke="#1a1c28" stroke-width="{2 + 3 * u:.1f}" opacity="0.55"/>'
    s += '<path d="M 420 760 L 60 1920 M 660 760 L 1020 1920" stroke="#5a607a" stroke-width="5" opacity="0.7"/>'
    r = random.Random(72)
    for side in (-1, 1):
        for k in range(46):
            u = r.uniform(0, 1) ** 1.3; y = 770 + 1150 * u
            x = 540 + side * (130 + 360 * u + r.uniform(20, 260))
            sc = 0.5 + 1.6 * u
            s += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{14 * sc:.1f}" fill="#16281e"/>'
            if r.random() < 0.5:
                s += f'<circle cx="{x + 4 * sc:.0f}" cy="{y - 6 * sc:.0f}" r="{4 * sc:.1f}" fill="#7a3a50" opacity="0.8"/>'
    s += cypress(250, 860, 520, rim=rim) + cypress(830, 860, 520, rim=rim)
    s += cypress(40, 1500, 1150, col="#0a120e", dark="#040806", rim=rim) + cypress(1040, 1500, 1150, col="#0a120e", dark="#040806", rim=rim)
    return svg_render(s)


# ------------------------------------------------------------------ Zahhak's window
def window_room():
    """a dark room seen through Zahhak's window: a warm lamp glow at the left, a hanging, a dark doorway"""
    s = ("<defs>" + FILTERS + lg("rm", [(0, "#0c0e18", 1), (1, "#06070c", 1)]) +
         rg("lamp", 230, 760, 520, [(0, "#ffb060", 0.32), (0.5, "#a05a2a", 0.10), (1, "#000", 0)]) + "</defs>")
    s += f'<rect width="{W}" height="{H}" fill="url(#rm)"/>'
    s += ('<rect x="600" y="520" width="260" height="900" fill="#3a1418" opacity="0.65"/>'
          '<path d="M 600 520 L 860 520" stroke="#8a6a2a" stroke-width="8" opacity="0.6"/>'
          + "".join(f'<path d="M {x} 540 L {x} 1410" stroke="#1a0608" stroke-width="5" opacity="0.6"/>' for x in range(630, 860, 50)) +
          '<path d="M 300 1400 L 300 900 Q 380 830, 460 900 L 460 1400 Z" fill="#05060a"/>')
    s += f'<rect width="{W}" height="{H}" fill="url(#lamp)"/>'
    return svg_render(s)


def window_wall(pal="night"):
    """the palace wall in moonlight with an arched window (opening x 300-780, top y 440, sill y 1500), as an fg layer: transparent in
    the opening; jasmine on the left; moonlight from the left. pal "night" | "predawn" """
    top = "#3e4660" if pal == "night" else "#4e5470"
    bot = "#1e2234" if pal == "night" else "#262a3e"
    s = ("<defs>" + FILTERS + lg("ww", [(0, top, 1), (1, bot, 1)]) +
         lg("wlit", [(0, "#a8bce8", 0.35), (0.4, "#a8bce8", 0.0)], vertical=False) + "</defs>")
    hole = "M 300 1500 L 300 700 Q 300 520, 540 440 Q 780 520, 780 700 L 780 1500 Z"
    s += f'<path d="M 0 0 L {W} 0 L {W} {H} L 0 {H} Z {hole}" fill="url(#ww)" fill-rule="evenodd"/>'
    s += f'<path d="M 0 0 L {W} 0 L {W} {H} L 0 {H} Z {hole}" fill="url(#wlit)" fill-rule="evenodd"/>'
    for k in range(16):                                                        # plaster joints
        y = 80 + k * 120
        s += f'<path d="M 0 {y} L 250 {y} M 830 {y} L {W} {y}" stroke="#141826" stroke-width="2" opacity="0.5"/>'
    s += (f'<path d="M 270 1530 L 270 700 Q 270 490, 540 400 Q 810 490, 810 700 L 810 1530" fill="none" stroke="#5a6488" stroke-width="22"/>'
          f'<path d="M 286 1520 L 286 700 Q 286 506, 540 420 Q 794 506, 794 700 L 794 1520" fill="none" stroke="#1a1e2c" stroke-width="6"/>'
          f'<path d="M 256 1500 L 824 1500 L 846 1560 L 234 1560 Z" fill="#5a6280" stroke="#1a1e2c" stroke-width="4"/>'
          f'<path d="M 234 1560 L 846 1560 L 846 1590 L 234 1590 Z" fill="#2a2e44"/>')
    r = random.Random(81)
    vine = "M 120 1920 C 160 1700, 90 1500, 170 1300 C 230 1150, 160 950, 230 800 C 260 720, 250 640, 290 600"
    s += f'<path d="{vine}" stroke="#1a2a1e" stroke-width="10" fill="none"/>'
    for k in range(70):
        u = r.uniform(0, 1); y = 1920 - 1320 * u; x = 150 + 60 * math.sin(u * 9) + r.uniform(-60, 60) + 120 * u
        s += f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="16" ry="9" fill="#1e3424" transform="rotate({r.uniform(-60, 60):.0f},{x:.0f},{y:.0f})"/>'
        if r.random() < 0.35:
            s += "".join(f'<circle cx="{x + 7 * math.cos(a):.0f}" cy="{y + 7 * math.sin(a):.0f}" r="4" fill="#e8e8f4" opacity="0.85"/>' for a in (0, 1.26, 2.51, 3.77, 5.03))
    return svg_render(s)


# ------------------------------------------------------------------ part 2: Mardas's (now Zahhak's) palace by day, the kitchen, the table
def _tiles(x0, y0, x1, y1, step, col="#2f8a96", col2="#f0e6cc"):
    s = f'<rect x="{x0}" y="{y0}" width="{x1 - x0}" height="{y1 - y0}" fill="{col}"/>'
    for x in range(x0, x1, step):
        for y in range(y0, y1, step):
            cx, cy = x + step / 2, y + step / 2
            s += f'<path d="M {cx} {cy - step * 0.38} L {cx + step * 0.38} {cy} L {cx} {cy + step * 0.38} L {cx - step * 0.38} {cy} Z" fill="{col2}" opacity="0.85"/>'
    return s


def palace_hall():
    """the palace's throne hall by day (Mardas's, then Zahhak's): white walls, turquoise tile bands, arched alcoves, sunbeams from high
    windows, brass lamps; a white and gold throne (cushion top y 990, x 380-700) on three marble steps (y 1180-1310); a red carpet;
    courtiers stand at y 1330-1750"""
    s = ("<defs>" + FILTERS + lg("pw", [(0, "#e8dcc4", 1), (1, "#d6c6a6", 1)]) + lg("pf", [(0, "#c8b494", 1), (1, "#8a7050", 1)]) +
         lg("beam", [(0, "#fff6dc", 0.45), (1, "#fff6dc", 0.0)]) + lg("cush", [(0, "#b8242c", 1), (1, "#7a1218", 1)]) + "</defs>")
    s += f'<rect width="{W}" height="{H}" fill="url(#pw)"/>'
    s += _tiles(0, 1140, W, 1180, 40)
    for ax in (40, 820):                                                     # alcoves
        s += (f'<path d="M {ax} 1140 L {ax} 700 Q {ax + 110} 540, {ax + 220} 700 L {ax + 220} 1140 Z" fill="#cbb896" stroke="#2f8a96" stroke-width="10"/>'
              f'<path d="M {ax + 20} 1140 L {ax + 20} 710 Q {ax + 110} 580, {ax + 200} 710 L {ax + 200} 1140" fill="none" stroke="#f0e6cc" stroke-width="3" stroke-dasharray="10 8"/>'
              f'<path d="M {ax + 60} 980 C {ax + 60} 900, {ax + 160} 900, {ax + 160} 980 L {ax + 150} 1060 L {ax + 70} 1060 Z" fill="#b8693c" stroke="#5a2e18" stroke-width="3"/>')
    for wx in (300, 780):                                                    # high windows and their beams
        s += (f'<path d="M {wx - 40} 420 L {wx - 40} 300 Q {wx} 250, {wx + 40} 300 L {wx + 40} 420 Z" fill="#fff6dc" stroke="#2f8a96" stroke-width="6"/>'
              f'<path d="M {wx - 40} 420 L {wx + 40} 420 L {wx + 260} 1500 L {wx + 60} 1500 Z" fill="url(#beam)" opacity="0.8"/>')
    s += f'<path d="M 360 1180 L 360 640 Q 540 470, 720 640 L 720 1180 Z" fill="#dccaa6" stroke="#2f8a96" stroke-width="10"/>'
    s += f'<path d="M 384 1180 L 384 650 Q 540 505, 696 650 L 696 1180" fill="none" stroke="#c9a24a" stroke-width="4"/>'
    for k, (x0, x1, y0) in enumerate([(220, 860, 1270), (260, 820, 1225), (300, 780, 1180)]):
        s += (f'<rect x="{x0}" y="{y0}" width="{x1 - x0}" height="{50 if k else 42}" fill="#{0xf2 - 8 * k:02x}{0xec - 8 * k:02x}{0xe0 - 8 * k:02x}" stroke="#a8987a" stroke-width="3"/>'
              f'<path d="M {x0} {y0 + 2} L {x1} {y0 + 2}" stroke="#c9a24a" stroke-width="4" opacity="0.8"/>')
    s += (f'<path d="M 400 1000 L 400 740 Q 540 600, 680 740 L 680 1000 Z" fill="#f4ecdc" stroke="#c9a24a" stroke-width="8"/>'
          f'<path d="M 424 990 L 424 750 Q 540 640, 656 750 L 656 990" fill="none" stroke="#2f8a96" stroke-width="5"/>'
          + "".join(f'<path d="M 540 720 L {540 + 34 * math.cos(math.radians(a)):.0f} {720 + 34 * math.sin(math.radians(a)):.0f}" stroke="#c9a24a" stroke-width="6"/>' for a in range(0, 360, 30)) +
          f'<circle cx="540" cy="720" r="16" fill="#c9a24a" stroke="#7a5a22" stroke-width="3"/>'
          f'<rect x="370" y="1040" width="340" height="140" fill="#efe6d4" stroke="#c9a24a" stroke-width="4"/>'
          f'<path d="M 386 1070 L 694 1070 M 386 1150 L 694 1150" stroke="#2f8a96" stroke-width="4" opacity="0.8"/>'
          f'<rect x="380" y="988" width="320" height="58" rx="18" fill="url(#cush)" stroke="#4a0a10" stroke-width="3"/>'
          f'<path d="M 392 1000 L 688 1000" stroke="#c9a24a" stroke-width="4" opacity="0.8"/>'
          f'<rect x="352" y="900" width="40" height="150" rx="8" fill="#efe6d4" stroke="#c9a24a" stroke-width="3"/>'
          f'<rect x="688" y="900" width="40" height="150" rx="8" fill="#efe6d4" stroke="#c9a24a" stroke-width="3"/>'
          f'<circle cx="372" cy="894" r="15" fill="#c9a24a" stroke="#7a5a22" stroke-width="3"/><circle cx="708" cy="894" r="15" fill="#c9a24a" stroke="#7a5a22" stroke-width="3"/>')
    for lx in (170, 910):
        s += (f'<path d="M {lx} 0 L {lx} 520" stroke="#7a5a30" stroke-width="3"/>'
              f'<path d="M {lx - 40} 520 L {lx + 40} 520 L {lx + 26} 560 L {lx - 26} 560 Z" fill="#b9832f" stroke="#5a3a14" stroke-width="3"/>'
              f'<circle cx="{lx}" cy="540" r="60" fill="#ffd890" opacity="0.25" filter="url(#b12)"/>')
    s += f'<rect x="0" y="1310" width="{W}" height="{H - 1310}" fill="url(#pf)"/>'
    for k in range(10):
        y = 1310 + k * k * 7 + k * 14
        s += f'<path d="M 0 {y} L {W} {y}" stroke="#6a5438" stroke-width="{2 + k * 0.4:.1f}" opacity="0.4"/>'
    for k in range(-8, 9):
        s += f'<path d="M {540 + k * 70} 1310 L {540 + k * 240} 1920" stroke="#6a5438" stroke-width="2.5" opacity="0.35"/>'
    s += ('<path d="M 440 1310 L 640 1310 L 780 1920 L 300 1920 Z" fill="#a8242c"/>'
          '<path d="M 456 1310 L 624 1310 L 752 1920 L 328 1920 Z" fill="none" stroke="#c9a24a" stroke-width="5"/>')
    return svg_render(s)


def palace_hall_close():
    """close on the white and gold throne: its tall back (rosette at (540, 520)) behind the king, whose neck is at about (540, 1010)"""
    s = ("<defs>" + FILTERS + lg("pw", [(0, "#e8dcc4", 1), (1, "#cdbb98", 1)]) + lg("beam", [(0, "#fff6dc", 0.4), (1, "#fff6dc", 0.0)]) + "</defs>")
    s += f'<rect width="{W}" height="{H}" fill="url(#pw)"/>'
    s += '<path d="M 700 0 L 860 0 L 1180 1920 L 960 1920 Z" fill="url(#beam)" opacity="0.7"/>'
    s += f'<path d="M 150 1920 L 150 760 Q 540 300, 930 760 L 930 1920 Z" fill="#f4ecdc" stroke="#c9a24a" stroke-width="14"/>'
    s += f'<path d="M 190 1920 L 190 780 Q 540 360, 890 780 L 890 1920" fill="none" stroke="#2f8a96" stroke-width="8"/>'
    s += "".join(f'<path d="M 540 520 L {540 + 70 * math.cos(math.radians(a)):.0f} {520 + 70 * math.sin(math.radians(a)):.0f}" stroke="#c9a24a" stroke-width="10"/>' for a in range(0, 360, 30))
    s += '<circle cx="540" cy="520" r="30" fill="#c9a24a" stroke="#7a5a22" stroke-width="4"/>'
    s += "".join(f'<circle cx="{x}" cy="{y}" r="8" fill="#2f8a96" opacity="0.8"/>' for x, y in
                 [(150, 900), (150, 1100), (150, 1300), (150, 1500), (930, 900), (930, 1100), (930, 1300), (930, 1500)])
    return svg_render(s)


def kitchen():
    """the palace kitchen: brick walls, a raised hearth at the left (top y 960, x 80-520) with the fire under it (opening x 150-450,
    y 1000-1160, flames drawn by the scene) and a big copper pot on it (rim y 820, x 200-440); hanging pans and herbs; shelves with jars
    at the right; a window with a beam; a person stands at feet y 1600-1700"""
    s = ("<defs>" + FILTERS + lg("kw", [(0, "#5a3222", 1), (0.35, "#8a5236", 1), (1, "#6a3c26", 1)]) + lg("kf", [(0, "#7a5034", 1), (1, "#3a2416", 1)]) +
         rg("fire", 300, 1080, 620, [(0, "#ffb060", 0.45), (0.5, "#c0602a", 0.12), (1, "#000", 0)]) +
         lg("beam", [(0, "#fff0c8", 0.4), (1, "#fff0c8", 0.0)]) + "</defs>")
    s += f'<rect width="{W}" height="{H}" fill="url(#kw)"/>'
    r = random.Random(91)
    for row in range(26):
        y = row * 60
        for col in range(10):
            x = col * 120 + (60 if row % 2 else 0) - 60
            s += f'<rect x="{x + 3}" y="{y + 3}" width="114" height="54" fill="#{r.randint(0x82, 0x9a):02x}{r.randint(0x4a, 0x58):02x}{r.randint(0x30, 0x3a):02x}" opacity="0.45"/>'
    s += f'<rect x="0" y="0" width="{W}" height="380" fill="#1a0e08" opacity="0.35" filter="url(#b40)"/>'
    s += ('<path d="M 760 560 L 760 380 Q 860 300, 960 380 L 960 560 Z" fill="#ffefc8" stroke="#3a2416" stroke-width="8"/>'
          '<path d="M 860 380 L 860 560 M 760 470 L 960 470" stroke="#3a2416" stroke-width="6"/>'
          '<path d="M 760 560 L 960 560 L 620 1500 L 420 1500 Z" fill="url(#beam)" opacity="0.7"/>')
    for k, y in enumerate((760, 960)):                                     # shelves with jars
        s += f'<rect x="700" y="{y}" width="360" height="18" fill="#5a3a22" stroke="#2a180e" stroke-width="3"/>'
        for j in range(4):
            jx = 730 + j * 85 + (20 if k else 0); jh = 70 + 20 * ((j + k) % 2)
            s += (f'<path d="M {jx} {y} C {jx - 26} {y - jh * 0.3}, {jx - 22} {y - jh}, {jx + 4} {y - jh} L {jx + 26} {y - jh} C {jx + 52} {y - jh}, {jx + 56} {y - jh * 0.3}, {jx + 30} {y} Z" '
                  f'fill="{["#b8693c", "#2f7a86", "#c9a24a", "#8a4a2a"][(j + k) % 4]}" stroke="#2a180e" stroke-width="3"/>')
    for k, (px, py) in enumerate([(160, 420), (300, 460), (440, 410)]):    # hanging copper pans
        s += (f'<path d="M {px} 0 L {px} {py - 40}" stroke="#2a180e" stroke-width="3"/>'
              f'<circle cx="{px}" cy="{py}" r="48" fill="#c0703a" stroke="#4a2410" stroke-width="4"/><circle cx="{px - 12}" cy="{py - 12}" r="16" fill="#f0a868" opacity="0.6"/>'
              f'<path d="M {px} {py - 48} L {px} {py - 90}" stroke="#4a2410" stroke-width="10"/>')
    for hx in (600, 660):                                                   # herbs and garlic
        s += f'<path d="M {hx} 0 L {hx} 300" stroke="#2a180e" stroke-width="2"/>'
        s += "".join(f'<ellipse cx="{hx + 10 * math.sin(i)}" cy="{300 + 18 * i}" rx="12" ry="9" fill="{"#e8e0cc" if hx == 660 else "#5a7a3a"}" stroke="#2a180e" stroke-width="2"/>' for i in range(5))
    s += ('<rect x="60" y="960" width="480" height="560" fill="#7a4428" stroke="#2a180e" stroke-width="4"/>'
          '<rect x="50" y="944" width="500" height="30" rx="6" fill="#9a5a34" stroke="#2a180e" stroke-width="4"/>'
          '<path d="M 150 1180 L 150 1060 Q 300 960, 450 1060 L 450 1180 Z" fill="#1a0a04" stroke="#2a180e" stroke-width="4"/>')
    for row in range(9):
        y = 990 + row * 60
        s += f'<path d="M 60 {y} L 540 {y}" stroke="#4a2416" stroke-width="3" opacity="0.6"/>'
    s += ('<path d="M 190 840 C 180 930, 210 960, 320 960 C 430 960, 460 930, 450 840 Z" fill="#b8682e" stroke="#3a1a08" stroke-width="5"/>'
          '<ellipse cx="320" cy="840" rx="132" ry="24" fill="#8a4a1e" stroke="#3a1a08" stroke-width="5"/>'
          '<ellipse cx="320" cy="842" rx="112" ry="16" fill="#c8862e"/>'
          '<path d="M 230 880 C 250 920, 290 930, 330 930" stroke="#f0a868" stroke-width="8" fill="none" opacity="0.5"/>')
    s += f'<rect x="0" y="1520" width="{W}" height="{H - 1520}" fill="url(#kf)"/>'
    s += f'<rect width="{W}" height="{H}" fill="url(#fire)"/>'
    return svg_render(s)


def table_cloth():
    """a dish on the royal table: the hall blurred above, a red cloth with a gold border below (the dish sits at about (540, 900))"""
    s = ("<defs>" + FILTERS + lg("tw", [(0, "#e8dcc4", 1), (1, "#cdbb98", 1)]) + lg("cl", [(0, "#9a1c24", 1), (1, "#5a0a10", 1)]) + "</defs>")
    s += f'<rect width="{W}" height="{H}" fill="url(#tw)"/>'
    s += '<g filter="url(#b20)"><path d="M 300 760 L 300 300 Q 540 120, 780 300 L 780 760 Z" fill="#f4ecdc" stroke="#c9a24a" stroke-width="14"/>'
    s += '<circle cx="540" cy="360" r="40" fill="#c9a24a"/><rect x="0" y="560" width="1080" height="40" fill="#2f8a96"/></g>'
    s += '<path d="M -100 760 L 1180 760 L 1180 1920 L -100 1920 Z" fill="url(#cl)"/>'
    s += '<path d="M -100 800 L 1180 800" stroke="#c9a24a" stroke-width="12"/><path d="M -100 830 L 1180 830" stroke="#c9a24a" stroke-width="4"/>'
    r = random.Random(95)
    for k in range(60):
        x = r.uniform(-60, 1140); y = r.uniform(870, 1900); sc = 0.6 + (y - 870) / 900
        s += f'<path d="M {x:.0f} {y - 10 * sc:.0f} L {x + 10 * sc:.0f} {y:.0f} L {x:.0f} {y + 10 * sc:.0f} L {x - 10 * sc:.0f} {y:.0f} Z" fill="#c9a24a" opacity="0.45"/>'
    return svg_render(s)


# ------------------------------------------------------------------ part 3: Jamshid's hall (Persepolis style)
LAPIS, LAPIS_D = "#1e3a7a", "#122656"


def _rosette(x, y, r, col=GOLD, dark=GOLD_D, n=12):
    out = f'<circle cx="{x}" cy="{y}" r="{r}" fill="{dark}"/>'
    for k in range(n):
        a = 2 * math.pi * k / n
        out += f'<ellipse cx="{x + r * 0.55 * math.cos(a):.1f}" cy="{y + r * 0.55 * math.sin(a):.1f}" rx="{r * 0.36:.1f}" ry="{r * 0.16:.1f}" fill="{col}" transform="rotate({math.degrees(a):.0f},{x + r * 0.55 * math.cos(a):.1f},{y + r * 0.55 * math.sin(a):.1f})"/>'
    return out + f'<circle cx="{x}" cy="{y}" r="{r * 0.22:.1f}" fill="{GOLD_L}"/>'


def _bull_capital(x, y, w=150):
    """a double-bull capital (two kneeling bull fronts back to back) centred at x, its saddle top at y"""
    out = ""
    for sd in (-1, 1):
        hx = x + sd * w * 0.42
        out += (f'<path d="M {x} {y + 4} L {x + sd * w * 0.30:.0f} {y + 4} C {x + sd * w * 0.45:.0f} {y + 2}, {x + sd * w * 0.55:.0f} {y + 22}, {x + sd * w * 0.55:.0f} {y + 46} '
                f'L {x + sd * w * 0.50:.0f} {y + 88} L {x + sd * w * 0.36:.0f} {y + 88} L {x + sd * w * 0.32:.0f} {y + 58} L {x} {y + 58} Z" fill="#b8a07a" stroke="#5a4a32" stroke-width="3"/>'
              f'<ellipse cx="{hx:.0f}" cy="{y + 30}" rx="{w * 0.13:.0f}" ry="{w * 0.15:.0f}" fill="#a8906a" stroke="#5a4a32" stroke-width="3"/>'
              f'<path d="M {hx - w * 0.08:.0f} {y + 12} C {hx - w * 0.16:.0f} {y - 14}, {hx - w * 0.04:.0f} {y - 24}, {hx + sd * w * 0.02:.0f} {y - 30}" stroke="#5a4a32" stroke-width="7" fill="none" stroke-linecap="round"/>'
              f'<path d="M {hx + w * 0.08:.0f} {y + 12} C {hx + w * 0.16:.0f} {y - 14}, {hx + w * 0.04:.0f} {y - 24}, {hx + sd * w * 0.02:.0f} {y - 30}" stroke="#5a4a32" stroke-width="7" fill="none" stroke-linecap="round"/>'
              f'<circle cx="{hx + sd * w * 0.05:.0f}" cy="{y + 24}" r="4" fill="#2a2018"/>')
    return out + f'<rect x="{x - w * 0.22:.0f}" y="{y - 6}" width="{w * 0.44:.0f}" height="14" fill="#7a5a32"/>'


def _column(x, top, base, w=56):
    """a slender fluted stone column with a bell base and a double-bull capital; capital top at `top`, foot at `base`"""
    out = (f'<rect x="{x - w / 2:.0f}" y="{top + 88}" width="{w}" height="{base - top - 130}" fill="#d8c8a8" stroke="#8a7656" stroke-width="3"/>'
           + "".join(f'<path d="M {x - w / 2 + k * w / 6:.1f} {top + 96} L {x - w / 2 + k * w / 6:.1f} {base - 46}" stroke="#a8946e" stroke-width="2.5" opacity="0.8"/>' for k in range(1, 6)) +
           f'<path d="M {x - w / 2 - 6:.0f} {top + 88} L {x + w / 2 + 6:.0f} {top + 88} L {x + w / 2 + 2:.0f} {top + 104} L {x - w / 2 - 2:.0f} {top + 104} Z" fill="#c8b48e" stroke="#8a7656" stroke-width="2"/>'
           f'<path d="M {x - w / 2:.0f} {base - 46} C {x - w * 0.9:.0f} {base - 30}, {x - w * 1.2:.0f} {base - 6}, {x - w * 1.2:.0f} {base} L {x + w * 1.2:.0f} {base} '
           f'C {x + w * 1.2:.0f} {base - 6}, {x + w * 0.9:.0f} {base - 30}, {x + w / 2:.0f} {base - 46} Z" fill="#c8b48e" stroke="#8a7656" stroke-width="3"/>'
           + "".join(f'<path d="M {x + k * w * 0.2:.1f} {base - 44} C {x + k * w * 0.3:.1f} {base - 26}, {x + k * w * 0.4:.1f} {base - 10}, {x + k * w * 0.42:.1f} {base}" stroke="#a8946e" stroke-width="2" fill="none"/>' for k in (-2, -1, 0, 1, 2)))
    return out + _bull_capital(x, top, w * 2.7)


def jamshid_hall():
    """King Jamshid's hall by day, in the style of Persepolis: limestone walls, slender fluted columns with double-bull capitals under
    cedar beams, lapis blue panels with gold rosettes, a gold sun disc with rays over the throne; a golden jewelled throne (cushion top
    y 990, x 380-700) on three stone steps (y 1180-1310); two bronze fire stands at x 160 and 920 (bowls at y 1150: the scene lights
    them); a blue carpet; people stand at y 1330-1750"""
    s = ("<defs>" + FILTERS + lg("jw", [(0, "#efe2c4", 1), (1, "#d8c49e", 1)]) + lg("jf", [(0, "#cdb894", 1), (1, "#8a7452", 1)]) +
         lg("jcar", [(0, "#1a3470", 1), (1, "#0e1e46", 1)]) + lg("jcush", [(0, "#2a4ea0", 1), (1, "#16306a", 1)]) +
         rg("jsun", 540, 610, 330, [(0, "#fff2c0", 0.9), (0.35, "#f0c860", 0.45), (1, "#f0c860", 0)]) +
         lg("jbeam", [(0, "#fff6dc", 0.4), (1, "#fff6dc", 0.0)]) + "</defs>")
    s += f'<rect width="{W}" height="{H}" fill="url(#jw)"/>'
    # cedar beams and a painted frieze
    s += f'<rect x="0" y="0" width="{W}" height="230" fill="#5a3a22"/>'
    for k in range(9):
        s += f'<rect x="{k * 130 - 20}" y="0" width="60" height="230" fill="#4a2e1a"/>'
    s += f'<rect x="0" y="230" width="{W}" height="44" fill="{LAPIS}"/>'
    s += "".join(_rosette(60 + k * 120, 252, 16) for k in range(9))
    s += f'<path d="M 0 274 L {W} 274" stroke="{GOLD}" stroke-width="6"/>'
    # lapis panels between the columns, with rosettes
    for x0, x1 in ((0, 122), (178, 302), (778, 902), (958, W)):
        s += f'<rect x="{x0}" y="340" width="{x1 - x0}" height="800" fill="{LAPIS}"/><rect x="{x0 + 10}" y="350" width="{x1 - x0 - 20}" height="780" fill="none" stroke="{GOLD}" stroke-width="4"/>'
        s += "".join(_rosette((x0 + x1) / 2, 420 + j * 130, 22) for j in range(6))
    # the sun disc behind the throne and its glow
    s += f'<rect x="300" y="280" width="480" height="900" fill="url(#jsun)"/>'
    for k in range(24):
        a = 2 * math.pi * k / 24
        r0, r1 = 120, 200 if k % 2 == 0 else 165
        s += f'<path d="M {540 + r0 * math.cos(a):.0f} {600 + r0 * math.sin(a):.0f} L {540 + r1 * math.cos(a - 0.05):.0f} {600 + r1 * math.sin(a - 0.05):.0f} L {540 + r1 * math.cos(a + 0.05):.0f} {600 + r1 * math.sin(a + 0.05):.0f} Z" fill="{GOLD}" opacity="0.85"/>'
    s += f'<circle cx="540" cy="600" r="118" fill="{GOLD}" stroke="{GOLD_D}" stroke-width="6"/><circle cx="540" cy="600" r="92" fill="{GOLD_L}" opacity="0.6"/>'
    s += f'<circle cx="540" cy="600" r="70" fill="none" stroke="{GOLD_D}" stroke-width="4"/>'
    # drapes on both sides of the throne
    for sd in (-1, 1):
        x = 540 + sd * 200
        s += (f'<path d="M {x - 50} 280 C {x - 60} 600, {x - 40} 900, {x - 70} 1180 L {x + 70} 1180 C {x + 40} 900, {x + 60} 600, {x + 50} 280 Z" fill="{LAPIS_D}" stroke="#0a1636" stroke-width="3"/>'
              f'<path d="M {x - 20} 290 C {x - 26} 600, {x - 10} 900, {x - 30} 1170 M {x + 20} 290 C {x + 26} 600, {x + 14} 900, {x + 34} 1170" stroke="#2a4a8a" stroke-width="6" fill="none"/>'
              f'<path d="M {x - 70} 1180 L {x + 70} 1180" stroke="{GOLD}" stroke-width="10"/>')
    # columns along the back wall
    for x in (150, 330, 750, 930):
        s += _column(x, 270, 1180)
    # steps of the platform, with rows of tiny relief figures (a procession)
    for k, (x0, x1, y0) in enumerate([(200, 880, 1270), (240, 840, 1225), (280, 800, 1180)]):
        hgt = 42 if k == 2 else 50
        s += f'<rect x="{x0}" y="{y0}" width="{x1 - x0}" height="{hgt}" fill="#{0xd8 - 10 * k:02x}{0xc8 - 10 * k:02x}{0xa8 - 10 * k:02x}" stroke="#8a7656" stroke-width="3"/>'
        s += "".join(f'<circle cx="{x}" cy="{y0 + 13}" r="4" fill="#8a7656" opacity="0.6"/><path d="M {x - 4} {y0 + hgt - 9} L {x - 3} {y0 + 19} L {x + 3} {y0 + 19} L {x + 6} {y0 + hgt - 9} Z" fill="#8a7656" opacity="0.5"/>'
                     for x in range(x0 + 16, x1 - 8, 22))
    # the throne: a tall golden back with lapis inlay and jewels, a blue cushion, lion-paw feet
    s += (f'<path d="M 400 1000 L 400 760 Q 540 620, 680 760 L 680 1000 Z" fill="{GOLD}" stroke="{GOLD_D}" stroke-width="8"/>'
          f'<path d="M 426 990 L 426 772 Q 540 664, 654 772 L 654 990 Z" fill="{LAPIS}" stroke="{GOLD_L}" stroke-width="4"/>'
          + _rosette(540, 800, 34) +
          "".join(f'<circle cx="{x}" cy="{y}" r="9" fill="{c}" stroke="{GOLD_D}" stroke-width="2"/>' for x, y, c in
                  ((452, 900, "#b8121c"), (628, 900, "#b8121c"), (452, 960, "#2a8a4a"), (628, 960, "#2a8a4a"), (540, 712, "#b8121c"))) +
          f'<rect x="370" y="1040" width="340" height="140" fill="{GOLD}" stroke="{GOLD_D}" stroke-width="4"/>'
          f'<path d="M 386 1070 L 694 1070 M 386 1150 L 694 1150" stroke="{LAPIS}" stroke-width="8"/>'
          + "".join(f'<circle cx="{x}" cy="1110" r="10" fill="#b8121c" stroke="{GOLD_D}" stroke-width="2"/>' for x in range(410, 690, 56)) +
          f'<rect x="380" y="988" width="320" height="58" rx="18" fill="url(#jcush)" stroke="#0a1636" stroke-width="3"/>'
          f'<path d="M 392 1000 L 688 1000" stroke="{GOLD_L}" stroke-width="4" opacity="0.8"/>'
          f'<rect x="352" y="900" width="40" height="150" rx="8" fill="{GOLD}" stroke="{GOLD_D}" stroke-width="3"/>'
          f'<rect x="688" y="900" width="40" height="150" rx="8" fill="{GOLD}" stroke="{GOLD_D}" stroke-width="3"/>'
          f'<circle cx="372" cy="892" r="18" fill="{GOLD_L}" stroke="{GOLD_D}" stroke-width="3"/><circle cx="708" cy="892" r="18" fill="{GOLD_L}" stroke="{GOLD_D}" stroke-width="3"/>'
          f'<path d="M 372 1180 C 360 1150, 380 1140, 392 1160 M 708 1180 C 720 1150, 700 1140, 688 1160" stroke="{GOLD_D}" stroke-width="6" fill="none"/>')
    # floor, carpet and the two fire stands
    s += f'<rect x="0" y="1310" width="{W}" height="{H - 1310}" fill="url(#jf)"/>'
    for k in range(10):
        y = 1310 + k * k * 7 + k * 14
        s += f'<path d="M 0 {y} L {W} {y}" stroke="#6a5438" stroke-width="{2 + k * 0.4:.1f}" opacity="0.35"/>'
    for k in range(-8, 9):
        s += f'<path d="M {540 + k * 70} 1310 L {540 + k * 240} 1920" stroke="#6a5438" stroke-width="2.5" opacity="0.3"/>'
    s += (f'<path d="M 430 1310 L 650 1310 L 790 1920 L 290 1920 Z" fill="url(#jcar)"/>'
          f'<path d="M 446 1310 L 634 1310 L 762 1920 L 318 1920 Z" fill="none" stroke="{GOLD}" stroke-width="6"/>'
          + "".join(f'<path d="M {540 - 8 - k * 0.05 * (y - 1310)} {y} L 540 {y - 14 - k} L {540 + 8 + k * 0.05 * (y - 1310)} {y} L 540 {y + 14 + k} Z" fill="{GOLD}" opacity="0.7"/>'
                    for k, y in enumerate((1400, 1520, 1660, 1820))))
    for fx_ in (160, 920):
        s += (f'<path d="M {fx_ - 50} 1380 L {fx_ + 50} 1380 L {fx_ + 30} 1360 L {fx_ - 30} 1360 Z" fill="#8a5a22" stroke="#3a2410" stroke-width="3"/>'
              f'<rect x="{fx_ - 12}" y="1180" width="24" height="182" fill="#9a6a2a" stroke="#3a2410" stroke-width="3"/>'
              f'<path d="M {fx_ - 70} 1150 L {fx_ + 70} 1150 C {fx_ + 60} 1196, {fx_ - 60} 1196, {fx_ - 70} 1150 Z" fill="#b8822e" stroke="#3a2410" stroke-width="4"/>'
              f'<path d="M {fx_ - 76} 1150 L {fx_ + 76} 1150" stroke="#e0b25a" stroke-width="6"/>')
    s += f'<path d="M 0 0 L 220 0 L 640 1500 L 300 1500 Z" fill="url(#jbeam)" opacity="0.5"/>'
    return svg_render(s)


def jamshid_hall_close():
    """close on Jamshid's golden throne: its lapis and gold back with the sun disc at (540, 520) behind the king's head (neck at about
    (540, 1010)), drapes and columns soft at the sides"""
    s = ("<defs>" + FILTERS + lg("jw", [(0, "#efe2c4", 1), (1, "#d2bc94", 1)]) +
         rg("jsun", 540, 520, 520, [(0, "#fff2c0", 0.9), (0.35, "#f0c860", 0.4), (1, "#f0c860", 0)]) + "</defs>")
    s += f'<rect width="{W}" height="{H}" fill="url(#jw)"/>'
    s += f'<g filter="url(#b12)">' + _column(70, 200, 1900, 110) + _column(1010, 200, 1900, 110) + '</g>'
    s += f'<g filter="url(#b6)"><path d="M 150 0 C 130 600, 170 1200, 120 1920 L 260 1920 C 230 1200, 250 600, 240 0 Z" fill="{LAPIS_D}"/>'
    s += f'<path d="M 930 0 C 950 600, 910 1200, 960 1920 L 820 1920 C 850 1200, 830 600, 840 0 Z" fill="{LAPIS_D}"/></g>'
    s += f'<rect width="{W}" height="{H}" fill="url(#jsun)"/>'
    s += f'<path d="M 190 1920 L 190 760 Q 540 300, 890 760 L 890 1920 Z" fill="{GOLD}" stroke="{GOLD_D}" stroke-width="14"/>'
    s += f'<path d="M 232 1920 L 232 784 Q 540 380, 848 784 L 848 1920 Z" fill="{LAPIS}" stroke="{GOLD_L}" stroke-width="8"/>'
    for k in range(24):
        a = 2 * math.pi * k / 24
        r0, r1 = 150, 250 if k % 2 == 0 else 205
        s += f'<path d="M {540 + r0 * math.cos(a):.0f} {520 + r0 * math.sin(a):.0f} L {540 + r1 * math.cos(a - 0.05):.0f} {520 + r1 * math.sin(a - 0.05):.0f} L {540 + r1 * math.cos(a + 0.05):.0f} {520 + r1 * math.sin(a + 0.05):.0f} Z" fill="{GOLD}"/>'
    s += f'<circle cx="540" cy="520" r="148" fill="{GOLD}" stroke="{GOLD_D}" stroke-width="8"/><circle cx="540" cy="520" r="112" fill="{GOLD_L}" opacity="0.6"/>'
    s += "".join(_rosette(x, y, 30) for x, y in ((300, 1000), (780, 1000), (300, 1300), (780, 1300), (300, 1600), (780, 1600)))
    s += "".join(f'<circle cx="{x}" cy="{y}" r="13" fill="{c}" stroke="{GOLD_D}" stroke-width="3"/>' for x, y, c in
                 ((210, 900, "#b8121c"), (870, 900, "#b8121c"), (210, 1200, "#2a8a4a"), (870, 1200, "#2a8a4a"), (210, 1500, "#b8121c"), (870, 1500, "#b8121c")))
    return svg_render(s)


# ------------------------------------------------------------------ part 4: Zahhak's bedchamber at night
def bedchamber():
    """Zahhak's bedchamber at night: black and purple walls, the gold serpent sign over a wide bed with a crimson canopy (posts at x 130
    and 950, mattress top y 1190, front y 1190-1330, pillows at the left, x 150-400), a tall moonlit window at the right (x 800-960,
    y 420-900) with its beam, a bronze lamp stand at x 70 (flame at about (70, 960), drawn by the scene); floor from y 1330"""
    s = ("<defs>" + FILTERS + lg("bw", [(0, "#0c0910", 1), (0.5, "#1c1422", 1), (1, "#120d16", 1)]) + lg("bf", [(0, "#1e1620", 1), (1, "#07050a", 1)]) +
         lg("cov", [(0, "#7a1220", 1), (1, "#3e0810", 1)]) + lg("moon", [(0, "#b8c8ff", 0.35), (1, "#b8c8ff", 0.0)]) +
         rg("lampg", 70, 960, 520, [(0, "#ffae5a", 0.30), (0.5, "#a0502a", 0.08), (1, "#000", 0)]) + "</defs>")
    s += f'<rect width="{W}" height="{H}" fill="url(#bw)"/>'
    for x in range(0, W, 120):
        s += f'<path d="M {x} 0 L {x} 1330" stroke="#241a2a" stroke-width="3" opacity="0.6"/>'
    s += f'<rect x="0" y="250" width="{W}" height="16" fill="{GOLD_D}" opacity="0.7"/>'
    s += serpent_emblem(540, 400, 1.15)
    # the window and its moonbeam
    s += ('<path d="M 800 900 L 800 520 Q 880 400, 960 520 L 960 900 Z" fill="#26304e" stroke="#7a5a22" stroke-width="8"/>'
          '<path d="M 880 420 L 880 900 M 800 700 L 960 700" stroke="#3a2a1a" stroke-width="6"/>'
          '<circle cx="920" cy="600" r="26" fill="#e8ecff" opacity="0.9"/>'
          '<path d="M 800 900 L 960 900 L 700 1700 L 380 1700 Z" fill="url(#moon)"/>')
    # canopy and curtains
    s += ('<path d="M 100 560 L 980 560 L 980 610 L 100 610 Z" fill="#4a0a14" stroke="#1a0408" stroke-width="4"/>'
          f'<path d="M 100 560 L 980 560" stroke="{GOLD}" stroke-width="8"/>')
    for k in range(8):
        x0 = 110 + k * 110
        s += f'<path d="M {x0} 610 Q {x0 + 55} 660, {x0 + 110} 610" fill="#5a0c18" stroke="#1a0408" stroke-width="3"/>'
    for sd, x in ((-1, 130), (1, 950)):
        s += (f'<rect x="{x - 14}" y="560" width="28" height="770" fill="#2a1a12" stroke="#120806" stroke-width="3"/>'
              f'<circle cx="{x}" cy="548" r="20" fill="{GOLD}" stroke="{GOLD_D}" stroke-width="3"/>'
              f'<path d="M {x - sd * 10} 610 C {x - sd * 160} 760, {x - sd * 40} 900, {x - sd * 20} 1000 L {x + sd * 14} 1000 L {x + sd * 14} 610 Z" fill="#6a0e1c" stroke="#1a0408" stroke-width="3"/>'
              f'<path d="M {x - sd * 30} 960 L {x + sd * 10} 960" stroke="{GOLD}" stroke-width="10"/>')
    # the bed
    s += ('<path d="M 120 1190 L 960 1190 L 960 1330 L 120 1330 Z" fill="#2a1a12" stroke="#120806" stroke-width="4"/>'
          f'<path d="M 120 1200 L 960 1200" stroke="{GOLD}" stroke-width="6"/>'
          '<path d="M 140 1150 C 400 1120, 700 1120, 950 1150 L 960 1200 L 130 1200 Z" fill="#e8dccc" stroke="#3a2a20" stroke-width="3"/>'
          '<rect x="150" y="1080" width="250" height="90" rx="40" fill="#efe4d0" stroke="#3a2a20" stroke-width="4"/>'
          '<path d="M 120 1330 L 960 1330 L 960 1270 C 700 1240, 400 1240, 120 1270 Z" fill="url(#cov)" stroke="#1a0408" stroke-width="3"/>')
    # the lamp stand
    s += ('<rect x="62" y="980" width="16" height="350" fill="#8a5a22" stroke="#3a2410" stroke-width="3"/>'
          '<path d="M 20 1330 L 120 1330 L 100 1310 L 40 1310 Z" fill="#8a5a22" stroke="#3a2410" stroke-width="3"/>'
          '<path d="M 30 970 L 110 970 C 100 1000, 40 1000, 30 970 Z" fill="#b8822e" stroke="#3a2410" stroke-width="3"/>')
    s += f'<rect x="0" y="1330" width="{W}" height="{H - 1330}" fill="url(#bf)"/>'
    for k in range(9):
        y = 1330 + k * k * 7 + k * 14
        s += f'<path d="M 0 {y} L {W} {y}" stroke="#2a2030" stroke-width="2" opacity="0.5"/>'
    s += f'<rect width="{W}" height="{H}" fill="url(#lampg)"/>'
    return svg_render(s)


# ------------------------------------------------------------------ part 5: Mount Damavand (title, the dream, Abtin's road), the dream palace gate
DAMA = {   # sky stops, mountain light/shadow, snow light/shadow, foothills (far, near), plain (top, bottom), mist
    "night": dict(sky=[(0, "#060a1e", 1), (0.3, "#101a3e", 1), (0.52, "#24305e", 1), (0.58, "#3a4270", 1)],
                  mt="#2a3050", mts="#161a30", snow="#dfe6f6", snows="#8a96b8", far="#1c2240", near="#11152a",
                  plain=("#1c2238", "#07080e"), mist="#8a96c8"),
    "dream": dict(sky=[(0, "#12061a", 1), (0.28, "#3a0e30", 1), (0.48, "#7a1e34", 1), (0.58, "#c0503a", 1)],
                  mt="#4a1a3a", mts="#2a0c22", snow="#f2c8d4", snows="#a87088", far="#3a1230", near="#240a1e",
                  plain=("#3a1428", "#0e040c"), mist="#e8a0b8"),
    "dusk": dict(sky=[(0, "#1e2450", 1), (0.3, "#5a3a68", 1), (0.46, "#c06a5a", 1), (0.54, "#f0a060", 1), (0.58, "#ffd890", 1)],
                 mt="#7a5a78", mts="#4a3450", snow="#ffe2cc", snows="#c09aa8", far="#5a4058", near="#3e2c3c",
                 plain=("#8a6a4a", "#3a2a22"), mist="#ffc8a0"),
}


def _dama_mountain(p, seed=7):
    """the cone of Damavand: summit (610, 525), feet beyond the frame at y 1110; light from the left"""
    s = ('<path d="M -260 1110 Q 330 905, 560 548 Q 610 518, 666 550 Q 900 905, 1460 1110 Z" fill="{mt}"/>'.format(**p) +
         '<path d="M 610 524 Q 640 528, 666 550 Q 900 905, 1460 1110 L 760 1110 Q 690 800, 610 524 Z" fill="{mts}" opacity="0.85"/>'.format(**p))
    r = random.Random(seed)
    # gullies
    for k in range(9):
        x0 = lerp_(470, 760, k / 8) + r.uniform(-12, 12)
        y0 = _dama_slope(x0) + 230
        x1 = x0 + (x0 - 610) * r.uniform(0.6, 1.0)
        y1 = y0 + r.uniform(160, 300)
        s += f'<path d="M {x0:.0f} {y0:.0f} Q {x0 + (x1 - x0) * 0.4:.0f} {y0 + (y1 - y0) * 0.5:.0f} {x1:.0f} {y1:.0f}" stroke="{p["mts"]}" stroke-width="{r.uniform(4, 9):.1f}" fill="none" opacity="0.55"/>'
    # the snow cap: a soft edge with broad, uneven fingers running down the gullies (smoothed)
    from chars import smooth_path
    pts = [(560, 548), (610, 522), (666, 550)]
    n = 22
    for k in range(n + 1):
        u = k / n
        x = lerp_(850, 388, u) + r.uniform(-6, 6)
        y_slope = _dama_slope(x)
        kind = r.random()
        finger = 170 + 70 * r.random() if kind < 0.3 else (90 + 40 * r.random() if kind < 0.6 else 30 + 30 * r.random())
        depth = (50 + finger) * (0.3 + 0.7 * math.sin(math.pi * u) ** 0.6)
        pts.append((x, min(1050, y_slope + depth)))
    sd = smooth_path(pts)
    s += f'<path d="{sd}" fill="{p["snow"]}"/><clipPath id="snowclip"><path d="{sd}"/></clipPath>'
    s += f'<path d="M 612 520 L 1100 520 L 1100 1100 L 700 1100 Q 676 760, 612 520 Z" fill="{p["snows"]}" opacity="0.75" clip-path="url(#snowclip)"/>'
    # a plume of cloud blown off the summit
    s += (f'<ellipse cx="740" cy="512" rx="150" ry="26" fill="{p["mist"]}" opacity="0.45" filter="url(#b12)"/>'
          f'<ellipse cx="880" cy="500" rx="190" ry="20" fill="{p["mist"]}" opacity="0.3" filter="url(#b20)"/>')
    return s


def _dama_slope(x):
    """y of the mountain outline at x (the quadratic curves of _dama_mountain, approximated)"""
    if x <= 560:
        # Q from (-260,1110) ctrl (330,905) to (560,548): solve for u by bisection on x
        P0, P1, P2 = (-260, 1110), (330, 905), (560, 548)
    elif x <= 666:
        P0, P1, P2 = (560, 548), (610, 518), (666, 550)
    else:
        P0, P1, P2 = (666, 550), (900, 905), (1460, 1110)
    lo, hi = 0.0, 1.0
    for _ in range(40):
        u = (lo + hi) / 2
        xx = (1 - u) ** 2 * P0[0] + 2 * (1 - u) * u * P1[0] + u * u * P2[0]
        if xx < x:
            lo = u
        else:
            hi = u
    u = (lo + hi) / 2
    return (1 - u) ** 2 * P0[1] + 2 * (1 - u) * u * P1[1] + u * u * P2[1]


def _dama_x(x, side):
    return x


def lerp_(a, b, u):
    return a + (b - a) * u


def damavand(pal="night", road=False):
    """Mount Damavand on the horizon: the snow-capped cone (summit (610, 525)) over two rows of foothills; the plain from y 1110;
    pal "night" (a moon at the upper left, stars), "dream" (purple and crimson, mist; for the dream), "dusk" (a low sun at the left).
    road=True: a dirt road winds from the bottom (x 330-790) to the horizon at x 600; people walk on it at y 1350-1800."""
    p = DAMA[pal]
    s = "<defs>" + FILTERS + lg("dsky", p["sky"]) + lg("dpl", [(0, p["plain"][0], 1), (1, p["plain"][1], 1)])
    if pal == "dusk":
        s += rg("dsun", 170, 1030, 700, [(0, "#fff4d0", 0.95), (0.1, "#ffd08a", 0.6), (1, "#ff9a5a", 0)])
    elif pal == "night":
        s += rg("dmoon", 250, 400, 420, [(0, "#e8f0ff", 0.5), (0.2, "#b8c8f0", 0.15), (1, "#000", 0)])
    else:
        s += rg("dmoon", 830, 430, 460, [(0, "#ffd0c0", 0.45), (0.3, "#d06070", 0.12), (1, "#000", 0)])
    s += lg("droad", [(0, "#c8a070" if pal == "dusk" else "#3a3048", 1), (1, "#7a5a3a" if pal == "dusk" else "#1a1420", 1)]) + "</defs>"
    s += f'<rect width="{W}" height="{H}" fill="url(#dsky)"/>'
    if pal == "night":
        s += stars(501, 160, 900) + '<rect width="1080" height="1920" fill="url(#dmoon)"/><circle cx="250" cy="400" r="40" fill="#f4f6ff"/>'
    elif pal == "dream":
        s += stars(502, 60, 700) + '<rect width="1080" height="1920" fill="url(#dmoon)"/><circle cx="830" cy="430" r="58" fill="#f6c8b8" opacity="0.9"/>'
        s += clouds(W, 503, [640, 760, 880], col="#d86a7a", hi="#ffb0a0", op=0.35)
    else:
        s += clouds(W, 504, [560, 700, 820, 930], col="#f09a8a", hi="#ffd2a0", op=0.5)
        s += '<rect width="1080" height="1920" fill="url(#dsun)"/><circle cx="170" cy="1030" r="54" fill="#fff6dc"/>'
    s += _dama_mountain(p)
    s += f'<path d="{ridge(W, 1075, 70, 505, rough=0.5)}" fill="{p["far"]}"/>'
    s += f'<rect x="0" y="1040" width="{W}" height="70" fill="{p["mist"]}" opacity="0.18" filter="url(#b20)"/>'
    s += f'<path d="{ridge(W, 1112, 40, 506, rough=0.6)}" fill="{p["near"]}"/>'
    s += f'<rect x="0" y="1105" width="{W}" height="{H - 1105}" fill="url(#dpl)"/>'
    r = random.Random(507)
    if road:
        cl = [(600, 1100), (575, 1180), (650, 1300), (520, 1480), (600, 1700), (560, 1960)]
        def wd(y):
            return 8 + (y - 1100) / 860 * 230
        left, right = [], []
        for i, (x, y) in enumerate(cl):
            left.append((x - wd(y), y)); right.append((x + wd(y), y))
        d = "M " + " L ".join(f"{x:.0f} {y:.0f}" for x, y in left) + " L " + " L ".join(f"{x:.0f} {y:.0f}" for x, y in reversed(right)) + " Z"
        s += f'<path d="{d}" fill="url(#droad)" opacity="0.9" filter="url(#b3)"/>'
        for k in range(26):
            y = r.uniform(1150, 1900); i = max(0, min(len(cl) - 2, sum(1 for c in cl if c[1] < y) - 1))
            (xa, ya), (xb, yb) = cl[i], cl[i + 1]
            x = xa + (xb - xa) * (y - ya) / max(1, yb - ya) + r.uniform(-0.8, 0.8) * wd(y)
            s += f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{3 + (y - 1100) / 90:.1f}" ry="{1.5 + (y - 1100) / 200:.1f}" fill="#5a4030" opacity="0.6"/>'
    tuft = {"night": ("#1e2a30", "#3a4a58"), "dream": ("#2a0e22", "#5a2a44"), "dusk": ("#5a5a2a", "#a89a50")}[pal]
    s += grass_tufts(508, 1130, 1900, 60, col=tuft[0], hi=tuft[1])
    for _ in range(14):
        x = r.uniform(0, W); y = r.uniform(1150, 1900); sc = 0.4 + (y - 1100) / 700
        s += f'<path d="M {x - 26 * sc:.0f} {y:.0f} Q {x - 18 * sc:.0f} {y - 22 * sc:.0f} {x + 4 * sc:.0f} {y - 24 * sc:.0f} Q {x + 26 * sc:.0f} {y - 14 * sc:.0f} {x + 30 * sc:.0f} {y:.0f} Z" fill="{p["near"]}" opacity="0.8"/>'
    if pal == "dusk":
        for x, h in ((70, 330), (140, 260), (980, 300), (1040, 380)):
            s += cypress(x, 1180, h, col="#2a1e2a", dark="#1a121c", rim="#ffb080", w=0.11)
    if pal == "dream":
        for k in range(5):
            y = 1150 + k * 150
            s += f'<ellipse cx="{r.uniform(200, 900):.0f}" cy="{y}" rx="{r.uniform(420, 700):.0f}" ry="{30 + 8 * k}" fill="{p["mist"]}" opacity="0.13" filter="url(#b20)"/>'
    return svg_render(s)


def dream_gate():
    """the dream: Zahhak's palace as a black shape against a purple and crimson sky with a red moon; its arched gate (opening x 430-650,
    apex y 960, sill y 1250) blazes with light that spills down a path to the bottom; mist on the ground. Figures come out of the gate at
    feet y 1255 (scale ~0.15) and walk to y 1700 (scale ~0.55)"""
    p = DAMA["dream"]
    s = ("<defs>" + FILTERS + lg("gsky", p["sky"]) + lg("gpl", [(0, "#2a0e20", 1), (1, "#07020a", 1)]) +
         rg("gmoon", 800, 470, 420, [(0, "#ffd0c0", 0.45), (0.3, "#d06070", 0.12), (1, "#000", 0)]) +
         rg("glow", 540, 1120, 520, [(0, "#fff0c8", 0.9), (0.18, "#ffc070", 0.55), (0.5, "#c05a3a", 0.18), (1, "#000", 0)]) +
         lg("gate", [(0, "#ffd890", 1), (0.6, "#fff6dc", 1), (1, "#ffe8b0", 1)]) +
         lg("spill", [(0, "#ffe0a0", 0.55), (1, "#ffb070", 0.0)]) + "</defs>")
    s += f'<rect width="{W}" height="{H}" fill="url(#gsky)"/>' + stars(511, 70, 650)
    s += '<rect width="1080" height="1920" fill="url(#gmoon)"/><circle cx="800" cy="470" r="62" fill="#f2b8a8" opacity="0.92"/>'
    s += clouds(W, 512, [560, 690, 800], col="#c85a6a", hi="#ffa090", op=0.35)
    dark, edge = "#0b0610", "#2a1222"
    # the palace: wall, towers, domes, banners
    s += (f'<path d="M 40 1250 L 40 930 L 1040 930 L 1040 1250 Z" fill="{dark}"/>'
          + "".join(f'<rect x="{x}" y="904" width="34" height="30" fill="{dark}"/>' for x in range(46, 1040, 62)))
    for tx in (110, 970):
        s += (f'<rect x="{tx - 70}" y="700" width="140" height="550" fill="{dark}"/>'
              + "".join(f'<rect x="{tx - 70 + k * 40}" y="672" width="26" height="32" fill="{dark}"/>' for k in range(4)) +
              f'<path d="M {tx} 690 L {tx} 520" stroke="{dark}" stroke-width="8"/>'
              f'<path d="M {tx} 526 C {tx + 60} 540, {tx + 100} 520, {tx + 150} 548 L {tx + 140} 600 C {tx + 100} 580, {tx + 60} 600, {tx} 586 Z" fill="#14080e" stroke="{edge}" stroke-width="3"/>')
    for cx, rr, top in ((300, 110, 820), (780, 110, 820)):
        s += (f'<path d="M {cx - rr} 940 L {cx - rr} {top + 40} Q {cx - rr} {top - rr}, {cx} {top - rr - 40} Q {cx + rr} {top - rr}, {cx + rr} {top + 40} L {cx + rr} 940 Z" fill="{dark}"/>'
              f'<path d="M {cx} {top - rr - 40} L {cx} {top - rr - 110}" stroke="{dark}" stroke-width="7"/>')
    s += (f'<path d="M 360 940 L 360 760 Q 360 540, 540 470 Q 720 540, 720 760 L 720 940 Z" fill="{dark}"/>'
          f'<path d="M 540 470 L 540 360" stroke="{dark}" stroke-width="10"/><circle cx="540" cy="350" r="14" fill="{dark}"/>'
          f'<path d="M 390 760 Q 390 570, 540 500" stroke="{edge}" stroke-width="4" fill="none" opacity="0.8"/>')
    for wx in (210, 380, 700, 870):
        s += f'<path d="M {wx - 14} 1080 L {wx - 14} 1040 Q {wx} 1020, {wx + 14} 1040 L {wx + 14} 1080 Z" fill="#ff9a50" opacity="0.55"/>'
    s += serpent_emblem(540, 860, 0.55, col="#6a4a1a", dark="#2a1a0a")
    # the blazing gate
    s += ('<rect width="1080" height="1920" fill="url(#glow)"/>'
          '<path d="M 410 1250 L 410 1060 Q 410 950, 540 930 Q 670 950, 670 1060 L 670 1250 Z" fill="#3a1a14"/>'
          '<path d="M 430 1250 L 430 1066 Q 430 972, 540 958 Q 650 972, 650 1066 L 650 1250 Z" fill="url(#gate)"/>')
    # the ground, the path of light, mist
    s += f'<rect x="0" y="1250" width="{W}" height="{H - 1250}" fill="url(#gpl)"/>'
    s += '<path d="M 430 1250 L 650 1250 L 900 1920 L 180 1920 Z" fill="url(#spill)"/>'
    r = random.Random(513)
    for k in range(9):
        y = 1260 + k * 80
        s += f'<path d="M 0 {y} L {W} {y}" stroke="#3a1a2a" stroke-width="2" opacity="0.4"/>'
    for k in range(6):
        y = 1230 + k * 120
        s += f'<ellipse cx="{r.uniform(150, 930):.0f}" cy="{y}" rx="{r.uniform(380, 640):.0f}" ry="{26 + 10 * k}" fill="{p["mist"]}" opacity="0.14" filter="url(#b20)"/>'
    return svg_render(s)
