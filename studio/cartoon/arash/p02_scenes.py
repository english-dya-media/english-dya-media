"""Part 2 · The Bow — 2D cartoon. Timing matches arash/p02_audio.py
(scene starts s1 0, s2 7.8, s3 12.4, s4 48.4, s5 72.0, s6 89.8, s7 105.6, s8 124.8; end card 144.8; total 150.0)."""
import math, random
from PIL import Image, ImageFilter, ImageDraw
from film import Shot, W, H, ease, lerp, talk_pose, blink_at, cam_push, cam_static, Motes, Embers, Snow, svg_render
from chars import pose, horse, Ctx, FEET, fmt, prop
from stage import at_neck, at_feet, rider, Glow, lw_for, fire_svg, back_heads, random_spec, glow_img
import bgs, zbg, abg
from cast import *
from p01_scenes import P, tp, bg, cam_xy, flame, table, DAWNL, DAYL, SUN_DAY, NIGHTL, LAMPL, LAMPC, FIREL
import p02_audio as A2

S0 = A2.S
PREDAWN = dict(ambient=(0.78, 0.76, 0.92), rim=(6, -3), rim_col=(1.0, 0.72, 0.58), rim_str=1.0, ramp=(0, W, 0.86, 1.06))
SUN_PRE = (930, 1110, 900, (0.10, 0.06, 0.05))
SILH = dict(ambient=(0.24, 0.22, 0.32), rim=(6, -3), rim_col=(1.0, 0.76, 0.56), rim_str=1.3)      # a dark shape with a glowing edge
FORGEL = dict(ambient=(0.74, 0.64, 0.64), point=(240, 1010, 900, 0.55, 1.25, (1.0, 0.55, 0.25)), rim_point=(240, 6), rim_col=(1.0, 0.62, 0.3),
              rim_str=1.0)
SPL = dict(ambient=(0.97, 1.04, 0.97), rim=(0, -3), rim_col=(0.72, 1.0, 0.78), rim_str=0.9)
GREENL = (150, 255, 170)
FORESTL = dict(ambient=(0.96, 1.0, 0.94), rim=(-5, -2), rim_col=(1.0, 0.95, 0.75), rim_str=0.8, ramp=(0, W, 0.9, 1.05))
HOMEL = dict(ambient=(0.84, 0.74, 0.74), point=(230, 1240, 900, 0.6, 1.2, (1.0, 0.58, 0.28)), rim_point=(230, 6), rim_col=(1.0, 0.64, 0.32),
             rim_str=0.9)
TORCHL = dict(ambient=(0.62, 0.66, 0.9), rim=(5, -3), rim_col=(1.0, 0.66, 0.38), rim_str=0.85, ramp=(0, W, 1.05, 0.9))


# ---------------------------------------------------------------- helpers
def at(t, t0, d):
    """0..1 ease from t0 over d seconds"""
    return ease((t - t0) / d)


def lines_in(shot_start, *ids):
    """[(line id, start in the shot)] for lines of p02_audio.LINES"""
    d = dict(A2.LINES)
    return [(i, d[i] - shot_start) for i in ids]


def forge_bg(blur=0):
    """the royal smithy at night (abg.forge)"""
    return bg("forge", abg.forge, blur)


def anvil_svg(x, y, s, iron=0.0):
    """an anvil on a tree stump standing on (x, y) (s = the scale of the smith beside it); iron > 0: a glowing arrowhead on it"""
    o = (f'<g transform="translate({x:.1f},{y:.1f}) scale({s:.4f})">'
         f'<path d="M -88 0 L 88 0 L 76 -580 L -76 -580 Z" fill="#5a3a22" stroke="#1b0f0a" stroke-width="5"/>'
         f'<path d="M -50 -60 L -44 -540 M 30 -40 L 36 -550" stroke="#3a2414" stroke-width="5" opacity="0.6"/>'
         f'<ellipse cx="0" cy="-580" rx="78" ry="16" fill="#7a5232" stroke="#1b0f0a" stroke-width="4"/>'
         f'<path d="M -70 -588 L 70 -588 L 50 -640 L 64 -658 L 26 -670 L -26 -670 L -64 -658 L -50 -640 Z" fill="#34343c" stroke="#1b0f0a" stroke-width="5"/>'
         f'<path d="M -120 -670 L 140 -670 L 140 -720 L -60 -720 C -130 -716, -190 -700, -230 -678 C -190 -680, -150 -676, -120 -670 Z" fill="#3e3e48" stroke="#1b0f0a" stroke-width="5"/>'
         f'<path d="M -60 -714 L 134 -714" stroke="#8a8a98" stroke-width="7"/>')
    if iron > 0:
        o += (f'<path d="M -10 -722 L 70 -748 L -10 -774 L 4 -748 Z" fill="#ffb040" stroke="#7a2a0a" stroke-width="4" opacity="{iron:.2f}"/>'
              f'<path d="M 4 -748 L 64 -748" stroke="#fff0b0" stroke-width="6" opacity="{iron:.2f}"/>'
              f'<path d="M -10 -748 L -150 -748" stroke="#2a2a30" stroke-width="10"/>'
              f'<ellipse cx="30" cy="-748" rx="70" ry="30" fill="#ff9a40" opacity="{0.35 * iron:.2f}"/>')
    return o + '</g>'


def hammer_arm(t, hits, up=("ik", -330, -120), down=("ik", -300, 430, "down")):
    """the hammer arm of a smith standing to the right of his anvil: raised between blows, down on each blow (hits in shot time)"""
    nxt = min([h for h in hits if h >= t - 0.1] or [99])
    prev = max([h for h in hits if h < t - 0.1] or [-99])
    u = 1 - ease((nxt - t) / 0.28) if nxt - t < 0.28 else 0.0
    r_ = ease((t - prev - 0.1) / 0.35) if t - prev < 0.45 else 1.0
    k = max(u, 1 - r_) if prev > -99 else u
    arm = ("ik", lerp(up[1], down[1], k), lerp(up[2], down[2], k), "down")
    return arm, lerp(25, -128, k)


