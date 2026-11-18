"""Parts 11-12 (row 6 of OUTLINE.md, "Sohrab's Army"): every shot as a shadow-play scene.

Importing this module registers part 11's shots; p12_scenes.py imports it and registers part 12's.
New here, to reuse: dawn_two() (two people standing at the window from night to sunrise), throne() and
sit_throne() (a king sitting cross-legged on a throne on a dais), crown_shape(), curtain() (the lit curtain of
the shadow stories, full frame), the horse test (a horse sinking under a hand, horse(P["sink"]), with the hands
following its back: croup()), pasture() (the high mountain pasture at dawn), camp() (tents on the plain),
kettle_drum() + drummer(), army_band() (rows of riders and foot soldiers with spears and banners, drawn once;
raised=True for the cheer), dark_hall() and brazier() (Afrasiab's palace at night, red fire).
meydan() (p09_scenes) takes behind=... to put far hills between the sky and the city.
Line timings come from pNN/audio/timeline.json (LN), so the action follows the voices.
"""
import math, random
import numpy as np
import skia
import anim
from anim import C, mix, mixc, clamp, ease, sstep, Cam, Pen, rope, spath, ppath, paint, fillp, W, H
from puppets import person, horse, LOOKS
import sets as S
from ep01_scenes import loc, jaw, get, vig, tag, A, ground, INK, hall, Scroller, gallop_sky, tufts_list
from p05_scenes import TAHM, WARM, MOON, shadow_layer, ghost_layer, register
from p07_scenes import LN, dissolve, gem_at, seated, dawn_window, courtyard, DAWN
from p09_scenes import YS, DAY, NOON, SUNSET, SH_B, flick, meydan, seated_two

COLT = (255, 130, 150)                         # rose rim of the colt of Rakhsh's line (Rakhsh had it in part 1)
KING_R = dict(LOOKS["rostam"], head="crown")   # Rostam crowned, in Sohrab's dream
BARE_R = dict(LOOKS["rostam"], head="bare")
EMBER = (255, 112, 64)                         # Afrasiab's firelight
CROWN = [(-33, 30, 0), (-35, -18, 0), (-23, 0, 0), (-13, -30, 0), (-1, -4, 0), (11, -36, 0), (21, -4, 0), (33, -22, 0),
         (35, 26, 0), (3, 20), (-19, 24)]


# ------------------------------------------------------------------ props
def throne(cc, x, y, s, face=1):
    """A royal throne on a low dais (puppet pen), facing +x; the seat top is at y - 160 s (see sit_throne)."""
    anim.begin_fig(cc, (x - 280 * s, y - 640 * s, x + 280 * s, y + 20 * s))
    cc.save()
    cc.translate(x, y)
    cc.scale(s * face, s)
    fillp(cc, ppath([(-190, 0), (230, 0), (214, -30), (-176, -30)]))
    fillp(cc, spath([(-120, -30, 0), (-128, -150, 0), (170, -150, 0), (160, -30, 0)]))
    fillp(cc, ppath([(-136, -164), (182, -164), (172, -146), (-128, -146)]))
    for px in (-108, 146):
        fillp(cc, spath([(px - 22, 2, 0), (px - 16, -34), (px + 14, -34), (px + 26, 2, 0)]))
    fillp(cc, spath([(-128, -150, 0), (-138, -420), (-126, -500), (-98, -540), (-80, -610, 0), (-62, -540),
                     (-38, -500), (-28, -420), (-40, -150, 0)]))
    fillp(cc, ppath([(-60, -252), (132, -252), (132, -238), (-60, -238)]))
    fillp(cc, ppath([(118, -252), (134, -252), (134, -150), (118, -150)]))
    if Pen.mode != "anchor":
        cc.drawCircle(138, -262, 15, anim.ink())
    cc.restore()
    cc.restore()


def sit_throne(cc, x, y, s, face, P, t, look):
    """A king sitting cross-legged on his throne (the throne's dais on the floor at y)."""
    throne(cc, x, y, s, face)
    seated(cc, x + 12 * s * face, y - 160 * s, s, face, P, t, look)


def crown_shape(cc, x, y, s):
    cc.save()
    cc.translate(x, y)
    cc.scale(s, s)
    fillp(cc, spath(CROWN))
    cc.restore()


def croup(hx, hy, hs, face, sink=0.0, lx=-150, lie=0.0):
    """Screen point on a horse's back (local x lx, default the croup) for horse(hx, hy, hs, face, sink=..., lie=...)."""
    return hx + hs * face * lx, hy + hs * (-9 + 46 * sink * (1 - lie) + 132 * lie - 290)


def collapse(u):
    """A horse giving way under the hand, u = 0..1: knees buckle (sink), then it goes down on its belly (lie);
    rel (0..1) is when the hand lets go."""
    return 0.85 * ease(clamp(u / 0.45)), ease(clamp((u - 0.4) / 0.6)), sstep(0.4, 0.75, u)


def HILL(x):
    """Height of the far hill of the high pastures (p11 S07)."""
    return 846 - 130 * math.exp(-((x - 760) / 170) ** 2) - 40 * math.exp(-((x - 1060) / 200) ** 2) - 6 * math.sin(x * 0.03)


def to_local(px, py, X, Y, s, face):
    """A screen point in a puppet's local frame (for hand targets)."""
    return (px - X) / s * face, (py - Y) / s


def kettle_drum(cc, x, y, s):
    """A big kettle drum (puppet pen): a bowl on short legs, the skin flat at y - 72 s."""
    fillp(cc, spath([(x - 70 * s, y - 70 * s, 0), (x - 62 * s, y - 34 * s), (x - 30 * s, y - 10 * s), (x + 30 * s, y - 10 * s),
                     (x + 62 * s, y - 34 * s), (x + 70 * s, y - 70 * s, 0)]))
    fillp(cc, ppath([(x - 76 * s, y - 78 * s), (x + 76 * s, y - 78 * s), (x + 76 * s, y - 66 * s), (x - 76 * s, y - 66 * s)]))
    for k in (-1, 1):
        fillp(cc, ppath([(x + k * 30 * s - 5 * s, y - 14 * s), (x + k * 30 * s + 5 * s, y - 14 * s),
                         (x + k * 44 * s + 5 * s, y), (x + k * 44 * s - 5 * s, y)]))


def drummer(cc, x, y, s, face, t, beat, seed=0.0):
    """A drummer behind a kettle drum, beating it with both fists (beat 0..1 = how hard)."""
    ph = t * 7.0 + seed
    a = 0.5 + 0.5 * math.sin(ph)
    b = 0.5 + 0.5 * math.sin(ph + math.pi)
    up = lambda u: -300 - 170 * u * beat
    person(cc, x, y, s, face, {"hand": (96, up(a)), "rhand": (70, up(b)), "head": 6, "lean": 6, "seed": seed}, t, "guard")
    kettle_drum(cc, x + 110 * s * face, y, s * 1.1)


def drum_rings(c, x, y, t, a, seed=0.0):
    """Faint rings of sound spreading from a drum."""
    if a <= 0.01:
        return
    p = skia.Paint(AntiAlias=True)
    p.setStyle(skia.Paint.kStroke_Style)
    p.setStrokeWidth(3)
    for k in range(2):
        u = (t * 1.75 + seed + k * 0.5) % 1.0
        p.setColor(C(255, 236, 200, 110 * a * (1 - u)))
        c.drawOval(skia.Rect.MakeXYWH(x - 30 - 140 * u, y - 14 - 60 * u, 60 + 280 * u, 28 + 120 * u), p)


def brazier(c, x, y, s, t, a=1.0):
    """A tall iron fire bowl (plain silhouette), its flames and red light."""
    pt = paint(C(*INK))
    c.drawPath(spath([(x - 60 * s, y, 0), (x - 12 * s, y - 40 * s), (x - 8 * s, y - 210 * s, 0), (x + 8 * s, y - 210 * s, 0),
                      (x + 12 * s, y - 40 * s), (x + 60 * s, y, 0)]), pt)
    c.drawPath(spath([(x - 80 * s, y - 250 * s, 0), (x - 66 * s, y - 220 * s), (x - 30 * s, y - 204 * s), (x + 30 * s, y - 204 * s),
                      (x + 66 * s, y - 220 * s), (x + 80 * s, y - 250 * s, 0)]), pt)
    fl = flick(t, 4.0)
    S.glow(c, x, y - 300 * s, 760 * s, EMBER, 150 * a * fl)
    for k, dx in enumerate((-34, 0, 30)):
        S.flame(c, x + dx * s, y - 244 * s, s * (1.0 if k == 1 else 0.72), t, seed=k * 2.3 + 1.0, a=a)


def curtain(c, t):
    """The lit curtain of the shadow stories, filling the frame (warm folds, a lamp below)."""
    S.lin(c, 0, H, [(0, (60, 26, 18)), (0.2, (170, 96, 52)), (0.45, (236, 168, 96)), (0.62, (214, 140, 80)),
                    (0.8, (110, 50, 30)), (1, (16, 6, 6))])
    pf = skia.Paint(AntiAlias=True)
    pf.setShader(skia.GradientShader.MakeLinear([skia.Point(0, 0), skia.Point(96, 0)],
                                                [C(90, 36, 20, 90), C(255, 230, 190, 30), C(90, 36, 20, 90)],
                                                [0.0, 0.5, 1.0], skia.TileMode.kRepeat))
    c.drawRect(skia.Rect.MakeLTRB(0, 0, W, H), pf)
    S.glow(c, 300, 1000, 900, (255, 190, 110), 110 * flick(t))


def army_band(raised, seed=12, w=1500, h=300):
    """Rows of riders and foot soldiers with spears and banners, drawn once into an image (black silhouettes, to
    be tinted when drawn). The front row stands on y = h - 8; raised=True lifts spears and banners (the cheer)."""
    arr = np.zeros((h, w, 4), np.uint8)
    surf = skia.Surface(arr)
    c = surf.getCanvas()
    rnd = random.Random(seed)
    Pen.mode = "fill"
    rows = [(h - 64, 0.15, 44), (h - 36, 0.19, 56), (h - 8, 0.24, 70)]
    for (gy, sc, sp) in rows:
        x = rnd.uniform(0, sp)
        while x < w + 40:
            tt = rnd.uniform(0, 9)
            look = rnd.choice(["warrior_tu", "rider", "warrior_tu", "guard"])
            lift = rnd.uniform(0.8, 1.0)
            if rnd.random() < 0.6:
                horse(c, x, gy, sc, 1, {"gait": "stand", "neck": rnd.uniform(-6, 12), "head": rnd.uniform(-4, 8),
                                        "saddle": True, "rider": look,
                                        "rider_pose": {"hand_kind": "spear", "head": -2,
                                                       "hand": (60, -440 - 80 * lift) if raised else (110, -330)}}, tt)
            else:
                person(c, x, gy, sc * 1.1, 1, {"hand_kind": "spear", "seed": x,
                                               "hand": (50, -500 - 60 * lift) if raised else (100, -320)}, tt, look)
            if rnd.random() < 0.16:
                bx, top = x + rnd.uniform(-10, 10), gy - sc * rnd.uniform(900, 1000) - (40 if raised else 0)
                c.drawRect(skia.Rect.MakeLTRB(bx - 1.6, top, bx + 1.6, gy - 10), paint(C(*INK)))
                fw = rnd.uniform(40, 60)
                c.drawPath(spath([(bx, top, 0), (bx + fw, top + 6), (bx + fw * 0.8, top + 18, 0), (bx + fw, top + 30),
                                  (bx, top + 26, 0)]), paint(C(*INK)))
            x += sp * rnd.uniform(0.75, 1.2)
    return skia.Image.fromarray(arr)


