"""Part 3 · The Doctor — 2D cartoon. Timing matches zahhak/p03_audio.py
(scene starts s1 0, s2 7.4, s3 12.0, s4 42.6, s5 71.8, s6 108.2; end card 145.4; total 150.4)."""
import math, random
from PIL import Image, ImageFilter, ImageDraw
from film import Shot, W, H, ease, lerp, talk_pose, blink_at, cam_push, cam_static, Motes, Embers, svg_render
from chars import pose, horse, Ctx, FEET, fmt
from stage import at_neck, at_feet, rider, Glow, lw_for, back_heads, fire_svg
import bgs, zbg
from cast import *
from p01_scenes import P, bg, cam_xy, tp, darken, fade_to, torch_flame, hall_fx, placed, TORCH, HALL, NIGHT
from p02_scenes import glint, eyes_of, court

SWING = 21.7 - 19.6          # the sword comes down in s3 C (shot time)
DAYHALL = dict(rim=(-5, -2), rim_col=(1.0, 0.85, 0.6), ramp=(0, W, 1.05, 0.92), ambient=(1.0, 0.97, 0.93))
DAYCLOSE = dict(rim=(-6, -2), rim_col=(1.0, 0.85, 0.6), ramp=(0, W, 1.06, 0.9), ambient=(1.0, 0.97, 0.94))
SUNTOP = (300, 300, 900, (0.10, 0.07, 0.03))
MOON = dict(ambient=(0.58, 0.64, 0.9), rim=(5, -3), rim_col=(0.72, 0.82, 1.0), rim_str=0.6)
BRAZ = dict(ambient=(0.72, 0.66, 0.76), point=(540, 1150, 900, 0.6, 1.1, (1.0, 0.55, 0.25)), rim=(0, -3), rim_col=(1.0, 0.65, 0.35), rim_str=0.7)
BRAZ_CLOSE = dict(ambient=(0.78, 0.72, 0.8), rim=(-5, -2), rim_col=(1.0, 0.62, 0.32), rim_str=0.9, ramp=(0, W, 1.05, 0.85))


def night_of(fn, col=(8, 12, 34), a=165):
    def f():
        return Image.alpha_composite(fn(), Image.new("RGBA", (W, H), col + (a,)))
    return f


def cam_svg(cam, t, body, par=1.0):
    """the camera transform of a layer that moves like the background (par = the shot's bg_par) or like the cast (par 1)"""
    k, cx, cy, px, py = cam(t)
    k = 1 + (k - 1) * par
    return f'<g transform="translate({px * par:.2f},{py * par:.2f}) translate({cx:.2f},{cy:.2f}) scale({k:.5f}) translate({-cx:.2f},{-cy:.2f})">{body}</g>'


def shadow_fx(cam, body_fn, col=(22, 12, 8), a=0.8, blur=4, par=0.6):
    """a pre_fx: the silhouette of body_fn(t) thrown on the wall of the background"""
    def fx(im, t):
        body = body_fn(t)
        if not body:
            return
        al = svg_render(cam_svg(cam, t, body, par)).getchannel("A").filter(ImageFilter.GaussianBlur(blur)).point(lambda v: int(v * a))
        layer = Image.new("RGBA", (W, H), col + (0,))
        layer.putalpha(al)
        im.alpha_composite(layer)
    return fx


def svg_fx(cam, body_fn, par=1.0):
    """a pre_fx: an SVG layer drawn behind the cast, unlit (glows, halos)"""
    def fx(im, t):
        body = body_fn(t)
        if body:
            im.alpha_composite(svg_render(cam_svg(cam, t, body, par)))
    return fx


