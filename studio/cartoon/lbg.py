"""Painted backgrounds of Leyli & Majnun (SVG -> PNG; cache them with bgs.cached("ly_<name>", lbg.<name>)).
Part 1: the open desert at dusk with its dunes (dunes), a close view of the sand where Majnun writes (sand_close), the camp of the Banu
Amir among its palms (camp), the front of the chief's big black tent (chief_tent), the tent school under its awning (school) and the
inside of Leyli's family tent at night (tent_night). Part 2: Leyli's father's tent (leyli_tent), the Kaaba (kaaba, kaaba_close).
Part 3: the open sand plain of the battles (plain, with Leyli's tribe's tents far away when tents=True)."""
import math, random
from film import svg_render, W, H
from bgs import FILTERS, lg, rg, ridge, clouds, stars
from abg import _dune_row
from zbg import palm as palm_silhouette

SKY = {
    "dawn": [(0, "#4a5a96", 1), (0.28, "#b48aa8", 1), (0.44, "#f4b08c", 1), (0.53, "#ffe0b0", 1)],
    "day": [(0, "#3c78b8", 1), (0.32, "#8ebedc", 1), (0.5, "#efe8cc", 1)],
    "dusk": [(0, "#2a2c64", 1), (0.26, "#7a4e84", 1), (0.42, "#e8806a", 1), (0.52, "#ffc27e", 1)],
    "night": [(0, "#05070f", 1), (0.35, "#111a3c", 1), (0.52, "#2a3460", 1)],
}
SAND = {   # (lit, shade) of the near dunes, far to near
    "dawn": [("#e8c0a0", "#b88a86"), ("#e6b48e", "#ae7e74"), ("#e0a67c", "#a06c60"), ("#d8986a", "#8e5a4e")],
    "day": [("#ecd2a0", "#cfa878"), ("#e8c48a", "#c49660"), ("#e2b474", "#b4824e"), ("#dca462", "#a87040")],
    "dusk": [("#e8a874", "#9a6a6a"), ("#e09a62", "#8a5a5a"), ("#d68a52", "#7a4a4c"), ("#c87a46", "#6a3e40")],
    "night": [("#5a5a7a", "#3a3a58"), ("#52526e", "#32324e"), ("#4a4a64", "#2c2c44"), ("#42425a", "#26263a")],
}
SUNPOS = {"dawn": (860, 1000), "day": (880, 380), "dusk": (210, 960), "night": (820, 300)}
TENT = ("#2a2422", "#3c3430", "#16110f")        # goat-hair cloth: body, woven stripe, shadow
GROUND_Y = {"camp": 1180, "chief_tent": 1330, "school": 1000, "tent_night": 1300, "dunes": 1180}


def _sky(pal, sid="sky"):
    sx, sy = SUNPOS[pal]
    s = lg(sid, SKY[pal])
    glow = {"dawn": "#ffd6a0", "day": "#fff8e0", "dusk": "#ffb070", "night": "#c8d4ff"}[pal]
    s += rg(sid + "g", sx, sy, 760 if pal != "night" else 300, [(0, glow, 0.85 if pal != "night" else 0.5), (0.2, glow, 0.35), (1, glow, 0)])
    return s


def _sky_draw(pal, sid="sky", sun=True):
    sx, sy = SUNPOS[pal]
    s = f'<rect width="{W}" height="{H}" fill="url(#{sid})"/><rect width="{W}" height="{H}" fill="url(#{sid}g)"/>'
    if pal == "night":
        s += stars(4101, 260, 1000) + f'<circle cx="{sx}" cy="{sy}" r="34" fill="#f4f0e0"/><circle cx="{sx + 12}" cy="{sy - 8}" r="30" fill="#2a3460" opacity="0.0"/>'
    elif sun:
        r = {"dawn": 70, "day": 44, "dusk": 80}[pal]
        col = {"dawn": "#fff0c8", "day": "#fffdf2", "dusk": "#ffe6b0"}[pal]
        s += f'<circle cx="{sx}" cy="{sy}" r="{r}" fill="{col}" opacity="0.95"/>'
    if pal in ("dawn", "dusk"):
        s += clouds(W, 4102, [420, 560, 700], col="#ffb090" if pal == "dawn" else "#f08870", hi="#ffe0b8", op=0.45)
    elif pal == "day":
        s += clouds(W, 4103, [260, 420], col="#ffffff", hi="#ffffff", op=0.3)
    return s


def date_palm(x, y, h, lean=0.0, seed=0, trunk=("#7a5a3a", "#5a3e26", "#a08058"), leaf=("#3e5a2a", "#2a4220", "#6a8a42"), n=11, sway=0.0):
    """a date palm with a ringed trunk and a crown of feathered fronds; base of the trunk at (x, y)"""
    r = random.Random(seed)
    tx, ty = x + lean * h, y - h
    o = ""
    # trunk: a tapering curved band, with leaf-base scars as chevrons
    pts_l, pts_r = [], []
    for k in range(13):
        u = k / 12
        cx = x + lean * h * (u ** 1.4); cy = y - h * u
        w = (h * 0.045) * (1.15 - 0.45 * u)
        pts_l.append((cx - w, cy)); pts_r.append((cx + w, cy))
    d = "M " + " L ".join(f"{a:.1f} {b:.1f}" for a, b in pts_l + pts_r[::-1]) + " Z"
    o += f'<path d="{d}" fill="{trunk[0]}" stroke="#1b0f0a" stroke-width="2.5"/>'
    o += f'<path d="M ' + " L ".join(f"{a + (b2 - a) * 0.65:.1f} {bb:.1f}" for (a, bb), (b2, _) in zip(pts_l, pts_r)) + f'" stroke="{trunk[1]}" stroke-width="{h * 0.03:.1f}" fill="none" opacity="0.5"/>'
    for k in range(1, 22):
        u = k / 22
        cx = x + lean * h * (u ** 1.4); cy = y - h * u
        w = (h * 0.045) * (1.15 - 0.45 * u)
        o += (f'<path d="M {cx - w:.1f} {cy:.1f} L {cx:.1f} {cy + w * 0.55:.1f} L {cx + w:.1f} {cy:.1f}" stroke="{trunk[1]}" stroke-width="{max(1.5, h * 0.008):.1f}" fill="none"/>'
              f'<path d="M {cx - w * 0.8:.1f} {cy - 3:.1f} L {cx:.1f} {cy + w * 0.4 - 3:.1f}" stroke="{trunk[2]}" stroke-width="{max(1, h * 0.005):.1f}" fill="none" opacity="0.6"/>')
    # fronds: back ones darker, front ones lighter
    fr = h * 0.42
    fronds = []
    for k in range(n):
        a = math.radians(-180 + (k + 0.5) * (180 / n) + r.uniform(-8, 8))
        droop = 0.35 + 0.45 * abs(math.cos(a))
        L = fr * r.uniform(0.85, 1.1)
        ex = tx + math.cos(a) * L + sway * 10 * math.cos(a)
        ey = ty + math.sin(a) * L * 0.55 + L * droop * 0.55
        cx_, cy_ = tx + math.cos(a) * L * 0.55, ty + math.sin(a) * L * 0.6 - L * 0.12
        fronds.append((abs(math.cos(a)), ex, ey, cx_, cy_, L))
    for back in (True, False):
        for k, (cosa, ex, ey, cx_, cy_, L) in enumerate(fronds):
            if (k % 2 == 0) != back:
                continue
            col = leaf[1] if back else leaf[0]
            o += f'<path d="M {tx:.1f} {ty:.1f} Q {cx_:.1f} {cy_:.1f} {ex:.1f} {ey:.1f}" stroke="{col}" stroke-width="{max(2, h * 0.012):.1f}" fill="none"/>'
            for j in range(1, 14):          # leaflets hanging from the rachis
                u = j / 14
                px = (1 - u) ** 2 * tx + 2 * (1 - u) * u * cx_ + u * u * ex
                py = (1 - u) ** 2 * ty + 2 * (1 - u) * u * cy_ + u * u * ey
                ll = L * 0.22 * math.sin(math.pi * (0.15 + 0.85 * u))
                for sd in (-1, 1):
                    o += (f'<path d="M {px:.1f} {py:.1f} q {sd * ll * 0.35:.1f} {ll * 0.3:.1f} {sd * ll * 0.25:.1f} {ll * 0.9:.1f}" '
                          f'stroke="{col}" stroke-width="{max(1.6, h * 0.007):.1f}" fill="none" stroke-linecap="round"/>')
            if not back:
                o += f'<path d="M {tx:.1f} {ty:.1f} Q {cx_:.1f} {cy_ - 3:.1f} {ex:.1f} {ey - 3:.1f}" stroke="{leaf[2]}" stroke-width="{max(1, h * 0.004):.1f}" fill="none" opacity="0.8"/>'
    # dates under the crown
    for k in range(3):
        dx = (k - 1) * h * 0.04
        o += f'<ellipse cx="{tx + dx:.1f}" cy="{ty + h * 0.05:.1f}" rx="{h * 0.022:.1f}" ry="{h * 0.035:.1f}" fill="#a85a1a" stroke="#1b0f0a" stroke-width="1.5"/>'
    return o


