"""Parts 9-10 (row 5 of OUTLINE.md, "Whose Son Am I?"): every shot as a shadow-play scene.

Importing this module registers part 9's shots; p10_scenes.py imports it and registers part 10's.
New here, to reuse: Sohrab as a boy (LOOKS "young_sohrab"; also "boy" and "wrestler"), the "bow" prop with
bow_string() and Arrow (an arrow in flight), target(), a rocking cradle(), a small chest() whose lid opens on a
red glow, ruby(), scroll() (a letter), meydan() (the training field of Samangan, morning to sunset),
night_two() (two people standing at the moon window), seated_two() (mother and son sitting by the candle,
stories on the curtain behind them) and west_window() (mountains under the moon, with a vision in the sky).
Line timings come from pNN/audio/timeline.json (LN), so the action follows the voices.
"""
import math, random
import skia
import anim
from anim import C, mix, mixc, clamp, ease, sstep, Cam, Pen, rope, spath, ppath, paint, fillp, W, H
from puppets import person, horse, LOOKS
import sets as S
from ep01_scenes import loc, jaw, get, vig, tag, A, ground, INK
from p05_scenes import (TAHM, WARM, MOON, standing_candle, wall_panel, shadow_layer, ghost_layer, moon_window,
                        city_night, register)
from p07_scenes import LN, dissolve, gem, gem_at, seated, baby

YS = "young_sohrab"
DAY = (255, 214, 160)                               # morning sun
NOON = (255, 196, 130)                              # late afternoon
SUNSET = (255, 150, 100)
NIGHT = mixc(MOON, WARM, 0.5)                       # moonlight + lamp
SH_B = (0, 260, W, 1000)                            # where shadows land on the curtain


def flick(t, seed=0.0):
    return 0.9 + 0.07 * math.sin(t * 8 + seed) + 0.04 * math.sin(t * 17 + seed)


# ------------------------------------------------------------------ props
def ruby(c, x, y, r, t, a=1.0, seed=0.0, glow=1.0):
    """A shining ruby set in gold (drawn in colour over the silhouettes)."""
    if a <= 0.01:
        return
    pulse = 0.8 + 0.2 * math.sin(t * 2.3 + seed)
    S.glow(c, x, y, r * 8, (255, 60, 60), 110 * a * pulse * glow)
    S.glow(c, x, y, r * 2.6, (255, 160, 150), 120 * a * pulse * glow)
    gp = skia.Paint(AntiAlias=True, Color=C(240, 196, 90, 235 * a))
    gp.setStyle(skia.Paint.kStroke_Style)
    gp.setStrokeWidth(max(1.5, r * 0.26))
    c.drawOval(skia.Rect.MakeXYWH(x - r * 1.18, y - r * 0.98, 2.36 * r, 1.96 * r), gp)
    p = skia.Paint(AntiAlias=True)
    p.setShader(skia.GradientShader.MakeRadial(skia.Point(x - r * 0.3, y - r * 0.35), r * 1.5,
                                               [C(255, 214, 214, 255 * a), C(214, 26, 48, 255 * a),
                                                C(84, 0, 16, 255 * a)], [0.0, 0.5, 1.0]))
    c.drawOval(skia.Rect.MakeXYWH(x - r, y - r * 0.8, 2 * r, 1.6 * r), p)
    tw = max(0.0, math.sin(t * 1.7 + seed * 2.1)) ** 10
    if tw > 0.04:
        sp = paint(C(255, 246, 236, 230 * a * tw))
        L = r * 2.6 * tw + r * 0.6
        cx, cy = x - r * 0.35, y - r * 0.4
        c.drawPath(ppath([(cx - L, cy), (cx, cy - r * 0.16), (cx + L, cy), (cx, cy + r * 0.16)]), sp)
        c.drawPath(ppath([(cx, cy - L), (cx + r * 0.16, cy), (cx, cy + L), (cx - r * 0.16, cy)]), sp)


def scroll(c, x, y, w, h, ang, a=1.0, warm=0.0):
    """Rostam's letter: a lit parchment with rolled ends and lines of writing."""
    if a <= 0.01:
        return
    c.save()
    c.translate(x, y)
    c.rotate(ang)
    c.drawRect(skia.Rect.MakeLTRB(-w / 2, -h / 2, w / 2, h / 2), paint(C(*mixc((250, 232, 190), (255, 200, 170), warm), 255 * a)))
    for sy in (-1, 1):
        c.drawRoundRect(skia.Rect.MakeLTRB(-w / 2 - 6, sy * h / 2 - 7, w / 2 + 6, sy * h / 2 + 7), 7, 7,
                        paint(C(150, 100, 60, 255 * a)))
    for k in range(5):
        yy = -h / 2 + h * (k + 1) / 6.5
        c.drawRect(skia.Rect.MakeLTRB(-w * 0.36, yy, w * 0.36 - (k % 2) * w * 0.12, yy + 2.2), paint(C(90, 50, 30, 150 * a)))
    c.restore()


def bow_string(cc, who, drawn, nock=False):
    """The bow's string (and a nocked arrow) between the anchors of the 'bow' prop and the draw hand."""
    top, bot, rh, hd = A(who + "bowtop"), A(who + "bowbot"), A(who + "rhand"), A(who + "hand")
    if not (top and bot):
        return
    mid = ((top[0] + bot[0]) / 2, (top[1] + bot[1]) / 2)
    if drawn > 0.01 and rh:
        mid = (mix(mid[0], rh[0], drawn), mix(mid[1], rh[1], drawn))
    rope(cc, top, mid, 0, 1.6)
    rope(cc, mid, bot, 0, 1.6)
    if nock and hd:
        tip = (hd[0] + (hd[0] - mid[0]) * 0.25, hd[1] + (hd[1] - mid[1]) * 0.25)
        rope(cc, mid, tip, 0, 2.0)
        dx, dy = tip[0] - mid[0], tip[1] - mid[1]
        d = math.hypot(dx, dy) or 1.0
        ux, uy = dx / d, dy / d
        fillp(cc, ppath([(tip[0] + ux * 12, tip[1] + uy * 12), (tip[0] - uy * 5, tip[1] + ux * 5),
                         (tip[0] + uy * 5, tip[1] - ux * 5)]))


def arrow(c, x0, y0, x1, y1, u, s=1.0):
    """An arrow flying from (x0, y0) to (x1, y1); u = 0..1 of the flight (it stays stuck at u >= 1)."""
    u = clamp(u)
    x = mix(x0, x1, u)
    y = mix(y0, y1, u) - 30 * s * math.sin(u * math.pi)
    ang = math.atan2((y1 - y0) - 30 * s * math.pi * math.cos(u * math.pi), x1 - x0)
    c.save()
    c.translate(x, y)
    c.rotate(math.degrees(ang))
    pt = paint(C(*INK))
    c.drawRect(skia.Rect.MakeLTRB(-70 * s, -1.6 * s, 0, 1.6 * s), pt)
    c.drawPath(ppath([(10 * s, 0), (-4 * s, -5 * s), (-4 * s, 5 * s)]), pt)
    for sy in (-1, 1):
        c.drawPath(ppath([(-70 * s, 0), (-56 * s, 0), (-62 * s, 8 * s * sy), (-76 * s, 8 * s * sy)]), pt)
    c.restore()


def target(c, x, y, r, t, hit=0.0):
    """An archery target of straw on a stand; hit (0..1) makes it shake."""
    sh = 3 * math.sin(t * 40) * hit
    pt = paint(C(*INK))
    for dx in (-0.8, 0.8):
        c.drawPath(ppath([(x + dx * r * 0.4 - 5, y), (x + dx * r * 0.4 + 5, y), (x + dx * r * 1.1 + 6, y + r * 3.2),
                          (x + dx * r * 1.1 - 6, y + r * 3.2)]), pt)
    c.save()
    c.translate(x + sh, y)
    for k, (rr, col) in enumerate(((1.0, (226, 196, 140)), (0.72, (160, 52, 40)), (0.5, (226, 196, 140)),
                                   (0.26, (160, 52, 40)))):
        c.drawCircle(0, 0, r * rr, paint(C(*col)))
    e = skia.Paint(AntiAlias=True, Color=C(*INK))
    e.setStyle(skia.Paint.kStroke_Style)
    e.setStrokeWidth(5)
    c.drawCircle(0, 0, r, e)
    c.restore()


def stuck(c, x, y, s, ang=180.0):
    """An arrow stuck in the target, its shaft pointing back at the archer."""
    c.save()
    c.translate(x, y)
    c.rotate(ang)
    pt = paint(C(*INK))
    c.drawRect(skia.Rect.MakeLTRB(0, -1.6 * s, 50 * s, 1.6 * s), pt)
    for sy in (-1, 1):
        c.drawPath(ppath([(50 * s, 0), (38 * s, 0), (44 * s, 7 * s * sy), (56 * s, 7 * s * sy)]), pt)
    c.restore()


