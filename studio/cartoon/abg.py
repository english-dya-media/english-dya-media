"""Painted backgrounds of Arash the Archer (SVG -> PNG; cache them with bgs.cached("ar_<name>", abg.<name>)).
Part 1: the besieged fortress in the green mountains of Tabaristan, with the tents of Turan all round (siege), and the yard inside
its walls (fort_yard)."""
import math, random
from film import svg_render, W, H
from bgs import FILTERS, lg, rg, ridge, hill, clouds, stars, grass_tufts, boulder, pine, _strata, poplar

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


def siege(pal="dawn", tents=True):
    """Tabaristan: misty green mountains; the Iranian fortress on a wooded hill in the middle (walls y 700-900, keep top FORT_TOP); the dark
    tents of Turan with red stripes and black-red pennants all round its foot (y 1000-1300, campfires at night); a meadow in front
    (people stand at y 1380-1750). pal: dawn / day / dusk / night. tents=False (part 3): the camp is gone, only trampled rings and the
    ashes of its fires are left"""
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
    tents_ = []
    for k in range(34):
        x = r.uniform(-40, 1120); y = r.uniform(1040, 1300)
        if 260 < x < 820 and y < 1110:
            continue
        tents_.append((y, x))
    for y, x in sorted(tents_):
        sc = 0.5 + (y - 1040) / 260 * 0.7
        if not tents:          # where a tent stood: a ring of flattened, paler grass; now and then the ashes of a fire
            s += f'<ellipse cx="{x:.0f}" cy="{y - 4:.0f}" rx="{38 * sc:.0f}" ry="{9 * sc:.0f}" fill="#b8b08a" opacity="0.35"/>'
            if r.random() < 0.3:
                s += f'<ellipse cx="{x + 40 * sc:.0f}" cy="{y - 2:.0f}" rx="{10 * sc:.0f}" ry="{4 * sc:.0f}" fill="#3a3430" opacity="0.6"/>'
            r.random()
            continue
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


# ---------------------------------------------------------------- part 2: the summit before sunrise; the old forest
SUMMIT = {   # sky stops, glow (east, at the right), far peaks (fill, snow, shade), cloud sea (hi, mid, lo), summit snow (lit, shade), rock
    "predawn": dict(sky=[(0, "#060a22", 1), (0.22, "#121a46", 1), (0.4, "#3a3270", 1), (0.5, "#8a4a78", 1), (0.56, "#e0866a", 1), (0.6, "#ffc890", 1)],
                    glow=("#ffd8a0", "#ff9a6a"), stars=True, peak=("#4a3e6e", "#c8b8e0", "#2e2850"), sea=("#e8c8d8", "#9a88b8", "#5a5084"),
                    snow=("#e4e0f2", "#8a88b6"), rock=("#2e2a40", "#1a1828", "#5a5470"), sun=None),
    "sunrise": dict(sky=[(0, "#1e3a7a", 1), (0.26, "#4a6aa8", 1), (0.42, "#c88aa0", 1), (0.5, "#ffb07a", 1), (0.56, "#ffd890", 1), (0.6, "#fff0c0", 1)],
                    glow=("#fff4d0", "#ffb060"), stars=False, peak=("#8a6a8a", "#fff0e0", "#5a4a6a"), sea=("#fff4ec", "#f0c8b8", "#b08aa8"),
                    snow=("#fff6ee", "#c0a8c8"), rock=("#4a3a48", "#2a2030", "#8a7088"), sun=(905, 1120, 70)),
}
SUMMIT_FLOOR = 1300     # the top of the summit (x 540); summit_y(x) is the snow line people stand on


def summit_y(x):
    """y of the summit's top edge at x (people stand on it; it falls away to both sides)"""
    return SUMMIT_FLOOR + 3.86e-4 * (x - 540) ** 2