def black_tent(x0, x1, y, h, depth=90, open_front=True, lit=False, poles=3, rugs=True, back_pat=True, light=None, curtain=("#5a1a14", "#e8dcc8", "#1a1210")):
    """a long Bedouin tent of black goat hair seen from the front: the roof sags between its poles, the front is raised on poles
    (open: the inside shows a woven back curtain, rugs and cushions), the ends slope to the ground, guy ropes run out to stakes.
    Base (ground) at y from x0 to x1; the front edge is h above the ground."""
    body, stripe, dark = TENT
    w = x1 - x0
    top = y - h
    o = ""
    # guy ropes behind/at the sides
    for k in range(poles + 2):
        px = x0 + w * k / (poles + 1)
        sd = -1 if k <= (poles + 1) / 2 else 1
        o += f'<path d="M {px:.0f} {top + 6:.0f} L {px + sd * w * 0.12:.0f} {y + 26:.0f}" stroke="#4a3a2a" stroke-width="2.4" opacity="0.8"/>'
    # roof surface (seen a little from above) and its sagging front edge
    xs = [x0 + w * k / (poles + 1) for k in range(poles + 2)]
    edge = [(x0 - 30, top + 40)]
    for i, px in enumerate(xs):
        edge.append((px, top - (6 if 0 < i < len(xs) - 1 else -10)))
        if i < len(xs) - 1:
            edge.append(((px + xs[i + 1]) / 2, top + 16))
    edge.append((x1 + 30, top + 40))
    roof_back = [(x1 + 10, top - depth * 0.45), (x0 - 10, top - depth * 0.45)]
    d = "M " + " L ".join(f"{a:.0f} {b:.0f}" for a, b in edge + roof_back) + " Z"
    o += f'<path d="{d}" fill="{body}" stroke="#0e0a08" stroke-width="3"/>'
    for k in range(1, 5):            # woven strips along the roof
        yy = top - depth * 0.45 + k * (depth * 0.45 + 10) / 5
        o += f'<path d="M {x0 - 10 + k * 4:.0f} {yy:.0f} L {x1 + 10 - k * 4:.0f} {yy:.0f}" stroke="{stripe}" stroke-width="5" opacity="0.7"/>'
    # the open front: inside
    inner_top = top + 18
    if open_front:
        o += f'<path d="M {x0 + 10:.0f} {inner_top:.0f} L {x1 - 10:.0f} {inner_top:.0f} L {x1 - 30:.0f} {y:.0f} L {x0 + 30:.0f} {y:.0f} Z" fill="{dark}"/>'
        if back_pat:                 # the woven back curtain (sahah): bands of red, white and black triangles
            by0, by1 = inner_top + (y - inner_top) * 0.18, inner_top + (y - inner_top) * 0.5
            o += f'<rect x="{x0 + 24:.0f}" y="{by0:.0f}" width="{w - 48:.0f}" height="{by1 - by0:.0f}" fill="{curtain[0]}" opacity="0.85"/>'
            step = 26
            for k in range(int((w - 48) / step)):
                xx = x0 + 24 + k * step
                o += (f'<path d="M {xx:.0f} {by0 + 6:.0f} l {step / 2:.0f} {(by1 - by0) * 0.4:.0f} l {step / 2:.0f} {-(by1 - by0) * 0.4:.0f} Z" fill="{curtain[1]}" opacity="0.8"/>'
                      f'<path d="M {xx:.0f} {by1 - 6:.0f} l {step / 2:.0f} {-(by1 - by0) * 0.35:.0f} l {step / 2:.0f} {(by1 - by0) * 0.35:.0f} Z" fill="{curtain[2]}" opacity="0.8"/>')
            o += f'<path d="M {x0 + 24:.0f} {by0:.0f} L {x1 - 24:.0f} {by0:.0f} M {x0 + 24:.0f} {by1:.0f} L {x1 - 24:.0f} {by1:.0f}" stroke="#c9a24a" stroke-width="3" opacity="0.7"/>'
        if rugs:
            ry = y - (y - inner_top) * 0.16
            o += (f'<path d="M {x0 + 40:.0f} {y - 2:.0f} L {x0 + 70:.0f} {ry:.0f} L {x1 - 70:.0f} {ry:.0f} L {x1 - 40:.0f} {y - 2:.0f} Z" fill="#8a2420" stroke="#2a0e0a" stroke-width="2"/>'
                  f'<path d="M {x0 + 60:.0f} {y - 8:.0f} L {x0 + 82:.0f} {ry + 6:.0f} L {x1 - 82:.0f} {ry + 6:.0f} L {x1 - 60:.0f} {y - 8:.0f} Z" fill="none" stroke="#e0b060" stroke-width="2.5" opacity="0.8"/>')
            for k in range(4):           # cushions along the back
                cx = x0 + 90 + k * (w - 180) / 3
                o += f'<ellipse cx="{cx:.0f}" cy="{ry - 14:.0f}" rx="{w * 0.06:.0f}" ry="{(y - inner_top) * 0.09:.0f}" fill="{["#6a2a5a", "#2a4a7a", "#a8642a", "#3a6a4a"][k % 4]}" stroke="#140a08" stroke-width="2"/>'
        if lit:
            o += f'<path d="M {x0 + 10:.0f} {inner_top:.0f} L {x1 - 10:.0f} {inner_top:.0f} L {x1 - 30:.0f} {y:.0f} L {x0 + 30:.0f} {y:.0f} Z" fill="#ffb060" opacity="0.28"/>'
    else:
        o += f'<path d="M {x0 + 10:.0f} {inner_top:.0f} L {x1 - 10:.0f} {inner_top:.0f} L {x1 - 20:.0f} {y:.0f} L {x0 + 20:.0f} {y:.0f} Z" fill="{body}" stroke="#0e0a08" stroke-width="2"/>'
        for k in range(1, 6):
            yy = inner_top + k * (y - inner_top) / 6
            o += f'<path d="M {x0 + 14:.0f} {yy:.0f} L {x1 - 14:.0f} {yy:.0f}" stroke="{stripe}" stroke-width="4" opacity="0.6"/>'
    # sloping ends
    o += (f'<path d="M {x0 - 30:.0f} {top + 40:.0f} L {x0 + 10:.0f} {inner_top:.0f} L {x0 + 30:.0f} {y:.0f} L {x0 - 70:.0f} {y:.0f} Z" fill="{body}" stroke="#0e0a08" stroke-width="2.5"/>'
          f'<path d="M {x1 + 30:.0f} {top + 40:.0f} L {x1 - 10:.0f} {inner_top:.0f} L {x1 - 30:.0f} {y:.0f} L {x1 + 70:.0f} {y:.0f} Z" fill="{body}" stroke="#0e0a08" stroke-width="2.5"/>'
          f'<path d="M {x1 + 30:.0f} {top + 40:.0f} L {x1 - 10:.0f} {inner_top:.0f} L {x1 - 30:.0f} {y:.0f} L {x1 + 70:.0f} {y:.0f} Z" fill="#000" opacity="0.25"/>')
    # poles at the front
    for i, px in enumerate(xs[1:-1]):
        o += f'<path d="M {px:.0f} {top - 4:.0f} L {px:.0f} {y:.0f}" stroke="#5a3a1e" stroke-width="7"/><path d="M {px:.0f} {top - 4:.0f} L {px:.0f} {y:.0f}" stroke="#1b0f0a" stroke-width="1.5" fill="none"/>'
    if light:                         # a light colour along the front edge (sunrise, sunset)
        o += f'<path d="M ' + " L ".join(f"{a:.0f} {b - 2:.0f}" for a, b in edge) + f'" stroke="{light}" stroke-width="4" fill="none" opacity="0.7"/>'
    # shadow on the ground in front
    o += f'<ellipse cx="{(x0 + x1) / 2:.0f}" cy="{y + 8:.0f}" rx="{w * 0.56:.0f}" ry="{h * 0.08:.0f}" fill="#000" opacity="0.18"/>'
    return o


