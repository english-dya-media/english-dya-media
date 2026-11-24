"""Part 2 · The Proposal — 2D cartoon. Timing matches leyli/p02_audio.py
(scene starts s1 0, s2 8.0, s3 12.6, s4 40.0, s5 71.0, s6 103.4; end card 135.4; total 140.6)."""
import math, random
from PIL import Image, ImageFilter
from film import Shot, W, H, ease, lerp, talk_pose, blink_at, cam_push, Motes, svg_render
from chars import pose, camel, gazelle, Ctx, FEET
from stage import at_neck, at_feet, Glow, lw_for
import bgs, lbg
from cast import *
from p01_scenes import (P, tp, bg, cam_xy, seated, body_xy, birds, SandWind, spec_copy, DUSKL, SUN_DUSK, DAWNL, SUN_DAWN, DAYL, SUN_DAY,
                        LAMPC)
import p02_audio as AU

NIGHTK = dict(ambient=(0.74, 0.74, 0.9), rim=(5, -3), rim_col=(1.0, 0.85, 0.6), rim_str=0.8, ramp=(0, W, 0.95, 1.05))   # the Kaaba's lamps
TORCHL = dict(ambient=(0.8, 0.68, 0.7), rim=(-5, -2), rim_col=(1.0, 0.62, 0.32), rim_str=0.95, ramp=(0, W, 1.06, 0.86))


def L(t0, *ids):
    """line ids -> [(id, start within a shot that begins at t0)]; a line said twice is taken at its first time after t0"""
    out = []
    for i in ids:
        ts_ = [t for lid, t in AU.LINES if lid == i and t >= t0 - 0.5]
        out.append((i, min(ts_) - t0))
    return out


def flame(x, y, t, s=1.0, seed=0):
    ph = seed * 1.3
    h = (120 + 30 * math.sin(t * 13 + ph) + 18 * math.sin(t * 7.3 + ph)) * s
    sw = 10 * math.sin(t * 5 + ph) * s
    return (f'<path d="M {x - 30 * s:.1f} {y:.1f} C {x - 40 * s:.1f} {y - h * 0.45:.1f}, {x - 10 * s + sw:.1f} {y - h * 0.8:.1f}, {x + sw:.1f} {y - h:.1f} '
            f'C {x + 14 * s + sw:.1f} {y - h * 0.75:.1f}, {x + 40 * s:.1f} {y - h * 0.45:.1f}, {x + 30 * s:.1f} {y:.1f} Z" fill="#ff8a1a"/>'
            f'<path d="M {x - 16 * s:.1f} {y:.1f} C {x - 20 * s:.1f} {y - h * 0.35:.1f}, {x - 4 * s + sw * 0.6:.1f} {y - h * 0.6:.1f}, {x + sw * 0.6:.1f} {y - h * 0.72:.1f} '
            f'C {x + 8 * s + sw * 0.6:.1f} {y - h * 0.55:.1f}, {x + 20 * s:.1f} {y - h * 0.35:.1f}, {x + 16 * s:.1f} {y:.1f} Z" fill="#ffd84a"/>')