def cradle(cc, x, y, s, t, rock=1.0, with_baby=True, arm=0.0):
    """A wooden cradle hanging from a frame (puppet pen); the basket swings, the baby's head shows."""
    for sx in (-1, 1):
        px = x + sx * 140 * s
        fillp(cc, ppath([(px - 40 * s, y), (px - 28 * s, y), (px + 3 * s, y - 250 * s), (px - 5 * s, y - 250 * s)]))
        fillp(cc, ppath([(px + 40 * s, y), (px + 28 * s, y), (px - 3 * s, y - 250 * s), (px + 5 * s, y - 250 * s)]))
    fillp(cc, ppath([(x - 156 * s, y - 256 * s), (x + 156 * s, y - 256 * s), (x + 156 * s, y - 244 * s),
                     (x - 156 * s, y - 244 * s)]))
    ang = 7 * math.sin(t * 1.7) * rock
    cc.save()
    cc.translate(x, y - 250 * s)
    cc.rotate(ang)
    cc.translate(-x, -(y - 250 * s))
    for sx in (-1, 1):
        rope(cc, (x, y - 250 * s), (x + sx * 104 * s, y - 120 * s), 0, 2.2 * s)
    if with_baby:
        baby(cc, x + 8 * s, y - 128 * s, 0.95 * s, t, 0, arm, 1, 0.5)
    fillp(cc, spath([(x - 118 * s, y - 122 * s, 0), (x - 104 * s, y - 70 * s), (x - 60 * s, y - 48 * s), (x + 60 * s, y - 48 * s),
                     (x + 104 * s, y - 70 * s), (x + 118 * s, y - 122 * s, 0), (x + 96 * s, y - 112 * s, 0),
                     (x - 96 * s, y - 112 * s, 0)]))
    cc.restore()


def chest(cc, x, y, s, lid):
    """A small chest on the floor (puppet pen); lid (0..1) swings open about its left hinge."""
    fillp(cc, spath([(x - 70 * s, y, 0), (x - 70 * s, y - 64 * s, 0), (x + 70 * s, y - 64 * s, 0), (x + 70 * s, y, 0)]))
    fillp(cc, ppath([(x - 78 * s, y - 2 * s), (x + 78 * s, y - 2 * s), (x + 78 * s, y + 6 * s), (x - 78 * s, y + 6 * s)]))
    cc.save()
    cc.translate(x - 72 * s, y - 64 * s)
    cc.rotate(-105 * ease(clamp(lid)))
    fillp(cc, spath([(0, 0, 0), (2 * s, -18 * s), (40 * s, -32 * s), (104 * s, -32 * s), (142 * s, -18 * s), (144 * s, 0, 0)]))
    cc.restore()


def chest_glow(c, x, y, s, lid, t):
    """Red light rising from the open chest."""
    if lid <= 0.02:
        return
    S.glow(c, x, y - 70 * s, 260 * s, (255, 70, 60), 120 * lid * flick(t, 2.0))
    S.glow(c, x, y - 64 * s, 90 * s, (255, 170, 140), 110 * lid)


# ------------------------------------------------------------------ sets
def meydan(an, c, t, cam, mood=0.0, key="md"):
    """The training field outside the palace of Samangan: far city and dome, a low wall, bright sand.
    mood 0 = morning, 1 = late afternoon, 2 = sunset."""
    m1, m2 = clamp(mood), clamp(mood - 1)
    top = mixc(mixc((96, 130, 180), (100, 100, 156), m1), (60, 26, 64), m2)
    mid = mixc(mixc((200, 190, 180), (226, 166, 130), m1), (214, 84, 70), m2)
    low = mixc(mixc((250, 216, 164), (255, 196, 128), m1), (255, 168, 96), m2)
    S.lin(c, 0, 900, [(0, top), (0.5, mid), (0.82, low), (1, low)])
    with cam(0.2):
        sx, sy = mix(mix(880, 790, m1), 640, m2), mix(mix(430, 590, m1), 760, m2)
        S.sun(c, sx, sy, mix(60, 120, m2), (255, 246, 214), mixc((255, 214, 150), (255, 120, 70), m2), 560, 150 + 30 * m2)
        get(an, key + "cl", lambda: S.Clouds([(260, 14), (340, 10), (430, 16)], 91, 300, 600)).draw(
            c, t, mixc((150, 120, 140), (110, 30, 50), m2), 150)
    haze = mixc(mixc((150, 132, 140), (170, 120, 110), m1), (130, 50, 60), m2)
    img, _ = get(an, key + "city" + str(int(mood * 10)), lambda: S.city(1500, 900, 880, 93, haze, False, None))
    with cam(0.4):
        c.save()
        c.translate(-60, 382)
        c.scale(0.5, 0.5)
        c.drawImage(img, 0, 0)
        c.restore()
        S.lin(c, 760, 830, [(0, (*low, 0)), (1, (*low, 120))], (-300, 760, 1400, 830))
    with cam(0.65):
        wall = mixc(haze, (40, 26, 30), 0.55)
        pt = paint(C(*wall))
        c.drawRect(skia.Rect.MakeLTRB(-300, 806, 1400, 830), pt)
        for k in range(40):
            c.drawRect(skia.Rect.MakeLTRB(-300 + k * 46, 796, -300 + k * 46 + 26, 806), pt)
    with cam(1.0):
        ground(c, 828, mixc(mixc((214, 180, 130), (214, 160, 108), m1), (176, 96, 64), m2), (40, 24, 18))


def candle_room(an, c, t, cam, floor=1000, panel=(120, 960, 300, 900), lamp=None):
    """Tahmineh's room at night: dark walls, a warm curtain lit by a candle (stories fall on it as shadows)."""
    fl = flick(t)
    with cam(0.7):
        S.lin(c, 0, H, [(0, (16, 10, 22)), (0.45, (40, 24, 34)), (1, (6, 3, 5))])
        wall_panel(c, *panel, (110, 60, 46), (180, 112, 76), 90)
        if lamp:
            S.hanging_lamp(c, lamp[0], lamp[1], 1.1, t, 100, 2.0)
            S.glow(c, lamp[0], lamp[1] + 300, 560, (255, 170, 90), 70 * fl)
        S.glow(c, 540, 760, 620, (255, 180, 100), 100 * fl)
    with cam(1.0):
        ground(c, floor, (36, 20, 22))


def night_two(an, c, t, lt, dur, PS, sx, PT, tx, key, zk=0.06, cover=0.0, gem_a=0.6, face_t=-1, behind=None):
    """Two people standing at the moon window: Sohrab (left) and Tahmineh (right); a lamp at the right."""
    focus = (540, 700)
    zoom = 1.0 + zk * ease(lt / max(dur, 0.1))
    cam = Cam(c, focus, zoom)
    moon_window(an, c, t, cam, 540, 1010, 400, 720, cover, key)
    with cam(0.6):
        S.hanging_lamp(c, 980, 250, 1.1, t, 110, 3.0)
        S.glow(c, 980, 560, 520, (255, 170, 90), 80 * flick(t))
    if behind:
        behind(cam)

    def figs(cc):
        with Cam(cc, focus, zoom)(1.0):
            tag("s:")
            person(cc, sx, 1330, 1.42, 1, PS, t, YS)
            tag("t:")
            person(cc, tx, 1330, 1.5, face_t, PT, t, TAHM)
            tag("")
    an.figures(c, figs, NIGHT, (0, 150, 1080, 1500), anchors=True)
    gem_at(c, "s:hand_up", t, 8 * zoom, gem_a, 0, 0, 1.0, 0.6)
    vig(an, c, 170)


def seated_two(an, c, t, lt, dur, PS, PT, zk=0.06, shadows=None, lid=None, sx=230, tx=850, gem_a=0.7, glow=WARM,
               gem_glow=0.7, extra=None, focus=(540, 700), zoom0=0.0):
    """Mother and son sitting by the candle; shadows(c) may draw stories on the curtain behind them;
    lid (0..1) opens the chest between them."""
    zoom = 1.0 + zoom0 + zk * ease(lt / max(dur, 0.1))
    cam = Cam(c, focus, zoom)
    candle_room(an, c, t, cam, 1000)
    if shadows:
        with cam(0.7):
            shadows(c)

    def figs(cc):
        with Cam(cc, focus, zoom)(1.0):
            tag("s:")
            seated(cc, sx, 1010, 1.22, 1, PS, t, YS)
            tag("t:")
            seated(cc, tx, 1010, 1.2, -1, PT, t, TAHM)
            tag("")
            if lid is not None:
                chest(cc, 540, 1012, 1.25, lid)
    an.figures(c, figs, glow, (0, 200, 1080, 1200), anchors=True)
    with cam(1.0):
        standing_candle(c, 540 if lid is None else 640, 960, t, 0.5, 2.0)
        if lid is not None:
            chest_glow(c, 540, 1012, 1.25, lid, t)
    if extra:
        extra(cam, zoom)
    gem_at(c, "s:hand_up", t, 9 * zoom, gem_a, 0, 0, 1.0, gem_glow)
    get(an, "mo_st", lambda: S.Motes(40, 95, 300, 1000)).draw(c, t, (255, 200, 140), 60, rise=4, drift=0.2)
    vig(an, c, 180)


