"""Part 6 · The Cow Barmayeh — 2D cartoon. Timing matches zahhak/p06_audio.py
(scene starts s1 0, s2 8.0, s3 12.6, s4 41.0, s5 59.4, s6 86.8; end card 114.4; total 119.4)."""
import math, random
from PIL import Image, ImageFilter, ImageDraw
from film import Shot, W, H, ease, lerp, talk_pose, blink_at, cam_push, cam_static, Motes, Embers, svg_render
from chars import pose, horse, cow, Ctx, FEET, fmt, prop
from stage import at_neck, at_feet, rider, Glow, lw_for, fire_svg
import bgs, zbg
from cast import *
from p01_scenes import P, bg, cam_xy, tp, darken, fade_to, torch_flame, hall_fx, placed, flipped, TORCH, HALL, NIGHT
from p03_scenes import night_of, svg_fx, torches_wide, torches_close
from p05_scenes import hand_at, shake

DAWNL = dict(rim=(-5, -2), rim_col=(1.0, 0.85, 0.7), ramp=(0, W, 1.06, 0.92), ambient=(1.0, 0.96, 0.95))
DUSKL = dict(rim=(5, -2), rim_col=(1.0, 0.72, 0.45), rim_str=0.9, ramp=(0, W, 0.86, 1.06), ambient=(0.92, 0.84, 0.86))
DAYL = dict(rim=(5, -2), rim_col=(1.0, 0.9, 0.7), ambient=(1.0, 0.98, 0.95))
NIGHTL = dict(NIGHT, rim=(5, -2), rim_col=(1.0, 0.75, 0.45), rim_str=0.6)
CAVEL = dict(rim=(5, -2), rim_col=(1.0, 0.7, 0.4), rim_str=0.9, ramp=(0, W, 0.92, 1.06), ambient=(0.96, 0.92, 0.94))
SUN_DAWN = (200, 880, 900, (0.12, 0.08, 0.05))
SUN_DUSK = (880, 900, 900, (0.14, 0.07, 0.04))


def mead(pal, blur=0, broken=False, tall=False):
    name = f"meadow_{pal}" + ("_broken" if broken else "") + ("_tall" if tall else "")
    return bg(name, lambda: zbg.meadow(pal, broken, tall), blur)


def barmayeh(t, x, y, s, graze=0.0, flip=False, seed=0):
    c = Ctx(lw_for(s))
    svg = cow(c, t=t, graze=graze, seed=seed, peacock=True)
    return flipped(svg, x, y, s) if flip else placed(svg, x, y, s)


def sparkles(t, x, y, w, h, n=12, seed=0):
    """little stars twinkling over the cow"""
    r = random.Random(seed)
    o = ""
    for k in range(n):
        px, py, ph = x + r.uniform(-w / 2, w / 2), y + r.uniform(-h / 2, h / 2), r.uniform(0, 6.3)
        a = max(0.0, math.sin(t * 2.2 + ph))
        if a > 0.05:
            rr = 10 * a
            o += (f'<path d="M {px:.1f} {py - rr:.1f} L {px + rr * 0.2:.1f} {py - rr * 0.2:.1f} L {px + rr:.1f} {py:.1f} L {px + rr * 0.2:.1f} {py + rr * 0.2:.1f} '
                  f'L {px:.1f} {py + rr:.1f} L {px - rr * 0.2:.1f} {py + rr * 0.2:.1f} L {px - rr:.1f} {py:.1f} L {px - rr * 0.2:.1f} {py - rr * 0.2:.1f} Z" '
                  f'fill="#fff8d8" opacity="{0.9 * a:.2f}"/>')
    return o


def mist(a=0.4, seed=61):
    r = random.Random(seed)
    img = bgs.cached(f"zh_meadow_mist_{seed}", lambda: svg_render("".join(
        f'<ellipse cx="{r.uniform(-200, 2000):.0f}" cy="{r.uniform(1100, 1800):.0f}" rx="{r.uniform(260, 500):.0f}" ry="{r.uniform(30, 70):.0f}" '
        f'fill="#ffffff" opacity="0.35"/>' for _ in range(22)), 2200, H).filter(ImageFilter.GaussianBlur(26)))

    def fx(im, t):
        x = int(200 + 22 * t)
        m = img.crop((x, 0, x + W, H))
        m.putalpha(m.getchannel("A").point(lambda v: int(v * a)))
        im.alpha_composite(m)
    return fx


