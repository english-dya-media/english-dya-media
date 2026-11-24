"""Part 3 · Nawfal — 2D cartoon. Timing matches leyli/p03_audio.py
(scene starts s1 0, s2 7.6, s3 12.2, s4 47.0, s5 68.6, s6 92.6, s7 122.0; end card 139.8; total 145.0).
The battles are dust, lances, banners and shouting: nobody is hurt on screen."""
import math, random
from PIL import Image, ImageFilter
from film import Shot, W, H, ease, lerp, blink_at, cam_push, Motes, svg_render
from chars import horse, camel, gazelle, Ctx
from stage import at_neck, at_feet, rider, lw_for
import bgs, lbg
from cast import *
from p01_scenes import P, tp, bg, seated, birds, SandWind, DUSKL, SUN_DUSK, DAWNL, SUN_DAWN, DAYL, SUN_DAY, LAMPC
from p02_scenes import gifts, praying
import p03_audio as AU

DUSTL = dict(DAYL, ambient=(0.97, 0.93, 0.88))             # day light through the dust of the battle
GREY_H = dict(col="#c8c6c0", mane="#5a5a5a", blanket="#1e5a3a")      # Nawfal's big grey horse
HORSES_N = [("#6b4426", "#1d120c", "#1e5a3a"), ("#3a2a1e", "#120c08", "#e8e0cc"), ("#8a5a32", "#2a1a10", "#1e5a3a"), ("#2a2224", "#0e0a0a", None)]
HORSES_T = [("#2a2224", "#0e0a0a", "#5a1416"), ("#5a3a22", "#1d120c", "#26242c"), ("#1a1a1e", "#0a0a0c", "#7a1418"), ("#7a5236", "#2a1a10", None)]


def L(t0, *ids):
    """line ids -> [(id, start within a shot that begins at t0)]; a line said twice is taken at its first time after t0"""
    out = []
    for i in ids:
        ts_ = [t for lid, t in AU.LINES if lid == i and t >= t0 - 0.5]
        out.append((i, min(ts_) - t0))
    return out


def shaky(cam, amp=5.0, f=13.0, t0=0.0, t1=99.0):
    """a camera that shakes between t0 and t1 (the ground trembling under the horses)"""
    def c(t):
        k, cx, cy, px, py = cam(t)
        a = amp if t0 <= t <= t1 else 0.0
        return k, cx, cy, px + a * math.sin(t * f), py + 0.7 * a * math.sin(t * f * 1.3 + 1.0)
    return c


def dust_tex():
    return bgs.cached("ly_dust_tex", lambda: svg_render("".join(
        f'<ellipse cx="{random.Random(i).uniform(-200, 2000):.0f}" cy="{random.Random(i + 50).uniform(1000, 1800):.0f}" '
        f'rx="{random.Random(i + 9).uniform(160, 380):.0f}" ry="{random.Random(i + 3).uniform(40, 120):.0f}" fill="#d0b080" opacity="0.55"/>'
        for i in range(36)), 2200, H).filter(ImageFilter.GaussianBlur(26)))


def dust_fx(a=0.7, speed=120.0, x0=200, lift=0, fade=None):
    """drifting clouds of dust; lift moves the band up (px); a: strength (or fade(t) -> 0..1 times a)"""
    tex = dust_tex()

    def fx(im, t):
        k = a * (fade(t) if fade else 1.0)
        if k <= 0.01:
            return
        x = int(x0 + speed * t) % 1100
        d = tex.crop((x, 0, x + W, H))
        if lift:
            d = d.transform((W, H), Image.AFFINE, (1, 0, 0, 0, 1, lift))
        if k < 0.99:
            d.putalpha(d.getchannel("A").point(lambda v: int(v * k)))
        im.alpha_composite(d)
    return fx


def mounted(S, q, t, x, y, s, cols=GREY_H, gait="stand", seed=0, flip=False, head_down=0.0):
    """a rider on a horse (the horse faces right, flip=True: left); gait stand / walk / gallop"""
    rate = {"stand": 0.0, "walk": 4.2, "gallop": 10.5}[gait]
    ph = t * rate + seed
    hb = -18 * math.sin(ph) if gait == "gallop" else 6 * math.sin(t * 1.1 + seed)
    col, mane, blanket = (cols["col"], cols["mane"], cols["blanket"]) if isinstance(cols, dict) else cols
    return rider(S, q, t, lambda c: horse(c, col=col, mane=mane, walk=gait != "stand", phase=ph, t=t + seed, head_bob=hb, blanket=blanket,
                                          head_down=head_down), x, y, s, flip=flip)


def lance_q(t, seed, side=1, lines=(), level=0.0, **kw):
    """a rider's pose with a lance: side 1 rides to the right; level 0 upright … 1 lowered for the charge"""
    base = dict(turn=0.35, gx=0.8, gy=-0.1, furrow=0.9, brow=-0.1, armR="forward", armL=("ik", 230, 120), wind=1.0)
    base.update(kw)
    q = tp(list(lines), t, seed, **base)
    q["propL"] = ("lance_green" if side > 0 else "lance_red", 40 * level)
    return q


def army_rider(S, t, x, y, s, side, seed, gait="gallop", level=0.5, banner=False, cheer=0.0, cols=None):
    """one rider of a side (1: Nawfal's men, riding right; -1: Leyli's tribe, riding left)"""
    q = P(turn=0.35, gx=0.8, gy=-0.1 - 0.4 * cheer, furrow=1.0 - cheer, brow=-0.1 + 0.6 * cheer, mouth_o=0.35 + 0.25 * math.sin(t * 7 + seed),
          armR="forward", armL=("ik", 230, 120 - 140 * cheer), wind=1.0, blink=blink_at(t, seed))
    lv = level * (0.7 + 0.3 * math.sin(t * 5 + seed))
    q["propL"] = ("banner_green" if side > 0 else "banner_red") if banner else (("lance_green" if side > 0 else "lance_red"), 40 * lv)
    cl = cols or (HORSES_N if side > 0 else HORSES_T)[seed % 4]
    return mounted(S, q, t, x, y, s, cols=cl, gait=gait, seed=seed, flip=side < 0)


