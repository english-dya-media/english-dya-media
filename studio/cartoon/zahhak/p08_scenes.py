"""Part 8 · The Blacksmith's Banner — 2D cartoon. Timing matches zahhak/p08_audio.py
(scene starts s1 0, s2 8.6, s3 13.2, s4 51.2, s5 84.8, s6 97.0, s7 135.2; end card 154.4; total 159.4)."""
import math, random
from PIL import Image, ImageFilter, ImageDraw
from film import Shot, W, H, ease, lerp, talk_pose, blink_at, cam_push, cam_static, Motes, Embers, svg_render
from chars import pose, horse, Ctx, FEET, fmt, prop, SKINS, OUT, kaviani, kav_point, KAV_JEWELS
from stage import at_neck, at_feet, lying_at, rider, Glow, lw_for, fire_svg, back_heads, random_spec
import bgs, zbg
from zbg import CAMP_FLANK, CAMP_TENT, CAMP_FIRE
from cast import *
from p01_scenes import P, bg, cam_xy, tp, darken, fade_to, placed, flipped
from p03_scenes import svg_fx, cam_svg
from p04_scenes import tear
from p05_scenes import hand_at, shake, silhouette, mace_at, flash, dream_fx, warriors, gate_bg
from p06_scenes import mist, sparkles
from p07_scenes import anvil_svg, hammer_arm, market_crowd, Cheering, dust_tex, kaveh_q
import p08_audio as A8

DAYC = dict(rim=(5, -2), rim_col=(1.0, 0.9, 0.72), ramp=(0, W, 0.94, 1.04), ambient=(1.0, 0.97, 0.94))
SUN_DAYC = (900, 420, 900, (0.08, 0.07, 0.04))
DAWNC = dict(rim=(-5, -2), rim_col=(1.0, 0.82, 0.66), ramp=(0, W, 1.06, 0.9), ambient=(1.0, 0.95, 0.94))
SUN_DAWNC = (200, 860, 900, (0.12, 0.08, 0.05))
MOONC = dict(ambient=(0.6, 0.66, 0.92), rim=(-5, -3), rim_col=(0.75, 0.84, 1.0), rim_str=0.7)
FIREC = dict(ambient=(0.62, 0.64, 0.88), point=(CAMP_FIRE[0], CAMP_FIRE[1] - 60, 760, 0.55, 1.15, (1.0, 0.55, 0.25)),
             rim_point=(CAMP_FIRE[0], 6), rim_col=(1.0, 0.65, 0.32), rim_str=0.85)
DOORC = dict(ambient=(0.66, 0.68, 0.92), rim=(-5, -2), rim_col=(1.0, 0.7, 0.4), rim_str=0.85, ramp=(0, W, 1.06, 0.84))
GOLDL = (255, 226, 160)


def camp_bg(pal, blur=0):
    return bg(f"camp_{pal}", lambda: zbg.camp(pal), blur)


# ---------------------------------------------------------------- the rock on the hill
ROCK_R = 84
ROCK_COL = ("#77778a", "#3e3e4c", "#c0c6e0")
U_STOP = 0.84            # where the spell holds it, on the lower slope above the tent


def _rock_path(r=ROCK_R):
    pts = []
    n = len(CAMP_FLANK)
    for i, (x, y) in enumerate(CAMP_FLANK):
        segs = []
        if i > 0:
            segs.append((CAMP_FLANK[i - 1], (x, y)))
        if i < n - 1:
            segs.append(((x, y), CAMP_FLANK[i + 1]))
        nx = ny = 0.0
        for (x0, y0), (x1, y1) in segs:
            L = math.hypot(x1 - x0, y1 - y0)
            nx += -(y1 - y0) / L; ny += (x1 - x0) / L
        L = math.hypot(nx, ny)
        pts.append((x + nx / L * r * 0.86, y + ny / L * r * 0.86))
    return [(990, 600 - r * 0.86), (930, 606 - r * 0.86)] + pts       # it rests on the summit first, then goes over the edge


ROCK_PATH = _rock_path()
ROCK_LEN = [0.0]
for (_xa, _ya), (_xb, _yb) in zip(ROCK_PATH, ROCK_PATH[1:]):
    ROCK_LEN.append(ROCK_LEN[-1] + math.hypot(_xb - _xa, _yb - _ya))


def rock_at(u):
    """centre of the rock and the distance rolled, u 0 (top) .. 1 (bottom of the flank)"""
    s_ = max(0.0, min(1.0, u)) * ROCK_LEN[-1]
    for i in range(len(ROCK_PATH) - 1):
        if s_ <= ROCK_LEN[i + 1] or i == len(ROCK_PATH) - 2:
            f = (s_ - ROCK_LEN[i]) / max(1e-6, ROCK_LEN[i + 1] - ROCK_LEN[i])
            (xa, ya), (xb, yb) = ROCK_PATH[i], ROCK_PATH[i + 1]
            return lerp(xa, xb, f), lerp(ya, yb, f), s_
    return ROCK_PATH[-1][0], ROCK_PATH[-1][1], ROCK_LEN[-1]


def roll_u(tt, dur):
    """how far the rock has rolled tt s after it broke loose (it stops at U_STOP after dur s)"""
    if tt <= 0:
        return 0.0
    return U_STOP * min(1.0, tt / dur) ** 1.6


def rock_svg(u, wobble=0.0, r=ROCK_R):
    x, y, dist = rock_at(u)
    rot = -math.degrees(dist / r) + wobble
    return bgs.boulder(x, y, r, 851, col=ROCK_COL[0], dark=ROCK_COL[1], lit=ROCK_COL[2], rot=rot)


class Dust:
    """puffs of dust left behind the rolling rock (spawned along the path while it rolls), and a cloud where it stops"""
    def __init__(self, t_roll, dur, seed=0, stop_cloud=True):
        r = random.Random(seed)
        self.t_roll, self.dur = t_roll, dur
        self.p = [(r.uniform(0, 1), r.uniform(-1, 1), r.uniform(0.6, 1.2), r.uniform(0, 6.3)) for _ in range(26)]
        self.stop = stop_cloud

    def svg(self, t):
        o = ""
        for k, (f, j, sz, ph) in enumerate(self.p):
            ts = self.t_roll + f * self.dur              # when this puff is left behind
            age = t - ts
            if age < 0 or age > 2.4:
                continue
            x, y, _ = rock_at(roll_u(ts - self.t_roll, self.dur))
            x += 30 * j + 18 * age; y += ROCK_R * 0.7 - 30 * age
            rr = (24 + 50 * age) * sz
            o += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{rr:.1f}" fill="#8a8494" opacity="{max(0.0, 0.42 * (1 - age / 2.4)):.2f}"/>'
        if self.stop:
            age = t - (self.t_roll + self.dur)
            if 0 < age < 3.5:
                x, y, _ = rock_at(U_STOP)
                for k in range(9):
                    a = k / 9 * math.pi + 0.2
                    rr = (30 + 60 * ease(age / 1.5)) * (0.8 + 0.3 * math.sin(k * 2.3))
                    cx = x + math.cos(a) * (60 + 80 * ease(age / 1.5)) * (1 if k % 2 else -1)
                    cy = y + ROCK_R * 0.6 - 30 * ease(age / 2.0) - 10 * k % 3
                    o += f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{rr:.1f}" fill="#8a8494" opacity="{max(0.0, 0.4 * (1 - age / 3.5)):.2f}"/>'
        return f'<g opacity="0.9">{o}</g>' if o else ""


