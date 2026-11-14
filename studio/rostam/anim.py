"""Silhouette (shadow-puppet) animation for the Rostam & Sohrab episodes.

Every animated scene draws one 1080x1920 frame with skia. render.py uses it as
the background of a scene whose id is in SCENES and puts subtitles, verse
cards and the watermark on top.

  python3 -I anim.py still <ep_dir> <global_t> <out.png> [scene_id]
"""
import json, math, random, sys, wave
import numpy as np
import skia
from PIL import Image

W, H, FPS = 1080, 1920, 30
LO = 4                      # glow is blurred at 1/LO resolution


# ---------------------------------------------------------------- helpers
def C(r, g, b, a=255):
    return skia.Color(int(r), int(g), int(b), int(max(0, min(255, a))))


def mix(a, b, t):
    return a + (b - a) * t


def mixc(c1, c2, t):
    return tuple(mix(x, y, t) for x, y in zip(c1, c2))


def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))


def sstep(e0, e1, x):
    t = clamp((x - e0) / (e1 - e0))
    return t * t * (3 - 2 * t)


def ease(p):
    p = clamp(p)
    return p * p * (3 - 2 * p)


def spath(pts, closed=True, k=1 / 6):
    """Smooth path through points (Catmull-Rom as cubics); (x, y, 0) is a sharp corner."""
    n = len(pts)
    P = [(p[0], p[1]) for p in pts]
    sharp = [len(p) > 2 for p in pts]
    tang = []
    for i in range(n):
        if sharp[i] or (not closed and (i == 0 or i == n - 1)):
            tang.append((0.0, 0.0))
        else:
            a, b = P[(i - 1) % n], P[(i + 1) % n]
            tang.append(((b[0] - a[0]) * k, (b[1] - a[1]) * k))
    path = skia.Path()
    path.moveTo(*P[0])
    for i in range(n if closed else n - 1):
        j = (i + 1) % n
        p1, p2 = P[i], P[j]
        path.cubicTo(p1[0] + tang[i][0], p1[1] + tang[i][1],
                     p2[0] - tang[j][0], p2[1] - tang[j][1], p2[0], p2[1])
    if closed:
        path.close()
    return path


def ppath(pts, closed=True):
    path = skia.Path()
    path.moveTo(*pts[0])
    for p in pts[1:]:
        path.lineTo(*p)
    if closed:
        path.close()
    return path


_PAINTS = {}


def paint(color):
    p = _PAINTS.get(color)
    if p is None:
        p = skia.Paint(AntiAlias=True, Color=color)
        _PAINTS[color] = p
    return p


def bez(p0, p1, p2, p3, n=10):
    out = []
    for i in range(n):
        t = i / (n - 1)
        u = 1 - t
        out.append((u ** 3 * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t ** 3 * p3[0],
                    u ** 3 * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t ** 3 * p3[1]))
    return out


def ik(S, T, L1, L2, sign):
    """Two-bone limb from S reaching for T; returns elbow, wrist, forearm angle."""
    dx, dy = T[0] - S[0], T[1] - S[1]
    d = clamp(math.hypot(dx, dy), abs(L1 - L2) + 0.5, L1 + L2 - 0.5)
    a = math.atan2(dy, dx)
    A = math.acos(clamp((L1 * L1 + d * d - L2 * L2) / (2 * L1 * d), -1, 1))
    E = (S[0] + L1 * math.cos(a + sign * A), S[1] + L1 * math.sin(a + sign * A))
    a2 = math.atan2(T[1] - E[1], T[0] - E[0])
    return E, (E[0] + L2 * math.cos(a2), E[1] + L2 * math.sin(a2)), a2


def _k(t, keys):
    """Eased interpolation of a number or a point through (time, value) keys."""
    if t <= keys[0][0]:
        return keys[0][1]
    for (t0, v0), (t1, v1) in zip(keys, keys[1:]):
        if t <= t1:
            e = ease((t - t0) / (t1 - t0))
            if isinstance(v0, tuple):
                return tuple(mix(a, b, e) for a, b in zip(v0, v1))
            return mix(v0, v1, e)
    return keys[-1][1]


class Cam:
    """Push-in about a focus point; k scales the move for parallax layers."""

    def __init__(self, c, focus, zoom):
        self.c, self.f, self.z = c, focus, zoom

    def __call__(self, k):
        cam = self

        class _L:
            def __enter__(s):
                z = 1 + (cam.z - 1) * k
                cam.c.save()
                cam.c.translate(cam.f[0], cam.f[1])
                cam.c.scale(z, z)
                cam.c.translate(-cam.f[0], -cam.f[1])

            def __exit__(s, *a):
                cam.c.restore()
        return _L()


# ------------------------------------------------- silhouette pen (3 passes)
class Pen:
    """Figures are drawn three times: a white mask (blurred into the glow),
    a slightly fattened rim in the light colour, then the black puppet."""
    mode = "fill"
    FILL = skia.Paint(AntiAlias=True, Color=C(10, 5, 8))
    MASK = skia.Paint(AntiAlias=True, Color=C(255, 255, 255))
    RIM = skia.Paint(AntiAlias=True, Color=C(255, 190, 110))
    HOLE = skia.Paint(AntiAlias=True)
    HOLE.setBlendMode(skia.BlendMode.kClear)
    NONE = skia.Paint(Color=C(0, 0, 0, 0))
    NONE.setBlendMode(skia.BlendMode.kDst)


ANCH = {}
TAG = [""]
SHIFT = [0.0]          # vertical shift of the whole scene (layout vs. text)
SHIFTS = {}


def anchor(c, name, x, y):
    """Remember where a local point lands on screen (anchor pass only)."""
    if Pen.mode == "anchor":
        p = c.getTotalMatrix().mapXY(x, y)
        ANCH[TAG[0] + name] = (p.x(), p.y() - SHIFT[0])


