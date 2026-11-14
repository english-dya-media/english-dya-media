"""Episode 1 (The Lost Horse): every shot as a shadow-play scene.

Importing this module registers the scenes in anim.SCENES. Each scene draws
the frame at global time t; lt is the time inside the shot.
"""
import math, random
import skia
import anim
from anim import (C, mix, mixc, clamp, ease, sstep, _k, Cam, Pen, ANCH, TAG, rope, spath, ppath, paint,
                  fillp, begin_fig, taper, bez, W, H)
import puppets
from puppets import person, horse
import sets as S

TAU = math.tau
INK = (10, 5, 8)


def loc(an, sid, t):
    return t - an.start[sid], an.end[sid] - an.start[sid]


def jaw(an, role, t, k=8.0):
    return k * an.talk(role, t)


def get(an, key, fn):
    v = an.cache.get(key)
    if v is None:
        v = an.cache[key] = fn()
    return v


def vig(an, c, strength=150):
    c.save()
    c.resetMatrix()
    c.drawImage(get(an, ("vig", strength), lambda: S.vignette_img(strength)), 0, 0)
    c.restore()


def tag(name):
    TAG[0] = name


def A(name):
    return ANCH.get(name)


def tufts_list(seed, n, x0, x1, y, h0=10, h1=26):
    rnd = random.Random(seed)
    return [(rnd.uniform(x0, x1), y + rnd.uniform(-3, 3), rnd.uniform(h0, h1), rnd.uniform(-0.4, 0.4)) for _ in range(n)]


def reed_list(seed, n, x0, x1, y, h0, h1):
    rnd = random.Random(seed)
    return [(rnd.uniform(x0, x1), y + rnd.uniform(-6, 6), rnd.uniform(h0, h1), rnd.uniform(0, 6.3)) for _ in range(n)]


def ground(c, y, top, bot=(4, 2, 5), curve=0.0, x0=-600, x1=1700):
    g = skia.Path()
    g.moveTo(x0, y)
    g.quadTo(540, y + curve, x1, y)
    g.lineTo(x1, 2600)
    g.lineTo(x0, 2600)
    g.close()
    p = skia.Paint(AntiAlias=True)
    p.setShader(skia.GradientShader.MakeLinear([skia.Point(0, y), skia.Point(0, y + 600)],
                                               [C(*top), C(*mixc(top, bot, 0.6)), C(*bot)], [0.0, 0.25, 1.0]))
    c.drawPath(g, p)


# =============================================================== S02 poet
def s02(an, c, t):
    lt, dur = loc(an, "S02", t)
    zoom = 1 + 0.08 * ease(lt / dur)
    focus = (560, 640)
    cam = Cam(c, focus, zoom)
    st = get(an, "st02", lambda: S.Stars(120, 760, 4))
    hills = get(an, "hl02", lambda: S.make_ridge(250, 950, 690, 26, 3))
    S.lin(c, 0, H, [(0, (20, 11, 14)), (0.45, (38, 21, 21)), (1.0, (6, 3, 5))])
    fl = 0.9 + 0.08 * math.sin(t * 7.3) + 0.05 * math.sin(t * 13.1)
    with cam(0.5):
        win = S.arch_path(590, 740, 440, 540)
        c.save()
        c.clipPath(win, skia.ClipOp.kIntersect, True)
        S.lin(c, 200, 740, [(0, (8, 12, 38)), (0.65, (26, 34, 80)), (1, (62, 58, 100))])
        st.draw(c, t, 0.9, 740)
        S.moon(c, 680, 430, 40)
        S.ridge(c, hills, (16, 12, 30))
        c.restore()
        fp = skia.Paint(AntiAlias=True, Color=C(18, 10, 12))
        fp.setStyle(skia.Paint.kStroke_Style)
        fp.setStrokeWidth(24)
        c.drawPath(win, fp)
        c.drawRect(skia.Rect.MakeLTRB(586, 300, 594, 740), paint(C(18, 10, 12)))
    lx, ly = 792, 742
    S.glow(c, lx, ly, 680, (255, 158, 80), 125 * fl)
    with cam(1.0):
        ground(c, 830, (40, 20, 18), (6, 3, 5))
        S.glow(c, lx, 840, 300, (255, 150, 70), 50 * fl)
    look_up = sstep(11.3, 12.4, lt)
    write = 1 - look_up
    pen = (139 + 6 * math.sin(t * 5.1) * write, -275 + 4 * math.sin(t * 9.7) * write - look_up * 20)
    P = {"mode": "sit", "hand_kind": "pen", "hand": pen, "head": mix(9, -16, look_up) + 1.5 * math.sin(t * 1.3),
         "lean": mix(6, 0, look_up), "rhand": (-6, -262), "seed": 1.0}

    def figs(cc):
        with Cam(cc, focus, zoom)(1.0):
            person(cc, 400, 830, 1.15, 1, P, t, "poet")
            # lectern and lamp stool
            fillp(cc, ppath([(512, 830), (528, 830), (612, 744), (598, 742)]))
            fillp(cc, ppath([(608, 830), (592, 830), (510, 744), (524, 742)]))
            fillp(cc, ppath([(500, 742), (562, 752), (624, 738), (624, 746), (562, 760), (500, 750)]))
            fillp(cc, spath([(752, 830, 0), (758, 796, 0), (812, 796, 0), (818, 830, 0)]))
            fillp(cc, spath([(762, 796), (770, 782), (800, 780), (816, 772, 0), (824, 766, 0), (812, 786), (806, 796)]))
    an.figures(c, figs, (255, 176, 96), (200, 300, 900, 900))
    with cam(1.0):
        # the open manuscript, lit by the lamp; a page turns
        pg = paint(C(250, 226, 178))
        c.drawPath(ppath([(504, 706), (560, 718), (560, 748), (504, 736)]), pg)
        c.drawPath(ppath([(560, 718), (620, 702), (620, 734), (560, 748)]), pg)
        ln = paint(C(70, 40, 30, 150))
        for i in range(5):
            c.drawRect(skia.Rect.MakeLTRB(512, 712 + i * 5 + 0.2 * i, 552, 713.2 + i * 5), ln)
            c.drawRect(skia.Rect.MakeLTRB(568, 712 + i * 5 - 2 * i * 0.4, 612, 713.2 + i * 5 - 0.8 * i), ln)
        u = sstep(7.2, 8.6, lt)
        if 0 < u < 1:
            ex = mix(620, 504, u)
            lift = math.sin(u * math.pi) * 46
            c.drawPath(spath([(560, 718, 0), (mix(590, 532, u), 712 - lift * 0.8), (ex, mix(702, 706, u) - lift * 0.3, 0),
                              (ex, mix(734, 736, u) - lift * 0.3, 0), (mix(590, 532, u), 742 - lift * 0.8), (560, 748, 0)]),
                       paint(C(255, 236, 196)))
        S.flame(c, 822, 764, 0.42, t, 1.0)
        S.glow(c, 822, 744, 90, (255, 220, 150), 160 * fl)
    get(an, "mo02", lambda: S.Motes(60, 2, 300, 900)).draw(c, t, (255, 200, 140), 90, rise=4, drift=0.3)
    vig(an, c, 170)


# ============================================================ S03 storm
def s03(an, c, t):
    lt, dur = loc(an, "S03", t)
    zoom = 1 + 0.1 * ease(lt / dur)
    focus = (540, 560)
    cam = Cam(c, focus, zoom)
    calm = sstep(23.0, 30.0, lt)
    flashes = [2.2, 9.6, 17.2, 22.6]
    fl = 0.0
    for ft in flashes:
        if lt >= ft:
            d = lt - ft
            fl = max(fl, math.exp(-d * 7) + 0.6 * math.exp(-max(0, d - 0.18) * 9) * (d > 0.18))
    sky = [(0, mixc((10, 12, 24), (14, 16, 34), calm)), (0.45, mixc((40, 46, 70), (50, 50, 84), calm)),
           (0.75, mixc((96, 100, 124), (170, 120, 110), calm)), (1.0, mixc((130, 130, 146), (236, 168, 126), calm))]
    S.lin(c, 0, 900, [(p, mixc(col, (150, 160, 200), fl * 0.35)) for p, col in sky])
    with cam(0.3):
        if fl > 0.05:
            for ft, bx in zip(flashes, (180, 900, 260, 860)):
                if 0 <= lt - ft < 0.28:
                    S.glow(c, bx, 520, 520, (190, 200, 255), 160 * fl)
                    S.bolt(c, bx, 230, 760, int(ft * 10), 255)
        S.storm_clouds(c, t, mixc((30, 32, 48), (60, 46, 66), calm), 150, 6, 11, 1.0 + (1 - calm), 235 * (1 - 0.5 * calm))
    wind = 0.9 * (1 - calm) + 0.15
    gust = wind * (0.8 + 0.4 * math.sin(t * 0.9))
    with cam(1.0):
        hill = spath([(-300, 2400, 0), (-300, 1000), (200, 920), (540, 874), (880, 916), (1380, 1000), (1380, 2400, 0)])
        c.drawPath(hill, paint(C(*INK)))
        fruit_on = [(-80, -300), (-20, -360), (40, -270)]
        if lt < 5.6:
            fruit_on.append((70, -326))
        S.tree(c, 540, 880, 1.45, t, "citron", gust, 4, INK, fruit_on)
        # the unripe fruit torn off by the wind
        if lt >= 5.6:
            u = clamp((lt - 5.6) / 1.5)
            x0, y0 = 540 + 70 * 1.45, 880 - 326 * 1.45
            x1, y1 = 680, 868
            fx = mix(x0, x1, u) + 18 * math.sin(u * 3)
            fy = mix(y0, y1, u * u)
            if lt > 7.1:
                b = lt - 7.1
                fx = x1 + 22 * clamp(b / 0.6)
                fy = y1 - abs(math.sin(min(b, 0.6) / 0.6 * math.pi)) * 18 * (1 - clamp(b / 0.6)) + 2
            c.drawCircle(fx, fy, 11.5, paint(C(*INK)))
            c.drawPath(spath([(fx - 2, fy - 10), (fx + 6, fy - 20), (fx + 12, fy - 16), (fx + 4, fy - 9)]), paint(C(*INK)))
    leaves = get(an, "lv03", lambda: [(random.Random(k).uniform(0, 1), random.Random(k * 7).uniform(300, 900),
                                       random.Random(k * 3).uniform(0, 6)) for k in range(26)])
    lp = paint(C(*INK))
    for (u0, y0, ph) in leaves:
        u = (u0 + lt * 0.16 * (0.6 + wind)) % 1.0
        x = -60 + u * 1220
        y = y0 + 60 * math.sin(lt * 1.3 + ph) + u * 120
        c.save()
        c.translate(x, y)
        c.rotate(lt * 200 + ph * 50)
        c.drawPath(spath([(-7, 0), (0, -3), (7, 0), (0, 3)]), lp)
        c.restore()
    rn = sstep(0.0, 3.0, lt) * (1 - calm) * (0.7 + 0.5 * sstep(12, 16, lt))
    if rn > 0.02:
        S.rain(c, t, int(220 * rn), 110 * rn, 2, 0.28)
    vig(an, c, 160)