def draw_band(c, img, x, y, col, a=1.0):
    if a <= 0.01:
        return
    p = skia.Paint()
    p.setAlphaf(clamp(a))
    p.setColorFilter(skia.ColorFilters.Blend(C(*col), skia.BlendMode.kSrcIn))
    c.drawImage(img, x, y, skia.SamplingOptions(skia.FilterMode.kLinear), p)


# ------------------------------------------------------------------ sets
def dawn_two(an, c, t, lt, dur, PS, sx, PT, tx, key, dawn, sun=0.0, zk=0.06, gem_a=0.7, face_s=1, face_t=-1):
    """Sohrab (left) and Tahmineh (right) standing at the window while the night turns to sunrise."""
    focus = (540, 700)
    zoom = 1.0 + zk * ease(lt / max(dur, 0.1))
    cam = Cam(c, focus, zoom)
    dawn_window(an, c, t, cam, 540, 1010, 400, 720, dawn, key, sun=sun, k=0.6)
    with cam(0.6):
        S.hanging_lamp(c, 980, 250, 1.1, t, 110, 3.0)
        S.glow(c, 980, 560, 520, (255, 170, 90), 70 * flick(t) * (1 - 0.5 * clamp(dawn)))

    def figs(cc):
        with Cam(cc, focus, zoom)(1.0):
            tag("s:")
            person(cc, sx, 1330, 1.42, face_s, PS, t, YS)
            tag("t:")
            person(cc, tx, 1330, 1.5, face_t, PT, t, TAHM)
            tag("")
    an.figures(c, figs, mixc(WARM, DAWN, clamp(dawn)), (0, 150, 1080, 1500), anchors=True)
    gem_at(c, "s:hand_up", t, 8 * zoom, gem_a, 0, 0, 1.0, 0.6)
    vig(an, c, 170)


def colt_hill(an, c, cam, mood):
    """A far hill on the right under the low sun (for meydan(behind=...)): the high pastures."""
    with cam(0.3):
        pts = get(an, "hill117", lambda: [(x, HILL(x)) for x in range(500, 1500, 6)])
        S.ridge(c, pts, mixc((150, 100, 120), (104, 40, 58), clamp(mood - 1)))


def pasture(an, c, t, cam, dawn=0.5, key="pa"):
    """The high mountain pasture at dawn: snowy peaks, mist in the valley, a grassy slope with a lone tree."""
    top = mixc((40, 44, 92), (92, 120, 178), dawn)
    mid = mixc((160, 112, 150), (240, 182, 162), dawn)
    low = mixc((240, 170, 140), (255, 218, 172), dawn)
    S.lin(c, 0, 900, [(0, top), (0.55, mid), (0.84, low), (1, low)])
    with cam(0.15):
        S.sun(c, 720, mix(760, 600, dawn), 60, (255, 246, 214), (255, 190, 130), 520, 110 + 50 * dawn)
        get(an, key + "cl", lambda: S.Clouds([(300, 12), (380, 9), (450, 14)], 121, 260, 520)).draw(
            c, t, mixc((150, 110, 150), (236, 176, 172), dawn), 150)
    pk = get(an, key + "pk", lambda: (S.make_ridge(-600, 1700, 690, 150, 122, 8, 4, 0.75),
                                       S.make_ridge(-600, 1700, 760, 80, 123, 8, 4, 0.4),
                                       S.make_ridge(-600, 1700, 816, 30, 124)))
    with cam(0.25):
        S.ridge(c, pk[0], mixc((196, 190, 222), (255, 238, 228), dawn))
        c.save()
        c.translate(0, 24)
        S.ridge(c, pk[0], mixc((112, 104, 148), (172, 150, 178), dawn))
        c.restore()
    with cam(0.35):
        S.lin(c, 690, 800, [(0, (*low, 0)), (0.7, (*low, 150)), (1, (*low, 0))], (-600, 690, 1700, 800))
        S.ridge(c, pk[1], mixc((72, 64, 102), (122, 102, 126), dawn))
    with cam(0.55):
        S.lin(c, 770, 846, [(0, (*low, 0)), (1, (*low, 110))], (-600, 770, 1700, 846))
        S.ridge(c, pk[2], mixc((46, 40, 58), (86, 72, 78), dawn))
    with cam(0.8):
        ground(c, 870, mixc((52, 60, 44), (92, 100, 66), dawn), (14, 12, 8), -14)
        S.tufts(c, get(an, key + "tf", lambda: tufts_list(125, 60, -300, 1400, 874, 10, 30)), t, INK, 0.4)
        S.tree(c, 40, 874, 0.8, t, "plane", 0.25, 5, INK)


def camp(an, c, t, cam, key="cp"):
    """The plain outside Samangan in the morning: tents with pennants, far hills, bright dust."""
    S.lin(c, 0, 880, [(0, (84, 112, 162)), (0.5, (196, 184, 172)), (0.84, (248, 212, 158)), (1, (252, 224, 172))])
    with cam(0.2):
        S.sun(c, 250, 520, 56, (255, 248, 222), (255, 214, 150), 520, 150)
        get(an, key + "cl", lambda: S.Clouds([(250, 14), (330, 10), (420, 16)], 131, 300, 600)).draw(c, t, (160, 130, 150), 140)
    rg = get(an, key + "rg", lambda: (S.make_ridge(-600, 1700, 770, 50, 132, 8, 4, 0.4), S.make_ridge(-600, 1700, 816, 20, 133)))
    with cam(0.4):
        S.ridge(c, rg[0], (150, 130, 150))
        S.lin(c, 740, 820, [(0, (250, 220, 170, 0)), (1, (250, 220, 170, 120))], (-600, 740, 1700, 820))
    with cam(0.55):
        S.ridge(c, rg[1], (110, 90, 96))
    with cam(0.8):
        ground(c, 866, (150, 116, 80), (36, 26, 18))
        for (x, s_) in ((60, 0.7), (300, 0.9), (560, 0.62), (800, 0.85), (1040, 0.7)):
            S.tent(c, x, 866, s_, t + x, INK)


def dark_hall(an, c, t, cam, fire=1.0):
    """Afrasiab's palace at night: dark red stone, pointed arches with a red moon, heavy pillars."""
    with cam(0.6):
        S.lin(c, 0, H, [(0, (12, 4, 8)), (0.35, (44, 12, 16)), (0.55, (34, 10, 14)), (1, (4, 2, 3))])
        for k, x in enumerate((160, 540, 920)):
            arch = S.arch_path(x, 830, 230, 560)
            c.save()
            c.clipPath(arch, skia.ClipOp.kIntersect, True)
            S.lin(c, 270, 830, [(0, (30, 10, 24)), (0.7, (90, 26, 30)), (1, (120, 40, 34))], (x - 130, 260, x + 130, 840))
            if k == 1:
                S.moon(c, x + 30, 430, 30, (255, 196, 170), (200, 60, 50))
            img, _ = get(an, "dh_city", lambda: S.city(700, 300, 290, 151, (14, 4, 8), False, None))
            c.drawImage(img, x - 350, 560)
            c.restore()
            edge = skia.Paint(AntiAlias=True, Color=C(*INK))
            edge.setStyle(skia.Paint.kStroke_Style)
            edge.setStrokeWidth(18)
            c.drawPath(arch, edge)
        pt = paint(C(*INK))
        for x in (-20, 350, 730, 1100):
            c.drawRect(skia.Rect.MakeLTRB(x - 44, 160, x + 44, 900), pt)
            c.drawRect(skia.Rect.MakeLTRB(x - 58, 140, x + 58, 172), pt)
        c.drawRect(skia.Rect.MakeLTRB(-100, 0, 1200, 150), pt)
        S.glow(c, 420, 760, 760, EMBER, 70 * fire * flick(t, 2.0))
    with cam(1.0):
        ground(c, 900, (44, 12, 12))


# ================================================================== part 11 shots
def p11_s01(an, c, t):
    """Hook + title: at the window at first light the boy swears to take Kavus's crown for his father;
    his mother is shaken."""
    lt = t - an.start["S01"]
    dur = an.end["TITLE"] - an.start["S01"]
    a0, a1 = LN("p11", "S01", 0)
    b0, b1 = LN("p11", "S01", 1)
    sweep = sstep(a0 + 0.2, a0 + 0.9, lt) * (1 - sstep(a1 - 1.6, a1 - 1.1, lt))
    up = sstep(a1 - 1.4, a1 - 0.8, lt) * (1 - sstep(b1 + 1.4, b1 + 2.6, lt))
    shock = sstep(b0 - 0.4, b0 + 0.3, lt)
    reach = sstep(b0 + 1.0, b0 + 1.6, lt)
    if up > 0.01:
        h, hk = (mix(190, 70, up), mix(-390, -560, up)), "fist"
    else:
        h, hk = (mix(40, 190, sweep), mix(-262, -390, sweep)), ("open" if sweep > 0.3 else "fist")
    PS = {"jaw": jaw(an, "SOHRAB", t, 8), "hand": h, "hand_kind": hk, "rhand": (-30, -262),
          "head": -2 - 5 * up + 1.2 * math.sin(t * 0.8), "lean": 3 * sweep - 2 * up, "wind": 0.3}
    PT = {"jaw": jaw(an, "TAHMINEH", t, 6),
          "hand": (mix(mix(50, 26, shock), 150, reach), mix(mix(-300, -372, shock), -392, reach)), "hand_kind": "open",
          "rhand": (mix(-30, 20, shock * (1 - reach)), mix(-262, -380, shock * (1 - reach))), "rhand_kind": "open",
          "head": 4 - 8 * shock + 7 * reach + 1.2 * math.sin(t * 0.7), "lean": -5 * shock + 4 * reach, "wind": 0.3}
    dawn = mix(0.5, 0.82, ease(lt / dur))
    dawn_two(an, c, t, lt, dur, PS, 260, PT, 830, "dw111", dawn, 0.35 * sstep(dur - 5.0, dur, lt), 0.09, 0.75)