def _ground(y0, pal, seed, tufts=True):
    """the sandy ground of the camp from y0 down, with footprints, pebbles and a few dry tufts"""
    r = random.Random(seed)
    lit, shade = {"dawn": ("#dcae8a", "#b07e6a"), "day": ("#e2c08e", "#c09a6a"), "dusk": ("#d49468", "#9a6250"),
                  "night": ("#4a4660", "#302c44")}[pal]
    s = f'<rect x="0" y="{y0}" width="{W}" height="{H - y0}" fill="url(#gr{seed})"/>'
    defs = lg(f"gr{seed}", [(0, lit, 1), (1, shade, 1)])
    for k in range(70):
        x = r.uniform(-20, W); y = r.uniform(y0 + 10, H)
        s += f'<path d="M {x:.0f} {y:.0f} q {14 + (y - y0) * 0.03:.0f} -4 {30 + (y - y0) * 0.06:.0f} 0" stroke="#fff0d0" stroke-width="{1.4 + (y - y0) * 0.002:.1f}" fill="none" opacity="0.3"/>'
    for k in range(40):
        x = r.uniform(0, W); y = r.uniform(y0 + 20, H); rr = 2 + (y - y0) * 0.006
        s += f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{rr:.1f}" ry="{rr * 0.6:.1f}" fill="#7a5a3a" opacity="0.45"/>'
    if tufts:
        for k in range(14):
            x = r.uniform(0, W); y = r.uniform(y0 + 30, H - 40); sc = 0.6 + (y - y0) / 600
            for j in range(5):
                s += (f'<path d="M {x:.0f} {y:.0f} q {r.uniform(-8, 8) * sc:.0f} {-r.uniform(10, 18) * sc:.0f} {r.uniform(-20, 20) * sc:.0f} {-r.uniform(18, 34) * sc:.0f}" '
                      f'stroke="#8a7a3a" stroke-width="{2 * sc:.1f}" fill="none" opacity="0.8"/>')
    return defs, s


# ------------------------------------------------------------------ the open desert (hook; Qays walks into it)
DUNE_TOP = 1180          # the near flat sand where Majnun sits in dunes(): people at y 1250-1500


def dunes(pal="dusk"):
    """the open desert: a wide sky, far dunes on a low horizon (y 900), a broad near dune whose flat top runs across the frame from
    y 1180; the sun low at the left (dusk) or right (dawn)"""
    s = "<defs>" + FILTERS + _sky(pal) + lg("nd", [(0, SAND[pal][3][0], 1), (1, SAND[pal][3][1], 1)]) + "</defs>"
    s += _sky_draw(pal)
    s += f'<path d="{ridge(W, 920, 50, 4111, rough=0.3)}" fill="{SAND[pal][0][1]}" opacity="0.8"/>'
    s += f'<rect x="0" y="880" width="{W}" height="60" fill="#fff0d8" opacity="0.25" filter="url(#b20)"/>'
    for i, (base, amp) in enumerate(((930, 40), (990, 70), (1080, 100))):
        lit, shade = SAND[pal][i]
        s += _dune_row(4120 + i, base, amp, 380 * (1 + i * 0.3), 720 * (1 + i * 0.3), lit, shade, crest="#fff0d8")
    # the near dune: a broad smooth surface with ripples
    s += (f'<path d="M -40 {DUNE_TOP + 20} C 200 {DUNE_TOP - 30}, 600 {DUNE_TOP - 40}, 1120 {DUNE_TOP + 10} L 1120 {H} L -40 {H} Z" fill="url(#nd)"/>'
          f'<path d="M -40 {DUNE_TOP + 20} C 200 {DUNE_TOP - 30}, 600 {DUNE_TOP - 40}, 1120 {DUNE_TOP + 10}" stroke="#fff0d0" stroke-width="4" fill="none" opacity="0.6"/>')
    r = random.Random(4130)
    for k in range(60):
        y = r.uniform(DUNE_TOP + 20, H); x = r.uniform(-60, W)
        L = 40 + (y - DUNE_TOP) * 0.25
        s += f'<path d="M {x:.0f} {y:.0f} q {L * 0.5:.0f} {-6 - (y - DUNE_TOP) * 0.01:.0f} {L:.0f} 0" stroke="#fff0d0" stroke-width="{1.5 + (y - DUNE_TOP) * 0.003:.1f}" fill="none" opacity="0.35"/>'
        s += f'<path d="M {x + 4:.0f} {y + 4:.0f} q {L * 0.5:.0f} {-6 - (y - DUNE_TOP) * 0.01:.0f} {L:.0f} 0" stroke="{SAND[pal][3][1]}" stroke-width="{1.5 + (y - DUNE_TOP) * 0.003:.1f}" fill="none" opacity="0.35"/>'
    if pal in ("dusk", "dawn"):     # long low light
        sx, sy = SUNPOS[pal]
        s += f'<rect x="0" y="{DUNE_TOP - 60}" width="{W}" height="200" fill="#ffd0a0" opacity="0.12" filter="url(#b40)"/>'
    return svg_render(s)


