"""Generic shadow puppets for the episodes: people in many looks and poses,
horses and onagers with gaits and riders, and hand-held props.

All puppets face +x in local units (feet at 0, standing hips at -250,
shoulders -410, head about -490) and are mirrored with face=-1.
"""
import math
import skia
from anim import (C, mix, clamp, spath, ppath, paint, bez, ik, Pen, ink, fillp, hole, detail,
                  begin_fig, limb, taper, boot, lappets, anchor)

TAU = math.tau

LOOKS = {
    "rostam": dict(b=1.15, heavy=True, head="helmet", plume=True, beard="long", garment="armor", mantle=True),
    "rostam_bare": dict(b=1.15, heavy=True, head="bare", beard="long", garment="armor", mantle=True),
    "rostam_robe": dict(b=1.15, heavy=True, head="bare", beard="long", garment="robe"),
    "young_rostam": dict(b=1.06, head="bare", beard="short", garment="tunic"),
    "herdsman": dict(b=0.95, head="wool", beard="long", garment="robe_short"),
    "king": dict(b=1.05, head="crown", beard="long", garment="robe", cape=True),
    "noble": dict(b=1.0, head="turban", beard="short", garment="robe"),
    "guard": dict(b=1.0, head="cone", beard="short", garment="tunic"),
    "rider": dict(b=1.0, head="fur", beard="short", garment="tunic"),
    "tahmineh": dict(b=0.86, female=True, head="veil_crown", beard="none", garment="dress"),
    "maid": dict(b=0.82, female=True, head="veil", beard="none", garment="dress"),
    "poet": dict(b=0.95, head="turban", beard="long", garment="robe"),
    "musician": dict(b=0.95, head="turban", beard="short", garment="robe"),
    "sohrab": dict(b=1.05, head="cone", plume=True, hair=True, beard="none", garment="tunic", cape=True),
    "gordafarid": dict(b=0.9, female=True, head="cone", plume=True, hair=True, beard="none", garment="armor"),
    "warrior_ir": dict(b=1.05, head="cone", beard="short", garment="armor"),
    "warrior_tu": dict(b=1.05, head="fur", beard="short", garment="armor"),
    "kavus": dict(b=1.05, head="crown", beard="long", garment="robe", cape=True),
    "afrasiab": dict(b=1.1, head="crown", beard="long", garment="robe", cape=True),
    "mobed": dict(b=0.95, head="turban", beard="long", garment="robe"),
    "div": dict(b=1.35, heavy=True, head="horns", beard="long", garment="tunic"),
    "young_sohrab": dict(b=1.0, head="bare", hair=True, beard="none", garment="tunic"),   # Sohrab as a boy
    "boy": dict(b=0.95, head="bare", beard="none", garment="tunic"),
    "wrestler": dict(b=1.15, heavy=True, head="bare", beard="short", garment="tunic"),
}

L1, L2 = 120, 106          # thigh, shin
STRIPE = [75]              # how brightly the tiger stripes glow


# ------------------------------------------------------------------ legs
def _leg(c, hip, knee, ankle, s=1.0, foot=True):
    limb(c, hip, 24 * s, knee, 18 * s)
    limb(c, knee, 18 * s, ankle, 12.5 * s)
    if foot:
        c.save()
        c.translate(ankle[0], ankle[1] + 24)
        boot(c, 0, 0.92)
        c.restore()


def leg_pose(mode, P, t):
    """Joint positions for both legs and the hip height."""
    if mode == "walk":
        ph = P.get("phase", 0.0)
        A, K = math.radians(P.get("stride", 21)), math.radians(48)
        out = []
        for k, off in (("rear", math.pi), ("front", 0.0)):
            phi = ph + off
            th = A * math.sin(phi)
            ka = K * max(0.0, math.cos(phi - 0.35)) ** 1.3
            kn = (L1 * math.sin(th), L1 * math.cos(th))
            an = (kn[0] + L2 * math.sin(th - ka), kn[1] + L2 * math.cos(th - ka))
            out.append((k, kn, an))
        drop = max(o[2][1] for o in out)
        hy = -(drop + 24)
        legs = {k: ((k == "front") * 14 - (k == "rear") * 14, (kn[0], hy + kn[1]), (an[0], hy + an[1]))
                for k, kn, an in out}
        return hy, legs
    fa, ra = P.get("stance", (46, 40))
    return -250, {"rear": (-14, (-ra * 0.5 - 6, -130), (-ra, -24)),
                  "front": (14, (fa * 0.7 + 4, -132), (fa, -24))}


def draw_legs(c, mode, P, t, L):
    """Draws the legs for the pose and returns the hip height (local y)."""
    if mode in ("stand", "walk", "lie"):
        if mode == "lie":
            hy, legs = -250, {"rear": (-10, (-8, -130), (-6, -24)), "front": (10, (8, -132), (10, -24))}
        else:
            hy, legs = leg_pose(mode, P, t)
        for k in ("rear", "front"):
            hx, kn, an = legs[k]
            _leg(c, (hx, hy), kn, an)
        P["_ankles"] = (legs["front"][2][0], legs["rear"][2][0])
        return hy
    if mode == "sit":
        hy = -62
        for dx in (0, -14):
            limb(c, (dx, hy), 30, (96 + dx, -46), 21)
            limb(c, (96 + dx, -46), 20, (18 + dx, -20), 14)
        fillp(c, spath([(-58, -70), (-30, -98), (60, -86), (122, -62), (126, -26, 0), (60, -4, 0), (-60, -4, 0)]))
        return hy
    if mode == "kneel":
        hy = -150
        _leg(c, (-10, hy), (-12, -22), (-108, -18), foot=False)
        fillp(c, spath([(-118, -30), (-96, -32), (-92, -6, 0), (-134, -4, 0)]))
        _leg(c, (14, hy), (92, -104), (92, -24))
        return hy
    if mode == "ride":
        hy = -250
        kn, an = (66, -176), (44, -86)
        limb(c, (12, hy), 25, kn, 19)
        limb(c, kn, 18, an, 12.5)
        c.save()
        c.translate(an[0], an[1] + 24)
        c.rotate(-8)
        boot(c, 0, 0.92)
        c.restore()
        return hy
    raise ValueError(mode)