def p11_s02(an, c, t):
    """The sleepless night at the window: a vision of Rostam riding far away; he paces; dawn breaks and he raises
    his fist."""
    lt, dur = loc(an, "S02", t)
    L = [LN("p11", "S02", k) for k in range(4)]
    focus = (540, 690)
    zoom = 1.0 + 0.08 * ease(lt / dur)
    cam = Cam(c, focus, zoom)
    dawn = sstep(L[2][0] + 1.0, L[3][1] - 0.4, lt)
    sun = sstep(L[3][0] + 0.5, dur + 0.6, lt)
    dawn_window(an, c, t, cam, 540, 1010, 400, 720, dawn, "dw112", sun=1.0 * sun, k=0.6)
    vis = sstep(L[0][0] + 0.3, L[0][0] + 1.5, lt) * (1 - sstep(L[1][1] - 1.8, L[1][1] - 0.2, lt))
    if vis > 0.01:
        u = clamp((lt - L[0][0]) / (L[1][1] - L[0][0]))
        with cam(0.6):
            c.save()
            c.clipPath(S.arch_path(540, 1000, 376, 700), skia.ClipOp.kIntersect, True)
            ghost_layer(c, (300, 250, 780, 1020), 0.62 * vis, (255, 214, 160), 2.4)
            horse(c, mix(400, 690, u), mix(730, 690, u), mix(0.34, 0.14, ease(u)), 1,
                  {"gait": "gallop", "phase": t * 1.7, "saddle": True, "rider": "rostam",
                   "rider_pose": {"lean": 10, "hand": (110, -330), "hand_kind": "oxmace", "mace": 40, "wind": 1.0}}, t)
            c.restore()
            c.restore()
    w0, w1 = L[2][0] + 0.1, L[2][1] - 0.1
    walk = clamp((lt - w0) / (w1 - w0))
    turn = lt > L[3][0] + 0.5
    up = sstep(L[3][0] + 1.6, L[3][0] + 2.2, lt)
    look = 1 - sstep(w0 - 0.5, w0 + 0.3, lt)
    walking = 0 < walk < 1
    PS = {"mode": "walk" if walking else "stand", "phase": lt * 3.4, "stride": 14,
          "hand": (mix(40, 70, up), mix(-262, -560, up)), "hand_kind": "fist", "rhand": (-30, -262),
          "head": -7 * look + 7 * walking - 5 * up + 1.2 * math.sin(t * 0.7), "lean": 3 * walking, "wind": 0.3}
    x = mix(250, 700, ease(walk))

    def figs(cc):
        with Cam(cc, focus, zoom)(1.0):
            tag("s:")
            person(cc, x, 1330, 1.42, -1 if turn else 1, PS, t, YS)
            tag("")
    an.figures(c, figs, mixc(MOON, DAWN, dawn), (0, 150, 1080, 1500), anchors=True)
    gem_at(c, "s:hand_up", t, 8 * zoom, 0.5 + 0.4 * up, 0, 0, 1.0, 0.5 + 0.6 * up)
    get(an, "mo112", lambda: S.Motes(30, 112, 250, 1000)).draw(c, t, (200, 214, 255), 50 * (1 - dawn), rise=3, drift=0.2)
    vig(an, c, 175)


def p11_s03(an, c, t):
    """By the candle at first light he tells his plan; on the curtain Kavus is thrown from his throne, Rostam sits
    on it and a crown comes down on his head."""
    lt, dur = loc(an, "S03", t)
    L = [LN("p11", "S03", k) for k in range(7)]
    lean = sstep(L[0][0], L[0][0] + 0.6, lt)
    fist0 = sstep(L[0][1] - 1.6, L[0][1] - 1.1, lt) * (1 - sstep(L[0][1], L[0][1] + 0.4, lt))
    sweep = sstep(L[1][0] + 0.3, L[1][0] + 1.0, lt) * (1 - sstep(L[1][1], L[1][1] + 0.5, lt))
    offer = sstep(L[3][0] + 0.2, L[3][0] + 0.8, lt) * (1 - sstep(L[4][0], L[4][0] + 0.3, lt))
    up = sstep(L[4][0], L[4][0] + 0.4, lt) * (1 - sstep(L[4][1] + 0.3, L[4][1] + 0.8, lt))
    chop = sstep(L[6][0] + 0.2, L[6][0] + 0.6, lt)
    alarm = sstep(L[2][0] - 0.1, L[2][0] + 0.4, lt) * (1 - sstep(L[2][1] + 0.2, L[2][1] + 0.8, lt))
    plead = sstep(L[5][0], L[5][0] + 0.6, lt) * (1 - sstep(L[6][0] + 0.5, L[6][0] + 1.2, lt))
    if up > 0.01:
        h, hk = (mix(130, 70, up), mix(-430, -560, up)), "fist"
    elif offer > 0.01:
        h, hk = (mix(110, 140, offer), mix(-300, -430, offer)), "open"
    elif sweep > 0.01:
        h, hk = (mix(110, 190, sweep), mix(-300, -390, sweep)), "open"
    elif chop > 0.01:
        h, hk = (mix(110, 170, chop), mix(-300, -350, chop)), "fist"
    else:
        h, hk = (mix(110, 90, fist0), mix(-300, -400, fist0)), ("fist" if fist0 > 0.3 else "open")
    PS = {"jaw": jaw(an, "SOHRAB", t, 8), "hand": h, "hand_kind": hk, "rhand": (-30, -262),
          "head": 3 - 4 * up - 3 * offer + 1.2 * math.sin(t * 0.8), "lean": 4 * lean + 4 * chop - 2 * up}
    PT = {"jaw": jaw(an, "TAHMINEH", t, 6),
          "hand": (mix(mix(80, 100, alarm), 170, plead), mix(mix(-300, -470, alarm), -340, plead)), "hand_kind": "open",
          "rhand": (mix(-30, 60, alarm), mix(-262, -450, alarm)), "rhand_kind": "open" if alarm > 0.3 else "fist",
          "head": 4 - 6 * alarm + 2 * plead + 1.2 * math.sin(t * 0.7), "lean": 3 - 6 * alarm + 4 * plead}
    th = sstep(L[1][0] + 0.3, L[1][0] + 1.3, lt)
    fall = clamp((lt - (L[1][1] - 1.3)) / 1.2)
    ro = sstep(L[3][0] + 0.2, L[3][0] + 1.4, lt)
    cr = clamp((lt - L[4][0] - 0.2) / 1.4)
    dim = 1 - 0.35 * sstep(L[5][0], L[5][0] + 0.6, lt) * (1 - sstep(L[6][0], L[6][0] + 0.5, lt))
    mace_up = sstep(L[6][0] + 0.4, L[6][0] + 1.2, lt)
    TX, TY, TS = 540, 880, 0.62
    SX, SY = TX + 12 * TS, TY - 160 * TS
    crown_at = (SX + 8 * TS, SY - 345 * TS)

    def shadows(cc):
        if th < 0.01:
            return
        shadow_layer(cc, SH_B, 0.86 * th * dim, (56, 22, 14), 2.4)
        throne(cc, TX, TY, TS, 1)
        if fall < 1:
            cc.save()
            cc.saveLayerAlpha(None, int(255 * (1 - fall)))
            if fall > 0:
                px, py = TX + 150 * TS, TY - 160 * TS
                cc.translate(px + 160 * fall, py + 120 * fall * fall)
                cc.rotate(80 * ease(fall))
                cc.translate(-px, -py)
            seated(cc, SX, SY, TS, 1, {"hand": (110, -320), "hand_kind": "open", "rhand": (-30, -262),
                                       "head": -2 + 20 * fall}, t, "kavus")
            cc.restore()
            cc.restore()
        if ro > 0.01:
            cc.save()
            cc.saveLayerAlpha(None, int(255 * ro))
            seated(cc, SX, SY, TS, 1, {"hand_kind": "oxmace", "hand": (mix(110, 70, mace_up), mix(-330, -520, mace_up)),
                                       "mace": mix(10, -10, mace_up), "head": -2, "rhand": (-30, -262)},
                   t, KING_R if cr >= 1 else BARE_R)
            if 0 < cr < 1:
                crown_shape(cc, crown_at[0], mix(300, crown_at[1], ease(cr)), TS)
            cc.restore()
            cc.restore()
        cc.restore()

    def extra(cam, zoom):
        fl = sstep(0.9, 1.0, cr) * math.exp(-max(0.0, lt - L[4][0] - 1.6) * 2.0)
        if fl > 0.01:
            with cam(0.7):
                S.glow(c, crown_at[0], crown_at[1], 170, (255, 226, 160), 150 * fl)
    seated_two(an, c, t, lt, dur, PS, PT, 0.07, shadows, gem_a=0.75, extra=extra)


