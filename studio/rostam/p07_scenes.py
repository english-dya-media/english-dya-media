"""Parts 7-8 (row 4 of OUTLINE.md, "Rostam's Armband"): every shot as a shadow-play scene.

Importing this module registers part 7's shots; p08_scenes.py imports it and registers part 8's.
New here, to reuse: gem() (Rostam's jewel, drawn glowing over the silhouettes), baby() (a swaddled newborn,
puppet pen), dawn_window() (the sky before sunrise through an arched window), months_window() (moon phases
with falling leaves, snow and blossom), Coins (gold showered at the wedding), lamp_row() (lamps lit one by
one), courtyard() (the palace courtyard by day), birth_room(), dissolve() (a cross-fade inside one shot).
Line timings are read from pNN/audio/timeline.json (LN), so the action follows the voices if they change.
"""
import json, math, os, random
import skia
import anim
from anim import C, mix, mixc, clamp, ease, sstep, _k, Cam, Pen, ANCH, rope, spath, ppath, paint, fillp, W, H
import puppets
from puppets import person, horse, LOOKS
import sets as S
from ep01_scenes import loc, jaw, get, vig, tag, A, ground, INK, hall
from p05_scenes import (TAHM, WARM, MOON, candle_light, standing_candle, in_bed, bed, blanket, wall_panel,
                        king_room, ghost_layer, shadow_layer, eagle, palace, city_night, moon_window, register)

HERE = os.path.dirname(os.path.abspath(__file__))
DAWN = (255, 198, 150)                             # rim light at sunrise
DAY = (255, 214, 160)                              # morning sun
_TL = {}


def LN(part, sid, k):
    """(start, end) of line k of shot sid, in seconds from the shot's start (as an.start counts it)."""
    if part not in _TL:
        tl = json.load(open(os.path.join(HERE, part, "audio", "timeline.json"), encoding="utf-8"))
        _TL[part] = {s["id"]: [(l["start"] - (0.0 if i == 0 else s["start"]), l["end"] - (0.0 if i == 0 else s["start"]))
                               for l in s["lines"]] for i, s in enumerate(tl["scenes"])}
    return _TL[part][sid][k]


def dissolve(c, lt, t0, d, draw_a, draw_b):
    """Shot A until t0, then a cross-dissolve of d seconds into shot B."""
    if lt < t0:
        draw_a()
    elif lt >= t0 + d:
        draw_b()
    else:
        draw_a()
        c.saveLayerAlpha(None, int(255 * ease((lt - t0) / d)))
        draw_b()
        c.restore()


# ------------------------------------------------------------------ props
def gem(c, x, y, r, t, a=1.0, seed=0.0, glow=1.0, col=(255, 160, 70)):
    """Rostam's jewel: a faceted stone that glows and twinkles (drawn over the silhouettes)."""
    if a <= 0.01:
        return
    pulse = 0.82 + 0.18 * math.sin(t * 2.6 + seed)
    S.glow(c, x, y, r * 10, col, 110 * a * pulse * glow)
    S.glow(c, x, y, r * 3.2, (255, 222, 150), 150 * a * pulse * glow)
    p = skia.Paint(AntiAlias=True)
    p.setShader(skia.GradientShader.MakeRadial(skia.Point(x - r * 0.3, y - r * 0.4), r * 1.6,
                                               [C(255, 244, 200, 255 * a), C(236, 128, 48, 255 * a),
                                                C(140, 34, 26, 255 * a)], [0.0, 0.45, 1.0]))
    c.drawPath(ppath([(x, y - r * 1.2), (x + r * 0.95, y - r * 0.4), (x + r * 0.75, y + r * 0.65), (x, y + r * 1.1),
                      (x - r * 0.75, y + r * 0.65), (x - r * 0.95, y - r * 0.4)]), p)
    lp = skia.Paint(AntiAlias=True, Color=C(255, 236, 190, 150 * a))
    lp.setStyle(skia.Paint.kStroke_Style)
    lp.setStrokeWidth(max(1.0, r * 0.12))
    c.drawPath(ppath([(x - r * 0.95, y - r * 0.4), (x - r * 0.35, y - r * 0.1), (x + r * 0.35, y - r * 0.1),
                      (x + r * 0.95, y - r * 0.4)], False), lp)
    c.drawPath(ppath([(x - r * 0.35, y - r * 0.1), (x, y + r * 1.1), (x + r * 0.35, y - r * 0.1)], False), lp)
    tw = max(0.0, math.sin(t * 1.9 + seed)) ** 8
    if tw > 0.03:
        sp = paint(C(255, 250, 230, 230 * a * tw))
        L = r * 3.2 * tw + r
        cx, cy = x - r * 0.35, y - r * 0.5
        c.drawPath(ppath([(cx - L, cy), (cx, cy - r * 0.18), (cx + L, cy), (cx, cy + r * 0.18)]), sp)
        c.drawPath(ppath([(cx, cy - L), (cx + r * 0.18, cy), (cx, cy + L), (cx - r * 0.18, cy)]), sp)


def seated(cc, X, Y, s, face, P, t, look):
    """A person sitting on the floor: person(mode="sit") clipped at the floor line
    (the seated robe of puppets.garment hangs below the feet; in_bed hides it the same way)."""
    cc.save()
    cc.clipRect(skia.Rect.MakeLTRB(-5000, -5000, 5000, Y + 2))
    person(cc, X, Y, s, face, dict(P, mode="sit"), t, look)
    cc.restore()


def gem_at(c, name, t, r, a=1.0, dx=0.0, dy=0.0, seed=0.0, glow=1.0):
    p = A(name)
    if p:
        gem(c, p[0] + dx, p[1] + dy, r, t, a, seed, glow)
    return p


def baby(cc, x, y, s, t, ang=0.0, arm=0.0, face=1, wr=1.0):
    """A swaddled newborn lying on its back (puppet pen), head at local (-44, -2), face up, the bundle to the
    right (about 120 x 36 at s=1). arm (0..1) raises a tiny fist; anchors 'barm' (the arm) and 'bhead'."""
    anim.begin_fig(cc, (x - 160 * s, y - 120 * s, x + 160 * s, y + 120 * s))
    cc.save()
    cc.translate(x, y)
    cc.rotate(ang)
    cc.scale(s * face, s)
    w = 2.0 * math.sin(t * 2.7) * wr
    fillp(cc, spath([(-30, -15), (0, -18), (36, -16), (62, -11), (76, -3), (72, 9), (44, 15), (2, 17), (-28, 14)]))
    if Pen.mode != "anchor":
        cc.drawCircle(-44, -2, 17, anim.ink())
    for k, hx in enumerate((6, 28, 50)):          # cut-out pattern of the swaddling cloth
        anim.hole(cc, ppath([(hx - 5, 0), (hx, -5 + k * 0.6), (hx + 5, 0), (hx, 5 - k * 0.6)]))
    fillp(cc, spath([(-52, -16, 0), (-46, -25), (-42, -27, 0), (-39, -19), (-36, -16, 0)]))      # nose, face up
    if arm > 0.01:
        hx, hy = -18 + 6 * arm + w, -14 - 24 * arm
        anim.limb(cc, (-14, -10), 6, (hx, hy), 5)
        if Pen.mode != "anchor":
            cc.drawCircle(hx, hy - 3, 6.5, anim.ink())
        anim.anchor(cc, "barm", mix(-14, hx, 0.45), mix(-10, hy, 0.45))
    else:
        anim.anchor(cc, "barm", -10, -16)
    anim.anchor(cc, "bhead", -44, -4)
    cc.restore()
    cc.restore()


def moon_phase(c, x, y, r, f, waxing=True, a=1.0):
    """The moon with lit fraction f (0 new .. 1 full); waxing = lit on the right."""
    f = clamp(f)
    S.glow(c, x, y, r * 6, (150, 180, 230), 90 * a * (0.2 + 0.8 * f))
    disc = skia.Path()
    disc.addCircle(x, y, r)
    if f < 0.985:
        sh = skia.Path()
        sh.addCircle(x + (-2 if waxing else 2) * r * f, y, r * 1.03)
        disc = skia.Op(disc, sh, skia.PathOp.kDifference_PathOp)
    p = skia.Paint(AntiAlias=True)
    p.setShader(skia.GradientShader.MakeRadial(skia.Point(x, y), r, [C(250, 244, 222, 255 * a), C(250, 244, 222, 255 * a),
                                                                       C(225, 222, 216, 255 * a)], [0.0, 0.85, 1.0]))
    c.drawPath(disc, p)


class Fall:
    """Things falling past a window: 'leaf', 'snow' or 'petal'."""

    def __init__(self, n, seed, x0, x1, y0, y1):
        rnd = random.Random(seed)
        self.p = [(rnd.uniform(x0, x1), rnd.uniform(0, 1), rnd.uniform(0.6, 1.4), rnd.uniform(0, 6.3)) for _ in range(n)]
        self.y0, self.y1 = y0, y1

    def draw(self, c, t, kind, a=1.0, speed=70.0):
        if a <= 0.01:
            return
        span = self.y1 - self.y0
        for (x, u, sz, ph) in self.p:
            y = self.y0 + (u * span + t * speed * (0.6 + 0.4 * sz)) % span
            xx = x + 26 * math.sin(t * 1.2 + ph) + (14 * t if kind != "snow" else 6 * t) % 60
            if kind == "snow":
                c.drawCircle(xx, y, 2.6 * sz, paint(C(240, 244, 255, 210 * a)))
            else:
                col = C(*((40, 24, 22) if kind == "leaf" else (255, 196, 214)), (230 if kind == "leaf" else 220) * a)
                c.save()
                c.translate(xx, y)
                c.rotate(t * 90 * sz + ph * 57)
                k = 8 * sz if kind == "leaf" else 5.5 * sz
                c.drawPath(spath([(-k, 0), (0, -k * 0.45), (k, 0), (0, k * 0.45)]), paint(col))
                c.restore()