def rope(c, p0, p1, sag=30.0, w=2.6):
    """A rope between two screen points, drawn in the current pen pass."""
    if Pen.mode == "anchor" or p0 is None or p1 is None:
        return
    base = ink()
    p = skia.Paint(AntiAlias=True, Color=base.getColor())
    p.setStyle(skia.Paint.kStroke_Style)
    p.setStrokeWidth(w + (3.2 if Pen.mode == "rim" else 0))
    p.setStrokeCap(skia.Paint.kRound_Cap)
    path = skia.Path()
    path.moveTo(*p0)
    path.quadTo((p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2 + sag, *p1)
    c.drawPath(path, p)


Pen.RIM.setStyle(skia.Paint.kStrokeAndFill_Style)
Pen.RIM.setStrokeWidth(3.2)
Pen.RIM.setStrokeJoin(skia.Paint.kRound_Join)


def ink():
    m = Pen.mode
    return Pen.FILL if m == "fill" else Pen.RIM if m == "rim" else Pen.MASK if m == "mask" else Pen.NONE


def fillp(c, path):
    if Pen.mode != "anchor":
        c.drawPath(path, ink())


def hole(c, path):
    if Pen.mode == "fill":
        c.drawPath(path, Pen.HOLE)


def detail(c, path, p):
    if Pen.mode == "fill":
        c.drawPath(path, p)


def begin_fig(c, bounds):
    if Pen.mode == "fill":
        c.saveLayer(skia.Rect.MakeLTRB(*bounds), None)
    else:
        c.save()


def limb(c, p0, r0, p1, r1):
    """Tapered capsule from p0 (radius r0) to p1 (radius r1)."""
    if Pen.mode == "anchor":
        return
    pt = ink()
    dx, dy = p1[0] - p0[0], p1[1] - p0[1]
    d = math.hypot(dx, dy) or 1.0
    nx, ny = -dy / d, dx / d
    c.drawPath(ppath([(p0[0] + nx * r0, p0[1] + ny * r0), (p1[0] + nx * r1, p1[1] + ny * r1),
                      (p1[0] - nx * r1, p1[1] - ny * r1), (p0[0] - nx * r0, p0[1] - ny * r0)]), pt)
    c.drawCircle(p0[0], p0[1], r0, pt)
    c.drawCircle(p1[0], p1[1], r1, pt)


def taper(c, pts, w0, w1, p=None):
    """A tapered band along a curve (feathers, tails, locks of hair)."""
    if Pen.mode == "anchor":
        return
    n = len(pts)
    left, right = [], []
    for i, q in enumerate(pts):
        a, b = pts[max(0, i - 1)], pts[min(n - 1, i + 1)]
        dx, dy = b[0] - a[0], b[1] - a[1]
        d = math.hypot(dx, dy) or 1.0
        w = mix(w0, w1, i / (n - 1))
        left.append((q[0] - dy / d * w, q[1] + dx / d * w))
        right.append((q[0] + dy / d * w, q[1] - dx / d * w))
    path = spath(left + right[::-1])
    if p is None:
        c.drawPath(path, ink())
    else:
        detail(c, path, p)


def boot(c, ax, s=1.0):
    """Boot with a curled toe; ankle at x=ax, facing +x, sole on y=0."""
    fillp(c, spath([(ax - 15 * s, -36), (ax + 10 * s, -38), (ax + 16 * s, -18), (ax + 40 * s, -11),
                    (ax + 56 * s, -16), (ax + 62 * s, -28, 0), (ax + 64 * s, -12), (ax + 52 * s, 0, 0),
                    (ax - 22 * s, 0, 0), (ax - 22 * s, -20)]))


def lappets(c, top_y, hem_y, x0, x1, hx0, hx1, n):
    """Armour skirt from the waist with a scalloped hem."""
    pts = [(x1, top_y), (x0, top_y), (hx0, hem_y - 10)]
    for i in range(n):
        xa, xb = mix(hx0, hx1, i / n), mix(hx0, hx1, (i + 0.5) / n)
        pts += [(xa, hem_y - 10), (xb, hem_y + 7)]
    pts.append((hx1, hem_y - 10))
    fillp(c, ppath(pts))


# ------------------------------------------------------------- characters
def rostam(c, X, Y, s, face, P, t):
    """Rostam: domed helmet with plume, long beard, tiger-skin mantle, mace.
    P: lean, head, jaw, hand (front wrist target), elbow_out."""
    begin_fig(c, (X - 240 * s, Y - 700 * s, X + 240 * s, Y + 30 * s))
    c.save()
    c.translate(X, Y)
    c.scale(s * face, s)
    br = 1.5 * math.sin(t * 2 * math.pi / 4.2)
    # legs: front leg forward, rear leg back
    limb(c, (-16, -250), 25, (-38, -130), 19)
    limb(c, (-38, -130), 19, (-62, -24), 13)
    boot(c, -62)
    limb(c, (16, -250), 26, (50, -132), 19)
    limb(c, (50, -132), 19, (66, -24), 13)
    boot(c, 66)
    c.save()
    c.translate(0, -250)
    c.rotate(P.get("lean", 0.0))
    c.translate(0, 250)
    # rear arm: hand on the hip, elbow out behind
    Sr = (-24, -410 + br)
    E, Wr, _ = ik(Sr, (-50, -268), 88, 84, -1)
    limb(c, Sr, 21, E, 17)
    limb(c, E, 17, Wr, 13)
    fillp(c, spath([(Wr[0] - 12, Wr[1] - 10), (Wr[0] + 14, Wr[1] - 6), (Wr[0] + 12, Wr[1] + 12),
                    (Wr[0] - 10, Wr[1] + 10)]))
    # torso, belt, armoured skirt
    fillp(c, spath([(-44, -262), (-54, -320), (-58, -384), (-46, -420 + br), (-18, -434 + br),
                    (10, -440 + br), (34, -428 + br), (50, -404 + br), (62, -364), (66, -330), (60, -296),
                    (50, -270), (54, -256, 0), (44, -246, 0), (-42, -246, 0)]))
    fillp(c, spath([(-50, -276, 0), (60, -276, 0), (62, -258, 0), (-50, -258, 0)]))
    lappets(c, -262, -150, -50, 56, -82, 92, 7)
    # tiger-skin mantle over the shoulders: jagged fur hem, a paw on the chest, the tail
    sw = 4 * math.sin(t * 1.3)
    m = [(-20, -438 + br, 0), (-56, -424 + br), (-72, -392), (-80, -352)]
    for i in range(8):
        x = mix(-82, 40, i / 7)
        m.append((x, -330 + (12 if i % 2 else 0) + 0.06 * (x + 82) * (1 if i % 2 else -0.3), 0))
    m += [(52, -372), (60, -404 + br), (40, -426 + br, 0)]
    fillp(c, spath(m))

    taper(c, bez((-70, -344), (-84 + sw, -296), (-98 + sw * 1.5, -250), (-86 + sw * 2, -214), 12), 6.5, 2.5)
    stripe = C(255, 170, 90, 75)
    for (x, y) in [(-62, -404), (-70, -372), (-30, -356), (4, -358), (-48, -344)]:
        taper(c, [(x - 7, y - 7), (x + 1, y), (x + 11, y + 3)], 2.2, 0.6, paint(stripe))
    # head: nods and turns about the neck
    c.save()
    c.translate(8, -446 + br)
    c.rotate(P.get("head", 0.0))
    c.translate(-8, 446 - br)
    c.translate(0, br)
    limb(c, (2, -432), 17, (8, -462), 17)
    c.save()
    c.translate(12, -578)
    c.rotate(2.5 * math.sin(t * 1.7))
    for k, (a, b, e) in enumerate([((-16, -50), (-60, -78), (-104, -58)),
                                   ((-10, -40), (-52, -60), (-92, -34)),
                                   ((-4, -30), (-36, -46), (-70, -14))]):
        taper(c, bez((0, 0), a, b, e, 12), 6.5 - k, 1.1)
    c.restore()
    fillp(c, spath([(-20, -472), (-24, -496), (-12, -520), (10, -527), (30, -515), (37, -504), (34, -497),
                    (38, -491), (49, -480, 0), (41, -476), (43, -471), (38, -467), (41, -462), (36, -452),
                    (20, -444), (2, -446), (-14, -456)]))
    # helmet: dome, rim, tall finial, mail curtain at the nape
    fillp(c, spath([(-27, -486, 0), (-30, -508), (-22, -532), (-6, -547), (12, -551), (30, -541),
                    (40, -522), (44, -507, 0), (12, -508), (-12, -500)]))
    fillp(c, spath([(-32, -510, 0), (46, -512, 0), (46, -504, 0), (-30, -500, 0)]))
    fillp(c, spath([(6, -548, 0), (9, -566), (5, -572), (12, -598, 0), (19, -572), (15, -566), (18, -548, 0)]))
    fillp(c, spath([(-27, -494), (-40, -464), (-44, -436, 0), (-22, -430, 0), (-10, -446), (-14, -472)]))
    hole(c, spath([(23, -497, 0), (28, -499.5), (33, -497, 0), (28, -495.5)]))
    for i in range(5):
        hole(c, spath([(mix(-22, 34, (i + 0.5) / 5) - 2.5, -506, 0), (mix(-22, 34, (i + 0.5) / 5), -508.5),
                       (mix(-22, 34, (i + 0.5) / 5) + 2.5, -506, 0), (mix(-22, 34, (i + 0.5) / 5), -503.5)]))
    # beard and moustache move with the jaw
    c.save()
    c.translate(-4, -470)
    c.rotate(P.get("jaw", 0.0))
    c.translate(4, 470)
    fillp(c, spath([(38, -478, 0), (60, -473, 0), (48, -466), (56, -452), (64, -432), (68, -410),
                    (66, -392), (56, -372), (48, -352, 0), (40, -372), (24, -396), (8, -418), (-4, -440),
                    (-10, -458), (-12, -470, 0), (2, -474), (22, -471)]))
    for k in range(3):
        taper(c, [(30 + k * 8, -446 + k * 4), (40 + k * 7, -420 + k * 6), (46 + k * 4, -392 + k * 8)],
              1.2, 0.4, paint(C(255, 170, 90, 60)))
    c.restore()
    c.restore()
    # front arm holding the mace upright
    S = (16, -410 + br)
    T = P.get("hand", (98, -300))
    E, Wr, a2 = ik(S, T, 92, 90, 1)
    limb(c, S, 23, E, 18)
    limb(c, E, 18, Wr, 13)
    hx, hy = Wr[0] + 8 * math.cos(a2), Wr[1] + 8 * math.sin(a2)
    c.save()
    c.translate(hx, hy)
    c.rotate(P.get("mace", 0.0))
    fillp(c, ppath([(-5, 96), (5, 96), (5, -112), (-5, -112)]))
    fillp(c, spath([(0, -108, 0), (16, -112), (25, -126), (24, -142), (14, -154), (0, -158, 0), (-14, -154),
                    (-24, -142), (-25, -126), (-16, -112)]))
    fillp(c, ppath([(-3, -156), (0, -176), (3, -156)]))
    for k in (-1, 1):
        hole(c, spath([(9 * k, -118, 0), (12 * k, -134), (8 * k, -150, 0), (6 * k, -134)]))
    c.drawCircle(0, 0, 0.1, ink())
    c.restore()
    fillp(c, spath([(hx - 13, hy - 12), (hx + 10, hy - 14), (hx + 15, hy + 2), (hx + 8, hy + 14),
                    (hx - 12, hy + 12)]))
    c.restore()
    c.restore()
    c.restore()


def sohrab(c, X, Y, s, face, P, t, wind=1.0):
    """Sohrab: young, beardless, long hair, tall plume, cape, spear.
    P: lean, head, jaw, hand (front wrist target), hand_open."""
    begin_fig(c, (X - 270 * s, Y - 820 * s, X + 270 * s, Y + 30 * s))
    c.save()
    c.translate(X, Y)
    c.scale(s * face, s)
    br = 1.4 * math.sin(t * 2 * math.pi / 3.8 + 1.0)
    limb(c, (-14, -250), 22, (-30, -130), 17)
    limb(c, (-30, -130), 17, (-54, -24), 12)
    boot(c, -54, 0.9)
    limb(c, (14, -250), 22, (44, -132), 17)
    limb(c, (44, -132), 17, (58, -24), 12)
    boot(c, 58, 0.9)
    # spear planted behind him, pennant in the wind
    sx = -78
    fillp(c, ppath([(sx - 3.5, 0), (sx - 3.5, -720), (sx + 3.5, -720), (sx + 3.5, 0)]))
    fillp(c, spath([(sx, -792, 0), (sx + 9, -752), (sx + 6, -724), (sx, -716, 0), (sx - 6, -724), (sx - 9, -752)]))
    pen = []
    for i in range(9):
        u = i / 8
        pen.append((sx - u * 74 * wind, -712 + u * 5 + 6 * math.sin(t * 6 + u * 5) * u))
    for i in range(8, -1, -1):
        u = i / 8
        pen.append((sx - u * 66 * wind - (10 if i == 8 else 0), -688 - u * 6 + 6 * math.sin(t * 6 + u * 5) * u))
    fillp(c, spath(pen))
    c.save()
    c.translate(0, -250)
    c.rotate(P.get("lean", 0.0))
    c.translate(0, 250)
    Sr = (-18, -410 + br)
    E, Wr, a2 = ik(Sr, (sx + 4, -322), 90, 86, -1)
    limb(c, Sr, 19, E, 15)
    limb(c, E, 15, Wr, 11)
    c.drawCircle(Wr[0], Wr[1], 12, ink())
    # cape from the shoulders, flowing back to the knees
    cape = [(0, -432 + br, 0), (-28, -428 + br)]
    for i in range(1, 9):
        u = i / 8
        cape.append((-36 - u * (26 + 50 * wind) + 7 * wind * math.sin(t * 3.1 - u * 4.5) * u, -420 + u * 262))
    for i in range(1, 5):
        u = i / 4
        cape.append((mix(-62 - 50 * wind, -40, u) + 4 * math.sin(t * 3.4 + u * 6),
                     -158 + 6 * math.sin(i * 2.2) - 4 * math.sin(t * 2.7 + u * 7)))
    cape += [(-38, -300), (-34, -400)]
    fillp(c, spath(cape))
    # slim torso, belt, tunic to the knee
    fillp(c, spath([(-36, -262), (-42, -326), (-46, -388), (-38, -420 + br), (-14, -434 + br), (14, -440 + br),
                    (34, -424 + br), (52, -394 + br), (56, -360), (44, -310), (34, -272), (38, -256, 0),
                    (30, -246, 0), (-34, -246, 0)]))
    fillp(c, spath([(-40, -278, 0), (42, -278, 0), (44, -262, 0), (-40, -262, 0)]))
    fl = 3 * math.sin(t * 2.9)
    fillp(c, spath([(-38, -264, 0), (40, -264, 0), (56, -200), (64, -140, 0), (26, -132, 0), (18, -150, 0),
                    (8, -132, 0), (-56 + fl, -136, 0), (-48, -200)]))
    for i in range(6):
        x = mix(-46, 56, (i + 0.5) / 6)
        hole(c, spath([(x - 2.4, -152, 0), (x, -154.6), (x + 2.4, -152, 0), (x, -149.4)]))
    # head
    c.save()
    c.translate(6, -446 + br)
    c.rotate(P.get("head", 0.0))
    c.translate(-6, 446 - br)
    c.translate(0, br)
    limb(c, (0, -432), 15, (6, -460), 15)
    for k, (dy, ln) in enumerate(((0, 1.0), (10, 0.86), (20, 0.72))):
        pts = []
        for i in range(9):
            u = i / 8
            pts.append((-18 - u * (34 + 30 * wind) * ln + 5 * wind * math.sin(t * 3.6 - u * 4 + k) * u,
                        -498 + dy + u * (96 - dy) * ln))
        taper(c, pts, 6.5 - k, 1.5)
    c.save()
    c.translate(10, -566)
    c.rotate(3 * math.sin(t * 1.9 + 0.7))
    for k, (a, b, e) in enumerate([((-6, -66), (-40, -112), (-92, -104)),
                                   ((-2, -54), (-34, -92), (-80, -76)),
                                   ((2, -42), (-26, -72), (-62, -52))]):
        taper(c, bez((0, 0), a, b, e, 12), 6 - k, 1.1)
    c.restore()
    fillp(c, spath([(-18, -472), (-21, -496), (-10, -518), (10, -526), (28, -515), (34, -503), (31, -496),
                    (35, -490), (44, -481, 0), (37, -477), (39, -472, 0), (30, -458), (12, -447), (-2, -449),
                    (-14, -458)]))
    c.save()
    c.translate(10, -470)
    c.rotate(P.get("jaw", 0.0))
    c.translate(-10, 470)
    fillp(c, spath([(39, -472, 0), (36, -468), (38, -463), (35, -456), (27, -449), (12, -447), (8, -462)]))
    c.restore()
    fillp(c, spath([(37, -474, 0), (45, -471.5), (40, -470, 0)]))
    # pointed helmet with a rim and a finial
    fillp(c, spath([(-25, -488, 0), (-27, -510), (-17, -532), (0, -550), (8, -564, 0), (16, -550),
                    (31, -532), (38, -512), (37, -505, 0), (8, -508), (-12, -500)]))
    fillp(c, spath([(-29, -512, 0), (40, -514, 0), (40, -506, 0), (-27, -502, 0)]))
    fillp(c, ppath([(6, -560), (9, -580), (12, -560)]))
    hole(c, spath([(19, -496, 0), (24, -498.5), (29, -496, 0), (24, -494.6)]))
    c.restore()
    # front arm: the gesturing hand
    S = (12, -408 + br)
    T = P.get("hand", (26, -254))
    E, Wr, a2 = ik(S, T, 92, 88, 1)
    limb(c, S, 20, E, 16)
    limb(c, E, 16, Wr, 12)
    op = P.get("hand_open", 0.0)
    c.save()
    c.translate(*Wr)
    c.rotate(math.degrees(a2) - 24 * op)
    if op > 0.3:
        fillp(c, spath([(-4, -9), (14, -10), (30, -8), (37, -3), (32, 3), (16, 9), (-2, 9)]))
        fillp(c, spath([(6, -9), (14, -20), (20, -18), (16, -8)]))
    else:
        c.drawCircle(8, 0, 13, ink())
    c.restore()
    c.restore()
    c.restore()
    c.restore()


# ------------------------------------------------------------ the world
class World:
    """Dusk battlefield between the two armies (cold open and title)."""

    HZ = 880

    def __init__(self, seed=7):
        rnd = random.Random(seed)
        xs = list(range(-500, 1600, 6))

        def ridge(base, amp, ph):
            out = []
            for x in xs:
                y = base
                for k in range(4):
                    y += amp / (1.9 ** k) * math.sin(x * 0.004 * (2.1 ** k) + ph[k])
                out.append((x, y))
            return out
        self.far = ridge(842, 26, [rnd.uniform(0, 6) for _ in range(4)])
        self.near = ridge(872, 12, [rnd.uniform(0, 6) for _ in range(4)])
        self.clouds = [(rnd.uniform(-300, 1300), y, rnd.uniform(520, 900), th, rnd.uniform(5, 10))
                       for y, th in ((252, 26), (318, 18), (392, 30), (452, 16))]
        self.dust = [(rnd.uniform(-100, 1180), rnd.uniform(260, 1150), rnd.uniform(1.2, 3.4),
                      rnd.uniform(6, 22), rnd.uniform(0, 6.3), rnd.uniform(0.3, 1.0)) for _ in range(90)]
        self.tufts = [(rnd.uniform(-40, 1120), rnd.uniform(10, 26), rnd.uniform(-0.4, 0.4)) for _ in range(46)]
        self.band = self._armies(rnd)
        v = np.zeros((H, W, 4), np.uint8)
        yy, xx = np.mgrid[0:H, 0:W]
        r = np.sqrt(((xx - 540) / 1.0) ** 2 + ((yy - 760) / 1.25) ** 2) / 1150
        v[..., 3] = (np.clip((r - 0.45) / 0.55, 0, 1) ** 1.6 * 160).astype(np.uint8)
        self.vig = skia.Image.fromarray(v)

    def _armies(self, rnd):
        """The two distant armies and the Turanian tents, drawn once."""
        x0, y0, w, h = -500, 780, 2100, 140
        arr = np.zeros((h, w, 4), np.uint8)
        s = skia.Surface(arr)
        c = s.getCanvas()
        c.translate(-x0, -y0)
        ac = paint(C(24, 8, 18))
        for (x, tall) in [(930, 44), (990, 50), (1060, 40), (1130, 52), (1205, 46), (1290, 42)]:
            c.drawPath(spath([(x - tall * 0.75, 897, 0), (x - tall * 0.5, 890 - tall * 0.35), (x, 897 - tall, 0),
                              (x + tall * 0.5, 890 - tall * 0.35), (x + tall * 0.75, 897, 0)]), ac)
            c.drawRect(skia.Rect.MakeLTRB(x - 1, 897 - tall - 16, x + 1, 897 - tall), ac)
            c.drawPath(ppath([(x + 1, 897 - tall - 16), (x + 13, 897 - tall - 12), (x + 1, 897 - tall - 9)]), ac)
        for side, xa, xb in (("ir", -300, 230), ("tu", 850, 1380)):
            for (yy, hh) in ((893, 22), (899, 27), (905, 32)):
                x = xa + rnd.uniform(0, 10)
                while x < xb:
                    hgt = hh * rnd.uniform(0.92, 1.08)
                    wd = hgt * 0.34
                    c.drawPath(ppath([(x - wd * 0.5, yy), (x - wd * 0.42, yy - hgt * 0.62),
                                      (x + wd * 0.42, yy - hgt * 0.62), (x + wd * 0.5, yy)]), ac)
                    c.drawCircle(x, yy - hgt * 0.72, hgt * 0.13, ac)
                    sx = x + wd * 0.45
                    c.drawRect(skia.Rect.MakeLTRB(sx - 0.7, yy - hgt * 1.45, sx + 0.7, yy - hgt * 0.3), ac)
                    if rnd.random() < 0.12:
                        fx = 1 if side == "ir" else -1
                        top = yy - hgt * 1.45
                        c.drawPath(ppath([(sx, top), (sx + fx * hgt * 0.7, top + 2 + rnd.uniform(-2, 2)),
                                          (sx + fx * hgt * 0.62, top + hgt * 0.42), (sx, top + hgt * 0.4)]), ac)
                    x += hh * rnd.uniform(0.55, 0.9)
        return skia.Image.fromarray(arr), (x0, y0)

    def sky(self, c, t, d, cam):
        stops0 = [(0.00, (18, 10, 34)), (0.22, (52, 20, 58)), (0.42, (126, 32, 54)), (0.60, (200, 70, 42)),
                  (0.76, (238, 130, 54)), (0.90, (247, 184, 90)), (1.00, (251, 210, 122))]
        stops1 = [(0.00, (8, 5, 18)), (0.24, (30, 10, 36)), (0.45, (92, 18, 40)), (0.62, (164, 42, 32)),
                  (0.78, (214, 88, 40)), (0.92, (234, 142, 64)), (1.00, (242, 172, 92))]
        stops = [(p, mixc(a, b, d)) for (p, a), (_, b) in zip(stops0, stops1)]
        p = skia.Paint()
        p.setShader(skia.GradientShader.MakeLinear([skia.Point(0, 0), skia.Point(0, self.HZ + 30)],
                                                   [C(*col) for _, col in stops], [s for s, _ in stops]))
        c.drawPaint(p)
        sun = (540, 655 + 85 * d)
        core = mixc((255, 240, 200), (255, 206, 140), d)
        edge = mixc((255, 200, 112), (244, 128, 64), d)
        with cam(0.25):
            gp = skia.Paint(AntiAlias=True)
            gp.setShader(skia.GradientShader.MakeRadial(skia.Point(*sun), 640, [
                C(*edge, 150), C(*edge, 64), C(*edge, 0)], [0.32, 0.58, 1.0]))
            c.drawCircle(sun[0], sun[1], 640, gp)
            rp = skia.Paint(AntiAlias=True)
            rp.setShader(skia.GradientShader.MakeRadial(skia.Point(*sun), 1150, [C(*core, 40), C(*core, 0)],
                                                        [0.25, 1.0]))
            for i in range(11):
                a = i * math.tau / 11 + t * 0.016 - 1.2
                wd = 0.04 + 0.02 * math.sin(i * 2.3)
                c.drawPath(ppath([sun, (sun[0] + 1150 * math.cos(a - wd), sun[1] + 1150 * math.sin(a - wd)),
                                  (sun[0] + 1150 * math.cos(a + wd), sun[1] + 1150 * math.sin(a + wd))]), rp)
            dp = skia.Paint(AntiAlias=True)
            dp.setShader(skia.GradientShader.MakeRadial(skia.Point(sun[0], sun[1] - 60), 300,
                                                        [C(*core), C(*core), C(*edge)], [0.0, 0.55, 1.0]))
            c.drawCircle(sun[0], sun[1], 275, dp)
        with cam(0.3):
            ccol = mixc((52, 16, 40), (28, 9, 24), d)
            for (x0, y, L, th, sp) in self.clouds:
                x = (x0 - sp * t + 400) % 1900 - 400
                for k, (a, sc) in enumerate(((120, 1.0), (200, 0.55))):
                    cp = skia.Path()
                    cp.moveTo(x - L / 2 * sc, y)
                    cp.cubicTo(x - L * 0.25 * sc, y - th * sc, x + L * 0.2 * sc, y - th * 0.8 * sc, x + L / 2 * sc, y + 2)
                    cp.cubicTo(x + L * 0.2 * sc, y + th * 0.45 * sc, x - L * 0.2 * sc, y + th * 0.5 * sc,
                               x - L / 2 * sc, y)
                    c.drawPath(cp, paint(C(*ccol, a)))

    def land(self, c, t, d, cam):
        HZ = self.HZ
        with cam(0.4):
            fp = skia.Paint(AntiAlias=True)
            fp.setShader(skia.GradientShader.MakeLinear([skia.Point(0, 790), skia.Point(0, HZ + 20)], [
                C(*mixc((112, 40, 64), (70, 22, 44), d)), C(*mixc((70, 24, 44), (40, 12, 30), d))]))
            c.drawPath(ppath([(-500, 2000)] + self.far + [(1600, 2000)]), fp)
        with cam(0.5):
            c.drawPath(ppath([(-500, 2000)] + self.near + [(1600, 2000)]),
                       paint(C(*mixc((48, 16, 32), (30, 9, 22), d))))
        with cam(0.6):
            pl = skia.Paint()
            pl.setShader(skia.GradientShader.MakeLinear([skia.Point(0, HZ), skia.Point(0, 930)], [
                C(*mixc((60, 22, 34), (40, 14, 26), d)), C(24, 8, 16)]))
            c.drawRect(skia.Rect.MakeLTRB(-500, HZ, 1600, 1000), pl)
            img, (x0, y0) = self.band
            c.drawImage(img, x0, y0)
            hz = skia.Paint()
            hc = mixc((246, 150, 80), (226, 96, 52), d)
            hz.setShader(skia.GradientShader.MakeLinear([skia.Point(0, 820), skia.Point(0, 960)], [
                C(*hc, 0), C(*hc, 92), C(*hc, 0)], [0.0, 0.55, 1.0]))
            c.drawRect(skia.Rect.MakeLTRB(-500, 820, 1600, 960), hz)
        with cam(0.8):
            gp = skia.Paint(AntiAlias=True)
            gp.setShader(skia.GradientShader.MakeLinear([skia.Point(0, 905), skia.Point(0, 1500)], [
                C(*mixc((52, 20, 24), (36, 12, 18), d)), C(16, 6, 10), C(4, 2, 5)], [0.0, 0.3, 1.0]))
            g = skia.Path()
            g.moveTo(-500, 912)
            g.quadTo(540, 930, 1600, 906)
            g.lineTo(1600, 2400)
            g.lineTo(-500, 2400)
            g.close()
            c.drawPath(g, gp)
            tc = paint(C(12, 5, 9))
            for (x, h, lean) in self.tufts:
                y = 912 + 18 * (1 - ((x - 540) / 1050) ** 2) - 2
                for k in range(-2, 3):
                    tip = (x + k * 4 + (lean + 0.25 * math.sin(t * 2 + x)) * h, y - h * (1 - abs(k) * 0.2))
                    c.drawPath(ppath([(x + k * 3 - 2, y + 2), tip, (x + k * 3 + 2, y + 2)]), tc)
            sh = skia.Paint(AntiAlias=True)
            sh.setShader(skia.GradientShader.MakeLinear([skia.Point(0, 935), skia.Point(0, 1500)],
                                                        [C(0, 0, 0, 150), C(0, 0, 0, 0)]))
            for fx in (350, 735):
                c.drawPath(ppath([(fx - 55, 935), (fx + 55, 935), (fx + 160, 1500), (fx - 120, 1500)]), sh)

    def foreground(self, c, t, cam):
        col = paint(C(10, 5, 8))
        with cam(1.35):
            a, b = (1150, 1620), (1000, 600)
            dx, dy = b[0] - a[0], b[1] - a[1]
            L = math.hypot(dx, dy)
            ux, uy = dx / L, dy / L
            c.drawPath(ppath([(a[0] - 5 * uy, a[1] + 5 * ux), (b[0] - 4 * uy, b[1] + 4 * ux),
                              (b[0] + 4 * uy, b[1] - 4 * ux), (a[0] + 5 * uy, a[1] - 5 * ux)]), col)
            tip = (b[0] + 48 * ux, b[1] + 48 * uy)
            c.drawPath(spath([(tip[0], tip[1], 0), (b[0] + 10, b[1] - 4), (b[0] + 2, b[1] + 6, 0),
                              (b[0] - 8, b[1] - 2)]), col)
            base = (b[0] + 8, b[1] + 26)
            pts = [(base[0] + i / 8 * 96, base[1] + i / 8 * 8 + 8 * math.sin(t * 5.2 - i / 8 * 5) * i / 8)
                   for i in range(9)]
            pts += [(base[0] + 96, base[1] + 30 + 8 * math.sin(t * 5.2 - 5)), (base[0] + 74, base[1] + 24, 0)]
            pts += [(base[0] + u * 80, base[1] + 44 + 9 * math.sin(t * 5.2 - u * 5) * u) for u in (0.55, 0.3, 0.0)]
            c.drawPath(spath(pts), col)
            a, b = (-60, 1560), (92, 690)
            dx, dy = b[0] - a[0], b[1] - a[1]
            L = math.hypot(dx, dy)
            ux, uy = dx / L, dy / L
            c.drawPath(ppath([(a[0] - 6 * uy, a[1] + 6 * ux), (b[0] - 5 * uy, b[1] + 5 * ux),
                              (b[0] + 5 * uy, b[1] - 5 * ux), (a[0] + 6 * uy, a[1] - 6 * ux)]), col)
            c.drawCircle(b[0], b[1] - 4, 7, col)
            base = (b[0] + 2, b[1] + 10)
            wv = lambda u: 7 * math.sin(t * 4.6 - u * 4.5) * u
            pts = [(base[0] + u * 84, base[1] + u * 8 + wv(u)) for u in (0, 0.25, 0.5, 0.75, 1.0)]
            pts += [(base[0] + 80, base[1] + 112 + wv(1), 0), (base[0] + 60, base[1] + 86 + wv(0.75), 0),
                    (base[0] + 42, base[1] + 118 + wv(0.5), 0), (base[0] + 22, base[1] + 92 + wv(0.25), 0),
                    (base[0] + 4, base[1] + 120, 0)]
            c.drawPath(spath(pts), col)

    def particles(self, c, t, d):
        dp = skia.Paint(AntiAlias=True)
        dp.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 1.6))
        base = mixc((255, 214, 150), (255, 170, 110), d)
        for (x0, y0, r, sp, ph, a) in self.dust:
            x = (x0 + sp * t) % 1280 - 100
            y = (y0 - 6 * t * a + 10 * math.sin(t * 0.7 + ph) - 200) % 1000 + 200
            fl = 0.55 + 0.45 * math.sin(t * 2.3 + ph * 3)
            dp.setColor(C(*base, 140 * a * fl))
            c.drawCircle(x, y, r, dp)