def p11_s04(an, c, t):
    """The dream grows on the curtain: Sohrab rides against Afrasiab and throws him from his throne; then father and
    son stand side by side, a sun over the one and a moon over the other, while the stars go out."""
    lt, dur = loc(an, "S04", t)
    L = [LN("p11", "S04", k) for k in range(4)]
    focus = (600, 640)
    zoom = 1.0 + 0.06 * ease(lt / dur)
    cam = Cam(c, focus, zoom)
    curtain(c, t)
    sway = 5 * math.sin(t * 1.3)
    a_r = sstep(-1.0, 0.6, lt) * (1 - sstep(L[1][0] - 0.4, L[1][0] + 0.4, lt))     # Rostam enthroned
    a_f = sstep(L[1][0] - 0.3, L[1][0] + 0.5, lt) * (1 - sstep(L[2][0] - 0.5, L[2][0] + 0.2, lt))
    a_2 = sstep(L[2][0] - 0.3, L[2][0] + 0.5, lt)
    ride = clamp((lt - L[1][0] - 0.1) / 2.6)
    hit = L[1][0] + 2.7
    fall = clamp((lt - hit) / 1.0)
    rear = math.sin(clamp((lt - hit + 0.2) / 1.4) * math.pi) * 34 if hit - 0.2 < lt < hit + 1.2 else 0.0
    sky = sstep(L[3][0] - 0.2, L[3][0] + 1.4, lt)
    with cam(0.8):
        if sky > 0.01:
            fl = 0.9 + 0.1 * math.sin(t * 2.0)
            S.glow(c, 380, 440, 360, (255, 220, 140), 170 * sky * fl)
            S.sun(c, 380, 440, 46 * sky, (255, 248, 214), (255, 200, 120), 220, 120 * sky, 9, t)
            S.glow(c, 730, 450, 260, (190, 210, 255), 140 * sky)
            c.saveLayerAlpha(None, int(255 * sky))
            S.moon(c, 730, 450, 34)
            c.restore()
            rnd = random.Random(114)
            for k in range(16):
                sx_, sy_ = rnd.uniform(160, 960), rnd.uniform(320, 600)
                a = (1 - sstep(L[3][0] + 0.6 + k * 0.08, L[3][0] + 1.6 + k * 0.1, lt)) * sstep(L[3][0] - 0.6, L[3][0] + 0.3, lt)
                tw = 0.6 + 0.4 * math.sin(t * 3 + k)
                if a > 0.01:
                    sp = paint(C(255, 246, 220, 230 * a * tw))
                    r = rnd.uniform(5, 9)
                    c.drawPath(ppath([(sx_ - r, sy_), (sx_, sy_ - r * 0.25), (sx_ + r, sy_), (sx_, sy_ + r * 0.25)]), sp)
                    c.drawPath(ppath([(sx_, sy_ - r), (sx_ + r * 0.25, sy_), (sx_, sy_ + r), (sx_ - r * 0.25, sy_)]), sp)
        if a_r > 0.01:
            shadow_layer(c, SH_B, 0.86 * a_r, (44, 20, 14), 2.2)
            c.save()
            c.translate(sway, 0)
            sit_throne(c, 520, 880, 0.66, 1, {"hand_kind": "oxmace", "hand": (110, -330), "mace": 10, "head": -2,
                                             "rhand": (-30, -262)}, t, KING_R)
            c.restore()
            c.restore()
        if a_f > 0.01:
            shadow_layer(c, SH_B, 0.86 * a_f, (44, 20, 14), 2.2)
            c.save()
            c.translate(sway, 0)
            throne(c, 860, 880, 0.62, -1)
            if fall < 1:
                c.saveLayerAlpha(None, int(255 * (1 - fall)))
                px, py = 860 - 0.62 * 12, 880 - 0.62 * 160
                c.translate(px + 150 * fall, py + 150 * fall * fall)
                c.rotate(80 * ease(fall))
                c.translate(-px, -py)
                seated(c, px, py, 0.62, -1, {"hand": (mix(110, 160, sstep(hit - 1.2, hit - 0.4, lt)), -330),
                                             "hand_kind": "open", "rhand": (-30, -262), "head": -2 - 14 * fall}, t, "afrasiab")
                c.restore()
            if ride > 0:
                gx = mix(-250, 560, ease(ride))
                g = {"gait": "rear", "rear": rear} if rear > 1 else {"gait": "gallop", "phase": t * 1.9}
                horse(c, gx, 880, 0.56, 1, dict(g, saddle=True, rider="sohrab",
                                              rider_pose={"hand_kind": "spear", "hand": (130, -380), "lean": 10, "wind": 1.0}), t)
            c.restore()
            c.restore()
        if a_2 > 0.01:
            shadow_layer(c, SH_B, 0.86 * a_2, (44, 20, 14), 2.2)
            c.save()
            c.translate(sway, 0)
            person(c, 380, 880, 0.74, 1, {"hand_kind": "oxmace", "hand": (110, -330), "mace": 10, "head": -3,
                                          "stance": (58, 48), "wind": 0.8}, t, KING_R)
            person(c, 730, 880, 0.7, -1, {"hand_kind": "spear", "hand": (100, -330), "head": -3, "stance": (54, 46),
                                          "wind": 0.8}, t, "sohrab")
            c.restore()
            c.restore()
    point = sstep(L[1][0], L[1][0] + 0.6, lt) * (1 - sstep(L[1][1], L[1][1] + 0.5, lt))
    chest_ = sstep(L[2][0] + 0.2, L[2][0] + 0.7, lt) * (1 - sstep(L[2][1], L[2][1] + 0.5, lt))
    lift = sstep(L[3][0] + 0.2, L[3][0] + 0.9, lt)
    if lift > 0.01:
        h = (mix(110, 120, lift), mix(-300, -470, lift))
    elif chest_ > 0.01:
        h = (mix(110, 30, chest_), mix(-300, -372, chest_))
    else:
        h = (mix(110, 160, point), mix(-300, -400, point))
    PS = {"jaw": jaw(an, "SOHRAB", t, 8), "hand": h, "hand_kind": "open", "rhand": (-30, -262),
          "head": -4 - 3 * lift + 1.2 * math.sin(t * 0.8), "lean": -3 * lift}

    def figs(cc):
        with Cam(cc, focus, zoom)(1.0):
            tag("s:")
            seated(cc, 120, 1260, 1.62, 1, PS, t, YS)
            tag("")
    an.figures(c, figs, WARM, (0, 300, 1080, 1500), anchors=True)
    gem_at(c, "s:hand_up", t, 11 * zoom, 0.8, 0, 0, 1.0, 0.8)
    S.glow(c, 640, 1240, 520, (255, 170, 80), 90 * flick(t))
    vig(an, c, 200)


def p11_s05(an, c, t):
    """Morning at the window: 'War is not a game.' -- 'No man in Samangan can stand against me... but first I need a
    horse.' He strides out."""
    lt, dur = loc(an, "S05", t)
    L = [LN("p11", "S05", k) for k in range(4)]
    plead = sstep(L[0][0], L[0][0] + 0.6, lt) * (1 - sstep(L[1][0] + 0.4, L[1][0] + 1.0, lt))
    chest_ = sstep(L[1][0] + 0.3, L[1][0] + 0.8, lt) * (1 - sstep(L[1][1], L[1][1] + 0.4, lt))
    turn = lt > L[2][0] + 0.3
    think = sstep(L[2][0] + 0.3, L[2][0] + 0.9, lt) * (1 - sstep(L[3][0], L[3][0] + 0.3, lt))
    up = sstep(L[3][0], L[3][0] + 0.4, lt) * (1 - sstep(L[3][1] + 0.1, L[3][1] + 0.5, lt))
    walk = clamp((lt - L[3][1] - 0.15) / 1.4)
    worry = sstep(L[2][0] + 0.3, L[2][0] + 1.0, lt)
    if up > 0.01:
        h, hk = (mix(120, 70, up), mix(-380, -560, up)), "fist"
    elif think > 0.01:
        h, hk = (mix(40, 150, think), mix(-262, -380, think)), "open"
    else:
        h, hk = (mix(40, 30, chest_), mix(-262, -372, chest_)), ("open" if chest_ > 0.3 else "fist")
    PS = {"mode": "walk" if 0 < walk < 1 else "stand", "phase": lt * 4.2, "stride": 18,
          "jaw": jaw(an, "SOHRAB", t, 8), "hand": h, "hand_kind": hk, "rhand": (-30, -262),
          "head": -3 * chest_ - 4 * think - 4 * up + 1.2 * math.sin(t * 0.8), "lean": -2 * chest_ + 6 * (0 < walk < 1),
          "wind": 0.3}
    PT = {"jaw": jaw(an, "TAHMINEH", t, 6),
          "hand": (mix(mix(50, 160, plead), 30, worry), mix(mix(-300, -380, plead), -372, worry)), "hand_kind": "open",
          "rhand": (mix(-30, 20, worry), mix(-262, -380, worry)), "rhand_kind": "open",
          "head": 3 + 2 * plead + 10 * worry + 1.2 * math.sin(t * 0.7), "lean": 4 * plead + 2 * worry, "wind": 0.3}
    dawn_two(an, c, t, lt, dur, PS, 260 - 420 * ease(walk), PT, 830, "dw115", 1.0, mix(1.25, 1.55, lt / dur), 0.06,
             0.8, -1 if turn else 1)


