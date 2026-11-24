"""Part 4 · Leyli's Wedding — 2D cartoon. Timing matches leyli/p04_audio.py
(scene starts s1 0, s2 7.6, s3 12.2, s4 35.6, s5 60.2, s6 74.2, s7 111.4; end card 121.4; total 126.6).
The wedding is shown with music and lamps; romance stays modest (Leyli keeps Ibn Salam at a distance)."""
import math, random
from PIL import Image, ImageFilter
from film import Shot, W, H, ease, lerp, blink_at, cam_push, Motes, svg_render
from chars import camel, Ctx, FEET, person, CAMEL_SADDLE_Y
from stage import at_neck, at_feet, lw_for, Glow, back_heads
import bgs, lbg
from cast import *
from p01_scenes import P, tp, bg, cam_xy, seated, birds, SandWind, DUSKL, SUN_DUSK, DAWNL, SUN_DAWN, DAYL, SUN_DAY, LAMPC
from p03_scenes import gazelles, seat_shadow, tear, majnun_sit_q, GZ
import p04_audio as AU

WEDL = dict(ambient=(0.84, 0.76, 0.8), rim=(-5, -2), rim_col=(1.0, 0.68, 0.38), rim_str=0.9, ramp=(0, W, 1.04, 0.92))     # the lamps
MOONIN = dict(ambient=(0.7, 0.7, 0.84), rim=(5, -2), rim_col=(0.78, 0.86, 1.0), rim_str=0.8, ramp=(0, W, 0.86, 1.06))   # moonlight
CAMEL_K = 0.66                   # the camel drawn next to a rider of stage.rider's size (as in babak/p08_scenes.py)


def L(t0, *ids):
    """line ids -> [(id, start within a shot that begins at t0)]; a line said twice is taken at its first time after t0"""
    out = []
    for i in ids:
        ts_ = [t for lid, t in AU.LINES if lid == i and t >= t0 - 0.5]
        out.append((i, min(ts_) - t0))
    return out


def camel_rider(S, q, t, x, y, s, flip=False, walk=True, rate=2.6, k=0.0, col="#c49a64", blanket="#3a2e26"):
    """a camel with a rider on the saddle on its hump (a copy of the helper in zahhak/p10_scenes.py)"""
    c = Ctx(lw_for(s * CAMEL_K))
    rs = 0.31
    qq = dict(q); qq["legs"] = "none"
    neck_y = CAMEL_SADDLE_Y * CAMEL_K - 330 * rs * S["bs"]
    rid = f'<g transform="translate(10,{neck_y + FEET * S["bs"] * rs:.1f}) scale({rs})">{person(S, qq, t, lw_for(s * rs))}</g>'
    sx = -s if flip else s
    return (f'<g transform="translate({x:.1f},{y:.1f}) scale({sx:.4f},{s:.4f})"><g transform="scale({CAMEL_K})">'
            f'{camel(c, col=col, dark="#9a7448", walk=walk, phase=t * rate + k, t=t + k, blanket=blanket)}</g>{rid}</g>')


def litter(x, y, s, t):
    """the bride's litter on a camel's hump: a little domed tent of red cloth with gold edges, swaying with the step (camel units at (x, y))"""
    sw = 4 * math.sin(t * 2.6)
    return (f'<g transform="translate({x:.1f},{y:.1f}) scale({s:.4f}) rotate({sw:.2f})">'
            '<path d="M -170 0 L -150 -200 C -120 -330, 120 -330, 150 -200 L 170 0 Z" fill="#9a1420" stroke="#2a0608" stroke-width="6"/>'
            '<path d="M -150 -200 C -120 -330, 120 -330, 150 -200" stroke="#e8c060" stroke-width="12" fill="none"/>'
            '<path d="M -170 0 L 170 0" stroke="#e8c060" stroke-width="14"/>'
            + "".join(f'<path d="M {-150 + 40 * k} 0 l 20 34 l 20 -34" fill="#e8c060"/>' for k in range(8)) +
            '<path d="M -60 -40 L -60 -190 C -40 -230, 40 -230, 60 -190 L 60 -40 Z" fill="#5a0a10" opacity="0.6"/>'
            '<circle cx="0" cy="-318" r="16" fill="#e8c060" stroke="#2a0608" stroke-width="4"/></g>')


