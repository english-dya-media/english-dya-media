"""Part 1 · The Prince and the Stranger — 2D cartoon. Timing matches zahhak/p01_audio.py
(scene starts s1 0, s2 9.9, s3 14.5, s4 50.6, s5 100.4, s6 124.6; end card 138.0; total 143.0)."""
import math, random
from PIL import Image, ImageFilter, ImageDraw
from film import Shot, W, H, ease, lerp, talk_pose, blink_at, cam_push, cam_static, Motes, Embers, svg_render
from chars import pose, horse, camel, cow, goat, Ctx, FEET, fmt, prop, hand
from stage import at_neck, at_feet, rider, Glow, lw_for, random_spec
import bgs, zbg
from cast import *


def P(**kw):
    return pose(**kw)


def bg(name, fn, blur=0):
    """a zbg background, cached as build/bg/zh_<name>[_b<blur>].png"""
    if blur:
        return bgs.cached(f"zh_{name}_b{blur}", lambda: bgs.cached(f"zh_{name}", fn).filter(ImageFilter.GaussianBlur(blur)))
    return bgs.cached(f"zh_{name}", fn)


def cam_xy(cam, t, x, y):
    """where a point of the mid layer lands on the screen"""
    k, cx, cy, px, py = cam(t)
    return (x - cx) * k + cx + px, (y - cy) * k + cy + py


def tp(lines, t, seed, **kw):
    return P(**talk_pose(lines, t, seed, kw))


def torch_flame(x, y, t, s=1.0, seed=0):
    """a torch flame standing on (x, y)"""
    ph = seed * 1.3
    h = (120 + 30 * math.sin(t * 13 + ph) + 18 * math.sin(t * 7.3 + ph)) * s
    sw = 10 * math.sin(t * 5 + ph) * s
    return (f'<path d="M {x - 30 * s:.1f} {y:.1f} C {x - 40 * s:.1f} {y - h * 0.45:.1f}, {x - 10 * s + sw:.1f} {y - h * 0.8:.1f}, {x + sw:.1f} {y - h:.1f} '
            f'C {x + 14 * s + sw:.1f} {y - h * 0.75:.1f}, {x + 40 * s:.1f} {y - h * 0.45:.1f}, {x + 30 * s:.1f} {y:.1f} Z" fill="#ff8a1a"/>'
            f'<path d="M {x - 16 * s:.1f} {y:.1f} C {x - 20 * s:.1f} {y - h * 0.35:.1f}, {x - 4 * s + sw * 0.6:.1f} {y - h * 0.6:.1f}, {x + sw * 0.6:.1f} {y - h * 0.72:.1f} '
            f'C {x + 8 * s + sw * 0.6:.1f} {y - h * 0.55:.1f}, {x + 20 * s:.1f} {y - h * 0.35:.1f}, {x + 16 * s:.1f} {y:.1f} Z" fill="#ffd84a"/>'
            f'<ellipse cx="{x:.1f}" cy="{y - h * 0.18:.1f}" rx="{9 * s:.1f}" ry="{16 * s:.1f}" fill="#fff6c0"/>')


def flipped(svg, x, y, s):
    """an animal drawn facing right, turned to face left, origin at (x, y)"""
    return f'<g transform="translate({x:.1f},{y:.1f}) scale({-s:.4f},{s:.4f})">{svg}</g>'


def placed(svg, x, y, s):
    return f'<g transform="translate({x:.1f},{y:.1f}) scale({s:.4f})">{svg}</g>'


def darken(peak, t0, t1, col=(0, 0, 0)):
    """an fx that darkens the frame from t0 to t1 (smoothly in and out)"""
    def fx(im, t):
        a = ease((t - t0) / 0.4) * (1 - ease((t - t1 + 0.4) / 0.4)) if t1 > t0 else 0
        if a > 0:
            im.alpha_composite(Image.new("RGBA", (W, H), col + (int(255 * peak * a),)))
    return fx


def fade_to(col, t0, t1, peak=1.0):
    def fx(im, t):
        a = ease((t - t0) / max(0.01, t1 - t0)) * peak
        if a > 0:
            im.alpha_composite(Image.new("RGBA", (W, H), col + (int(255 * a),)))
    return fx


WARM = (1.0, 0.7, 0.4)
TORCH = dict(ambient=(0.8, 0.74, 0.82), point=(40, 700, 1100, 0.55, 1.15, (1.0, 0.55, 0.25)), rim_point=(-400, 6), rim_col=(1.0, 0.62, 0.3), rim_str=0.95)
HALL = dict(ambient=(0.74, 0.68, 0.78), point=(540, 720, 760, 0.55, 1.1, (1.0, 0.55, 0.25)), rim=(0, -3), rim_col=(1.0, 0.65, 0.35), rim_str=0.6)
PLAIN = dict(rim=(-5, -2), rim_col=WARM, ramp=(0, W, 1.06, 0.88), ambient=(1.0, 0.98, 0.94))
YARD = dict(rim=(5, -2), rim_col=(1.0, 0.74, 0.5), ramp=(0, W, 0.9, 1.06), ambient=(1.0, 0.95, 0.92))
NIGHT = dict(ambient=(0.6, 0.68, 0.95), rim=(5, -3), rim_col=(0.72, 0.82, 1.0), rim_str=0.6)
WINDOW = dict(ambient=(0.62, 0.68, 0.92), rim=(-5, -3), rim_col=(0.75, 0.85, 1.0), rim_str=0.75)
PREDAWN = dict(ambient=(0.74, 0.74, 0.92), rim=(5, -3), rim_col=(1.0, 0.82, 0.9), rim_str=0.5)
WINDOW_PD = dict(ambient=(0.72, 0.72, 0.92), rim=(-5, -3), rim_col=(1.0, 0.85, 0.92), rim_str=0.6)


# ================================================================ S1 the snake king (0-9.9)
def king(t, lines, seed, **kw):
    base = dict(legs="sit", turn=0.08, gx=0.2, gy=0.1, furrow=0.6, brow=-0.1, armL="relaxed", armR="relaxed", wind=0.05)
    base.update(kw)
    return tp(lines, t, seed, **base)


def hall_fx(cam, flames, embers_seed=1):
    out = []
    for i, (x, y) in enumerate(flames):
        out.append(Glow(lambda t, x=x, y=y: cam_xy(cam, t, x, y - 60), 190, (255, 170, 90), 0.45))
        out.append(Embers(14, embers_seed + i, (x - 40, y - 260, x + 40, y - 60), (50, 120)))
    return out