def far_battle(t, y0=1120, n=9, s=0.16, spread=(60, 1020), seed=0, fight=True):
    """a line of small riders of both sides meeting in the dust far away: green on the left, red on the right, lances bobbing"""
    r = random.Random(seed)
    o = ""
    xs = sorted(r.uniform(*spread) for _ in range(n))
    for k, x in enumerate(xs):
        side = 1 if x < (spread[0] + spread[1]) / 2 else -1
        S = (NAWFAL_MAN, NAWFAL_MAN_2, NAWFAL_MAN_3)[k % 3] if side > 0 else (TRIBE_MAN, TRIBE_MAN_2, TRIBE_MAN_3)[k % 3]
        dx = (14 * math.sin(t * 2.2 + k) + side * 10 * math.sin(t * 1.3 + k * 2)) if fight else 0.0
        o += army_rider(S, t, x + dx, y0 + r.uniform(-14, 14), s * r.uniform(0.9, 1.1), side, seed * 10 + k, gait="gallop" if fight else "walk",
                        level=0.6, banner=(k % 4 == 1))
    return o


def clash_flash(x, y, t, t0, s=1.0):
    """a short white star where metal meets metal (no blood)"""
    u = (t - t0) / 0.25
    if not 0 <= u <= 1:
        return ""
    r = (20 + 50 * u) * s
    a = 1 - u
    pts = " ".join(f"{x + r * (1 if k % 2 == 0 else 0.3) * math.cos(k * math.pi / 4):.1f},{y + r * (1 if k % 2 == 0 else 0.3) * math.sin(k * math.pi / 4):.1f}"
                   for k in range(8))
    return f'<polygon points="{pts}" fill="#fffbe8" opacity="{0.9 * a:.2f}"/>'


def tear(x, y, t, t0, s=1.0):
    """a tear running down from (x, y) after t0"""
    u = (t - t0) % 2.4 / 2.4 if t > t0 else -1
    if u < 0:
        return ""
    return (f'<path d="M {x:.1f} {y + 70 * u * s:.1f} c {-7 * s:.1f} {12 * s:.1f}, {-7 * s:.1f} {20 * s:.1f}, 0 {22 * s:.1f} c {7 * s:.1f} {-2 * s:.1f}, {7 * s:.1f} {-10 * s:.1f}, 0 {-22 * s:.1f} Z" '
            f'fill="#cfe6ff" opacity="{0.85 * (1 - u):.2f}" stroke="#6a8ab0" stroke-width="1.2"/>')


def seat_shadow(x, y, w):
    return f'<ellipse cx="{x + 60}" cy="{y + 6}" rx="{w}" ry="{w * 0.12:.0f}" fill="#2a1018" opacity="0.25"/>'


def gazelles(t, pos, startle=None, c=None):
    """gazelles on the dune: pos = [(x, y, scale, look)]; startle: (t0) the heads come up and the ears twitch"""
    c = c or Ctx(lw_for(1.0))
    o = ""
    for k, (x, y, s, look) in reversed(list(enumerate(pos))):
        g = ease((t - startle) / 0.4) if startle is not None else 0.0
        graze = (0.6 if k == 0 else 0.25) * (1 - g) * (0.6 + 0.4 * math.sin(t * 0.5 + k))
        o += (f'<g transform="translate({x},{y}) scale({s})">'
              f'{gazelle(c, t=t + k * 1.3, seed=k, look=look if g < 0.5 else -0.4, ear=1.0 if 0.2 < g < 0.9 else 0.0, graze=graze)}</g>')
    return o


# ================================================================ S1 the hook (0-7.6): the demand before Leyli's tribe; "Never!"; the charge
def nawfal_demand(dur, lines, seed, fade_in=0.0, blur=0):
    pt = bg("plain_day_tents", lambda: lbg.plain("day", tents=True), blur)
    cam = cam_push(1.0, 1.05, 520, 900, dur)
    men = [(NAWFAL_MAN_2, 110, 1250, 0.58, 1, True), (NAWFAL_MAN, 250, 1230, 0.54, 2, False), (NAWFAL_MAN_3, 40, 1270, 0.62, 3, False)]
    shout = [l[1] for l in lines]

    def mid(t):
        o = ""
        for S, x, y, s, k, ban in men:
            o += army_rider(S, t, x, y, s, 1, k, gait="stand", level=0.0, banner=ban)
        loud = any(0.0 < t - st < 3.0 for st in shout)
        q = lance_q(t, seed, 1, lines, level=0.0, furrow=1.3 if loud else 0.8, brow=-0.3 if loud else 0.1, gy=-0.05,
                    armR="fist_up" if any(1.6 < t - st < 3.0 for st in shout) else "forward")
        o += mounted(NAWFAL, q, t, 470, 1640, 1.5, gait="stand", seed=seed)
        return o
    return Shot(dur, pt, mid, cam=cam, light=DAYL, sun=SUN_DAY, bloom=0.5, fade_in=fade_in,
                fx=[dust_fx(0.45, 60, 300, lift=180), Motes(30, 300 + seed, (255, 236, 200), (0, 300, W, 1500), (20, -6), amax=80)])


def father_never(dur, lines, seed, extra=()):
    ltb = bg("leyli_tent_day", lambda: lbg.leyli_tent("day"), 6)
    cam = cam_push(1.0, 1.06, 540, 880, dur)
    t_never = lines[0][1]

    def mid(t):
        hard = ease((t - t_never + 0.1) / 0.2)
        q = tp(list(lines) + list(extra), t, seed, turn=-0.3, gx=-0.7, gy=0.0, furrow=0.6 + 0.8 * hard, brow=0.1 - 0.4 * hard,
               armL="relaxed", armR="point" if t > t_never + 0.1 else "relaxed", wind=0.4)
        return at_neck(LEYLI_FATHER, q, t, 540, 960, 1.0)
    return Shot(dur, ltb, mid, cam=cam, light=DAYL, sun=SUN_DAY)