def gifts(x, y, s=1.0):
    """the gifts set down before Leyli's father's tent: two chests with gold, bolts of silk, a silver jug"""
    o = f'<g transform="translate({x},{y}) scale({s})">'
    o += ('<rect x="-230" y="-90" width="170" height="100" rx="8" fill="#6a3a1a" stroke="#1b0f0a" stroke-width="4"/>'
          '<path d="M -230 -60 L -60 -60" stroke="#c9a24a" stroke-width="8"/><rect x="-158" y="-74" width="26" height="30" rx="4" fill="#c9a24a" stroke="#1b0f0a" stroke-width="3"/>'
          '<path d="M -236 -90 C -220 -130, -70 -130, -54 -90 Z" fill="#7a4a22" stroke="#1b0f0a" stroke-width="4"/>'
          '<circle cx="-200" cy="-104" r="9" fill="#f0d070"/><circle cx="-180" cy="-110" r="9" fill="#f0d070"/><circle cx="-100" cy="-104" r="9" fill="#f0d070"/>')
    for k, (col, hi) in enumerate((("#2a6a8a", "#8ac8e0"), ("#8a1a4a", "#e08ab0"), ("#c9a24a", "#f8e8a8"))):
        yy = -24 - k * 34
        o += (f'<rect x="-20" y="{yy}" width="190" height="34" rx="17" fill="{col}" stroke="#1b0f0a" stroke-width="3"/>'
              f'<path d="M -6 {yy + 10} L 156 {yy + 10}" stroke="{hi}" stroke-width="4" opacity="0.7"/>')
    o += ('<path d="M 200 10 C 180 -20, 190 -70, 220 -90 L 214 -120 L 246 -120 L 240 -90 C 270 -70, 280 -20, 260 10 Z" fill="#c8ccd4" stroke="#1b0f0a" stroke-width="3"/>'
          '<path d="M 262 -70 C 300 -70, 296 -20, 262 -24" stroke="#c8ccd4" stroke-width="8" fill="none"/>')
    return o + '</g>'


# ================================================================ S1 the hook (0-8.0): Majnun prays at the door of the Kaaba
def kaaba_bg(blur=0):
    return bg("kaaba", lbg.kaaba, blur)


def kaaba_close_bg(blur=0):
    return bg("kaaba_close", lbg.kaaba_close, blur)


def praying(t, lines, seed, close=False, **kw):
    """Majnun with his hands raised to the door's threshold, palms open, eyes closed"""
    eyes = kw.pop("eyes", 0.92)
    up = ("ik", -190, -330, "down") if not close else ("ik", -210, -260, "down")
    q = tp(lines, t, seed, turn=kw.pop("turn", 0.15), gx=0.1, gy=kw.pop("gy", -0.4), sad=kw.pop("sad", 0.7), brow=0.8, furrow=-0.4,
           armR=up, armL=("ik", -up[1], up[2], "down"), openR=True, openL=True, wind=0.3, **kw)
    q["blink"] = max(q["blink"], eyes)
    return q


def s1():
    kc = kaaba_close_bg()
    kbb = kaaba_close_bg(6)
    LA = L(0.0, "p2s1a")
    camA = cam_push(1.0, 1.08, 520, 760, 3.9)

    def midA(t):
        return at_feet(MAJNUN, praying(t, LA, 1), t, 470, 1580, 0.62)
    A = Shot(3.9, kc, midA, cam=camA, light=NIGHTK, grade="night", bloom=0.6, fade_in=0.5)
    LB = L(3.9, "p2s1b")
    camB = cam_push(1.0, 1.05, 540, 860, 4.1)

    def midB(t):
        q = praying(t, LB, 2, close=True, gy=-0.5 if t < 2.4 else -0.8)
        if t > 2.6:
            q["blink"] = blink_at(t, 2)
        return at_neck(MAJNUN, q, t, 540, 1000, 1.05)
    B = Shot(4.1, kbb, midB, cam=camB, light=NIGHTK, grade="night", bloom=0.6, fade_out=0.6,
             fx=[Motes(40, 101, (255, 230, 190), (0, 300, W, 1200), (0, -10), amax=80)])
    return [A, B]


# ================================================================ S2 title (8.0-12.6): a caravan on the dunes at dawn
def s2():
    dn = bg("dunes_dawn", lambda: lbg.dunes("dawn"))

    def mid(t):
        c = Ctx(lw_for(0.14))
        o = ""
        for k in range(4):
            x = 120 + k * 150 + 26 * t
            o += f'<g transform="translate({x:.1f},{1176 - 2 * k}) scale(0.14)">{camel(c, walk=True, phase=t * 3.0 + k, t=t + k, saddle=True)}</g>'
        return birds(t, 900, 520, n=4, s=0.8) + o
    return [Shot(4.6, dn, mid, cam=cam_push(1.0, 1.05, 540, 1000, 4.6), sun=SUN_DAWN, light=DAWNL, bloom=0.7, fade_in=0.4, fade_out=0.5,
                 fx=[Motes(30, 201, (255, 230, 210), (0, 1000, W, 1600), (-8, -4), amax=70)])]