def keeper_q(lines, t, seed, **kw):
    base = dict(turn=-0.3, gx=-0.6, gy=0.0, brow=0.3, furrow=0.2, armR=("ik", -100, 200, "down"), propR="stick", armL="relaxed", wind=0.4)
    base.update(kw)
    return tp(lines, t, seed, **base)


# ================================================================ S1 the hook (0-8.0)
def s1():
    md = mead("dawn")
    camA = cam_push(1.0, 1.06, 600, 1000, 4.8)

    def midA(t):
        return barmayeh(t, 600, 1112, 0.8, graze=0.5 + 0.5 * math.sin(t * 0.7)) + sparkles(t, 600, 900, 420, 220, 14, 1)
    A = Shot(4.8, md, midA, cam=camA, light=DAWNL, sun=SUN_DAWN, fx=[mist(0.5), Glow(lambda t: cam_xy(camA, t, 600, 950), 360, (255, 230, 180), 0.3),
                                                                  Motes(40, 601, (255, 240, 210), (0, 900, W, 1700), (6, -10), amax=110)],
             bloom=0.8, fade_in=0.5)

    dnb = bg("damavand_night", lambda: zbg.damavand("night"), 8)
    LB = [("p6s1b", 0.1)]

    def midB(t):
        f = tp(LB, t, 1, turn=0.35, gx=0.8, gy=-0.1, sad=0.8, brow=0.9, furrow=-0.5, armL="hold_baby", armR="hold_baby", propL="baby", wind=1.0,
               tilt=3 * math.sin(t * 6), nod=4 * math.sin(t * 9))
        return at_neck(FARANAK, f, t, 520 + 10 * math.sin(t * 9), 1010, 1.05)
    B = Shot(3.2, dnb, midB, cam=cam_push(1.0, 1.05, 520, 860, 3.2), light=dict(NIGHT, rim=(-5, -2), rim_col=(0.8, 0.86, 1.0), rim_str=0.7),
             fx=[Motes(30, 602, (220, 230, 255), (0, 200, W, 1500), (-160, 10), amax=80)], grade="night", fade_out=0.4)
    return [A, B]


# ================================================================ S2 title (8.0-12.6)
def s2():
    md = mead("dawn")
    cam = cam_push(1.0, 1.07, 640, 1200, 4.6)

    def mid(t):
        return barmayeh(t, 700, 1112, 0.42, graze=0.6 + 0.4 * math.sin(t * 0.8)) + sparkles(t, 700, 1000, 240, 120, 8, 2)
    return [Shot(4.6, md, mid, cam=cam, light=DAWNL, sun=SUN_DAWN, fx=[mist(0.45, 62), Motes(40, 603, (255, 240, 210), (0, 900, W, 1700), (6, -10), amax=90)],
                 bloom=0.7, fade_in=0.4, fade_out=0.5)]