# ========================================================= S04 ridge
def simorgh(c, x, y, s, t):
    """The Simorgh in flight: crested head, great flapping wings, long eyed tail."""
    begin_fig(c, (x - 700 * s, y - 500 * s, x + 700 * s, y + 500 * s))
    c.save()
    c.translate(x, y)
    c.scale(-s, s)
    f = math.sin(t * 2.4)
    for k in range(4):
        pts = []
        L = 300 - k * 40
        for i in range(11):
            u = i / 10
            pts.append((-80 - u * L, 4 + k * 12 + u * 30 + 26 * math.sin(t * 2.2 - u * 3 + k) * u))
        taper(c, pts, 10 - k * 1.5, 3)
        ex, ey = pts[-1]
        fillp(c, spath([(ex - 18, ey), (ex, ey - 15), (ex + 16, ey), (ex, ey + 15)]))
        anim.hole(c, spath([(ex - 7, ey), (ex, ey - 6), (ex + 7, ey), (ex, ey + 6)]))

    def wing(amp, dx):
        tip = (-60 + dx, -22 - 230 * amp)
        lead = bez((40 + dx, -22), (20 + dx, -22 - 140 * amp), (-20 + dx, -22 - 210 * amp), tip, 9)
        trail = []
        for i in range(1, 8):
            u = i / 7
            px = mix(tip[0], -70 + dx, u)
            py = mix(tip[1], -6, u ** 0.8)
            trail.append((px - (16 if i % 2 else 0), py + (10 if i % 2 else 0), 0))
        fillp(c, spath(lead + trail + [(-20 + dx, -4), (30 + dx, -10)]))
    wing(0.75 * f, 26)
    fillp(c, spath([(110, -10), (80, -26), (20, -28), (-50, -20), (-96, -2), (-40, 16), (40, 18), (96, 8)]))
    fillp(c, spath([(92, -20), (128, -44), (150, -50), (166, -46), (180, -38, 0), (164, -32), (140, -28), (112, -6)]))
    for k in range(3):
        taper(c, [(146, -50), (134 - k * 8, -74 - k * 4), (118 - k * 12, -86 - k * 2)], 3.5, 1)
    anim.hole(c, spath([(152, -43, 0), (157, -45), (161, -42, 0), (157, -40)]))
    wing(f, 0)
    c.restore()
    c.restore()


def s04(an, c, t):
    lt, dur = loc(an, "S04", t)
    zoom = 1.08 - 0.08 * ease(lt / dur)
    focus = (620, 560)
    cam = Cam(c, focus, zoom)
    S.lin(c, 0, 820, [(0, (34, 36, 86)), (0.35, (98, 72, 128)), (0.62, (214, 128, 128)), (0.82, (250, 182, 140)),
                      (1.0, (255, 214, 160))])
    with cam(0.2):
        S.sun(c, 250, 812 - 30 * ease(lt / dur), 92, (255, 246, 214), (255, 196, 140), 520, 170)
        get(an, "cl04", lambda: S.Clouds([(250, 14), (330, 10), (420, 18), (520, 9)], 6)).draw(c, t, (120, 70, 110), 150, 0.6)
    layers = get(an, "rg04", lambda: [S.make_ridge(-600, 1700, b, a, sd, 8, 4, sh) for b, a, sd, sh in
                                      ((700, 60, 1, 0.4), (760, 46, 2, 0.3), (812, 30, 3, 0.2))])
    cols = [(150, 110, 150), (104, 76, 120), (62, 44, 82)]
    for k, (pts, col) in enumerate(zip(layers, cols)):
        with cam(0.3 + 0.2 * k):
            S.ridge(c, pts, col)
            S.lin(c, 640 + k * 60, 860 + k * 40, [(0, (*mixc(col, (255, 210, 190), 0.5), 0)),
                                                   (0.5, (*mixc(col, (255, 210, 190), 0.5), 90)),
                                                   (1, (*mixc(col, (255, 210, 190), 0.5), 0))], (-600, 640 + k * 60, 1700, 860 + k * 40))
    with cam(0.5):
        S.birds(c, t, get(an, "bd04", lambda: [(random.Random(k).uniform(0, 1400), random.Random(k + 9).uniform(330, 480),
                                                -38, random.Random(k + 3).uniform(6, 10), k) for k in range(7)]), (40, 24, 50))
    with cam(1.0):
        c.drawPath(spath([(-300, 2400, 0), (-300, 1000), (180, 960), (420, 905), (560, 876), (640, 864, 0), (720, 870),
                          (820, 900), (1000, 940), (1400, 990), (1400, 2400, 0)]), paint(C(*INK)))
    raise_m = sstep(17.6, 19.6, lt)
    P = {"hand_kind": "mace", "hand": (mix(98, 70, raise_m), mix(-300, -560, raise_m)), "mace": mix(0, -10, raise_m),
         "head": -3 + 2 * math.sin(t * 0.7), "stance": (54, 44), "wind": 0.8, "jaw": 0.0}
    sx = mix(1600, -600, clamp((lt - 6.6) / 9.0))

    def figs(cc):
        with Cam(cc, focus, zoom)(1.0):
            person(cc, 640, 866, 0.95, -1, P, t, "rostam")
        if 6.6 <= lt <= 15.6:
            with Cam(cc, focus, zoom)(0.6):
                simorgh(cc, sx, 330 + 24 * math.sin(lt * 0.8), 1.0, t)
    an.figures(c, figs, (255, 196, 150), (0, 120, 1080, 1000))
    vig(an, c, 140)


# ========================================================= S05 tiger skin
def s05(an, c, t):
    lt, dur = loc(an, "S05", t)
    S.lin(c, 0, H, [(0, (40, 8, 10)), (0.35, (150, 40, 18)), (0.6, (230, 110, 40)), (0.8, (120, 30, 14)), (1, (20, 4, 6))])
    S.glow(c, 540, 900, 900, (255, 150, 60), 110 + 20 * math.sin(t * 3))
    get(an, "mo05", lambda: S.Motes(140, 5, 100, 1500)).draw(c, t, (255, 190, 90), 220, rise=60, drift=0.3)
    pan = mix(-120, 140, ease(lt / dur))
    mace_up = sstep(8.6, 10.4, lt)
    puppets.STRIPE[0] = 190
    P = {"hand_kind": "oxmace", "hand": (mix(120, 112, mace_up), mix(-150, -330, mace_up)), "mace": mix(70, 6, mace_up),
         "head": -4, "wind": 1.0, "jaw": 0.0}

    def figs(cc):
        cc.save()
        cc.translate(0, pan * 0.5)
        person(cc, 400, 1960, 3.0, 1, P, t, "rostam")
        cc.restore()
    an.figures(c, figs, (255, 170, 80), (0, 0, 1080, 1500))
    puppets.STRIPE[0] = 75
    vig(an, c, 170)


# ===================================================== S06 valley + herd
def valley_sky(c, warm=0.0):
    S.lin(c, 0, 830, [(0, mixc((60, 96, 150), (70, 70, 130), warm)), (0.5, mixc((120, 160, 186), (190, 140, 130), warm)),
                      (0.85, mixc((226, 214, 170), (246, 184, 120), warm)), (1, mixc((246, 228, 180), (250, 206, 140), warm))])


def valley_hills(an, c, cam, kfar=0.3):
    layers = get(an, "rg06", lambda: [S.make_ridge(-600, 1700, b, a, sd, 8, 4, sh) for b, a, sd, sh in
                                      ((600, 120, 21, 0.5), (700, 70, 22, 0.3), (780, 40, 23, 0.1))])
    cols = [(110, 132, 150), (70, 92, 100), (40, 52, 56)]
    for k, (pts, col) in enumerate(zip(layers, cols)):
        with cam(kfar + 0.2 * k):
            S.ridge(c, pts, col)


def herd_list():
    rnd = random.Random(12)
    return [(rnd.uniform(-1100, -500), rnd.uniform(735, 790), rnd.uniform(0.27, 0.36), rnd.uniform(0, 1)) for _ in range(7)]


def s06(an, c, t):
    lt, dur = loc(an, "S06", t)
    if lt < 5.8:
        focus = (540, 600)
        zoom = 1 + 0.05 * ease(lt / 5.8)
        cam = Cam(c, focus, zoom)
        valley_sky(c, 0.2)
        valley_hills(an, c, cam)
        with cam(0.8):
            ground(c, 860, (34, 40, 32))
        sink = sstep(1.2, 2.8, lt) * (0.85 + 0.1 * math.sin(lt * 9) * sstep(2.8, 3.4, lt))
        press = sstep(0.6, 1.4, lt)
        Ph = {"gait": "stand", "sink": sink, "head": 10 * sink, "neck": 8 * sink, "saddle": False}
        Pr = {"hand": (mix(60, 122, press), mix(-300, -276 + 20 * sink, press)), "hand_kind": "open", "lean": 7 * press,
              "head": 6 * press, "stance": (60, 50)}

        def figs(cc):
            with Cam(cc, focus, zoom)(1.0):
                horse(cc, 560, 868, 0.9, 1, Ph, t)
                person(cc, 300, 868, 1.0, 1, Pr, t, "young_rostam")
        an.figures(c, figs, (255, 226, 170), (0, 200, 1080, 1000))
        vig(an, c, 130)
        return
    lt2 = lt - 5.8
    focus = (540, 640)
    zoom = 1 + 0.06 * ease(lt2 / 10)
    cam = Cam(c, focus, zoom)
    valley_sky(c, 0.1)
    valley_hills(an, c, cam)
    with cam(0.75):
        ground(c, 800, (46, 58, 46), (10, 12, 10))
        for (x0, y, s, ph) in herd_list():
            x = x0 + 150 * lt2 + 540
            S.dust(c, x - 120 * s, y - 30 * s, 90 * s, t, (200, 190, 150), 70, int(ph * 99))
    with cam(1.0):
        c.drawPath(spath([(-300, 2400, 0), (-300, 860), (100, 868), (380, 884), (700, 940), (1400, 1000),
                          (1400, 2400, 0)]), paint(C(*INK)))
    point = sstep(10.6, 11.4, lt2 + 5.8 - 5.8 + 0.0) if False else sstep(4.8, 5.6, lt2)

    def herd(cc):
        with Cam(cc, focus, zoom)(0.75):
            for i, (x0, y, s, ph) in enumerate(herd_list()):
                if i == 3:
                    continue
                horse(cc, x0 + 150 * lt2 + 540, y, s, 1, {"gait": "gallop", "phase": t * 1.8 + ph}, t)
        with Cam(cc, focus, zoom)(1.0):
            person(cc, 330, 876, 0.85, 1, {"hand": (mix(30, 190, point), mix(-262, -450, point)),
                                          "hand_kind": "open" if point > 0.5 else "fist", "head": -4 * point,
                                          "jaw": jaw(an, "ROSTAM", t), "stance": (50, 40)}, t, "young_rostam")
            person(cc, 150, 872, 0.82, 1, {"hand_kind": "staff", "hand": (60, -300), "rhand": (-24, -262),
                                          "lean": 4, "head": 4}, t, "herdsman")

    def colt(cc):
        x0, y, s, ph = herd_list()[3]
        with Cam(cc, focus, zoom)(0.75):
            horse(cc, x0 + 150 * lt2 + 540, y, s * 0.92, 1, {"gait": "gallop", "phase": t * 1.9 + ph}, t)
    an.figures(c, herd, (255, 226, 170), (0, 200, 1080, 1000))
    an.figures(c, colt, (255, 120, 140), (0, 400, 1080, 900), alpha=210)
    vig(an, c, 130)