def p11_s06(an, c, t):
    """The training field: the finest horses are brought; under his hand the first sinks to its belly; the king is
    amazed; two more bend; he stands among them with empty hands."""
    lt, dur = loc(an, "S06", t)
    L = [LN("p11", "S06", k) for k in range(5)]
    k_cut = L[2][0] - 0.5
    m1 = L[3][0] - 0.3
    m2 = m1 + 2.7
    fin = L[4][0] - 1.0

    def wide():
        focus = (560, 660)
        zoom = 1.0 + 0.05 * ease(lt / (k_cut + 0.6))
        cam = Cam(c, focus, zoom)
        meydan(an, c, t, cam, 0.25, "md116")
        led = clamp(lt / 3.9)
        hx, hs = mix(1350, 520, ease(led)), 0.86
        hm = mix(1060, 230, ease(led))
        wk = clamp((lt - L[1][0]) / 1.6)
        sx = mix(1180, 760, ease(wk))
        sink_u = clamp((lt - L[1][1] + 0.2) / 1.9)
        sink, lie, rel = collapse(sink_u)
        press = sstep(L[1][0] + 2.2, L[1][0] + 2.8, lt) * (1 - rel)
        sx += 40 * rel
        PH = {"gait": "walk" if 0 < led < 1 else "stand", "phase": t * 0.9, "sink": sink, "lie": lie,
              "neck": 4 * math.sin(t * 1.6) * (1 - sink_u) + 14 * sink - 18 * lie, "head": 10 * sink - 4 * lie, "tail": 6}
        cx, cy = croup(hx, 870, hs, -1, sink, -150, lie)
        hand = to_local(cx, cy, sx, 870, 0.84, -1)
        PS = {"mode": "walk" if 0 < wk < 1 else "stand", "phase": lt * 4.2, "stride": 18,
              "hand": (mix(40, hand[0], press), mix(-262, hand[1], press)), "hand_kind": "open",
              "rhand": (mix(-30, hand[0] - 20, press), mix(-262, hand[1] + 4, press)), "rhand_kind": "open",
              "head": 2 + 8 * press + 6 * rel, "lean": 3 * (0 < wk < 1) + 10 * press + 6 * sink * (1 - rel), "stance": (56, 48),
              "wind": 0.5}
        PM = {"mode": "walk" if 0 < led < 1 else "stand", "phase": t * 3.4, "stride": 16, "hand": (110, -330),
              "hand_kind": "open", "rprop": "staff", "rhand": (-20, -300), "head": 3 + 6 * sink, "lean": -4 * sink}

        def figs(cc):
            with Cam(cc, focus, zoom)(1.0):
                tag("h:")
                horse(cc, hx, 870, hs, -1, PH, t)
                tag("m:")
                person(cc, hm, 870, 0.8, -1, PM, t, "herdsman")
                tag("s:")
                if lt > L[1][0] - 0.1:
                    person(cc, sx, 870, 0.84, -1, PS, t, YS)
                tag("")
            rope(cc, A("m:hand"), A("h:mouth"), 26, 2.2)
        an.figures(c, figs, DAY, (0, 200, 1080, 1000), anchors=True)
        if sink_u > 0.7:
            u = clamp((lt - L[1][1] + 0.2 - 0.75 * 1.9) / 1.8)
            for k in range(4):
                S.dust(c, 420 + k * 80, 862 - 20 * u, 40 + 110 * u, t, (232, 204, 156), 140 * (1 - u), k)
        vig(an, c, 140)

    def king():
        focus = (620, 680)
        zoom = 1.12 + 0.05 * ease((lt - k_cut) / (m1 - k_cut))
        cam = Cam(c, focus, zoom)
        meydan(an, c, t, cam, 0.3, "md116")
        amaze = sstep(L[2][0] - 0.1, L[2][0] + 0.5, lt)
        PK = {"jaw": jaw(an, "KING_SAMANGAN", t, 7), "hand": (mix(40, 120, amaze), mix(-262, -500, amaze)),
              "hand_kind": "open" if amaze > 0.3 else "fist", "rhand": (mix(-30, -70, amaze), mix(-262, -480, amaze)),
              "rhand_kind": "open" if amaze > 0.3 else "fist", "head": 3 - 6 * amaze + 1.2 * math.sin(t * 0.6),
              "lean": -5 * amaze}

        def figs(cc):
            with Cam(cc, focus, zoom)(0.7):
                horse(cc, 260, 866, 0.5, -1, {"gait": "stand", "sink": 0.85, "lie": 1.0, "neck": -4, "head": 6}, t)
            with Cam(cc, focus, zoom)(1.0):
                person(cc, 700, 1330, 1.45, -1, PK, t, "king")
        an.figures(c, figs, DAY, (0, 150, 1080, 1500))
        vig(an, c, 150)

    def close(lt0, face, hx, hdx):
        focus = (540, 760)
        zoom = 1.0 + 0.05 * ease((lt - lt0) / 2.8)
        cam = Cam(c, focus, zoom)
        meydan(an, c, t, cam, 0.35, "md116")
        hs = 1.1
        sink_u = clamp((lt - lt0 - 0.5) / 1.6)
        sink, lie, rel = collapse(sink_u)
        press = sstep(lt0 + 0.1, lt0 + 0.5, lt) * (1 - rel)
        sx = hx + hdx - 30 * rel * face
        cx, cy = croup(hx, 1010, hs, face, sink, -150, lie)
        hand = to_local(cx, cy, sx, 1010, 1.1, face)
        PS = {"hand": (mix(70, hand[0], press), mix(-300, hand[1], press)), "hand_kind": "open",
              "rhand": (mix(40, hand[0] - 22, press), mix(-300, hand[1] + 6, press)), "rhand_kind": "open",
              "head": 6 + 6 * press, "lean": 8 * (1 - rel) + 6 * press + 6 * sink * (1 - rel), "stance": (60, 50), "wind": 0.5}
        PH = {"gait": "stand", "sink": sink, "lie": lie, "neck": 6 * math.sin(t * 2.0) * (1 - sink_u) + 16 * sink - 20 * lie,
              "head": 10 * sink - 4 * lie + 4 * math.sin(t * 1.4), "tail": 8, "wind": 0.7}

        def figs(cc):
            with Cam(cc, focus, zoom)(1.0):
                horse(cc, hx, 1010, hs, face, PH, t)
                tag("s:")
                person(cc, sx, 1010, 1.1, face, PS, t, YS)
                tag("")
        an.figures(c, figs, DAY, (0, 150, 1080, 1300), anchors=True)
        gem_at(c, "s:hand_up", t, 7 * zoom, 0.6, 0, 0, 1.0, 0.4)
        if sink_u > 0.7:
            u = clamp((lt - lt0 - 0.5 - 0.75 * 1.6) / 1.4)
            for k in range(4):
                S.dust(c, hx - 160 + k * 100, 990 - 20 * u, 60 + 120 * u, t, (232, 204, 156), 120 * (1 - u), k + 5)
        vig(an, c, 150)

    def final():
        focus = (540, 700)
        zoom = 1.0 + 0.06 * ease((lt - fin) / (dur - fin))
        cam = Cam(c, focus, zoom)
        meydan(an, c, t, cam, 0.5, "md116")
        op = sstep(L[4][0] - 0.2, L[4][0] + 0.5, lt)
        shake = 3 * math.sin(t * 5) * sstep(L[4][0] + 0.6, L[4][0] + 1.0, lt) * (1 - sstep(L[4][1], L[4][1] + 0.6, lt))
        PS = {"jaw": jaw(an, "SOHRAB", t, 8), "hand": (mix(40, 170, op), mix(-262, -400, op)), "hand_kind": "open",
              "rhand": (mix(-30, -150, op), mix(-262, -400, op)), "rhand_kind": "open",
              "head": -6 * op + shake, "lean": -2 * op, "wind": 0.5}

        def figs(cc):
            with Cam(cc, focus, zoom)(0.75):
                for (x, s_, f, sd) in ((640, 0.62, -1, 0.0), (900, 0.56, 1, 1.0)):
                    horse(cc, x, 862, s_, f, {"gait": "stand", "sink": 0.85, "lie": 1.0, "neck": -4 + 3 * math.sin(t + sd),
                                              "head": 6, "tail": 4}, t)
            with Cam(cc, focus, zoom)(1.0):
                tag("s:")
                person(cc, 330, 1330, 1.42, 1, PS, t, YS)
                tag("")
        an.figures(c, figs, NOON, (0, 150, 1080, 1500), anchors=True)
        gem_at(c, "s:hand_up", t, 8 * zoom, 0.6, 0, 0, 1.0, 0.5)
        vig(an, c, 150)

    dissolve(c, lt, k_cut, 0.5, wide,
             lambda: dissolve(c, lt, m1, 0.45, king,
                              lambda: dissolve(c, lt, m2, 0.45, lambda: close(m1, 1, 650, -320),
                                               lambda: dissolve(c, lt, fin, 0.5, lambda: close(m2, -1, 430, 330), final))))


def p11_s07(an, c, t):
    """Turn + end: at sunset the old herdsman tells of a wild colt in the high pastures -- 'They say his father was
    Rakhsh' -- far off, a colt rears against the setting sun. 'Bring him to me!'"""
    lt = t - an.start["S07"]
    dur = an.end["END"] - an.start["S07"]
    L = [LN("p11", "S07", k) for k in range(4)]
    end0 = an.start["END"] - an.start["S07"]
    focus = (640, 690)
    zoom = 1.0 + 0.05 * ease(lt / end0) + 0.14 * ease(clamp((lt - end0) / (dur - end0)))
    cam = Cam(c, focus, zoom)
    mood = 1.75
    meydan(an, c, t, cam, mood, "md117", lambda cm: colt_hill(an, c, cm, mood))
    walk = clamp(lt / 2.2)
    hx = mix(1180, 930, ease(walk))
    point = sstep(L[0][1] - 2.4, L[0][1] - 1.8, lt) * (1 - sstep(L[1][1], L[1][1] + 0.6, lt))
    turn_s = sstep(L[2][0] + 0.4, L[2][0] + 1.2, lt)
    sp = sstep(L[3][0] + 0.2, L[3][0] + 0.7, lt)
    run = clamp((lt - L[1][0] - 0.4) / 3.0)
    cx = mix(1200, 772, ease(run))
    rears = [(L[2][0] + 1.0, L[2][0] + 2.6), (end0 + 1.4, end0 + 3.0)]
    rr = 0.0
    for a, b in rears:
        if a <= lt <= b:
            rr = math.sin((lt - a) / (b - a) * math.pi) * 40
    if run < 1:
        PC = {"gait": "gallop", "phase": t * 1.9}
    elif rr > 1:
        PC = {"gait": "rear", "rear": rr}
    else:
        PC = {"gait": "stand", "neck": 8 * math.sin(t * 2.1), "head": 6 * math.sin(t * 1.3), "wind": 0.9}
    PM = {"mode": "walk" if 0 < walk < 1 else "stand", "phase": lt * 3.4, "stride": 14, "jaw": jaw(an, "HERDSMAN", t, 9),
          "hand": (mix(40, 160, point), mix(-262, -500, point)), "hand_kind": "open" if point > 0.3 else "fist",
          "rprop": "staff", "rhand": (-20, -300), "head": 4 - 6 * point + 1.2 * math.sin(t * 0.6), "lean": 4}
    PS = {"jaw": jaw(an, "SOHRAB", t, 8), "hand": (mix(40, 180, sp), mix(-262, -470, sp)), "hand_kind": "open" if sp > 0.3 else "fist",
          "rhand": (-30, -262), "head": 2 - 6 * turn_s - 3 * sp + 1.2 * math.sin(t * 0.8), "lean": 4 * sp, "wind": 0.6,
          "mode": "walk" if 0 < sstep(L[3][0] + 0.3, L[3][0] + 1.6, lt) < 1 else "stand", "phase": lt * 4.0, "stride": 14}
    sxp = mix(230, 300, sstep(L[3][0] + 0.3, L[3][0] + 1.6, lt))

    def colt(cc):
        with Cam(cc, focus, zoom)(0.3):
            if lt > L[1][0] + 0.3:
                horse(cc, cx, HILL(cx) + 5, 0.24, -1, PC, t)
    an.figures(c, colt, COLT, (500, 400, 1200, 900), alpha=210, sigma=2.4)

    def figs(cc):
        with Cam(cc, focus, zoom)(1.0):
            tag("s:")
            person(cc, sxp, 1330, 1.42, 1, PS, t, YS)
            tag("")
            person(cc, hx, 1330, 1.45, -1, PM, t, "herdsman")
    an.figures(c, figs, SUNSET, (0, 150, 1080, 1500), anchors=True)
    gem_at(c, "s:hand_up", t, 8 * zoom, 0.7, 0, 0, 1.0, 0.6 + 0.6 * sp)
    vig(an, c, 160)