# ---------------------------------------------------------------- bodies
def torso(c, L, br):
    b = L.get("b", 1.0)
    if L.get("heavy"):
        fillp(c, spath([(-44 * b, -262), (-54 * b, -320), (-58 * b, -384), (-46 * b, -420 + br), (-18 * b, -434 + br),
                        (10, -440 + br), (34 * b, -428 + br), (50 * b, -404 + br), (62 * b, -364), (66 * b, -330),
                        (60 * b, -296), (50 * b, -270), (54 * b, -256, 0), (44 * b, -246, 0), (-42 * b, -246, 0)]))
    elif L.get("female"):
        fillp(c, spath([(-34 * b, -262), (-40 * b, -320), (-42 * b, -384), (-34 * b, -414 + br), (-12 * b, -430 + br),
                        (10, -436 + br), (28 * b, -422 + br), (44 * b, -396 + br), (54 * b, -372), (48 * b, -348),
                        (36 * b, -318), (30 * b, -278), (34 * b, -256, 0), (28 * b, -246, 0), (-32 * b, -246, 0)]))
    else:
        fillp(c, spath([(-40 * b, -262), (-48 * b, -326), (-50 * b, -388), (-40 * b, -420 + br), (-16 * b, -434 + br),
                        (12, -440 + br), (34 * b, -424 + br), (54 * b, -394 + br), (60 * b, -356), (48 * b, -308),
                        (38 * b, -272), (42 * b, -256, 0), (34 * b, -246, 0), (-38 * b, -246, 0)]))


def garment(c, L, P, t, mode, hy):
    b = L.get("b", 1.0)
    g = L.get("garment", "tunic")
    fa, ra = P.get("_ankles", (46, -40))
    fl = 3 * math.sin(t * 2.9 + P.get("seed", 0))
    if mode == "sit":
        if g in ("robe", "robe_short", "dress"):
            fillp(c, spath([(-44 * b, -262), (46 * b, -262), (70, -170), (120, -96), (138, -30, 0), (60, -4, 0),
                            (-66, -4, 0), (-70, -80), (-52, -190)]))
        else:
            fillp(c, spath([(-50 * b, -276, 0), (58 * b, -276, 0), (60 * b, -258, 0), (-50 * b, -258, 0)]))
        return
    if mode == "ride":
        fillp(c, spath([(-44 * b, -270, 0), (46 * b, -270, 0), (88, -196), (60, -172, 0), (-30, -196), (-56, -230)]))
        return
    if g == "armor":
        fillp(c, spath([(-50 * b, -276, 0), (60 * b, -276, 0), (62 * b, -258, 0), (-50 * b, -258, 0)]))
        lappets(c, -262, -150, -50 * b, 56 * b, -82 * b, 92 * b, 7)
    elif g == "tunic":
        fillp(c, spath([(-40 * b, -280, 0), (42 * b, -280, 0), (44 * b, -262, 0), (-40 * b, -262, 0)]))
        fillp(c, spath([(-38 * b, -264, 0), (40 * b, -264, 0), (56 * b, -200), (max(64, fa + 12), -140, 0),
                        (26, -132, 0), (16, -150, 0), (6, -132, 0), (min(-56, ra - 14) + fl, -136, 0), (-48 * b, -200)]))
    else:
        hem = {"robe": -18, "robe_short": -96, "dress": -4}[g]
        front = max(70 * b, fa + 30) if hem > -50 else 70 * b
        back = min(-74 * b, ra - 34) if hem > -50 else -72 * b
        trail = -26 if g == "dress" else 0
        fillp(c, spath([(-40 * b, -270), (44 * b, -270), (58 * b, -200), (front, hem + 6), (front - 8, hem, 0),
                        (back + trail + fl, hem + (4 if g == "dress" else 0), 0), (back + 10, hem + 4),
                        (-56 * b, -200)]))
        if g != "dress":
            fillp(c, spath([(-42 * b, -282, 0), (44 * b, -282, 0), (46 * b, -264, 0), (-42 * b, -264, 0)]))
    bel = P.get("belly", 0.0)              # a woman with child (0..1)
    if bel > 0.01 and g == "dress":
        fillp(c, spath([(26 * b, -348), (34 * b + 20 * bel, -316), (40 * b + 36 * bel, -276), (40 * b + 32 * bel, -236),
                        (44 * b + 14 * bel, -206), (20 * b, -206), (0, -280)]))


def mantle(c, br, t):
    sw = 4 * math.sin(t * 1.3)
    m = [(-20, -438 + br, 0), (-56, -424 + br), (-72, -392), (-80, -352)]
    for i in range(8):
        x = mix(-82, 40, i / 7)
        m.append((x, -330 + (12 if i % 2 else 0) + 0.06 * (x + 82) * (1 if i % 2 else -0.3), 0))
    m += [(52, -372), (60, -404 + br), (40, -426 + br, 0)]
    fillp(c, spath(m))
    taper(c, bez((-70, -344), (-84 + sw, -296), (-98 + sw * 1.5, -250), (-86 + sw * 2, -214), 12), 6.5, 2.5)
    stripe = C(255, 170, 90, STRIPE[0])
    for (x, y) in [(-62, -404), (-70, -372), (-30, -356), (4, -358), (-48, -344)]:
        taper(c, [(x - 7, y - 7), (x + 1, y), (x + 11, y + 3)], 2.2, 0.6, paint(stripe))