# ================================================================ S3 the meadow (12.6-41.0)
def s3():
    dn = bg("damavand_night", lambda: zbg.damavand("night"))
    camA = cam_push(1.0, 1.05, 540, 1300, 4.8)

    def midA(t):
        x = lerp(-80, 1150, t / 4.8)
        f = P(legs="walk", phase=t * 7.0, turn=0.45, gx=0.9, gy=-0.1, sad=0.7, brow=0.8, furrow=-0.4, armL="hold_baby", armR="hold_baby", propL="baby",
              wind=1.0, blink=blink_at(t, 3))
        return at_feet(FARANAK, f, t, x, 1520, 0.4)
    A = Shot(4.8, dn, midA, cam=camA, light=dict(NIGHT, rim=(-5, -3), rim_col=(0.8, 0.86, 1.0), rim_str=0.7), grade="night", fade_in=0.4,
             fx=[Motes(40, 604, (220, 230, 255), (0, 300, W, 1500), (-30, 4), amax=70)])

    md = mead("dusk")
    camB = cam_push(1.0, 1.05, 560, 1300, 4.8)

    def midB(t):
        u = ease(t / 3.2)
        f = P(legs="walk" if u < 1 else "stand", phase=t * 5.6, turn=0.2, gx=0.6, gy=0.0, sad=0.6, brow=0.7, furrow=-0.3,
              armL="hold_baby", armR="hold_baby", propL="baby", wind=0.6, blink=blink_at(t, 4))
        turn_ = ease((t - 1.6) / 0.6)
        k = keeper_q([], t, 5, turn=lerp(0.3, -0.4, turn_), gx=lerp(0.6, -0.8, turn_), brow=0.3 + 0.4 * turn_)
        return (barmayeh(t, 300, 1112, 0.45, graze=0.6 + 0.4 * math.sin(t * 0.8)) + at_feet(KEEPER, k, t, 860, 1380, 0.4) +
                at_feet(FARANAK, f, t, lerp(540, 600, u), lerp(1290, 1440, u), lerp(0.3, 0.4, u)))
    B = Shot(4.8, md, midB, cam=camB, light=DUSKL, sun=SUN_DUSK, fx=[Motes(30, 605, (255, 220, 170), (0, 800, W, 1600), (4, -8), amax=80)])

    mdb = mead("dusk", 6)
    camC = cam_push(1.0, 1.08, 600, 950, 5.0)

    def midC(t):
        return barmayeh(t, 620, 1290, 1.45, graze=0.3 + 0.3 * math.sin(t * 0.9)) + sparkles(t, 620, 870, 640, 320, 16, 3)
    C = Shot(5.0, mdb, midC, cam=camC, light=DUSKL, sun=SUN_DUSK, bloom=0.8,
             fx=[Glow(lambda t: cam_xy(camC, t, 600, 940), 420, (255, 220, 160), 0.25), Motes(40, 606, (255, 230, 180), (100, 700, 1000, 1500), (4, -12), amax=110)])

    LD = [("p6s3d", 0.2), ("p6s3e", 2.5)]

    def midD(t):
        f = tp(LD, t, 6, turn=0.3, gx=0.7, gy=0.05, sad=0.85, brow=1.0, furrow=-0.6, armL="hold_baby", armR="hold_baby", propL="baby", wind=0.4)
        return at_neck(FARANAK, f, t, 500, 1000, 1.1)
    camD = cam_push(1.0, 1.05, 500, 860, 6.2)
    D = Shot(6.2, mdb, midD, cam=camD, light=DUSKL, sun=SUN_DUSK)

    LE = [("p6s3f", 0.2)]

    def midE(t):
        k = keeper_q(LE, t, 7, turn=-0.3, gx=-0.7, gy=0.0, brow=0.4, furrow=0.3, smile=0.25 * ease((t - 1.5) / 0.5), nod=6 * ease((t - 0.4) / 0.4))
        return at_neck(KEEPER, k, t, 580, 1050, 1.25)
    E = Shot(3.4, mdb, midE, cam=cam_push(1.0, 1.04, 580, 860, 3.4), light=DUSKL, sun=SUN_DUSK)

    LF = [("p6s3g", 0.3)]
    camF = cam_push(1.05, 1.12, 560, 1250, 4.2)

    def midF(t):
        k = P(turn=-0.3, gx=-0.6, gy=0.5, brow=0.4, smile=0.4, armL="hold_baby", armR="hold_baby", propL="baby", wind=0.3, blink=blink_at(t, 8))
        f = tp(LF, t, 9, turn=0.35, gx=0.8, gy=0.3, sad=0.8, brow=0.8, furrow=-0.5, armL="relaxed", armR=("ik", 230, 180), wind=0.3)
        return (barmayeh(t, 860, 1112, 0.4, graze=0.5, flip=True) + at_feet(KEEPER, k, t, 640, 1640, 0.5) + at_feet(FARANAK, f, t, 400, 1650, 0.5))
    F = Shot(4.2, md, midF, cam=camF, light=DUSKL, sun=SUN_DUSK, fx=[Motes(30, 607, (255, 220, 170), (0, 800, W, 1600), (4, -8), amax=80)], fade_out=0.5)
    return [A, B, C, D, E, F]


