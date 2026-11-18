"""Part 5 · Zahhak's Dream — 2D cartoon. Timing matches zahhak/p05_audio.py
(scene starts s1 0, s2 7.6, s3 12.2, s4 46.4, s5 66.0, s6 101.4; end card 135.6; total 140.6)."""
import math, random
from PIL import Image, ImageFilter, ImageDraw
from film import Shot, W, H, ease, lerp, talk_pose, blink_at, cam_push, cam_static, Motes, Embers, svg_render
from chars import pose, Ctx, FEET, fmt, prop, ARM_PRESETS, arm_pts, ik_angles
from stage import at_neck, at_feet, lying_at, Glow, lw_for, fire_svg, random_spec
import bgs, zbg
from cast import *
from p01_scenes import P, bg, cam_xy, tp, darken, fade_to, torch_flame, hall_fx, placed, flipped, TORCH, HALL, NIGHT, WINDOW
from p02_scenes import glint, eyes_of, court
from p03_scenes import night_of, shadow_fx, svg_fx, cam_svg, torches_wide, torches_close, crown_svg

LAMP = dict(ambient=(0.62, 0.6, 0.8), point=(70, 960, 900, 0.6, 1.1, (1.0, 0.55, 0.25)), rim=(5, -3), rim_col=(0.72, 0.82, 1.0), rim_str=0.5)
LAMPCLOSE = dict(ambient=(0.8, 0.76, 0.86), rim=(5, -2), rim_col=(1.0, 0.75, 0.45), rim_str=0.7)
ZCLOSE = dict(ambient=(0.62, 0.6, 0.8), rim=(-5, -2), rim_col=(1.0, 0.62, 0.32), rim_str=0.8)
DREAM = dict(ambient=(0.78, 0.66, 0.8), rim=(0, -3), rim_col=(1.0, 0.7, 0.5), rim_str=0.7)
HOUSE = dict(ambient=(0.7, 0.62, 0.66), point=(230, 1180, 1000, 0.55, 1.15, (1.0, 0.55, 0.25)), rim_point=(230, 6), rim_col=(1.0, 0.65, 0.3))
HOUSECLOSE = dict(rim=(-6, -2), rim_col=(1.0, 0.65, 0.35), ramp=(0, W, 1.08, 0.8), ambient=(0.84, 0.76, 0.76))
DUSK = dict(rim=(-5, -2), rim_col=(1.0, 0.7, 0.45), rim_str=0.9, ramp=(0, W, 1.04, 0.84), ambient=(0.92, 0.82, 0.84))
DOORNIGHT = dict(NIGHT, rim=(5, -2), rim_col=(1.0, 0.75, 0.45), rim_str=0.6)
GOLDEN = (255, 196, 120)


# ---------------------------------------------------------------- helpers
def hand_at(S, preset, side, x, y, s, flip=False, neck=False):
    """screen position of a hand of a person placed with at_feet(S, …, x, y, s) (neck=True: at_neck); side +1 = armL, -1 = armR"""
    bs = S["bs"]
    if neck:
        y = y + FEET * bs * s
    shw = (150 if S["kind"] == "woman" else 172) * S["build"]
    sh = (side * shw * 0.92, 60)
    if isinstance(preset, tuple) and preset and preset[0] == "ik":
        a1, a2 = ik_angles(sh, (preset[1], preset[2]), 300, 270, side, len(preset) > 3 and preset[3] == "down")
    else:
        a1, a2 = ARM_PRESETS.get(preset, preset) if isinstance(preset, str) else preset
    e, h = arm_pts(sh, a1, a2, 300, 270, side)
    fa = a1 - a2
    hx, hy = h[0] + side * math.sin(math.radians(fa)) * 26, h[1] + math.cos(math.radians(fa)) * 26
    sx = -s if flip else s
    return x + sx * bs * hx, y + s * (-FEET * bs + bs * hy)


def mace_at(x, y, s, t, ang=0.0, glint_t=None):
    """the ox-headed mace in colour, its grip at (x, y) (the scale of the person holding it); an optional star-like glint"""
    c = Ctx(lw_for(s))
    o = f'<g transform="translate({x:.1f},{y:.1f}) scale({s:.4f})">{prop(c, "mace", 0, 0, ang, t)}</g>'
    if glint_t is not None:
        u = (t - glint_t) / 0.7
        if 0 < u < 1:
            a = math.sin(math.pi * u)
            gx, gy = x + s * (math.sin(math.radians(ang)) * 300 + 100 * math.cos(math.radians(ang))), y - s * 330 * math.cos(math.radians(ang))
            r1, r2 = 70 * a * s / 0.6, 10 * a * s / 0.6
            o += (f'<path d="M {gx:.1f} {gy - r1:.1f} L {gx + r2:.1f} {gy - r2:.1f} L {gx + r1:.1f} {gy:.1f} L {gx + r2:.1f} {gy + r2:.1f} L {gx:.1f} {gy + r1:.1f} '
                  f'L {gx - r2:.1f} {gy + r2:.1f} L {gx - r1:.1f} {gy:.1f} L {gx - r2:.1f} {gy - r2:.1f} Z" fill="#fffbe8" opacity="{0.95 * a:.2f}"/>')
    return o


def silhouette(cam, body_fn, fill=(14, 8, 20), glow=GOLDEN, blur=9, ga=0.9, par=1.0, over=None):
    """an fx (pre_fx or fx) drawing body_fn(t) as a dark figure with a glowing edge: the warriors of the dream;
    over(t): SVG drawn in colour on top of the figure (the gold mace)"""
    def fx(im, t):
        body = body_fn(t)
        if body:
            A = svg_render(cam_svg(cam, t, body, par)).getchannel("A")
            g = A.filter(ImageFilter.GaussianBlur(blur)).point(lambda v: int(min(255, v * 1.7 * ga)))
            layer = Image.new("RGBA", (W, H), glow + (0,))
            layer.putalpha(g)
            im.alpha_composite(layer)
            dark = Image.new("RGBA", (W, H), fill + (0,))
            dark.putalpha(A)
            im.alpha_composite(dark)
        if over:
            o = over(t)
            if o:
                im.alpha_composite(svg_render(cam_svg(cam, t, o, par)))
    return fx