def s06b(an, c, t):
    lt, dur = loc(an, "S06b", t)
    focus = (600, 560)
    zoom = 1 + 0.05 * ease(lt / dur)
    cam = Cam(c, focus, zoom)
    valley_sky(c, 0.15)
    valley_hills(an, c, cam, 0.2)
    with cam(0.5):
        ground(c, 800, (46, 58, 46), (10, 12, 10))
    warn = sstep(8.6, 9.4, lt) * (1 - sstep(13.5, 14.5, lt))

    def figs(cc):
        with Cam(cc, focus, zoom)(0.5):
            for i in range(5):
                x = (i * 230 + 70 * lt) % 1500 - 200
                horse(cc, x, 790 + (i % 2) * 8, 0.16, 1, {"gait": "gallop", "phase": t * 1.8 + i * 0.3}, t)
        with Cam(cc, focus, zoom)(1.0):
            person(cc, 660, 1400, 1.95, -1, {"hand_kind": "open", "hand": (mix(40, 116, warn), mix(-262, -430, warn)),
                                            "rhand_kind": "staff", "rhand": (-10, -300), "jaw": jaw(an, "HERDSMAN", t, 9),
                                            "head": 2 * math.sin(t * 0.9), "lean": 3}, t, "herdsman")
    an.figures(c, figs, (255, 226, 170), (0, 0, 1080, 1500))
    vig(an, c, 140)


def s06c(an, c, t):
    lt, dur = loc(an, "S06c", t)
    focus = (540, 620)
    zoom = 1 + 0.05 * ease(lt / dur)
    cam = Cam(c, focus, zoom)
    valley_sky(c, 0.25)
    valley_hills(an, c, cam)
    with cam(0.8):
        ground(c, 860, (36, 44, 34))
    # the mare: charges, rears at the roar, wheels away
    if lt < 2.8:
        mx, mface, mg = mix(1300, 990, ease(lt / 2.8)), -1, {"gait": "gallop", "phase": t * 2.0}
    elif lt < 4.2:
        r = math.sin(clamp((lt - 2.8) / 1.4) * math.pi) * 40
        mx, mface, mg = 990, -1, {"gait": "rear", "rear": r}
    else:
        mx, mface, mg = mix(990, 1550, clamp((lt - 4.2) / 3.2)), 1, {"gait": "gallop", "phase": t * 2.0}
    roar = sstep(2.9, 3.3, lt) * (1 - sstep(4.6, 5.4, lt))
    walk = clamp((lt - 7.0) / 4.0)
    rx = mix(330, 510, ease(walk))
    on_back = sstep(10.6, 11.6, lt)
    Pr = {"mode": "walk" if 0 < walk < 1 else "stand", "phase": (lt - 7.0) * 5.2,
          "hand": (mix(40, 94, on_back), mix(-262, -226, on_back)) if roar < 0.01 else (60, -540),
          "hand_kind": "open", "rhand": (-40, -540) if roar > 0.01 else (60, -300), "rhand_kind": "open" if roar > 0.01 else "fist",
          "head": -15 * roar + 4 * on_back, "lean": -5 * roar + 5 * on_back, "jaw": 12 * roar, "stance": (54, 44)}

    def figs(cc):
        with Cam(cc, focus, zoom)(1.0):
            tag("mare:")
            if lt < 7.5:
                horse(cc, mx, 868, 0.66, mface, mg, t)
            tag("colt:")
            horse(cc, 650, 868, 0.62, 1, {"gait": "stand", "head": 6 * math.sin(t * 0.8) - 6 * roar,
                                         "sink": 0.04 * on_back * (1 + math.sin(t * 6)) * 0.5}, t)
            tag("hm:")
            person(cc, 150, 868, 0.82, 1, {"hand_kind": "staff", "hand": (60, -300), "jaw": jaw(an, "HERDSMAN", t),
                                          "head": 3, "lean": 4}, t, "herdsman")
            tag("yr:")
            person(cc, rx, 868, 0.85, 1, Pr, t, "young_rostam")
            tag("")
        rope(cc, A("yr:rhand"), A("colt:neck"), 50, 2.2)
    an.figures(c, figs, (255, 226, 170), (0, 200, 1080, 1000), anchors=True)
    vig(an, c, 130)


# =================================================== S07 Rakhsh at sunset
def s07(an, c, t):
    lt, dur = loc(an, "S07", t)
    focus = (540, 560)
    zoom = 1 + 0.08 * ease(lt / dur)
    cam = Cam(c, focus, zoom)
    S.lin(c, 0, 860, [(0, (30, 8, 34)), (0.3, (110, 20, 60)), (0.6, (220, 70, 60)), (0.82, (250, 150, 80)), (1, (255, 200, 120))])
    with cam(0.25):
        S.sun(c, 560, 640 + 40 * ease(lt / dur), 240, (255, 236, 190), (255, 150, 90), 640, 160, 9, t)
        get(an, "cl07", lambda: S.Clouds([(260, 16), (340, 12), (430, 20)], 8)).draw(c, t, (70, 14, 40), 190)
    rg = get(an, "rg07", lambda: (S.make_ridge(-600, 1700, 800, 40, 31), S.make_ridge(-600, 1700, 838, 18, 32)))
    with cam(0.4):
        S.ridge(c, rg[0], (110, 34, 60))
    with cam(0.55):
        S.ridge(c, rg[1], (60, 16, 36))
    with cam(0.8):
        ground(c, 862, (50, 18, 22))
        S.tufts(c, get(an, "tf07", lambda: tufts_list(7, 40, -200, 1300, 866)), t)
    P = {"hand": (172 + 6 * math.sin(t * 1.6), -356 + 10 * math.sin(t * 1.6)), "hand_kind": "open",
         "jaw": jaw(an, "ROSTAM", t, 6), "head": 4 + 2 * math.sin(t * 0.6), "stance": (50, 44)}
    Ph = {"gait": "stand", "neck": 22 + 6 * math.sin(t * 0.9), "head": 8 + 4 * math.sin(t * 1.2), "saddle": True}

    def figs(cc):
        with Cam(cc, focus, zoom)(1.0):
            horse(cc, 800, 868, 0.95, -1, Ph, t)
            person(cc, 330, 868, 1.0, 1, P, t, "rostam")
    an.figures(c, figs, (255, 190, 120), (0, 100, 1080, 1000))
    vig(an, c, 150)


# ================================================= S08 the border lands
def s08(an, c, t):
    lt, dur = loc(an, "S08", t)
    pan = 260 * ease(lt / dur)
    S.lin(c, 0, 860, [(0, (52, 70, 120)), (0.45, (140, 140, 160)), (0.8, (236, 196, 140)), (1, (250, 218, 160))])
    S.sun(c, 900 - pan * 0.1, 690, 70, (255, 246, 214), (255, 210, 150), 460, 120)
    get(an, "cl08", lambda: S.Clouds([(240, 18), (300, 12), (380, 22), (470, 10), (560, 14)], 9)).draw(c, t, (90, 80, 110), 150)
    layers = get(an, "rg08", lambda: [S.make_ridge(-800, 2200, b, a, sd, 8, 4, sh) for b, a, sd, sh in
                                      ((690, 70, 41, 0.6), (760, 40, 42, 0.2), (820, 22, 43, 0.0))])
    cols = [(130, 120, 150), (96, 84, 100), (62, 52, 58)]
    for k, (pts, col) in enumerate(zip(layers, cols)):
        c.save()
        c.translate(-pan * (0.2 + 0.3 * k), 0)
        S.ridge(c, pts, col)
        if k == 1:
            S.tower_ruin(c, 900, 748, 0.8, col)
        c.restore()
    c.save()
    c.translate(-pan * 0.8, 0)
    river = spath([(-400, 846), (100, 836), (400, 850), (700, 838), (1000, 852), (1400, 842), (1800, 850),
                   (1800, 868), (1400, 860), (1000, 872), (700, 858), (400, 870), (100, 856), (-400, 866)])
    c.drawPath(river, paint(C(236, 196, 150)))
    ground(c, 880, (30, 22, 24))
    S.tufts(c, get(an, "tf08", lambda: tufts_list(8, 70, -400, 2000, 884, 12, 30)), t)
    c.restore()

    def figs(cc):
        cc.save()
        cc.translate(-pan * 0.5, 0)
        horse(cc, mix(200, 900, lt / dur), 778, 0.13, 1, {"gait": "walk", "phase": t * 0.9, "rider": "rider",
                                                          "rider_pose": {"hand": (100, -300)}}, t)
        cc.restore()
    an.figures(c, figs, (255, 220, 170), (0, 600, 1080, 900))
    S.birds(c, t, get(an, "bd08", lambda: [(random.Random(k).uniform(0, 1400), random.Random(k + 5).uniform(300, 420),
                                            34, random.Random(k + 2).uniform(6, 11), k) for k in range(9)]))
    vig(an, c, 130)


# ===================================================== S09 dawn at the tent
def s09(an, c, t):
    lt, dur = loc(an, "S09", t)
    focus = (540, 600)
    zoom = 1 + 0.06 * ease(lt / dur)
    cam = Cam(c, focus, zoom)
    S.lin(c, 0, 860, [(0, (16, 20, 52)), (0.4, (60, 62, 116)), (0.75, (190, 130, 150)), (1, (244, 196, 170))])
    with cam(0.2):
        get(an, "st09", lambda: S.Stars(70, 500, 9)).draw(c, t, 0.5, 500)
        S.glow(c, 760, 860, 600, (255, 190, 160), 110)
    rg = get(an, "rg09", lambda: (S.make_ridge(-600, 1700, 790, 50, 51, 8, 4, 0.3), S.make_ridge(-600, 1700, 836, 20, 52)))
    with cam(0.4):
        S.ridge(c, rg[0], (90, 76, 120))
        S.lin(c, 760, 860, [(0, (230, 200, 210, 0)), (0.6, (230, 200, 210, 110)), (1, (230, 200, 210, 0))], (-600, 760, 1700, 860))
    with cam(0.6):
        S.ridge(c, rg[1], (44, 36, 60))
    with cam(0.85):
        ground(c, 862, (30, 26, 40))
    belt = sstep(10.2, 11.0, lt) * (1 - sstep(12.4, 13.0, lt))
    quiver = lt > 12.7
    P = {"hand": (mix(40, 50, belt), mix(-262, -268, belt)) if belt > 0 else (40 + 4 * math.sin(t), -262),
         "rhand": (mix(-30, 20, belt), -270) if belt > 0 else (-30, -262), "jaw": jaw(an, "ROSTAM", t, 6),
         "head": mix(8, -2, sstep(9, 11, lt)) + 2 * math.sin(t * 0.7), "quiver": quiver, "stance": (50, 40)}

    def figs(cc):
        with Cam(cc, focus, zoom)(1.0):
            S.tent(cc, 220, 866, 1.1, t, INK)
            horse(cc, 860, 868, 0.72, -1, {"gait": "stand", "saddle": True, "neck": 4 + 4 * math.sin(t * 0.5),
                                           "head": 3 * math.sin(t * 0.8)}, t)
            person(cc, 520, 868, 0.82, 1, P, t, "rostam")
    an.figures(c, figs, (255, 206, 186), (0, 200, 1080, 1000))
    vig(an, c, 140)


