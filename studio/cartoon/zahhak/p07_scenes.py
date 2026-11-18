"""Part 7 · Kaveh the Blacksmith — 2D cartoon. Timing matches zahhak/p07_audio.py
(scene starts s1 0, s2 7.6, s3 12.2, s4 48.4, s5 72.0, s6 129.4; end card 143.6; total 148.6)."""
import math, random
from PIL import Image, ImageFilter, ImageDraw
from film import Shot, W, H, ease, lerp, talk_pose, blink_at, cam_push, cam_static, Motes, Embers, svg_render
from chars import pose, Ctx, FEET, fmt, prop, SKINS, OUT
from stage import at_neck, at_feet, Glow, lw_for, fire_svg, crowd_row, back_heads, random_spec
import bgs, zbg
from cast import *
from p01_scenes import P, bg, cam_xy, tp, darken, fade_to, torch_flame, hall_fx, placed, flipped, TORCH, HALL, NIGHT
from p03_scenes import night_of, svg_fx, cam_svg, torches_wide, torches_close
from p05_scenes import hand_at, shake, silhouette, zk_throne, guards_hall, LAMP, ZCLOSE
from p06_scenes import mead, mist, DAWNL, SUN_DAWN

RIP1 = 2.5           # s1 A: the paper tears (shot time)
RIP2 = 1.6           # s5 K
BANGS = (0.25, 0.75, 1.25)                     # s5 A: fists on the door (shot time)
DAYM = dict(rim=(5, -2), rim_col=(1.0, 0.9, 0.72), ramp=(0, W, 0.94, 1.04), ambient=(1.0, 0.97, 0.94))
SUN_DAY = (170, 520, 900, (0.10, 0.08, 0.04))
DAWNM = dict(rim=(-5, -2), rim_col=(1.0, 0.7, 0.45), rim_str=0.9, ramp=(0, W, 1.06, 0.88), ambient=(0.94, 0.86, 0.9))
KCLOSE = dict(ambient=(0.84, 0.78, 0.84), rim=(-5, -2), rim_col=(1.0, 0.64, 0.34), rim_str=0.9, ramp=(0, W, 1.06, 0.86))
INK = "#3a2616"

# nobles of every land in Zahhak's hall: two groups turned to the throne (S, x, side)
NOB_L = [(COURTIER, 70, 1), (NOBLE_1, 195, 1), (MOBED_1, 320, 1)]
NOB_R = [(NOBLE_2, 760, -1), (COURTIER3, 885, -1), (COURTIER2, 1010, -1)]


# ---------------------------------------------------------------- the paper
def _wavy(x0, y0, x1, y1, seed, amp=4.0):
    """a line of 'writing': a wavy stroke from (x0, y0) to (x1, y1) with little loops"""
    r = random.Random(seed)
    n = 18
    pts = []
    for i in range(n + 1):
        u = i / n
        pts.append((lerp(x0, x1, u), lerp(y0, y1, u) + amp * math.sin(u * 37 + seed) + r.uniform(-1.5, 1.5)))
    return "M " + " L ".join(f"{x:.1f} {y:.1f}" for x, y in pts)