def dream_mist():
    r = random.Random(55)
    body = "".join(f'<ellipse cx="{r.uniform(-200, 2400):.0f}" cy="{r.uniform(250, 1900):.0f}" rx="{r.uniform(220, 480):.0f}" ry="{r.uniform(50, 120):.0f}" '
                   f'fill="#f4c8dc" opacity="{r.uniform(0.18, 0.34):.2f}"/>' for _ in range(40))
    return svg_render(body, 2400, H).filter(ImageFilter.GaussianBlur(34))


def dream_vig():
    import numpy as np
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    d = np.sqrt(((xx - W / 2) / (W * 0.6)) ** 2 + ((yy - H / 2) / (H * 0.55)) ** 2)
    a = (np.clip((d - 0.55) / 0.6, 0, 1) ** 1.5 * 200).astype("uint8")
    arr = np.zeros((H, W, 4), "uint8")
    arr[..., 0], arr[..., 1], arr[..., 2] = 30, 6, 26
    arr[..., 3] = a
    return Image.fromarray(arr, "RGBA")


def dream_fx(a=1.0, speed=36, x0=200, tint=(110, 30, 90, 46)):
    """the look of the dream: drifting pink mist, a purple tint, dark edges"""
    mist = bgs.cached("zh_dream_mist", dream_mist)
    vig = bgs.cached("zh_dream_vig", dream_vig)

    def fx(im, t):
        x = int(min(2400 - W, x0 + speed * t))
        m = mist.crop((x, 0, x + W, H))
        if a < 1:
            m.putalpha(m.getchannel("A").point(lambda v: int(v * a)))
        im.alpha_composite(m)
        im.alpha_composite(Image.new("RGBA", (W, H), tint[:3] + (int(tint[3] * a),)))
        im.alpha_composite(vig)
    return fx


def flash(t0, dur=0.6, col=(255, 250, 240)):
    def fx(im, t):
        u = (t - t0) / dur
        if -0.15 < u < 1:
            a = ease((u + 0.15) / 0.15) if u < 0 else 1 - ease(u)
            im.alpha_composite(Image.new("RGBA", (W, H), col + (int(255 * a),)))
    return fx


def shake(base, t0, t1, amp=12):
    def cam(t):
        k, cx, cy, px, py = base(t)
        a = amp * (1 - ease((t - t0) / max(0.01, t1 - t0))) if t0 <= t <= t1 else 0
        return k, cx, cy, px + a * math.sin(t * 37), py + a * math.cos(t * 29)
    return cam


def gate_bg():
    return bg("dream_gate", zbg.dream_gate)


def dream_hall():
    return bgs.cached("zh_hall_dream", lambda: Image.alpha_composite(bg("hall", zbg.hall), Image.new("RGBA", (W, H), (90, 20, 70, 70))))


def warriors(t, u, spread=1.0, walk=True, young_arm=None):
    """the three warriors of the dream walking out of the gate: u 0 (in the gate) .. 1 (near); returns (svg body, mace svg)"""
    y = lerp(1262, 1600, u)
    s = lerp(0.15, 0.46, u ** 1.1)
    o = ""
    for k, (S, dx) in enumerate(((DREAM_ELDER, -1), (DREAM_ELDER, 1))):
        x = 540 + dx * lerp(95, 270, u) * spread
        q = P(legs="walk" if walk else "stand", phase=t * 4.4 + k * 1.3, turn=-0.12 * dx, gx=0.0, armL=(20, 10), propL="spear",
              armR="relaxed", blink=0.0, wind=0.6)
        o += at_feet(S, q, t, x, y - 10 * u, s * 0.96, flip=(dx > 0))
    arm = young_arm or "hold_lantern"
    q = P(legs="walk" if walk else "stand", phase=t * 4.4 + 0.6, turn=0.0, gx=0.0, armL=arm, armR="relaxed", blink=0.0, wind=0.7)
    o += at_feet(DREAM_YOUNG, q, t, 540, y + 14 * u, s)
    hx, hy = hand_at(DREAM_YOUNG, arm, 1, 540, y + 14 * u, s)
    return o, mace_at(hx, hy, s * DREAM_YOUNG["bs"], t)


def sleeper(t, wake=0.0):
    """Zahhak asleep in his bed (p04 s6 C)"""
    z = P(blink=1.0 - wake, armL="relaxed", armR="relaxed", wind=0.0, breathe=math.sin(t * 1.4), snake_rise=0.55 + 0.45 * wake,
          snake_looks=(-0.6 + 1.4 * wake + 0.3 * math.sin(t * 1.7), -0.6 + 1.4 * wake + 0.3 * math.sin(t * 1.3 + 1)),
          hisses=(0.5 * wake, 0.5 * wake), turn=0.0, brow=1.2 * wake, furrow=0.4 - 0.9 * wake)
    return lying_at(ZAHHAK_NIGHT, z, t, 600, 1190, 0.36)


def mobed_row(t, xs, y, s, look=0.0, bow=0.0, seed=0, extra=None):
    """the wise men standing in two groups turned to the throne; xs: [(S, x, side)]"""
    o = ""
    for k, (S, x, side) in enumerate(xs):
        q = P(turn=0.42 * side, gx=0.7 * side + look, gy=-0.2 + 0.7 * bow, nod=14 * bow, brow=0.6, furrow=-0.2, sad=0.4,
              armL="chest", armR="chest" if k % 2 else "relaxed", blink=blink_at(t, seed + k), breathe=math.sin(t * 2 + k))
        if extra:
            q.update(extra(k, t))
        o += at_feet(S, q, t, x, y + 18 * (k % 2), s)
    return o