def held_glow(t, t0, dur=1.6):
    """the spell: a ring of golden light round the rock where it stops"""
    u = (t - t0) / dur
    if not 0 < u < 1:
        return ""
    x, y, _ = rock_at(U_STOP)
    a = math.sin(math.pi * u)
    return (f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{ROCK_R * (1.2 + 0.8 * u):.1f}" fill="none" stroke="#ffe8a0" stroke-width="{10 * a:.1f}" opacity="{0.8 * a:.2f}"/>'
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{ROCK_R * 1.15:.1f}" fill="#ffe8a0" opacity="{0.18 * a:.2f}"/>')


def palm_ring(x, y, t, t0, dur=0.9, s=1.0):
    """the secret word: rings of light going out from an open palm"""
    o = ""
    for k in range(2):
        u = (t - t0 - 0.18 * k) / dur
        if 0 < u < 1:
            a = 1 - u
            o += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{(30 + 260 * u) * s:.1f}" fill="none" stroke="#ffe6a0" stroke-width="{(12 * a) * s:.1f}" opacity="{0.85 * a:.2f}"/>'
    return o


def fereydun_door(t, raise_=1.0, seed=0, x=CAMP_TENT[0] + 10, y=1330, s=0.27):
    """Fereydun small at his tent door at night, his left arm (picture right) out towards the hill"""
    q = P(turn=0.4, gx=0.8, gy=-0.6, furrow=1.0, armL=("ik", lerp(150, 330, raise_), lerp(300, -60, raise_)), openL=raise_ > 0.5, armR="relaxed",
          blink=blink_at(t, seed), wind=0.3)
    return at_feet(FEREYDUN, q, t, x, y, s)


def wide_rock(dur, t_roll, roll_dur, t_stop_glow=None, fereydun=None, fade_in=0.0, fade_out=0.0, cam=None, dust_seed=0):
    """the camp at night from the side: the rock rolls down the flank of the hill (t_roll: when it breaks loose, shot time)"""
    night = camp_bg("night")
    cam = cam or cam_push(1.0, 1.05, 720, 1000, dur)
    dust = Dust(t_roll, roll_dur, dust_seed)

    def mid(t):
        tt = t - t_roll
        wob = 5 * math.sin(t * 22) * ease(t / max(0.01, t_roll)) if tt < 0 else 0.0
        o = fire_svg(CAMP_FIRE[0], CAMP_FIRE[1] - 4, 34, t, 3)
        o += dust.svg(t) + rock_svg(roll_u(tt, roll_dur), wob)
        if t_stop_glow is not None:
            o += held_glow(t, t_stop_glow)
        if fereydun:
            o += fereydun(t)
        return o
    fx = [Glow(lambda t: cam_xy(cam, t, CAMP_FIRE[0], CAMP_FIRE[1] - 40), 200, (255, 160, 80), 0.4),
          Embers(16, 851, (CAMP_FIRE[0] - 30, CAMP_FIRE[1] - 200, CAMP_FIRE[0] + 30, CAMP_FIRE[1] - 40), (40, 100))]
    return Shot(dur, night, mid, cam=shake(cam, t_roll + roll_dur, t_roll + roll_dur + 0.5, 5) if t_stop_glow is not None else cam,
                light=MOONC, fx=fx, grade="night", bloom=0.5, fade_in=fade_in, fade_out=fade_out)


def tent_inside():
    """inside Fereydun's tent at night: canvas walls with seams, the lit door flap at the right, a hanging oil lamp, a rug"""
    s = ("<defs>" + bgs.FILTERS + bgs.lg("tw", [(0, "#2a2430", 1), (1, "#4a3a36", 1)]) +
         bgs.rg("tl", 300, 700, 700, [(0, "#ffb060", 0.45), (1, "#ffb060", 0)]) + "</defs>")
    s += f'<rect width="{W}" height="{H}" fill="url(#tw)"/>'
    for x in range(-40, W + 80, 120):
        s += f'<path d="M {x} 0 C {x + 30} 600, {x - 20} 1200, {x + 10} 1920" stroke="#1a141c" stroke-width="5" opacity="0.5"/>'
    s += '<path d="M 0 360 C 300 420, 780 420, 1080 360" stroke="#5e1e22" stroke-width="18" opacity="0.8"/>'
    s += '<path d="M 820 1300 L 950 520 L 1080 1300 Z" fill="#3a4466" opacity="0.6"/>'
    s += '<rect width="1080" height="1920" fill="url(#tl)"/>' + bgs.oil_lamp(300, 700, 600)
    s += '<path d="M -40 1250 L 1120 1250 L 1120 1920 L -40 1920 Z" fill="#3a2420"/>'
    s += '<path d="M 60 1300 L 1020 1300 L 1060 1880 L 20 1880 Z" fill="#6a1e1e" stroke="#2a0e0e" stroke-width="5"/>'
    s += '<path d="M 110 1340 L 970 1340 L 1000 1840 L 80 1840 Z" fill="none" stroke="#c9a24a" stroke-width="8" opacity="0.8"/>'
    return svg_render(s)


def bedding():
    """Fereydun's bed seen from above, at night: a rug with a gold border on the tent floor, lamp light from the upper left"""
    s = ("<defs>" + bgs.FILTERS + bgs.rg("bl", 160, 420, 900, [(0, "#ffb060", 0.4), (1, "#ffb060", 0)]) + "</defs>")
    s += f'<rect width="{W}" height="{H}" fill="#2a1e1c"/>'
    s += '<path d="M -60 250 L 1140 250 L 1140 1700 L -60 1700 Z" fill="#5e1a1e" stroke="#1a0a0a" stroke-width="6"/>'
    s += '<path d="M -60 310 L 1140 310 M -60 1640 L 1140 1640" stroke="#c9a24a" stroke-width="12"/>'
    r = random.Random(853)
    for k in range(14):
        x = 40 + k * 80
        s += f'<path d="M {x} 330 L {x + 40} 370 L {x} 410 L {x - 40} 370 Z" fill="#c9a24a" opacity="0.6"/><path d="M {x} 1560 L {x + 40} 1600 L {x} 1640 L {x - 40} 1600 Z" fill="#c9a24a" opacity="0.6"/>'
    for k in range(60):
        x, y = r.uniform(0, W), r.uniform(450, 1500)
        s += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r.uniform(8, 18):.0f}" fill="#7a2a24" opacity="0.5"/>'
    s += '<rect width="1080" height="1920" fill="url(#bl)"/>'
    return svg_render(s)


def waking(dur, t_wake, fade_in=0.0):
    """Fereydun asleep, seen from above, close on his face; his eyes open at t_wake and look towards the noise"""
    bed = bgs.cached("zh_p8_bedding", bedding)
    cam = cam_push(1.3, 1.38, 420, 760, dur)

    def mid(t):
        w = ease((t - t_wake) / 0.25)
        q = P(blink=1.0 - w, brow=1.0 * w, furrow=0.3 - 0.8 * w, gx=0.0, gy=0.9 * w, turn=0.0, armL="relaxed", armR="relaxed",
              breathe=math.sin(t * 1.4) * (1 - w), wind=0.0, tilt=2 * w)
        pillow = ('<path d="M 240 520 C 200 640, 210 900, 250 1010 C 330 1040, 600 1040, 640 1000 C 680 880, 680 620, 640 520 C 560 480, 320 480, 240 520 Z" '
                  'fill="#e6dcc4" stroke="#2a1a10" stroke-width="5"/><path d="M 300 560 C 280 700, 290 880, 310 960" stroke="#c8bca0" stroke-width="10" fill="none"/>')
        blanket = ('<path d="M 600 380 C 700 360, 900 360, 1140 380 L 1140 1300 C 900 1320, 700 1320, 600 1300 C 640 1000, 640 700, 600 380 Z" fill="#3e3a6a" '
                   'stroke="#120e1e" stroke-width="5"/><path d="M 640 420 C 670 700, 670 1000, 640 1260" stroke="#c9a24a" stroke-width="12" fill="none"/>')
        return pillow + lying_at(FEREYDUN, q, t, 1430, 960, 1.25) + blanket
    return Shot(dur, bed, mid, cam=cam, bg_par=1.0, light=dict(ambient=(0.74, 0.7, 0.84), rim=(-5, -2), rim_col=(1.0, 0.7, 0.4), rim_str=0.7),
                fx=[Glow(lambda t: (140, 420), 380, (255, 170, 90), 0.3)], grade="night", bloom=0.5, fade_in=fade_in)


def stop_close(dur, line, t_line, seed=0):
    """Fereydun at his tent door at night, close: he throws out his open hand at the rock: "Stop!" """
    nb = camp_bg("night", 6)
    cam = cam_push(1.0, 1.05, 480, 860, dur)
    X, Y, S_ = 340, 1020, 1.0
    ARM = lambda u: ("ik", lerp(170, 560, u), lerp(330, -40, u))

    def mid(t):
        u = ease((t - t_line + 0.25) / 0.25)
        q = tp([(line, t_line)], t, seed, turn=0.45, gx=0.9, gy=-0.6, furrow=1.5, brow=-0.5, armL=ARM(u), openL=u > 0.6, armR="relaxed", wind=0.5)
        o = at_neck(FEREYDUN, q, t, X, Y, S_)
        hx, hy = hand_at(FEREYDUN, ARM(u), 1, X, Y, S_, neck=True)
        return o + palm_ring(hx, hy - 30, t, t_line + 0.1, s=1.6)
    return Shot(dur, nb, mid, cam=shake(cam, t_line + 0.1, t_line + 0.5, 6), light=DOORC,
                fx=[Glow(lambda t: (60, 980), 360, (255, 170, 90), 0.35)], grade="night", bloom=0.7)


# ================================================================ S1 the hook (0-8.6)
def s1():
    A = wide_rock(2.6, A8.ROLL1, A8.STOP1 - A8.ROLL1, fade_in=0.3, cam=cam_push(1.1, 1.16, 760, 1000, 2.6), dust_seed=1)
    B = waking(1.0, 0.25)
    C = stop_close(1.4, "p8s1a", A8.LINES[0][1] - 3.6, 1)
    t0 = 5.0     # D starts at part time 5.0: the rock is already held
    D = wide_rock(3.6, A8.ROLL1 - t0, A8.STOP1 - A8.ROLL1, t_stop_glow=0.0, fade_out=0.5,
                  cam=cam_push(1.08, 1.16, 600, 1100, 3.6), dust_seed=1)
    return [A, B, C, D]


# ================================================================ S2 title (8.6-13.2): the Kaviani banner against the dawn sky
def big_banner(x, y, s, t, ang=0.0, **kw):
    c = Ctx(lw_for(s))
    return f'<g transform="translate({x:.1f},{y:.1f}) rotate({ang:.2f}) scale({s:.4f})">{kaviani(c, t, **kw)}</g>'


def banner_glints(t, x, y, s, t0s=(0.6, 1.5, 2.6, 3.4)):
    o = ""
    for k, t0 in enumerate(t0s):
        u = (t - t0) / 0.6
        if 0 < u < 1:
            jx, jy = kav_point(t, *KAV_JEWELS[k % len(KAV_JEWELS)][:2]) if k % 2 else kav_point(t, 0.5, 0.45)
            gx, gy = x + jx * s, y + jy * s
            a = math.sin(math.pi * u); r1, r2 = 60 * a * s, 9 * a * s
            o += (f'<path d="M {gx:.1f} {gy - r1:.1f} L {gx + r2:.1f} {gy - r2:.1f} L {gx + r1:.1f} {gy:.1f} L {gx + r2:.1f} {gy + r2:.1f} L {gx:.1f} {gy + r1:.1f} '
                  f'L {gx - r2:.1f} {gy + r2:.1f} L {gx - r1:.1f} {gy:.1f} L {gx - r2:.1f} {gy - r2:.1f} Z" fill="#fffbe8" opacity="{0.95 * a:.2f}"/>')
    return o


