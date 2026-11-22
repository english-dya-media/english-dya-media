"""Part 9 · Crossing the Arvand — 2D cartoon. Timing matches zahhak/p09_audio.py
(scene starts s1 0, s2 7.4, s3 12.0, s4 35.6, s5 60.0, s6 83.4, s7 106.8; end card 118.6; total 124.0)."""
import math, random
from PIL import Image, ImageFilter, ImageDraw
from film import Shot, W, H, ease, lerp, talk_pose, blink_at, cam_push, cam_static, Motes, Embers, svg_render
from chars import pose, horse, Ctx, FEET, fmt, prop, SKINS, OUT
from stage import at_neck, at_feet, rider, Glow, lw_for, fire_svg, back_heads, random_spec
import bgs, zbg
from cast import *
from p01_scenes import P, bg, cam_xy, tp, darken, fade_to, torch_flame, hall_fx, TORCH, HALL
from p03_scenes import torches_wide, torches_close, night_of
from p05_scenes import hand_at, shake, silhouette, flash, guards_hall, zk_throne
from p07_scenes import kaveh_q, kondrow_at, dust_tex
from p08_scenes import fq, RIVL, SUN_RIV, big_banner
import p09_audio as A9

DUSKP = dict(rim=(-5, -2), rim_col=(1.0, 0.7, 0.5), rim_str=0.9, ramp=(0, W, 1.05, 0.88), ambient=(0.92, 0.84, 0.88))
SUN_DUSKP = (540, 1000, 900, (0.12, 0.06, 0.04))
GOLRANG = dict(col="#c8b48a", mane="#6a5a3a", blanket="#8a1a1a")


def golrang(c, t, walk=False, phase=0.0, head_down=0.0, head_bob=0.0):
    return horse(c, col=GOLRANG["col"], mane=GOLRANG["mane"], walk=walk, phase=phase, t=t, blanket=GOLRANG["blanket"], head_down=head_down,
                 head_bob=head_bob)


def mounted(S, q, t, horse_fn, x, y, s, water=None, flip=True):
    """a rider (horse scale s, ground under the belly at (x, y)); water: the screen y of the river surface — everything below it is
    hidden and a ring of foam is drawn where the horse meets the water"""
    body = rider(S, q, t, horse_fn, x, y, s, flip=flip)
    if water is None:
        return body
    cid = f"wc{abs(hash((round(x), round(y), round(t * 30)))) % 999999}"
    foam = ""
    for k in range(7):
        u = k / 6
        fx_ = x + lerp(-300, 300, u) * s * (-1 if flip else 1)
        foam += (f'<ellipse cx="{fx_:.1f}" cy="{water + 4 * math.sin(t * 6 + k):.1f}" rx="{(60 + 20 * math.sin(t * 4 + k)) * s:.1f}" ry="{12 * s:.1f}" '
                 f'fill="#eef8f8" opacity="0.75"/>')
    return (f'<clipPath id="{cid}"><rect x="-200" y="-400" width="1500" height="{water + 400:.1f}"/></clipPath>'
            f'<g clip-path="url(#{cid})">{body}</g>' + foam)


def mid_river():
    """the middle of the Arvand: sky, the far bank low on the horizon (y ~880), water everywhere below"""
    p = zbg.ARV
    r = random.Random(911)
    s = ("<defs>" + bgs.FILTERS + bgs.lg("msky", p["sky"]) + bgs.lg("mwat", [(0, "#7aa8b4", 1), (1, "#2e5a6a", 1)]) +
         bgs.rg("msun", 860, 640, 520, [(0, "#fff6dc", 0.8), (1, "#ffd8a0", 0)]) + "</defs>")
    s += f'<rect width="{W}" height="{H}" fill="url(#msky)"/>' + bgs.clouds(W, 912, [380, 520, 660], col="#ffffff", hi="#fff6e8", op=0.45)
    s += '<rect width="1080" height="1920" fill="url(#msun)"/><circle cx="860" cy="640" r="40" fill="#fffaf0"/>'
    s += f'<path d="{bgs.hill(W, 860, 50, 913)}" fill="{p["far"]}" opacity="0.8"/>'
    for x, h in ((80, 110), (200, 90), (700, 120), (960, 100)):
        s += zbg.palm(x, 880, h, col=p["palm"], lean=r.uniform(-0.2, 0.2))
    s += f'<rect x="0" y="872" width="{W}" height="14" fill="{p["sand"][1]}"/>'
    s += f'<rect x="0" y="884" width="{W}" height="{H - 884}" fill="url(#mwat)"/>'
    for k in range(160):
        y = r.uniform(890, H); w = r.uniform(20, 140) * (0.4 + (y - 880) / 600)
        x = r.uniform(-60, W)
        s += f'<path d="M {x:.0f} {y:.0f} L {x + w:.0f} {y:.0f}" stroke="#e8f4f4" stroke-width="{1.5 + (y - 880) / 300:.1f}" opacity="{r.uniform(0.2, 0.55):.2f}"/>'
    return svg_render(s)