def summit(pal="predawn"):
    """the snowy top of the great mountain above a sea of cloud before sunrise: the east (where the sun comes up) is at the right; far peaks
    stand out of the clouds (y 940-1150); the summit's snow line runs through summit_y(x) (y 1300 at x 540, 1430 at the edges): people stand
    on it at y 1300-1360; rocks and snow fall away below. pal: predawn / sunrise (part 3)"""
    p = SUMMIT[pal]
    r = random.Random(2201)
    s = "<defs>" + FILTERS + lg("msky", p["sky"]) + rg("mglow", 920, 1110, 900, [(0, p["glow"][0], 0.85), (0.25, p["glow"][1], 0.45), (1, p["glow"][1], 0)])
    s += lg("msea", [(0, p["sea"][1], 1), (1, p["sea"][2], 1)]) + lg("msnow", [(0, p["snow"][0], 1), (1, p["snow"][1], 1)])
    s += '<clipPath id="mshade"><rect x="-60" y="0" width="420" height="1940"/></clipPath>' + "</defs>"
    s += f'<rect width="{W}" height="{H}" fill="url(#msky)"/>'
    if p["stars"]:
        s += stars(2202, 170, 720)
        s += '<circle cx="190" cy="330" r="3.5" fill="#ffffff"/><circle cx="190" cy="330" r="14" fill="#cfd8ff" opacity="0.3" filter="url(#b6)"/>'   # the morning star
    s += f'<rect width="{W}" height="{H}" fill="url(#mglow)"/>'
    s += clouds(W, 2203, [760, 860], col=p["glow"][1], hi=p["glow"][0], op=0.4)
    if p["sun"]:
        sx, sy, sr_ = p["sun"]
        s += (f'<circle cx="{sx}" cy="{sy}" r="{sr_ * 3.2:.0f}" fill="#fff0c0" opacity="0.35" filter="url(#b40)"/>'
              f'<circle cx="{sx}" cy="{sy}" r="{sr_}" fill="#fff8e0"/>')
    # far peaks above the clouds, lit from the right
    for k, (cx, top, w) in enumerate(((150, 960, 300), (420, 1010, 240), (760, 985, 280), (1010, 1030, 220))):
        s += (f'<path d="M {cx - w} 1160 L {cx - w * 0.2:.0f} {top + 40} L {cx:.0f} {top} L {cx + w * 0.25:.0f} {top + 50} L {cx + w} 1160 Z" fill="{p["peak"][0]}"/>'
              f'<path d="M {cx:.0f} {top} L {cx + w * 0.25:.0f} {top + 50} L {cx + w * 0.45:.0f} {top + 90} L {cx + w * 0.2:.0f} {top + 80} L {cx + w * 0.05:.0f} {top + 110} '
              f'L {cx - w * 0.1:.0f} {top + 70} L {cx - w * 0.2:.0f} {top + 40} Z" fill="{p["peak"][1]}" opacity="0.9"/>'
              f'<path d="M {cx - w} 1160 L {cx - w * 0.2:.0f} {top + 40} L {cx:.0f} {top} L {cx - w * 0.05:.0f} 1160 Z" fill="{p["peak"][2]}" opacity="0.55"/>')
    # the sea of cloud
    s += f'<rect x="0" y="1110" width="{W}" height="{H - 1110}" fill="url(#msea)"/>'
    for row in range(4):
        y = 1085 + row * 42; x = -140
        while x < W + 140:
            rx = r.uniform(70, 160) * (1 + row * 0.25); ry = rx * r.uniform(0.3, 0.42)
            lit = p["sea"][0] if x > 520 else p["sea"][1]
            s += f'<ellipse cx="{x:.0f}" cy="{y + r.uniform(-10, 12):.0f}" rx="{rx:.0f}" ry="{ry:.0f}" fill="{lit}" opacity="{0.55 + 0.1 * row:.2f}" filter="url(#b6)"/>'
            x += rx * r.uniform(0.9, 1.3)
    # the summit: rock below, snow on top; its top edge is summit_y(x)
    top = [(x, summit_y(x)) for x in range(-60, 1141, 40)]
    rock = "M -60 1940 L " + " L ".join(f"{x:.0f} {y + 40:.0f}" for x, y in top) + " L 1140 1940 Z"
    s += f'<path d="{rock}" fill="{p["rock"][0]}"/>'
    for k in range(16):           # strata and cracks in the rock face
        y0 = r.uniform(1420, 1900); x0 = r.uniform(-40, 1000)
        s += f'<path d="M {x0:.0f} {y0:.0f} l {r.uniform(80, 260):.0f} {r.uniform(-30, 30):.0f}" stroke="{p["rock"][1]}" stroke-width="{r.uniform(3, 7):.1f}" opacity="0.7"/>'
    # the snow comes down in soft tongues between the rocks (smoothed)
    from chars import smooth_path
    edge = [(1140, summit_y(1140) + 90)]
    for k, x in enumerate(range(1100, -61, -60)):
        edge.append((x, summit_y(x) + 70 + 110 * (0.5 + 0.5 * math.sin(k * 1.9)) + r.uniform(0, 50)))
    edge.append((-60, summit_y(-60) + 120))
    pts = [(x, y - 3) for x, y in top] + edge
    snow = smooth_path(pts)
    s += f'<path d="{snow}" fill="url(#msnow)"/>'
    s += f'<path d="{snow}" fill="{p["snow"][1]}" opacity="0.35" clip-path="url(#mshade)"/>'
    s += "".join(f'<path d="M {x:.0f} {summit_y(x) + 2:.0f} q 30 -6 60 0" stroke="#ffffff" stroke-width="5" opacity="0.6" fill="none"/>' for x in range(-40, 1100, 130))
    for i, (x, rr) in enumerate(((60, 70), (1010, 80), (250, 46), (860, 52), (130, 120), (980, 130))):
        y = summit_y(x) + (30 if rr < 100 else 260)
        s += boulder(x, y, rr, seed=2210 + i, col=p["rock"][0], dark=p["rock"][1], lit=p["rock"][2])
        s += f'<path d="M {x - rr * 0.9:.0f} {y - rr * 0.55:.0f} Q {x:.0f} {y - rr * 0.95:.0f} {x + rr * 0.8:.0f} {y - rr * 0.5:.0f}" stroke="{p["snow"][0]}" stroke-width="{rr * 0.18:.0f}" fill="none" stroke-linecap="round"/>'
    s += f'<rect x="0" y="{SUMMIT_FLOOR - 60}" width="{W}" height="120" fill="{p["sea"][0]}" opacity="0.08" filter="url(#b20)"/>'
    return svg_render(s)


FOREST_OLD = dict(sky="#c8d8c0", far=("#5a7a6a", "#7a9a86"), mid=("#2e4a3a", "#3e5e48"), floor=("#4a5a2e", "#2a3a1e"), bark=("#4e4036", "#2e241e", "#7a6a5a"),
                  moss="#5a7a32", ray="#fff4c8", leaf=("#1e3424", "#2e4a2e", "#4a6a36"))
OLD_TREE_X = (130, 470)      # the old tree's trunk in old_forest() (at the ground, y 1320)


