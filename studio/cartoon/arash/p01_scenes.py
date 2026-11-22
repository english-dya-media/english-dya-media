"""Part 1 · The Siege — 2D cartoon. Timing matches arash/p01_audio.py
(scene starts s1 0, s2 7.8, s3 12.4, s4 36.4, s5 52.8, s6 85.2; end card 116.0; total 121.4)."""
import math, random
from PIL import Image, ImageFilter, ImageDraw
from film import Shot, W, H, ease, lerp, talk_pose, blink_at, cam_push, cam_static, Motes, Embers, svg_render
from chars import pose, horse, Ctx, FEET, fmt, prop
from stage import at_neck, at_feet, rider, Glow, lw_for, fire_svg, back_heads, random_spec
import bgs, zbg, abg
from cast import *
import p01_audio as A1

DAWNL = dict(rim=(-5, -2), rim_col=(1.0, 0.8, 0.62), rim_str=0.9, ramp=(0, W, 1.05, 0.9), ambient=(0.98, 0.92, 0.94))
SUN_DAWN = (170, 1030, 900, (0.12, 0.08, 0.05))
DAYL = dict(rim=(5, -2), rim_col=(1.0, 0.92, 0.75), ramp=(0, W, 0.94, 1.05), ambient=(1.0, 0.98, 0.95))
SUN_DAY = (900, 400, 900, (0.08, 0.07, 0.04))
DUSKL = dict(rim=(-5, -2), rim_col=(1.0, 0.7, 0.48), rim_str=0.9, ramp=(0, W, 1.05, 0.86), ambient=(0.92, 0.84, 0.88))
SUN_DUSK = (150, 700, 900, (0.12, 0.06, 0.04))
NIGHTL = dict(ambient=(0.62, 0.68, 0.94), rim=(5, -3), rim_col=(0.75, 0.84, 1.0), rim_str=0.7)
LAMPL = dict(ambient=(0.8, 0.72, 0.74), point=(540, 560, 900, 0.6, 1.15, (1.0, 0.6, 0.3)), rim=(0, -3), rim_col=(1.0, 0.68, 0.38), rim_str=0.7)
LAMPC = dict(ambient=(0.84, 0.76, 0.78), rim=(-5, -2), rim_col=(1.0, 0.66, 0.36), rim_str=0.9, ramp=(0, W, 1.06, 0.86))
TENTL = dict(ambient=(0.78, 0.72, 0.82), rim=(-5, -2), rim_col=(1.0, 0.65, 0.35), rim_str=0.9, ramp=(0, W, 1.05, 0.88))
FIREL = dict(ambient=(0.6, 0.62, 0.86), rim_point=(0, 6), rim_col=(1.0, 0.6, 0.3), rim_str=1.0, ramp=(0, W, 1.1, 0.8))


# ---------------------------------------------------------------- helpers
def P(**kw):
    return pose(**kw)


def tp(lines, t, seed, **kw):
    return P(**talk_pose(lines, t, seed, kw))


def bg(name, fn, blur=0):
    """a background cached as build/bg/ar_<name>[_b<blur>].png"""
    if blur:
        return bgs.cached(f"ar_{name}_b{blur}", lambda: bgs.cached(f"ar_{name}", fn).filter(ImageFilter.GaussianBlur(blur)))
    return bgs.cached(f"ar_{name}", fn)


def cam_xy(cam, t, x, y):
    k, cx, cy, px, py = cam(t)
    return (x - cx) * k + cx + px, (y - cy) * k + cy + py


def flame(x, y, t, s=1.0, seed=0):
    """a small flame standing on (x, y)"""
    ph = seed * 1.3
    h = (120 + 30 * math.sin(t * 13 + ph) + 18 * math.sin(t * 7.3 + ph)) * s
    sw = 10 * math.sin(t * 5 + ph) * s
    return (f'<path d="M {x - 30 * s:.1f} {y:.1f} C {x - 40 * s:.1f} {y - h * 0.45:.1f}, {x - 10 * s + sw:.1f} {y - h * 0.8:.1f}, {x + sw:.1f} {y - h:.1f} '
            f'C {x + 14 * s + sw:.1f} {y - h * 0.75:.1f}, {x + 40 * s:.1f} {y - h * 0.45:.1f}, {x + 30 * s:.1f} {y:.1f} Z" fill="#ff8a1a"/>'
            f'<path d="M {x - 16 * s:.1f} {y:.1f} C {x - 20 * s:.1f} {y - h * 0.35:.1f}, {x - 4 * s + sw * 0.6:.1f} {y - h * 0.6:.1f}, {x + sw * 0.6:.1f} {y - h * 0.72:.1f} '
            f'C {x + 8 * s + sw * 0.6:.1f} {y - h * 0.55:.1f}, {x + 20 * s:.1f} {y - h * 0.35:.1f}, {x + 16 * s:.1f} {y:.1f} Z" fill="#ffd84a"/>')


