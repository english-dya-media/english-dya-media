"""Scenery for the shadow-play episodes: skies, sun and moon, hills, trees,
reeds, water, tents, cities, fire, weather, interiors and particles."""
import math, random
import numpy as np
import skia
from anim import C, mix, mixc, clamp, ease, spath, ppath, paint, W, H

TAU = math.tau


def lin(c, y0, y1, stops, rect=None):
    """Vertical gradient; stops = [(pos, (r,g,b[,a])), ...]."""
    p = skia.Paint()
    p.setShader(skia.GradientShader.MakeLinear([skia.Point(0, y0), skia.Point(0, y1)],
                                               [C(*col) for _, col in stops], [s for s, _ in stops]))
    if rect is None:
        c.drawPaint(p)
    else:
        c.drawRect(skia.Rect.MakeLTRB(*rect), p)


def radial(c, x, y, r, stops, blend=None):
    p = skia.Paint(AntiAlias=True)
    p.setShader(skia.GradientShader.MakeRadial(skia.Point(x, y), r, [C(*col) for _, col in stops],
                                               [s for s, _ in stops]))
    if blend:
        p.setBlendMode(blend)
    c.drawCircle(x, y, r, p)


def glow(c, x, y, r, col, a=150, blend=skia.BlendMode.kScreen):
    radial(c, x, y, r, [(0.0, (*col, a)), (0.35, (*col, a * 0.45)), (1.0, (*col, 0))], blend)


def sun(c, x, y, r, core, edge, halo=600, ha=150, rays=0, t=0.0):
    radial(c, x, y, halo, [(0.3, (*edge, ha)), (0.58, (*edge, ha * 0.42)), (1.0, (*edge, 0))])
    if rays:
        rp = skia.Paint(AntiAlias=True)
        rp.setShader(skia.GradientShader.MakeRadial(skia.Point(x, y), 1150, [C(*core, 36), C(*core, 0)], [0.25, 1.0]))
        for i in range(rays):
            a = i * TAU / rays + t * 0.016 - 1.2
            wd = 0.04 + 0.02 * math.sin(i * 2.3)
            c.drawPath(ppath([(x, y), (x + 1150 * math.cos(a - wd), y + 1150 * math.sin(a - wd)),
                              (x + 1150 * math.cos(a + wd), y + 1150 * math.sin(a + wd))]), rp)
    radial(c, x, y - r * 0.22, r * 1.09, [(0.0, core), (0.55, core), (1.0, edge)])


def moon(c, x, y, r, col=(250, 244, 222), halo=(150, 180, 230)):
    glow(c, x, y, r * 6, halo, 90)
    radial(c, x, y, r, [(0.0, col), (0.85, col), (1.0, mixc(col, (200, 200, 210), 0.5))])
    for (dx, dy, rr) in ((-0.3, -0.2, 0.18), (0.25, 0.1, 0.22), (-0.05, 0.35, 0.12), (0.35, -0.35, 0.1)):
        c.drawCircle(x + dx * r, y + dy * r, rr * r, paint(C(210, 205, 196, 70)))


class Stars:
    def __init__(self, n=160, y1=900, seed=3):
        rnd = random.Random(seed)
        self.s = [(rnd.uniform(0, W), rnd.uniform(0, y1) ** 1.0, rnd.uniform(0.6, 2.2), rnd.uniform(0, 6.3),
                   rnd.uniform(0.6, 2.4)) for _ in range(n)]

    def draw(self, c, t, a=1.0, y_fade=900):
        p = skia.Paint(AntiAlias=True)
        for (x, y, r, ph, f) in self.s:
            tw = 0.55 + 0.45 * math.sin(t * f + ph)
            fade = clamp(1 - y / y_fade)
            p.setColor(C(255, 248, 230, 230 * a * tw * (0.35 + 0.65 * fade)))
            c.drawCircle(x, y, r, p)


def make_ridge(x0, x1, base, amp, seed, step=8, oct_=4, sharp=0.0):
    rnd = random.Random(seed)
    ph = [rnd.uniform(0, 6.3) for _ in range(oct_)]
    out = []
    x = x0
    while x <= x1:
        y = base
        for k in range(oct_):
            v = math.sin(x * 0.004 * (2.1 ** k) + ph[k])
            if sharp and k < 2:
                v = 1 - 2 * abs(v) ** (1 - sharp)
            y += amp / (1.9 ** k) * v
        out.append((x, y))
        x += step
    return out


