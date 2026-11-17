"""Part 4 · The Two Cooks — 2D cartoon. Timing matches zahhak/p04_audio.py
(scene starts s1 0, s2 7.4, s3 12.0, s4 33.0, s5 60.6, s6 89.0; end card 116.2; total 121.2)."""
import math, random
from PIL import Image, ImageFilter, ImageDraw
from film import Shot, W, H, ease, lerp, talk_pose, blink_at, cam_push, cam_static, Motes, Embers, svg_render
from chars import pose, Ctx, FEET, fmt, prop, goat, hand
from stage import at_neck, at_feet, lying_at, Glow, lw_for, fire_svg, random_spec
import bgs, zbg
from cast import *
from p01_scenes import P, bg, cam_xy, tp, darken, torch_flame, hall_fx, placed, flipped, TORCH, HALL, NIGHT
from p02_scenes import glint, eyes_of, court, steam, platter
from p03_scenes import night_of, shadow_fx, svg_fx, torches_wide

KITCH = dict(point=(320, 1080, 1000, 0.62, 1.15, (1.0, 0.55, 0.25)), rim_point=(320, 6), rim_col=(1.0, 0.62, 0.3), rim_str=0.9)
KNIGHT = dict(ambient=(0.7, 0.66, 0.8), point=(300, 1100, 1000, 0.6, 1.15, (1.0, 0.55, 0.25)), rim_point=(300, 6), rim_col=(1.0, 0.62, 0.3), rim_str=0.9)
KCLOSE = dict(ambient=(0.76, 0.7, 0.82), rim=(-5, -2), rim_col=(1.0, 0.62, 0.3), rim_str=0.9, ramp=(0, W, 1.08, 0.82))
DOORLIGHT = dict(ambient=(0.66, 0.68, 0.86), rim=(5, -2), rim_col=(0.75, 0.82, 1.0), rim_str=0.7, ramp=(0, W, 0.86, 1.04))
HOME = dict(point=(230, 1180, 900, 0.5, 1.15, (1.0, 0.55, 0.25)), rim_point=(230, 6), rim_col=(1.0, 0.65, 0.3))
HOMECLOSE = dict(rim=(-6, -2), rim_col=(1.0, 0.65, 0.35), ramp=(0, W, 1.08, 0.82), ambient=(0.9, 0.84, 0.82))
DOOR = (800, 1010, 1040, 1620)          # the kitchen's back door: x0, x1, arch top, sill


def kitchen_night():
    return Image.alpha_composite(bg("kitchen", zbg.kitchen), Image.new("RGBA", (W, H), (10, 8, 22, 120)))


def back_door(t, open_=1.0):
    """the back door of the kitchen (drawn over the brick wall at the right): a dark night outside, the door swung in"""
    x0, x1, top, sill = DOOR
    mid = (x0 + x1) / 2
    o = (f'<path d="M {x0 - 24} {sill} L {x0 - 24} {top + 70} Q {mid} {top - 70}, {x1 + 24} {top + 70} L {x1 + 24} {sill} Z" fill="#4a2a18" stroke="#1e1008" stroke-width="5"/>'
         f'<path d="M {x0} {sill} L {x0} {top + 80} Q {mid} {top - 40}, {x1} {top + 80} L {x1} {sill} Z" fill="#0e1430"/>')
    r = random.Random(4)
    for k in range(14):
        sx, sy = r.uniform(x0 + 10, x1 - 10), r.uniform(top + 40, sill - 300)
        o += f'<circle cx="{sx:.0f}" cy="{sy:.0f}" r="{r.uniform(1.2, 2.6):.1f}" fill="#ffffff" opacity="{0.5 + 0.4 * math.sin(t * 2 + k):.2f}"/>'
    o += f'<path d="M {x0} {sill - 220} C {x0 + 60} {sill - 260}, {x1 - 60} {sill - 250}, {x1} {sill - 230} L {x1} {sill} L {x0} {sill} Z" fill="#141c34"/>'
    w = (x1 - x0) * (1 - 0.82 * open_)
    o += (f'<path d="M {x1} {top + 80} L {x1 - w:.1f} {top + 60 + 40 * open_:.1f} L {x1 - w:.1f} {sill + 30 * open_:.1f} L {x1} {sill} Z" fill="#6a3e22" stroke="#1e1008" stroke-width="4"/>'
          f'<path d="M {x1 - w * 0.5:.1f} {top + 90:.1f} L {x1 - w * 0.5:.1f} {sill:.1f}" stroke="#4a2a14" stroke-width="4"/>')
    return o