def old_forest():
    """the old forest of Tabaristan in the morning: misty trunks behind, light falling from the upper right, the oldest tree at the left (its
    trunk x 130-470, roots spread at the ground y 1320, the canopy over the top of the frame); moss and ferns; people stand at y 1360-1700"""
    P = FOREST_OLD
    r = random.Random(2301)
    s = "<defs>" + FILTERS + lg("fsky", [(0, P["sky"], 1), (1, "#9ab49a", 1)]) + lg("ffloor", [(0, P["floor"][0], 1), (1, P["floor"][1], 1)])
    s += lg("fbark", [(0, P["bark"][1], 1), (0.35, P["bark"][0], 1), (0.75, P["bark"][2], 1), (1, P["bark"][0], 1)], vertical=False) + "</defs>"
    s += f'<rect width="{W}" height="{H}" fill="url(#fsky)"/>'
    # misty trunks far away, then nearer
    for layer, (col, n, w0, op) in enumerate(((P["far"][1], 14, 26, 0.55), (P["far"][0], 10, 44, 0.75), (P["mid"][1], 7, 70, 0.95))):
        for k in range(n):
            x = r.uniform(380, 1100); w = w0 * r.uniform(0.8, 1.3)
            s += f'<path d="M {x - w / 2:.0f} 1340 L {x - w * 0.42:.0f} -20 L {x + w * 0.42:.0f} -20 L {x + w / 2:.0f} 1340 Z" fill="{col}" opacity="{op}"/>'
        s += f'<rect x="0" y="0" width="{W}" height="1400" fill="#dfe8d8" opacity="{0.22 - 0.06 * layer:.2f}"/>'
    # the forest floor
    s += f'<path d="M -40 1300 C 300 1280, 700 1300, 1120 1290 L 1120 1940 L -40 1940 Z" fill="url(#ffloor)"/>'
    s += grass_tufts(2302, 1310, 1900, 50, col=P["leaf"][0], hi=P["leaf"][2])
    for k in range(9):        # ferns
        x = r.uniform(-20, 1100); y = r.uniform(1450, 1900); h = 60 + (y - 1400) * 0.25
        for j in range(7):
            a = math.radians(-160 + j * 23)
            s += (f'<path d="M {x:.0f} {y:.0f} Q {x + math.cos(a) * h * 0.6:.0f} {y + math.sin(a) * h * 0.9 - 20:.0f} {x + math.cos(a) * h:.0f} {y + math.sin(a) * h * 0.6:.0f}" '
                  f'stroke="{P["leaf"][1 + j % 2]}" stroke-width="{4 + h / 40:.1f}" fill="none" stroke-linecap="round"/>')
    # the oldest tree: a huge trunk with buttress roots, moss, knots; its canopy hangs over the top
    x0, x1 = OLD_TREE_X
    trunk = (f"M {x0 - 120} 1330 C {x0 - 40} 1300, {x0 - 10} 1250, {x0 + 10} 1150 C {x0 + 30} 900, {x0 - 10} 500, {x0 + 20} 120 "
             f"C {x0 + 40} -40, {x1 - 60} -40, {x1 - 40} 120 C {x1 - 10} 500, {x1 - 40} 900, {x1 - 30} 1150 C {x1 - 20} 1250, {x1 + 40} 1300, {x1 + 150} 1335 "
             f"C {x1 + 40} 1345, {x1 - 40} 1342, {(x0 + x1) / 2 + 40:.0f} 1336 C {x0 + 80} 1342, {x0 - 40} 1345, {x0 - 120} 1330 Z")
    s += f'<path d="{trunk}" fill="url(#fbark)" stroke="#1b120c" stroke-width="5"/>'
    for k in range(13):       # deep bark furrows
        xx = lerp_(x0 + 30, x1 - 40, k / 12) + r.uniform(-8, 8)
        s += (f'<path d="M {xx:.0f} {r.uniform(60, 200):.0f} C {xx + r.uniform(-30, 30):.0f} 500, {xx + r.uniform(-30, 30):.0f} 900, {xx + r.uniform(-20, 20):.0f} {r.uniform(1150, 1300):.0f}" '
              f'stroke="{P["bark"][1]}" stroke-width="{r.uniform(4, 9):.1f}" fill="none" opacity="0.7"/>')
    s += (f'<ellipse cx="{x0 + 190}" cy="1010" rx="34" ry="52" fill="{P["bark"][1]}" stroke="#1b120c" stroke-width="4"/>'
          f'<ellipse cx="{x0 + 190}" cy="1012" rx="18" ry="30" fill="#120c08"/>')
    for k in range(10):       # moss
        yy = r.uniform(700, 1300); xx = x0 + r.uniform(0, 120)
        s += f'<ellipse cx="{xx:.0f}" cy="{yy:.0f}" rx="{r.uniform(18, 40):.0f}" ry="{r.uniform(40, 90):.0f}" fill="{P["moss"]}" opacity="0.55"/>'
    for sd, (rx, ry) in ((-1, (x0 - 130, 1340)), (1, (x1 + 160, 1342)), (1, (x1 + 60, 1350))):      # roots
        s += f'<path d="M {(x0 + x1) / 2:.0f} 1300 C {rx - sd * 60:.0f} 1290, {rx:.0f} 1320, {rx + sd * 40:.0f} 1350" stroke="{P["bark"][0]}" stroke-width="34" fill="none" stroke-linecap="round"/>'
    # its canopy across the top, and some leaves of nearer trees at the right
    for col, dy, k in ((P["leaf"][0], 0, 1.0), (P["leaf"][1], -20, 0.8), (P["leaf"][2], -40, 0.5)):
        rr = random.Random(2303)
        for j in range(26):
            cx = rr.uniform(-120, 1000); cy = rr.uniform(-80, 260) + dy
            s += f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{rr.uniform(90, 170) * k:.0f}" fill="{col}"/>'
    # light falling from the upper right
    for k, (xa, wa) in enumerate(((760, 90), (900, 60), (620, 50), (1000, 110))):
        s += (f'<path d="M {xa:.0f} 200 L {xa + wa:.0f} 200 L {xa - 420 + wa * 2:.0f} 1500 L {xa - 420:.0f} 1500 Z" fill="{P["ray"]}" opacity="{0.10 + 0.03 * (k % 2):.2f}" '
              f'filter="url(#b20)"/>')
    s += f'<ellipse cx="560" cy="1340" rx="420" ry="40" fill="{P["ray"]}" opacity="0.12" filter="url(#b20)"/>'
    return svg_render(s)


def lerp_(a, b, u):
    return a + (b - a) * u


FORGE_FIRE = (240, 1010)     # the glowing coals of forge()
FORGE_FLOOR = 1160           # the foot of the back wall; people stand at y 1200-1400