class Coins:
    """Gold showered over the bride and groom."""

    def __init__(self, n, seed, x0, x1):
        rnd = random.Random(seed)
        self.k = [(rnd.uniform(x0, x1), rnd.uniform(0, 1), rnd.uniform(0.7, 1.3), rnd.uniform(0, 6.3),
                   rnd.uniform(-30, 30)) for _ in range(n)]

    def draw(self, c, t, a, y0=180, y1=900, speed=230.0):
        if a <= 0.01:
            return
        span = y1 - y0
        for (x, u, sz, ph, dx) in self.k:
            y = y0 + (u * span + t * speed * sz) % span
            fade = clamp((y - y0) / 60) * clamp((y1 - y) / 90)
            xx = x + dx * math.sin(t * 1.7 + ph)
            flip = 0.15 + 0.85 * abs(math.sin(t * 5.5 * sz + ph))
            r = 6.5 * sz
            c.drawOval(skia.Rect.MakeXYWH(xx - r * flip, y - r, 2 * r * flip, 2 * r), paint(C(255, 210, 110, 235 * a * fade)))
            if flip > 0.93:
                S.glow(c, xx, y, 26 * sz, (255, 230, 160), 160 * a * fade)


def lamp_row(c, t, xs, y, lit, s=1.0, chain=150):
    """Hanging lamps; lit[k] (0..1) lights lamp k (an unlit lamp is only its silhouette)."""
    pt = paint(C(*INK))
    for k, (x, u) in enumerate(zip(xs, lit)):
        if u > 0.02:
            c.save()
            c.saveLayerAlpha(None, int(255 * clamp(u)))
            S.hanging_lamp(c, x, y, s, t, chain, k * 1.7)
            c.restore()
            c.restore()
        if u < 0.98:
            c.save()
            c.translate(x, y)
            c.rotate(0.9 * math.sin(t * 0.9 + k * 1.7))
            c.drawRect(skia.Rect.MakeLTRB(-1.5, -chain, 1.5, 0), pt)
            c.scale(s, s)
            c.drawPath(spath([(-26, 0, 0), (-30, 18), (-18, 40), (0, 46), (18, 40), (30, 18), (26, 0, 0)]), pt)
            c.restore()


# ------------------------------------------------------------------ sets
def dawn_window(an, c, t, cam, x, yb, w, h, dawn, key="dw", sun=0.0, k=0.5, cover=0.0):
    """A dark room with a tall arched window: the sky before sunrise (dawn 0 = night .. 1 = sunrise).
    sun (0..1) lifts the sun over the far rooftops; cover (0..1) dims it behind a cloud."""
    S.lin(c, 0, H, [(0, (14, 10, 22)), (0.5, mixc((24, 18, 34), (48, 30, 38), dawn)), (1, (6, 4, 8))])
    arch = S.arch_path(x, yb, w, h)
    with cam(k):
        c.save()
        c.clipPath(arch, skia.ClipOp.kIntersect, True)
        S.lin(c, yb - h, yb, [(0, mixc((10, 14, 40), (70, 80, 140), dawn)), (0.55, mixc((34, 44, 92), (200, 136, 150), dawn)),
                              (1, mixc((70, 76, 120), (255, 198, 140), dawn))], (x - w, yb - h - 40, x + w, yb + 10))
        get(an, key + "st", lambda: S.Stars(110, 900, 47)).draw(c, t, clamp(1 - dawn * 1.4), 900)
        if dawn < 0.9:
            c.saveLayerAlpha(None, int(255 * clamp(1 - dawn * 1.1)))
            S.moon(c, x - w * 0.2, yb - h * 0.6 + 90 * dawn, w * 0.085)
            c.restore()
        S.glow(c, x + w * 0.12, yb - 40, w * 1.3, (255, 186, 120), 170 * dawn * (1 - 0.5 * cover))
        if sun > 0:
            S.sun(c, x + w * 0.12, yb - 40 - 170 * sun, w * 0.1, (255, 246, 214), (255, 190, 120), w * 1.1,
                  150 * (1 - 0.7 * cover))
        get(an, key + "cl", lambda: S.Clouds([(yb - h * 0.42, 12), (yb - h * 0.3, 8), (yb - h * 0.62, 10)], 49, 200, 460)).draw(
            c, t * 2, mixc((22, 26, 54), (150, 90, 110), dawn), 170)
        if cover > 0:
            S.radial(c, x + w * 0.12, yb - 40 - 170 * sun, w * 0.6,
                     [(0, (60, 34, 50, 230 * cover)), (0.7, (60, 34, 50, 200 * cover)), (1, (60, 34, 50, 0))])
        img, _ = get(an, key + "city", lambda: S.city(900, 400, 380, 48, (8, 8, 16), False, None))
        c.drawImage(img, x - w * 0.9, yb - 330)
        c.restore()
        edge = skia.Paint(AntiAlias=True, Color=C(*INK))
        edge.setStyle(skia.Paint.kStroke_Style)
        edge.setStrokeWidth(24)
        c.drawPath(arch, edge)
        pt = paint(C(*INK))
        c.drawRect(skia.Rect.MakeLTRB(x - 4, yb - h + 20, x + 4, yb), pt)
        c.drawRect(skia.Rect.MakeLTRB(x - w / 2, yb - h * 0.45 - 4, x + w / 2, yb - h * 0.45 + 4), pt)
        c.drawRect(skia.Rect.MakeLTRB(x - w / 2 - 40, yb, x + w / 2 + 40, yb + 26), pt)
    p = skia.Paint(AntiAlias=True)
    p.setShader(skia.GradientShader.MakeLinear([skia.Point(x, yb - h), skia.Point(x - w * 0.3, yb + 600)],
                                               [C(255, 200, 160, 60 * dawn), C(255, 200, 160, 0)]))
    c.drawPath(ppath([(x - w / 2, yb - h * 0.7), (x + w / 2, yb - h * 0.5), (x + w * 1.2, yb + 700),
                      (x - w * 1.2, yb + 700)]), p)


def months_window(an, c, t, cam, x, yb, w, h, lt, key="mw"):
    """Night window while the months pass: the moon runs through its phases, autumn leaves, snow, blossom."""
    S.lin(c, 0, H, [(0, (10, 10, 22)), (0.5, (22, 22, 40)), (1, (5, 4, 8))])
    arch = S.arch_path(x, yb, w, h)
    au = sstep(5.6, 7.0, lt) * (1 - sstep(10.4, 11.4, lt))          # autumn
    wi = sstep(10.4, 11.4, lt) * (1 - sstep(14.8, 15.8, lt))        # winter
    sp = sstep(14.8, 15.8, lt)                                      # spring
    with cam(0.5):
        c.save()
        c.clipPath(arch, skia.ClipOp.kIntersect, True)
        top = mixc(mixc(mixc((10, 14, 40), (16, 14, 36), au), (20, 26, 50), wi), (14, 20, 46), sp)
        low = mixc(mixc(mixc((70, 76, 120), (96, 70, 90), au), (120, 130, 160), wi), (90, 90, 130), sp)
        S.lin(c, yb - h, yb, [(0, top), (0.6, mixc(top, low, 0.6)), (1, low)], (x - w, yb - h - 40, x + w, yb + 10))
        get(an, key + "st", lambda: S.Stars(90, 900, 53)).draw(c, t, 0.9, 900)
        # the moon waxes and wanes, faster and faster once the months start passing
        cyc = lt / 30.0 if lt < 6.0 else 0.2 + (lt - 6.0) / 2.6
        ph = cyc % 1.0
        f = 1 - abs(ph - 0.5) * 2
        moon_phase(c, x + w * 0.14, yb - h * 0.64, w * 0.14, f, ph < 0.5)
        get(an, key + "cl", lambda: S.Clouds([(yb - h * 0.35, 10), (yb - h * 0.25, 7)], 55, 200, 420)).draw(
            c, t * 2, (20, 24, 50), 170)
        img, _ = get(an, key + "city", lambda: S.city(900, 400, 380, 56, (8, 8, 16), False, None))
        c.drawImage(img, x - w * 0.9, yb - 330)
        if wi > 0.01:      # snow on the roofs
            S.lin(c, yb - 200, yb, [(0, (220, 230, 255, 0)), (1, (220, 230, 255, 40 * wi))], (x - w, yb - 200, x + w, yb))
        fall = get(an, key + "fall", lambda: Fall(46, 57, x - w / 2 - 40, x + w / 2 + 40, yb - h, yb))
        fall.draw(c, t, "leaf", au, 60)
        fall.draw(c, t + 3.0, "snow", wi, 45)
        fall.draw(c, t + 7.0, "petal", sp, 40)
        c.restore()
        edge = skia.Paint(AntiAlias=True, Color=C(*INK))
        edge.setStyle(skia.Paint.kStroke_Style)
        edge.setStrokeWidth(26)
        c.drawPath(arch, edge)
        pt = paint(C(*INK))
        c.drawRect(skia.Rect.MakeLTRB(x - 4, yb - h + 20, x + 4, yb), pt)
        c.drawRect(skia.Rect.MakeLTRB(x - w / 2, yb - h * 0.45 - 4, x + w / 2, yb - h * 0.45 + 4), pt)
        c.drawRect(skia.Rect.MakeLTRB(x - w / 2 - 40, yb, x + w / 2 + 40, yb + 26), pt)
    p = skia.Paint(AntiAlias=True)
    p.setShader(skia.GradientShader.MakeLinear([skia.Point(x, yb - h), skia.Point(x - w * 1.4, yb + 500)],
                                               [C(150, 170, 230, 64), C(150, 170, 230, 0)]))
    c.drawPath(ppath([(x - w / 2, yb - h * 0.7), (x + w / 2, yb - h * 0.5), (x + w * 0.1, yb + 700),
                      (x - w * 1.6, yb + 700)]), p)