def cape(c, br, t, wind=1.0, length=262):
    pts = [(0, -432 + br, 0), (-28, -428 + br)]
    for i in range(1, 9):
        u = i / 8
        pts.append((-36 - u * (26 + 50 * wind) + 7 * wind * math.sin(t * 3.1 - u * 4.5) * u, -420 + u * length))
    for i in range(1, 5):
        u = i / 4
        pts.append((mix(-62 - 50 * wind, -40, u) + 4 * math.sin(t * 3.4 + u * 6),
                    -420 + length + 4 + 6 * math.sin(i * 2.2) - 4 * math.sin(t * 2.7 + u * 7)))
    pts += [(-38, -300), (-34, -400)]
    fillp(c, spath(pts))


# ----------------------------------------------------------------- heads
FACE_M = [(-20, -472), (-24, -496), (-12, -520), (10, -527), (30, -515), (37, -504), (34, -497),
          (38, -491), (49, -480, 0), (41, -476), (43, -471), (38, -467), (41, -462), (36, -452),
          (20, -444), (2, -446), (-14, -456)]
FACE_Y = [(-18, -472), (-21, -496), (-10, -518), (10, -526), (28, -515), (34, -503), (31, -496),
          (35, -490), (44, -481, 0), (37, -477), (39, -472, 0), (30, -458), (12, -447), (-2, -449), (-14, -458)]
FACE_F = [(-18, -472), (-20, -496), (-10, -516), (8, -523), (26, -513), (31, -503), (29, -497), (32, -491),
          (39, -483, 0), (33, -479), (35, -474, 0), (31, -471), (34, -467), (29, -459), (16, -450), (0, -450),
          (-12, -458)]