def rostam_shadow(c, x, y, s, a, t, face=1, col=(60, 26, 16), mace_up=0.0):
    """Rostam's shadow on the curtain: helmet and plume, tiger skin, the ox-head mace."""
    if a <= 0.01:
        return
    shadow_layer(c, SH_B, a, col, 2.4)
    person(c, x, y, s, face, {"hand_kind": "oxmace", "hand": (mix(110, 60, mace_up), mix(-330, -560, mace_up)),
                              "mace": mix(10, -10, mace_up), "head": -2, "wind": 0.8, "stance": (58, 48)}, t, "rostam")
    c.restore()


# ================================================================== part 9 shots
def p9_s01(an, c, t):
    """Hook + title: at night by the moon window, the boy demands: 'Whose son am I?' -- she turns away."""
    lt = t - an.start["S01"]
    dur = an.end["TITLE"] - an.start["S01"]
    a0, a1 = LN("p09", "S01", 0)
    b0, b1 = LN("p09", "S01", 1)
    ask = sstep(a0 - 0.2, a0 + 0.5, lt) * (1 - sstep(b1 + 0.8, b1 + 2.0, lt))
    fist = sstep(a1 - 1.0, a1 - 0.6, lt) * (1 - sstep(b1 + 0.8, b1 + 2.0, lt))
    away = sstep(b0, b0 + 0.6, lt)
    PS = {"jaw": jaw(an, "SOHRAB", t, 8), "hand": (mix(40, 160, ask), mix(-262, -380, ask)),
          "hand_kind": "open" if ask > 0.3 and fist < 0.5 else "fist",
          "rhand": (mix(-30, -10, fist), mix(-262, -290, fist)), "head": 1 - 4 * ask + 1.2 * math.sin(t * 0.8),
          "lean": 4 * ask, "wind": 0.3}
    PT = {"jaw": jaw(an, "TAHMINEH", t, 6), "hand": (mix(60, 26, away), mix(-300, -372, away)), "hand_kind": "open",
          "rhand": (-30, -262), "head": 3 + 11 * away + 1.2 * math.sin(t * 0.7), "lean": -3 * away, "wind": 0.3}
    night_two(an, c, t, lt, dur, PS, 250 + 30 * ask, PT, 830, "w91", 0.09)


def p9_s02(an, c, t):
    """Ten years earlier: Samangan under the moon; the baby in his cradle (Rostam's shadow on the curtain);
    then the little boy toddling to his mother: 'Slow down, my little lion!'"""
    lt, dur = loc(an, "S02", t)
    n0, n1 = LN("p09", "S02", 0)
    f0, f1 = LN("p09", "S02", 1)
    g0, g1 = LN("p09", "S02", 2)
    s0, s1 = LN("p09", "S02", 3)
    cut = n1 - 0.5
    grow = g0 + 1.4

    def city():
        focus = (560, 650)
        zoom = 1 + 0.18 * ease(lt / (cut + 0.8))
        city_night(an, c, t, Cam(c, focus, zoom), "c92", 0.0)
        vig(an, c, 160)

    def room(toddler):
        focus = (560, 640)
        zoom = 1.0 + 0.07 * ease((lt - cut) / (dur - cut))
        cam = Cam(c, focus, zoom)
        candle_room(an, c, t, cam, 900, (60, 1020, 280, 900), (560, 220))
        sh = sstep(f0 + 0.3, f0 + 1.3, lt) * (1 - sstep(f1 - 0.4, f1 + 0.6, lt))
        if sh > 0.01:
            with cam(0.7):
                rostam_shadow(c, 300, 860, 0.62, 0.62 * sh, t, 1)
        walk = clamp((lt - s0 + 0.4) / 3.2)
        arms = sstep(s0 - 0.6, s0 + 0.2, lt)
        if not toddler:
            PT = {"jaw": jaw(an, "TAHMINEH", t, 6), "hand": (150 + 6 * math.sin(t * 1.7), -300), "hand_kind": "open",
                  "rhand": (-30, -262), "head": 14 + 2 * math.sin(t * 0.8), "lean": 6, "wind": 0.3}
        else:
            PT = {"jaw": jaw(an, "TAHMINEH", t, 6), "hand": (mix(80, 160, arms), mix(-300, -330, arms)), "hand_kind": "open",
                  "rhand": (mix(-30, 70, arms), mix(-262, -320, arms)), "rhand_kind": "open",
                  "head": 12 - 8 * sstep(s0, s0 + 0.5, lt) + 2 * math.sin(t * 3.0) * sstep(s0, s1, lt) * (1 - sstep(s1, s1 + 0.5, lt)),
                  "lean": 4 + 4 * arms, "wind": 0.3}

        def figs(cc):
            with Cam(cc, focus, zoom)(1.0):
                cradle(cc, 520, 900, 0.82, t, 0.0 if toddler else 1.0, not toddler, sstep(f1, f1 + 1.0, lt))
                seated(cc, 860, 900, 1.2, -1, PT, t, TAHM)
                if toddler:
                    x = mix(330, 640, ease(walk))
                    person(cc, x, 900, 0.36, 1, {"mode": "walk" if 0 < walk < 1 else "stand", "phase": lt * 5.0, "stride": 24,
                                                 "hand": (mix(60, 110, walk), -330), "hand_kind": "open",
                                                 "rhand": (-50, -330), "rhand_kind": "open", "head": -6, "lean": 4}, t, YS)
        an.figures(c, figs, WARM, (0, 200, 1080, 1100))
        get(an, "mo92", lambda: S.Motes(40, 92, 300, 900)).draw(c, t, (255, 200, 140), 60, rise=4, drift=0.2)
        vig(an, c, 170)

    dissolve(c, lt, cut, 0.8, city, lambda: dissolve(c, lt, grow, 0.9, lambda: room(False), lambda: room(True)))


def p9_s03(an, c, t):
    """The training field: at three he gallops a horse; at five he shoots, the target is hit, the king cheers."""
    lt, dur = loc(an, "S03", t)
    r0, r1 = LN("p09", "S03", 0)
    a0, a1 = LN("p09", "S03", 1)
    k0, k1 = LN("p09", "S03", 2)
    cut = r1 - 0.1

    def ride():
        focus = (540, 640)
        zoom = 1.0 + 0.04 * ease(lt / (cut + 0.8))
        cam = Cam(c, focus, zoom)
        meydan(an, c, t, cam, 0.0, "md93")
        x = mix(-160, 820, lt / (cut + 0.9))

        def figs(cc):
            with Cam(cc, focus, zoom)(1.0):
                horse(cc, x, 870, 0.56, 1, {"gait": "gallop", "phase": t * 2.1, "saddle": True, "rider": YS,
                                            "rider_scale": 0.6, "rider_pose": {"lean": 8, "hand": (100, -330),
                                                                               "hand_kind": "open", "wind": 1.0}}, t)
                person(cc, 1000, 870, 0.9, -1, {"hand": (40, -262), "rhand": (-30, -262), "head": 2 + 2 * math.sin(t * 0.6)},
                       t, "king")
        an.figures(c, figs, DAY, (0, 200, 1080, 1000))
        for k in range(4):
            u = (lt * 2.0 + k * 0.25) % 1.0
            S.dust(c, x - 120 - u * 160, 860 - u * 30, 30 + u * 60, t, (230, 200, 150), 80 * (1 - u), k)
        vig(an, c, 140)

    def archery():
        focus = (620, 660)
        zoom = 1.0 + 0.06 * ease((lt - cut) / (dur - cut))
        cam = Cam(c, focus, zoom)
        meydan(an, c, t, cam, 0.15, "md93")
        shots = [(a0 + 1.9, a0 + 2.3), (k0 + 2.2, k0 + 2.6)]       # (release, hit)
        rel = None
        for k, (r, h) in enumerate(shots):
            if lt >= r - 1.8:
                rel = k
        draw_ = 0.0
        if rel is not None:
            r, h = shots[rel]
            draw_ = sstep(r - 1.4, r - 0.6, lt) * (1 - sstep(r, r + 0.08, lt))
        raise_ = sstep(cut + 0.4, cut + 1.2, lt)
        cheer = sstep(k0, k0 + 0.6, lt) * (1 - sstep(k1 + 0.3, k1 + 1.0, lt))
        hit_at = [h for (r, h) in shots if lt >= h]
        shake = max([math.exp(-(lt - h) * 6) for h in hit_at], default=0.0)
        with cam(1.0):
            target(c, 930, 650, 54, t, shake)
            for k, h in enumerate(hit_at):
                stuck(c, 930 - 10 + k * 14, 646 - 8 + k * 12, 1.0, 188 - k * 10)
        PB = {"hand_kind": "bow", "hand": (mix(60, 160, raise_), mix(-300, -404, raise_)),
              "rhand": (mix(-30, mix(118, 20, draw_), raise_), mix(-262, -420, raise_)),
              "head": -4 * raise_, "lean": -2 * draw_, "stance": (52, 46), "wind": 0.4}
        PK = {"jaw": jaw(an, "KING_SAMANGAN", t, 7), "hand": (mix(40, 110, cheer), mix(-262, -520, cheer)),
              "hand_kind": "open" if cheer > 0.3 else "fist", "rhand": (mix(-30, -60, cheer), mix(-262, -500, cheer)),
              "rhand_kind": "open" if cheer > 0.3 else "fist", "head": 2 - 4 * cheer + 1.2 * math.sin(t * 0.6)}
        nock = draw_ > 0.05 or (rel is not None and lt < shots[rel][0] and raise_ > 0.9)

        def figs(cc):
            with Cam(cc, focus, zoom)(1.0):
                person(cc, 150, 870, 0.92, 1, PK, t, "king")
                tag("b:")
                person(cc, 470, 870, 0.6, 1, PB, t, YS)
                tag("")
            bow_string(cc, "b:", draw_, nock)
        an.figures(c, figs, DAY, (0, 200, 1080, 1000), anchors=True)
        with cam(1.0):
            for (r, h) in shots:
                if r <= lt < h:
                    arrow(c, 560, 626, 912, 642, (lt - r) / (h - r), 1.0)
        vig(an, c, 140)

    dissolve(c, lt, cut, 0.8, ride, archery)