def forge():
    """the royal smithy at night: stone walls, the forge at the left (a brick hearth with glowing coals at FORGE_FIRE under a hood that goes
    up into the dark, the bellows beside it), tongs and hammers on the wall at the right, a small window with the night sky, a water barrel;
    a packed earth floor from FORGE_FLOOR (people stand at y 1200-1400, the anvil is drawn by the scenes)"""
    r = random.Random(2401)
    fx, fy = FORGE_FIRE
    s = "<defs>" + FILTERS + lg("kwall", [(0, "#2a2024", 1), (1, "#4a3830", 1)]) + lg("kfloor", [(0, "#4a3426", 1), (1, "#1e1410", 1)])
    s += rg("kglow", fx, fy, 900, [(0, "#ffb060", 0.75), (0.25, "#e06a2a", 0.35), (1, "#000000", 0)]) + "</defs>"
    s += f'<rect width="{W}" height="{H}" fill="url(#kwall)"/>'
    # stone blocks
    y = 40
    while y < FORGE_FLOOR:
        off = 0 if (y // 90) % 2 else 70
        for x in range(-70 + off, W + 70, 140):
            s += f'<rect x="{x + 3}" y="{y + 3}" width="{134}" height="{84}" rx="10" fill="#3a2e2c" stroke="#1a1214" stroke-width="4" opacity="{r.uniform(0.6, 1.0):.2f}"/>'
        y += 90
    # the window with the night sky
    s += ('<path d="M 780 560 L 780 420 Q 850 340, 920 420 L 920 560 Z" fill="#0e1636" stroke="#1a1214" stroke-width="8"/>'
          '<circle cx="880" cy="430" r="3" fill="#ffffff"/><circle cx="820" cy="470" r="2" fill="#dfe6ff"/><circle cx="860" cy="520" r="2" fill="#dfe6ff"/>'
          '<path d="M 850 360 L 850 560 M 780 470 L 920 470" stroke="#2a1e1a" stroke-width="7"/>')
    # tools on the wall
    for k, x in enumerate((640, 720, 800, 880, 960)):
        s += f'<circle cx="{x}" cy="690" r="7" fill="#6a5a4a"/>'
        if k % 2 == 0:      # tongs
            s += (f'<path d="M {x} 696 L {x - 14} 900 M {x} 696 L {x + 14} 900" stroke="#2a2a30" stroke-width="9" stroke-linecap="round"/>'
                  f'<path d="M {x - 14} 900 L {x - 4} 930 M {x + 14} 900 L {x + 4} 930" stroke="#2a2a30" stroke-width="7"/>')
        else:               # hammers
            s += (f'<path d="M {x} 696 L {x} 880" stroke="#5a3a1c" stroke-width="10"/>'
                  f'<rect x="{x - 30}" y="870" width="60" height="34" rx="6" fill="#3a3a44" stroke="#14141a" stroke-width="4"/>')
    s += ''.join(f'<path d="M {x - 26} 980 A 26 26 0 1 1 {x + 26} 980" stroke="#4a4a52" stroke-width="10" fill="none"/>' for x in (690, 790, 890))
    # the hearth: brick body, coals, the hood above
    s += (f'<path d="M 20 {FORGE_FLOOR} L 20 1040 L 470 1040 L 470 {FORGE_FLOOR} Z" fill="#6a3a28" stroke="#1a0e0a" stroke-width="5"/>'
          + "".join(f'<path d="M 20 {yy} L 470 {yy}" stroke="#3a1e14" stroke-width="3"/>' for yy in (1080, 1120)) +
          f'<path d="M 40 1040 L 450 1040 L 430 {fy - 40} L 60 {fy - 40} Z" fill="#2a1410"/>'
          f'<ellipse cx="{fx}" cy="{fy}" rx="180" ry="34" fill="#ff7a1a"/>'
          f'<ellipse cx="{fx}" cy="{fy - 4}" rx="130" ry="22" fill="#ffc040"/>'
          f'<ellipse cx="{fx}" cy="{fy - 6}" rx="70" ry="12" fill="#fff0a0"/>')
    for k in range(22):
        x = fx + r.uniform(-170, 170); yy = fy + r.uniform(-14, 20)
        s += f'<circle cx="{x:.0f}" cy="{yy:.0f}" r="{r.uniform(6, 14):.0f}" fill="{r.choice(["#3a1a10", "#ff9a30", "#c0401a"])}" opacity="0.8"/>'
    s += (f'<path d="M 60 {fy - 40} L 430 {fy - 40} L 360 600 L 130 600 Z" fill="#4a2a20" stroke="#1a0e0a" stroke-width="5"/>'
          f'<path d="M 130 600 L 360 600 L 330 -20 L 160 -20 Z" fill="#3a2018" stroke="#1a0e0a" stroke-width="5"/>'
          f'<path d="M 60 {fy - 40} L 430 {fy - 40}" stroke="#8a4a2a" stroke-width="10"/>'
          f'<path d="M 120 {fy - 70} L 380 {fy - 70} L 340 700 L 160 700 Z" fill="#ff8a3a" opacity="0.18" filter="url(#b20)"/>')
    # the bellows at the left
    s += ('<path d="M -30 1000 L 40 980 L 60 1030 L -30 1080 Z" fill="#6a4426" stroke="#1a0e0a" stroke-width="4"/>'
          '<path d="M -30 1000 C 10 960, 10 1110, -30 1080" fill="#8a5a32" stroke="#1a0e0a" stroke-width="4"/>')
    # the floor
    s += f'<rect x="0" y="{FORGE_FLOOR}" width="{W}" height="{H - FORGE_FLOOR}" fill="url(#kfloor)"/>'
    s += f'<path d="M 0 {FORGE_FLOOR} L {W} {FORGE_FLOOR}" stroke="#14100c" stroke-width="6"/>'
    for k in range(30):
        x = r.uniform(0, W); yy = r.uniform(FORGE_FLOOR + 20, 1900)
        s += f'<ellipse cx="{x:.0f}" cy="{yy:.0f}" rx="{r.uniform(8, 24):.0f}" ry="{r.uniform(3, 7):.0f}" fill="#120c08" opacity="0.4"/>'
    # the water barrel
    s += ('<path d="M 900 1140 L 1050 1140 L 1060 1330 L 890 1330 Z" fill="#5a3a20" stroke="#1a0e0a" stroke-width="5"/>'
          '<path d="M 895 1180 L 1055 1180 M 892 1290 L 1058 1290" stroke="#2a2a30" stroke-width="9"/>'
          '<ellipse cx="975" cy="1140" rx="75" ry="16" fill="#1a2a3a" stroke="#1a0e0a" stroke-width="4"/>')
    # the light of the fire on everything
    s += f'<rect width="{W}" height="{H}" fill="url(#kglow)"/>'
    return svg_render(s)


# ---------------------------------------------------------------- part 3: the desert, the great river Jeyhun and its walnut tree, Tirgan
def _dune_row(seed, base, amp, wmin, wmax, lit, shade, crest="#fff0c8"):
    """a row of dunes across the frame as one continuous surface (no seams): sharp crests, rounded valleys; the sun is at the right, so
    the face left of each crest is in shade"""
    r = random.Random(seed)
    pts = []                                   # alternating valley, crest, valley, …
    x = r.uniform(-400, -150)
    pts.append((x - 300, base + r.uniform(-10, 20)))
    while x < W + 300:
        w = r.uniform(wmin, wmax)
        pts.append((x, base + r.uniform(-10, 25)))
        pts.append((x + w * r.uniform(0.5, 0.66), base - amp * r.uniform(0.7, 1.1)))
        x += w
    pts.append((x, base + r.uniform(-10, 20)))
    d = f"M {pts[0][0]:.0f} {base + 900:.0f} L {pts[0][0]:.0f} {pts[0][1]:.0f}"
    for i in range(1, len(pts)):
        (xa, ya), (xb, yb) = pts[i - 1], pts[i]
        if yb < ya:      # up to a crest: steep at the end (sharp crest)
            d += f" C {xa + (xb - xa) * 0.5:.0f} {ya:.0f}, {xb - (xb - xa) * 0.2:.0f} {yb + (ya - yb) * 0.15:.0f}, {xb:.0f} {yb:.0f}"
        else:            # down from a crest into the valley: rounded
            d += f" C {xa + (xb - xa) * 0.25:.0f} {ya + (yb - ya) * 0.2:.0f}, {xb - (xb - xa) * 0.45:.0f} {yb:.0f}, {xb:.0f} {yb:.0f}"
    d += f" L {pts[-1][0]:.0f} {base + 900:.0f} Z"
    o = f'<path d="{d}" fill="{lit}"/>'
    for i in range(2, len(pts) - 1, 2):       # the shaded face left of each crest
        (vx, vy), (cx, cy) = pts[i - 1], pts[i]
        fx, fy = cx - (cx - vx) * 0.12, base + amp * 0.35 + 50
        o += (f'<path d="M {cx:.0f} {cy:.0f} C {cx - (cx - vx) * 0.2:.0f} {cy + (vy - cy) * 0.15:.0f}, {vx + (cx - vx) * 0.5:.0f} {vy:.0f}, {vx:.0f} {vy:.0f} '
              f'C {vx + (fx - vx) * 0.45:.0f} {vy + 10:.0f}, {fx - 40:.0f} {fy:.0f}, {fx:.0f} {fy:.0f} C {cx - 20:.0f} {cy + (fy - cy) * 0.5:.0f}, '
              f'{cx - 6:.0f} {cy + 30:.0f}, {cx:.0f} {cy:.0f} Z" fill="{shade}" opacity="0.8"/>')
        o += (f'<path d="M {cx - (cx - vx) * 0.3:.0f} {cy + (vy - cy) * 0.08:.0f} Q {cx - 12:.0f} {cy:.0f} {cx:.0f} {cy:.0f} Q {cx + 40:.0f} {cy + 8:.0f} '
              f'{cx + 120:.0f} {cy + 40:.0f}" stroke="{crest}" stroke-width="3" fill="none" opacity="0.7"/>')
    return o


DESERT_SUN = (850, 430)


def desert():
    """the deserts on the way to Khorasan in the late morning: a hot pale sky with the sun high at the right (DESERT_SUN), far blue
    mountains on the horizon (y 960), golden dunes with sharp crests, their left slopes in shade, from y 980 to the bottom; a tiny caravan
    on a far crest; the arrow flies over it in the scenes (y 400-900)"""
    r = random.Random(3101)
    s = "<defs>" + FILTERS + lg("dsky", [(0, "#3e74b4", 1), (0.32, "#8cb6d6", 1), (0.48, "#e8e0c4", 1), (0.52, "#f4dcae", 1)])
    s += rg("dsun", DESERT_SUN[0], DESERT_SUN[1], 700, [(0, "#fffbe8", 0.9), (0.12, "#fff0c0", 0.45), (1, "#ffe0a0", 0)]) + "</defs>"
    s += f'<rect width="{W}" height="{H}" fill="url(#dsky)"/><rect width="{W}" height="{H}" fill="url(#dsun)"/>'
    s += f'<circle cx="{DESERT_SUN[0]}" cy="{DESERT_SUN[1]}" r="46" fill="#fffdf2"/>'
    s += clouds(W, 3102, [300, 520], col="#ffffff", hi="#ffffff", op=0.35)
    s += f'<path d="{ridge(W, 980, 120, 3103, rough=0.4)}" fill="#8a96b8" opacity="0.75"/>'
    s += f'<rect x="0" y="930" width="{W}" height="80" fill="#f8ecd0" opacity="0.4" filter="url(#b20)"/>'
    layers = [(990, 40, ("#e8c48a", "#c89a68")), (1060, 70, ("#e6b878", "#c08a58")), (1180, 110, ("#e2ac68", "#b47a48")),
              (1340, 150, ("#dca05a", "#a86c3c")), (1540, 190, ("#d6964e", "#9a6032")), (1760, 220, ("#d08c44", "#8a542a"))]
    for i, (base, amp, (lit, shade)) in enumerate(layers):
        s += _dune_row(3110 + i, base, amp, 380 * (1 + i * 0.25), 700 * (1 + i * 0.25), lit, shade)
        if i == 1:      # a tiny caravan on a far dune: camels and their drivers, dark in the haze
            for k in range(6):
                cx, cy = 300 + k * 26, 1030 + k * 1.5
                s += (f'<path d="M {cx - 9} {cy} L {cx - 8} {cy - 9} C {cx - 6} {cy - 16}, {cx + 2} {cy - 16}, {cx + 4} {cy - 10} L {cx + 9} {cy - 14} L {cx + 11} {cy - 12} '
                      f'L {cx + 7} {cy - 7} L {cx + 7} {cy} M {cx - 6} {cy} L {cx - 6} {cy - 5} M {cx + 4} {cy} L {cx + 4} {cy - 5}" stroke="#6a5a50" stroke-width="2" fill="#6a5a50"/>')
        for k in range(int(10 + 6 * i)):          # wind ripples on the sand
            xx = r.uniform(-20, W); yy = base + r.uniform(20, 200 + 40 * i)
            s += f'<path d="M {xx:.0f} {yy:.0f} q {20 + 8 * i:.0f} {-4 - i:.0f} {40 + 16 * i:.0f} 0" stroke="#fff0c8" stroke-width="{1.5 + 0.5 * i:.1f}" fill="none" opacity="0.35"/>'
    s += f'<rect x="0" y="960" width="{W}" height="200" fill="#fff4dc" opacity="0.18" filter="url(#b20)"/>'
    return svg_render(s)


WALNUT = (730, 985)          # the foot of the great walnut tree's trunk on the far bank in jeyhun()
WALNUT_HIT = (741, 912)      # where the arrow strikes its trunk


def walnut_tree(x, y, h, seed=0, leaf=("#2e4a22", "#3e5e2a", "#5a7a36"), bark=("#8a8074", "#5a5248", "#b0a698")):
    """a great walnut tree: a short thick pale trunk forking into big limbs, a wide round crown of dark leaves; foot of the trunk at (x, y)"""
    r = random.Random(seed)
    tw = h * 0.07
    o = (f'<path d="M {x - tw * 1.4:.0f} {y:.0f} C {x - tw:.0f} {y - h * 0.15:.0f}, {x - tw * 0.9:.0f} {y - h * 0.3:.0f}, {x - tw * 1.3:.0f} {y - h * 0.42:.0f} '
         f'L {x - tw * 3.2:.0f} {y - h * 0.62:.0f} L {x - tw * 2.4:.0f} {y - h * 0.66:.0f} L {x - tw * 0.3:.0f} {y - h * 0.46:.0f} L {x + tw * 0.2:.0f} {y - h * 0.7:.0f} '
         f'L {x + tw * 1.0:.0f} {y - h * 0.7:.0f} L {x + tw * 0.8:.0f} {y - h * 0.46:.0f} L {x + tw * 2.8:.0f} {y - h * 0.64:.0f} L {x + tw * 3.4:.0f} {y - h * 0.58:.0f} '
         f'L {x + tw * 1.2:.0f} {y - h * 0.4:.0f} C {x + tw * 0.9:.0f} {y - h * 0.3:.0f}, {x + tw:.0f} {y - h * 0.15:.0f}, {x + tw * 1.5:.0f} {y:.0f} Z" '
         f'fill="{bark[0]}" stroke="#2a241e" stroke-width="{max(2, h * 0.006):.1f}"/>'
         f'<path d="M {x - tw * 0.4:.0f} {y:.0f} C {x - tw * 0.2:.0f} {y - h * 0.2:.0f}, {x - tw * 0.6:.0f} {y - h * 0.3:.0f}, {x - tw * 0.9:.0f} {y - h * 0.4:.0f}" '
         f'stroke="{bark[1]}" stroke-width="{max(2, h * 0.012):.1f}" fill="none" opacity="0.6"/>'
         f'<path d="M {x + tw * 0.5:.0f} {y:.0f} C {x + tw * 0.6:.0f} {y - h * 0.2:.0f}, {x + tw * 0.5:.0f} {y - h * 0.3:.0f}, {x + tw * 0.7:.0f} {y - h * 0.4:.0f}" '
         f'stroke="{bark[2]}" stroke-width="{max(2, h * 0.01):.1f}" fill="none" opacity="0.6"/>')
    blobs = []
    for k in range(26):
        a = r.uniform(0, 2 * math.pi); d = r.uniform(0, 1) ** 0.6
        bx = x + math.cos(a) * d * h * 0.5; by = y - h * 0.74 + math.sin(a) * d * h * 0.22
        blobs.append((by, bx, h * r.uniform(0.1, 0.17)))
    for by, bx, rr in sorted(blobs):
        o += f'<circle cx="{bx:.0f}" cy="{by:.0f}" r="{rr:.0f}" fill="{leaf[0]}"/>'
    for by, bx, rr in sorted(blobs)[:16]:
        o += f'<circle cx="{bx + rr * 0.2:.0f}" cy="{by - rr * 0.25:.0f}" r="{rr * 0.75:.0f}" fill="{leaf[1]}"/>'
    for by, bx, rr in sorted(blobs)[:9]:
        o += f'<circle cx="{bx + rr * 0.35:.0f}" cy="{by - rr * 0.4:.0f}" r="{rr * 0.45:.0f}" fill="{leaf[2]}" opacity="0.8"/>'
    o += f'<ellipse cx="{x:.0f}" cy="{y - h * 0.5:.0f}" rx="{h * 0.36:.0f}" ry="{h * 0.07:.0f}" fill="#16220e" opacity="0.35"/>'
    return o


def jeyhun(pal="noon"):
    """the great river Jeyhun (the Oxus) at the far edge of Khorasan, at noon, from the near bank: pale mountains far away, the far bank
    (y 900-1000) with poplars and the great walnut tree (trunk foot WALNUT; its crown x 520-940, y 610-900), the wide river (y 1000-1400)
    glittering under the sun, the near bank of sand and grass with reeds at both sides (riders and people at y 1450-1800)"""
    r = random.Random(3201)
    s = "<defs>" + FILTERS + lg("jsky", [(0, "#3a72b8", 1), (0.35, "#8ec0e0", 1), (0.5, "#e4eedc", 1)])
    s += lg("jriv", [(0, "#a8c8c0", 1), (0.25, "#5a9098", 1), (1, "#2e5a66", 1)]) + lg("jbank", [(0, "#c8b080", 1), (1, "#8a7048", 1)]) + "</defs>"
    s += f'<rect width="{W}" height="{H}" fill="url(#jsky)"/>'
    s += clouds(W, 3202, [260, 420, 560], col="#ffffff", hi="#ffffff", op=0.55)
    s += f'<path d="{ridge(W, 900, 150, 3203, rough=0.45)}" fill="#a8b4cc" opacity="0.8"/>'
    s += f'<path d="{ridge(W, 930, 80, 3204, rough=0.35)}" fill="#8aa0a8" opacity="0.8"/>'
    s += f'<rect x="0" y="860" width="{W}" height="90" fill="#ffffff" opacity="0.25" filter="url(#b20)"/>'
    # the far bank: a strip of green steppe, poplars, the great walnut tree
    s += f'<path d="M -40 1004 C 200 990, 500 996, 760 990 C 900 986, 1000 992, 1120 988 L 1120 920 C 900 930, 600 914, 300 924 C 150 928, 40 920, -40 926 Z" fill="#7a9a52"/>'
    s += f'<path d="M -40 1004 C 200 990, 500 996, 760 990 C 900 986, 1000 992, 1120 988 L 1120 1004 Z" fill="#a89a6a"/>'
    for px in (60, 110, 170, 980, 1030):
        s += poplar(px, 960 + r.uniform(-6, 6), r.uniform(110, 160), col="#4a6a36", dark="#33502a")
    for k in range(8):
        bx = r.uniform(250, 520) if k < 4 else r.uniform(920, 1060)
        s += f'<circle cx="{bx:.0f}" cy="{962 + r.uniform(-6, 6):.0f}" r="{r.uniform(14, 26):.0f}" fill="#4e6a34"/>'
    s += walnut_tree(WALNUT[0], WALNUT[1], 400, seed=3205)
    # the river
    s += f'<rect x="-20" y="1000" width="1120" height="420" fill="url(#jriv)"/>'
    for k in range(90):                      # the sun on the water, a glittering path, and small waves everywhere
        y = r.uniform(1004, 1400); w = r.uniform(16, 90) * (0.5 + (y - 1000) / 400)
        x = 820 + r.gauss(0, 40 + (y - 1000) * 0.35)
        s += f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{w:.0f}" ry="{1.5 + (y - 1000) / 160:.1f}" fill="#fffbe8" opacity="{r.uniform(0.3, 0.75):.2f}"/>'
    for k in range(60):
        y = r.uniform(1010, 1400); x = r.uniform(-20, W)
        s += f'<path d="M {x:.0f} {y:.0f} q {20 + (y - 1000) / 8:.0f} {-3 - (y - 1000) / 120:.0f} {40 + (y - 1000) / 4:.0f} 0" stroke="#d8ecec" stroke-width="{1.5 + (y - 1000) / 200:.1f}" fill="none" opacity="0.35"/>'
    s += '<rect x="0" y="996" width="1080" height="24" fill="#e8f0e0" opacity="0.35" filter="url(#b6)"/>'
    # the near bank
    s += f'<path d="M -40 1420 C 200 1396, 500 1410, 760 1400 C 900 1394, 1020 1404, 1120 1398 L 1120 1940 L -40 1940 Z" fill="url(#jbank)"/>'
    s += f'<path d="M -40 1420 C 200 1396, 500 1410, 760 1400 C 900 1394, 1020 1404, 1120 1398" stroke="#e8dcb8" stroke-width="6" fill="none" opacity="0.6"/>'
    s += grass_tufts(3206, 1440, 1900, 40, col="#6a7a3a", hi="#9aaa5a")
    for side in (-1, 1):                      # reeds at both edges
        for k in range(26):
            x = (r.uniform(-30, 160) if side < 0 else r.uniform(920, 1110)); h = r.uniform(160, 360)
            yb = r.uniform(1400, 1560); lean = r.uniform(-30, 30)
            s += f'<path d="M {x:.0f} {yb:.0f} q {lean * 0.4:.0f} {-h * 0.5:.0f} {lean:.0f} {-h:.0f}" stroke="{r.choice(["#5a6a2e", "#6a7a38", "#4a5a26"])}" stroke-width="{r.uniform(4, 8):.1f}" fill="none" stroke-linecap="round"/>'
            if k % 3 == 0:
                s += f'<ellipse cx="{x + lean:.0f}" cy="{yb - h - 14:.0f}" rx="7" ry="22" fill="#7a5a32" transform="rotate({lean * 0.6:.0f},{x + lean:.0f},{yb - h - 14:.0f})"/>'
    return svg_render(s)


WALNUT_ARROW = (600, 760)    # where the arrow's head is buried in the trunk in walnut_close()


def walnut_close():
    """close on the great walnut tree's trunk (x 430-760) at noon: pale grey bark with long furrows, a big limb forking up at the left,
    pinnate leaves and green walnuts hanging from the top; behind, the bright river and the far bank, soft; the arrow is drawn by the
    scenes at WALNUT_ARROW"""
    r = random.Random(3301)
    s = "<defs>" + FILTERS + lg("wsky", [(0, "#5a8ec4", 1), (0.45, "#b8d4e4", 1), (0.6, "#e8eedc", 1)])
    s += lg("wbark", [(0, "#5e564c", 1), (0.35, "#8a8276", 1), (0.7, "#a8a092", 1), (1, "#6a6258", 1)], vertical=False) + "</defs>"
    # the soft background: sky, the far plain, the bright river
    back = f'<rect width="{W}" height="{H}" fill="url(#wsky)"/>'
    back += f'<rect x="0" y="1150" width="{W}" height="120" fill="#8aa868"/>'
    back += f'<rect x="0" y="1270" width="{W}" height="700" fill="#4a8890"/>'
    for k in range(40):
        y = r.uniform(1280, 1900); x = r.uniform(0, W)
        back += f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{r.uniform(30, 120):.0f}" ry="4" fill="#f8f4e0" opacity="{r.uniform(0.3, 0.7):.2f}"/>'
    s += f'<g filter="url(#b12)">{back}</g>'
    # the trunk and a big limb
    s += ('<path d="M 430 1960 C 450 1500, 470 1100, 440 760 C 420 560, 300 380, 180 200 L 300 150 C 400 300, 480 460, 520 600 '
          'C 560 420, 600 220, 620 -40 L 760 -40 C 740 300, 720 700, 760 1100 C 780 1500, 770 1800, 790 1960 Z" fill="url(#wbark)" stroke="#2a241e" stroke-width="6"/>')
    for k in range(16):                     # long furrows in the bark
        x0 = r.uniform(460, 740)
        s += (f'<path d="M {x0:.0f} {r.uniform(1500, 1940):.0f} C {x0 + r.uniform(-20, 20):.0f} 1300, {x0 + r.uniform(-30, 30):.0f} 1000, {x0 + r.uniform(-20, 40):.0f} {r.uniform(200, 800):.0f}" '
              f'stroke="#4a443c" stroke-width="{r.uniform(3, 7):.1f}" fill="none" opacity="0.55"/>')
    for k in range(10):
        x0 = r.uniform(470, 730); y0 = r.uniform(300, 1800)
        s += f'<path d="M {x0:.0f} {y0:.0f} l {r.uniform(-8, 8):.0f} {r.uniform(60, 160):.0f}" stroke="#c8c0b2" stroke-width="3" opacity="0.5"/>'
    s += '<ellipse cx="660" cy="1240" rx="22" ry="34" fill="#4a443c" stroke="#2a241e" stroke-width="4"/>'
    # leaves: pinnate leaves hanging from above, green walnuts
    def leaf(x, y, ang, sc, col):
        o = f'<g transform="translate({x:.0f},{y:.0f}) rotate({ang:.0f}) scale({sc:.2f})"><path d="M 0 0 L 0 260" stroke="#4a5a2a" stroke-width="5"/>'
        for j in range(4):
            for sd in (-1, 1):
                yy = 40 + j * 60
                o += f'<ellipse cx="{sd * 46}" cy="{yy}" rx="44" ry="20" fill="{col}" stroke="#1e2a12" stroke-width="3" transform="rotate({sd * 25},{sd * 46},{yy})"/>'
        o += f'<ellipse cx="0" cy="290" rx="22" ry="44" fill="{col}" stroke="#1e2a12" stroke-width="3"/></g>'
        return o
    for k in range(18):
        x = r.uniform(-60, 1140); y = r.uniform(-80, 240)
        s += leaf(x, y, r.uniform(-50, 50), r.uniform(0.7, 1.1), r.choice(["#3e6a2a", "#4e7a32", "#2e5a22"]))
    for x, y in ((140, 300), (210, 330), (880, 280), (930, 320)):
        s += f'<circle cx="{x}" cy="{y}" r="30" fill="#6a8a3a" stroke="#1e2a12" stroke-width="3"/><circle cx="{x - 9}" cy="{y - 10}" r="9" fill="#9ab85a" opacity="0.7"/>'
    s += f'<rect width="{W}" height="{H}" fill="#fff8e0" opacity="0.06"/>'
    return svg_render(s)


def tirgan():
    """a village stream on Tirgan, in early summer: mud-brick houses with flat roofs and poplars on the far side, a willow at the left, the
    stream across the middle (water y 1190-1330, stones), green grass in front (children stand at y 1400-1560)"""
    r = random.Random(3401)
    s = "<defs>" + FILTERS + lg("tsky", [(0, "#3a7ac4", 1), (0.4, "#9cc8e4", 1), (0.55, "#eef2dc", 1)])
    s += lg("twat", [(0, "#8ac0c8", 1), (1, "#3a7a86", 1)]) + lg("tgrass", [(0, "#7aa846", 1), (1, "#4a7a2a", 1)]) + "</defs>"
    s += f'<rect width="{W}" height="{H}" fill="url(#tsky)"/>'
    s += clouds(W, 3402, [300, 460], col="#ffffff", hi="#ffffff", op=0.6)
    s += f'<path d="{ridge(W, 930, 130, 3403, rough=0.4)}" fill="#9ab0b8" opacity="0.8"/>'
    s += f'<path d="{hill(W, 1010, 90, 3404)}" fill="#8aa860"/>'
    # the village on the far side
    for k, (x, w, h) in enumerate(((120, 170, 110), (300, 150, 130), (470, 190, 100), (690, 160, 120), (880, 200, 105))):
        s += bgs_flat_house(x, 1090, w, h)
    for px in (40, 230, 410, 640, 820, 1040):
        s += poplar(px, 1100, r.uniform(200, 280), col="#4a7a36", dark="#33602a")
    s += f'<path d="M -40 1110 C 300 1100, 700 1120, 1120 1104 L 1120 1200 L -40 1200 Z" fill="#6a9a40"/>'
    # the stream
    s += ('<path d="M -40 1196 C 200 1186, 500 1200, 760 1190 C 900 1186, 1020 1196, 1120 1190 L 1120 1336 C 900 1346, 600 1330, 300 1342 '
          'C 150 1346, 40 1338, -40 1342 Z" fill="url(#twat)"/>')
    for k in range(70):
        y = r.uniform(1200, 1330); x = r.uniform(-20, W)
        s += f'<path d="M {x:.0f} {y:.0f} q 20 -4 40 0" stroke="#e8f8f8" stroke-width="2.5" fill="none" opacity="{r.uniform(0.3, 0.7):.2f}"/>'
    for k in range(12):
        x = r.uniform(0, W); y = r.uniform(1220, 1330)
        s += boulder(x, y, r.uniform(14, 30), seed=3410 + k, col="#8a8a80", dark="#5a5a52", lit="#b8b8aa")
    # the grass in front
    s += ('<path d="M -40 1338 C 150 1346, 300 1336, 600 1330 C 900 1344, 1020 1336, 1120 1336 L 1120 1940 L -40 1940 Z" fill="url(#tgrass)"/>')
    s += grass_tufts(3405, 1350, 1900, 70, col="#4a7a2a", hi="#8ab84a")
    for k in range(30):          # little flowers
        x = r.uniform(0, W); y = r.uniform(1360, 1900)
        s += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r.uniform(4, 8):.0f}" fill="{r.choice(["#ffffff", "#ffd84a", "#f08aa8"])}"/>'
    # the willow at the left, its branches hanging over the water
    s += '<path d="M 60 1360 C 70 1200, 40 1000, 90 820 L 130 820 C 120 1000, 150 1200, 150 1360 Z" fill="#5a4a3a" stroke="#2a2018" stroke-width="4"/>'
    for k in range(34):
        x0 = r.uniform(-60, 360); y0 = r.uniform(640, 860); L = r.uniform(240, 520)
        s += f'<path d="M {x0:.0f} {y0:.0f} q {r.uniform(-20, 30):.0f} {L * 0.5:.0f} {r.uniform(-10, 40):.0f} {L:.0f}" stroke="{r.choice(["#5a8a36", "#6a9a3e", "#4a7a2e"])}" stroke-width="{r.uniform(6, 12):.1f}" fill="none" stroke-linecap="round"/>'
    for k in range(14):
        s += f'<circle cx="{r.uniform(-40, 320):.0f}" cy="{r.uniform(600, 800):.0f}" r="{r.uniform(50, 90):.0f}" fill="{r.choice(["#5a8a36", "#4a7a2e"])}"/>'
    return svg_render(s)


def bgs_flat_house(x, y, w, h):
    """a mud-brick house with a flat roof (bgs.flat_house), its walls warmed by the summer sun"""
    from bgs import flat_house
    return flat_house(x, y, w, h, wall="#c8a478", shade="#a07e58", roof="#7a5a3e")