def charge(dur, seed, n_front=4, fade_out=0.0, fade_in=0.0, pal="day", x_speed=520.0, cheer_t=None):
    """Nawfal's riders gallop to the right across the plain, in dust"""
    pl = bg(f"plain_{pal}", lambda: lbg.plain(pal))
    r = random.Random(seed)
    rows = []
    for k in range(n_front + 3):
        far = k >= n_front
        y = r.uniform(1170, 1200) if far else r.uniform(1260, 1330)
        s = r.uniform(0.3, 0.36) if far else r.uniform(0.5, 0.6)
        rows.append(((NAWFAL_MAN, NAWFAL_MAN_2, NAWFAL_MAN_3)[k % 3], -200 - k * 260 + r.uniform(-60, 60), y, s, k))
    rows.sort(key=lambda e: e[2])
    cam = shaky(cam_push(1.0, 1.04, 540, 1000, dur), 4.0, 15.0)

    def mid(t):
        o = ""
        for S, x0, y, s, k in rows:
            o += army_rider(S, t, x0 + x_speed * (t + 0.6) + (k % 2) * 40, y, s, 1, seed + k, level=0.8, banner=(k % 3 == 1))
        q = lance_q(t, seed, 1, (), level=0.9, mouth_o=0.6, furrow=1.3)
        o += mounted(NAWFAL, q, t, -260 + (x_speed * 0.9) * (t + 0.3), 1420, 0.78, gait="gallop", seed=seed)
        return o
    return Shot(dur, pl, mid, cam=cam, light=DAYL, sun=SUN_DAY, bloom=0.5, fade_out=fade_out, fade_in=fade_in,
                pre_fx=[dust_fx(0.5, 160, 500, lift=260)], fx=[dust_fx(0.55, 260, 100, lift=120)])


def s1():
    A = nawfal_demand(3.8, L(0.0, "p3s1a"), 1, fade_in=0.3)
    B = father_never(1.4, L(3.8, "p3s1b"), 2)
    C = charge(2.4, 10, fade_out=0.4)
    return [A, B, C]


# ================================================================ S2 title (7.6-12.2): Nawfal's riders on the dune at sunrise
def s2():
    dn = bg("dunes_dawn", lambda: lbg.dunes("dawn"))
    riders_ = [(NAWFAL, 0.5, 1450, 0), (NAWFAL_MAN, 0.44, 1380, 1), (NAWFAL_MAN_2, 0.46, 1420, 2), (NAWFAL_MAN_3, 0.42, 1350, 3)]

    def mid(t):
        o = birds(t, 900, 520, n=4, s=0.8)
        for S, s, y, k in sorted(riders_, key=lambda e: e[2]):
            x = 80 + 260 * k + 34 * t
            if S is NAWFAL:
                q = lance_q(t, 21, 1, (), level=0.0, furrow=0.6, brow=0.1, gx=0.6, gy=-0.2, wind=0.8)
                o += mounted(NAWFAL, q, t, x, y, s, gait="walk", seed=21)
            else:
                o += army_rider(S, t, x, y, s, 1, 22 + k, gait="walk", level=0.0, banner=(k == 2))
        return o
    return [Shot(4.6, dn, mid, cam=cam_push(1.0, 1.04, 540, 1100, 4.6), sun=SUN_DAWN, light=DAWNL, bloom=0.7, fade_in=0.4, fade_out=0.5,
                 fx=[Motes(30, 201, (255, 230, 210), (0, 1000, W, 1600), (-8, -4), amax=70)])]


# ================================================================ S3 Nawfal finds Majnun; the promise (12.2-47.0)
GZ = [(600, 1262, 1.0, 0.0), (790, 1232, 0.86, 0.6)]


def majnun_sit_q(t, seed, look=0.3, **kw):
    base = dict(legs="sit", turn=0.3, gx=look, gy=0.2, sad=0.4, brow=0.4, furrow=-0.2, armL=("ik", 260, 330), armR="relaxed", wind=0.5,
                blink=blink_at(t, seed), breathe=math.sin(t * 1.4))
    base.update(kw)
    return P(**base)