# ================================================================== part 12 shots
def colt_test(an, c, t, lt, T, dawn, zoom, focus=(560, 680), cheer=(0.0, 0.0), stroke=None, joy=None):
    """The high pasture: the herdsman holds the wild colt on a lasso; Sohrab walks up, lays his hands on its back and
    presses; the colt holds. T = (walk0, walk1, rear0, rear1, press0)."""
    w0, w1, r0, r1, p0 = T
    cam = Cam(c, focus, zoom)
    pasture(an, c, t, cam, dawn, "pa12")
    walk = clamp((lt - w0) / (w1 - w0))
    sx = mix(-140, 400, ease(walk))
    rr = math.sin(clamp((lt - r0) / (r1 - r0)) * math.pi) * 36 if r0 <= lt <= r1 else 0.0
    press = sstep(p0, p0 + 0.6, lt)
    hold = sstep(p0 + 0.4, p0 + 0.8, lt)
    jit = 0.035 * hold * (0.5 + 0.5 * math.sin(lt * 9)) * (1 - (sstep(stroke, stroke + 0.5, lt) if stroke else 0.0))
    st = sstep(stroke, stroke + 0.6, lt) if stroke else 0.0
    jy = sstep(joy, joy + 0.4, lt) * (1 - (sstep(stroke - 0.4, stroke, lt) if stroke else 0.0)) if joy else 0.0
    hx, hy, hs = 640, 874, 0.82
    if rr > 1:
        PC = {"gait": "rear", "rear": rr, "wind": 1.0}
    else:
        PC = {"gait": "stand", "sink": jit, "neck": 10 * math.sin(t * 2.3) * (1 - hold) - 8 * hold * (1 - st) + 20 * st,
              "head": 5 * math.sin(t * 1.7) * (1 - hold) - 6 * hold + 8 * st, "tail": 10 * math.sin(t * 2.0), "wind": 0.9}
    cx, cy = croup(hx, hy, hs, 1, jit if rr <= 1 else 0.0, -140)
    hand = to_local(cx, cy, sx, hy, 0.84, 1)
    pat = 6 * math.sin(lt * 8) * st
    if jy > 0.01:
        h, hk = (mix(hand[0], 70, jy), mix(hand[1], -560, jy)), "fist"
    else:
        h, hk = (mix(40, hand[0], press), mix(-262, hand[1] + pat, press)), "open"
    PS = {"mode": "walk" if 0 < walk < 1 else "stand", "phase": lt * 4.2, "stride": 18, "jaw": jaw(an, "SOHRAB", t, 8),
          "hand": h, "hand_kind": hk, "rhand": (mix(-30, hand[0] - 24, press * (1 - st)), mix(-262, hand[1] + 6, press * (1 - st))),
          "rhand_kind": "open", "head": 2 + 8 * press * (1 - jy) - 6 * jy - 4 * st,
          "lean": 3 * (0 < walk < 1) + 10 * hold * (1 - jy) * (1 - st) + 3 * st, "stance": (60, 50), "wind": 0.6}
    ch = sstep(cheer[0], cheer[0] + 0.5, lt) * (1 - sstep(cheer[1], cheer[1] + 0.8, lt)) if cheer[1] > 0 else 0.0
    tug = rr / 36.0
    PM = {"jaw": jaw(an, "HERDSMAN", t, 9), "hand": (mix(mix(100, 80, tug), 110, ch), mix(mix(-330, -300, tug), -520, ch)),
          "hand_kind": "fist" if ch < 0.3 else "open", "rhand": (mix(mix(60, 40, tug), -60, ch), mix(mix(-320, -300, tug), -500, ch)),
          "rhand_kind": "fist" if ch < 0.3 else "open", "head": 4 - 4 * ch + 1.2 * math.sin(t * 0.6),
          "lean": -8 * tug - 4 * ch, "stance": (60, 54)}

    def colt_fig(cc):
        with Cam(cc, focus, zoom)(1.0):
            horse(cc, hx, hy, hs, 1, PC, t)
    an.figures(c, colt_fig, COLT, (0, 200, 1080, 1000), alpha=200)

    def figs(cc):
        with Cam(cc, focus, zoom)(1.0):
            if Pen.mode == "anchor":
                tag("c:")
                horse(cc, hx, hy, hs, 1, PC, t)
            tag("m:")
            person(cc, 950, hy, 0.8, -1, PM, t, "herdsman")
            tag("s:")
            if sx > -120:
                person(cc, sx, hy, 0.84, 1, PS, t, YS)
            tag("")
        rope(cc, A("m:hand"), A("c:neck"), 24 + 20 * tug - 14 * ch, 2.2)
    an.figures(c, figs, mixc(DAWN, DAY, dawn), (0, 200, 1080, 1000), anchors=True)
    gem_at(c, "s:hand_up", t, 6 * zoom, 0.6, 0, 0, 1.0, 0.4 + 0.6 * jy)
    vig(an, c, 140)


def p12_s01(an, c, t):
    """Hook + title: at dawn in the high pasture the wild colt rears; Sohrab presses its back -- it does not bend."""
    lt = t - an.start["S01"]
    dur = an.end["TITLE"] - an.start["S01"]
    a0, a1 = LN("p12", "S01", 0)
    b0, b1 = LN("p12", "S01", 1)
    colt_test(an, c, t, lt, (0.4, 2.8, 0.2, 2.2, 3.0), mix(0.45, 0.7, lt / dur), 1.0 + 0.08 * ease(lt / dur),
              joy=b0 + 1.2, stroke=dur - 3.0)


def p12_s02(an, c, t):
    """Recap: every horse of Samangan bends under his hand; then the herdsman leads him up to the high pasture where
    the wild colt grazes -- and Rakhsh's ghost runs in the sky."""
    lt, dur = loc(an, "S02", t)
    L = [LN("p12", "S02", k) for k in range(4)]
    cut = L[1][1] + 0.3

    def field():
        focus = (560, 660)
        zoom = 1.0 + 0.05 * ease(lt / (cut + 0.8))
        cam = Cam(c, focus, zoom)
        meydan(an, c, t, cam, 0.3, "md122")
        hx, hs = 520, 0.86
        sink_u = clamp((lt - L[1][0] - 1.0) / 1.9)
        sink, lie, rel = collapse(sink_u)
        press = sstep(L[1][0] + 0.2, L[1][0] + 0.8, lt) * (1 - rel)
        sx = 760 + 40 * rel
        cx, cy = croup(hx, 870, hs, -1, sink, -150, lie)
        hand = to_local(cx, cy, sx, 870, 0.84, -1)
        fist = sstep(L[0][0] + 1.6, L[0][0] + 2.2, lt) * (1 - sstep(L[0][1], L[0][1] + 0.5, lt))
        if press > 0.01:
            h = (mix(40, hand[0], press), mix(-262, hand[1], press))
        else:
            h = (mix(40, 70, fist), mix(-262, -540, fist))
        PS = {"hand": h, "hand_kind": "open" if press > 0.3 else "fist",
              "rhand": (mix(-30, hand[0] - 20, press), mix(-262, hand[1] + 4, press)), "rhand_kind": "open",
              "head": 2 - 5 * fist + 8 * press, "lean": 10 * press + 6 * sink, "stance": (56, 48), "wind": 0.5}
        PH = {"gait": "stand", "sink": sink, "lie": lie, "neck": 4 * math.sin(t * 1.6) * (1 - sink_u) + 14 * sink - 18 * lie,
              "head": 10 * sink - 4 * lie}

        def figs(cc):
            with Cam(cc, focus, zoom)(1.0):
                horse(cc, hx, 870, hs, -1, PH, t)
                tag("s:")
                person(cc, sx, 870, 0.84, -1, PS, t, YS)
                tag("")
        an.figures(c, figs, DAY, (0, 200, 1080, 1000), anchors=True)
        if sink_u > 0.7:
            u = clamp((lt - L[1][0] - 1.0 - 0.75 * 1.9) / 1.6)
            for k in range(4):
                S.dust(c, 400 + k * 80, 862 - 20 * u, 40 + 110 * u, t, (232, 204, 156), 140 * (1 - u), k)
        vig(an, c, 140)

    def climb():
        lt2 = lt - cut
        focus = (600, 690)
        zoom = 1.0 + 0.07 * ease(lt2 / (dur - cut))
        cam = Cam(c, focus, zoom)
        dawn = mix(0.25, 0.45, lt2 / (dur - cut))
        pasture(an, c, t, cam, dawn, "pa12")
        walk = clamp((lt2 + 0.6) / 4.6)
        look = sstep(L[3][0] - cut, L[3][0] - cut + 0.8, lt)
        ghost = sstep(L[3][0] + 0.6, L[3][0] + 1.8, lt) * (1 - sstep(dur - 1.0, dur, lt))
        if ghost > 0.01:
            with cam(0.2):
                ghost_layer(c, (0, 250, W, 820), 0.5 * ghost, (255, 190, 200), 3.0)
                u = clamp((lt - L[3][0] - 0.6) / 4.0)
                horse(c, mix(200, 760, u), 560, 0.5, 1, {"gait": "gallop", "phase": t * 1.6, "wind": 1.0}, t)
                c.restore()
        hm_x, s_x = mix(-160, 300, ease(walk)), mix(-360, 120, ease(walk))
        PM = {"mode": "walk" if 0 < walk < 1 else "stand", "phase": lt * 3.4, "stride": 14, "rprop": "staff",
              "rhand": (-20, -300), "hand": (mix(40, 160, look), mix(-262, -460, look)), "hand_kind": "open" if look > 0.3 else "fist",
              "head": 3 - 4 * look, "lean": 5 * (0 < walk < 1)}
        PS = {"mode": "walk" if 0 < walk < 1 else "stand", "phase": lt * 4.0 + 1.0, "stride": 16,
              "head": -2 - 5 * look + 1.2 * math.sin(t * 0.8), "lean": 4 * (0 < walk < 1), "wind": 0.6}
        PC = {"gait": "stand", "neck": 62 * (1 - look) + 6 * look, "head": 14 * (1 - look) + 4 * math.sin(t * 1.3),
              "tail": 8 * math.sin(t * 1.7), "wind": 0.8}

        def colt_fig(cc):
            with Cam(cc, focus, zoom)(1.0):
                horse(cc, 830, 874, 0.62, -1, PC, t)
        an.figures(c, colt_fig, COLT, (0, 200, 1080, 1000), alpha=200)

        def figs(cc):
            with Cam(cc, focus, zoom)(1.0):
                person(cc, hm_x, 874, 0.78, 1, PM, t, "herdsman")
                tag("s:")
                person(cc, s_x, 874, 0.8, 1, PS, t, YS)
                tag("")
        an.figures(c, figs, DAWN, (0, 200, 1080, 1000), anchors=True)
        gem_at(c, "s:hand_up", t, 6 * zoom, 0.5, 0, 0, 1.0, 0.4)
        vig(an, c, 140)

    dissolve(c, lt, cut, 0.8, field, climb)


def p12_s03(an, c, t):
    """The test: he walks up to the lassoed colt, lays his hands on its back and presses with all his strength; it
    stands like a mountain; the herdsman cheers; Sohrab pats its back."""
    lt, dur = loc(an, "S03", t)
    L = [LN("p12", "S03", k) for k in range(4)]
    colt_test(an, c, t, lt, (0.0, 2.4, 0.3, 1.9, 3.0), mix(0.5, 0.65, lt / dur), 1.04 + 0.08 * ease(lt / dur),
              (580, 680), cheer=(L[2][0] - 0.2, L[2][1]), stroke=L[3][0] + 0.3)


def p12_s04(an, c, t):
    """He rides the colt out like the wind: 'Faster! King Kavus, get ready!'"""
    lt, dur = loc(an, "S04", t)
    L = [LN("p12", "S04", k) for k in range(3)]
    gallop_sky(c, t)
    S.sun(c, 860, 700, 80, (255, 248, 220), (255, 214, 150), 480, 140)
    sc = get(an, "sc124", lambda: Scroller(141))
    sc.draw(c, lt, 900, [(150, 140, 170), (90, 80, 100), (40, 30, 34)])
    for k in range(5):
        u = ((lt * 2.2 + k * 0.2) % 1.0)
        S.dust(c, 330 - u * 380, 860 - u * 40, 40 + u * 90, t, (220, 190, 150), 90 * (1 - u), k)
    fist = sstep(L[1][0], L[1][0] + 0.4, lt) * (1 - sstep(L[1][1] + 0.4, L[1][1] + 0.9, lt))
    P = {"gait": "gallop", "phase": t * 1.95, "saddle": True, "rider": YS, "rider_scale": 0.86, "wind": 1.0,
         "rider_pose": {"lean": 12 - 8 * fist, "hand": (mix(110, 60, fist), mix(-320, -570, fist)), "hand_kind": "fist",
                        "rhand": (60, -300), "head": 4 - 6 * fist, "wind": 1.2, "jaw": jaw(an, "SOHRAB", t, 8)}}

    def figs(cc):
        tag("r:")
        horse(cc, 520, 872, 0.84, 1, P, t)
        tag("")
    an.figures(c, figs, (255, 176, 156), (0, 200, 1080, 1000), anchors=True)
    gem_at(c, "r:hand_up", t, 5, 0.6, 0, 0, 1.0, 0.4)
    vig(an, c, 130)