def arrow_svg(x, y, ang, s, trail=0.0):
    """an arrow in flight, its middle at (x, y), pointing at angle ang (degrees, 0 = right); a golden trail behind it"""
    o = f'<g transform="translate({x:.1f},{y:.1f}) rotate({ang:.1f}) scale({s:.4f})">'
    if trail > 0:
        o += (f'<path d="M -260 -10 L {-260 - 900 * trail:.0f} -2 L {-260 - 900 * trail:.0f} 2 L -260 10 Z" fill="#ffe6a8" opacity="0.55"/>'
              f'<path d="M -260 -4 L {-260 - 600 * trail:.0f} 0 L -260 4 Z" fill="#ffffff" opacity="0.8"/>')
    o += ('<path d="M -260 0 L 230 0" stroke="#1b0f0a" stroke-width="13"/><path d="M -260 0 L 230 0" stroke="#d8b47a" stroke-width="7"/>'
          '<path d="M 300 0 L 226 -22 L 236 0 L 226 22 Z" fill="#dfe4ea" stroke="#1b0f0a" stroke-width="4"/>'
          '<path d="M -200 0 L -270 -42 L -300 -40 L -240 0 L -300 40 L -270 42 Z" fill="#6a4a2e" stroke="#1b0f0a" stroke-width="4"/>'
          '<path d="M -150 0 L -205 -30 L -226 -28 L -186 0 L -226 28 L -205 30 Z" fill="#8a6a42" stroke="#1b0f0a" stroke-width="3"/>')
    return o + '</g>'


def merlons(y=1130, col="#3a3640", dark="#1e1c24", lit="#5a5666"):
    """a battlement across the bottom of the frame (in front of a person standing behind it)"""
    o = f'<rect x="-40" y="{y + 90}" width="1160" height="{H - y}" fill="{col}" stroke="{dark}" stroke-width="4"/>'
    for x in range(-20, 1100, 200):
        o += (f'<rect x="{x}" y="{y}" width="120" height="100" fill="{col}" stroke="{dark}" stroke-width="4"/>'
              f'<rect x="{x + 96}" y="{y}" width="24" height="100" fill="{dark}" opacity="0.5"/>'
              f'<path d="M {x} {y + 4} L {x + 120} {y + 4}" stroke="{lit}" stroke-width="4"/>')
    o += f'<path d="M -40 {y + 94} L 1120 {y + 94}" stroke="{lit}" stroke-width="4"/>'
    for yy in range(y + 160, H, 70):
        o += f'<path d="M -40 {yy} L 1120 {yy}" stroke="{dark}" stroke-width="3" opacity="0.6"/>'
    return o


def table(y=1330, x0=230, x1=850):
    return (f'<path d="M {x0} {y} L {x1} {y} L {x1 + 40} {y + 60} L {x0 - 40} {y + 60} Z" fill="#6a4426" stroke="#1b0f0a" stroke-width="4"/>'
            f'<rect x="{x0 - 40}" y="{y + 60}" width="{x1 - x0 + 80}" height="26" fill="#4a2e18" stroke="#1b0f0a" stroke-width="4"/>'
            f'<path d="M {x0 + 60} {y + 8} L {x1 - 80} {y + 4} L {x1 - 60} {y + 50} L {x0 + 40} {y + 54} Z" fill="#e8d8b0" stroke="#5a4428" stroke-width="3"/>'
            f'<path d="M {x0 + 120} {y + 30} C {x0 + 220} {y + 10}, {x0 + 300} {y + 44}, {x1 - 140} {y + 24}" stroke="#7a5a3a" stroke-width="4" fill="none"/>'
            f'<circle cx="{(x0 + x1) / 2:.0f}" cy="{y + 26}" r="9" fill="#2a4a8a"/>')