def moon_spill(cam):
    """moonlight on the floor in front of the open back door (an unlit layer behind the cast)"""
    x0, x1, top, sill = DOOR
    return svg_fx(cam, lambda t: f'<path d="M {x0} {sill} L {x1} {sill} L {x1 - 120} {sill + 300} L {x0 - 330} {sill + 300} Z" fill="#9ab0ff" opacity="0.16"/>')


def kitchen_fire(t):
    return fire_svg(300, 1176, 80, t, 2) + steam(320, 820, t, 4, 260, 5)


def tear(x, y, t, t0, s=1.0):
    """a tear running down from (x, y) after t0"""
    u = (t - t0) % 2.2 / 2.2 if t > t0 else -1
    if u < 0:
        return ""
    return (f'<path d="M {x:.1f} {y + 70 * u * s:.1f} c {-7 * s:.1f} {12 * s:.1f}, {-7 * s:.1f} {20 * s:.1f}, 0 {22 * s:.1f} c {7 * s:.1f} {-2 * s:.1f}, {7 * s:.1f} {-10 * s:.1f}, 0 {-22 * s:.1f} Z" '
            f'fill="#cfe6ff" opacity="{0.85 * (1 - u):.2f}" stroke="#6a8ab0" stroke-width="1.2"/>')


def cooks_close(t, LA, LB, seeds=(1, 2), sad=0.0, tears_t=None, look_each=True):
    """Garmayel (left) and Armayel (right), close, by the fire"""
    g = tp(LA, t, seeds[0], turn=0.35, gx=0.7 if look_each else 0.2, gy=0.1, brow=0.3 + 0.4 * sad, furrow=0.2 - 0.6 * sad, sad=sad, armL="relaxed", armR="relaxed")
    a = tp(LB, t, seeds[1], turn=-0.35, gx=-0.7 if look_each else -0.2, gy=0.1, brow=0.3 + 0.4 * sad, furrow=0.3 - 0.6 * sad, sad=sad, armL="relaxed", armR="relaxed")
    o = at_neck(GARMAYEL_COOK, g, t, 330, 1010, 1.0) + at_neck(ARMAYEL_COOK, a, t, 770, 1030, 1.02)
    if tears_t is not None:
        for (x, y, s_, sd, k) in ((330, 1010, 1.0, 0.35, 0), (770, 1030, 1.02, -0.35, 1)):
            ex, ey = eyes_of(x, y, s_, sd)[1 if sd < 0 else 0]
            o += tear(ex, ey + 18, t, tears_t + 0.6 * k, 1.0)
    return o


# ================================================================ S1 the hook (0-7.4)
def s1():
    kn = bgs.cached("zh_kitchen_night", kitchen_night)
    knb = bgs.cached("zh_kitchen_night_b6", lambda: kn.filter(ImageFilter.GaussianBlur(6)))
    camA = cam_push(1.0, 1.05, 540, 880, 4.6)
    LA = [("p4s1a", 0.6)]

    def midA(t):
        return cooks_close(t, LA, [], seeds=(1, 2), sad=0.3)
    A = Shot(4.6, knb, midA, cam=camA, light=KCLOSE, grade="fire", bloom=0.6, fade_in=0.5,
             fx=[Glow(lambda t: cam_xy(camA, t, 60, 1150), 300, (255, 160, 80), 0.45)])

    camB = cam_push(1.0, 1.04, 540, 1200, 2.8)

    def midB(t):
        g = tp([], t, 3, turn=0.35, gx=0.8, gy=0.0, sad=0.3, armL="relaxed", armR="relaxed")
        a = tp([], t, 4, turn=-0.35, gx=-0.8, gy=0.0, sad=0.3, armL="relaxed", armR="relaxed")
        return kitchen_fire(t) + at_feet(GARMAYEL_COOK, g, t, 600, 1660, 0.44) + at_feet(ARMAYEL_COOK, a, t, 790, 1670, 0.45)
    B = Shot(2.8, kn, midB, cam=camB, light=KNIGHT, fx=[Embers(30, 41, (180, 900, 440, 1170), (60, 150))], grade="fire", bloom=0.6, fade_out=0.6)
    return [A, B]


# ================================================================ S2 title (7.4-12.0): the back door at night
def s2():
    kn = bgs.cached("zh_kitchen_night", kitchen_night)
    cam = cam_push(1.04, 1.12, 760, 1250, 4.6)

    def mid(t):
        return kitchen_fire(t) + back_door(t, 0.7)
    return [Shot(4.6, kn, mid, cam=cam, light=KNIGHT, pre_fx=[moon_spill(cam)], fx=[Embers(30, 42, (180, 900, 440, 1170), (60, 150))],
                 grade="fire", bloom=0.7, fade_in=0.4, fade_out=0.5)]