def p12_s05(an, c, t):
    """The king's hall: 'Grandfather, I am going to war against Kavus.' -- 'You are only a boy!' The old king looks
    at him a long time, smiles, and lays his hand on his shoulder: 'Take my gold, my weapons and my horses.'"""
    lt, dur = loc(an, "S05", t)
    L = [LN("p12", "S05", k) for k in range(5)]
    focus = (540, 640)
    zoom = 1.0 + 0.06 * ease(lt / dur)
    cam = Cam(c, focus, zoom)
    with cam(0.6):
        hall(an, c, t)
        for k, x in enumerate((260, 540, 820)):
            S.hanging_lamp(c, x, 300, 1.0, t, 160, k)
    with cam(0.9):
        ground(c, 900, (40, 18, 12))
    step = sstep(L[0][0], L[0][0] + 0.8, lt)
    fist = sstep(L[0][0] + 0.8, L[0][0] + 1.3, lt) * (1 - sstep(L[0][1], L[0][1] + 0.4, lt))
    chest_ = sstep(L[2][0] + 0.2, L[2][0] + 0.7, lt) * (1 - sstep(L[2][0] + 2.0, L[2][0] + 2.5, lt))
    beg = sstep(L[2][0] + 2.2, L[2][0] + 2.7, lt) * (1 - sstep(L[3][0] + 0.5, L[3][0] + 1.2, lt))
    alarm = sstep(L[1][0] - 0.1, L[1][0] + 0.4, lt) * (1 - sstep(L[1][1] + 0.3, L[1][1] + 1.0, lt))
    look = sstep(L[3][0] + 0.4, L[3][0] + 1.4, lt) * (1 - sstep(L[3][1] - 1.4, L[3][1] - 0.6, lt))
    nod = sstep(L[3][1] - 1.2, L[3][1] - 0.4, lt)
    kwalk = clamp((lt - L[4][0] + 0.2) / 1.4)
    kx = mix(800, 680, ease(kwalk))
    sx = mix(260, 300, step) + 60 * ease(clamp((lt - L[4][0] - 0.2) / 1.2))
    bless = sstep(L[4][1] - 2.0, L[4][1] - 1.4, lt)
    shoulder = (sx + 1.42 * 18, 1340 - 1.42 * 404)
    sh_l = to_local(shoulder[0], shoulder[1], kx, 1360, 1.55, -1)
    touch = sstep(L[4][0] + 1.0, L[4][0] + 1.6, lt)
    if chest_ > 0.01:
        h, hk = (mix(40, 30, chest_), mix(-262, -372, chest_)), "open"
    elif beg > 0.01:
        h, hk = (mix(40, 160, beg), mix(-262, -360, beg)), "open"
    else:
        h, hk = (mix(40, 70, fist), mix(-262, -470, fist)), "fist"
    sw = 0 < step < 1 or 0 < (lt - L[4][0] - 0.2) / 1.2 < 1
    PS = {"mode": "walk" if sw else "stand", "phase": lt * 4.0, "stride": 12, "jaw": jaw(an, "SOHRAB", t, 8),
          "hand": h, "hand_kind": hk, "rhand": (-30, -262), "head": -3 * fist + 2 * beg - 3 * touch + 1.2 * math.sin(t * 0.8),
          "lean": 3 * fist + 4 * beg, "wind": 0.2, "stance": (mix(46, 34, touch), 40)}
    if touch > 0.01:
        kh = (mix(40, sh_l[0], touch), mix(-262, sh_l[1], touch))
    elif alarm > 0.01:
        kh = (mix(40, 120, alarm), mix(-262, -470, alarm))
    else:
        kh = (40, -262)
    PK = {"mode": "walk" if 0 < kwalk < 1 else "stand", "phase": lt * 3.4, "stride": 12, "jaw": jaw(an, "KING_SAMANGAN", t, 7),
          "hand": kh, "hand_kind": "open" if max(alarm, touch) > 0.3 else "fist",
          "rhand": (mix(-30, -60, alarm), mix(-262, -460, alarm)), "rhand_kind": "open" if alarm > 0.3 else "fist",
          "stance": (mix(46, 34, touch), 40),
          "head": 2 - 6 * alarm + 10 * look - 6 * nod + 3 * math.sin(lt * 5) * sstep(L[3][1] - 1.0, L[3][1] - 0.6, lt) * (1 - sstep(L[3][1], L[3][1] + 0.4, lt))
          + 1.2 * math.sin(t * 0.6),
          "lean": -5 * alarm + 3 * look + 4 * touch - 2 * bless}

    def figs(cc):
        with Cam(cc, focus, zoom)(1.0):
            tag("s:")
            person(cc, sx, 1340, 1.42, 1, PS, t, YS)
            tag("")
            person(cc, kx, 1360, 1.55, -1, PK, t, "king")
    an.figures(c, figs, (255, 190, 116), (0, 150, 1080, 1500), anchors=True)
    gem_at(c, "s:hand_up", t, 8 * zoom, 0.7, 0, 0, 1.0, 0.6)
    vig(an, c, 160)


def p12_s06(an, c, t):
    """Warriors ride in from every side to the tents; the war drums beat on the gate towers; his mother comes to him
    in tears and lays her hand on the jewel on his arm: 'One day, you will need it.'"""
    lt, dur = loc(an, "S06", t)
    L = [LN("p12", "S06", k) for k in range(5)]
    c1 = L[1][0] - 0.3
    c2 = L[2][0] - 0.5

    def plain():
        focus = (540, 700)
        zoom = 1.0 + 0.05 * ease(lt / (c1 + 0.8))
        cam = Cam(c, focus, zoom)
        camp(an, c, t, cam, "cp126")

        def figs(cc):
            with Cam(cc, focus, zoom)(0.85):
                for i in range(5):
                    x = -260 + 110 * lt + i * 150
                    horse(cc, x, 864 - (i % 2) * 6, 0.3 - (i % 2) * 0.03, 1,
                          {"gait": "gallop", "phase": t * 1.9 + i * 0.37, "saddle": True, "rider": "warrior_tu",
                           "rider_pose": {"hand_kind": "spear", "hand": (110, -340), "lean": 8}}, t)
                for i in range(4):
                    x = 1320 - 90 * lt - i * 170
                    horse(cc, x, 870 - (i % 2) * 6, 0.32 - (i % 2) * 0.03, -1,
                          {"gait": "walk", "phase": t * 0.9 + i * 0.3, "saddle": True, "rider": "rider",
                           "rider_pose": {"hand_kind": "spear", "hand": (100, -330)}}, t)
        an.figures(c, figs, DAY, (0, 300, 1080, 1000))
        for k in range(4):
            u = ((lt * 1.6 + k * 0.25) % 1.0)
            S.dust(c, -150 + 110 * lt + 200 * k - 80, 856, 40 + 60 * u, t, (232, 204, 156), 70 * (1 - u), k)
        vig(an, c, 140)

    def court():
        lt2 = lt - c1
        focus = (560, 660)
        zoom = 1.0 + 0.05 * ease(lt2 / (c2 - c1 + 0.6))
        cam = Cam(c, focus, zoom)
        courtyard(an, c, t, cam, "cy126")
        beat = sstep(0.0, 0.8, lt2)
        with cam(0.7):
            Pen.mode = "fill"
            for (x, f, sd) in ((300, 1, 0.0), (790, -1, 1.7)):
                c.drawRect(skia.Rect.MakeLTRB(x - 70, 640, x + 70, 742), paint(C(*INK)))
                for k in range(4):
                    c.drawRect(skia.Rect.MakeLTRB(x - 70 + k * 40, 624, x - 50 + k * 40, 640), paint(C(*INK)))
                drummer(c, x - 40 * f, 640, 0.3, f, t, beat, sd)
                drum_rings(c, x + 0.3 * 110 * f - 40 * f, 610, t, beat, sd)
        walk = clamp((lt2 - 0.3) / 3.4)
        tx = mix(1160, 720, ease(walk))
        wipe = sstep(2.6, 3.2, lt2)
        PT = {"mode": "walk" if 0 < walk < 1 else "stand", "phase": lt2 * 3.4, "stride": 14,
              "hand": (mix(40, 40, wipe), mix(-262, -470, wipe)), "hand_kind": "open", "rhand": (-30, -262),
              "head": 10 + 4 * wipe, "lean": 4, "wind": 0.5}
        PS = {"hand": (40, -262), "rhand": (-30, -262), "head": 2 + 1.2 * math.sin(t * 0.8), "stance": (52, 46), "wind": 0.5}

        def figs(cc):
            with Cam(cc, focus, zoom)(1.0):
                tag("s:")
                person(cc, 400, 870, 0.9, 1, PS, t, YS)
                tag("")
                person(cc, tx, 870, 0.92, -1, PT, t, TAHM)
        an.figures(c, figs, DAY, (0, 200, 1080, 1000), anchors=True)
        gem_at(c, "s:hand_up", t, 5 * zoom, 0.6, 0, 0, 1.0, 0.4)
        vig(an, c, 140)

    def close():
        lt3 = lt - c2
        focus = (540, 700)
        zoom = 1.06 + 0.06 * ease(lt3 / (dur - c2))
        cam = Cam(c, focus, zoom)
        courtyard(an, c, t, cam, "cy126")
        with cam(0.7):
            Pen.mode = "fill"
            for (x, f, sd) in ((300, 1, 0.0), (790, -1, 1.7)):
                c.drawRect(skia.Rect.MakeLTRB(x - 70, 640, x + 70, 742), paint(C(*INK)))
                for k in range(4):
                    c.drawRect(skia.Rect.MakeLTRB(x - 70 + k * 40, 624, x - 50 + k * 40, 640), paint(C(*INK)))
                drummer(c, x - 40 * f, 640, 0.3, f, t, 0.7, sd)
        step = clamp((lt - L[2][0] + 0.2) / 1.0)
        tx = mix(780, 610, ease(step))
        sx = mix(260, 330, sstep(L[4][0], L[4][0] + 0.6, lt))
        show = sstep(L[2][0] + 0.2, L[2][0] + 0.8, lt) * (1 - sstep(L[4][0] - 0.3, L[4][0] + 0.3, lt))
        reach = sstep(L[2][0] + 0.6, L[2][0] + 1.3, lt) * (1 - sstep(L[4][0] - 0.2, L[4][0] + 0.4, lt))
        comfort = sstep(L[4][0] + 0.1, L[4][0] + 0.8, lt)
        sh_t = (tx - 1.5 * 12, 1330 - 1.5 * 404)
        sl = to_local(sh_t[0], sh_t[1], sx, 1330, 1.42, 1)
        if comfort > 0.01:
            sh, shk = (mix(150, sl[0], comfort), mix(-330, sl[1], comfort)), "open"
        else:
            sh, shk = (mix(40, 150, show), mix(-262, -330, show)), "fist"
        PS = {"jaw": jaw(an, "SOHRAB", t, 8), "hand": sh, "hand_kind": shk, "rhand": (-30, -262),
              "head": 4 + 6 * show - 4 * comfort + 1.2 * math.sin(t * 0.8), "lean": 2 * comfort, "wind": 0.5}
        lift = sstep(L[3][0], L[3][0] + 0.6, lt)

        def figs(cc):
            with Cam(cc, focus, zoom)(1.0):
                tag("s:")
                person(cc, sx, 1330, 1.42, 1, PS, t, YS)
                up = A("s:hand_up")
                tl = (150, -350)
                if up:          # her hand goes to the jewel on his arm (undo the camera to get the world point)
                    wx = focus[0] + (up[0] - focus[0]) / zoom
                    wy = focus[1] + (up[1] - focus[1]) / zoom
                    tl = to_local(wx, wy, tx, 1330, 1.5, -1)
                PT = {"jaw": jaw(an, "TAHMINEH", t, 6), "hand": (mix(40, tl[0], reach), mix(-262, tl[1], reach)),
                      "hand_kind": "open", "rhand": (mix(-30, 20, lift), mix(-262, -380, lift)), "rhand_kind": "open",
                      "head": 8 + 4 * reach + 1.2 * math.sin(t * 0.7), "lean": 4 + 3 * reach,
                      "mode": "walk" if 0 < step < 1 else "stand", "phase": lt * 3.4, "stride": 12, "wind": 0.5}
                tag("t:")
                person(cc, tx, 1330, 1.5, -1, PT, t, TAHM)
                tag("")
        an.figures(c, figs, DAY, (0, 150, 1080, 1500), anchors=True)
        gl = 0.6 + 1.6 * reach
        gem_at(c, "s:hand_up", t, 9 * zoom, 1.0, 0, 0, 1.0, gl)
        vig(an, c, 160)

    dissolve(c, lt, c1, 0.6, plain, lambda: dissolve(c, lt, c2, 0.6, court, close))