# ================================================================ S1 the hook (0-7.6)
def s1():
    gate = gate_bg()
    camA = cam_push(1.0, 1.06, 540, 1000, 3.4)
    X, Y, SC = 540, 1720, 0.52

    def armA(t):
        lift = ease((t - 0.2) / 1.0)
        return (lerp(40, 165, lift), lerp(60, -15, lift))

    def bodyA(t):
        q = P(turn=0.05, gx=0.0, armL=armA(t), armR="relaxed", blink=0.0, wind=0.9)
        return at_feet(DREAM_YOUNG, q, t, X, Y, SC)

    def maceA(t):
        hx, hy = hand_at(DREAM_YOUNG, armA(t), 1, X, Y, SC)
        return mace_at(hx, hy, SC * DREAM_YOUNG["bs"], t, glint_t=1.4)
    A = Shot(3.4, gate, None, cam=camA, fx=[dream_fx(), silhouette(camA, bodyA, over=maceA),
                                            Motes(40, 501, (255, 220, 170), (0, 400, W, 1700), (4, -14), amax=110)],
             grade="night", bloom=0.8, fade_in=0.4)

    bed = bg("bedchamber", zbg.bedchamber)
    camB = cam_push(1.5, 1.7, 174, 1632, 4.2)

    def midB(t):
        return torch_flame(70, 975, t, 0.5, 2) + sleeper(t, ease((t - 3.5) / 0.3))
    B = Shot(4.2, bed, midB, cam=camB, bg_par=1.0, light=LAMP, fx=[Glow(lambda t: cam_xy(camB, t, 70, 930), 260, (255, 170, 90), 0.4)],
             grade="night", bloom=0.4, fade_out=0.3)
    return [A, B]


# ================================================================ S2 title (7.6-12.2): Damavand at night
def s2():
    dn = bg("damavand_night", lambda: zbg.damavand("night"))
    cam = cam_push(1.0, 1.07, 600, 760, 4.6)
    return [Shot(4.6, dn, None, cam=cam, fx=[Motes(60, 502, (230, 236, 255), (0, 300, W, 1300), (-10, 6), amax=90)],
                 grade="night", bloom=0.7, fade_in=0.4, fade_out=0.5)]