# ================================================================ S3 a thousand years; two young men every night (12.0-33.0)
def s3():
    hall = bg("hall", zbg.hall)
    camA = cam_push(1.0, 1.08, 540, 980, 7.6)

    def midA(t):
        z = tp([], t, 5, legs="sit", turn=0.0, gx=0.0, gy=0.3, furrow=0.7, brow=-0.1, armL="relaxed", armR="relaxed",
               snake_looks=(0.6 + 0.4 * math.sin(t * 1.1), 0.5 + 0.5 * math.sin(t * 1.3 + 1)),
               hisses=(0.5 * max(0.0, math.sin(t * 1.6)), 0.5 * max(0.0, math.sin(t * 1.4 + 2))))
        return torches_wide(t) + at_neck(ZAHHAK_KING, z, t, 540, 793, 0.36) + court(t, bow=1.0, seed=5)
    A = Shot(7.6, hall, midA, cam=camA, light=HALL, fx=hall_fx(camA, [(80, 640), (1000, 640)], 21), grade="fire", bloom=0.6, fade_in=0.4)

    wall = bgs.cached("shadow_wall", bgs.shadow_wall)
    camB = cam_push(1.0, 1.04, 540, 900, 4.6)

    def shadowB(t):
        o = ""
        for k, (S, dx, kind) in enumerate(((ZGUARD, 0, "g"), (YOUNG_MAN, 230, "y"), (YOUNG_MAN_2, 430, "y"), (ZGUARD, 640, "g"))):
            x = 1150 + dx - 190 * t
            ph = t * 5.0 + k
            if kind == "g":
                q = P(legs="walk", phase=ph, turn=-0.45, gx=-0.9, armL=(20, 10), propL="pike", armR="relaxed", blink=0.0)
            else:
                q = P(legs="walk", phase=ph, turn=-0.45, gx=-0.9, armL=("ik", 50, 330), armR=("ik", -50, 330), chains="rope", blink=0.0, sad=0.8)
            o += at_feet(S, q, t, x, 1690, 0.72)
        return o
    B = Shot(4.6, wall, None, cam=camB, pre_fx=[shadow_fx(camB, shadowB, a=0.8, blur=3)], grade="fire", bloom=0.4, fx=[darken(0.25, -1.0, 9.0, (10, 4, 2))])

    door = bgs.cached("zh_house_door_night", night_of(lambda: bgs.cached("house_door", bgs.house_door), (6, 10, 30), 170))
    camC = cam_push(1.0, 1.04, 470, 900, 3.4)
    LC = [("p4s3c", 0.3)]
    lanC = lambda t: cam_xy(camC, t, 430 + 0.85 * 160, 760 + 0.85 * 560)

    def midC(t):
        m = tp(LC, t, 6, turn=-0.35, gx=-0.9, gy=-0.1, sad=0.9, brow=0.9, furrow=-0.5, armR="reach", armL="hold_lantern", propL="lantern", wind=0.4)
        return at_neck(POOR_MOTHER, m, t, 430, 760, 0.85)
    C = Shot(3.4, door, midC, cam=camC, light=dict(NIGHT, rim=(5, -2), rim_col=(1.0, 0.75, 0.45), rim_str=0.6),
             fx=[Glow(lanC, 230, (255, 190, 110), 0.5)], grade="night")

    camD = cam_push(1.0, 1.07, 480, 1000, 5.4)
    ground = 1300

    def midD(t):
        m = tp([], t, 7, legs="sit", turn=-0.3, gx=-0.8, gy=0.2, sad=0.9, brow=0.6, furrow=-0.4, armL="chest", armR="relaxed")
        c = Ctx(lw_for(0.7))
        return (at_neck(POOR_MOTHER, m, t, 470, ground - 575 * 0.95 * 0.72, 0.72) +
                f'<g transform="translate(700,{ground - 80}) scale(0.7)">{prop(c, "lantern", 0, 0, 0, t)}</g>')
    D = Shot(5.4, door, midD, cam=camD, light=dict(NIGHT, rim=(5, -2), rim_col=(1.0, 0.75, 0.45), rim_str=0.6),
             fx=[Glow(lambda t: cam_xy(camD, t, 700, ground - 20), 200, (255, 190, 110), 0.4 * (1.0)),
                 Motes(30, 43, (220, 230, 255), (0, 200, W, 900), (3, 2), amax=70)], grade="night", fade_out=0.8)
    return [A, B, C, D]