def s1():
    close = bg("hall_close", zbg.hall_close)
    camA = cam_push(1.0, 1.06, 540, 900, 4.0)
    LA = [("p1s1a", 1.0)]

    def midA(t):
        stroke = ("ik", 250 + 16 * math.sin(t * 2.2), 150 + 26 * math.sin(t * 2.2), "down")
        q = king(t, LA, 3, turn=0.22, gx=0.8, gy=-0.4, armL=stroke, armR="relaxed",
                 snake_looks=(1.0, -0.85 + 0.15 * math.sin(t * 1.3)), hisses=(0.6 * max(0.0, 1 - abs(t - 0.8) / 0.6), 0.0))
        q["blink"] = max(q["blink"], 0.32)
        return torch_flame(40, 740, t, 1.1) + torch_flame(1040, 740, t + 1.7, 1.1, 1) + at_neck(ZAHHAK_KING, q, t, 560, 1040, 1.0)
    A = Shot(4.0, close, midA, cam=camA, light=TORCH, fx=hall_fx(camA, [(40, 740), (1040, 740)]), grade="fire", bloom=0.6, fade_in=0.6)

    hall = bg("hall", zbg.hall)
    camB = cam_push(1.0, 1.05, 540, 880, 3.0)

    def midB(t):
        q = king(t + 4.0, [], 4, turn=0.0, gx=0.0, gy=0.3, snake_looks=(0.9, 0.7))
        return torch_flame(80, 640, t, 0.75) + torch_flame(1000, 640, t + 1.3, 0.75, 1) + at_neck(ZAHHAK_KING, q, t, 540, 793, 0.36)
    B = Shot(3.0, hall, midB, cam=camB, light=HALL, fx=hall_fx(camB, [(80, 640), (1000, 640)], 3) + [Motes(40, 4, (255, 210, 150), (200, 300, 880, 1300), (4, -6), amax=70)],
             grade="fire", bloom=0.7)

    closeb = bg("hall_close", zbg.hall_close, 5)
    camC = cam_push(1.0, 1.08, 420, 800, 2.9)

    def midC(t):
        op = ease((t - 0.5) / 0.4)
        h = ease((t - 1.15) / 0.35) * (1 - 0.3 * ease((t - 2.3) / 0.5))
        q = king(t + 7.0, [], 5, turn=0.06, gx=0.05, gy=0.15, furrow=1.0, brow=-0.5,
                 snake_looks=(1.0, -0.9 + 0.5 * ease((t - 1.0) / 0.6)), hisses=(0.0, h))
        q["blink"] = max(q["blink"] * op, 1.0 - op, 0.22)
        return torch_flame(40, 740, t, 1.1) + at_neck(ZAHHAK_KING, q, t, 380, 1150, 1.9)
    C = Shot(2.9, closeb, midC, cam=camC, light=TORCH, fx=[Glow(lambda t: cam_xy(camC, t, 40, 680), 220, (255, 170, 90), 0.4)],
             grade="fire", bloom=0.6, fade_out=0.5)
    return [A, B, C]


# ================================================================ S2 title (9.9-14.5)
def s2():
    hall = bg("hall", zbg.hall)
    cam = cam_push(1.05, 1.12, 540, 880, 4.6)

    def mid(t):
        q = king(t + 9.9, [], 4, turn=0.0, gx=0.0, gy=0.3, snake_looks=(0.9, 0.7))
        return torch_flame(80, 640, t, 0.75) + torch_flame(1000, 640, t + 1.3, 0.75, 1) + at_neck(ZAHHAK_KING, q, t, 540, 793, 0.36)
    return [Shot(4.6, hall, mid, cam=cam, light=HALL, fx=hall_fx(cam, [(80, 640), (1000, 640)], 7) + [Embers(40, 9, (60, 700, 1020, 1500), (60, 150))],
                 grade="fire", bloom=0.7, fade_in=0.3, fade_out=0.5)]


# ================================================================ S3 Mardas's land (14.5-50.6)
def queue_far():
    r = random.Random(11)
    body = ""
    for k in range(7):
        S = random_spec(r, ("man", "woman", "boy", "woman", "man"))
        x = 700 - 22 * k + r.uniform(-6, 6); y = 1034 + 13 * k
        body += at_feet(S, P(turn=0.45, gx=0.8, gy=-0.2, armL="hold_bread", armR="hold_bread", propL="bowl"), r.uniform(0, 3), x, y, 0.075 + 0.002 * k)
    return svg_render(body)