def p9_s04(an, c, t):
    """Ten years old: taller than every boy; the king calls for a challenger; Sohrab lifts the champion
    over his head and throws him down on the sand."""
    lt, dur = loc(an, "S04", t)
    k0, k1 = LN("p09", "S04", 1)
    w0, w1 = LN("p09", "S04", 2)
    g0, g1 = LN("p09", "S04", 3)
    focus = (560, 640)
    zoom = 1.0 + 0.06 * ease(lt / dur)
    cam = Cam(c, focus, zoom)
    meydan(an, c, t, cam, 0.9, "md94")
    call = sstep(k0, k0 + 0.6, lt) * (1 - sstep(k1 + 0.4, k1 + 1.2, lt))
    amaze = sstep(g0, g0 + 0.5, lt) * (1 - sstep(g1 + 0.6, g1 + 1.6, lt))
    part = sstep(k0 + 0.6, k0 + 2.8, lt)                        # the boys step back to the edge of the ring
    enter = clamp((lt - w0 - 0.1) / 3.0)
    T1 = w1 + 0.2                                              # face-off ends
    grab = sstep(T1, T1 + 0.5, lt)
    lift = clamp((lt - T1 - 0.6) / 0.8)
    slam = clamp((lt - T1 - 1.4) / 0.45)
    down = lt >= T1 + 1.85
    sx = mix(540, 590, grab)
    wx = mix(1200, 760, ease(enter)) - 50 * grab
    cheer = sstep(T1 + 1.9, T1 + 2.3, lt) * (1 - sstep(dur - 3.0, dur - 1.0, lt))
    arms_up = max(sstep(T1 + 0.4, T1 + 0.9, lt) * (1 - sstep(T1 + 1.6, T1 + 2.0, lt)), 0.0)
    proud = sstep(T1 + 2.2, T1 + 3.0, lt)
    if arms_up > 0.01:
        sh, srh = (mix(120, 40, arms_up), mix(-330, -525, arms_up)), (mix(80, -10, arms_up), mix(-330, -515, arms_up))
        sk = "open"
    elif grab > 0.01 and not down:
        sh, srh, sk = (mix(40, 150, grab), mix(-262, -340, grab)), (mix(-30, 100, grab), mix(-262, -330, grab)), "open"
    else:
        sh, srh, sk = (mix(40, 60, proud), mix(-262, -250, proud)), (mix(-30, -50, proud), mix(-262, -250, proud)), "fist"
    PS = {"hand": sh, "rhand": srh, "hand_kind": sk, "rhand_kind": sk, "stance": (60, 50),
          "head": -3 * proud + 2 * math.sin(t * 0.7) + 6 * grab * (1 - arms_up), "lean": 6 * grab * (1 - arms_up) - 3 * arms_up,
          "wind": 0.5}
    PK = {"jaw": jaw(an, "KING_SAMANGAN", t, 7),
          "hand": (mix(mix(40, 190, call), 100, amaze), mix(mix(-262, -420, call), -520, amaze)),
          "hand_kind": "open" if max(call, amaze) > 0.3 else "fist",
          "rhand": (mix(-30, -60, amaze), mix(-262, -500, amaze)), "rhand_kind": "open" if amaze > 0.3 else "fist",
          "head": 2 - 3 * call - 5 * amaze + 1.2 * math.sin(t * 0.6), "lean": -4 * amaze}
    PW = {"mode": "walk" if 0 < enter < 1 else "stand", "phase": lt * 3.6, "stride": 18, "stance": (62, 54),
          "hand": (mix(60, 160, grab), mix(-280, -360, grab)), "hand_kind": "open",
          "rhand": (mix(-40, 90, grab), mix(-270, -350, grab)), "rhand_kind": "open",
          "head": 4 + 4 * grab, "lean": 6 + 6 * grab}

    def figs(cc):
        with Cam(cc, focus, zoom)(0.8):
            rnd = random.Random(94)
            for k in range(9):
                x = 280 + k * 90 + rnd.uniform(-20, 20)
                up = cheer * (0.6 + 0.4 * math.sin(t * 7 + k))
                person(cc, x, 836, 0.36, 1 if x < 560 else -1,
                       {"hand": (mix(40, 90, up), mix(-262, -520, up)), "hand_kind": "open" if up > 0.3 else "fist",
                        "head": -4 * up, "seed": k}, t, "noble" if k % 3 == 0 else "boy" if k % 3 == 1 else "guard")
        with Cam(cc, focus, zoom)(1.0):
            person(cc, 120, 870, 0.92, 1, PK, t, "king")
            for i, (x0, x1, f) in enumerate(((380, 250, 1), (720, 900, -1), (800, 990, -1))):
                bx = mix(x0, x1, ease(part))
                person(cc, bx, 870, 0.56, f, {"mode": "walk" if 0.02 < part < 0.98 else "stand", "phase": lt * 5 + i,
                                              "stride": 16, "head": -8 + 2 * math.sin(t + i), "seed": i,
                                              "hand": (40, -262)}, t, "boy")
            person(cc, sx, 870, 0.84, 1, PS, t, YS)
            if lift <= 0:
                if enter > 0:
                    person(cc, wx, 870, 0.98, -1, PW, t, "wrestler")
            elif not down:
                e = ease(lift)
                hip0, hip_top = 870 - 0.98 * 250, 870 - 0.84 * 520 - 40
                ang = mix(0, 86, ease(clamp(lift / 0.55)))
                hx = mix(wx, sx + 20, e)
                hy = mix(hip0, hip0 - 60, ease(clamp(lift / 0.55))) if lift < 0.55 else \
                    mix(hip0 - 60, hip_top, ease((lift - 0.55) / 0.45))
                if slam > 0:
                    q = slam * slam
                    hx = mix(sx + 20, 850, slam)
                    hy = mix(hip_top, 870 - 60, q) - 30 * math.sin(slam * math.pi)
                    ang = mix(86, 96, slam)
                cc.save()
                cc.translate(hx, hy)
                cc.rotate(ang)
                person(cc, 0, 0.98 * 250, 0.98, -1, dict(PW, mode="stand", hand=(120, -420), rhand=(60, -440),
                                                        lean=0, head=-10), t, "wrestler")
                cc.restore()
            else:
                person(cc, 860, 872, 0.98, -1, {"mode": "lie", "head": -6 + 3 * math.sin(t * 2), "hand": (60, -330),
                                                "rhand": (-40, -300)}, t, "wrestler")
    an.figures(c, figs, NOON, (0, 200, 1080, 1000))
    if down:
        u = clamp((lt - T1 - 1.85) / 1.6)
        for k in range(4):
            S.dust(c, 780 + k * 60, 860 - 20 * u, 40 + 120 * u, t, (230, 196, 150), 140 * (1 - u), k)
    vig(an, c, 140)


