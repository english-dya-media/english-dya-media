"""Painted backgrounds of Arash the Archer (SVG -> PNG; cache them with bgs.cached("ar_<name>", abg.<name>)).
Part 1: the besieged fortress in the green mountains of Tabaristan, with the tents of Turan all round (siege), and the yard inside
its walls (fort_yard)."""
import math, random
from film import svg_render, W, H
from bgs import FILTERS, lg, rg, ridge, hill, clouds, stars, grass_tufts, boulder, pine, _strata

GOLD, GOLD_D = "#c9a24a", "#7a5a22"
SKY = {
    "dawn": [(0, "#3a4a82", 1), (0.3, "#a87aa0", 1), (0.46, "#f0a888", 1), (0.54, "#ffd8a8", 1)],
    "day": [(0, "#4a7ab8", 1), (0.35, "#9cc4dc", 1), (0.52, "#e6eedc", 1)],
    "dusk": [(0, "#26285a", 1), (0.3, "#6a4a78", 1), (0.46, "#e0806a", 1), (0.54, "#ffc890", 1)],
    "night": [(0, "#04060f", 1), (0.35, "#101a3a", 1), (0.52, "#24305a", 1)],
}
GREEN = {"dawn": ("#4a6a5a", "#2e4a3e", "#20382e"), "day": ("#5a8a5a", "#3a6a42", "#2a5034"), "dusk": ("#4a5a5a", "#2e3e40", "#1e2c2e"),
         "night": ("#1e2a36", "#141e28", "#0c141c")}
FORT_TOP = (540, 610)        # the top of the keep in siege()
TENT_COLS = (("#1c1a20", "#8a1a1a"), ("#24202a", "#6a1414"), ("#2a2224", "#9a2a1a"))


def _banner(x, y, h, t=0.0, col="#1e4a8a", sun=True):
    """a pennant on a pole standing on (x, y)"""
    o = (f'<rect x="{x - 3}" y="{y - h}" width="6" height="{h}" fill="#3a2a1a"/>'
         f'<path d="M {x + 3} {y - h + 4} L {x + 3 + h * 0.42:.0f} {y - h + 4 + h * 0.08:.0f} L {x + 3 + h * 0.36:.0f} {y - h + 4 + h * 0.18:.0f} '
         f'L {x + 3 + h * 0.42:.0f} {y - h + 4 + h * 0.28:.0f} L {x + 3} {y - h + 4 + h * 0.3:.0f} Z" fill="{col}" stroke="#101018" stroke-width="2"/>')
    if sun:
        o += f'<circle cx="{x + 3 + h * 0.17:.0f}" cy="{y - h + 4 + h * 0.15:.0f}" r="{h * 0.045:.1f}" fill="{GOLD}"/>'
    return o


def _tent(x, y, w, h, cols, lit=False):
    body, stripe = cols
    o = (f'<path d="M {x - w / 2:.0f} {y} L {x:.0f} {y - h:.0f} L {x + w / 2:.0f} {y} Z" fill="{body}" stroke="#08070a" stroke-width="2"/>'
         f'<path d="M {x:.0f} {y - h:.0f} L {x - w * 0.18:.0f} {y} M {x:.0f} {y - h:.0f} L {x + w * 0.18:.0f} {y}" stroke="{stripe}" stroke-width="{max(2, w * 0.05):.0f}"/>'
         f'<path d="M {x - w * 0.1:.0f} {y} L {x:.0f} {y - h * 0.45:.0f} L {x + w * 0.1:.0f} {y} Z" fill="{"#ffb060" if lit else "#08070a"}"/>'
         f'<rect x="{x - 1.5:.0f}" y="{y - h - w * 0.25:.0f}" width="3" height="{w * 0.25:.0f}" fill="#141014"/>'
         f'<path d="M {x + 1:.0f} {y - h - w * 0.25:.0f} l {w * 0.22:.0f} {w * 0.05:.0f} l {-w * 0.22:.0f} {w * 0.07:.0f} Z" fill="{stripe}"/>')
    return o