# ================================================= S10 / S11 the gallop
class Scroller:
    def __init__(self, seed):
        rnd = random.Random(seed)
        self.rocks = [(rnd.uniform(0, 2400), rnd.uniform(16, 44)) for _ in range(9)]
        self.tufts = [(rnd.uniform(0, 2400), rnd.uniform(14, 34), rnd.uniform(-0.5, 0.2)) for _ in range(40)]
        self.near = S.make_ridge(0, 2400, 900, 0, seed)
        self.mid = S.make_ridge(-200, 2600, 780, 50, seed + 1, 10)
        self.far = S.make_ridge(-200, 2600, 730, 80, seed + 2, 10, 4, 0.5)

    def draw(self, c, t, speed, cols):
        for k, (pts, col, f) in enumerate(((self.far, cols[0], 0.06), (self.mid, cols[1], 0.2))):
            off = (speed * f * t) % 2400
            for dx in (-off, 2400 - off):
                c.save()
                c.translate(dx, 0)
                S.ridge(c, pts, col)
                c.restore()
        ground(c, 870, cols[2], (4, 2, 5), 0, -600, 1700)
        off = (speed * t) % 2400
        pt = paint(C(*INK))
        for (x, r) in self.rocks:
            xx = (x - off) % 2400 - 300
            c.drawPath(spath([(xx - r, 878, 0), (xx - r * 0.6, 878 - r * 0.7), (xx + r * 0.3, 878 - r * 0.8),
                              (xx + r, 878, 0)]), pt)
        S.tufts(c, [((x - off) % 2400 - 300, 880, h, l) for (x, h, l) in self.tufts], t, INK, 0.5)


def gallop_sky(c, t):
    S.lin(c, 0, 880, [(0, (40, 70, 130)), (0.5, (150, 160, 180)), (0.85, (246, 206, 150)), (1, (252, 224, 170))])


def s10(an, c, t):
    lt, dur = loc(an, "S10", t)
    gallop_sky(c, t)
    S.sun(c, 860, 720, 80, (255, 248, 220), (255, 214, 150), 480, 140)
    sc = get(an, "sc10", lambda: Scroller(61))
    sc.draw(c, lt, 900, [(150, 140, 170), (90, 80, 100), (40, 30, 34)])
    for k in range(5):
        u = ((lt * 2.2 + k * 0.2) % 1.0)
        S.dust(c, 330 - u * 380, 860 - u * 40, 40 + u * 90, t, (220, 190, 150), 90 * (1 - u), k)
    ph = t * 1.9
    P = {"gait": "gallop", "phase": ph, "saddle": True, "rider": "rostam",
         "rider_pose": {"lean": 12, "hand": (120, -330), "hand_kind": "mace", "mace": 60, "head": 4, "wind": 1.2}}

    def figs(cc):
        horse(cc, 520, 872, 0.82, 1, P, t)
    an.figures(c, figs, (255, 220, 170), (0, 200, 1080, 1000))
    vig(an, c, 130)


def s11(an, c, t):
    lt, dur = loc(an, "S11", t)
    gallop_sky(c, t)
    S.sun(c, 200, 700, 80, (255, 248, 220), (255, 214, 150), 480, 140)
    sc = get(an, "sc11", lambda: Scroller(71))
    sc.draw(c, lt, 820, [(140, 130, 160), (96, 82, 96), (46, 34, 34)])
    for k in range(5):
        u = ((lt * 2.2 + k * 0.2) % 1.0)
        S.dust(c, 210 - u * 300, 860 - u * 40, 40 + u * 90, t, (220, 190, 150), 90 * (1 - u), k)
        S.dust(c, 620 - u * 300, 860 - u * 40, 30 + u * 70, t, (220, 190, 150), 70 * (1 - u), k + 9)
    throw = lt >= 9.6
    caught = clamp((lt - 9.9) / 2.0)
    fist = sstep(14.2, 14.6, lt)
    rp = {"lean": 10, "head": 2, "wind": 1.2, "jaw": jaw(an, "ROSTAM", t, 8)}
    if not throw:
        rp.update({"hand": (60, -540), "hand_kind": "lasso"})
    elif fist > 0:
        rp.update({"hand": (70, -560), "hand_kind": "fist", "rhand": (100, -330)})
    else:
        rp.update({"hand": (150, -360), "hand_kind": "fist"})
    ons = [(720, 0.5, 0.1), (900, 0.46, 0.55), (1040, 0.44, 0.3), (820, 0.4, 0.8)]

    def figs(cc):
        for i, (x, s, ph) in enumerate(ons):
            xx = x + 40 * math.sin(lt * 0.5 + i) - (caught * 330 if i == 0 else 0)
            g = {"gait": "gallop", "phase": t * 2.1 + ph}
            if i == 0 and caught >= 1:
                g = {"gait": "rear", "rear": 22 + 6 * math.sin(t * 6)}
            tag(f"on{i}:")
            horse(cc, xx, 866 - i * 6, s, 1, g, t, "onager")
        tag("rk:")
        horse(cc, 300, 872, 0.78, 1, {"gait": "gallop", "phase": t * 1.95, "saddle": True, "rider": "rostam",
                                      "rider_pose": rp}, t)
        tag("")
        if throw:
            rope(cc, A("rk:hand"), A("on0:neck"), 20 * (1 - caught) + 10, 2.2)
    an.figures(c, figs, (255, 220, 170), (0, 200, 1080, 1000), anchors=throw)
    vig(an, c, 130)


# ======================================================== S12 campfire
def s12(an, c, t):
    lt, dur = loc(an, "S12", t)
    focus = (560, 640)
    zoom = 1 + 0.07 * ease(lt / dur)
    cam = Cam(c, focus, zoom)
    S.lin(c, 0, 820, [(0, (10, 12, 34)), (0.5, (36, 34, 78)), (0.85, (110, 64, 86)), (1, (170, 94, 80))])
    with cam(0.2):
        get(an, "st12", lambda: S.Stars(130, 700, 12)).draw(c, t, 0.7, 700)
    rg = get(an, "rg12", lambda: S.make_ridge(-600, 1700, 800, 34, 81))
    with cam(0.5):
        S.ridge(c, rg, (34, 22, 46))
    with cam(0.85):
        ground(c, 862, (34, 18, 20))
    sparks = get(an, "sp12", lambda: [(random.Random(k).uniform(-60, 60), random.Random(k + 1).uniform(40, 90),
                                        random.Random(k + 2).uniform(0, 1), 1) for k in range(40)])
    lean = sstep(14.3, 15.5, lt)
    P = {"mode": "sit", "hand": (mix(150, 60, lean), mix(-300, -280, lean)), "hand_kind": "open",
         "rhand": (-40, -262), "jaw": jaw(an, "ROSTAM", t, 7), "head": mix(6, -10, lean) + 2 * math.sin(t * 0.8),
         "lean": mix(4, -9, lean)}

    def figs(cc):
        with Cam(cc, focus, zoom)(0.55):
            horse(cc, 930, 800, 0.36, -1, {"gait": "graze"}, t)
        with Cam(cc, focus, zoom)(1.0):
            for x in (470, 760):
                fillp(cc, ppath([(x - 5, 866), (x + 5, 866), (x + 5, 700), (x - 5, 700)]))
                fillp(cc, ppath([(x - 4, 708), (x - 22, 676), (x - 16, 674), (x, 700)]))
                fillp(cc, ppath([(x + 4, 708), (x + 22, 676), (x + 16, 674), (x, 700)]))
            fillp(cc, ppath([(420, 690), (820, 694), (820, 704), (420, 700)]))
            fillp(cc, spath([(540, 698), (548, 668), (580, 652), (640, 650), (684, 664), (700, 696), (650, 712),
                             (580, 712)]))
            person(cc, 300, 868, 1.0, 1, P, t, "rostam_bare")
    an.figures(c, figs, (255, 150, 70), (0, 300, 1080, 1000), alpha=170)
    with cam(1.0):
        S.campfire(c, 615, 862, 1.05, t, sparks)
    vig(an, c, 160)


# ================================================== S13 / S17 the meadow
def meadow(an, c, t, cam, warm):
    S.lin(c, 0, 860, [(0, mixc((60, 90, 130), (70, 50, 90), warm)), (0.5, mixc((170, 170, 160), (220, 130, 100), warm)),
                      (0.85, mixc((240, 210, 150), (250, 170, 100), warm)), (1, mixc((250, 226, 170), (255, 200, 130), warm))])
    with cam(0.2):
        S.sun(c, 820, 700 + 60 * warm, 70, (255, 248, 220), mixc((255, 214, 150), (255, 160, 90), warm), 520, 150)
    rg = get(an, "rg13", lambda: (S.make_ridge(-600, 1700, 770, 36, 91), S.make_ridge(-600, 1700, 812, 16, 92)))
    with cam(0.4):
        S.ridge(c, rg[0], mixc((110, 120, 120), (130, 80, 90), warm))
    with cam(0.55):
        S.ridge(c, rg[1], mixc((60, 70, 60), (70, 40, 46), warm))
    with cam(0.8):
        ground(c, 800, mixc((110, 116, 90), (130, 84, 70), warm), mixc((80, 84, 64), (90, 60, 50), warm))
        S.water(c, 826, 866, t, mixc((244, 228, 180), (252, 190, 130), warm), mixc((200, 190, 150), (220, 140, 100), warm))
        ground(c, 866, (16, 10, 10))
        S.tufts(c, get(an, "tf13", lambda: tufts_list(13, 50, -300, 1400, 868, 10, 28)), t, INK, 0.35)
        S.reeds(c, get(an, "rd13", lambda: reed_list(14, 26, 900, 1300, 870, 90, 170)), t, INK, 0.3)