def p9_s05(an, c, t):
    """Sunset: the boys mock him -- 'who is your father?' He has no answer; they run off laughing."""
    lt, dur = loc(an, "S05", t)
    b0, b1 = LN("p09", "S05", 0)
    m0, m1 = LN("p09", "S05", 1)
    l0, l1 = LN("p09", "S05", 2)
    n0, n1 = LN("p09", "S05", 3)
    focus = (420, 660)
    zoom = 1.0 + 0.12 * ease(lt / dur)
    cam = Cam(c, focus, zoom)
    meydan(an, c, t, cam, 2.0, "md95")
    walk = clamp(lt / 1.0)
    turn = lt > 1.1
    point = sstep(b0 + 0.2, b0 + 0.7, lt) * (1 - sstep(l1, l1 + 0.6, lt))
    chest_ = sstep(m0, m0 + 0.4, lt) * (1 - sstep(m1 - 0.3, m1 + 0.3, lt))
    laugh = sstep(l0 - 0.2, l0 + 0.2, lt) * (1 - sstep(l1 + 1.0, l1 + 1.6, lt))
    run = clamp((lt - l1 - 0.2) / 2.8)
    low = sstep(n0, n0 + 1.2, lt)
    PS = {"mode": "walk" if lt < 1.0 else "stand", "phase": lt * 4.2, "stride": 18,
          "jaw": jaw(an, "SOHRAB", t, 8), "hand": (mix(40, 30, chest_), mix(-262, -372, chest_)),
          "hand_kind": "open" if chest_ > 0.3 else "fist", "rhand": (-30, -262),
          "head": -2 * chest_ + 14 * low + 1.2 * math.sin(t * 0.6), "lean": 3 * low, "wind": 0.6}

    def figs(cc):
        with Cam(cc, focus, zoom)(1.0):
            person(cc, mix(430, 380, walk), 870, 0.84, 1 if turn else -1, PS, t, YS)
            for i, (x, s) in enumerate(((800, 0.6), (900, 0.56), (990, 0.58))):
                bob = laugh * (0.5 + 0.5 * math.sin(t * 15 + i * 1.3))
                P = {"mode": "walk" if 0 < run < 1 else "stand", "phase": lt * 6 + i, "stride": 26,
                     "jaw": jaw(an, "BOY", t, 9) if i == 0 else 6 * bob,
                     "head": -8 * bob - 4 * laugh, "lean": -6 * laugh + 10 * (0 < run < 1), "seed": i}
                if i == 0 and point > 0.01:
                    P.update({"hand": (mix(40, 180, point), mix(-262, -400, point)), "hand_kind": "open"})
                else:
                    P.update({"hand": (mix(40, 60, laugh), mix(-262, -300, laugh)),
                              "rhand": (mix(-30, -10, laugh), mix(-262, -290, laugh))})
                if run <= 0.0 or run < 1:
                    person(cc, x + 460 * ease(run), 870, s, 1 if run > 0.02 else -1, P, t, "boy")
    an.figures(c, figs, SUNSET, (0, 200, 1080, 1000))
    vig(an, c, 150 + 20 * low)


def p9_s06(an, c, t):
    """That night: he walks in and asks his mother -- then the threat. She shrinks back."""
    lt, dur = loc(an, "S06", t)
    L = [LN("p09", "S06", k) for k in range(9)]
    walk = clamp((lt - 0.1) / 2.4)
    sx = mix(-140, 250, ease(walk))
    ask = sstep(L[1][0], L[1][0] + 0.5, lt) * (1 - sstep(L[1][1], L[1][1] + 0.5, lt))
    sky = sstep(L[3][0] + 1.2, L[3][0] + 1.9, lt) * (1 - sstep(L[3][1], L[3][1] + 0.5, lt))
    open_ = sstep(L[4][0], L[4][0] + 0.5, lt) * (1 - sstep(L[4][1] + 0.1, L[4][1] + 0.6, lt))
    fists = sstep(L[6][0], L[6][0] + 0.4, lt) * (1 - sstep(L[7][0], L[7][0] + 0.6, lt))
    threat = sstep(L[8][0] + 0.2, L[8][0] + 0.8, lt)
    nod = sstep(L[2][0], L[2][0] + 0.4, lt) * (1 - sstep(L[2][1], L[2][1] + 0.4, lt))
    away = sstep(L[5][0], L[5][0] + 0.5, lt) * (1 - sstep(L[7][0] - 0.2, L[7][0] + 0.3, lt))
    reach = sstep(L[7][0] + 0.3, L[7][0] + 0.9, lt) * (1 - sstep(L[8][0], L[8][0] + 0.4, lt))
    recoil = sstep(L[8][0] + 0.3, L[8][0] + 0.9, lt)
    look = sstep(0.8, 2.0, lt)
    if threat > 0.01:
        h, hk, rh = (mix(40, 70, threat), mix(-262, -560, threat)), "fist", (-30, -262)
    elif sky > 0.01:
        h, hk, rh = (mix(40, 70, sky), mix(-262, -600, sky)), "open", (-30, -262)
    elif open_ > 0.01:
        h, hk, rh = (mix(40, 160, open_), mix(-262, -350, open_)), "open", (mix(-30, -90, open_), mix(-262, -330, open_))
    elif ask > 0.01:
        h, hk, rh = (mix(40, 150, ask), mix(-262, -370, ask)), "open", (-30, -262)
    else:
        h, hk, rh = (mix(40, 50, fists), mix(-262, -250, fists)), "fist", (mix(-30, -40, fists), -262)
    PS = {"mode": "walk" if 0 < walk < 1 else "stand", "phase": lt * 4.0, "stride": 18,
          "jaw": jaw(an, "SOHRAB", t, 8), "hand": h, "hand_kind": hk, "rhand": rh,
          "head": -3 * sky + 4 * fists - 2 * threat + 1.2 * math.sin(t * 0.8), "lean": 4 * fists + 6 * threat, "wind": 0.3}
    PT = {"jaw": jaw(an, "TAHMINEH", t, 6),
          "hand": (mix(mix(mix(50, 70, nod), 26, max(away, recoil)), 150, reach), mix(mix(-300, -372, max(away, recoil)), -390, reach)),
          "hand_kind": "open", "rhand": (mix(-30, 20, recoil), mix(-262, -380, recoil)), "rhand_kind": "open",
          "head": mix(10, 0, look) + 5 * nod + 12 * away - 8 * recoil + 1.2 * math.sin(t * 0.7),
          "lean": -2 * away - 8 * recoil + 3 * reach, "wind": 0.3}
    night_two(an, c, t, lt, dur, PS, sx + 70 * threat, PT, 830, "w91", 0.06, gem_a=0.5)


def p9_s07(an, c, t):
    """Turn + end: close on Tahmineh -- ten years of a secret; 'Sit down, and listen.'
    Behind her, Rostam's giant shadow rises on the curtain."""
    lt = t - an.start["S07"]
    dur = an.end["END"] - an.start["S07"]
    k0, k1 = LN("p09", "S07", 1)
    s0, s1 = LN("p09", "S07", 2)
    n0, n1 = LN("p09", "S07", 3)
    focus = (560, 640)
    zoom = 1.0 + 0.1 * ease(lt / dur)
    cam = Cam(c, focus, zoom)
    fl = flick(t)
    with cam(0.6):
        S.lin(c, 0, H, [(0, (16, 10, 22)), (0.45, (44, 26, 34)), (1, (6, 3, 5))])
        wall_panel(c, 0, 1100, 260, 1200, (100, 54, 44), (170, 104, 74), 96)
        S.glow(c, 1000, 640, 700, (255, 170, 90), 110 * fl)
        sh = sstep(n0 + 0.4, n0 + 2.6, lt)
        if sh > 0.01:
            rostam_shadow(c, 290, 1100, 1.36, 0.84 * sh, t, 1, (46, 18, 12), sstep(n1 + 0.4, n1 + 2.0, lt))
    secret = sstep(k0 + 1.0, k0 + 2.0, lt)
    sit = sstep(s0, s0 + 0.6, lt) * (1 - sstep(s1 + 0.2, s1 + 0.8, lt))
    P = {"jaw": jaw(an, "TAHMINEH", t, 6), "hand": (mix(mix(30, 60, secret), 170, sit), mix(mix(-370, -330, secret), -300, sit)),
         "hand_kind": "open", "rhand": (mix(20, -30, secret), mix(-380, -262, secret)), "rhand_kind": "open",
         "head": 14 - 6 * secret - 10 * sit + 4 * sstep(s1 + 0.4, s1 + 1.4, lt) + 1.2 * math.sin(t * 0.6),
         "lean": 3 - 2 * secret, "wind": 0.35}

    def figs(cc):
        with Cam(cc, focus, zoom)(1.0):
            person(cc, 720, 1660, 2.25, -1, P, t, TAHM)
    an.figures(c, figs, mixc(WARM, NIGHT, 0.3), (0, 150, 1080, 1800), alpha=170)
    S.glow(c, 1060, 760, 300, (255, 200, 140), 60 * fl)
    get(an, "mo97", lambda: S.Motes(40, 97, 250, 1000)).draw(c, t, (255, 210, 150), 60, rise=3, drift=0.2)
    vig(an, c, 180)