def head(c, L, P, t, br):
    hg = L.get("head", "bare")
    fem = L.get("female", False)
    beard = L.get("beard", "none")
    wind = P.get("wind", 0.6)
    c.save()
    c.translate(8, -446 + br)
    c.rotate(P.get("head", 0.0))
    c.translate(-8, 446 - br)
    c.translate(0, br)
    limb(c, (2, -432), 16 if not fem else 13, (8, -460), 16 if not fem else 13)
    if hg == "veil" or hg == "veil_crown":
        sw = 5 * math.sin(t * 1.8)
        pts = [(-4, -530), (16, -530), (32, -517), (38, -504, 0), (29, -508), (18, -517), (0, -518), (-14, -508),
               (-20, -480)]
        for i in range(1, 7):
            u = i / 6
            pts.append((-24 - u * (38 + 26 * wind) + sw * u, -470 + u * 220))
        pts += [(-40 - 20 * wind + sw, -244, 0), (-30, -300), (-22, -380), (-18, -440)]
        fillp(c, spath(pts))
    if L.get("hair"):
        for k, (dy, ln) in enumerate(((0, 1.0), (10, 0.86), (20, 0.72))):
            pts = []
            for i in range(9):
                u = i / 8
                pts.append((-18 - u * (34 + 30 * wind) * ln + 5 * wind * math.sin(t * 3.6 - u * 4 + k) * u,
                            -498 + dy + u * (96 - dy) * ln))
            taper(c, pts, 6.5 - k, 1.5)
    if hg == "cone" and L.get("plume"):
        c.save()
        c.translate(10, -566)
        c.rotate(3 * math.sin(t * 1.9 + 0.7))
        for k, (a, b2, e) in enumerate([((-6, -66), (-40, -112), (-92, -104)),
                                        ((-2, -54), (-34, -92), (-80, -76)),
                                        ((2, -42), (-26, -72), (-62, -52))]):
            taper(c, bez((0, 0), a, b2, e, 12), 6 - k, 1.1)
        c.restore()
    if hg == "helmet" and L.get("plume"):
        c.save()
        c.translate(12, -578)
        c.rotate(2.5 * math.sin(t * 1.7))
        for k, (a, b2, e) in enumerate([((-16, -50), (-60, -78), (-104, -58)),
                                        ((-10, -40), (-52, -60), (-92, -34)),
                                        ((-4, -30), (-36, -46), (-70, -14))]):
            taper(c, bez((0, 0), a, b2, e, 12), 6.5 - k, 1.1)
        c.restore()
    if hg == "crown":
        for k, ph in ((0, 0.0), (1, 1.3)):
            pts = [(-20 + 4 * k, -512 + 4 * k)]
            for i in range(1, 7):
                u = i / 6
                pts.append((-24 - 6 * k - u * (16 + 14 * wind) + 4 * math.sin(t * 2.6 + u * 4 + ph) * u,
                            -512 + 4 * k + u * (100 - 14 * k)))
            taper(c, pts, 4.0, 2.4)
    face = FACE_F if fem else FACE_Y if beard in ("none", "short") and not L.get("heavy") else FACE_M
    fillp(c, spath(face))
    jaw = P.get("jaw", 0.0)
    if beard in ("none",):
        if not fem:
            c.save()
            c.translate(10, -470)
            c.rotate(jaw)
            c.translate(-10, 470)
            fillp(c, spath([(39, -472, 0), (36, -468), (38, -463), (35, -456), (27, -449), (12, -447), (8, -462)]))
            c.restore()
        else:
            c.save()
            c.translate(10, -472)
            c.rotate(jaw * 0.7)
            c.translate(-10, 472)
            fillp(c, spath([(34, -471, 0), (31, -468), (34, -464), (29, -457), (16, -450), (8, -462)]))
            c.restore()
    else:
        c.save()
        c.translate(-4, -470)
        c.rotate(jaw)
        c.translate(4, 470)
        if beard == "long":
            fillp(c, spath([(38, -478, 0), (60, -473, 0), (48, -466), (56, -452), (64, -432), (68, -410),
                            (66, -392), (56, -372), (48, -352, 0), (40, -372), (24, -396), (8, -418), (-4, -440),
                            (-10, -458), (-12, -470, 0), (2, -474), (22, -471)]))
        else:
            fillp(c, spath([(38, -477, 0), (52, -472, 0), (42, -466), (46, -454), (42, -440), (32, -428, 0),
                            (22, -438), (6, -446), (-6, -452), (-12, -470, 0), (2, -474), (22, -471)]))
        c.restore()
    # headgear
    if hg == "helmet":
        fillp(c, spath([(-27, -486, 0), (-30, -508), (-22, -532), (-6, -547), (12, -551), (30, -541),
                        (40, -522), (44, -507, 0), (12, -508), (-12, -500)]))
        fillp(c, spath([(-32, -510, 0), (46, -512, 0), (46, -504, 0), (-30, -500, 0)]))
        fillp(c, spath([(6, -548, 0), (9, -566), (5, -572), (12, -598, 0), (19, -572), (15, -566), (18, -548, 0)]))
        fillp(c, spath([(-27, -494), (-40, -464), (-44, -436, 0), (-22, -430, 0), (-10, -446), (-14, -472)]))
        for i in range(5):
            x = mix(-22, 34, (i + 0.5) / 5)
            hole(c, spath([(x - 2.5, -506, 0), (x, -508.5), (x + 2.5, -506, 0), (x, -503.5)]))
    elif hg == "cone":
        fillp(c, spath([(-25, -488, 0), (-27, -510), (-17, -532), (0, -550), (8, -564, 0), (16, -550),
                        (31, -532), (38, -512), (37, -505, 0), (8, -508), (-12, -500)]))
        fillp(c, spath([(-29, -512, 0), (40, -514, 0), (40, -506, 0), (-27, -502, 0)]))
        fillp(c, spath([(-25, -496), (-34, -470), (-36, -446, 0), (-18, -442, 0), (-12, -470)]))
    elif hg == "crown":
        fillp(c, spath([(-26, -500, 0), (-28, -548, 0), (-16, -530, 0), (-6, -560, 0), (6, -534, 0), (18, -566, 0),
                        (28, -534, 0), (40, -552, 0), (42, -504, 0), (10, -510), (-12, -506)]))
        c.drawCircle(18, -572, 6, ink()) if Pen.mode != "anchor" else None
        for i in range(4):
            x = mix(-18, 34, (i + 0.5) / 4)
            hole(c, spath([(x - 3, -520, 0), (x, -524), (x + 3, -520, 0), (x, -516)]))
        fillp(c, spath([(-22, -500), (-26, -470), (-24, -446, 0), (-12, -456), (-14, -486)]))
    elif hg == "fur":
        fillp(c, spath([(-24, -500, 0), (-26, -522), (-14, -540), (6, -548), (-14, -566), (-34, -566, 0),
                        (-20, -556), (-2, -556), (22, -544), (34, -526), (38, -508, 0)]))
        fur = [(-34, -500, 0)]
        for i in range(10):
            x = mix(-34, 44, i / 9)
            fur.append((x, -516 - (5 if i % 2 else 0), 0))
        fur += [(46, -500, 0), (44, -492, 0)]
        for i in range(10):
            x = mix(44, -34, i / 9)
            fur.append((x, -492 + (4 if i % 2 else 0), 0))
        fillp(c, ppath([(p[0], p[1]) for p in fur]))
    elif hg == "wool":
        fillp(c, spath([(-26, -484, 0), (-30, -508), (-20, -532), (2, -542), (24, -534), (36, -516), (39, -504, 0),
                        (10, -508), (-10, -500)]))
    elif hg == "turban":
        fillp(c, spath([(-30, -488, 0), (-36, -512), (-28, -540), (-6, -556), (20, -557), (40, -542), (48, -518),
                        (44, -500, 0), (10, -506), (-14, -498)]))
        fillp(c, spath([(40, -540), (46, -556), (50, -538)]))
        taper(c, bez((-30, -500), (-44, -480), (-46, -456), (-40, -432), 8), 6, 3)
        for i in range(3):
            detail(c, spath([(-30 + i * 8, -548 + i * 14, 0), (44 - i * 2, -544 + i * 12, 0),
                             (44 - i * 2, -541 + i * 12, 0), (-30 + i * 8, -545 + i * 14, 0)]),
                   paint(C(255, 190, 120, 40)))
    elif hg == "bare":
        fillp(c, spath([(-22, -468), (-28, -496), (-18, -520), (4, -531), (26, -524), (36, -508, 0), (20, -514),
                        (0, -510), (-10, -494), (-14, -470), (-18, -446), (-28, -428), (-38, -436), (-34, -462)]))
    elif hg == "horns":         # a div: wild hair, two great curved horns, a pointed ear
        hair = [(-24, -470, 0)]
        for i in range(9):
            u = i / 8
            a = math.radians(mix(200, 330, u))
            r = 30 if i % 2 else 46
            hair.append((4 + r * math.cos(a), -500 + r * math.sin(a), 0))
        hair += [(38, -506, 0), (8, -508)]
        fillp(c, ppath([(p[0], p[1]) for p in hair]))
        taper(c, bez((-8, -522), (-30, -566), (-74, -582), (-92, -548), 10), 10, 2)
        taper(c, bez((12, -526), (22, -576), (62, -598), (84, -572), 10), 9, 2)
        fillp(c, spath([(-6, -488, 0), (-22, -504), (-14, -486, 0)]))
    elif hg == "veil_crown":
        fillp(c, ppath([(-12, -524), (-10, -542), (-2, -530), (6, -547), (14, -530), (22, -541), (26, -522)]))
    if hg not in ("veil", "veil_crown"):
        hole(c, spath([(23, -497, 0), (28, -499.5), (33, -497, 0), (28, -495.5)]))
    else:
        hole(c, spath([(19, -497, 0), (24, -499.5), (29, -497, 0), (24, -495.5)]))
    anchor(c, "eye", 28, -497)
    c.restore()