def s13(an, c, t):
    lt, dur = loc(an, "S13", t)
    focus = (540, 640)
    zoom = 1 + 0.06 * ease(lt / dur)
    cam = Cam(c, focus, zoom)
    meadow(an, c, t, cam, 0.0)

    def figs(cc):
        with Cam(cc, focus, zoom)(0.9):
            S.tree(cc, 250, 866, 1.05, t, "plane", 0.15, 2, INK)
        with Cam(cc, focus, zoom)(1.0):
            horse(cc, 900, 872, 0.62, -1, {"gait": "graze", "tail": 10 * math.sin(t * 1.4)}, t)
            person(cc, 720, 870, 0.82, 1, {"mode": "lie", "jaw": jaw(an, "ROSTAM", t, 6), "head": 4,
                                          "hand": (30, -300), "rhand": (-20, -270)}, t, "rostam_bare")
            fillp(cc, spath([(250, 870, 0), (254, 846), (268, 834), (288, 834), (300, 846), (304, 870, 0)]))
            fillp(cc, ppath([(320, 862), (440, 856), (440, 866), (320, 870)]))
            cc.drawCircle(446, 860, 14, anim.ink()) if Pen.mode != "anchor" else None
    an.figures(c, figs, (255, 226, 170), (0, 0, 1080, 1000))
    bf = get(an, "bf13", lambda: [(random.Random(k).uniform(0, 1000), random.Random(k + 4).uniform(600, 820), k) for k in range(3)])
    for (x0, y0, k) in bf:
        x = x0 + 40 * math.sin(t * 0.5 + k)
        y = y0 + 30 * math.sin(t * 0.9 + k * 2)
        f = abs(math.sin(t * 14 + k))
        c.drawPath(spath([(x, y, 0), (x - 9 * f, y - 8), (x - 3, y), (x - 9 * f, y + 6), (x, y, 0), (x + 9 * f, y + 6),
                          (x + 3, y), (x + 9 * f, y - 8)]), paint(C(*INK)))
    vig(an, c, 140)


def s17(an, c, t):
    lt, dur = loc(an, "S17", t)
    focus = (540, 640)
    zoom = 1.04 - 0.04 * ease(lt / dur)
    cam = Cam(c, focus, zoom)
    meadow(an, c, t, cam, 0.85)
    turn = lt > 2.6
    call = (1 - sstep(4.6, 5.6, lt))
    P = {"hand": (mix(30, 58, call), mix(-262, -474, call)), "hand_kind": "open" if call > 0.5 else "fist",
         "jaw": jaw(an, "ROSTAM", t, 10), "head": mix(10, -6, call) if lt < 4.6 else mix(-6, 12, sstep(4.6, 6.0, lt)),
         "stance": (50, 44)}

    def figs(cc):
        with Cam(cc, focus, zoom)(0.9):
            S.tree(cc, 250, 866, 1.05, t, "plane", 0.25, 2, INK)
        with Cam(cc, focus, zoom)(1.0):
            person(cc, 600, 872, 0.95, -1 if turn else 1, P, t, "rostam")
    an.figures(c, figs, (255, 190, 120), (0, 0, 1080, 1000))
    vig(an, c, 150)


# ===================================================== S14 the riders
def plain_sky(c, haze=0.0):
    S.lin(c, 0, 860, [(0, (70, 80, 120)), (0.45, (170, 150, 150)), (0.8, (238, 190, 130)), (1, (246, 214, 160))])


def plain(an, c, cam, key, warm=0.0):
    rg = get(an, key, lambda: (S.make_ridge(-600, 1700, 760, 60, 101, 8, 4, 0.4), S.make_ridge(-600, 1700, 820, 22, 102)))
    with cam(0.4):
        S.ridge(c, rg[0], mixc((140, 120, 140), (150, 80, 90), warm))
    with cam(0.55):
        S.ridge(c, rg[1], mixc((90, 70, 80), (90, 40, 50), warm))
    with cam(0.85):
        ground(c, 860, mixc((44, 32, 30), (50, 24, 24), warm))


def s14(an, c, t):
    lt, dur = loc(an, "S14", t)
    focus = (540, 620)
    zoom = 1 + 0.05 * ease(lt / dur)
    cam = Cam(c, focus, zoom)
    plain_sky(c)
    with cam(0.2):
        S.sun(c, 300, 700, 76, (255, 246, 214), (255, 206, 140), 460, 130)
    plain(an, c, cam, "rg14")
    stop = sstep(5.6, 6.6, lt)
    v = 70

    def figs(cc):
        with Cam(cc, focus, zoom)(1.0):
            for i in range(7):
                depth = (i % 3)
                s = 0.5 - depth * 0.06
                x = 980 + i * 120 - v * min(lt, 6.2) - v * 0.5 * max(0, lt - 6.2) * (i > 0) * (1 - stop * 0.8)
                if i == 0:
                    x = 980 - v * min(lt, 6.2)
                y = 872 - depth * 10
                moving = not (i == 0 and lt > 6.2)
                rp = {"hand": (100, -300), "jaw": jaw(an, "RIDER", t, 8) if i == 0 else 0.0, "head": 6 if i == 0 and stop > 0.5 else 0}
                if i == 0 and stop > 0:
                    rp.update({"hand": (mix(100, 150, stop), mix(-300, -210, stop)), "hand_kind": "open", "head": 14 * stop})
                horse(cc, x, y, s, -1, {"gait": "walk" if moving else "stand", "phase": t * 0.9 + i * 0.37, "saddle": True,
                                        "rider": "rider", "rider_pose": rp, "neck": 14 * stop if i == 0 else 0}, t)
    an.figures(c, figs, (255, 210, 150), (0, 200, 1080, 1000))
    vig(an, c, 130)


def s14b(an, c, t):
    lt, dur = loc(an, "S14b", t)
    focus = (720, 760)
    zoom = 1 + 0.12 * ease(lt / dur)
    cam = Cam(c, focus, zoom)
    plain_sky(c)
    with cam(0.3):
        S.sun(c, 860, 640, 70, (255, 246, 214), (255, 206, 140), 420, 120)
    rg = get(an, "rg14b", lambda: S.make_ridge(-600, 1700, 700, 40, 111))
    with cam(0.4):
        S.ridge(c, rg, (120, 110, 130))
    with cam(0.7):
        ground(c, 760, (70, 70, 54), (30, 26, 20))
        S.water(c, 846, 862, t, (240, 214, 160), (190, 170, 130))
        S.tree(c, 960, 800, 0.36, t, "plane", 0.1, 3, (40, 34, 30))
    lasso = sstep(11.6, 12.6, lt)

    def figs(cc):
        with Cam(cc, focus, zoom)(0.7):
            horse(cc, 700, 836, 0.34, 1, {"gait": "graze", "tail": 8 * math.sin(t * 1.3)}, t)
        with Cam(cc, focus, zoom)(1.0):
            cc.drawPath(spath([(-300, 2400, 0), (-300, 960), (200, 940), (520, 1010), (800, 1200), (900, 2400, 0)]),
                        anim.ink()) if Pen.mode != "anchor" else None
            for i, (x, role) in enumerate(((110, "RIDER2"), (330, "RIDER"))):
                rp = {"hand": (110, -310), "jaw": jaw(an, role, t, 8), "head": 10}
                if lasso > 0 and i == 1:
                    rp.update({"hand": (40, -540), "hand_kind": "lasso", "loop": 40})
                horse(cc, x, 1000 + i * 14, 1.0, 1, {"gait": "stand", "saddle": True, "rider": "rider", "rider_pose": rp,
                                                    "neck": 10 + 3 * math.sin(t * 0.7 + i), "head": 8}, t)
    an.figures(c, figs, (255, 210, 150), (0, 0, 1080, 1300))
    vig(an, c, 150)