# ================================================================ S4 three years; the spy; Zahhak (41.0-59.4)
def s4():
    mday = mead("day")
    mdayt = mead("day", tall=True)
    camA = cam_push(1.0, 1.06, 560, 1300, 7.0, py0=-420, py1=-420)
    LA = [("p6s4e", 4.0)]

    def midA1(t):
        o = ""
        k = keeper_q(LA, t, 10, legs="sit", turn=0.35, gx=0.7, gy=0.3, smile=0.5, brow=0.3, furrow=-0.2, armR="relaxed", propR=None)
        o += at_neck(KEEPER, k, t, 230, 1420 - 575 * 0.4, 0.4)
        o += barmayeh(t, 730, 1500, 0.6, graze=0.4 + 0.4 * math.sin(t * 0.7))
        u = ease(t / 3.0)
        pat = math.sin(t * 5) if t > 3.2 else 0.0
        b = P(legs="walk" if u < 1 else "stand", phase=t * 6.0, turn=0.4, gx=0.8, gy=-0.3, smile=0.8, brow=0.4,
              armL=("ik", 170, 40 + 25 * pat) if t > 3.2 else "relaxed", armR="relaxed", blink=blink_at(t, 11), wind=0.3)
        o += at_feet(FEREYDUN_CHILD, b, t, lerp(340, 505, u), 1540, 0.44)
        return o
    A1 = Shot(7.0, mdayt, midA1, cam=camA, bg_par=1.0, light=DAYL, fx=[Motes(30, 608, (255, 250, 220), (0, 800, W, 1600), (8, -6), amax=70)], fade_in=0.5)

    camA2 = cam_push(1.7, 1.78, 160, 1180, 3.0)

    def midA2(t):
        peek = ease((t - 0.3) / 0.6)
        q = tp([], t, 12, turn=0.35, gx=0.9, gy=0.0, furrow=0.6, brow=-0.2, smile=0.3, armL="relaxed", armR=("ik", -120, -40), wind=0.2)
        clip = ('<clipPath id="behindtrunk"><path d="M 172 760 L 1080 760 L 1080 1420 L 206 1420 L 198 1250 C 182 1100, 194 980, 170 860 Z"/></clipPath>')
        return clip + '<g clip-path="url(#behindtrunk)">' + at_feet(SPY, q, t, lerp(130, 196, peek), 1296, 0.27) + '</g>'
    A2 = Shot(3.0, mday, midA2, cam=camA2, bg_par=1.0, light=DAYL)

    hallb = bg("hall", zbg.hall, 6)
    LB = [("p6s4c", 0.2)]

    def midB(t):
        q = tp(LB, t, 13, turn=0.25, gx=0.6, gy=-0.4, furrow=0.5, brow=0.2, smile=0.35, nod=8, armL="chest", armR="offer" if t > 1.4 else "relaxed")
        return at_neck(SPY, q, t, 540, 1060, 1.2)
    B = Shot(4.0, hallb, midB, cam=cam_push(1.0, 1.04, 540, 860, 4.0), light=dict(HALL, point=None, rim=(-5, -2), rim_col=(1.0, 0.65, 0.35), rim_str=0.8),
             grade="fire", bloom=0.5)

    close = bg("hall_close", zbg.hall_close)
    LC = [("p6s4d", 0.2)]
    camC = shake(cam_push(1.0, 1.06, 540, 860, 4.4), 1.6, 2.4, 8)

    def midC(t):
        q = tp(LC, t, 14, turn=0.05, gx=0.1, gy=0.1, furrow=0.2 if t < 1.4 else 1.0, brow=0.9 if t < 1.4 else -0.4,
               armL="relaxed", armR="point" if t > 2.0 else "relaxed", snake_looks=(1.0, 1.0),
               hisses=(0.8 * (0.6 + 0.4 * math.sin(t * 5)) if t > 1.4 else 0.2, 0.8 * (0.6 + 0.4 * math.sin(t * 4 + 1)) if t > 1.4 else 0.2))
        return torches_close(t) + at_neck(ZAHHAK_KING, q, t, 540, 1030, 1.0)
    C = Shot(4.4, close, midC, cam=camC, light=TORCH, fx=hall_fx(camC, [(40, 740), (1040, 740)], 609), grade="fire", bloom=0.6, fade_out=0.4)
    return [A1, A2, B, C]


