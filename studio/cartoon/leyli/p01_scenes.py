"""Part 1 · The School — 2D cartoon. Timing matches leyli/p01_audio.py
(scene starts s1 0, s2 8.4, s3 13.0, s4 41.0, s5 84.6, s6 108.2; end card 138.2; total 143.4)."""
import math, os, random
import numpy as np
from PIL import Image, ImageFilter, ImageDraw, ImageFont
from film import Shot, W, H, ease, lerp, talk_pose, blink_at, cam_push, Motes, svg_render
from chars import pose, camel, gazelle, Ctx, FEET, fmt, SKINS, OUT, prop
from stage import at_neck, at_feet, Glow, lw_for
import bgs, lbg
from cast import *
import p01_audio as A1

LT = dict(A1.LINES)
DUSKL = dict(rim=(-5, -2), rim_col=(1.0, 0.72, 0.5), rim_str=0.95, ramp=(0, W, 1.06, 0.84), ambient=(0.96, 0.86, 0.84))
SUN_DUSK = (210, 960, 900, (0.14, 0.07, 0.04))
DAWNL = dict(rim=(5, -2), rim_col=(1.0, 0.8, 0.64), rim_str=0.9, ramp=(0, W, 0.88, 1.05), ambient=(0.98, 0.93, 0.95))
SUN_DAWN = (860, 1000, 900, (0.12, 0.08, 0.05))
DAYL = dict(rim=(5, -2), rim_col=(1.0, 0.94, 0.8), ramp=(0, W, 0.94, 1.05), ambient=(1.0, 0.98, 0.95))
SUN_DAY = (880, 380, 900, (0.08, 0.07, 0.04))
SHADEL = dict(rim=(0, -3), rim_col=(1.0, 0.95, 0.84), rim_str=0.8, ambient=(0.93, 0.9, 0.9), ramp=(0, W, 0.97, 1.02))   # under the awning
LAMPL = dict(ambient=(0.7, 0.62, 0.7), rim_point=(330, 6), rim_col=(1.0, 0.66, 0.36), rim_str=0.95)
LAMPC = dict(ambient=(0.82, 0.72, 0.74), rim=(-5, -2), rim_col=(1.0, 0.64, 0.34), rim_str=0.95, ramp=(0, W, 1.08, 0.8))
DOORL = dict(ambient=(0.8, 0.76, 0.9), rim=(-5, -2), rim_col=(1.0, 0.66, 0.36), rim_str=0.9, ramp=(0, W, 1.1, 0.84))


# ---------------------------------------------------------------- helpers
def P(**kw):
    return pose(**kw)


def tp(lines, t, seed, **kw):
    return P(**talk_pose(lines, t, seed, kw))


def L(t0, *ids):
    """line ids -> [(id, start within a shot that begins at t0)]"""
    return [(i, LT[i] - t0) for i in ids]


def bg(name, fn, blur=0):
    """a background cached as build/bg/ly_<name>[_b<blur>].png"""
    if blur:
        return bgs.cached(f"ly_{name}_b{blur}", lambda: bgs.cached(f"ly_{name}", fn).filter(ImageFilter.GaussianBlur(blur)))
    return bgs.cached(f"ly_{name}", fn)


def cam_xy(cam, t, x, y):
    k, cx, cy, px, py = cam(t)
    return (x - cx) * k + cx + px, (y - cy) * k + cy + py


def seated(S, q, t, x, floor, s, flip=False):
    """a person sitting cross-legged on the floor at y floor"""
    return at_neck(S, q, t, x, floor - 575 * S["bs"] * s, s, flip)


def body_xy(S, xf, yf, s, X, Y):
    """screen point (X, Y) -> body coordinates (for an ("ik", x, y) arm) of a person drawn with at_feet(S, …, xf, yf, s)"""
    return (X - xf) / (s * S["bs"]), (Y - yf) / (s * S["bs"]) + FEET


def birds(t, x0=360, y0=520, n=5, s=1.0):
    o = ""
    for k in range(n):
        x = x0 - 26 * t + k * 54 * s + 12 * math.sin(k * 2.1); y = y0 + k * 22 * s + 8 * math.sin(t * 2 + k)
        fl = 9 * s * math.sin(t * 10 + k * 1.7)
        o += (f'<path d="M {x - 14 * s:.1f} {y - fl:.1f} Q {x - 6 * s:.1f} {y - 3 * s:.1f} {x:.1f} {y:.1f} Q {x + 6 * s:.1f} {y - 3 * s:.1f} {x + 14 * s:.1f} {y - fl:.1f}" '
              f'stroke="#2a1a2e" stroke-width="{3.2 * s:.1f}" fill="none" stroke-linecap="round"/>')
    return o


class SandWind:
    """sand carried by the wind: thin streaks and grains flying to the right; strength(t) 0..1"""
    def __init__(self, n=260, seed=1, box=(0, 600, W, 1920), speed=(700, 1400), strength=lambda t: 1.0, col=(255, 228, 190)):
        r = random.Random(seed)
        self.p = [(r.uniform(box[0] - 400, box[2]), r.uniform(box[1], box[3]), r.uniform(*speed), r.uniform(6, 30), r.uniform(0.4, 1.0))
                  for _ in range(n)]
        self.box, self.strength, self.col = box, strength, col

    def __call__(self, im, t):
        a = self.strength(t)
        if a <= 0.01:
            return
        lay = Image.new("RGBA", im.size)
        d = ImageDraw.Draw(lay)
        x0, y0, x1, y1 = self.box
        span = x1 - x0 + 500
        for (x, y, v, ln, al) in self.p:
            xx = x0 - 250 + (x - x0 + v * t) % span
            yy = y + 18 * math.sin(t * 3 + x * 0.01)
            d.line([(xx - ln, yy + 2), (xx, yy)], fill=self.col + (int(160 * al * a),), width=2)
        im.alpha_composite(lay.filter(ImageFilter.GaussianBlur(0.8)))


class Smoke:
    """thin smoke rising from (x, y)"""
    def __init__(self, x, y, n=10, seed=2, col=(200, 196, 200), a=0.35, scale=1.0):
        self.x, self.y, self.n, self.seed, self.col, self.a, self.s = x, y, n, seed, col, a, scale

    def __call__(self, im, t):
        lay = Image.new("RGBA", im.size)
        d = ImageDraw.Draw(lay)
        for k in range(self.n):
            age = (t * 0.35 + k / self.n) % 1.0
            yy = self.y - age * 420 * self.s
            xx = self.x + 50 * self.s * age + 14 * self.s * math.sin(age * 7 + k)
            rr = (10 + 50 * age) * self.s
            d.ellipse((xx - rr, yy - rr, xx + rr, yy + rr), fill=self.col + (int(255 * self.a * (1 - age) * min(1, age * 5)),))
        im.alpha_composite(lay.filter(ImageFilter.GaussianBlur(10 * self.s)))