def s3():
    dd = bg("dunes_day", lambda: lbg.dunes("day"))
    ddb = bg("dunes_day", lambda: lbg.dunes("day"), 6)

    # A1: Majnun among the gazelles (narration: his father warned him; he went deeper into the desert)
    camA1 = cam_push(1.0, 1.05, 520, 1050, 6.4)

    def midA1(t):
        o = gazelles(t, GZ)
        o += seat_shadow(330, 1222, 170)
        o += seated(MAJNUN, majnun_sit_q(t, 1, look=0.5, gy=0.3), t, 330, 1222, 0.62)
        return birds(t, 980, 460, n=4, s=0.8) + o
    A1 = Shot(6.4, dd, midA1, cam=camA1, light=DAYL, sun=SUN_DAY, bloom=0.5, fade_in=0.4,
              fx=[SandWind(140, 311, (0, 1000, W, 1900), (500, 900), strength=lambda t: 0.35)])

    # A2: Nawfal and his men ride over the dune from the right, a falcon on his fist
    camA2 = cam_push(1.02, 1.0, 560, 1050, 4.6)
    arrive = 3.4

    def midA2(t):
        u = ease(t / arrive)
        o = gazelles(t, GZ, startle=1.2)
        look = 0.5 + 0.4 * ease((t - 1.0) / 0.6)
        o += seat_shadow(330, 1222, 170)
        o += seated(MAJNUN, majnun_sit_q(t, 2, look=look, gy=0.1, sad=0.3), t, 330, 1222, 0.62)
        walking = t < arrive
        man = P(turn=0.35, gx=0.8, gy=0.0, furrow=0.4, armR="forward", armL=("ik", 230, 120), propL="spear_green", wind=0.6, blink=blink_at(t, 32))
        o += mounted(WARRIOR, man, t, lerp(1380, 1060, u), 1205, 0.52, cols=HORSES_N[0], gait="walk" if walking else "stand", seed=32, flip=True)
        nq = P(turn=0.35, gx=0.8, gy=0.1, furrow=0.3, brow=0.3, armR="forward", armL=("ik", 250, 300), propL="falcon", wind=0.6, blink=blink_at(t, 31))
        o += mounted(NAWFAL, nq, t, lerp(1260, 900, u), 1240, 0.6, gait="walk" if walking else "stand", seed=31, flip=True)
        return o
    A2 = Shot(4.6, dd, midA2, cam=camA2, light=DAYL, sun=SUN_DAY, bloom=0.5,
              fx=[SandWind(140, 312, (0, 1000, W, 1900), (500, 900), strength=lambda t: 0.3)])

    # B: Nawfal on his horse: "Who is that thin man, sitting with the gazelles?"
    LB = L(23.2, "p3s3c")
    camB = cam_push(1.0, 1.05, 560, 820, 3.0)

    def midB(t):
        q = tp(LB, t, 33, turn=0.35, gx=0.8, gy=0.3, furrow=0.2, brow=0.5, armR="forward", armL=("ik", 220, 80), wind=0.6)
        q["propL"] = "falcon"
        return mounted(NAWFAL, q, t, 600, 1580, 1.3, seed=33, flip=True)
    B = Shot(3.0, ddb, midB, cam=camB, light=DAYL, sun=SUN_DAY)

    # C: his man: "That is Majnun, my chief. He is mad with love for a girl called Leyli."
    LC = L(26.2, "p3s3d")
    camC = cam_push(1.0, 1.05, 540, 820, 4.4)

    def midC(t):
        q = tp(LC, t, 34, turn=0.35, gx=0.6, gy=0.2, furrow=0.1, brow=0.4, smile=0.1, armL="point" if 0.8 < t < 2.6 else "forward",
               armR=("ik", -230, 120), wind=0.6)
        q["propR"] = "spear_green"
        return mounted(WARRIOR, q, t, 560, 1580, 1.3, cols=HORSES_N[0], seed=34, flip=True)
    C = Shot(4.4, ddb, midC, cam=camC, light=DAYL, sun=SUN_DAY)

    # D: Nawfal sits by Majnun: "Tell me your story, friend." — "I love Leyli… but her father will never give her to me."
    LDn = L(30.6, "p3s3e")
    LDm = L(30.6, "p3s3f")
    camD = cam_push(1.0, 1.05, 540, 1000, 6.6)

    def midD(t):
        c = Ctx(lw_for(0.5))
        o = f'<g transform="translate(980,1170) scale(-0.5,0.5)">{horse(c, t=t, col=GREY_H["col"], mane=GREY_H["mane"], blanket=GREY_H["blanket"], head_down=0.7 + 0.2 * math.sin(t * 0.7))}</g>'
        o += gazelles(t, [(140, 1250, 0.8, 0.4)])
        o += seat_shadow(270, 1250, 160) + seat_shadow(740, 1250, 170)
        m = tp(LDm, t, 35, legs="sit", turn=0.35, gx=0.7, gy=0.2, sad=0.6, brow=0.7, furrow=-0.3, armL=("ik", 60, 330),
               armR="chest" if t > 3.2 else "relaxed", wind=0.5)
        o += seated(MAJNUN, m, t, 270, 1250, 0.7)
        n = tp(LDn, t, 36, legs="sit", turn=-0.35, gx=-0.8, gy=0.2, brow=0.5, furrow=-0.1, smile=0.2, armL=("ik", 60, 330),
               armR="offer" if 0.3 < t < 2.4 else ("ik", -60, 330), wind=0.4, cloak_len=0.55)
        o += seated(NAWFAL, n, t, 740, 1250, 0.72)
        return o
    D = Shot(6.6, dd, midD, cam=camD, light=DAYL, sun=SUN_DAY, bloom=0.5)

    # E: Nawfal close: "Then I will help you. I swear it: Leyli will be yours!" — "But you must eat, and rest… and wait for me."
    LE = L(37.2, "p3s3g", "p3s3h")
    camE = cam_push(1.0, 1.06, 540, 860, 6.5)

    def midE(t):
        sw = 1.2 < t < 3.4
        gentle = ease((t - 3.6) / 0.6)
        q = tp(LE, t, 37, turn=-0.25, gx=-0.6, gy=0.05, furrow=0.7 * (1 - gentle), brow=0.2 + 0.3 * gentle, smile=0.35 * gentle,
               armL="relaxed", armR="fist_up" if sw else ("offer" if t > 4.0 else "chest"), openR=t > 4.0, wind=0.4)
        return at_neck(NAWFAL, q, t, 540, 960, 1.0)
    E = Shot(6.5, ddb, midE, cam=camE, light=DAYL, sun=SUN_DAY)

    # F: Majnun close: "For Leyli… I will wait." (a first smile)
    LF = L(43.7, "p3s3i")
    camF = cam_push(1.0, 1.05, 540, 880, 3.3)

    def midF(t):
        q = tp(LF, t, 38, turn=0.25, gx=0.6, gy=0.1, sad=0.5 - 0.3 * ease((t - 1.6) / 0.8), brow=0.7, furrow=-0.4,
               smile=0.45 * ease((t - 1.4) / 0.8), armL="relaxed", armR="chest", wind=0.6)
        return at_neck(MAJNUN, q, t, 540, 1000, 1.05)
    F = Shot(3.3, ddb, midF, cam=camF, light=DAYL, sun=SUN_DAY, fade_out=0.5,
             fx=[SandWind(100, 313, (0, 300, W, 1900), (500, 900), strength=lambda t: 0.3)])
    return [A1, A2, B, C, D, E, F]