def cypress(c, x, y, h, t, seed=0.0):
    """A garden cypress (plain silhouette), swaying a little."""
    sw = 4 * math.sin(t * 0.8 + seed)
    w = h * 0.16
    c.drawPath(spath([(x - 6, y, 0), (x - w, y - h * 0.18), (x - w * 0.95, y - h * 0.5), (x - w * 0.6 + sw * 0.5, y - h * 0.8),
                      (x + sw, y - h, 0), (x + w * 0.6 + sw * 0.5, y - h * 0.8), (x + w * 0.95, y - h * 0.5),
                      (x + w, y - h * 0.18), (x + 6, y, 0)]), paint(C(*INK)))


def courtyard(an, c, t, cam, key="cy"):
    """The palace courtyard of Samangan in the morning: the great dome behind a low wall, cypresses, warm ground."""
    S.lin(c, 0, 900, [(0, (92, 120, 170)), (0.5, (190, 176, 170)), (0.85, (248, 206, 150)), (1, (252, 222, 170))])
    with cam(0.2):
        S.sun(c, 880, 520, 60, (255, 248, 222), (255, 214, 150), 520, 150)
        get(an, key + "cl", lambda: S.Clouds([(250, 14), (330, 10), (420, 16)], 61, 300, 600)).draw(c, t, (150, 120, 140), 150)
    with cam(0.4):
        c.save()
        c.translate(140, 170)
        c.scale(0.75, 0.75)
        palace(c, 560, 880, t, 0.15)
        c.restore()
    with cam(0.7):
        pt = paint(C(*INK))
        c.drawRect(skia.Rect.MakeLTRB(-300, 742, 1400, 870), pt)
        for k in range(40):
            c.drawRect(skia.Rect.MakeLTRB(-300 + k * 46, 724, -300 + k * 46 + 26, 742), pt)
        for x in (60, 1010):
            cypress(c, x, 760, 430, t, x * 0.01)
        S.lin(c, 600, 742, [(0, (255, 220, 170, 0)), (1, (255, 220, 170, 40))], (-300, 600, 1400, 742))
    with cam(1.0):
        ground(c, 866, (120, 84, 60), (30, 20, 16))


def birth_room(an, c, t, cam, lamp=1.0):
    """The candle-lit room where Sohrab is born: a warm curtain behind the bed, two tall candles."""
    with cam(0.7):
        S.lin(c, 0, H, [(0, (16, 10, 18)), (0.45, (40, 22, 30)), (1, (6, 3, 5))])
        wall_panel(c, 260, 1200, 300, 1080, (92, 46, 42), (156, 90, 66), 84)
        S.hanging_lamp(c, 640, 210, 1.2, t, 100, 2.5)
        S.glow(c, 640, 700, 640, (255, 160, 80), 50 * lamp)


# ================================================================== part 7 shots
def two_jewel(an, c, t, lt, dur, PR, PT, gem_name, dawn, zk=0.06, gem_a=1.0, gdx=0.0, gdy=0.0):
    """Two-shot at the window before sunrise: Rostam (left) and Tahmineh (right); the jewel between them."""
    focus = (540, 680)
    zoom = 1.0 + zk * ease(lt / max(dur, 0.1))
    cam = Cam(c, focus, zoom)
    dawn_window(an, c, t, cam, 540, 1010, 400, 720, dawn, "dw1", k=0.6)

    def figs(cc):
        with Cam(cc, focus, zoom)(1.0):
            tag("r:")
            person(cc, 250, 1330, 1.6, 1, PR, t, "rostam_robe")
            tag("t:")
            person(cc, 830, 1330, 1.5, -1, PT, t, TAHM)
            tag("")
    an.figures(c, figs, mixc(WARM, DAWN, dawn), (0, 150, 1080, 1500), anchors=True)
    if gem_name:
        gem_at(c, gem_name, t, 11 * zoom, gem_a, gdx, gdy)
    vig(an, c, 170)


def p7_s01(an, c, t):
    """Hook + title: before sunrise, Rostam holds out the jewel: 'If it is a son...'"""
    lt = t - an.start["S01"]
    dur = an.end["TITLE"] - an.start["S01"]
    a, b = LN("p07", "S01", 0)
    offer = sstep(0.0, 0.9, lt)
    reach = sstep(a + 1.6, a + 2.8, lt)
    PR = {"jaw": jaw(an, "ROSTAM", t, 7), "hand": (mix(80, 150, offer), mix(-300, -392, offer)), "hand_kind": "open",
          "rhand": (-30, -262), "head": 7 + 1.5 * math.sin(t * 0.7), "lean": 3 * offer}
    PT = {"hand": (mix(40, 108, reach), mix(-270, -372, reach)), "hand_kind": "open", "head": 4 + 6 * reach,
          "rhand": (-30, -262), "wind": 0.3, "lean": 2 * reach}
    two_jewel(an, c, t, lt, dur, PR, PT, "r:hand", 0.32 + 0.06 * ease(lt / dur), gdx=16, gdy=-14)


def p7_s02(an, c, t):
    """Samangan under the moon; then the king's room: the mobed has woken him with Rostam's message."""
    lt, dur = loc(an, "S02", t)
    n1 = LN("p07", "S02", 1)[0]
    k0, k1 = LN("p07", "S02", 3)

    def city():
        focus = (560, 650)
        zoom = 1 + 0.2 * ease(lt / (n1 + 0.8))
        city_night(an, c, t, Cam(c, focus, zoom), "c72", 0.0)
        get(an, "mo72", lambda: S.Motes(40, 72, 300, 900)).draw(c, t, (200, 210, 255), 70, rise=2, drift=0.2)
        vig(an, c, 160)

    def room():
        u = lt - n1
        focus = (700, 640)
        zoom = 1.0 + 0.1 * ease(u / (dur - n1))
        cam = Cam(c, focus, zoom)
        king_room(an, c, t, cam)
        wonder = sstep(k0 + 0.1, k0 + 0.8, lt)
        bow = sstep(n1 + 0.4, n1 + 1.4, lt) * (1 - sstep(k0 - 1.0, k0, lt))
        turn = sstep(n1 + 3.0, n1 + 4.0, lt)
        PK = {"jaw": jaw(an, "KING_SAMANGAN", t, 7), "head": 6 - 4 * turn - 8 * wonder + 1.2 * math.sin(t * 0.6),
              "hand": (mix(50, 124, wonder), mix(-280, -430, wonder)), "hand_kind": "open" if wonder > 0.3 else "fist",
              "rhand": (mix(-20, 30, wonder), mix(-260, -420, wonder)), "rhand_kind": "open" if wonder > 0.3 else "fist",
              "lean": -6 * wonder}
        PM = {"hand_kind": "lamp", "hand": (110, -360), "rprop": "staff", "rhand": (-10, -300),
              "head": 12 * bow + 2, "lean": 14 * bow + 4}

        def figs(cc):
            with Cam(cc, focus, zoom)(1.0):
                in_bed(cc, t, 830, 782, 0.9, 0, PK, "king")
                bed(cc, 640, 1080, 786, 866, "right")
                blanket(cc, 836, 670, 786, 0.9, 0.5)
                tag("mo:")
                person(cc, 380, 866, 0.86, 1, PM, t, "mobed")
                tag("")
        an.figures(c, figs, WARM, (0, 200, 1080, 1000), anchors=True)
        candle_light(c, an, "mo:flame", t, 520, 110, 5.0, 0.26)
        vig(an, c, 170)
    dissolve(c, lt, n1 - 0.6, 0.8, city, room)


ARCADE = (180, 470, 760, 1050)


def p7_s03(an, c, t):
    """The king rises like a cypress and gives his orders; the lamps of the palace are lit one by one."""
    lt, dur = loc(an, "S03", t)
    c0, c1 = LN("p07", "S03", 1)
    w0, w1 = LN("p07", "S03", 2)
    focus = (420, 640)
    zoom = 1.0 + 0.05 * ease(lt / dur)
    cam = Cam(c, focus, zoom)
    lit = [sstep(c0 + 0.9 + 0.7 * k, c0 + 1.3 + 0.7 * k, lt) for k in range(4)]
    with cam(0.6):
        S.lin(c, 0, H, [(0, (8, 12, 26)), (0.5, (20, 26, 48)), (1, (4, 4, 8))])
        pt = paint(C(*INK))
        for k, x in enumerate(ARCADE):
            c.drawPath(S.arch_path(x, 900, 210, 560), paint(C(50, 66, 112)))
            p = skia.Paint(AntiAlias=True)
            p.setShader(skia.GradientShader.MakeLinear([skia.Point(0, 640), skia.Point(0, 900)],
                                                       [C(120, 140, 200, 60), C(120, 140, 200, 0)]))
            c.drawPath(ppath([(x - 105, 640), (x + 105, 640), (x + 200, 900), (x + 10, 900)]), p)
            c.drawRect(skia.Rect.MakeLTRB(x + 145 - 40, 180, x + 145 + 40, 920), pt)
        c.drawRect(skia.Rect.MakeLTRB(-200, 120, 1300, 220), pt)
        for k, u in enumerate(lit):
            if u > 0:
                S.glow(c, ARCADE[k], 600, 420, (255, 170, 80), 80 * u)
        lamp_row(c, t, list(ARCADE), 420, lit, 1.0, 200)
    with cam(0.85):
        ground(c, 900, (30, 22, 30))
    rise = sstep(0.0, 2.4, lt)
    point = sstep(c0, c0 + 0.6, lt) * (1 - sstep(c1 + 0.2, c1 + 0.9, lt))
    joy = sstep(w0 + 1.6, w0 + 2.2, lt)
    if point > 0.01:
        hand, rhand = (mix(40, 190, point), mix(-262, -430, point)), (-30, -262)
    else:
        hand, rhand = (mix(40, 90, joy), mix(-262, -520, joy)), (mix(-30, -60, joy), mix(-262, -500, joy))
    PK = {"jaw": jaw(an, "KING_SAMANGAN", t, 7), "hand": hand, "hand_kind": "open" if max(point, joy) > 0.3 else "fist",
          "rhand": rhand, "rhand_kind": "open" if joy > 0.3 else "fist",
          "head": mix(14, -4, rise) - 3 * joy + 1.2 * math.sin(t * 0.6), "lean": mix(16, 0, rise), "wind": 0.5}
    run = [clamp((lt - c0 - 1.0 - 0.8 * k) / 3.6) for k in range(2)]

    def figs(cc):
        with Cam(cc, focus, zoom)(0.75):
            for k, u in enumerate(run):
                if 0 < u < 1:
                    tag(f"sv{k}:")
                    person(cc, mix(1150, 560, u), 900, 0.42, -1, {"mode": "walk", "phase": lt * 6 + k, "stride": 26,
                                                                 "lean": 8, "hand_kind": "lamp", "hand": (110, -360)},
                           t, "guard" if k == 0 else "maid")
            tag("")
        with Cam(cc, focus, zoom)(1.0):
            person(cc, 330, 1560 + 260 * (1 - ease(rise)), 1.85, 1, PK, t, "king")
    an.figures(c, figs, WARM, (0, 100, 1080, 1700), anchors=True)
    for k, u in enumerate(run):
        if 0 < u < 1:
            candle_light(c, an, f"sv{k}:flame", t, 160, 90, k, 0.12)
    vig(an, c, 170)