def daf(x, y, s, t, hit=0.0):
    """a frame drum held up in front of the chest: a wooden rim, a pale skin, small rings inside the rim"""
    r = 120 * s
    return (f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="{r:.1f}" ry="{r * 1.02:.1f}" fill="#e8d8b0" stroke="#6a4424" stroke-width="{14 * s:.1f}"/>'
            f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="{r * 0.92:.1f}" ry="{r * 0.94:.1f}" fill="none" stroke="#2a1a10" stroke-width="{2 * s:.1f}"/>'
            + "".join(f'<circle cx="{x + r * 0.84 * math.cos(a):.1f}" cy="{y + r * 0.84 * math.sin(a):.1f}" r="{7 * s:.1f}" fill="none" '
                      f'stroke="#c9a24a" stroke-width="{3 * s:.1f}"/>' for a in [k * math.pi / 4 + 0.2 * hit for k in range(8)]) +
            f'<ellipse cx="{x - r * 0.3:.1f}" cy="{y - r * 0.3:.1f}" rx="{r * 0.3:.1f}" ry="{r * 0.18:.1f}" fill="#fff8e0" opacity="0.4"/>')


def beat(t, period=0.48):
    """0..1 pulse on the music's beat"""
    return max(0.0, math.cos(2 * math.pi * t / period)) ** 6


def clap_arms(t, seed=0, period=0.48):
    """hands that clap on the beat"""
    u = 0.5 + 0.5 * math.cos(2 * math.pi * (t + seed * 0.03) / period)
    return ("ik", lerp(26, 110, 1 - u), 150), ("ik", lerp(-26, -110, 1 - u), 150)


# ================================================================ S1 the hook (0-7.6): the traveller's news; "Married…?"
def traveller_shot(dur, lines, seed, fade_in=0.0, **kw):
    ddb = bg("dunes_day", lambda: lbg.dunes("day"), 6)
    cam = cam_push(1.0, 1.04, 540, 820, dur)

    def mid(t):
        base = dict(turn=0.35, gx=0.6, gy=0.35, brow=0.4, furrow=0.1, armR="relaxed", armL="offer" if any(0.4 < t - st < 2.6 for _, st in lines) else "relaxed",
                    openL=True, wind=0.6)
        base.update(kw)
        q = tp(list(lines), t, seed, **base)
        return camel_rider(TRAVELLER, q, t, 560, 1640, 1.22, flip=True, walk=False, k=seed)
    return Shot(dur, ddb, mid, cam=cam, light=DAYL, sun=SUN_DAY, fade_in=fade_in,
                fx=[SandWind(100, 400 + seed, (0, 300, W, 1900), (500, 900), strength=lambda t: 0.3)])


def majnun_close(dur, lines, seed, shock_t=None, fade_out=0.0, gust_t=None, **kw):
    ddb = bg("dunes_day", lambda: lbg.dunes("day"), 6)
    cam = cam_push(1.0, 1.06, 540, 880, dur)

    def mid(t):
        sh = ease((t - shock_t) / 0.25) if shock_t is not None else 0.0
        base = dict(turn=0.25, gx=0.5, gy=0.1 + 0.4 * ease((t - (shock_t or 0) - 1.2) / 0.6) * (1 if shock_t is not None else 0),
                    sad=0.4 + 0.5 * sh, brow=0.6 + 0.4 * sh, furrow=-0.4, armL="relaxed", armR="relaxed", wind=0.8)
        base.update(kw)
        q = tp(list(lines), t, seed, **base)
        return at_neck(MAJNUN, q, t, 540, 1000, 1.05)
    gs = (lambda t: 0.3 + 0.6 * ease((t - gust_t) / 0.4) * (1 - ease((t - gust_t - 1.8) / 0.8))) if gust_t is not None else (lambda t: 0.3)
    return Shot(dur, ddb, mid, cam=cam, light=DAYL, sun=SUN_DAY, fade_out=fade_out,
                fx=[SandWind(160, 410 + seed, (0, 300, W, 1900), (600, 1000), strength=gs)])