# ================================================================ S4 the demand; "Never!"; the first battle; Majnun on the dune (47.0-68.6)
def battle_shot(dur, seed, pal="day", big=True, cam=None, fade_in=0.0, fade_out=0.0, meet=1.4, bigger=False, sun=SUN_DAY, light=DUSTL):
    """the two sides meet in the middle of the plain: green from the left, red from the right. A far line of small riders with lances and
    banners on the horizon, two riders a side in the middle, and in front Nawfal and a rider of Leyli's tribe who meet with crossed lances
    (a flash of metal); dust behind them and low in front, so the faces stay clear. Nobody is hurt."""
    pl = bg(f"plain_{pal}", lambda: lbg.plain(pal))
    r = random.Random(seed)
    nback = 14 if bigger else 10
    back = []
    for k in range(nback):
        side = 1 if (k % 2 == 0 or (bigger and k % 3 == 2)) else -1
        S = (NAWFAL_MAN, NAWFAL_MAN_2, NAWFAL_MAN_3)[k % 3] if side > 0 else (TRIBE_MAN, TRIBE_MAN_2, TRIBE_MAN_3)[k % 3]
        back.append((S, side, r.uniform(-40, 470) if side > 0 else r.uniform(610, 1120), r.uniform(1112, 1138), r.uniform(0.2, 0.24), k))
    back.sort(key=lambda e: e[3])
    mid_ = [(NAWFAL_MAN_2, 1, 150, 1232, 0.42, 20), (NAWFAL_MAN_3, 1, -70, 1252, 0.44, 21),
            (TRIBE_MAN, -1, 930, 1236, 0.42, 22), (TRIBE_MAN_3, -1, 1150, 1256, 0.44, 23)]
    if bigger:
        mid_ += [(NAWFAL_MAN, 1, 330, 1244, 0.43, 24), (NAWFAL_MAN_2, 1, -250, 1240, 0.42, 25)]
    mid_.sort(key=lambda e: e[3])
    flashes = [(r.uniform(meet + 0.05, dur - 0.3), 540 + r.uniform(-70, 70), r.uniform(780, 900)) for _ in range(int((dur - meet) * 2.0))]
    flashes.append((meet, 540, 840))
    cam = cam or shaky(cam_push(1.0, 1.05, 540, 1000, dur), 4.0, 14.0)

    def mid(t):
        o = ""
        u = ease(t / meet)
        for S, side, x0, y, s, k in back:
            xx = x0 + side * 120 * u + 16 * math.sin(t * 2.3 + k)
            o += army_rider(S, t, xx, y, s, side, seed + k, level=0.7, banner=(k % 4 == 1))
        for S, side, x0, y, s, k in mid_:
            xx = lerp(x0 - side * 260, x0, u) + side * 14 * math.sin(t * 3 + k)
            o += army_rider(S, t, xx, y, s, side, seed + k, level=0.9 if t > meet else 0.6, banner=(k == 21))
        if big:
            clash = t > meet
            wob = 12 * math.sin(t * 6) if clash else 0.0
            rear_n = -13 * max(0.0, math.sin((t - meet) * 2.6)) if clash else 0.0
            rear_e = 13 * max(0.0, math.sin((t - meet) * 2.6 + 2.2)) if clash else 0.0
            xn, xe = lerp(-380, 250, u) + wob, lerp(1460, 830, u) - wob
            nq = lance_q(t, seed + 40, 1, (), level=0.9 + (0.15 * math.sin(t * 6) if clash else 0.0), mouth_o=0.55, furrow=1.3)
            o += (f'<g transform="rotate({rear_n:.2f},{xn - 150 * 0.9:.1f},1430)">' +
                  mounted(NAWFAL, nq, t, xn, 1430, 0.9, gait="gallop" if not clash else "walk", seed=seed + 40) + '</g>')
            eq = lance_q(t, seed + 41, -1, (), level=0.9 + (0.15 * math.sin(t * 6 + 1.5) if clash else 0.0), mouth_o=0.55, furrow=1.3)
            o += (f'<g transform="rotate({rear_e:.2f},{xe + 150 * 0.88:.1f},1440)">' +
                  mounted(TRIBE_MAN_2, eq, t, xe, 1440, 0.88, cols=HORSES_T[0], gait="gallop" if not clash else "walk", seed=seed + 41,
                          flip=True) + '</g>')
        for (tf, xf, yf) in flashes:
            o += clash_flash(xf, yf, t, tf, 0.9)
        return o
    return Shot(dur, pl, mid, cam=cam, light=light, sun=sun, bloom=0.5, fade_in=fade_in, fade_out=fade_out,
                pre_fx=[dust_fx(0.55, 90, 300, lift=330), dust_fx(0.3, -60, 800, lift=520)], fx=[dust_fx(0.55, 200, 700, lift=-180)])


def s4():
    # A: the army rides to Leyli's tribe (caption)
    pt = bg("plain_day_tents", lambda: lbg.plain("day", tents=True))
    r = random.Random(401)
    col_ = [((NAWFAL_MAN, NAWFAL_MAN_2, NAWFAL_MAN_3)[k % 3], -150 - 210 * k + r.uniform(-40, 40), 1200 if k % 2 else 1300,
             0.42 if k % 2 else 0.6, k) for k in range(7)]
    camA = shaky(cam_push(1.0, 1.04, 540, 1000, 4.0), 3.0, 15.0)

    def midA(t):
        o = ""
        for S, x0, y, s, k in sorted(col_, key=lambda e: e[2]):
            o += army_rider(S, t, x0 + 330 * t, y, s, 1, 410 + k, level=0.2, banner=(k % 3 == 1))
        q = lance_q(t, 420, 1, (), level=0.0, furrow=0.9)
        o += mounted(NAWFAL, q, t, 120 + 330 * t, 1310, 0.62, gait="gallop", seed=420)
        return o
    A = Shot(4.0, pt, midA, cam=camA, light=DAYL, sun=SUN_DAY, bloom=0.5, fade_in=0.3,
             pre_fx=[dust_fx(0.4, 200, 600, lift=300)], fx=[dust_fx(0.45, 300, 200, lift=-160)])
    B = nawfal_demand(3.4, L(51.0, "p3s1a"), 402, blur=6)
    C = father_never(3.8, L(54.4, "p3s1b"), 403, extra=L(54.4, "p3s4b"))
    D = battle_shot(6.4, 404, fade_in=0.0)

    # E: Majnun on a high dune; the battle far away
    dd = bg("dunes_day", lambda: lbg.dunes("day"))
    camE = cam_push(1.0, 1.06, 520, 1000, 4.0)

    def midE(t):
        o = far_battle(t, 1000, n=10, s=0.09, seed=41)
        o += seat_shadow(300, 1222, 170)
        pray = ease((t - 2.0) / 1.0)
        hx, hy = 290 - 100 * pray + 40 * math.sin(math.pi * pray), lerp(150, -330, pray)      # open hands rise along an arc into prayer
        q = majnun_sit_q(t, 42, look=0.7 - 0.5 * pray, gy=-0.1 - 0.3 * pray, sad=0.5 + 0.2 * pray,
                         armL=("ik", hx, hy, "down"), armR=("ik", -hx, hy, "down"), openL=True, openR=True)
        if pray > 0.6:
            q["blink"] = max(q["blink"], 0.9)
        o += seated(MAJNUN, q, t, 300, 1222, 0.62)
        return o
    E = Shot(4.0, dd, midE, cam=camE, light=DAYL, sun=SUN_DAY, bloom=0.5,
             pre_fx=[dust_fx(0.55, 70, 400, lift=820)], fx=[SandWind(120, 411, (0, 1000, W, 1900), (500, 900), strength=lambda t: 0.3)])
    return [A, B, C, D, E]