def s3():
    plain = bg("plain", zbg.plain)
    q_img = bgs.cached("zh_p1_queue", queue_far)

    def bgA1(t):
        im = plain.copy(); im.alpha_composite(q_img); return im
    camA1 = cam_push(1.0, 1.06, 640, 1000, 7.1)
    r = random.Random(5)
    flock = [(380 + 34 * k + r.uniform(-14, 14), 1046 + r.uniform(0, 50), r.uniform(0.17, 0.21), r.choice(["#e9e3d6", "#7a5a3a", "#2c2624", "#e9e3d6"]),
              r.uniform(0, 6), r.random() < 0.5) for k in range(9)]

    def herd_far(t):
        c = Ctx(lw_for(0.2))
        o = ""
        for (x, y, s, ph) in [(250, 1010, 0.16, 0.0), (318, 1024, 0.17, 2.0)]:
            o += placed(cow(c, t=t + ph, graze=0.5 + 0.5 * math.sin(t * 0.7 + ph)), x, y, s)
        for k, (x, y, s, col, ph, walk) in enumerate(sorted(flock, key=lambda f: f[1])):
            dark = {"#e9e3d6": "#b9ae9a", "#7a5a3a": "#5a3e26", "#2c2624": "#1a1614"}[col]
            xx = x - (10 * t if walk else 0)
            o += placed(goat(c, col=col, dark=dark, t=t + ph, graze=0 if walk else 0.5 + 0.5 * math.sin(t + ph), walk=walk, phase=t * 5 + ph), xx, y, s)
        for k, (x, y, s) in enumerate([(930, 1062, 0.19), (1040, 1078, 0.2)]):
            o += flipped(camel(c, t=t + k, walk=True, phase=t * 3.2 + k * 1.3, saddle=False), x - 16 * t, y, s)
        o += at_feet(HERDSMAN, P(legs="walk", phase=t * 4.2, turn=-0.4, gx=-0.7, armR="relaxed", armL=("ik", 120, 330), propL="stick", wind=0.3), t, 760 - 14 * t, 1112, 0.085)
        return o
    A1 = Shot(7.1, bgA1, herd_far, cam=camA1, light=PLAIN, sun=(210, 680, 700, (0.10, 0.07, 0.03)),
              fx=[Motes(40, 6, (255, 240, 210), (0, 400, W, 1300), (-8, -3), amax=80)], fade_in=0.6)

    camA2 = cam_push(1.02, 1.06, 560, 1000, 3.4)

    def herd_near(t):
        c = Ctx(lw_for(0.5))
        o = placed(cow(c, t=t, graze=0.6 + 0.4 * math.sin(t * 0.8)), 110, 1200, 0.42)
        for k, (x, y, s_, col, ph) in enumerate([(330, 1104, 0.36, "#e9e3d6", 0.0), (470, 1122, 0.38, "#2c2624", 1.0), (600, 1140, 0.4, "#7a5a3a", 2.0),
                                                  (420, 1160, 0.42, "#e9e3d6", 2.7)]):
            dark = {"#e9e3d6": "#b9ae9a", "#7a5a3a": "#5a3e26", "#2c2624": "#1a1614"}[col]
            o += placed(goat(c, col=col, dark=dark, t=t + ph, walk=True, phase=t * 5.5 + ph), x - 24 * t, y, s_)
        for k, (x, y, s_) in enumerate([(860, 1300, 0.58), (1100, 1336, 0.6)]):
            o += flipped(camel(c, t=t + k, walk=True, phase=t * 3.4 + k * 1.7, saddle=False), x - 30 * t, y, s_)
        o += at_feet(HERDSMAN, P(legs="walk", phase=t * 4.8, turn=-0.45, gx=-0.8, armR="relaxed", armL=("ik", 120, 330), propL="stick", wind=0.4, smile=0.3,
                                 blink=blink_at(t, 9)), t, 300 - 26 * t, 1330, 0.42)
        return o
    A2 = Shot(3.4, plain, herd_near, cam=camA2, light=PLAIN, sun=(210, 680, 700, (0.10, 0.07, 0.03)),
              fx=[Motes(40, 7, (255, 240, 210), (0, 400, W, 1300), (-12, -3), amax=80)])

    gate = bg("gate", zbg.gate)
    r2 = random.Random(21)
    line_people = [(random_spec(r2, kinds), x, y, s_) for kinds, x, y, s_ in
                   [(("man",), 40, 1600, 0.5), (("woman",), 170, 1610, 0.52), (("man",), 300, 1622, 0.54)]]

    def midA3(t):
        o = ""
        for i, (S, x, y, s_) in enumerate(line_people):
            o += at_feet(S, P(turn=0.4, gx=0.7, gy=0.1, armL="hold_bread", armR="hold_bread", propL="bowl", blink=blink_at(t, 30 + i), breathe=math.sin(t * 2 + i)), t, x, y, s_)
        o += at_feet(POOR_MOTHER, P(turn=0.4, gx=0.7, gy=0.2, armL=("ik", 240, 250), armR="relaxed", propL="milk_bowl", blink=blink_at(t, 33), smile=0.5), t, 470, 1640, 0.56)
        pour_ang = 70 + 6 * math.sin(t * 2)
        m = P(turn=0.38, gx=0.75, gy=0.45, smile=0.6, armL=("ik", 300, 70), propL=("jug", pour_ang), armR="relaxed", blink=blink_at(t, 34), breathe=math.sin(t * 1.6))
        o += at_feet(MARDAS, m, t, 830, 1650, 0.58, flip=True)
        return o
    A3 = Shot(3.4, gate, midA3, cam=cam_push(1.0, 1.04, 540, 1000, 3.4), light=dict(rim=(-5, -2), rim_col=WARM, ramp=(0, W, 1.04, 0.9)),
              sun=(540, 700, 800, (0.08, 0.06, 0.02)), fx=[Motes(30, 8, (255, 240, 210), (200, 300, 880, 1300), (4, -4), amax=70)])

    gateb = bg("gate", zbg.gate, 8)
    LB1 = [("p1s3d", 0.5)]

    def midB1(t):
        lift = 30 * ease((t - 0.4) / 0.4)
        b = tp(LB1, t, 40, turn=0.38, gx=0.75, gy=-0.7, brow=0.6, furrow=-0.3, armL=("ik", 100, 290 - lift), armR=("ik", -100, 290 - lift))
        bx, by = 470, 720 + (300 - lift) * 0.744 + 4
        bowl = (f'<path d="M {bx - 92:.1f} {by - 8:.1f} L {bx + 92:.1f} {by - 8:.1f} C {bx + 86:.1f} {by + 58:.1f}, {bx - 86:.1f} {by + 58:.1f}, {bx - 92:.1f} {by - 8:.1f} Z" fill="#8a5a32" stroke="#1b0f0a" stroke-width="3.5"/>'
                f'<ellipse cx="{bx:.1f}" cy="{by - 8:.1f}" rx="91" ry="15" fill="#5a3418" stroke="#1b0f0a" stroke-width="3"/>'
                f'<path d="M {bx - 60:.1f} {by + 22:.1f} C {bx - 20:.1f} {by + 36:.1f}, {bx + 20:.1f} {by + 36:.1f}, {bx + 60:.1f} {by + 22:.1f}" stroke="#c08a52" stroke-width="4" fill="none" opacity="0.7"/>')
        return at_neck(POOR_BOY, b, t, 470, 720, 1.2) + bowl
    B1 = Shot(2.2, gateb, midB1, cam=cam_push(1.0, 1.03, 470, 700, 2.2), light=dict(rim=(-6, -2), rim_col=WARM, ramp=(0, W, 1.05, 0.88)),
              sun=(540, 600, 800, (0.08, 0.06, 0.02)))

    LB2 = [("p1s3e", 0.3)]

    def midB2(t):
        m = tp(LB2, t, 41, turn=0.3, gx=0.7, gy=0.55, smile=0.75, brow=0.25, furrow=-0.4, armL="relaxed", armR="relaxed")
        return at_neck(MARDAS, m, t, 560, 1060, 1.4, flip=True)
    B2 = Shot(2.4, gateb, midB2, cam=cam_push(1.0, 1.03, 560, 850, 2.4), light=dict(rim=(-6, -2), rim_col=WARM, ramp=(0, W, 1.05, 0.88)),
              sun=(540, 600, 800, (0.08, 0.06, 0.02)))

    gateb2 = bgs.cached("zh_gate_insert", lambda: Image.alpha_composite(bgs.cached("zh_gate", zbg.gate).filter(ImageFilter.GaussianBlur(18)),
                                                                          Image.new("RGBA", (W, H), (40, 24, 12, 110))))

    def midB3(t):
        c = Ctx(1.0)
        lvl = ease((t - 0.25) / 1.4)
        ang = -95 + 5 * math.sin(t * 2.2)
        jx, jy, js = 700, 330, 3.0
        a = math.radians(-ang)
        sx_, sy_ = 132 * math.cos(a) + 52 * math.sin(a), 132 * math.sin(a) - 52 * math.cos(a)
        tx, ty = jx - js * sx_, jy + js * sy_
        bx, by = 500, 900
        o = (f'<path d="M 1150 120 L 1190 330 L {jx + 50} {jy + 50} L {jx - 10} {jy - 40} Z" fill="#ece5d6" stroke="#1b0f0a" stroke-width="6"/>'
             f'<path d="M 1150 120 L 1166 210 L {jx + 70} {jy + 10} L {jx + 34} {jy - 26} Z" fill="#c8bea8" opacity="0.6"/>'
             f'<circle cx="{jx + 24}" cy="{jy + 6}" r="48" fill="#c9a24a" stroke="#1b0f0a" stroke-width="5"/>')
        o += f'<g transform="translate({jx},{jy}) scale({-js},{js}) rotate({-ang:.1f})">{prop(c, "jug", 0, 0, 0, t)}</g>'
        o += f'<g transform="translate({jx + 6},{jy + 6}) scale(1.3) translate({-jx - 6},{-jy - 6})">{hand(c, MARDAS, jx + 6, jy + 6, 20, 1)}</g>'
        if 0.15 < t < 1.85:
            w = 16 + 2 * math.sin(t * 17)
            d = f"M {tx:.1f} {ty:.1f} C {tx - 6:.1f} {ty + 90:.1f}, {bx + 40 + 6 * math.sin(t * 9):.1f} {by - 150:.1f}, {bx + 30:.1f} {by - 14:.1f}"
            o += (f'<path d="{d}" stroke="#b8a888" stroke-width="{w + 6:.1f}" fill="none" stroke-linecap="round" opacity="0.6"/>'
                  f'<path d="{d}" stroke="#fdfaf2" stroke-width="{w:.1f}" fill="none" stroke-linecap="round"/>')
        o += (f'<path d="M {bx - 230} {by - 14} L {bx + 230} {by - 14} C {bx + 216} {by + 150}, {bx - 216} {by + 150}, {bx - 230} {by - 14} Z" fill="#8a5a32" stroke="#1b0f0a" stroke-width="6"/>'
              f'<ellipse cx="{bx}" cy="{by - 14}" rx="228" ry="40" fill="#5a3418" stroke="#1b0f0a" stroke-width="5"/>'
              f'<ellipse cx="{bx}" cy="{by - 12 + 18 * (1 - lvl):.1f}" rx="{206 * (0.55 + 0.45 * lvl):.1f}" ry="{32 * (0.55 + 0.45 * lvl):.1f}" fill="#f8f4ec" opacity="{min(1, lvl * 3):.2f}"/>'
              f'<path d="M {bx - 160} {by + 50} C {bx - 60} {by + 84}, {bx + 60} {by + 84}, {bx + 160} {by + 50}" stroke="#c08a52" stroke-width="7" fill="none" opacity="0.7"/>')
        if 0.2 < t < 1.9:
            k = (t * 2.5) % 1; rr = 26 + 40 * k
            o += f'<ellipse cx="{bx + 30}" cy="{by - 12}" rx="{rr:.1f}" ry="{rr * 0.2:.1f}" fill="none" stroke="#ffffff" stroke-width="3" opacity="{0.8 * (1 - k):.2f}"/>'
        for sd in (-1, 1):
            hx_, hy_ = bx + sd * 238, by + 40
            o += (f'<path d="M {hx_ + sd * 330} {by + 700} L {hx_ + sd * 60} {hy_ + 46} L {hx_ - sd * 30} {hy_ - 18} L {hx_ + sd * 200} {by + 760} Z" fill="#6a7f8f" stroke="#1b0f0a" stroke-width="5"/>'
                  f'<circle cx="{hx_ + sd * 18:.1f}" cy="{hy_ + 16:.1f}" r="46" fill="#8a9aa8" stroke="#1b0f0a" stroke-width="4"/>'
                  f'<g transform="translate({hx_},{hy_}) scale(1.5) translate({-hx_},{-hy_})">{hand(c, POOR_BOY, hx_, hy_, sd * 70, sd)}</g>')
        return o
    B3 = Shot(2.0, gateb2, midB3, cam=cam_push(1.0, 1.04, 520, 700, 2.0), light=dict(rim=(-6, -2), rim_col=WARM, ramp=(0, W, 1.05, 0.9)),
              sun=(540, 500, 700, (0.10, 0.07, 0.02)))

    LC = [("p1s3f", 0.3)]; LCh = [("p1s3g", 2.3)]

    def midC(t):
        sad = 0.25 * ease((t - 4.0) / 0.6)
        m = tp(LC, t, 42, turn=-0.32, gx=-0.75, gy=0.05, smile=0.4 * (1 - ease((t - 3.6) / 0.6)), sad=sad, armL="relaxed", armR="relaxed")
        pt = ease((t - 2.4) / 0.4) * (1 - ease((t - 4.4) / 0.4))
        h = tp(LCh, t, 43, turn=0.34 - 0.3 * pt, gx=0.8 - 1.4 * pt, gy=0.0, smile=0.25, nod=6 * ease((t - 2.0) / 0.3) * (1 - ease((t - 2.6) / 0.3)), armL="relaxed",
               armR=("ik", lerp(-200, -420, pt), lerp(420, -40, pt)) if pt > 0.01 else "relaxed")
        return at_neck(HERDSMAN, h, t, 300, 1000, 0.95) + at_neck(MARDAS, m, t, 760, 990, 0.95)
    C = Shot(5.0, gateb, midC, cam=cam_push(1.0, 1.04, 540, 850, 5.0), light=dict(rim=(-6, -2), rim_col=WARM, ramp=(0, W, 1.05, 0.88)),
             sun=(540, 600, 800, (0.08, 0.06, 0.02)), fade_out=0.3)

    strip = bgs.cached("zh_ride_strip", zbg.ride_strip)

    def bgD(t):
        x0 = int(300 + 300 * t)
        return strip.crop((x0, 0, x0 + W, H))
    herd = [(r.uniform(-60, 1100), r.uniform(1150, 1210), r.uniform(0.2, 0.26), r.choice(["#5a3a22", "#3a2a1e", "#7a4a2a", "#2a2226", "#8a6a4a"]), r.uniform(0, 6),
             r.uniform(-20, 20)) for _ in range(7)]

    def midD(t):
        c = Ctx(lw_for(0.25))
        o = ""
        for (x, y, s, col, ph, v) in sorted(herd, key=lambda h_: h_[1]):
            o += placed(horse(c, col=col, walk=True, phase=t * 10 + ph, t=t + ph, saddle=False, head_bob=-12 * math.sin(t * 10 + ph)), (x + v * t) % 1240 - 80, y, s)
        for k in range(10):                                                    # dust kicked up behind
            age = ((t * 2.2 + k * 0.1) % 1.0)
            dx = -age * 420; r_ = 20 + 70 * age
            o += f'<ellipse cx="{360 + dx + 20 * math.sin(k * 3.1):.1f}" cy="{1345 - 40 * age - 6 * (k % 3):.1f}" rx="{r_:.1f}" ry="{r_ * 0.5:.1f}" fill="#cdb084" opacity="{0.8 * (1 - age):.2f}"/>'
        q = P(turn=0.45, gx=0.9, gy=0.1, smile=0.55, brow=0.3, furrow=-0.2, armR="forward", armL="forward", wind=1.0, blink=blink_at(t, 44), tilt=4)
        bounce = -14 * abs(math.sin(t * 10.5)); pitch = 3 * math.sin(t * 10.5)
        o += (f'<g transform="translate(0,{bounce:.1f}) rotate({pitch:.2f},540,1200)">' +
              rider(ZAHHAK_PRINCE, q, t, lambda c_: horse(c_, col="#1e1a1e", mane="#0a0808", walk=True, phase=t * 10.5, t=t, head_bob=-18 * math.sin(t * 10.5),
                                                         blanket="#8e1a24"), 470, 1350, 1.0) + '</g>')
        return o
    D = Shot(5.0, bgD, midD, cam=cam_static(), light=dict(rim=(-5, -2), rim_col=WARM, ramp=(0, W, 1.06, 0.9)),
             fx=[Motes(70, 9, (214, 180, 130), (0, 1150, 700, 1420), (-320, -10), (2, 6), 150)], sun=(150, 700, 700, (0.10, 0.07, 0.03)))

    stripb = bgs.cached("zh_ride_strip_e_b6", lambda: strip.crop((1700, 0, 1700 + W, H)).filter(ImageFilter.GaussianBlur(6)))
    LE = [("p1s3i", 0.4)]

    def midE(t):
        c = Ctx(lw_for(1.4))
        pat = 30 * math.sin(t * 3.0)
        c = Ctx(lw_for(2.6))
        o = placed(horse(c, col="#1e1a1e", mane="#0a0808", t=t, head_bob=6 * math.sin(t * 1.3), saddle=True, blanket="#8e1a24"), -520, 1800, 2.2)
        z = tp([], t, 45, turn=-0.18, gx=-0.4 if t < 3.0 else 0.4, gy=-0.1, smile=0.6 * (1 - 0.6 * ease((t - 3.2) / 0.8)), brow=0.3, furrow=-0.2, wind=0.7,
               armR=("ik", -292 + pat * 0.3, -175 + pat * 0.4, "down"), armL="relaxed")
        return o + at_neck(ZAHHAK_PRINCE, z, t, 680, 1000, 1.3)
    E = Shot(5.6, stripb, midE, cam=cam_push(1.0, 1.05, 600, 850, 5.6), light=dict(rim=(-6, -2), rim_col=WARM, ramp=(0, W, 1.05, 0.88)),
             fx=[Motes(40, 10, (255, 230, 190), (0, 300, W, 1300), (-30, -4), amax=80), darken(0.22, 3.4, 9.0, (20, 10, 30))],
             sun=(150, 700, 700, (0.10, 0.07, 0.03)), fade_out=0.6)
    return [A1, A2, A3, B1, B2, B3, C, D, E]