def p7_s04(an, c, t):
    """The wedding in the hall: the king leads Tahmineh to Rostam; gold is showered; a noble's toast."""
    lt, dur = loc(an, "S04", t)
    k0, k1 = LN("p07", "S04", 1)
    r0, r1 = LN("p07", "S04", 2)
    g0, g1 = LN("p07", "S04", 3)
    n0, n1 = LN("p07", "S04", 4)
    focus = (540, 640)
    zoom = 1.0 + 0.06 * ease(lt / dur)
    cam = Cam(c, focus, zoom)
    with cam(0.6):
        hall(an, c, t)
        for k, x in enumerate((260, 540, 820)):
            S.hanging_lamp(c, x, 300, 1.0, t, 160, k)
    with cam(0.9):
        ground(c, 866, (40, 18, 12))
        S.glow(c, 540, 870, 500, (255, 160, 80), 60)
    walk = clamp(lt / 4.6)
    wk = ease(walk)
    take_ = sstep(LN("p07", "S04", 2)[0] + 1.8, LN("p07", "S04", 2)[0] + 2.8, lt)
    tx = mix(940, 610, wk) - 70 * take_
    kx = mix(1140, 810, wk)
    give = sstep(k0 + 0.3, k0 + 1.0, lt) * (1 - sstep(k1, k1 + 0.6, lt))
    honour = sstep(r0, r0 + 0.5, lt) * (1 - sstep(r0 + 1.6, r0 + 2.2, lt))
    take = sstep(r0 + 1.8, r0 + 2.8, lt)
    cups = sstep(g0 + 1.0, g0 + 1.8, lt)
    toast = sstep(n0 - 0.2, n0 + 0.4, lt)
    PT = {"mode": "walk" if 0 < walk < 1 else "stand", "phase": lt * 3.4, "stride": 13, "wind": 0.3,
          "hand": (mix(40, 120, take), mix(-270, -350, take)), "hand_kind": "open",
          "rhand": (mix(-90, -30, sstep(4.2, 5.0, lt)), mix(-330, -262, sstep(4.2, 5.0, lt))), "rhand_kind": "open",
          "head": 3 + 3 * take}
    PK = {"mode": "walk" if 0 < walk < 1 else "stand", "phase": lt * 3.4 + 1.0, "stride": 13,
          "jaw": jaw(an, "KING_SAMANGAN", t, 7),
          "hand": (mix(mix(90, 60, sstep(4.2, 5.0, lt)), 170, give), mix(-330, -420, give)), "hand_kind": "open",
          "rhand": (-30, -262), "head": 2 - 4 * give + 1.2 * math.sin(t * 0.6)}
    if honour > 0.01:
        rh, rk = (mix(60, 30, honour), mix(-300, -380, honour)), "open"
    else:
        rh, rk = (mix(60, 150, take), mix(-300, -350, take)), "open" if take > 0.3 else "fist"
    PR = {"jaw": jaw(an, "ROSTAM", t, 6), "hand": rh, "hand_kind": rk, "rhand": (-30, -262),
          "head": 4 + 4 * honour + 1.2 * math.sin(t * 0.7), "lean": 4 * honour}
    nobles = [(70, 1), (160, 1), (985, -1), (1070, -1)]

    def figs(cc):
        with Cam(cc, focus, zoom)(0.8):
            for i, (x, f) in enumerate(nobles):
                up = cups if i != 3 else max(cups, toast)
                person(cc, x, 820, 0.5, f, {"hand_kind": "cup", "hand": (mix(80, 110, up), mix(-300, -470, up)),
                                            "jaw": jaw(an, "NOBLE", t, 9) if i == 3 else 0.0, "seed": i,
                                            "head": 2 - 4 * up}, t, "noble")
        with Cam(cc, focus, zoom)(1.0):
            person(cc, 270, 866, 0.95, 1, PR, t, "rostam_robe")
            person(cc, tx, 866, 0.88, -1, PT, t, TAHM)
            person(cc, kx, 866, 0.9, -1, PK, t, "king")
    an.figures(c, figs, (255, 196, 120), (0, 200, 1080, 1000))
    with cam(1.0):
        get(an, "coins74", lambda: Coins(46, 74, 200, 760)).draw(c, t, sstep(g0, g0 + 1.2, lt) * (1 - sstep(dur - 1.0, dur, lt)))
    vig(an, c, 150)


SH_B = (0, 260, W, 1000)


def p7_s05(an, c, t):
    """All night they talk by a candle; his stories fall as shadows on the curtain (Zabol, Zal; the king's wars)."""
    lt, dur = loc(an, "S05", t)
    z0, z1 = LN("p07", "S05", 2)
    w0, w1 = LN("p07", "S05", 3)
    s0, s1 = LN("p07", "S05", 4)
    m0, m1 = LN("p07", "S05", 5)
    focus = (540, 700)
    zoom = 1.0 + 0.06 * ease(lt / dur)
    cam = Cam(c, focus, zoom)
    fl = 0.9 + 0.07 * math.sin(t * 8) + 0.04 * math.sin(t * 17)
    with cam(0.7):
        S.lin(c, 0, H, [(0, (16, 10, 22)), (0.45, (40, 24, 34)), (1, (6, 3, 5))])
        wall_panel(c, 120, 960, 300, 900, (110, 60, 46), (180, 112, 76), 90)
        S.glow(c, 540, 760, 620, (255, 180, 100), 110 * fl)
        # stories cast by the candle on the curtain
        v1 = sstep(z0 + 0.2, z0 + 1.0, lt) * (1 - sstep(z1 + 0.1, z1 + 0.7, lt))
        v2 = sstep(w0 + 0.1, w0 + 0.8, lt) * (1 - sstep(w1 + 0.3, w1 + 1.0, lt))
        if v1 > 0.01:
            shadow_layer(c, SH_B, 0.8 * v1, (60, 26, 16), 2.4)
            c.drawPath(spath([(140, 800, 0), (230, 600), (300, 520), (360, 590), (440, 460), (520, 380, 0), (600, 470),
                              (680, 550), (760, 500), (860, 610), (950, 800, 0)]), Pen.FILL)
            person(c, 640, 800, 0.56, -1, {"hand_kind": "staff", "hand": (60, -300), "rhand": (-24, -262), "lean": 4,
                                           "head": 6, "wind": 0.6}, t, "mobed")
            c.restore()
        if v2 > 0.01:
            u = lt - w0
            shadow_layer(c, SH_B, 0.8 * v2, (60, 26, 16), 2.4)
            fillp(c, spath([(372, 760, 0), (372, 560), (386, 548), (400, 560), (400, 700), (480, 700), (486, 760, 0)]))
            person(c, 420, 760, 0.5, 1, {"mode": "sit", "hand": (mix(60, 150, sstep(0.4, 1.0, u)), mix(-300, -420, sstep(0.4, 1.0, u))),
                                         "hand_kind": "open", "head": -2}, t, "kavus")
            for i in range(3):
                horse(c, mix(560, 900, clamp(u / 4.0)) + i * 90, 760 - i * 8, 0.3, 1,
                      {"gait": "gallop", "phase": t * 1.9 + i * 0.3, "saddle": True, "rider": "warrior_ir",
                       "rider_pose": {"hand_kind": "spear", "hand": (110, -340), "lean": 8}}, t)
            c.restore()
    with cam(1.0):
        ground(c, 1000, (36, 20, 22))
    ask = sstep(LN("p07", "S05", 1)[0], LN("p07", "S05", 1)[0] + 0.6, lt) * (1 - sstep(LN("p07", "S05", 1)[1], LN("p07", "S05", 1)[1] + 0.6, lt))
    point = sstep(z0 + 0.3, z0 + 1.0, lt) * (1 - sstep(w1, w1 + 0.7, lt))
    sad = sstep(s0, s0 + 0.6, lt)
    must = sstep(m0, m0 + 0.6, lt)
    PR = {"mode": "sit", "jaw": jaw(an, "ROSTAM", t, 7), "hand": (mix(mix(120, 200, point), 110, must), mix(mix(-300, -460, point), -330, must)),
          "hand_kind": "open", "rhand": (-30, -262), "head": 2 - 6 * point + 6 * must + 1.2 * math.sin(t * 0.6), "lean": 3 * must}
    PT = {"mode": "sit", "jaw": jaw(an, "TAHMINEH", t, 6), "hand": (mix(100, 150, ask), mix(-300, -380, ask)), "hand_kind": "open",
          "rhand": (-30, -262), "head": 3 + 10 * sad + 1.2 * math.sin(t * 0.8), "lean": 4 * sad, "wind": 0.3}

    def figs(cc):
        with Cam(cc, focus, zoom)(1.0):
            seated(cc, 210, 1010, 1.25, 1, PR, t, "rostam_robe")
            seated(cc, 870, 1010, 1.2, -1, PT, t, TAHM)
            fillp(cc, spath([(440, 1010, 0), (452, 960), (628, 960), (640, 1010, 0)]))
    an.figures(c, figs, WARM, (0, 200, 1080, 1200))
    with cam(1.0):
        standing_candle(c, 540, 962, t, 0.55, 2.0)
    get(an, "mo75", lambda: S.Motes(40, 75, 300, 1000)).draw(c, t, (255, 200, 140), 70, rise=4, drift=0.2)
    vig(an, c, 180)