# ================================================================ S5 the prayer; the warrior; no winner; the bigger army; victory (68.6-92.6)
def s5():
    ddb = bg("dunes_day", lambda: lbg.dunes("day"), 6)
    far_dust = [dust_fx(0.5, 60, 400, lift=760)]
    # A: Majnun prays for Leyli's people
    LA = L(68.6, "p3s5a")
    camA = cam_push(1.0, 1.06, 540, 860, 5.2)

    def midA(t):
        return at_neck(MAJNUN, praying(t, LA, 51, close=True, sad=0.7), t, 540, 1000, 1.05)
    A = Shot(5.2, ddb, midA, cam=camA, light=DAYL, sun=SUN_DAY, pre_fx=far_dust, fade_in=0.3)

    # B: the warrior below the dune: "Majnun! We fight for you… and you pray for them?"
    plb = bg("plain_day", lambda: lbg.plain("day"), 6)
    LB = L(73.8, "p3s5b")
    camB = cam_push(1.0, 1.05, 540, 860, 3.5)

    def midB(t):
        q = tp(LB, t, 52, turn=-0.25, gx=-0.6, gy=-0.6, furrow=1.2, brow=-0.1, armL=("ik", 230, 120), armR="point" if 0.4 < t < 2.6 else "relaxed",
               wind=0.8)
        q["propL"] = "spear_green"
        return at_neck(WARRIOR, q, t, 540, 960, 1.0)
    B = Shot(3.5, plb, midB, cam=camB, light=DUSTL, sun=SUN_DAY, pre_fx=[dust_fx(0.5, 120, 200, lift=500)],
             fx=[Motes(40, 521, (230, 210, 170), (0, 300, W, 1500), (40, -6), amax=90)])

    # C: Majnun: "They are Leyli's people. If they are hurt… my heart is hurt."
    LC = L(77.3, "p3s5c")
    camC = cam_push(1.0, 1.07, 540, 860, 5.1)

    def midC(t):
        q = tp(LC, t, 53, turn=0.25, gx=0.5, gy=0.3, sad=0.8, brow=0.9, furrow=-0.5, armL="relaxed", armR="chest" if t > 1.8 else "relaxed",
               wind=0.6)
        o = at_neck(MAJNUN, q, t, 540, 1000, 1.05)
        ex, ey = 540 + (-40 + 3) * 1.05, 1000 - 178 * 1.05
        return o + tear(ex, ey + 22, t, 2.6, 1.05)
    C = Shot(5.1, ddb, midC, cam=camC, light=DAYL, sun=SUN_DAY, pre_fx=far_dust)

    # D: dusk: the two sides ride apart; nobody won
    pld = bg("plain_dusk", lambda: lbg.plain("dusk"))
    camD = cam_push(1.0, 1.03, 540, 1000, 3.0)

    def midD(t):
        o = ""
        for k in range(5):
            side = 1 if k % 2 == 0 else -1
            S = (NAWFAL_MAN, TRIBE_MAN, NAWFAL_MAN_2, TRIBE_MAN_2, NAWFAL_MAN_3)[k]
            x = (480 - 120 * k - 60 * t) if side > 0 else (600 + 110 * k + 60 * t)
            q = P(turn=-0.35, gx=-0.6, gy=0.3, sad=0.4, furrow=0.3, armR="forward", armL=("ik", 230, 120), wind=0.6, blink=blink_at(t, 540 + k))
            q["propL"] = ("lance_green" if side > 0 else "lance_red", 0)
            # each side rides home: Nawfal's men to the left, Leyli's tribe to the right
            o += mounted(S, q, t, x, 1190 + 30 * (k % 2), 0.34, cols=(HORSES_N if side > 0 else HORSES_T)[k % 4], gait="walk", seed=540 + k,
                         flip=side > 0)
        return o
    D = Shot(3.0, pld, midD, cam=camD, light=DUSKL, sun=SUN_DUSK, bloom=0.6, fade_in=0.3,
             pre_fx=[dust_fx(0.35, 30, 600, lift=300)])

    # E1: dawn: the bigger army charges
    E1 = battle_shot(3.6, 550, pal="dawn", bigger=True, meet=1.6, sun=SUN_DAWN, light=dict(DAWNL, ambient=(0.96, 0.9, 0.9)), fade_in=0.2)

    # E2: victory: Nawfal raises his lance; his men cheer; far away by the tents, Leyli's tribe lower their banners
    pt = bg("plain_day_tents", lambda: lbg.plain("day", tents=True))
    camE2 = cam_push(1.0, 1.05, 520, 900, 3.6)

    def midE2(t):
        o = ""
        up = ease((t - 0.3) / 0.6)
        for k in range(4):
            q = P(turn=-0.3, gx=-0.5, gy=0.6, sad=0.6, furrow=0.2, armL=(20, 10), armR="relaxed", blink=blink_at(t, 560 + k), wind=0.5)
            q["propL"] = ("banner_red", 120 + 8 * k) if k % 2 == 0 else ("spear_red", 150)
            o += at_feet((TRIBE_MAN, TRIBE_MAN_2, TRIBE_MAN_3, TRIBE_MAN)[k], q, t, 700 + 95 * k, 1100 + 6 * k, 0.12)
        for k, (S, x, y, s) in enumerate(((NAWFAL_MAN_3, 40, 1270, 0.62), (NAWFAL_MAN_2, 110, 1250, 0.58), (NAWFAL_MAN, 250, 1230, 0.54))):
            o += army_rider(S, t, x, y, s, 1, 570 + k, gait="stand", level=0.0, banner=(k == 1), cheer=up * (0.6 + 0.4 * math.sin(t * 6 + k)))
        q = lance_q(t, 575, 1, (), level=0.0, furrow=0.2, brow=0.5, smile=0.6 * up, mouth_o=0.5 * up, gy=-0.3,
                    armL=("ik", 260, lerp(120, -120, up), "down"), armR="fist_up" if up > 0.5 else "forward")
        o += mounted(NAWFAL, q, t, 470, 1640, 1.5, seed=575)
        return o
    E2 = Shot(3.6, pt, midE2, cam=camE2, light=DAYL, sun=SUN_DAY, bloom=0.6, fade_out=0.4,
              fx=[dust_fx(0.3, 60, 900, lift=-150), Motes(40, 576, (255, 236, 200), (0, 300, W, 1500), (20, -10), amax=90)])
    return [A, B, C, D, E1, E2]


# ================================================================ S6 Leyli's father in the dust; Nawfal gives up; Majnun walks away (92.6-122.0)
def dust_head(x, y, s, t, seed=0):
    """dust falling from an old man's head cloth"""
    r = random.Random(seed)
    o = ""
    for k in range(14):
        ph = (t * 0.7 + r.random()) % 1.0
        xx = x + r.uniform(-120, 120) * s + 10 * math.sin(t * 2 + k)
        yy = y + ph * 260 * s
        o += f'<circle cx="{xx:.1f}" cy="{yy:.1f}" r="{r.uniform(1.5, 3.5) * s:.1f}" fill="#d8c0a0" opacity="{0.7 * (1 - ph):.2f}"/>'
    return o