# ================================================================ S4 the stranger (50.6-100.4)
def black_horse(c, t, head_down=0.0, bob=0.0):
    return horse(c, col="#1e1a1e", mane="#0a0808", t=t, head_bob=bob, saddle=False, head_down=head_down)


def s4():
    yard = bg("yard", zbg.yard)
    yardb = bg("yard", zbg.yard, 8)
    camA = cam_push(1.0, 1.05, 600, 1000, 5.6)
    LA = []

    def midA(t):
        c = Ctx(lw_for(1.45))
        o = placed(black_horse(c, t, head_down=0.1 + 0.05 * math.sin(t * 0.7)), 113, 1480, 1.45)
        br = 40 * math.sin(t * 5.2)
        z = tp(LA, t, 50, turn=-0.4, gx=-0.8, gy=0.25, smile=0.3, armR=("ik", -330 + br, 80 + 0.3 * br), propR="brush", armL="relaxed", wind=0.2)
        o += at_feet(ZAHHAK_PRINCE, z, t, 760, 1480, 0.48)
        if t > 2.6:
            u = ease((t - 2.6) / 3.0)
            ib = P(legs="walk" if u < 1 else "stand", phase=t * 5.6, turn=-0.45, gx=-0.8, smile=0.55, armL="relaxed", armR="relaxed", blink=blink_at(t, 51))
            o += at_feet(IBLIS_FRIEND, ib, t, lerp(905, 960, u), lerp(1395, 1500, u), lerp(0.36, 0.47, u))
        return o
    A = Shot(5.6, yard, midA, cam=camA, light=YARD, sun=(900, 990, 700, (0.10, 0.07, 0.03)),
             fx=[Motes(50, 11, (255, 236, 200), (0, 400, W, 1400), (-6, -4), amax=90)], fade_in=0.5)

    LB = [("p1s4b", 0.3), ("p1s4c", 2.7)]; LBz = [("p1s4d", 5.0)]

    def midB(t):
        c = Ctx(lw_for(1.9))
        o = placed(black_horse(c, t, head_down=0.05, bob=4 * math.sin(t)), -470, 1800, 1.9)
        admire = t < 2.6
        ib = tp(LB, t, 52, turn=-0.35, gx=-0.8 if not admire else -1.0, gy=0.0 if not admire else -0.25, smile=0.7, brow=0.35, furrow=-0.35,
                armL="offer" if 0.3 < t < 2.4 else "relaxed", armR="chest" if t > 2.6 else "relaxed")
        z = tp(LBz, t, 53, turn=0.35 if t > 1.0 else 0.1, gx=0.8 if t > 1.0 else -0.4, gy=0.0, smile=0.45 * ease((t - 2.8) / 0.6) * (1 - ease((t - 4.6) / 0.4)),
               brow=0.5 * ease((t - 4.6) / 0.3), armL="relaxed", armR=("ik", -260, 300))
        return o + at_neck(ZAHHAK_PRINCE, z, t, 420, 960, 0.85) + at_neck(IBLIS_FRIEND, ib, t, 800, 975, 0.85)
    B = Shot(6.4, yardb, midB, cam=cam_push(1.0, 1.04, 560, 850, 6.4), light=YARD, sun=(900, 900, 700, (0.10, 0.07, 0.03)))

    LC = [("p1s4e", 0.3), ("p1s4f", 3.2)]

    def midC(t):
        lean = ease((t - 3.0) / 0.5)
        ib = tp(LC, t, 54, turn=-0.3, gx=-0.65, gy=0.05, smile=0.65 - 0.2 * lean, brow=0.35 + 0.15 * lean, furrow=-0.3, tilt=-3 * lean,
                armR=("ik", -270, 120 - 30 * lean, "down") if t > 3.2 else "relaxed", armL="relaxed")
        return at_neck(IBLIS_FRIEND, ib, t, 600 - 20 * lean, 1060, 1.45)
    C = Shot(7.0, yardb, midC, cam=cam_push(1.0, 1.05, 600, 850, 7.0), light=YARD, sun=(900, 900, 700, (0.10, 0.07, 0.03)))

    LD = [("p1s4g", 0.3)]

    def midD(t):
        g = ease((t - 1.8) / 0.25) * (1 - ease((t - 2.7) / 0.4))
        z = tp(LD, t, 55, turn=0.3, gx=0.7, gy=0.05, smile=0.2 * (1 - g), brow=0.2 + 0.5 * g, furrow=0.1, armL="chest", armR="relaxed", wind=0.15 + 1.2 * g)
        if g > 0.3:
            z["blink"] = max(z["blink"], 0.6)
        return at_neck(ZAHHAK_PRINCE, z, t, 470, 1060, 1.45)
    D = Shot(3.2, yardb, midD, cam=cam_push(1.0, 1.04, 470, 850, 3.2), light=YARD, sun=(900, 900, 700, (0.10, 0.07, 0.03)),
             fx=[darken(0.45, 1.8, 2.9, (10, 8, 20)), Motes(60, 12, (255, 236, 200), (0, 300, W, 1300), (-220, -20), amax=120)])

    LE = [("p1s4h", 0.3), ("p1s4i", 5.0)]

    def midE(t):
        close_in = ease(t / 8.0)
        ib = tp(LE, t, 56, turn=-0.32, gx=-0.75, gy=0.0, smile=0.5, brow=0.2, furrow=0.1, tilt=-2 - 2 * close_in,
                armL="offer" if 5.6 < t < 9.2 else "relaxed", armR="chest" if 0.6 < t < 4.4 else "relaxed")
        troubled = ease((t - 6.6) / 0.8)
        z = tp([], t, 57, turn=0.32, gx=0.75, gy=0.05 + 0.4 * troubled, smile=0.25 * (1 - troubled), brow=0.3 * troubled, furrow=0.2 + 0.6 * troubled,
               sad=0.25 * troubled, armL="relaxed", armR="relaxed")
        return at_neck(ZAHHAK_PRINCE, z, t, 370, 980, 0.95) + at_neck(IBLIS_FRIEND, ib, t, 740 - 40 * close_in, 990, 0.95)
    E = Shot(9.8, yardb, midE, cam=cam_push(1.0, 1.07, 560, 850, 9.8), light=dict(YARD, ambient=(0.94, 0.9, 0.9)), sun=(900, 900, 600, (0.08, 0.05, 0.02)),
             fx=[darken(0.12, 4.0, 12.0, (20, 10, 30))])

    LF = [("p1s4j", 0.3)]

    def midF(t):
        back = ease((t - 0.2) / 0.5)
        z = tp(LF, t, 58, turn=0.3, gx=0.8, gy=-0.05, brow=0.8 * (1 - ease((t - 1.6) / 0.5)), furrow=0.2 + 0.8 * ease((t - 1.4) / 0.5), sad=0.2,
               armL=("ik", 230, 150) if 1.3 < t < 4.0 else "relaxed", armR="relaxed", nod=-6 * back)
        return at_neck(ZAHHAK_PRINCE, z, t, 470 - 40 * back, 1060, 1.45)
    F = Shot(4.8, yardb, midF, cam=cam_push(1.0, 1.04, 470, 850, 4.8), light=dict(YARD, ambient=(0.92, 0.88, 0.9)), sun=(900, 900, 600, (0.08, 0.05, 0.02)),
             fx=[darken(0.15, -1, 9, (20, 10, 30))])

    LG = [("p1s4k", 0.2), ("p1s4l", 4.2)]

    def midG(t):
        ib = tp(LG, t, 59, turn=-0.22, gx=-0.35, gy=0.0, smile=0.25 + 0.15 * ease((t - 4.0) / 0.6), brow=-0.3, furrow=0.6, armL="relaxed", armR="relaxed")
        ib["blink"] = max(ib["blink"], 0.28)
        return at_neck(IBLIS_FRIEND, ib, t, 600, 1060, 1.5)
    G = Shot(6.5, yardb, midG, cam=cam_push(1.0, 1.06, 600, 830, 6.5), light=dict(YARD, ambient=(0.8, 0.76, 0.84), rim_str=1.0), sun=(900, 900, 500, (0.06, 0.03, 0.01)),
             fx=[darken(0.3, -1, 9, (14, 8, 24))])

    LH = [("p1s4m", 0.4)]; LHi = [("p1s4n", 2.2)]

    def midH(t):
        z = tp(LH, t, 60, turn=0.25, gx=0.3, gy=0.7, sad=0.45, brow=0.2, furrow=0.6, armL="relaxed", armR="relaxed", nod=8)
        reach = ease((t - 1.6) / 0.7)
        ib = tp(LHi, t, 61, turn=-0.35, gx=-0.8, gy=0.25, smile=0.55, brow=0.1, furrow=0.0,
                armR=("ik", lerp(-220, -420, reach), lerp(420, 70, reach), "down") if t > 1.6 else "relaxed", armL="relaxed")
        return at_neck(ZAHHAK_PRINCE, z, t, 330, 985, 0.95) + at_neck(IBLIS_FRIEND, ib, t, 880 - 30 * reach, 990, 0.95)
    Hs = Shot(6.5, yardb, midH, cam=cam_push(1.0, 1.05, 560, 850, 6.5), light=dict(YARD, ambient=(0.86, 0.82, 0.88)), sun=(900, 900, 500, (0.06, 0.03, 0.01)),
              fx=[darken(0.18, -1, 9, (14, 8, 24))], fade_out=0.8)
    return [A, B, C, D, E, F, G, Hs]


