"""Part 3 · Arash's Arrow — 2D cartoon. Timing matches arash/p03_audio.py
(scene starts s1 0, s2 7.8, s3 12.4, s4 62.4, s5 87.0, s6 112.0; end card 141.4; total 147.0)."""
import math, random
from PIL import Image, ImageFilter, ImageDraw, ImageOps
from film import Shot, W, H, ease, lerp, talk_pose, blink_at, cam_push, cam_static, Motes, Embers, Snow, svg_render
from chars import pose, horse, Ctx, FEET, fmt, prop, ik_angles, arm_pts, ARM_PRESETS, SKINS, OUT
from stage import at_neck, at_feet, rider, Glow, lw_for, fire_svg, back_heads, random_spec, glow_img
import bgs, zbg, abg
from cast import *
from p01_scenes import P, tp, bg, cam_xy, flame, arrow_svg, DAWNL, DAYL, SUN_DAY, NIGHTL, LAMPL, LAMPC, TENTL, FIREL, DUSKL
from p02_scenes import FadeGlow, snow_wind, torch_pole, PREDAWN
import p03_audio as A3

S0 = A3.S
SUNRISE = dict(ambient=(1.0, 0.94, 0.9), rim=(6, -3), rim_col=(1.0, 0.82, 0.55), rim_str=1.1, ramp=(0, W, 0.84, 1.08))
SUN_RISE = (905, 1120, 900, (0.12, 0.08, 0.03))
SUNC = dict(ambient=(1.0, 0.93, 0.88), rim=(6, -2), rim_col=(1.0, 0.8, 0.5), rim_str=1.1, ramp=(0, W, 0.82, 1.1))      # close, the sun at the right
NOON = dict(ambient=(1.0, 0.99, 0.96), rim=(5, -3), rim_col=(1.0, 0.95, 0.8), rim_str=0.8, ramp=(0, W, 0.92, 1.05))
SUN_NOON = (850, 430, 900, (0.08, 0.07, 0.04))
GOLD = (255, 214, 140)


# ---------------------------------------------------------------- helpers
def at(t, t0, d):
    """0..1 ease from t0 over d seconds"""
    return ease((t - t0) / d)


def lines_in(shot_start, *ids):
    """[(line id, start in the shot)] for lines of p03_audio.LINES"""
    d = dict(A3.LINES)
    return [(i, d[i] - shot_start) for i in ids]


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


def fist(S, x, y, r):
    """a closed hand drawn over a grip (bow, string), at (x, y), radius r (scene px)"""
    sk, sh, hi = SKINS[S["skin"]]
    return (f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="{r * 0.95:.1f}" ry="{r * 1.1:.1f}" fill="{sk}" stroke="{OUT}" stroke-width="{max(1.2, r * 0.1):.1f}"/>'
            f'<path d="M {x - r * 0.7:.1f} {y - r * 0.35:.1f} L {x + r * 0.7:.1f} {y - r * 0.35:.1f} M {x - r * 0.7:.1f} {y + r * 0.2:.1f} L {x + r * 0.7:.1f} {y + r * 0.2:.1f}" '
            f'stroke="{sh}" stroke-width="{max(1.0, r * 0.08):.1f}" opacity="0.8"/>')


def great_bow(draw, nock, arrow=None, glow=0.0, shake=0.0, t=0.0):
    """the great bow facing right (its back to the target, the grip at (0, 0), bow units), bent by draw 0..1, its string pulled back to
    (nock, 0) (nock < 0; a string at rest is at x -40); arrow = (tail x, head x) of a nocked arrow; glow: a golden light along the arrow"""
    wood, dark, light = "#6a4422", "#3a2412", "#a8743e"
    tx, ty = -52 - 150 * draw, 360 - 46 * draw
    o = ""
    if glow > 0 and arrow:
        o += (f'<path d="M {arrow[0]:.0f} 0 L {arrow[1]:.0f} 0" stroke="#ffe8a8" stroke-width="{40 + 30 * glow:.0f}" opacity="{0.25 * glow:.2f}" '
              f'stroke-linecap="round" filter="url(#bowglow)"/>')
    for sd in (-1, 1):
        o += (f'<path d="M {tx:.1f} {sd * ty:.1f} C {tx + 46 + 30 * draw:.1f} {sd * (ty - 70):.1f}, {44 + 14 * draw:.1f} {sd * (190 - 10 * draw):.1f}, 22 {sd * 26}" '
              f'stroke="{OUT}" stroke-width="19" fill="none" stroke-linecap="round"/>'
              f'<path d="M {tx:.1f} {sd * ty:.1f} C {tx + 46 + 30 * draw:.1f} {sd * (ty - 70):.1f}, {44 + 14 * draw:.1f} {sd * (190 - 10 * draw):.1f}, 22 {sd * 26}" '
              f'stroke="{wood}" stroke-width="13" fill="none" stroke-linecap="round"/>'
              f'<path d="M {tx + 8:.1f} {sd * (ty - 12):.1f} C {tx + 46 + 30 * draw:.1f} {sd * (ty - 80):.1f}, {38 + 14 * draw:.1f} {sd * (190 - 10 * draw):.1f}, 18 {sd * 40}" '
              f'stroke="{light}" stroke-width="4" fill="none" opacity="0.8"/>'
              f'<path d="M {tx + 26:.1f} {sd * (ty - 8):.1f} C {tx + 18:.1f} {sd * (ty + 4):.1f}, {tx + 8:.1f} {sd * (ty + 6):.1f}, {tx:.1f} {sd * ty:.1f}" '
              f'stroke="{OUT}" stroke-width="15" fill="none" stroke-linecap="round"/>'
              f'<path d="M {tx + 26:.1f} {sd * (ty - 8):.1f} C {tx + 18:.1f} {sd * (ty + 4):.1f}, {tx + 8:.1f} {sd * (ty + 6):.1f}, {tx:.1f} {sd * ty:.1f}" '
              f'stroke="{wood}" stroke-width="9" fill="none" stroke-linecap="round"/>')
    o += '<rect x="8" y="-34" width="28" height="68" rx="8" fill="#3a2412" stroke="#1b0f0a" stroke-width="2"/>'
    # the string: from the tips to the nock (or straight when at rest), shaking after the release
    sx = nock
    if shake > 0:
        sx = -40 + 60 * shake * math.sin(t * 95)
    o += (f'<path d="M {tx + 6:.1f} {-ty:.1f} L {sx:.1f} 0 L {tx + 6:.1f} {ty:.1f}" stroke="#efe6cc" stroke-width="3.5" fill="none" stroke-linejoin="round"/>')
    if arrow:
        a0, a1 = arrow
        o += (f'<path d="M {a0:.1f} 0 L {a1 - 60:.1f} 0" stroke="{OUT}" stroke-width="11"/><path d="M {a0:.1f} 0 L {a1 - 60:.1f} 0" stroke="#c8a46a" stroke-width="6"/>'
              f'<path d="M {a1:.1f} 0 L {a1 - 64:.1f} -16 L {a1 - 56:.1f} 0 L {a1 - 64:.1f} 16 Z" fill="#dfe4ea" stroke="{OUT}" stroke-width="3"/>'
              f'<path d="M {a0 + 20:.1f} 0 L {a0 + 70:.1f} -26 L {a0 + 100:.1f} -24 L {a0 + 64:.1f} 0 L {a0 + 100:.1f} 24 L {a0 + 70:.1f} 26 Z" fill="#6a4a2e" stroke="{OUT}" stroke-width="3"/>')
    return o


BOW_DEFS = '<defs><filter id="bowglow" x="-50%" y="-200%" width="200%" height="500%"><feGaussianBlur stdDeviation="14"/></filter></defs>'


def archer(S, q, x, y, s, t, draw=0.0, holding=True, arrow=True, glow=0.0, shake=0.0, arrow_gone=False, neck=True):
    """a person facing right drawing the great bow: the bow in the left hand (q["armL"]), the right hand (q["armR"]) on the string;
    draw 0..1 bends the bow; holding=False: the string is at rest; arrow_gone: the arrow has left. Returns person + bow + hands (SVG)."""
    q = dict(q); q["propL"] = None; q["propR"] = None
    body = (at_neck if neck else at_feet)(S, q, t, x, y, s)
    bx, by = hand_at(S, q["armL"], 1, x, y, s, neck=neck)
    hx, hy = hand_at(S, q["armR"], -1, x, y, s, neck=neck)
    k = s * S["bs"]
    ang = math.degrees(math.atan2(by - hy, bx - hx))
    D = math.hypot(bx - hx, by - hy) / k
    nock = -D if holding else -40
    if draw is None:                       # the bow bends as far as the string is pulled
        draw = max(0.0, min(1.0, (D - 130) / 710)) if holding else 0.0
    arr = None
    if arrow and not arrow_gone:
        tail = nock
        arr = (tail, tail + 930)
    g = (f'<g transform="translate({bx:.1f},{by:.1f}) rotate({ang:.2f}) scale({k:.4f})">' + great_bow(draw, nock, arr, glow, shake, t) + '</g>')
    hands = fist(S, bx, by, 30 * k)
    if holding:
        hands += fist(S, hx, hy, 28 * k)
    return BOW_DEFS + body + g + hands