# ------------------------------------------------------------------ arms
def hand_shape(c, W, a2, kind, op=1.0):
    c.save()
    c.translate(*W)
    c.rotate(math.degrees(a2) - 24 * op)
    if kind == "open":
        fillp(c, spath([(-4, -9), (14, -10), (30, -8), (37, -3), (32, 3), (16, 9), (-2, 9)]))
        fillp(c, spath([(6, -9), (14, -20), (20, -18), (16, -8)]))
    else:
        if Pen.mode != "anchor":
            c.drawCircle(8, 0, 13, ink())
    c.restore()


def arm(c, S, T, sign, r=(21, 16, 12), hand="fist", name=None):
    E, Wr, a2 = ik(S, T, 92, 88, sign)
    limb(c, S, r[0], E, r[1])
    limb(c, E, r[1], Wr, r[2])
    if hand in ("fist", "open"):
        hand_shape(c, Wr, a2, hand)
    if name:
        anchor(c, name, Wr[0] + 8 * math.cos(a2), Wr[1] + 8 * math.sin(a2))
        anchor(c, name + "_up", (S[0] + E[0]) / 2, (S[1] + E[1]) / 2)      # upper arm (an armband)
    return E, Wr, a2


def prop(c, kind, W, a2, P, t):
    hx, hy = W[0] + 8 * math.cos(a2), W[1] + 8 * math.sin(a2)
    if kind == "mace":
        c.save()
        c.translate(hx, hy)
        c.rotate(P.get("mace", 0.0))
        fillp(c, ppath([(-5, 96), (5, 96), (5, -112), (-5, -112)]))
        fillp(c, spath([(0, -108, 0), (16, -112), (25, -126), (24, -142), (14, -154), (0, -158, 0), (-14, -154),
                        (-24, -142), (-25, -126), (-16, -112)]))
        fillp(c, ppath([(-3, -156), (0, -176), (3, -156)]))
        for k in (-1, 1):
            hole(c, spath([(9 * k, -118, 0), (12 * k, -134), (8 * k, -150, 0), (6 * k, -134)]))
        c.restore()
    elif kind == "oxmace":
        c.save()
        c.translate(hx, hy)
        c.rotate(P.get("mace", 0.0))
        fillp(c, ppath([(-5, 110), (5, 110), (5, -120), (-5, -120)]))
        fillp(c, spath([(-16, -112, 0), (-20, -140), (-14, -168), (0, -196, 0), (14, -168), (20, -140), (16, -112, 0)]))
        taper(c, bez((-14, -160), (-36, -168), (-48, -190), (-40, -214), 9), 6, 1.5)
        taper(c, bez((14, -160), (36, -168), (48, -190), (40, -214), 9), 6, 1.5)
        fillp(c, spath([(-18, -150, 0), (-30, -146), (-26, -138, 0)]))
        fillp(c, spath([(18, -150, 0), (30, -146), (26, -138, 0)]))
        for k in (-1, 1):
            hole(c, spath([(7 * k - 3, -160, 0), (7 * k, -163), (7 * k + 3, -160, 0), (7 * k, -157)]))
        c.restore()
    elif kind == "staff":
        fillp(c, ppath([(hx - 4, hy + 240), (hx + 4, hy + 240), (hx + 4, hy - 130), (hx - 4, hy - 130)]))
        taper(c, bez((hx, hy - 128), (hx + 4, hy - 150), (hx + 24, hy - 156), (hx + 26, hy - 136), 8), 4, 3)
    elif kind == "spear":
        fillp(c, ppath([(hx - 3.5, hy + 250), (hx + 3.5, hy + 250), (hx + 3.5, hy - 300), (hx - 3.5, hy - 300)]))
        fillp(c, spath([(hx, hy - 370, 0), (hx + 9, hy - 332), (hx + 6, hy - 304), (hx, hy - 296, 0),
                        (hx - 6, hy - 304), (hx - 9, hy - 332)]))
    elif kind == "cup":
        fillp(c, spath([(hx - 4, hy - 10, 0), (hx - 14, hy - 34, 0), (hx + 14, hy - 34, 0), (hx + 4, hy - 10, 0),
                        (hx + 3, hy, 0), (hx + 10, hy + 4, 0), (hx - 10, hy + 4, 0), (hx - 3, hy, 0)]))
        anchor(c, "cup", hx, hy - 34)
    elif kind == "lamp":
        fillp(c, spath([(hx - 26, hy - 6), (hx - 10, hy - 18), (hx + 12, hy - 18), (hx + 30, hy - 26, 0),
                        (hx + 40, hy - 30, 0), (hx + 30, hy - 14), (hx + 14, hy - 2), (hx - 18, hy + 2)]))
        anchor(c, "flame", hx + 40, hy - 40)
    elif kind == "candle":
        fillp(c, ppath([(hx - 7, hy - 4), (hx + 7, hy - 4), (hx + 7, hy - 46), (hx - 7, hy - 46)]))
        fillp(c, spath([(hx - 18, hy - 2), (hx + 18, hy - 2), (hx + 14, hy + 6), (hx - 14, hy + 6)]))
        anchor(c, "flame", hx, hy - 58)
    elif kind == "pen":
        fillp(c, ppath([(hx - 2, hy + 4), (hx + 34, hy + 34), (hx + 31, hy + 37), (hx - 4, hy + 8)]))
        anchor(c, "pen", hx + 34, hy + 36)
    elif kind == "sword":
        c.save()
        c.translate(hx, hy)
        c.rotate(P.get("sword", 0.0))
        fillp(c, ppath([(-5, -20), (5, -20), (4, -206), (0, -232), (-4, -206)]))
        fillp(c, spath([(-26, -26, 0), (26, -26, 0), (22, -16, 0), (-22, -16, 0)]))
        fillp(c, ppath([(-4, -16), (4, -16), (4, 18), (-4, 18)]))
        if Pen.mode != "anchor":
            c.drawCircle(0, 22, 7, ink())
        anchor(c, "tip", 0, -232)
        c.restore()
    elif kind == "lance":
        # a spear that turns about the hand: P["lance"] degrees (0 = point up as "spear", 90 = point forward)
        c.save()
        c.translate(hx, hy)
        c.rotate(P.get("lance", 0.0))
        fillp(c, ppath([(-3.5, 250), (3.5, 250), (3.5, -300), (-3.5, -300)]))
        fillp(c, spath([(0, -370, 0), (9, -332), (6, -304), (0, -296, 0), (-6, -304), (-9, -332)]))
        anchor(c, "tip", 0, -370)
        anchor(c, "butt", 0, 250)
        c.restore()
    elif kind == "dagger":
        c.save()
        c.translate(hx, hy)
        c.rotate(P.get("dagger", 0.0))
        fillp(c, spath([(-6, -14, 0), (6, -14, 0), (5, -60), (2, -100), (0, -118, 0), (-3, -98), (-5, -60)]))
        fillp(c, spath([(-18, -18, 0), (18, -18, 0), (15, -10, 0), (-15, -10, 0)]))
        fillp(c, ppath([(-3.5, -10), (3.5, -10), (3.5, 14), (-3.5, 14)]))
        anchor(c, "tip", 0, -118)
        c.restore()
    elif kind == "club":
        c.save()
        c.translate(hx, hy)
        c.rotate(P.get("mace", 0.0))
        fillp(c, spath([(-6, 70, 0), (6, 70, 0), (14, -60), (24, -140), (14, -176), (-8, -180), (-24, -146), (-14, -60)]))
        for (kx, ky) in ((22, -120), (-22, -100), (16, -160), (-18, -150)):
            fillp(c, ppath([(kx - 5, ky - 4), (kx + 9 * (1 if kx > 0 else -1), ky), (kx - 5, ky + 4)]))
        c.restore()
    elif kind == "bow":
        # a bow held upright; the scene draws the string between the anchors bowtop/bowbot (and the draw hand)
        c.save()
        c.translate(hx, hy)
        c.rotate(P.get("bow", 0.0))
        for sy in (-1, 1):
            taper(c, bez((0, 0), (10, 52 * sy), (-2, 104 * sy), (-22, 126 * sy), 10), 6.5, 2.0)
        fillp(c, ppath([(-6, -18), (6, -18), (6, 18), (-6, 18)]))
        anchor(c, "bowtop", -22, -126)
        anchor(c, "bowbot", -22, 126)
        c.restore()
    elif kind == "lasso":
        rr = P.get("loop", 46)
        ang = t * 7.5
        ex = rr * (0.9 + 0.1 * math.sin(ang))
        ring = skia.Path()
        ring.addOval(skia.Rect.MakeXYWH(hx - ex, hy - 70 - rr * 0.32, 2 * ex, rr * 0.64))
        ring.addOval(skia.Rect.MakeXYWH(hx - ex + 7, hy - 70 - rr * 0.32 + 5, 2 * ex - 14, rr * 0.64 - 10))
        ring.setFillType(skia.PathFillType.kEvenOdd)
        fillp(c, ring)
        fillp(c, ppath([(hx - 2, hy), (hx + 2, hy), (hx + 3, hy - 70 + rr * 0.3), (hx - 1, hy - 70 + rr * 0.3)]))