# ================================================================ S3 years later: Majnun in the desert; the chief and the elder (12.6-40.0)
def s3():
    dd = bg("dunes_day", lambda: lbg.dunes("day"))
    camA = cam_push(1.0, 1.06, 560, 1000, 9.6)

    def midA(t):
        u = t / 9.6
        c = Ctx(lw_for(0.8))
        o = ""
        for k, (x0, x1, y, s) in enumerate(((40, 330, 1215, 0.8), (-120, 200, 1205, 0.7))):
            gw = t < 9.0
            o += (f'<g transform="translate({lerp(x0, x1, u):.1f},{y}) scale({-s},{s})">'          # flipped: they walk to the right
                  f'{gazelle(c, t=t + k, seed=k, walk=gw, phase=t * 5.0 + k, look=0.2)}</g>')
        q = P(legs="walk", phase=t * 4.2, turn=0.35, gx=0.7, gy=-0.2, sad=0.3, brow=0.5, smile=0.2, armL="relaxed", armR="relaxed", wind=1.0,
              blink=blink_at(t, 3), breathe=math.sin(t * 2))
        o += at_feet(MAJNUN, q, t, lerp(430, 760, u), 1240, 0.55)
        return o
    A = Shot(9.6, dd, midA, cam=camA, light=DAYL, sun=SUN_DAY, bloom=0.5,
             fx=[SandWind(160, 301, (0, 1000, W, 1900), (500, 900), strength=lambda t: 0.5)])

    ddb = bg("dunes_day", lambda: lbg.dunes("day"), 6)
    LB = L(22.2, "p2s3c")
    camB = cam_push(1.0, 1.05, 540, 860, 4.4)

    def midB(t):
        q = tp(LB, t, 4, turn=0.2, gx=0.3, gy=-0.6, sad=0.3, brow=0.6, furrow=-0.3, smile=0.35, armL="relaxed", armR="chest" if t > 1.0 else "relaxed",
               wind=1.0)
        return at_neck(MAJNUN, q, t, 540, 1000, 1.05)
    B = Shot(4.4, ddb, midB, cam=camB, light=DAYL, sun=SUN_DAY, fx=[SandWind(120, 302, (0, 300, W, 1900), (500, 900), strength=lambda t: 0.4)])

    ct = bg("chief_tent_day", lambda: lbg.chief_tent("day"))
    ctb = bg("chief_tent_day", lambda: lbg.chief_tent("day"), 6)
    LC1 = L(26.6, "p2s3d")
    camC1 = cam_push(1.0, 1.04, 540, 1000, 3.7)

    def midC1(t):
        e = tp(LC1, t, 5, turn=-0.35, gx=-0.8, gy=0.1, sad=0.5, brow=0.7, furrow=-0.2, armL="relaxed", armR="offer" if 0.8 < t < 3.0 else "relaxed",
               wind=0.3)
        c = tp([], t, 6, turn=0.35, gx=0.8, gy=0.4, sad=0.6, brow=0.6, furrow=-0.2, armL="relaxed", armR="relaxed", wind=0.3)
        return at_feet(CHIEF, c, t, 360, 1640, 0.66) + at_feet(ELDER, e, t, 730, 1640, 0.64)
    C1 = Shot(3.7, ct, midC1, cam=camC1, light=DAYL, sun=SUN_DAY, fade_in=0.3)
    LC2 = L(30.3, "p2s3e")
    camC2 = cam_push(1.0, 1.05, 540, 860, 5.5)

    def midC2(t):
        q = tp(LC2, t, 7, turn=0.25, gx=0.6, gy=0.0, sad=0.2, brow=0.3, furrow=0.6, armL="relaxed", armR="chest" if t > 1.5 else "relaxed", wind=0.3)
        return at_neck(CHIEF, q, t, 540, 960, 1.0)
    C2 = Shot(5.5, ctb, midC2, cam=camC2, light=DAYL, sun=SUN_DAY)
    LC3 = L(35.8, "p2s3f")
    camC3 = cam_push(1.0, 1.04, 540, 860, 4.2)

    def midC3(t):
        q = tp(LC3, t, 8, turn=-0.25, gx=-0.6, gy=0.1, brow=0.5, furrow=0.2, smile=0.15, armL="relaxed", armR="offer" if 0.4 < t < 2.4 else "relaxed",
               wind=0.3)
        return at_neck(ELDER, q, t, 540, 960, 1.0)
    C3 = Shot(4.2, ctb, midC3, cam=camC3, light=DAYL, sun=SUN_DAY, fade_out=0.4)
    return [A, B, C1, C2, C3]