# ================================================================ S1 the hook (0-7.8): an arrow over Damavand at sunrise
def s1():
    dusk = bgs.cached("zh_damavand_dusk", lambda: zbg.damavand("dusk"))
    T0 = A1.ARROW - 0.1
    camA = cam_push(1.25, 1.32, 600, 760, 3.6)

    def midA(t):
        u = (t - T0) / 2.8
        if u <= 0 or u >= 1.15:
            return ""
        uu = min(1.0, u)
        x = lerp(-260, 760, ease(uu) * 0.6 + uu * 0.4); y = lerp(980, 440, uu) - 120 * math.sin(math.pi * uu) * 0.5
        s = lerp(1.5, 0.12, uu ** 0.8)
        ang = lerp(-28, -10, uu)
        a = 1.0 if u < 1.0 else max(0.0, 1 - (u - 1.0) / 0.15)
        return f'<g opacity="{a:.2f}">{arrow_svg(x, y, ang, s, trail=min(1.0, u * 2))}</g>'
    A = Shot(3.6, dusk, midA, cam=camA, bg_par=1.0, light=dict(DAWNL, ramp=None), sun=(170, 1030, 900, (0.14, 0.09, 0.05)), fade_in=0.4,
             fx=[Motes(40, 101, (255, 230, 200), (0, 200, W, 1300), (-10, -4), amax=90)], bloom=0.7)

    camB = cam_push(1.0, 1.05, 600, 800, 4.2)

    def midB(t):
        u = t / 4.0
        x = lerp(760, 1060, u); y = lerp(440, 330, u)
        glint = 0.6 + 0.4 * math.sin(t * 9)
        line = f'<path d="M 520 520 Q {lerp(600, 800, u):.0f} {lerp(450, 390, u):.0f} {x:.0f} {y:.0f}" stroke="#ffe6a8" stroke-width="3" fill="none" opacity="{0.6 * (1 - u * 0.5):.2f}"/>'
        return (line + f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{14 * glint:.1f}" fill="#fff2c8" opacity="0.5"/>'
                + arrow_svg(x, y, -24, 0.1))
    B = Shot(4.2, dusk, midB, cam=camB, bg_par=1.0, light=dict(DAWNL, ramp=None), sun=(170, 1030, 900, (0.14, 0.09, 0.05)), fade_out=0.5,
             fx=[Motes(40, 102, (255, 230, 200), (0, 200, W, 1300), (-10, -4), amax=90)], bloom=0.7)
    return [A, B]


# ================================================================ S2 title (7.8-12.4): the besieged fortress at dawn
def s2():
    sg = bg("siege_dawn", lambda: abg.siege("dawn"))
    return [Shot(4.6, sg, None, cam=cam_push(1.0, 1.06, 540, 800, 4.6), sun=SUN_DAWN,
                 fx=[Motes(40, 201, (255, 230, 210), (0, 200, W, 1300), (-8, -4), amax=80)], bloom=0.6, fade_in=0.4, fade_out=0.5)]