def s1():
    A = traveller_shot(4.4, L(0.0, "p4s1a"), 1, fade_in=0.3)
    B = majnun_close(3.2, L(4.4, "p4s1b"), 2, shock_t=0.3, fade_out=0.5, gust_t=0.4)
    return [A, B]


# ================================================================ S2 title (7.6-12.2): the bride's litter crosses the dunes at dusk
def s2():
    dn = bg("dunes_dusk", lambda: lbg.dunes("dusk"))

    PS = 0.25                       # the people walking with the camel; the camel at the matching size (camel_rider: person = 0.31 x rider scale)
    CS = PS / 0.31 * CAMEL_K

    def mid(t):
        x = 470 + 40 * t
        c = Ctx(lw_for(CS))
        o = (f'<g transform="translate({x:.1f},1700) scale({CS:.4f})">{camel(c, walk=True, phase=t * 2.6, t=t, blanket="#9a1420")}</g>'
             + litter(x + 10 * CS, 1700 + CAMEL_SADDLE_Y * CS + 20, CS, t))
        lead = P(legs="walk", phase=t * 2.6, turn=0.35, gx=0.7, gy=0.0, armR="relaxed", armL="hold_lantern", propL="lantern", wind=0.5,
                 blink=blink_at(t, 21))
        o += at_feet(SERVANT_A, lead, t, x + 300, 1710, PS)
        back = P(legs="walk", phase=t * 2.6 + 1.5, turn=0.35, gx=0.7, gy=0.0, armL="relaxed", armR="hold_lantern", propR="lantern", wind=0.5,
                 blink=blink_at(t, 22))
        o += at_feet(SERVANT_B, back, t, x - 330, 1715, PS)
        return birds(t, 860, 520, n=4, s=0.8) + o
    lan = [Glow(lambda t: (470 + 40 * t + 300 + 40, 1710 - 200), 100, (255, 190, 110), 0.5),
           Glow(lambda t: (470 + 40 * t - 330 - 40, 1715 - 200), 100, (255, 190, 110), 0.5)]
    return [Shot(4.6, dn, mid, cam=cam_push(1.0, 1.04, 540, 1200, 4.6), sun=SUN_DUSK, light=DUSKL, bloom=0.7, fade_in=0.4, fade_out=0.5,
                 fx=lan + [Motes(30, 201, (255, 230, 210), (0, 1000, W, 1600), (-8, -4), amax=70)])]


# ================================================================ S3 the wedding (12.2-35.6)
def couple(t, lines_l=(), lines_i=(), leyli_sad=0.8, seed=0):
    """the bride and groom on their cushions under the canopy (scale for the wide shot: the camera zooms in for the medium shot)"""
    cx, fy = lbg.WED_SEAT
    i = tp(list(lines_i), t, seed + 1, legs="sit", turn=-0.3, gx=-0.7, gy=0.1, smile=0.5, brow=0.3, armL=("ik", 60, 330), armR=("ik", -60, 330),
           wind=0.1)
    l = tp(list(lines_l), t, seed + 2, legs="sit", turn=0.1, gx=0.1, gy=0.6, sad=leyli_sad, brow=0.8, furrow=-0.4, armL=("ik", 60, 330),
           armR=("ik", -60, 330), wind=0.1)
    return seated(LEYLI_BRIDE, l, t, cx - 95, fy, 0.34) + seated(IBN_SALAM, i, t, cx + 105, fy, 0.35)