def p7_s06(an, c, t):
    """Close: at the window before sunrise, Rostam unties the jewel from his arm and holds it to the light."""
    lt, dur = loc(an, "S06", t)
    f0, f1 = LN("p07", "S06", 1)
    k0, k1 = LN("p07", "S06", 2)
    focus = (520, 620)
    zoom = 1.0 + 0.07 * ease(lt / dur)
    cam = Cam(c, focus, zoom)
    dawn = 0.42 + 0.1 * ease(lt / dur)
    dawn_window(an, c, t, cam, 790, 1180, 520, 900, dawn, "dw6", k=0.6)
    untie = sstep(1.2, 2.6, lt)          # the rear hand goes to the armband
    free = sstep(3.0, 3.8, lt)           # the jewel comes away with it
    raise_ = sstep(f0, f0 + 1.2, lt) * (1 - sstep(k0, k0 + 0.6, lt))
    offer = sstep(k0, k0 + 0.8, lt)
    PR = {"jaw": jaw(an, "ROSTAM", t, 6), "head": 4 - 6 * raise_ + 1.2 * math.sin(t * 0.6),
          "hand": (mix(mix(70, 120, free), 170, max(raise_, offer)), mix(mix(-300, -340, free), mix(-470, -400, offer), max(raise_, offer))),
          "hand_kind": "open" if free > 0.5 else "fist",
          "rhand": (mix(mix(-30, 40, untie), 60, free), mix(mix(-262, -372, untie), -330, free)), "rhand_kind": "fist"}

    def figs(cc):
        with Cam(cc, focus, zoom)(1.0):
            tag("r:")
            person(cc, 330, 1640, 2.3, 1, PR, t, "rostam_robe")
            tag("")
    an.figures(c, figs, mixc(WARM, DAWN, 0.6), (0, 100, 1080, 1800), anchors=True)
    up, rh, hd = A("r:hand_up"), A("r:rhand"), A("r:hand")
    if up and rh and hd:
        if free < 0.5:
            p = up if untie < 0.9 else (mix(up[0], rh[0], free * 2), mix(up[1], rh[1], free * 2))
        else:
            p = (mix(rh[0], hd[0] + 30, (free - 0.5) * 2), mix(rh[1], hd[1] - 22, (free - 0.5) * 2))
        gem(c, p[0], p[1], 15 * zoom, t, 1.0, 1.0, 1.0 + 0.6 * raise_)
    vig(an, c, 170)


def p7_s06b(an, c, t):
    """Two-shot: a daughter, sew it into her hair; a son, tie it on his arm -- he lays it in her hands."""
    lt, dur = loc(an, "S06b", t)
    d0, d1 = LN("p07", "S06b", 0)
    s0, s1 = LN("p07", "S06b", 1)
    hair = sstep(d0 + 1.6, d0 + 2.4, lt) * (1 - sstep(d1 + 0.1, d1 + 0.6, lt))
    give = sstep(s0 + 2.2, s0 + 3.2, lt)
    reach = sstep(0.0, 1.0, lt)
    PR = {"jaw": jaw(an, "ROSTAM", t, 7), "hand": (mix(150, 176, give), mix(-392, -372, give)), "hand_kind": "open",
          "rhand": (-30, -262), "head": 7 - 4 * hair + 1.5 * math.sin(t * 0.7), "lean": 3 + 2 * give}
    PT = {"hand": (mix(mix(40, 108, reach), 70, hair), mix(mix(-270, -372, reach), -470, hair)), "hand_kind": "open",
          "head": 6 - 6 * hair + 4 * give, "rhand": (-30, -262), "wind": 0.3, "lean": 2}
    two_jewel(an, c, t, lt, dur, PR, PT, "r:hand", 0.4 + 0.05 * ease(lt / dur), 0.05, 1.0, 16, -14)


def p7_s07(an, c, t):
    """Rostam's words become a vision in the dawn sky: a tall young hero, an eagle brought down, the sun."""
    lt, dur = loc(an, "S07", t)
    e0, e1 = LN("p07", "S07", 1)
    u0, u1 = LN("p07", "S07", 2)
    h0, h1 = LN("p07", "S07", 3)
    focus = (600, 640)
    zoom = 1.0 + 0.08 * ease(lt / dur)
    cam = Cam(c, focus, zoom)
    sun = sstep(u0 - 0.5, u1 + 0.5, lt)
    dawn = 0.55 + 0.25 * sun
    dawn_window(an, c, t, cam, 640, 1200, 760, 1040, dawn, "dw7", 0.7 * sun, k=0.5)
    vis = sstep(0.3, 1.8, lt) * (1 - sstep(h0 - 0.2, h0 + 1.4, lt))
    if vis > 0.01:
        with cam(0.5):
            c.save()
            c.clipPath(S.arch_path(640, 1200, 760, 1040), skia.ClipOp.kIntersect, True)
            ghost_layer(c, (240, 160, 1040, 1200), 0.6 * vis, (255, 226, 170), 2.6)
            catch = sstep(e0 + 0.4, e1 + 0.3, lt)
            person(c, 660, 900, 0.95, -1, {"hand_kind": "open" if catch < 0.95 else "fist",
                                           "hand": (mix(60, 90, catch), mix(-300, -560, catch)), "rhand_kind": "spear",
                                           "rhand": (-10, -300), "head": -6 * catch, "wind": 1.0, "stance": (54, 44)}, t, "sohrab")
            if e0 - 0.5 < lt:
                u = clamp((lt - e0 + 0.5) / 2.6)
                eagle(c, mix(1000, 600, ease(u)), mix(250, 330, ease(u)) + 40 * math.sin(u * math.pi), 0.55, t, -1, 1.0, 7.0)
            c.restore()
            c.restore()
    heart = sstep(h0, h0 + 0.8, lt)
    P = {"jaw": jaw(an, "TAHMINEH", t, 6), "hand": (mix(80, 40, heart), mix(-350, -380, heart)), "hand_kind": "open",
         "rhand": (mix(-30, 20, heart), mix(-262, -360, heart)), "head": mix(-4, 8, heart) + 1.2 * math.sin(t * 0.7),
         "wind": 0.5, "lean": 2 * heart}

    def figs(cc):
        with Cam(cc, focus, zoom)(1.0):
            tag("t:")
            person(cc, 170, 1520, 2.0, 1, P, t, TAHM)
            tag("")
    an.figures(c, figs, mixc(MOON, DAWN, dawn), (0, 150, 1080, 1700), alpha=170, anchors=True)
    gem_at(c, "t:hand", t, 12 * zoom, 1.0, 14, -12, 2.0)
    vig(an, c, 180)


def p7_s08(an, c, t):
    """Turn + end: the jewel in Tahmineh's hands as the sun rises; a cloud darkens it -- 'the darkest day'."""
    lt = t - an.start["S08"]
    d0, d1 = LN("p07", "S08", 1)
    dur = an.end["END"] - an.start["S08"]
    focus = (560, 640)
    zoom = 1.02 + 0.1 * ease(lt / dur)
    cam = Cam(c, focus, zoom)
    sun = sstep(0.0, d0 + 2.0, lt)
    cover = sstep(d1 - 2.2, d1 + 0.6, lt)
    dawn_window(an, c, t, cam, 700, 1150, 640, 960, 0.75 + 0.2 * sun, "dw8", 0.4 + 0.5 * sun, k=0.5, cover=cover)
    P = {"hand": (66, -336), "hand_kind": "open", "rhand": (44, -322), "rhand_kind": "open",
         "head": 12 + 1.2 * math.sin(t * 0.6), "wind": 0.4, "lean": 4}

    def figs(cc):
        with Cam(cc, focus, zoom)(1.0):
            tag("t:")
            person(cc, 400, 1640, 2.25, 1, P, t, TAHM)
            tag("")
    an.figures(c, figs, mixc(DAWN, (170, 120, 140), cover), (0, 150, 1080, 1800), alpha=160 - 50 * cover, anchors=True)
    gem_at(c, "t:hand", t, 17 * zoom, 1.0, 22, -18, 0.0, 1.0 - 0.45 * cover)
    if cover > 0.01:
        S.lin(c, 0, H, [(0, (20, 6, 10, 0)), (1, (20, 6, 10, 90 * cover))])
    vig(an, c, 180 + 40 * cover)


P07 = {"S01": p7_s01, "TITLE": p7_s01, "S02": p7_s02, "S03": p7_s03, "S04": p7_s04, "S05": p7_s05, "S06": p7_s06,
       "S06b": p7_s06b, "S07": p7_s07, "S08": p7_s08, "END": p7_s08}
SHIFT7 = {}


# ================================================================== part 8 shots
def bed_mother(cc, t, P, hx=840, ytop=1046, s=1.45, ang=0.0, x0=560, x1=1130, knee=0.5):
    """Tahmineh in bed, sitting up (ang 0) or lying back (ang ~70), facing left; returns nothing."""
    tag("t:")
    in_bed(cc, t, hx, ytop - 4, s, ang, P, TAHM)
    tag("")
    bed(cc, x0, x1, ytop, ytop + 80 * max(1.0, s), "right")
    blanket(cc, hx + 6, x0 + 30, ytop, s, knee)