def _fortress(pal):
    """the Iranian fortress: sand-coloured stone, round towers, the keep in the middle, blue banners with a gold sun"""
    stone, shade, lit = {"night": ("#4a4652", "#2e2c36", "#6a6676"), "dusk": ("#9a7a6a", "#6a5048", "#c8a088"),
                         "dawn": ("#b89a86", "#7e6658", "#e2c2a8"), "day": ("#c8b08e", "#8e7a62", "#ecd8b8")}[pal]
    o = ""
    o += f'<path d="M 300 900 L 300 760 L 780 760 L 780 900 Z" fill="{stone}" stroke="#20181a" stroke-width="3"/>'
    o += "".join(f'<rect x="{x}" y="744" width="20" height="18" fill="{stone}" stroke="#20181a" stroke-width="2"/>' for x in range(304, 776, 34))
    for x, top in ((300, 700), (780, 700), (430, 720), (650, 720)):
        o += (f'<rect x="{x - 38}" y="{top}" width="76" height="{900 - top}" fill="{stone}" stroke="#20181a" stroke-width="3"/>'
              f'<rect x="{x - 38}" y="{top}" width="22" height="{900 - top}" fill="{shade}" opacity="0.6"/>'
              + "".join(f'<rect x="{x - 38 + k * 20}" y="{top - 16}" width="14" height="18" fill="{stone}" stroke="#20181a" stroke-width="2"/>' for k in range(4)) +
              f'<rect x="{x - 6}" y="{top + 40}" width="12" height="24" rx="5" fill="{"#ffb24a" if pal == "night" else "#2a2024"}"/>')
    kx, ky = FORT_TOP
    o += (f'<rect x="{kx - 70}" y="{ky}" width="140" height="{900 - ky}" fill="{stone}" stroke="#20181a" stroke-width="3"/>'
          f'<rect x="{kx - 70}" y="{ky}" width="40" height="{900 - ky}" fill="{shade}" opacity="0.6"/>'
          + "".join(f'<rect x="{kx - 70 + k * 28}" y="{ky - 18}" width="18" height="20" fill="{stone}" stroke="#20181a" stroke-width="2"/>' for k in range(5)) +
          f'<rect x="{kx - 8}" y="{ky + 50}" width="16" height="30" rx="7" fill="{"#ffb24a" if pal == "night" else "#2a2024"}"/>')
    o += f'<path d="M 505 900 L 505 845 Q 540 815, 575 845 L 575 900 Z" fill="#20181a"/>'
    o += _banner(kx, ky - 18, 110) + _banner(300, 684, 80) + _banner(780, 684, 80)
    o += f'<path d="M 300 790 L 780 790" stroke="{lit}" stroke-width="3" opacity="0.5"/>'
    return o


def siege(pal="dawn"):
    """Tabaristan: misty green mountains; the Iranian fortress on a wooded hill in the middle (walls y 700-900, keep top FORT_TOP); the dark
    tents of Turan with red stripes and black-red pennants all round its foot (y 1000-1300, campfires at night); a meadow in front
    (people stand at y 1380-1750). pal: dawn / day / dusk / night"""
    r = random.Random(1501)
    g1, g2, g3 = GREEN[pal]
    s = "<defs>" + FILTERS + lg("ssky", SKY[pal]) + lg("smead", [(0, g2, 1), (1, g3, 1)]) + "</defs>"
    s += f'<rect width="{W}" height="{H}" fill="url(#ssky)"/>'
    if pal == "night":
        s += stars(1502, 160, 800) + '<circle cx="840" cy="380" r="40" fill="#f2f4ff"/>'
    elif pal in ("dawn", "dusk"):
        s += clouds(W, 1503, [420, 560], col="#f4b0a0" if pal == "dawn" else "#e08a7a", hi="#ffe0c0", op=0.5)
    else:
        s += clouds(W, 1503, [380, 520], col="#ffffff", hi="#ffffff", op=0.6)
    far = {"dawn": ("#8a8aa8", "#6a7a8a"), "day": ("#8aa0b8", "#6a8a96"), "dusk": ("#6a5a7a", "#4e4a62"), "night": ("#1a2036", "#141a2c")}[pal]
    s += f'<path d="{ridge(W, 900, 210, 1504, rough=0.5)}" fill="{far[0]}"/>'
    s += f'<rect x="0" y="820" width="{W}" height="120" fill="#ffffff" opacity="{0.06 if pal == "night" else 0.22}" filter="url(#b20)"/>'
    s += f'<path d="{ridge(W, 980, 170, 1505, rough=0.45)}" fill="{far[1]}"/>'
    s += f'<rect x="0" y="930" width="{W}" height="110" fill="#ffffff" opacity="{0.05 if pal == "night" else 0.2}" filter="url(#b20)"/>'
    # the wooded hill with the fortress
    s += f'<path d="M -40 1180 C 120 1080, 220 900, 330 880 L 760 880 C 880 900, 980 1060, 1120 1160 L 1120 1300 L -40 1300 Z" fill="{g1}"/>'
    for k in range(60):
        x = r.uniform(-20, 1100); y = r.uniform(930, 1260)
        if 300 < x < 790 and y < 960:
            continue
        s += pine(x, y, r.uniform(60, 120), col=g2, dark=g3)
    s += _fortress(pal)
    # Turan's camp round the foot of the hill
    tents = []
    for k in range(34):
        x = r.uniform(-40, 1120); y = r.uniform(1040, 1300)
        if 260 < x < 820 and y < 1110:
            continue
        tents.append((y, x))
    for y, x in sorted(tents):
        sc = 0.5 + (y - 1040) / 260 * 0.7
        s += _tent(x, y, 70 * sc, 56 * sc, TENT_COLS[int(x) % 3], lit=(pal == "night" and r.random() < 0.6))
        if pal == "night" and r.random() < 0.35:
            s += (f'<circle cx="{x + 40 * sc:.0f}" cy="{y - 6:.0f}" r="{16 * sc:.0f}" fill="#ffb060" opacity="0.35" filter="url(#b6)"/>'
                  f'<path d="M {x + 34 * sc:.0f} {y:.0f} L {x + 40 * sc:.0f} {y - 16 * sc:.0f} L {x + 46 * sc:.0f} {y:.0f} Z" fill="#ffc870"/>')
        elif pal != "night" and r.random() < 0.15:
            s += f'<path d="M {x:.0f} {y - 60 * sc:.0f} C {x - 20:.0f} {y - 160:.0f}, {x + 30:.0f} {y - 220:.0f}, {x + 10:.0f} {y - 320:.0f}" stroke="#c8c0c8" stroke-width="{14 * sc:.0f}" fill="none" opacity="0.3" filter="url(#b6)"/>'
    # the meadow in front
    s += f'<path d="M -40 1330 C 300 1290, 700 1300, 1120 1320 L 1120 1940 L -40 1940 Z" fill="url(#smead)"/>'
    s += grass_tufts(1506, 1340, 1900, 70, col=g3, hi=g1)
    for x, y_, rr in ((90, 1700, 70), (980, 1650, 90), (300, 1880, 110)):
        s += boulder(x, y_, rr, seed=x + 3, col="#6a6a62" if pal != "night" else "#2a2a32", dark="#3a3a36" if pal != "night" else "#16161c",
                     lit="#9a9a8e" if pal != "night" else "#4a4a58")
    return svg_render(s)