def s3():
    wd = bgs.cached("ly_wedding", lbg.wedding)
    wdb = bg("wedding", lbg.wedding, 6)
    heads = bgs.cached("ly_p4_wedding_heads", lambda: back_heads(4501, 8, 1820, 0.55, col="#120c10", blur=3))
    glows = [Glow(lambda t, x=x: (x, 1110), 160, (255, 180, 100), 0.35) for x in (170, 1010)]

    # A1: the wedding at night: music, the guests clap, the bride and groom under the canopy
    camA1 = cam_push(1.0, 1.05, 540, 1250, 5.4)

    def midA1(t):
        o = couple(t, seed=30)
        b = beat(t)
        dq = P(legs="sit", turn=0.3, gx=0.5, gy=0.1, smile=0.4, armL=("ik", 120, 120 - 20 * b), armR=("ik", -40, 200 + 30 * b), wind=0.2,
               blink=blink_at(t, 31))
        o += seated(DRUMMER, dq, t, 130, 1540, 0.42) + daf(130 + 30, 1540 - 575 * 0.42 + 80, 0.42, t, b)
        pq = P(legs="sit", turn=0.35, gx=0.6, gy=0.1, smile=0.5, armR=("ik", -60 + 14 * math.sin(t * 9), 360), armL=("ik", 210, 20), propR="tanbur",
               wind=0.2, blink=blink_at(t, 32))
        o += seated(PLAYER, pq, t, 300, 1550, 0.42)
        for k, (S, x, fy, s) in enumerate(((GOSSIP_A, 790, 1540, 0.42), (GOSSIP_B, 950, 1550, 0.42), (MOTHER, 1080, 1560, 0.42))):
            al, ar = clap_arms(t, k)
            q = P(legs="sit", turn=-0.3, gx=-0.6, gy=0.0, smile=0.5 if S is not MOTHER else 0.0, sad=0.5 if S is MOTHER else 0.0, armL=al if S is not MOTHER else ("ik", 60, 330),
                  armR=ar if S is not MOTHER else ("ik", -60, 330), wind=0.2, blink=blink_at(t, 33 + k))
            o += seated(S, q, t, x, fy, s)
        return o
    A1 = Shot(5.4, wd, midA1, fg=heads, cam=camA1, light=WEDL, grade="fire", bloom=0.7, fade_in=0.4,
              fx=glows + [Motes(40, 301, (255, 210, 150), (0, 700, W, 1500), (6, -12), amax=90)])

    # A2: the musicians, closer
    camA2 = cam_push(1.0, 1.05, 540, 900, 3.4)

    def midA2(t):
        b = beat(t)
        dq = P(turn=0.3, gx=0.5, gy=0.1, smile=0.5, armL=("ik", 150, 80 - 20 * b), armR=("ik", -30, 160 + 40 * b), wind=0.2, blink=blink_at(t, 37),
               mouth_o=0.2 * b)
        o = at_neck(DRUMMER, dq, t, 330, 940, 0.92) + daf(330 + 40, 940 + 150, 0.92, t, b)
        pq = P(turn=-0.3, gx=-0.5, gy=0.2, smile=0.6, armR=("ik", -60 + 14 * math.sin(t * 9), 360), armL=("ik", 210, 20), propR="tanbur", wind=0.2,
               blink=blink_at(t, 38))
        o += at_neck(PLAYER, pq, t, 760, 960, 0.92)
        return o
    A2 = Shot(3.4, wdb, midA2, cam=camA2, light=WEDL, grade="fire", bloom=0.6)

    # B: the two women: "Look at the bride! She is as beautiful as the moon!" — "Then why are her eyes so sad?"
    LBa = L(21.0, "p4s3c")
    LBb = L(21.0, "p4s3d")
    camB = cam_push(1.0, 1.04, 540, 900, 8.4)

    def midB(t):
        turn_b = ease((t - 4.4) / 0.5)
        a = tp(LBa, t, 39, turn=-0.3 + 0.55 * ease((t - 3.6) / 0.5), gx=-0.7 + 1.2 * ease((t - 3.6) / 0.5), gy=0.0, smile=0.6, brow=0.5,
               armL="relaxed", armR="offer" if 0.6 < t < 3.0 else "chest", wind=0.2)
        b = tp(LBb, t, 40, turn=-0.3 * (1 - turn_b) + 0.0, gx=-0.7 * (1 - turn_b) - 0.3 * turn_b, gy=0.1, sad=0.6 * turn_b, brow=0.5 + 0.3 * turn_b,
               furrow=-0.2, smile=0.4 * (1 - turn_b), armL="relaxed", armR="chest" if t > 5.0 else "relaxed", wind=0.2)
        return at_neck(GOSSIP_A, a, t, 330, 990, 0.95) + at_neck(GOSSIP_B, b, t, 760, 1000, 0.95)
    B = Shot(8.4, wdb, midB, cam=camB, light=WEDL, grade="fire", bloom=0.5)

    # D1: the bride and groom (narration: everyone was happy… except the bride)
    camD1 = cam_push(1.75, 1.85, 540, 1060, 3.6)

    def midD1(t):
        return couple(t, seed=41, leyli_sad=0.85)
    D1 = Shot(3.6, wd, midD1, cam=camD1, bg_par=1.0, light=WEDL, grade="fire", bloom=0.6,
              fx=[Motes(30, 302, (255, 210, 150), (0, 500, W, 1400), (4, -10), amax=80)])

    # D2: Leyli close: her eyes go down
    camD2 = cam_push(1.0, 1.05, 540, 880, 2.6)

    def midD2(t):
        q = P(turn=0.15, gx=0.2 - 0.2 * ease((t - 0.8) / 0.6), gy=0.2 + 0.5 * ease((t - 0.8) / 0.6), sad=0.85, brow=0.9, furrow=-0.5, armL="relaxed",
              armR="relaxed", wind=0.1, blink=max(blink_at(t, 42), 0.45 * ease((t - 1.0) / 0.6)), breathe=math.sin(t * 1.6))
        return at_neck(LEYLI_BRIDE, q, t, 540, 1000, 1.08)
    D2 = Shot(2.6, wdb, midD2, cam=camD2, light=WEDL, grade="fire", bloom=0.5, fade_out=0.5)
    return [A1, A2, B, D1, D2]