# ================================================================== part 10 shots
def west_window(an, c, t, cam, x, yb, w, h, key="ww", vis=0.0, red=0.0):
    """A tall arched window looking west: mountains under the moon; vis (0..1) shows a vision in the sky
    (a young hero leading riders toward Iran); red tints the night."""
    S.lin(c, 0, H, [(0, (10, 10, 22)), (0.5, (22, 20, 38)), (1, (5, 4, 8))])
    arch = S.arch_path(x, yb, w, h)
    with cam(0.5):
        c.save()
        c.clipPath(arch, skia.ClipOp.kIntersect, True)
        S.lin(c, yb - h, yb, [(0, mixc((10, 14, 40), (40, 10, 24), red)), (0.6, mixc((40, 50, 100), (110, 40, 60), red)),
                              (1, mixc((96, 96, 146), (170, 80, 80), red))], (x - w, yb - h - 40, x + w, yb + 10))
        get(an, key + "st", lambda: S.Stars(110, 900, 303)).draw(c, t, 1.0, 900)
        S.moon(c, x - w * 0.22, yb - h * 0.72, w * 0.09)
        rg = get(an, key + "rg", lambda: (S.make_ridge(x - w, x + w, yb - 200, 110, 301, 8, 4, 0.5),
                                          S.make_ridge(x - w, x + w, yb - 110, 60, 302, 8, 4, 0.2)))
        S.ridge(c, rg[0], mixc((64, 70, 116), (110, 50, 70), red))
        S.lin(c, yb - 330, yb - 180, [(0, (180, 190, 240, 0)), (1, (180, 190, 240, 50))], (x - w, yb - 330, x + w, yb - 180))
        S.ridge(c, rg[1], mixc((30, 32, 62), (60, 22, 36), red))
        get(an, key + "cl", lambda: S.Clouds([(yb - h * 0.5, 9), (yb - h * 0.38, 7)], 304, 200, 420)).draw(
            c, t * 2, mixc((24, 28, 56), (70, 24, 40), red), 160)
        if vis > 0.01:
            ghost_layer(c, (x - w / 2, yb - h, x + w / 2, yb), 0.62 * vis, (255, 196, 140), 2.4)
            u = clamp(vis)
            bx = x - w * 0.12 + 120 * (1 - u)
            by = yb - 250
            for i in range(4):
                rx = bx + 150 + i * 100 + 10 * math.sin(t * 1.3 + i)
                horse(c, rx, by - (i % 2) * 10, 0.24, -1, {"gait": "gallop", "phase": t * 1.6 + i * 0.37, "saddle": True,
                                                           "rider": "warrior_tu", "rider_pose": {"hand_kind": "spear",
                                                                                                "hand": (110, -340), "lean": 8}}, t)
                if i in (0, 2):
                    fillp(c, ppath([(rx - 2, by - 170), (rx - 56, by - 160), (rx - 48, by - 142), (rx - 2, by - 146)]))
            horse(c, bx, by + 8, 0.34, -1, {"gait": "gallop", "phase": t * 1.6, "saddle": True, "rider": "sohrab",
                                            "rider_pose": {"hand_kind": "spear", "hand": (130, -400), "lean": 10, "wind": 1.0}}, t)
            c.restore()
        c.restore()
        edge = skia.Paint(AntiAlias=True, Color=C(*INK))
        edge.setStyle(skia.Paint.kStroke_Style)
        edge.setStrokeWidth(28)
        c.drawPath(arch, edge)
        c.drawRect(skia.Rect.MakeLTRB(x - w / 2 - 50, yb, x + w / 2 + 50, yb + 30), paint(C(*INK)))
    p = skia.Paint(AntiAlias=True)
    p.setShader(skia.GradientShader.MakeLinear([skia.Point(x, yb - h), skia.Point(x - w * 1.2, yb + 600)],
                                               [C(150, 170, 230, 60), C(150, 170, 230, 0)]))
    c.drawPath(ppath([(x - w / 2, yb - h * 0.7), (x + w / 2, yb - h * 0.5), (x + w * 0.2, yb + 700),
                      (x - w * 1.5, yb + 700)]), p)


def ancestor(c, x, y, s, a, t, who):
    """One of Sohrab's forefathers as a shadow on the curtain (drawn inside a shadow_layer)."""
    if a <= 0.01:
        return
    c.saveLayerAlpha(None, int(255 * clamp(a)))
    if who == "nariman":
        person(c, x, y, s, 1, {"hand_kind": "spear", "hand": (100, -330), "head": -2, "wind": 0.7, "stance": (56, 46)}, t,
               dict(LOOKS["warrior_ir"], beard="long"))
    elif who == "sam":
        person(c, x, y, s, 1, {"hand_kind": "mace", "hand": (110, -330), "mace": 14, "head": -2, "wind": 0.7,
                               "stance": (58, 48)}, t, dict(LOOKS["warrior_ir"], beard="long", heavy=True, b=1.12))
    elif who == "zal":
        person(c, x, y, s, 1, {"hand_kind": "staff", "hand": (90, -320), "head": 0, "wind": 0.9, "stance": (50, 42)}, t,
               dict(LOOKS["noble"], head="bare", hair=True, beard="long", cape=True))
    else:
        person(c, x, y, s, 1, {"hand_kind": "oxmace", "hand": (110, -330), "mace": 10, "head": -3, "wind": 0.9,
                               "stance": (60, 50)}, t, "rostam")
    c.restore()


def p10_s01(an, c, t):
    """Hook + title: by the candle she tells him: 'Your father is Rostam' -- his shadow rises on the curtain."""
    lt = t - an.start["S01"]
    dur = an.end["TITLE"] - an.start["S01"]
    a0, a1 = LN("p10", "S01", 0)
    b0, b1 = LN("p10", "S01", 1)
    sh = sstep(a0 + 1.6, a0 + 3.0, lt)
    awe = sstep(b0, b0 + 0.5, lt)
    PS = {"jaw": jaw(an, "SOHRAB", t, 8), "hand": (mix(110, 150, awe), mix(-300, -400, awe)), "hand_kind": "open",
          "rhand": (mix(-30, -60, awe), mix(-262, -360, awe)), "rhand_kind": "open" if awe > 0.3 else "fist",
          "head": 3 - 10 * awe + 1.2 * math.sin(t * 0.8), "lean": 2 - 6 * awe}
    PT = {"jaw": jaw(an, "TAHMINEH", t, 6), "hand": (mix(80, 140, sstep(a0, a0 + 0.6, lt)), mix(-300, -350, sstep(a0, a0 + 0.6, lt))),
          "hand_kind": "open", "rhand": (-30, -262), "head": 4 + 1.2 * math.sin(t * 0.7), "lean": 3}

    def shadows(cc):
        rostam_shadow(cc, 540, 880, 0.74, 0.8 * sh, t, 1, (56, 22, 14), sstep(dur - 3.0, dur - 1.6, lt))
    seated_two(an, c, t, lt, dur, PS, PT, 0.1, shadows)


def p10_s02(an, c, t):
    """Samangan at night; then the two by the candle: 'You are the son of Rostam... and of Zal, Sam, Nariman.'"""
    lt, dur = loc(an, "S02", t)
    L = [LN("p10", "S02", k) for k in range(7)]
    cut = L[0][1] - 0.4

    def city():
        focus = (560, 650)
        zoom = 1 + 0.16 * ease(lt / (cut + 0.8))
        city_night(an, c, t, Cam(c, focus, zoom), "c102", 0.0)
        vig(an, c, 160)

    def room():
        reach = sstep(L[2][0], L[2][0] + 0.6, lt) * (1 - sstep(L[3][0], L[3][0] + 0.5, lt))
        lean_in = sstep(L[4][0] - 0.2, L[4][0] + 0.4, lt) * (1 - sstep(L[6][0], L[6][0] + 0.6, lt))
        count = sstep(L[5][0], L[5][0] + 0.5, lt) * (1 - sstep(L[5][1], L[5][1] + 0.5, lt))
        sky = sstep(L[6][0], L[6][0] + 0.6, lt)
        sh = sstep(L[3][0] + 0.8, L[3][0] + 2.0, lt)
        PS = {"jaw": jaw(an, "SOHRAB", t, 8), "hand": (mix(110, 150, lean_in), mix(-300, -330, lean_in)), "hand_kind": "open",
              "rhand": (-30, -262), "head": 3 - 6 * lean_in - 12 * sky + 1.2 * math.sin(t * 0.8), "lean": 6 * lean_in}
        if sky > 0.01:
            th, tk = (mix(80, 70, sky), mix(-300, -560, sky)), "open"
        elif count > 0.01:
            th, tk = (mix(80, 170, count), mix(-300, -420, count)), "open"
        else:
            th, tk = (mix(80, 170, reach), mix(-300, -330, reach)), "open"
        PT = {"jaw": jaw(an, "TAHMINEH", t, 6), "hand": th, "hand_kind": tk, "rhand": (-30, -262),
              "head": 4 - 6 * sky + 1.2 * math.sin(t * 0.7), "lean": 3 + 3 * reach}

        def shadows(cc):
            rostam_shadow(cc, 540, 880, 0.74, 0.8 * sh, t, 1, (56, 22, 14))
        seated_two(an, c, t, lt - cut, dur - cut, PS, PT, 0.07, shadows)
    dissolve(c, lt, cut, 0.8, city, room)