# ================================================================ S5 the warning; Alborz; the holy man (59.4-86.8)
def s5():
    mn = mead("night", tall=True)
    camA = cam_push(1.0, 1.05, 560, 1300, 4.4, py0=-250, py1=-250)
    lanA = lambda t: cam_xy(camA, t, *hand_at(FARANAK, "hold_lantern", 1, lerp(560, 600, ease(t / 3.0)), lerp(1290, 1440, ease(t / 3.0)),
                                                lerp(0.3, 0.4, ease(t / 3.0))))

    def midA(t):
        u = ease(t / 3.0)
        f = P(legs="walk" if u < 1 else "stand", phase=t * 6.0, turn=0.2, gx=0.6, gy=0.0, sad=0.5, brow=0.9, furrow=-0.4, armL="hold_lantern",
              propL="lantern", armR="relaxed", wind=0.6, blink=blink_at(t, 15))
        k = keeper_q([], t, 16, turn=-0.4, gx=-0.8, brow=0.7, furrow=-0.2, armR="relaxed", propR=None, armL=("ik", 100, 300, "down"))
        b = P(turn=-0.3, gx=-0.7, gy=-0.3, brow=0.5, armR=("ik", -100, 260, "down"), armL="relaxed", blink=blink_at(t, 17), wind=0.3)
        return (at_feet(KEEPER, k, t, 860, 1380, 0.4) + at_feet(FEREYDUN_CHILD, b, t, 800, 1390, 0.36) +
                at_feet(FARANAK, f, t, lerp(560, 600, u), lerp(1290, 1440, u), lerp(0.3, 0.4, u)))
    A = Shot(4.4, mn, midA, cam=camA, bg_par=1.0, light=NIGHTL, fx=[Glow(lanA, 160, (255, 190, 110), 0.5)], grade="night", fade_in=0.4)

    mnb = mead("night", 8)
    LB = [("p6s5b", 0.2)]
    camB = cam_push(1.0, 1.05, 520, 860, 3.6)

    def midB(t):
        f = tp(LB, t, 18, turn=0.3, gx=0.7, gy=0.0, sad=0.6, brow=0.9, furrow=-0.3, armL="hold_lantern", propL="lantern", armR="chest", wind=0.5)
        return at_neck(FARANAK, f, t, 520, 1010, 1.05)
    B = Shot(3.6, mnb, midB, cam=camB, light=dict(NIGHTL, rim_str=0.8, ambient=(0.78, 0.76, 0.9)),
             fx=[Glow(lambda t: cam_xy(camB, t, 520 + 1.05 * 160, 1010 + 1.05 * 560), 260, (255, 190, 110), 0.5)], grade="night")

    LC = [("p6s5c", 0.2)]

    def midC(t):
        k = keeper_q(LC, t, 19, turn=-0.3, gx=-0.7, brow=0.6, furrow=0.4, armR="relaxed", propR=None, armL="point" if t > 0.8 else "relaxed")
        return at_neck(KEEPER, k, t, 580, 1050, 1.25)
    C = Shot(2.6, mnb, midC, cam=cam_push(1.0, 1.04, 580, 860, 2.6), light=dict(NIGHTL, rim=(-5, -2), rim_str=0.8, ambient=(0.78, 0.76, 0.9)),
             grade="night", fade_out=0.3)

    al = bg("alborz_dawn", lambda: zbg.alborz("dawn"))
    camD = cam_push(1.0, 1.05, 400, 1400, 6.0)

    def path_pt(u):
        return lerp(120, 470, u), lerp(1640, 1380, u)

    def midD(t):
        u = 0.15 + 0.7 * t / 6.0
        x, y = path_pt(u)
        s = lerp(0.46, 0.38, u)
        f = P(legs="walk", phase=t * 4.4, turn=0.4, gx=0.8, gy=0.2, sad=0.3, brow=0.5, furrow=0.2, armL=("ik", 150, 330, "down"), armR="relaxed",
              wind=0.7, blink=blink_at(t, 20))
        bx, by = path_pt(u + 0.07)
        b = P(legs="walk", phase=t * 6.0 + 1, turn=0.4, gx=0.8, gy=-0.2, brow=0.3, armR=("ik", -120, 120), armL="relaxed", wind=0.5, blink=blink_at(t, 21))
        return at_feet(FARANAK, f, t, x, y, s) + at_feet(FEREYDUN_CHILD, b, t, bx + 20, by + 14, s * 0.95)
    D = Shot(6.0, al, midD, cam=camD, light=CAVEL, sun=SUN_DAWN, fx=[Motes(30, 610, (255, 240, 220), (0, 700, W, 1500), (10, -4), amax=70)], fade_in=0.4)

    LE = [("p6s5e", 0.3)]
    camE = cam_push(1.0, 1.06, 620, 1250, 4.6)

    def midE(t):
        h = tp([], t, 22, turn=-0.35, gx=-0.8, gy=0.1, brow=0.4, smile=0.25, armL="relaxed", armR="relaxed", wind=0.3)
        f = tp(LE, t, 23, turn=0.35, gx=0.8, gy=0.0, sad=0.3, brow=0.6, furrow=-0.2, armL="relaxed", armR=("ik", -80, 300, "down"), wind=0.4)
        b = P(turn=0.35, gx=0.8, gy=-0.4, brow=0.6, smile=0.2, armL="relaxed", armR="relaxed", blink=blink_at(t, 24), wind=0.3)
        return (at_feet(HERMIT, h, t, 790, 1295, 0.42) + at_feet(FEREYDUN_CHILD, b, t, 590, 1338, 0.4) + at_feet(FARANAK, f, t, 470, 1340, 0.42))
    E = Shot(4.6, al, midE, cam=camE, light=CAVEL, sun=SUN_DAWN, fx=[Glow(lambda t: cam_xy(camE, t, 780, 1150), 260, (255, 170, 90), 0.35)])

    alb = bg("alborz_dawn", lambda: zbg.alborz("dawn"), 8)
    LF = [("p6s5f", 0.2)]

    def midF(t):
        f = tp(LF, t, 25, turn=0.3, gx=0.7, gy=0.0, sad=0.75, brow=1.0, furrow=-0.5, armL="relaxed", armR="chest", wind=0.5)
        return at_neck(FARANAK, f, t, 500, 1010, 1.05)
    F = Shot(2.2, alb, midF, cam=cam_push(1.0, 1.04, 500, 860, 2.2), light=dict(CAVEL, ramp=None), sun=SUN_DAWN)

    LG = [("p6s5g", 0.2)]
    camG = cam_push(1.0, 1.05, 540, 1100, 4.0)

    def midG(t):
        reach = ease((t - 1.8) / 0.6)
        hx, hy = 540 + lerp(-40, -150, reach), 1000
        h = tp(LG, t, 26, turn=-0.25, gx=-0.4, gy=0.4 + 0.2 * reach, brow=0.4, smile=0.35, furrow=-0.2,
               armR=("ik", lerp(-150, -330, reach), lerp(260, -40, reach), "down"), armL="relaxed", wind=0.3)
        b = P(turn=0.3, gx=0.5, gy=-0.6, brow=0.6, smile=0.4 * reach, armL="relaxed", armR="relaxed", blink=blink_at(t, 27), wind=0.2)
        return at_neck(HERMIT, h, t, 640, 900, 0.9) + at_feet(FEREYDUN_CHILD, b, t, 335, 1570, 0.78)
    G = Shot(4.0, alb, midG, cam=camG, light=dict(CAVEL, ramp=None), sun=SUN_DAWN, fx=[Glow(lambda t: cam_xy(camG, t, 900, 1100), 320, (255, 170, 90), 0.3)],
             fade_out=0.4)
    return [A, B, C, D, E, F, G]