def sparks_fx(cam, hits, at_xy, n=16, seed=0):
    """sparks flying from the anvil at each blow (hits in shot time); at_xy: where the hammer meets the iron (scene coordinates)"""
    def fx(im, t):
        d = ImageDraw.Draw(im, "RGBA")
        for k, h in enumerate(hits):
            u = t - h
            if 0 <= u < 0.7:
                r = random.Random(seed * 100 + k)
                for j in range(n):
                    a = r.uniform(-2.9, -0.2); v = r.uniform(260, 560)
                    x = at_xy[0] + math.cos(a) * v * u; y = at_xy[1] + math.sin(a) * v * u + 700 * u * u
                    cx_, cy_ = cam_xy(cam, t, x, y)
                    k_ = cam(t)[0]
                    rr = (3.2 - 3 * u) * k_
                    al = int(255 * (1 - u / 0.7))
                    d.ellipse((cx_ - rr, cy_ - rr, cx_ + rr, cy_ + rr), fill=(255, 220, 120, al))
                    tx, ty = cam_xy(cam, t, x - math.cos(a) * v * 0.03, y - math.sin(a) * v * 0.03)
                    d.line((tx, ty, cx_, cy_), fill=(255, 170, 60, al // 2), width=max(1, int(2 * k_)))
    return fx


def flash_at(cam, hits, at_xy, r=90):
    """a short bright glow where the hammer hits"""
    g = glow_img(r, (255, 210, 120), 0.9)

    def fx(im, t):
        for h in hits:
            u = (t - h) / 0.25
            if 0 <= u < 1:
                x, y = cam_xy(cam, t, *at_xy)
                gg = g.copy(); gg.putalpha(g.getchannel("A").point(lambda v: int(v * (1 - u))))
                im.alpha_composite(gg, (int(x - r), int(y - r)))
    return fx


class FadeGlow:
    """a soft glow whose strength changes with time: afn(t) 0..1"""
    def __init__(self, posfn, r, col, afn):
        self.img = glow_img(r, col, 1.0); self.posfn, self.r, self.afn = posfn, r, afn

    def __call__(self, im, t):
        a = self.afn(t)
        if a <= 0.01:
            return
        x, y = self.posfn(t)
        g = self.img.copy(); g.putalpha(self.img.getchannel("A").point(lambda v: int(v * min(1.0, a))))
        im.alpha_composite(g, (int(x - self.r), int(y - self.r)))


def leaves_of_light(x, y, s, t, a=1.0, n=9, rad=300, seed=0):
    """small leaves of green light circling slowly round (x, y)"""
    o = ""
    for k in range(n):
        ph = k / n * 2 * math.pi + seed
        th = ph + t * 0.6
        rr = rad * s * (0.8 + 0.25 * math.sin(t * 0.9 + k))
        lx, ly = x + math.cos(th) * rr, y + math.sin(th) * rr * 0.55 - 40 * s * math.sin(t * 0.7 + k)
        ang = math.degrees(th) + 90 + 20 * math.sin(t * 2 + k)
        op = a * (0.45 + 0.35 * math.sin(t * 1.7 + k * 1.3))
        sz = s * (1.0 + 0.3 * (k % 3))
        o += (f'<g transform="translate({lx:.1f},{ly:.1f}) rotate({ang:.1f}) scale({sz:.3f})" opacity="{max(0.0, op):.2f}">'
              f'<path d="M 0 -26 C 14 -12, 14 12, 0 26 C -14 12, -14 -12, 0 -26 Z" fill="#c8ffd0"/>'
              f'<path d="M 0 -22 L 0 22" stroke="#7ad88a" stroke-width="2.5"/></g>')
    return o


def sprouts(x, y, s, t, grow, seed=0, n=7, spread=170):
    """little green shoots with white flowers growing from the floor round (x, y)"""
    r = random.Random(seed)
    o = ""
    for k in range(n):
        g = ease(grow * 1.6 - k * 0.09)
        if g <= 0:
            continue
        sx = x + r.uniform(-spread, spread) * s / 0.42; sy = y + r.uniform(-8, 10)
        h = r.uniform(26, 60) * s / 0.42 * g
        lean = r.uniform(-10, 10) + 4 * math.sin(t * 1.5 + k)
        o += (f'<path d="M {sx:.1f} {sy:.1f} q {lean * 0.5:.1f} {-h * 0.5:.1f} {lean:.1f} {-h:.1f}" stroke="#6ad07a" stroke-width="{3.2 * s / 0.42:.1f}" fill="none" stroke-linecap="round"/>'
              f'<ellipse cx="{sx + lean * 0.4 + 7:.1f}" cy="{sy - h * 0.55:.1f}" rx="{8 * s / 0.42 * g:.1f}" ry="{4 * s / 0.42 * g:.1f}" fill="#8ae89a" transform="rotate(-30,{sx + lean * 0.4 + 7:.1f},{sy - h * 0.55:.1f})"/>')
        if k % 2 == 0 and g > 0.8:
            fx_, fy_ = sx + lean, sy - h
            o += (f'<circle cx="{fx_:.1f}" cy="{fy_:.1f}" r="{7 * s / 0.42:.1f}" fill="#ffffff" opacity="0.95"/>'
                  f'<circle cx="{fx_:.1f}" cy="{fy_:.1f}" r="{3 * s / 0.42:.1f}" fill="#ffe07a"/>')
    return o


def spandarmad(t, lines, x, y, s, seed, a=1.0, glow=1.0, **kw):
    """Spandarmad, the guardian of the earth: a woman of soft green light, placed at_neck at (x, y), scale s; a = how much of her is there"""
    if a <= 0.01:
        return ""
    fl = 8 * math.sin(t * 1.2) * s
    base = dict(turn=0.0, gx=0.2, gy=0.0, brow=0.3, furrow=-0.4, smile=0.35, armL="relaxed", armR="relaxed", wind=0.5)
    base.update(kw)
    q = tp(lines, t, seed, **base)
    cy = y + 240 * s + fl
    halo = ('<defs><radialGradient id="spglow" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="#eaffea" stop-opacity="0.55"/>'
            '<stop offset="0.55" stop-color="#b8ffc8" stop-opacity="0.22"/><stop offset="1" stop-color="#9af0b0" stop-opacity="0"/></radialGradient>'
            '<radialGradient id="sphead" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="#ffffff" stop-opacity="0.6"/>'
            '<stop offset="1" stop-color="#d8ffd8" stop-opacity="0"/></radialGradient></defs>'
            f'<ellipse cx="{x:.1f}" cy="{cy:.1f}" rx="{520 * s:.1f}" ry="{980 * s:.1f}" fill="url(#spglow)" opacity="{a * glow:.2f}"/>'
            f'<circle cx="{x:.1f}" cy="{y - 170 * s + fl:.1f}" r="{260 * s:.1f}" fill="url(#sphead)" opacity="{a * glow:.2f}"/>'
            f'<circle cx="{x:.1f}" cy="{y - 170 * s + fl:.1f}" r="{168 * s:.1f}" fill="none" stroke="#c8f8d0" stroke-width="{4 * s:.1f}" opacity="{0.4 * a * glow:.2f}"/>')
    return (f'<g opacity="{a:.3f}">' + halo + at_neck(SPANDARMAD, q, t, x, y + fl, s) + '</g>'
            + leaves_of_light(x, y + 120 * s, s, t, a * glow, seed=seed))


def eagle_svg(x, y, s, t, ang=0.0):
    """a golden eagle soaring, seen from below, flying towards ang (degrees, 0 = right); its middle at (x, y)"""
    flap = 0.12 * math.sin(t * 2.2)
    o = f'<g transform="translate({x:.1f},{y:.1f}) rotate({ang:.1f}) scale({s:.4f})">'
    for sd in (-1, 1):
        tip = 270 * (1 - flap)
        o += (f'<path d="M 34 {-14 * sd} C 30 {-110 * sd}, 10 {-200 * sd}, -14 {-tip * sd:.0f} L -36 {-(tip - 6) * sd:.0f} L -48 {-(tip - 26) * sd:.0f} '
              f'L -60 {-(tip - 52) * sd:.0f} L -70 {-(tip - 82) * sd:.0f} L -74 {-(tip - 114) * sd:.0f} C -70 {-110 * sd}, -54 {-50 * sd}, -40 {-16 * sd} Z" '
              f'fill="#3a2414" stroke="#140a04" stroke-width="5" stroke-linejoin="round"/>'
              f'<path d="M 26 {-30 * sd} C 20 {-110 * sd}, 2 {-180 * sd}, -16 {-(tip - 40) * sd:.0f}" stroke="#6a4424" stroke-width="16" fill="none" opacity="0.8"/>')
    o += ('<path d="M -40 -26 L -132 -44 L -142 0 L -132 44 L -40 26 Z" fill="#4a2e18" stroke="#140a04" stroke-width="5" stroke-linejoin="round"/>'
          '<ellipse cx="0" cy="0" rx="78" ry="30" fill="#4a2e18" stroke="#140a04" stroke-width="5"/>'
          '<ellipse cx="80" cy="0" rx="28" ry="22" fill="#a87a3a" stroke="#140a04" stroke-width="5"/>'
          '<path d="M 104 -8 L 128 0 L 104 10 Z" fill="#e8b830" stroke="#140a04" stroke-width="4"/>')
    return o + '</g>'


def feather_svg(x, y, s, ang):
    """an eagle's feather: brown vane with a pale base, its middle at (x, y)"""
    return (f'<g transform="translate({x:.1f},{y:.1f}) rotate({ang:.1f}) scale({s:.4f})">'
            '<path d="M 0 -120 C 26 -80, 30 30, 6 96 L -6 96 C -24 30, -22 -80, 0 -120 Z" fill="#6a4426" stroke="#1b0f0a" stroke-width="4"/>'
            '<path d="M 6 96 C 14 60, 22 40, 20 20 L -16 20 C -18 40, -12 60, -6 96 Z" fill="#e8dcc8" opacity="0.9"/>'
            '<path d="M -10 -60 L 12 -76 M -14 -20 L 14 -40 M -16 20 L 14 0" stroke="#3a2412" stroke-width="3" opacity="0.6"/>'
            '<path d="M 0 -118 L 0 140" stroke="#d8c8a8" stroke-width="5"/></g>')


def cloak_flying(x, y, s, u, t):
    """Arash's olive cloak taken by the wind: it slides off his back (neck at (x, y), scale s) at u = 0 and flies away up to the left like a
    sail, fluttering; draw it before him (it goes behind his back)"""
    if u <= 0 or u >= 1.0:
        return ""
    k = ease(u)
    cx = x + s * lerp(-60, -1150, k ** 1.1); cy = y + s * lerp(480, -520, k)
    rot = lerp(-8, -95, k) + 10 * math.sin(t * 9)
    sx_ = s * lerp(1.0, 0.8, k) * (1 + 0.16 * math.sin(t * 13)); sy_ = s * lerp(1.0, 0.8, k)
    w1 = 50 * math.sin(t * 15); w2 = 60 * math.sin(t * 11 + 1); w3 = 40 * math.sin(t * 17 + 2)
    op = 1.0 if u < 0.8 else max(0.0, 1 - (u - 0.8) / 0.2)
    outer = (f"M -150 -400 C -50 -430, 50 -430, 150 -400 C {260 + w1:.0f} -200, {330 + w2:.0f} 80, {300 + w2:.0f} 380 "
             f"C {200 + w3:.0f} {330 + w1:.0f}, {100 - w3:.0f} {450 + w2:.0f}, 0 {390 + w3:.0f} C {-100 + w1:.0f} {460 - w3:.0f}, {-220 - w2:.0f} {350 + w1:.0f}, "
             f"{-320 - w1:.0f} 400 C {-330 - w2:.0f} 80, {-270 - w1:.0f} -200, -150 -400 Z")
    inner = (f"M -120 -380 C -40 -400, 40 -400, 120 -380 C {200 + w1:.0f} -200, {250 + w2:.0f} 60, {230 + w2:.0f} 330 "
             f"C {150 + w3:.0f} {300 + w1:.0f}, {80 - w3:.0f} {400 + w2:.0f}, 0 {350 + w3:.0f} C {-80 + w1:.0f} {400 - w3:.0f}, {-170 - w2:.0f} {310 + w1:.0f}, "
             f"{-250 - w1:.0f} 350 C {-260 - w2:.0f} 60, {-210 - w1:.0f} -200, -120 -380 Z")
    return (f'<g transform="translate({cx:.1f},{cy:.1f}) rotate({rot:.1f}) scale({sx_:.4f},{sy_:.4f})" opacity="{op:.2f}">'
            f'<path d="{outer}" fill="#343e22" stroke="#1b0f0a" stroke-width="5"/>'
            f'<path d="{inner}" fill="#4e5a36"/>'
            f'<path d="M 100 -380 C 170 -150, {200 + w2 * 0.5:.0f} 100, {210 + w2 * 0.6:.0f} 320" stroke="#6e7a4e" stroke-width="18" fill="none" opacity="0.6"/>'
            f'<path d="M -60 -390 C -90 -120, {-120 + w1 * 0.4:.0f} 120, {-140 + w1 * 0.5:.0f} 340" stroke="#2a3218" stroke-width="12" fill="none" opacity="0.5"/>'
            f'<circle cx="-112" cy="-392" r="18" fill="#b9832f" stroke="#1b0f0a" stroke-width="3"/><circle cx="112" cy="-392" r="18" fill="#b9832f" stroke="#1b0f0a" stroke-width="3"/>'
            '</g>')


def torch_pole(x, y, h, t, s=1.0, seed=0):
    """a torch on a pole planted in the ground at (x, y)"""
    return (f'<path d="M {x - 5 * s:.1f} {y:.1f} L {x - 4 * s:.1f} {y - h:.1f} L {x + 4 * s:.1f} {y - h:.1f} L {x + 5 * s:.1f} {y:.1f} Z" fill="#3a2614" stroke="#120a06" stroke-width="{2 * s:.1f}"/>'
            f'<path d="M {x - 12 * s:.1f} {y - h:.1f} L {x + 12 * s:.1f} {y - h:.1f} L {x + 9 * s:.1f} {y - h + 16 * s:.1f} L {x - 9 * s:.1f} {y - h + 16 * s:.1f} Z" fill="#2a1e14"/>'
            f'<circle cx="{x:.1f}" cy="{y - h - 30 * s:.1f}" r="{60 * s:.1f}" fill="#ffa050" opacity="0.25"/>'
            + flame(x, y - h + 2 * s, t, 0.32 * s, seed))


def snow_wind(seed, n=190, wind=-520):
    return Snow(n, seed, wind, (30, 110), (1.2, 3.4), (90, 200))


# ================================================================ S1 the hook (0-7.8): sparks at the anvil; the man on the summit
FORGE_AT = (470, 1300, 0.46)          # the anvil: feet (x, y) and the scale of the smith beside it
SMITH_AT = (618, 1286)


def smith_at_work(t, hits, iron=1.0, lines=(), seed=0, **kw):
    ax, ay, sk = FORGE_AT
    arm, ang = hammer_arm(t, hits)
    base = dict(turn=-0.35, gx=-0.7, gy=0.7, furrow=0.7, brow=0.0, armR=arm, propR=("hammer", ang), armL=("ik", -150, 330, "down"), wind=0.1)
    base.update(kw)
    q = tp(list(lines), t, seed, **base)
    return anvil_svg(ax, ay, sk, iron) + at_feet(SMITH, q, t, SMITH_AT[0], SMITH_AT[1], sk)


def s1():
    fg = forge_bg()
    hits = A2.HOOK_STRIKES
    camA = cam_push(1.5, 1.6, 470, 960, 4.2)
    hit_xy = (FORGE_AT[0] + 10, FORGE_AT[1] - 720 * FORGE_AT[2] - 20)
    A = Shot(4.2, fg, lambda t: smith_at_work(t, hits), cam=camA, bg_par=1.0, light=FORGEL, grade="fire", bloom=0.7, fade_in=0.3,
             fx=[Glow(lambda t: cam_xy(camA, t, *abg.FORGE_FIRE), 380, (255, 150, 70), 0.3), flash_at(camA, hits, hit_xy), sparks_fx(camA, hits, hit_xy),
                 Embers(30, 101, (60, 700, 420, 1000), (60, 150))])

    # B: Arash on the summit before sunrise, a dark shape against the glow, his cloak in the wind
    sm = bg("summit_predawn", lambda: abg.summit("predawn"))
    camB = cam_push(1.15, 1.25, 600, 1150, 3.6)

    def midB(t):
        q = P(turn=0.35, gx=0.9, gy=-0.2, furrow=0.2, armL=("ik", 340, 220, "down"), propL="bow", armR="relaxed", wind=1.2, blink=blink_at(t, 3),
              breathe=math.sin(t * 1.8))
        return at_feet(ARASH, q, t, 600, abg.summit_y(600), 0.5)
    B = Shot(3.6, sm, midB, cam=camB, bg_par=1.0, light=SILH, sun=SUN_PRE, bloom=0.7, fade_out=0.5,
             fx=[snow_wind(102), Motes(30, 103, (255, 220, 200), (0, 300, W, 1300), (-30, -2), amax=90)])
    return [A, B]


# ================================================================ S2 title (7.8-12.4): the besieged fortress at night
def s2():
    sg = bg("siege_night", lambda: abg.siege("night"))
    return [Shot(4.6, sg, None, cam=cam_push(1.0, 1.06, 540, 800, 4.6), grade="night",
                 fx=[Motes(30, 201, (255, 220, 170), (0, 900, W, 1300), (-4, -6), amax=70)], bloom=0.6, fade_in=0.4, fade_out=0.5)]


# ================================================================ S3 the king can't sleep; Spandarmad (12.4-48.4)
def s3():
    T = S0["s3"]
    room = bgs.cached("war_room", bgs.war_room)
    roomb = bgs.cached("war_room_b7", lambda: bgs.cached("war_room", bgs.war_room).filter(ImageFilter.GaussianBlur(7)))
    roomd = bgs.cached("ar_war_room_dark_b8", lambda: Image.alpha_composite(bgs.cached("war_room", bgs.war_room).filter(ImageFilter.GaussianBlur(8)),
                                                                            Image.new("RGBA", (W, H), (6, 14, 16, 150))))
    lamp = lambda cam: Glow(lambda t: cam_xy(cam, t, 540, 520), 260, (255, 170, 90), 0.4)

    # A: wide: the king alone at the table in the night (narrator)
    LA = lines_in(T, "p2s3a")
    camA = cam_push(1.0, 1.05, 540, 1000, 4.6)

    def midA(t):
        sigh = ease((t - 2.2) / 0.6) * (1 - ease((t - 3.6) / 0.6))
        m = P(turn=0.1, gx=0.2, gy=0.9, sad=0.6, brow=0.6, furrow=0.3, nod=6 + 6 * sigh, armL=("ik", 220, 520), armR=("ik", -220, 520),
              blink=blink_at(t, 1), breathe=math.sin(t * 1.4), wind=0.1, cloak_len=0.9)
        return at_feet(MANUCHEHR, m, t, 540, 1560, 0.42) + table(1330)
    A = Shot(4.6, room, midA, cam=camA, light=LAMPL, grade="fire", bloom=0.6, fade_in=0.4, fx=[lamp(camA)])

    # B: close: "No bow in Iran can shoot that far…"
    LB = lines_in(T + 4.6, "p2s3b")
    camB = cam_push(1.0, 1.05, 540, 860, 3.8)

    def midB(t):
        q = tp(LB, t, 2, turn=0.1, gx=0.3 - 0.6 * ease((t - 1.6) / 0.8), gy=0.6, sad=0.6, brow=0.6, furrow=0.3, armL="relaxed", armR="relaxed", wind=0.1)
        return at_neck(MANUCHEHR, q, t, 540, 960, 1.0)
    B = Shot(3.8, roomb, midB, cam=camB, light=LAMPC, grade="fire", bloom=0.5)

    # C: a green light grows at the left; he turns: "Who is there?"
    T_C = T + 8.4
    LC = lines_in(T_C, "p2s3c")
    camC = cam_push(1.0, 1.04, 540, 860, 2.8)
    g0 = A2.GREEN - T_C

    def midC(t):
        look = ease((t - g0 - 0.6) / 0.5)
        q = tp(LC, t, 3, turn=0.2 - 0.6 * look, gx=0.3 - 1.2 * look, gy=0.4 - 0.4 * look, sad=0.3 * (1 - look), brow=0.6 + 0.4 * look,
               furrow=0.3 - 0.6 * look, armL="relaxed", armR="relaxed", wind=0.1)
        return at_neck(MANUCHEHR, q, t, 580, 960, 1.0)
    C = Shot(2.8, roomb, midC, cam=camC, light=dict(LAMPC, rim=(-6, -2), rim_col=(0.62, 1.0, 0.7), ramp=(0, W, 1.08, 0.84)), grade="fire", bloom=0.6,
             fx=[FadeGlow(lambda t: (40, 760), 520, GREENL, lambda t: 0.65 * ease((t - g0) / 1.8))])

    # D: wide: Spandarmad appears in a column of green light at the left; shoots grow from the stone floor; the king steps back
    T_D = T + 11.2
    LD = lines_in(T_D, "p2s3d")
    camD = cam_push(1.0, 1.05, 540, 1050, 4.4)
    ap = A2.APPEAR - T_D

    def midD(t):
        a = ease((t - ap) / 1.1)
        back = ease((t - ap - 0.3) / 0.8)
        m = P(turn=-0.3, gx=-0.9, gy=0.0, brow=1.0, furrow=-0.6, sad=0.0, armL="relaxed", armR=("ik", -260, 120) if back > 0.5 else "relaxed",
              openR=True, blink=blink_at(t, 4), breathe=math.sin(t * 2.4), wind=0.1)
        sp = spandarmad(t, LD, 330, 1560 - FEET * 0.42, 0.42, 5, a=a, armL="relaxed", armR="relaxed")
        return (sp + sprouts(330, 1562, 0.42, t, ease((t - ap - 0.4) / 2.0), seed=6)
                + at_feet(MANUCHEHR, m, t, lerp(760, 820, back), 1560, 0.42))
    D = Shot(4.4, room, midD, cam=camD, light=dict(ambient=(0.8, 0.86, 0.86), point=(330, 1100, 900, 0.8, 1.12, (0.45, 0.9, 0.55)), rim=(-6, -2),
                                                    rim_col=(0.62, 1.0, 0.7), rim_str=0.9),
             grade="night", bloom=0.6, fx=[FadeGlow(lambda t: cam_xy(camD, t, 330, 1120), 560, GREENL, lambda t: 0.5 * ease((t - ap) / 1.1)), lamp(camD),
                                            Motes(40, 301, (200, 255, 210), (150, 600, 520, 1560), (2, -30), amax=150)])

    # E: Spandarmad close: "I am Spandarmad, the guardian of this earth."
    T_E = T + 15.6
    LE = lines_in(T_E, "p2s3e")
    camE = cam_push(1.0, 1.05, 540, 860, 3.8)

    def midE(t):
        return spandarmad(t, LE, 540, 980, 0.95, 7, armL="chest", armR="relaxed", gx=0.0, gy=0.1)
    E = Shot(3.8, roomd, midE, cam=camE, light=SPL, grade="night", bloom=0.9,
             fx=[Glow(lambda t: cam_xy(camE, t, 540, 820), 520, GREENL, 0.32), Motes(50, 302, (200, 255, 210), (0, 300, W, 1400), (3, -24), amax=150)])

    # F: Spandarmad tells how the bow and arrow must be made: the oldest tree; an eagle's feathers
    T_F = T + 19.4
    LF = lines_in(T_F, "p2s3f", "p2s3g")
    camF = cam_push(1.0, 1.06, 540, 900, 5.8)
    g_ = LF[1][1]

    def midF(t):
        offer = ease((t - 0.4) / 0.5) * (1 - ease((t - g_ + 0.4) / 0.4))
        wing = ease((t - g_ - 0.1) / 0.7)
        armR = ("ik", lerp(-200, -470, max(offer, wing)), lerp(470, 170, max(offer, wing)), "down")
        armL = ("ik", lerp(200, 470, wing), lerp(470, 170, wing), "down")
        return spandarmad(t, LF, 540, 1000, 0.72, 8, armR=armR, openR=max(offer, wing) > 0.5, armL=armL, openL=wing > 0.5,
                          gx=-0.4 * offer + 0.2 * (1 - offer), gy=0.0)
    F = Shot(5.8, roomd, midF, cam=camF, light=SPL, grade="night", bloom=0.9,
             fx=[Glow(lambda t: cam_xy(camF, t, 540, 900), 560, GREENL, 0.3), Motes(50, 303, (200, 255, 210), (0, 300, W, 1400), (3, -24), amax=150)])

    # G: the king listens (her voice: "And make the point from the finest iron.") and asks: "And who will shoot it?"
    T_G = T + 25.2
    LG = lines_in(T_G, "p2s3i")
    camG = cam_push(1.0, 1.06, 540, 860, 6.2)

    def midG(t):
        nodk = ease((t - 2.8) / 0.4) * (1 - ease((t - 3.3) / 0.4))
        q = tp(LG, t, 9, turn=-0.25, gx=-0.7, gy=0.0, brow=0.8 - 0.3 * ease((t - 3.4) / 1.0), furrow=-0.4, sad=0.1, nod=10 * nodk, armL="relaxed",
               armR="relaxed", wind=0.1)
        return at_neck(MANUCHEHR, q, t, 560, 960, 1.0)
    G = Shot(6.2, roomb, midG, cam=camG, light=dict(LAMPC, rim=(-6, -2), rim_col=(0.62, 1.0, 0.7), ramp=(0, W, 1.1, 0.82)), grade="night", bloom=0.6,
             fx=[Glow(lambda t: (30, 760), 520, GREENL, 0.5)])

    # H: "He has already stepped forward." She smiles and fades into green light; the lamp is the only light again
    T_H = T + 31.4
    LH = lines_in(T_H, "p2s3j")
    camH = cam_push(1.0, 1.05, 540, 900, 4.6)
    v0 = A2.VANISH - T_H

    def midH(t):
        a = 1 - ease((t - v0) / 1.3)
        return spandarmad(t, LH, 540, 1000, 0.72, 10, a=a, armL="chest", armR="relaxed", smile=0.5, gx=0.2, gy=0.1)

    def rise(im, t):
        a = ease((t - v0) / 0.6) * (1 - ease((t - v0 - 1.6) / 0.8))
        if a > 0:
            Motes(70, 304, (210, 255, 220), (300, 400, 780, 1400), (0, -90), size=(1.6, 4.0), amax=int(220 * a))(im, t)
    I = Shot(4.6, roomd, midH, cam=camH, light=SPL, grade="night", bloom=0.9, fade_out=0.5,
             fx=[FadeGlow(lambda t: cam_xy(camH, t, 540, 900), 560, GREENL, lambda t: 0.3 * (1 - ease((t - v0) / 1.3))), rise])
    return [A, B, C, D, E, F, G, I]



# ================================================================ S4 the craftsmen (48.4-72.0): the old tree; the eagle's feather; the iron; the bow
def s4():
    T = S0["s4"]
    forest = bg("old_forest", abg.old_forest)
    forestb = bg("old_forest", abg.old_forest, 8)
    rays = lambda seed: Motes(50, seed, (255, 246, 210), (300, 300, W, 1500), (-10, 6), size=(1.2, 3.0), amax=140)

    # A: the old forest; the bowyer walks to the oldest tree (narrator: "For days and nights…")
    LA = lines_in(T, "p2s4a")
    camA = cam_push(1.0, 1.06, 540, 1100, 5.4)
    WALK = (0.0, 4.2)

    def midA(t):
        u = ease((t - WALK[0]) / (WALK[1] - WALK[0]))
        walking = t < WALK[1]
        up = ease((t - 4.3) / 0.8)
        q = P(turn=-0.35, gx=-0.8, gy=-0.6 * up, brow=0.4 * up, furrow=0.1, smile=0.2 * up, legs="walk" if walking else "stand", phase=t * 4.6,
              armR="relaxed", propR="stick", armL="relaxed", blink=blink_at(t, 1), wind=0.3)
        return at_feet(BOWYER, q, t, lerp(1010, 650, u), 1500, 0.42)
    A = Shot(5.4, forest, midA, cam=camA, light=FORESTL, bloom=0.6, fade_in=0.4, fx=[rays(401)])

    # B: he lays his hand on the bark: "This tree is older than any king."
    T_B = T + 5.4
    LB = lines_in(T_B, "p2s4b")
    camB = cam_push(1.0, 1.04, 520, 900, 3.2)

    def midB(t):
        reach = ease((t - 0.1) / 0.6)
        q = tp(LB, t, 2, turn=-0.3, gx=-0.6, gy=-0.4, brow=0.5, furrow=-0.2, smile=0.3,
               armR=("ik", lerp(-200, -430, reach), lerp(420, 40, reach), "down"), openR=reach > 0.6, armL="relaxed", wind=0.2)
        return at_neck(BOWYER, q, t, 700, 880, 0.85)
    B = Shot(3.2, forest, midB, cam=camB, light=FORESTL, bloom=0.6, fx=[rays(402)])

    # C: an eagle circles high over Tabaristan; one feather falls
    day = bg("siege_day", lambda: abg.siege("day"))
    camC = cam_push(1.0, 1.05, 540, 760, 4.0)
    DROP = 1.3

    def eagle_pos(t):
        th = 2.4 - 0.55 * t
        x, y = 540 + 290 * math.cos(th), 380 + 70 * math.sin(th)
        dx, dy = 290 * math.sin(th), -70 * math.cos(th)             # direction of travel (th decreasing)
        return x, y, math.degrees(math.atan2(dy, dx))

    def feather_pos(t):
        ex, ey, _ = eagle_pos(DROP)
        u = t - DROP
        return ex + 70 * math.sin(u * 2.2) + 30 * u, ey + 175 * u, 30 * math.sin(u * 2.2 + 0.6)

    def midC(t):
        x, y, ang = eagle_pos(t)
        o = eagle_svg(x, y, 0.42, t, ang)
        if t > DROP:
            fx_, fy_, fa = feather_pos(t)
            o += feather_svg(fx_, fy_, 0.45, fa)
        return o
    C = Shot(4.0, day, midC, cam=camC, light=dict(DAYL, rim=(0, -3)), sun=SUN_DAY, fx=[Motes(20, 403, (255, 250, 230), (0, 200, W, 1000), (-8, 0), amax=60)])

    # D: the feather comes down into the bowyer's open hand; he smiles
    T_D = T + 12.6
    camD = cam_push(1.0, 1.04, 540, 860, 2.2)
    land = A2.CATCH - T_D
    HAND = (520 + 260 * 0.95, 900 - 30 * 0.95)

    def midD(t):
        u = ease(t / land) if t < land else 1.0
        fx_ = lerp(HAND[0] - 160, HAND[0] - 20, u) + (0 if t >= land else 50 * math.sin(t * 3))
        fy_ = lerp(320, HAND[1] - 95, u)
        fa = lerp(40, 78, u) + (0 if t >= land else 20 * math.sin(t * 4))
        smile = ease((t - land) / 0.5)
        q = P(turn=0.25, gx=0.7, gy=0.5 - 0.6 * (1 - u), brow=0.4, furrow=-0.2, smile=0.5 * smile, armL=("ik", 260, -30, "down"), openL=True, armR="relaxed",
              blink=blink_at(t, 7), breathe=math.sin(t * 2), wind=0.2)
        return at_neck(BOWYER, q, t, 520, 900, 0.95) + feather_svg(fx_, fy_, 0.68, fa)
    D = Shot(2.2, forestb, midD, cam=camD, light=FORESTL, bloom=0.6, fx=[rays(404)])

    # E: the smith at the anvil: "The finest iron… for one arrow."
    T_E = T + 14.8
    hits = [h - T_E for h in A2.FORGE_STRIKES]
    LE = lines_in(T_E, "p2s4c")
    camE = cam_push(1.15, 1.22, 470, 1000, 4.2)
    hit_xy = (FORGE_AT[0] + 10, FORGE_AT[1] - 720 * FORGE_AT[2] - 20)

    def midE(t):
        talking = LE[0][1] - 0.2 < t < LE[0][1] + 2.8
        return smith_at_work(t, hits, lines=LE, seed=5, gy=0.7 if not talking else 0.3, gx=-0.7 if not talking else -0.3, furrow=0.6, smile=0.15 * talking)
    E = Shot(4.2, forge_bg(), midE, cam=camE, bg_par=1.0, light=FORGEL, grade="fire", bloom=0.7,
             fx=[Glow(lambda t: cam_xy(camE, t, *abg.FORGE_FIRE), 380, (255, 150, 70), 0.3), flash_at(camE, hits, hit_xy), sparks_fx(camE, hits, hit_xy, seed=4),
                 Embers(26, 405, (60, 700, 420, 1000), (60, 150))])

    # F: the bowyer holds up the finished bow and plucks the string: "It is ready. But who can draw a bow like this?"
    T_F = T + 19.0
    LF = lines_in(T_F, "p2s4d")
    pl = A2.PLUCK - T_F
    camF = cam_push(1.0, 1.05, 540, 860, 4.6)

    def midF(t):
        reach = ease((t - pl + 0.5) / 0.4) * (1 - ease((t - pl - 0.2) / 0.5))
        q = tp(LF, t, 6, turn=0.25, gx=0.8, gy=-0.5, brow=0.6, furrow=-0.1, smile=0.2, armL=("ik", 330, -20, "down"), propL="bow",
               armR=("ik", lerp(-120, 330, reach), lerp(420, -140, reach)) if reach > 0.02 else "relaxed", wind=0.1)
        o = at_neck(BOWYER, q, t, 470, 900, 0.8)
        if 0 <= t - pl < 0.8:          # the string still shaking
            a = 1 - (t - pl) / 0.8
            sx = 470 + (330 + 40) * 0.8
            o += f'<path d="M {sx:.1f} {900 - 16 - 280} Q {sx + 14 * a * math.sin(t * 90):.1f} {900 - 16} {sx:.1f} {900 - 16 + 280}" stroke="#fff6d8" stroke-width="3" fill="none" opacity="{0.8 * a:.2f}"/>'
        return o
    F = Shot(4.6, forge_bg(7), midF, cam=camF, light=dict(FORGEL, point=(60, 1000, 1100, 0.6, 1.2, (1.0, 0.55, 0.25)), rim_point=None, rim=(-6, -2),
                                                         rim_col=(1.0, 0.62, 0.3)),
             grade="fire", bloom=0.6, fade_out=0.4, fx=[Glow(lambda t: (60, 1000), 420, (255, 150, 70), 0.35)])
    return [A, B, C, D, E, F]


# ================================================================ S5 the bow is given to Arash (72.0-89.8)
def bow_on_table(x, y, s, t):
    c = Ctx(lw_for(s))
    return f'<g transform="translate({x:.1f},{y:.1f}) rotate(90) scale({s:.4f})">{prop(c, "bow", 0, 0, 0, t)}</g>'


def s5():
    T = S0["s5"]
    room = bgs.cached("war_room", bgs.war_room)
    roomb = bgs.cached("war_room_b7", lambda: bgs.cached("war_room", bgs.war_room).filter(ImageFilter.GaussianBlur(7)))
    lamp = lambda cam: Glow(lambda t: cam_xy(cam, t, 540, 520), 260, (255, 170, 90), 0.4)

    # A: the bow lies on the table; Arash comes in; "Arash. This bow is yours."
    LA = lines_in(T, "p2s5a")
    camA = cam_push(1.0, 1.05, 540, 1050, 3.8)
    e0, e1 = A2.ENTER - T, A2.ENTER - T + 1.6

    def midA(t):
        u = ease((t - e0) / (e1 - e0))
        walking = e0 < t < e1
        a = P(turn=0.3, gx=0.6, gy=0.2 + 0.5 * ease((t - 2.4) / 0.5), brow=0.3, furrow=0.2, legs="walk" if walking else "stand", phase=t * 5.2,
              armL="relaxed", armR="relaxed", blink=blink_at(t, 1), wind=0.2)
        m = tp(LA, t, 2, turn=-0.35, gx=-0.8, gy=0.1, sad=0.3, brow=0.4, furrow=0.2, armR="offer" if 1.0 < t < 3.2 else "relaxed", armL="relaxed",
               wind=0.1, cloak_len=0.9)
        return (at_feet(ARASH, a, t, lerp(-80, 290, u), 1560, 0.42) + at_feet(MANUCHEHR, m, t, 790, 1560, 0.42) + table(1330)
                + bow_on_table(540, 1352, 0.42, t))
    A = Shot(3.8, room, midA, cam=camA, light=LAMPL, grade="fire", bloom=0.6, fade_in=0.3, fx=[lamp(camA)])

    # B: the king: "You know what this shot will cost you."
    T_B = T + 3.8
    LB = lines_in(T_B, "p2s5b")
    camB = cam_push(1.0, 1.05, 540, 860, 3.2)

    def midB(t):
        q = tp(LB, t, 3, turn=-0.2, gx=-0.6, gy=0.1, sad=0.6, brow=0.7, furrow=-0.2, armL="relaxed", armR="relaxed", wind=0.1)
        return at_neck(MANUCHEHR, q, t, 560, 960, 1.0)
    B = Shot(3.2, roomb, midB, cam=camB, light=dict(LAMPC, rim=(5, -2), ramp=(0, W, 0.86, 1.06)), grade="fire", bloom=0.5)

    # C: Arash with the bow: "I have seen the children in our streets, my king." … "They are hungry. And I am an archer."
    T_C = T + 7.0
    LC = lines_in(T_C, "p2s5c", "p2s5d")
    camC = cam_push(1.0, 1.08, 540, 860, 7.4)
    t2 = LC[1][1]

    def midC(t):
        look = ease((t - t2 - 1.2) / 0.4) * (1 - ease((t - t2 - 2.4) / 0.4))
        q = tp(LC, t, 4, turn=0.2, gx=0.5 + 0.4 * look, gy=0.1 + 0.6 * look, brow=0.3, furrow=0.2, sad=0.2 * ease((t - 0.5) / 1.0) * (1 - look),
               armL=("ik", 340, 220, "down"), propL="bow", armR="relaxed", wind=0.2)
        return at_neck(ARASH, q, t, 520, 960, 1.0)
    C = Shot(7.4, roomb, midC, cam=camC, light=LAMPC, grade="fire", bloom=0.5)

    # D: the king, moved: "Iran will never forget your name."
    T_D = T + 14.4
    LD = lines_in(T_D, "p2s5e")
    camD = cam_push(1.0, 1.05, 540, 860, 3.4)

    def midD(t):
        q = tp(LD, t, 5, turn=-0.2, gx=-0.6, gy=0.0, sad=0.4, brow=0.6, furrow=-0.3, smile=0.2, armR="chest" if t > 0.3 else "relaxed", armL="relaxed",
               wind=0.1)
        return at_neck(MANUCHEHR, q, t, 560, 960, 1.0)
    D = Shot(3.4, roomb, midD, cam=camD, light=dict(LAMPC, rim=(5, -2), ramp=(0, W, 0.86, 1.06)), grade="fire", bloom=0.5, fade_out=0.4)
    return [A, B, C, D]


# ================================================================ S6 his mother (89.8-105.6)
def open_door(u, t):
    """the door of the house at the right of bgs.interior opening onto the night (u 0..1)"""
    if u <= 0:
        return ""
    x0, x1, y0, y1 = 772, 1012, 736, 1398
    w = (x1 - x0) * (1 - 0.82 * u)
    return (f'<rect x="{x0}" y="{y0}" width="{x1 - x0}" height="{y1 - y0}" fill="#0c1430"/>'
            f'<circle cx="{x0 + 60}" cy="{y0 + 90}" r="3" fill="#ffffff"/><circle cx="{x0 + 170}" cy="{y0 + 160}" r="2" fill="#dfe6ff"/>'
            f'<path d="M {x0} {y1} L {x1} {y1} L {x1} {y1 - 40} L {x0} {y1 - 60} Z" fill="#1c2238"/>'
            f'<path d="M {x1} {y0} L {x1 - w:.1f} {y0 + 20 * u:.1f} L {x1 - w:.1f} {y1 + 6 * u:.1f} L {x1} {y1} Z" fill="#5a3a22" stroke="#1b0f0a" stroke-width="4"/>')


def s6():
    T = S0["s6"]
    home = bgs.cached("interior", bgs.interior)
    homeb = bgs.cached("interior_b8", lambda: bgs.cached("interior", bgs.interior).filter(ImageFilter.GaussianBlur(8)))
    fire = lambda t: fire_svg(230, 1300, 62, t)
    WARMC = dict(rim=(-6, -2), rim_col=(1.0, 0.66, 0.38), rim_str=0.9, ramp=(0, W, 1.08, 0.84), ambient=(0.92, 0.84, 0.82))

    # A: his mother by the fire; the door opens; Arash comes in: "Arash… is it true?"
    LA = lines_in(T, "p2s6a")
    camA = cam_push(1.0, 1.05, 560, 1150, 4.2)
    d0 = A2.DOOR - T

    def midA(t):
        door = ease((t - d0) / 0.7)
        u = ease((t - d0 - 0.6) / 1.8)
        walking = d0 + 0.6 < t < d0 + 2.4
        turn = ease((t - d0 - 0.2) / 0.5)
        m = tp(LA, t, 1, turn=-0.3 + 0.65 * turn, gx=-0.6 + 1.4 * turn, gy=0.5 - 0.6 * turn, sad=0.5, brow=0.5 + 0.3 * turn, furrow=-0.2,
               armL="chest", armR="relaxed", wind=0.1)
        a = P(turn=-0.3, gx=-0.6, gy=0.2, brow=0.3, furrow=0.2, legs="walk" if walking else "stand", phase=t * 5.0, armL=("ik", 340, 220, "down"),
              propL="bow", armR="relaxed", blink=blink_at(t, 2), wind=0.3)
        arash = at_feet(ARASH, a, t, lerp(890, 760, u), lerp(1398, 1560, u), lerp(0.36, 0.56, u)) if t > d0 + 0.5 else ""
        return open_door(door, t) + fire(t) + arash + at_feet(ARASH_MOTHER, m, t, 380, 1580, 0.6)
    A = Shot(4.2, home, midA, cam=camA, light=HOMEL, grade="fire", bloom=0.6, fade_in=0.4,
             fx=[Glow(lambda t: cam_xy(camA, t, 230, 1230), 330, (255, 160, 80), 0.45), Embers(20, 601, (170, 1120, 290, 1290), (40, 100))])

    # B: Arash: "It is true, Mother. At sunrise."
    T_B = T + 4.2
    LB = lines_in(T_B, "p2s6b")
    camB = cam_push(1.0, 1.04, 540, 860, 3.2)

    def midB(t):
        q = tp(LB, t, 3, turn=-0.25, gx=-0.6, gy=0.4, brow=0.4, furrow=-0.1, sad=0.3, smile=0.1, armL=("ik", 340, 220, "down"), propL="bow",
               armR="relaxed", wind=0.2)
        return at_neck(ARASH, q, t, 560, 960, 1.0)
    B = Shot(3.2, homeb, midB, cam=camB, light=WARMC, grade="fire", bloom=0.5)

    # C: she lays her hand on his face: "My son… you were always brave." … "Go. And let your arrow fly far."
    T_C = T + 7.4
    LC = lines_in(T_C, "p2s6c", "p2s6d")
    camC = cam_push(1.0, 1.05, 540, 900, 5.8)

    def midC(t):
        hand = ease((t - 0.4) / 0.8) * (1 - ease((t - 4.9) / 0.6))
        m = tp(LC, t, 4, turn=0.3, gx=0.7, gy=-0.6, sad=0.6, brow=0.6, furrow=-0.3, smile=0.3 * ease((t - 2.8) / 0.8),
               armL=("ik", lerp(150, 430, hand), lerp(420, -170, hand)) if hand > 0.02 else "relaxed", openL=hand > 0.5, armR="relaxed", wind=0.1)
        a = P(turn=-0.3, gx=-0.7, gy=0.5, brow=0.5, furrow=-0.2, sad=0.4, smile=0.25 * ease((t - 3.4) / 0.8), armL=("ik", 340, 220, "down"),
              propL="bow", armR="relaxed", blink=blink_at(t, 5), breathe=math.sin(t * 1.8), wind=0.2)
        return at_neck(ARASH, a, t, 760, 960, 0.74) + at_neck(ARASH_MOTHER, m, t, 380, 1030, 0.74)
    C = Shot(5.8, homeb, midC, cam=camC, light=WARMC, grade="fire", bloom=0.5)

    # D: he goes back to the door and turns once more; she watches him go
    camD = cam_push(1.0, 1.03, 560, 1150, 2.6)

    def midD(t):
        u = ease(t / 1.8)
        back = ease((t - 1.8) / 0.4)
        m = P(turn=0.35, gx=0.8, gy=-0.1, sad=0.8, brow=0.7, furrow=-0.3, armL="chest", armR="chest", blink=blink_at(t, 6), breathe=math.sin(t * 2),
              wind=0.1)
        a = P(turn=0.35 - 0.7 * back, gx=0.6 - 1.4 * back, gy=0.1, sad=0.4, brow=0.4, furrow=-0.2, legs="walk" if t < 1.8 else "stand", phase=t * 5.0,
              armL=("ik", 340, 220, "down"), propL="bow", armR="relaxed", blink=blink_at(t, 8), wind=0.3)
        return (open_door(1.0, t) + fire(t) + at_feet(ARASH, a, t, lerp(740, 880, u), lerp(1540, 1404, u), lerp(0.55, 0.37, u))
                + at_feet(ARASH_MOTHER, m, t, 380, 1580, 0.6))
    D = Shot(2.6, home, midD, cam=camD, light=HOMEL, grade="fire", bloom=0.6, fade_out=0.7,
             fx=[Glow(lambda t: cam_xy(camD, t, 230, 1230), 330, (255, 160, 80), 0.45), Embers(20, 602, (170, 1120, 290, 1290), (40, 100))])
    return [A, B, C, D]


# ================================================================ S7 before dawn: the climb; the armies wait (105.6-124.8)
CLIMB = [(300, 880), (380, 815), (460, 735), (515, 668), (552, 606)]       # Arash's torch on the left flank of the mountain (zbg.damavand)


def climb_at(u):
    seg = [math.dist(CLIMB[i], CLIMB[i + 1]) for i in range(len(CLIMB) - 1)]
    d = max(0.0, min(1.0, u)) * sum(seg)
    for i, l in enumerate(seg):
        if d <= l:
            f = d / l
            return lerp(CLIMB[i][0], CLIMB[i + 1][0], f), lerp(CLIMB[i][1], CLIMB[i + 1][1], f)
        d -= l
    return CLIMB[-1]


def torch_light(u, t, s=1.0, trail=True):
    x, y = climb_at(u)
    o = ""
    if trail:
        for k in range(1, 12):
            px, py = climb_at(u - k * 0.02)
            o += f'<circle cx="{px:.1f}" cy="{py:.1f}" r="{2.2 * s:.1f}" fill="#ffc070" opacity="{0.4 * (1 - k / 12):.2f}"/>'
    fl = 0.85 + 0.15 * math.sin(t * 13) * math.sin(t * 7)
    return (o + f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{34 * s * fl:.1f}" fill="#ff9a30" opacity="0.28"/>'
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{16 * s * fl:.1f}" fill="#ffb050" opacity="0.6"/>'
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{6 * s:.1f}" fill="#fff6d0"/>')


def s7():
    T = S0["s7"]
    night = bgs.cached("zh_damavand_night", lambda: zbg.damavand("night"))
    road = bgs.cached("zh_damavand_night_road", lambda: zbg.damavand("night", road=True))
    roadb = bgs.cached("zh_damavand_night_road_b6", lambda: bgs.cached("zh_damavand_night_road", lambda: zbg.damavand("night", road=True))
                       .filter(ImageFilter.GaussianBlur(6)))
    NIGHTA = dict(NIGHTL, rim=(5, -3))

    # A: a small light climbs the dark mountain (narrator: "Before dawn, Arash climbed the mountain.")
    camA = cam_push(1.0, 1.18, 470, 760, 4.2)

    def midA(t):
        return torch_light(lerp(0.15, 0.55, t / 4.2), t, 1.0)
    A = Shot(4.2, night, midA, cam=camA, bg_par=1.0, light=dict(rim=(0, 0)), grade="night", bloom=0.8, fade_in=0.4,
             fx=[FadeGlow(lambda t: cam_xy(camA, t, *climb_at(lerp(0.15, 0.55, t / 4.2))), 70, (255, 170, 80), lambda t: 0.8),
                 Motes(20, 701, (220, 230, 255), (0, 200, W, 1100), (-6, 0), amax=60)])

    # B: below, both armies wait with torches and look up at the mountain
    r = random.Random(702)
    iran = [(IRAN_SOLDIER, 70, 1600, 0.36), (IRAN_SOLDIER_3, 190, 1560, 0.33), (IRAN_SOLDIER_2, 300, 1620, 0.37), (IRAN_SOLDIER, 140, 1700, 0.4)]
    turan = [(TURAN_SOLDIER, 800, 1590, 0.35), (TURAN_SOLDIER_2, 920, 1560, 0.33), (TURAN_SOLDIER, 1010, 1640, 0.38), (TURAN_SOLDIER_2, 880, 1700, 0.4)]
    heads = bgs.cached("ar_p02_army_heads", lambda: back_heads(703, 8, 1840, 0.62, col="#0c0a12", blur=3))

    def army_rows():
        rr = random.Random(704)
        body = ""
        for y, sc, n in ((1330, 0.17, 9), (1400, 0.21, 8), (1470, 0.25, 6)):
            for side, specs, x0, x1 in ((-1, (IRAN_SOLDIER, IRAN_SOLDIER_2, IRAN_SOLDIER_3), -20, 420), (1, (TURAN_SOLDIER, TURAN_SOLDIER_2), 660, 1100)):
                for k in range(n):
                    x = lerp(x0, x1, (k + rr.uniform(0.1, 0.9)) / n)
                    q = pose(turn=-0.3 * side, gx=-0.6 * side, gy=-0.9, armL=(20, 10), propL="spear", armR="relaxed", brow=0.4)
                    body += at_feet(rr.choice(specs), q, rr.uniform(0, 3), x, y + rr.uniform(-6, 6), sc * rr.uniform(0.94, 1.06))
        return Image.alpha_composite(bgs.cached("zh_damavand_night_road", lambda: zbg.damavand("night", road=True)), svg_render(body))
    road = bgs.cached("ar_p02_armies", army_rows)
    TORCHES = [(40, 1330), (250, 1345), (390, 1320), (700, 1330), (860, 1345), (1040, 1325)]
    camB = cam_push(1.0, 1.04, 540, 1150, 3.6)

    def midB(t):
        o = torch_light(0.62 + 0.01 * t, t, 0.9, trail=False) + "".join(torch_pole(x, y, 150, t, 0.5, k) for k, (x, y) in enumerate(TORCHES))
        rows = sorted([(y, S, x, s_, -1) for S, x, y, s_ in iran] + [(y, S, x, s_, 1) for S, x, y, s_ in turan], key=lambda v: v[0])
        for k, (y, S, x, s_, side) in enumerate(rows):
            torch = k % 2 == 0
            q = P(turn=0.3 * -side, gx=0.6 * -side, gy=-0.9, brow=0.5, furrow=0.1, armL=(20, 10), propL="spear" if not torch else None,
                  armR="hold_lantern" if torch else "relaxed", propR="torch" if torch else None, blink=blink_at(t, 70 + k), breathe=math.sin(t * 2 + k),
                  wind=0.4)
            o += at_feet(S, q, t, x, y, s_)
        return o
    B = Shot(3.6, road, midB, fg=heads, cam=camB, light=TORCHL, grade="night", bloom=0.7,
             fx=[Glow(lambda t: cam_xy(camB, t, 150, 1150), 260, (255, 150, 70), 0.3), Glow(lambda t: cam_xy(camB, t, 900, 1150), 260, (255, 150, 70), 0.3)])

    # C: the two witnesses of Turan: "Look. A light, near the top." — "Let him climb. It is only one arrow."
    T_C = T + 7.8
    LCa = lines_in(T_C, "p2s7c"); LCb = lines_in(T_C, "p2s7d")
    camC = cam_push(1.0, 1.05, 540, 900, 6.6)

    def midC(t):
        pt = ease((t - 0.5) / 0.4) * (1 - ease((t - 2.4) / 0.4))
        a = tp(LCa, t, 1, turn=0.25, gx=0.2 - 0.9 * pt, gy=-0.4 - 0.5 * pt, brow=0.5, furrow=0.2,
               armR=("ik", lerp(-220, -400, pt), lerp(380, -440, pt), "down") if pt > 0.02 else "relaxed", armL="relaxed", wind=0.4)
        b = tp(LCb, t, 2, turn=-0.25, gx=-0.5 if t < 2.6 else 0.3, gy=-0.6 if t < 2.6 else 0.0, brow=0.3, furrow=0.4, smile=0.35 * ease((t - 2.6) / 0.5),
               armL="chest", armR="chest", wind=0.4)
        return torch_pole(545, 1380, 520, t, 1.4, 3) + at_neck(WITNESS_A, a, t, 300, 1000, 0.78) + at_neck(WITNESS_B, b, t, 790, 1010, 0.78)
    C = Shot(6.6, roadb, midC, cam=camC, light=dict(TORCHL, point=(545, 780, 900, 0.7, 1.2, (1.0, 0.6, 0.3)), ramp=None, rim_point=(545, 6)),
             grade="night", bloom=0.6, fx=[Glow(lambda t: cam_xy(camC, t, 545, 790), 280, (255, 160, 80), 0.4)])

    # D: the boy and his mother from the hungry yard: "Mother, will Arash come back?" — "Watch the mountain, my son."
    T_D = T + 14.4
    LDb = lines_in(T_D, "p2s7e"); LDm = lines_in(T_D, "p2s7f")
    camD = cam_push(1.0, 1.05, 540, 860, 4.8)

    def midD(t):
        hand = ease((t - 3.4) / 0.6)
        b = tp(LDb, t, 3, turn=0.35, gx=0.8, gy=-0.6, sad=0.6, brow=0.7, furrow=-0.3, armL="relaxed", armR="relaxed", wind=0.3)
        m = tp(LDm, t, 4, turn=-0.25, gx=-0.4 if t < 2.0 else 0.3, gy=-0.8 if t > 2.0 else 0.4, sad=0.6, brow=0.6, furrow=-0.2, armL="chest",
               armR=("ik", lerp(-200, -330, hand), lerp(330, 150, hand)) if hand > 0.02 else "relaxed", wind=0.3)
        return at_neck(MOTHER, m, t, 650, 880, 0.95) + at_neck(BOY, b, t, 360, 1000, 0.95)
    D = Shot(4.8, roadb, midD, cam=camD, light=dict(TORCHL, rim=(-5, -2), ramp=(0, W, 1.08, 0.86)), grade="night", bloom=0.6, fade_out=0.4,
             fx=[Glow(lambda t: cam_xy(camD, t, 60, 900), 300, (255, 150, 70), 0.35)])
    return [A, B, C, D]


# ================================================================ S8 the summit (124.8-150.0): the wind takes his cloak; "Look at me…"
def s8():
    T = S0["s8"]
    sm = bg("summit_predawn", lambda: abg.summit("predawn"))
    smb = bg("summit_predawn", lambda: abg.summit("predawn"), 6)

    # A: Arash comes up onto the summit with the great bow; he looks down at the armies
    camA = cam_push(1.0, 1.05, 540, 1100, 4.2)

    def midA(t):
        u = ease(t / 3.2)
        walking = t < 3.2
        x = lerp(1150, 600, u)
        look = ease((t - 3.2) / 0.5)
        q = P(turn=-0.35 + 0.2 * look, gx=-0.7, gy=-0.1 + 0.8 * look, brow=0.3, furrow=0.3, legs="walk" if walking else "stand", phase=t * 4.8,
              armL=("ik", 340, 220, "down"), propL="bow", armR="relaxed", blink=blink_at(t, 1), breathe=math.sin(t * 2.4), wind=1.2)
        return at_feet(ARASH, q, t, x, abg.summit_y(x), 0.44)
    A = Shot(4.2, sm, midA, cam=camA, light=PREDAWN, sun=SUN_PRE, bloom=0.6, fade_in=0.4,
             fx=[snow_wind(801), Motes(30, 802, (255, 220, 200), (0, 300, W, 1300), (-30, -2), amax=90)])

    # B: he opens the clasp of his cloak, and the wind takes it
    T_B = T + 4.2
    cl = A2.CLOAK - T_B
    camB = cam_push(1.0, 1.04, 540, 900, 3.2)

    def midB(t):
        reach = ease((t - 0.2) / 0.6) * (1 - ease((t - cl - 0.2) / 0.5))
        gone = t >= cl
        q = P(turn=0.1, gx=-0.6 if gone else 0.1, gy=-0.4 if gone else 0.3, brow=0.4, furrow=0.2, armL=("ik", 340, 220, "down"), propL="bow",
              armR=("ik", lerp(-200, -100, reach), lerp(420, 60, reach)) if reach > 0.02 else "relaxed", blink=blink_at(t, 3), breathe=math.sin(t * 2.4),
              wind=1.3)
        return cloak_flying(540, 940, 0.8, (t - cl) / 1.1, t) + at_neck(ARASH_BARE if gone else ARASH, q, t, 540, 940, 0.8)
    B = Shot(3.2, smb, midB, cam=camB, light=PREDAWN, sun=SUN_PRE, bloom=0.6, fx=[snow_wind(803)])

    # C: without his cloak, his arms open: "People of Iran! People of Turan!"
    T_C = T + 7.4
    LC = lines_in(T_C, "p2s8a")
    camC = cam_push(1.0, 1.06, 540, 1050, 3.6)

    def midC(t):
        op = ease((t - 0.1) / 0.5)
        q = tp(LC, t, 4, turn=0.0, gx=0.0, gy=0.6, brow=0.6, furrow=0.3, armR=("ik", lerp(-200, -520, op), lerp(470, 110, op), "down"), openR=op > 0.5,
               armL=("ik", lerp(340, 500, op), lerp(220, 110, op), "down"), propL="bow", wind=1.3)
        return at_feet(ARASH_BARE, q, t, 540, abg.summit_y(540), 0.5)
    C = Shot(3.6, sm, midC, cam=camC, light=PREDAWN, sun=SUN_PRE, bloom=0.6, fx=[snow_wind(804)])

    # D: close: "Look at me. I am healthy and strong." … "After this shot… I will not be."
    T_D = T + 11.0
    LD = lines_in(T_D, "p2s8b", "p2s8c")
    camD = cam_push(1.0, 1.08, 540, 860, 8.8)
    t2 = LD[1][1]

    def midD(t):
        chest = ease((t - 1.2) / 0.4) * (1 - ease((t - t2 + 0.3) / 0.5))
        east = ease((t - t2 - 3.4) / 0.8)
        q = tp(LD, t, 5, turn=0.05 + 0.2 * east, gx=0.0 + 0.8 * east, gy=0.2 - 0.2 * east, brow=0.4, furrow=-0.1 * (t > t2), sad=0.35 * ease((t - t2) / 0.6),
               armR="chest" if chest > 0.5 else "relaxed", armL=("ik", 340, 220, "down"), propL="bow", wind=1.2)
        return at_neck(ARASH_BARE, q, t, 540, 960, 1.0)
    D = Shot(8.8, smb, midD, cam=camD, light=dict(PREDAWN, rim_str=1.1), sun=SUN_PRE, bloom=0.6, fx=[snow_wind(805, n=200)])

    # E: he turns to the east and lifts the bow towards the coming sun (the end card comes up over this)
    camE = cam_push(1.0, 1.04, 600, 1100, 5.4)

    def midE(t):
        lift = ease((t - 0.6) / 1.2)
        q = P(turn=0.4, gx=0.9, gy=-0.3, brow=0.3, furrow=0.2, armL=("ik", lerp(340, 420, lift), lerp(220, -240, lift), "down"), propL="bow",
              armR="relaxed", blink=blink_at(t, 9), breathe=math.sin(t * 2), wind=1.2)
        return at_feet(ARASH_BARE, q, t, 520, abg.summit_y(520), 0.46)
    E = Shot(5.4, sm, midE, cam=camE, light=PREDAWN, sun=SUN_PRE, bloom=0.7, fade_out=0.8,
             fx=[snow_wind(806), Motes(30, 807, (255, 220, 200), (0, 300, W, 1300), (-30, -2), amax=90)])
    return [A, B, C, D, E]


SCENES = {"s1": s1, "s2": s2, "s3": s3, "s4": s4, "s5": s5, "s6": s6, "s7": s7, "s8": s8}