class Ripples:
    """moving white ripple lines on the water (an fx), drifting left"""
    def __init__(self, seed, n=50, y0=900, y1=H):
        r = random.Random(seed)
        self.p = [(r.uniform(0, W), r.uniform(y0, y1), r.uniform(30, 120), r.uniform(0, 6.3)) for _ in range(n)]

    def __call__(self, im, t):
        d = ImageDraw.Draw(im, "RGBA")
        for x, y, w, ph in self.p:
            sc = 0.5 + (y - 900) / 900
            xx = (x - 60 * t * sc) % (W + 200) - 100
            a = int(120 * (0.5 + 0.5 * math.sin(t * 2 + ph)))
            d.line((xx, y, xx + w * sc, y), fill=(240, 250, 250, a), width=max(1, int(3 * sc)))


# ================================================================ S1 the hook (0-7.4)
def s1():
    riv = bg("arvand", zbg.arvand)
    LA = [("p9s1a", 0.4)]
    camA = cam_push(1.0, 1.05, 560, 1100, 3.4)

    def midA(t):
        go = ease((t - 2.4) / 0.6)
        q = tp(LA, t, 1, turn=-0.4, gx=-0.7, gy=-0.2, furrow=1.0, brow=-0.2, armR="forward",
               armL=("ik", lerp(230, 300, go), lerp(120, -200, go)), propL="mace", wind=0.7)
        k = P(turn=-0.3, gx=-0.6, gy=-0.4, furrow=0.6, brow=0.3, armR="fist_up", propR="kaviani", armL="relaxed", blink=blink_at(t, 2), wind=0.8)
        return (at_feet(KAVEH_NOAPRON, k, t, 880, 1420, 0.27) +
                mounted(FEREYDUN, q, t, lambda c: golrang(c, t, walk=go > 0.1, phase=t * 6, head_bob=-20 * go), 600 - 60 * go, 1450, 0.88))
    A = Shot(3.4, riv, midA, cam=camA, light=RIVL, sun=SUN_RIV, fade_in=0.3)

    # B: Golrang leaps into the river and goes out into the deep water
    camB = cam_push(1.0, 1.06, 540, 1150, 4.0)
    T_IN = A9.PLUNGE - 3.4

    def posB(t):
        u = ease(t / 3.6)
        return lerp(760, 380, u), lerp(1480, 1250, u), lerp(0.84, 0.5, u)

    def midB(t):
        x, y, s = posB(t)
        water = None
        if t > T_IN - 0.2:
            depth = ease((t - T_IN + 0.2) / 0.8) * 300 * s
            water = y - depth
        q = P(turn=-0.4, gx=-0.7, gy=-0.3, furrow=1.2, brow=-0.3, armR="forward", armL=("ik", 300, -200), propL="mace", blink=blink_at(t, 3), wind=0.9)
        o = mounted(FEREYDUN, q, t, lambda c: golrang(c, t, walk=True, phase=t * 7, head_bob=-30 * max(0.0, math.sin(t * 3))), x, y, s, water=water)
        u = (t - T_IN) / 1.2
        if 0 < u < 1:                       # the splash
            for k in range(14):
                a = -math.pi * (0.1 + 0.8 * k / 13)
                v = 260 + 120 * math.sin(k * 2.3)
                px = x + math.cos(a) * v * u * s * 1.4; py = (y - 120 * s) + math.sin(a) * v * u * s * 1.4 + 500 * u * u * s
                o += f'<circle cx="{px:.1f}" cy="{py:.1f}" r="{(16 + 8 * math.sin(k)) * s * (1 - 0.5 * u):.1f}" fill="#f2fbff" opacity="{0.9 * (1 - u):.2f}"/>'
        return o
    B = Shot(4.0, riv, midB, cam=camB, light=RIVL, sun=SUN_RIV, fade_out=0.4)
    return [A, B]


# ================================================================ S2 title (7.4-12.0): Zahhak's palace at dusk
def s2():
    dz = bg("dezh_dusk", lambda: zbg.dezh("dusk"))
    cam = cam_push(1.0, 1.06, 540, 800, 4.6)
    return [Shot(4.6, dz, None, cam=cam, fx=[Motes(40, 921, (255, 220, 190), (0, 200, W, 1300), (-8, -4), amax=90)], sun=SUN_DUSKP,
                 grade="warm", bloom=0.7, fade_in=0.4, fade_out=0.5)]