def s2():
    dawn = camp_bg("dawn", 3)
    cam = cam_push(1.0, 1.06, 540, 700, 4.6)

    def mid(t):
        return big_banner(540, 1230, 1.05, t + 2.0, ang=2 * math.sin(t * 0.8)) + banner_glints(t, 540, 1230, 1.05)
    return [Shot(4.6, dawn, mid, cam=cam, light=dict(DAWNC, ramp=None), sun=(200, 860, 900, (0.14, 0.09, 0.05)),
                 fx=[Motes(50, 852, (255, 236, 210), (0, 200, W, 1300), (-10, -6), amax=100)], bloom=0.7, fade_in=0.4, fade_out=0.5)]



# ================================================================ S3 Kaveh comes to Fereydun; the banner (13.2-51.2)
def crowd_walkers(seed, n, x0s, ys, scs):
    r = random.Random(seed)
    return [(random_spec(r, ("man", "man", "woman", "man", "boy")), x0s[k % len(x0s)] + r.uniform(-40, 40), ys[k % len(ys)], scs[k % len(scs)],
             r.uniform(0, 6.3)) for k in range(n)]


def fq(lines, t, seed, **kw):
    base = dict(turn=0.2, gx=0.5, gy=0.0, furrow=0.5, brow=0.1, armL="relaxed", armR="relaxed", wind=0.3)
    base.update(kw)
    return tp(lines, t, seed, **base)


def s3():
    day = camp_bg("day")
    dayb = camp_bg("day", 6)
    # A: Kaveh and the people walk into the camp; Fereydun and his mother come to meet them
    camA = cam_push(1.0, 1.05, 560, 1200, 7.2)
    walkers = crowd_walkers(831, 8, (-560, -440, -330, -220, -680, -760, -500, -380), (1540, 1610, 1500, 1680, 1580, 1500, 1720, 1460),
                            (0.44, 0.47, 0.42, 0.5, 0.45, 0.41, 0.52, 0.4))
    STOP_A = 5.6

    def midA(t):
        u = ease(min(t, STOP_A) / STOP_A)
        walking = t < STOP_A
        o = ""
        f = P(turn=-0.35, gx=-0.8, gy=-0.1, brow=0.5, furrow=0.2, armL="relaxed", armR="relaxed", blink=blink_at(t, 1), wind=0.3)
        m = P(turn=-0.35, gx=-0.8, gy=-0.1, brow=0.6, sad=0.2, armL="chest", armR="relaxed", blink=blink_at(t, 2), wind=0.3)
        o += at_feet(FARANAK, m, t, 950, 1470, 0.43) + at_feet(FEREYDUN, f, t, 800, 1500, 0.46)
        for k, (S, x0, y, sc, ph) in sorted(enumerate(walkers), key=lambda e: e[1][2]):
            q = P(legs="walk" if walking else "stand", phase=t * 5 + ph, turn=0.35, gx=0.7, gy=-0.1, brow=0.4, armL="relaxed", armR="relaxed",
                  blink=blink_at(t, 10 + k), wind=0.3)
            o += at_feet(S, q, t, x0 + 560 * u, y, sc)
        k = P(legs="walk" if walking else "stand", phase=t * 5, turn=0.35, gx=0.7, gy=-0.1, furrow=0.8, brow=0.0, armR=("ik", -150, 220),
              propR="apron_spear", armL="relaxed", blink=blink_at(t, 3), wind=0.4)
        o += at_feet(KAVEH_NOAPRON, k, t, lerp(-160, 470, u), 1560, 0.47)
        return o
    A = Shot(7.2, day, midA, cam=camA, light=DAYC, sun=SUN_DAYC, fx=[Motes(40, 831, (255, 240, 210), (0, 600, W, 1500), (8, -6), amax=80)], fade_in=0.5)

    # B: Kaveh speaks
    LB = [("p8s3c", 0.3), ("p8s3d", 3.7)]

    def midB(t):
        q = kaveh_q(LB, t, 4, turn=0.25, gx=0.6, gy=-0.2, furrow=0.9, brow=-0.1, armR=("ik", -190, 250), propR="apron_spear",
                    armL="fist_up" if 3.9 < t < 5.4 else ("chest" if 0.6 < t < 3.0 else "relaxed"), wind=0.4)
        return at_neck(KAVEH_NOAPRON, q, t, 600, 930, 1.0)
    B = Shot(5.8, dayb, midB, cam=cam_push(1.0, 1.04, 560, 800, 5.8), light=dict(DAYC, ramp=(0, W, 0.92, 1.05)), sun=SUN_DAYC)

    # C: Fereydun looks up at the apron on the spear, then smiles
    LC = [("p8s3e", 0.3), ("p8s3f", 3.3)]

    def midC(t):
        look = 1 - ease((t - 2.9) / 0.4)
        smile = ease((t - 3.1) / 0.6)
        q = fq(LC, t, 5, turn=-0.2, gx=-0.6 * look - 0.3, gy=-0.8 * look, brow=0.8 * look + 0.2, furrow=-0.2, smile=0.5 * smile, armL="relaxed",
               armR="relaxed")
        return at_neck(FEREYDUN, q, t, 540, 960, 1.05)
    C = Shot(5.0, dayb, midC, cam=cam_push(1.0, 1.05, 540, 800, 5.0), light=dict(DAYC, ramp=(0, W, 1.05, 0.92)), sun=SUN_DAYC)

    # D: "Bring silk, gold and jewels!"
    LD = [("p8s3g", 0.2)]
    heads = bgs.cached("zh_p8_heads_day", lambda: back_heads(832, 9, 1830, 0.66, col="#2a2018", blur=4))

    def midD(t):
        raise_ = ease((t - 0.3) / 0.4)
        q = fq(LD, t, 6, turn=-0.1, gx=-0.3, gy=-0.3, furrow=0.6, brow=0.4, smile=0.3, armL="fist_up" if raise_ > 0.5 else "relaxed",
               armR="relaxed", wind=0.4)
        k = kaveh_q([], t, 7, turn=0.3, gx=0.7, gy=-0.2, furrow=0.3, brow=0.4, smile=0.3, armR=("ik", -150, 220), propR="apron_spear",
                    armL="relaxed", wind=0.4)
        return at_feet(KAVEH_NOAPRON, k, t, 300, 1600, 0.58) + at_feet(FEREYDUN, q, t, 680, 1580, 0.6)
    D = Shot(4.4, day, midD, fg=heads, cam=cam_push(1.04, 1.08, 520, 1100, 4.4), bg_par=1.0, light=DAYC, sun=SUN_DAYC)

    # E: the apron is dressed in silk, gold and jewels; ribbons
    E0 = 35.6
    pops = [p - E0 for p in A8.BANNER_POPS]
    dayb8 = camp_bg("day", 10)
    GX, GY, GS = 540, 1600, 1.25

    def stateE(t):
        silk = ease((t - 0.4) / 1.4)
        star = ease((t - pops[0]) / 0.25)
        jewels = sum(1 for p_ in pops[1:] if t > p_) + (1 if t > 6.2 else 0)
        ribbons = tuple(ease((t - 3.9 - 0.45 * k) / 0.8) for k in range(5))
        return silk, star, jewels, ribbons

    def midE(t):
        silk, star, jewels, ribbons = stateE(t)
        o = big_banner(GX, GY, GS, t, silk=silk, star=star, jewels=jewels, ribbons=ribbons)
        for k, p_ in enumerate(pops):
            u = (t - p_) / 0.5
            if 0 < u < 1:
                jx, jy = kav_point(t, 0.5, 0.45) if k == 0 else kav_point(t, *KAV_JEWELS[k - 1][:2])
                gx, gy = GX + jx * GS, GY + jy * GS
                a = math.sin(math.pi * u); r1, r2 = (110 if k == 0 else 60) * a, 10 * a
                o += (f'<path d="M {gx:.1f} {gy - r1:.1f} L {gx + r2:.1f} {gy - r2:.1f} L {gx + r1:.1f} {gy:.1f} L {gx + r2:.1f} {gy + r2:.1f} L {gx:.1f} {gy + r1:.1f} '
                      f'L {gx - r2:.1f} {gy + r2:.1f} L {gx - r1:.1f} {gy:.1f} L {gx - r2:.1f} {gy - r2:.1f} Z" fill="#fffbe8" opacity="{0.95 * a:.2f}"/>')
        return o
    E = Shot(8.0, dayb8, midE, cam=cam_push(1.0, 1.06, 540, 640, 8.0), light=dict(DAYC, ramp=None, ambient=(1.02, 0.99, 0.96)), sun=(900, 300, 800, (0.1, 0.08, 0.05)),
             fx=[Motes(40, 833, (255, 240, 200), (200, 200, 900, 1300), (4, -10), amax=110)], bloom=0.7)

    # F: Kaveh raises the Kaviani banner; the people cheer
    cheer = Cheering(834, [(140, 1490, 0.4), (320, 1480, 0.39), (800, 1490, 0.4), (970, 1500, 0.4),
                           (70, 1660, 0.48), (1010, 1670, 0.48), (240, 1720, 0.5), (860, 1730, 0.5)])
    back = bgs.cached("zh_p8_crowd_back", lambda: market_crowd(835, 12, 1360, 0.32, -20, 1100, 0.0))

    def bgF(t):
        im = day.copy()
        im.alpha_composite(back, (0, int(2 * math.sin(t * 2))))
        return im
    camF = cam_push(1.1, 1.0, 540, 1000, 7.6)

    def midF(t):
        lift = ease(t / 0.8)
        k = P(turn=0.0, gx=0.0, gy=-0.6, furrow=0.8, brow=0.3, smile=0.4, armR=("ik", lerp(-170, -60, lift), lerp(200, -470, lift)) if lift < 1 else "fist_up",
              propR="kaviani", armL="fist_up" if (t > 1.2 and math.sin(t * 2.4) > 0) else "relaxed", mouth_o=max(0.0, 0.4 * math.sin(t * 5)) if t > 1 else 0.0,
              blink=blink_at(t, 8), wind=0.6)
        f = P(turn=-0.25, gx=-0.4, gy=-0.6, brow=0.5, smile=0.6, armL="relaxed", armR="relaxed", blink=blink_at(t, 9), wind=0.4)
        return at_feet(FEREYDUN, f, t, 700, 1440, 0.43) + at_feet(KAVEH_NOAPRON, k, t, 470, 1430, 0.43) + cheer.svg(t, 1.0, (520, 900))
    dust = dust_tex()

    def dustF(im, t):
        x = int(400 + 40 * t)
        d = dust.crop((x, 0, x + W, H)).transform((W, H), Image.AFFINE, (1, 0, 0, 0, 1, 180))
        d.putalpha(d.getchannel("A").point(lambda v: int(v * 0.3)))
        im.alpha_composite(d)
    F = Shot(7.6, bgF, midF, cam=camF, light=DAYC, sun=SUN_DAYC, fx=[dustF, Motes(60, 836, (255, 236, 200), (0, 300, W, 1600), (12, -10), amax=110)],
             fade_out=0.5)
    return [A, B, C, D, E, F]