# ================================================================ S4 Leyli's tribe at dusk: the gifts; the refusal (40.0-71.0)
def s4():
    lt = bg("leyli_tent_dusk", lambda: lbg.leyli_tent("dusk"))
    ltb = bg("leyli_tent_dusk", lambda: lbg.leyli_tent("dusk"), 6)
    camA = cam_push(1.0, 1.05, 560, 1050, 5.4)

    def midA(t):
        c = Ctx(lw_for(0.5))
        o = f'<g transform="translate(250,1470) scale(0.5)">{camel(c, t=t, saddle=True, blanket="#5a1a1e")}</g>'
        o += gifts(540, 1560, 0.7)
        for k, (S, x, y) in enumerate(((SERVANT_A, 420, 1500), (SERVANT_B, 660, 1490))):
            q = P(turn=0.2 if k == 0 else -0.2, gx=0.4 if k == 0 else -0.4, gy=0.4, brow=0.2, armL="chest", armR="chest", blink=blink_at(t, 10 + k),
                  breathe=math.sin(t * 2 + k), wind=0.4)
            o += at_feet(S, q, t, x, y, 0.46)
        u = ease(t / 2.4)
        cq = P(legs="walk" if t < 2.4 else "stand", phase=t * 4.4, turn=0.35, gx=0.7, gy=0.0, brow=0.3, smile=0.2, armL="relaxed",
               armR="relaxed" if t < 3.0 else "offer", wind=0.5, blink=blink_at(t, 12), breathe=math.sin(t * 1.7))
        o += at_feet(CHIEF, cq, t, lerp(120, 320, u), 1600, 0.56)
        fq = P(turn=-0.35, gx=-0.7, gy=0.1, furrow=0.8, brow=-0.1, armL="relaxed", armR="relaxed", wind=0.5, blink=blink_at(t, 13),
               breathe=math.sin(t * 1.5))
        o += at_feet(LEYLI_FATHER, fq, t, 840, 1590, 0.58)
        return o
    A = Shot(5.4, lt, midA, cam=camA, light=DUSKL, sun=SUN_DUSK, bloom=0.6)

    LB = L(45.4, "p2s4b")
    camB = cam_push(1.0, 1.04, 540, 900, 4.8)

    def midB(t):
        c = tp(LB, t, 14, turn=0.35, gx=0.8, gy=0.0, brow=0.4, smile=0.25, armL="relaxed", armR="offer" if 0.4 < t < 3.6 else "chest", wind=0.4)
        f = tp([], t, 15, turn=-0.35, gx=-0.8, gy=0.1, furrow=0.8, brow=-0.1, armL="relaxed", armR="relaxed", wind=0.4)
        return at_feet(CHIEF, c, t, 330, 1720, 0.82) + at_feet(LEYLI_FATHER, f, t, 770, 1720, 0.84)
    B = Shot(4.8, ltb, midB, cam=camB, light=DUSKL, sun=SUN_DUSK)

    LC = L(50.2, "p2s4c", "p2s4d")
    camC = cam_push(1.0, 1.06, 540, 860, 8.2)

    def midC(t):
        cold = ease((t - 3.6) / 0.4)
        q = tp(LC, t, 16, turn=-0.25, gx=-0.6, gy=0.0, furrow=0.5 + 0.5 * cold, brow=0.2 - 0.4 * cold, smile=0.15 * (1 - cold),
               armL="relaxed", armR="offer" if 0.6 < t < 2.8 else ("point" if 5.6 < t < 7.2 else "relaxed"), wind=0.3)
        return at_neck(LEYLI_FATHER, q, t, 540, 960, 1.0)
    C = Shot(8.2, ltb, midC, cam=camC, light=DUSKL, sun=SUN_DUSK)

    LD = L(58.4, "p2s4e")
    camD = cam_push(1.0, 1.05, 540, 860, 4.2)

    def midD(t):
        q = tp(LD, t, 17, turn=0.25, gx=0.6, gy=0.2, sad=0.6, brow=0.8, furrow=-0.4, armL="relaxed", armR="chest", wind=0.3)
        return at_neck(CHIEF, q, t, 540, 960, 1.0)
    D = Shot(4.2, ltb, midD, cam=camD, light=DUSKL, sun=SUN_DUSK)

    tnb = bg("tent_night", lbg.tent_night, 6)
    camE = cam_push(1.0, 1.05, 560, 860, 3.6)

    def midE(t):
        q = tp([], t, 18, turn=0.3, gx=0.8, gy=0.3 + 0.3 * ease((t - 1.8) / 0.6), sad=0.4 + 0.5 * ease((t - 1.0) / 1.2), brow=0.8, furrow=-0.4,
               armL="relaxed", armR="chest", wind=0.1)
        return at_neck(LEYLI_W, q, t, 560, 1000, 1.08)
    E = Shot(3.6, tnb, midE, cam=camE, light=LAMPC, grade="fire", bloom=0.5)

    LF = L(66.2, "p2s4f")
    camF = cam_push(1.0, 1.06, 540, 860, 4.8)

    def midF(t):
        away = ease((t - 3.2) / 0.6)
        q = tp(LF, t, 19, turn=-0.25 - 0.4 * away, gx=-0.6 - 0.3 * away, gy=0.0, furrow=1.0, brow=-0.3, armL="relaxed", armR="relaxed", wind=0.3)
        return at_neck(LEYLI_FATHER, q, t, 540, 960, 1.0)
    F = Shot(4.8, ltb, midF, cam=camF, light=DUSKL, sun=SUN_DUSK, fade_out=0.5)
    return [A, B, C, D, E, F]