# ================================================================ S4 Armayel and Garmayel (33.0-60.6)
def s4():
    room = bgs.cached("interior", bgs.interior)
    roomb = bgs.cached("zh_interior_b9", lambda: room.filter(ImageFilter.GaussianBlur(9)))

    camA = cam_push(1.0, 1.06, 560, 1150, 6.2)
    LA = [("p4s4a", 0.4)]

    def midA(t):
        pace = math.sin(t * 0.9)
        a = tp([], t, 8, turn=0.3 * pace, gx=0.6 * pace, gy=0.0, furrow=0.8, brow=0.2, sad=0.3, armL="hip", armR="relaxed",
               legs="walk" if abs(math.cos(t * 0.9)) > 0.4 else "stand", phase=t * 4)
        g = tp([], t, 9, turn=-0.3, gx=-0.6, gy=0.3, furrow=0.3, brow=0.3, sad=0.3, armL="relaxed", armR="chest")
        return fire_svg(230, 1300, 62, t) + at_feet(ARMAYEL, a, t, 470 + 50 * pace, 1520, 0.5) + at_feet(GARMAYEL, g, t, 790, 1500, 0.48)
    A = Shot(6.2, room, midA, cam=camA, light=HOME, fx=[Embers(20, 44, (170, 1100, 290, 1290), (40, 100))], grade="fire", fade_in=0.4)

    LB = [("p4s4b", 0.2)]

    def midB(t):
        a = tp(LB, t, 10, turn=0.3, gx=0.6, gy=0.0, furrow=1.0, brow=-0.2, sad=0.3, armL=("ik", 120, 230, "down") if t > 1.4 else "relaxed", armR="relaxed")
        return at_neck(ARMAYEL, a, t, 500, 1040, 1.3)
    B = Shot(3.4, roomb, midB, cam=cam_push(1.0, 1.04, 500, 860, 3.4), light=HOMECLOSE, sun=(0, 1100, 700, (0.12, 0.06, 0.02)), grade="fire")

    LC = [("p4s4c", 0.2)]

    def midC(t):
        g = tp(LC, t, 11, turn=-0.3, gx=-0.6, gy=0.1, furrow=0.2, brow=0.4, smile=0.2 * ease((t - 2.0) / 0.6), armL="relaxed",
               armR="offer" if 1.8 < t < 3.8 else "relaxed")
        return at_neck(GARMAYEL, g, t, 580, 1040, 1.3)
    C = Shot(4.2, roomb, midC, cam=cam_push(1.0, 1.04, 580, 860, 4.2), light=HOMECLOSE, sun=(0, 1100, 700, (0.12, 0.06, 0.02)), grade="fire")

    LDa = [("p4s4d", 0.2), ("p4s4g", 5.2)]
    LDg = [("p4s4e", 2.4), ("p4s4h", 7.2)]

    def midD(t):
        a = tp(LDa, t, 12, turn=0.35, gx=0.8, gy=0.0, furrow=0.6 if t < 4.5 else 0.2, brow=0.7 if t < 2.4 else 0.4, sad=0.2 + 0.3 * (t > 5.0),
               armL="relaxed", armR="relaxed")
        g = tp(LDg, t, 13, turn=-0.35, gx=-0.8, gy=0.0, furrow=0.1, brow=0.3, smile=0.3 if t > 7.2 else 0.15, armL="relaxed",
               armR=("ik", -260, 200, "down") if t > 7.6 else "relaxed")
        return at_neck(ARMAYEL, a, t, 330, 1000, 0.95) + at_neck(GARMAYEL, g, t, 760, 1010, 0.92)
    D = Shot(9.4, roomb, midD, cam=cam_push(1.0, 1.08, 540, 860, 9.4), light=HOMECLOSE, sun=(0, 1100, 700, (0.12, 0.06, 0.02)), grade="fire")

    kit = bg("kitchen", zbg.kitchen)

    def midH(t):
        st = math.sin(t * 4.0)
        hx, hy = -320 + 40 * st, 60 + 16 * math.cos(t * 4.0)
        a = tp([], t, 14, turn=-0.35, gx=-0.6, gy=0.5, smile=0.2, brow=0.2, furrow=0.3, armR=("ik", hx, hy), armL="relaxed")
        wx, wy = 660 + hx * 0.7, 817 + hy * 0.7
        ladle = f'<path d="M {wx:.1f} {wy:.1f} L {wx - 120:.1f} {wy + 60:.1f}" stroke="#5a3a1c" stroke-width="9" stroke-linecap="round"/>'
        u = ease(t / 3.0)
        g = tp([], t, 15, turn=-0.4, gx=-0.8, gy=0.2, smile=0.2, brow=0.2, armR="hold_bread", propR="bread", armL="relaxed",
               legs="walk" if t < 3.0 else "stand", phase=t * 5.2)
        return kitchen_fire(t) + ladle + at_neck(ARMAYEL_COOK, a, t, 660, 817, 0.7) + at_feet(GARMAYEL_COOK, g, t, lerp(1180, 930, u), 1770, 0.67)
    Hs = Shot(4.4, kit, midH, cam=cam_push(1.0, 1.05, 560, 950, 4.4), light=KITCH, fx=[Embers(30, 45, (180, 900, 440, 1170), (60, 150))],
              grade="fire", bloom=0.6, fade_out=0.5)
    return [A, B, C, D, Hs]