def farr_svg(x, y, r, t, a=1.0):
    """the farr, the light of God on a king: a golden halo of flames around the head (as in Persian painting), centre (x, y)"""
    if a <= 0.01:
        return ""
    n = 16
    pts = []
    for k in range(n * 2):
        ang = math.pi * k / n
        rr = r * (1.32 + 0.1 * math.sin(t * 5 + k * 1.9)) if k % 2 == 0 else r * 1.02
        pts.append((x + rr * math.cos(ang + 0.05 * math.sin(t * 2)), y + rr * math.sin(ang + 0.05 * math.sin(t * 2))))
    d = "M " + " L ".join(f"{px:.1f} {py:.1f}" for px, py in pts) + " Z"
    return (f'<defs><radialGradient id="farr" cx="{x:.1f}" cy="{y:.1f}" r="{r * 1.4:.1f}" gradientUnits="userSpaceOnUse">'
            f'<stop offset="0" stop-color="#fff6d0" stop-opacity="{0.95 * a:.2f}"/><stop offset="0.6" stop-color="#ffd86a" stop-opacity="{0.7 * a:.2f}"/>'
            f'<stop offset="1" stop-color="#f0a830" stop-opacity="0"/></radialGradient></defs>'
            f'<path d="{d}" fill="#f6c24a" opacity="{0.55 * a:.2f}" stroke="#d8902a" stroke-width="4" stroke-opacity="{0.6 * a:.2f}"/>'
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r * 1.4:.1f}" fill="url(#farr)"/>')


def head_of(x, y, s):
    """the middle of a head placed with at_neck(…, x, y, s)"""
    return x, y - 200 * s


def throne_shadow(x, y, s):
    """the silhouette of a tall throne behind a seated king whose neck is at (x, y)"""
    return (f'<path d="M {x - 230 * s:.0f} {y + 700 * s:.0f} L {x - 230 * s:.0f} {y + 150 * s:.0f} Q {x:.0f} {y + 60 * s:.0f}, {x + 230 * s:.0f} {y + 150 * s:.0f} '
            f'L {x + 230 * s:.0f} {y + 700 * s:.0f} Z" fill="#000"/><rect x="{x - 300 * s:.0f}" y="{y + 380 * s:.0f}" width="{600 * s:.0f}" height="{420 * s:.0f}" fill="#000"/>'
            f'<circle cx="{x - 300 * s:.0f}" cy="{y + 360 * s:.0f}" r="{30 * s:.0f}" fill="#000"/><circle cx="{x + 300 * s:.0f}" cy="{y + 360 * s:.0f}" r="{30 * s:.0f}" fill="#000"/>')


def crown_svg(x, y, s=1.0):
    """a tall gold crown standing on (x, y) (bottom of the band)"""
    out = f'<g transform="translate({x:.1f},{y:.1f}) scale({s:.3f})">'
    for k, cx in enumerate((-92, -46, 0, 46, 92)):
        hgt = (64 if cx == 0 else (52 if abs(cx) < 60 else 40)) * 1.7
        out += (f'<path d="M {cx - 22} -60 L {cx} {-60 - hgt:.0f} L {cx + 22} -60 Z" fill="#d29a2e" stroke="#1b0f0a" stroke-width="3"/>'
                f'<circle cx="{cx}" cy="{-66 - hgt:.0f}" r="9" fill="#f6d77e" stroke="#1b0f0a" stroke-width="2"/>')
    out += ('<path d="M -110 0 C -52 10, 52 10, 110 0 L 106 -60 C 50 -72, -50 -72, -106 -60 Z" fill="#d29a2e" stroke="#1b0f0a" stroke-width="3"/>'
            '<ellipse cx="0" cy="-30" rx="12" ry="14" fill="#b8121c" stroke="#1b0f0a" stroke-width="2"/>'
            '<ellipse cx="-66" cy="-30" rx="9" ry="10" fill="#1c4aa8" stroke="#1b0f0a" stroke-width="2"/><ellipse cx="66" cy="-30" rx="9" ry="10" fill="#1c4aa8" stroke="#1b0f0a" stroke-width="2"/>')
    return out + '</g>'


def flask_svg(x, y, s=1.0, col="#4a9a5a"):
    return (f'<g transform="translate({x:.1f},{y:.1f}) scale({s:.3f})">'
            f'<path d="M -14 -170 L 14 -170 L 14 -96 C 66 -78, 84 -30, 84 6 C 84 66, 42 100, 0 100 C -42 100, -84 66, -84 6 C -84 -30, -66 -78, -14 -96 Z" '
            f'fill="#d8ece8" fill-opacity="0.55" stroke="#1b0f0a" stroke-width="4"/>'
            f'<path d="M -78 20 C -50 34, 50 34, 78 20 C 76 70, 40 94, 0 94 C -40 94, -76 70, -78 20 Z" fill="{col}" opacity="0.85"/>'
            f'<ellipse cx="-34" cy="-30" rx="12" ry="26" fill="#fff" opacity="0.6"/><rect x="-20" y="-186" width="40" height="20" rx="5" fill="#8a5a2a" stroke="#1b0f0a" stroke-width="3"/></g>')


# ================================================================ S1 the hook (0-7.4)
def s1():
    closeb = bg("hall_close", zbg.hall_close, 4)
    camA = cam_push(1.0, 1.06, 560, 860, 3.8)
    LA = [("p3s1a", 0.8)]

    def midA(t):
        q = tp(LA, t, 1, turn=-0.25, gx=-0.4, gy=0.25, smile=0.5, brow=0.3, furrow=-0.2, nod=6 * ease(t / 1.0), armR="chest", armL="relaxed")
        return torch_flame(40, 740, t, 1.1) + at_neck(IBLIS_DOCTOR, q, t, 560, 1060, 1.45)
    A = Shot(3.8, closeb, midA, cam=camA, light=TORCH, grade="fire", bloom=0.6, fade_in=0.5,
             fx=[Glow(lambda t: cam_xy(camA, t, 40, 680), 220, (255, 170, 90), 0.4), glint(camA, eyes_of(560, 1060, 1.45, -0.25), 2.7, 3.6)])

    wall = bgs.cached("shadow_wall", bgs.shadow_wall)
    camB = cam_push(1.0, 1.05, 520, 900, 3.6)

    def shadowB(t):
        q = P(legs="sit", turn=0.1, gx=0.2, armL="relaxed", armR="relaxed", snake_rise=1.0, blink=0.0,
              snake_looks=(0.4 + 0.6 * math.sin(t * 1.3), 0.2 + 0.7 * math.sin(t * 1.1 + 1)),
              hisses=(0.8 * max(0.0, math.sin(t * 2.2)), 0.8 * max(0.0, math.sin(t * 2.0 + 2))))
        return throne_shadow(500, 860, 0.85) + at_neck(ZAHHAK_YOUNG_KING, q, t, 500, 860, 0.85)
    B = Shot(3.6, wall, None, cam=camB, pre_fx=[shadow_fx(camB, shadowB, a=0.82, blur=5)], grade="fire", bloom=0.4, fade_out=0.7,
             fx=[darken(0.25, -1.0, 9.0, (10, 4, 2))])
    return [A, B]


# ================================================================ S2 title (7.4-12.0): the doctor's table
def s2():
    tab = bgs.cached("zh_table_cloth_dim", lambda: Image.alpha_composite(bg("table_cloth", zbg.table_cloth), Image.new("RGBA", (W, H), (14, 8, 10, 150))))

    def mid(t):
        o = ""
        # a mortar and pestle
        o += ('<path d="M 150 1180 L 390 1180 C 380 1300, 330 1350, 270 1350 C 210 1350, 160 1300, 150 1180 Z" fill="#8a7a6a" stroke="#1b0f0a" stroke-width="5"/>'
              '<ellipse cx="270" cy="1180" rx="122" ry="26" fill="#5a4a3e" stroke="#1b0f0a" stroke-width="5"/>'
              '<path d="M 300 1170 L 420 990" stroke="#a8988a" stroke-width="34" stroke-linecap="round"/><path d="M 300 1170 L 420 990" stroke="#1b0f0a" stroke-width="3" fill="none"/>')
        o += flask_svg(560, 1250, 1.2, "#4a9a5a") + flask_svg(730, 1290, 0.9, "#c9921c") + flask_svg(880, 1250, 1.05, "#a8262a")
        # a little oil lamp
        o += ('<path d="M 600 1420 C 640 1460, 760 1460, 800 1420 L 860 1400 L 800 1440 C 760 1480, 640 1480, 600 1440 Z" fill="#b8822e" stroke="#1b0f0a" stroke-width="4"/>'
              '<ellipse cx="700" cy="1420" rx="100" ry="22" fill="#d8a64a" stroke="#1b0f0a" stroke-width="4"/>')
        o += torch_flame(850, 1398, t, 0.45, 3)
        # dried herbs and a scroll
        for k in range(6):
            a = -0.9 + k * 0.34
            o += f'<path d="M 120 1500 Q {120 + 90 * math.cos(a):.0f} {1440 + 30 * math.sin(a):.0f}, {120 + 210 * math.cos(a):.0f} {1420 + 90 * math.sin(a):.0f}" stroke="#6a7a3a" stroke-width="9" fill="none" stroke-linecap="round"/>'
        o += ('<rect x="300" y="1500" width="380" height="60" rx="26" fill="#eadbb4" stroke="#1b0f0a" stroke-width="4" transform="rotate(-6,490,1530)"/>'
              '<path d="M 340 1520 L 640 1488 M 344 1544 L 600 1517" stroke="#8a6a3a" stroke-width="4" transform="rotate(-6,490,1530)"/>')
        return o
    cam = cam_push(1.04, 1.1, 560, 1250, 4.6)
    return [Shot(4.6, tab, mid, cam=cam, light=dict(point=(850, 1300, 900, 0.6, 1.15, (1.0, 0.6, 0.3)), rim=(5, -2), rim_col=(1.0, 0.7, 0.4)),
                 fx=[Glow(lambda t: cam_xy(cam, t, 850, 1350), 260, (255, 180, 100), 0.5)], grade="fire", bloom=0.7, fade_in=0.4, fade_out=0.5)]


# ================================================================ S3 the snakes, the cut, the doctors (12.0-42.6)
def zk(t, lines, seed, rise=1.0, **kw):
    """young King Zahhak (seated) with his snakes; snake_looks/hisses can be passed in kw"""
    base = dict(legs="sit", turn=0.1, gx=0.2, gy=0.1, furrow=0.6, brow=0.0, armL="relaxed", armR="relaxed", wind=0.05, snake_rise=rise,
                snake_looks=(0.6 + 0.4 * math.sin(t * 1.2), 0.5 + 0.5 * math.sin(t * 1.4 + 1)))
    base.update(kw)
    return tp(lines, t, seed, **base)


def hall_wide(cam, seed=3, extra=()):
    return dict(light=HALL, fx=hall_fx(cam, [(80, 640), (1000, 640)], seed) + list(extra), grade="fire", bloom=0.6)


def torches_wide(t):
    return torch_flame(80, 640, t, 0.75) + torch_flame(1000, 640, t + 1.3, 0.75, 1)


def torches_close(t):
    return torch_flame(40, 740, t, 1.1) + torch_flame(1040, 740, t + 1.7, 1.1, 1)


def s3():
    hall = bg("hall", zbg.hall)
    close = bg("hall_close", zbg.hall_close)
    closeb = bg("hall_close", zbg.hall_close, 6)

    camA = cam_push(1.0, 1.06, 540, 950, 5.4)
    LA = [("p3s3a", 0.5)]

    def midA(t):
        look = math.sin(t * 1.6)
        z = zk(t, [], 1, turn=0.3 * look, gx=0.8 * look, gy=0.2, furrow=0.9, brow=0.3, sad=0.3,
               armL=("ik", 200, -120, "down") if 1.5 < t < 3.8 else "relaxed",
               hisses=(0.8 * max(0.0, math.sin(t * 2.4)), 0.8 * max(0.0, math.sin(t * 2.1 + 2))))
        return torches_wide(t) + at_neck(ZAHHAK_YOUNG_KING, z, t, 540, 793, 0.36) + court(t, back=1.0, seed=3)
    A = Shot(5.4, hall, midA, cam=camA, fade_in=0.4, **hall_wide(camA))

    camB = cam_push(1.0, 1.05, 540, 860, 2.2)
    LB = [("p3s3b", 0.2)]

    def midB(t):
        z = zk(t, LB, 2, turn=0.15, gx=0.4, gy=0.0, furrow=1.0, brow=-0.4, armR="fist_up" if t > 0.3 else "relaxed",
               snake_looks=(-0.6, -0.5), hisses=(0.9, 0.7))
        return torches_close(t) + at_neck(ZAHHAK_YOUNG_KING, z, t, 540, 1030, 1.15)
    B = Shot(2.2, close, midB, cam=camB, light=TORCH, fx=[Glow(lambda t: cam_xy(camB, t, 40, 680), 220, (255, 170, 90), 0.4)], grade="fire", bloom=0.6)

    wall = bgs.cached("shadow_wall", bgs.shadow_wall)
    camC = cam_push(1.0, 1.04, 540, 900, 2.4)

    def shadowC(t):
        u = ease((t - (SWING - 0.25)) / 0.3)
        a1 = lerp(165, 55, u)
        lift = ease(t / 0.8)
        q = P(turn=-0.5, gx=-0.9, armR=(lerp(40, a1, lift), 0), propR=("sword", lerp(40, a1, lift)), armL="relaxed", blink=0.0)
        k = P(legs="sit", turn=0.2, gx=0.4, armL="relaxed", armR="relaxed", snake_rise=1.0, blink=0.0, snake_looks=(0.9, 0.3 + 0.5 * math.sin(t * 3)),
              hisses=(0.9 * max(0.0, math.sin(t * 3)), 0.9))
        return throne_shadow(420, 900, 0.8) + at_neck(ZAHHAK_YOUNG_KING, k, t, 420, 900, 0.8) + at_feet(ZGUARD, q, t, 830, 1720, 0.82)
    C = Shot(2.4, wall, None, cam=camC, pre_fx=[shadow_fx(camC, shadowC, a=0.82, blur=4)], grade="fire", bloom=0.4,
             fx=[darken(0.2, -1.0, 9.0, (10, 4, 2))])

    camD = cam_push(1.0, 1.06, 540, 860, 7.8)
    LD = [("p3s3d", 5.9)]
    GROW = 2.3

    def midD(t):
        relief = 1 - ease((t - GROW - 1.2) / 0.6)
        rise = ease((t - GROW) / 2.7)
        horror = ease((t - GROW - 1.6) / 0.6)
        z = zk(t, LD, 4, rise=rise, turn=0.05 + 0.15 * horror, gx=0.3 * horror, gy=0.3 - 0.6 * horror, furrow=-0.4 * relief + 0.2 * horror,
               brow=0.2 * relief + 1.3 * horror, smile=0.45 * relief * ease((t - 0.6) / 0.8), sad=0.3 * horror, nod=10 * relief - 6 * horror,
               armL="chest" if t < GROW + 1.6 else ("both_out" if horror > 0.5 else "relaxed"),
               armR="chest" if t < GROW + 1.4 else ("both_out" if horror > 0.5 else "relaxed"),
               snake_looks=(-0.8 + 1.4 * rise, -0.6 + 1.2 * rise), hisses=(0.8 * ease((t - GROW - 2.4) / 0.4), 0.9 * ease((t - GROW - 2.6) / 0.4)))
        if t < GROW + 1.4:
            z["blink"] = 1.0
        z["mouth_o"] = max(z["mouth_o"], 0.35 * horror)
        return torches_close(t) + at_neck(ZAHHAK_YOUNG_KING, z, t, 540, 1030, 1.15)
    D = Shot(7.8, close, midD, cam=camD, light=TORCH, fx=[Glow(lambda t: cam_xy(camD, t, 40, 680), 220, (255, 170, 90), 0.4),
                                                          darken(0.18, GROW + 1.0, 9.0, (20, 8, 24))], grade="fire", bloom=0.6)

    # the doctors: E around the throne, F and G close, H sent away
    camE = cam_push(1.45, 1.52, 540, 1000, 3.8)

    def doctors(t, leave=0.0, seed=0):
        o = ""
        reach = max(0.0, math.sin(t * 1.4))
        flinch = ease((t - 1.6) / 0.25) * (1 - ease((t - 2.6) / 0.5))
        for k, (S, x, y, s, side, kw) in enumerate((
                (DOCTOR_A, 395, 1180, 0.33, 1, dict(armL=("ik", lerp(320, 170, flinch), lerp(-180, 140, flinch)), armR="relaxed")),
                (DOCTOR_B, 690, 1180, 0.33, -1, dict(armR=("ik", -130, 120, "down"), propR=("flask", 0), armL="relaxed")),
                (DOCTOR_C, 250, 1290, 0.36, 1, dict(armL=("ik", 160, 150, "down"), propL="scroll", armR="relaxed")))):
            xx = x - 520 * ease((leave - 0.1 * k) / 0.8)
            walking = 0.05 < leave < 0.95
            q = tp([], t, 30 + k + seed, turn=0.4 * side if not walking else -0.45, gx=0.8 * side if not walking else -0.9, gy=-0.5 if not walking else 0.0,
                   furrow=0.6, brow=0.4 + 0.5 * flinch * (k == 0), sad=0.3, legs="walk" if walking else "stand", phase=t * 7, **kw)
            o += at_feet(S, q, t, xx, y, s)
        return o

    def midE(t):
        z = zk(t, [], 5, turn=0.1, gx=0.2, gy=0.0, furrow=0.8, brow=0.2, snake_looks=(1.0 - 1.6 * ease((t - 1.4) / 0.3), 0.7),
               hisses=(ease((t - 1.5) / 0.2) * (1 - ease((t - 2.6) / 0.4)), 0.3))
        return torches_wide(t) + at_neck(ZAHHAK_YOUNG_KING, z, t, 540, 793, 0.36) + doctors(t)
    E = Shot(3.8, hall, midE, cam=camE, bg_par=1.0, **hall_wide(camE, 5))

    LF = [("p3s3f", 0.2)]

    def midF(t):
        q = tp(LF, t, 7, turn=0.25, gx=0.5, gy=0.2, furrow=0.7, brow=0.6, sad=0.4, nod=4 * math.sin(t * 3) if t > 1.4 else 0, armL="relaxed", armR="relaxed")
        q["turn"] += 0.12 * math.sin(t * 3.2) if t > 1.4 else 0
        return torch_flame(40, 740, t, 1.1) + at_neck(DOCTOR_A, q, t, 560, 1050, 1.35)
    camF = cam_push(1.0, 1.04, 560, 860, 2.6)
    F = Shot(2.6, closeb, midF, cam=camF, light=TORCH, fx=[Glow(lambda t: cam_xy(camF, t, 40, 680), 220, (255, 170, 90), 0.4)], grade="fire", bloom=0.5)

    LG = [("p3s3g", 0.2)]

    def midG(t):
        q = tp(LG, t, 8, turn=-0.25, gx=-0.3 if t < 1.2 else -0.7, gy=0.6 if t < 1.2 else 0.0, furrow=0.5, brow=0.4, sad=0.5,
               armL=("ik", 120, 160, "down"), propL=("flask", 0), armR="relaxed")
        return torch_flame(1040, 740, t, 1.1, 1) + at_neck(DOCTOR_B, q, t, 520, 1050, 1.35)
    camG = cam_push(1.0, 1.04, 520, 860, 2.8)
    G = Shot(2.8, closeb, midG, cam=camG, light=dict(TORCH, point=(1040, 700, 1100, 0.55, 1.15, (1.0, 0.55, 0.25)), rim_point=(1400, 6)),
             fx=[Glow(lambda t: cam_xy(camG, t, 1040, 680), 220, (255, 170, 90), 0.4)], grade="fire", bloom=0.5)

    camH = cam_push(1.45, 1.4, 540, 1000, 3.6)
    LH = [("p3s3h", 0.2)]

    def midH(t):
        z = zk(t, LH, 9, turn=-0.2, gx=-0.6, gy=0.0, furrow=1.0, brow=-0.3, armR="point" if t > 0.3 else "relaxed",
               snake_looks=(1.0, 0.9), hisses=(0.8, 0.9))
        return torches_wide(t) + at_neck(ZAHHAK_YOUNG_KING, z, t, 540, 793, 0.36) + doctors(t, leave=ease((t - 0.9) / 2.2), seed=5)
    Hs = Shot(3.6, hall, midH, cam=camH, bg_par=1.0, fade_out=0.4, **hall_wide(camH, 7))
    return [A, B, C, D, E, F, G, Hs]


# ================================================================ S4 the grey doctor (42.6-71.8)
def horns(x, neck_y, s, k, bob=0.0):
    """two horns on a shadow's head (neck at (x, neck_y), person scale s); k 0..1 grows them"""
    if k <= 0.01:
        return ""
    o = ""
    for sd in (-1, 1):
        bx, by = x + sd * 50 * s, neck_y - 300 * s + bob
        tx, ty = x + sd * (60 + 70 * k) * s, neck_y - (300 + 170 * k) * s + bob
        o += (f'<path d="M {bx - 26 * s:.1f} {by:.1f} C {bx - 20 * s + sd * 40 * s * k:.1f} {by - 60 * s * k:.1f}, {tx - sd * 10 * s:.1f} {ty + 40 * s * k:.1f}, {tx:.1f} {ty:.1f} '
              f'C {tx + sd * 4 * s:.1f} {ty + 60 * s * k:.1f}, {bx + 30 * s + sd * 30 * s * k:.1f} {by - 30 * s * k:.1f}, {bx + 26 * s:.1f} {by:.1f} Z" fill="#000"/>')
    return o


def s4():
    hall = bg("hall", zbg.hall)
    closeb = bg("hall_close", zbg.hall_close, 6)

    # A: the grey doctor walks in and bows; his golden eyes
    camA = cam_push(1.0, 1.1, 540, 1100, 5.0)

    def iblis_pos(t):
        u = ease(t / 3.0)
        return lerp(-60, 400, u), lerp(1600, 1440, u), lerp(0.44, 0.40, u)

    def midA(t):
        z = zk(t, [], 11, turn=-0.25, gx=-0.6, gy=0.4, furrow=0.7, brow=0.3, sad=0.2, snake_looks=(0.2, 0.9), hisses=(0.0, 0.0))
        x, y, s_ = iblis_pos(t)
        walking = t < 3.0
        bow = ease((t - 3.1) / 0.4) * (1 - ease((t - 3.9) / 0.4))
        q = tp([], t, 12, turn=0.3, gx=0.6, gy=-0.6 + 0.8 * bow if t > 3.0 else 0.0, nod=18 * bow, smile=0.4, brow=0.2,
               legs="walk" if walking else "stand", phase=t * 5.4, armR="relaxed", propR="bag", armL="chest" if t > 3.0 else "relaxed")
        return torches_wide(t) + at_neck(ZAHHAK_YOUNG_KING, z, t, 540, 793, 0.36) + at_feet(IBLIS_DOCTOR, q, t, x, y, s_)
    A = Shot(5.0, hall, midA, cam=camA, fade_in=0.3,
             **hall_wide(camA, 9, [glint(camA, eyes_of(400, 1440 - FEET * 0.40, 0.40, 0.3), 4.0, 4.8)]))

    def iblis_close(lines, seed, x=480, offer=None, glint_t=None, dur=3.0, cam=None):
        cam = cam or cam_push(1.0, 1.04, x, 860, dur)

        def mid(t):
            q = tp(lines, t, seed, turn=0.25, gx=0.5, gy=0.1, smile=0.45, brow=0.25, furrow=-0.2,
                   armL="offer" if (offer and offer[0] < t < offer[1]) else "relaxed", armR="relaxed")
            return torch_flame(40, 740, t, 1.1) + at_neck(IBLIS_DOCTOR, q, t, x, 1060, 1.45)
        fx = [Glow(lambda t: cam_xy(cam, t, 40, 680), 220, (255, 170, 90), 0.4)]
        if glint_t:
            fx.append(glint(cam, eyes_of(x, 1060, 1.45, 0.25), *glint_t))
        return Shot(dur, closeb, mid, cam=cam, light=TORCH, fx=fx, grade="fire", bloom=0.5)

    B = iblis_close([("p3s4b", 0.3)], 13, offer=(1.6, 3.4), dur=3.6)

    def zahhak_close(lines, seed, dur, **kw):
        cam = cam_push(1.0, 1.04, 580, 860, dur)

        def mid(t):
            base = dict(turn=-0.2, gx=-0.5, gy=0.1, furrow=0.2, brow=0.7, sad=0.6, snake_looks=(-0.2, 0.8), hisses=(0.0, 0.0))
            base.update({k: (v(t) if callable(v) else v) for k, v in kw.items()})
            z = zk(t, lines, seed, **base)
            return torch_flame(1040, 740, t, 1.1, 1) + at_neck(ZAHHAK_YOUNG_KING, z, t, 600, 1030, 1.15)
        return Shot(dur, bg("hall_close", zbg.hall_close), mid, cam=cam,
                    light=dict(TORCH, point=(1040, 700, 1100, 0.55, 1.15, (1.0, 0.55, 0.25)), rim_point=(1400, 6)),
                    fx=[Glow(lambda t: cam_xy(cam, t, 1040, 680), 220, (255, 170, 90), 0.4)], grade="fire", bloom=0.5)

    C = zahhak_close([("p3s4c", 0.2)], 14, 2.2, armL=lambda t: "both_out" if t > 0.5 else "relaxed")
    D = iblis_close([("p3s4d", 0.2)], 15, offer=(0.3, 2.0), dur=2.4)
    E = zahhak_close([("p3s4e", 0.15)], 16, 1.4, sad=0.2, brow=0.5, furrow=0.5, snake_looks=(-1.0, -0.9), gx=-0.7)

    # F: the whisper, very close
    camF = cam_push(1.0, 1.06, 520, 900, 4.2)
    LF = [("p3s4f", 0.3)]

    def midF(t):
        q = tp(LF, t, 17, turn=0.3, gx=0.7, gy=0.0, smile=0.3, brow=0.0, furrow=0.3, tilt=-4, armL="relaxed", armR="relaxed")
        q["blink"] = max(q["blink"], 0.25)
        return torch_flame(40, 760, t, 1.1) + at_neck(IBLIS_DOCTOR, q, t, 520, 1180, 1.9)
    F = Shot(4.2, closeb, midF, cam=camF, light=dict(TORCH, ambient=(0.62, 0.56, 0.66)),
             fx=[Glow(lambda t: cam_xy(camF, t, 40, 700), 240, (255, 170, 90), 0.45), darken(0.3, -1.0, 9.0, (8, 4, 10)),
                 glint(camF, eyes_of(520, 1180, 1.9, 0.3), 3.4, 4.2)], grade="fire", bloom=0.5)

    # G: the two of them; the snakes answer
    LG = [("p3s4g", 0.3)]

    def midG(t):
        h = ease((t - 1.0) / 0.3)
        z = zk(t, [], 18, turn=-0.15, gx=-0.3 + 0.4 * h, gy=0.3 - 0.3 * h, furrow=0.2, brow=0.4 + 0.8 * h, sad=0.4, armL="relaxed", armR="relaxed",
               snake_looks=(1.0, 0.6), hisses=(0.9 * h, 0.7 * ease((t - 1.6) / 0.3)))
        z["mouth_o"] = max(z["mouth_o"], 0.3 * h)
        q = tp(LG, t, 19, turn=0.5, gx=0.8, gy=0.3, smile=0.5, brow=0.2 + 0.4 * h, tilt=10 - 6 * h, nod=10, armL="relaxed", armR="relaxed")
        return at_neck(IBLIS_DOCTOR, q, t, 270 - 20 * h, 1090, 0.9) + at_neck(ZAHHAK_YOUNG_KING, z, t, 680, 960, 0.95)
    camG = cam_push(1.0, 1.05, 540, 880, 3.4)
    G = Shot(3.4, closeb, midG, cam=camG, light=TORCH, fx=[Glow(lambda t: cam_xy(camG, t, 40, 680), 220, (255, 170, 90), 0.4)], grade="fire", bloom=0.5)

    # H1: his shadow on the wall as he goes; H2: the king alone
    wall = bgs.cached("shadow_wall", bgs.shadow_wall)
    camH = cam_push(1.0, 1.04, 540, 900, 3.2)

    def shadowH(t):
        u = t / 3.2
        x = lerp(1060, 220, u)
        ph = t * 5.2
        q = P(legs="walk", phase=ph, turn=-0.45, gx=-0.9, armR="relaxed", propR="bag", armL="relaxed", blink=0.0)
        s_ = 0.78
        neck_y = 1700 - FEET * s_
        bob = -10 * abs(math.cos(ph)) * s_
        return at_feet(IBLIS_DOCTOR, q, t, x, 1700, s_) + horns(x, neck_y, s_, ease((t - 0.7) / 1.2), bob)
    H1 = Shot(3.2, wall, None, cam=camH, pre_fx=[shadow_fx(camH, shadowH, a=0.85, blur=3)], grade="fire", bloom=0.4,
              fx=[darken(0.25, -1.0, 9.0, (10, 4, 2))])

    camH2 = cam_push(1.1, 1.0, 540, 950, 3.8)

    def midH2(t):
        z = zk(t + 3.0, [], 20, turn=0.0, gx=0.0, gy=0.4, furrow=0.8, brow=0.2, sad=0.5, snake_looks=(0.7 + 0.3 * math.sin(t), 0.6 + 0.3 * math.sin(t * 1.3)),
               hisses=(0.4 * max(0.0, math.sin(t * 1.7)), 0.4 * max(0.0, math.sin(t * 1.5 + 2))))
        return torches_wide(t) + at_neck(ZAHHAK_YOUNG_KING, z, t, 540, 793, 0.36)
    H2 = Shot(3.8, hall, midH2, cam=camH2, fade_out=0.7, **hall_wide(camH2, 11, [darken(0.3, -1.0, 9.0, (8, 4, 12))]))
    return [A, B, C, D, E, F, G, H1, H2]


# ================================================================ S5 Jamshid's pride; the light of God leaves him (71.8-108.2)
FRONT_NOBLES = [(NOBLE_1, 250, 1500, 0.40, 1), (IRAN_NOBLE, 105, 1640, 0.47, 1), (NOBLE_2, 835, 1505, 0.40, -1), (NOBLE_3, 980, 1645, 0.47, -1)]


def jamshid_court():
    from stage import crowd_row
    im = bg("jamshid_hall", zbg.jamshid_hall).copy()
    im.alpha_composite(crowd_row(71, 4, 1405, 0.3, x0=250, x1=420, kinds=("man",), turn_to=0.4))
    im.alpha_composite(crowd_row(72, 4, 1405, 0.3, x0=660, x1=830, kinds=("man",), turn_to=-0.4))
    return im


def nobles(t, bow=0.0, leave=None, seed=0):
    """the four nobles in front; bow 0..1; leave(k) -> 0..1 walking out to their side of the hall"""
    o = ""
    for k, (S, x, y, s, side) in enumerate(FRONT_NOBLES):
        u = leave(k) if leave else 0.0
        walking = 0.02 < u < 0.98
        if u >= 0.98:
            continue
        xx = x - side * 520 * u
        q = tp([], t, 40 + k + seed, turn=(0.4 * side) if not walking else -0.5 * side, gx=0.8 * side if not walking else -0.9 * side,
               gy=-0.4 + 1.2 * bow, nod=20 * bow, smile=0.3 * (1 - bow) * (1 - u), sad=0.3 * bow, brow=0.2,
               armL="chest" if bow > 0.4 else "relaxed", armR="relaxed", legs="walk" if walking else "stand", phase=t * 6 + k)
        o += at_feet(S, q, t, xx, y, s)
    return o


def jam(t, lines, seed, **kw):
    base = dict(legs="sit", turn=0.0, gx=0.0, gy=0.2, smile=0.55, brow=0.35, furrow=-0.3, armL="relaxed", armR="relaxed", wind=0.05, cloak_len=0.6)
    base.update(kw)
    return tp(lines, t, seed, **base)


def braziers(t, s=0.55):
    return torch_flame(160, 1150, t, s, 4) + torch_flame(920, 1150, t + 0.7, s, 5)


def s5():
    court_bg = bgs.cached("zh_jamshid_hall_court", jamshid_court)
    hallj = bg("jamshid_hall", zbg.jamshid_hall)
    closej = bg("jamshid_hall_close", zbg.jamshid_hall_close)

    camA = cam_push(1.0, 1.07, 540, 1050, 5.4)
    hx, hy = head_of(540, 793, 0.36)

    def midA(t):
        j = jam(t, [], 21, gy=0.4, smile=0.6)
        return braziers(t) + at_neck(JAMSHID, j, t, 540, 793, 0.36) + nobles(t)
    A = Shot(5.4, court_bg, midA, cam=camA, light=DAYHALL, sun=SUNTOP, fade_in=0.6,
             pre_fx=[svg_fx(camA, lambda t: farr_svg(hx, hy, 70, t, 1.0), par=0.6)],
             fx=[Motes(50, 51, (255, 236, 190), (0, 300, W, 1500), (6, -6), amax=90)])

    # A2: his rich, happy land
    land = bgs.cached("belalabad_wide", bgs.belalabad_wide)
    cows = [(640, 1246, 0.6, 0.0, "#7a5a3e"), (820, 1206, 0.52, 1.7, "#5a4030"), (950, 1176, 0.46, 3.1, "#8a6a4a")]
    fam = random.Random(53)
    from stage import random_spec
    folk = [random_spec(fam, ("man",)), random_spec(fam, ("woman",)), random_spec(fam, ("boy",))]

    def midA2(t):
        from chars import cow
        o = ""
        c = Ctx(lw_for(0.3))
        for x, y, s_, ph, col in cows:
            o += f'<g transform="translate({x},{y}) scale({s_})">{cow(c, col=col, t=t + ph, graze=0.5 + 0.5 * math.sin(t * 0.8 + ph))}</g>'
        for k, (S, dx, s_) in enumerate(zip(folk, (0, 70, 140), (0.3, 0.29, 0.3))):
            u = t / 4.2
            q = P(legs="walk", phase=t * 5.6 + k, turn=0.35, gx=0.6, smile=0.6, armL="relaxed", armR="wave" if (k == 2 and int(t * 2) % 2 == 0) else "relaxed",
                  wind=0.3, blink=blink_at(t, 60 + k))
            o += at_feet(S, q, t, lerp(120, 330, u) - dx, lerp(1480, 1420, u) + 10 * k, s_)
        return o
    A2 = Shot(4.2, land, midA2, cam=cam_push(1.1, 1.14, 470, 1150, 4.2, 0, -60, 0, 0), light=dict(rim=(5, -3), rim_col=(1.0, 0.8, 0.5), ramp=(0, W, 0.88, 1.05)),
              sun=(1000, 600, 800, (0.08, 0.06, 0.02)), fx=[Motes(40, 52, (255, 240, 200), (0, 600, W, 1400), (-6, -3), amax=90)])

    # B: "Look at this world!"
    camB = cam_push(1.0, 1.04, 540, 860, 4.6)
    LB = [("p3s5c", 0.2)]
    bx, by = head_of(540, 1040, 1.2)

    def midB(t):
        j = jam(t, LB, 22, gy=-0.1, smile=0.7, brow=0.5, nod=-6, armL="both_out" if t < 2.6 else "chest", armR="both_out" if t < 2.6 else "relaxed")
        return at_neck(JAMSHID, j, t, 540, 1040, 1.2)
    B = Shot(4.6, closej, midB, cam=camB, light=DAYCLOSE, sun=SUNTOP, pre_fx=[svg_fx(camB, lambda t: farr_svg(bx, by, 205, t, 1.0))],
             fx=[Motes(40, 53, (255, 236, 190), (0, 300, W, 1500), (6, -6), amax=90)])

    # C: "Your food, your sleep, your peace… all come from me."
    camC = cam_push(1.55, 1.62, 540, 980, 4.8)
    LC = [("p3s5d", 0.2)]
    heads = bgs.cached("zh_p3_backheads", lambda: back_heads(31, 7, 1780, 0.6, col="#2a1c14", blur=4))

    def midC(t):
        j = jam(t, LC, 23, turn=0.1 * math.sin(t * 0.9), gx=0.4 * math.sin(t * 0.9), gy=0.2, smile=0.6,
                armR=("ik", lerp(-420, -200, ease((t - 0.4) / 2.6)), -60, "down") if t < 3.2 else "relaxed", armL="chest" if t > 3.0 else "relaxed")
        return braziers(t) + at_neck(JAMSHID, j, t, 540, 793, 0.36)
    C = Shot(4.8, hallj, midC, fg=heads, cam=camC, bg_par=1.0, light=DAYHALL, sun=SUNTOP,
             pre_fx=[svg_fx(camC, lambda t: farr_svg(hx, hy, 70, t, 1.0))])

    # D: he stands: "call me the maker of the world!"
    camD = cam_push(1.3, 1.38, 540, 1000, 4.0)
    LD = [("p3s5e", 0.2)]
    sx_, sy_ = head_of(540, 1180 - FEET * 0.38, 0.38)

    def midD(t):
        lift = ease((t - 0.2) / 0.8)
        j = tp(LD, t, 24, turn=0.0, gx=0.0, gy=-0.2, smile=0.6, brow=0.6, furrow=-0.3, armL=(lerp(20, 150, lift), -10), armR=(lerp(20, 150, lift), -10), wind=0.2)
        return braziers(t) + at_feet(JAMSHID, j, t, 540, 1180, 0.38)
    D = Shot(4.0, hallj, midD, cam=camD, bg_par=1.0, light=DAYHALL, sun=SUNTOP,
             pre_fx=[svg_fx(camD, lambda t: farr_svg(sx_, sy_, 74, t, 1.0))], fx=[Motes(40, 54, (255, 236, 190), (0, 300, W, 1500), (6, -6), amax=90)])

    # E: the nobles bow their heads; no one says a word
    hallb = bg("jamshid_hall", zbg.jamshid_hall, 8)

    def midE(t):
        o = ""
        for k, (S, x, y, s_) in enumerate(((NOBLE_1, 220, 1110, 0.8), (NOBLE_2, 540, 1140, 0.8), (IRAN_NOBLE, 860, 1110, 0.82))):
            bow = ease((t - 0.2 - 0.25 * k) / 0.6)
            q = tp([], t, 45 + k, turn=0.1 * (1 - k), gx=0.2, gy=-0.3 + 1.3 * bow, nod=22 * bow, sad=0.35 * bow, brow=0.3, furrow=0.3,
                   armL="chest" if bow > 0.5 else "relaxed", armR="relaxed")
            q["blink"] = max(q["blink"], 0.55 * bow)
            o += at_neck(S, q, t, x, y, s_)
        return o
    E = Shot(2.4, hallb, midE, cam=cam_push(1.0, 1.03, 540, 900, 2.4), light=DAYCLOSE, sun=SUNTOP)

    # F: the light leaves him
    camF = cam_push(1.0, 1.05, 540, 860, 5.4)
    LF = [("p3s5g", 0.3)]
    GO = 2.2

    def farrF(t):
        u = ease((t - GO) / 2.0)
        return farr_svg(bx, by - 900 * u ** 1.4, 205 * (1 - 0.5 * u), t, 1.0 - 0.9 * u)

    def midF(t):
        loss = ease((t - GO - 0.3) / 1.0)
        j = jam(t, LF, 25, gy=0.2 - 0.6 * loss, smile=0.6 * (1 - loss), brow=0.4 + 0.6 * loss, sad=0.6 * loss, furrow=-0.3 - 0.4 * loss, nod=-10 * loss,
                armL="relaxed", armR="relaxed")
        if GO + 0.4 < t < GO + 2.2:
            j["gy"] = -1.0
        return at_neck(JAMSHID, j, t, 540, 1040, 1.2)

    class Rising:
        """motes of gold going up after the farr"""
        def __call__(self, im, t):
            u = (t - GO) / 2.4
            if not 0 < u < 1.4:
                return
            d = ImageDraw.Draw(im, "RGBA")
            r = random.Random(7)
            for k in range(40):
                ph = r.uniform(0, 1)
                v = (u + ph * 0.5)
                x = bx + r.uniform(-220, 220) * (1 - 0.5 * v) + 30 * math.sin(t * 3 + k)
                y = by - 900 * min(1.0, v) ** 1.4 + r.uniform(-80, 160)
                a = int(220 * max(0.0, 1 - abs(v - 0.5) * 1.6))
                sx, sy = cam_xy(camF, t, x, y)
                rr = r.uniform(2, 5)
                if a > 0:
                    d.ellipse((sx - rr, sy - rr, sx + rr, sy + rr), fill=(255, 226, 150, a))
    F = Shot(5.4, closej, midF, cam=camF, light=DAYCLOSE, sun=SUNTOP, pre_fx=[svg_fx(camF, farrF)],
             fx=[Rising(), darken(0.32, GO + 0.6, 9.0, (16, 14, 30))])

    # G: one by one the nobles go; Jamshid alone
    camG = cam_push(1.06, 1.0, 540, 1050, 5.6)

    def midG(t):
        j = jam(t, [], 26, gy=0.7, smile=0.0, sad=0.8, brow=0.5, furrow=-0.4, nod=8)
        return braziers(t, 0.45) + at_neck(JAMSHID, j, t, 540, 793, 0.36) + nobles(t, leave=lambda k: ease((t - 0.4 - 0.9 * k) / 2.2))
    G = Shot(5.6, hallj, midG, cam=camG, light=dict(DAYHALL, ambient=(0.86, 0.84, 0.9)), fade_out=0.8,
             fx=[darken(0.35, -1.0, 9.0, (14, 14, 30))])
    return [A, A2, B, C, D, E, F, G]


# ================================================================ S6 Iran chooses Zahhak; Jamshid runs; the princesses (108.2-150.4)
def s6():
    strip = bgs.cached("zh_ride_strip", zbg.ride_strip)

    # A: the riders of Iran gallop to the Arab lands
    def bgA(t):
        x0 = int(300 + 360 * t)
        return strip.crop((x0, 0, x0 + W, H))
    riders = [(IRAN_NOBLE, 560, 1560, 0.86, "#3a2a1e", 0.0), (NOBLE_3, 250, 1470, 0.66, "#7a4a2a", 1.3), (NOBLE_1, 860, 1440, 0.6, "#5a3a22", 2.1),
              (NOBLE_2, 20, 1410, 0.54, "#2a2226", 0.7)]

    def midA(t):
        o = ""
        for S, x, y, s_, col, ph in sorted(riders, key=lambda r_: r_[2]):
            q = P(turn=0.45, gx=0.9, gy=0.1, furrow=0.5, brow=0.2, armR="forward", armL="forward", wind=1.0, blink=blink_at(t, int(ph * 10)))
            bounce = -14 * s_ * abs(math.sin(t * 10.5 + ph))
            o += (f'<g transform="translate(0,{bounce:.1f})">' +
                  rider(S, q, t, lambda c_, col=col, ph=ph: horse(c_, col=col, walk=True, phase=t * 10.5 + ph, t=t + ph, head_bob=-18 * math.sin(t * 10.5 + ph)),
                        x + 8 * math.sin(t * 0.7 + ph), y, s_) + '</g>')
        for k in range(14):
            age = ((t * 2.0 + k * 0.07) % 1.0)
            o += f'<ellipse cx="{60 + 900 * (k / 14) - age * 300:.1f}" cy="{1500 - 30 * age:.1f}" rx="{20 + 70 * age:.1f}" ry="{(20 + 70 * age) * 0.45:.1f}" fill="#cdb084" opacity="{0.6 * (1 - age):.2f}"/>'
        return o
    A = Shot(5.2, bgA, midA, cam=cam_static(), light=dict(rim=(-5, -2), rim_col=(1.0, 0.75, 0.45), ramp=(0, W, 1.06, 0.9)),
             sun=(150, 700, 700, (0.10, 0.07, 0.03)), fade_in=0.4, fx=[Motes(60, 61, (214, 180, 130), (0, 1200, W, 1500), (-300, -10), (2, 6), 140)])

    # B: in Zahhak's hall the noble kneels
    hall = bg("hall", zbg.hall)
    camB = cam_push(1.3, 1.36, 540, 1050, 5.4)
    LB = [("p3s6b", 0.3)]

    def midB(t):
        z = tp([], t, 50, legs="sit", turn=-0.2, gx=-0.5, gy=0.4, furrow=0.6, brow=0.0, smile=0.2, armL="relaxed", armR="relaxed",
               snake_looks=(0.9, 0.6 + 0.3 * math.sin(t)), hisses=(0.0, 0.0))
        o = torches_wide(t) + at_neck(ZAHHAK_KING, z, t, 540, 793, 0.36)
        for k, (S, x, y, s_) in enumerate(((NOBLE_3, 250, 1400, 0.37), (NOBLE_1, 700, 1410, 0.37))):
            q = tp([], t, 51 + k, legs="sit", turn=0.45 if x < 540 else -0.45, gx=0.8 if x < 540 else -0.8, gy=-0.5, nod=14, brow=0.3, furrow=0.4,
                   armL="chest", armR="relaxed")
            o += at_neck(S, q, t, x, y - 575 * s_, s_)
        n = tp(LB, t, 53, legs="sit", turn=0.4, gx=0.7, gy=-0.7, brow=0.4, furrow=0.3, armL="offer" if 2.6 < t < 4.8 else "chest", armR="relaxed")
        return o + at_neck(IRAN_NOBLE, n, t, 430, 1350 - 575 * 0.36, 0.36)
    B = Shot(5.4, hall, midB, cam=camB, bg_par=1.0, **hall_wide(camB, 13))

    # C: "Your king? …Gladly."
    camC = cam_push(1.0, 1.05, 560, 860, 2.4)
    LC = [("p3s6c", 0.2)]

    def midC(t):
        z = tp(LC, t, 54, legs="sit", turn=-0.22, gx=-0.7, gy=0.1, furrow=0.5, brow=0.2 if t < 1.0 else -0.2, smile=0.3 + 0.4 * ease((t - 1.1) / 0.4),
               armL="relaxed", armR="relaxed", snake_looks=(0.9, -0.6 + 0.4 * math.sin(t * 2)), hisses=(0.0, 0.5 * ease((t - 1.6) / 0.3)))
        z["blink"] = max(z["blink"], 0.3)
        return torches_close(t) + at_neck(ZAHHAK_KING, z, t, 560, 1040, 1.0)
    C = Shot(2.4, bg("hall_close", zbg.hall_close), midC, cam=camC, light=TORCH,
             fx=[Glow(lambda t: cam_xy(camC, t, 40, 680), 220, (255, 170, 90), 0.4)], grade="fire", bloom=0.6)

    # D: the army marches on Jamshid's palace
    def bgD(t):
        x0 = int(1500 + 150 * t)
        return strip.crop((x0, 0, x0 + W, H))
    army = [(ZGUARD, 190, 1430, 0.6, "#121216", 0.9, True), (ZGUARD, 820, 1415, 0.56, "#2a2226", 1.7, True)]
    foot = [(ZGUARD, x, 1290 + 6 * (k % 2), 0.2, k * 0.9) for k, x in enumerate((-60, 40, 140, 240, 340, 440, 540, 640, 740, 840, 940, 1040))]

    def midD(t):
        o = ""
        for S, x, y, s_, ph in foot:
            q = P(legs="walk", phase=t * 5 + ph, turn=0.45, gx=0.8, armL=(20, 10), propL="pike", armR="relaxed", furrow=0.8, blink=0.0)
            o += at_feet(S, q, t, x + 30 * t, y, s_)
        for S, x, y, s_, col, ph, ban in army:
            q = P(turn=0.45, gx=0.9, furrow=0.8, armR=(30, 20), propR="banner_black" if ban else None, armL="forward", wind=0.8)
            o += rider(S, q, t, lambda c_, col=col, ph=ph: horse(c_, col=col, walk=True, phase=t * 4.2 + ph, t=t + ph), x + 40 * t, y, s_)
        z = P(turn=0.45, gx=0.9, gy=0.1, furrow=0.6, smile=0.2, armR="forward", armL="forward", wind=0.6, snake_rise=1.0, snake_looks=(0.9, 0.8),
              blink=blink_at(t, 70))
        o += rider(ZAHHAK_KING, z, t, lambda c_: horse(c_, col="#0e0c10", mane="#050405", walk=True, phase=t * 4.2, t=t, blanket="#6a0c14"), 430 + 40 * t, 1580, 0.86)
        return o
    D = Shot(4.8, bgD, midD, cam=cam_push(1.0, 1.04, 540, 1200, 4.8), light=dict(rim=(-5, -2), rim_col=(1.0, 0.6, 0.35), ramp=(0, W, 1.08, 0.9), ambient=(1.0, 0.88, 0.82)),
             sun=(100, 1000, 900, (0.16, 0.06, 0.02)), grade="fire", fx=[darken(0.16, -1.0, 9.0, (40, 12, 20)),
                                                                          Motes(50, 62, (214, 150, 110), (0, 1150, W, 1500), (-80, -10), (2, 6), 130)])

    # E: night in Jamshid's hall: seated, he takes off his crown and lays it on the seat (E1); he goes down into the dark (E2)
    hall_n = bgs.cached("zh_jamshid_hall_night", night_of(lambda: bg("jamshid_hall", zbg.jamshid_hall)))
    camE = cam_push(1.5, 1.56, 560, 1000, 3.2)
    JN = dict(JAMSHID, cloak="#24242c", cloak2="#141418", cloak_hi="#3a3a46")
    JN_BARE = dict(JN, head="none")
    PUT = 1.8                              # he has taken off his crown and holds it in his lap; at PUT he lays it on the seat
    SEAT = (650, 990)                      # where the crown is left (bottom of its band)
    CROWN_S = 0.3
    LAP = 300

    def hands(t):
        """(armL target, armR target, crown position or None) in person units from the neck; the crown is held between the hands"""
        if t < PUT:
            y = LAP + 8 * math.sin(t * 1.3)
            return ("ik", 95, y), ("ik", -95, y), (0, y + 25)
        u = ease((t - PUT) / 0.6)
        sx, sy = (SEAT[0] - 540) / 0.36, (SEAT[1] - 793) / 0.36
        back = ease((t - PUT - 0.75) / 0.45)
        if u < 1:
            x, y = lerp(0, sx, u), lerp(LAP + 25, sy, u)
            return ("ik", x + 60, y - 25), ("ik", lerp(-95, -240, u), lerp(LAP, 330, u)), (x, y)
        return ("ik", lerp(sx + 60, 240, back), lerp(sy - 25, 330, back)), "relaxed", None

    def midE1(t):
        aL, aR, crown = hands(t)
        j = jam(t, [], 55, gy=1.0 if t < PUT + 0.6 else 0.3, gx=0.0 if t < PUT else 0.4, smile=0.0, sad=0.85, brow=0.5, furrow=-0.4, nod=10, armL=aL, armR=aR)
        o = at_neck(JN_BARE, j, t, 540, 793, 0.36)
        if crown:
            o += crown_svg(540 + crown[0] * 0.36, 793 + crown[1] * 0.36, CROWN_S)
        else:
            o = crown_svg(SEAT[0], SEAT[1], CROWN_S) + o
        return o
    E1 = Shot(3.2, hall_n, midE1, cam=camE, bg_par=1.0, light=MOON, grade="night",
              fx=[Motes(30, 63, (200, 210, 255), (300, 300, 800, 1300), (4, 6), amax=60)])

    camE2 = cam_push(1.12, 1.06, 540, 1050, 3.0)

    def midE2(t):
        u = ease(t / 3.0)
        q = tp([], t + 3.2, 55, turn=-0.45, gx=-0.8, gy=0.3, sad=0.85, brow=0.5, furrow=-0.4, armL="relaxed", armR="relaxed", legs="walk", phase=t * 4.6)
        alpha = 1 - ease((t - 1.8) / 1.1)
        body = at_feet(JN_BARE, q, t, lerp(560, 130, u), lerp(1300, 1420, u), lerp(0.36, 0.4, u))
        return crown_svg(SEAT[0], SEAT[1], CROWN_S) + (f'<g opacity="{alpha:.3f}">{body}</g>' if alpha < 1 else body)
    E2 = Shot(3.0, hall_n, midE2, cam=camE2, light=MOON, grade="night",
              fx=[glint(camE2, [(SEAT[0], SEAT[1] - 30)], 0.6, 1.6), darken(0.25, 1.5, 9.0, (4, 6, 18))])

    # F: Zahhak on Jamshid's throne; the princesses brought in
    def hall_dark():
        im = bg("jamshid_hall", zbg.jamshid_hall)
        return Image.alpha_composite(im, Image.new("RGBA", (W, H), (18, 8, 16, 150)))
    hall_z = bgs.cached("zh_jamshid_hall_zahhak", hall_dark)
    camF = cam_push(1.0, 1.08, 540, 1100, 7.8)
    LF = []

    def midF(t):
        z = tp([], t, 56, legs="sit", turn=0.0, gx=-0.2 + 0.3 * ease((t - 3.0) / 1.0), gy=0.5, furrow=0.6, smile=0.3, armL="relaxed", armR="relaxed",
               snake_looks=(0.9, 0.9), hisses=(0.0, 0.0))
        o = braziers(t) + at_neck(ZAHHAK_KING, z, t, 540, 793, 0.36)
        for x, ph in ((300, 0.0), (780, 1.0)):
            o += at_feet(ZGUARD, P(turn=0.3 if x < 540 else -0.3, gx=0.6 if x < 540 else -0.6, armL=(20, 10), propL="pike", armR="relaxed", furrow=0.8,
                                   blink=blink_at(t, int(ph * 9 + 80))), t, x, 1340, 0.34)
        u = ease(t / 5.6)
        walking = t < 5.6
        for k, sd in enumerate((-1, 1)):
            q = P(turn=0.2 * sd, gx=0.4 * sd, armL=(20, 10), propL="pike", armR="relaxed", furrow=0.9, legs="walk" if walking else "stand",
                  phase=t * 4.6 + k, blink=blink_at(t, 85 + k))
            o += at_feet(ZGUARD, q, t, 540 + sd * 190 * lerp(1.4, 1.0, u), lerp(1820, 1400, u), lerp(0.52, 0.37, u))
        for k, (S, dx, sd) in enumerate(((ARNAVAZ, -60, 0.0), (SHAHRNAZ, 60, 0.7))):
            q = tp([], t, 57 + k, turn=0.2 if k == 0 else -0.2, gx=0.5 if k == 0 else -0.4, gy=-0.6, sad=0.8, brow=0.6, furrow=-0.3,
                   armL="chest" if k == 1 else ("ik", 220, 380, "down"), armR=("ik", -220, 380, "down") if k == 1 else "relaxed",
                   legs="walk" if walking else "stand", phase=t * 4.6 + sd)
            o += at_feet(S, q, t, 540 + dx * lerp(1.6, 1.0, u), lerp(1900, 1450, u), lerp(0.6, 0.4, u))
        return o
    F = Shot(7.8, hall_z, midF, cam=camF, light=BRAZ, grade="fire", bloom=0.6,
             fx=[Glow(lambda t: cam_xy(camF, t, 160, 1080), 200, (255, 170, 90), 0.4), Glow(lambda t: cam_xy(camF, t, 920, 1080), 200, (255, 170, 90), 0.4)])

    # G: the sisters, close
    hallzb = bgs.cached("zh_jamshid_hall_zahhak_b8", lambda: hall_z.filter(ImageFilter.GaussianBlur(8)))
    LG = [("p3s6h", 0.2)]

    def midG(t):
        tremble = 2.2 * math.sin(t * 31)
        a = tp(LG, t, 58, turn=0.35, gx=0.8, gy=0.1, sad=0.7, brow=0.6, furrow=-0.4, armL=("ik", 300, 330, "down"), armR="relaxed")
        b = tp([], t, 59, turn=0.0, gx=-0.3 if t < 1.2 else 0.5, gy=-0.5 if t < 1.2 else 0.2, sad=0.9, brow=0.9, furrow=-0.5, armR=("ik", -300, 330, "down"),
               armL="chest")
        return at_neck(SHAHRNAZ, b, t, 720 + tremble, 1040, 0.98) + at_neck(ARNAVAZ, a, t, 370, 1020, 1.0)
    G = Shot(2.6, hallzb, midG, cam=cam_push(1.0, 1.04, 540, 880, 2.6), light=BRAZ_CLOSE, grade="fire")

    # H: "Welcome… to my palace." — then the end card
    closez = bgs.cached("zh_jamshid_hall_close_dark", lambda: Image.alpha_composite(bg("jamshid_hall_close", zbg.jamshid_hall_close),
                                                                                   Image.new("RGBA", (W, H), (18, 8, 16, 165))))
    camH = cam_push(1.0, 1.1, 540, 860, 7.8)
    LH = [("p3s6i", 0.3)]

    def midH(t):
        z = tp(LH, t, 60, legs="sit", turn=-0.05, gx=-0.2, gy=0.3, furrow=0.6, brow=-0.2, smile=0.45, armL="relaxed", armR="relaxed",
               snake_looks=(0.9 - 1.2 * ease((t - 1.0) / 0.5), 0.9 - 1.2 * ease((t - 1.3) / 0.5)),
               hisses=(ease((t - 1.0) / 0.3) * (1 - ease((t - 2.6) / 0.5)), ease((t - 1.4) / 0.3) * (1 - ease((t - 3.0) / 0.5))))
        z["blink"] = max(z["blink"], 0.28)
        return at_neck(ZAHHAK_KING, z, t, 540, 1040, 1.15)
    HS6 = Shot(7.8, closez, midH, cam=camH, light=BRAZ_CLOSE, grade="fire", bloom=0.6, fade_out=1.0)
    return [A, B, C, D, E1, E2, F, G, HS6]


SCENES = {"s1": s1, "s2": s2, "s3": s3, "s4": s4, "s5": s5, "s6": s6}