# ================================================================ S5 Mecca: the prayer at the Kaaba (71.0-103.4)
def s5():
    kb = kaaba_bg()
    kbb = kaaba_bg(6)
    camA = cam_push(1.0, 1.06, 560, 1100, 4.4)

    A = Shot(4.4, kb, None, cam=camA, light=NIGHTK, grade="night", bloom=0.6, fade_in=0.4,
             fx=[Motes(40, 500, (255, 236, 200), (0, 1000, W, 1500), (0, -8), amax=70)])

    LB = L(75.4, "p2s5b")
    camB = cam_push(1.0, 1.05, 540, 860, 6.8)

    def midB(t):
        q = tp(LB, t, 22, turn=0.25, gx=0.6, gy=0.1, sad=0.5, brow=0.7, furrow=-0.2, armL="relaxed", armR="offer" if 0.4 < t < 3.0 else "relaxed",
               wind=0.2)
        return at_neck(CHIEF, q, t, 540, 960, 1.0)
    B = Shot(6.8, kbb, midB, cam=camB, light=NIGHTK, grade="night", bloom=0.5)

    LC = L(82.2, "p2s5c", "p2s5d")
    kc = kaaba_close_bg()
    camC = cam_push(1.0, 1.1, 520, 760, 10.0)

    def midC(t):
        firm = ease((t - 5.4) / 0.5)
        q = praying(t, LC, 23, gy=-0.4 - 0.3 * firm, sad=0.7 - 0.3 * firm)
        if 4.8 < t < 5.6:
            q["blink"] = blink_at(t, 23)
        return at_feet(MAJNUN, q, t, 470, 1580, 0.62)
    C1 = Shot(10.0, kc, midC, cam=camC, light=NIGHTK, grade="night", bloom=0.6)

    kcb = kaaba_close_bg(6)
    LC2 = L(92.2, "p2s1a", "p2s1b")
    camC2 = cam_push(1.0, 1.06, 540, 860, 5.6)

    def midC2(t):
        q = praying(t, LC2, 25, close=True, sad=0.85)
        return at_neck(MAJNUN, q, t, 540, 1000, 1.05)
    C2 = Shot(5.6, kcb, midC2, cam=camC2, light=NIGHTK, grade="night", bloom=0.6,
              fx=[Motes(40, 501, (255, 230, 190), (0, 300, W, 1200), (0, -10), amax=80)])

    camD = cam_push(1.0, 1.05, 540, 860, 5.6)

    def midD(t):
        q = tp([], t, 26, turn=0.15, gx=0.3, gy=0.6, sad=0.95, brow=0.9, furrow=-0.5, armL="relaxed", armR="chest", wind=0.2)
        q["blink"] = max(q["blink"], 0.9 * ease((t - 2.4) / 0.5))
        return at_neck(CHIEF, q, t, 540, 960, 1.0)
    D = Shot(5.6, kcb, midD, cam=camD, light=NIGHTK, grade="night", bloom=0.5, fade_out=0.6)
    return [A, B, C1, C2, D]