def sand_close(pal="dusk"):
    """the sand seen from close above, in low warm light: wind ripples, a few pebbles; Majnun writes in the middle (y 600-1000)"""
    r = random.Random(4140)
    lit, shade = {"dusk": ("#e8a26a", "#a8664a"), "day": ("#e8c48a", "#b48a5a")}[pal]
    s = "<defs>" + FILTERS + rg("sc", 760, 300, 1700, [(0, lit, 1), (1, shade, 1)]) + "</defs>"
    s += f'<rect width="{W}" height="{H}" fill="url(#sc)"/>'
    for k in range(46):           # ripples: long soft ridges across the frame, a light crest and a shaded trough
        y = -40 + k * 44 + r.uniform(-8, 8)
        pts = [(x, y + 16 * math.sin(x / 140 + k * 0.7) + 6 * math.sin(x / 47 + k)) for x in range(-40, W + 80, 40)]
        d = "M " + " L ".join(f"{a:.0f} {b:.0f}" for a, b in pts)
        s += (f'<path d="{d}" stroke="#ffe8c4" stroke-width="5" fill="none" opacity="0.45" filter="url(#b3)"/>'
              f'<path d="{d}" stroke="#8a4a32" stroke-width="7" fill="none" opacity="0.25" transform="translate(0,9)" filter="url(#b3)"/>')
    for k in range(90):
        x, y = r.uniform(0, W), r.uniform(0, H); rr = r.uniform(2, 7)
        s += f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{rr:.1f}" ry="{rr * 0.7:.1f}" fill="{r.choice(("#7a4a32", "#c88a5a", "#f4d0a0"))}" opacity="{r.uniform(0.3, 0.7):.2f}"/>'
    s += f'<rect width="{W}" height="{H}" fill="#3a1a2a" opacity="0.0"/>'
    return svg_render(s)


# ------------------------------------------------------------------ the camp of the Banu Amir
def camp(pal="dawn"):
    """the camp among palms: far dunes and palm groves on the horizon (y 1000), black tents in two rows, the chief's long tent at the left
    (x 40-640, ground y 1180), a small fire ring at (820, 1300); people at y 1250-1800"""
    s = "<defs>" + FILTERS + _sky(pal)
    gdefs, gs = _ground(GROUND_Y["camp"] - 60, pal, 4150)
    s += gdefs + "</defs>"
    s += _sky_draw(pal)
    for i, (base, amp) in enumerate(((990, 50), (1040, 60))):
        lit, shade = SAND[pal][i]
        s += _dune_row(4160 + i, base, amp, 420, 760, lit, shade, crest="#fff0d8")
    hz = {"dawn": "#3a3a4a", "day": "#3a5a3a", "dusk": "#2a2a3a", "night": "#10121c"}[pal]
    r = random.Random(4170)
    for k in range(16):            # the far palm grove
        x = r.uniform(-40, W + 40); hh = r.uniform(110, 190)
        s += palm_silhouette(x, 1100 + r.uniform(-10, 10), hh, col=hz, lean=r.uniform(-0.12, 0.12), n=8)
    s += gs
    light = {"dawn": "#ffb88a", "day": None, "dusk": "#ffa070", "night": None}[pal]
    # far tents (right), middle tents, then the chief's tent (left, nearest)
    s += black_tent(700, 980, 1120, 80, depth=40, poles=2, rugs=False, back_pat=False, light=light)
    s += black_tent(560, 700, 1105, 60, depth=30, poles=1, open_front=False, light=light)
    s += date_palm(1010, 1160, 330, lean=-0.06, seed=4171)
    s += black_tent(690, 1060, 1215, 130, depth=60, poles=2, light=light)
    s += date_palm(660, 1230, 420, lean=0.05, seed=4172)
    s += black_tent(40, 600, GROUND_Y["camp"], 200, depth=80, poles=3, light=light)
    # the fire ring
    s += ''.join(f'<ellipse cx="{820 + 46 * math.cos(a):.0f}" cy="{1310 + 16 * math.sin(a):.0f}" rx="14" ry="9" fill="#6a5a4a" stroke="#2a1a10" stroke-width="2"/>'
                 for a in [k * math.pi / 5 for k in range(10)])
    s += '<ellipse cx="820" cy="1310" rx="36" ry="10" fill="#2a1a12"/>'
    # a near palm at the left edge
    s += date_palm(-30, 1900, 1100, lean=0.08, seed=4173)
    if pal == "dusk":
        s += f'<rect width="{W}" height="{H}" fill="#4a2a5a" opacity="0.12"/>'
    return svg_render(s)


def chief_tent(pal="dawn"):
    """close to the front of the chief's tent: the open front from x 40 to 1040 (ground y 1330), cushions and rugs inside, a palm at the
    right; people stand in front of it at y 1450-1700 (feet)"""
    s = "<defs>" + FILTERS + _sky(pal)
    gdefs, gs = _ground(GROUND_Y["chief_tent"] - 80, pal, 4180)
    s += gdefs + "</defs>"
    s += _sky_draw(pal)
    lit, shade = SAND[pal][1]
    s += _dune_row(4181, 1080, 70, 420, 760, lit, shade, crest="#fff0d8")
    hz = {"dawn": "#3a3a4a", "day": "#3a5a3a", "dusk": "#2a2a3a", "night": "#10121c"}[pal]
    r = random.Random(4182)
    for k in range(8):
        x = r.uniform(-40, W + 40)
        s += palm_silhouette(x, 1170, r.uniform(160, 240), col=hz, lean=r.uniform(-0.1, 0.1), n=8)
    s += gs
    light = {"dawn": "#ffb88a", "day": None, "dusk": "#ffa070", "night": None}[pal]
    s += black_tent(40, 1040, GROUND_Y["chief_tent"], 470, depth=120, poles=3, light=light)
    s += date_palm(1010, 1500, 1120, lean=-0.05, seed=4183)
    # a saddle and a water skin by the tent
    s += ('<path d="M 120 1350 C 140 1310, 220 1306, 240 1350 Z" fill="#6a3a1a" stroke="#1b0f0a" stroke-width="3"/>'
          '<path d="M 130 1342 L 230 1342" stroke="#c9a24a" stroke-width="5"/>'
          '<ellipse cx="900" cy="1340" rx="44" ry="26" fill="#5a3a22" stroke="#1b0f0a" stroke-width="3"/><path d="M 930 1326 l 26 -22" stroke="#1b0f0a" stroke-width="6"/>')
    return svg_render(s)


# ------------------------------------------------------------------ the tent school
SCHOOL_RUG = 1000        # the top of the rug in school(): children sit on it at y 1080-1250 (seat), so their faces stay above y 1000
BOARD = (80, 520, 300, 780)      # the teacher's writing board in school(): x0, y0, x1, y1; alif, ba, ta on it at y 600-700