def ridge(c, pts, col, bottom=2400, grad=None):
    path = ppath([(pts[0][0], bottom)] + pts + [(pts[-1][0], bottom)])
    if grad:
        p = skia.Paint(AntiAlias=True)
        p.setShader(skia.GradientShader.MakeLinear([skia.Point(0, grad[0]), skia.Point(0, grad[1])],
                                                   [C(*grad[2]), C(*grad[3])]))
        c.drawPath(path, p)
    else:
        c.drawPath(path, paint(C(*col)))


class Clouds:
    def __init__(self, ys, seed=5, lmin=420, lmax=900):
        rnd = random.Random(seed)
        self.k = [(rnd.uniform(-300, 1300), y, rnd.uniform(lmin, lmax), th, rnd.uniform(5, 12)) for y, th in ys]

    def draw(self, c, t, col, a=200, speed=1.0):
        for (x0, y, L, th, sp) in self.k:
            x = (x0 - sp * t * speed + 400) % 1900 - 400
            for k, (aa, sc) in enumerate(((a * 0.6, 1.0), (a, 0.6))):
                cp = skia.Path()
                cp.moveTo(x - L / 2 * sc, y)
                cp.cubicTo(x - L * 0.25 * sc, y - th * sc, x + L * 0.2 * sc, y - th * 0.8 * sc, x + L / 2 * sc, y + 2)
                cp.cubicTo(x + L * 0.2 * sc, y + th * 0.45 * sc, x - L * 0.2 * sc, y + th * 0.5 * sc, x - L / 2 * sc, y)
                c.drawPath(cp, paint(C(*col, aa)))


def storm_clouds(c, t, col, y0=180, rows=5, seed=11, speed=1.0, a=230):
    rnd = random.Random(seed)
    for r in range(rows):
        y = y0 + r * 95
        sp = (14 + r * 5) * speed
        for k in range(7):
            x = (rnd.uniform(0, 1500) + sp * t) % 1700 - 300
            rx, ry = rnd.uniform(160, 320), rnd.uniform(50, 90)
            p = skia.Paint(AntiAlias=True)
            cc = mixc(col, (0, 0, 0), r * 0.06)
            p.setShader(skia.GradientShader.MakeRadial(skia.Point(x, y), rx, [C(*cc, a), C(*cc, a * 0.7), C(*cc, 0)],
                                                       [0.0, 0.6, 1.0]))
            c.save()
            c.translate(x, y)
            c.scale(1, ry / rx)
            c.translate(-x, -y)
            c.drawCircle(x, y, rx, p)
            c.restore()


def tufts(c, items, t, col=(10, 5, 8), wind=0.25):
    pt = paint(C(*col))
    for (x, y, h, lean) in items:
        for k in range(-2, 3):
            tip = (x + k * 4 + (lean + wind * math.sin(t * 2 + x)) * h, y - h * (1 - abs(k) * 0.2))
            c.drawPath(ppath([(x + k * 3 - 2, y + 2), tip, (x + k * 3 + 2, y + 2)]), pt)