def birth_two(an, c, t, lt, dur, PM, mx, PT, ang, baby_on, arm=0.0, zk=0.05, zoom0=0.0, curtain=None):
    """Two-shot in the birth room: the maid (left) and Tahmineh in bed (right); the baby with one of them."""
    focus = (560, 700)
    zoom = 1.0 + zoom0 + zk * ease(lt / max(dur, 0.1))
    cam = Cam(c, focus, zoom)
    birth_room(an, c, t, cam)
    if curtain:
        with cam(0.7):
            curtain()

    def figs(cc):
        with Cam(cc, focus, zoom)(1.0):
            tag("m:")
            person(cc, mx, 1110, 1.02, 1, PM, t, "maid")
            tag("")
            bed_mother(cc, t, PT, 840, 1046, 1.45, ang)
        if baby_on == "maid":
            h, r = A("m:hand"), A("m:rhand")
            if h and r:
                tag("b:")
                baby(cc, (h[0] + r[0]) / 2 + 18 * zoom, (h[1] + r[1]) / 2 - 20 * zoom, 1.15 * zoom, t, 6, arm, -1)
                tag("")
        elif baby_on == "mother":
            h, r = A("t:hand"), A("t:rhand")
            if h and r:
                tag("b:")
                baby(cc, (h[0] + r[0]) / 2 - 10 * zoom, (h[1] + r[1]) / 2 - 20 * zoom, 1.15 * zoom, t, 4, arm, 1)
                tag("")
    an.figures(c, figs, WARM, (0, 150, 1080, 1400), anchors=True)
    with cam(1.0):
        standing_candle(c, 110, 1110, t, 0.9, 1.0, False)
    vig(an, c, 170)


def p8_s01(an, c, t):
    """Hook + title: the night of the birth -- the maid lifts the baby: 'A boy, my lady!'"""
    lt = t - an.start["S01"]
    dur = an.end["TITLE"] - an.start["S01"]
    g0, g1 = LN("p08", "S01", 1)
    lift = sstep(0.2, 1.2, lt)
    reach = sstep(g0, g0 + 0.8, lt)
    PM = {"jaw": jaw(an, "MAID", t, 7), "hand": (mix(110, 150, lift), mix(-340, -400, lift)), "hand_kind": "fist",
          "rhand": (mix(70, 92, lift), mix(-330, -392, lift)), "head": 4 - 8 * lift, "lean": -3 * lift, "wind": 0.3}
    PT = {"jaw": jaw(an, "TAHMINEH", t, 6), "hand": (mix(50, 150, reach), mix(-280, -420, reach)), "hand_kind": "open",
          "rhand": (-30, -262), "head": 6 - 6 * reach + 1.2 * math.sin(t * 0.7)}
    birth_two(an, c, t, lt, dur, PM, 330, PT, mix(28, 14, reach), "maid", sstep(0.8, 1.6, lt), 0.06)


def p8_s02(an, c, t):
    """Nine months earlier: Samangan at sunrise; then Rostam, armed for the road, says goodbye to Tahmineh."""
    lt, dur = loc(an, "S02", t)
    r0, r1 = LN("p08", "S02", 3)
    q0, q1 = LN("p08", "S02", 4)
    h0, h1 = LN("p08", "S02", 5)
    a0, a1 = LN("p08", "S02", 6)
    cut = r0 - 0.6

    def city():
        focus = (560, 640)
        zoom = 1.0 + 0.16 * ease(lt / cut)
        cam = Cam(c, focus, zoom)
        rise = ease(lt / cut)
        S.lin(c, 0, 900, [(0, mixc((20, 24, 60), (60, 70, 130), rise)), (0.5, mixc((90, 70, 110), (200, 130, 130), rise)),
                          (0.85, mixc((200, 120, 100), (255, 190, 130), rise)), (1, (255, 214, 160))])
        with cam(0.2):
            get(an, "st82", lambda: S.Stars(80, 500, 82)).draw(c, t, clamp(0.6 - rise), 500)
            S.sun(c, 820, 860 - 200 * rise, 70, (255, 246, 214), (255, 180, 110), 560, 170)
            get(an, "cl82", lambda: S.Clouds([(380, 12), (470, 9), (560, 14)], 83, 300, 600)).draw(c, t * 2, (120, 70, 90), 170)
        img, lights = get(an, "city82", lambda: S.city(1500, 900, 880, 24, INK, True, None))
        with cam(0.6):
            c.drawImage(img, -200, 0)
        with cam(1.0):
            palace(c, 560, 880, t, 0.6)
            ground(c, 880, (14, 8, 12))
            S.birds(c, t, get(an, "bd82", lambda: [(random.Random(k).uniform(0, 1400), random.Random(k + 5).uniform(300, 460),
                                                    40, random.Random(k + 2).uniform(6, 10), k) for k in range(8)]), (20, 10, 16))
        vig(an, c, 150)

    def room():
        u = lt - cut
        focus = (560, 700)
        zoom = 1.0 + 0.06 * ease(u / (dur - cut))
        cam = Cam(c, focus, zoom)
        dawn_window(an, c, t, cam, 560, 1060, 380, 720, 0.85, "dw82", 0.35, k=0.6)
        hold = sstep(h0, h0 + 1.2, lt)
        away = sstep(a0, a0 + 0.6, lt)
        go = clamp((lt - a0 - 0.4) / 2.6)
        rx = mix(310, 380, hold)
        tx = mix(780, 690, hold) if away < 0.5 else mix(690, 900, ease(go))
        PR = {"jaw": jaw(an, "ROSTAM", t, 6), "hand": (mix(mix(98, 150, sstep(r0, r0 + 0.6, lt) * (1 - sstep(r1, r1 + 0.5, lt))), 160, hold * (1 - away)),
                                                       mix(-300, -400, hold * (1 - away))),
              "hand_kind": "open" if hold > 0.3 and away < 0.5 else "fist", "mace": 0.0,
              "rprop": "mace", "rhand": (-30, -262), "head": 4 + 14 * hold * (1 - away) + 6 * away + 1.2 * math.sin(t * 0.6),
              "lean": 6 * hold * (1 - away), "stance": (50, 44), "wind": 0.4}
        PT = {"jaw": jaw(an, "TAHMINEH", t, 6), "mode": "walk" if 0 < go < 1 else "stand", "phase": lt * 3.2, "stride": 12,
              "hand": (mix(mix(60, 90, sstep(q0, q0 + 0.5, lt)), 50, away), mix(mix(-300, -390, sstep(q0, q0 + 0.5, lt) * (1 - hold)), -470, away)),
              "hand_kind": "open", "rhand": (-30, -262), "head": 4 - 8 * hold * (1 - away) + 16 * away, "lean": -4 * hold * (1 - away) + 6 * away,
              "wind": 0.35}

        def figs(cc):
            with Cam(cc, focus, zoom)(1.0):
                person(cc, rx, 1250, 1.35, 1, PR, t, "rostam")
                person(cc, tx, 1250, 1.3, 1 if away > 0.5 else -1, PT, t, TAHM)
        an.figures(c, figs, DAWN, (0, 150, 1080, 1400))
        vig(an, c, 170)
    dissolve(c, lt, cut, 0.8, city, room)


def p8_s03(an, c, t):
    """Morning in the courtyard: the king greets Rostam and brings good news -- Rakhsh is found."""
    lt, dur = loc(an, "S03", t)
    v0, v1 = LN("p08", "S03", 1)
    g0, g1 = LN("p08", "S03", 2)
    w0, w1 = LN("p08", "S03", 3)
    focus = (540, 640)
    zoom = 1.0 + 0.05 * ease(lt / dur)
    cam = Cam(c, focus, zoom)
    courtyard(an, c, t, cam)
    walk = clamp(lt / 2.6)
    kx = mix(1000, 740, ease(walk))
    greet = sstep(0.0, 0.8, lt) * (1 - sstep(2.6, 3.2, lt))
    news = sstep(g0 + 1.8, g0 + 2.4, lt)
    eager = sstep(w0, w0 + 0.5, lt)
    PK = {"mode": "walk" if 0 < walk < 1 else "stand", "phase": lt * 3.4, "stride": 14,
          "jaw": jaw(an, "KING_SAMANGAN", t, 7),
          "hand": (mix(mix(50, 130, greet), -120, news), mix(mix(-270, -400, greet), -430, news)), "hand_kind": "open",
          "rhand": (mix(-30, 60, greet), mix(-262, -380, greet)), "rhand_kind": "open" if greet > 0.3 else "fist",
          "head": 2 - 3 * greet + 1.2 * math.sin(t * 0.6)}
    PR = {"jaw": jaw(an, "ROSTAM", t, 6), "carry": "saddle", "hand_kind": "open" if eager > 0.3 else "fist",
          "hand": (mix(40, 150, eager), mix(-262, -400, eager)),
          "head": 3 - 6 * eager + 1.2 * math.sin(t * 0.7), "lean": 4 * eager + 3 * sstep(v0, v0 + 0.4, lt) * (1 - sstep(v1, v1 + 0.4, lt)),
          "stance": (52, 44), "wind": 0.4}

    def figs(cc):
        with Cam(cc, focus, zoom)(1.0):
            person(cc, mix(330, 380, eager), 866, 1.0, 1, PR, t, "rostam")
            person(cc, kx, 866, 0.92, -1, PK, t, "king")
            person(cc, kx + 190, 866, 0.85, -1, {"mode": "walk" if 0 < walk < 1 else "stand", "phase": lt * 3.4 + 0.8,
                                                 "stride": 14, "rprop": "spear", "rhand": (-10, -300), "hand": (40, -262),
                                                 "head": 2}, t, "guard")
    an.figures(c, figs, DAY, (0, 200, 1080, 1000))
    vig(an, c, 140)


SADDLE = [(-60, 8), (-50, -16), (-34, -22, 0), (-18, -8), (20, -8), (38, -22, 0), (50, -14), (58, 8), (34, 20), (-46, 20)]