def school(pal="day"):
    """the school: inside a big open awning of black goat hair (its underside and three poles above, y 0-330), the bright desert and
    palms beyond the open sides (y 330-1000), a long red rug on the sand from SCHOOL_RUG; the writing board on a stand at the left"""
    s = "<defs>" + FILTERS + _sky(pal) + lg("aw", [(0, "#1a1512", 1), (1, "#3a302a", 1)])
    gdefs, gs = _ground(900, pal, 4190, tufts=False)
    s += gdefs + lg("rug", [(0, "#a02c22", 1), (1, "#6a1612", 1)]) + "</defs>"
    s += _sky_draw(pal, sun=False)
    for i, (base, amp) in enumerate(((850, 50), (900, 60))):
        lit, shade = SAND[pal][i]
        s += _dune_row(4191 + i, base, amp, 420, 760, lit, shade, crest="#fff6e0")
    s += gs
    r = random.Random(4193)
    for k in range(7):
        s += date_palm(r.uniform(-40, W + 40), 935 + r.uniform(-15, 10), r.uniform(300, 440), lean=r.uniform(-0.08, 0.08), seed=4194 + k,
                       leaf=("#4a6a32", "#344e24", "#7a9a4a"))
    s += black_tent(700, 940, 930, 60, depth=26, poles=2, rugs=False, back_pat=False)
    # the awning: underside with woven stripes, sagging front edge, three poles
    s += ('<path d="M -40 -40 L 1120 -40 L 1120 320 C 900 356, 760 300, 540 340 C 320 300, 180 356, -40 320 Z" fill="url(#aw)" stroke="#0a0806" stroke-width="4"/>')
    for k in range(8):
        yy = 10 + k * 40
        s += f'<path d="M -40 {yy} C 300 {yy + 22}, 780 {yy + 22}, 1120 {yy}" stroke="#4a3e36" stroke-width="7" fill="none" opacity="0.55"/>'
    s += '<path d="M -40 320 C 180 356, 320 300, 540 340 C 760 300, 900 356, 1120 320" stroke="#6a5a4a" stroke-width="5" fill="none" opacity="0.7"/>'
    for x in (150, 540, 930):
        s += (f'<rect x="{x - 9}" y="310" width="18" height="{SCHOOL_RUG - 310 + 14}" fill="#6a4628" stroke="#1b0f0a" stroke-width="3"/>'
              f'<rect x="{x - 3}" y="310" width="5" height="{SCHOOL_RUG - 310}" fill="#a07a4a" opacity="0.6"/>')
    # the shade under the awning on the sand
    s += f'<rect x="0" y="930" width="{W}" height="{H - 930}" fill="#2a1a12" opacity="0.35"/>'
    # the rug
    R = SCHOOL_RUG
    s += (f'<path d="M -40 {R} L 1120 {R} L 1120 {H} L -40 {H} Z" fill="url(#rug)" stroke="#2a0a08" stroke-width="3"/>'
          f'<path d="M -40 {R + 24} L 1120 {R + 24}" stroke="#e0b060" stroke-width="6" opacity="0.8"/>')
    for k in range(18):
        x = 30 + k * 62
        s += f'<path d="M {x} {R + 56} l 20 24 l -20 24 l -20 -24 Z" fill="#1e2a5a" opacity="0.6"/><circle cx="{x}" cy="{R + 80}" r="5" fill="#e0b060" opacity="0.7"/>'
    for k in range(7):
        yy = R + 160 + k * 120
        s += f'<path d="M -40 {yy} L 1120 {yy}" stroke="#4a0e0a" stroke-width="5" opacity="0.5"/>'
    # the writing board on its stand (at the left, behind the teacher)
    x0, y0, x1, y1 = BOARD
    s += (f'<path d="M {x0 + 30} {R + 10} L {x0 + 70} {y1 - 20} M {x1 - 30} {R + 10} L {x1 - 70} {y1 - 20}" stroke="#5a3a1e" stroke-width="12"/>'
          f'<rect x="{x0}" y="{y0}" width="{x1 - x0}" height="{y1 - y0}" rx="16" fill="#c8a46a" stroke="#1b0f0a" stroke-width="4"/>'
          f'<rect x="{x0 + 16}" y="{y0 + 16}" width="{x1 - x0 - 32}" height="{y1 - y0 - 32}" rx="10" fill="#efe0b8"/>')
    dy = y0 - 720         # the letters were drawn for a board at y 720
    # alif, ba, ta from right to left, as the teacher reads them
    s += (f'<g transform="translate(0,{dy})">'
          '<path d="M 254 790 L 254 880" stroke="#2a1a10" stroke-width="10" stroke-linecap="round"/>'                                      # alif
          '<path d="M 162 846 Q 166 880 196 880 L 216 880 Q 224 866 220 848" stroke="#2a1a10" stroke-width="9" fill="none" stroke-linecap="round"/>'   # ba
          '<circle cx="190" cy="904" r="7" fill="#2a1a10"/>'
          '<path d="M 104 846 Q 108 880 132 880 L 146 880 Q 154 866 150 848" stroke="#2a1a10" stroke-width="9" fill="none" stroke-linecap="round"/>'   # ta
          '<circle cx="120" cy="826" r="6.5" fill="#2a1a10"/><circle cx="138" cy="826" r="6.5" fill="#2a1a10"/>'
          '<path d="M 116 950 L 264 950" stroke="#8a6a3a" stroke-width="3" opacity="0.5"/></g>')
    return svg_render(s)


# ------------------------------------------------------------------ Leyli's family tent at night
TENT_DOOR = (720, 1060)      # the opening of the tent in tent_night(): x 720-1060, the night sky and the camp outside
LAMP_AT = (330, 1010)        # the oil lamp on its stand in tent_night()