# ================================================================ S3 the war; the siege; hunger (12.4-36.4)
def s3():
    sg = bg("siege_dawn", lambda: abg.siege("dawn"))
    # A: the fortress on its hill, the tents of Turan all round
    A = Shot(4.8, sg, None, cam=cam_push(1.04, 1.16, 540, 860, 4.8), sun=SUN_DAWN,
             fx=[Motes(40, 301, (255, 230, 210), (0, 200, W, 1300), (-8, -4), amax=80)], bloom=0.6, fade_in=0.3)

    # B: Turan's camp below the fortress: Afrasiab rides past his soldiers
    camp = bg("siege_day", lambda: abg.siege("day"))
    camB = cam_push(1.0, 1.05, 540, 1100, 8.6)
    guards = [(TURAN_SOLDIER, 120, 1500, 0.34, 1), (TURAN_SOLDIER_2, 250, 1470, 0.32, 1), (TURAN_SOLDIER_2, 860, 1470, 0.32, -1),
              (TURAN_SOLDIER, 990, 1500, 0.34, -1)]

    def midB(t):
        o = ""
        for k, (S, x, y, s, side) in enumerate(guards):
            q = P(turn=0.3 * side, gx=0.6 * side, gy=-0.2, furrow=0.6, brow=0.0, armL=(20, 10), propL="spear", armR="relaxed",
                  blink=blink_at(t, 30 + k), breathe=math.sin(t * 2 + k), wind=0.4)
            o += at_feet(S, q, t, x, y, s)
        u = ease(t / 6.5)
        x = lerp(1180, 560, u)
        q = P(turn=-0.35, gx=-0.4, gy=-0.6, furrow=0.4, brow=0.1, smile=0.4, armR="forward", armL="relaxed", blink=blink_at(t, 35), wind=0.7)
        o += rider(AFRASIAB, q, t, lambda c: horse(c, col="#1a1a1e", walk=t < 6.5, phase=t * 4.2, t=t, blanket="#7a0e12", head_down=0.1),
                   x, 1440, 0.86, flip=True)
        return o
    B = Shot(8.6, camp, midB, cam=camB, light=DAYL, sun=SUN_DAY, fx=[Motes(30, 302, (255, 240, 220), (0, 300, W, 1400), (-6, -2), amax=60)])

    # C: inside the fortress: no more bread
    yard = bg("fort_yard_day", lambda: abg.fort_yard("day"))
    r = random.Random(303)
    folk = [random_spec(r, ("man",)), random_spec(r, ("woman",)), random_spec(r, ("man",))]
    camC = cam_push(1.0, 1.05, 540, 1100, 4.4)

    def midC(t):
        o = ""
        old = P(legs="sit", turn=-0.3, gx=-0.5, gy=0.6, sad=0.8, brow=0.6, furrow=-0.3, armL="chest", armR="relaxed", blink=blink_at(t, 40),
                breathe=math.sin(t * 1.6))
        o += at_neck(folk[0], old, t, 900, 1010, 0.33)
        q1 = P(turn=0.3, gx=0.5, gy=0.5, sad=0.8, brow=0.6, furrow=-0.2, armR="offer", propR="bowl", armL="relaxed", blink=blink_at(t, 41),
               breathe=math.sin(t * 1.8))
        o += at_feet(folk[2], q1, t, 210, 1470, 0.36)
        q2 = P(turn=0.2, gx=0.3, gy=0.6, sad=0.9, brow=0.7, furrow=-0.3, armL="chest", armR="chest", blink=blink_at(t, 42), breathe=math.sin(t * 2))
        o += at_feet(folk[1], q2, t, 360, 1490, 0.35)
        q3 = P(turn=-0.2, gx=-0.3, gy=0.4, sad=0.6, brow=0.5, furrow=0.0, armL=(20, 10), propL="spear", armR="relaxed", blink=blink_at(t, 43))
        o += at_feet(IRAN_SOLDIER_2, q3, t, 640, 1460, 0.35)
        return o
    C = Shot(4.4, yard, midC, cam=camC, light=DAYL, sun=SUN_DAY, fade_in=0.2)

    # D: the mother and her boy: "Mother, I'm hungry." — "I know, my son. Be patient."
    yardb = bg("fort_yard_day", lambda: abg.fort_yard("day"), 7)
    LDb = [("p1s3e", 0.3)]; LDm = [("p1s3f", 2.1)]
    camD = cam_push(1.0, 1.05, 540, 860, 6.2)

    def midD(t):
        hug = ease((t - 2.0) / 0.6)
        b = tp(LDb, t, 1, turn=0.35, gx=0.8, gy=-0.6, sad=0.7, brow=0.7, furrow=-0.3, armL="relaxed", armR="relaxed", wind=0.3)
        m = tp(LDm, t, 2, turn=-0.3, gx=-0.8, gy=0.5, sad=0.6, brow=0.6, furrow=-0.2, smile=0.25 * hug, armL="chest",
               armR=("ik", lerp(-200, -330, hug), lerp(260, 150, hug)), wind=0.3)
        return at_neck(MOTHER, m, t, 650, 880, 0.95) + at_neck(BOY, b, t, 360, 1000, 0.95)
    D = Shot(6.2, yardb, midD, cam=camD, light=DAYL, sun=SUN_DAY, fade_out=0.4)
    return [A, B, C, D]