# ================================================================ S5 the kitchen at night (60.6-89.0)
def s5():
    kn = bgs.cached("zh_kitchen_night", kitchen_night)
    knb = bgs.cached("zh_kitchen_night_b6", lambda: kn.filter(ImageFilter.GaussianBlur(6)))

    camA = cam_push(1.0, 1.04, 540, 1200, 4.4)

    def midA(t):
        o = kitchen_fire(t)
        turn_ = ease((t - 0.3) / 0.5)
        for k, (S, x, y, s_) in enumerate(((GARMAYEL_COOK, 640, 1650, 0.44), (ARMAYEL_COOK, 820, 1665, 0.45))):
            q = tp([], t, 16 + k, turn=-0.45 * turn_ + 0.3 * (1 - turn_), gx=-0.9 * turn_, gy=0.0, brow=0.6 * turn_, sad=0.4 * turn_, furrow=0.3,
                   armL="relaxed", armR="relaxed")
            o += at_feet(S, q, t, x, y, s_)
        u = ease(t / 2.4)
        walking = t < 2.4
        for k, (S, x0, x1, y, s_, kind) in enumerate(((ZGUARD, -420, -60, 1720, 0.48, "g"), (YOUNG_MAN, -260, 160, 1700, 0.46, "y"),
                                                      (YOUNG_MAN_2, -120, 330, 1690, 0.45, "y"), (ZGUARD, -560, 30, 1760, 0.5, "g"))):
            ph = t * 5.2 + k
            if kind == "g":
                q = tp([], t, 18 + k, turn=0.4, gx=0.8, furrow=0.9, brow=-0.2, armL=(20, 10), propL="pike", armR="forward" if walking else "relaxed",
                       legs="walk" if walking else "stand", phase=ph)
            else:
                q = tp([], t, 18 + k, turn=0.35 if t < 2.6 else -0.2, gx=0.7, gy=0.0, sad=0.9, brow=0.9, furrow=-0.5, chains="rope",
                       armL=("ik", 50, 330), armR=("ik", -50, 330), legs="walk" if walking else "stand", phase=ph)
            o += at_feet(S, q, t, lerp(x0, x1, u), y, s_)
        return o
    A = Shot(4.4, kn, midA, cam=camA, light=KNIGHT, fx=[Embers(30, 46, (180, 900, 440, 1170), (60, 150))], grade="fire", bloom=0.6)

    LB = [("p4s5b", 0.2)]

    def midB(t):
        q = tp(LB, t, 22, turn=0.25, gx=0.6, gy=0.0, furrow=1.0, brow=-0.4, smile=0.25, armR="point" if t > 0.6 else "relaxed", armL="relaxed")
        return at_neck(ZGUARD, q, t, 500, 1050, 1.25)
    B = Shot(2.2, knb, midB, cam=cam_push(1.0, 1.04, 500, 860, 2.2), light=KCLOSE, grade="fire", bloom=0.5,
             fx=[Glow(lambda t: (60, 1150), 300, (255, 160, 80), 0.45)])

    camC = cam_push(1.0, 1.07, 540, 880, 7.8)

    def midC(t):
        return cooks_close(t, [], [], seeds=(23, 24), sad=0.4 + 0.5 * ease((t - 2.0) / 1.0), tears_t=4.4)
    C = Shot(7.8, knb, midC, cam=camC, light=KCLOSE, grade="fire", bloom=0.6, fx=[Glow(lambda t: cam_xy(camC, t, 60, 1150), 300, (255, 160, 80), 0.45)])

    camD = cam_push(1.3, 1.36, 820, 1320, 4.2)
    LD = [("p4s5d", 0.3)]

    def midD(t):
        g = tp(LD, t, 25, turn=0.4, gx=0.8, gy=0.1, sad=0.4, brow=0.6, furrow=-0.2, armL=("ik", 230, 40), armR="relaxed")
        y = tp([], t, 26, turn=-0.35, gx=-0.8, gy=0.0, sad=0.6, brow=0.8, furrow=-0.4, armL="chest", armR="relaxed")
        return back_door(t, 1.0) + at_feet(GARMAYEL_COOK, g, t, 680, 1660, 0.46) + at_feet(YOUNG_MAN, y, t, 890, 1640, 0.45)
    D = Shot(4.2, kn, midD, cam=camD, bg_par=1.0, light=DOORLIGHT, pre_fx=[moon_spill(camD)], grade="night")

    LE = [("p4s5e", 0.2)]

    def midE(t):
        go = ease((t - 2.0) / 0.9)
        y = tp(LE, t, 27, turn=-0.3 + 0.75 * go, gx=-0.7 + 1.6 * go, gy=0.0, sad=0.5, brow=0.7, furrow=-0.5, smile=0.5 * (1 - go), armL="chest", armR="relaxed")
        return at_neck(YOUNG_MAN, y, t, 560 + 700 * go, 1040, 1.3)
    E = Shot(3.0, knb, midE, cam=cam_push(1.0, 1.04, 560, 860, 3.0), light=DOORLIGHT, grade="night",
             fx=[Glow(lambda t: (1000, 1000), 420, (150, 170, 255), 0.3)])

    tab = bgs.cached("zh_table_cloth_night", lambda: Image.alpha_composite(bg("table_cloth", zbg.table_cloth), Image.new("RGBA", (W, H), (14, 8, 16, 140))))

    def midF(t):
        down = ease((t - 0.6) / 1.2)
        ly = lerp(560, 880, down)
        o = f'<g transform="translate(540,900) scale(1.3) translate(-540,-900)">' + platter(540, 930, 300, "#c8ccd4", "#9aa0aa")
        o += (f'<path d="M 330 {ly:.1f} C 330 {ly - 200:.1f}, 750 {ly - 200:.1f}, 750 {ly:.1f} Z" fill="#d0d4dc" stroke="#2a2a30" stroke-width="5"/>'
              f'<path d="M 380 {ly - 30:.1f} C 400 {ly - 140:.1f}, 520 {ly - 170:.1f}, 600 {ly - 160:.1f}" stroke="#ffffff" stroke-width="10" fill="none" opacity="0.5"/>'
              f'<ellipse cx="540" cy="{ly - 160:.1f}" rx="26" ry="16" fill="#b8bcc6" stroke="#2a2a30" stroke-width="4"/>')
        c = Ctx(1.0)
        o += (f'<path d="M 556 {ly - 214:.1f} L 800 {ly - 640:.1f}" stroke="#1b0f0a" stroke-width="86" stroke-linecap="round"/>'
              f'<path d="M 556 {ly - 214:.1f} L 800 {ly - 640:.1f}" stroke="#7a5a3a" stroke-width="80" stroke-linecap="round"/>'
              f'<circle cx="556" cy="{ly - 214:.1f}" r="40" fill="#a8946e" stroke="#1b0f0a" stroke-width="3"/>')
        o += f'<g transform="translate(540,{ly - 190:.1f}) scale(1.6)">{hand(c, ARMAYEL_COOK, 0, 0, 180, 1)}</g>'
        return o + '</g>'
    F = Shot(4.2, tab, midF, cam=cam_push(1.0, 1.05, 540, 900, 4.2), light=dict(KCLOSE, ramp=None), sun=(100, 900, 700, (0.12, 0.06, 0.02)), grade="fire")

    LG = [("p4s5g", 0.2)]

    def midG(t):
        a = tp(LG, t, 28, turn=0.15, gx=0.3, gy=0.0, furrow=0.6, brow=0.0, smile=0.35 * ease((t - 1.0) / 0.6), armL="relaxed", armR="relaxed")
        return at_neck(ARMAYEL_COOK, a, t, 560, 1040, 1.3)
    camG = cam_push(1.0, 1.04, 560, 860, 2.6)
    G = Shot(2.6, knb, midG, cam=camG, light=KCLOSE, grade="fire", bloom=0.5, fade_out=0.5, fx=[Glow(lambda t: cam_xy(camG, t, 60, 1150), 300, (255, 160, 80), 0.45)])
    return [A, B, C, D, E, F, G]