# ================================================================ S4 Ibn Salam's tent at night (35.6-60.2)
def s4():
    rt = bg("rich_tent", lbg.rich_tent)
    rtb = bg("rich_tent", lbg.rich_tent, 6)
    lamp = Glow(lambda t: lbg.RICH_LAMP, 200, (255, 180, 100), 0.35)

    LA = L(35.6, "p4s4a")
    camA = cam_push(1.0, 1.04, 540, 1100, 5.0)

    def midA(t):
        i = tp(LA, t, 50, turn=-0.3, gx=-0.7, gy=0.0, smile=0.4, brow=0.4, armR="relaxed" if t < 3.6 else "chest", armL="offer" if 0.6 < t < 3.6 else "relaxed",
               openL=True, wind=0.1)
        l = tp([], t, 51, turn=0.3, gx=0.5, gy=0.5, sad=0.7, brow=0.8, furrow=-0.3, armL="relaxed", armR="chest", wind=0.1)
        return at_feet(LEYLI_BRIDE, l, t, 250, 1700, 0.62) + at_feet(IBN_SALAM, i, t, 800, 1710, 0.64)
    A = Shot(5.0, rt, midA, cam=camA, light=LAMPC, grade="fire", bloom=0.6, fade_in=0.4, fx=[lamp])

    LB = L(40.6, "p4s4b")
    camB = cam_push(1.0, 1.05, 540, 880, 5.4)

    def midB(t):
        q = tp(LB, t, 52, turn=0.25, gx=0.6, gy=0.1 if t > 0.8 else 0.5, sad=0.6, brow=0.7, furrow=-0.3, armL="relaxed", armR="chest" if t > 2.6 else "relaxed",
               wind=0.1)
        return at_neck(LEYLI_BRIDE, q, t, 540, 1000, 1.08)
    B = Shot(5.4, rtb, midB, cam=camB, light=LAMPC, grade="fire", bloom=0.5)

    LC = L(46.0, "p4s4c", "p4s4d")
    camC = cam_push(1.02, 1.1, 540, 880, 6.6)

    def midC(t):
        stop = 4.6 < t < 6.4
        q = tp(LC, t, 53, turn=0.25, gx=0.6, gy=0.1, sad=0.7, brow=0.8 - 0.3 * ease((t - 4.4) / 0.4), furrow=-0.3 + 0.6 * ease((t - 4.4) / 0.4),
               armL=("ik", 130, 150) if stop else "relaxed", openL=True, armR="chest", wind=0.1)
        return at_neck(LEYLI_BRIDE, q, t, 540, 1000, 1.08)
    C = Shot(6.6, rtb, midC, cam=camC, light=LAMPC, grade="fire", bloom=0.5)

    LD = L(52.6, "p4s4e", "p4s4f")
    camD = cam_push(1.0, 1.06, 540, 880, 7.6)

    def midD(t):
        warm = ease((t - 3.8) / 0.8)
        q = tp(LD, t, 54, turn=-0.25, gx=-0.6, gy=0.3 - 0.3 * ease((t - 0.6) / 0.5), sad=0.6 * (1 - warm) + 0.2, brow=0.7, furrow=-0.3,
               smile=0.35 * warm, armL="relaxed", armR="chest", wind=0.1)
        return at_neck(IBN_SALAM, q, t, 540, 960, 1.0)
    D = Shot(7.6, rtb, midD, cam=camD, light=LAMPC, grade="fire", bloom=0.5, fade_out=0.5)
    return [A, B, C, D]