def p8_s04(an, c, t):
    """Rakhsh is led in; Rostam runs to him and strokes his neck, then swings the saddle onto his back."""
    lt, dur = loc(an, "S04", t)
    o0, o1 = LN("p08", "S04", 1)
    s0, s1 = LN("p08", "S04", 2)
    focus = (600, 660)
    zoom = 1.0 + 0.05 * ease(lt / dur)
    cam = Cam(c, focus, zoom)
    courtyard(an, c, t, cam)
    led = clamp(lt / 3.6)
    hx = mix(1240, 870, ease(led))
    run = clamp((lt - 0.8) / 2.4)
    rx = mix(170, 520, ease(run))
    stroke = sstep(3.2, 3.8, lt) * (1 - sstep(s0 + 0.2, s0 + 0.8, lt))
    lift = sstep(s0 + 0.6, s0 + 1.3, lt)
    toss = clamp((lt - s0 - 1.5) / 0.7)
    on = toss >= 1
    thank = sstep(s0 + 2.6, s0 + 3.2, lt)
    nuzzle = sstep(o0, o0 + 0.8, lt) * (1 - sstep(o1 + 0.2, o1 + 1.0, lt))
    if lift > 0.01 and not on:
        swing = sstep(s0 + 1.4, s0 + 1.9, lt)
        hand, rhand = (mix(100, 160, swing), mix(-440, -500, swing)), (mix(60, 130, swing), mix(-430, -490, swing))
    else:
        hand = (mix(40, 150, stroke) + 10 * math.sin(t * 3) * stroke, mix(-262, -345, stroke))
        rhand = (-30, -262)
    PR = {"mode": "walk" if 0 < run < 1 else "stand", "phase": lt * 5.5, "stride": 24, "jaw": jaw(an, "ROSTAM", t, 6),
          "hand": hand, "hand_kind": "open", "rhand": rhand, "rhand_kind": "open",
          "carry": "saddle" if lift < 0.5 else None,
          "head": 2 - 4 * stroke + 12 * thank + 1.2 * math.sin(t * 0.7),
          "lean": 8 * (0 < run < 1) + 4 * stroke + 9 * thank, "stance": (50, 44), "wind": 0.5}
    PH = {"gait": "walk" if 0 < led < 1 else "stand", "phase": t * 0.8, "saddle": on,
          "neck": 10 * math.sin(t * 2.3) * (1 - nuzzle) + 22 * nuzzle, "head": 8 * nuzzle + 5 * math.sin(t * 1.7), "tail": 6}

    def horse_fig(cc):
        with Cam(cc, focus, zoom)(1.0):
            horse(cc, hx, 870, 0.86, -1, PH, t)
    an.figures(c, horse_fig, (255, 140, 150), (0, 200, 1080, 1000), alpha=200)

    def figs(cc):
        with Cam(cc, focus, zoom)(1.0):
            if Pen.mode == "anchor":          # Rakhsh's anchors for the lead rope and the saddle
                tag("rk:")
                horse(cc, hx, 870, 0.86, -1, PH, t)
            tag("g:")
            person(cc, hx + 230, 870, 0.86, -1, {"mode": "walk" if 0 < led < 1 else "stand", "phase": t * 3.2,
                                                 "hand": (110, -330), "hand_kind": "open", "head": 3}, t, "herdsman")
            tag("r:")
            person(cc, rx, 870, 0.95, -1 if thank > 0.5 else 1, PR, t, "rostam")
            tag("")
            person(cc, 110, 870, 0.9, 1, {"hand": (mix(40, 120, thank), mix(-262, -360, thank)), "hand_kind": "open",
                                          "head": -2 + 4 * thank, "jaw": 0.0}, t, "king")
        h, r, sd = A("r:hand"), A("r:rhand"), A("rk:saddle")
        if lift > 0.5 and not on and h and r and sd:
            mx_, my_ = (h[0] + r[0]) / 2, (h[1] + r[1]) / 2 - 16 * zoom
            if toss > 0:
                e = ease(toss)
                mx_, my_ = mix(mx_, sd[0], e), mix(my_, sd[1] - 10 * zoom, e) - 120 * zoom * math.sin(e * math.pi)
            cc.save()
            cc.translate(mx_, my_)
            cc.rotate(-30 * toss * (1 - toss) * 4)
            cc.scale(-0.85 * zoom, 0.85 * zoom)
            fillp(cc, spath(SADDLE))
            cc.restore()
        if led < 1 or lt < s0:
            rope(cc, A("g:hand"), A("rk:mouth"), 30, 2.4)
    an.figures(c, figs, DAY, (0, 200, 1080, 1000), anchors=True)
    vig(an, c, 140)


def p8_s05(an, c, t):
    """From Tahmineh's window: Rostam gallops away across the plain until he is only a cloud of dust."""
    lt, dur = loc(an, "S05", t)
    b0, b1 = LN("p08", "S05", 1)
    focus = (560, 700)
    zoom = 1.0 + 0.06 * ease(lt / dur)
    cam = Cam(c, focus, zoom)
    S.lin(c, 0, H, [(0, (24, 16, 22)), (0.5, (44, 30, 34)), (1, (8, 5, 6))])
    arch = S.arch_path(640, 1240, 780, 1100)
    u = clamp((lt - 0.2) / 8.6)
    k = ease(u) * 0.6 + u * 0.4
    px, py = mix(660, 836, k), mix(1000, 784, k)
    sc = mix(0.34, 0.035, k)
    with cam(0.5):
        c.save()
        c.clipPath(arch, skia.ClipOp.kIntersect, True)
        S.lin(c, 140, 1240, [(0, (100, 130, 180)), (0.45, (210, 190, 176)), (0.62, (252, 214, 160)), (1, (200, 150, 110))],
              (200, 100, 1080, 1240))
        S.sun(c, 900, 520, 52, (255, 248, 222), (255, 214, 150), 420, 140)
        get(an, "cl85", lambda: S.Clouds([(330, 12), (420, 9), (500, 14)], 85, 300, 600)).draw(c, t, (160, 130, 150), 140)
        rg = get(an, "rg85", lambda: (S.make_ridge(-200, 1400, 720, 70, 851, 8, 4, 0.4), S.make_ridge(-200, 1400, 770, 30, 852)))
        S.ridge(c, rg[0], (150, 130, 150))
        S.ridge(c, rg[1], (110, 90, 100))
        S.lin(c, 770, 1240, [(0, (176, 140, 110)), (1, (110, 80, 60))], (-200, 770, 1400, 1240))
        c.drawPath(ppath([(600, 1240), (720, 1240), (840, 780), (826, 780)]), paint(C(210, 176, 136)))
        for j in range(6):
            q = clamp(k - j * 0.035)
            S.dust(c, mix(660, 836, q), mix(1000, 784, q) - 8, mix(70, 10, q) * (1 + 0.3 * j), t, (230, 200, 160),
                   (90 - j * 12) * (1 if u < 0.98 else 0.8), j)
        c.restore()
    if sc > 0.045:
        def rider(cc):
            with Cam(cc, focus, zoom)(0.5):
                horse(cc, px, py, sc, 1, {"gait": "gallop", "phase": t * 1.9, "saddle": True, "rider": "rostam",
                                            "rider_pose": {"lean": 10, "hand": (110, -320), "hand_kind": "mace", "mace": 50,
                                                           "wind": 1.0}}, t)
        an.figures(c, rider, DAY, (200, 600, 1080, 1240), alpha=110, rim=False)
    with cam(0.5):
        c.save()
        c.clipPath(arch, skia.ClipOp.kIntersect, True)
        c.drawRect(skia.Rect.MakeLTRB(-200, 1150, 1400, 1260), paint(C(*INK)))
        for j in range(30):
            c.drawRect(skia.Rect.MakeLTRB(-200 + j * 50, 1128, -200 + j * 50 + 28, 1150), paint(C(*INK)))
        c.restore()
        edge = skia.Paint(AntiAlias=True, Color=C(*INK))
        edge.setStyle(skia.Paint.kStroke_Style)
        edge.setStrokeWidth(30)
        c.drawPath(arch, edge)
    wave = sstep(b0, b0 + 0.6, lt) * (1 - sstep(b1 + 1.0, b1 + 2.0, lt))
    P = {"jaw": jaw(an, "TAHMINEH", t, 6), "hand": (mix(50, 140, wave), mix(-280, -470, wave)), "hand_kind": "open",
         "rhand": (-20, -330), "head": -2 - 4 * wave + 6 * sstep(b1 + 1.5, dur, lt) + 1.2 * math.sin(t * 0.7),
         "wind": 0.6, "lean": 2 * wave}

    def figs(cc):
        with Cam(cc, focus, zoom)(1.0):
            person(cc, 150, 1640, 2.1, 1, P, t, TAHM)
    an.figures(c, figs, DAY, (0, 150, 1080, 1800), alpha=170)
    vig(an, c, 170)


def p8_s06(an, c, t):
    """Night after night at the window, the jewel in her hand; the months pass and her child grows."""
    lt, dur = loc(an, "S06", t)
    m0, m1 = LN("p08", "S06", 0)
    y0, y1 = LN("p08", "S06", 1)
    j0, j1 = LN("p08", "S06", 3)
    c0, c1 = LN("p08", "S06", 4)
    focus = (560, 640)
    zoom = 1.0 + 0.08 * ease(lt / dur)
    cam = Cam(c, focus, zoom)
    months_window(an, c, t, cam, 770, 900, 470, 700, lt, "mw86")
    hold = sstep(j0, j0 + 0.8, lt)
    belly = sstep(c0 - 4.0, c1, lt)
    leave = clamp((lt - y1 - 0.2) / 2.6)
    mx = mix(130, -160, ease(leave))
    P = {"jaw": jaw(an, "TAHMINEH", t, 6), "hand": (mix(70, 110, hold), mix(-340, -400, hold)), "hand_kind": "open",
         "rhand": (mix(-30, 30, sstep(c0, c0 + 0.8, lt)), mix(-262, -290, sstep(c0, c0 + 0.8, lt))),
         "head": 2 - 4 * hold + 6 * sstep(c0, c0 + 1.0, lt) + 1.2 * math.sin(t * 0.6),
         "wind": 0.4, "belly": belly}

    def figs(cc):
        with Cam(cc, focus, zoom)(1.0):
            tag("t:")
            person(cc, 430, 1420, 1.55, 1, P, t, TAHM)
            tag("m:")
            if leave < 1:
                person(cc, mx, 1240, 1.05, -1 if leave > 0 else 1,
                       {"mode": "walk" if 0 < leave < 1 else "stand", "phase": lt * 4, "stride": 14, "hand_kind": "candle",
                        "hand": (100, -380), "jaw": jaw(an, "MAID", t, 7), "head": 2, "wind": 0.3}, t, "maid")
            tag("")
    an.figures(c, figs, MOON, (0, 150, 1080, 1600), alpha=170, anchors=True)
    if leave < 1:
        candle_light(c, an, "m:flame", t, 420, 110, 3.0, 0.26)
    gem_at(c, "t:hand", t, 11 * zoom, 1.0, 14, -12, 4.0, 0.7 + 0.5 * hold)
    vig(an, c, 180)