# ---------------------------------------------------------------- person
def person(c, X, Y, s, face, P, t, look):
    """A full puppet. P: mode (stand/walk/sit/kneel/lie/ride), phase, stance,
    lean, head, jaw, hand/rhand (wrist targets), hand_kind/rhand_kind, props,
    carry ('saddle'), quiver, wind, seed. Coordinates are the standing frame."""
    L = LOOKS[look] if isinstance(look, str) else look
    mode = P.get("mode", "stand")
    b = L.get("b", 1.0)
    if mode == "lie":
        begin_fig(c, (X - 720 * s, Y - 380 * s, X + 720 * s, Y + 80 * s))
    else:
        begin_fig(c, (X - 330 * s, Y - 800 * s, X + 330 * s, Y + 80 * s))
    c.save()
    c.translate(X, Y)
    c.scale(s * face, s)
    if mode == "lie":
        c.translate(0, -56 * b)
        c.rotate(-90)
    seed = P.get("seed", 0.0)
    br = 1.4 * math.sin(t * 2 * math.pi / 4.0 + seed)
    hy = draw_legs(c, mode, P, t, L)
    dy = hy + 250
    c.save()
    c.translate(0, dy)
    c.translate(0, -250)
    c.rotate(P.get("lean", 0.0))
    c.translate(0, 250)
    # rear arm first (behind the body)
    Sr = (-20 * b, -410 + br)
    if P.get("carry") == "saddle":
        rt = (-28, -440)
    else:
        rt = P.get("rhand", (-30 * b, -262))
    E, Wr, ar = arm(c, Sr, rt, -1, hand=P.get("rhand_kind", "fist"), name="rhand")
    if P.get("rprop"):
        prop(c, P["rprop"], Wr, ar, P, t)
    if L.get("cape"):
        cape(c, br, t, P.get("wind", 0.6))
    if P.get("quiver"):
        c.save()
        c.translate(-46 * b, -360)
        c.rotate(-24)
        fillp(c, spath([(-14, -60, 0), (14, -60, 0), (12, 70, 0), (-12, 70, 0)]))
        for i in range(4):
            taper(c, [(-9 + i * 6, -60), (-10 + i * 6, -86)], 2, 1)
            fillp(c, ppath([(-14 + i * 6, -86), (-10 + i * 6, -98), (-6 + i * 6, -86)]))
        c.restore()
    torso(c, L, br)
    garment(c, L, P, t, mode, hy)
    if L.get("mantle"):
        mantle(c, br, t)
    head(c, L, P, t, br)
    if P.get("carry") == "saddle":
        c.save()
        c.translate(-44, -420)
        c.rotate(-6)
        c.scale(0.85, 0.85)
        fillp(c, spath([(-92, 8), (-80, -22), (-60, -30, 0), (-40, -12), (20, -12), (44, -30, 0), (60, -20),
                        (70, 10), (40, 26), (-60, 26)]))
        fillp(c, spath([(-70, 20, 0), (60, 20, 0), (54, 64, 0), (-64, 64, 0)]))
        for i in range(7):
            x = mix(-60, 50, i / 6)
            fillp(c, ppath([(x - 4, 62), (x + 4, 62), (x, 74)]))
        c.restore()
    St = (14 * b, -408 + br)
    T = P.get("hand", (40 * b, -262))
    kind = P.get("hand_kind", "fist")
    E, Wr, a2 = arm(c, St, T, 1, hand=kind if kind in ("fist", "open") else "fist", name="hand")
    if kind not in ("fist", "open"):
        prop(c, kind, Wr, a2, P, t)
    anchor(c, "pneck", 8, -440)
    c.restore()
    c.restore()
    c.restore()