# ================================================================ S6 the ruler; the messenger; the father runs (103.4-140.6)
def s6():
    cd = bgs.cached("court_dusk", bgs.court_dusk)
    cdb = bgs.cached("court_dusk_b6", lambda: bgs.cached("court_dusk", bgs.court_dusk).filter(ImageFilter.GaussianBlur(6)))
    LA = L(103.4, "p2s6b")
    camA = cam_push(1.0, 1.06, 540, 900, 8.5)

    def midA(t):
        o = flame(170, 720, t, 0.5, 1) + flame(910, 720, t + 0.7, 0.5, 2)
        r = tp([], t, 30, legs="sit", turn=0.2, gx=0.5, gy=0.4, furrow=0.4, brow=0.1, armL=("ik", 60, 430), armR=("ik", -60, 430), wind=0.1)
        o += seated(RULER, r, t, 540, 862, 0.5)
        k = tp(LA, t, 31, turn=-0.3, gx=-0.6, gy=-0.6, furrow=0.9, brow=-0.1, armL="relaxed", armR="point" if t > 5.8 else "relaxed", wind=0.3)
        o += at_feet(KINSMAN, k, t, 800, 1230, 0.5)
        for gx_ in (110, 230):
            o += at_feet(SERVANT_A if gx_ == 110 else SERVANT_B, P(turn=0.3, gx=0.5, gy=-0.3, armL="chest", armR="relaxed", blink=blink_at(t, gx_)),
                         t, gx_, 1215, 0.44)
        return o
    A1 = Shot(8.5, cd, midA, cam=camA, light=TORCHL, grade="fire", bloom=0.6, fade_in=0.4,
              fx=[Glow(lambda t: cam_xy(camA, t, 170, 680), 220, (255, 170, 90), 0.4), Glow(lambda t: cam_xy(camA, t, 910, 680), 220, (255, 170, 90), 0.4)])

    LA2 = L(111.9, "p2s6c")
    camA2 = cam_push(1.0, 1.05, 540, 860, 5.3)

    def midA2(t):
        q = tp(LA2, t, 32, turn=0.2, gx=0.4, gy=0.2, furrow=0.6, brow=-0.2, smile=0.1, armL="relaxed", armR="offer" if 1.4 < t < 3.4 else "relaxed",
               openR=True, wind=0.1)
        return at_neck(RULER, q, t, 540, 960, 1.0)
    A2 = Shot(5.3, cdb, midA2, cam=camA2, light=TORCHL, grade="fire", bloom=0.5)

    cpd = bg("camp_dusk", lambda: lbg.camp("dusk"))
    cpdb = bg("camp_dusk", lambda: lbg.camp("dusk"), 6)
    LB = L(117.2, "p2s6d")
    camB = cam_push(1.0, 1.05, 560, 1000, 7.4)
    RUNIN = AU.RUN - 117.2

    def midB(t):
        u = ease((t - RUNIN + 0.6) / 1.4)
        turned = ease((t - RUNIN - 0.4) / 0.4)
        c = tp([], t, 33, turn=-0.1 + 0.45 * turned, gx=-0.3 + 1.1 * turned, gy=0.2 - 0.2 * turned, brow=0.2 + 0.6 * turned, sad=0.6 * ease((t - 3.2) / 0.6),
               mouth_o=0.0, armL="relaxed", armR="relaxed" if t < 3.0 else "chest", wind=0.5)
        m = tp(LB, t, 34, legs="walk" if u < 1 else "stand", phase=t * 9.0, turn=-0.35, gx=-0.8, gy=-0.1, brow=0.8, furrow=-0.3,
               armL="relaxed" if u < 1 else "point", armR="relaxed", wind=0.8)
        return at_feet(CHIEF, c, t, 330, 1520, 0.56) + at_feet(MESSENGER, m, t, lerp(1180, 660, u), 1530, 0.56)
    B = Shot(7.4, cpd, midB, cam=camB, light=DUSKL, sun=SUN_DUSK, bloom=0.6)

    LC = L(124.6, "p2s6e")
    camC = cam_push(1.0, 1.06, 540, 860, 4.8)

    def midC(t):
        q = tp(LC, t, 35, turn=0.2, gx=0.4 - 0.9 * ease((t - 3.4) / 0.4), gy=0.0, sad=0.5, brow=0.9, furrow=-0.3, armL="relaxed", armR="relaxed",
               wind=0.6)
        return at_neck(CHIEF, q, t, 540, 960, 1.0)
    C = Shot(4.8, cpdb, midC, cam=camC, light=DUSKL, sun=SUN_DUSK)

    dn = bg("dunes_dusk", lambda: lbg.dunes("dusk"))
    camD = cam_push(1.04, 1.0, 480, 1100, 11.2)

    def midD(t):
        u = ease(t / 10.0)
        x = lerp(860, 380, u); y = lerp(1600, 1220, u); s = lerp(0.6, 0.26, u)
        q = P(legs="walk" if t < 10.2 else "stand", phase=t * 6.0, turn=-0.45, gx=-0.9, gy=-0.3, sad=0.5, brow=0.8, armL="relaxed",
              armR="forward" if t < 10.2 else "relaxed", wind=1.4, blink=blink_at(t, 36), breathe=math.sin(t * 3))
        sh = (f'<g transform="translate({x:.1f},{y:.1f}) scale({s:.4f})"><path d="M -60 0 L 760 160 L 820 90 L 40 -20 Z" fill="#3a1830" opacity="0.28"/></g>')
        return sh + at_feet(CHIEF, q, t, x, y, s)
    D = Shot(11.2, dn, midD, cam=camD, light=DUSKL, sun=SUN_DUSK, bloom=0.7, fade_out=0.6,
             fx=[SandWind(200, 601, (0, 1000, W, 1900), (600, 1000), strength=lambda t: 0.6)])
    return [A1, A2, B, C, D]


SCENES = {"s1": s1, "s2": s2, "s3": s3, "s4": s4, "s5": s5, "s6": s6}