# ================================================================ S4 night on the wall; the council (36.4-52.8)
def s4():
    plain = bgs.cached("night_plain", bgs.night_plain)
    # A: Manuchehr on the wall looks at the enemy's fires: "Look… their fires are everywhere."
    LA = [("p1s4d", 0.4)]
    camA = cam_push(1.0, 1.05, 540, 860, 4.2)

    rf = random.Random(401)
    fires = [(rf.uniform(330, 1080), rf.uniform(1020, 1235)) for _ in range(34)]

    def midA(t):
        q = tp(LA, t, 1, turn=0.35, gx=0.9, gy=0.5, sad=0.4, brow=0.5, furrow=0.3, armL="point" if 0.6 < t < 2.6 else "relaxed", armR="relaxed",
               wind=0.6)
        o = ""
        for k, (x, y) in enumerate(sorted(fires, key=lambda f: f[1])):
            sc = 0.06 + (y - 1000) / 240 * 0.1
            o += (f'<circle cx="{x:.0f}" cy="{y - 8 * sc / 0.1:.0f}" r="{90 * sc:.1f}" fill="#ffa050" opacity="0.3"/>' + flame(x, y, t + k * 0.37, sc, k))
        return o + at_neck(MANUCHEHR, q, t, 250, 930, 0.78) + merlons(1250)
    A = Shot(4.2, plain, midA, cam=camA, light=dict(NIGHTL, rim_point=(1200, 6), rim_col=(1.0, 0.7, 0.45)), grade="night", bloom=0.6, fade_in=0.4,
             fx=[Glow(lambda t: cam_xy(camA, t, 900, 1300), 420, (255, 150, 70), 0.18)])

    # B: the council room: "My people are hungry… and my soldiers are tired."
    room = bgs.cached("war_room", bgs.war_room)
    LB = [("p1s4a", 0.2)]
    camB = cam_push(1.0, 1.05, 540, 1000, 4.8)

    def midB(t):
        m = tp(LB, t, 2, turn=0.35, gx=0.7, gy=0.2, sad=0.5, brow=0.5, furrow=0.4, armL="relaxed", armR="relaxed" if t < 1.5 else "chest", wind=0.1,
               cloak_len=0.9)
        g = P(turn=-0.35, gx=-0.8, gy=-0.1, furrow=0.6, brow=0.2, armL="relaxed", armR="relaxed", blink=blink_at(t, 3), breathe=math.sin(t * 2))
        return at_feet(MANUCHEHR, m, t, 330, 1560, 0.42) + at_feet(GENERAL, g, t, 770, 1560, 0.42) + table(1330)
    B = Shot(4.8, room, midB, cam=camB, light=LAMPL, grade="fire", bloom=0.6,
             fx=[Glow(lambda t: cam_xy(camB, t, 540, 520), 260, (255, 170, 90), 0.4)])

    roomb = bgs.cached("war_room_b7", lambda: bgs.cached("war_room", bgs.war_room).filter(ImageFilter.GaussianBlur(7)))
    # C: the general: "Then ask for peace, my king. His men are tired too."
    LC = [("p1s4b", 0.2)]
    camC = cam_push(1.0, 1.04, 540, 860, 4.2)

    def midC(t):
        q = tp(LC, t, 3, turn=-0.25, gx=-0.6, gy=0.0, furrow=0.5, brow=0.3, armL="offer" if 1.0 < t < 3.4 else "relaxed", armR="relaxed", wind=0.1)
        return at_neck(GENERAL, q, t, 540, 960, 1.0)
    C = Shot(4.2, roomb, midC, cam=camC, light=LAMPC, grade="fire", bloom=0.5)

    # D: Manuchehr: "Send a messenger to Afrasiab."
    LD = [("p1s4c", 0.2)]
    camD = cam_push(1.0, 1.04, 540, 860, 3.2)

    def midD(t):
        q = tp(LD, t, 4, turn=0.25, gx=0.6, gy=0.1, furrow=0.6, brow=0.2, sad=0.3, nod=6 * ease((t - 0.1) / 0.4), armL="relaxed", armR="relaxed", wind=0.1)
        return at_neck(MANUCHEHR, q, t, 540, 960, 1.0)
    D = Shot(3.2, roomb, midD, cam=camD, light=dict(LAMPC, rim=(5, -2), ramp=(0, W, 0.86, 1.06)), grade="fire", bloom=0.5, fade_out=0.3)
    return [A, B, C, D]