# ================================================================ S4 the brothers; the mace drawn in the dust and forged (51.2-84.8)
def dust_ground():
    """the ground of the camp seen from above: sandy earth, pebbles, a few blades of grass"""
    r = random.Random(841)
    s = ("<defs>" + bgs.FILTERS + bgs.rg("dg", 400, 600, 1200, [(0, "#d8bc8c", 1), (1, "#a8865c", 1)]) + "</defs>")
    s += f'<rect width="{W}" height="{H}" fill="url(#dg)"/>'
    for k in range(260):
        x, y = r.uniform(-20, W + 20), r.uniform(-20, H + 20)
        rr = r.uniform(3, 14)
        s += f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{rr:.1f}" ry="{rr * r.uniform(0.6, 1):.1f}" fill="{r.choice(("#8a6a46", "#b89870", "#e6d0a8", "#7a5a3a"))}" opacity="{r.uniform(0.3, 0.7):.2f}"/>'
    for k in range(40):
        x, y = r.uniform(0, W), r.uniform(0, H)
        for j in range(4):
            s += f'<path d="M {x:.0f} {y:.0f} q {r.uniform(-10, 10):.0f} {-r.uniform(10, 20):.0f} {r.uniform(-24, 24):.0f} {-r.uniform(20, 40):.0f}" stroke="#7a8a4a" stroke-width="3" fill="none" opacity="0.6"/>'
    s += '<path d="M 120 1500 l 40 -16 l 50 10 M 860 300 l 30 20 l 40 -6" stroke="#6a4a2e" stroke-width="5" fill="none" opacity="0.4"/>'
    return svg_render(s)


def _ox_strokes():
    """the ox-headed mace drawn in the dust: (polyline points) in drawing order"""
    shaft = [(540, 1060), (540, 900), (540, 760)]
    head = [(540, 760), (500, 740), (470, 700), (452, 640), (446, 590), (440, 545), (405, 520), (365, 488), (335, 440), (326, 400),
            (350, 432), (392, 470), (440, 492), (482, 476), (540, 468), (598, 476), (640, 492), (688, 470), (730, 432), (754, 400),
            (745, 440), (715, 488), (675, 520), (640, 545), (634, 590), (628, 640), (610, 700), (580, 740), (540, 760)]
    return [shaft, head]


def _dense(pts, step=8):
    out = [pts[0]]
    for (xa, ya), (xb, yb) in zip(pts, pts[1:]):
        n = max(1, int(math.hypot(xb - xa, yb - ya) / step))
        out += [(lerp(xa, xb, k / n), lerp(ya, yb, k / n)) for k in range(1, n + 1)]
    return out


OX = [_dense(p_) for p_ in _ox_strokes()]
OX_DOTS = [(492, 600), (588, 600), (520, 700), (560, 700)]


def groove(pts):
    if len(pts) < 2:
        return ""
    d = "M " + " L ".join(f"{x:.1f} {y:.1f}" for x, y in pts)
    d2 = "M " + " L ".join(f"{x + 3:.1f} {y + 3:.1f}" for x, y in pts)
    return (f'<path d="{d2}" stroke="#f6e6c4" stroke-width="8" fill="none" stroke-linecap="round" stroke-linejoin="round" opacity="0.9"/>'
            f'<path d="{d}" stroke="#4a301a" stroke-width="16" fill="none" stroke-linecap="round" stroke-linejoin="round" opacity="0.9"/>')


def drawing_hand(px, py, col="#2a4a7a", cuff="#c9a24a", skin="light", out=0.0):
    """Fereydun's hand drawing in the dust with a stick whose tip is at (px, py); the sleeve comes in from the bottom right"""
    sk = SKINS[skin]
    dx, dy = 700 * out, 800 * out
    tx, ty = px + dx, py + dy
    hx, hy = tx + 150, ty + 180
    ux, uy = 0.62, 0.78
    nx, ny = -uy, ux
    w0, w1, L = 60, 82, 900
    pts = [(hx + ux * 40 + nx * w0, hy + uy * 40 + ny * w0), (hx + ux * L + nx * w1, hy + uy * L + ny * w1),
           (hx + ux * L - nx * w1, hy + uy * L - ny * w1), (hx + ux * 40 - nx * w0, hy + uy * 40 - ny * w0)]
    sleeve = "M " + " L ".join(f"{x:.1f} {y:.1f}" for x, y in pts) + " Z"
    c0 = (hx + ux * 52 + nx * (w0 + 6), hy + uy * 52 + ny * (w0 + 6)); c1 = (hx + ux * 52 - nx * (w0 + 6), hy + uy * 52 - ny * (w0 + 6))
    return (f'<path d="M {tx:.1f} {ty:.1f} L {hx + 30:.1f} {hy + 36:.1f}" stroke="#2a1a10" stroke-width="16" stroke-linecap="round"/>'
            f'<path d="M {tx:.1f} {ty:.1f} L {hx + 30:.1f} {hy + 36:.1f}" stroke="#8a5a2e" stroke-width="10" stroke-linecap="round"/>'
            f'<path d="{sleeve}" fill="{col}" stroke="{OUT}" stroke-width="3.4"/>'
            f'<path d="M {c0[0]:.1f} {c0[1]:.1f} L {c1[0]:.1f} {c1[1]:.1f}" stroke="{cuff}" stroke-width="30" stroke-linecap="round"/>'
            f'<ellipse cx="{hx + 4:.1f}" cy="{hy + 2:.1f}" rx="64" ry="50" transform="rotate(-40,{hx + 4:.1f},{hy + 2:.1f})" fill="{sk[0]}" stroke="{OUT}" stroke-width="3.4"/>'
            f'<path d="M {hx - 40:.1f} {hy - 10:.1f} C {hx - 30:.1f} {hy + 20:.1f}, {hx - 6:.1f} {hy + 38:.1f}, {hx + 22:.1f} {hy + 44:.1f}" stroke="{sk[1]}" stroke-width="4" fill="none"/>'
            f'<ellipse cx="{hx - 26:.1f}" cy="{hy - 26:.1f}" rx="26" ry="17" transform="rotate(-40,{hx - 26:.1f},{hy - 26:.1f})" fill="{sk[2]}" stroke="{OUT}" stroke-width="3"/>')