# ---------------------------------------------------------------- the name in the sand
NAME_FONT = os.path.join(os.path.dirname(os.path.abspath(lbg.__file__)), "fonts", "Vazirmatn-Bold.ttf")
_NAME = {}


def name_data():
    """the name «لیلی» as a mask in the middle of the sand close-up, and the path a finger follows while writing it (right to left)"""
    if not _NAME:
        f = ImageFont.truetype(NAME_FONT, 430, layout_engine=ImageFont.Layout.RAQM)
        im = Image.new("L", (W, H), 0)
        ImageDraw.Draw(im).text((560, 760), "لیلی", font=f, fill=255, anchor="mm", direction="rtl")
        m = np.asarray(im.filter(ImageFilter.GaussianBlur(2.5))).astype(np.float32) / 255
        cols = np.where(m.max(0) > 0.3)[0]
        x0, x1 = int(cols.min()), int(cols.max())
        ys = np.arange(H)[:, None]
        wsum = m.sum(0)
        yc = np.where(wsum > 0.5, (m * ys).sum(0) / np.maximum(wsum, 1e-6), np.nan)
        xs = np.arange(W)
        ok = ~np.isnan(yc)
        yc = np.interp(xs, xs[ok], yc[ok])
        yc = np.convolve(yc, np.ones(31) / 31, mode="same")
        _NAME.update(m=m, x0=x0, x1=x1, yc=yc)
    return _NAME


def name_pos(u):
    """where the finger is when a fraction u of the name is written"""
    d = name_data()
    x = d["x1"] - u * (d["x1"] - d["x0"])
    return x, float(d["yc"][int(min(W - 1, max(0, x)))])