def fort_yard(pal="day"):
    """inside the fortress: the back wall (top y 560) with the gate tower (x 400-680, a shut wooden gate, sill y 1270), blue banners with a
    gold sun on the tower, a well at the right (x 860), empty baskets and cracked jars at the left; packed earth from y 1270 (people stand at
    y 1330-1750). pal: day / dusk"""
    r = random.Random(1601)
    stone, shade, top = ("#b8a488", "#8a765e", "#d8c4a4") if pal == "day" else ("#8a7068", "#5e4a46", "#b08a78")
    s = "<defs>" + FILTERS + lg("ysky", SKY["day" if pal == "day" else "dusk"]) + lg("yground", [(0, "#8a7458" if pal == "day" else "#5e4c42", 1),
                                                                                                    (1, "#5a4a38" if pal == "day" else "#2e2622", 1)]) + "</defs>"
    s += f'<rect width="{W}" height="{H}" fill="url(#ysky)"/>'
    s += clouds(W, 1602, [360, 470], col="#ffffff" if pal == "day" else "#e08a7a", hi="#ffffff" if pal == "day" else "#ffd0a8", op=0.5)
    s += f'<path d="{ridge(W, 640, 120, 1603, rough=0.4)}" fill="{"#7a9a8a" if pal == "day" else "#4e4a62"}" opacity="0.8"/>'
    # the wall
    s += f'<rect x="-20" y="560" width="1120" height="720" fill="{stone}" stroke="#2a2018" stroke-width="3"/>'
    s += "".join(f'<rect x="{x}" y="532" width="40" height="30" fill="{stone}" stroke="#2a2018" stroke-width="2"/>' for x in range(-10, 1100, 70))
    y = 600
    while y < 1270:
        off = 0 if (y // 60) % 2 else 50
        s += f'<path d="M -20 {y} L 1100 {y}" stroke="{shade}" stroke-width="3" opacity="0.6"/>'
        s += "".join(f'<path d="M {x} {y} L {x} {y + 60}" stroke="{shade}" stroke-width="3" opacity="0.5"/>' for x in range(off, 1100, 100))
        y += 60
    # the gate tower
    s += (f'<rect x="400" y="420" width="280" height="850" fill="{stone}" stroke="#2a2018" stroke-width="3"/>'
          f'<rect x="400" y="420" width="70" height="850" fill="{shade}" opacity="0.5"/>'
          + "".join(f'<rect x="{x}" y="392" width="36" height="30" fill="{stone}" stroke="#2a2018" stroke-width="2"/>' for x in range(404, 680, 56)) +
          f'<path d="M 450 1270 L 450 1030 Q 540 930, 630 1030 L 630 1270 Z" fill="#5a3a22" stroke="#2a1a10" stroke-width="5"/>'
          f'<path d="M 540 960 L 540 1270" stroke="#2a1a10" stroke-width="5"/>'
          + "".join(f'<path d="M 452 {yy} L 628 {yy}" stroke="#3a2414" stroke-width="4"/>' for yy in (1060, 1130, 1200)) +
          f'<circle cx="515" cy="1150" r="9" fill="{GOLD}"/><circle cx="565" cy="1150" r="9" fill="{GOLD}"/>'
          f'<path d="M {440} 1000 Q 540 880, 640 1000" stroke="{top}" stroke-width="10" fill="none"/>')
    for bx in (430, 650):
        s += (f'<rect x="{bx - 3}" y="470" width="6" height="40" fill="#3a2a1a"/><path d="M {bx - 40} 505 L {bx + 40} 505 L {bx + 40} 760 L {bx} 730 L {bx - 40} 760 Z" '
              f'fill="#1e4a8a" stroke="#101828" stroke-width="3"/><circle cx="{bx}" cy="600" r="22" fill="{GOLD}"/>'
              + "".join(f'<path d="M {bx} 600 L {bx + 34 * math.cos(a):.0f} {600 + 34 * math.sin(a):.0f}" stroke="{GOLD}" stroke-width="4"/>'
                        for a in [k * math.pi / 4 for k in range(8)]))
    # the ground, the well, baskets and jars
    s += f'<rect x="-20" y="1270" width="1120" height="680" fill="url(#yground)"/>'
    s += f'<path d="M -20 1270 L 1100 1270" stroke="#3a2a1e" stroke-width="5"/>'
    for k in range(40):
        x = r.uniform(0, W); yy = r.uniform(1300, 1900)
        s += f'<ellipse cx="{x:.0f}" cy="{yy:.0f}" rx="{r.uniform(6, 20):.0f}" ry="{r.uniform(3, 7):.0f}" fill="#3a2e22" opacity="0.4"/>'
    s += (f'<ellipse cx="880" cy="1300" rx="110" ry="30" fill="#6a5a4a" stroke="#2a2018" stroke-width="3"/>'
          f'<path d="M 770 1300 L 770 1210 L 990 1210 L 990 1300" fill="{stone}" stroke="#2a2018" stroke-width="3"/>'
          f'<ellipse cx="880" cy="1210" rx="110" ry="28" fill="#2a2018" stroke="#2a2018" stroke-width="3"/>'
          f'<path d="M 790 1210 L 800 1060 L 960 1060 L 970 1210" stroke="#5a3a22" stroke-width="10" fill="none"/>'
          f'<path d="M 880 1060 L 880 1150" stroke="#8a6a42" stroke-width="4"/><rect x="866" y="1150" width="28" height="30" fill="#6a4a2a"/>')
    for x, yy, w in ((80, 1330, 90), (190, 1350, 70)):
        s += (f'<path d="M {x - w / 2} {yy - w * 0.7:.0f} L {x + w / 2} {yy - w * 0.7:.0f} L {x + w * 0.38:.0f} {yy} L {x - w * 0.38:.0f} {yy} Z" fill="#a8844e" stroke="#4a3418" stroke-width="3"/>'
              + "".join(f'<path d="M {x - w * 0.45:.0f} {yy - w * 0.7 + k * w * 0.16:.0f} L {x + w * 0.45:.0f} {yy - w * 0.7 + k * w * 0.16:.0f}" stroke="#7a5a2e" stroke-width="2"/>' for k in range(1, 5)))
    s += (f'<path d="M 300 1360 C 270 1330, 280 1280, 310 1270 L 340 1270 C 370 1280, 380 1330, 350 1360 Z" fill="#b5653a" stroke="#4a2a18" stroke-width="3"/>'
          f'<path d="M 312 1280 L 330 1310 L 322 1340" stroke="#3a1a0a" stroke-width="3" fill="none"/>'
          f'<path d="M 250 1390 C 230 1380, 230 1350, 250 1345 L 280 1345 C 300 1350, 300 1380, 280 1390 Z" fill="#9a5230" stroke="#4a2a18" stroke-width="3"/>')
    return svg_render(s)