# ================================================================ S3 the crossing (12.0-35.6)
def s3():
    rivb = bg("arvand", zbg.arvand, 5)
    mid = bgs.cached("zh_p9_mid_river", mid_river)
    riv = bg("arvand", zbg.arvand)
    # A: Fereydun at the water's edge; "Follow me!"
    LA = [("p9s3b", 3.8)]

    def midA(t):
        turn_ = ease((t - 3.5) / 0.4)
        q = fq(LA, t, 1, turn=-0.3 + 0.7 * turn_, gx=-0.7 + 1.5 * turn_, gy=-0.2, furrow=1.0, brow=0.0,
               armL=("ik", 330, -330, "down") if turn_ > 0.5 else "relaxed", propL="mace", armR="relaxed", wind=0.7)
        return at_neck(FEREYDUN, q, t, 480, 960, 0.98)
    A = Shot(6.4, rivb, midA, cam=cam_push(1.0, 1.05, 500, 800, 6.4), light=dict(RIVL, ramp=(0, W, 0.92, 1.06)), sun=SUN_RIV, fade_in=0.3)

    # B: the army swims across (mid-river, from right to left)
    r = random.Random(931)
    riders = [(FEREYDUN, "golrang", 380, 1330, 0.95, 0.0), (KAYANUSH, "#3a2a1e", 760, 1250, 0.8, 1.1), (PURMAYEH, "#5a3a22", 980, 1200, 0.7, 2.0),
              (KAVEH_NOAPRON, "#4a3a32", 620, 1500, 1.05, 0.7)] + \
             [(r.choice((FSOLDIER, FSOLDIER_2, FSOLDIER_3)), r.choice(("#5a3a22", "#3a2a1e", "#6a4a2a", "#2a2a2e")), 1150 + 160 * k, 1120 + 30 * (k % 2),
               0.55 - 0.04 * (k % 2), 3 + k) for k in range(4)]

    def swimmers(t, dx_rate=55, x_off=0):
        o = ""
        for S, col, x0, y0, s, ph in sorted(riders, key=lambda e: e[3]):
            x = x0 + x_off - dx_rate * t
            y = y0 + 8 * math.sin(t * 2.2 + ph)
            water = y - 300 * s + 10 * math.sin(t * 3 + ph)
            hf = (lambda c, t=t, ph=ph: golrang(c, t, walk=True, phase=t * 3 + ph, head_bob=-40)) if col == "golrang" else \
                 (lambda c, t=t, ph=ph, col=col: horse(c, col=col, walk=True, phase=t * 3 + ph, t=t + ph, head_bob=-40))
            if S is KAVEH_NOAPRON:
                q = P(turn=-0.3, gx=-0.6, gy=-0.3, furrow=0.9, brow=0.2, armR="fist_up", propR="kaviani", armL="forward", blink=blink_at(t, 9), wind=0.9)
            elif S is FEREYDUN:
                q = P(turn=-0.4, gx=-0.7, gy=-0.3, furrow=1.0, brow=0.0, armR="forward", armL=("ik", 230, 120), propL="mace", blink=blink_at(t, 8), wind=0.9)
            else:
                q = P(turn=-0.4, gx=-0.7, gy=-0.2, furrow=0.8, brow=0.4, armR="forward", armL="forward", blink=blink_at(t, 10 + ph), wind=0.9)
            o += mounted(S, q, t, hf, x, y, s, water=water)
        return o
    B = Shot(7.4, mid, lambda t: swimmers(t), cam=cam_push(1.0, 1.05, 540, 1100, 7.4), light=RIVL, sun=(860, 640, 900, (0.10, 0.08, 0.04)),
             fx=[Ripples(932)])

    # C: Kaveh in the river, the banner high: "Hold on to your horses!"
    LC = [("p9s3d", 0.2)]
    midw = bgs.cached("zh_p9_mid_river_b5", lambda: mid.filter(ImageFilter.GaussianBlur(5)))

    def midC(t):
        bob = 10 * math.sin(t * 2.2)
        q = kaveh_q(LC, t, 2, turn=0.3, gx=0.8, gy=-0.1, furrow=1.0, brow=0.2, armR=("ik", -300, 60), propR="kaviani", armL="wave" if 0.3 < t < 2.4 else "relaxed",
                    wind=0.9)
        body = at_neck(KAVEH_NOAPRON, q, t, 600, 900 + bob, 0.9)
        wl = 1230 + 8 * math.sin(t * 3)
        cid = "kvw"
        foam = "".join(f'<ellipse cx="{360 + 70 * k:.0f}" cy="{wl + 5 * math.sin(t * 5 + k):.1f}" rx="60" ry="12" fill="#eef8f8" opacity="0.7"/>' for k in range(7))
        water = (f'<path d="M -40 {wl:.1f} ' + " ".join(f"L {x} {wl + 10 * math.sin(t * 3 + x / 90):.1f}" for x in range(0, 1200, 60)) +
                 f' L 1120 1920 L -40 1920 Z" fill="#4a7a8a" opacity="0.92"/>')
        return (f'<clipPath id="{cid}"><rect x="-100" y="-100" width="1300" height="{wl + 100:.1f}"/></clipPath><g clip-path="url(#{cid})">{body}</g>' +
                water + foam)
    C = Shot(3.0, midw, midC, cam=cam_push(1.0, 1.04, 560, 800, 3.0), light=dict(RIVL, ramp=(0, W, 0.94, 1.05)), sun=(860, 640, 900, (0.10, 0.08, 0.04)),
             fx=[Ripples(933, 40, 1240)])

    # D: they come out of the water onto the far bank
    def posD(k, t):
        u = ease((t - 0.3 * k) / 4.6)
        return u

    out_riders = [(FEREYDUN, "golrang", 520, 0.0), (KAVEH_NOAPRON, "#4a3a32", 780, 0.6), (KAYANUSH, "#3a2a1e", 280, 1.0)]

    def midD(t):
        o = ""
        for k, (S, col, x0, ph) in enumerate(sorted(out_riders, key=lambda e: -e[3])):
            u = posD(k, t)
            y = lerp(1250, 1500, u); s = lerp(0.5, 0.82, u); x = x0 + 80 * (1 - u)
            water = y - 300 * s * (1 - ease(u / 0.7)) if u < 0.7 else None
            hf = (lambda c, t=t: golrang(c, t, walk=True, phase=t * 6)) if col == "golrang" else (lambda c, t=t, col=col, ph=ph: horse(c, col=col, walk=True, phase=t * 6 + ph, t=t))
            if S is KAVEH_NOAPRON:
                q = P(turn=-0.3, gx=-0.6, gy=-0.2, furrow=0.6, brow=0.3, smile=0.3 * u, armR="fist_up", propR="kaviani", armL="forward", blink=blink_at(t, 9), wind=0.8)
            elif S is FEREYDUN:
                q = P(turn=-0.4, gx=-0.7, gy=-0.2, furrow=0.6, brow=0.2, smile=0.3 * u, armR="forward", armL=("ik", 230, 120), propL="mace", blink=blink_at(t, 8), wind=0.8)
            else:
                q = P(turn=-0.4, gx=-0.7, gy=-0.2, furrow=0.5, brow=0.4, armR="forward", armL="forward", blink=blink_at(t, 7), wind=0.8)
            o += mounted(S, q, t, hf, x, y, s, water=water)
        return o
    D = Shot(6.8, riv, midD, cam=cam_push(1.0, 1.05, 540, 1150, 6.8), light=RIVL, sun=SUN_RIV, fade_out=0.6)
    return [A, B, C, D]