def groove(base, u, vis=1.0, seed=0):
    """the sand picture with the part u (0..1, from the right) of the name pressed into it; vis fades it (the wind)"""
    if u <= 0 or vis <= 0:
        return base
    d = name_data()
    m = d["m"]
    xr = d["x1"] - u * (d["x1"] - d["x0"])
    reveal = np.clip((np.arange(W) - xr) / 18 + 0.5, 0, 1)[None, :]
    R = m * reveal
    if vis < 1:
        r = np.random.default_rng(seed)
        noise = np.asarray(Image.fromarray((r.random((H // 8, W // 8)) * 255).astype(np.uint8)).resize((W, H), Image.BILINEAR)).astype(np.float32) / 255
        R = R * np.clip((vis * 1.6 - noise * 0.6), 0, 1)
    sh = lambda a, dx, dy: np.roll(np.roll(a, dy, 0), dx, 1)
    hi = np.clip(sh(R, 5, 4) - R, 0, 1)            # the lit wall (the light comes from the left)
    lo = np.clip(R - sh(R, 4, 3), 0, 1)            # the shaded wall
    f = np.asarray(base.convert("RGB")).astype(np.float32) / 255
    dark = np.array([0.42, 0.22, 0.14], np.float32)
    f = f * (1 - 0.55 * R[..., None]) + dark * 0.55 * R[..., None]
    f = f * (1 - 0.4 * lo[..., None]) + np.array([0.25, 0.12, 0.08], np.float32) * 0.4 * lo[..., None]
    f = f * (1 - 0.6 * hi[..., None]) + np.array([1.0, 0.9, 0.76], np.float32) * 0.6 * hi[..., None]
    return Image.fromarray((np.clip(f, 0, 1) * 255).astype(np.uint8)).convert("RGBA")


def finger_hand(px, py, lift=0.0, skin="tan", sleeve="#e6e0d2"):
    """Majnun's hand writing in the sand with one finger whose tip is at (px, py); the arm comes in from the bottom right"""
    sk = SKINS[skin]
    py = py - 70 * lift
    ux, uy = 0.5, 0.866
    nx, ny = -uy, ux
    kx, ky = px + ux * 120, py + uy * 120
    hx, hy = kx + ux * 80, ky + uy * 80
    ang = math.degrees(math.atan2(uy, ux))
    sx0, sy0 = hx + ux * 150, hy + uy * 150
    sx1, sy1 = hx + ux * 1300, hy + uy * 1300
    arm = f'M {sx0 + nx * 52:.1f} {sy0 + ny * 52:.1f} L {sx1 + nx * 74:.1f} {sy1 + ny * 74:.1f} L {sx1 - nx * 74:.1f} {sy1 - ny * 74:.1f} L {sx0 - nx * 52:.1f} {sy0 - ny * 52:.1f} Z'
    c0 = hx + ux * 330; c1 = hy + uy * 330
    sl = (f'M {c0 + nx * 96:.1f} {c1 + ny * 96:.1f} L {c0 + ux * 40 + nx * 60:.1f} {c1 + uy * 40 + ny * 60:.1f} L {c0 + ux * 10 + nx * 20:.1f} {c1 + uy * 10 + ny * 20:.1f} '
          f'L {c0 + ux * 60 - nx * 10:.1f} {c1 + uy * 60 - ny * 10:.1f} L {c0 + ux * 20 - nx * 60:.1f} {c1 + uy * 20 - ny * 60:.1f} L {c0 - nx * 100:.1f} {c1 - ny * 100:.1f} '
          f'L {c0 + ux * 900 - nx * 140:.1f} {c1 + uy * 900 - ny * 140:.1f} L {c0 + ux * 900 + nx * 140:.1f} {c1 + uy * 900 + ny * 140:.1f} Z')
    shadow = (f'<g opacity="0.28" filter="url(#hs)" transform="translate(34,22)"><path d="{arm}" fill="#2a1008"/>'
              f'<ellipse cx="{hx:.1f}" cy="{hy:.1f}" rx="92" ry="66" transform="rotate({ang:.1f},{hx:.1f},{hy:.1f})" fill="#2a1008"/>'
              f'<path d="M {px:.1f} {py:.1f} L {kx:.1f} {ky:.1f}" stroke="#2a1008" stroke-width="40" stroke-linecap="round"/></g>')
    o = '<defs><filter id="hs" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="10"/></filter></defs>' + shadow
    o += f'<path d="{arm}" fill="{sk[0]}" stroke="{OUT}" stroke-width="4"/>'
    o += f'<path d="{sl}" fill="{sleeve}" stroke="{OUT}" stroke-width="4"/><path d="M {c0 + ux * 120:.1f} {c1 + uy * 120:.1f} l {nx * 60:.1f} {ny * 60:.1f}" stroke="#b4ac9c" stroke-width="5"/>'
    # curled fingers, then the palm, the thumb and the writing finger
    for k, (a, b) in enumerate(((0.35, -50), (0.15, -62), (-0.05, -66))):
        fx_, fy_ = hx - ux * 40 + nx * b * 0.9, hy - uy * 40 + ny * b * 0.9
        o += f'<ellipse cx="{fx_:.1f}" cy="{fy_:.1f}" rx="30" ry="22" transform="rotate({ang:.1f},{fx_:.1f},{fy_:.1f})" fill="{sk[0]}" stroke="{OUT}" stroke-width="3.4"/>'
    o += f'<ellipse cx="{hx:.1f}" cy="{hy:.1f}" rx="96" ry="70" transform="rotate({ang:.1f},{hx:.1f},{hy:.1f})" fill="{sk[0]}" stroke="{OUT}" stroke-width="4"/>'
    o += f'<path d="M {hx - nx * 40 - ux * 30:.1f} {hy - ny * 40 - uy * 30:.1f} q {ux * 40:.1f} {uy * 40:.1f} {ux * 80 + nx * 10:.1f} {uy * 80 + ny * 10:.1f}" stroke="{sk[1]}" stroke-width="4" fill="none"/>'
    tx_, ty_ = hx + nx * 74 - ux * 10, hy + ny * 74 - uy * 10
    o += f'<ellipse cx="{tx_:.1f}" cy="{ty_:.1f}" rx="44" ry="22" transform="rotate({ang - 30:.1f},{tx_:.1f},{ty_:.1f})" fill="{sk[0]}" stroke="{OUT}" stroke-width="3.4"/>'
    o += (f'<path d="M {px:.1f} {py:.1f} L {kx + nx * 6:.1f} {ky + ny * 6:.1f}" stroke="{OUT}" stroke-width="40" stroke-linecap="round"/>'
          f'<path d="M {px:.1f} {py:.1f} L {kx + nx * 6:.1f} {ky + ny * 6:.1f}" stroke="{sk[0]}" stroke-width="32" stroke-linecap="round"/>'
          f'<path d="M {px + ux * 4 + nx * 6:.1f} {py + uy * 4 + ny * 6:.1f} l {ux * 16:.1f} {uy * 16:.1f}" stroke="{sk[2]}" stroke-width="8" stroke-linecap="round"/>'
          f'<path d="M {px + ux * 60 - nx * 8:.1f} {py + uy * 60 - ny * 8:.1f} l {nx * 14:.1f} {ny * 14:.1f}" stroke="{sk[1]}" stroke-width="3"/>')
    return o


def tablet_lying(x, y, s=1.0, ang=-8):
    """a writing board lying on the rug (Leyli's empty place)"""
    return (f'<g transform="translate({x},{y}) rotate({ang}) scale({s},{s * 0.45})">'
            f'<rect x="-70" y="-100" width="140" height="200" rx="14" fill="#c8a46a" stroke="#1b0f0a" stroke-width="4"/>'
            f'<rect x="-56" y="-86" width="112" height="172" rx="10" fill="#e8d4a4"/>'
            f'<path d="M -34 -50 q 10 -16 20 0 q 10 16 22 0 M 34 -50 L 34 -18 M -30 4 q 18 10 36 0 M -34 50 q 30 14 64 0" stroke="#3a2a1a" stroke-width="5" fill="none"/></g>')


# ================================================================ S1 the hook (0-8.4): a name in the sand; the wind; again
def s1():
    sand = bg("sand_close_dusk", lambda: lbg.sand_close("dusk"))
    t0, t1 = A1.WRITE
    camA = cam_push(1.0, 1.06, 560, 800, 3.9)

    def bgA(t):
        return groove(sand, ease((t - t0) / (t1 - t0)) if t > t0 else 0.0)

    def midA(t):
        u = ease((t - t0) / (t1 - t0)) if t > t0 else 0.0
        x, y = name_pos(u)
        lift = 1 - ease((t - t0 + 0.3) / 0.3) if t < t0 else ease((t - t1) / 0.3)
        wob = 6 * math.sin(t * 17) * (1 if t0 < t < t1 else 0)
        return finger_hand(x + wob, y + wob * 0.5, lift=lift)
    A = Shot(3.9, bgA, midA, cam=camA, bg_par=1.0, light=dict(DUSKL, ramp=None), sun=(80, 200, 1100, (0.16, 0.08, 0.04)), fade_in=0.5,
             fx=[Motes(40, 101, (255, 220, 180), (0, 200, W, 1500), (-8, -3), amax=80)], bloom=0.5)

    dn = bg("dunes_dusk", lambda: lbg.dunes("dusk"))
    camB = cam_push(1.0, 1.05, 560, 1000, 2.5)
    G = A1.GUST - 3.9

    def midB(t):
        g = ease((t - G + 0.2) / 0.4) * (1 - ease((t - G - 1.6) / 0.6))
        c = Ctx(lw_for(1.0))
        o = ""
        for k, (x, y, s, look) in reversed(list(enumerate(((760, 1262, 1.08, 0.0), (965, 1222, 0.92, 0.6))))):
            o += (f'<g transform="translate({x},{y}) scale({s})">'
                  f'{gazelle(c, t=t + k * 1.3, seed=k, look=look, ear=1.0 if g > 0.3 else 0.0, graze=0.15 * (1 - g) if k == 1 else 0.0)}</g>')
        writing = t < G - 0.2
        arm = ("ik", 330 + 30 * math.sin(t * 5), 560) if writing else ("ik", 260, 330)
        q = P(legs="sit", turn=0.3, gx=0.4 if writing else 0.2, gy=0.7 if writing else 0.3 - 0.3 * g, sad=0.4 + 0.2 * g, brow=0.4, furrow=-0.2,
              armL=arm, armR="relaxed", wind=0.4 + 1.2 * g, blink=max(blink_at(t, 3), 0.8 * g if g > 0.6 else 0.0), breathe=math.sin(t * 1.4))
        o += lbg_seat_shadow(400, 1222, 170)
        o += seated(MAJNUN, q, t, 400, 1222, 0.62)
        return o
    B = Shot(2.5, dn, midB, cam=camB, light=DUSKL, sun=SUN_DUSK, bloom=0.6,
             fx=[SandWind(420, 102, (0, 900, W, 1900), (900, 1500), strength=lambda t: ease((t - G + 0.3) / 0.4) * (1 - ease((t - G - 1.4) / 0.6)))])

    camC = cam_push(1.04, 1.08, 560, 800, 2.0)
    T2 = A1.WRITE[0] + 6.9 - 6.4

    def bgC(t):
        trace = groove(sand, 1.0, vis=0.28 * (1 - ease(t / 0.8)), seed=5)
        u = 0.36 * ease((t - 0.5) / 1.5) if t > 0.5 else 0.0
        return groove(trace, u) if u > 0 else trace

    def midC(t):
        u = 0.36 * ease((t - 0.5) / 1.5) if t > 0.5 else 0.0
        x, y = name_pos(u)
        lift = 1 - ease((t - 0.1) / 0.4)
        return finger_hand(x + 5 * math.sin(t * 17), y, lift=lift)
    C = Shot(2.0, bgC, midC, cam=camC, bg_par=1.0, light=dict(DUSKL, ramp=None), sun=(80, 200, 1100, (0.16, 0.08, 0.04)), fade_out=0.5,
             fx=[SandWind(160, 103, (0, 0, W, H), (500, 900), strength=lambda t: 0.6 * (1 - ease(t / 1.2)))], bloom=0.5)
    return [A, B, C]


def lbg_seat_shadow(x, y, w):
    return f'<ellipse cx="{x + 60}" cy="{y + 6}" rx="{w}" ry="{w * 0.12:.0f}" fill="#2a1018" opacity="0.25"/>'


# ================================================================ S2 title (8.4-13.0): the camp at dawn
def s2():
    cp = bg("camp_dawn", lambda: lbg.camp("dawn"))

    def mid(t):
        return birds(t, 980, 480, n=6, s=0.8)
    return [Shot(4.6, cp, mid, cam=cam_push(1.0, 1.06, 540, 1000, 4.6), sun=SUN_DAWN, light=DAWNL,
                 fx=[Smoke(820, 1300, seed=201, a=0.25), Motes(40, 202, (255, 230, 210), (0, 950, W, 1600), (-8, -4), amax=80)],
                 bloom=0.6, fade_in=0.4, fade_out=0.5)]


# ================================================================ S3 the Banu Amir; the chief and his son (13.0-41.0)
def s3():
    cp = bg("camp_dawn", lambda: lbg.camp("dawn"))
    r = random.Random(301)
    herder = spec_copy(BOY_A, kind="man", bs=1.0, hs=1.0, beard="short", beard_col="#1a120c", head="kufiya", kufiya_col="#e8e0d0",
                       kufiya_shade="#c8bca8", agal="#1a1a1a", garment="robe", col="#8a6a4a", col2="#6a4e34", belt=None, sash="#5a3a22")
    woman = spec_copy(GOSSIP_B, scarf_col="#3a2a4a")
    camA = cam_push(1.0, 1.06, 540, 1100, 8.9)

    def midA(t):
        o = ""
        u = t / 8.9
        cx_ = lerp(1180, 760, u)
        c = Ctx(lw_for(0.36))
        o += f'<g transform="translate({cx_ + 120:.1f},1318) scale(-0.36,0.36)">{camel(c, walk=True, phase=t * 3.4, t=t, saddle=False)}</g>'
        q = P(legs="walk", phase=t * 3.4, turn=-0.3, gx=-0.6, armR=("ik", 140, 200), armL="relaxed", wind=0.3, blink=blink_at(t, 1))
        o += at_feet(herder, q, t, cx_ - 30, 1330, 0.19)
        o += (f'<path d="M {cx_ - 30 - 0.19 * 120:.1f} {1330 - 0.19 * 900:.1f} Q {cx_ + 20:.1f} {1330 - 0.19 * 700:.1f} {cx_ + 120 - 0.36 * 480:.1f} {1318 - 0.36 * 700:.1f}" '
              f'stroke="#3a2414" stroke-width="2" fill="none"/>')
        x = lerp(250, 420, u)
        q = P(legs="walk", phase=t * 5.0, turn=0.3, gx=0.6, armL=("ik", 120, -120), propL=("jug", 0), armR="relaxed", wind=0.3, blink=blink_at(t, 2))
        o += at_feet(woman, q, t, x, 1440, 0.24)
        return birds(t, 1000, 470, n=4, s=0.7) + o
    A = Shot(8.9, cp, midA, cam=camA, light=DAWNL, sun=SUN_DAWN, bloom=0.6,
             fx=[Smoke(820, 1300, seed=301, a=0.25), Motes(40, 302, (255, 230, 210), (0, 950, W, 1600), (-8, -4), amax=80)])

    ct = bg("chief_tent_dawn", lambda: lbg.chief_tent("dawn"))
    camB = cam_push(1.0, 1.22, 650, 930, 6.5)

    def midB(t):
        uq = ease((t - 0.2) / 1.6); uc = ease((t - 0.7) / 2.0)
        qwalk = 0.2 < t < 1.8; cwalk = 0.7 < t < 2.7
        cq = P(legs="walk" if cwalk else "stand", phase=t * 4.4, turn=0.2 if cwalk else 0.35, gx=0.4 if cwalk else 0.8, gy=0.2 if cwalk else 0.6,
               smile=0.4, brow=0.2, armL="relaxed", armR="relaxed", wind=0.3, blink=blink_at(t, 3), breathe=math.sin(t * 1.6))
        o = at_feet(CHIEF, cq, t, lerp(470, 400, uc), lerp(1395, 1555, uc), lerp(0.46, 0.6, uc))
        kq = P(legs="walk" if qwalk else "stand", phase=t * 6.0, turn=0.1 if qwalk else -0.3, gx=0.2 if qwalk else -0.7, gy=0.0 if qwalk else -0.7,
               smile=0.6, brow=0.4, armL="relaxed", armR="relaxed", wind=0.3, blink=blink_at(t, 4), breathe=math.sin(t * 1.9))
        o += at_feet(QAYS, kq, t, lerp(600, 660, uq), lerp(1395, 1575, uq), lerp(0.46, 0.62, uq))
        return o
    B = Shot(6.5, ct, midB, cam=camB, light=DAWNL, sun=SUN_DAWN, bloom=0.6,
             fx=[Motes(40, 303, (255, 230, 210), (0, 200, W, 1300), (-8, -4), amax=80)])

    ctb = bg("chief_tent_dawn", lambda: lbg.chief_tent("dawn"), 6)
    LC = L(28.4, "p1s3d")
    camC = cam_push(1.0, 1.04, 540, 900, 4.2)

    def midC(t):
        c = tp(LC, t, 1, turn=0.35, gx=0.8, gy=0.5, smile=0.5, brow=0.3, furrow=-0.2, armL="relaxed", armR="offer" if 1.2 < t < 3.4 else "relaxed",
               wind=0.3)
        k = tp([], t, 2, turn=-0.35, gx=-0.7, gy=-0.6, smile=0.5 * ease((t - 2.4) / 0.6) + 0.2, brow=0.4, armL="relaxed", armR="relaxed", wind=0.3)
        return at_feet(CHIEF, c, t, 330, 1720, 0.82) + at_feet(QAYS, k, t, 740, 1960, 1.15)
    C = Shot(4.2, ctb, midC, cam=camC, light=DAWNL, sun=SUN_DAWN)

    LD = L(32.6, "p1s3e")
    camD = cam_push(1.0, 1.04, 540, 860, 3.0)

    def midD(t):
        k = tp(LD, t, 3, turn=-0.25, gx=-0.6, gy=-0.6, brow=0.7, smile=0.3, armL="relaxed", armR="relaxed", wind=0.3)
        return at_neck(QAYS, k, t, 540, 1020, 1.3)
    D = Shot(3.0, ctb, midD, cam=camD, light=DAWNL, sun=SUN_DAWN)

    LE = L(35.6, "p1s3f")
    camE = cam_push(1.0, 1.05, 540, 860, 5.4)

    def midE(t):
        nod = 8 * ease((t - 4.1) / 0.3) * (1 - ease((t - 4.6) / 0.4))
        c = tp(LE, t, 4, turn=0.25, gx=0.5, gy=0.5, smile=0.6, brow=0.3, furrow=-0.3, nod=nod, armL="relaxed", armR="offer" if 1.4 < t < 3.6 else "relaxed",
               wind=0.3)
        return at_neck(CHIEF, c, t, 540, 960, 1.0)
    E = Shot(5.4, ctb, midE, cam=camE, light=DAWNL, sun=SUN_DAWN, fade_out=0.5)
    return [A, B, C, D, E]


def spec_copy(S, **kw):
    q = dict(S); q.update(kw); return q


# ================================================================ S4 the school (41.0-84.6)
ROW = [(LEYLI, 470), (GIRL_A, 600), (BOY_A, 730), (QAYS, 860), (BOY_B, 990)]
WIDE = {id(GIRL_A): (575, 1075, 0.5), id(BOY_A): (760, 1075, 0.5), id(BOY_B): (955, 1075, 0.5), id(LEYLI): (500, 1195, 0.6), id(QAYS): (870, 1195, 0.6)}


def s4():
    sc = bg("school_day", lambda: lbg.school("day"))
    scb = bg("school_day", lambda: lbg.school("day"), 7)

    def row(t, floor=1150, s=0.58, xs=None, looks=None, lines=None, skip=(), wide=False):
        o = ""
        order = sorted(enumerate(ROW), key=lambda kv: WIDE[id(kv[1][0])][1]) if wide else list(enumerate(ROW))
        for k, (S, x) in order:
            if S in skip:
                continue
            if wide:
                x, fl, sc_ = WIDE[id(S)]
            else:
                x, fl, sc_ = (xs[k] if xs else x), floor, s
            gx, gy, turn = (looks or {}).get(id(S), (-0.6, 0.3, -0.3))
            q = tp((lines or {}).get(id(S), []), t, 10 + k, turn=turn, gx=gx, gy=gy, brow=0.2, armL=("ik", 50, 430), armR=("ik", -50, 430),
                   legs="sit", wind=0.2)
            o += seated(S, q, t, x, fl, sc_)
        return o

    # A: the school under its awning: the teacher, the children on the rug
    camA = cam_push(1.0, 1.1, 470, 860, 4.2)

    def midA(t):
        tq = P(legs="sit", turn=0.35, gx=0.7, gy=0.2, smile=0.2, brow=0.3, armL="relaxed", armR=("ik", 120, 330), propR=("stick", 60), wind=0.2,
               blink=blink_at(t, 5), breathe=math.sin(t * 1.4))
        o = seated(TEACHER, tq, t, 330, 1150, 0.55)
        looks = {id(LEYLI): (-0.3, 0.6, -0.1), id(QAYS): (-0.8, 0.0, -0.35)}
        return o + row(t, looks=looks, wide=True)
    A = Shot(4.2, sc, midA, cam=camA, light=SHADEL, sun=SUN_DAY, bloom=0.5,
             fx=[Motes(50, 401, (255, 240, 210), (0, 330, W, 1000), (6, -2), amax=90)])

    # B: Leyli, close
    LB = []
    camB = cam_push(1.0, 1.05, 540, 860, 4.6)

    def midB(t):
        up = ease((t - 2.2) / 0.5)
        q = tp(LB, t, 20, turn=0.15 + 0.15 * up, gx=0.1 + 0.8 * up, gy=0.7 - 0.8 * up, brow=0.2 + 0.2 * up, smile=0.35 * ease((t - 3.0) / 0.6),
               armL=("ik", 50, 430), armR=("ik", -50, 430), legs="sit", wind=0.3)
        return at_neck(LEYLI, q, t, 540, 1040, 1.3)
    B = Shot(4.6, scb, midB, cam=camB, light=SHADEL, sun=SUN_DAY, fx=[Motes(40, 402, (255, 240, 210), (0, 300, W, 1100), (6, -2), amax=90)])

    # C: Qays, close, looking at her
    camC = cam_push(1.0, 1.04, 540, 860, 2.8)

    def midC(t):
        q = tp([], t, 21, turn=-0.3, gx=-0.9, gy=0.1 + 0.6 * ease((t - 2.0) / 0.3), brow=0.6 - 0.3 * ease((t - 1.2) / 0.4), smile=0.55 * ease((t - 1.0) / 0.5),
               armL="relaxed", armR="relaxed", legs="sit", wind=0.3)
        return at_neck(QAYS, q, t, 540, 1040, 1.3)
    C = Shot(2.8, scb, midC, cam=camC, light=SHADEL, sun=SUN_DAY)

    # D1: the teacher at the board: "Children, repeat after me. Alif… ba… ta…"
    LD = L(52.6, "p1s4c")
    camD = cam_push(1.22, 1.28, 330, 700, 4.0)
    TS = 0.62

    def midD(t):
        k = 0 if t < 2.3 else (1 if t < 2.9 else 2)
        tips = [(254, 600), (192, 640), (128, 640)]
        tx, ty = tips[k] if t > 1.6 else (300, 700)
        hx, hy = body_xy(TEACHER, 470, 1520, TS, tx + 150, ty + 150)
        q = tp(LD, t, 22, turn=-0.25 if t < 1.6 else -0.35, gx=-0.4 if t < 1.0 else -0.8, gy=0.0, brow=0.4, armR=("ik", hx, hy), propR=("stick", -45),
               armL="relaxed", wind=0.2)
        return at_feet(TEACHER, q, t, 470, 1520, TS)
    D1 = Shot(4.0, sc, midD, cam=camD, light=SHADEL, sun=SUN_DAY)

    # D2: the children: "Alif… ba… ta…" (Qays and Leyli only look at each other)
    camD2 = cam_push(1.0, 1.05, 540, 860, 4.4)
    xs2 = [150, 345, 540, 735, 930]

    def midD2(t):
        lines = {id(GIRL_A): L(56.6, "p1s4d"), id(BOY_A): L(56.6, "p1s4d2"), id(BOY_B): L(56.6, "p1s4d3")}
        looks = {id(LEYLI): (0.9, 0.0, 0.3), id(QAYS): (-0.9, 0.0, -0.3), id(GIRL_A): (-0.7, -0.2, -0.3), id(BOY_A): (-0.7, -0.2, -0.3),
                 id(BOY_B): (-0.7, -0.2, -0.3)}
        return row(t, floor=1200, s=0.64, xs=xs2, looks=looks, lines=lines)
    D2 = Shot(4.4, scb, midD2, cam=camD2, light=SHADEL, sun=SUN_DAY)

    # E: the whispers
    LEg = L(61.0, "p1s4e"); LEb = L(61.0, "p1s4f")
    camE = cam_push(1.0, 1.04, 540, 860, 5.4)

    def midE(t):
        g = tp(LEg, t, 23, turn=0.35, gx=0.8 if t < 2.8 else 0.6, gy=0.1, brow=0.6, smile=0.4, armL=("ik", 125, -110, "down") if t < 2.9 else ("ik", 50, 430),
               armR=("ik", -50, 430), legs="sit", wind=0.2, tilt=5)
        b = tp(LEb, t, 24, turn=-0.35, gx=-0.8, gy=0.1, brow=0.6, smile=0.5 * ease((t - 2.6) / 0.4), armR=("ik", -125, -110, "down") if t > 2.9 else ("ik", -50, 430),
               armL=("ik", 50, 430), legs="sit", wind=0.2, tilt=-5 if t > 2.9 else 0)
        return seated(GIRL_A, g, t, 340, 1420, 1.05) + seated(BOY_A, b, t, 750, 1420, 1.05)
    E = Shot(5.4, scb, midE, cam=camE, light=SHADEL, sun=SUN_DAY)

    # F: the teacher: "Qays! What comes after ta?"
    LF = L(66.4, "p1s4g")
    camF = cam_push(1.0, 1.05, 540, 860, 3.0)

    def midF(t):
        q = tp(LF, t, 25, turn=0.3, gx=0.8, gy=0.0, brow=-0.3, furrow=0.9, armR=("ik", 230, 40) if t > 0.2 else "relaxed", propR=("stick", 75),
               armL="relaxed", wind=0.2)
        return at_neck(TEACHER, q, t, 520, 980, 1.0)
    F = Shot(3.0, scb, midF, cam=camF, light=SHADEL, sun=SUN_DAY)

    # G: Qays: "…Leyli?" — the children laugh
    LG = L(69.4, "p1s4h")
    camG = cam_push(1.0, 1.05, 540, 860, 4.2)
    LA = A1.LAUGH - 69.4

    def midG(t):
        st = ease((t - LA - 0.1) / 0.3)
        q = tp(LG, t, 26, turn=-0.3 + 0.4 * st, gx=-0.9 + 1.3 * st, gy=0.0 + 0.5 * ease((t - LA - 1.2) / 0.4), brow=0.2 + 0.6 * st,
               smile=0.5 * (1 - st) + 0.25 * ease((t - LA - 1.4) / 0.5), sad=0.3 * st, armL="relaxed", armR="relaxed" if t < LA + 1.2 else "chest",
               legs="sit", wind=0.3)
        return at_neck(QAYS, q, t, 540, 1040, 1.3)
    G = Shot(4.2, scb, midG, cam=camG, light=SHADEL, sun=SUN_DAY)

    # H: the teacher sighs: "Everyone here is learning to read… except you two."
    LH = L(73.6, "p1s4i")
    camH = cam_push(1.0, 1.05, 540, 860, 4.4)

    def midH(t):
        sigh = ease(t / 0.3) * (1 - ease((t - 0.7) / 0.3))
        q = tp(LH, t, 27, turn=0.2, gx=0.5, gy=0.1, brow=0.5, furrow=-0.3, smile=0.35 * ease((t - 2.4) / 0.6), nod=10 * sigh, tilt=-4 * sigh,
               armR="relaxed", propR=None, armL="relaxed", wind=0.2)
        q["blink"] = max(q["blink"], sigh)
        return at_neck(TEACHER, q, t, 540, 980, 1.0)
    H = Shot(4.4, scb, midH, cam=camH, light=SHADEL, sun=SUN_DAY)

    # I: the two, day after day: "The other children learned letters. These two learned love."
    camI = cam_push(1.0, 1.06, 540, 860, 6.6)

    def midI(t):
        lq = tp([], t, 28, turn=0.35, gx=0.9, gy=0.1, smile=0.5, brow=0.3, armL=("ik", 50, 430), armR=("ik", -50, 430), legs="sit", wind=0.3)
        qq = tp([], t, 29, turn=-0.35, gx=-0.9, gy=0.1, smile=0.55, brow=0.3, armL=("ik", 50, 430), armR=("ik", -50, 430), legs="sit", wind=0.3)
        return seated(LEYLI, lq, t, 300, 1420, 1.0) + seated(QAYS, qq, t, 790, 1420, 1.0)

    def warm(im, t):
        a = 0.5 * ease((t - 2.0) / 4.0)
        im.alpha_composite(Image.new("RGBA", im.size, (255, 150, 60, int(40 * a))))
    I = Shot(6.6, scb, midI, cam=camI, light=SHADEL, sun=SUN_DAY, fade_out=0.6, bloom=0.7,
             fx=[Motes(60, 403, (255, 230, 180), (0, 300, W, 1200), (8, -4), amax=110), warm])
    return [A, B, C, D1, D2, E, F, G, H, I]


# ================================================================ S5 the talk reaches Leyli's tent (84.6-108.2)
def s5():
    cd = bg("camp_dusk", lambda: lbg.camp("dusk"))
    camA = cam_push(1.0, 1.06, 500, 900, 5.0)

    def midA(t):
        lean = ease((t - 0.3) / 0.6)
        a = P(turn=0.35, gx=0.8, gy=0.2, brow=0.5, smile=0.3, armL=("ik", 120, -110, "down") if t < 3.4 else "relaxed", armR="relaxed", wind=1.0,
              tilt=6 * lean, blink=blink_at(t, 30), mouth_o=0.25 * max(0, math.sin(t * 9)) if t < 3.2 else 0.0, breathe=math.sin(t * 1.6))
        b = P(turn=-0.3, gx=-0.7 if t < 3.0 else 0.5, gy=0.2, brow=0.4 + 0.5 * ease((t - 1.2) / 0.4), mouth_o=0.35 * ease((t - 1.2) / 0.3),
              armR="chest" if t < 3.0 else "relaxed", armL="point" if t > 3.2 else "relaxed", wind=1.0, blink=blink_at(t, 31), breathe=math.sin(t * 1.8))
        return at_feet(GOSSIP_A, a, t, 390, 1490, 0.55) + at_feet(GOSSIP_B, b, t, 610, 1490, 0.55)
    A = Shot(5.0, cd, midA, cam=camA, light=DUSKL, sun=SUN_DUSK, bloom=0.6,
             fx=[SandWind(300, 501, (0, 900, W, 1900), (700, 1200), strength=lambda t: 0.8)])

    tn = bg("tent_night", lbg.tent_night)
    tnb = bg("tent_night", lbg.tent_night, 6)
    LB = L(89.6, "p1s5b")
    camB = cam_push(1.14, 1.18, 540, 1900, 5.0)

    def lamp_flame(t, x=lbg.LAMP_AT[0] + 62, y=lbg.LAMP_AT[1] - 4, s=1.0):
        h = (34 + 6 * math.sin(t * 13) + 4 * math.sin(t * 7.7)) * s
        return (f'<path d="M {x - 9 * s:.1f} {y:.1f} C {x - 12 * s:.1f} {y - h * 0.5:.1f}, {x + 2 * s:.1f} {y - h * 0.8:.1f}, {x:.1f} {y - h:.1f} '
                f'C {x + 6 * s:.1f} {y - h * 0.7:.1f}, {x + 12 * s:.1f} {y - h * 0.4:.1f}, {x + 9 * s:.1f} {y:.1f} Z" fill="#ffc050"/>'
                f'<path d="M {x - 4 * s:.1f} {y:.1f} C {x - 5 * s:.1f} {y - h * 0.3:.1f}, {x:.1f} {y - h * 0.5:.1f}, {x:.1f} {y - h * 0.55:.1f} '
                f'C {x + 3 * s:.1f} {y - h * 0.4:.1f}, {x + 5 * s:.1f} {y - h * 0.2:.1f}, {x + 4 * s:.1f} {y:.1f} Z" fill="#fff4c0"/>')

    def midB(t):
        m = tp(LB, t, 32, turn=0.35, gx=0.8, gy=0.3, sad=0.3, brow=0.6, furrow=-0.2, armL="relaxed", armR="chest", legs="sit", wind=0.1)
        l = tp([], t, 33, turn=-0.3, gx=-0.8, gy=0.2 + 0.3 * ease((t - 2.5) / 0.5), sad=0.4 * ease((t - 1.5) / 1.0), brow=0.6, armL="relaxed",
               armR="relaxed", legs="sit", wind=0.1)
        return lamp_flame(t) + seated(MOTHER, m, t, 440, 1345, 0.66) + seated(LEYLI, l, t, 720, 1360, 0.68)
    B = Shot(5.0, tn, midB, cam=camB, bg_par=1.0, light=LAMPL, grade="fire", bloom=0.6,
             fx=[Glow(lambda t: cam_xy(camB, t, lbg.LAMP_AT[0] + 62, lbg.LAMP_AT[1] - 20), 380, (255, 170, 90), 0.4)])

    LC = L(94.6, "p1s5c")
    camC = cam_push(1.0, 1.04, 540, 860, 3.2)

    def midC(t):
        q = tp(LC, t, 34, turn=-0.25, gx=-0.6, gy=0.1, sad=0.6, brow=0.8, furrow=-0.4, armL="relaxed", armR="chest" if t > 0.6 else "relaxed",
               legs="sit", wind=0.1)
        return at_neck(LEYLI, q, t, 540, 1040, 1.3)
    C = Shot(3.2, tnb, midC, cam=camC, light=LAMPC, grade="fire", bloom=0.5)

    LD = L(97.8, "p1s5d")
    camD = cam_push(1.0, 1.05, 860, 800, 4.6)

    def midD(t):
        u = ease((t - 0.1) / 1.0)
        q = tp(LD, t, 35, turn=-0.3, gx=-0.7, gy=0.4, furrow=0.9, brow=-0.2, armL="relaxed", armR="relaxed", wind=0.3,
               legs="walk" if 0.1 < t < 1.1 else "stand", phase=t * 4.5)
        o = at_feet(LEYLI_FATHER, q, t, lerp(930, 880, u), lerp(1340, 1380, u), lerp(0.6, 0.64, u))
        o += ('<path d="M -60 1920 C -60 1700, 40 1600, 170 1600 C 300 1600, 380 1700, 380 1920 Z" fill="#120c0e" opacity="0.92"/>'
              '<path d="M 330 1920 C 330 1760, 400 1690, 490 1690 C 580 1690, 650 1760, 650 1920 Z" fill="#0e0a0c" opacity="0.92"/>')
        return lamp_flame(t) + o
    D = Shot(4.6, tn, midD, cam=camD, light=dict(LAMPL, rim_point=(330, 6)), grade="fire", bloom=0.6,
             fx=[Glow(lambda t: cam_xy(camD, t, lbg.LAMP_AT[0] + 62, lbg.LAMP_AT[1] - 20), 380, (255, 170, 90), 0.4)])

    LE = L(102.4, "p1s5e")
    camE = cam_push(1.0, 1.04, 540, 860, 3.5)

    def midE(t):
        q = tp(LE, t, 36, turn=-0.2, gx=-0.5, gy=0.3, furrow=1.0, brow=-0.3, armL="relaxed", armR="relaxed", wind=0.2)
        return at_neck(LEYLI_FATHER, q, t, 540, 960, 1.0)
    E1 = Shot(3.5, tnb, midE, cam=camE, light=DOORL, grade="night", bloom=0.4)

    camE2 = cam_push(1.0, 1.05, 540, 860, 2.3)

    def midE2(t):
        q = tp([], t, 37, turn=-0.2, gx=-0.3, gy=0.8, sad=0.95, brow=0.9, furrow=-0.5, armL="relaxed", armR="chest", legs="sit", wind=0.1)
        return at_neck(LEYLI, q, t, 540, 1040, 1.3)

    def flicker(im, t):
        a = 0.06 + 0.05 * math.sin(t * 11) * math.sin(t * 5.3)
        im.alpha_composite(Image.new("RGBA", im.size, (0, 0, 0, int(255 * max(0.0, a)))))
    E2 = Shot(2.3, tnb, midE2, cam=camE2, light=LAMPC, grade="fire", bloom=0.5, fade_out=0.8, fx=[flicker])
    return [A, B, C, D, E1, E2]


# ================================================================ S6 Majnun (108.2-143.4)
def s6():
    sc = bg("school_day", lambda: lbg.school("day"))
    scb = bg("school_day", lambda: lbg.school("day"), 7)
    # A: Leyli's place is empty: "Where is Leyli?"
    LA = L(108.2, "p1s6a")
    camA = cam_push(1.0, 1.1, 600, 860, 3.6)
    xs2 = [190, 380, 570, 760, 950]

    def midA(t):
        o = tablet_lying(128, 1172, 0.9)
        for k, (S, x) in enumerate(ROW):
            if S is LEYLI:
                continue
            x = xs2[k]
            if S is QAYS:
                q = tp(LA, t, 40, turn=-0.3, gx=-0.9, gy=0.4, sad=0.5, brow=0.8, furrow=-0.3, armL="relaxed", armR="relaxed", legs="sit", wind=0.2)
            else:
                q = tp([], t, 41 + k, turn=-0.3, gx=-0.6 if t < 2.0 else 0.6, gy=-0.2, brow=0.3, armL=("ik", 50, 430), armR=("ik", -50, 430),
                       legs="sit", wind=0.2)
            o += seated(S, q, t, x, 1200, 0.72)
        return o
    A = Shot(3.6, scb, midA, cam=camA, light=SHADEL, sun=SUN_DAY)

    LB = L(111.8, "p1s6b")
    camB = cam_push(1.0, 1.05, 540, 860, 3.8)

    def midB(t):
        q = tp(LB, t, 46, turn=0.25, gx=0.6, gy=0.3, sad=0.5, brow=0.7, furrow=-0.4, armR="relaxed", armL="relaxed", wind=0.2)
        return at_neck(TEACHER, q, t, 540, 980, 1.0)
    B = Shot(3.8, scb, midB, cam=camB, light=SHADEL, sun=SUN_DAY)

    # C: Qays walks among the tents calling her name
    cpd = bg("camp_day", lambda: lbg.camp("day"))
    LC = L(115.6, "p1s6c")
    camC = cam_push(1.0, 1.05, 540, 1000, 6.0)
    elder = spec_copy(CHIEF, beard="white", kufiya_col="#e8e0d0", cloak="#3a4a3a", cloak2="#24301f", cloak_hi="#8a9a6a")

    def midC(t):
        u = t / 6.0
        calling = 0.9 < t < 2.6
        q = tp(LC, t, 47, turn=-0.25, gx=-0.6, gy=-0.4, brow=0.7, sad=0.4, legs="walk", phase=t * 5.0, nod=-6 if calling else 0,
               armR="relaxed", armL=("ik", 128, -118, "down") if calling else "relaxed", wind=0.4)
        o = ""
        c = Ctx(lw_for(0.4))
        o += f'<g transform="translate(860,1300) scale(-0.42,0.42)">{camel(c, t=t, saddle=True)}</g>'
        e = P(turn=0.3, gx=0.6 if t > 1.2 else -0.2, gy=0.0, brow=0.5, sad=0.3 * ease((t - 1.5) / 1.0), armL="relaxed", armR="relaxed",
              blink=blink_at(t, 48), wind=0.3)
        o += at_feet(elder, e, t, 990, 1330, 0.24)
        w = P(turn=0.3, gx=0.7, gy=0.1, brow=0.5, armL="chest", armR="relaxed", blink=blink_at(t, 49), wind=0.3)
        o += at_feet(GOSSIP_A, w, t, 150, 1250, 0.24)
        o += at_feet(QAYS, q, t, lerp(820, 470, u), 1400, 0.52)
        return o
    C = Shot(6.0, cpd, midC, cam=camC, light=DAYL, sun=SUN_DAY, bloom=0.5)

    # D: the boys run after him: "Look! Majnun! The madman!" — "Majnun! Majnun!"
    LDa = L(121.6, "p1s6d"); LDb = L(121.6, "p1s6e")
    camD = cam_push(1.0, 1.04, 540, 1000, 6.6)

    def midD(t):
        o = ""
        u = t / 6.6
        look = ease((t - 2.4) / 0.4) * (1 - ease((t - 3.8) / 0.4))
        q = P(legs="walk", phase=t * 4.6, turn=0.25 - 0.55 * look, gx=0.5 - 1.2 * look, gy=0.4 * (1 - look), sad=0.6, brow=0.6, armL="relaxed",
              armR="relaxed", wind=0.4, blink=blink_at(t, 50), breathe=math.sin(t * 2))
        o += at_feet(QAYS, q, t, lerp(560, 900, u), lerp(1390, 1330, u), lerp(0.5, 0.42, u))
        for k, (S, x0, x1, lines, seed) in enumerate(((BOY_C, -160, 235, [], 51), (BOY_A, -60, 385, LDa, 52), (BOY_B, -280, 85, LDb, 53))):
            run = ease(t / 2.6)
            x = lerp(x0, x1, run)
            moving = t < 2.6
            laughing = 0.5 + 0.5 * math.sin(t * 9 + k)
            b = tp(lines, t, seed, legs="walk" if moving else "stand", phase=t * 9.0 + k, turn=0.35, gx=0.8, gy=0.0, brow=0.5, smile=0.7,
                   armR="point" if k != 2 else ("ik", 200, -60), armL="relaxed" if k != 2 else "point", wind=0.5)
            if not lines:
                b["mouth_o"] = max(b["mouth_o"], 0.3 * laughing)
            o += at_feet(S, b, t, x, (1405, 1440, 1425)[k], (0.49, 0.52, 0.5)[k])
        return o
    D = Shot(6.6, cpd, midD, cam=camD, light=DAYL, sun=SUN_DAY, bloom=0.5)

    # E: he walks alone into the dunes at sunset (the end card from 10.0)
    dn = bg("dunes_dusk", lambda: lbg.dunes("dusk"))
    camE = cam_push(1.08, 1.0, 480, 1100, 15.2)

    def midE(t):
        u = ease(t / 13.0)
        x = lerp(760, 380, u); y = lerp(1560, 1200, u); s = lerp(0.6, 0.22, u)
        q = P(legs="walk" if t < 13.0 else "stand", phase=t * 4.0, turn=-0.5, gx=-0.9, gy=-0.2, sad=0.5, brow=0.5, armL="relaxed", armR="relaxed",
              wind=0.8, blink=blink_at(t, 54), breathe=math.sin(t * 2))
        sh = (f'<g transform="translate({x:.1f},{y:.1f}) scale({s:.4f})"><path d="M -60 0 L 760 160 L 820 90 L 40 -20 Z" fill="#3a1830" opacity="0.28"/></g>')
        o = sh + at_feet(QAYS, q, t, x, y, s)
        if t > 6.0:
            a = ease((t - 6.0) / 1.5)
            c = Ctx(lw_for(0.2))
            for k, (gx_, gy_) in enumerate(((880, 1100), (950, 1108))):
                o += f'<g opacity="{a:.2f}" transform="translate({gx_},{gy_}) scale(0.2)">{gazelle(c, t=t + k, seed=k, look=0.3, graze=0.0)}</g>'
        return o
    E = Shot(15.2, dn, midE, cam=camE, light=DUSKL, sun=SUN_DUSK, bloom=0.7,
             fx=[Motes(50, 601, (255, 220, 190), (0, 1050, W, 1700), (-8, -3), amax=90)], fade_out=0.6)
    return [A, B, C, D, E]


SCENES = {"s1": s1, "s2": s2, "s3": s3, "s4": s4, "s5": s5, "s6": s6}