# ================================================================ S5 Turan's camp; Afrasiab (52.8-85.2)
def s5():
    def camp_night():
        im = bgs.cached("army_camp", bgs.army_camp)
        out = Image.alpha_composite(im, Image.new("RGBA", im.size, (8, 10, 30, 175)))
        out.alpha_composite(svg_render(bgs.stars(501, 120, 700)))
        return out.filter(ImageFilter.GaussianBlur(6))
    campn = bg("camp_night_b6", camp_night)
    # A: a tired soldier of Turan by a fire: "So many years in these cold mountains… I want to go home."
    LA = [("p1s5g", 0.3)]
    camA = cam_push(1.0, 1.05, 540, 860, 4.6)

    def midA(t):
        q = tp(LA, t, 1, turn=0.3, gx=0.5, gy=0.4, sad=0.7, brow=0.6, furrow=-0.2, armL="chest", armR="relaxed", wind=0.3)
        return at_neck(TURAN_SOLDIER, q, t, 600, 980, 0.95) + fire_svg(140, 1500, 90, t, seed=5)
    A = Shot(4.6, campn, midA, cam=camA, light=FIREL, grade="fire", bloom=0.6, fade_in=0.3,
             fx=[Glow(lambda t: cam_xy(camA, t, 140, 1350), 420, (255, 150, 70), 0.45), Embers(30, 502, (40, 900, 260, 1450), (60, 150))])

    tent = bgs.cached("command_tent", bgs.command_tent)
    tentb = bgs.cached("command_tent_b6", lambda: bgs.cached("command_tent", bgs.command_tent).filter(ImageFilter.GaussianBlur(6)))

    def tent_wide(t, lines_a=(), laugh=0.0, bow=0.4, seed=0, lines_m=()):
        o = ""
        for k, (S, x) in enumerate(((TURAN_SOLDIER, 110), (TURAN_SOLDIER_2, 980))):
            q = P(turn=0.35 if x < 540 else -0.35, gx=0.6 if x < 540 else -0.6, gy=-0.1, furrow=0.6 - laugh, smile=0.6 * laugh,
                  mouth_o=0.4 * laugh * max(0.0, math.sin(t * 9 + k)), armL=(20, 10), propL="spear", armR="relaxed", blink=blink_at(t, 50 + k))
            o += at_feet(S, q, t, x, 1560, 0.4)
        ad = P(turn=-0.2, gx=-0.6, gy=0.0, furrow=0.2, smile=0.4 * laugh, mouth_o=0.3 * laugh * max(0.0, math.sin(t * 8 + 2)), armL="chest", armR="chest",
               blink=blink_at(t, 53))
        o += at_feet(ADVISOR, ad, t, 860, 1500, 0.38)
        af = tp(list(lines_a), t, 5 + seed, turn=-0.3, gx=-0.7, gy=0.1, furrow=0.3 - 0.4 * laugh, brow=0.2, smile=0.4 + 0.5 * laugh,
                armL="hip", armR="relaxed" if laugh < 0.5 else "fist_up", wind=0.2)
        if laugh > 0:
            af["mouth_o"] = max(af["mouth_o"], laugh * (0.45 + 0.3 * math.sin(t * 11)))
            af["nod"] = af.get("nod", 0) - 8 * laugh * abs(math.sin(t * 5.5))
        o += at_feet(AFRASIAB, af, t, 680, 1540, 0.44)
        ms = tp(list(lines_m), t, 9, turn=0.35, gx=0.7, gy=-0.2 + 0.8 * bow, nod=16 * bow, brow=0.6, furrow=-0.3, sad=0.2, armL="chest", armR="chest")
        o += at_feet(MESSENGER, ms, t, 320, 1560, 0.42)
        return o
    # B: the messenger: "Great king, King Manuchehr asks for peace."
    LB = [("p1s5a", 0.2)]
    camB = cam_push(1.0, 1.05, 540, 1060, 4.2)

    def midB(t):
        return tent_wide(t, bow=0.2 + 0.5 * ease((t - 2.6) / 0.6), lines_m=LB)
    B = Shot(4.2, tent, midB, cam=camB, light=TENTL, grade="fire",
             bloom=0.5, fx=[Glow(lambda t: cam_xy(camB, t, 250, 610), 200, (255, 170, 90), 0.35), Glow(lambda t: cam_xy(camB, t, 840, 610), 200, (255, 170, 90), 0.35)])

    # C: Afrasiab, close, laughing: "Peace? Ha! Now that he is hungry, he wants peace!"
    LC = [("p1s5b", 0.2)]
    camC = cam_push(1.0, 1.05, 540, 860, 4.0)

    def midC(t):
        ha = ease((t - 0.7) / 0.2) * (1 - ease((t - 1.5) / 0.3))
        q = tp(LC, t, 6, turn=-0.1, gx=-0.3, gy=0.0, furrow=-0.2, brow=0.5, smile=0.7, armL="hip", armR="relaxed", wind=0.15)
        q["mouth_o"] = max(q["mouth_o"], 0.6 * ha)
        q["nod"] -= 8 * ha
        return at_neck(AFRASIAB, q, t, 540, 960, 1.0)
    C = Shot(4.0, tentb, midC, cam=camC, light=TENTL, grade="fire", bloom=0.5)

    # D: the advisor: "My king, our men are tired too. They want to go home."
    LD = [("p1s5h", 0.2)]
    camD = cam_push(1.0, 1.04, 540, 860, 4.8)

    def midD(t):
        q = tp(LD, t, 7, turn=-0.25, gx=-0.6, gy=0.1, brow=0.6, furrow=-0.2, sad=0.3, armL="chest", armR="chest", nod=6, wind=0.1)
        return at_neck(ADVISOR, q, t, 540, 960, 1.0)
    D = Shot(4.8, tentb, midD, cam=camD, light=dict(TENTL, rim=(5, -2), ramp=(0, W, 0.88, 1.05)), grade="fire", bloom=0.5)

    # E: Afrasiab decides: "Very well. Tell your king to shoot one arrow." … "Where it falls, there will be the border." … "Before it, Iran. After it, Turan."
    LE = [("p1s5c", 0.2), ("p1s5d", 3.8), ("p1s5e", 7.0)]
    camE = cam_push(1.0, 1.08, 540, 860, 10.6)

    def midE(t):
        sly = ease((t - 0.1) / 0.5)
        armR, armL = "relaxed", "hip"
        if 0.6 < t < 3.2:
            armR = "offer"                              # "one arrow"
        elif 7.0 < t < 8.4:
            armR = "point"                              # "before it, Iran"
        elif 8.4 < t < 10.0:
            armL = "point"                              # "after it, Turan"
        q = tp(LE, t, 8, turn=-0.1, gx=-0.2, gy=0.0, furrow=0.3, brow=0.2 + 0.3 * sly, smile=0.3 * sly, armL=armL, armR=armR, wind=0.15)
        return at_neck(AFRASIAB, q, t, 540, 960, 1.0)
    E = Shot(10.6, tentb, midE, cam=camE, light=TENTL, grade="fire", bloom=0.5)

    # F: wide: "One arrow! How far can one arrow fly?" — they all laugh
    LF = [("p1s5f", 0.2)]
    camF = cam_push(1.0, 1.06, 540, 1060, 4.2)
    LT = A1.LAUGH - 81.0

    def midF(t):
        laugh = ease((t - LT + 0.2) / 0.3) * (1 - ease((t - LT - 2.4) / 0.4))
        return tent_wide(t, lines_a=LF, laugh=laugh, bow=0.4 + 0.4 * ease((t - 3.0) / 0.5), seed=1)
    F = Shot(4.2, tent, midF, cam=camF, light=TENTL, grade="fire", bloom=0.5, fade_out=0.4,
             fx=[Glow(lambda t: cam_xy(camF, t, 250, 610), 200, (255, 170, 90), 0.35), Glow(lambda t: cam_xy(camF, t, 840, 610), 200, (255, 170, 90), 0.35)])
    return [A, B, C, D, E, F]