# ================================================================ S5 the garden at night (100.4-124.6)
def branches_svg(x, y, cover, seed=0, w=170):
    """branches and leaves laid over the pit at (x, y); cover 0..1"""
    r = random.Random(seed)
    o = ""
    n = int(10 * cover)
    for k in range(n):
        a = r.uniform(-0.4, 0.4); L = r.uniform(0.7, 1.1) * w
        cx_ = x + r.uniform(-w * 0.35, w * 0.35); cy_ = y + r.uniform(-16, 16)
        x0, y0 = cx_ - math.cos(a) * L / 2, cy_ - math.sin(a) * L / 2 * 0.3
        x1, y1 = cx_ + math.cos(a) * L / 2, cy_ + math.sin(a) * L / 2 * 0.3
        o += f'<path d="M {x0:.1f} {y0:.1f} L {x1:.1f} {y1:.1f}" stroke="#3a2c20" stroke-width="8" stroke-linecap="round"/>'
        for j in range(6):
            u = r.uniform(0.1, 0.9); lx, ly = x0 + (x1 - x0) * u, y0 + (y1 - y0) * u
            o += f'<ellipse cx="{lx:.1f}" cy="{ly - 4:.1f}" rx="14" ry="6" fill="#2e4a30" stroke="#121c12" stroke-width="1.5" transform="rotate({r.uniform(-50, 50):.0f},{lx:.1f},{ly - 4:.1f})"/>'
    if cover > 0.7:
        a = (cover - 0.7) / 0.3
        for k in range(int(40 * a)):
            lx = x + r.uniform(-w * 0.6, w * 0.6); ly = y + r.uniform(-24, 24)
            o += f'<ellipse cx="{lx:.1f}" cy="{ly:.1f}" rx="9" ry="4" fill="#3a3626" opacity="0.9" transform="rotate({r.uniform(-60, 60):.0f},{lx:.1f},{ly:.1f})"/>'
    return o