# --------------------------------------------------------------- engine
class Anim:
    def __init__(self, ep_dir):
        self.talk = Talk(ep_dir)
        self.world = World()
        self.arr = np.zeros((H, W, 4), np.uint8)
        self.surface = skia.Surface(self.arr)
        self.lo = skia.Surface(W // LO, H // LO)
        self.lo2 = skia.Surface(W // LO, H // LO)
        tl = json.load(open(f"{ep_dir}/audio/timeline.json", encoding="utf-8"))
        sc = tl["scenes"]
        self.start = {s["id"]: (0.0 if i == 0 else s["start"]) for i, s in enumerate(sc)}
        self.end = {s["id"]: (sc[i + 1]["start"] if i + 1 < len(sc) else tl["duration"]) for i, s in enumerate(sc)}
        self.cache = {}

    def has(self, sid):
        return sid in SCENES

    def figures(self, c, draw, glow, box, alpha=150, sigma=3.2, anchors=False, rim=True):
        """Draw puppets with a soft backlight glow and a bright rim.
        draw(canvas) draws all figures with their camera transform."""
        if anchors:
            ANCH.clear()
            Pen.mode = "anchor"
            draw(c)
        lc = self.lo.getCanvas()
        lc.clear(C(0, 0, 0, 0))
        lc.save()
        lc.scale(1 / LO, 1 / LO)
        lc.translate(0, SHIFT[0])
        Pen.mode = "mask"
        draw(lc)
        lc.restore()
        img = self.lo.makeImageSnapshot()
        bc = self.lo2.getCanvas()
        bc.clear(C(0, 0, 0, 0))
        p = skia.Paint()
        p.setImageFilter(skia.ImageFilters.Blur(sigma, sigma, skia.TileMode.kDecal, None))
        p.setColorFilter(skia.ColorFilters.Blend(C(*glow, alpha), skia.BlendMode.kSrcIn))
        bc.drawImage(img, 0, 0, skia.SamplingOptions(), p)
        x0, y0, x1, y1 = box
        y0, y1 = max(0, y0 + SHIFT[0]), min(H, y1 + SHIFT[0])
        c.save()
        c.resetMatrix()
        c.drawImageRect(self.lo2.makeImageSnapshot(), skia.Rect.MakeLTRB(x0 / LO, y0 / LO, x1 / LO, y1 / LO),
                        skia.Rect.MakeLTRB(x0, y0, x1, y1), skia.SamplingOptions(skia.FilterMode.kLinear))
        c.restore()
        if rim:
            Pen.RIM.setColor(C(*glow))
            Pen.mode = "rim"
            draw(c)
        Pen.mode = "fill"
        draw(c)

    def frame(self, sid, t_global):
        c = self.surface.getCanvas()
        c.clear(C(0, 0, 0))
        c.save()
        SHIFT[0] = SHIFTS.get(sid, 0.0)
        c.translate(0, SHIFT[0])
        try:
            SCENES[sid](self, c, t_global)
        finally:
            SHIFT[0] = 0.0
        c.restore()
        return Image.fromarray(self.arr, "RGBA").convert("RGB")


# ------------------------------------------------------------- talk sync
class Talk:
    """Mouth/beard movement from the loudness of each character's lines."""

    def __init__(self, ep_dir):
        script = json.load(open(f"{ep_dir}/script.json", encoding="utf-8"))
        tl = json.load(open(f"{ep_dir}/audio/timeline.json", encoding="utf-8"))
        w = wave.open(f"{ep_dir}/audio/episode.wav")
        sr, n, ch = w.getframerate(), w.getnframes(), w.getnchannels()
        x = np.frombuffer(w.readframes(n), dtype=np.int16).astype(np.float32)
        if ch > 1:
            x = x.reshape(-1, ch).mean(1)
        hop = sr // FPS
        nf = len(x) // hop
        rms = np.sqrt((x[:nf * hop].reshape(nf, hop) ** 2).mean(1))
        self.env = {}
        for sc, ts in zip(script["scenes"], tl["scenes"]):
            for ln, lt in zip(sc["lines"], ts["lines"]):
                a, b = int(lt["start"] * FPS), int(lt["end"] * FPS)
                seg = rms[a:b]
                if len(seg) == 0:
                    continue
                arr = self.env.setdefault(ln["role"], np.zeros(nf, np.float32))
                arr[a:b] = np.clip(seg / (np.percentile(seg, 92) + 1e-6), 0, 1)
        for k in self.env:
            self.env[k] = np.convolve(self.env[k], [0.25, 0.5, 0.25], mode="same")

    def __call__(self, role, t):
        arr = self.env.get(role)
        i = int(round(t * FPS))
        return float(arr[i]) if arr is not None and 0 <= i < len(arr) else 0.0


# --------------------------------------------------------------- scenes
def cold_open(an, c, t):
    """S01 + TITLE: Rostam and Sohrab face each other at sunset (global time t)."""
    w = an.world
    d = sstep(8.5, 22.0, t)
    zoom = 1 + 0.12 * ease(t / 22.3)
    focus = (545, 520)
    cam = Cam(c, focus, zoom)
    w.sky(c, t, d, cam)
    w.land(c, t, d, cam)
    glow = mixc((255, 188, 106), (250, 134, 72), d)
    sp = {"hand": _k(t, [(0.6, (28, -256)), (1.4, (86, -334)), (2.6, (82, -330)), (3.4, (50, -292)),
                           (4.0, (116, -356)), (5.9, (116, -352)), (7.2, (30, -256))]),
          "hand_open": _k(t, [(0.9, 0.0), (1.3, 1.0), (6.4, 1.0), (7.0, 0.0)]),
          "lean": _k(t, [(3.6, 0.0), (4.4, 2.6), (6.0, 2.6), (7.4, 0.0)]),
          "head": _k(t, [(5.9, 0.0), (6.4, -3.5), (8.6, -3.5), (9.8, 1.5)]),
          "jaw": 9.0 * an.talk("SOHRAB", t)}
    rp = {"head": _k(t, [(5.7, 0.0), (6.3, 5.0), (8.3, 5.0), (10.2, 11.0)]),
          "lean": _k(t, [(5.8, 0.0), (6.4, -1.4), (9.0, -1.4), (11.0, 0.6)]),
          "hand": _k(t, [(9.4, (98, -300)), (11.0, (96, -290))]),
          "mace": _k(t, [(9.4, 0.0), (11.0, -4.0)]),
          "jaw": 6.0 * an.talk("ROSTAM", t)}

    def figs(cc):
        with Cam(cc, focus, zoom)(1.0):
            rostam(cc, 350, 935, 1.0, 1, rp, t)
            sohrab(cc, 735, 935, 0.98, -1, sp, t)
    an.figures(c, figs, glow, (40, 120, 1040, 1080))
    w.foreground(c, t, cam)
    w.particles(c, t, d)
    c.drawImage(w.vig, 0, 0)


SCENES = {}          # filled by the part's scenes module (epNN_scenes.py / pNN_scenes.py)


if __name__ == "__main__":
    if sys.argv[1] == "still":
        ep, t, out = sys.argv[2], float(sys.argv[3]), sys.argv[4]
        sid = sys.argv[5] if len(sys.argv) > 5 else "S01"
        Anim(ep).frame(sid, t).save(out)