def p8_s07(an, c, t):
    """The birth: the maid gives the newborn to Tahmineh; on the curtain, the shadows of the old heroes."""
    lt, dur = loc(an, "S07", t)
    m0, m1 = LN("p08", "S07", 1)
    l0, l1 = LN("p08", "S07", 2)
    p0, p1 = LN("p08", "S07", 3)
    walk = clamp((lt - 0.8) / 2.6)
    mx = mix(250, 470, ease(walk))
    hand_over = sstep(3.6, 4.6, lt)
    fist = sstep(m0 + 1.6, m0 + 2.2, lt) * (1 - sstep(l1, l1 + 0.8, lt))
    look = sstep(l0, l0 + 0.6, lt)
    heroes = sstep(p0 + 0.8, p0 + 2.2, lt) * (1 - sstep(dur - 0.8, dur, lt))
    PM = {"mode": "walk" if 0 < walk < 1 else "stand", "phase": lt * 3.4, "stride": 12, "jaw": jaw(an, "MAID", t, 7),
          "hand": (mix(90, 150, hand_over) if hand_over < 0.99 else mix(150, 60, sstep(4.6, 5.4, lt)), mix(-330, -340, hand_over)),
          "hand_kind": "fist", "rhand": (mix(70, 120, hand_over), mix(-320, -330, hand_over)),
          "head": 4 + 4 * hand_over, "wind": 0.3}
    PT = {"jaw": jaw(an, "TAHMINEH", t, 6), "hand": (mix(150, 120, sstep(4.2, 5.2, lt)), mix(-380, -330, sstep(4.2, 5.2, lt))),
          "hand_kind": "open", "rhand": (mix(-30, 60, hand_over), mix(-262, -320, hand_over)), "rhand_kind": "open",
          "head": 6 + 8 * look + 1.2 * math.sin(t * 0.7)}

    def curtain():
        if heroes > 0.01:
            shadow_layer(c, (240, 280, 1200, 1000), 0.75 * heroes, (70, 30, 18), 2.4)
            for i, (x, look_, s, P) in enumerate(((470, "warrior_ir", 0.72, {"hand_kind": "spear", "hand": (100, -320)}),
                                                  (700, "rostam", 0.82, {"hand_kind": "oxmace", "hand": (110, -330), "mace": 10}),
                                                  (930, "warrior_ir", 0.72, {"hand_kind": "mace", "hand": (100, -320), "mace": 20}))):
                person(c, x, 940, s, -1 if i == 2 else 1, dict(P, head=-2, wind=0.7, stance=(56, 46)), t, look_)
            c.restore()
    baby_on = "maid" if hand_over < 0.6 else "mother"
    birth_two(an, c, t, lt, dur, PM, mx, PT, mix(14, 4, sstep(0.5, 2.5, lt)), baby_on, fist, 0.07, 0.0, curtain)


def p8_s08(an, c, t):
    """Close: the baby smiles; she names him Sohrab and ties his father's jewel on his arm."""
    lt, dur = loc(an, "S08", t)
    n0, n1 = LN("p08", "S08", 1)
    j0, j1 = LN("p08", "S08", 2)
    focus = (560, 640)
    zoom = 1.0 + 0.07 * ease(lt / dur)
    cam = Cam(c, focus, zoom)
    with cam(0.6):
        S.lin(c, 0, H, [(0, (16, 10, 22)), (0.45, (48, 28, 34)), (1, (6, 3, 5))])
        wall_panel(c, 300, 1200, 280, 1100, (110, 62, 50), (170, 106, 76), 96)
    shine = sstep(1.8, 3.4, lt) * (1 - 0.4 * sstep(n1, j1, lt))
    S.glow(c, 380, 640, 560, (255, 214, 140), 140 * shine)
    tie = sstep(j0 + 0.4, j0 + 2.2, lt)
    arm = sstep(j0, j0 + 0.6, lt)
    P = {"jaw": jaw(an, "TAHMINEH", t, 6), "hand": (mix(96, 104, tie), mix(-410, -420, tie)), "hand_kind": "open",
         "rhand": (mix(50, 96, tie), mix(-380, -440, tie)), "rhand_kind": "open",
         "head": 12 + 1.2 * math.sin(t * 0.6), "lean": 3}

    def figs(cc):
        with Cam(cc, focus, zoom)(1.0):
            tag("t:")
            in_bed(cc, t, 780, 1060, 2.2, 2, P, TAHM)
            tag("")
            fillp(cc, spath([(-100, 1400, 0), (-100, 1110), (300, 1100), (600, 1110), (800, 1140), (840, 1400, 0)]))
        h, r = A("t:hand"), A("t:rhand")
        if h and r:
            tag("b:")
            baby(cc, (h[0] + r[0]) / 2 - 14 * zoom, (h[1] + r[1]) / 2 - 30 * zoom, 2.0 * zoom, t, 6, arm, 1, 0.6)
            tag("")
    an.figures(c, figs, WARM, (0, 150, 1080, 1500), anchors=True)
    hd = A("b:bhead")
    if hd and shine > 0.01:
        S.glow(c, hd[0], hd[1], 160, (255, 230, 170), 120 * shine)
    if tie < 0.98:
        gem_at(c, "t:rhand", t, 12 * zoom, 1.0, -10, -10, 5.0)
    else:
        gem_at(c, "b:barm", t, 10 * zoom, 1.0, 0, 0, 5.0)
    get(an, "mo88", lambda: S.Motes(40, 88, 250, 1000)).draw(c, t, (255, 210, 150), 70, rise=3, drift=0.2)
    vig(an, c, 180)


def p8_s09(an, c, t):
    """Turn + end: at the moon window with her son -- a vision of two riders facing each other; a cloud takes the moon."""
    lt = t - an.start["S09"]
    d0, d1 = LN("p08", "S09", 1)
    focus = (600, 620)
    zoom = 1.04 + 0.1 * ease(lt / (an.end["END"] - an.start["S09"]))
    cam = Cam(c, focus, zoom)
    cover = sstep(d1 - 0.6, d1 + 3.0, lt)
    moon_window(an, c, t, cam, 780, 880, 440, 640, cover, key="w89")
    vis = sstep(d0 + 0.6, d0 + 2.0, lt) * (1 - sstep(d1 + 1.6, d1 + 3.4, lt))
    if vis > 0.01:
        with cam(0.5):
            c.save()
            c.clipPath(S.arch_path(780, 880, 440, 640), skia.ClipOp.kIntersect, True)
            ghost_layer(c, (560, 240, 1000, 880), 0.55 * vis, (255, 170, 140), 2.6)
            ch = sstep(d0 + 0.6, d1, lt)
            horse(c, mix(640, 700, ch), 560, 0.26, 1, {"gait": "gallop", "phase": t * 1.6, "saddle": True, "rider": "sohrab",
                                                       "rider_pose": {"hand_kind": "spear", "hand": (120, -340), "lean": 8}}, t)
            horse(c, mix(930, 870, ch), 560, 0.28, -1, {"gait": "gallop", "phase": t * 1.6 + 0.3, "saddle": True, "rider": "rostam",
                                                        "rider_pose": {"hand_kind": "mace", "hand": (110, -360), "mace": 20, "lean": 8}}, t)
            c.restore()
            c.restore()
    rock = math.sin(t * 1.6)
    P = {"jaw": jaw(an, "TAHMINEH", t, 6), "hand": (110 + 4 * rock, -350 + 6 * rock), "hand_kind": "open",
         "rhand": (60, -340), "rhand_kind": "open", "head": 8 - 10 * sstep(d0, d0 + 1.0, lt) * (1 - cover) + 1.2 * math.sin(t * 0.7),
         "wind": 0.5}

    def figs(cc):
        with Cam(cc, focus, zoom)(1.0):
            tag("t:")
            person(cc, 360, 1500, 2.0, 1, P, t, TAHM)
            tag("")
        h, r = A("t:hand"), A("t:rhand")
        if h and r:
            baby(cc, (h[0] + r[0]) / 2 + 16 * zoom, (h[1] + r[1]) / 2 - 26 * zoom, 1.8 * zoom, t, -8 - 3 * rock, 0.0, -1, 0.4)
    an.figures(c, figs, mixc(MOON, (120, 130, 170), cover), (0, 200, 1080, 1600), alpha=170 - 60 * cover, anchors=True)
    get(an, "mo89", lambda: S.Motes(40, 89, 250, 1000)).draw(c, t, (200, 214, 255), 70, rise=3, drift=0.2)
    vig(an, c, 180 + 30 * cover)


P08 = {"S01": p8_s01, "TITLE": p8_s01, "S02": p8_s02, "S03": p8_s03, "S04": p8_s04, "S05": p8_s05, "S06": p8_s06,
       "S07": p8_s07, "S08": p8_s08, "S09": p8_s09, "END": p8_s09}
SHIFT8 = {}


register(P07, SHIFT7)