def pit_svg(x, y, depth, cover=0.0, seed=0, scale=1.0):
    """the pit (an opening in the path) with the dug earth around it"""
    if depth <= 0:
        return ""
    rx, ry = 120 * scale * depth ** 0.5, 32 * scale * depth ** 0.5
    o = (f'<ellipse cx="{x}" cy="{y + 4 * scale:.1f}" rx="{rx + 14 * scale:.1f}" ry="{ry + 7 * scale:.1f}" fill="#2a2420"/>'
         f'<ellipse cx="{x}" cy="{y}" rx="{rx:.1f}" ry="{ry:.1f}" fill="#040406"/>'
         f'<path d="M {x - rx:.1f} {y:.1f} C {x - rx * 0.6:.1f} {y + ry * 0.6:.1f}, {x + rx * 0.6:.1f} {y + ry * 0.6:.1f}, {x + rx:.1f} {y:.1f}" stroke="#3a3028" stroke-width="{4 * scale:.1f}" fill="none"/>')
    if cover > 0:
        o += branches_svg(x, y, cover, seed, w=rx * 2.1)
    return o


def mound_svg(x, y, size, scale=1.0):
    if size <= 0:
        return ""
    w, h = 120 * scale * size ** 0.5, 46 * scale * size ** 0.6
    return (f'<path d="M {x - w:.1f} {y:.1f} C {x - w * 0.6:.1f} {y - h:.1f}, {x + w * 0.5:.1f} {y - h * 1.1:.1f}, {x + w:.1f} {y:.1f} Z" fill="#2e2620" stroke="#120e0c" stroke-width="3"/>'
            f'<path d="M {x - w * 0.5:.1f} {y - h * 0.55:.1f} C {x - w * 0.2:.1f} {y - h * 0.85:.1f}, {x + w * 0.2:.1f} {y - h * 0.9:.1f}, {x + w * 0.45:.1f} {y - h * 0.6:.1f}" stroke="#5a5a72" stroke-width="3" fill="none" opacity="0.6"/>')