# ================================================================ S5 Leyli alone at night (60.2-74.2)
def s5():
    rt = bg("rich_tent", lbg.rich_tent)
    night = bgs.cached("ly_rich_tent_dim", lambda: Image.alpha_composite(bgs.cached("ly_rich_tent", lbg.rich_tent).convert("RGBA"),
                                                                         Image.new("RGBA", (W, H), (8, 10, 30, 90))))
    nightb = bgs.cached("ly_rich_tent_dim_b6", lambda: night.filter(ImageFilter.GaussianBlur(6)))
    camA = cam_push(1.0, 1.06, 700, 1100, 6.8)

    def midA(t):
        q = P(legs="sit", turn=0.35, gx=0.8, gy=-0.35, sad=0.85, brow=0.9, furrow=-0.5, armL=("ik", 60, 330), armR="chest", wind=0.2,
              blink=max(blink_at(t, 55), 0.3), breathe=math.sin(t * 1.4))
        return seat_shadow(560, 1290, 160) + seated(LEYLI_W, q, t, 600, 1290, 0.6)
    A = Shot(6.8, night, midA, cam=camA, light=MOONIN, grade="night", bloom=0.6, fade_in=0.5,
             fx=[Glow(lambda t: cam_xy(camA, t, 910, 500), 160, (210, 225, 255), 0.25)])

    LB = L(67.0, "p4s5b")
    camB = cam_push(1.0, 1.06, 540, 880, 7.2)

    def midB(t):
        q = tp(LB, t, 56, turn=0.25, gx=0.7, gy=-0.3 + 0.6 * ease((t - 5.0) / 0.8), sad=0.9, brow=1.0, furrow=-0.5, armL="relaxed", armR="chest",
               wind=0.1)
        q["blink"] = max(q["blink"], 0.25 + 0.5 * ease((t - 5.2) / 0.6))
        ex, ey = 540 + (-40 + 3) * 1.08 * 0.95, 1000 - 178 * 1.08 * 0.95
        return at_neck(LEYLI_W, q, t, 540, 1000, 1.08) + tear(ex, ey + 24, t, 1.6, 1.0)
    B = Shot(7.2, nightb, midB, cam=camB, light=MOONIN, grade="night", bloom=0.5, fade_out=0.6)
    return [A, B]