def p10_s03(an, c, t):
    """The forefathers on the curtain: Nariman, Sam, Zal, Rostam; Rostam rides; Rostam and the White Div."""
    lt, dur = loc(an, "S03", t)
    g0, g1 = LN("p10", "S03", 1)
    d0, d1 = LN("p10", "S03", 2)
    y0, y1 = LN("p10", "S03", 3)
    focus = (600, 640)
    zoom = 1.0 + 0.06 * ease(lt / dur)
    cam = Cam(c, focus, zoom)
    fl = flick(t)
    S.lin(c, 0, H, [(0, (60, 26, 18)), (0.2, (170, 96, 52)), (0.45, (236, 168, 96)), (0.62, (214, 140, 80)),
                    (0.8, (110, 50, 30)), (1, (16, 6, 6))])
    pf = skia.Paint(AntiAlias=True)
    pf.setShader(skia.GradientShader.MakeLinear([skia.Point(0, 0), skia.Point(96, 0)],
                                                [C(90, 36, 20, 90), C(255, 230, 190, 30), C(90, 36, 20, 90)],
                                                [0.0, 0.5, 1.0], skia.TileMode.kRepeat))
    c.drawRect(skia.Rect.MakeLTRB(0, 0, W, H), pf)
    S.glow(c, 300, 1000, 900, (255, 190, 110), 110 * fl)
    sway = 5 * math.sin(t * 1.3)
    out = sstep(g0 - 0.2, g0 + 0.6, lt)
    with cam(0.8):
        if out < 0.99:
            shadow_layer(c, SH_B, 0.86 * (1 - out), (44, 20, 14), 2.2)
            c.save()
            c.translate(sway, 0)
            for who, x, s_, k in (("nariman", 380, 0.6, 2.8), ("sam", 560, 0.64, 3.4), ("zal", 740, 0.62, 3.9),
                                  ("rostam", 920, 0.7, 4.8)):
                ancestor(c, x, 860, s_, sstep(k - 0.3, k + 0.4, lt), t, who)
            c.restore()
            c.restore()
        ride = clamp((lt - g0 + 0.2) / 4.0)
        if 0 < ride < 1:
            shadow_layer(c, SH_B, 0.86 * sstep(0, 0.1, ride) * (1 - sstep(0.9, 1.0, ride)), (44, 20, 14), 2.2)
            horse(c, mix(240, 1220, ride), 866, 0.8, 1, {"gait": "gallop", "phase": t * 1.9, "saddle": True, "rider": "rostam",
                                                         "rider_pose": {"lean": 12, "hand": (120, -330), "hand_kind": "oxmace",
                                                                        "mace": 60, "head": 4, "wind": 1.2}}, t)
            c.restore()
        dv = sstep(d0 - 0.4, d0 + 0.3, lt)
        if dv > 0.01:
            u = lt - d0
            hit = sstep(1.9, 2.3, u)
            fall = sstep(y0 - 0.6, y0 + 0.4, lt)
            win = sstep(y0, y0 + 0.8, lt)
            shadow_layer(c, SH_B, 0.86 * dv, (44, 20, 14), 2.2)
            c.save()
            c.translate(sway, 0)
            person(c, 460 + 40 * hit, 860, 0.86, 1, {"hand_kind": "oxmace",
                                                    "hand": (mix(mix(40, 160, hit), 70, win), mix(mix(-580, -360, hit), -600, win)),
                                                    "mace": mix(mix(-40, 70, hit), -10, win), "lean": 8 * hit * (1 - win),
                                                    "head": -4 - 4 * win, "wind": 0.8, "stance": (64, 52)}, t, "rostam")
            c.save()
            c.translate(860 + 50 * hit + 60 * fall, 860)
            c.rotate(40 * fall)
            person(c, 0, 0, 0.84, -1, {"hand_kind": "club", "hand": (70, -560), "mace": -30 - 30 * hit,
                                       "lean": -16 * hit, "head": -10 * hit, "jaw": 8,
                                       "rhand": (-80, -420), "rhand_kind": "open", "stance": (60, 56)}, t, "div")
            c.restore()
            c.restore()
            c.restore()
    look = sstep(0.4, 1.4, lt)
    PS = {"jaw": jaw(an, "SOHRAB", t, 8), "hand": (mix(110, 140, sstep(d0, d0 + 0.5, lt)), mix(-300, -380, sstep(d0, d0 + 0.5, lt))),
          "hand_kind": "open", "rhand": (-30, -262), "head": -6 * look + 1.2 * math.sin(t * 0.8), "lean": -3 * look}

    def figs(cc):
        with Cam(cc, focus, zoom)(1.0):
            tag("s:")
            seated(cc, 120, 1260, 1.62, 1, PS, t, YS)
            tag("")
    an.figures(c, figs, WARM, (0, 300, 1080, 1500), anchors=True)
    gem_at(c, "s:hand_up", t, 11 * zoom, 0.8, 0, 0, 1.0, 0.8)
    S.glow(c, 640, 1240, 520, (255, 170, 80), 90 * fl)
    vig(an, c, 200)


def p10_s04(an, c, t):
    """The chest: the letter, three rubies in gold; 'He thinks you are still a little child'; the jewel on his arm."""
    lt, dur = loc(an, "S04", t)
    L = [LN("p10", "S04", k) for k in range(6)]
    lid = sstep(1.0, 2.2, lt)
    show = sstep(L[1][0] + 0.2, L[1][0] + 1.0, lt)
    rub = sstep(L[1][0] + 2.4, L[1][0] + 3.4, lt)
    lean_in = sstep(L[2][0] - 0.2, L[2][0] + 0.4, lt) * (1 - sstep(L[3][1], L[3][1] + 0.6, lt))
    arm = sstep(L[4][0], L[4][0] + 0.6, lt)
    touch = sstep(L[5][0], L[5][0] + 0.7, lt)
    sad = sstep(L[3][0] + 1.2, L[3][0] + 2.0, lt) * (1 - sstep(L[3][1] + 0.4, L[3][1] + 1.0, lt))
    PS = {"jaw": jaw(an, "SOHRAB", t, 8), "hand": (mix(mix(110, 140, lean_in), 60, arm), mix(mix(-300, -320, lean_in), -470, arm)),
          "hand_kind": "open" if arm < 0.5 else "fist", "rhand": (mix(-30, 30, arm), mix(-262, -360, arm)),
          "rhand_kind": "open" if arm > 0.5 else "fist",
          "head": 6 + 6 * lean_in - 4 * arm + 1.2 * math.sin(t * 0.8), "lean": 5 * lean_in}
    PT = {"jaw": jaw(an, "TAHMINEH", t, 6),
          "hand": (mix(mix(80, 120, sstep(0.4, 1.2, lt) * (1 - show)), mix(150, 170, touch), max(show * (1 - touch), touch)),
                   mix(-300, mix(-380, -350, touch), max(show * (1 - touch), touch))),
          "hand_kind": "open", "rhand": (mix(-30, 50, rub * (1 - touch)), mix(-262, -300, rub * (1 - touch))), "rhand_kind": "open",
          "head": 8 + 6 * sad + 1.2 * math.sin(t * 0.7), "lean": 4 + 4 * touch}

    def extra(cam, zoom):
        h = A("t:hand")
        if h and show > 0.01 and touch < 0.6:
            scroll(c, h[0] - 30 * zoom, h[1] - 50 * zoom, 70 * zoom, 96 * zoom, -14, show * (1 - sstep(0.0, 0.6, touch)), 0.3)
        with cam(1.0):
            for k in range(3):
                a = sstep(L[1][0] + 2.4 + 0.35 * k, L[1][0] + 3.0 + 0.35 * k, lt)
                ruby(c, 500 + k * 40, 916 - 6 * (k % 2), 11, t, a, k * 1.3)
    gg = 0.7 + 1.0 * arm * (1 - sstep(L[5][1], L[5][1] + 1.0, lt))
    seated_two(an, c, t, lt, dur, PS, PT, 0.08, None, lid, gem_a=0.9, gem_glow=gg, extra=extra, focus=(540, 760))