def s5():
    gn = bg("garden_night", lambda: zbg.garden("night"))
    camA = cam_push(1.0, 1.08, 540, 1100, 9.6)

    def midA(t):
        if t < 7.2:
            return ""
        u = ease((t - 7.2) / 2.2)
        q = P(legs="walk" if u < 1 else "stand", phase=t * 5, turn=0.4 - 0.6 * u, gx=0.6 - 0.9 * u, gy=0.2, armL="relaxed", propL=("shovel", 6),
              armR="relaxed", smile=0.4, blink=blink_at(t, 70))
        return at_feet(IBLIS_FRIEND, q, t, lerp(250, 470, u), lerp(1290, 1330, u), lerp(0.31, 0.33, u))
    A = Shot(9.6, gn, midA, cam=camA, light=NIGHT, grade="night", fade_in=0.8,
             fx=[Motes(18, 13, (220, 240, 160), (100, 900, 980, 1500), (6, -10), (1.5, 3), 160)])

    gc = bg("garden_close_night", lambda: zbg.garden_close("night"))
    gcb = bg("garden_close_night", lambda: zbg.garden_close("night"), 5)
    DIG = 0.92
    PX, PY, PRX, PRY = 540, 965, 120, 32                                        # the pit (mid coords of garden_close)
    clip_id = "pitclip"
    clip = (f'<defs><clipPath id="{clip_id}"><path d="M -200 -200 L 1300 -200 L 1300 {PY} L {PX + PRX} {PY} '
            f'A {PRX} {PRY} 0 0 1 {PX - PRX} {PY} L -200 {PY} Z"/></clipPath></defs>')

    def midB(t):
        """Iblis down in the pit up to his waist, digging; seen close (the camera is pushed in on the pit)"""
        ph = (t % DIG) / DIG
        push = math.sin(min(1.0, ph / 0.45) * math.pi / 2) if ph < 0.45 else 1 - ease((ph - 0.45) / 0.3)
        lift = ease((ph - 0.45) / 0.35) * (1 - ease((ph - 0.85) / 0.15))
        s_ = 0.365; nx_, ny_ = 555, PY - 400 * s_ + 10 * push
        hu = (60 - 40 * lift, 230 + 80 * push - 40 * lift)                     # upper hand, at his right hip
        hl = (-170 - 130 * lift, 350 + 90 * push - 150 * lift)                 # lower hand, forward
        q = P(turn=-0.3, gx=-0.55, gy=0.7 - 0.5 * lift, furrow=0.3, smile=0.25, brow=-0.1, armL=("ik", hu[0], hu[1], "down"), armR=("ik", hl[0], hl[1], "down"),
              wind=0.1, blink=blink_at(t, 71), nod=10 * push - 4 * lift, tilt=-3 * push, legs="none")
        bsc = s_ * IBLIS_FRIEND["bs"]
        wu = (nx_ + hu[0] * bsc, ny_ + hu[1] * bsc); wl = (nx_ + hl[0] * bsc, ny_ + hl[1] * bsc)
        dx, dy = wl[0] - wu[0], wl[1] - wu[1]; L = math.hypot(dx, dy) or 1
        ux, uy = dx / L, dy / L
        top = (wu[0] - ux * 45, wu[1] - uy * 45); end = (wl[0] + ux * 190, wl[1] + uy * 190)
        nx, ny = -uy, ux
        blade = [(end[0] + nx * 18, end[1] + ny * 18), (end[0] - nx * 18, end[1] - ny * 18),
                 (end[0] - nx * 15 + ux * 48, end[1] - ny * 15 + uy * 48), (end[0] + ux * 60, end[1] + uy * 60), (end[0] + nx * 15 + ux * 48, end[1] + ny * 15 + uy * 48)]
        shovel = (f'<path d="M {top[0]:.1f} {top[1]:.1f} L {end[0]:.1f} {end[1]:.1f}" stroke="#1b0f0a" stroke-width="8" stroke-linecap="round"/>'
                  f'<path d="M {top[0]:.1f} {top[1]:.1f} L {end[0]:.1f} {end[1]:.1f}" stroke="#6a4424" stroke-width="5" stroke-linecap="round"/>'
                  f'<path d="M ' + " L ".join(f"{x:.1f} {y:.1f}" for x, y in blade) + ' Z" fill="#8e949e" stroke="#1b0f0a" stroke-width="2"/>')
        o = clip + mound_svg(390, 990, 0.6 + 0.4 * min(1.0, t / 5.0))
        o += f'<ellipse cx="{PX}" cy="{PY + 4}" rx="{PRX + 16}" ry="{PRY + 8}" fill="#2a2420"/><ellipse cx="{PX}" cy="{PY}" rx="{PRX}" ry="{PRY}" fill="#040406"/>'
        o += f'<g clip-path="url(#{clip_id})">' + at_neck(IBLIS_FRIEND, q, t, nx_, ny_, s_) + shovel + '</g>'
        o += f'<path d="M {PX - PRX} {PY} A {PRX} {PRY} 0 0 0 {PX + PRX} {PY}" stroke="#3a3028" stroke-width="7" fill="none"/>'
        if 0.55 < ph < 0.99:                                                    # earth thrown onto the pile
            k = (ph - 0.55) / 0.44
            sx0, sy0 = PX - 70, PY - 10
            rr_ = random.Random(int(t / DIG))
            for j in range(10):
                vx = rr_.uniform(90, 190); vy = rr_.uniform(170, 260); sz = rr_.uniform(5, 10)
                xx = sx0 - vx * k + rr_.uniform(-8, 8); yy = sy0 - vy * k + 330 * k * k
                o += f'<ellipse cx="{xx:.1f}" cy="{yy:.1f}" rx="{sz:.1f}" ry="{sz * 0.7:.1f}" fill="#6a5a46" stroke="#1a140e" stroke-width="1.5"/>'
        return o
    B = Shot(5.0, gc, midB, cam=cam_push(2.05, 2.15, 555, 945, 5.0), bg_par=1.0, light=NIGHT, grade="night")

    LC = [("p1s5d", 1.6)]

    def midC(t):
        drop = ease((t - 0.35) / 0.45)
        cover = ease((t - 0.7) / 0.6)
        o = mound_svg(380, 985, 1.0) + pit_svg(540, 965, 1.0, cover=cover, seed=4)
        up = ease((t - 1.3) / 0.5)
        hold = t < 0.8
        q = tp(LC, t, 72, turn=-0.35 + 0.15 * up, gx=-0.6 - 0.2 * up, gy=0.7 - 1.5 * up, furrow=0.2 - 0.4 * up, smile=0.3 + 0.4 * up, brow=0.4 * up,
               armR=("ik", -200, 330 + 80 * drop) if hold else "relaxed", armL=("ik", -20, 330 + 80 * drop) if hold else "relaxed")
        o += at_feet(IBLIS_FRIEND, q, t, 690, 975, 0.36)
        if t < 0.85:                                                            # the bundle of branches, carried and then dropped
            bx = lerp(690 - 40, 560, drop); by = lerp(975 - 360, 955, drop ** 1.6)
            r = random.Random(3)
            for k in range(7):
                a = r.uniform(-0.5, 0.5); L = 170
                o += (f'<path d="M {bx - math.cos(a) * L / 2:.1f} {by - math.sin(a) * L / 2:.1f} L {bx + math.cos(a) * L / 2:.1f} {by + math.sin(a) * L / 2:.1f}" '
                      f'stroke="#2a2018" stroke-width="6" stroke-linecap="round"/>')
                for j in range(4):
                    u = r.uniform(0.1, 0.9); lx = bx + math.cos(a) * L * (u - 0.5); ly = by + math.sin(a) * L * (u - 0.5)
                    o += f'<ellipse cx="{lx:.1f}" cy="{ly - 4:.1f}" rx="12" ry="5" fill="#2e4a30" transform="rotate({r.uniform(-50, 50):.0f},{lx:.1f},{ly - 4:.1f})"/>'
        return o
    C = Shot(4.6, gc, midC, cam=cam_push(1.04, 1.1, 600, 800, 4.6), light=NIGHT, grade="night")

    room = bg("window_room", zbg.window_room)
    wall = bg("window_wall", lambda: zbg.window_wall("night"))
    LD = []

    def midD(t):
        z = tp(LD, t, 73, turn=0.2, gx=0.3, gy=0.75, sad=0.5, brow=0.5, furrow=0.7, armL="relaxed", armR="relaxed", wind=0.05)
        z["blink"] = max(z["blink"], 0.2)
        return at_neck(ZAHHAK_PRINCE, z, t, 540, 1040, 1.25)
    D = Shot(5.0, room, midD, fg=wall, cam=cam_push(1.0, 1.06, 540, 800, 5.0), light=WINDOW, grade="night", fade_out=0.6)
    return [A, B, C, D]