def s6():
    pt = bg("plain_day_tents", lambda: lbg.plain("day", tents=True))
    ptb = bg("plain_day_tents", lambda: lbg.plain("day", tents=True), 6)
    wind = SandWind(160, 601, (0, 900, W, 1900), (500, 900), strength=lambda t: 0.45)

    # A: the old man walks to Nawfal through the dust
    camA = cam_push(1.0, 1.04, 560, 1000, 4.0)

    def midA(t):
        c = Ctx(lw_for(0.42))
        o = f'<g transform="translate(150,1250) scale(0.42)">{horse(c, t=t, col=GREY_H["col"], mane=GREY_H["mane"], blanket=GREY_H["blanket"], head_down=0.5)}</g>'
        for k, (S, x, y, s) in enumerate(((NAWFAL_MAN, 40, 1235, 0.4), (NAWFAL_MAN_3, 610, 1225, 0.38))):
            q = P(turn=0.3, gx=0.7, gy=0.1, furrow=0.4, armL=(20, 10), armR="relaxed", blink=blink_at(t, 610 + k), wind=0.6)
            q["propL"] = "pike"
            o += at_feet(S, q, t, x, y, s)
        m = P(turn=0.3, gx=0.7, gy=0.1, sad=0.3, brow=0.6, furrow=-0.2, armL="relaxed", armR="chest", wind=1.0, blink=blink_at(t, 612),
              breathe=math.sin(t * 2))
        o += at_feet(MAJNUN, m, t, 230, 1330, 0.44)
        n = P(turn=0.35, gx=0.8, gy=0.1, furrow=0.6, armL="hip", armR="relaxed", wind=0.6, blink=blink_at(t, 613), breathe=math.sin(t * 1.5))
        o += at_feet(NAWFAL, n, t, 420, 1340, 0.47)
        u = ease(t / 3.6)
        walking = t < 3.6
        f = P(legs="walk" if walking else "stand", phase=t * 3.0, turn=-0.35, gx=-0.6, gy=0.6, sad=0.8, brow=0.8, furrow=-0.3,
              armL="relaxed", armR="relaxed", wind=0.8, blink=blink_at(t, 614), breathe=math.sin(t * 2))
        fx_, fy_ = lerp(1180, 770, u), 1345
        o += at_feet(LEYLI_FATHER_DUST, f, t, fx_, fy_, 0.46) + dust_head(fx_, fy_ - 640, 0.46, t, 615)
        return o
    A = Shot(4.0, pt, midA, cam=camA, light=DUSTL, sun=SUN_DAY, bloom=0.5, fade_in=0.4, fx=[wind, dust_fx(0.3, 50, 300, lift=300)])

    # B: "You have won, Nawfal. I am an old man… and my tribe is beaten."
    LB = L(96.6, "p3s6a")
    camB = cam_push(1.0, 1.05, 540, 860, 5.2)

    def midB(t):
        q = tp(LB, t, 62, turn=-0.25, gx=-0.4, gy=0.6 - 0.6 * ease((t - 0.6) / 0.6), sad=0.8, brow=0.8, furrow=-0.4, armL="relaxed",
               armR="chest" if t > 2.2 else "relaxed", wind=0.6)
        return at_neck(LEYLI_FATHER_DUST, q, t, 540, 960, 1.0) + dust_head(540, 700, 1.0, t, 621)
    B = Shot(5.2, ptb, midB, cam=camB, light=DUSTL, sun=SUN_DAY, fx=[wind])

    # C: "Kill her if you want… but I will never give my daughter to a madman."
    LC = L(101.8, "p3s6b")
    camC = cam_push(1.02, 1.12, 540, 860, 6.4)

    def midC(t):
        hard = ease((t - 2.6) / 0.6)
        q = tp(LC, t, 63, turn=-0.2, gx=-0.5, gy=0.0, sad=0.6 * (1 - hard), brow=0.6 - 0.9 * hard, furrow=0.2 + 1.1 * hard,
               armL="relaxed", armR="point" if 2.8 < t < 5.0 else "relaxed", wind=0.6)
        return at_neck(LEYLI_FATHER_DUST, q, t, 540, 960, 1.0) + dust_head(540, 700, 1.0, t, 631)
    C = Shot(6.4, ptb, midC, cam=camC, light=DUSTL, sun=SUN_DAY, fx=[wind])

    # D: Nawfal: "Go home, old man. I will not take a daughter from her father by force."
    LD = L(108.2, "p3s6c")
    camD = cam_push(1.0, 1.06, 540, 860, 5.2)

    def midD(t):
        q = tp(LD, t, 64, turn=0.25, gx=0.6, gy=0.3 - 0.3 * ease((t - 0.6) / 0.5), sad=0.5, brow=0.6, furrow=-0.1,
               armL="relaxed", armR="offer" if 1.2 < t < 3.2 else "relaxed", openR=True, wind=0.5)
        return at_neck(NAWFAL, q, t, 540, 960, 1.0)
    D = Shot(5.2, ptb, midD, cam=camD, light=DUSTL, sun=SUN_DAY, fx=[wind])

    # E: Majnun and Nawfal: "Nawfal… you promised me!" — "Forgive me, my friend."
    LEm = L(113.4, "p3s6d")
    LEn = L(113.4, "p3s6e")
    camE = cam_push(1.0, 1.04, 540, 900, 4.2)

    def midE(t):
        m = tp(LEm, t, 65, turn=0.35, gx=0.8, gy=-0.1, sad=0.9, brow=1.0, furrow=-0.5, armR="relaxed", armL="reach" if 0.2 < t < 2.4 else "relaxed",
               openL=True, wind=0.9)
        n = tp(LEn, t, 66, turn=-0.35, gx=-0.8 if t < 2.4 else -0.4, gy=0.1 if t < 2.4 else 0.6, sad=0.6, brow=0.7, furrow=-0.3, armL="relaxed",
               armR="chest" if t > 2.5 else "relaxed", wind=0.5)
        return at_feet(MAJNUN, m, t, 330, 1720, 0.7) + at_feet(NAWFAL, n, t, 760, 1730, 0.72)
    E = Shot(4.2, ptb, midE, cam=camE, light=DUSTL, sun=SUN_DAY, fx=[wind])

    # F: Majnun walks away into the dunes at dusk
    dn = bg("dunes_dusk", lambda: lbg.dunes("dusk"))
    camF = cam_push(1.04, 1.0, 480, 1100, 4.4)

    def midF(t):
        u = ease(t / 4.4)
        x = lerp(700, 470, u); y = lerp(1520, 1250, u); s = lerp(0.56, 0.3, u)
        q = P(legs="walk", phase=t * 5.0, turn=-0.45, gx=-0.9, gy=0.3, sad=0.7, brow=0.8, armL="relaxed", armR="relaxed", wind=1.4,
              blink=blink_at(t, 67), breathe=math.sin(t * 3))
        sh = f'<g transform="translate({x:.1f},{y:.1f}) scale({s:.4f})"><path d="M -60 0 L 760 160 L 820 90 L 40 -20 Z" fill="#3a1830" opacity="0.28"/></g>'
        return sh + at_feet(MAJNUN, q, t, x, y, s)
    F = Shot(4.4, dn, midF, cam=camF, light=DUSKL, sun=SUN_DUSK, bloom=0.7, fade_out=0.6,
             fx=[SandWind(200, 602, (0, 1000, W, 1900), (600, 1000), strength=lambda t: 0.6)])
    return [A, B, C, D, E, F]