def lightness(svg, a):
    """the same SVG turned golden and bright (a 0..1): light filling a body"""
    if a <= 0.01:
        return ""
    return ('<defs><filter id="goldf" color-interpolation-filters="sRGB"><feColorMatrix type="matrix" values="0.45 0.45 0.25 0 0.32  0.38 0.42 0.2 0 0.24  '
            '0.18 0.2 0.2 0 0.06  0 0 0 1 0"/></filter></defs>'
            f'<g filter="url(#goldf)" opacity="{a:.3f}">{svg}</g>')


class LightMotes:
    """golden motes rising from a body and carried away by the wind (to the left and up): emitted from the box (x0, y0, x1, y1) in scene
    coordinates between t0 and t1 (shot time), seen through camera cam"""
    def __init__(self, cam, box, t0, t1, n=260, seed=0, wind=(-170, -120), col=GOLD, size=(1.8, 4.6)):
        r = random.Random(seed)
        x0, y0, x1, y1 = box
        self.p = [(r.uniform(x0, x1), r.uniform(y0, y1), r.uniform(t0, t1), r.uniform(1.4, 2.6), r.uniform(*size), r.uniform(0, 6.3),
                   r.uniform(0.7, 1.3)) for _ in range(n)]
        self.cam, self.wind, self.col = cam, wind, col

    def __call__(self, im, t):
        d = ImageDraw.Draw(im, "RGBA")
        k = self.cam(t)[0]
        for x, y, ts, life, sz, ph, sp in self.p:
            u = (t - ts) / life
            if not 0 <= u < 1:
                continue
            px = x + self.wind[0] * sp * (t - ts) * (0.6 + u) + 18 * math.sin(t * 3 + ph)
            py = y + self.wind[1] * sp * (t - ts) + 10 * math.sin(t * 2.2 + ph)
            cx, cy = cam_xy(self.cam, t, px, py)
            a = int(255 * min(1.0, u * 6) * (1 - u) ** 1.2)
            rr = sz * k * (1 - 0.4 * u)
            d.ellipse((cx - rr * 2.6, cy - rr * 2.6, cx + rr * 2.6, cy + rr * 2.6), fill=self.col + (a // 6,))
            d.ellipse((cx - rr, cy - rr, cx + rr, cy + rr), fill=(255, 246, 220, a))


def shake_cam(cam, t0, amp=10, dur=0.5):
    """a camera with a short shake from t0 (shot time)"""
    def c(t):
        k, cx, cy, px, py = cam(t)
        u = (t - t0) / dur
        if 0 <= u < 1:
            e = (1 - u) ** 2 * amp
            px += e * math.sin(t * 70); py += e * math.cos(t * 57)
        return k, cx, cy, px, py
    return c


def bow_lying(x, y, s, t, ang=90.0):
    """the great bow lying on the snow (the prop turned on its side), its grip at (x, y)"""
    c = Ctx(lw_for(s))
    return f'<g transform="translate({x:.1f},{y:.1f}) scale({s:.4f})">{prop(c, "bow", 0, 0, ang, t)}</g>'


def flying_arrow(x, y, ang, s, trail=1.0, glow=1.0):
    """the arrow in flight with its golden trail and a soft light round it"""
    o = ""
    if glow > 0:
        o += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{140 * s + 10:.1f}" fill="#fff0c0" opacity="{0.35 * glow:.2f}" filter="url(#arglow)"/>'
    return ('<defs><filter id="arglow" x="-100%" y="-100%" width="300%" height="300%"><feGaussianBlur stdDeviation="10"/></filter></defs>'
            + o + arrow_svg(x, y, ang, s, trail=trail))




def dawn_foot(blur=0):
    """the foot of the mountain at sunrise: Damavand with the road (zbg.damavand("dusk", road=True)) turned left to right, so that the
    sun is in the east at the right, as on the summit; the summit at (470, 525)"""
    return bg("damavand_dawn_road", lambda: ImageOps.mirror(zbg.damavand("dusk", road=True)), blur)


def summit_bg(blur=0):
    return bg("summit_sunrise", lambda: abg.summit("sunrise"), blur)


def sun_glow(cam, a=0.45, r=520):
    """the rising sun's glow on the summit view (abg.summit("sunrise"): sun at (905, 1120))"""
    return FadeGlow(lambda t: cam_xy(cam, t, 905, 1120), r, (255, 220, 150), (a if callable(a) else (lambda t: a)))


# ================================================================ S1 the hook (0-7.8): the arrow over the desert, then over the river
def s1():
    des = bg("desert", abg.desert)
    camA = cam_push(1.0, 1.06, 540, 900, 3.8)

    def midA(t):
        u = t / 3.8
        x = lerp(-220, 1300, u); y = lerp(860, 660, u) - 40 * math.sin(math.pi * u)
        return flying_arrow(x, y, -7, 0.36, trail=1.0)
    A = Shot(3.8, des, midA, cam=camA, light=dict(rim=(0, 0)), sun=SUN_NOON, bloom=0.6, fade_in=0.4,
             fx=[Motes(40, 101, (255, 236, 200), (0, 900, W, 1700), (-60, -4), amax=80)])

    riv = bg("jeyhun", abg.jeyhun)
    camB = cam_push(1.0, 1.05, 540, 800, 4.0)

    def midB(t):
        u = t / 4.0
        x = lerp(-240, 1320, u); y = lerp(560, 450, u)
        return flying_arrow(x, y, -4, 0.2, trail=1.0)
    B = Shot(4.0, riv, midB, cam=camB, light=dict(rim=(0, 0)), sun=(820, 300, 900, (0.08, 0.07, 0.04)), bloom=0.6, fade_out=0.3,
             fx=[Motes(30, 102, (255, 250, 230), (0, 900, W, 1400), (-20, -2), amax=60)])
    return [A, B]


# ================================================================ S2 title (7.8-12.4): the summit at sunrise
def s2():
    cam = cam_push(1.0, 1.05, 600, 1100, 4.6)

    def mid(t):
        q = P(turn=0.4, gx=0.9, gy=-0.1, furrow=0.2, armL=("ik", 340, 220, "down"), propL="bow", armR="relaxed", wind=1.2, blink=blink_at(t, 3),
              breathe=math.sin(t * 1.8))
        return at_feet(ARASH_BARE, q, t, 470, abg.summit_y(470), 0.3)
    return [Shot(4.6, summit_bg(), mid, cam=cam, bg_par=1.0, light=SUNRISE, sun=SUN_RISE, bloom=0.7, fade_in=0.3, fade_out=0.4,
                 fx=[sun_glow(cam, 0.35), snow_wind(201), Motes(30, 202, (255, 230, 200), (0, 300, W, 1300), (-30, -2), amax=90)])]


# ================================================================ S3 the shot (12.4-62.4)
DRAW_BOW = ("ik", 690, -50)              # the bow arm, straight out to the east
ANCHOR = ("ik", -150, -50, "down")        # the string hand at full draw: beside the cheek, the elbow back


def s3():
    T = S0["s3"]
    sm = summit_bg()
    smb = summit_bg(6)

    # A: sunrise; Arash on the summit with the great bow; he looks down at the armies, then at the sun (narrator)
    camA = cam_push(1.0, 1.06, 560, 1100, 4.4)

    def midA(t):
        sun = ease((t - 2.2) / 0.8)
        q = P(turn=-0.1 + 0.5 * sun, gx=-0.3 + 1.2 * sun, gy=0.6 - 0.7 * sun, brow=0.3, furrow=0.2, armL=("ik", 340, 220, "down"), propL="bow",
              armR="relaxed", blink=blink_at(t, 1), breathe=math.sin(t * 1.9), wind=1.2)
        return at_feet(ARASH_BARE, q, t, 560, abg.summit_y(560), 0.44)
    A = Shot(4.4, sm, midA, cam=camA, bg_par=1.0, light=SUNRISE, sun=SUN_RISE, bloom=0.7, fade_in=0.4,
             fx=[sun_glow(camA, lambda t: 0.25 + 0.35 * ease(t / 4.0), 560), snow_wind(301), Motes(30, 302, (255, 230, 200), (0, 300, W, 1300), (-30, -2), amax=90)])

    # B: below, the king and his general look up: "My king… he is ready." — "Then all of Iran is with him."
    T_B = T + 4.4
    LBg = lines_in(T_B, "p3s3b"); LBm = lines_in(T_B, "p3s3c")
    foot = dawn_foot(5)
    camB = cam_push(1.0, 1.05, 540, 900, 5.8)
    heads = bgs.cached("ar_p03_foot_heads", lambda: back_heads(311, 8, 1820, 0.6, col="#1a1216", blur=3))

    def midB(t):
        tm = LBm[0][1]
        g = tp(LBg, t, 1, turn=0.3, gx=0.6 if t < tm - 0.3 else -0.2, gy=0.1 if t < tm - 0.3 else -0.8, brow=0.5, furrow=0.2, armL="relaxed",
               armR="relaxed", wind=0.6)
        m = tp(LBm, t, 2, turn=-0.25, gx=-0.4 if t < 2.4 else -0.6, gy=-0.85 if t < 2.4 or t > tm + 1.6 else -0.2, sad=0.35, brow=0.6, furrow=-0.2,
               armR="chest" if t > tm + 0.2 else "relaxed", armL="relaxed", wind=0.6, cloak_len=0.9)
        return at_neck(GENERAL, g, t, 300, 1000, 0.8) + at_neck(MANUCHEHR, m, t, 770, 990, 0.82)
    B = Shot(5.8, foot, midB, fg=heads, cam=camB, light=SUNRISE, sun=(1000, 900, 900, (0.12, 0.08, 0.04)), bloom=0.6,
             fx=[Motes(30, 303, (255, 230, 200), (0, 300, W, 1300), (-20, -2), amax=70)])

    # C: Arash, close: he holds up the arrow: "All my strength… into this one arrow." Then to the east: "Fly far… for the children of Iran."
    T_C = T + 10.2
    LC = lines_in(T_C, "p3s3d", "p3s3e")
    camC = cam_push(1.0, 1.08, 540, 860, 8.4)
    te = LC[1][1]

    def midC(t):
        lift = ease((t - 0.1) / 0.6) * (1 - ease((t - te + 0.6) / 0.6))
        east = ease((t - te + 0.4) / 0.6)
        armR = ("ik", lerp(-250, -340, lift), lerp(330, -180, lift), "down")
        q = tp(LC, t, 3, turn=0.1 + 0.3 * east, gx=-0.6 * (1 - east) + 0.9 * east, gy=-0.6 * (1 - east) - 0.1 * east, brow=0.3, furrow=0.3,
               sad=0.2 * (1 - east), smile=0.15 * east, armR=armR, propR="arrow", armL=("ik", 340, 220, "down"), propL="bow", wind=1.1)
        return at_neck(ARASH_BARE, q, t, 540, 960, 1.0)
    C = Shot(8.4, smb, midC, cam=camC, light=SUNC, sun=SUN_RISE, bloom=0.6, fx=[snow_wind(304, n=150)])

    # D0: closer: he lifts the great bow and sets the arrow on the string
    T_D = T + 18.6
    nk = A3.NOCK - T_D
    camD0 = cam_push(1.0, 1.04, 520, 900, 1.2)

    def midD0(t):
        up = ease(t / 0.9)
        on = ease((t - nk + 0.3) / 0.3)
        q = P(turn=0.4, gx=0.8, gy=0.3, furrow=0.4, brow=0.2, armL=("ik", lerp(420, 560, up), lerp(320, 150, up)),
              armR=("ik", lerp(-120, 420, on), lerp(380, 150, up), ), wind=1.0, blink=blink_at(t, 6))
        return archer(ARASH_BARE, q, 380, 900, 0.9, t, draw=0.0, holding=on > 0.98, arrow=on > 0.6)
    D0 = Shot(1.2, smb, midD0, cam=camD0, light=dict(SUNC, rim_str=1.2), sun=SUN_RISE, bloom=0.7, fx=[snow_wind(311, n=150)])

    # D1: the draw: the string comes back to his cheek, the elbow comes down, the great bow bends; light gathers on the arrow
    d0, d1 = A3.DRAW[0] - T_D - 1.2, A3.DRAW[1] - T_D - 1.2
    camD = cam_push(1.0, 1.07, 520, 820, 5.2)

    def pose_D(t):
        u = ease((t - d0) / (d1 - d0))
        trem = 3 * ease((t - d1 + 0.6) / 0.6) * math.sin(t * 31)
        hand = ("ik", lerp(-80, ANCHOR[1], u), ANCHOR[2] + trem, "down")
        return P(turn=0.45, gx=0.9, gy=0.0, furrow=0.4 + 0.5 * u, brow=0.2, sad=0.0, armL=("ik", DRAW_BOW[1], DRAW_BOW[2] + trem), armR=hand,
                 blink=blink_at(t, 4) * (1 - u), breathe=math.sin(t * 2.6) * (1 - u), wind=1.0), u

    def midD(t):
        q, u = pose_D(t)
        return archer(ARASH_BARE, q, 400, 860, 0.62, t, draw=0.4 + 0.6 * u, glow=ease((t - d1 + 1.6) / 1.6))

    def gl(t):
        return 0.15 + 0.55 * ease((t - d0) / (d1 - d0 + 1.0))
    D = Shot(5.2, smb, midD, cam=camD, light=dict(SUNC, rim_str=1.2), sun=SUN_RISE, bloom=0.8,
             fx=[FadeGlow(lambda t: cam_xy(camD, t, 680, 830), 420, GOLD, gl), snow_wind(305, n=150),
                 Motes(50, 306, (255, 236, 190), (100, 400, 1000, 1200), (-12, -20), amax=120)])

    # E: close: the release; the string goes, the hand flies back and opens, a flash, his hair in the wind
    T_E = T + 25.0
    rl = A3.RELEASE - T_E
    camE = shake_cam(cam_push(1.04, 1.06, 560, 900, 1.4), rl, amp=12, dur=0.45)

    def midE(t):
        gone = t >= rl
        k = ease((t - rl) / 0.18)
        hand = ("ik", ANCHOR[1] - 70 * k, ANCHOR[2] - 30 * k, "down")
        q = P(turn=0.45, gx=0.9, gy=0.0, furrow=0.9 - 0.6 * k, brow=0.2 + 0.4 * k, armL=DRAW_BOW, armR=hand, openR=gone, blink=0.0,
              wind=1.0 + 0.8 * k, mouth_o=0.25 * k)
        o = archer(ARASH_BARE, q, 560, 1000, 1.05, t, draw=None if not gone else 0.0, holding=not gone, arrow_gone=gone, glow=1.0 * (not gone),
                   shake=max(0.0, 1 - (t - rl) / 0.6) if gone else 0.0)
        if gone:      # the arrow's light, gone to the east in a flash
            a = max(0.0, 1 - (t - rl) / 0.7)
            bx, by = hand_at(ARASH_BARE, DRAW_BOW, 1, 560, 1000, 1.05, neck=True)
            o += f'<path d="M {bx - 300:.0f} {by:.0f} L 1200 {by - 20:.0f}" stroke="#fff4d0" stroke-width="{14 * a + 2:.0f}" opacity="{a:.2f}" stroke-linecap="round"/>'
        return o
    E = Shot(1.4, smb, midE, cam=camE, light=dict(SUNC, rim_str=1.3), sun=SUN_RISE, bloom=0.9,
             fx=[FadeGlow(lambda t: (760, 840), 520, (255, 236, 190), lambda t: 0.5 + 0.5 * max(0.0, 1 - abs(t - rl) / 0.35)), snow_wind(307, n=160, wind=-900)])

    # F: wide: the arrow flies away over the peaks into the sunrise, a line of gold behind it
    camF = cam_push(1.0, 1.06, 640, 1000, 2.6)
    AX, AY = 330, abg.summit_y(330)
    bx0, by0 = hand_at(ARASH_BARE, DRAW_BOW, 1, AX, AY, 0.36)

    def arrow_F(t):
        u = ease(min(1.0, t / 2.4) * 0.9 + 0.1 * min(1.0, t / 2.4)) if t > 0 else 0
        u = 1 - (1 - min(1.0, t / 2.4)) ** 2.2
        x = lerp(bx0 + 60, 1010, u); y = lerp(by0, 660, u) - 140 * math.sin(math.pi * u * 0.8)
        return x, y, u

    def midF(t):
        x, y, u = arrow_F(t)
        trail = "".join(f'<circle cx="{lerp(bx0 + 60, x, k / 30):.1f}" cy="{lerp(by0, y, k / 30) - 140 * math.sin(math.pi * (u * k / 30) * 0.8) + 140 * math.sin(math.pi * u * 0.8) * (k / 30) - 0:.1f}" '
                        f'r="{lerp(5, 2, k / 30):.1f}" fill="#fff0c0" opacity="{0.15 + 0.5 * k / 30:.2f}"/>' for k in range(30))
        q = P(turn=0.45, gx=0.9, gy=-0.2, furrow=0.3, brow=0.5, armL=DRAW_BOW, armR=("ik", -230, -90, "down"), openR=True, wind=1.3, blink=0.0)
        body = archer(ARASH_BARE, q, AX, AY, 0.36, t, draw=0.0, holding=False, arrow_gone=True, neck=False, shake=max(0.0, 0.5 - t / 1.4))
        return body + trail + flying_arrow(x, y, lerp(-20, -10, u), lerp(0.3, 0.05, u), trail=1.0)
    F = Shot(2.6, sm, midF, cam=camF, bg_par=1.0, light=SUNRISE, sun=SUN_RISE, bloom=0.8,
             fx=[sun_glow(camF, 0.55), snow_wind(308, n=200, wind=-800)])

    # G: medium close: the light fills him; he closes his eyes, calm, and begins to turn into light and wind
    T_G = T + 29.0
    g0, f0, f1 = A3.GLOW - T_G, A3.FADE[0] - T_G, A3.FADE[1] - T_G
    camG = cam_push(1.0, 1.05, 540, 860, 3.6)
    GX, GY, GS = 540, 900, 0.85

    def body_G(t):
        lower = ease((t - 0.0) / 1.4)
        q = P(turn=0.35 - 0.2 * lower, gx=0.8 - 0.6 * lower, gy=-0.3 + 0.2 * lower, brow=0.4, furrow=-0.3 * lower, smile=0.3 * ease((t - 1.0) / 1.0),
              blink=max(blink_at(t, 5) * (t < 1.2), ease((t - 1.4) / 1.2)), armL=("ik", lerp(560, 340, lower), lerp(-40, 220, lower), "down"),
              armR="relaxed", wind=1.2, breathe=math.sin(t * 1.4))
        return q

    def midG(t):
        q = body_G(t)
        body = at_neck(ARASH_BARE, q, t, GX, GY, GS)
        a = 1 - ease((t - f0) / (f1 - f0)) if t > f0 else 1.0
        gold = ease((t - g0) / 1.2)
        bx, by = hand_at(ARASH_BARE, q["armL"], 1, GX, GY, GS, neck=True)
        bow = bow_lying(bx, by, GS * ARASH_BARE["bs"], t, ang=lerp(-20, 0, ease(t / 1.4)))
        return f'<g opacity="{a:.3f}">{body}{lightness(body, 0.85 * gold)}</g>' + bow
    G = Shot(3.6, smb, midG, cam=camG, light=dict(SUNC, rim_str=1.2), sun=SUN_RISE, bloom=0.9,
             fx=[FadeGlow(lambda t: cam_xy(camG, t, GX, GY + 150), 560, GOLD, lambda t: 0.2 + 0.6 * ease((t - g0) / 1.2)),
                 LightMotes(camG, (GX - 220, GY - 330, GX + 220, GY + 700), f0 - 0.3, 3.6, n=300, seed=309),
                 snow_wind(310, n=150, wind=-700)])

    # H: wide (the camera low on the summit): the last of his light is carried away by the wind; the great bow falls on the snow
    T_H = T + 32.6
    camH = cam_push(1.4, 1.43, 540, 1900, 2.6)
    HX = 540; HY = abg.summit_y(HX); HS = 0.3
    bf = A3.BOWFALL - T_H

    def midH(t):
        tg = t + 3.6                                  # G's clock
        a = 1 - ease((tg - f0) / (f1 - f0))
        q = body_G(tg)
        q["armL"] = ("ik", 340, 220, "down")
        body = at_feet(ARASH_BARE, q, t, HX, HY, HS)
        o = f'<g opacity="{a:.3f}">{lightness(body, 0.9)}</g>' if a > 0.01 else ""
        bx, by = hand_at(ARASH_BARE, ("ik", 340, 220, "down"), 1, HX, HY, HS)
        u = min(1.0, max(0.0, (t - bf) / 0.45)) ** 2
        land = (bx + 40, HY - 12)
        x = lerp(bx, land[0], u); y = lerp(by, land[1], u)
        o += bow_lying(x, y, HS * ARASH_BARE["bs"], t, ang=lerp(0, 88, u))
        if t > bf + 0.45:          # a puff of snow where it lands
            p_ = (t - bf - 0.45) / 0.8
            if p_ < 1:
                o += f'<ellipse cx="{land[0]:.0f}" cy="{land[1]:.0f}" rx="{60 + 80 * p_:.0f}" ry="{14 + 18 * p_:.0f}" fill="#ffffff" opacity="{0.6 * (1 - p_):.2f}"/>'
        return o
    Hh = Shot(2.6, sm, midH, cam=camH, bg_par=1.0, light=SUNRISE, sun=None, bloom=0.4,
              fx=[FadeGlow(lambda t: cam_xy(camH, t, HX, HY - 250), 300, GOLD, lambda t: 0.3 * (1 - ease((t + 3.6 - f0) / (f1 - f0)))),
                  LightMotes(camH, (HX - 80, HY - 480, HX + 80, HY - 20), 0.0, 1.4, n=160, seed=311, wind=(-150, -110)),
                  snow_wind(312, n=220, wind=-800)])

    # I: close on the empty summit: only the bow on the snow, and the wind (narrator)
    def midI(t):
        drift = ('<defs><linearGradient id="drift" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff6ee"/><stop offset="0.25" stop-color="#ece0e6"/>'
                 '<stop offset="1" stop-color="#b8a4c4"/></linearGradient></defs>'
                 '<path d="M -60 1010 C 200 960, 420 990, 640 975 C 820 962, 960 985, 1140 970 L 1140 1960 L -60 1960 Z" fill="url(#drift)"/>'
                 '<path d="M -60 1010 C 200 960, 420 990, 640 975 C 820 962, 960 985, 1140 970" stroke="#ffffff" stroke-width="10" fill="none" opacity="0.85"/>'
                 '<path d="M -60 1010 C 120 990, 260 1010, 380 1060 C 300 1120, 120 1130, -60 1120 Z" fill="#a898bc" opacity="0.35"/>'
                 '<path d="M 640 975 C 760 1000, 820 1060, 760 1130 C 900 1100, 1040 1060, 1140 1040 L 1140 970 C 960 985, 820 962, 640 975 Z" fill="#a898bc" opacity="0.3"/>')
        for k, (x0, y0, w) in enumerate(((90, 1150, 260), (520, 1110, 320), (300, 1260, 380), (760, 1230, 300), (120, 1420, 420), (640, 1400, 380))):
            drift += f'<path d="M {x0} {y0} q {w * 0.5:.0f} -18 {w} 0" stroke="#ffffff" stroke-width="5" fill="none" opacity="0.5"/>'
        drift += '<ellipse cx="560" cy="990" rx="360" ry="22" fill="#8a7a9a" opacity="0.35"/>'
        return drift + bow_lying(560, 968, 0.9, t, ang=86)
    camI = cam_push(1.0, 1.06, 560, 960, 4.8)
    I = Shot(4.8, smb, midI, cam=camI, light=dict(SUNC, rim=(0, -3)), sun=None, bloom=0.5,
             fx=[Snow(360, 313, -900, (40, 140), (1.4, 4.2), (90, 220)), LightMotes(camI, (300, 500, 1000, 1000), 0.0, 2.5, n=40, seed=314)])

    # J: below: the hungry boy and his mother in the wind: "Mother… where is Arash?" — "He is the wind now, my son."
    T_J = T + 40.0
    LJb = lines_in(T_J, "p3s3j"); LJm = lines_in(T_J, "p3s3k")
    camJ = cam_push(1.0, 1.05, 540, 880, 6.4)

    def midJ(t):
        tm = LJm[0][1]
        look = ease((t - tm + 0.2) / 0.5)
        hand = ease((t - tm - 0.6) / 0.6)
        b = tp(LJb, t, 3, turn=0.35, gx=0.2 + 0.6 * ease((t - 1.6) / 0.4), gy=-0.9 + 0.3 * ease((t - 1.6) / 0.4), sad=0.5, brow=0.7, furrow=-0.3,
               armL="relaxed", armR="relaxed", wind=1.1)
        m = tp(LJm, t, 4, turn=-0.25, gx=-0.3 - 0.4 * look, gy=-0.9 + 1.2 * look, sad=0.6, brow=0.6, furrow=-0.2, smile=0.25 * look, armL="chest",
               armR=("ik", lerp(-200, -330, hand), lerp(330, 150, hand)) if hand > 0.02 else "relaxed", wind=1.1)
        return at_neck(MOTHER, m, t, 650, 880, 0.95) + at_neck(BOY, b, t, 360, 1000, 0.95)
    J = Shot(6.4, dawn_foot(6), midJ, cam=camJ, light=SUNRISE, sun=(1000, 900, 900, (0.12, 0.08, 0.04)), bloom=0.6,
             fx=[LightMotes(camJ, (700, 200, 1300, 900), 0.0, 6.0, n=60, seed=315, wind=(-160, -30))])

    # K: Arash's mother, close, the wind in her blue scarf: "My brave son…"
    T_K = T + 46.4
    LK = lines_in(T_K, "p3s3l")
    camK = cam_push(1.0, 1.06, 540, 860, 3.6)

    def midK(t):
        q = tp(LK, t, 5, turn=0.1, gx=0.3, gy=-0.75, sad=0.6, brow=0.7, furrow=-0.3, smile=0.3 * ease((t - 1.8) / 0.8), armL="chest", armR="relaxed",
               wind=1.4)
        return at_neck(ARASH_MOTHER, q, t, 540, 960, 0.95)
    K = Shot(3.6, dawn_foot(6), midK, cam=camK, light=SUNRISE, sun=(1000, 900, 900, (0.12, 0.08, 0.04)), bloom=0.6, fade_out=0.6,
             fx=[LightMotes(camK, (700, 300, 1300, 900), 0.0, 3.4, n=50, seed=316, wind=(-170, -40))])
    return [A, B, C, D0, D, E, F, G, Hh, I, J, K]



# ================================================================ S4 the flight (62.4-87.0): the witnesses ride after it; the desert; the river
WIT_HORSES = {"A": "#2a2224", "B": "#6b4426"}


def witness_rider(S, t, x, y, s, lines=(), seed=0, gallop=True, flip=False, **kw):
    base = dict(turn=0.35, gx=0.8, gy=-0.7, furrow=0.6, brow=0.4, armR="forward", armL="forward", wind=1.0)
    base.update(kw)
    q = tp(list(lines), t, seed, **base)
    col = WIT_HORSES["A" if S is WITNESS_A else "B"]
    ph = t * (10.5 if gallop else 4.2) + seed
    return rider(S, q, t, lambda c: horse(c, col=col, walk=True, phase=ph, t=t + seed, head_bob=(-18 * math.sin(ph)) if gallop else 0.0,
                                          blanket="#5a0e10" if S is WITNESS_A else "#2a2a34"), x, y, s, flip=flip)


def s4():
    T = S0["s4"]
    # A: the two witnesses of Turan gallop across the plain, looking up at the arrow's light: "Ride! Don't lose it!" — "It is still flying!"
    LAa = lines_in(T, "p3s4a"); LAb = lines_in(T, "p3s4b")
    strip = bgs.cached("zh_ride_strip", zbg.ride_strip)

    def bgA(t):
        x0 = int(200 + 260 * t)
        return strip.crop((x0, 0, x0 + W, H))
    camA = cam_push(1.0, 1.03, 540, 1000, 5.2)

    def midA(t):
        bob = 8 * math.sin(t * 21)
        pt = ease((t - 0.4) / 0.4) * (1 - ease((t - 2.0) / 0.4))
        sky = flying_arrow(lerp(820, 980, t / 5.2), lerp(330, 300, t / 5.2), -6, 0.1, trail=1.0)
        b = witness_rider(WITNESS_B, t, 380 + 10 * math.sin(t * 1.3), 1330 + bob * 0.8, 0.78, lines=LAb, seed=2, gx=0.8, gy=-0.8)
        a = witness_rider(WITNESS_A, t, 600 + 12 * math.sin(t * 1.1), 1470 + bob, 0.95, lines=LAa, seed=1, gx=0.9, gy=-0.6,
                          armL=("ik", lerp(200, 420, pt), lerp(300, -260, pt)) if pt > 0.02 else "forward")
        return sky + b + a
    A = Shot(5.2, bgA, midA, cam=camA, light=dict(DAYL, rim=(5, -3)), sun=(900, 300, 900, (0.08, 0.07, 0.04)), bloom=0.5, fade_in=0.3,
             fx=[Motes(70, 401, (200, 170, 120), (0, 1350, W, 1650), (-260, -10), size=(2, 6), amax=110)])

    # B: high over the desert, the arrow flies on (narrator: "The arrow flew all morning…")
    des = bg("desert", abg.desert)
    camB = cam_push(1.08, 1.14, 760, 700, 4.6)

    def midB(t):
        u = t / 4.6
        return flying_arrow(lerp(-120, 1220, u), lerp(470, 400, u), -3, 0.16, trail=1.0)
    B = Shot(4.6, des, midB, cam=camB, light=dict(rim=(0, 0)), sun=SUN_NOON, bloom=0.6,
             fx=[Motes(40, 402, (255, 236, 200), (0, 900, W, 1700), (-50, -4), amax=70)])

    # C: the great river; the arrow comes down out of the sky and strikes the walnut tree on the far bank
    riv = bg("jeyhun", abg.jeyhun)
    T_C = T + 9.8
    hit = A3.IMPACT - T_C
    camC = cam_push(1.0, 1.7, 740, 900, 5.2)
    hx, hy = abg.WALNUT_HIT

    def arrow_C(t):
        u = min(1.0, max(0.0, t / hit))
        x = lerp(-150, hx - 14, u); y = lerp(240, hy, u ** 1.6)
        dx = (hx - 14) - (-150); dy = (hy - 240) * 1.6 * max(u, 0.05) ** 0.6
        return x, y, math.degrees(math.atan2(dy, dx)), lerp(0.22, 0.06, u)

    def midC(t):
        if t < hit:
            x, y, ang, sc = arrow_C(t)
            return flying_arrow(x, y, ang, sc, trail=1.0)
        x, y, ang, sc = arrow_C(hit)
        wob = 6 * math.exp(-(t - hit) * 4) * math.sin((t - hit) * 40)
        return arrow_svg(x - 4, y, ang + wob, sc)

    def leaves(im, t):
        if t < hit:
            return
        d = ImageDraw.Draw(im, "RGBA")
        r = random.Random(403)
        for k in range(26):
            vx = r.uniform(-60, 60); vy0 = r.uniform(-40, 20); ph = r.uniform(0, 6)
            u = t - hit - r.uniform(0, 0.3)
            if u < 0:
                continue
            x = hx + r.uniform(-140, 140) + vx * u + 14 * math.sin(u * 4 + ph); y = hy - r.uniform(60, 260) + vy0 * u + 60 * u * u
            cx, cy = cam_xy(camC, t, x, y)
            k_ = camC(t)[0]
            a = int(230 * max(0.0, 1 - u / 1.6))
            d.ellipse((cx - 5 * k_, cy - 3 * k_, cx + 5 * k_, cy + 3 * k_), fill=(70, 110, 50, a))
    C = Shot(5.2, riv, midC, cam=camC, bg_par=1.0, light=dict(rim=(0, 0)), sun=(820, 300, 900, (0.08, 0.07, 0.04)), bloom=0.6,
             fx=[leaves, FadeGlow(lambda t: cam_xy(camC, t, hx, hy), 160, (255, 240, 190), lambda t: 0.8 * max(0.0, 1 - abs(t - hit) / 0.5) if t > hit - 0.2 else 0.0)])

    # D: close: the arrow deep in the walnut tree, still shaking; leaves and a green walnut fall; its light fades
    wc = bg("walnut_close", abg.walnut_close)
    camD = cam_push(1.08, 1.16, 560, 760, 2.8)
    ax, ay = abg.WALNUT_ARROW
    ANG = 24.0

    def midD(t):
        wob = 5 * math.exp(-t * 2.2) * math.sin(t * 34)
        a = ANG + wob
        r_ = math.radians(a)
        # the head is in the wood: draw the shaft from the bark back towards the archer
        cx_, cy_ = ax - math.cos(r_) * 300 * 0.9, ay - math.sin(r_) * 300 * 0.9
        o = f'<g>{arrow_svg(cx_, cy_, a, 0.9)}</g>'
        o += '<ellipse cx="{:.0f}" cy="{:.0f}" rx="16" ry="22" fill="#3a342c" opacity="0.7"/>'.format(ax - 4, ay)
        wy = 330 + 900 * max(0.0, t - 0.5) ** 2 if t > 0.5 else 330
        if wy < 2000:
            o += f'<circle cx="210" cy="{wy:.0f}" r="30" fill="#6a8a3a" stroke="#1e2a12" stroke-width="3"/>'
        return o

    def fall_leaves(im, t):
        d = ImageDraw.Draw(im, "RGBA")
        r = random.Random(404)
        for k in range(14):
            x0 = r.uniform(80, 1000); v = r.uniform(120, 220); ph = r.uniform(0, 6)
            y = r.uniform(-100, 300) + v * t
            x = x0 + 40 * math.sin(t * 2.2 + ph)
            cx, cy = cam_xy(camD, t, x, y)
            d.ellipse((cx - 22, cy - 10, cx + 22, cy + 10), fill=(70, 110, 50, 220))
    D = Shot(2.8, wc, midD, cam=camD, bg_par=1.0, light=dict(NOON, rim=(-5, -2)), sun=None, bloom=0.6,
             fx=[fall_leaves, FadeGlow(lambda t: cam_xy(camD, t, ax - 120, ay - 50), 260, (255, 236, 180), lambda t: 0.6 * (1 - ease(t / 2.4)))])

    # E1: the witnesses ride up to the near bank and rein in; one points across: "There! In that walnut tree!"
    T_E = T + 17.8
    LE = lines_in(T_E, "p3s4e")
    camE = cam_push(1.3, 1.34, 540, 1900, 3.4)          # low: the bank comes up above the subtitles

    def midE(t):
        u = ease(t / 1.4)
        moving = t < 1.4
        pt = ease((t - LE[0][1] - 0.1) / 0.4)
        b = witness_rider(WITNESS_B, t, lerp(-300, 180, u), 1480, 0.7, seed=4, gallop=moving, gx=0.5, gy=-0.6, armR="forward", armL="forward")
        a = witness_rider(WITNESS_A, t, lerp(60, 560, u), 1560, 0.8, lines=LE, seed=3, gallop=moving, gx=0.6, gy=-0.7,
                          armL=("ik", lerp(200, 440, pt), lerp(300, -320, pt)) if pt > 0.02 else "forward")
        return b + a
    E = Shot(3.4, riv, midE, cam=camE, bg_par=1.0, light=NOON, sun=(820, 300, 900, (0.08, 0.07, 0.04)), bloom=0.5,
             fx=[Motes(40, 405, (200, 180, 140), (0, 1400, W, 1700), (-120, -10), size=(2, 5), amax=90)])

    # E2: close on the two of them, the river and the tree behind: "On the other side of the river…"
    T_E2 = T + 21.2
    LE2 = lines_in(T_E2, "p3s4f")
    rivb = bg("jeyhun", abg.jeyhun, 6)
    camE2 = cam_push(1.0, 1.05, 540, 860, 3.4)

    def midE2(t):
        b = tp(LE2, t, 5, turn=-0.2, gx=-0.3 if t < 0.5 else 0.5, gy=-0.4, brow=0.8, furrow=-0.5, sad=0.2, armL="relaxed", armR="relaxed", wind=0.5)
        a = tp([], t, 6, turn=0.25, gx=0.2, gy=-0.4, brow=0.7, furrow=-0.4, armL="relaxed", armR="relaxed", mouth_o=0.15, wind=0.5)
        return at_neck(WITNESS_A, a, t, 300, 1000, 0.8) + at_neck(WITNESS_B, b, t, 790, 990, 0.8)
    E2 = Shot(3.4, rivb, midE2, cam=camE2, light=NOON, sun=(820, 300, 900, (0.08, 0.07, 0.04)), bloom=0.5)
    return [A, B, C, D, E, E2]


# ================================================================ S5 Afrasiab keeps his word (87.0-112.0)
def s5():
    T = S0["s5"]
    tent = bgs.cached("command_tent", bgs.command_tent)
    tentb = bgs.cached("command_tent_b6", lambda: bgs.cached("command_tent", bgs.command_tent).filter(ImageFilter.GaussianBlur(6)))
    lamps = lambda cam: [Glow(lambda t: cam_xy(cam, t, 250, 610), 200, (255, 170, 90), 0.35), Glow(lambda t: cam_xy(cam, t, 840, 610), 200, (255, 170, 90), 0.35)]

    # A: the tent at night: the witnesses come in and bow before Afrasiab (narrator)
    camA = cam_push(1.0, 1.05, 540, 1060, 4.6)

    def midA(t):
        o = ""
        for k, (S, x) in enumerate(((TURAN_SOLDIER, 110), (TURAN_SOLDIER_2, 980))):
            q = P(turn=0.35 if x < 540 else -0.35, gx=0.6 if x < 540 else -0.6, gy=-0.1, furrow=0.6, armL=(20, 10), propL="spear", armR="relaxed",
                  blink=blink_at(t, 50 + k))
            o += at_feet(S, q, t, x, 1560, 0.4)
        o += at_feet(ADVISOR, P(turn=-0.2, gx=-0.6, furrow=0.2, armL="chest", armR="chest", blink=blink_at(t, 53)), t, 860, 1500, 0.38)
        o += at_feet(AFRASIAB, P(turn=-0.3, gx=-0.7, gy=0.1, furrow=0.4, brow=0.3, armL="hip", armR="relaxed", blink=blink_at(t, 54), wind=0.2),
                     t, 680, 1540, 0.44)
        for k, (S, x1, y) in enumerate(((WITNESS_B, 250, 1580), (WITNESS_A, 400, 1560))):
            u = ease((t - 0.2 * k) / 2.2)
            walking = 0.2 * k < t < 2.2 + 0.2 * k
            bow = ease((t - 2.6 - 0.2 * k) / 0.6)
            q = P(turn=0.35, gx=0.7, gy=-0.2 + 0.9 * bow, nod=14 * bow, brow=0.5, furrow=0.2, legs="walk" if walking else "stand", phase=t * 5 + k,
                  armL="chest" if bow > 0.3 else "relaxed", armR="chest" if bow > 0.3 else "relaxed", blink=blink_at(t, 55 + k), wind=0.3)
            o += at_feet(S, q, t, lerp(-120 - 60 * k, x1, u), y, 0.42)
        return o
    A = Shot(4.6, tent, midA, cam=camA, light=TENTL, grade="fire", bloom=0.5, fade_in=0.4, fx=lamps(camA))

    # B: the first witness: "Great king, the arrow fell beyond the Jeyhun River."
    LB = lines_in(T + 4.6, "p3s5b")
    camB = cam_push(1.0, 1.05, 540, 860, 4.2)

    def midB(t):
        q = tp(LB, t, 1, turn=0.25, gx=0.6, gy=-0.3 if t < 3.6 else 0.6, nod=8, brow=0.6, furrow=-0.2, sad=0.2, armL="chest", armR="chest", wind=0.1)
        return at_neck(WITNESS_A, q, t, 540, 960, 1.0)
    B = Shot(4.2, tentb, midB, cam=camB, light=dict(TENTL, rim=(5, -2), ramp=(0, W, 0.88, 1.05)), grade="fire", bloom=0.5)

    # C: Afrasiab, close: "Beyond the Jeyhun?!"
    LC = lines_in(T + 8.8, "p3s5c")
    camC = cam_push(1.02, 1.08, 540, 860, 2.4)

    def midC(t):
        q = tp(LC, t, 2, turn=-0.1, gx=-0.3, gy=0.0, brow=1.0, furrow=-0.6, smile=0.0, armL="hip", armR="relaxed", wind=0.15)
        q["mouth_o"] = max(q["mouth_o"], 0.25 * ease((t - 1.6) / 0.3))
        return at_neck(AFRASIAB, q, t, 540, 960, 1.0)
    C = Shot(2.4, tentb, midC, cam=camC, light=TENTL, grade="fire", bloom=0.5)

    # D: the old advisor: "My king… you gave your word."
    LD = lines_in(T + 11.2, "p3s5d")
    camD = cam_push(1.0, 1.04, 540, 860, 3.6)

    def midD(t):
        q = tp(LD, t, 3, turn=-0.25, gx=-0.6, gy=0.1, brow=0.6, furrow=-0.2, sad=0.3, armL="chest", armR="chest", nod=6, wind=0.1)
        return at_neck(ADVISOR, q, t, 540, 960, 1.0)
    D = Shot(3.6, tentb, midD, cam=camD, light=dict(TENTL, rim=(5, -2), ramp=(0, W, 0.88, 1.05)), grade="fire", bloom=0.5)

    # E: Afrasiab is silent, then: "I did. Then the river is the border." … "Fold the tents. We are going home."
    T_E = T + 14.8
    LE = lines_in(T_E, "p3s5e", "p3s5f")
    camE = cam_push(1.0, 1.08, 540, 860, 6.8)
    t2 = LE[1][1]

    def midE(t):
        down = ease((t - 0.1) / 0.5) * (1 - ease((t - LE[0][1] + 0.3) / 0.4))
        cmd = ease((t - t2 - 0.6) / 0.4)
        q = tp(LE, t, 4, turn=-0.1 - 0.25 * cmd, gx=-0.2 - 0.6 * cmd, gy=0.6 * down, sad=0.3 * down, brow=0.2, furrow=0.4 - 0.3 * down,
               armL="hip", armR="point" if cmd > 0.5 else "relaxed", wind=0.15)
        return at_neck(AFRASIAB, q, t, 540, 960, 1.0)
    E = Shot(6.8, tentb, midE, cam=camE, light=TENTL, grade="fire", bloom=0.5)

    # F: the tired soldier of Turan by his fire, smiling for the first time: "Home…"
    def camp_night():
        im = bgs.cached("army_camp", bgs.army_camp)
        out = Image.alpha_composite(im, Image.new("RGBA", im.size, (8, 10, 30, 175)))
        out.alpha_composite(svg_render(bgs.stars(501, 120, 700)))
        return out.filter(ImageFilter.GaussianBlur(6))
    campn = bg("camp_night_b6", camp_night)
    LF = lines_in(T + 21.6, "p3s5g")
    camF = cam_push(1.0, 1.05, 540, 860, 3.4)

    def midF(t):
        sm = ease((t - 0.4) / 0.8)
        q = tp(LF, t, 5, turn=0.3, gx=0.5 - 0.6 * sm, gy=0.4 - 0.7 * sm, sad=0.7 * (1 - sm), smile=0.7 * sm, brow=0.6 * (1 - sm) + 0.3 * sm,
               furrow=-0.2, armL="chest", armR="relaxed", wind=0.3)
        return at_neck(TURAN_SOLDIER, q, t, 600, 980, 0.95) + fire_svg(140, 1500, 90, t, seed=5)
    F = Shot(3.4, campn, midF, cam=camF, light=FIREL, grade="fire", bloom=0.6, fade_out=0.5,
             fx=[Glow(lambda t: cam_xy(camF, t, 140, 1350), 420, (255, 150, 70), 0.45), Embers(30, 502, (40, 900, 260, 1450), (60, 150))])
    return [A, B, C, D, E, F]


# ================================================================ S6 peace; Tirgan; the arrow still flying (112.0-147.0)
def thread_band(x, y, s, t, ang=0.0, flutter=1.0):
    """a seven-coloured thread tied round a wrist at (x, y) (s: the person's scale), its two ends fluttering in the wind"""
    cols = ("#d8282a", "#f08a1a", "#f2d22a", "#3aa84a", "#2a7ad8", "#3a3aa8", "#8a3ab8")
    o = f'<g transform="translate({x:.1f},{y:.1f}) rotate({ang:.1f}) scale({s:.4f})">'
    for k, c in enumerate(cols):
        o += f'<path d="M -34 {-18 + k * 5.2:.1f} Q 0 {-10 + k * 5.2:.1f} 34 {-18 + k * 5.2:.1f}" stroke="{c}" stroke-width="5.5" fill="none"/>'
    for j, (dx, ph) in enumerate(((-10, 0.0), (8, 1.3))):
        w = 14 * flutter * math.sin(t * 9 + ph)
        for k, c in enumerate(cols[::2]):
            o += f'<path d="M {dx} 14 q {w + 6:.1f} 30 {w * 1.6 - 8 + k * 4:.1f} 70" stroke="{c}" stroke-width="4" fill="none" stroke-linecap="round"/>'
    return o + '</g>'


class WaterDrops:
    """water thrown from a hand: arcs of drops (shot time t0, from (x, y) towards dx) that sparkle and fall back"""
    def __init__(self, cam, throws, seed=0):
        self.cam, self.throws, self.seed = cam, throws, seed

    def __call__(self, im, t):
        d = ImageDraw.Draw(im, "RGBA")
        k_ = self.cam(t)[0]
        for i, (t0, x, y, dx) in enumerate(self.throws):
            u = t - t0
            if not 0 <= u < 1.2:
                continue
            r = random.Random(self.seed * 100 + i)
            for j in range(54):
                vx = dx * r.uniform(0.45, 1.25); vy = -r.uniform(520, 900); dl = r.uniform(0, 0.12)
                uu = u - dl
                if uu < 0:
                    continue
                px = x + vx * uu; py = y + vy * uu + 900 * uu * uu
                cx, cy = cam_xy(self.cam, t, px, py)
                a = int(235 * max(0.0, 1 - uu / 1.1))
                rr = r.uniform(3, 9) * k_
                if j % 5 == 0:          # a streak of water
                    tx_, ty_ = cam_xy(self.cam, t, px - vx * 0.04, py - (vy + 1800 * uu) * 0.04)
                    d.line((tx_, ty_, cx, cy), fill=(200, 232, 255, a // 2), width=max(2, int(rr)))
                d.ellipse((cx - rr, cy - rr, cx + rr, cy + rr), fill=(210, 238, 255, a))
                d.ellipse((cx - rr * 0.4, cy - rr * 0.6, cx + rr * 0.2, cy - rr * 0.1), fill=(255, 255, 255, a))


def s6():
    T = S0["s6"]
    # A: dawn: the camp of Turan is gone; birds over the fortress (narrator)
    sg = bg("siege_dawn_empty", lambda: abg.siege("dawn", tents=False))
    camA = cam_push(1.0, 1.07, 540, 860, 4.8)
    birds = [(random.Random(600 + k).uniform(-200, 300), 380 + 40 * k, 0.8 + 0.1 * k) for k in range(6)]

    def midA(t):
        o = ""
        for k, (x0, y0, sc) in enumerate(birds):
            x = x0 + 120 * t * sc; y = y0 - 10 * t + 8 * math.sin(t * 2 + k)
            f = 10 * math.sin(t * 9 + k)
            o += f'<path d="M {x - 16 * sc:.1f} {y - f * sc:.1f} Q {x - 7 * sc:.1f} {y - 4:.1f} {x:.1f} {y:.1f} Q {x + 7 * sc:.1f} {y - 4:.1f} {x + 16 * sc:.1f} {y - f * sc:.1f}" stroke="#2a2430" stroke-width="3" fill="none"/>'
        return o
    A = Shot(4.8, sg, midA, cam=camA, light=dict(rim=(0, 0)), sun=(170, 1030, 900, (0.12, 0.08, 0.05)), bloom=0.6, fade_in=0.5,
             fx=[Motes(40, 601, (255, 230, 210), (0, 200, W, 1300), (-8, -4), amax=80)])

    # B: the fortress yard: the boy runs to his mother with bread: "Mother! Bread!" — "Yes, my son. Thanks to Arash."
    T_B = T + 4.8
    LBb = lines_in(T_B, "p3s6b"); LBm = lines_in(T_B, "p3s6c")
    yard = bg("fort_yard_day", lambda: abg.fort_yard("day"), 5)
    camB = cam_push(1.0, 1.05, 540, 900, 6.2)

    def midB(t):
        u = ease(t / 1.2)
        running = t < 1.2
        hug = ease((t - LBm[0][1] - 0.4) / 0.6)
        show = ease((t - 1.0) / 0.4)
        b = tp(LBb, t, 1, turn=-0.3, gx=-0.7, gy=-0.4, smile=0.8, brow=0.6, armL=("ik", lerp(200, 280, show), lerp(240, 110, show)), propL="bread",
               armR="relaxed", legs="walk" if running else "stand", phase=t * 9, wind=0.3)
        bx_ = lerp(1180, 700, u)
        hx_, hy_ = bx_ - 10, 950 - 0.9 * BOY["hs"] * 300
        tgt = ((hx_ - 380) / (0.78 * MOTHER["bs"]), (hy_ - 644) / (0.78 * MOTHER["bs"]))
        m = tp(LBm, t, 2, turn=0.3, gx=0.7, gy=0.6, smile=0.4 + 0.3 * ease((t - 1.0) / 0.5), sad=0.2, brow=0.4,
               armL=("ik", lerp(200, tgt[0], hug), lerp(400, tgt[1], hug), "down") if hug > 0.02 else "chest", openL=hug > 0.5, armR="relaxed", wind=0.2)
        return at_neck(MOTHER, m, t, 380, 644, 0.78) + at_neck(BOY, b, t, bx_, 950, 0.9)
    B = Shot(6.2, yard, midB, cam=camB, light=dict(DAYL, rim=(5, -2)), sun=SUN_DAY, bloom=0.5,
             fx=[Motes(30, 602, (255, 246, 220), (0, 300, W, 1300), (-6, -4), amax=70)])

    # C: Tirgan, today: two pairs of children splash water at each other at the village stream, laughing (narrator)
    T_C = T + 11.0
    tg = bg("tirgan", abg.tirgan)
    camC = cam_push(1.0, 1.05, 540, 1000, 6.6)
    # (spec, x, feet y, scale, facing +1 right / -1 left)
    kids = [(CHILD_A, 150, 1500, 0.66, 1), (CHILD_B, 420, 1540, 0.7, -1), (CHILD_C, 680, 1470, 0.64, 1), (KID, 930, 1530, 0.7, -1)]
    SPL = [s_ - T_C for s_ in A3.SPLASHES]
    THROWER = [0, 3, 2, 1, 0, 3]                   # who throws at each splash (a pair throws at each other in turn)
    UP = lambda sd: ("ik", 320, 40) if sd > 0 else ("ik", -320, 40)
    LOW = lambda sd: ("ik", 260, 360) if sd > 0 else ("ik", -260, 360)
    throws = []
    for ts, k in zip(SPL, THROWER):
        S, x, y, sc, sd = kids[k]
        hx, hy = hand_at(S, UP(sd), sd, x, y, sc)
        throws.append((ts, hx, hy - 20, 330 * sd))

    def midC(t):
        o = ""
        for k, (S, x, y, sc, sd) in enumerate(kids):
            mine = [ts for ts, kk in zip(SPL, THROWER) if kk == k]
            hit = [ts + 0.45 for ts, kk in zip(SPL, THROWER) if (kk ^ 1) == k]          # the other one of the pair is splashed
            sw = max([ease((t - ts + 0.3) / 0.3) * (1 - ease((t - ts - 0.15) / 0.4)) for ts in mine] + [0.0])
            back = max([ease((t - ts + 0.7) / 0.35) * (1 - ease((t - ts + 0.3) / 0.15)) for ts in mine] + [0.0])
            duck = max([ease((t - th + 0.25) / 0.2) * (1 - ease((t - th - 0.4) / 0.4)) for th in hit] + [0.0])
            arm = LOW(sd) if sw < 0.02 else ("ik", lerp(LOW(sd)[1], UP(sd)[1], sw), lerp(LOW(sd)[2], UP(sd)[2], sw))
            if back > 0.02 and sw < 0.02:
                arm = ("ik", LOW(sd)[1] - sd * 120 * back, LOW(sd)[2] + 40 * back)
            guard = ("ik", sd * 150, -200) if duck > 0.3 else "relaxed"
            q = P(turn=0.35 * sd, gx=0.8 * sd, gy=0.0, smile=0.75, brow=0.6 + 0.3 * duck, mouth_o=0.25 + 0.3 * max(0.0, math.sin(t * 8 + k)) + 0.3 * duck,
                  blink=max(blink_at(t, 30 + k), 0.8 * duck), nod=-6 * duck,
                  armL=arm if sd > 0 else guard, armR=arm if sd < 0 else guard, propL="bowl" if sd > 0 else None, propR="bowl" if sd < 0 else None,
                  wind=0.4, breathe=math.sin(t * 3 + k))
            o += at_feet(S, q, t, x + 5 * math.sin(t * 2.3 + k), y - 6 * abs(math.sin(t * 5 + k)) * (0.5 + duck), sc)
        return o
    C = Shot(6.6, tg, midC, cam=camC, light=dict(DAYL, rim=(5, -3)), sun=(900, 300, 900, (0.08, 0.07, 0.04)), bloom=0.5,
             fx=[WaterDrops(camC, throws, seed=7), Motes(30, 603, (255, 250, 230), (0, 300, W, 1300), (-6, -4), amax=60)])

    # D: the girl ties a coloured thread round her little brother's wrist: "Make a wish… and give it to the wind." — "Like Arash?" — "Like Arash."
    T_D = T + 17.6
    LDg = lines_in(T_D, "p3s6e", "p3s6g"); LDk = lines_in(T_D, "p3s6f")
    tgb = bg("tirgan", abg.tirgan, 6)
    camD = cam_push(1.0, 1.06, 560, 880, 6.8)
    KX, KY, KS = 720, 1010, 0.95
    WRIST = ("ik", -380, 110)

    def midD(t):
        tie = ease((t - 0.2) / 0.8)
        up = ease((t - 5.6) / 0.6)
        wr = ("ik", lerp(WRIST[1], -380, up), lerp(WRIST[2], -300, up))
        wx, wy = hand_at(KID, wr, -1, KX, KY, KS, neck=True)
        gx_, gy_ = 400, 900
        k = 1.0 * 0.64        # the girl's scale × bs
        tgt = ((wx - gx_) / (1.0 * GIRL["bs"]), (wy - (gy_ + FEET * GIRL["bs"] * 1.0)) / (1.0 * GIRL["bs"]) + FEET)
        work = 6 * math.sin(t * 7) * (1 - up)
        g = tp(LDg, t, 1, turn=0.3, gx=0.6 if t < 4.6 else 0.7, gy=0.6 if t < 1.4 else 0.1, smile=0.4 + 0.3 * ease((t - 4.6) / 0.6), brow=0.4,
               armL=("ik", tgt[0] - 30 + work, tgt[1] - 10) if up < 0.5 else "relaxed", armR=("ik", tgt[0] + 40 - work, tgt[1] + 20) if up < 0.5 else "relaxed",
               wind=0.5)
        kq = tp(LDk, t, 2, turn=-0.3, gx=-0.7 if t < 5.4 else -0.2, gy=0.5 if t < 2.8 else -0.2 - 0.5 * up, smile=0.3 + 0.5 * ease((t - 4.6) / 0.8),
                brow=0.6, armR=wr, armL="relaxed", wind=0.5)
        o = at_neck(KID, kq, t, KX, KY, KS)
        o += thread_band(wx, wy + 6, KS * KID["bs"] * 1.4, t, ang=-20, flutter=0.4 + up)
        o += at_neck(GIRL, g, t, gx_, gy_, 1.0)
        return o
    D = Shot(6.8, tgb, midD, cam=camD, light=dict(DAYL, rim=(5, -2)), sun=(900, 300, 900, (0.08, 0.07, 0.04)), bloom=0.5)

    # E: over Damavand at dusk, the arrow is still flying (narrator: "And some say… the arrow is still flying."); the end card comes up over it
    dm = bgs.cached("zh_damavand_dusk", lambda: zbg.damavand("dusk"))
    camE = cam_push(1.0, 1.08, 600, 760, 10.6)

    def midE(t):
        u = t / 10.6
        x = lerp(-140, 1240, u); y = lerp(560, 330, u) - 60 * math.sin(math.pi * u)
        return flying_arrow(x, y, lerp(-14, -6, u), 0.17, trail=1.0, glow=1.3)
    E = Shot(10.6, dm, midE, cam=camE, bg_par=1.0, light=dict(rim=(0, 0)), sun=(170, 1030, 900, (0.14, 0.09, 0.05)), bloom=0.7, fade_out=0.8,
             fx=[Motes(40, 604, (255, 230, 200), (0, 200, W, 1300), (-10, -4), amax=80)])
    return [A, B, C, D, E]


SCENES = {"s1": s1, "s2": s2, "s3": s3, "s4": s4, "s5": s5, "s6": s6}