# ================================================================ S4 the palace; the gate; the talisman; the throne (35.6-60.0)
def sky_dusk():
    s = ("<defs>" + bgs.FILTERS + bgs.lg("sd", [(0, "#2a2050", 1), (0.5, "#7a4a70", 1), (0.8, "#e8906a", 1), (1, "#ffd0a0", 1)]) + "</defs>")
    s += f'<rect width="{W}" height="{H}" fill="url(#sd)"/>' + bgs.clouds(W, 941, [300, 420], col="#f6c8b8", hi="#fff0e0", op=0.5)
    im = svg_render(s)
    im.alpha_composite(bgs.cloud_sea(1350, 942, w=W, hi="#fff0e8", mid="#f0c8c0", lo="#c8a0b0"))
    return im


def talisman_svg(x, y, s, t, crack=0.0, fall=0.0):
    """Zahhak's talisman: a black obelisk with a gold serpent sign and two red eyes, standing on (x, y); crack 0..1 glows its cracks,
    fall 0..1 topples it to the right and down"""
    ang = 95 * ease(fall) ** 1.5
    drop = 700 * max(0.0, fall - 0.5) ** 2 * 4
    eye = "#ff3a2a" if crack < 0.9 else "#6a1a1a"
    o = (f'<g transform="translate({x:.1f},{y + drop:.1f}) rotate({ang:.1f}) scale({s:.3f})">'
         '<path d="M -70 0 L -50 -620 L 0 -700 L 50 -620 L 70 0 Z" fill="#141118" stroke="#000" stroke-width="5"/>'
         '<path d="M -50 -620 L 0 -700 L 10 -640 L -20 -40 L -70 0 Z" fill="#2a2430" opacity="0.8"/>'
         f'<g transform="translate(0,-430) scale(0.9)">{zbg.serpent_emblem(0, 0, 0.9)}</g>'
         f'<circle cx="-16" cy="-560" r="9" fill="{eye}"/><circle cx="16" cy="-560" r="9" fill="{eye}"/>')
    if crack > 0:
        a = min(1.0, crack)
        o += (f'<path d="M -10 -680 L 14 -590 L -12 -500 L 18 -400 L -8 -300 L 20 -180 L -6 -60" stroke="#ffd27a" stroke-width="{6 * a:.1f}" fill="none" opacity="{a:.2f}"/>'
              f'<path d="M 14 -590 L 40 -560 M 18 -400 L -30 -360 M 20 -180 L 46 -150" stroke="#ffd27a" stroke-width="{4 * a:.1f}" fill="none" opacity="{a:.2f}"/>')
    return o + '</g>'