# ================================================================ S7 Ibn Salam; "Then Leyli is yours"; Leyli in her tent (122.0-145.0)
def s7():
    lt = bg("leyli_tent_dusk", lambda: lbg.leyli_tent("dusk"))
    ltb = bg("leyli_tent_dusk", lambda: lbg.leyli_tent("dusk"), 6)
    camA = cam_push(1.0, 1.05, 560, 1050, 6.2)

    def midA(t):
        c = Ctx(lw_for(0.5))
        o = f'<g transform="translate(250,1470) scale(0.5)">{camel(c, t=t, saddle=True, blanket="#22407a")}</g>'
        o += gifts(560, 1560, 0.7)
        for k, (S, x, y) in enumerate(((SERVANT_A, 470, 1470), (SERVANT_B, 660, 1460))):
            set_down = ease((t - 1.0 - 0.6 * k) / 0.8)
            q = P(turn=0.2 if k == 0 else -0.2, gx=0.4 if k == 0 else -0.4, gy=0.4, brow=0.2, armL="chest" if set_down < 0.5 else "relaxed",
                  armR="chest" if set_down < 0.5 else "relaxed", blink=blink_at(t, 70 + k), breathe=math.sin(t * 2 + k), wind=0.4)
            o += at_feet(S, q, t, x, y, 0.42)
        u = ease(t / 2.6)
        iq = P(legs="walk" if t < 2.6 else "stand", phase=t * 4.0, turn=0.35, gx=0.7, gy=0.0, brow=0.3, smile=0.3, armL="relaxed",
               armR="relaxed" if t < 3.2 else "chest", wind=0.4, blink=blink_at(t, 72), breathe=math.sin(t * 1.7))
        o += at_feet(IBN_SALAM, iq, t, lerp(100, 320, u), 1600, 0.56)
        fq = P(turn=-0.35, gx=-0.7, gy=0.1, furrow=0.3, brow=0.2, smile=0.2 * ease((t - 3.0) / 1.0), armL="relaxed", armR="relaxed", wind=0.5,
               blink=blink_at(t, 73), breathe=math.sin(t * 1.5))
        o += at_feet(LEYLI_FATHER, fq, t, 860, 1590, 0.58)
        return o
    A = Shot(6.2, lt, midA, cam=camA, light=DUSKL, sun=SUN_DUSK, bloom=0.6, fade_in=0.4)

    LB = L(128.2, "p3s7b")
    camB = cam_push(1.0, 1.05, 540, 860, 4.3)

    def midB(t):
        q = tp(LB, t, 74, turn=0.25, gx=0.6, gy=0.1, brow=0.4, furrow=-0.1, smile=0.35, armL="relaxed", armR="chest" if t < 2.0 else "offer",
               openR=t >= 2.0, wind=0.3)
        q["nod"] = q.get("nod", 0) + 6 * ease(t / 0.6) * (1 - ease((t - 1.2) / 0.6))       # a polite bow of the head
        return at_neck(IBN_SALAM, q, t, 540, 960, 1.0)
    B = Shot(4.3, ltb, midB, cam=camB, light=DUSKL, sun=SUN_DUSK)

    LC = L(132.5, "p3s7c")
    camC = cam_push(1.0, 1.06, 540, 860, 3.8)

    def midC(t):
        q = tp(LC, t, 75, turn=-0.25, gx=-0.6, gy=0.0, furrow=0.3, brow=0.2, smile=0.3, armL="relaxed", armR="offer" if 0.6 < t < 2.6 else "relaxed",
               wind=0.3)
        return at_neck(LEYLI_FATHER, q, t, 540, 960, 1.0)
    C = Shot(3.8, ltb, midC, cam=camC, light=DUSKL, sun=SUN_DUSK)

    tnb = bg("tent_night", lbg.tent_night, 6)
    camD = cam_push(1.0, 1.06, 560, 860, 8.7)

    def midD(t):
        q = P(turn=0.3, gx=0.8 - 0.5 * ease((t - 1.6) / 0.8), gy=0.2 + 0.5 * ease((t - 1.8) / 0.8), sad=0.4 + 0.5 * ease((t - 0.8) / 1.4), brow=0.8,
              furrow=-0.4, armL="relaxed", armR="chest", wind=0.1, blink=max(blink_at(t, 76), 0.55 * ease((t - 2.0) / 0.6)),
              breathe=math.sin(t * 1.6))
        o = at_neck(LEYLI_W, q, t, 560, 1000, 1.08)
        ex, ey = 560 + (-40 + 4) * 1.08 * 0.95, 1000 - 178 * 1.08 * 0.95
        return o + tear(ex, ey + 24, t, 2.6, 1.0)
    D = Shot(8.7, tnb, midD, cam=camD, light=LAMPC, grade="fire", bloom=0.5, fade_out=0.6)
    return [A, B, C, D]


SCENES = {"s1": s1, "s2": s2, "s3": s3, "s4": s4, "s5": s5, "s6": s6, "s7": s7}