def s4():
    day = camp_bg("day")
    dayb = camp_bg("day", 6)
    # A1: the three brothers
    LA = [("p8s4a", 0.2)]

    def midA1(t):
        kn = ease((t - 2.2) / 0.4) * (1 - ease((t - 3.4) / 0.4))
        pn = ease((t - 3.5) / 0.4)
        k = tp([], t, 1, turn=0.25, gx=0.5 - 0.3 * kn, gy=0.1, furrow=0.2, brow=0.2, smile=0.3 * kn, nod=10 * kn, armL="relaxed", armR="chest")
        f = tp([], t, 2, turn=0.0, gx=-0.4 * kn + 0.5 * pn, gy=0.0, furrow=0.3, brow=0.2, smile=0.2, armL="relaxed", armR="relaxed")
        pq = tp([], t, 3, turn=-0.25, gx=-0.5 + 0.3 * pn, gy=0.1, furrow=0.3, brow=0.1, smile=0.3 * pn, nod=10 * pn, armL="relaxed", armR="relaxed")
        return at_neck(KAYANUSH, k, t, 220, 1000, 0.72) + at_neck(PURMAYEH, pq, t, 860, 1010, 0.7) + at_neck(FEREYDUN, f, t, 540, 960, 0.76)
    A1 = Shot(4.8, dayb, midA1, cam=cam_push(1.0, 1.04, 540, 820, 4.8), light=dict(DAYC, ramp=(0, W, 0.95, 1.04)), sun=SUN_DAYC, fade_in=0.4)

    # A2: Fereydun asks his brothers for the smiths; they go
    LF, LK = [("p8s4b", 0.2)], [("p8s4c", 4.4)]

    def midA2(t):
        go = ease((t - 5.0) / 1.2)
        f = fq(LF, t, 4, turn=-0.35, gx=-0.8, gy=0.0, furrow=0.4, brow=0.3, armL="relaxed", armR="offer" if 0.6 < t < 3.6 else "relaxed")
        k = tp(LK, t, 5, turn=0.35 - 0.7 * go, gx=0.8 - 1.6 * go, gy=0.0, furrow=0.2, brow=0.3, smile=0.3, nod=6 * ease((t - 4.4) / 0.3),
               legs="walk" if go > 0.02 else "stand", phase=t * 5, armL="relaxed", armR="chest" if 4.2 < t < 5.0 else "relaxed")
        pq = tp([], t, 6, turn=0.35 - 0.7 * go, gx=0.8 - 1.6 * go, gy=0.0, furrow=0.3, brow=0.2, legs="walk" if go > 0.02 else "stand",
                phase=t * 5 + 1.6, armL="relaxed", armR="relaxed")
        return (at_feet(PURMAYEH, pq, t, 470 - 330 * go, 1610, 0.56) + at_feet(KAYANUSH, k, t, 260 - 330 * go, 1600, 0.58) +
                at_feet(FEREYDUN, f, t, 790, 1590, 0.6))
    A2 = Shot(6.2, day, midA2, cam=cam_push(1.02, 1.06, 540, 1150, 6.2), bg_par=1.0, light=DAYC, sun=SUN_DAYC)

    # B: the shape drawn in the dust
    ground = bgs.cached("zh_p8_dust_ground", dust_ground)
    T0, T1 = 0.5, 5.4
    lens = [len(p_) for p_ in OX]

    def midB(t):
        u = ease((t - T0) / (T1 - T0)) if t > T0 else 0.0
        n = int(u * sum(lens))
        o = ""
        tip = OX[0][0]
        for st in OX:
            k = min(len(st), n)
            if k >= 1:
                o += groove(st[:k]); tip = st[k - 1]
            n -= len(st)
            if n <= 0:
                break
        dots = sum(1 for k in range(4) if t > 5.5 + 0.2 * k)
        for (x, y) in OX_DOTS[:dots]:
            o += f'<circle cx="{x}" cy="{y}" r="11" fill="#5a3e24" opacity="0.85"/><circle cx="{x + 3}" cy="{y + 3}" r="4" fill="#f0dcb4" opacity="0.7"/>'
        if dots:
            tip = OX_DOTS[dots - 1]
        out = (1 - ease((t - T0 + 0.5) / 0.5)) if t < T0 else ease((t - 6.0) / 0.4)
        return o + drawing_hand(tip[0], tip[1], out=out)
    B = Shot(6.4, ground, midB, cam=cam_push(1.0, 1.05, 540, 720, 6.4), light=dict(rim=(5, -2), rim_col=(1.0, 0.9, 0.72), ambient=(1.0, 0.97, 0.94)),
             sun=(200, 200, 900, (0.08, 0.06, 0.03)))

    # C: the smith
    LC = [("p8s4f", 0.2)]

    def midC(t):
        grin = ease((t - 1.0) / 0.5)
        q = tp(LC, t, 7, turn=0.2, gx=0.4, gy=0.1, brow=1.0 - 0.6 * grin, furrow=-0.4 + 0.5 * grin, smile=0.6 * grin, nod=-4 + 8 * grin,
               armL="relaxed", armR="fist_up" if grin > 0.6 else "relaxed", wind=0.2)
        return at_neck(SMITH, q, t, 520, 950, 1.05)
    C = Shot(2.6, dayb, midC, cam=cam_push(1.0, 1.04, 520, 800, 2.6), light=dict(DAYC, ramp=(0, W, 1.04, 0.92)), sun=SUN_DAYC)

    # D: the forge: two smiths, the hot ox head on the anvil, sparks
    hits = [h - 71.2 for h in A8.FORGE_HITS]
    AX, AY, SK = 330, 1450, 0.62
    camD = cam_push(1.0, 1.05, 420, 1050, 3.0)

    def midD(t):
        arm, ang = hammer_arm(t, hits=hits)
        q = P(turn=-0.35, gx=-0.7, gy=0.7, furrow=0.8, brow=0.0, armR=arm, propR=("hammer", ang), armL=("ik", -60, 420, "down"),
              blink=blink_at(t, 3), breathe=math.sin(t * 2), wind=0.1)
        q2 = P(turn=0.35, gx=0.7, gy=0.7, furrow=0.6, brow=0.1, armL=("ik", 190, 250), armR=("ik", 120, 300), blink=blink_at(t, 4), wind=0.1)
        hot = (f'<g transform="translate({AX + 30},{AY - 720 * SK - 18}) rotate(-90) scale({SK * 0.9:.3f})">'
               f'<circle cx="0" cy="-230" r="120" fill="#ff8a2a" opacity="0.35"/>{prop(Ctx(1.2), "mace", 0, 0, 0, t)}</g>')
        tongs = (f'<path d="M {AX - 190:.0f} {AY - 560:.0f} L {AX - 20:.0f} {AY - 470:.0f} M {AX - 186:.0f} {AY - 548:.0f} L {AX - 10:.0f} {AY - 460:.0f}" '
                 f'stroke="#2a2426" stroke-width="9" stroke-linecap="round"/>')
        fire = fire_svg(70, AY - 20, 70, t, 5)
        return (fire + at_feet(SMITH_2, q2, t, AX - 250, AY - 10, SK) + anvil_svg(AX, AY, SK) + hot + tongs +
                at_feet(SMITH, q, t, AX + 212, AY - 20, SK))

    def sparks(im, t):
        d = ImageDraw.Draw(im, "RGBA")
        for k, h in enumerate(hits):
            u = t - h
            if 0 <= u < 0.7:
                r = random.Random(k + 50)
                for j in range(18):
                    a = r.uniform(-2.9, -0.2); v = r.uniform(280, 600)
                    x = AX + 30 + math.cos(a) * v * u; y = AY - 720 * SK - 20 + math.sin(a) * v * u + 700 * u * u
                    cx_, cy_ = cam_xy(camD, t, x, y)
                    s_ = 4.0 * (1 - u / 0.7)
                    d.ellipse((cx_ - s_, cy_ - s_, cx_ + s_, cy_ + s_), fill=(255, 224, 150, int(255 * (1 - u / 0.7))))
    D = Shot(3.0, dayb, midD, cam=camD, light=dict(DAYC, ramp=(0, W, 1.06, 0.94)), sun=(70, 1380, 600, (0.16, 0.08, 0.02)),
             fx=[sparks, Glow(lambda t: cam_xy(camD, t, AX + 30, AY - 470), 240, (255, 150, 70), 0.4),
                 Embers(30, 842, (20, AY - 260, 140, AY - 40), (60, 140))], grade="fire", bloom=0.7)

    # E1: the mace shines like the sun
    LE = [("p8s4g", 0.2)]
    XE, YE, SE = 470, 960, 1.0
    ARME = lambda u: ("ik", lerp(150, 330, u), lerp(300, -330, u), "down")

    def midE1(t):
        u = ease((t - 0.2) / 0.7)
        q = tp([], t, 8, turn=0.25, gx=0.6 * u, gy=-0.8 * u, furrow=0.6, brow=0.5, smile=0.3 * u, armL=ARME(u), propL="mace", armR="relaxed", wind=0.4)
        o = at_neck(FEREYDUN, q, t, XE, YE, SE)
        hx, hy = hand_at(FEREYDUN, ARME(u), 1, XE, YE, SE, neck=True)
        gu = (t - 1.2) / 0.9
        if 0 < gu < 1:
            a = math.sin(math.pi * gu); gx, gy = hx + 10, hy - 240 * SE * FEREYDUN["bs"]
            r1, r2 = 150 * a, 16 * a
            o += (f'<circle cx="{gx:.1f}" cy="{gy:.1f}" r="{120 * a:.1f}" fill="#fff0c0" opacity="{0.4 * a:.2f}"/>'
                  f'<path d="M {gx:.1f} {gy - r1:.1f} L {gx + r2:.1f} {gy - r2:.1f} L {gx + r1:.1f} {gy:.1f} L {gx + r2:.1f} {gy + r2:.1f} L {gx:.1f} {gy + r1:.1f} '
                  f'L {gx - r2:.1f} {gy + r2:.1f} L {gx - r1:.1f} {gy:.1f} L {gx - r2:.1f} {gy - r2:.1f} Z" fill="#fffbe8" opacity="{0.95 * a:.2f}"/>')
        return o
    E1 = Shot(3.6, dayb, midE1, cam=cam_push(1.0, 1.05, 520, 760, 3.6), light=dict(DAYC, ramp=(0, W, 0.92, 1.06)), sun=(880, 300, 900, (0.16, 0.12, 0.06)),
              fx=[Motes(40, 843, (255, 240, 200), (300, 100, 1000, 900), (6, -12), amax=120)], bloom=0.9)

    # E2: the dream of Zahhak (part 5): the youngest warrior lifts the ox-headed mace
    gate = gate_bg()
    camE2 = cam_push(1.0, 1.06, 540, 1000, 3.4)
    X2, Y2, S2 = 540, 1720, 0.52

    def armE2(t):
        lift = ease((t - 0.2) / 1.0)
        return (lerp(40, 165, lift), lerp(60, -15, lift))

    def bodyE2(t):
        return at_feet(DREAM_YOUNG, P(turn=0.05, gx=0.0, armL=armE2(t), armR="relaxed", blink=0.0, wind=0.9), t, X2, Y2, S2)

    def maceE2(t):
        hx, hy = hand_at(DREAM_YOUNG, armE2(t), 1, X2, Y2, S2)
        return mace_at(hx, hy, S2 * DREAM_YOUNG["bs"], t, glint_t=1.4)
    E2 = Shot(3.4, gate, None, cam=camE2, fx=[dream_fx(), silhouette(camE2, bodyE2, over=maceE2),
                                              Motes(40, 844, (255, 220, 170), (0, 400, W, 1700), (4, -14), amax=110)],
              grade="night", bloom=0.8, fade_in=0.3, fade_out=0.3)

    # F: gold for the smiths
    LF2 = [("p8s4i", 0.3)]

    def midF(t):
        give = ease((t - 0.4) / 0.5)
        f = fq(LF2, t, 9, turn=0.35, gx=0.8, gy=0.0, furrow=0.2, brow=0.3, smile=0.5, armL="offer" if give > 0.5 else "relaxed",
               propL="purse" if (give > 0.5 and t < 2.2) else None, armR="relaxed")
        take = ease((t - 2.0) / 0.3)
        sm = P(turn=-0.35, gx=-0.8, gy=0.0, brow=0.5, smile=0.6, nod=12 * ease((t - 2.4) / 0.4), armR="offer" if take > 0.5 else "relaxed",
               propR="purse" if take > 0.5 else None, armL="relaxed", blink=blink_at(t, 10), wind=0.2)
        sm2 = P(turn=-0.35, gx=-0.8, gy=0.0, brow=0.4, smile=0.5, nod=10 * ease((t - 2.6) / 0.4), armL="chest", armR="relaxed", blink=blink_at(t, 11), wind=0.2)
        return at_feet(SMITH_2, sm2, t, 900, 1580, 0.56) + at_feet(SMITH, sm, t, 700, 1600, 0.6) + at_feet(FEREYDUN, f, t, 330, 1590, 0.6)
    F = Shot(3.6, day, midF, cam=cam_push(1.02, 1.05, 540, 1150, 3.6), bg_par=1.0, light=DAYC, sun=SUN_DAYC, fade_out=0.4)
    return [A1, A2, B, C, D, E1, E2, F]