def s4():
    dz = bg("dezh_dusk", lambda: zbg.dezh("dusk"))
    dzb = bg("dezh_dusk", lambda: zbg.dezh("dusk"), 6)
    # A: the black palace above the clouds; the riders small on the road
    def midA(t):
        o = ""
        for k, (S, col, x, y, s) in enumerate(((KAYANUSH, "#3a2a1e", 830, 1560, 0.5), (FEREYDUN, "golrang", 620, 1600, 0.55),
                                               (PURMAYEH, "#5a3a22", 990, 1590, 0.5))):
            q = P(turn=-0.3, gx=-0.5, gy=-0.8, furrow=0.6, brow=0.5, armR="forward", armL=("ik", 230, 120) if S is FEREYDUN else "forward",
                  propL="mace" if S is FEREYDUN else None, blink=blink_at(t, 20 + k), wind=0.6)
            hf = (lambda c, t=t: golrang(c, t, head_down=0.1)) if col == "golrang" else (lambda c, t=t, col=col: horse(c, col=col, t=t))
            o += mounted(S, q, t, hf, x, y, s)
        k = P(turn=-0.3, gx=-0.5, gy=-0.8, furrow=0.5, brow=0.5, armR="fist_up", propR="kaviani", armL="relaxed", blink=blink_at(t, 24), wind=0.7)
        return at_feet(KAVEH_NOAPRON, k, t, 400, 1620, 0.17) + o
    A = Shot(4.8, dz, midA, cam=cam_push(1.0, 1.06, 540, 900, 4.8), light=DUSKP, sun=SUN_DUSKP, fade_in=0.4,
             fx=[Motes(30, 941, (255, 220, 190), (0, 200, W, 1300), (-8, -4), amax=90)])

    # B: "This palace is full of dark magic. But we will not wait."
    LB = [("p9s4b", 0.2)]

    def midB(t):
        q = fq(LB, t, 1, turn=0.1, gx=0.2, gy=-0.7 + 0.6 * ease((t - 2.2) / 0.4), furrow=1.0, brow=0.3, armL="relaxed", armR="relaxed", wind=0.6)
        return at_neck(FEREYDUN, q, t, 540, 960, 0.98)
    B = Shot(4.6, dzb, midB, cam=cam_push(1.0, 1.04, 540, 800, 4.6), light=dict(DUSKP, ramp=(0, W, 1.0, 0.95)), sun=SUN_DUSKP)

    # C: he rides through the gate; the guards step back
    camC = cam_push(1.3, 1.36, 540, 1250, 4.8)

    def midC(t):
        u = ease(t / 4.2)
        x = lerp(1000, 580, u); y = lerp(1560, 1320, u); s = lerp(0.62, 0.34, u)
        o = ""
        for j, gx_ in enumerate((420, 660)):
            back = ease((t - 1.0) / 0.8)
            sd = -1 if gx_ < 540 else 1
            g = P(turn=0.3 * -sd, gx=0.6, gy=0.1, furrow=-0.2, brow=1.0 * back, sad=0.3 * back, armL=(20, 10), propL="pike", armR="relaxed",
                  legs="walk" if 0 < back < 1 else "stand", phase=t * 6, blink=blink_at(t, 30 + j))
            o += at_feet(ZGUARD, g, t, gx_ + sd * 60 * back, 1296, 0.11)
        q = P(turn=-0.3, gx=-0.6, gy=-0.3, furrow=1.0, brow=-0.2, armR="forward", armL=("ik", 300, -200), propL="mace", blink=blink_at(t, 33), wind=0.8)
        return o + mounted(FEREYDUN, q, t, lambda c: golrang(c, t, walk=True, phase=t * 6.5), x, y, s)
    C = Shot(4.8, dz, midC, cam=camC, bg_par=1.0, light=dict(DUSKP, point=(540, 1200, 600, 0.8, 1.15, (1.0, 0.55, 0.25))), sun=SUN_DUSKP,
             fx=[Glow(lambda t: cam_xy(camC, t, 540, 1180), 260, (255, 170, 90), 0.35)])

    # D: the talisman on the tower top cracks and falls
    sky = bgs.cached("zh_p9_sky_dusk", sky_dusk)
    TF = A9.FALL - 49.8
    TC = A9.CRASH - 49.8

    def midD(t):
        crack = ease((t - TF + 1.0) / 0.9)
        fall = ease((t - TF) / (TC - TF)) if t > TF else 0.0
        tower = ('<path d="M 180 1920 L 180 1300 L 900 1300 L 900 1920 Z" fill="#16121a" stroke="#000" stroke-width="4"/>'
                 '<path d="M 180 1300 L 900 1300 L 900 1330 L 180 1330 Z" fill="#2a2430"/>')
        front = ("".join(f'<rect x="{180 + k * 80}" y="1290" width="52" height="70" fill="#16121a" stroke="#000" stroke-width="3"/>' for k in range(9)) +
                 '<path d="M 180 1360 L 900 1360 L 900 1920 L 180 1920 Z" fill="#16121a" stroke="#000" stroke-width="4"/>'
                 '<path d="M 180 1400 L 900 1400" stroke="#c9a24a" stroke-width="8" opacity="0.8"/><rect x="180" y="1360" width="130" height="560" fill="#241e2a" opacity="0.8"/>')
        q = P(turn=0.3, gx=0.7, gy=-0.6, furrow=1.2, brow=-0.2, armL=("ik", 260, -320, "down") if t < TF - 0.6 else ("ik", 380, 120), propL="mace",
              armR="relaxed", blink=blink_at(t, 40), wind=0.9)
        o = tower + at_feet(FEREYDUN, q, t, 360, 1340, 0.46) + talisman_svg(640, 1340, 0.9, t, crack, fall) + front
        u = (t - TC) / 2.0
        if 0 < u < 1:
            for k in range(10):
                a = k / 10 * math.pi
                o += (f'<circle cx="{900 + math.cos(a) * 200 * u * (1.2 if k % 2 else 0.8):.1f}" cy="{1330 - math.sin(a) * 120 * u:.1f}" r="{(40 + 60 * u):.1f}" '
                      f'fill="#8a7a7e" opacity="{0.5 * (1 - u):.2f}"/>')
        return o
    D = Shot(5.4, sky, midD, cam=shake(cam_push(1.0, 1.04, 540, 1000, 5.4), TC, TC + 0.6, 10), light=DUSKP, sun=(540, 1500, 900, (0.12, 0.06, 0.04)),
             fx=[flash(TF - 0.85, 0.35, (255, 240, 200))], bloom=0.7)

    # E: Fereydun on the snake king's throne
    hall = bg("hall", zbg.hall)
    camE = cam_push(1.0, 1.06, 540, 1000, 4.8)

    def midE(t):
        f = tp([], t, 5, legs="sit", turn=0.0, gx=0.0, gy=0.2, furrow=0.6, brow=0.2, armL=("ik", 200, 300), propL="mace", armR="relaxed", wind=0.1, cloak_len=0.6)
        k = P(turn=0.4, gx=0.7, gy=-0.3, furrow=0.3, brow=0.3, smile=0.3, armR="fist_up", propR="kaviani", armL="relaxed", blink=blink_at(t, 50), wind=0.3)
        o = torches_wide(t) + at_neck(FEREYDUN, f, t, 540, 793, 0.36)
        o += at_feet(KAVEH_NOAPRON, k, t, 220, 1560, 0.36)
        for j, (S, x) in enumerate(((KAYANUSH, 790), (PURMAYEH, 920))):
            o += at_feet(S, P(turn=-0.4, gx=-0.7, gy=-0.3, furrow=0.6, brow=0.2, armL="relaxed", armR="relaxed", blink=blink_at(t, 51 + j)), t, x, 1540 + 20 * j, 0.36)
        return o
    E = Shot(4.8, hall, midE, cam=camE, light=HALL, fx=hall_fx(camE, [(80, 640), (1000, 640)], 943), grade="fire", bloom=0.6, fade_out=0.4)
    return [A, B, C, D, E]