# ================================================================ S3 the dream (12.2-46.4)
def s3():
    bedb = bg("bedchamber", zbg.bedchamber, 8)
    bed = bg("bedchamber", zbg.bedchamber)

    LA = [("p5s3a", 0.3)]
    camA = cam_push(1.0, 1.04, 520, 860, 4.0)

    def midA(t):
        a = tp(LA, t, 1, turn=0.3, gx=0.7, gy=0.15, sad=0.4, brow=0.5, furrow=-0.2, smile=0.15, armL="hold_lantern", propL="lantern", armR="relaxed")
        return at_neck(ARNAVAZ, a, t, 520, 1020, 1.05)
    A = Shot(4.0, bedb, midA, cam=camA, light=dict(LAMP, point=None, rim=(5, -2), rim_col=(1.0, 0.75, 0.45), rim_str=0.7, ambient=(0.8, 0.76, 0.86)),
             fx=[Glow(lambda t: cam_xy(camA, t, 520 + 1.05 * 160, 1020 + 1.05 * 560), 260, (255, 190, 110), 0.5)], grade="night", fade_in=0.4)

    LB = [("p5s3b", 0.2)]
    camB = cam_push(1.0, 1.07, 540, 860, 3.8)

    def midB(t):
        z = tp(LB, t, 2, turn=0.12, gx=-0.4 + 0.2 * math.sin(t * 0.8), gy=-0.3, brow=1.1, furrow=-0.7, sad=0.6, armL="relaxed", armR="relaxed",
               snake_looks=(0.6 + 0.4 * math.sin(t * 2.1), 0.5 + 0.5 * math.sin(t * 1.8 + 1)),
               hisses=(0.3 * max(0.0, math.sin(t * 2.3)), 0.3 * max(0.0, math.sin(t * 2.0 + 2))))
        z["blink"] = min(z["blink"], 0.3)
        return at_neck(ZAHHAK_NIGHT, z, t, 540, 1030, 1.15)
    B = Shot(3.8, bedb, midB, cam=camB, light=ZCLOSE, grade="night", bloom=0.4, fx=[dream_fx(a=0.0)] if False else [])

    gate = gate_bg()
    camC = cam_push(1.0, 1.08, 540, 1150, 3.9)

    def bodyC(t):
        return warriors(t, ease(t / 3.9) * 0.85)[0]

    def maceC(t):
        return warriors(t, ease(t / 3.9) * 0.85)[1]
    C = Shot(3.9, gate, None, cam=camC, fx=[dream_fx(), silhouette(camC, bodyC, over=maceC),
                                            Motes(40, 503, (255, 220, 170), (0, 400, W, 1700), (4, -14), amax=100)],
             grade="night", bloom=0.8, fade_in=0.5)

    gateb = bg("dream_gate", zbg.dream_gate, 6)
    camD = shake(cam_push(1.0, 1.08, 540, 1000, 4.4), 3.9, 4.4, 10)
    XD, YD, SD = 470, 1990, 0.68

    def armD(t):
        lift = ease((t - 0.3) / 1.6)
        down = ease((t - 3.7) / 0.25)
        a1 = lerp(lerp(40, 168, lift), 70, down)
        a2 = lerp(lerp(60, -18, lift), 10, down)
        return (a1, a2)

    def bodyD(t):
        q = P(turn=-0.1, gx=-0.2, gy=0.3, armL=armD(t), armR="relaxed", blink=0.0, wind=1.0)
        return at_feet(DREAM_YOUNG, q, t, XD, YD, SD)

    def maceD(t):
        hx, hy = hand_at(DREAM_YOUNG, armD(t), 1, XD, YD, SD)
        down = ease((t - 3.7) / 0.25)
        return mace_at(hx, hy, SD * DREAM_YOUNG["bs"], t, ang=lerp(0, 75, down), glint_t=1.7)
    D = Shot(4.4, gateb, None, cam=camD, fx=[dream_fx(a=0.8), silhouette(camD, bodyD, blur=12, over=maceD),
                                             Motes(50, 504, (255, 220, 170), (0, 300, W, 1700), (4, -14), amax=110), flash(3.95, 0.7)],
             grade="night", bloom=0.9)

    dh = dream_hall()
    camE = cam_push(1.08, 1.14, 540, 1150, 3.3)
    ARM_E = ("ik", 230, 150)

    def warriorE(t):
        pull = ease(t / 3.3)
        return lerp(1080, 1130, pull), 1600, 0.52

    def bodyE(t):
        x, y, s = warriorE(t)
        q = P(turn=-0.45, gx=-0.8, armL="relaxed", armR=ARM_E, blink=0.0, legs="walk", phase=t * 4.0, wind=0.8)
        return at_feet(DREAM_YOUNG, q, t, x, y, s, flip=True)

    def midE(t):
        pull = ease(t / 3.3)
        x, y, s = lerp(560, 650, pull), 1560, 0.5
        wx, wy, ws = warriorE(t)
        hx, hy = hand_at(DREAM_YOUNG, ARM_E, -1, wx, wy, ws, flip=True)
        lx, ly = (hx - x) / s, (hy - y) / s + FEET * ZAHHAK_KING["bs"]
        z = tp([], t, 3, turn=0.3, gx=0.6, gy=0.3, brow=0.9, furrow=-0.5, sad=0.8, armL=("ik", 70, 330), armR=("ik", -70, 330), chains="rope", lead=(lx, ly),
               legs="walk", phase=t * 3.0, snake_rise=0.7, snake_looks=(-0.5, -0.4), hisses=(0.0, 0.0), wind=0.6)
        z["blink"] = max(z["blink"], 0.45)
        return torches_wide(t) + at_feet(ZAHHAK_KING, z, t, x, y, s)
    E = Shot(3.3, dh, midE, cam=camE, light=DREAM, fx=hall_fx(camE, [(80, 640), (1000, 640)], 505) + [dream_fx(a=0.45, x0=600), silhouette(camE, bodyE),
                                                                                                     flash(-0.45, 0.7)],
             grade="night", bloom=0.6)

    dd = bg("damavand_dream", lambda: zbg.damavand("dream"))
    camF = cam_push(1.0, 1.06, 560, 1300, 6.4)
    r = random.Random(506)
    crowd = [(random_spec(r, ("man", "man", "woman", "boy")), r.uniform(-30, 30), r.uniform(-30, 40), r.uniform(0.85, 1.1), r.uniform(0, 6)) for _ in range(11)]

    def lead_x(t):
        return lerp(380, 780, t / 6.4)

    def bodyF(t):
        o = ""
        x0 = lead_x(t)
        q = P(turn=0.45, gx=0.8, armL="forward", armR=("ik", -240, 200, "down"), blink=0.0, legs="walk", phase=t * 4.4, wind=0.8)
        o += at_feet(DREAM_YOUNG, q, t, x0 + 140, 1500, 0.3)
        for k, (S, dx, dy, sc, ph) in enumerate(crowd):
            x = x0 - 230 - 64 * k + dx
            arm = ("raise" if k % 3 == 0 else ("forward" if k % 3 == 1 else "relaxed"))
            q = P(turn=0.45, gx=0.8, armL=arm, armR="forward", blink=0.0, legs="walk", phase=t * 6.5 + ph, wind=0.6)
            o += at_feet(S, q, t, x, 1480 + dy * 0.6, 0.19 * sc)
        return o

    def midF(t):
        x0 = lead_x(t)
        s = 0.27
        x, y = x0 - 60, 1505
        hx, hy = hand_at(DREAM_YOUNG, ("ik", -240, 200, "down"), -1, x0 + 140, 1500, 0.3)
        lx, ly = (hx - x) / s, (hy - y) / s + FEET * ZAHHAK_KING["bs"]
        z = P(turn=0.4, gx=0.8, gy=0.4, brow=0.9, furrow=-0.5, sad=0.9, armL=("ik", 70, 330), armR=("ik", -70, 330), chains="rope", lead=(lx, ly),
              legs="walk", phase=t * 4.4, snake_rise=0.7, snake_looks=(-0.6, -0.5), blink=0.3, wind=0.6)
        lean = 9 + 3 * math.sin(t * 4.4)
        return f'<g transform="rotate({lean:.1f},{x:.1f},{y:.1f})">' + at_feet(ZAHHAK_KING, z, t, x, y, s) + '</g>'
    F = Shot(6.4, dd, midF, cam=camF, light=DREAM, pre_fx=[silhouette(camF, bodyF, blur=6, ga=0.8)],
             fx=[dream_fx(a=0.55, speed=30, x0=300)], grade="night", bloom=0.7, fade_out=0.6)

    LG = [("p5s3h", 0.4)]
    camG = cam_push(1.0, 1.05, 560, 1150, 4.0, py0=-240, py1=-250)

    def midG(t):
        z = tp([], t, 4, legs="sit", turn=0.3, gx=0.7, gy=0.0, brow=0.8, furrow=-0.4, sad=0.6, armL="relaxed", armR="chest",
               snake_rise=1.0, snake_looks=(0.4 + 0.3 * math.sin(t * 1.7), 0.5 + 0.3 * math.sin(t * 1.4 + 1)), hisses=(0.0, 0.0))
        a = tp(LG, t, 5, turn=-0.35, gx=-0.8, gy=0.2, sad=0.3, brow=0.3, furrow=0.1, armL="hold_lantern", propL="lantern", armR="relaxed")
        return (torch_flame(70, 975, t, 0.5, 2) + at_neck(ZAHHAK_NIGHT, z, t, 400, 1185 - 575 * 0.42, 0.42) +
                at_feet(ARNAVAZ, a, t, 790, 1600, 0.5))
    G = Shot(4.0, bed, midG, cam=camG, bg_par=1.0, light=LAMP, fx=[Glow(lambda t: cam_xy(camG, t, 70, 930), 220, (255, 170, 90), 0.4),
                                                      Glow(lambda t: cam_xy(camG, t, 790 + 0.5 * 160, 1600 - 1290 * 0.95 * 0.5 + 0.5 * 560 + 40), 180, (255, 190, 110), 0.4)],
             grade="night", bloom=0.4, fade_in=0.4)

    LH = [("p5s3i", 0.1)]
    camH = cam_push(1.0, 1.05, 520, 860, 4.4)

    def midH(t):
        a = tp(LH, t, 6, turn=0.25, gx=0.6, gy=0.1, sad=0.2, brow=0.2, furrow=0.3, nod=4 * ease((t - 2.4) / 0.4), armL="hold_lantern", propL="lantern", armR="relaxed")
        return at_neck(ARNAVAZ, a, t, 520, 1020, 1.05)
    H_ = Shot(4.4, bedb, midH, cam=camH, light=dict(LAMP, point=None, rim=(5, -2), rim_col=(1.0, 0.75, 0.45), rim_str=0.7, ambient=(0.8, 0.76, 0.86)),
              fx=[Glow(lambda t: cam_xy(camH, t, 520 + 1.05 * 160, 1020 + 1.05 * 560), 260, (255, 190, 110), 0.5)], grade="night", fade_out=0.5)
    return [A, B, C, D, E, F, G, H_]