# ================================================================ S6 the storm; sixteen years later (86.8-119.4)
def s6():
    mday = mead("day", tall=True)
    dust = bgs.cached("zh_dust_tex", lambda: svg_render("".join(
        f'<ellipse cx="{random.Random(i).uniform(-200, 2000):.0f}" cy="{random.Random(i + 50).uniform(1200, 1800):.0f}" rx="{random.Random(i + 9).uniform(160, 380):.0f}" '
        f'ry="{random.Random(i + 3).uniform(40, 110):.0f}" fill="#b89a6a" opacity="0.55"/>' for i in range(30)), 2200, H).filter(ImageFilter.GaussianBlur(26)))
    camA = shake(cam_push(1.0, 1.05, 540, 1300, 4.2, py0=-260, py1=-260), 0.0, 4.2, 6)

    def midA(t):
        o = ""
        riders = [(ZAHHAK_KING, 0, 1500, 0.66, "#141016"), (ZGUARD, 330, 1440, 0.54, "#3a2a1e"), (ZGUARD, 520, 1560, 0.6, "#5a3a22"), (ZGUARD, 780, 1460, 0.52, "#2a2a2e")]
        for k, (S, dx, y, s, col) in enumerate(riders):
            x = 1300 + dx - 470 * t
            q = P(turn=-0.4, gx=-0.9, armL="forward", armR=(20, 10) if S is ZGUARD else "forward", propR="spear" if S is ZGUARD else None, furrow=1.0,
                  brow=-0.4, wind=1.0, blink=0.0, snake_looks=(1.0, 1.0), hisses=(0.8, 0.8))
            o += rider(S, q, t, lambda c, col=col, k=k: horse(c, col=col, walk=True, phase=t * 9 + k, t=t + k, head_bob=-20 * abs(math.sin(t * 9 + k))),
                       x, y, s, flip=True)
        return o

    def dustfx(im, t):
        x = int(min(1100, 400 + 300 * t))
        d = dust.crop((x, 0, x + W, H)).transform((W, H), Image.AFFINE, (1, 0, 0, 0, 1, 260))
        d.putalpha(d.getchannel("A").point(lambda v: int(v * min(0.75, 0.2 + t / 2.4))))
        im.alpha_composite(d)
    A = Shot(4.2, mday, midA, cam=camA, bg_par=1.0, light=DAYL, fx=[dustfx], fade_in=0.2)

    mb = mead("day", broken=True, tall=True)
    camB = cam_push(1.0, 1.12, 560, 1500, 5.6, py0=-260, py1=-260)
    mbg = Image.alpha_composite(mb, Image.new("RGBA", mb.size, (120, 110, 100, 70)))

    def midB(t):
        c = Ctx(1.0)
        o = f'<g transform="translate(300,1262) rotate(-18) scale(0.55)">{prop(c, "stick", 0, -200, 0, t)}</g>'
        for k in range(9):
            a = -0.4 + k * 0.42
            o += (f'<circle cx="{410 + 34 * math.cos(a):.0f}" cy="{1150 + 40 * math.sin(a):.0f}" r="9" fill="{["#f05a7a", "#f6d04a", "#ffffff"][k % 3]}" '
                  f'stroke="#1b0f0a" stroke-width="2"/>')
        return o

    def settle(im, t):
        d = dust.crop((600, 0, 600 + W, H))
        d.putalpha(d.getchannel("A").point(lambda v: int(v * max(0.0, 0.7 - t / 6.0))))
        im.alpha_composite(d)
    B = Shot(5.6, mbg, midB, cam=camB, bg_par=1.0, light=dict(DAYL, ambient=(0.86, 0.84, 0.82)), fx=[settle, Motes(40, 611, (210, 190, 160), (0, 900, W, 1800), (-6, 8), amax=90)],
             grade="warm", fade_out=0.3)

    door_night = bgs.cached("zh_house_door_night", night_of(lambda: bgs.cached("house_door", bgs.house_door), (6, 10, 30), 170))
    camBb = cam_push(1.0, 1.06, 450, 1000, 4.0)

    def midBb(t):
        o = '<rect x="320" y="660" width="260" height="740" fill="#ff8a2a" opacity="0.55"/>'
        for k, (x, y, sz) in enumerate(((450, 1400, 130), (200, 400, 150), (520, 380, 170), (700, 420, 130), (450, 820, 90))):
            o += fire_svg(x, y, sz, t + k * 0.7, k)
        return o

    def smoke(im, t):
        layer = Image.new("RGBA", (W, H))
        d = ImageDraw.Draw(layer, "RGBA")
        for k in range(14):
            age = (t * 0.6 + k * 0.17) % 1.0
            x = 200 + 50 * k + 40 * math.sin(age * 4 + k); y = 380 - age * 420; r_ = 50 + age * 130
            d.ellipse((x - r_, y - r_, x + r_, y + r_), fill=(60, 50, 56, int(90 * (1 - age))))
        im.alpha_composite(layer.filter(ImageFilter.GaussianBlur(18)))
    Bb = Shot(4.0, door_night, midBb, cam=camBb, light=dict(rim=(0, 0)), fx=[smoke, Embers(60, 612, (100, 300, 800, 1400), (120, 260)),
                                                                            Glow(lambda t: cam_xy(camBb, t, 450, 800), 520, (255, 140, 60), 0.45)],
              grade="fire", bloom=0.8, fade_in=0.3, fade_out=0.6)

    ad = bg("alborz_day", lambda: zbg.alborz("day"))
    camC = cam_push(1.0, 1.08, 560, 1350, 6.4)

    def midC(t):
        u = ease(t / 6.0)
        x = lerp(780, 380, u); y = lerp(1300, 1660, u); s = lerp(0.36, 0.56, u)
        q = P(legs="walk" if t < 6.0 else "stand", phase=t * 4.2, turn=-0.25, gx=-0.4, gy=0.0, brow=0.3, furrow=0.3, armL="relaxed", armR="relaxed",
              wind=0.8, blink=blink_at(t, 30))
        return at_feet(FEREYDUN, q, t, x, y, s)
    C = Shot(6.4, ad, midC, cam=camC, light=dict(DAYL, ramp=(0, W, 0.94, 1.04)), fx=[Motes(30, 613, (255, 250, 230), (0, 700, W, 1500), (10, -4), amax=60)],
             fade_in=0.6)

    mdb = mead("dawn", 8)
    LD = [("p6s6d", 0.2), ("p6s6e", 2.3)]

    def midD(t):
        q = tp(LD, t, 31, turn=0.25, gx=0.6, gy=0.0, brow=0.6 if t > 2.0 else 0.3, furrow=0.3, sad=0.3, armL="relaxed", armR="relaxed", wind=0.5)
        return at_neck(FEREYDUN, q, t, 520, 1020, 1.1)
    D = Shot(4.4, mdb, midD, cam=cam_push(1.0, 1.05, 520, 860, 4.4), light=dict(DAWNL, ramp=None), sun=SUN_DAWN)

    def midE(t):
        f = tp([], t, 32, turn=-0.3, gx=-0.7, gy=0.0, sad=0.6 + 0.3 * ease((t - 0.8) / 0.8), brow=1.0, furrow=-0.6, armL="chest", armR="relaxed", wind=0.4)
        f["blink"] = min(f["blink"], 0.2)
        return at_neck(FARANAK, f, t, 560, 1010, 1.05)
    E = Shot(3.0, mdb, midE, cam=cam_push(1.0, 1.06, 560, 860, 3.0), light=dict(DAWNL, ramp=None), sun=SUN_DAWN)

    md = mead("dawn")
    camI = cam_push(1.04, 1.1, 560, 1350, 5.0)

    def midI(t):
        q = P(turn=0.3, gx=0.7, gy=0.0, brow=0.6, furrow=0.3, sad=0.3, armL="relaxed", armR="relaxed", wind=0.5, blink=blink_at(t, 33))
        f = P(turn=-0.3, gx=-0.7, gy=-0.2, sad=0.8, brow=1.0, furrow=-0.5, armL="chest", armR="relaxed", wind=0.4, blink=blink_at(t, 34))
        return at_feet(FEREYDUN, q, t, 430, 1640, 0.5) + at_feet(FARANAK, f, t, 690, 1640, 0.47)
    I = Shot(5.0, md, midI, cam=camI, light=DAWNL, sun=SUN_DAWN, fx=[mist(0.35, 63)], fade_out=0.8)
    return [A, B, Bb, C, D, E, I]


SCENES = {"s1": s1, "s2": s2, "s3": s3, "s4": s4, "s5": s5, "s6": s6}