# ================================================================ S5 Arnavaz and Shahrnaz (60.0-83.4)
def sisters_q(lines, t, seed, **kw):
    base = dict(turn=0.2, gx=0.5, gy=-0.4, brow=0.6, furrow=-0.3, sad=0.4, armL="relaxed", armR="chest", wind=0.2)
    base.update(kw)
    return tp(lines, t, seed, **base)


def s5():
    hall = bg("hall", zbg.hall)
    hallb = bg("hall", zbg.hall, 6)
    close = bg("hall_close", zbg.hall_close)
    camA = cam_push(1.0, 1.05, 540, 1050, 4.8)

    def midA(t):
        u = ease(min(t, 3.6) / 3.6)
        walking = t < 3.6
        f = tp([], t, 1, legs="sit", turn=0.0, gx=0.5, gy=0.4, furrow=0.3, brow=0.4, armL=("ik", 200, 300), propL="mace", armR="relaxed", wind=0.1, cloak_len=0.6)
        o = torches_wide(t) + at_neck(FEREYDUN, f, t, 540, 793, 0.36)
        for k, (S, x0, x1) in enumerate(((SHAHRNAZ, 1240, 830), (ARNAVAZ, 1120, 690))):
            q = P(legs="walk" if walking else "stand", phase=t * 4.6 + k, turn=-0.35, gx=-0.7, gy=-0.5, brow=0.8, furrow=-0.4, sad=0.5,
                  armL="chest", armR="relaxed", blink=blink_at(t, 2 + k), wind=0.2)
            o += at_feet(S, q, t, lerp(x0, x1, u), 1560 + 20 * k, 0.4)
        return o
    A = Shot(4.8, hall, midA, cam=camA, light=HALL, fx=hall_fx(camA, [(80, 640), (1000, 640)], 951), grade="fire", bloom=0.6, fade_in=0.3)

    LB = [("p9s5b", 0.2)]

    def midB(t):
        return at_neck(ARNAVAZ, sisters_q(LB, t, 3, turn=-0.2, gx=-0.5, gy=-0.4), t, 540, 960, 1.0)
    B = Shot(4.2, hallb, midB, cam=cam_push(1.0, 1.04, 540, 800, 4.2),
             light=dict(TORCH, rim_point=(1500, 6)), fx=hall_fx(cam_push(1.0, 1.04, 540, 800, 4.2), [(1040, 740)], 952), grade="fire", bloom=0.5)

    LC = [("p9s5c", 0.2), ("p9s5d", 3.4)]
    camC = cam_push(1.0, 1.06, 540, 860, 7.4)

    def midC(t):
        grief = ease((t - 3.3) / 0.5)
        q = tp(LC, t, 4, turn=0.15, gx=0.4, gy=0.0, furrow=0.6 + 0.6 * grief, brow=0.2 + 0.4 * grief, sad=0.4 * grief, armL=("ik", 200, 300), propL="mace",
               armR="chest" if t < 3.0 else "relaxed", wind=0.2)
        return torches_close(t) + at_neck(FEREYDUN, q, t, 540, 1030, 1.0)
    C = Shot(7.4, close, midC, cam=camC, light=TORCH, fx=hall_fx(camC, [(40, 740), (1040, 740)], 953), grade="fire", bloom=0.6)

    LD = [("p9s5e", 0.2)]

    def midD(t):
        rel = ease((t - 0.1) / 0.5)
        return at_neck(ARNAVAZ, sisters_q(LD, t, 5, turn=-0.2, gx=-0.5, gy=-0.4, brow=0.6 + 0.6 * rel, sad=0.4 - 0.3 * rel, smile=0.3 * rel,
                                          armR="chest", armL="relaxed"), t, 540, 960, 1.0)
    D = Shot(3.0, hallb, midD, cam=cam_push(1.0, 1.04, 540, 800, 3.0), light=dict(TORCH, rim_point=(1500, 6)), grade="fire", bloom=0.5)

    LE = [("p9s5f", 0.2)]

    def midE(t):
        return at_neck(SHAHRNAZ, sisters_q(LE, t, 6, turn=-0.25, gx=-0.6, gy=-0.3, brow=0.7, sad=0.5, armR="relaxed", armL="chest"), t, 540, 970, 1.0)
    E = Shot(4.0, hallb, midE, cam=cam_push(1.0, 1.04, 540, 800, 4.0), light=dict(TORCH, rim_point=(1500, 6)), grade="fire", bloom=0.5, fade_out=0.3)
    return [A, B, C, D, E]