# ================================================================ S6 the desert: the news; Majnun's answer; into the wild (74.2-111.4)
def s6():
    dd = bg("dunes_day", lambda: lbg.dunes("day"))

    # A: a traveller on a camel comes to Majnun among the gazelles
    camA = cam_push(1.02, 1.0, 560, 1050, 4.8)

    def midA(t):
        u = ease(t / 3.8)
        o = gazelles(t, GZ, startle=1.6)
        o += seat_shadow(330, 1222, 170)
        o += seated(MAJNUN, majnun_sit_q(t, 61, look=0.5 + 0.4 * ease((t - 1.4) / 0.6), gy=0.1), t, 330, 1222, 0.62)
        q = P(turn=0.35, gx=0.6, gy=0.2, brow=0.3, armR="relaxed", armL="relaxed", wind=0.6, blink=blink_at(t, 62))
        o += camel_rider(TRAVELLER, q, t, lerp(1380, 900, u), 1140, 0.55, flip=True, walk=t < 3.8, k=1.0)
        return o
    A = Shot(4.8, dd, midA, cam=camA, light=DAYL, sun=SUN_DAY, bloom=0.5, fade_in=0.4,
             fx=[SandWind(140, 601, (0, 1000, W, 1900), (500, 900), strength=lambda t: 0.3)])
    B = traveller_shot(3.6, L(79.0, "p4s6b"), 63)
    C = traveller_shot(4.0, L(82.6, "p4s1a"), 64)
    D = majnun_close(2.4, L(86.6, "p4s1b"), 65, shock_t=0.2, gust_t=0.3)
    E = traveller_shot(5.0, L(89.0, "p4s6c"), 66, brow=0.2, furrow=0.3, smile=0.1)
    F = majnun_close(3.6, L(94.0, "p4s6d"), 67, sad=0.6, brow=0.7, gy=0.1, smile=0.15, armR="chest")

    # G: Majnun stands and looks up at the sky: "Let her be happy. The moon is far away… but its light still finds me."
    ddb = bg("dunes_day", lambda: lbg.dunes("day"), 6)
    LG = L(97.6, "p4s6e")
    camG = cam_push(1.0, 1.06, 540, 860, 6.4)

    def midG(t):
        q = tp(LG, t, 68, turn=0.15, gx=0.2, gy=-0.5 + 0.2 * ease((t - 4.0) / 0.8), sad=0.5, brow=0.7, furrow=-0.4, smile=0.3 * ease((t - 3.0) / 1.0),
               armL="relaxed", armR="chest", wind=1.0)
        return at_neck(MAJNUN, q, t, 540, 1000, 1.05)
    G = Shot(6.4, ddb, midG, cam=camG, light=DAYL, sun=SUN_DAY,
             fx=[SandWind(160, 602, (0, 300, W, 1900), (600, 1000), strength=lambda t: 0.5), Motes(30, 603, (255, 240, 210), (0, 300, W, 1200), (10, -6), amax=70)])

    # H: Majnun walks into the wild at dusk, two gazelles following him
    dn = bg("dunes_dusk", lambda: lbg.dunes("dusk"))
    camH = cam_push(1.04, 1.0, 480, 1100, 7.4)

    def midH(t):
        u = ease(t / 7.4)
        x = lerp(700, 430, u); y = lerp(1520, 1240, u); s = lerp(0.56, 0.28, u)
        q = P(legs="walk", phase=t * 4.6, turn=-0.45, gx=-0.9, gy=0.3, sad=0.5, brow=0.7, armL="relaxed", armR="relaxed", wind=1.4,
              blink=blink_at(t, 69), breathe=math.sin(t * 3))
        sh = f'<g transform="translate({x:.1f},{y:.1f}) scale({s:.4f})"><path d="M -60 0 L 760 160 L 820 90 L 40 -20 Z" fill="#3a1830" opacity="0.28"/></g>'
        c = Ctx(lw_for(s * 1.6))
        o = ""
        for k, (dx, dy, ks) in enumerate(((260, 30, 1.55), (420, 10, 1.35))):
            gx_, gy_ = x + dx * s / 0.56, y + dy * s / 0.56
            o += (f'<g transform="translate({gx_:.1f},{gy_:.1f}) scale({ks * s:.4f})">'
                  f'{__import__("chars").gazelle(c, t=t + k, seed=k, walk=True, phase=t * 5.0 + k, look=0.1)}</g>')
        return sh + o + at_feet(MAJNUN, q, t, x, y, s)
    H = Shot(7.4, dn, midH, cam=camH, light=DUSKL, sun=SUN_DUSK, bloom=0.7, fade_out=0.6,
             fx=[SandWind(200, 604, (0, 1000, W, 1900), (600, 1000), strength=lambda t: 0.6)])
    return [A, B, C, D, E, F, G, H]