def tent_night():
    """inside Leyli's family tent at night: the woven back curtain with red and white bands, cushions along it, a rug, a hanging water
    skin, an oil lamp on a stand (LAMP_AT); the front opening at the right (TENT_DOOR x) shows the night and a far campfire; floor y 1300"""
    s = "<defs>" + FILTERS + _sky("night", "ns") + lg("tw", [(0, "#1c1614", 1), (1, "#2e2420", 1)]) + lg("rugn", [(0, "#7a2018", 1), (1, "#4a120e", 1)])
    s += rg("lamp", LAMP_AT[0], LAMP_AT[1], 900, [(0, "#ffb060", 0.55), (0.45, "#a0502a", 0.18), (1, "#000", 0)]) + "</defs>"
    s += f'<rect width="{W}" height="{H}" fill="url(#tw)"/>'
    # the opening: night sky, far dunes, a campfire
    x0, x1 = TENT_DOOR
    s += f'<clipPath id="door"><path d="M {x0} 380 L {x1} 330 L {x1} 1300 L {x0} 1300 Z"/></clipPath><g clip-path="url(#door)">'
    s += f'<rect x="{x0}" y="300" width="{x1 - x0}" height="1000" fill="url(#ns)"/><rect x="{x0}" y="300" width="{x1 - x0}" height="1000" fill="url(#nsg)"/>'
    rr = random.Random(4202)
    s += "".join(f'<circle cx="{rr.uniform(x0, x1):.0f}" cy="{rr.uniform(330, 950):.0f}" r="{rr.uniform(0.8, 2.2):.1f}" fill="#fff" opacity="{rr.uniform(0.4, 1):.2f}"/>' for _ in range(50))
    s += f'<circle cx="{x0 + 230}" cy="520" r="26" fill="#f4f0e0"/>'
    s += f'<path d="{ridge(W, 1120, 40, 4203, rough=0.3)}" fill="#3a3a58"/>'
    s += f'<rect x="{x0}" y="1150" width="{x1 - x0}" height="160" fill="#2c2a44"/>'
    s += black_tent(x0 + 90, x0 + 300, 1150, 60, depth=24, poles=1, rugs=False, back_pat=False, lit=True)
    s += (f'<circle cx="{x0 + 70}" cy="1210" r="40" fill="#ffa040" opacity="0.35" filter="url(#b12)"/>'
          f'<path d="M {x0 + 56} 1220 Q {x0 + 70} 1180 {x0 + 84} 1220 Z" fill="#ffb050"/>')
    s += '</g>'
    # the tent cloth: the roof slopes down from the ridge, woven strips
    s += f'<path d="M -40 -40 L 1120 -40 L 1120 330 L {x1} 330 L {x0} 380 L -40 470 Z" fill="#241c18"/>'
    for k in range(10):
        yy = -10 + k * 46
        s += f'<path d="M -40 {yy + 40} L 1120 {yy}" stroke="#3a302a" stroke-width="8" opacity="0.7"/>'
    s += f'<path d="M {x0} 380 L {x0} 1300" stroke="#5a3a1e" stroke-width="14"/><path d="M {x0 - 6} 380 L {x0 - 6} 1300" stroke="#1b0f0a" stroke-width="3"/>'
    s += f'<path d="M {x0 - 40} 380 C {x0 - 20} 700, {x0 - 30} 1000, {x0 - 10} 1300 L {x0 + 40} 1300 C {x0 + 20} 1000, {x0 + 30} 700, {x0 + 10} 380 Z" fill="#2a2220" stroke="#0e0a08" stroke-width="3"/>'
    # the woven back curtain
    by0, by1 = 520, 1180
    s += f'<rect x="-40" y="{by0}" width="{x0 - 30 + 40}" height="{by1 - by0}" fill="#4a1410"/>'
    for band, (yy, hh) in enumerate(((by0 + 40, 70), (by0 + 250, 90), (by0 + 480, 70))):
        s += f'<rect x="-40" y="{yy}" width="{x0 - 30 + 40}" height="{hh}" fill="#e6d8c0" opacity="0.85"/>'
        step = 34
        for k in range(int((x0 + 10) / step)):
            xx = -40 + k * step
            s += (f'<path d="M {xx} {yy + hh} l {step / 2} {-hh * 0.8} l {step / 2} {hh * 0.8} Z" fill="#8a1a14" opacity="0.9"/>'
                  f'<path d="M {xx + step / 2 - 4} {yy + 8} l 4 6 l 4 -6 Z" fill="#1a1210"/>')
    s += f'<path d="M -40 {by0} L {x0 - 30} {by0} M -40 {by1} L {x0 - 30} {by1}" stroke="#c9a24a" stroke-width="4" opacity="0.6"/>'
    # the floor, rug and cushions
    s += f'<rect x="-40" y="1290" width="1160" height="{H - 1290}" fill="#3a2a20"/>'
    s += (f'<path d="M -40 1330 L {x0 + 60} 1330 L {x0 + 160} {H} L -40 {H} Z" fill="url(#rugn)" stroke="#1a0806" stroke-width="3"/>'
          f'<path d="M -40 1366 L {x0 + 70} 1366" stroke="#e0b060" stroke-width="5" opacity="0.7"/>')
    for k in range(6):
        x = 40 + k * 110
        s += f'<path d="M {x} 1420 l 26 30 l -26 30 l -26 -30 Z" fill="#1e2a5a" opacity="0.6"/>'
    for k, (cx, col) in enumerate(((90, "#6a2a5a"), (260, "#2a4a7a"), (560, "#a8642a"))):
        s += (f'<ellipse cx="{cx}" cy="1250" rx="92" ry="56" fill="{col}" stroke="#140a08" stroke-width="3"/>'
              f'<path d="M {cx - 60} 1240 Q {cx} 1220 {cx + 60} 1240" stroke="#e0b060" stroke-width="4" fill="none" opacity="0.7"/>')
    # a water skin hanging from the roof pole, a chest
    s += ('<path d="M 610 380 L 610 520" stroke="#3a2414" stroke-width="5"/><ellipse cx="610" cy="590" rx="48" ry="74" fill="#6a4426" stroke="#1b0f0a" stroke-width="3"/>'
          '<rect x="470" y="1150" width="130" height="90" rx="8" fill="#5a3a1e" stroke="#1b0f0a" stroke-width="3"/><path d="M 470 1180 L 600 1180" stroke="#c9a24a" stroke-width="4"/>')
    # the lamp on its stand
    lx, ly = LAMP_AT
    s += (f'<path d="M {lx} {ly + 30} L {lx} 1300 M {lx - 40} 1300 L {lx + 40} 1300" stroke="#6a4a2a" stroke-width="9"/>'
          f'<path d="M {lx - 44} {ly + 10} C {lx - 40} {ly + 40}, {lx + 40} {ly + 40}, {lx + 50} {ly + 6} L {lx + 70} {ly - 2} L {lx + 40} {ly + 4} Z" fill="#b8822e" stroke="#1b0f0a" stroke-width="3"/>')
    s += f'<rect width="{W}" height="{H}" fill="url(#lamp)"/>'
    return svg_render(s)


# ------------------------------------------------------------------ part 2: Leyli's father's tent; the Kaaba
def leyli_tent(pal="dusk"):
    """the front of Leyli's father's big tent (her tribe): like chief_tent() but with an indigo and red back curtain, a palm at the left and
    a tethered horse's post at the right; ground y 1330, people stand at feet y 1450-1720"""
    s = "<defs>" + FILTERS + _sky(pal)
    gdefs, gs = _ground(GROUND_Y["chief_tent"] - 80, pal, 4210)
    s += gdefs + "</defs>"
    s += _sky_draw(pal)
    lit, shade = SAND[pal][1]
    s += _dune_row(4211, 1070, 80, 420, 760, lit, shade, crest="#fff0d8")
    hz = {"dawn": "#3a3a4a", "day": "#3a5a3a", "dusk": "#2a2a3a", "night": "#10121c"}[pal]
    r = random.Random(4212)
    for k in range(8):
        s += palm_silhouette(r.uniform(-40, W + 40), 1165, r.uniform(160, 240), col=hz, lean=r.uniform(-0.1, 0.1), n=8)
    s += gs
    light = {"dawn": "#ffb88a", "day": None, "dusk": "#ffa070", "night": None}[pal]
    s += black_tent(60, 1060, GROUND_Y["chief_tent"], 470, depth=120, poles=3, light=light, curtain=("#1e2450", "#e8dcc8", "#8a1a14"))
    s += date_palm(40, 1520, 1150, lean=0.06, seed=4213)
    s += ('<path d="M 960 1340 L 960 1190" stroke="#5a3a1e" stroke-width="10"/><circle cx="960" cy="1190" r="9" fill="#5a3a1e"/>'
          '<path d="M 960 1200 Q 990 1260 1030 1250" stroke="#8a6a3a" stroke-width="4" fill="none"/>')
    if pal == "dusk":
        s += f'<rect width="{W}" height="{H}" fill="#4a2a5a" opacity="0.12"/>'
    return svg_render(s)


KAABA = (250, 830, 520, 1250)      # the Kaaba's front face in kaaba(): x0, x1, top, bottom (the courtyard floor from y 1250)
KAABA_DOOR = (440, 560, 830, 1120) # its golden door (raised above the floor, as it is)


def _arabesque(x0, x1, y, h, col="#e0b24a", dark="#8a6420", seed=0):
    """a band of gold ornament (scrolls and knots, not letters) between x0 and x1, centred on y, h high"""
    r = random.Random(seed)
    o = f'<rect x="{x0}" y="{y - h / 2:.0f}" width="{x1 - x0}" height="{h}" fill="#141114"/>'
    o += f'<path d="M {x0} {y - h / 2 + 4:.0f} L {x1} {y - h / 2 + 4:.0f} M {x0} {y + h / 2 - 4:.0f} L {x1} {y + h / 2 - 4:.0f}" stroke="{col}" stroke-width="3"/>'
    x = x0 + 14
    while x < x1 - 30:
        w = r.uniform(30, 52)
        o += (f'<path d="M {x:.0f} {y + 6:.0f} C {x + w * 0.2:.0f} {y - h * 0.32:.0f}, {x + w * 0.6:.0f} {y - h * 0.32:.0f}, {x + w * 0.5:.0f} {y:.0f} '
              f'C {x + w * 0.4:.0f} {y + h * 0.3:.0f}, {x + w * 0.9:.0f} {y + h * 0.25:.0f}, {x + w:.0f} {y - 4:.0f}" stroke="{col}" stroke-width="3.2" fill="none"/>'
              f'<circle cx="{x + w * 0.5:.0f}" cy="{y - h * 0.18:.0f}" r="3" fill="{col}"/>')
        x += w
    return o