# ================================================================ S5 dawn: the mother; the march (84.8-97.0)
def s5():
    dawn = camp_bg("dawn")
    dawnb = camp_bg("dawn", 5)
    LA = [("p8s5a", 0.3)]

    def midA(t):
        f = fq(LA, t, 1, turn=-0.35, gx=-0.8, gy=0.1, furrow=0.3, brow=0.4, sad=0.2, armL="relaxed", armR="chest" if 1.6 < t < 3.6 else "relaxed")
        m = tp([], t, 2, turn=0.35, gx=0.8, gy=-0.2, brow=0.8, furrow=-0.4, sad=0.5 + 0.2 * ease((t - 2.0) / 1.0), armL="relaxed", armR="chest", wind=0.3)
        return at_neck(FARANAK, m, t, 330, 1000, 0.84) + at_neck(FEREYDUN, f, t, 760, 960, 0.86)
    A = Shot(3.8, dawnb, midA, cam=cam_push(1.0, 1.04, 540, 820, 3.8), light=DAWNC, sun=SUN_DAWNC, fade_in=0.4)

    LB = [("p8s5b", 0.2)]
    from p02_scenes import eyes_of

    def midB(t):
        smile = ease((t - 0.9) / 0.6)
        m = tp(LB, t, 3, turn=0.2, gx=0.5, gy=-0.1, brow=1.0, furrow=-0.6, sad=0.7 - 0.3 * smile, smile=0.4 * smile, armL="relaxed", armR="chest", wind=0.3)
        o = at_neck(FARANAK, m, t, 540, 960, 1.05)
        ex, ey = eyes_of(540, 960, 1.05, 0.2)[0]
        return o + tear(ex, ey + 20, t, 0.4, 1.0)
    B = Shot(2.4, dawnb, midB, cam=cam_push(1.0, 1.04, 540, 800, 2.4), light=dict(DAWNC, ramp=(0, W, 1.05, 0.9)), sun=SUN_DAWNC)

    # C: the army sets out, the banner in front: Kaveh on foot, Fereydun on his horse, his brothers riding behind, soldiers further back
    LC = [("p8s5c", 0.4)]
    r = random.Random(851)
    foot = [(r.choice((FSOLDIER, FSOLDIER_2, FSOLDIER_3)), 560 + 110 * k + r.uniform(-20, 20), 1335 + 14 * (k % 3), 0.26 + 0.01 * (k % 3), r.uniform(0, 6.3))
            for k in range(8)]

    def midC(t):
        dx = -18 * t
        o = ""
        for k, (S, x0, y, sc, ph) in enumerate(foot):
            q = P(legs="walk", phase=t * 5.5 + ph, turn=-0.3, gx=-0.6, armL=(20, 10), propL="pike", armR="relaxed", furrow=0.5, blink=blink_at(t, 20 + k), wind=0.4)
            o += at_feet(S, q, t, x0 + dx, y, sc)
        for k, (S, x0, y, sc, col) in enumerate(((PURMAYEH, 1290, 1392, 0.8, "#5a3a22"), (KAYANUSH, 1050, 1400, 0.82, "#3a2a1e"))):
            q = P(turn=-0.4, gx=-0.8, armR="forward", armL="forward", furrow=0.4, blink=blink_at(t, 30 + k), wind=0.6)
            o += rider(S, q, t, lambda c, col=col, k=k: horse(c, col=col, walk=True, phase=t * 4.2 + k, t=t + k), x0 + dx, y, sc, flip=True)
        q = P(turn=-0.4, gx=-0.8, gy=-0.1, armR="forward", armL=("ik", 230, 120), propL="mace", furrow=0.6, brow=0.2, blink=blink_at(t, 33), wind=0.7)
        o += rider(FEREYDUN, q, t, lambda c: horse(c, col="#c8b48a", mane="#6a5a3a", walk=True, phase=t * 4.2 + 2.2, t=t + 2, blanket="#8a1a1a"),
                   800 + dx, 1480, 1.0, flip=True)
        k = P(legs="walk", phase=t * 5.2, turn=-0.3, gx=-0.6, gy=-0.3, furrow=0.6, brow=0.2, armR="fist_up", propR="kaviani", armL="relaxed",
              blink=blink_at(t, 34), wind=0.6)
        o += at_feet(KAVEH_NOAPRON, k, t, 300 + dx, 1530, 0.4)
        return o
    dust = dust_tex()

    def dustC(im, t):
        x = int(200 + 60 * t)
        d = dust.crop((x, 0, x + W, H)).transform((W, H), Image.AFFINE, (1, 0, 0, 0, 1, 120))
        d.putalpha(d.getchannel("A").point(lambda v: int(v * 0.35)))
        im.alpha_composite(d)
    C = Shot(6.0, dawn, midC, cam=cam_push(1.0, 1.05, 480, 1100, 6.0), light=DAWNC, sun=SUN_DAWNC,
             fx=[dustC, Motes(50, 852, (255, 236, 210), (0, 300, W, 1500), (-12, -6), amax=100)], fade_out=0.5)
    return [A, B, C]



# ================================================================ S6 night: Sorush; the jealous brothers; the rock (97.0-135.2)
def wings_svg(x, y, s, t, a=1.0):
    """Sorush's soft wings of light behind the shoulders of a figure placed at_neck at (x, y), scale s"""
    o = ""
    for sd in (-1, 1):
        flap = 6 * math.sin(t * 1.6 + sd)
        bx, by = x + sd * 120 * s, y + 90 * s
        for k, (L, col, op) in enumerate(((560, "#fff6dc", 0.55), (470, "#ffffff", 0.75), (360, "#fff2c8", 0.85))):
            ang = math.radians(-35 - 12 * k + flap)
            tx, ty = bx + sd * math.cos(ang) * L * s, by + math.sin(ang) * L * s
            mx, my = bx + sd * 260 * s, by + (120 - 40 * k) * s
            o += (f'<path d="M {bx:.1f} {by:.1f} C {bx + sd * 120 * s:.1f} {by - 260 * s:.1f}, {tx - sd * 80 * s:.1f} {ty - 60 * s:.1f}, {tx:.1f} {ty:.1f} '
                  f'C {tx - sd * 20 * s:.1f} {ty + 120 * s:.1f}, {mx:.1f} {my + 60 * s:.1f}, {bx:.1f} {by + 140 * s:.1f} Z" fill="{col}" opacity="{op * a:.2f}" '
                  f'stroke="#e8c060" stroke-width="{2.4 * s:.1f}" stroke-opacity="{0.6 * a:.2f}"/>')
            for j in range(5):
                u = (j + 1) / 6
                fx_, fy_ = lerp(bx, tx, u), lerp(by + 70 * s, ty + 40 * s, u)
                o += f'<path d="M {fx_:.1f} {fy_:.1f} l {sd * 30 * s:.1f} {90 * s:.1f}" stroke="#e8c060" stroke-width="{2 * s:.1f}" opacity="{0.35 * a:.2f}"/>'
    return o