# ================================================================ S6 "Who can shoot that arrow?" — Arash (85.2-121.4)
def s6():
    yard = bg("fort_yard_dusk", lambda: abg.fort_yard("dusk"))
    yardb = bg("fort_yard_dusk", lambda: abg.fort_yard("dusk"), 7)
    heads = bgs.cached("ar_p01_yard_heads", lambda: back_heads(601, 9, 1780, 0.6, col="#1a1216", blur=3))
    side = [(IRAN_SOLDIER, 110, 1520, 0.38, 1), (IRAN_SOLDIER_3, 220, 1470, 0.35, 1), (IRAN_SOLDIER_2, 860, 1470, 0.35, -1),
            (IRAN_SOLDIER, 970, 1520, 0.38, -1)]

    def soldiers(t, look_down=0.0, part=0.0):
        o = ""
        for k, (S, x, y, s, sd) in enumerate(side):
            q = P(turn=0.3 * sd, gx=0.6 * sd, gy=-0.3 + 1.0 * look_down, brow=0.5, furrow=0.2, sad=0.3 * look_down, armL=(20, 10), propL="spear",
                  armR="relaxed", blink=blink_at(t, 60 + k), breathe=math.sin(t * 2 + k), wind=0.4)
            o += at_feet(S, q, t, x - sd * 40 * part, y, s)
        return o
    # A: Manuchehr before his soldiers: "One arrow… for all of Iran."
    LA = [("p1s6a", 0.3)]
    camA = cam_push(1.0, 1.05, 540, 1100, 4.6)

    def midA(t):
        m = tp(LA, t, 1, turn=0.0, gx=0.0, gy=0.1, sad=0.4, brow=0.5, furrow=0.4, armL="relaxed", armR="relaxed", wind=0.3)
        return soldiers(t) + at_feet(MANUCHEHR, m, t, 540, 1440, 0.4)
    A = Shot(4.6, yard, midA, fg=heads, cam=camA, light=DUSKL, sun=SUN_DUSK, fade_in=0.3)

    # B: Manuchehr, close: "Who can shoot that arrow?"
    LB = [("p1s6b", 0.2)]
    camB = cam_push(1.0, 1.05, 540, 860, 3.4)

    def midB(t):
        q = tp(LB, t, 2, turn=0.05, gx=0.1 + 0.5 * math.sin(t * 0.9), gy=-0.1, sad=0.3, brow=0.6, furrow=0.2, armL="relaxed", armR="offer" if t > 0.4 else "relaxed",
               wind=0.3)
        return at_neck(MANUCHEHR, q, t, 540, 960, 1.0)
    B = Shot(3.4, yardb, midB, cam=camB, light=DUSKL, sun=SUN_DUSK)

    # C: silence; the soldiers look down; one whispers: "No one can shoot that far…"
    LC = [("p1s6e", 1.4)]
    camC = cam_push(1.0, 1.04, 540, 860, 5.0)

    def midC(t):
        o = ""
        for k, (S, x, s) in enumerate(((IRAN_SOLDIER_2, 250, 0.7), (IRAN_SOLDIER, 820, 0.7))):
            lines = LC if k == 0 else []
            q = tp(lines, t, 10 + k, turn=0.3 if x < 540 else -0.3, gx=0.5 if x < 540 else -0.5, gy=0.7, brow=0.6, furrow=-0.2, sad=0.6,
                   armL=(20, 10), propL="spear", armR="relaxed", wind=0.3)
            o += at_neck(S, q, t, x, 1000, s)
        return o
    C = Shot(5.0, yardb, midC, cam=camC, light=DUSKL, sun=SUN_DUSK)

    # D: Arash comes forward through the soldiers: "I can, my king."
    LD = [("p1s6c", A1.LINES[[l for l, _ in A1.LINES].index("p1s6c")][1] - 98.2)]
    camD = cam_push(1.0, 1.06, 540, 1100, 4.4)
    WALK = (0.2, 2.4)

    def midD(t):
        u = ease((t - WALK[0]) / (WALK[1] - WALK[0]))
        walking = WALK[0] < t < WALK[1]
        q = tp(LD, t, 3, turn=0.0, gx=0.0, gy=-0.3, brow=0.1, furrow=0.2, smile=0.0, armL=("ik", 340, 220, "down"), propL="bow", armR="relaxed",
               legs="walk" if walking else "stand", phase=t * 5.2, wind=0.5)
        return soldiers(t, look_down=0.3 * (1 - u), part=u) + at_feet(ARASH, q, t, 540, lerp(1330, 1480, u), lerp(0.3, 0.4, u))
    D = Shot(4.4, yard, midD, fg=heads, cam=camD, light=DUSKL, sun=SUN_DUSK)

    # E: Manuchehr, moved: "This arrow must fly farther than any arrow ever flew."
    LE = [("p1s6g", 0.2)]
    camE = cam_push(1.0, 1.05, 540, 860, 5.2)

    def midE(t):
        q = tp(LE, t, 4, turn=-0.15, gx=-0.4, gy=0.2, sad=0.4, brow=0.7, furrow=-0.2, smile=0.15, armL="relaxed", armR="relaxed", wind=0.3)
        return at_neck(MANUCHEHR, q, t, 540, 960, 1.0)
    E = Shot(5.2, yardb, midE, cam=camE, light=DUSKL, sun=SUN_DUSK)

    # F: Arash, close: "I know, my king." — "His name was Arash. And he knew what this arrow would cost him." (end card from 8.2)
    LF = [("p1s6h", 0.2)]
    camF = cam_push(1.0, 1.1, 540, 860, 13.6)

    def midF(t):
        q = tp(LF, t, 5, turn=0.15, gx=0.4 - 0.5 * ease((t - 2.2) / 0.8), gy=0.0 - 0.3 * ease((t - 2.2) / 0.8), brow=0.2, furrow=0.1, smile=0.1,
               armL=("ik", 340, 220, "down"), propL="bow", armR="relaxed", wind=0.5)
        return at_neck(ARASH, q, t, 540, 960, 1.0)
    F = Shot(13.6, yardb, midF, cam=camF, light=dict(DUSKL, rim_str=1.0), sun=SUN_DUSK, fade_out=0.8,
             fx=[Motes(40, 602, (255, 220, 190), (0, 300, W, 1300), (-8, -4), amax=80)])
    return [A, B, C, D, E, F]


SCENES = {"s1": s1, "s2": s2, "s3": s3, "s4": s4, "s5": s5, "s6": s6}