def sheet(tl, tr, br, bl, seed=1, sigs=3, seal=True, rows=7, lw=1.0):
    """the testimonial: a cream sheet with lines of writing, signatures and Zahhak's black seal, corners tl tr br bl (screen)"""
    def at(u, v):        # bilinear point on the sheet, u across, v down
        top = (lerp(tl[0], tr[0], u), lerp(tl[1], tr[1], u)); bot = (lerp(bl[0], br[0], u), lerp(bl[1], br[1], u))
        return lerp(top[0], bot[0], v), lerp(top[1], bot[1], v)
    o = (f'<path d="M {tl[0]:.1f} {tl[1]:.1f} L {tr[0]:.1f} {tr[1]:.1f} L {br[0]:.1f} {br[1]:.1f} L {bl[0]:.1f} {bl[1]:.1f} Z" fill="#efe2bf" '
         f'stroke="{OUT}" stroke-width="{2.4 * lw:.1f}"/>')
    a, b = at(0.06, 0.04), at(0.94, 0.04)
    o += f'<path d="M {a[0]:.1f} {a[1]:.1f} L {b[0]:.1f} {b[1]:.1f}" stroke="#c8a870" stroke-width="{3 * lw:.1f}" opacity="0.8"/>'
    for k in range(rows):
        v = 0.12 + k * 0.075
        x0, y0 = at(0.12 if k else 0.3, v); x1, y1 = at(0.88 if k else 0.7, v)
        o += f'<path d="{_wavy(x0, y0, x1, y1, seed * 10 + k, 2.2 * lw)}" stroke="{INK}" stroke-width="{2.2 * lw:.1f}" fill="none" opacity="0.75"/>'
    for k in range(sigs):
        u0 = 0.1 + (k % 3) * 0.28; v0 = 0.72 + (k // 3) * 0.1
        x0, y0 = at(u0, v0); x1, y1 = at(u0 + 0.2, v0 - 0.02)
        o += f'<path d="{_wavy(x0, y0, x1, y1, seed * 31 + k, 7 * lw)}" stroke="#1a1430" stroke-width="{2.6 * lw:.1f}" fill="none"/>'
    if seal:
        sx, sy = at(0.5, 0.92)
        o += f'<circle cx="{sx:.1f}" cy="{sy:.1f}" r="{14 * lw:.1f}" fill="#16121a" stroke="#c9a24a" stroke-width="{2 * lw:.1f}"/>'
    return o


def torn_half(tl, tr, br, bl, side, seed=1):
    """one half of the torn sheet; the jagged tear runs down the middle"""
    r = random.Random(seed)
    jag = [(0.5 + r.uniform(-0.06, 0.06), k / 8) for k in range(9)]
    def at(u, v):
        top = (lerp(tl[0], tr[0], u), lerp(tl[1], tr[1], u)); bot = (lerp(bl[0], br[0], u), lerp(bl[1], br[1], u))
        return lerp(top[0], bot[0], v), lerp(top[1], bot[1], v)
    if side < 0:
        pts = [at(0, 0)] + [at(u, v) for u, v in jag] + [at(0, 1)]
    else:
        pts = [at(1, 0)] + [at(u, v) for u, v in jag] + [at(1, 1)]
    d = "M " + " L ".join(f"{x:.1f} {y:.1f}" for x, y in pts) + " Z"
    cid = f"half{seed}{'l' if side < 0 else 'r'}{abs(hash((round(tl[0]), round(tl[1])))) % 99999}"
    return f'<clipPath id="{cid}"><path d="{d}"/></clipPath><g clip-path="url(#{cid})">{sheet(tl, tr, br, bl, seed)}</g><path d="{d}" fill="none" stroke="{OUT}" stroke-width="2.2"/>'


def rot(pts, cx, cy, ang):
    a = math.radians(ang); ca, sa = math.cos(a), math.sin(a)
    return [(cx + (x - cx) * ca - (y - cy) * sa, cy + (x - cx) * sa + (y - cy) * ca) for x, y in pts]


class Scraps:
    """scraps of the torn paper falling and turning; spawn around (x, y) at t0, spread `spread`, sizes ~`size` px"""
    def __init__(self, t0, x, y, spread=220, size=40, n=16, seed=0, fall=(260, 420), up=(-380, -120)):
        r = random.Random(seed)
        self.t0 = t0
        self.p = [(x + r.uniform(-spread, spread) * 0.4, y + r.uniform(-spread, spread) * 0.3, r.uniform(-1, 1) * spread * 1.6, r.uniform(*up),
                   r.uniform(*fall), r.uniform(0.6, 1.3) * size, r.uniform(0, 6.3), r.uniform(-500, 500), r.uniform(1.5, 3.0)) for _ in range(n)]

    def svg(self, t, floor=None):
        u = t - self.t0
        if u <= 0:
            return ""
        o = ""
        for x, y, vx, vy, fall, sz, ph, spin, fr in self.p:
            drag = 1 - math.exp(-u * 2.2)
            px = x + vx * drag / 2.2 + 30 * math.sin(u * fr * 2 + ph)
            py = y + vy * drag / 2.2 + fall * max(0.0, u - 0.25) * 0.9
            if floor is not None:
                py = min(py, floor + 20 * math.sin(ph))
            a = ph * 57 + spin * u * (0.3 if floor is not None and py >= floor - 1 else 1.0)
            w_, h_ = sz, sz * 0.7 * abs(math.cos(u * fr + ph)) + sz * 0.15
            pts = rot([(px - w_ / 2, py - h_ / 2), (px + w_ / 2, py - h_ / 2 + 4), (px + w_ / 2 - 3, py + h_ / 2), (px - w_ / 2 + 2, py + h_ / 2 - 3)], px, py, a)
            o += ('<path d="M ' + " L ".join(f"{a_:.1f} {b_:.1f}" for a_, b_ in pts) + ' Z" fill="#efe2bf" stroke="#3a2a1a" stroke-width="1.6"/>'
                  f'<path d="M {pts[0][0] * 0.7 + pts[2][0] * 0.3:.1f} {pts[0][1] * 0.7 + pts[2][1] * 0.3:.1f} L {pts[1][0] * 0.6 + pts[3][0] * 0.4:.1f} '
                  f'{pts[1][1] * 0.6 + pts[3][1] * 0.4:.1f}" stroke="{INK}" stroke-width="1.4" opacity="0.6"/>')
        return o


def held_sheet(S, armR, armL, x, y, s, h=230, t=0.0, tear=0.0, seed=1, neck=True):
    """the sheet held by its top corners in both hands of S (placed at_neck at (x, y) scale s); tear 0..1 pulls the halves apart"""
    hr = hand_at(S, armR, -1, x, y, s, neck=neck)
    hl = hand_at(S, armL, 1, x, y, s, neck=neck)
    hh = h * s * S["bs"]
    tl, tr = (hr[0] + 6, hr[1] - 6), (hl[0] - 6, hl[1] - 6)
    bl, br = (tl[0] + 8, tl[1] + hh), (tr[0] - 8, tr[1] + hh)
    if tear <= 0:
        return sheet(tl, tr, br, bl, seed, lw=s * 1.4)
    ang = 26 * ease(tear)
    left = rot([tl, ((tl[0] + tr[0]) / 2, tl[1]), ((bl[0] + br[0]) / 2, bl[1]), bl], tl[0], tl[1], -ang)
    right = rot([((tl[0] + tr[0]) / 2, tr[1]), tr, br, ((bl[0] + br[0]) / 2, br[1])], tr[0], tr[1], ang)
    # draw each half as the matching half of a full sheet: map the half's corners back to a whole sheet (twice as wide)
    L = torn_half(left[0], (2 * left[1][0] - left[0][0], 2 * left[1][1] - left[0][1]), (2 * left[2][0] - left[3][0], 2 * left[2][1] - left[3][1]), left[3], -1, seed)
    R = torn_half((2 * right[0][0] - right[1][0], 2 * right[0][1] - right[1][1]), right[1], right[2], (2 * right[3][0] - right[2][0], 2 * right[3][1] - right[2][1]), 1, seed)
    return L + R


def tear_arms(t, t_rip, hold=(95, 215), pull=(170, -70), drop=0.75):
    """arm targets (body units) holding the sheet in front of the chest, then ripping it apart at t_rip and throwing the halves down
    (drop s later); returns (armR, armL, tear 0..1, thrown 0..1)"""
    u = ease((t - t_rip) / 0.3)
    th = ease((t - t_rip - drop) / 0.35)
    hx, hy = hold
    x = hx + pull[0] * u + 60 * th; y = hy + pull[1] * u + 260 * th
    return ("ik", -x, y), ("ik", x, y), u, th


# ---------------------------------------------------------------- other helpers
def dust_tex():
    """the drifting dust of part 6 (same cache file)"""
    return bgs.cached("zh_dust_tex", lambda: svg_render("".join(
        f'<ellipse cx="{random.Random(i).uniform(-200, 2000):.0f}" cy="{random.Random(i + 50).uniform(1200, 1800):.0f}" rx="{random.Random(i + 9).uniform(160, 380):.0f}" '
        f'ry="{random.Random(i + 3).uniform(40, 110):.0f}" fill="#b89a6a" opacity="0.55"/>' for i in range(30)), 2200, H).filter(ImageFilter.GaussianBlur(26)))


def memory_fx(a=0.55, tint=(70, 40, 20)):
    """the look of Faranak's memories: warm sepia, soft dark edges"""
    yy, xx = [v.astype("float32") for v in __import__("numpy").mgrid[0:H, 0:W]]
    import numpy as np
    d = np.clip((np.sqrt(((xx - W / 2) / (W * 0.55)) ** 2 + ((yy - H * 0.45) / (H * 0.5)) ** 2) - 0.55) / 0.5, 0, 1)
    edge = Image.fromarray((d * 235).astype(np.uint8))

    def fx(im, t):
        g = im.convert("L").convert("RGBA")
        sep = Image.blend(g, Image.new("RGBA", (W, H), (200, 150, 100, 255)), 0.35)
        im.alpha_composite(Image.blend(im, sep, a))
        dark = Image.new("RGBA", (W, H), tint + (0,)); dark.putalpha(edge)
        im.alpha_composite(dark)
    return fx


def kaveh_q(lines, t, seed, **kw):
    base = dict(turn=0.2, gx=0.5, gy=0.0, furrow=0.9, brow=-0.3, armL="relaxed", armR="relaxed", wind=0.15)
    base.update(kw)
    return tp(lines, t, seed, **base)


def nobles(t, look=0.0, bow=0.0, seed=0, fear=0.0, y=1520, s=0.36, extra=None):
    """the great men in two groups turned to the throne; look turns their eyes (-1 to the left door … +1)"""
    o = ""
    for k, (S, x, side) in enumerate(NOB_L + NOB_R):
        lk = look * (1.0 if side > 0 else 1.0)
        turn = lerp(0.42 * side, -0.45 if look < 0 else 0.45, abs(look)) if look else 0.42 * side
        q = P(turn=turn, gx=0.7 * side if not look else 0.9 * (1 if look > 0 else -1), gy=-0.2 + 0.7 * bow, nod=14 * bow, brow=0.5 + 0.6 * fear,
              furrow=-0.2 - 0.3 * fear, sad=0.3 + 0.3 * fear, armL="chest", armR="chest" if k % 2 else "relaxed", blink=blink_at(t, seed + k),
              breathe=math.sin(t * 2 + k))
        if extra:
            q.update(extra(k, t))
        o += at_feet(S, q, t, x, y + 18 * (k % 2), s)
    return o


def kondrow_at(t, x=760, y=1372, s=0.33, seed=0, **kw):
    q = P(turn=-0.35, gx=-0.6, gy=0.0, brow=0.6, furrow=-0.3, sad=0.2, armL=("ik", 150, 260, "down"), propL="scroll", armR="relaxed",
          blink=blink_at(t, 70 + seed), breathe=math.sin(t * 2.4))
    q.update(kw)
    return at_feet(KONDROW, q, t, x, y, s)


def throne_zk(t, seed, **kw):
    base = dict(snake_looks=(0.6 + 0.4 * math.sin(t * 1.1), 0.5 + 0.5 * math.sin(t * 1.3 + 1)))
    base.update(kw)
    return zk_throne(t, seed, **base)


class Many:
    def __init__(self, *items):
        self.items = items

    def svg(self, t, floor=None):
        return "".join(i.svg(t, floor) for i in self.items)


def thrown_scraps(S, t_rip, x, y, s, seed, drop=0.75, size=58, floor=None):
    """the halves thrown down from both hands (where the hands are when the throw starts) break into falling scraps"""
    aR, aL, _, _ = tear_arms(t_rip + drop, t_rip)
    hr = hand_at(S, aR, -1, x, y, s, neck=True); hl = hand_at(S, aL, 1, x, y, s, neck=True)
    return Many(Scraps(t_rip + drop + 0.1, hr[0] + 40, hr[1] + 90, spread=150, size=size, n=7, seed=seed, fall=(320, 480), up=(-200, -40)),
                Scraps(t_rip + drop + 0.1, hl[0] - 40, hl[1] + 90, spread=150, size=size, n=7, seed=seed + 1, fall=(320, 480), up=(-200, -40)))


def kaveh_tearing(t, lines, t_rip, x, y, s, seed, scraps, S=None):
    """Kaveh (placed at_neck at (x, y), scale s) holds up the paper, shouts, rips it in two and throws the halves down: scraps fall"""
    S = S or KAVEH
    aR, aL, u, th = tear_arms(t, t_rip)
    q = kaveh_q(lines, t, seed, turn=0.05, gx=0.1, gy=-0.1 + 0.5 * th, furrow=1.0, brow=-0.6, armR=aR, armL=aL)
    q["mouth_o"] = max(q["mouth_o"], 0.4 * u * (1 - ease((t - t_rip - 0.9) / 0.4)))
    o = torch_flame(40, 740, t, 1.1) + torch_flame(1040, 740, t + 1.7, 1.1, 1) + at_neck(S, q, t, x, y, s)
    if th < 0.5:
        o += held_sheet(S, aR, aL, x, y, s, t=t, tear=u, seed=7)
    return o + scraps.svg(t)


# ================================================================ S1 the hook (0-7.6)
def s1():
    close = bg("hall_close", zbg.hall_close)
    hallb = bg("hall", zbg.hall, 6)
    camA = cam_push(1.0, 1.05, 540, 760, 3.9)
    LA = [("p7s1a", 0.4)]
    X, Y, SC = 540, 620, 0.95

    def midA(t):
        return kaveh_tearing(t, LA, RIP1, X, Y, SC, 1, scrapsA)
    scrapsA = thrown_scraps(KAVEH, RIP1, X, Y, SC, 71)
    A = Shot(3.9, hallb, midA, cam=shake(camA, RIP1, RIP1 + 0.5, 7), light=KCLOSE, fx=hall_fx(camA, [(40, 740), (1040, 740)], 701),
             grade="fire", bloom=0.6, fade_in=0.3)

    camB = cam_push(1.0, 1.06, 540, 860, 3.7)
    fall = Scraps(-0.6, 540, 300, spread=420, size=52, n=14, seed=72, fall=(160, 260), up=(-40, 40))

    def midB(t):
        shock = ease((t - 0.2) / 0.5)
        q = tp([], t, 2, turn=0.0, gx=0.0, gy=0.1, furrow=1.0 - 1.6 * shock, brow=-0.3 + 1.4 * shock, sad=0.2, armL="relaxed", armR="relaxed",
               snake_looks=(1.0, 1.0), hisses=(0.9 * (0.6 + 0.4 * math.sin(t * 5)), 0.9 * (0.6 + 0.4 * math.sin(t * 4 + 1))))
        q["blink"] = min(q["blink"], 0.15)
        return torches_close(t) + at_neck(ZAHHAK_KING, q, t, 540, 1030, 1.0) + fall.svg(t)
    B = Shot(3.7, close, midB, cam=camB, light=TORCH, fx=hall_fx(camB, [(40, 740), (1040, 740)], 702), grade="fire", bloom=0.6, fade_out=0.4)
    return [A, B]


# ================================================================ S2 title (7.6-12.2): the market at dawn, Kaveh at his anvil
def anvil_svg(x, y, s):
    """Kaveh's anvil on a tree stump, standing on the ground at (x, y); s = the scale of the people next to it (top of the face at y - 720 s)"""
    return (f'<g transform="translate({x:.1f},{y:.1f}) scale({s:.4f})">'
            f'<path d="M -88 0 L 88 0 L 76 -580 L -76 -580 Z" fill="#5a3a22" stroke="{OUT}" stroke-width="5"/>'
            f'<path d="M -50 -60 L -44 -540 M 30 -40 L 36 -550" stroke="#3a2414" stroke-width="5" opacity="0.6"/>'
            f'<ellipse cx="0" cy="-580" rx="78" ry="16" fill="#7a5232" stroke="{OUT}" stroke-width="4"/>'
            f'<path d="M -70 -588 L 70 -588 L 50 -640 L 64 -658 L 26 -670 L -26 -670 L -64 -658 L -50 -640 Z" fill="#34343c" stroke="{OUT}" stroke-width="5"/>'
            f'<path d="M -120 -670 L 140 -670 L 140 -720 L -60 -720 C -130 -716, -190 -700, -230 -678 C -190 -680, -150 -676, -120 -670 Z" fill="#3e3e48" stroke="{OUT}" stroke-width="5"/>'
            f'<path d="M -60 -714 L 134 -714" stroke="#8a8a98" stroke-width="7"/></g>')


STRIKES = (0.7, 1.3, 1.9, 3.0, 3.6)


def hammer_arm(t, hits=STRIKES, up=("ik", -330, -120), down=("ik", -300, 430, "down")):
    """the hammer arm of a smith standing to the right of his anvil: raised between blows, down on each blow; returns (arm, hammer angle)"""
    nxt = min([h for h in hits if h >= t - 0.1] or [99])
    prev = max([h for h in hits if h < t - 0.1] or [-99])
    u = 1 - ease((nxt - t) / 0.28) if nxt - t < 0.28 else 0.0          # coming down
    r_ = ease((t - prev - 0.1) / 0.35) if t - prev < 0.45 else 1.0      # lifting again
    k = max(u, 1 - r_) if prev > -99 else u
    arm = ("ik", lerp(up[1], down[1], k), lerp(up[2], down[2], k), "down")
    return arm, lerp(25, -128, k)


def s2():
    md = bg("market_dawn", lambda: zbg.market("dawn"))
    cam = cam_push(1.0, 1.07, 380, 1150, 4.6)
    AX, AY, SK = 318, 1372, 0.4

    def mid(t):
        arm, ang = hammer_arm(t)
        q = P(turn=-0.35, gx=-0.7, gy=0.7, furrow=0.7, brow=0.0, armR=arm, propR=("hammer", ang), armL=("ik", -60, 420, "down"),
              blink=blink_at(t, 3), breathe=math.sin(t * 2), wind=0.1)
        return at_feet(KAVEH, q, t, 455, 1350, SK) + anvil_svg(AX, AY, SK)

    def sparks(im, t):
        d = ImageDraw.Draw(im, "RGBA")
        for k, h in enumerate(STRIKES):
            u = t - h
            if 0 <= u < 0.7:
                r = random.Random(k)
                for j in range(16):
                    a = r.uniform(-2.9, -0.2); v = r.uniform(260, 560)
                    x = AX + 10 + math.cos(a) * v * u; y = AY - 720 * SK + math.sin(a) * v * u + 700 * u * u
                    cx_, cy_ = cam_xy(cam, t, x, y)
                    s_ = 3.4 * (1 - u / 0.7)
                    d.ellipse((cx_ - s_, cy_ - s_, cx_ + s_, cy_ + s_), fill=(255, 224, 150, int(255 * (1 - u / 0.7))))
    return [Shot(4.6, md, mid, cam=cam, light=DAWNM, sun=(185, 1090, 520, (0.16, 0.08, 0.02)),
                 fx=[Embers(40, 703, (100, 950, 280, 1150), (40, 120)), sparks, Glow(lambda t: cam_xy(cam, t, 185, 1080), 300, (255, 150, 70), 0.35)],
                 grade="fire", bloom=0.7, fade_in=0.4, fade_out=0.5)]



# ================================================================ S3 the meadow at dawn: Faranak's story (12.2-48.4)
def s3():
    md = mead("dawn")
    mdb = mead("dawn", 8)
    camA = cam_push(1.0, 1.08, 560, 1300, 5.2)

    def midA(t):
        talk = 0.6 < t < 4.6
        f = P(turn=0.35, gx=0.8, gy=-0.3, sad=0.5, brow=0.6, furrow=-0.2, armL=("ik", 230, 300) if 1.2 < t < 4.2 else "relaxed", armR="chest",
              blink=blink_at(t, 1), breathe=math.sin(t * 2), mouth_o=max(0.0, 0.3 * math.sin(t * 9)) if talk else 0.0, wind=0.3)
        b = P(turn=-0.3, gx=-0.8, gy=0.35, sad=0.3, brow=0.5, furrow=0.0, armL="relaxed", armR="relaxed", blink=blink_at(t, 2),
              breathe=math.sin(t * 2 + 1), wind=0.3)
        return at_feet(FEREYDUN, b, t, 690, 1600, 0.46) + at_feet(FARANAK, f, t, 410, 1610, 0.44)
    A = Shot(5.2, md, midA, cam=camA, light=DAWNL, sun=SUN_DAWN, fx=[mist(0.4, 71), Motes(40, 704, (255, 240, 210), (0, 900, W, 1700), (6, -10), amax=100)],
             fade_in=0.5)

    LB = [("p7s3b", 0.2), ("p7s3c", 4.2)]

    def midB(t):
        fond = ease((t - 1.6) / 0.6) * (1 - ease((t - 3.8) / 0.6))
        f = tp(LB, t, 3, turn=0.3, gx=0.7, gy=0.05, sad=0.55 - 0.3 * fond, smile=0.35 * fond, brow=0.6, furrow=-0.3,
               armL="relaxed", armR="chest" if t > 4.4 else "relaxed", wind=0.4)
        return at_neck(FARANAK, f, t, 500, 1010, 1.05)
    B = Shot(7.6, mdb, midB, cam=cam_push(1.0, 1.05, 500, 860, 7.6), light=dict(DAWNL, ramp=None), sun=SUN_DAWN)

    # memory 1: Abtin led away by Zahhak's men on the road at dusk
    road = bg("damavand_dusk_road", lambda: zbg.damavand("dusk", road=True))
    camC = cam_push(1.0, 1.06, 560, 1350, 4.4)

    def bodyC(t):
        u = t / 4.4
        o = ""
        for k, (S, dx, dy, kw) in enumerate(((ZGUARD, -135, -10, dict(armL=(20, 10), propL="pike", armR="forward")),
                                             (ZGUARD, 135, -10, dict(armL=(20, 10), propL="pike", armR="forward")),
                                             (ABTIN, 0, 18, dict(armL="chest", armR="chest", chains="rope", gy=0.6, sad=0.6)))):
            sc = lerp(0.44, 0.3, u)
            x = lerp(560, 600, u) + dx * sc / 0.44
            y = lerp(1610, 1400, u) + dy * sc / 0.44
            q = P(legs="walk", phase=t * 5.0 + k * 1.3, turn=0.05, gx=0.0, blink=0.0, wind=0.6, **kw)
            o += at_feet(S, q, t, x, y, sc)
        return o
    C = Shot(4.4, road, None, cam=camC, sun=(170, 1030, 900, (0.16, 0.08, 0.03)),
             fx=[silhouette(camC, bodyC, fill=(30, 16, 22), glow=(255, 170, 100), blur=6, ga=0.7), memory_fx()], grade="warm", bloom=0.6,
             fade_in=0.4, fade_out=0.3)

    # memory 2: the cow in the meadow and the dust of the riders; the burning house
    mday = mead("day", tall=True)
    camD1 = cam_push(1.0, 1.04, 560, 1300, 1.9, py0=-420, py1=-420)
    from p06_scenes import barmayeh, sparkles

    def midD1(t):
        look = ease((t - 0.6) / 0.5)
        return barmayeh(t, 560, 1470, 0.8, graze=0.6 * (1 - look)) + sparkles(t, 560, 1160, 460, 220, 10, 4)

    dust = dust_tex()

    def dustD(im, t):
        x = int(1100 - 260 * t)
        d = dust.crop((x, 0, x + W, H)).transform((W, H), Image.AFFINE, (1, 0, 0, 0, 1, 520))
        d.putalpha(d.getchannel("A").point(lambda v: int(v * min(0.8, 0.2 + t / 1.6))))
        im.alpha_composite(d)
    D1 = Shot(1.9, mday, midD1, cam=camD1, bg_par=1.0, light=dict(rim=(5, -2), rim_col=(1.0, 0.9, 0.7), ambient=(1.0, 0.98, 0.95)),
              fx=[dustD, memory_fx()], grade="warm", fade_in=0.3)

    door_night = bgs.cached("zh_house_door_night", night_of(lambda: bgs.cached("house_door", bgs.house_door), (6, 10, 30), 170))
    camD2 = cam_push(1.0, 1.06, 450, 1000, 2.3)

    def midD2(t):
        o = '<rect x="320" y="660" width="260" height="740" fill="#ff8a2a" opacity="0.55"/>'
        for k, (x, y, sz) in enumerate(((450, 1400, 130), (200, 400, 150), (520, 380, 170), (700, 420, 130), (450, 820, 90))):
            o += fire_svg(x, y, sz, t + k * 0.7, k)
        return o

    def smoke(im, t):
        layer = Image.new("RGBA", (W, H))
        d = ImageDraw.Draw(layer, "RGBA")
        for k in range(14):
            age = (t * 0.6 + k * 0.17) % 1.0
            x = 200 + 50 * k + 40 * math.sin(age * 4 + k); y = 380 - age * 420; r_ = 50 + age * 130
            d.ellipse((x - r_, y - r_, x + r_, y + r_), fill=(60, 50, 56, int(90 * (1 - age))))
        im.alpha_composite(layer.filter(ImageFilter.GaussianBlur(18)))
    D2 = Shot(2.3, door_night, midD2, cam=camD2, light=dict(rim=(0, 0)),
              fx=[smoke, Embers(60, 705, (100, 300, 800, 1400), (120, 260)), Glow(lambda t: cam_xy(camD2, t, 450, 800), 520, (255, 140, 60), 0.45),
                  memory_fx(0.4)], grade="fire", bloom=0.8, fade_out=0.3)

    LE = [("p7s3f", 0.2)]

    def midE(t):
        up = ease(t / 0.5)
        fist = ease((t - 2.9) / 0.3)
        q = tp(LE, t, 4, turn=-0.25, gx=-0.6, gy=0.0, furrow=1.0 + 0.6 * fist, brow=-0.5, sad=0.0, armL="relaxed",
               armR="fist_up" if fist > 0.5 else ("chest" if t > 0.8 else "relaxed"), wind=0.5)
        return at_neck(FEREYDUN, q, t, 560, lerp(1150, 1030, up), 1.1)
    E = Shot(4.2, mdb, midE, cam=cam_push(1.0, 1.05, 560, 860, 4.2), light=dict(DAWNL, ramp=None), sun=SUN_DAWN)

    LF = [("p7s3g", 0.1)]

    def midF(t):
        f = tp(LF, t, 5, turn=0.3, gx=0.7, gy=-0.5, sad=0.7, brow=1.0, furrow=-0.5, armL="relaxed", armR="offer" if t > 0.5 else "relaxed", wind=0.4)
        return at_neck(FARANAK, f, t, 500, 1010, 1.05)
    F = Shot(3.4, mdb, midF, cam=cam_push(1.0, 1.04, 500, 860, 3.4), light=dict(DAWNL, ramp=None), sun=SUN_DAWN)

    LG = [("p7s3h", 0.2)]
    camG = cam_push(1.04, 1.1, 540, 1350, 3.4)

    def midG(t):
        f = tp(LG, t, 6, turn=0.35, gx=0.8, gy=-0.4, sad=0.5, brow=0.8, furrow=-0.4, smile=0.2 * ease((t - 2.0) / 0.5),
               armL=("ik", 300, 230), armR="chest", wind=0.4)
        b = tp([], t, 7, turn=-0.3, gx=-0.7, gy=0.35, furrow=0.8 - 0.6 * ease((t - 1.0) / 1.5), brow=0.2, sad=0.3, armL="relaxed", armR="relaxed", wind=0.5)
        return at_feet(FEREYDUN, b, t, 660, 1640, 0.5) + at_feet(FARANAK, f, t, 420, 1650, 0.48)
    G = Shot(3.4, md, midG, cam=camG, light=DAWNL, sun=SUN_DAWN, fx=[mist(0.3, 72)])

    LH = [("p7s3i", 0.4)]

    def midH(t):
        q = tp(LH, t, 8, turn=0.3, gx=0.8, gy=-0.3, furrow=0.6, brow=0.1, sad=0.1, armL="relaxed", armR="relaxed", wind=0.7)
        return at_neck(FEREYDUN, q, t, 500, 1030, 1.1)
    H_ = Shot(3.8, mdb, midH, cam=cam_push(1.0, 1.06, 500, 860, 3.8), light=dict(DAWNL, ramp=None), sun=SUN_DAWN,
              fx=[Motes(30, 706, (255, 240, 210), (0, 400, W, 1500), (10, -6), amax=90)], fade_out=0.6)
    return [A, B, C, D1, D2, E, F, G, H_]



# ================================================================ S4 the sleepless king; the great men; the paper (48.4-72.0)
def desk():
    """the paper insert: Zahhak's black table in torchlight, seen from above; the hall dark and blurred at the top"""
    s_ = ("<defs>" + bgs.FILTERS + bgs.lg("dk", [(0, "#120e14", 1), (1, "#060408", 1)]) + bgs.lg("tb", [(0, "#2a1c22", 1), (1, "#0e0a0e", 1)]) +
          bgs.rg("tg", 180, 380, 520, [(0, "#ffae5a", 0.45), (0.5, "#a0502a", 0.12), (1, "#000", 0)]) +
          bgs.rg("tg2", 540, 760, 700, [(0, "#ffb870", 0.22), (1, "#000", 0)]) + "</defs>")
    s_ += f'<rect width="{W}" height="{H}" fill="url(#dk)"/><rect width="{W}" height="{H}" fill="url(#tg)"/>'
    s_ += '<g filter="url(#b12)">' + "".join(f'<rect x="{x}" y="0" width="70" height="420" fill="#1c1820"/>' for x in (60, 950)) + \
          f'<g transform="translate(540,200) scale(1.4)">{zbg.serpent_emblem(0, 0, 1.0)}</g></g>'
    s_ += '<path d="M -40 400 L 1120 400 L 1120 1920 L -40 1920 Z" fill="url(#tb)"/><rect x="0" y="400" width="1080" height="1520" fill="url(#tg2)"/>'
    s_ += '<path d="M -40 440 L 1120 440" stroke="#c9a24a" stroke-width="10"/><path d="M -40 462 L 1120 462" stroke="#c9a24a" stroke-width="3"/>'
    r = random.Random(77)
    for k in range(50):
        x = r.uniform(-60, 1140); y = r.uniform(500, 1900); sc = 0.6 + (y - 500) / 900
        s_ += f'<path d="M {x:.0f} {y - 9 * sc:.0f} L {x + 9 * sc:.0f} {y:.0f} L {x:.0f} {y + 9 * sc:.0f} L {x - 9 * sc:.0f} {y:.0f} Z" fill="#c9a24a" opacity="0.3"/>'
    return svg_render(s_)


PAPER = ((180, 430), (900, 416), (950, 1000), (130, 1014))


def _paper_at(u, v):
    tl, tr, br, bl = PAPER
    top = (lerp(tl[0], tr[0], u), lerp(tl[1], tr[1], u)); bot = (lerp(bl[0], br[0], u), lerp(bl[1], br[1], u))
    return lerp(top[0], bot[0], v), lerp(top[1], bot[1], v)


def sig_pts(k, seed=4, lw=1.6):
    """the points of signature k on PAPER, as sheet() draws them"""
    u0 = 0.1 + (k % 3) * 0.28; v0 = 0.72 + (k // 3) * 0.1
    x0, y0 = _paper_at(u0, v0); x1, y1 = _paper_at(u0 + 0.2, v0 - 0.02)
    d = _wavy(x0, y0, x1, y1, seed * 31 + k, 7 * lw)
    return [tuple(float(v) for v in pt.split()) for pt in d[2:].split(" L ")]


def signing_hand(px, py, col, cuff="#c9a24a", skin="tan", out=0.0):
    """a noble's hand signing with a reed pen whose tip is at (px, py); the sleeve comes in from the bottom right; out 0..1 slides it away"""
    sk = SKINS[skin]
    dx, dy = 700 * out, 800 * out
    tx, ty = px + dx, py + dy                       # pen tip
    hx, hy = tx + 96, ty + 104                      # the fist round the pen
    ux, uy = 0.66, 0.75                             # along the forearm (down-right)
    nx, ny = -uy, ux                                # across it
    w0, w1, L = 62, 84, 900
    pts = [(hx + ux * 40 + nx * w0, hy + uy * 40 + ny * w0), (hx + ux * L + nx * w1, hy + uy * L + ny * w1),
           (hx + ux * L - nx * w1, hy + uy * L - ny * w1), (hx + ux * 40 - nx * w0, hy + uy * 40 - ny * w0)]
    sleeve = "M " + " L ".join(f"{x:.1f} {y:.1f}" for x, y in pts) + " Z"
    c0 = (hx + ux * 52 + nx * (w0 + 6), hy + uy * 52 + ny * (w0 + 6)); c1 = (hx + ux * 52 - nx * (w0 + 6), hy + uy * 52 - ny * (w0 + 6))
    return (f'<path d="{sleeve}" fill="{col}" stroke="{OUT}" stroke-width="3.4"/>'
            f'<path d="M {pts[0][0]:.1f} {pts[0][1]:.1f} L {pts[1][0]:.1f} {pts[1][1]:.1f}" stroke="#000" stroke-width="18" opacity="0.18"/>'
            f'<path d="M {c0[0]:.1f} {c0[1]:.1f} L {c1[0]:.1f} {c1[1]:.1f}" stroke="{cuff}" stroke-width="30" stroke-linecap="round"/>'
            f'<path d="M {tx:.1f} {ty:.1f} L {hx + 10:.1f} {hy + 8:.1f}" stroke="#a8743a" stroke-width="11" stroke-linecap="round"/>'
            f'<path d="M {tx:.1f} {ty:.1f} L {tx + 16:.1f} {ty + 18:.1f}" stroke="#1a1430" stroke-width="10" stroke-linecap="round"/>'
            f'<ellipse cx="{hx + 4:.1f}" cy="{hy + 2:.1f}" rx="66" ry="50" transform="rotate(-40,{hx + 4:.1f},{hy + 2:.1f})" fill="{sk[0]}" stroke="{OUT}" stroke-width="3.4"/>'
            f'<path d="M {hx - 40:.1f} {hy - 10:.1f} C {hx - 30:.1f} {hy + 20:.1f}, {hx - 6:.1f} {hy + 38:.1f}, {hx + 22:.1f} {hy + 44:.1f}" stroke="{sk[1]}" stroke-width="4" fill="none"/>'
            f'<ellipse cx="{hx - 26:.1f}" cy="{hy - 26:.1f}" rx="26" ry="17" transform="rotate(-40,{hx - 26:.1f},{hy - 26:.1f})" fill="{sk[2]}" stroke="{OUT}" stroke-width="3"/>')


def s4():
    bed = bg("bedchamber", zbg.bedchamber)
    bedb = bg("bedchamber", zbg.bedchamber, 8)
    camA = cam_push(1.0, 1.06, 560, 900, 3.6)

    def midA1(t):
        z = P(legs="sit", turn=0.05, gx=0.5 * math.sin(t * 0.9), gy=-0.1, brow=1.0, furrow=-0.5, sad=0.6, armL="relaxed", armR="relaxed",
              blink=min(0.3, blink_at(t, 1)), breathe=math.sin(t * 2.6), wind=0.0, snake_rise=0.9,
              snake_looks=(0.4 + 0.5 * math.sin(t * 1.9), 0.3 + 0.6 * math.sin(t * 1.5 + 1)),
              hisses=(0.4 * max(0.0, math.sin(t * 2.2)), 0.4 * max(0.0, math.sin(t * 1.8 + 2))))
        return torch_flame(70, 975, t, 0.5, 2) + at_neck(ZAHHAK_NIGHT, z, t, 560, 1190 - 575 * 0.52, 0.52)
    A1 = Shot(3.6, bed, midA1, cam=camA, light=LAMP, fx=[Glow(lambda t: cam_xy(camA, t, 70, 930), 220, (255, 170, 90), 0.4)], grade="night",
              bloom=0.4, fade_in=0.4)

    LA2 = [("p7s4b", 0.3)]

    def midA2(t):
        z = tp(LA2, t, 2, turn=-0.05, gx=-0.4 + 0.5 * math.sin(t * 1.1), gy=-0.2, brow=1.2, furrow=-0.7, sad=0.7, armL="relaxed", armR="relaxed",
               snake_looks=(0.6 + 0.4 * math.sin(t * 2.1), 0.5 + 0.5 * math.sin(t * 1.8 + 1)),
               hisses=(0.3 * max(0.0, math.sin(t * 2.3)), 0.3 * max(0.0, math.sin(t * 2.0 + 2))))
        z["blink"] = min(z["blink"], 0.25)
        return at_neck(ZAHHAK_NIGHT, z, t, 540, 1030, 1.15)
    A2 = Shot(3.0, bedb, midA2, cam=cam_push(1.0, 1.08, 540, 860, 3.0), light=dict(LAMP, rim=(-5, -2), rim_col=(1.0, 0.62, 0.32), rim_str=0.8),
              grade="night", bloom=0.4, fade_out=0.3)

    hall = bg("hall", zbg.hall)
    camB = cam_push(1.0, 1.05, 540, 1100, 6.4)

    def midB(t):
        o = torches_wide(t) + at_neck(ZAHHAK_KING, throne_zk(t, 3), t, 540, 793, 0.36) + guards_hall(t, 30) + kondrow_at(t)
        u = ease(t / 3.6)
        for k, (S, x, side) in enumerate(NOB_L + NOB_R):
            walking = u < 1
            x0 = -140 - 80 * k if side > 0 else 1220 + 80 * (k - 3)
            xx = lerp(x0, x, u)
            q = P(turn=0.42 * side, gx=0.7 * side, gy=-0.2, brow=0.6, furrow=-0.2, sad=0.4, legs="walk" if walking else "stand", phase=t * 4.6 + k,
                  armL="chest", armR="relaxed", blink=blink_at(t, 20 + k), breathe=math.sin(t * 2 + k), nod=10 * ease((t - 3.8 - 0.1 * k) / 0.5))
            o += at_feet(S, q, t, xx, 1520 + 18 * (k % 2), 0.36)
        return o
    B = Shot(6.4, hall, midB, cam=camB, light=HALL, fx=hall_fx(camB, [(80, 640), (1000, 640)], 704), grade="fire", bloom=0.6, fade_in=0.3)

    close = bg("hall_close", zbg.hall_close)
    LC = [("p7s4d", 0.2), ("p7s4e", 2.9)]
    camC = cam_push(1.0, 1.06, 540, 860, 5.4)

    def midC(t):
        cmd = ease((t - 2.9) / 0.3)
        q = tp(LC, t, 4, turn=0.05, gx=0.1, gy=0.1, furrow=0.5 + 0.5 * cmd, brow=0.1 - 0.5 * cmd, smile=0.3 * (1 - cmd), nod=4 * (1 - cmd),
               armL="relaxed", armR="point" if t > 3.0 else ("offer" if 0.6 < t < 2.4 else "relaxed"),
               snake_looks=(0.8, 0.9), hisses=(0.8 * cmd * (0.6 + 0.4 * math.sin(t * 5)), 0.8 * cmd * (0.6 + 0.4 * math.sin(t * 4 + 1))))
        return torches_close(t) + at_neck(ZAHHAK_KING, q, t, 540, 1030, 1.0)
    C = Shot(5.4, close, midC, cam=camC, light=TORCH, fx=hall_fx(camC, [(40, 740), (1040, 740)], 705), grade="fire", bloom=0.6)

    dsk = bgs.cached("zh_p7_desk", desk)
    SIGN = ((0.7, "#3a5a6a", "tan"), (2.0, "#1f6a6a", "light"), (3.3, "#b8642a", "old"))

    def midD(t):
        done = sum(1 for t0, _, _ in SIGN if t > t0 + 1.0)
        o = sheet(*PAPER, seed=4, sigs=done, seal=True, lw=1.6)
        for k, (t0, col, skin) in enumerate(SIGN):
            if t0 - 0.45 < t < t0 + 1.45:
                pts = sig_pts(k)
                u = min(1.0, max(0.0, (t - t0) / 1.0))
                n = max(2, int(u * (len(pts) - 1)) + 1)
                part = pts[:n]
                if 0 < u < 1:
                    o += '<path d="M ' + " L ".join(f"{x:.1f} {y:.1f}" for x, y in part) + '" stroke="#1a1430" stroke-width="4.2" fill="none"/>'
                tip = part[-1] if u > 0 else pts[0]
                slide = 1 - ease((t - t0 + 0.45) / 0.4) if t < t0 else ease((t - t0 - 1.05) / 0.4)
                o += signing_hand(tip[0], tip[1], col, skin=skin, out=slide)
        return o
    D = Shot(5.2, dsk, midD, cam=cam_push(1.0, 1.04, 540, 760, 5.2), light=dict(rim=(-4, -3), rim_col=(1.0, 0.7, 0.4), rim_str=0.6, ambient=(0.92, 0.86, 0.84)),
             fx=[Glow(lambda t: (180, 380), 300, (255, 170, 90), 0.3)], grade="fire", bloom=0.4, fade_out=0.3)
    return [A1, A2, B, C, D]



# ================================================================ S5 Kaveh (72.0-129.4)
def floor_scraps(x, y, n=9, seed=0, s=1.0):
    """torn bits of the paper lying on the floor around (x, y)"""
    r = random.Random(seed)
    o = ""
    for k in range(n):
        px, py = x + r.uniform(-130, 130) * s, y + r.uniform(-24, 24) * s
        w_, h_ = r.uniform(26, 44) * s, r.uniform(8, 14) * s
        a = r.uniform(-30, 30)
        o += (f'<rect x="{px - w_ / 2:.1f}" y="{py - h_ / 2:.1f}" width="{w_:.1f}" height="{h_:.1f}" fill="#efe2bf" stroke="#3a2a1a" stroke-width="1.2" '
              f'transform="rotate({a:.1f},{px:.1f},{py:.1f})"/>')
    return o


def s5():
    hall = bg("hall", zbg.hall)
    hallb = bg("hall", zbg.hall, 6)
    close = bg("hall_close", zbg.hall_close)

    # A: fists on the door; every head turns to it (the door is off to the left)
    camA = shake(cam_push(1.0, 1.04, 540, 1100, 3.0), BANGS[0], BANGS[-1] + 0.4, 6)

    def midA(t):
        look = -ease((t - 0.35) / 0.4)
        z = throne_zk(t, 5, gx=lerp(0.0, -0.9, -look), turn=lerp(0.0, -0.2, -look), furrow=0.9, brow=0.2 * -look,
                      snake_looks=(1.0, 1.0), hisses=(0.6 * -look, 0.6 * -look))
        return (torches_wide(t) + at_neck(ZAHHAK_KING, z, t, 540, 793, 0.36) + guards_hall(t, 31) + kondrow_at(t, gx=lerp(-0.6, -0.9, -look)) +
                nobles(t, look=look, seed=40, fear=0.4 * -look))
    A = Shot(3.0, hall, midA, cam=camA, light=HALL, fx=hall_fx(camA, [(80, 640), (1000, 640)], 706), grade="fire", bloom=0.6)

    LB = [("p7s5b", 0.1)]
    camB = cam_push(1.0, 1.05, 540, 860, 3.6)

    def midB(t):
        q = tp(LB, t, 6, turn=-0.15, gx=-0.6, gy=0.0, furrow=1.0, brow=-0.4, armL="relaxed", armR="point" if t > 1.6 else "relaxed",
               snake_looks=(1.0, 1.0), hisses=(0.7 * (0.6 + 0.4 * math.sin(t * 5)), 0.7 * (0.6 + 0.4 * math.sin(t * 4 + 1))))
        return torches_close(t) + at_neck(ZAHHAK_KING, q, t, 540, 1030, 1.0)
    B = Shot(3.6, close, midB, cam=camB, light=TORCH, fx=hall_fx(camB, [(40, 740), (1040, 740)], 707), grade="fire", bloom=0.6)

    # C: Kaveh marches in between two guards and stops before the throne
    LC = [("p7s5c", 3.3)]
    camC = cam_push(1.0, 1.06, 540, 1150, 5.4)
    STOP = 2.9

    def midC(t):
        u = ease(min(t, STOP) / STOP)
        walking = t < STOP
        z = P(**talk_pose(LC, t, 7, zk_throne(t, 7, gx=-0.3 * (1 - u), gy=0.5, furrow=0.9)))
        kx, ky = lerp(-170, 540, u), lerp(1760, 1640, u)
        k = P(legs="walk" if walking else "stand", phase=t * 5.0, turn=0.35 * (1 - ease((t - STOP + 0.4) / 0.5)), gx=0.6 * (1 - u), gy=-0.5,
              furrow=1.0, brow=-0.4, armL="relaxed", armR=("ik", -90, 300) if walking else "chest", blink=blink_at(t, 8), wind=0.2)
        o = torches_wide(t) + at_neck(ZAHHAK_KING, z, t, 540, 793, 0.36) + guards_hall(t, 32) + kondrow_at(t)
        o += nobles(t, look=-0.6 * (1 - ease((t - STOP) / 0.6)), seed=41, fear=0.5)
        for j, (dx, dy) in enumerate(((-210, -30), (200, -30))):
            sidestep = ease((t - STOP) / 0.6) * (40 if dx > 0 else -40)
            g = P(legs="walk" if walking else "stand", phase=t * 5.0 + j * 2, turn=0.35 * (1 - u) if dx < 0 else 0.2 - 0.6 * u, gx=0.6 if dx < 0 else -0.3,
                  armL=(20, 10), propL="pike", armR="forward", furrow=0.7, blink=blink_at(t, 9 + j))
            o += at_feet(ZGUARD, g, t, kx + dx + sidestep, ky + dy, 0.4)
        o += at_feet(KAVEH, k, t, kx, ky, 0.42)
        return o
    C = Shot(5.4, hall, midC, cam=camC, light=HALL, fx=hall_fx(camC, [(80, 640), (1000, 640)], 708), grade="fire", bloom=0.6)

    # D, E: Kaveh speaks
    KL = dict(KCLOSE, ramp=(0, W, 1.04, 0.9))
    LD = [("p7s5d", 0.2), ("p7s5e", 4.3)]

    def midD(t):
        grief = ease((t - 4.2) / 0.5)
        q = kaveh_q(LD, t, 10, turn=0.2, gx=0.6, gy=-0.3, furrow=1.0 + 0.4 * (1 - grief), brow=-0.4 + 0.9 * grief, sad=0.6 * grief,
                    armL="point" if 0.3 < t < 1.8 else ("both_out" if 4.6 < t < 6.6 else "relaxed"), armR="chest" if 1.9 < t < 4.0 else "relaxed")
        return torch_flame(40, 740, t, 1.1) + torch_flame(1040, 740, t + 1.7, 1.1, 1) + at_neck(KAVEH, q, t, 540, 1060, 1.15)
    camD = cam_push(1.0, 1.05, 540, 860, 7.8)
    D = Shot(7.8, hallb, midD, cam=camD, light=KL, fx=hall_fx(camD, [(40, 740), (1040, 740)], 709), grade="fire", bloom=0.5)

    LE = [("p7s5f", 0.2)]

    def midE(t):
        fist = ease((t - 2.4) / 0.3)
        q = kaveh_q(LE, t, 11, turn=0.15, gx=0.5, gy=-0.35, furrow=1.4, brow=-0.2, sad=0.5, armR="fist_up" if fist > 0.5 else "relaxed",
                    armL="chest", wind=0.2)
        return at_neck(KAVEH, q, t, 540, 1110, 1.45)
    camE = cam_push(1.0, 1.05, 540, 860, 4.4)
    E = Shot(4.4, hallb, midE, cam=camE, light=KL, fx=hall_fx(camE, [(40, 740), (1040, 740)], 710), grade="fire", bloom=0.5)

    LF = [("p7s5g", 0.1)]

    def midF(t):
        surprise = 1 - ease((t - 0.8) / 0.6)
        q = tp(LF, t, 12, turn=0.05, gx=-0.2, gy=0.0, furrow=0.6 - 0.8 * surprise, brow=0.9 * surprise, armL="relaxed",
               armR="wave" if 0.9 < t < 2.2 else "relaxed", snake_looks=(0.9, 1.0), hisses=(0.2, 0.3))
        return torches_close(t) + at_neck(ZAHHAK_KING, q, t, 540, 1030, 1.0)
    camF = cam_push(1.0, 1.04, 540, 860, 3.2)
    F = Shot(3.2, close, midF, cam=camF, light=TORCH, fx=hall_fx(camF, [(40, 740), (1040, 740)], 711), grade="fire", bloom=0.6)

    # G: the son is brought in and runs to his father
    LG = [("p7s5h", 2.4)]
    camG = cam_push(1.55, 1.6, 540, 1500, 4.6, py0=-120, py1=-120)
    FREE, ARRIVE = 1.3, 2.25

    def midG(t):
        o = torches_wide(t) + at_neck(ZAHHAK_KING, zk_throne(t, 24, gx=-0.4, gy=0.6, furrow=0.6), t, 540, 793, 0.36)
        for S, x, side in (NOB_L[0], NOB_R[-1]):
            o += at_feet(S, P(turn=0.42 * side, gx=0.7 * side, gy=0.0, brow=0.7, sad=0.4, armL="chest", armR="relaxed", blink=blink_at(t, x)), t, x, 1530, 0.36)
        run = ease((t - FREE) / (ARRIVE - FREE))
        hug = ease((t - ARRIVE) / 0.3)
        sx = lerp(820, 600, run) if t > FREE else lerp(980, 820, ease(t / FREE))
        led = t < FREE
        son = tp(LG, t, 13, legs="walk" if (t < FREE or t < ARRIVE) else "stand", phase=t * (5 if led else 7.5), turn=-0.35, gx=-0.8,
                 gy=0.1 if led else -0.2, sad=0.6 * (1 - hug), smile=0.6 * hug, brow=0.5 + 0.4 * hug, furrow=-0.2,
                 armL="relaxed", armR="relaxed", tilt=-7 * hug, chains="rope" if led else False, lead=(160, 250) if led else None)
        if led:
            g = P(legs="walk", phase=t * 5, turn=-0.35, gx=-0.8, furrow=0.7, armL=(20, 10), propL="pike", armR=("ik", -120, 260), blink=blink_at(t, 14))
            o += at_feet(ZGUARD, g, t, sx + 120, 1640, 0.4)
        else:
            g = P(turn=-0.2, gx=-0.4, furrow=0.6, armL=(20, 10), propL="pike", armR="relaxed", blink=blink_at(t, 14))
            o += at_feet(ZGUARD, g, t, 940, 1620, 0.4)
        k = kaveh_q([], t, 15, turn=0.35, gx=0.8, gy=0.1, furrow=0.6 - 1.2 * hug, brow=0.3 + 0.6 * hug, sad=0.5 - 0.2 * hug, smile=0.4 * hug,
                    armL="both_out" if FREE < t < ARRIVE else (("ik", 260, 130) if hug else "relaxed"), armR=("ik", 200, 260) if hug else "relaxed")
        o += at_feet(KAVEH, k, t, 400, 1660, 0.42) + at_feet(KAVEH_SON, son, t, sx, 1650, 0.4)
        return o
    G = Shot(4.6, hall, midG, cam=camG, bg_par=1.0, light=HALL, fx=hall_fx(camG, [(80, 640), (1000, 640)], 712), grade="fire", bloom=0.6)

    LH = [("p7s5i", 0.1)]

    def midH(t):
        q = tp(LH, t, 16, turn=0.0, gx=-0.3, gy=0.1, furrow=0.4, brow=0.2, smile=0.45, nod=6, armL="relaxed", armR="offer" if t > 1.2 else "relaxed",
               snake_looks=(0.7 + 0.3 * math.sin(t * 1.4), 0.8), hisses=(0.0, 0.2))
        return torches_close(t) + at_neck(ZAHHAK_KING, q, t, 540, 1030, 1.0)
    camH = cam_push(1.0, 1.05, 540, 860, 3.0)
    H_ = Shot(3.0, close, midH, cam=camH, light=TORCH, fx=hall_fx(camH, [(40, 740), (1040, 740)], 713), grade="fire", bloom=0.6)

    # I: he reads it
    LI = [("p7s5j", 1.3)]
    XI, YI, SI = 540, 640, 0.95

    def midI(t):
        look_up = ease((t - 1.1) / 0.3)
        aR, aL = ("ik", -120, 215), ("ik", 120, 215)
        q = kaveh_q(LI, t, 17, turn=0.05, gx=0.35 * math.sin(t * 5) * (1 - look_up) + 0.4 * look_up, gy=0.75 - 0.95 * look_up,
                    furrow=0.5 + 0.9 * look_up, brow=0.2 + 0.5 * look_up, sad=0.2 * look_up, armR=aR, armL=aL)
        q["blink"] = min(q["blink"], 0.4)
        return (torch_flame(40, 740, t, 1.1) + torch_flame(1040, 740, t + 1.7, 1.1, 1) + at_neck(KAVEH, q, t, XI, YI, SI) +
                held_sheet(KAVEH, aR, aL, XI, YI, SI, t=t, seed=7))
    camI = cam_push(1.0, 1.04, 540, 760, 3.0)
    I = Shot(3.0, hallb, midI, cam=camI, light=KL, fx=hall_fx(camI, [(40, 740), (1040, 740)], 714), grade="fire", bloom=0.5)

    # J: "Shame on you all!" — and the great men look down
    LJ = [("p7s5k", 0.2)]

    def midJ1(t):
        sweep = math.sin(t * 1.6)
        q = kaveh_q(LJ, t, 18, turn=-0.3, gx=-0.85, gy=0.0, furrow=1.8, brow=-0.8, armR=(82 + 10 * sweep, 0), armL="relaxed", wind=0.2)
        q["mouth_o"] = max(q["mouth_o"], 0.15)
        return torch_flame(40, 740, t, 1.1) + torch_flame(1040, 740, t + 1.7, 1.1, 1) + at_neck(KAVEH, q, t, 600, 1060, 1.15)
    camJ1 = cam_push(1.0, 1.04, 560, 860, 2.6)
    J1 = Shot(2.6, hallb, midJ1, cam=camJ1, light=dict(KL, ramp=(0, W, 0.9, 1.04)), fx=hall_fx(camJ1, [(40, 740), (1040, 740)], 715), grade="fire", bloom=0.5)

    def midJ2(t):
        o = ""
        for k, (S, x, y, sc, side) in enumerate(((COURTIER, 150, 1770, 0.58, 1), (NOBLE_1, 400, 1800, 0.6, 1), (MOBED_1, 660, 1780, 0.58, -1),
                                                 (NOBLE_2, 920, 1770, 0.58, -1))):
            down = ease((t - 0.2 - 0.15 * k) / 0.5)
            q = P(turn=0.3 * side, gx=0.6 * side * (1 - down), gy=0.2 + 0.7 * down, nod=12 * down, brow=0.6, furrow=-0.3, sad=0.4 + 0.4 * down,
                  armL="chest", armR="chest" if k % 2 else "relaxed", blink=max(blink_at(t, 60 + k), 0.35 * down), breathe=math.sin(t * 2 + k))
            o += at_feet(S, q, t, x, y, sc)
        return o
    camJ2 = cam_push(1.0, 1.04, 540, 900, 1.8)
    J2 = Shot(1.8, hallb, midJ2, cam=camJ2, light=dict(HALL, point=None, rim=(-5, -2), rim_col=(1.0, 0.65, 0.35), rim_str=0.8),
              fx=hall_fx(camJ2, [(40, 740), (1040, 740)], 716), grade="fire", bloom=0.5)

    # K: he tears it up
    LK = [("p7s5l", 0.1)]
    XK, YK, SK = 540, 600, 1.0
    scrapsK = thrown_scraps(KAVEH, RIP2, XK, YK, SK, 73, size=62)

    def midK(t):
        return kaveh_tearing(t, LK, RIP2, XK, YK, SK, 19, scrapsK)
    camK = cam_push(1.0, 1.06, 540, 740, 3.4)
    K = Shot(3.4, hallb, midK, cam=shake(camK, RIP2, RIP2 + 0.5, 8), light=KL, fx=hall_fx(camK, [(40, 740), (1040, 740)], 717), grade="fire", bloom=0.6)

    # L: father and son walk out; the scraps on the floor; nobody moves
    camL = cam_push(1.04, 1.0, 540, 1150, 4.0)

    def midL(t):
        z = zk_throne(t, 20, gx=-0.7, gy=0.3, furrow=1.0, brow=0.4, snake_looks=(1.0, 1.0),
                      hisses=(0.8 * (0.6 + 0.4 * math.sin(t * 5)), 0.8 * (0.6 + 0.4 * math.sin(t * 4 + 1))))
        o = torches_wide(t) + at_neck(ZAHHAK_KING, z, t, 540, 793, 0.36) + guards_hall(t, 33) + kondrow_at(t, brow=1.0, furrow=-0.6)
        o += nobles(t, look=-0.8, seed=42, fear=0.9)
        o += floor_scraps(470, 1690, 11, 7, 1.0)
        u = ease(t / 3.6)
        for S, dx, dy, ph, sc in ((KAVEH_SON, -90, -8, 1.0, 0.4), (KAVEH, 0, 0, 0.0, 0.42)):
            q = P(legs="walk", phase=t * 5.0 + ph, turn=-0.4, gx=-0.9, gy=0.0, furrow=0.8, brow=-0.2 if S is KAVEH else 0.3, armL="relaxed",
                  armR="relaxed" if S is KAVEH_SON else ("ik", -160, 230), blink=blink_at(t, 21 + ph), wind=0.2)
            o += at_feet(S, q, t, lerp(400, -260, u) + dx, 1660 + dy, sc)
        return o
    L = Shot(4.0, hall, midL, cam=camL, light=HALL, fx=hall_fx(camL, [(80, 640), (1000, 640)], 718), grade="fire", bloom=0.6)

    LM = [("p7s5m", 0.1)]

    def midM(t):
        q = tp(LM, t, 22, turn=0.25, gx=0.6, gy=0.2, brow=0.7, furrow=-0.3, sad=0.4, nod=8, armL="chest", armR="relaxed")
        return at_neck(COURTIER2, q, t, 560, 1060, 1.3)
    camM = cam_push(1.0, 1.04, 560, 860, 2.6)
    M = Shot(2.6, hallb, midM, cam=camM, light=dict(HALL, point=None, rim=(-5, -2), rim_col=(1.0, 0.68, 0.38), rim_str=0.85, ramp=(0, W, 1.05, 0.86),
                                                     ambient=(0.86, 0.8, 0.84)), sun=(80, 700, 800, (0.10, 0.05, 0.02)), grade="fire", bloom=0.5)

    LN = [("p7s5n", 0.2)]

    def midN(t):
        q = tp(LN, t, 23, turn=-0.1, gx=-0.5, gy=0.05, furrow=-0.2, brow=0.9, sad=0.5, armL="relaxed", armR="relaxed",
               snake_looks=(0.6 + 0.4 * math.sin(t * 2.2), 0.5 + 0.5 * math.sin(t * 1.9 + 1)),
               hisses=(0.5 * max(0.0, math.sin(t * 2.6)), 0.5 * max(0.0, math.sin(t * 2.2 + 2))))
        q["blink"] = min(q["blink"], 0.3)
        return torches_close(t) + at_neck(ZAHHAK_KING, q, t, 540, 1030, 1.0)
    camN = cam_push(1.0, 1.1, 540, 860, 5.0)
    N = Shot(5.0, close, midN, cam=camN, light=TORCH, fx=hall_fx(camN, [(40, 740), (1040, 740)], 719) + [darken(0.25, 2.5, 9.0, (10, 4, 16))],
             grade="fire", bloom=0.6, fade_out=0.6)
    return [A, B, C, D, E, F, G, H_, I, J1, J2, K, L, M, N]



# ================================================================ S6 the market: the apron on the spear (129.4-148.6)
def apron_svg(hl, hr, t, length=330):
    """Kaveh's leather apron held up by its neck strap between two hands (screen points hl, hr), hanging down `length` px"""
    (x0, y0), (x1, y1) = hl, hr
    cx = (x0 + x1) / 2
    top = min(y0, y1) + 30
    w_ = max(120.0, abs(x1 - x0) * 0.7)
    sw = 8 * math.sin(t * 3)
    d = (f"M {cx - w_ * 0.35:.1f} {top:.1f} L {cx + w_ * 0.35:.1f} {top:.1f} L {cx + w_ * 0.5 + sw:.1f} {top + length * 0.35:.1f} "
         f"L {cx + w_ * 0.55 + sw:.1f} {top + length:.1f} Q {cx + sw:.1f} {top + length + 26:.1f} {cx - w_ * 0.55 + sw:.1f} {top + length:.1f} "
         f"L {cx - w_ * 0.5 + sw:.1f} {top + length * 0.35:.1f} Z")
    return (f'<path d="M {x0:.1f} {y0:.1f} Q {cx:.1f} {top - 40:.1f} {x1:.1f} {y1:.1f}" stroke="#3a2414" stroke-width="7" fill="none"/>'
            f'<path d="M {x0:.1f} {y0:.1f} L {cx - w_ * 0.35:.1f} {top:.1f} M {x1:.1f} {y1:.1f} L {cx + w_ * 0.35:.1f} {top:.1f}" stroke="#3a2414" stroke-width="7"/>'
            f'<path d="{d}" fill="#7a4524" stroke="{OUT}" stroke-width="3"/>'
            f'<path d="M {cx - w_ * 0.3:.1f} {top + length * 0.6:.1f} L {cx + w_ * 0.3:.1f} {top + length * 0.6:.1f}" stroke="#3a2414" stroke-width="3" opacity="0.5"/>')


def market_crowd(seed, n, y, s, x0, x1, turn_to=0.0):
    """a static row of market people looking towards the middle (no pointing arms)"""
    r = random.Random(seed)
    xs = sorted(r.uniform(x0, x1) for _ in range(n))
    body = ""
    for x in xs:
        S = random_spec(r, ("man", "man", "woman", "man", "boy"))
        arms = r.choice([("relaxed", "relaxed"), ("chest", "relaxed"), ("relaxed", "chest"), ("hip", "relaxed"), ("down", "down")])
        q = P(turn=turn_to + r.uniform(-0.12, 0.12), gx=turn_to * 2 + r.uniform(-0.3, 0.3), armR=arms[0], armL=arms[1], blink=0.0,
              brow=r.uniform(0.2, 0.6), furrow=r.uniform(-0.2, 0.3))
        body += at_feet(S, q, r.uniform(0, 3), x, y + r.uniform(-8, 8), s * r.uniform(0.93, 1.07))
    return svg_render(body)


class Cheering:
    """people of the market raising their fists and shouting"""
    def __init__(self, seed, spots):
        r = random.Random(seed)
        self.people = [(random_spec(r, ("man", "man", "woman", "man", "boy")), x, y, sc, r.uniform(0, 6.3), r.choice([-1, 1])) for x, y, sc in spots]

    def svg(self, t, cheer=1.0, look=(540, 900)):
        o = ""
        for k, (S, x, y, sc, ph, hand) in enumerate(sorted(self.people, key=lambda p: p[2])):
            up = cheer * (0.5 + 0.5 * math.sin(t * 3.2 + ph)) > 0.45
            side = 1 if look[0] > x else -1
            q = P(turn=0.3 * side, gx=0.7 * side, gy=-0.6 * cheer, brow=0.5 + 0.4 * cheer, furrow=-0.2, smile=0.4 * cheer,
                  mouth_o=cheer * max(0.0, 0.5 * math.sin(t * 7 + ph)), armR="fist_up" if (up and hand < 0) else "relaxed",
                  armL="fist_up" if (up and hand > 0) else "relaxed", blink=blink_at(t, k + 80), breathe=math.sin(t * 2 + ph), wind=0.3)
            o += at_feet(S, q, t, x, y, sc)
        return o


def s6():
    md = bg("market_day", lambda: zbg.market("day"))
    back = bgs.cached("zh_p7_crowd_back", lambda: market_crowd(701, 12, 1330, 0.3, 420, 1100, -0.2))
    side = bgs.cached("zh_p7_crowd_side", lambda: market_crowd(702, 6, 1430, 0.36, 760, 1110, -0.35))

    def crowd_bg(t, rows=(back, side)):
        im = md.copy()
        for k, row in enumerate(rows):
            im.alpha_composite(row, (0, int(2 * math.sin(t * 2 + k))))
        return im

    camA = cam_push(1.0, 1.06, 560, 1250, 4.6)
    walkers = [(random_spec(random.Random(710 + k), ("man", "woman", "man")), x0, x1, y, sc, ph) for k, (x0, x1, y, sc, ph) in
               enumerate(((1180, 800, 1500, 0.4, 0.0), (1260, 900, 1560, 0.42, 1.1), (900, 700, 1380, 0.33, 2.2), (1300, 980, 1640, 0.46, 3.0)))]

    def midA(t):
        u = ease(t / 3.4)
        o = ""
        for S, x0, x1, y, sc, ph in walkers:
            v = ease((t - 0.2 * ph) / 3.0)
            q = P(legs="walk" if 0 < v < 1 else "stand", phase=t * 5 + ph, turn=-0.4, gx=-0.8, gy=-0.1, brow=0.5, furrow=-0.1, armL="relaxed", armR="relaxed",
                  blink=blink_at(t, 30 + ph), wind=0.3)
            o += at_feet(S, q, t, lerp(x0, x1, v), y, sc)
        k = P(legs="walk" if u < 1 else "stand", phase=t * 5.0, turn=0.35, gx=0.7, gy=-0.1, furrow=1.0, brow=-0.3, armL="relaxed", armR="relaxed",
              blink=blink_at(t, 31), wind=0.3)
        son = P(legs="walk" if u < 1 else "stand", phase=t * 5.0 + 1.5, turn=0.35, gx=0.7, gy=-0.3, brow=0.4, armL="relaxed", armR="relaxed",
                blink=blink_at(t, 32), wind=0.3)
        o += at_feet(KAVEH_SON, son, t, lerp(-260, 300, u), 1590, 0.42) + at_feet(KAVEH, k, t, lerp(-120, 470, u), 1620, 0.44)
        return o
    A = Shot(4.6, crowd_bg, midA, cam=camA, light=DAYM, sun=SUN_DAY, fx=[Motes(40, 707, (255, 240, 210), (0, 600, W, 1500), (8, -6), amax=80)],
             fade_in=0.5)

    # B1: he takes off his apron and holds it up; B2: his hands tie it under the head of a spear
    camB = cam_push(1.0, 1.04, 540, 1000, 2.6)
    XB, YB, SB = 540, 1760, 0.62

    def midB1(t):
        off = ease((t - 0.45) / 0.55)
        if t < 0.45:
            q = kaveh_q([], t, 33, turn=0.0, gx=0.0, gy=0.2, furrow=0.8, armR=("ik", -125, -50), armL=("ik", 125, -50))
            return at_feet(KAVEH, q, t, XB, YB, SB)
        aL = ("ik", lerp(140, 330, off), lerp(-420, -330, off))
        q = kaveh_q([], t, 33, turn=0.1, gx=0.5 * off, gy=-0.3, furrow=1.0, brow=-0.2, armR="relaxed", armL=aL)
        hx, hy = hand_at(KAVEH_NOAPRON, aL, 1, XB, YB, SB)
        sw = 10 * math.sin(t * 4)
        w_, L = 140 * SB / 0.62, 340 * SB / 0.62
        apron = (f'<path d="M {hx - 20:.1f} {hy:.1f} L {hx - w_ * 0.3:.1f} {hy + 50:.1f} M {hx + 20:.1f} {hy:.1f} L {hx + w_ * 0.3:.1f} {hy + 50:.1f}" '
                 f'stroke="#3a2414" stroke-width="7"/>'
                 f'<path d="M {hx - w_ * 0.32:.1f} {hy + 46:.1f} L {hx + w_ * 0.32:.1f} {hy + 46:.1f} L {hx + w_ * 0.5 + sw:.1f} {hy + 46 + L * 0.35:.1f} '
                 f'L {hx + w_ * 0.55 + sw * 1.4:.1f} {hy + 46 + L:.1f} Q {hx + sw:.1f} {hy + 70 + L:.1f} {hx - w_ * 0.55 + sw * 1.4:.1f} {hy + 46 + L:.1f} '
                 f'L {hx - w_ * 0.5 + sw:.1f} {hy + 46 + L * 0.35:.1f} Z" fill="#7a4524" stroke="{OUT}" stroke-width="3"/>'
                 f'<path d="M {hx - w_ * 0.3:.1f} {hy + 46 + L * 0.62:.1f} L {hx + w_ * 0.3:.1f} {hy + 46 + L * 0.62:.1f}" stroke="#3a2414" stroke-width="3" opacity="0.5"/>')
        return at_feet(KAVEH_NOAPRON, q, t, XB, YB, SB) + apron
    B1 = Shot(2.6, crowd_bg, midB1, cam=camB, light=DAYM, sun=SUN_DAY)

    sky = bg("market_day", lambda: zbg.market("day"), 10)

    def midB2(t):
        c = Ctx(1.0)
        o = prop(c, "apron_spear", 540, 1400, 0, t)
        pull = ease((t - 1.2) / 0.3)
        for sd in (-1, 1):
            hx = 540 + sd * (150 + 30 * pull) + 10 * math.sin(t * 9 + sd) * (1 - pull)
            hy = 432 + 12 * math.cos(t * 9 + sd) * (1 - pull)
            o += (f'<path d="M {hx:.1f} {hy + 20:.1f} L {hx + sd * 420:.1f} {hy + 900:.1f} L {hx + sd * 620:.1f} {hy + 760:.1f} L {hx + sd * 60:.1f} {hy - 10:.1f} Z" '
                  f'fill="#4e4844" stroke="{OUT}" stroke-width="3"/>'
                  f'<path d="M {hx + sd * 10:.1f} {hy + 40:.1f} L {hx + sd * 64:.1f} {hy + 10:.1f}" stroke="#6a5a4a" stroke-width="26" stroke-linecap="round"/>'
                  f'<ellipse cx="{hx:.1f}" cy="{hy:.1f}" rx="50" ry="40" transform="rotate({sd * 30},{hx:.1f},{hy:.1f})" fill="{SKINS["tan"][0]}" stroke="{OUT}" stroke-width="3"/>'
                  f'<ellipse cx="{hx - sd * 30:.1f}" cy="{hy - 18:.1f}" rx="20" ry="13" transform="rotate({sd * 30},{hx - sd * 30:.1f},{hy - 18:.1f})" fill="{SKINS["tan"][2]}" stroke="{OUT}" stroke-width="2.4"/>')
        return o
    B2 = Shot(2.0, sky, midB2, cam=cam_push(1.0, 1.05, 540, 600, 2.0), light=dict(DAYM, ramp=None), sun=(170, 520, 900, (0.12, 0.09, 0.05)))

    # C: he raises the banner
    LC = [("p7s6c", 0.6)]
    fg = bgs.cached("zh_p7_heads", lambda: back_heads(721, 9, 1830, 0.7, col="#2a1e18", blur=4))
    camC = cam_push(1.0, 1.05, 540, 1100, 3.4)

    def midC(t):
        lift = ease((t - 0.2) / 0.7)
        aR = ("ik", lerp(-170, -150, lift), lerp(260, -470, lift)) if lift < 1 else "fist_up"
        q = kaveh_q(LC, t, 34, turn=0.05, gx=-0.2, gy=-0.5, furrow=1.2, brow=-0.1, armR=aR, armL="fist_up" if t > 1.4 else "relaxed", wind=0.6)
        q["mouth_o"] = max(q["mouth_o"], 0.2 if 0.6 < t < 2.6 else 0.0)
        son = P(turn=-0.3, gx=-0.5, gy=-0.8, brow=0.8, smile=0.3, armL="relaxed", armR="relaxed", blink=blink_at(t, 35), wind=0.4)
        return (at_feet(KAVEH_SON, son, t, 760, 1600, 0.4) +
                at_neck(KAVEH_NOAPRON, P(**dict(q, propR="apron_spear")), t, 520, 1010, 0.45))
    C = Shot(3.4, crowd_bg, midC, fg=fg, cam=camC, light=DAYM, sun=SUN_DAY, fx=[Motes(40, 708, (255, 240, 210), (0, 300, W, 1500), (10, -8), amax=90)])

    # D: the crowd cheers; the banner over the square; end card
    cheer = Cheering(722, [(150, 1480, 0.38), (330, 1470, 0.38), (760, 1470, 0.38), (940, 1480, 0.38),
                           (230, 1620, 0.46), (860, 1620, 0.46), (560, 1660, 0.4),
                           (110, 1770, 0.52), (340, 1790, 0.54), (760, 1790, 0.54), (980, 1770, 0.52)])
    camD = cam_push(1.08, 1.0, 540, 1150, 6.6)
    dust = dust_tex()
    rim = ('<path d="M 330 1350 L 330 1440 Q 540 1490 750 1440 L 750 1350 Z" fill="#b89a74" stroke="#3a2418" stroke-width="4"/>'
           '<ellipse cx="540" cy="1350" rx="210" ry="40" fill="#cdb48e" stroke="#3a2418" stroke-width="4"/>'
           '<ellipse cx="540" cy="1352" rx="150" ry="24" fill="#5a8aa0" opacity="0.8"/>'
           + "".join(f'<path d="M {x} 1372 L {x} 1450" stroke="#8a7050" stroke-width="3" opacity="0.7"/>' for x in (390, 450, 510, 570, 630, 690)))

    def midD(t):
        q = P(turn=0.0, gx=0.0, gy=-0.6, furrow=1.0, brow=0.2, smile=0.2, armR="fist_up", propR="apron_spear", armL="fist_up" if math.sin(t * 2.4) > 0 else "relaxed",
              mouth_o=max(0.0, 0.5 * math.sin(t * 5)), blink=blink_at(t, 36), wind=0.7)
        son = P(turn=0.2, gx=0.3, gy=-0.6, brow=0.6, smile=0.6, armL="fist_up" if math.sin(t * 2.4 + 1.5) > 0 else "relaxed", armR="relaxed",
                blink=blink_at(t, 37), wind=0.5)
        return (rim + at_feet(KAVEH_SON, son, t, 640, 1352, 0.34) + at_feet(KAVEH_NOAPRON, q, t, 500, 1356, 0.37) + cheer.svg(t, 1.0, (520, 900)))

    def dustD(im, t):
        x = int(400 + 40 * t)
        d = dust.crop((x, 0, x + W, H)).transform((W, H), Image.AFFINE, (1, 0, 0, 0, 1, 180))
        d.putalpha(d.getchannel("A").point(lambda v: int(v * 0.35)))
        im.alpha_composite(d)
    D = Shot(6.6, crowd_bg, midD, cam=camD, light=DAYM, sun=SUN_DAY, fx=[dustD, Motes(60, 709, (255, 236, 200), (0, 300, W, 1600), (12, -10), amax=110)],
             fade_out=0.8)
    return [A, B1, B2, C, D]


SCENES = {"s1": s1, "s2": s2, "s3": s3, "s4": s4, "s5": s5, "s6": s6}