# ================================================================ S4 the wise men (46.4-66.0)
LEFT = [(MOBED_1, 105, 1), (ZIRAK, 245, 1), (MOBED_3, 385, 1)]
RIGHT = [(MOBED_2, 695, -1), (MOBED_4, 835, -1), (MOBED_1, 975, -1)]


def guards_hall(t, seed=0):
    o = ""
    for k, (x, side) in enumerate(((95, 1), (985, -1))):
        q = P(turn=0.4 * side, gx=0.8 * side, gy=-0.2, armL=(20, 10), propL="pike", armR="relaxed", furrow=0.7, blink=blink_at(t, seed + k))
        o += at_feet(ZGUARD, q, t, x, 1385, 0.34, flip=False)
    return o


def zk_throne(t, seed, **kw):
    base = dict(legs="sit", turn=0.0, gx=0.0, gy=0.3, furrow=0.7, brow=-0.1, armL="relaxed", armR="relaxed",
                snake_looks=(0.6 + 0.4 * math.sin(t * 1.1), 0.5 + 0.5 * math.sin(t * 1.3 + 1)),
                hisses=(0.4 * max(0.0, math.sin(t * 1.6)), 0.4 * max(0.0, math.sin(t * 1.4 + 2))))
    base.update(kw)
    return tp([], t, seed, **base)


def s4():
    hall = bg("hall", zbg.hall)
    camA = cam_push(1.0, 1.05, 540, 1100, 5.2)

    def midA(t):
        o = torches_wide(t) + at_neck(ZAHHAK_KING, zk_throne(t, 7), t, 540, 793, 0.36) + guards_hall(t, 10)
        u = ease(t / 3.4)
        for k, (S, x, side) in enumerate(LEFT + RIGHT):
            walking = u < 1
            x0 = -120 - 70 * k if side > 0 else 1200 + 70 * (k - 3)
            xx = lerp(x0, x, u)
            q = P(turn=0.42 * side, gx=0.7 * side, gy=-0.2, brow=0.6, furrow=-0.2, sad=0.4, legs="walk" if walking else "stand", phase=t * 4.6 + k,
                  armL="chest", armR="relaxed", blink=blink_at(t, 20 + k), breathe=math.sin(t * 2 + k))
            o += at_feet(S, q, t, xx, 1520 + 22 * (k % 3 == 1), 0.36)
        return o
    A = Shot(5.2, hall, midA, cam=camA, light=HALL, fx=hall_fx(camA, [(80, 640), (1000, 640)], 507), grade="fire", bloom=0.6, fade_in=0.5)

    close = bg("hall_close", zbg.hall_close)
    LB = [("p5s4b", 0.2)]
    camB = cam_push(1.0, 1.05, 540, 860, 3.6)

    def midB(t):
        q = tp(LB, t, 8, turn=0.05, gx=0.1, gy=0.2, furrow=1.0, brow=-0.3, nod=6, armL="relaxed", armR="relaxed",
               snake_looks=(0.9, 0.9), hisses=(0.5 * max(0.0, math.sin(t * 2.4)), 0.5 * max(0.0, math.sin(t * 2.0 + 1))))
        return torches_close(t) + at_neck(ZAHHAK_KING, q, t, 540, 1030, 1.0)
    B = Shot(3.6, close, midB, cam=camB, light=TORCH, fx=hall_fx(camB, [(40, 740), (1040, 740)], 508), grade="fire", bloom=0.6)

    hallb = bg("hall", zbg.hall, 6)
    camC = cam_push(1.0, 1.06, 540, 1000, 6.0)
    DAYS = (3.4, 4.4, 5.4)

    def midC(t):
        o = ""
        tired = sum(ease((t - d) / 0.5) for d in DAYS) / 3
        for k, (S, x, y, side) in enumerate(((MOBED_1, 170, 1640, 1), (ZIRAK, 420, 1660, 1), (MOBED_2, 690, 1650, -1), (MOBED_3, 930, 1640, -1))):
            look = 0.6 * math.sin(t * 0.9 + k * 1.7) if 0.6 < t < 3.0 else 0.0
            q = P(turn=0.3 * side, gx=0.5 * side + look, gy=0.5 + 0.3 * tired, nod=10 + 8 * tired, brow=0.8, furrow=-0.4, sad=0.5 + 0.3 * tired,
                  armL="chest", armR="chest" if k % 2 == 0 else "relaxed", blink=max(blink_at(t, 30 + k), 0.25 * tired), breathe=math.sin(t * 2.4 + k),
                  tilt=2 * math.sin(t * 1.3 + k))
            o += at_feet(S, q, t, x, y, 0.62)
        return o

    def days(im, t):
        a = 0.0
        for d in DAYS:
            u = (t - d) / 0.9
            if 0 < u < 1:
                a = max(a, math.sin(math.pi * u))
        if a > 0:
            im.alpha_composite(Image.new("RGBA", (W, H), (4, 2, 8, int(160 * a))))
    C = Shot(6.0, hallb, midC, cam=camC, light=HALL, sun=(540, 300, 1100, (0.08, 0.04, 0.02)), fx=[days], grade="fire", bloom=0.5)

    LD = [("p5s4d", 0.3)]
    camD = shake(cam_push(1.0, 1.06, 540, 860, 4.8, py0=110, py1=110), 0.3, 1.1, 9)      # lower: the caption «The fourth day» sits above the emblem

    def midD(t):
        up = ease((t - 0.1) / 0.5)
        q = tp(LD, t, 9, turn=0.0, gx=0.0, gy=0.1, furrow=1.0, brow=-0.6, armL="relaxed", armR="point" if t > 1.6 else "relaxed",
               snake_rise=1.0, snake_looks=(1.0, 1.0), hisses=(0.9 * (0.6 + 0.4 * math.sin(t * 5)), 0.9 * (0.6 + 0.4 * math.sin(t * 4 + 1))))
        q["mouth_o"] = max(q["mouth_o"], 0.0)
        return torches_close(t) + at_neck(ZAHHAK_KING, q, t, 540, lerp(1060, 990, up), 1.0)
    D = Shot(4.8, close, midD, cam=camD, light=TORCH, fx=hall_fx(camD, [(40, 740), (1040, 740)], 509), grade="fire", bloom=0.6, fade_out=0.4)
    return [A, B, C, D]