# ================================================================ S6 Kondrow (83.4-106.8)
def s6():
    hall = bg("hall", zbg.hall)
    hallb = bg("hall", zbg.hall, 6)
    close = bg("hall_close", zbg.hall_close)
    camA = cam_push(1.0, 1.05, 540, 1050, 7.0)

    def midA(t):
        u = ease(min(t, 3.0) / 3.0)
        walking = t < 3.0
        shock = ease((t - 3.0) / 0.4)
        f = tp([], t, 1, legs="sit", turn=0.0, gx=-0.4, gy=0.4, furrow=0.5, brow=0.2, armL=("ik", 200, 300), propL="mace", armR="relaxed", wind=0.1, cloak_len=0.6)
        o = torches_wide(t) + at_neck(FEREYDUN, f, t, 540, 793, 0.36)
        for k, (S, x) in enumerate(((ARNAVAZ, 380), (SHAHRNAZ, 700))):
            q = P(turn=-0.3 if x > 540 else 0.3, gx=-0.6, gy=0.0, brow=0.5, sad=0.2, armL="chest", armR="relaxed", blink=blink_at(t, 3 + k))
            o += at_feet(S, q, t, x, 1250, 0.3)
        kq = P(legs="walk" if walking else "stand", phase=t * 6, turn=0.35 * (1 - shock) - 0.05, gx=0.6 if walking else 0.1, gy=-0.4, brow=0.5 + 0.8 * shock,
               furrow=-0.3 - 0.4 * shock, sad=0.2, armL=("ik", 150, 260, "down"), propL="scroll", armR="relaxed", blink=blink_at(t, 5), wind=0.2)
        o += at_feet(KONDROW, kq, t, lerp(-120, 330, u), 1600, 0.4)
        return o
    A = Shot(7.0, hall, midA, cam=camA, light=HALL, fx=hall_fx(camA, [(80, 640), (1000, 640)], 961), grade="fire", bloom=0.6, fade_in=0.3)

    LB = [("p9s6b", 0.2)]

    def midB(t):
        bow = ease((t - 0.1) / 0.4)
        q = tp(LB, t, 2, turn=0.1, gx=0.3, gy=-0.3 + 0.9 * bow, nod=16 * bow, brow=0.6, furrow=-0.3, smile=0.5, armL="chest", armR="chest", wind=0.2)
        return at_neck(KONDROW, q, t, 540, 960, 1.0)
    B = Shot(2.4, hallb, midB, cam=cam_push(1.0, 1.03, 540, 800, 2.4), light=dict(TORCH, rim_point=(-400, 6)), grade="fire", bloom=0.5)

    LC = [("p9s6c", 0.2)]
    camC = cam_push(1.0, 1.05, 540, 860, 3.8)

    def midC(t):
        q = tp(LC, t, 3, turn=0.0, gx=-0.3, gy=0.2, furrow=0.4, brow=0.2, smile=0.3, armL=("ik", 200, 300), propL="mace", armR="offer" if 0.4 < t < 3.0 else "relaxed",
               wind=0.2)
        return torches_close(t) + at_neck(FEREYDUN, q, t, 540, 1030, 1.0)
    C = Shot(3.8, close, midC, cam=camC, light=TORCH, fx=hall_fx(camC, [(40, 740), (1040, 740)], 962), grade="fire", bloom=0.6)

    LD = [("p9s6d", 0.2)]

    def midD(t):
        bow = ease((t - 0.1) / 0.3) * (1 - ease((t - 1.5) / 0.4))
        sly = ease((t - 1.6) / 0.3)
        q = tp(LD, t, 4, turn=0.1 + 0.3 * sly, gx=0.3 + 0.6 * sly, gy=-0.2 + 0.8 * bow, nod=14 * bow, brow=0.4 - 0.6 * sly, furrow=0.2 + 0.8 * sly,
               smile=0.4 * (1 - sly), armL="chest", armR="chest", wind=0.2)
        return at_neck(KONDROW, q, t, 540, 960, 1.0)
    D = Shot(2.2, hallb, midD, cam=cam_push(1.0, 1.03, 540, 800, 2.2), light=dict(TORCH, rim_point=(-400, 6)), grade="fire", bloom=0.5, fade_out=0.3)

    # E: before dawn Kondrow gallops away from the palace
    dzn = bg("dezh_night", lambda: zbg.dezh("night"))
    camE = cam_push(1.0, 1.05, 540, 1100, 8.0)

    def midE(t):
        u = ease(t / 7.0)
        x = lerp(560, 1180, u); y = lerp(1330, 1720, u); s = lerp(0.3, 0.95, u)
        q = P(turn=0.4, gx=0.8, gy=0.0, furrow=0.8, brow=-0.2, armR="forward", armL="forward", blink=blink_at(t, 6), wind=1.0)
        return mounted(KONDROW, q, t, lambda c: horse(c, col="#2a2a2e", walk=True, phase=t * 9, t=t, head_bob=-20 * abs(math.sin(t * 4.5))), x, y, s, flip=False)
    E = Shot(8.0, dzn, midE, cam=camE, light=dict(ambient=(0.66, 0.68, 0.9), rim=(5, -3), rim_col=(0.75, 0.82, 1.0), rim_str=0.6), grade="night", bloom=0.5,
             fx=[Glow(lambda t: cam_xy(camE, t, 540, 1180), 260, (255, 170, 90), 0.3)], fade_out=0.5)
    return [A, B, C, D, E]