# ================================================================ S7 an old man with a stick: "Qays! My son! Where are you?" (111.4-126.6)
def s7():
    dw = bg("dunes_dawn", lambda: lbg.dunes("dawn"))
    camA = cam_push(1.0, 1.05, 540, 1150, 5.6)

    def midA(t):
        x = lerp(180, 420, t / 5.6); y = 1260; s = 0.34
        q = P(legs="walk", phase=t * 2.4, turn=0.35, gx=0.7, gy=0.2, sad=0.6, brow=0.8, furrow=-0.2, armL=("ik", 190 + 30 * math.sin(t * 2.4), 520),
              propL="staff", armR="relaxed", wind=0.8, blink=blink_at(t, 71), breathe=math.sin(t * 2))
        sh = f'<g transform="translate({x:.1f},{y:.1f}) scale({s:.4f})"><path d="M 60 0 L -760 120 L -820 60 L -40 -20 Z" fill="#3a2a40" opacity="0.25"/></g>'
        return sh + at_feet(CHIEF_OLD, q, t, x, y, s)
    A = Shot(5.6, dw, midA, cam=camA, light=DAWNL, sun=SUN_DAWN, bloom=0.7, fade_in=0.5,
             fx=[SandWind(140, 701, (0, 1000, W, 1900), (500, 900), strength=lambda t: 0.4), Motes(30, 702, (255, 230, 210), (0, 900, W, 1600), (-8, -4), amax=70)])

    dwb = bg("dunes_dawn", lambda: lbg.dunes("dawn"), 4)
    LB = L(117.0, "p4s7b")
    camB = cam_push(1.0, 1.04, 540, 1000, 9.6)

    def midB(t):
        call = LB[0][1]
        walking = t < call - 0.3 or t > call + 3.0
        u = t / 9.6
        x = lerp(380, 640, u)
        q = tp(LB, t, 72, legs="walk" if walking else "stand", phase=t * 2.4, turn=0.35 if walking else 0.1, gx=0.7 if walking else -0.6 + 1.2 * ease((t - call - 0.6) / 1.2),
               gy=0.0, sad=0.6, brow=0.9, furrow=-0.3, armL=("ik", 190 + (30 * math.sin(t * 2.4) if walking else 0), 520), propL="staff",
               armR="relaxed" if walking else ("ik", -70, -40), wind=0.8)
        return at_feet(CHIEF_OLD, q, t, x, 1720, 0.62)
    B = Shot(9.6, dwb, midB, cam=camB, light=DAWNL, sun=SUN_DAWN, bloom=0.6, fade_out=0.6,
             fx=[SandWind(160, 703, (0, 300, W, 1900), (500, 900), strength=lambda t: 0.4)])
    return [A, B]


SCENES = {"s1": s1, "s2": s2, "s3": s3, "s4": s4, "s5": s5, "s6": s6, "s7": s7}