# ================================================================ S5 Zirak (66.0-101.4)
def s5():
    hall = bg("hall", zbg.hall)
    hallb = bg("hall", zbg.hall, 6)
    close = bg("hall_close", zbg.hall_close)

    camA = cam_push(1.04, 1.1, 540, 1150, 5.2)

    def midA(t):
        o = torches_wide(t) + at_neck(ZAHHAK_KING, zk_throne(t, 11, gx=-0.3, gy=0.5), t, 540, 793, 0.36) + guards_hall(t, 12)
        others = [m for m in LEFT + RIGHT if m[0] is not ZIRAK]
        o += mobed_row(t, others, 1520, 0.36, bow=0.6, seed=40)
        u = ease((t - 1.0) / 2.4)
        q = P(turn=0.3 - 0.3 * u, gx=0.5 - 0.5 * u, gy=-0.3, brow=0.5, furrow=0.1, sad=0.3, legs="walk" if 0 < u < 1 else "stand", phase=t * 4.2,
              armL="chest", armR="relaxed", blink=blink_at(t, 41), nod=10 * ease((t - 3.8) / 0.5))
        o += at_feet(ZIRAK, q, t, lerp(245, 540, u), lerp(1520, 1580, u), lerp(0.36, 0.4, u))
        return o
    A = Shot(5.2, hall, midA, cam=camA, light=HALL, fx=hall_fx(camA, [(80, 640), (1000, 640)], 510), grade="fire", bloom=0.6, fade_in=0.4)

    ZL = dict(HALL, point=None, rim=(-5, -2), rim_col=(1.0, 0.68, 0.38), rim_str=0.85, ramp=(0, W, 1.05, 0.86), ambient=(0.86, 0.8, 0.84))
    LB = [("p5s5b", 0.1)]

    def midB(t):
        q = tp(LB, t, 12, turn=-0.2, gx=-0.4, gy=-0.2, brow=0.4, furrow=0.0, sad=0.35, armL="relaxed", armR="offer" if 1.6 < t < 3.8 else "relaxed")
        return at_neck(ZIRAK, q, t, 560, 1060, 1.3)
    camB = cam_push(1.0, 1.04, 560, 860, 4.6)
    B = Shot(4.6, hallb, midB, cam=camB, light=ZL, sun=(80, 700, 800, (0.10, 0.05, 0.02)), grade="fire", bloom=0.5)

    LC = [("p5s5c", 0.1)]
    camC = cam_push(1.04, 1.1, 520, 820, 4.7)

    def midC1(t):
        q = tp(LC, t, 13, turn=-0.15, gx=-0.3, gy=-0.3, brow=0.5, furrow=-0.1, sad=0.2, armL="relaxed", armR="relaxed")
        return at_neck(ZIRAK, q, t, 520, 1060, 1.3)
    C1 = Shot(4.7, hallb, midC1, cam=camC, light=ZL, sun=(80, 700, 800, (0.10, 0.05, 0.02)),
              fx=[Motes(30, 511, (255, 226, 170), (200, 400, 900, 1300), (2, -10), amax=80)], grade="fire", bloom=0.7)

    gate = gate_bg()
    camC2 = cam_push(1.0, 1.08, 540, 900, 4.6)
    X2, Y2, S2 = 540, 1720, 0.52

    def bodyC2(t):
        q = P(turn=0.05, gx=0.0, armL="fist_up", armR="relaxed", blink=0.0, wind=0.9)
        return at_feet(DREAM_YOUNG, q, t, X2, Y2, S2)

    def maceC2(t):
        hx, hy = hand_at(DREAM_YOUNG, "fist_up", 1, X2, Y2, S2)
        return mace_at(hx, hy, S2 * DREAM_YOUNG["bs"], t, glint_t=2.0)
    C2 = Shot(4.6, gate, None, cam=camC2, fx=[dream_fx(x0=500), silhouette(camC2, bodyC2, over=maceC2),
                                              Motes(40, 512, (255, 220, 170), (0, 400, W, 1700), (4, -14), amax=110)],
              grade="night", bloom=0.8, fade_in=0.4, fade_out=0.3)

    LD = [("p5s5e", 0.1)]

    def midD(t):
        q = tp(LD, t, 14, turn=0.05, gx=0.1, gy=0.0, furrow=-0.5, brow=1.0, sad=0.5, armL="relaxed", armR="relaxed",
               snake_looks=(1.0, 1.0), hisses=(0.6 * max(0.0, math.sin(t * 3)), 0.6 * max(0.0, math.sin(t * 2.6 + 1))))
        return torches_close(t) + at_neck(ZAHHAK_KING, q, t, 540, 1030, 1.0)
    camD = cam_push(1.04, 1.1, 540, 860, 2.6)
    D = Shot(2.6, close, midD, cam=camD, light=TORCH, fx=hall_fx(camD, [(40, 740), (1040, 740)], 513), grade="fire", bloom=0.6)

    LE = [("p5s5f", 0.2), ("p5s5g", 4.4)]
    camE = cam_push(1.0, 1.08, 560, 860, 6.7)

    def midE(t):
        q = tp(LE, t, 15, turn=-0.2, gx=-0.4, gy=-0.1, brow=0.3, furrow=0.4 if t > 4.2 else 0.1, sad=0.45, armL="relaxed",
               armR="point" if 4.5 < t < 6.2 else "relaxed")
        return at_neck(ZIRAK, q, t, 560, 1060, 1.3)
    E = Shot(6.7, hallb, midE, cam=camE, light=ZL, sun=(80, 700, 800, (0.10, 0.05, 0.02)), grade="fire", bloom=0.5)

    camF = cam_push(1.0, 1.04, 540, 860, 2.4)

    def midF(t):
        roll = ease((t - 0.3) / 0.6)
        fall = ease((t - 1.0) / 0.9)
        q = tp([], t, 16, turn=0.05, gx=0.0, gy=-0.6 * roll, furrow=-0.6, brow=1.2 * (1 - roll), sad=0.7, armL="relaxed", armR="relaxed",
               snake_rise=lerp(1.0, 0.5, fall), snake_looks=(1.0 - 1.6 * fall, 1.0 - 1.6 * fall), hisses=(0.0, 0.0), tilt=-8 * roll)
        q["blink"] = max(q["blink"], 0.9 * roll)
        body = at_neck(ZAHHAK_KING, q, t, 540, 1030, 1.0)
        return torches_close(t) + f'<g transform="translate({220 * fall:.1f},{900 * fall ** 1.6:.1f}) rotate({62 * fall:.1f},540,1500)">{body}</g>'
    F = Shot(2.4, close, midF, cam=camF, light=TORCH, fx=hall_fx(camF, [(40, 740), (1040, 740)], 514), grade="fire", bloom=0.6)

    camG = shake(cam_push(1.32, 1.4, 560, 1240, 4.6), 0.0, 0.6, 10)

    def midG(t):
        o = torches_wide(t)
        o += lying_at(ZAHHAK_KING, P(blink=1.0, armL="relaxed", armR="relaxed", snake_rise=0.5, snake_looks=(-0.8, -0.8), turn=0.0, sad=0.6), t, 600, 1302, 0.34)
        u = ease((t - 0.3) / 1.5)
        for k, (x0, x1, side) in enumerate(((-60, 200, 1), (1180, 915, -1))):
            q = P(turn=0.4 * side, gx=0.8 * side, gy=0.6, armL=(20, 10), propL="pike", armR="forward", furrow=0.1, brow=1.0, legs="walk" if u < 1 else "stand",
                  phase=t * 6, blink=blink_at(t, 50 + k))
            o += at_feet(ZGUARD, q, t, lerp(x0, x1, u), 1400, 0.36)
        return o
    G = Shot(4.6, hall, midG, cam=camG, bg_par=1.0, light=HALL, fx=hall_fx(camG, [(80, 640), (1000, 640)], 515), grade="fire", bloom=0.6, fade_out=0.5)
    return [A, B, C1, C2, D, E, F, G]