# ================================================================ S7 India: "What?!" (106.8-124.0)
def s7():
    tent = bgs.cached("command_tent", bgs.command_tent)
    tentb = bgs.cached("command_tent_b6", lambda: bgs.cached("command_tent", bgs.command_tent).filter(ImageFilter.GaussianBlur(6)))
    LA = [("p9s7a", 0.8)]
    camA = cam_push(1.0, 1.05, 540, 860, 8.2)
    LAMPT = dict(ambient=(0.78, 0.72, 0.82), rim=(-5, -2), rim_col=(1.0, 0.65, 0.35), rim_str=0.9, ramp=(0, W, 1.05, 0.88))

    def midA(t):
        kneel = ease((t - 0.3) / 0.4)
        k = tp(LA, t, 1, turn=0.35, gx=0.8, gy=-0.4 + 0.2 * kneel, brow=0.9, furrow=-0.5, sad=0.4, nod=6 * kneel, armL="offer" if 2.0 < t < 6.0 else "chest",
               armR="chest", wind=0.2)
        z = tp([], t, 2, turn=-0.3, gx=-0.7, gy=0.5, furrow=0.6 + 0.4 * ease((t - 4.0) / 1.0), brow=-0.1, armL="relaxed", armR="relaxed",
               snake_looks=(0.5 + 0.4 * math.sin(t * 1.3), 0.4 + 0.5 * math.sin(t * 1.1 + 1)),
               hisses=(0.3 * max(0.0, math.sin(t * 1.7)), 0.3 * max(0.0, math.sin(t * 1.5 + 2))))
        return at_neck(ZAHHAK_KING, z, t, 760, 900, 0.86) + at_neck(KONDROW, k, t, lerp(160, 300, kneel), lerp(1000, 1120, kneel), 0.8)
    A = Shot(8.2, tent, midA, cam=camA, light=LAMPT, fx=[Glow(lambda t: cam_xy(camA, t, 290, 780), 200, (255, 170, 90), 0.35)], grade="fire",
             bloom=0.5, fade_in=0.3)

    LB = [("p9s7b", 0.2)]
    camB = cam_push(1.0, 1.12, 540, 860, 9.0)

    def midB(t):
        shock = ease((t - 0.15) / 0.25)
        q = tp(LB, t, 3, turn=0.0, gx=0.0, gy=-0.1, furrow=1.4 - 2.0 * shock, brow=-0.2 + 1.4 * shock, armL="relaxed", armR="relaxed",
               snake_looks=(1.0, 1.0), snake_rise=1.0, hisses=(0.9 * shock * (0.6 + 0.4 * math.sin(t * 5)), 0.9 * shock * (0.6 + 0.4 * math.sin(t * 4 + 1))))
        q["blink"] = min(q["blink"], 0.15)
        q["mouth_o"] = max(q["mouth_o"], 0.5 * shock * (1 - ease((t - 0.9) / 0.5)))
        return at_neck(ZAHHAK_KING, q, t, 540, 1000, 1.0)
    B = Shot(9.0, tentb, midB, cam=shake(camB, 0.2, 0.7, 8), light=LAMPT, grade="fire", bloom=0.6,
             fx=[darken(0.35, 1.0, 9.5, (40, 0, 10))], fade_out=0.6)
    return [A, B]


SCENES = {"s1": s1, "s2": s2, "s3": s3, "s4": s4, "s5": s5, "s6": s6, "s7": s7}