def kaaba():
    """the Kaaba at night, shown simply from outside: the black cube under its cloth with the gold band and the golden door (KAABA,
    KAABA_DOOR), its right side in shade, the white courtyard (floor from y 1250) with lamps on tall posts, small far pilgrims in white,
    a starry sky with a thin moon; people stand at y 1280-1750"""
    x0, x1, top, bot = KAABA
    s = "<defs>" + FILTERS + _sky("night", "ks") + lg("kf", [(0, "#dcdce4", 1), (1, "#8a8a9a", 1)]) + lg("kb", [(0, "#1a181c", 1), (1, "#0e0d10", 1)])
    s += rg("klamp", 540, 900, 1100, [(0, "#ffd8a0", 0.3), (0.5, "#a06a3a", 0.08), (1, "#000", 0)]) + "</defs>"
    s += f'<rect width="{W}" height="{H}" fill="url(#ks)"/>' + stars(4220, 220, 900)
    s += '<path d="M 846 236 A 30 30 0 1 0 880 290 A 24 24 0 1 1 846 236 Z" fill="#f4f0e0"/>'
    # far colonnade
    s += f'<rect x="0" y="1010" width="{W}" height="240" fill="#2a2a38"/>'
    for k in range(14):
        x = -20 + k * 82
        s += (f'<path d="M {x} 1250 L {x} 1080 Q {x + 41} 1030 {x + 82} 1080 L {x + 82} 1250" stroke="#3e3e50" stroke-width="10" fill="none"/>'
              f'<circle cx="{x + 41}" cy="1120" r="6" fill="#ffd890" opacity="0.8"/>')
    s += f'<rect x="0" y="996" width="{W}" height="22" fill="#3e3e50"/>'
    # the courtyard floor
    s += f'<rect x="0" y="{bot}" width="{W}" height="{H - bot}" fill="url(#kf)"/>'
    for k in range(9):
        yy = bot + 30 + k * k * 9
        s += f'<path d="M 0 {yy} L {W} {yy}" stroke="#ffffff" stroke-width="2" opacity="0.25"/>'
    # far pilgrims walking round (small white figures)
    r = random.Random(4221)
    for k in range(40):
        x = r.uniform(-20, W + 20); y = r.uniform(bot + 10, bot + 60); hh = r.uniform(26, 36) * (1 + (y - bot) / 120)
        s += (f'<path d="M {x - hh * 0.18:.1f} {y:.1f} L {x - hh * 0.14:.1f} {y - hh * 0.75:.1f} Q {x:.1f} {y - hh * 0.85:.1f} {x + hh * 0.14:.1f} {y - hh * 0.75:.1f} '
              f'L {x + hh * 0.18:.1f} {y:.1f} Z" fill="#eeeef2" opacity="0.9"/><circle cx="{x:.1f}" cy="{y - hh * 0.88:.1f}" r="{hh * 0.11:.1f}" fill="#c89a72"/>')
    # the Kaaba: right side in shade, then the front face
    s += f'<path d="M {x1} {top} L {x1 + 150} {top + 40} L {x1 + 150} {bot - 30} L {x1} {bot} Z" fill="#0a090b" stroke="#000" stroke-width="2"/>'
    s += f'<rect x="{x0}" y="{top}" width="{x1 - x0}" height="{bot - top}" fill="url(#kb)" stroke="#000" stroke-width="3"/>'
    for k in range(1, 8):          # the folds of the cloth
        x = x0 + k * (x1 - x0) / 8
        s += f'<path d="M {x:.0f} {top + 10} L {x:.0f} {bot}" stroke="#2a2830" stroke-width="3" opacity="0.6"/>'
    s += _arabesque(x0, x1, top + 150, 64, seed=4222)
    s += f'<path d="M {x1} {top + 118} L {x1 + 150} {top + 150} L {x1 + 150} {top + 210} L {x1} {top + 182} Z" fill="#6a5020" opacity="0.6"/>'
    # the golden door with a small ornamented frame
    dx0, dx1, dy0, dy1 = KAABA_DOOR
    s += (f'<rect x="{dx0 - 16}" y="{dy0 - 16}" width="{dx1 - dx0 + 32}" height="{dy1 - dy0 + 16}" fill="#141114" stroke="#c9a24a" stroke-width="3"/>'
          f'<rect x="{dx0}" y="{dy0}" width="{dx1 - dx0}" height="{dy1 - dy0}" rx="6" fill="#c9a24a" stroke="#6a4a18" stroke-width="3"/>'
          f'<path d="M {(dx0 + dx1) / 2:.0f} {dy0} L {(dx0 + dx1) / 2:.0f} {dy1}" stroke="#6a4a18" stroke-width="3"/>')
    for k in range(4):
        yy = dy0 + 30 + k * (dy1 - dy0 - 60) / 3
        for xx in (dx0 + 28, dx1 - 28):
            s += f'<circle cx="{xx}" cy="{yy:.0f}" r="10" fill="none" stroke="#f0d48a" stroke-width="3"/><circle cx="{xx}" cy="{yy:.0f}" r="3" fill="#f0d48a"/>'
    s += f'<rect x="{dx0 - 30}" y="{dy1}" width="{dx1 - dx0 + 60}" height="14" fill="#8a8a96"/>'
    s += f'<path d="M {x0} {bot} L {x1} {bot} L {x1 + 150} {bot - 30}" stroke="#c8c8d4" stroke-width="8" fill="none"/>'
    # lamps on tall posts
    for lx, ly in ((90, 1160), (1000, 1150), (170, 1300), (940, 1290)):
        s += (f'<path d="M {lx} {ly + 140} L {lx} {ly}" stroke="#4a4a58" stroke-width="8"/>'
              f'<circle cx="{lx}" cy="{ly - 14}" r="60" fill="#ffd090" opacity="0.25" filter="url(#b12)"/>'
              f'<path d="M {lx - 14} {ly} L {lx + 14} {ly} L {lx + 10} {ly - 30} L {lx - 10} {ly - 30} Z" fill="#ffe2a8" stroke="#6a5a3a" stroke-width="2"/>')
    s += f'<rect width="{W}" height="{H}" fill="url(#klamp)"/>'
    return svg_render(s)


KAABA_SILL = 560        # kaaba_close(): the golden threshold of the door at the top left (x 60-520); hands raised to it reach y 540-600