def p12_s07(an, c, t):
    """Sunset: the army on the plain; Sohrab, now in armour, on the colt on a rise: 'Tomorrow, we ride to Iran!' --
    the spears go up."""
    lt, dur = loc(an, "S07", t)
    L = [LN("p12", "S07", k) for k in range(3)]
    focus = (600, 700)
    zoom = 1.0 + 0.07 * ease(lt / dur)
    cam = Cam(c, focus, zoom)
    S.lin(c, 0, 900, [(0, (40, 16, 46)), (0.35, (130, 40, 60)), (0.65, (226, 96, 60)), (0.85, (252, 160, 86)), (1, (255, 196, 120))])
    with cam(0.2):
        S.sun(c, 330, 790, 120, (255, 230, 176), (255, 130, 70), 640, 170, 9, t)
        get(an, "cl127", lambda: S.Clouds([(260, 16), (340, 12), (430, 20)], 127)).draw(c, t, (80, 16, 40), 190)
    rg = get(an, "rg127", lambda: (S.make_ridge(-600, 1700, 790, 40, 128), S.make_ridge(-600, 1700, 830, 18, 129)))
    with cam(0.4):
        S.ridge(c, rg[0], (116, 36, 60))
    with cam(0.55):
        S.ridge(c, rg[1], (66, 18, 38))
    cheer = sstep(L[1][1] - 0.6, L[1][1] + 0.2, lt) * (1 - sstep(L[2][0] + 0.6, L[2][0] + 1.2, lt)) + \
        sstep(L[2][1] - 0.4, L[2][1] + 0.3, lt)
    cheer = clamp(cheer)
    with cam(0.75):
        b0 = get(an, "army0", lambda: army_band(False))
        b1 = get(an, "army1", lambda: army_band(True))
        draw_band(c, b0, -760, 590, (40, 10, 22), 1 - cheer)
        draw_band(c, b1, -760, 590, (40, 10, 22), cheer)
        S.lin(c, 840, 900, [(0, (60, 18, 30, 0)), (1, (30, 8, 16, 255))], (-600, 840, 1700, 900))
    with cam(1.0):
        c.drawPath(spath([(-300, 2400, 0), (-300, 900), (300, 912), (620, 892), (820, 862), (1000, 858), (1400, 870),
                          (1400, 2400, 0)]), paint(C(*INK)))
    up = sstep(L[1][0], L[1][0] + 0.5, lt)
    point = sstep(L[2][0] + 0.2, L[2][0] + 0.8, lt)
    rr = math.sin(clamp((lt - L[2][1] + 0.6) / 1.6) * math.pi) * 30 if L[2][1] - 0.6 < lt < L[2][1] + 1.0 else 0.0
    rp = {"hand_kind": "spear", "hand": (mix(mix(110, 60, up), 170, point), mix(mix(-330, -540, up), -420, point)),
          "lean": 4 * point, "head": -3 * up, "wind": 1.0, "jaw": jaw(an, "SOHRAB", t, 8)}
    PC = {"gait": "rear", "rear": rr} if rr > 1 else {"gait": "stand", "neck": 6 * math.sin(t * 1.9), "head": 4 * math.sin(t * 1.2)}
    PC.update({"saddle": True, "rider": "sohrab", "rider_scale": 0.92, "rider_pose": rp, "wind": 0.9})

    def figs(cc):
        with Cam(cc, focus, zoom)(1.0):
            horse(cc, 830, 862, 0.66, -1, PC, t)
    an.figures(c, figs, COLT, (0, 150, 1080, 1000), alpha=200)
    vig(an, c, 150)


def p12_s08(an, c, t):
    """Turn + end: a rider gallops through the night; in his dark palace Afrasiab hears of the boy -- 'The son of
    Rostam, against Iran? Good. Very good.'"""
    lt = t - an.start["S08"]
    dur = an.end["END"] - an.start["S08"]
    L = [LN("p12", "S08", k) for k in range(4)]
    c1 = L[1][0] - 0.2
    c2 = L[2][0] - 0.6

    def night_ride():
        S.lin(c, 0, 880, [(0, (6, 8, 22)), (0.55, (24, 26, 58)), (1, (60, 52, 84))])
        get(an, "st128", lambda: S.Stars(140, 760, 128)).draw(c, t, 0.9, 760)
        S.moon(c, 780, 400, 60)
        sc = get(an, "sc128", lambda: Scroller(151))
        sc.draw(c, lt, 760, [(44, 44, 76), (26, 24, 44), (12, 10, 18)])
        P = {"gait": "gallop", "phase": t * 2.0, "saddle": True, "rider": "rider",
             "rider_pose": {"lean": 14, "hand": (120, -320), "head": 6, "wind": 1.2}}

        def figs(cc):
            horse(cc, 520, 872, 0.78, 1, P, t)
        an.figures(c, figs, MOON, (0, 200, 1080, 1000))
        vig(an, c, 160)

    def hall_wide():
        lt2 = lt - c1
        focus = (560, 680)
        zoom = 1.0 + 0.06 * ease(lt2 / (c2 - c1 + 0.6))
        cam = Cam(c, focus, zoom)
        dark_hall(an, c, t, cam)
        enter = clamp((lt2 - 0.2) / 2.0)
        kneel = lt2 > 2.3
        mx = mix(-80, 300, ease(enter))
        PM = {"mode": "kneel" if kneel else "walk", "phase": lt2 * 4.4, "stride": 18, "head": 12 if kneel else 4,
              "lean": 14 if kneel else 6, "hand": (90, -280) if kneel else (40, -262), "hand_kind": "open"}
        PA = {"hand": (110, -330), "hand_kind": "open", "rhand": (-30, -262), "head": 4 + 1.2 * math.sin(t * 0.5)}

        def figs(cc):
            with Cam(cc, focus, zoom)(1.0):
                sit_throne(cc, 800, 900, 1.0, -1, PA, t, "afrasiab")
                person(cc, mx, 900, 0.9, 1, PM, t, "rider")
        an.figures(c, figs, EMBER, (0, 150, 1080, 1100), alpha=170)
        with cam(1.0):
            brazier(c, 560, 900, 0.8, t)
        vig(an, c, 190)

    def afrasiab():
        lt3 = lt - c2
        focus = (640, 640)
        zoom = 1.0 + 0.1 * ease(lt3 / (dur - c2))
        cam = Cam(c, focus, zoom)
        dark_hall(an, c, t, cam, 1.2)
        lean = sstep(L[2][0], L[2][0] + 0.8, lt) * (1 - sstep(L[3][0] + 1.0, L[3][0] + 2.2, lt))
        palm = sstep(L[2][0] + 0.6, L[2][0] + 1.2, lt) * (1 - sstep(L[3][0] + 1.6, L[3][0] + 2.4, lt))
        grip = sstep(L[3][0] + 2.0, L[3][1] - 0.2, lt)
        mock = 4 * math.sin(lt * 4.0) * sstep(L[2][1] - 1.4, L[2][1] - 1.0, lt) * (1 - sstep(L[2][1], L[2][1] + 0.4, lt))
        if grip > 0.01:
            h, hk = (mix(150, 110, grip), mix(-380, -470, grip)), "fist" if grip > 0.4 else "open"
        else:
            h, hk = (mix(100, 160, palm), mix(-320, -380, palm)), "open"
        PA = {"jaw": jaw(an, "AFRASIAB", t, 7), "hand": h, "hand_kind": hk, "rhand": (-30, -262),
              "head": 4 - 4 * lean + 6 * grip + mock + 1.2 * math.sin(t * 0.5), "lean": 7 * lean - 3 * grip}
        fire = 1.0 + 0.6 * sstep(L[3][1] - 1.0, L[3][1] + 0.6, lt)

        def figs(cc):
            with Cam(cc, focus, zoom)(1.0):
                sit_throne(cc, 760, 1330, 1.75, -1, PA, t, "afrasiab")
        an.figures(c, figs, EMBER, (0, 100, 1080, 1500), alpha=180)
        with cam(1.0):
            brazier(c, 170, 1240, 1.2, t, fire)
        get(an, "mo128", lambda: S.Motes(50, 128, 300, 1100)).draw(c, t, (255, 150, 90), 110, rise=30, drift=0.2)
        vig(an, c, 200)

    dissolve(c, lt, c1, 0.7, night_ride, lambda: dissolve(c, lt, c2, 0.6, hall_wide, afrasiab))


P11 = {"S01": p11_s01, "TITLE": p11_s01, "S02": p11_s02, "S03": p11_s03, "S04": p11_s04, "S05": p11_s05,
       "S06": p11_s06, "S07": p11_s07, "END": p11_s07}
SHIFT11 = {}

P12 = {"S01": p12_s01, "TITLE": p12_s01, "S02": p12_s02, "S03": p12_s03, "S04": p12_s04, "S05": p12_s05,
       "S06": p12_s06, "S07": p12_s07, "S08": p12_s08, "END": p12_s08}
SHIFT12 = {}

register(P11, SHIFT11)