# ======================================================= S15 the fight
def s15(an, c, t):
    lt, dur = loc(an, "S15", t)
    sh = (4 * math.sin(t * 37) * sstep(1.5, 2.5, lt)) * (1 - sstep(19, 21, lt))
    focus = (540, 620)
    zoom = 1.05
    c.save()
    c.translate(sh, sh * 0.6)
    cam = Cam(c, focus, zoom)
    S.lin(c, 0, 860, [(0, (60, 34, 40)), (0.45, (170, 96, 70)), (0.8, (232, 160, 100)), (1, (240, 190, 130))])
    plain(an, c, cam, "rg15", 0.5)
    rears = [(1.6, 3.8), (8.0, 10.4), (14.6, 17.0)]
    rr = 0.0
    for a, b in rears:
        if a <= lt <= b:
            rr = math.sin((lt - a) / (b - a) * math.pi) * 42
    rface = -1 if (lt // 6.5) % 2 == 0 else 1
    gk = {"gait": "rear", "rear": rr} if rr > 0.5 else {"gait": "gallop", "phase": t * 2.2}
    fall = clamp((lt - 13.8) / 1.2)
    riders = [(160 + 60 * math.sin(lt * 0.9), 1, 0.62), (930 + 50 * math.sin(lt * 1.1 + 1), -1, 0.6),
              (1010 + 40 * math.sin(lt * 0.7 + 2), -1, 0.5)]

    def figs(cc):
        with Cam(cc, focus, zoom)(1.0):
            for i, (x, f, s) in enumerate(riders):
                tag(f"r{i}:")
                withr = not (i == 1 and lt > 13.8)
                rp = {"hand": (60, -540) if lt < 4.5 else (120, -380), "hand_kind": "lasso" if lt < 4.5 else "fist",
                      "jaw": jaw(an, "RIDER2", t, 10) if i == 1 else 0.0, "lean": -6}
                horse(cc, x + (160 * fall if i == 1 else 0), 870 - i * 8, s, f,
                      {"gait": "gallop", "phase": t * 2.0 + i * 0.3, "saddle": True,
                       "rider": "rider" if withr else None, "rider_pose": rp}, t)
            if lt > 13.8 and fall < 1:
                cc.save()
                cc.translate(930 + 30 * fall, 640 + 230 * fall * fall)
                cc.rotate(-110 * fall)
                person(cc, 0, 0, 0.6, -1, {"hand": (90, -420), "hand_kind": "open", "rhand": (-80, -400),
                                          "rhand_kind": "open"}, t, "rider")
                cc.restore()
            elif fall >= 1:
                person(cc, 1000, 872, 0.6, -1, {"mode": "lie"}, t, "rider")
            tag("rk:")
            horse(cc, 560, 872, 0.78, rface, gk, t)
            tag("")
        if lt > 4.5:
            rope(cc, A("r0:hand"), A("rk:neck"), 30, 2.2)
            if lt < 13.8:
                rope(cc, A("r1:hand"), A("rk:neck"), 24, 2.2)
            if lt > 9:
                rope(cc, A("r2:hand"), A("rk:head"), 30, 2.2)
    an.figures(c, figs, (255, 200, 140), (0, 200, 1080, 1000), anchors=lt > 4.5)
    for k in range(6):
        S.dust(c, 300 + k * 110 + 40 * math.sin(t * 0.7 + k), 850 - (k % 2) * 30, 140, t, (200, 150, 110), 80, k)
    c.restore()
    vig(an, c, 150)


# ================================================== S16 led away
def s16(an, c, t):
    lt, dur = loc(an, "S16", t)
    focus = (540, 640)
    zoom = 1 + 0.04 * ease(lt / dur)
    cam = Cam(c, focus, zoom)
    S.lin(c, 0, 860, [(0, (40, 16, 40)), (0.4, (150, 50, 60)), (0.75, (240, 130, 70)), (1, (252, 190, 110))])
    with cam(0.2):
        S.sun(c, 260, 760, 120, (255, 226, 170), (255, 140, 80), 560, 160)
    img = get(an, "city16", lambda: S.city(900, 520, 500, 16, (40, 14, 26), False))
    with cam(0.35):
        c.save()
        c.translate(-60, 330)
        c.scale(0.5, 0.5)
        c.drawImage(img[0], 0, 0)
        c.restore()
        c.drawPath(spath([(-300, 900, 0), (-300, 590), (60, 584), (260, 600), (480, 640), (700, 700), (1400, 760),
                          (1400, 900, 0)]), paint(C(70, 24, 40)))
    with cam(0.85):
        ground(c, 860, (50, 20, 26))
    v = 36
    toss = 14 * math.sin(t * 2.3) + 10 * math.sin(t * 3.7)
    rrear = math.sin(clamp((lt - 5.0) / 1.4) * math.pi) * 26 + math.sin(clamp((lt - 11.0) / 1.4) * math.pi) * 22

    def figs(cc):
        with Cam(cc, focus, zoom)(1.0):
            tag("a:")
            horse(cc, 640 - v * lt, 868, 0.56, -1, {"gait": "walk", "phase": t * 0.8, "saddle": True, "rider": "rider",
                                                    "rider_pose": {"rhand": (-60, -330), "jaw": jaw(an, "RIDER", t, 8),
                                                                   "head": -8}}, t)
            tag("rk:")
            horse(cc, 930 - v * lt, 872, 0.66, -1, {"gait": "rear", "rear": rrear} if rrear > 1 else
                  {"gait": "walk", "phase": t * 0.8 + 0.4, "neck": toss, "head": toss * 0.5}, t)
            tag("b:")
            horse(cc, 1220 - v * lt, 862, 0.5, -1, {"gait": "walk", "phase": t * 0.8 + 0.2, "saddle": True,
                                                     "rider": "rider", "rider_pose": {"hand": (90, -340),
                                                                                     "jaw": jaw(an, "RIDER2", t, 8)}}, t)
            tag("")
        rope(cc, A("a:rhand"), A("rk:neck"), 22, 2.2)
        rope(cc, A("b:hand"), A("rk:neck"), 22, 2.2)
    an.figures(c, figs, (255, 180, 110), (0, 200, 1080, 1000), anchors=True)
    vig(an, c, 150)


# ===================================================== S18 hoofprints
def s18(an, c, t):
    lt, dur = loc(an, "S18", t)
    focus = (480, 680)
    zoom = 1 + 0.06 * ease(lt / dur)
    cam = Cam(c, focus, zoom)
    S.lin(c, 0, 840, [(0, (40, 24, 60)), (0.45, (140, 70, 90)), (0.8, (236, 140, 90)), (1, (250, 186, 120))])
    with cam(0.2):
        S.sun(c, 860, 760, 90, (255, 230, 180), (255, 150, 90), 500, 150)
    rg = get(an, "rg18", lambda: S.make_ridge(-600, 1700, 790, 30, 121))
    with cam(0.45):
        S.ridge(c, rg, (80, 40, 60))
    with cam(1.0):
        ground(c, 838, (50, 24, 26))
        S.lin(c, 846, 878, [(0, (190, 120, 90)), (1, (120, 66, 56))], (-300, 846, 1400, 878))
        pr = paint(C(28, 12, 14))
        for k in range(9):
            x = 300 + k * 92 + (k % 2) * 30
            y = 856 + (k % 3) * 6
            c.drawPath(spath([(x - 14, y), (x - 10, y - 6), (x + 10, y - 6), (x + 14, y), (x + 6, y + 4, 0), (x, y - 1),
                              (x - 6, y + 4, 0)]), pr)
        ground(c, 878, (24, 12, 14))
        S.reeds(c, get(an, "rd18", lambda: reed_list(18, 30, 820, 1300, 870, 120, 240)), t, INK, 0.3)
    point = sstep(3.4, 4.2, lt) * (1 - sstep(6.0, 6.4, lt))
    fist = sstep(6.2, 6.7, lt)
    if fist > 0:
        hand, kind = (mix(150, 60, fist), mix(-380, -580, fist)), "fist"
    elif point > 0:
        hand, kind = (mix(126, 180, point), mix(-130, -400, point)), "open"
    else:
        hand, kind = (126 + 6 * math.sin(t * 2), -130), "open"
    P = {"mode": "kneel", "hand": hand, "hand_kind": kind, "jaw": jaw(an, "ROSTAM", t, 9),
         "head": mix(14, -6, max(point, fist)), "lean": mix(10, -2, max(point, fist))}

    def figs(cc):
        with Cam(cc, focus, zoom)(1.0):
            person(cc, 330, 870, 1.15, 1, P, t, "rostam")
    an.figures(c, figs, (255, 180, 110), (0, 100, 1080, 1000))
    vig(an, c, 150)


# =================================================== S19 the long walk
def s19(an, c, t):
    lt, dur = loc(an, "S19", t)
    S.lin(c, 0, 860, [(0, (34, 14, 40)), (0.4, (130, 40, 60)), (0.75, (236, 110, 60)), (1, (252, 170, 90))])
    if lt < 18.0:
        speed = 120
        S.sun(c, 860, 700, 110, (255, 226, 170), (255, 130, 70), 560, 160)
        sc = get(an, "sc19", lambda: Scroller(131))
        sc.draw(c, lt, speed, [(130, 60, 90), (80, 30, 50), (46, 18, 24)])
        img = get(an, "city19", lambda: S.city(900, 520, 500, 19, (60, 22, 38), False))
        c.save()
        c.translate(820 - lt * 2, 690)
        c.scale(0.22, 0.22)
        c.drawImage(img[0], 0, 0)
        c.restore()
        P = {"mode": "walk", "phase": lt * 4.6, "carry": "saddle", "hand_kind": "mace", "hand": (98, -300),
             "jaw": jaw(an, "ROSTAM", t, 7), "head": mix(10, -6, sstep(10.8, 11.8, lt)), "stride": 19}

        def figs(cc):
            person(cc, 470, 874, 1.0, 1, P, t, "rostam")
        an.figures(c, figs, (255, 170, 100), (0, 100, 1080, 1000))
    else:
        lt2 = lt - 18.0
        S.sun(c, 640, 760, 230, (255, 200, 140), (240, 90, 50), 700, 180)
        img = get(an, "city19", lambda: S.city(900, 520, 500, 19, (60, 22, 38), False))
        c.save()
        c.translate(820, 712)
        c.scale(0.2, 0.2)
        c.drawImage(img[0], 0, 0)
        c.restore()
        ground(c, 812, (50, 18, 26))
        S.water(c, 830, 866, t, (250, 170, 100), (200, 90, 60), (255, 230, 170))
        ground(c, 866, (24, 10, 14))

        def figs(cc):
            person(cc, mix(240, 600, lt2 / 15.5), 828, 0.36, 1, {"mode": "walk", "phase": t * 4.6, "carry": "saddle",
                                                                 "hand_kind": "mace", "hand": (98, -300)}, t, "rostam")
        an.figures(c, figs, (255, 170, 100), (0, 500, 1080, 900))
        rd = get(an, "rd19", lambda: reed_list(19, 70, 0, 2400, 900, 220, 520))
        off = (lt2 * 26) % 2400
        S.reeds(c, [((x - off) % 2400 - 300, y, h, ph) for (x, y, h, ph) in rd], t, INK, 0.25)
    vig(an, c, 150)


# ================================================ S20 / S21 the city gate
def dusk_sky(c):
    S.lin(c, 0, 900, [(0, (20, 12, 40)), (0.4, (76, 34, 76)), (0.75, (190, 86, 80)), (1, (240, 150, 100))])


def torch(c, x, y, t, s=1.0, seed=0.0):
    S.glow(c, x, y - 20 * s, 230 * s, (255, 150, 70), 140 + 20 * math.sin(t * 8 + seed))
    c.drawRect(skia.Rect.MakeLTRB(x - 4 * s, y - 10 * s, x + 4 * s, y + 40 * s), paint(C(*INK)))
    S.flame(c, x, y - 6 * s, 0.4 * s, t, seed)


def s20(an, c, t):
    lt, dur = loc(an, "S20", t)
    focus = (540, 600)
    zoom = 1 + 0.06 * ease(lt / dur)
    cam = Cam(c, focus, zoom)
    dusk_sky(c)
    with cam(0.2):
        get(an, "st20", lambda: S.Stars(60, 400, 20)).draw(c, t, 0.5, 400)
    img, lights = get(an, "city20", lambda: S.city(1600, 900, 860, 20, INK, True, 800))
    with cam(1.0):
        S.glow(c, 540, 820, 240, (255, 170, 90), 150)
        c.drawImage(img, -260, 0)
        for (x, y) in lights[::2]:
            c.drawRect(skia.Rect.MakeXYWH(x - 260 - 4, y - 8, 8, 14), paint(C(255, 190, 110, 200)))
        ground(c, 860, (30, 14, 20))
        for k, x in enumerate((300, 780)):
            torch(c, x, 676, t, 1.0, k)
    point = sstep(0.3, 1.0, lt)
    run_x = mix(620, 1150, clamp((lt - 1.4) / 6))

    def figs(cc):
        with Cam(cc, focus, zoom)(1.0):
            person(cc, 230, 692, 0.5, 1, {"hand": (mix(40, 170, point), mix(-262, -420, point)), "hand_kind": "open",
                                         "rhand_kind": "spear", "rhand": (-10, -300), "jaw": jaw(an, "GUARD", t, 10),
                                         "head": -4}, t, "guard")
            if lt > 1.4:
                person(cc, run_x, 692, 0.5, 1, {"mode": "walk", "phase": lt * 8, "stride": 26, "lean": 10,
                                               "rhand_kind": "spear", "rhand": (-10, -300)}, t, "guard")
            for k in range(4):
                x = 440 + k * 60 + 30 * math.sin(lt * 0.6 + k)
                person(cc, x, 864, 0.32, 1 if k % 2 else -1, {"mode": "walk", "phase": t * 4 + k}, t,
                       "noble" if k % 2 else "maid")
    an.figures(c, figs, (255, 170, 100), (0, 400, 1080, 1000))
    vig(an, c, 150)


def s21(an, c, t):
    lt, dur = loc(an, "S21", t)
    focus = (540, 640)
    zoom = 1 + 0.05 * ease(lt / dur)
    cam = Cam(c, focus, zoom)
    dusk_sky(c)
    img, lights = get(an, "city21", lambda: S.city(1600, 900, 870, 21, INK, True, 520))
    with cam(1.0):
        S.glow(c, 260, 830, 240, (255, 170, 90), 150)
        c.drawImage(img, -260, 0)
        for (x, y) in lights[::2]:
            c.drawRect(skia.Rect.MakeXYWH(x - 260 - 4, y - 8, 8, 14), paint(C(255, 190, 110, 200)))
        ground(c, 866, (30, 14, 20))
        for k, x in enumerate((130, 420)):
            torch(c, x, 680, t, 0.9, k)
    crowd = sstep(8.0, 10.0, lt)
    walk = clamp(lt / 6.5)
    kx = mix(240, 560, ease(walk))
    sp = sstep(16.7, 17.2, lt)
    heart = sstep(23.4, 24.0, lt)
    PK = {"mode": "walk" if 0 < walk < 1 else "stand", "phase": lt * 4.4,
          "hand": (mix(40, 120, sp * (1 - heart)) - 20 * heart, mix(-262, -330, sp) - 50 * heart),
          "hand_kind": "open", "jaw": jaw(an, "KING_SAMANGAN", t, 7), "head": 2, "lean": 4 * sp, "stance": (44, 40)}

    def figs(cc):
        with Cam(cc, focus, zoom)(1.0):
            if crowd > 0:
                rnd = random.Random(3)
                for k in range(16):
                    x = rnd.uniform(500, 1060)
                    y = 712 - 40 * crowd + rnd.uniform(-4, 4)
                    cc.drawCircle(x, y, 9, anim.ink()) if Pen.mode != "anchor" else None
                    fillp(cc, ppath([(x - 12, y + 30), (x - 9, y + 6), (x + 9, y + 6), (x + 12, y + 30)]))
            for i in range(3):
                nx = kx - 160 - i * 130
                if nx > 120:
                    person(cc, nx, 870 - i * 4, 0.78, 1, {"mode": "walk" if 0 < walk < 1 else "stand", "phase": lt * 4.4 + i,
                                                          "seed": i}, t, "noble")
            person(cc, kx, 872, 0.86, 1, PK, t, "king")
            person(cc, 850, 872, 0.9, -1, {"hand_kind": "mace", "hand": (98, -300), "head": 3 * math.sin(t * 0.5)}, t, "rostam")
            cc.save()
            cc.translate(980, 872)
            cc.scale(-0.7, 0.7)
            fillp(cc, spath([(-92, 0, 0), (-80, -42), (-60, -50, 0), (-40, -32), (20, -32), (44, -50, 0), (60, -40),
                             (70, 0, 0)]))
            cc.restore()
    an.figures(c, figs, (255, 170, 100), (0, 300, 1080, 1000))
    vig(an, c, 150)


# ================================================ S22 / S22b two-shot
def night_wall(an, c, t, pan):
    S.lin(c, 0, 1100, [(0, (8, 10, 28)), (0.5, (24, 26, 60)), (1, (50, 40, 70))])
    get(an, "st22", lambda: S.Stars(140, 900, 22)).draw(c, t, 0.8, 900)
    img, lights = get(an, "city22", lambda: S.city(1800, 1000, 980, 22, (14, 8, 14), True, None))
    c.save()
    c.translate(-300 - pan * 0.4, 0)
    c.drawImage(img, 0, 0)
    for (x, y) in lights[::2]:
        c.drawRect(skia.Rect.MakeXYWH(x - 4, y - 8, 8, 14), paint(C(255, 190, 110, 170)))
    c.restore()
    for k, x in enumerate((170, 930)):
        torch(c, x - pan * 0.6, 760, t, 1.3, k)


def two_shot(an, c, t, lt, pan, PR, PK, sid):
    night_wall(an, c, t, pan)

    def figs(cc):
        cc.save()
        cc.translate(-pan, 0)
        person(cc, 290, 1360, 1.65, 1, PR, t, "rostam")
        person(cc, 860, 1360, 1.55, -1, PK, t, "king")
        cc.restore()
    an.figures(c, figs, (255, 170, 100), (0, 0, 1080, 1400))
    vig(an, c, 160)


def s22(an, c, t):
    lt, dur = loc(an, "S22", t)
    open_h = sstep(11.6, 12.4, lt) * (1 - sstep(17.4, 17.9, lt))
    threat = sstep(17.8, 18.6, lt)
    PR = {"hand_kind": "mace", "hand": (mix(98, 120, threat), mix(-300, -390, threat)), "mace": mix(0, 28, threat),
          "jaw": jaw(an, "ROSTAM", t, 6), "head": 2 * math.sin(t * 0.7) - 3 * threat,
          "rhand": (mix(-30, 60, open_h), mix(-262, -330, open_h)), "rhand_kind": "open" if open_h > 0.3 else "fist"}
    PK = {"hand": (40, -262), "head": 3 + 6 * threat, "lean": -5 * threat, "jaw": 0.0}
    two_shot(an, c, t, lt, 0, PR, PK, "S22")


def s22b(an, c, t):
    lt, dur = loc(an, "S22b", t)
    pan = 80 * ease(lt / 3.0)
    calm = sstep(2.0, 2.8, lt) * (1 - sstep(10.6, 11.4, lt))
    order = sstep(12.4, 13.0, lt) * (1 - sstep(17.2, 17.8, lt))
    invite = sstep(17.8, 18.4, lt)
    nod = sstep(22.6, 23.6, lt)
    if order > 0:
        hand = (mix(40, -150, order), mix(-262, -430, order))
    elif invite > 0:
        hand = (mix(40, 120, invite), mix(-262, -320, invite))
    else:
        hand = (mix(40, 92, calm), mix(-262, -420, calm))
    PK = {"hand": hand, "hand_kind": "open", "rhand": (mix(-30, 60, calm), mix(-262, -428, calm)),
          "rhand_kind": "open" if calm > 0.3 else "fist", "jaw": jaw(an, "KING_SAMANGAN", t, 7),
          "head": -16 * order + 2 * math.sin(t * 0.8), "lean": 3 * calm}
    PR = {"hand_kind": "mace", "hand": (98, -300), "head": mix(-2, 9, nod) + 1.5 * math.sin(t * 0.6), "jaw": 0.0}
    two_shot(an, c, t, lt, pan, PR, PK, "S22b")


# ===================================================== S23 the feast
def hall(an, c, t, warm=1.0):
    S.lin(c, 0, H, [(0, (40, 18, 14)), (0.3, (150, 76, 34)), (0.5, (196, 110, 50)), (0.7, (90, 40, 22)), (1, (10, 5, 6))])
    pt = paint(C(*INK))
    arch = S.arch_path(540, 860, 620, 640)
    p = skia.Paint(AntiAlias=True)
    p.setShader(skia.GradientShader.MakeRadial(skia.Point(540, 560), 420, [C(255, 200, 120, 90), C(255, 200, 120, 0)]))
    c.drawPath(arch, p)
    edge = skia.Paint(AntiAlias=True, Color=C(*INK))
    edge.setStyle(skia.Paint.kStroke_Style)
    edge.setStrokeWidth(16)
    c.drawPath(arch, edge)
    for x in (40, 1040):
        c.drawRect(skia.Rect.MakeLTRB(x - 36, 150, x + 36, 900), pt)
        c.drawRect(skia.Rect.MakeLTRB(x - 50, 130, x + 50, 160), pt)
    c.drawRect(skia.Rect.MakeLTRB(-10, 0, 1090, 130), pt)
    for i in range(14):
        c.drawPath(spath([(i * 80, 130, 0), (i * 80 + 40, 176), (i * 80 + 80, 130, 0)]), pt)


def s23(an, c, t):
    lt, dur = loc(an, "S23", t)
    focus = (540, 620)
    zoom = 1 + 0.06 * ease(lt / dur)
    cam = Cam(c, focus, zoom)
    with cam(0.6):
        hall(an, c, t)
        for k, x in enumerate((260, 540, 820)):
            S.hanging_lamp(c, x, 300, 1.0, t, 160, k)
    with cam(0.9):
        ground(c, 860, (40, 18, 12))
        S.glow(c, 540, 870, 500, (255, 160, 80), 60)
    toast_k = sstep(4.2, 4.8, lt) * (1 - sstep(8.0, 8.8, lt))
    toast_r = sstep(8.6, 9.2, lt) * (1 - sstep(11.0, 11.8, lt))
    shake = sstep(16.4, 16.8, lt) * (1 - sstep(19.4, 20, lt))

    def figs(cc):
        with Cam(cc, focus, zoom)(0.75):
            for k in range(7):
                x = 160 + k * 125
                person(cc, x, 760, 0.42, 1 if k < 3 else -1, {"mode": "sit", "hand": (80, -300 - 30 * math.sin(t + k)),
                                                             "hand_kind": "cup", "seed": k}, t, "noble")
        with Cam(cc, focus, zoom)(1.0):
            fillp(cc, ppath([(240, 860), (840, 860), (850, 820), (230, 820)]))
            person(cc, 420, 822, 0.95, 1, {"mode": "sit", "hand": (mix(150, 120, toast_r), mix(-300, -480, toast_r)),
                                          "hand_kind": "cup", "jaw": jaw(an, "ROSTAM", t, 6),
                                          "head": 8 * math.sin(t * 7) * shake + 3}, t, "rostam_robe")
            person(cc, 680, 822, 0.9, -1, {"mode": "sit", "hand": (mix(150, 120, toast_k), mix(-300, -500, toast_k)),
                                          "hand_kind": "cup", "jaw": jaw(an, "KING_SAMANGAN", t, 7), "head": 2}, t, "king")
            # musicians: harp and lute
            person(cc, 120, 860, 0.72, 1, {"mode": "sit", "hand": (120 + 8 * math.sin(t * 6), -330 + 20 * math.sin(t * 3)),
                                          "hand_kind": "open", "rhand": (90, -250 + 10 * math.sin(t * 5))}, t, "musician")
            cc.save()
            cc.translate(120 + 0.72 * 150, 860 - 0.72 * 60)
            cc.scale(0.72, 0.72)
            fillp(cc, spath([(0, 0, 0), (-10, -220), (10, -300, 0), (90, -280), (110, -250, 0), (20, -40), (12, 0, 0)]))
            anim.hole(cc, spath([(18, -60, 0), (8, -230, 0), (80, -250, 0)]))
            for k in range(6):
                fillp(cc, ppath([(14 + k * 4, -70 - k * 8), (16 + k * 4, -70 - k * 8), (20 + k * 12, -240 - k * 2),
                                 (18 + k * 12, -240 - k * 2)]))
            cc.restore()
            person(cc, 960, 860, 0.72, -1, {"mode": "sit", "hand": (110, -300 + 14 * math.sin(t * 9)), "hand_kind": "open",
                                           "rhand": (60, -330)}, t, "musician")
            cc.save()
            cc.translate(960 - 0.72 * 90, 860 - 0.72 * 300)
            cc.scale(-0.72, 0.72)
            cc.rotate(-30)
            fillp(cc, spath([(-40, 0), (-20, -40), (20, -44), (44, -10), (30, 30), (-20, 36)]))
            fillp(cc, ppath([(30, -30), (150, -100), (156, -90), (36, -20)]))
            fillp(cc, ppath([(146, -104), (172, -122), (176, -110), (154, -96)]))
            cc.restore()
    an.figures(c, figs, (255, 196, 120), (0, 300, 1080, 1000))
    vig(an, c, 150)


# ================================================== S23b the lattice
def s23b(an, c, t):
    lt, dur = loc(an, "S23b", t)
    lean = ease(lt / dur)
    S.lin(c, 0, H, [(0, (10, 5, 8)), (1, (6, 3, 5))])
    S.lin(c, 150, 1300, [(0, (120, 50, 20)), (0.4, (250, 160, 70)), (0.7, (230, 120, 50)), (1, (60, 20, 10))],
          (330, 150, 1080, 1300))
    for k in range(2):
        x = (lt * (60 + k * 30) + k * 400) % 1100 - 100 + 330
        S.radial(c, x, 700 + k * 80, 160, [(0.0, (60, 20, 10, 150)), (1.0, (60, 20, 10, 0))])
    img = get(an, "lat23b", lambda: S.lattice(760, 1160, 92, 9))
    c.drawImage(img, 330, 150)
    S.glow(c, 640, 640, 600, (255, 170, 80), 60)
    P = {"hand": (mix(80, 104, lean), mix(-420, -440, lean)), "hand_kind": "open", "lean": 6 * lean,
         "head": 4 + 3 * lean, "wind": 0.15, "rhand": (-30, -262)}

    def figs(cc):
        person(cc, 400, 1460, 1.8, 1, P, t, "tahmineh")
    an.figures(c, figs, (255, 180, 100), (0, 0, 1080, 1500))
    vig(an, c, 170)


# ================================================== S24 the bedchamber
def chamber(an, c, t):
    S.lin(c, 0, H, [(0, (14, 10, 22)), (0.45, (34, 22, 34)), (0.6, (26, 16, 24)), (1, (6, 3, 5))])
    pt = paint(C(*INK))
    door = S.arch_path(170, 860, 220, 470)
    c.drawPath(door, paint(C(60, 40, 50)))
    edge = skia.Paint(AntiAlias=True, Color=C(*INK))
    edge.setStyle(skia.Paint.kStroke_Style)
    edge.setStrokeWidth(14)
    c.drawPath(door, edge)
    c.drawPath(spath([(420, 130, 0), (470, 300), (450, 520), (500, 760), (480, 862, 0), (430, 862, 0), (420, 600),
                      (400, 300)]), pt)
    c.drawRect(skia.Rect.MakeLTRB(380, 120, 1100, 140), pt)
    S.lin(c, 560, 800, [(0, (90, 50, 50)), (1, (150, 90, 70))], (560, 560, 1090, 800))
    for k in range(7):
        x = 590 + k * 74
        c.drawPath(spath([(x, 560, 0), (x + 30, 680), (x + 20, 800, 0), (x + 40, 800, 0), (x + 54, 680), (x + 74, 560, 0)]),
                   paint(C(60, 30, 34, 120)))


def s24(an, c, t):
    lt, dur = loc(an, "S24", t)
    focus = (560, 640)
    zoom = 1 + 0.05 * ease(lt / dur)
    cam = Cam(c, focus, zoom)
    with cam(0.7):
        chamber(an, c, t)
    with cam(1.0):
        ground(c, 862, (30, 18, 22))
    lying = lt > 8.4
    walk_in = clamp(lt / 4.2)
    kx = mix(120, 470, ease(walk_in))
    leave = clamp((lt - 7.6) / 3.0)
    if leave > 0:
        kx = mix(470, -200, leave)
    rx = mix(-120, 300, ease(clamp((lt - 0.6) / 4.4)))
    fl = 0.9 + 0.1 * math.sin(t * 7)

    def figs(cc):
        with Cam(cc, focus, zoom)(1.0):
            fillp(cc, spath([(620, 862, 0), (620, 790), (640, 776), (1060, 776), (1080, 790), (1080, 862, 0)]))
            fillp(cc, spath([(640, 776), (660, 744), (720, 738), (760, 760)]))
            fillp(cc, spath([(560, 862, 0), (564, 760, 0), (588, 760, 0), (592, 862, 0)]))
            fillp(cc, spath([(556, 760), (596, 760), (600, 746), (552, 746)]))
            if not lying:
                tag("k:")
                person(cc, kx, 868, 0.86, -1 if leave > 0 else 1,
                       {"mode": "walk" if (0 < walk_in < 1 or 0 < leave < 1) else "stand", "phase": t * 4.4,
                        "hand_kind": "lamp", "hand": (110, -360), "jaw": jaw(an, "KING_SAMANGAN", t, 7)}, t, "king")
                tag("")
                person(cc, rx, 868, 0.9, 1, {"mode": "walk" if lt < 5 else "stand", "phase": t * 4.2,
                                            "jaw": jaw(an, "ROSTAM", t, 6), "head": 3}, t, "rostam_robe")
            else:
                person(cc, 1000, 790, 0.78, 1, {"mode": "lie", "head": 6}, t, "rostam_robe")
                if leave < 1:
                    person(cc, kx, 868, 0.86, -1, {"mode": "walk", "phase": t * 4.4}, t, "king")
    an.figures(c, figs, (255, 180, 100), (0, 200, 1080, 1000), anchors=not lying)
    if not lying and A("k:flame"):
        fx, fy = A("k:flame")
        S.glow(c, fx, fy, 560, (255, 170, 80), 120 * fl)
        S.flame(c, fx, fy + 8, 0.3, t, 2)
    with cam(1.0):
        S.glow(c, 576, 736, 300, (255, 170, 80), (70 if lying else 30) * fl)
        S.flame(c, 576, 746, 0.26, t, 4)
    vig(an, c, 170)


# ============================================== S24b the city at night
def s24b(an, c, t):
    lt, dur = loc(an, "S24b", t)
    focus = (620, 600)
    zoom = 1 + 0.1 * ease(lt / dur)
    cam = Cam(c, focus, zoom)
    S.lin(c, 0, 900, [(0, (6, 8, 24)), (0.5, (20, 26, 62)), (1, (46, 50, 90))])
    with cam(0.2):
        get(an, "st24b", lambda: S.Stars(200, 800, 24)).draw(c, t, 1.0, 800)
        S.moon(c, 700, 470 - 40 * ease(lt / dur), 84)
        get(an, "cl24b", lambda: S.Clouds([(420, 14), (500, 10), (560, 16)], 25, 300, 600)).draw(c, t * 2.4, (30, 34, 60), 200)
    img, lights = get(an, "city24b", lambda: S.city(1500, 900, 880, 24, INK, True, None))
    with cam(1.0):
        c.drawImage(img, -200, 0)
        for k, (x, y) in enumerate(lights):
            if k % 3 == 0:
                a = 160 + 60 * math.sin(t * 2 + k)
                c.drawRect(skia.Rect.MakeXYWH(x - 200 - 4, y - 8, 8, 14), paint(C(255, 190, 110, a)))
        ground(c, 880, (10, 8, 14))
    vig(an, c, 160)


# ================================================ S25 + END the corridor
def s25(an, c, t):
    lt = t - an.start["S25"]
    focus = (540, 640)
    zoom = 1 + 0.08 * ease(lt / 27.0)
    cam = Cam(c, focus, zoom)
    S.lin(c, 0, H, [(0, (8, 8, 18)), (0.5, (16, 16, 32)), (1, (4, 3, 6))])
    pt = paint(C(*INK))
    with cam(0.8):
        for k, x in enumerate((170, 540, 910)):
            win = S.arch_path(x, 620, 170, 380)
            c.drawPath(win, paint(C(70, 90, 140)))
            p = skia.Paint(AntiAlias=True)
            p.setShader(skia.GradientShader.MakeLinear([skia.Point(0, 620), skia.Point(0, 870)],
                                                       [C(120, 140, 200, 70), C(120, 140, 200, 0)]))
            c.drawPath(ppath([(x - 85, 620), (x + 85, 620), (x + 190, 870), (x + 20, 870)]), p)
        for x in (0, 355, 725, 1090):
            c.drawRect(skia.Rect.MakeLTRB(x - 40, 150, x + 40, 900), pt)
        c.drawRect(skia.Rect.MakeLTRB(-100, 100, 1200, 200), pt)
    with cam(1.0):
        ground(c, 866, (20, 18, 30))
        c.drawPath(S.arch_path(80, 866, 150, 330), paint(C(30, 18, 20)))
        c.drawRect(skia.Rect.MakeLTRB(138, 600, 142, 866), paint(C(255, 190, 110, 120)))
    stop = 15.2
    u = clamp(lt / stop)
    mx = mix(1180, 330, ease(u) * 0.3 + u * 0.7)
    tx = mx + 300
    walking = lt < stop
    fl = 0.85 + 0.15 * math.sin(t * 8) + 0.05 * math.sin(t * 17)

    def figs(cc):
        with Cam(cc, focus, zoom)(1.0):
            tag("m:")
            person(cc, mx, 872, 0.82, -1, {"mode": "walk" if walking else "stand", "phase": lt * 3.6, "stride": 15,
                                          "hand_kind": "candle", "hand": (96, -360), "jaw": jaw(an, "MAID", t, 7),
                                          "head": -6 if 8 < lt < 11 else 0, "wind": 0.3}, t, "maid")
            tag("")
            person(cc, tx, 872, 0.86, -1, {"mode": "walk" if walking else "stand", "phase": lt * 3.6 + 1.2, "stride": 15,
                                          "hand": (60, -330), "hand_kind": "open", "jaw": jaw(an, "TAHMINEH", t, 6),
                                          "wind": 0.3, "head": 2}, t, "tahmineh")
    an.figures(c, figs, (255, 180, 100), (0, 200, 1080, 1000), anchors=True)
    if A("m:flame"):
        fx, fy = A("m:flame")
        S.glow(c, fx, fy, 520, (255, 170, 80), 120 * fl)
        S.flame(c, fx, fy + 10, 0.26, t, 3)
    vig(an, c, 170)


anim.SCENES.update({
    "S01": anim.cold_open, "TITLE": anim.cold_open,
    "S02": s02, "S03": s03, "S04": s04, "S05": s05, "S06": s06, "S06b": s06b, "S06c": s06c, "S07": s07,
    "S08": s08, "S09": s09, "S10": s10, "S11": s11, "S12": s12, "S13": s13, "S14": s14, "S14b": s14b,
    "S15": s15, "S16": s16, "S17": s17, "S18": s18, "S19": s19, "S20": s20, "S21": s21, "S22": s22,
    "S22b": s22b, "S23": s23, "S23b": s23b, "S24": s24, "S24b": s24b, "S25": s25, "END": s25,
})

anim.SHIFTS.update({"S02": -110, "S06": -60, "S06c": -70, "S08": -100, "S09": 150, "S10": 270, "S11": -90,
                    "S15": 170, "S18": -90})