def kaaba_close():
    """close to the Kaaba's wall at night: the black cloth with its folds fills the frame down to the white floor (y 1420), the lower part of
    the golden door with its threshold at the top left (x 60-520, sill KAABA_SILL), a lamp's warm light from the right; a man stands at the
    wall at feet y ~1560 with his raised hands at the threshold"""
    s = "<defs>" + FILTERS + lg("kc", [(0, "#1c1a1e", 1), (1, "#0c0b0e", 1)]) + lg("kfl", [(0, "#d8d8e2", 1), (1, "#9a9aa8", 1)])
    s += rg("kl", 1000, 700, 1100, [(0, "#ffd8a0", 0.22), (0.5, "#a06a3a", 0.06), (1, "#000", 0)]) + "</defs>"
    s += f'<rect width="{W}" height="{H}" fill="url(#kc)"/>'
    r = random.Random(4230)
    for k in range(14):            # deep folds of the cloth
        x = -40 + k * 84 + r.uniform(-10, 10)
        s += (f'<path d="M {x} -20 C {x + 10} 400, {x - 8} 900, {x + 6} 1420" stroke="#2c2a32" stroke-width="10" fill="none" opacity="0.7"/>'
              f'<path d="M {x + 22} -20 C {x + 32} 400, {x + 14} 900, {x + 28} 1420" stroke="#060508" stroke-width="8" fill="none" opacity="0.7"/>')
    # a faint woven pattern in the black cloth
    for k in range(60):
        x, y = r.uniform(0, W), r.uniform(600, 1400)
        s += f'<path d="M {x:.0f} {y:.0f} c 8 -10, 18 -2, 12 8 c -6 8, -16 6, -12 -4" stroke="#26242a" stroke-width="3" fill="none" opacity="0.8"/>'
    # the golden door's lower part with its threshold
    s += ('<rect x="40" y="-40" width="500" height="580" fill="#141114" stroke="#c9a24a" stroke-width="4"/>'
          '<rect x="70" y="-40" width="440" height="560" rx="6" fill="#c9a24a" stroke="#6a4a18" stroke-width="4"/>'
          '<path d="M 290 -40 L 290 520" stroke="#6a4a18" stroke-width="4"/>')
    for row in range(3):
        for xx in (150, 230, 350, 430):
            yy = 120 + row * 150
            s += (f'<circle cx="{xx}" cy="{yy}" r="26" fill="none" stroke="#f0d48a" stroke-width="4"/><circle cx="{xx}" cy="{yy}" r="8" fill="#f0d48a"/>'
                  f'<path d="M {xx - 26} {yy} L {xx + 26} {yy} M {xx} {yy - 26} L {xx} {yy + 26}" stroke="#8a6a28" stroke-width="2"/>')
    s += (f'<rect x="20" y="{KAABA_SILL - 30}" width="540" height="36" fill="#b8bcc8" stroke="#3a3a44" stroke-width="3"/>'
          f'<path d="M 30 {KAABA_SILL - 22} L 550 {KAABA_SILL - 22}" stroke="#ffffff" stroke-width="3" opacity="0.6"/>')
    # the floor
    s += f'<rect x="0" y="1420" width="{W}" height="{H - 1420}" fill="url(#kfl)"/><path d="M 0 1420 L {W} 1420" stroke="#ffffff" stroke-width="5" opacity="0.6"/>'
    for k in range(6):
        yy = 1460 + k * k * 14
        s += f'<path d="M 0 {yy} L {W} {yy}" stroke="#ffffff" stroke-width="2" opacity="0.25"/>'
    s += f'<rect width="{W}" height="{H}" fill="url(#kl)"/>'
    return svg_render(s)


# ------------------------------------------------------------------ part 3: the plain where Nawfal fights Leyli's tribe
PLAIN_Y = 1060           # plain(): the far edge of the flat sand; people stand at feet y 1250-1800, riders at 1350-1750
TRIBE_TENTS = (600, 1060)     # plain(tents=True): Leyli's tribe's black tents far away on the right, x 600-1060, ground y 1075


def acacia(x, y, h, seed=0, col="#3a4a24", trunk="#4a3422"):
    """a flat-topped desert acacia: a thin forked trunk and a wide umbrella of leaves; base at (x, y)"""
    r = random.Random(seed)
    o = (f'<path d="M {x:.0f} {y:.0f} L {x - 6:.0f} {y - h * 0.55:.0f} L {x - h * 0.3:.0f} {y - h * 0.85:.0f} M {x - 6:.0f} {y - h * 0.55:.0f} '
         f'L {x + h * 0.25:.0f} {y - h * 0.88:.0f}" stroke="{trunk}" stroke-width="{max(2, h * 0.04):.1f}" fill="none" stroke-linecap="round"/>')
    for k in range(7):
        cx = x - h * 0.55 + k * h * 0.18 + r.uniform(-8, 8); cy = y - h * 0.9 + r.uniform(-8, 8)
        o += f'<ellipse cx="{cx:.0f}" cy="{cy:.0f}" rx="{h * 0.2:.0f}" ry="{h * 0.08:.0f}" fill="{col}"/>'
    o += f'<ellipse cx="{x:.0f}" cy="{y - h * 0.95:.0f}" rx="{h * 0.6:.0f}" ry="{h * 0.07:.0f}" fill="#ffffff" opacity="0.08"/>'
    return o


def plain(pal="day", tents=False):
    """the open sand plain between low dunes: far dunes on a low horizon (y 960-1040), a hazy band, the flat ground from PLAIN_Y with
    tracks, pebbles and dry tufts, a few far acacias and rocks; tents=True: Leyli's tribe's black tents with dark red banners far away on
    the right (TRIBE_TENTS)"""
    s = "<defs>" + FILTERS + _sky(pal)
    gdefs, gs = _ground(PLAIN_Y, pal, 4300)
    s += gdefs + "</defs>"
    s += _sky_draw(pal)
    s += f'<path d="{ridge(W, 965, 30, 4301, rough=0.3)}" fill="{SAND[pal][0][1]}" opacity="0.7"/>'
    for i, (base, amp) in enumerate(((990, 40), (1030, 50))):
        lit, shade = SAND[pal][i]
        s += _dune_row(4302 + i, base, amp, 420 * (1 + i * 0.3), 760 * (1 + i * 0.3), lit, shade, crest="#fff0d8")
    s += gs
    haze = {"dawn": "#ffe0c0", "day": "#fff4dc", "dusk": "#ffc890"}[pal]
    s += f'<rect x="0" y="{PLAIN_Y - 40}" width="{W}" height="90" fill="{haze}" opacity="0.35" filter="url(#b20)"/>'
    hz = {"dawn": "#5a4a5a", "day": "#5a6a4a", "dusk": "#3a2a3a"}[pal]
    r = random.Random(4305)
    for k in range(5):
        x = r.choice((r.uniform(40, 520), r.uniform(560, 1040)))
        s += acacia(x, PLAIN_Y + r.uniform(0, 20), r.uniform(50, 80), seed=4306 + k, col=hz, trunk=hz)
    for k in range(6):                       # a few rocks on the plain
        x = r.uniform(0, W); y = r.uniform(PLAIN_Y + 60, 1500); rr = 8 + (y - PLAIN_Y) * 0.05
        s += (f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{rr * 1.6:.0f}" ry="{rr:.0f}" fill="#8a6a4a" stroke="#3a2a1a" stroke-width="2"/>'
              f'<ellipse cx="{x - rr * 0.3:.0f}" cy="{y - rr * 0.3:.0f}" rx="{rr * 0.8:.0f}" ry="{rr * 0.4:.0f}" fill="#c8a882" opacity="0.6"/>')
    if tents:
        x0, x1 = TRIBE_TENTS
        light = {"dawn": "#ffb88a", "day": None, "dusk": "#ffa070"}[pal]
        s += black_tent(x0 + 160, x1 + 40, PLAIN_Y + 5, 70, depth=30, poles=2, rugs=False, back_pat=False, light=light)
        s += black_tent(x0, x0 + 260, PLAIN_Y + 15, 60, depth=26, poles=1, open_front=False, light=light)
        for k, bx in enumerate((x0 + 120, x0 + 330, x1 - 40)):
            yb = PLAIN_Y + 10
            wv = 8 * (k % 2)
            s += (f'<path d="M {bx} {yb} L {bx} {yb - 150}" stroke="#3a2414" stroke-width="4"/>'
                  f'<path d="M {bx} {yb - 150} L {bx - 60} {yb - 140 + wv} L {bx - 56} {yb - 110 + wv} L {bx} {yb - 118} Z" fill="#7a1418" stroke="#1a0606" stroke-width="2"/>')
        s += date_palm(x0 + 40, PLAIN_Y + 25, 200, lean=-0.05, seed=4310)
        s += date_palm(x1 + 10, PLAIN_Y + 30, 230, lean=0.04, seed=4311)
    if pal == "dusk":
        s += f'<rect width="{W}" height="{H}" fill="#4a2a5a" opacity="0.12"/>'
    return svg_render(s)