def tree(c, x, y, s, t, kind="plane", wind=0.0, seed=1, col=(10, 5, 8), fruit=None):
    """Silhouette tree: trunk, branches and leafy clusters that sway."""
    rnd = random.Random(seed)
    pt = paint(C(*col))
    sway = (wind * 6 + 1.2) * math.sin(t * (1.1 + wind * 1.4)) + wind * 8
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    if kind == "plane":
        c.drawPath(spath([(-34, 0, 0), (-22, -120), (-26, -260), (-10, -360), (14, -360), (24, -250), (26, -120),
                          (44, 0, 0)]), pt)
        branches = [((-14, -300), (-150, -440)), ((10, -330), (130, -470)), ((0, -350), (-30, -560)),
                    ((-10, -250), (-220, -330)), ((16, -260), (210, -350)), ((4, -360), (70, -560))]
        blobs = [(-150, -470, 110), (130, -500, 120), (-30, -600, 130), (-230, -360, 90), (220, -380, 95),
                 (70, -600, 110), (-80, -520, 120), (40, -440, 110), (-180, -560, 80), (180, -580, 80)]
    elif kind == "citron":
        c.drawPath(spath([(-14, 0, 0), (-10, -90), (-14, -170), (-4, -220), (8, -220), (14, -160), (12, -80),
                          (18, 0, 0)]), pt)
        branches = [((-6, -190), (-90, -280)), ((6, -200), (90, -300)), ((0, -215), (-10, -330))]
        blobs = [(-90, -300, 70), (90, -320, 74), (-10, -360, 80), (-40, -280, 60), (50, -270, 60), (0, -300, 70)]
    else:
        c.drawPath(spath([(-10, 0, 0), (-6, -100), (6, -100), (12, 0, 0)]), pt)
        branches = [((0, -90), (-50, -150)), ((0, -90), (50, -160))]
        blobs = [(-40, -170, 50), (40, -180, 50), (0, -200, 55)]
    for (a, b) in branches:
        bx = b[0] + sway * (-b[1] / 400)
        c.drawPath(spath([(a[0] - 7, a[1], 0), (mix(a[0], bx, 0.5) - 4, mix(a[1], b[1], 0.5)), (bx, b[1], 0),
                          (mix(a[0], bx, 0.5) + 4, mix(a[1], b[1], 0.5) + 3), (a[0] + 7, a[1], 0)]), pt)
    for i, (bx, by, r) in enumerate(blobs):
        dx = sway * (-by / 380) + 2 * math.sin(t * 2.3 + i)
        cx, cy = bx + dx, by
        pts = []
        n = 14
        for k in range(n):
            a = k * TAU / n
            rr = r * (0.82 + 0.18 * math.sin(k * 2.7 + i * 1.3) + 0.06 * math.sin(t * 3 + k + i))
            pts.append((cx + rr * math.cos(a), cy + rr * 0.8 * math.sin(a)))
        c.drawPath(spath(pts), pt)
    if fruit:
        for (fx, fy) in fruit:
            c.drawCircle(fx + sway * (-fy / 380), fy, 9, pt)
    c.restore()


def reeds(c, items, t, col=(10, 5, 8), wind=0.4):
    pt = paint(C(*col))
    for (x, y, h, ph) in items:
        bend = (wind + 0.15 * math.sin(t * 1.7 + ph)) * h * 0.18
        tip = (x + bend, y - h)
        c.drawPath(spath([(x - 2.5, y, 0), (x + bend * 0.4 - 1.5, y - h * 0.55), tip, (x + bend * 0.4 + 1.5, y - h * 0.55),
                          (x + 2.5, y, 0)]), pt)
        if ph > 3.5:
            c.save()
            c.translate(*tip)
            c.rotate(math.degrees(math.atan2(bend, h)) * 0.6)
            c.drawPath(spath([(0, 0), (6, -10), (4, -34), (0, -42), (-4, -34), (-6, -10)]), pt)
            c.restore()
        else:
            lf = (x + bend * 0.5 + 26 * (1 if ph > 1.7 else -1), y - h * 0.45 + 10)
            c.drawPath(spath([(x + bend * 0.3, y - h * 0.32, 0), (mix(x, lf[0], 0.5), y - h * 0.52), lf]), pt)


def water(c, y0, y1, t, top, bot, hl=(255, 220, 160), seed=4, n=26):
    lin(c, y0, y1, [(0.0, top), (1.0, bot)], (-400, y0, 1500, y1))
    rnd = random.Random(seed)
    p = skia.Paint(AntiAlias=True)
    for k in range(n):
        yy = mix(y0 + 4, y1 - 4, rnd.random())
        x = (rnd.uniform(-200, 1300) + 20 * t * (0.5 + rnd.random())) % 1500 - 200
        w = rnd.uniform(30, 120)
        p.setColor(C(*hl, 90 + 60 * math.sin(t * 3 + k)))
        c.drawRect(skia.Rect.MakeXYWH(x, yy, w, 2.2), p)


def tent(c, x, y, s, t, col=(10, 5, 8)):
    pt = paint(C(*col))
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    c.drawPath(spath([(-150, 0, 0), (-140, -70), (-100, -140), (-30, -186), (0, -196, 0), (30, -186), (100, -140),
                      (140, -70), (150, 0, 0)]), pt)
    c.drawRect(skia.Rect.MakeLTRB(-3, -250, 3, -190), pt)
    fl = [(3, -250)] + [(3 + u * 60, -250 + 6 * math.sin(t * 5 + u * 5) * u + u * 4) for u in (0.25, 0.5, 0.75, 1.0)]
    fl += [(3 + u * 60, -222 + 6 * math.sin(t * 5 + u * 5) * u) for u in (1.0, 0.75, 0.5, 0.25)] + [(3, -222)]
    c.drawPath(ppath(fl), pt)
    c.drawPath(spath([(-30, 0, 0), (-26, -80), (0, -104), (26, -80), (30, 0, 0)]), paint(C(255, 190, 120, 26)))
    c.restore()