# ----------------------------------------------------------------- horse
def _leg_angles(gait, ph, fore):
    """Upper and lower segment angles (deg from straight down, + forward)."""
    if gait == "gallop":
        a = 34 * math.cos(TAU * ph)
        sw = max(0.0, -math.sin(TAU * ph))
        if fore:
            u = a + 6 + 46 * sw
            return u, u - 118 * sw ** 0.9 + 2
        u = a - 16 - 14 * sw
        return u, u + 26 + 62 * sw ** 0.9
    if gait == "walk":
        a = 17 * math.cos(TAU * ph)
        sw = max(0.0, -math.sin(TAU * ph))
        if fore:
            u = a + 3 + 22 * sw
            return u, u - 70 * sw + 2
        u = a - 18 - 6 * sw
        return u, u + 24 + 34 * sw
    if fore:
        return 3, 1
    return -20, 6


LIE_F, LIE_H = (54.0, -100.0), (64.0, -108.0)      # leg angles of a horse lying on its belly (P["lie"] = 1)


def horse(c, X, Y, s, face, P, t, kind="horse"):
    """Horse puppet. P: gait (stand/walk/gallop/rear/graze), phase, neck (deg),
    rear (deg), saddle, bridle, rider (look), rider_pose, wind, tail, sink (knees buckling, 0..1),
    lie (0..1: folds the legs under the body and lowers it to the ground)."""
    gait = P.get("gait", "stand")
    ph = P.get("phase", 0.0)
    on = kind == "onager"
    begin_fig(c, (X - 420 * s, Y - 760 * s, X + 420 * s, Y + 40 * s))
    c.save()
    c.translate(X, Y)
    c.scale(s * face, s)
    c.translate(0, -9)
    bob, pitch = 0.0, 0.0
    sink = P.get("sink", 0.0)
    if gait == "gallop":
        bob = -12 * math.sin(TAU * ph)
        pitch = 3.5 * math.sin(TAU * ph + 1.4)
    elif gait == "walk":
        bob = -2.5 * abs(math.sin(TAU * ph * 2))
    bob += sink * 46
    pitch += sink * 3
    lie = P.get("lie", 0.0) if gait != "rear" else 0.0
    if lie:
        bob += lie * 132 - sink * 46 * lie
        pitch += -sink * 3 * lie - 1.5 * lie
    rear = P.get("rear", 0.0) if gait == "rear" else 0.0
    offs = {"gallop": (0.0, 0.1, 0.42, 0.52), "walk": (0.0, 0.5, 0.25, 0.75)}.get(gait, (0, 0, 0, 0))
    phases = [ph + o for o in offs]

    def leg(x0, y0, fore, p, far):
        if gait == "rear":
            if fore:
                u, l = 58 + 16 * math.sin(t * 7 + far * 2), -60 + 30 * math.sin(t * 7 + far * 2)
            else:
                u, l = -20 + rear * 0.9, 6 + rear * 0.9
        else:
            u, l = _leg_angles(gait, p, fore)
            if sink:
                u, l = (u + 34 * sink, l - 30 * sink) if fore else (u - 30 * sink, l + 46 * sink)
            if lie:
                lu, ll = LIE_F if fore else LIE_H
                q = 1 - (1 - min(1.0, lie * 1.25)) ** 2          # legs fold ahead of the body coming down
                u, l = mix(u, lu, q), mix(l, ll, q)
        l1, l2 = (95, 82) if fore else (90, 86)
        k = (x0 + l1 * math.sin(math.radians(u)), y0 + l1 * math.cos(math.radians(u)))
        f = (k[0] + l2 * math.sin(math.radians(l)), k[1] + l2 * math.cos(math.radians(l)))
        limb(c, (x0, y0), 21 if fore else 23, k, 10.5)
        limb(c, k, 10, f, 9)
        pa = math.radians(l + (16 if fore else 12))
        hf = (f[0] + 20 * math.sin(pa), f[1] + 20 * math.cos(pa))
        limb(c, f, 10, hf, 9)
        fillp(c, spath([(hf[0] - 9, hf[1] - 4), (hf[0] + 12, hf[1] - 2), (hf[0] + 14, hf[1] + 12, 0),
                        (hf[0] - 10, hf[1] + 12, 0)]))
        return hf

    # pivot for rearing: the hind hooves
    c.save()
    if rear:
        c.translate(-140, -6)
        c.rotate(-rear)
        c.translate(140, 6)
    c.translate(0, bob)
    c.translate(0, -250)
    c.rotate(pitch)
    c.translate(0, 250)
    # far legs
    leg(100, -196, True, phases[3] if gait != "rear" else 0, 1)
    leg(-136, -190, False, phases[1] if gait != "rear" else 0, 1)
    # tail
    if Pen.mode != "anchor":
        tw = P.get("tail", 0.0)
        if gait == "gallop":
            base_a, sway = -100, 8 * math.sin(t * 9)
        elif gait == "rear":
            base_a, sway = 20, 6 * math.sin(t * 5)
        else:
            base_a, sway = 12 + tw, 10 * math.sin(t * 1.6 + 0.4) + 6 * math.sin(t * 3.7)
        for k, (ln, w0) in enumerate(((150, 15), (130, 11), (110, 8))):
            pts = []
            for i in range(10):
                u = i / 9
                a = math.radians(base_a + sway * u + (k - 1) * 8 + 10 * math.sin(t * 6 + u * 3) * u * (gait == "gallop"))
                r = ln * u * (0.75 if on else 1.0)
                pts.append((-162 + r * math.sin(a) - 6 * u * u * (gait != "gallop"), -284 + r * math.cos(a)))
            taper(c, pts, w0 * (0.6 if on else 1.0), 2 + (4 if on else 0) * (k == 0))
    # body
    fillp(c, spath([(150, -204), (166, -238), (128, -280), (90, -305), (10, -290), (-60, -292), (-120, -306),
                    (-160, -288), (-180, -252), (-176, -206), (-150, -170), (-100, -166), (-40, -170), (40, -172),
                    (110, -182)]))
    if P.get("saddle"):
        fillp(c, spath([(-6, -292, 0), (-12, -318), (-4, -322, 0), (8, -302), (56, -304), (74, -324, 0),
                        (82, -318), (78, -296, 0)]))
        fillp(c, spath([(-14, -298, 0), (88, -300, 0), (84, -232, 0), (-10, -228, 0)]))
    anchor(c, "saddle", 30, -306)
    anchor(c, "back", -40, -292)
    # neck + head
    neck = P.get("neck", 0.0) + (62 if gait == "graze" else 0) + (-18 if gait == "rear" else 0)
    neck += 3 * math.sin(TAU * ph) * (gait == "gallop") + 2 * math.sin(t * 1.2) * (gait in ("stand", "graze"))
    c.save()
    c.translate(124, -262)
    c.rotate(neck)
    c.translate(-124, 262)
    fillp(c, spath([(166, -238), (226, -372), (238, -405), (246, -420), (232, -432), (204, -436), (182, -420),
                    (152, -384), (122, -340), (90, -305), (128, -280)]))
    # head
    c.save()
    c.translate(214, -420)
    c.rotate(P.get("head", 0.0) + (14 if gait == "graze" else 0))
    c.translate(-214, 420)
    ear = 1.25 if on else 1.0
    fillp(c, spath([(202, -432), (232, -430), (262, -396), (294, -354), (308, -334), (306, -318), (284, -312),
                    (272, -318), (254, -330), (234, -352), (222, -372), (210, -400)]))
    fillp(c, spath([(204, -428, 0), (204 - 2 * ear, -428 - 34 * ear, 0), (218, -434, 0)]))
    fillp(c, spath([(196, -424, 0), (190 - 2 * ear, -424 - 30 * ear, 0), (208, -432, 0)]))
    hole(c, spath([(236, -404, 0), (243, -407), (249, -403, 0), (242, -400)]))
    hole(c, spath([(296, -338, 0), (300, -336), (299, -331, 0)]))
    anchor(c, "mouth", 284, -322)
    anchor(c, "head", 250, -380)
    c.restore()
    # mane
    if not on:
        wind = min(1.0, P.get("wind", 0.4) + (0.6 if gait == "gallop" else 0))
        crest = [(206, -436), (184, -422), (156, -390), (126, -346), (100, -312)]
        for i in range(11):
            u = i / 10
            j = min(3, int(u * 4))
            f = u * 4 - j
            bx = mix(crest[j][0], crest[j + 1][0], f)
            by = mix(crest[j][1], crest[j + 1][1], f) + 3
            ln = 34 + 14 * math.sin(i * 1.9) + 22 * wind
            a0 = math.radians(150 + 22 * wind + 6 * math.sin(t * 4 + i * 0.7))
            a1 = a0 + math.radians(18 - 10 * wind)
            p1 = (bx + ln * 0.55 * math.cos(a0), by + ln * 0.55 * math.sin(a0))
            p2 = (p1[0] + ln * 0.45 * math.cos(a1), p1[1] + ln * 0.45 * math.sin(a1))
            taper(c, [(bx + 6, by + 2), p1, p2], 8, 1.2)
        taper(c, [(214, -430), (226, -420), (234, -404)], 7, 2)
    else:
        for i in range(8):
            u = i / 7
            bx, by = mix(206, 100, u), mix(-436, -308, u)
            fillp(c, ppath([(bx - 6, by + 4), (bx - 2, by - 12), (bx + 6, by + 4)]))
    anchor(c, "neck", 170, -330)
    c.restore()
    if P.get("rider"):
        rp = dict(P.get("rider_pose", {}))
        rp["mode"] = "ride"
        c.save()
        c.translate(30, -306 + 250 - 6)
        c.translate(0, -250)
        c.rotate(-pitch * 0.5)
        rs = P.get("rider_scale", 1.0)          # a child on a grown horse
        if rs != 1.0:
            c.scale(rs, rs)
        c.translate(0, 250)
        _inner_person(c, rp, t, P["rider"])
        c.restore()
    leg(118, -200, True, phases[2] if gait != "rear" else 0, 0)
    leg(-120, -192, False, phases[0] if gait != "rear" else 0, 0)
    c.restore()
    c.restore()
    c.restore()


def _inner_person(c, P, t, look):
    """A rider drawn inside the horse's transform (no layer of its own)."""
    save = begin_fig
    globals()["begin_fig"] = lambda cc, b: cc.save()
    try:
        person(c, 0, 0, 1.0, 1, P, t, look)
    finally:
        globals()["begin_fig"] = save