def sorush(t, lines, x, y, s, seed, a=1.0, **kw):
    """Sorush, a figure of light: wings, a halo, her white and gold robe; a = how much of her is there (she fades away)"""
    if a <= 0.01:
        return ""
    fl = 10 * math.sin(t * 1.3)
    base = dict(turn=0.0, gx=0.2, gy=0.0, brow=0.3, furrow=-0.3, smile=0.35, armL="relaxed", armR="relaxed", wind=0.6)
    base.update(kw)
    q = tp(lines, t, seed, **base)
    halo = (f'<circle cx="{x:.1f}" cy="{y - 175 * s + fl:.1f}" r="{230 * s:.1f}" fill="#fff6d8" opacity="{0.35 * a:.2f}"/>'
            f'<circle cx="{x:.1f}" cy="{y - 175 * s + fl:.1f}" r="{190 * s:.1f}" fill="none" stroke="#ffe08a" stroke-width="{6 * s:.1f}" opacity="{0.6 * a:.2f}"/>')
    return f'<g opacity="{a:.3f}">' + wings_svg(x, y + fl, s, t, 1.0) + halo + at_neck(SORUSH, q, t, x, y + fl, s) + '</g>'


SORL = dict(ambient=(1.06, 1.04, 1.0), rim=(0, -3), rim_col=(1.0, 0.95, 0.8), rim_str=1.0)


def s6():
    night = camp_bg("night")
    nightb = camp_bg("night", 6)
    nightb8 = bgs.cached("zh_camp_night_b8_dark", lambda: Image.alpha_composite(camp_bg("night", 8), Image.new("RGBA", (W, H), (6, 8, 24, 90))))
    # A: Fereydun alone by the fire; a light appears
    LA = [("p8s6a", 0.3)]
    camA = cam_push(1.0, 1.05, 520, 900, 3.8)

    def midA(t):
        look = ease((t - 1.9) / 0.4)
        q = tp([], t, 1, legs="sit", turn=0.2 - 0.6 * look, gx=0.5 - 1.3 * look, gy=0.4 - 0.7 * look, furrow=0.3 - 0.6 * look, brow=0.2 + 0.8 * look,
               armL=("ik", 120, 330), armR=("ik", -120, 330), wind=0.2, cloak_len=0.5)
        seat = '<ellipse cx="460" cy="1326" rx="230" ry="34" fill="#0a0a12" opacity="0.6"/><path d="M 270 1330 L 650 1330 L 640 1290 L 280 1290 Z" fill="#3a2a22" stroke="#120a08" stroke-width="4"/>'
        return seat + at_neck(FEREYDUN, q, t, 460, 860, 0.8) + fire_svg(830, 1322, 80, t, 6)

    def lightA(im, t):
        a = ease((t - 1.4) / 1.4)
        if a > 0:
            g = Glow(lambda t_: (120, 560), 420, (255, 240, 200), 0.6 * a)
            g(im, t)
    A = Shot(3.8, nightb, midA, cam=camA, light=dict(FIREC, point=(830, 1240, 900, 0.55, 1.2, (1.0, 0.55, 0.25)), rim_point=(830, 6)),
             fx=[Glow(lambda t: cam_xy(camA, t, 830, 1250), 300, (255, 160, 80), 0.45), Embers(24, 861, (780, 1060, 880, 1300), (40, 110)), lightA,
                 Motes(30, 862, (255, 236, 190), (0, 300, 400, 900), (6, -10), amax=120)], grade="night", bloom=0.6, fade_in=0.4)

    # B: Sorush speaks
    LB = [("p8s6b", 0.2)]

    def midB(t):
        return sorush(t, LB, 540, 900, 0.95, 2, a=ease(t / 0.6), armL=("ik", 300, 120), openL=True, armR="relaxed")
    B = Shot(5.6, nightb8, midB, cam=cam_push(1.0, 1.04, 540, 760, 5.6), light=SORL,
             fx=[Glow(lambda t: (540, 760), 520, (255, 236, 190), 0.45), Motes(60, 863, (255, 236, 190), (100, 200, 1000, 1200), (4, -16), amax=140)],
             grade="night", bloom=0.9)

    # C: Fereydun, in the light
    def midC(t):
        q = tp([], t, 3, turn=-0.3, gx=-0.8, gy=-0.4, brow=1.0, furrow=-0.6, armL="relaxed", armR="relaxed", wind=0.3)
        q["blink"] = min(q["blink"], 0.2)
        return at_neck(FEREYDUN, q, t, 560, 960, 1.0)
    C = Shot(1.2, nightb8, midC, cam=cam_push(1.0, 1.03, 560, 800, 1.2),
             light=dict(ambient=(0.72, 0.74, 0.92), rim=(-6, -2), rim_col=(1.0, 0.9, 0.6), rim_str=1.2, ramp=(0, W, 1.2, 0.8)),
             fx=[Glow(lambda t: (0, 700), 500, (255, 236, 190), 0.4)], grade="night", bloom=0.6)

    # D: "I will teach you secret words…"; the light flows to him; she is gone
    LD = [("p8s6c", 0.2)]
    camD = cam_push(1.0, 1.04, 540, 800, 4.4)

    def midD(t):
        a = 1 - ease((t - 3.7) / 0.7)
        o = sorush(t, LD, 300, 920, 0.82, 4, a=a, armL=("ik", 300, 160), openL=True, armR="relaxed", gx=0.6, turn=0.2)
        f = tp([], t, 5, turn=-0.35, gx=-0.8 + 0.6 * (1 - a), gy=-0.2, brow=0.8, furrow=-0.4, smile=0.2 * ease((t - 2.6) / 0.6), armL="relaxed",
               armR="relaxed", wind=0.3)
        o += at_neck(FEREYDUN, f, t, 800, 970, 0.86)
        for k in range(14):                       # the secret words: little lights going from her palm to his forehead
            u = (t - 1.8 - 0.12 * k) / 1.0
            if 0 < u < 1:
                hx, hy = hand_at(SORUSH, ("ik", 300, 160), 1, 300, 920, 0.82, neck=True)
                ex, ey = 800, 970 - 200 * 0.86
                px = lerp(hx, ex, u); py = lerp(hy, ey, u) - 160 * math.sin(math.pi * u) + 20 * math.sin(k * 2.1)
                o += f'<circle cx="{px:.1f}" cy="{py:.1f}" r="{7 + 3 * math.sin(k):.1f}" fill="#fff2b0" opacity="{0.9 * math.sin(math.pi * u):.2f}"/>'
        return o

    def glowD(im, t):
        a = 1 - ease((t - 3.7) / 0.7)
        if a > 0.01:
            Glow(lambda t_: (300, 760), 460, (255, 236, 190), 0.45 * a)(im, t)
    D = Shot(4.4, nightb8, midD, cam=camD, light=dict(ambient=(0.95, 0.95, 1.0), rim=(-5, -2), rim_col=(1.0, 0.9, 0.65), rim_str=0.9, ramp=(0, W, 1.1, 0.85)),
             fx=[glowD, Motes(40, 864, (255, 236, 190), (0, 300, 700, 1200), (4, -16), amax=130)], grade="night", bloom=0.8, fade_out=0.3)

    # E1: the brothers on the hilltop
    top = bg("hilltop", zbg.hilltop)
    LE = [("p8s6d", 0.2), ("p8s6e", 2.6)]
    RX, RY, RR = 980, 1340, 330

    def big_rock(t, wob=0.0):
        return bgs.boulder(RX, RY, RR, 852, col=ROCK_COL[0], dark=ROCK_COL[1], lit=ROCK_COL[2], rot=wob)

    def midE1(t):
        k = tp([("p8s6e", 2.6)], t, 6, turn=-0.2 + 0.5 * ease((t - 2.4) / 0.3), gx=-0.5 + 1.2 * ease((t - 2.4) / 0.3), gy=0.5 - 0.5 * ease((t - 2.4) / 0.3),
               furrow=1.0, brow=-0.4, sad=0.1, armL="relaxed", armR="chest", wind=0.6)
        pq = tp([], t, 7, turn=-0.3, gx=-0.6, gy=0.6, furrow=0.9, brow=-0.3, armL="relaxed", armR="relaxed", wind=0.6)
        return big_rock(t) + at_feet(PURMAYEH, pq, t, 500, 1620, 0.62) + at_feet(KAYANUSH, k, t, 280, 1600, 0.62)
    E1 = Shot(5.6, top, midE1, cam=cam_push(1.0, 1.05, 480, 1000, 5.6), light=dict(MOONC, rim=(5, -3)), sun=(860, 330, 500, (0.06, 0.07, 0.1)),
              grade="night", bloom=0.5, fade_in=0.3)

    # E2: "Then help me push this rock. Quietly!" — they push
    LE2 = [("p8s6f", 0.2)]

    def midE2(t):
        push = ease((t - 2.3) / 0.4)
        wob = -2 * push * (0.5 + 0.5 * math.sin(t * 9)) - 6 * ease((t - 3.0) / 0.6)
        pq = tp(LE2, t, 8, turn=-0.3 + 0.7 * push, gx=-0.7 + 1.5 * push, gy=0.1, furrow=1.2 + 0.4 * push, brow=-0.5, nod=6 * push,
                armL=("ik", 294, 184) if push > 0.3 else ("point" if 0.8 < t < 2.2 else "relaxed"), armR=("ik", 200, 230) if push > 0.3 else "relaxed", wind=0.6)
        k = tp([], t, 9, turn=0.35, gx=0.7, gy=0.1, furrow=1.2, brow=-0.4, nod=6 * push, armL=("ik", 555, 222) if push > 0.3 else "relaxed",
               armR="relaxed", wind=0.6)
        rock = bgs.boulder(1250 + 6 * push * math.sin(t * 9), 1300, 520, 852, col=ROCK_COL[0], dark=ROCK_COL[1], lit=ROCK_COL[2], rot=wob)
        return rock + at_neck(KAYANUSH, k, t, 250, 920, 0.78) + at_neck(PURMAYEH, pq, t, 480, 900, 0.8)
    E2 = Shot(3.6, bg("hilltop", zbg.hilltop, 5), midE2, cam=cam_push(1.0, 1.04, 560, 800, 3.6), light=dict(MOONC, rim=(5, -3)),
              sun=(860, 330, 500, (0.06, 0.07, 0.1)), grade="night", bloom=0.5)

    # F1: the rock rolls down at the camp (the brothers small and dark on the summit)
    def brothers_top(t):
        o = ""
        for k, (S, x) in enumerate(((KAYANUSH, 1010), (PURMAYEH, 1060))):
            o += at_feet(S, P(turn=-0.3, gx=-0.6, gy=0.6, armL="relaxed", armR="relaxed", blink=0.0), t, x, 604, 0.1)
        return o
    camF = cam_push(1.1, 1.16, 760, 1000, 1.8)
    F1 = wide_rock(1.8, 0.0, A8.STOP2 - A8.ROLL2, cam=camF, dust_seed=2)
    F1.fx = list(F1.fx) + [silhouette(camF, brothers_top, fill=(8, 8, 14), glow=(110, 120, 160), blur=3, ga=0.5)]

    F2 = waking(1.4, 0.5)
    G = stop_close(1.4, "p8s6h", 0.2, 10)
    t0 = 125.8 - A8.ROLL2
    H_ = wide_rock(5.0, -t0, A8.STOP2 - A8.ROLL2, t_stop_glow=0.0, cam=cam_push(1.08, 1.18, 600, 1100, 5.0), dust_seed=2)

    # I: Fereydun looks up at the hilltop; two dark figures slip away
    LI = [("p8s6j", 0.2)]
    nb3 = camp_bg("night", 3)
    camI = cam_push(1.0, 1.04, 540, 800, 4.4)

    def midI(t):
        q = tp([], t, 11, turn=0.35, gx=0.8, gy=-0.7, furrow=0.9, brow=0.3, sad=0.2, armL="relaxed", armR="relaxed", wind=0.4)
        q["blink"] = max(q["blink"], 0.35 * ease((t - 3.2) / 0.4))
        return at_neck(FEREYDUN, q, t, 330, 1000, 0.86)

    def slip(t):
        u = ease((t - 0.6) / 2.6)
        o = ""
        for k, (S, x) in enumerate(((KAYANUSH, 960), (PURMAYEH, 1010))):
            o += at_feet(S, P(legs="walk", phase=t * 5 + k, turn=0.4, gx=0.8, armL="relaxed", armR="relaxed", blink=0.0), t, x + 170 * u, 600, 0.09)
        return o
    I = Shot(4.4, nb3, midI, cam=camI, light=DOORC, pre_fx=[silhouette(camI, slip, fill=(8, 8, 14), glow=(110, 120, 160), blur=3, ga=0.4, par=0.6)],
             fx=[Glow(lambda t: (40, 1000), 360, (255, 170, 90), 0.3)], grade="night", bloom=0.5, fade_out=0.5)
    return [A, B, C, D, E1, E2, F1, F2, G, H_, I]