def tower_ruin(c, x, y, s, col):
    pt = paint(C(*col))
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    c.drawPath(ppath([(-60, 0), (-52, -200), (-56, -214), (-40, -214), (-40, -236), (-26, -236), (-26, -210),
                      (-8, -228), (6, -196), (18, -240), (30, -244), (34, -206), (52, -210), (56, 0)]), pt)
    for (wx, wy) in ((-20, -150), (16, -110)):
        c.drawPath(spath([(wx - 7, wy + 18, 0), (wx - 7, wy), (wx, wy - 10), (wx + 7, wy), (wx + 7, wy + 18, 0)]),
                   paint(C(255, 200, 140, 40)))
    c.restore()


def city(w, h, base, seed=9, col=(10, 5, 8), windows=True, gate_x=None, torches=()):
    """Walled city skyline drawn once into an image of size (w, h); base is the
    wall foot y inside it. Returns (skia.Image, list of window/torch points)."""
    rnd = random.Random(seed)
    arr = np.zeros((h, w, 4), np.uint8)
    s = skia.Surface(arr)
    c = s.getCanvas()
    pt = paint(C(*col))
    lights = []
    # domes and buildings behind the wall
    x = 20
    while x < w - 60:
        bw = rnd.uniform(70, 150)
        bh = rnd.uniform(110, 230)
        c.drawRect(skia.Rect.MakeLTRB(x, base - 150 - bh, x + bw, base), pt)
        if rnd.random() < 0.45:
            r = bw * 0.42
            cx = x + bw / 2
            c.drawPath(spath([(cx - r, base - 150 - bh, 0), (cx - r * 0.9, base - 150 - bh - r * 0.7), (cx, base - 150 - bh - r * 1.25, 0),
                              (cx + r * 0.9, base - 150 - bh - r * 0.7), (cx + r, base - 150 - bh, 0)]), pt)
            c.drawRect(skia.Rect.MakeLTRB(cx - 1.5, base - 150 - bh - r * 1.25 - 26, cx + 1.5, base - 150 - bh - r * 1.2), pt)
        elif rnd.random() < 0.5:
            for k in range(int(bw // 18)):
                c.drawRect(skia.Rect.MakeLTRB(x + k * 18, base - 150 - bh - 12, x + k * 18 + 10, base - 150 - bh), pt)
        if windows:
            for k in range(rnd.randint(1, 3)):
                wx, wy = x + rnd.uniform(14, bw - 14), base - 150 - rnd.uniform(20, bh - 20)
                lights.append((wx, wy))
        x += bw + rnd.uniform(-20, 30)
    # tall towers
    for k in range(4):
        tx = rnd.uniform(60, w - 60)
        th = rnd.uniform(260, 360)
        c.drawRect(skia.Rect.MakeLTRB(tx - 22, base - th, tx + 22, base), pt)
        c.drawPath(ppath([(tx - 30, base - th), (tx, base - th - 50), (tx + 30, base - th)]), pt)
    # the wall with crenellations
    c.drawRect(skia.Rect.MakeLTRB(0, base - 150, w, base), pt)
    for k in range(int(w // 34) + 1):
        c.drawRect(skia.Rect.MakeLTRB(k * 34, base - 168, k * 34 + 20, base - 150), pt)
    for tx in range(0, w, 260):
        c.drawRect(skia.Rect.MakeLTRB(tx + 100, base - 210, tx + 160, base), pt)
        for k in range(3):
            c.drawRect(skia.Rect.MakeLTRB(tx + 100 + k * 22, base - 226, tx + 112 + k * 22, base - 210), pt)
    if gate_x is not None:
        p = skia.Paint(AntiAlias=True, Color=C(0, 0, 0, 0))
        p.setBlendMode(skia.BlendMode.kClear)
        c.drawPath(spath([(gate_x - 46, base, 0), (gate_x - 46, base - 92), (gate_x, base - 132, 0), (gate_x + 46, base - 92),
                          (gate_x + 46, base, 0)]), p)
    return skia.Image.fromarray(arr), lights


def flame(c, x, y, s, t, seed=0.0, a=1.0):
    """Animated flame shape (three coloured tongues)."""
    for k, (col, sc) in enumerate((((255, 110, 40), 1.0), ((255, 170, 60), 0.72), ((255, 236, 170), 0.42))):
        pts = []
        n = 9
        for i in range(n + 1):
            u = i / n
            side = math.sin(u * math.pi)
            wob = 0.18 * math.sin(t * 9 + u * 6 + seed + k) + 0.1 * math.sin(t * 17 + seed * 2)
            pts.append((x + (u - 0.5) * 2 * 30 * sc * s * (1 - 0.15 * side) + wob * 10 * s,
                        y - side * 6 * s))
        tipx = x + 8 * s * math.sin(t * 7 + seed) * sc
        tip = (tipx, y - (95 + 18 * math.sin(t * 11 + seed + k)) * sc * s)
        path = spath([pts[0], (x - 26 * sc * s, y - 40 * sc * s), (mix(x, tipx, 0.6) - 8 * sc * s, y - 72 * sc * s), tip + (0,),
                      (mix(x, tipx, 0.6) + 10 * sc * s, y - 70 * sc * s), (x + 26 * sc * s, y - 38 * sc * s), pts[-1],
                      (x, y + 4 * s)])
        c.drawPath(path, paint(C(*col, 235 * a)))


def campfire(c, x, y, s, t, sparks):
    glow(c, x, y - 60 * s, 520 * s, (255, 140, 60), 170)
    for k, dx in enumerate((-30, 0, 28)):
        flame(c, x + dx * s, y, s * (1.0 if k == 1 else 0.75), t, seed=k * 2.1)
    pt = paint(C(10, 5, 8))
    for k in range(4):
        a = math.radians(-20 + k * 14)
        c.drawPath(ppath([(x - 70 * s, y + 6 * s - k * 3), (x + 70 * s, y - 8 * s + k * 4), (x + 70 * s, y + 4 * s + k * 3),
                          (x - 70 * s, y + 14 * s)]), pt)
    p = skia.Paint(AntiAlias=True)
    for (sx, sp, ph, life) in sparks:
        u = ((t * sp / 120 + ph) % 1.0)
        px = x + sx * s + 30 * math.sin(t * 2 + ph * 10) * u
        py = y - 40 * s - u * 520 * s
        p.setColor(C(255, 190, 90, 230 * (1 - u)))
        c.drawCircle(px, py, 2.4 * (1 - u * 0.5), p)


def rain(c, t, n=160, a=90, seed=2, slant=0.32, y0=0, y1=1300):
    rnd = random.Random(seed)
    p = skia.Paint(AntiAlias=True, Color=C(200, 210, 230, a))
    p.setStrokeWidth(1.6)
    for k in range(n):
        x0 = rnd.uniform(-300, W + 100)
        sp = rnd.uniform(1300, 1800)
        y = (rnd.uniform(0, 2000) + sp * t) % (y1 - y0 + 200) + y0 - 100
        x = x0 + (y - y0) * slant
        ln = rnd.uniform(28, 48)
        c.drawLine(x, y, x + ln * slant, y + ln, p)


def bolt(c, x, y0, y1, seed, a=255):
    rnd = random.Random(seed)
    pts = [(x, y0)]
    yy, xx = y0, x
    while yy < y1:
        yy += rnd.uniform(30, 60)
        xx += rnd.uniform(-26, 26)
        pts.append((xx, yy))
    p = skia.Paint(AntiAlias=True, Color=C(230, 236, 255, a))
    p.setStyle(skia.Paint.kStroke_Style)
    p.setStrokeWidth(3)
    p.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 1.2))
    c.drawPath(ppath(pts, closed=False), p)


def birds(c, t, flock, col=(10, 5, 8)):
    pt = paint(C(*col))
    for (x0, y0, sp, sz, ph) in flock:
        x = (x0 + sp * t) % 1500 - 200 if sp > 0 else (x0 + sp * t) % 1500 - 200
        y = y0 + 8 * math.sin(t * 0.8 + ph)
        f = math.sin(t * 9 + ph)
        c.drawPath(spath([(x - sz, y - sz * 0.5 * f), (x - sz * 0.4, y - sz * 0.15 * f - 2), (x, y, 0),
                          (x + sz * 0.4, y - sz * 0.15 * f - 2), (x + sz, y - sz * 0.5 * f), (x + sz * 0.4, y + 2),
                          (x, y + 3, 0), (x - sz * 0.4, y + 2)]), pt)


def dust(c, x, y, r, t, col, a=110, seed=0):
    rnd = random.Random(seed)
    for k in range(6):
        dx, dy = rnd.uniform(-1, 1) * r, rnd.uniform(-0.4, 0.2) * r
        rr = r * rnd.uniform(0.5, 0.9) * (1 + 0.08 * math.sin(t * 2 + k))
        radial(c, x + dx, y + dy, rr, [(0.0, (*col, a)), (1.0, (*col, 0))])


def arch_path(x, y_bot, w, h):
    """Pointed Persian arch opening."""
    hw = w / 2
    return spath([(x - hw, y_bot, 0), (x - hw, y_bot - h + hw * 0.9), (x - hw * 0.62, y_bot - h + hw * 0.22),
                  (x, y_bot - h, 0), (x + hw * 0.62, y_bot - h + hw * 0.22), (x + hw, y_bot - h + hw * 0.9),
                  (x + hw, y_bot, 0)])


def lattice(w, h, cell=64, bar=7, col=(12, 6, 8)):
    """A carved screen of eight-pointed stars, drawn once into an image."""
    arr = np.zeros((h, w, 4), np.uint8)
    s = skia.Surface(arr)
    c = s.getCanvas()
    c.clear(C(*col))
    p = skia.Paint(AntiAlias=True, Color=C(0, 0, 0, 0))
    p.setBlendMode(skia.BlendMode.kClear)
    for j in range(-1, h // cell + 2):
        for i in range(-1, w // cell + 2):
            cx, cy = i * cell + (cell / 2 if j % 2 else 0), j * cell
            r = cell / 2 - bar
            star = []
            for k in range(16):
                a = k * TAU / 16
                rr = r if k % 2 == 0 else r * 0.62
                star.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
            c.drawPath(ppath(star), p)
    return skia.Image.fromarray(arr)


def hanging_lamp(c, x, y, s, t, chain=120, seed=0.0):
    pt = paint(C(10, 5, 8))
    sw = 3 * math.sin(t * 0.9 + seed)
    c.save()
    c.translate(x, y)
    c.rotate(sw * 0.3)
    c.drawRect(skia.Rect.MakeLTRB(-1.5, -chain, 1.5, 0), pt)
    c.scale(s, s)
    c.drawPath(spath([(-26, 0, 0), (-30, 18), (-18, 40), (0, 46), (18, 40), (30, 18), (26, 0, 0)]), pt)
    c.restore()
    glow(c, x, y + 30 * s, 260 * s, (255, 170, 80), 120 + 20 * math.sin(t * 6 + seed))
    flame(c, x, y + 4, 0.28 * s, t, seed)


def vignette_img(strength=150, cx=540, cy=760):
    v = np.zeros((H, W, 4), np.uint8)
    yy, xx = np.mgrid[0:H, 0:W]
    r = np.sqrt((xx - cx) ** 2 + ((yy - cy) / 1.25) ** 2) / 1150
    v[..., 3] = (np.clip((r - 0.45) / 0.55, 0, 1) ** 1.6 * strength).astype(np.uint8)
    return skia.Image.fromarray(v)


class Motes:
    """Floating dust or embers drifting through the frame."""

    def __init__(self, n=80, seed=1, y0=260, y1=1150):
        rnd = random.Random(seed)
        self.m = [(rnd.uniform(-100, 1180), rnd.uniform(y0, y1), rnd.uniform(1.2, 3.4), rnd.uniform(6, 22),
                   rnd.uniform(0, 6.3), rnd.uniform(0.3, 1.0)) for _ in range(n)]
        self.y0, self.y1 = y0, y1

    def draw(self, c, t, col, a=140, rise=6.0, drift=1.0):
        dp = skia.Paint(AntiAlias=True)
        dp.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 1.6))
        span = self.y1 - self.y0
        for (x0, y0, r, sp, ph, aa) in self.m:
            x = (x0 + sp * t * drift) % 1280 - 100
            y = (y0 - rise * t * aa + 10 * math.sin(t * 0.7 + ph) - self.y0) % span + self.y0
            fl = 0.55 + 0.45 * math.sin(t * 2.3 + ph * 3)
            dp.setColor(C(*col, a * aa * fl))
            c.drawCircle(x, y, r, dp)