# ================================================================ S6 before dawn (124.6-143.0)
def s6():
    gp = bg("garden_predawn", lambda: zbg.garden("predawn"))
    camA1 = cam_push(1.75, 1.8, 540, 1010, 2.0)

    def midA1(t):
        op = ease(t / 0.9)
        o = (f'<path d="M 500 1100 L 500 974 Q 540 934, 580 974 L 580 1100 Z" fill="#0c0a10"/>'
             f'<path d="M 500 1100 L 500 974 Q {lerp(540, 512, op):.1f} {lerp(934, 960, op):.1f}, {lerp(580, 516, op):.1f} {lerp(974, 990, op):.1f} '
             f'L {lerp(580, 516, op):.1f} 1100 Z" fill="#2a1a14" stroke="#1a100c" stroke-width="2"/>')
        if t > 0.6:
            u = ease((t - 0.6) / 1.4)
            m = P(legs="walk" if u < 1 else "stand", phase=t * 4, turn=0.1, gx=0.0, gy=-0.4, armL="chest", armR="chest", smile=0.4, blink=blink_at(t, 80))
            o += at_feet(MARDAS, m, t, 540, lerp(1098, 1112, u), lerp(0.125, 0.13, u))
        return o
    A1 = Shot(2.0, gp, midA1, cam=camA1, bg_par=1.0, light=PREDAWN, grade="night", fade_in=0.4)

    gcp = bg("garden_close_predawn", lambda: zbg.garden_close("predawn"), 6)
    LA2 = [("p1s6a", 0.3)]

    def midA2(t):
        m = tp(LA2, t, 81, turn=0.1, gx=0.15, gy=-0.75, smile=0.65, brow=0.35, furrow=-0.4, armL="chest", armR="chest", wind=0.15)
        if t > 2.0:
            m["blink"] = max(m["blink"], 0.7 * ease((t - 2.0) / 0.4))
        return at_neck(MARDAS, m, t, 540, 1080, 1.35)
    A2 = Shot(2.8, gcp, midA2, cam=cam_push(1.0, 1.04, 540, 820, 2.8), light=PREDAWN, grade="night")

    room = bg("window_room", zbg.window_room)
    wallp = bg("window_wall_predawn", lambda: zbg.window_wall("predawn"))
    LB = [("p1s6b", 0.5)]

    def midB(t):
        away = ease((t - 1.2) / 0.7)
        z = tp(LB, t, 82, turn=0.2 - 0.7 * away, gx=0.3 - 1.0 * away, gy=0.6, sad=0.6, brow=0.6, furrow=0.5, armL="relaxed", armR="relaxed")
        z["blink"] = max(z["blink"], ease((t - 1.6) / 0.4))
        return at_neck(ZAHHAK_PRINCE, z, t, 540, 1080, 1.5)
    B = Shot(2.6, room, midB, fg=wallp, cam=cam_push(1.08, 1.12, 540, 800, 2.6), light=WINDOW_PD, grade="night")

    camC = cam_push(1.0, 1.06, 540, 1150, 6.0)
    birds = [(random.Random(k).uniform(-30, 30), random.Random(k + 9).uniform(-20, 20), random.Random(k + 3).uniform(0.8, 1.3)) for k in range(9)]

    def bird(x, y, t, s, k):
        fl = 10 * s * math.sin(t * 16 + k)
        return f'<path d="M {x - 14 * s:.1f} {y - fl:.1f} Q {x - 6 * s:.1f} {y - 3:.1f} {x:.1f} {y:.1f} Q {x + 6 * s:.1f} {y - 3:.1f} {x + 14 * s:.1f} {y - fl:.1f}" stroke="#0c0c14" stroke-width="{3.2 * s:.1f}" fill="none" stroke-linecap="round"/>'

    def midC(t):
        o = pit_svg(540, 1480, 1.0, cover=1.0, seed=4, scale=0.9)
        u = t / 6.0
        y = lerp(1112, 1330, u); s = lerp(0.135, 0.3, u)
        m = P(legs="walk", phase=t * 3.6, turn=0.05, gx=0.0, gy=0.1, armL="chest", armR="chest", smile=0.4, blink=blink_at(t, 83))
        o += at_feet(MARDAS, m, t, 540, y, s)
        if t > 4.6:
            k_ = t - 4.6
            for k, (dx, dy, sp) in enumerate(birds):
                o += bird(200 + dx - 160 * k_ * sp - 30 * k, 700 + dy - 220 * k_ * sp + 18 * k, t, 1.2, k)
        return o
    C = Shot(6.0, gp, midC, cam=camC, light=PREDAWN, grade="night", fx=[fade_to((4, 4, 8), 4.8, 6.0, 0.8)])

    def bgE(t):
        return gp
    camE = cam_push(1.06, 1.1, 540, 1150, 5.0)

    def midE(t):
        o = pit_svg(540, 1480, 1.0, cover=1.0, seed=4, scale=0.9)
        for k in range(4):
            a = t * 0.6 + k * 1.6
            o += f'<path d="M {760 + 60 * math.cos(a) - 10:.1f} {420 + 20 * math.sin(a * 1.3):.1f} q 5 -5 10 0 q 5 -5 10 0" stroke="#0c0c14" stroke-width="3" fill="none"/>'
        return o
    E = Shot(5.0, bgE, midE, cam=camE, light=PREDAWN, grade="night", fx=[fade_to((4, 4, 8), -1.0, 0.0, 0.8)], fade_out=0.8)
    return [A1, A2, B, C, E]


SCENES = {"s1": s1, "s2": s2, "s3": s3, "s4": s4, "s5": s5, "s6": s6}