def p10_s05(an, c, t):
    """The warning: Afrasiab's shadow on the curtain, grows and reaches for the boy; then Rostam's shadow calls."""
    lt, dur = loc(an, "S05", t)
    L = [LN("p10", "S05", k) for k in range(7)]
    af = sstep(L[1][0] + 0.2, L[1][0] + 1.4, lt) * (1 - sstep(L[5][0] - 0.3, L[5][0] + 0.6, lt))
    grow = sstep(L[4][0], L[4][1], lt)
    ro = sstep(L[5][0] + 0.6, L[5][0] + 1.6, lt) * (1 - sstep(L[6][0], L[6][0] + 0.8, lt))
    finger = sstep(L[0][0], L[0][0] + 0.5, lt) * (1 - sstep(L[0][1], L[0][1] + 0.5, lt))
    why = sstep(L[3][0], L[3][0] + 0.4, lt) * (1 - sstep(L[3][1], L[3][1] + 0.5, lt))
    heart = sstep(L[6][0] - 0.2, L[6][0] + 0.5, lt)
    PS = {"jaw": jaw(an, "SOHRAB", t, 8), "hand": (mix(110, 160, why), mix(-300, -380, why)), "hand_kind": "open",
          "rhand": (-30, -262), "head": 4 - 4 * why - 6 * af + 1.2 * math.sin(t * 0.8), "lean": 3 * why}
    PT = {"jaw": jaw(an, "TAHMINEH", t, 6),
          "hand": (mix(mix(80, 70, finger), 30, heart), mix(mix(-300, -520, finger), -372, heart)),
          "hand_kind": "open", "rhand": (-30, -262), "head": 4 + 14 * heart + 1.2 * math.sin(t * 0.7), "lean": 3 + 3 * heart}

    def shadows(cc):
        if af > 0.01:
            s_ = mix(0.84, 1.04, ease(grow))
            shadow_layer(cc, SH_B, 0.86 * af, (36, 4, 8), 2.4)
            fillp(cc, spath([(560 + 80 * s_, 870, 0), (560 + 70 * s_, 600 - 200 * s_), (560 + 40 * s_, 560 - 240 * s_),
                             (560 + 10 * s_, 600 - 200 * s_), (560, 870, 0)]))
            for k, x in enumerate((360, 780)):
                person(cc, x, 870, 0.56, 1 if k == 0 else -1, {"hand_kind": "spear", "hand": (90, -320), "head": -2,
                                                               "stance": (50, 44)}, t, "warrior_tu")
            person(cc, 560, 870, s_, -1, {"mode": "sit", "hand": (mix(90, 210, grow), mix(-300, -420, grow)),
                                          "hand_kind": "open", "rhand": (-30, -262), "head": -4 - 4 * grow, "lean": 6 * grow},
                   t, "afrasiab")
            cc.restore()
        if ro > 0.01:
            shadow_layer(cc, SH_B, 0.8 * ro, (56, 22, 14), 2.4)
            person(cc, 600, 880, 0.74, -1, {"hand_kind": "open", "hand": (mix(140, 170, 0.5 + 0.5 * math.sin(t * 3)), -420),
                                            "rprop": "oxmace", "rhand": (-30, -300), "head": -2, "wind": 0.8}, t, "rostam")
            cc.restore()
        if af > 0.01:
            S.lin(cc, 300, 900, [(0, (40, 60, 120, 0)), (1, (40, 60, 120, 60 * af))], (120, 300, 960, 900))
    seated_two(an, c, t, lt, dur, PS, PT, 0.07, shadows, glow=mixc(WARM, (200, 120, 130), af * 0.5))


def p10_s06(an, c, t):
    """He stands up: 'With a father like him, why should I hide who I am?' -- the jewel shines on his arm."""
    lt, dur = loc(an, "S06", t)
    L = [LN("p10", "S06", k) for k in range(3)]
    focus = (540, 640)
    zoom = 1.0 + 0.06 * ease(lt / dur)
    cam = Cam(c, focus, zoom)
    moon_window(an, c, t, cam, 800, 1000, 420, 760, 0.0, "w106")
    with cam(0.6):
        S.glow(c, 60, 900, 700, (255, 170, 90), 90 * flick(t))
    rise = sstep(0.0, 1.6, lt)
    open_ = sstep(L[0][0] + 1.4, L[0][0] + 2.0, lt) * (1 - sstep(L[1][0], L[1][0] + 0.5, lt))
    chest_ = sstep(L[1][0], L[1][0] + 0.5, lt) * (1 - sstep(L[1][1] - 0.6, L[1][1], lt))
    up = sstep(L[1][1] - 0.6, L[1][1] + 0.2, lt)
    plead = sstep(L[2][0], L[2][0] + 0.6, lt)
    if up > 0.01:
        h, hk = (mix(40, 90, up), mix(-380, -560, up)), "fist"
    elif chest_ > 0.01:
        h, hk = (mix(160, 40, chest_), mix(-400, -380, chest_)), "fist"
    else:
        h, hk = (mix(60, 170, open_), mix(-280, -420, open_)), "open"
    PS = {"jaw": jaw(an, "SOHRAB", t, 8), "hand": h, "hand_kind": hk,
          "rhand": (mix(-30, -100, open_), mix(-262, -400, open_)), "rhand_kind": "open" if open_ > 0.3 else "fist",
          "head": -4 - 4 * up + 1.2 * math.sin(t * 0.8), "lean": -2 * up, "wind": 0.5}
    PT = {"jaw": jaw(an, "TAHMINEH", t, 6), "hand": (mix(80, 120, plead), mix(-300, -460, plead)), "hand_kind": "open",
          "rhand": (-30, -262), "head": -6 - 6 * plead + 1.2 * math.sin(t * 0.7), "lean": -4 * plead}

    def figs(cc):
        with Cam(cc, focus, zoom)(1.0):
            tag("s:")
            person(cc, 380, 1640 + 320 * (1 - ease(rise)), 2.1, 1, PS, t, YS)
            tag("t:")
            seated(cc, 930, 1250, 1.42, -1, PT, t, TAHM)
            tag("")
    an.figures(c, figs, NIGHT, (0, 100, 1080, 1800), anchors=True)
    gem_at(c, "s:hand_up", t, 15 * zoom, 1.0, 0, 0, 2.0, 1.0 + 0.6 * up)
    vig(an, c, 180)


def p10_s07(an, c, t):
    """Turn + end: he looks west from the window toward Iran; a vision -- a young hero leading an army."""
    lt = t - an.start["S07"]
    dur = an.end["END"] - an.start["S07"]
    L = [LN("p10", "S07", k) for k in range(5)]
    focus = (620, 620)
    zoom = 1.0 + 0.1 * ease(lt / dur)
    cam = Cam(c, focus, zoom)
    vis = sstep(L[4][0] + 0.4, L[4][0] + 2.6, lt)
    west_window(an, c, t, cam, 720, 1000, 560, 760, "ww107", vis, 0.45 * vis)
    walk = clamp((lt - 0.3) / 2.8)
    reach = sstep(L[2][0], L[2][0] + 0.6, lt) * (1 - sstep(L[3][0], L[3][0] + 0.4, lt))
    grip = sstep(L[3][0], L[3][0] + 0.5, lt)
    PS = {"mode": "walk" if 0 < walk < 1 else "stand", "phase": lt * 3.6, "stride": 16, "jaw": jaw(an, "SOHRAB", t, 8),
          "hand": (mix(40, 170, reach), mix(-262, -400, reach)), "hand_kind": "open" if reach > 0.3 else "fist",
          "rhand": (mix(-30, 40, grip), mix(-262, -356, grip)), "rhand_kind": "fist",
          "head": -4 - 4 * reach - 3 * vis + 1.2 * math.sin(t * 0.7), "wind": 0.5}

    def figs(cc):
        with Cam(cc, focus, zoom)(1.0):
            tag("s:")
            person(cc, mix(-140, 300, ease(walk)), 1420, 1.72, 1, PS, t, YS)
            tag("")
    an.figures(c, figs, mixc(MOON, (255, 170, 140), 0.4 * vis), (0, 150, 1080, 1700), anchors=True)
    gem_at(c, "s:hand_up", t, 12 * zoom, 1.0, 0, 0, 3.0, 0.8 + 0.9 * grip)
    get(an, "mo107", lambda: S.Motes(40, 107, 250, 1000)).draw(c, t, (200, 214, 255), 60, rise=3, drift=0.2)
    vig(an, c, 180 + 30 * vis)


P10 = {"S01": p10_s01, "TITLE": p10_s01, "S02": p10_s02, "S03": p10_s03, "S04": p10_s04, "S05": p10_s05,
       "S06": p10_s06, "S07": p10_s07, "END": p10_s07}
SHIFT10 = {"S04": -110}


P09 = {"S01": p9_s01, "TITLE": p9_s01, "S02": p9_s02, "S03": p9_s03, "S04": p9_s04, "S05": p9_s05, "S06": p9_s06,
       "S07": p9_s07, "END": p9_s07}
SHIFT9 = {"S04": 60}

register(P09, SHIFT9)