# ================================================================ S6 the mountains; the scream (89.0-121.2)
def s6():
    kn = bgs.cached("zh_kitchen_night", kitchen_night)
    camA = cam_push(1.3, 1.34, 820, 1320, 3.4)

    def midA(t):
        u = ease((t - 0.4) / 2.4)
        g = tp([], t, 30, turn=0.4, gx=0.8 - 1.6 * (t % 2 > 1), gy=0.0, sad=0.3, brow=0.5, furrow=0.2, armL=("ik", 230, 40), armR="relaxed")
        y = P(legs="walk", phase=t * 5.0, turn=0.45, gx=0.8, armL=("ik", 150, -50), propL="sack", armR="relaxed", sad=0.4, blink=blink_at(t, 31))
        alpha = 1 - ease((t - 2.2) / 0.8)
        body = at_feet(YOUNG_MAN_2, y, t, lerp(760, 960, u), lerp(1680, 1600, u), lerp(0.46, 0.4, u))
        return back_door(t, 1.0) + (f'<g opacity="{alpha:.3f}">{body}</g>' if alpha < 1 else body) + at_feet(GARMAYEL_COOK, g, t, 680, 1660, 0.46)
    A = Shot(3.4, kn, midA, cam=camA, bg_par=1.0, light=DOORLIGHT, pre_fx=[moon_spill(camA)], grade="night", fade_in=0.3)

    ridges = bgs.cached("ridges_dusk", bgs.ridges_dusk)
    r = random.Random(47)
    walkers = []
    for k in range(5):
        S = dict(random_spec(r, ("man",)), head="none", beard=r.choice(["light", "short", None]), hair=r.choice(["short", "teen_curly"]),
                 garment="tunic", col=r.choice(["#6a7f8f", "#8a6a3a", "#5a6a3a", "#7a4a3a", "#4a5a7a"]))
        walkers.append(S)

    def midB(t):
        o = ""
        items = []
        for k in range(10):
            u = (t * 0.035 + k * 0.1) % 1.0
            x = lerp(60, 780, u) + 30 * math.sin(u * 5)
            y = lerp(1760, 1240, u ** 0.9)
            s_ = lerp(0.3, 0.09, u ** 0.8)
            fade = min(1.0, u / 0.06, (1 - u) / 0.12)
            items.append((y, k, x, s_, fade))
        for y, k, x, s_, fade in sorted(items):
            if k % 2 == 0:
                S = walkers[(k // 2) % len(walkers)]
                q = P(legs="walk", phase=t * 5.2 + k, turn=0.4, gx=0.8, gy=-0.3, armL="relaxed", armR=("ik", -100, 200, "down") if k % 4 == 0 else "relaxed",
                      propR="stick" if k % 4 == 0 else None, wind=0.4, blink=blink_at(t, 50 + k))
                body = at_feet(S, q, t, x, y, s_)
            else:
                col = ["#e9e3d6", "#5a4a3e", "#e9e3d6", "#8a7a62"][(k // 2) % 4]
                c = Ctx(lw_for(s_ * 2.4))
                body = flipped(goat(c, col=col, t=t + k, walk=True, phase=t * 6 + k), x, y, s_ * 2.4)
            o += f'<g opacity="{fade:.3f}">{body}</g>' if fade < 1 else body
        return o
    B = Shot(8.2, ridges, midB, cam=cam_push(1.0, 1.06, 540, 1300, 8.2), light=dict(rim=(-5, -3), rim_col=(1.0, 0.65, 0.45), ramp=(0, W, 1.0, 0.86), ambient=(0.86, 0.8, 0.9)),
             sun=(540, 900, 900, (0.12, 0.06, 0.04)), fx=[Motes(40, 48, (255, 200, 160), (0, 400, W, 1300), (-6, -3), amax=70)], fade_in=0.4, fade_out=0.6)

    bed = bg("bedchamber", zbg.bedchamber)
    bedb = bg("bedchamber", zbg.bedchamber, 8)
    camC = cam_push(1.0, 1.08, 540, 1150, 3.8)
    LAMP = dict(ambient=(0.62, 0.6, 0.8), point=(70, 960, 900, 0.6, 1.1, (1.0, 0.55, 0.25)), rim=(5, -3), rim_col=(0.72, 0.82, 1.0), rim_str=0.5)

    def midC(t):
        z = P(blink=1.0, armL="relaxed", armR="relaxed", wind=0.0, breathe=math.sin(t * 1.4), snake_rise=0.55, snake_looks=(-0.6, -0.6),
              hisses=(0.0, 0.0), turn=0.0)
        return torch_flame(70, 975, t, 0.5, 2) + lying_at(ZAHHAK_NIGHT, z, t, 600, 1190, 0.36)
    C = Shot(3.8, bed, midC, cam=camC, light=LAMP, fx=[Glow(lambda t: cam_xy(camC, t, 70, 930), 200, (255, 170, 90), 0.4)], grade="night", fade_in=0.4)

    LD = [("p4s6e", 0.2)]
    camD = cam_push(1.08, 1.0, 540, 860, 2.8)

    def midD(t):
        wake = ease(t / 0.25)
        jit = 6 * math.sin(t * 47) * (1 - ease((t - 1.6) / 0.6))
        z = tp(LD, t, 32, turn=0.05, gx=0.0, gy=-0.4, brow=1.6 * wake, furrow=-0.9 * wake, sad=0.6, armL="both_out" if t > 0.4 else "relaxed",
               armR="both_out" if t > 0.4 else "relaxed", snake_rise=lerp(0.55, 1.0, wake), snake_looks=(1.0, 1.0), hisses=(0.9 * wake, 0.9 * wake))
        z["mouth_o"] = max(z["mouth_o"], (0.85 if 0.2 < t < 1.9 else 0.4) * wake)
        z["mouth_w"] = 1.15
        z["blink"] = 0.0
        return at_neck(ZAHHAK_NIGHT, z, t, 540 + jit, 1030, 1.15)
    D = Shot(2.8, bedb, midD, cam=camD, light=dict(LAMP, rim=(-5, -2), rim_col=(1.0, 0.62, 0.32), rim_str=0.8), grade="night", bloom=0.4)

    hall = bg("hall", zbg.hall)

    def shake_cam(base):
        def cam(t):
            k, cx, cy, px, py = base(t)
            a = 14 * (1 - ease((t - 1.4) / 1.6))
            return k, cx, cy, px + a * math.sin(t * 37), py + a * math.cos(t * 29)
        return cam
    camE = shake_cam(cam_push(1.04, 1.08, 540, 1000, 3.4))

    class Dust:
        def __call__(self, im, t):
            d = ImageDraw.Draw(im, "RGBA")
            rr = random.Random(9)
            for k in range(70):
                x = rr.uniform(0, W); v = rr.uniform(300, 700); y0 = rr.uniform(-200, 500)
                y = y0 + v * t
                if 0 < y < H:
                    s_ = rr.uniform(1.5, 4)
                    d.ellipse((x - s_, y - s_, x + s_, y + s_), fill=(200, 180, 160, int(150 * (1 - t / 3.4))))
    E = Shot(3.4, hall, lambda t: torches_wide(t), cam=camE, light=HALL, fx=hall_fx(camE, [(80, 640), (1000, 640)], 23) + [Dust()], grade="fire", bloom=0.6)

    LF = [("p4s6f", 0.2)]

    def midF(t):
        a = tp(LF, t, 33, turn=0.3, gx=0.7, gy=0.1, sad=0.6, brow=0.8, furrow=-0.4, armL="hold_lantern", propL="lantern", armR="relaxed")
        return at_neck(ARNAVAZ, a, t, 520, 1020, 1.05)
    camF = cam_push(1.0, 1.04, 520, 860, 3.6)
    F = Shot(3.6, bedb, midF, cam=camF, light=dict(LAMP, point=None, rim=(5, -2), rim_col=(1.0, 0.75, 0.45), rim_str=0.7, ambient=(0.8, 0.76, 0.86)),
             fx=[Glow(lambda t: cam_xy(camF, t, 520 + 1.05 * 160, 1020 + 1.05 * 560), 260, (255, 190, 110), 0.5)], grade="night")

    camG = cam_push(1.0, 1.1, 540, 860, 7.0)

    def midG(t):
        z = tp([], t, 34, turn=-0.1 + 0.1 * math.sin(t * 0.7), gx=-0.3, gy=0.2, brow=0.9, furrow=-0.3, sad=0.6, armL="relaxed", armR="relaxed",
               snake_looks=(0.6 + 0.4 * math.sin(t * 2.1), 0.5 + 0.5 * math.sin(t * 1.8 + 1)),
               hisses=(0.4 * max(0.0, math.sin(t * 2.3)), 0.4 * max(0.0, math.sin(t * 2.0 + 2))))
        z["mouth_o"] = max(z["mouth_o"], 0.15 + 0.1 * math.sin(t * 6))
        z["blink"] = min(z["blink"], 0.3)
        return at_neck(ZAHHAK_NIGHT, z, t, 540, 1030, 1.15)
    G = Shot(7.0, bedb, midG, cam=camG, light=dict(LAMP, rim=(-5, -2), rim_col=(1.0, 0.62, 0.32), rim_str=0.8), grade="night", bloom=0.4, fade_out=1.0)
    return [A, B, C, D, E, F, G]


SCENES = {"s1": s1, "s2": s2, "s3": s3, "s4": s4, "s5": s5, "s6": s6}