# ================================================================ S6 the search; the birth; the road (101.4-140.6)
def s6():
    close = bg("hall_close", zbg.hall_close)
    LA = [("p5s6a", 0.3)]
    camA = cam_push(1.0, 1.05, 540, 860, 3.2)

    def midA(t):
        q = tp(LA, t, 1, turn=0.1, gx=0.3, gy=0.1, furrow=1.0, brow=-0.2, sad=0.3, armL="relaxed", armR="point" if t > 0.8 else "relaxed",
               snake_looks=(0.9, 0.8), hisses=(0.6 * max(0.0, math.sin(t * 3)), 0.6 * max(0.0, math.sin(t * 2.6 + 1))))
        q["blink"] = max(q["blink"], 0.2)
        return torches_close(t) + at_neck(ZAHHAK_KING, q, t, 540, 1030, 1.0)
    A = Shot(3.2, close, midA, cam=camA, light=TORCH, fx=hall_fx(camA, [(40, 740), (1040, 740)], 516), grade="fire", bloom=0.6, fade_in=0.3)

    wall = bgs.cached("shadow_wall", bgs.shadow_wall)
    camB = cam_push(1.0, 1.04, 540, 900, 2.8)

    def shadowB(t):
        o = ""
        for k in range(5):
            x = -300 + 260 * k + 230 * t
            q = P(legs="walk", phase=t * 5.6 + k, turn=0.45, gx=0.9, armL=(20, 10), propL="pike", armR="hold_lantern" if k == 2 else "forward",
                  propR="lantern" if k == 2 else None, blink=0.0)
            o += at_feet(ZGUARD, q, t, x, 1690, 0.72)
        return o
    B1 = Shot(2.8, wall, None, cam=camB, pre_fx=[shadow_fx(camB, shadowB, a=0.8, blur=3)], grade="fire", bloom=0.4, fx=[darken(0.3, -1.0, 9.0, (10, 4, 2))])

    room = bg("window_room", zbg.window_room)
    wallw = bg("window_wall", lambda: zbg.window_wall("night"))
    camB2 = cam_push(1.08, 1.13, 540, 800, 2.8)

    def midB2(t):
        z = tp([], t, 2, turn=0.15, gx=0.4 + 0.3 * math.sin(t * 0.8), gy=-0.1, brow=0.6, furrow=0.6, sad=0.6, armL="relaxed", armR="relaxed",
               snake_looks=(-0.5 + 0.3 * math.sin(t * 1.9), -0.4 + 0.3 * math.sin(t * 1.5 + 1)), hisses=(0.0, 0.0))
        z["blink"] = max(z["blink"], 0.3)
        return at_neck(ZAHHAK_NIGHT, z, t, 540, 1120, 1.12)
    B2 = Shot(2.8, room, midB2, fg=wallw, cam=camB2, light=WINDOW, grade="night", fade_out=0.4)

    house = bgs.cached("zh_interior_night", night_of(lambda: bgs.cached("interior", bgs.interior), (10, 8, 26), 90))
    houseb = bgs.cached("zh_interior_night_b8", lambda: house.filter(ImageFilter.GaussianBlur(8)))
    camC = cam_push(1.28, 1.34, 680, 1250, 5.6, py0=-190, py1=-200)
    FLOOR = 1500

    def midC(t):
        f = tp([], t, 3, legs="sit", turn=0.15, gx=0.2, gy=0.8, smile=0.5, brow=0.3, furrow=-0.3, armL="hold_baby", armR="hold_baby", propL="baby",
               tilt=3 * math.sin(t * 1.4), wind=0.1)
        a = tp([], t, 4, legs="sit", turn=-0.35, gx=-0.8, gy=0.6, smile=0.55, brow=0.35, furrow=-0.3, armL="relaxed", armR="relaxed", wind=0.1)
        return fire_svg(230, 1300, 62, t) + at_neck(ABTIN, a, t, 800, FLOOR - 8 - 575 * 0.5, 0.5) + at_neck(FARANAK, f, t, 565, FLOOR - 575 * 0.95 * 0.5 + 6, 0.5)
    C = Shot(5.6, house, midC, cam=camC, bg_par=1.0, light=HOUSE, fx=[Embers(20, 517, (170, 1100, 290, 1290), (40, 100))], grade="fire", fade_in=0.5)

    LD = [("p5s6d", 0.1)]

    def midD(t):
        a = tp(LD, t, 5, turn=-0.3, gx=-0.7, gy=0.5, smile=0.6, brow=0.4, furrow=-0.3, armL="relaxed", armR="relaxed")
        return at_neck(ABTIN, a, t, 600, 1050, 1.3)
    D = Shot(2.6, houseb, midD, cam=cam_push(1.0, 1.04, 600, 860, 2.6), light=HOUSECLOSE, sun=(0, 1100, 700, (0.12, 0.06, 0.02)), grade="fire")

    LE = [("p5s6e", 0.2)]

    def midE(t):
        f = tp(LE, t, 6, turn=0.25, gx=0.5, gy=0.7, smile=0.55, brow=0.3, furrow=-0.3, armL="hold_baby", armR="hold_baby", propL="baby",
               tilt=3 * math.sin(t * 1.6), wind=0.1)
        return at_neck(FARANAK, f, t, 520, 1000, 1.15)
    E = Shot(2.5, houseb, midE, cam=cam_push(1.0, 1.04, 520, 860, 2.5), light=HOUSECLOSE, sun=(0, 1100, 700, (0.12, 0.06, 0.02)), grade="fire")

    door_dusk = bgs.cached("zh_house_door_dusk", lambda: Image.alpha_composite(bgs.cached("house_door", bgs.house_door),
                                                                              Image.new("RGBA", (W, H), (70, 26, 60, 120))))
    camF = cam_push(1.0, 1.06, 470, 1000, 6.5)

    def doorway(t):
        """the door open on a lamp-lit room"""
        return ('<rect x="320" y="660" width="260" height="740" fill="#2a1408"/>'
                '<rect x="320" y="660" width="260" height="740" fill="#ffb060" opacity="0.18"/>'
                '<path d="M 320 660 L 280 690 L 280 1420 L 320 1400 Z" fill="#6a4228" stroke="#3a2214" stroke-width="3"/>')

    def midF(t):
        out = ease((t - 3.6) / 2.4)
        look = math.sin(t * 1.5) if t < 3.4 else 0.6
        q = tp([], t, 7, turn=0.2 + 0.25 * look * (1 - out) + 0.25 * out, gx=0.8 * look * (1 - out) + 0.8 * out, gy=0.0, brow=0.6, furrow=0.4, sad=0.2,
               armL="hold_lantern" if t < 3.6 else ("ik", 120, 200, "down"), propL="stick" if t >= 3.6 else None, armR="chest",
               legs="walk" if 3.6 < t < 6.0 else "stand", phase=t * 4.2, wind=0.5)
        return doorway(t) + at_feet(ABTIN, q, t, lerp(450, 900, out), lerp(1400, 1460, out), lerp(0.56, 0.6, out))
    F = Shot(6.5, door_dusk, midF, cam=camF, light=DUSK, sun=(1000, 1100, 900, (0.14, 0.07, 0.04)), grade="warm", fade_in=0.4)

    road = bg("damavand_dusk_road", lambda: zbg.damavand("dusk", road=True))
    camG = cam_push(1.0, 1.06, 560, 1350, 4.4)
    STOP = 2.4

    def abtin_pos(t):
        u = min(t, STOP) / 4.4
        return lerp(600, 560, u), lerp(1330, 1460, u), lerp(0.3, 0.36, u)

    def midG(t):
        x, y, s = abtin_pos(t)
        walking = t < STOP
        fear = ease((t - STOP - 0.3) / 0.4)
        q = tp([], t, 8, turn=0.1 + 0.35 * fear, gx=0.2 + 0.8 * fear, gy=0.1, brow=0.3 + 0.9 * fear, furrow=0.2 - 0.6 * fear, sad=0.3,
               armL=("ik", 120, 200, "down"), propL="stick", armR="chest" if fear < 0.5 else "both_out", legs="walk" if walking else "stand", phase=t * 4.4, wind=0.6)
        return at_feet(ABTIN, q, t, x, y, s)

    def bodyG(t):
        u = ease((t - STOP) / 0.8)
        if u <= 0:
            return ""
        o = ""
        for k, (x, y, s) in enumerate(((960, 1500, 0.4), (850, 1560, 0.44))):
            q = P(turn=-0.4, gx=-0.9, armL=(20, 10), propL="pike", armR="forward", blink=0.0, legs="walk" if u < 1 else "stand", phase=t * 5 + k)
            o += at_feet(ZGUARD, q, t, lerp(x + 260, x, u), y, s)
        return o
    G = Shot(4.4, road, midG, cam=camG, light=DUSK, sun=(170, 1030, 900, (0.16, 0.08, 0.03)),
             fx=[silhouette(camG, bodyG, fill=(24, 12, 20), glow=(255, 150, 90), blur=5, ga=0.6)], grade="warm", bloom=0.6, fade_out=0.3)

    door_night = bgs.cached("zh_house_door_night", night_of(lambda: bgs.cached("house_door", bgs.house_door), (6, 10, 30), 170))
    camH = cam_push(1.0, 1.05, 470, 950, 3.8)
    lanH = lambda t: cam_xy(camH, t, 300, 1395)

    def faranak_door(t, sad=0.6):
        f = tp([], t, 9, turn=-0.3, gx=-0.9, gy=-0.1, sad=sad, brow=0.8, furrow=-0.4, armL="hold_baby", armR="hold_baby", propL="baby", wind=0.4)
        c = Ctx(lw_for(0.7))
        return at_neck(FARANAK, f, t, 470, 760, 0.85) + f'<g transform="translate(300,1320) scale(0.7)">{prop(c, "lantern", 0, 0, 0, t)}</g>'
    H_ = Shot(3.8, door_night, lambda t: faranak_door(t), cam=camH, light=DOORNIGHT, fx=[Glow(lanH, 200, (255, 190, 110), 0.45)], grade="night", fade_in=0.4)

    camI = cam_push(1.05, 1.1, 470, 950, 5.0)
    lanI = lambda t: cam_xy(camI, t, 300, 1395)
    I = Shot(5.0, door_night, lambda t: faranak_door(t + 3.8, 0.8), cam=camI, light=DOORNIGHT, fx=[Glow(lanI, 200, (255, 190, 110), 0.4)],
             grade="night", fade_out=0.8)
    return [A, B1, B2, C, D, E, F, G, H_, I]


SCENES = {"s1": s1, "s2": s2, "s3": s3, "s4": s4, "s5": s5, "s6": s6}