# ================================================================ S7 the Arvand (135.2-159.4)
RIVL = dict(rim=(5, -2), rim_col=(1.0, 0.88, 0.66), ramp=(0, W, 0.94, 1.05), ambient=(1.0, 0.97, 0.93))
SUN_RIV = (860, 700, 900, (0.10, 0.08, 0.04))


def fereydun_rider(t, x, y, s, walk=False, look=(-0.6, -0.4), seed=0, **kw):
    q = P(turn=-0.4, gx=look[0], gy=look[1], armR="forward", armL=("ik", 230, 120), propL="mace", furrow=0.7, brow=0.2,
          blink=blink_at(t, 40 + seed), wind=0.7)
    q.update(kw)
    return rider(FEREYDUN, q, t, lambda c: horse(c, col="#c8b48a", mane="#6a5a3a", walk=walk, phase=t * 4.2, t=t, blanket="#8a1a1a",
                                                 head_down=0.1 + 0.1 * math.sin(t * 0.8)), x, y, s, flip=True)


def s7():
    riv = bg("arvand", zbg.arvand)
    rivb = bg("arvand", zbg.arvand, 5)
    far = bg("arvand_far", zbg.arvand_far)
    # A: the army reaches the river
    r = random.Random(871)
    foot = [(r.choice((FSOLDIER, FSOLDIER_2, FSOLDIER_3)), 820 + 85 * k + r.uniform(-20, 20), 1392 + 12 * (k % 3), 0.24 + 0.01 * (k % 3), r.uniform(0, 6.3))
            for k in range(7)]
    camA = cam_push(1.0, 1.05, 540, 1100, 7.2)

    def midA(t):
        u = ease(min(t, 4.2) / 4.2)
        walking = t < 4.2
        dx = 320 * (1 - u)
        o = ""
        for k, (S, x0, y, sc, ph) in enumerate(foot):
            q = P(legs="walk" if walking else "stand", phase=t * 5.5 + ph, turn=-0.3, gx=-0.6, gy=-0.3, armL=(20, 10), propL="pike", armR="relaxed",
                  furrow=0.5, blink=blink_at(t, 50 + k), wind=0.4)
            o += at_feet(S, q, t, x0 + dx, y, sc)
        o += fereydun_rider(t, 600 + dx, 1440, 0.86, walk=walking)
        k = P(legs="walk" if walking else "stand", phase=t * 5.2, turn=-0.3, gx=-0.6, gy=-0.4, furrow=0.6, brow=0.2, armR="fist_up", propR="kaviani",
              armL="relaxed", blink=blink_at(t, 41), wind=0.7)
        o += at_feet(KAVEH_NOAPRON, k, t, 230 + dx, 1420, 0.27)
        return o
    A = Shot(7.2, riv, midA, cam=camA, light=RIVL, sun=SUN_RIV, fx=[Motes(40, 872, (255, 240, 210), (0, 400, W, 1400), (-6, -4), amax=80)], fade_in=0.5)

    # B: Fereydun calls across the water
    LB = [("p8s7c", 0.2)]

    def midB(t):
        q = fq(LB, t, 1, turn=0.35, gx=0.8, gy=-0.3, furrow=0.9, brow=0.1, armL="wave" if 0.2 < t < 2.8 else "relaxed", armR="relaxed", wind=0.6)
        return at_neck(FEREYDUN, q, t, 450, 960, 0.98)
    B = Shot(3.4, rivb, midB, cam=cam_push(1.0, 1.04, 480, 800, 3.4), light=dict(RIVL, ramp=(0, W, 0.92, 1.06)), sun=SUN_RIV)

    # C: the river keeper on his jetty
    LC = [("p8s7d", 0.2), ("p8s7e", 4.7)]

    def midC(t):
        shake_ = 0.25 * math.sin(t * 9) * ease((t - 4.7) / 0.2) * (1 - ease((t - 6.0) / 0.3))
        q = tp(LC, t, 2, turn=-0.2 + shake_, gx=-0.5, gy=0.0, furrow=1.3, brow=-0.4, armR=("ik", -200, 180), propR="stick",
               armL="point" if 0.6 < t < 2.6 else ("wave" if 4.6 < t < 6.0 else "relaxed"), wind=0.3)
        return at_neck(FERRYMAN, q, t, 560, 900, 0.92)
    C = Shot(6.4, far, midC, cam=cam_push(1.0, 1.04, 560, 760, 6.4), light=dict(RIVL, ramp=(0, W, 1.04, 0.94)), sun=(200, 760, 900, (0.08, 0.06, 0.03)))

    # D: Fereydun looks at the wide, deep river; the end card comes up
    def midD(t):
        k = P(turn=-0.2, gx=-0.4, gy=-0.4, furrow=0.6, brow=0.2, armR="fist_up", propR="kaviani", armL="relaxed", blink=blink_at(t, 42), wind=0.9)
        return (at_feet(KAVEH_NOAPRON, k, t, 220, 1420, 0.27) +
                fereydun_rider(t, 640, 1450, 0.88, look=(-0.7, -0.5), furrow=1.0, brow=-0.2))
    D = Shot(7.2, riv, midD, cam=cam_push(1.0, 1.08, 480, 1000, 7.2), light=RIVL, sun=SUN_RIV,
             fx=[Motes(40, 873, (255, 240, 210), (0, 400, W, 1400), (-10, -4), amax=80)], fade_out=0.8)
    return [A, B, C, D]


SCENES = {"s1": s1, "s2": s2, "s3": s3, "s4": s4, "s5": s5, "s6": s6, "s7": s7}
