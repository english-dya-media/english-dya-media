"""Part 2 · The King's Cook — 2D cartoon. Timing matches zahhak/p02_audio.py
(scene starts s1 0, s2 8.0, s3 12.6, s4 33.8, s5 73.0, s6 97.4; end card 115.4; total 120.4)."""
import math, random
from PIL import Image, ImageFilter
from film import Shot, W, H, ease, lerp, talk_pose, blink_at, cam_push, cam_static, Motes, Embers, svg_render
from chars import pose, Ctx, fmt, hand
from stage import at_neck, at_feet, fire_svg, Glow, lw_for, random_spec
import bgs, zbg
from cast import *
from p01_scenes import P, bg, cam_xy, tp, darken, fade_to, pit_svg, PREDAWN

HALLDAY = dict(rim=(5, -2), rim_col=(1.0, 0.85, 0.6), ramp=(0, W, 0.92, 1.05), ambient=(1.0, 0.97, 0.93))
DIM = dict(ambient=(0.74, 0.7, 0.74), rim=(-5, -2), rim_col=(1.0, 0.7, 0.4), rim_str=0.9)
KITCH = dict(point=(320, 1080, 1000, 0.62, 1.15, (1.0, 0.55, 0.25)), rim_point=(320, 6), rim_col=(1.0, 0.62, 0.3), rim_str=0.9)
TABLE = dict(rim=(5, -2), rim_col=(1.0, 0.85, 0.6), ambient=(1.0, 0.97, 0.93))
SUNBEAM = (900, 400, 900, (0.10, 0.07, 0.03))


def dimmed(name, fn, a=110):
    return bgs.cached(f"zh_{name}_dim", lambda: Image.alpha_composite(bgs.cached(f"zh_{name}", fn), Image.new("RGBA", (W, H), (12, 8, 10, a))))


def glint(cam, pts, t0, t1):
    """a star of light on the eyes (screen fx); pts: mid-layer points"""
    def fx(im, t):
        a = math.sin(math.pi * min(1.0, max(0.0, (t - t0) / (t1 - t0))))
        if a <= 0.02:
            return
        from PIL import ImageDraw
        d = ImageDraw.Draw(im, "RGBA")
        for (x, y) in pts:
            sx, sy = cam_xy(cam, t, x, y)
            r = 26 * a
            d.polygon([(sx - r, sy), (sx - r * 0.12, sy - r * 0.12), (sx, sy - r), (sx + r * 0.12, sy - r * 0.12), (sx + r, sy),
                       (sx + r * 0.12, sy + r * 0.12), (sx, sy + r), (sx - r * 0.12, sy + r * 0.12)], fill=(255, 236, 160, int(230 * a)))
            d.ellipse((sx - 5 * a, sy - 5 * a, sx + 5 * a, sy + 5 * a), fill=(255, 255, 240, int(255 * a)))
    return fx


def eyes_of(x, y, s, turn=0.0):
    fx_ = 12 * turn
    return [(x + (-40 + fx_) * s, y - 178 * s), (x + (40 + fx_) * s, y - 178 * s)]


def steam(x, y, t, n=3, h=160, seed=0):
    o = ""
    for k in range(n):
        ph = (t * 0.6 + k / n + seed * 0.37) % 1.0
        xx = x + (k - (n - 1) / 2) * 34 + 14 * math.sin(t * 2 + k)
        yy = y - ph * h
        o += (f'<path d="M {xx:.1f} {yy + 40:.1f} C {xx - 16:.1f} {yy + 20:.1f}, {xx + 16:.1f} {yy:.1f}, {xx:.1f} {yy - 30:.1f}" stroke="#ffffff" stroke-width="10" '
              f'fill="none" stroke-linecap="round" opacity="{0.35 * math.sin(math.pi * ph):.2f}"/>')
    return o


def keys_svg(x, y, ang=0.0, s=1.0):
    o = f'<g transform="translate({x:.1f},{y:.1f}) rotate({ang:.1f}) scale({s:.3f})">'
    o += '<circle cx="0" cy="0" r="26" fill="none" stroke="#c9a24a" stroke-width="7"/>'
    for k, a in enumerate((-40, 10, 60)):
        r_ = math.radians(a)
        x1, y1 = 26 * math.cos(r_), 26 * math.sin(r_)
        x2, y2 = 100 * math.cos(r_), 100 * math.sin(r_)
        o += (f'<path d="M {x1:.1f} {y1:.1f} L {x2:.1f} {y2:.1f}" stroke="#b9832f" stroke-width="8" stroke-linecap="round"/>'
              f'<path d="M {x2:.1f} {y2:.1f} l {12 * math.cos(r_ + 1.57):.1f} {12 * math.sin(r_ + 1.57):.1f}" stroke="#b9832f" stroke-width="8"/>'
              f'<circle cx="{x1 * 1.6:.1f}" cy="{y1 * 1.6:.1f}" r="9" fill="#e0b84e" stroke="#5a3a14" stroke-width="2"/>')
    return o + '</g>'


# ---------------------------------------------------------------- the dishes (drawn big, at (x, y) = the middle of the dish)
def platter(x, y, rx=300, col="#c0703a", rim="#8a4a1e"):
    return (f'<ellipse cx="{x}" cy="{y + 20}" rx="{rx + 10}" ry="{rx * 0.3 + 6:.0f}" fill="#000" opacity="0.25"/>'
            f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{rx * 0.3:.0f}" fill="{col}" stroke="#2a1408" stroke-width="5"/>'
            f'<ellipse cx="{x}" cy="{y}" rx="{rx * 0.82:.0f}" ry="{rx * 0.24:.0f}" fill="{rim}" opacity="0.45"/>')


def dish_plants(x, y, t):
    o = platter(x - 160, y + 60, 200, "#b88a5a", "#8a6a3a")
    for k, (dx, dy) in enumerate([(-260, 40), (-160, 20), (-60, 46)]):           # flat breads
        o += f'<ellipse cx="{x + dx}" cy="{y + dy}" rx="110" ry="40" fill="#e0b070" stroke="#5a3a14" stroke-width="4"/>' \
             f'<path d="M {x + dx - 70} {y + dy - 6} C {x + dx - 20} {y + dy - 20}, {x + dx + 20} {y + dy - 20}, {x + dx + 70} {y + dy - 6}" stroke="#a87a3a" stroke-width="4" fill="none"/>'
    o += platter(x + 190, y + 40, 170, "#d8d0c0", "#a8a090")
    for k, (dx, dy, col) in enumerate([(130, 0, "#b8202a"), (220, 10, "#c8302a"), (170, -40, "#7a2a6a"), (260, -30, "#7a2a6a"), (110, -50, "#6a9a3a")]):
        o += f'<circle cx="{x + dx}" cy="{y + dy}" r="44" fill="{col}" stroke="#2a0a0a" stroke-width="4"/><circle cx="{x + dx - 14}" cy="{y + dy - 14}" r="10" fill="#ffffff" opacity="0.35"/>'
    for k in range(7):                                                          # a bunch of herbs
        a = -1.2 + k * 0.4
        o += f'<path d="M {x - 40} {y + 160} Q {x - 40 + 60 * math.cos(a)} {y + 80}, {x - 40 + 140 * math.cos(a):.0f} {y + 60 + 60 * math.sin(a):.0f}" stroke="#4a7a2a" stroke-width="10" fill="none" stroke-linecap="round"/>'
    return o


def dish_eggs(x, y, t):
    o = (f'<ellipse cx="{x}" cy="{y + 40}" rx="250" ry="70" fill="#000" opacity="0.25"/>'
         f'<path d="M {x - 240} {y - 10} L {x + 240} {y - 10} C {x + 220} {y + 150}, {x - 220} {y + 150}, {x - 240} {y - 10} Z" fill="#f4f0e8" stroke="#2a2420" stroke-width="5"/>'
         f'<path d="M {x - 200} {y + 50} C {x - 100} {y + 80}, {x + 100} {y + 80}, {x + 200} {y + 50}" stroke="#2f8a96" stroke-width="10" fill="none"/>'
         f'<ellipse cx="{x}" cy="{y - 10}" rx="238" ry="56" fill="#e8e2d4" stroke="#2a2420" stroke-width="4"/>')
    for k, (dx, dy) in enumerate([(-120, -14), (-30, -26), (70, -10), (150, -24), (-70, 10), (40, 14)]):
        o += (f'<ellipse cx="{x + dx}" cy="{y + dy}" rx="46" ry="26" fill="#f2a414" stroke="#8a4a08" stroke-width="3"/>'
              f'<ellipse cx="{x + dx - 12}" cy="{y + dy - 8}" rx="14" ry="7" fill="#ffe8a0" opacity="0.8"/>')
    return o + steam(x, y - 40, t, 3, 200)


def roast_bird(x, y, s=1.0, col="#a8642a", flip=False):
    sx = -s if flip else s
    return (f'<g transform="translate({x},{y}) scale({sx},{s})">'
            f'<path d="M -120 0 C -120 -90, 60 -110, 110 -40 C 140 0, 100 50, 0 50 C -80 50, -120 30, -120 0 Z" fill="{col}" stroke="#3a1a08" stroke-width="5"/>'
            f'<path d="M -60 -60 C -20 -80, 40 -80, 80 -50" stroke="#e8a060" stroke-width="10" fill="none" opacity="0.6"/>'
            f'<path d="M 60 30 C 100 60, 140 60, 160 40 M 20 40 C 50 80, 90 90, 110 76" stroke="{col}" stroke-width="22" fill="none" stroke-linecap="round"/>'
            f'<path d="M 60 30 C 100 60, 140 60, 160 40 M 20 40 C 50 80, 90 90, 110 76" stroke="#3a1a08" stroke-width="3" fill="none"/>'
            f'<circle cx="164" cy="38" r="12" fill="#f4ecdc" stroke="#3a1a08" stroke-width="3"/><circle cx="114" cy="76" r="12" fill="#f4ecdc" stroke="#3a1a08" stroke-width="3"/></g>')


def dish_birds(x, y, t):
    o = platter(x, y + 30, 320)
    o += roast_bird(x - 120, y + 10, 1.0, "#9a5a24") + roast_bird(x + 130, y + 20, 0.8, "#b8742e", flip=True)
    for k in range(9):
        a = k * 0.7
        o += f'<ellipse cx="{x - 260 + k * 64:.0f}" cy="{y + 92 + 10 * math.sin(a):.0f}" rx="22" ry="10" fill="#4a7a2a" transform="rotate({20 * math.sin(a * 3):.0f},{x - 260 + k * 64:.0f},{y + 92:.0f})"/>'
    return o + steam(x, y - 60, t, 4, 200, 1)


def dish_chicken_lamb(x, y, t):
    o = platter(x, y + 30, 330, "#c9a24a", "#8a6a2a")
    o += roast_bird(x - 120, y + 10, 1.05, "#c07a32")
    for k in range(2):                                                          # lamb skewers
        y0 = y - 10 + k * 46
        o += f'<path d="M {x + 20} {y0 + 40} L {x + 320} {y0 - 30}" stroke="#7a7e86" stroke-width="7"/>'
        for j in range(4):
            cx_ = x + 70 + j * 62; cy_ = y0 + 28 - j * 15
            o += f'<rect x="{cx_ - 26}" y="{cy_ - 22}" width="52" height="44" rx="12" fill="#8a3a1e" stroke="#2a0e06" stroke-width="4"/>' \
                 f'<rect x="{cx_ - 18}" y="{cy_ - 16}" width="20" height="10" rx="4" fill="#c86a3a" opacity="0.7"/>'
    return o + steam(x, y - 60, t, 4, 200, 2)


def dish_stew(x, y, t):
    o = (f'<ellipse cx="{x}" cy="{y + 60}" rx="300" ry="80" fill="#000" opacity="0.25"/>'
         f'<path d="M {x - 280} {y - 10} L {x + 280} {y - 10} C {x + 260} {y + 180}, {x - 260} {y + 180}, {x - 280} {y - 10} Z" fill="#2f7a86" stroke="#123a40" stroke-width="5"/>'
         f'<path d="M {x - 240} {y + 60} C {x - 120} {y + 96}, {x + 120} {y + 96}, {x + 240} {y + 60}" stroke="#e8d8a0" stroke-width="8" fill="none"/>'
         f'<ellipse cx="{x}" cy="{y - 10}" rx="278" ry="64" fill="#1e5a62" stroke="#123a40" stroke-width="4"/>'
         f'<ellipse cx="{x}" cy="{y - 6}" rx="250" ry="52" fill="#e0901a"/>')
    r = random.Random(7)
    for k in range(9):                                                          # pieces of meat
        cx_ = x + r.uniform(-190, 190); cy_ = y - 6 + r.uniform(-30, 26)
        o += f'<ellipse cx="{cx_:.0f}" cy="{cy_:.0f}" rx="30" ry="16" fill="#8a3a1e" stroke="#3a1206" stroke-width="3"/>'
    for k in range(7):                                                          # rose petals
        cx_ = x + r.uniform(-200, 200); cy_ = y - 6 + r.uniform(-34, 30)
        o += f'<ellipse cx="{cx_:.0f}" cy="{cy_:.0f}" rx="16" ry="9" fill="#e86a8a" stroke="#8a2a4a" stroke-width="2" transform="rotate({r.uniform(-60, 60):.0f},{cx_:.0f},{cy_:.0f})"/>'
    o += (f'<path d="M {x + 300} {y - 220} C {x + 270} {y - 160}, {x + 270} {y - 60}, {x + 330} {y - 40} C {x + 390} {y - 60}, {x + 390} {y - 160}, {x + 360} {y - 220} Z" '
          f'fill="#f4b8c8" stroke="#6a2a3a" stroke-width="4" opacity="0.92"/><rect x="{x + 310}" y="{y - 270}" width="40" height="54" rx="8" fill="#f8d8e0" stroke="#6a2a3a" stroke-width="4"/>')
    return o + steam(x, y - 60, t, 5, 240, 3)


# ================================================================ S1 the hook (0-8.0)
def s1():
    dimc = dimmed("palace_hall_close", zbg.palace_hall_close)
    camA = cam_push(1.0, 1.06, 560, 860, 4.4)
    LA = [("p2s1a", 1.0)]

    def midA(t):
        q = tp(LA, t, 1, turn=-0.25, gx=-0.4, gy=0.25, smile=0.55, brow=0.3, furrow=-0.2, nod=8 * ease(t / 1.0), armR="chest", armL="relaxed")
        return at_neck(IBLIS_COOK, q, t, 560, 1060, 1.45)
    A = Shot(4.4, dimc, midA, cam=camA, light=DIM, grade="fire", fade_in=0.5,
             fx=[glint(camA, eyes_of(560, 1060, 1.45, -0.25), 2.6, 3.6)])

    close = bg("palace_hall_close", zbg.palace_hall_close)

    def shadow(im, t):
        u = ease((t - 0.3) / 2.6)
        if u <= 0:
            return
        x = lerp(1300, -400, u)
        g = Image.new("L", (W, H), 0)
        from PIL import ImageDraw
        if x < W:
            ImageDraw.Draw(g).rectangle((int(max(-W, x)), 0, W, H), fill=150)
        g = g.filter(ImageFilter.GaussianBlur(120))
        im.alpha_composite(Image.merge("RGBA", (g.point(lambda v: 10), g.point(lambda v: 6), g.point(lambda v: 14), g)))

    def midB(t):
        z = tp([], t + 4.4, 2, legs="sit", turn=0.1, gx=0.3, gy=0.1, smile=0.6 * (1 - ease((t - 2.2) / 0.6)), brow=0.2 + 0.4 * ease((t - 2.4) / 0.5),
               armL="relaxed", armR="relaxed", snake_rise=0.0)
        return at_neck(ZAHHAK_YOUNG_KING, z, t, 540, 1040, 1.3)
    B = Shot(3.6, close, midB, cam=cam_push(1.0, 1.05, 540, 820, 3.6), light=HALLDAY, sun=SUNBEAM, fx=[shadow], fade_out=0.5)
    return [A, B]


# ================================================================ S2 title (8.0-12.6)
def s2():
    kit = bg("kitchen", zbg.kitchen)

    def mid(t):
        return fire_svg(300, 1176, 80, t, 2) + steam(320, 820, t, 4, 260, 5)
    return [Shot(4.6, kit, mid, cam=cam_push(1.04, 1.1, 400, 960, 4.6), light=KITCH, fx=[Embers(40, 21, (180, 900, 440, 1170), (60, 150))],
                 grade="fire", bloom=0.7, fade_in=0.4, fade_out=0.5)]


# ================================================================ S3 the new king, the cook, the keys (12.6-33.8)
def court(t, bow=0.0, back=0.0, seed=0):
    """courtiers on both sides of the hall, turned to the throne; bow 0..1; back 0..1 = stepping away in fear"""
    o = ""
    people = [(COURTIER, 150, 1420, 0.38, 1), (COURTIER2, 300, 1470, 0.4, 1), (COURTIER3, 940, 1430, 0.38, -1), (COURTIER, 800, 1480, 0.4, -1)]
    for k, (S, x, y, s, side) in enumerate(people):
        xx = x - side * 90 * back
        q = P(turn=0.45 * side, gx=0.8 * side, gy=-0.2 + 0.6 * bow, nod=18 * bow, brow=0.6 * back, furrow=0.2, sad=0.3 * back,
              armL="chest" if bow > 0.3 else ("both_out" if back > 0.3 else "relaxed"), armR="chest" if bow > 0.3 else "relaxed",
              blink=blink_at(t, 90 + k), breathe=math.sin(t * 2 + k))
        o += at_feet(S, q, t, xx, y, s)
    return o


def s3():
    gp = bg("garden_predawn", lambda: zbg.garden("predawn"))

    def midA1(t):
        return pit_svg(540, 1480, 1.0, cover=0.3, seed=9, scale=0.9)
    A1 = Shot(3.8, gp, midA1, cam=cam_push(1.0, 1.06, 540, 1200, 3.8), light=PREDAWN, sun=(540, 840, 900, (0.12, 0.07, 0.05)), grade="warm", fade_in=0.4,
              fx=[Motes(20, 31, (255, 230, 200), (0, 400, W, 1300), (-6, -3), amax=60)])

    hall = bg("palace_hall", zbg.palace_hall)

    def midA2(t):
        z = tp([], t, 3, legs="sit", turn=0.0, gx=0.0, gy=0.35, smile=0.3, brow=0.1, armL="relaxed", armR="relaxed", snake_rise=0.0)
        return at_neck(ZAHHAK_YOUNG_KING, z, t, 540, 793, 0.36) + court(t, bow=ease((t - 0.6) / 0.8))
    A2 = Shot(4.2, hall, midA2, cam=cam_push(1.0, 1.04, 540, 1000, 4.2), light=HALLDAY, sun=SUNBEAM,
              fx=[Motes(40, 32, (255, 240, 210), (200, 300, 900, 1500), (8, 14), amax=70)])

    camB = cam_push(1.25, 1.3, 540, 1050, 5.0)
    LB = [("p2s3c", 0.4)]

    def midB(t):
        z = tp([], t + 4.2, 3, legs="sit", turn=-0.15, gx=-0.4, gy=0.6, smile=0.35, brow=0.2, armL="relaxed", armR="relaxed", snake_rise=0.0)
        o = at_neck(ZAHHAK_YOUNG_KING, z, t, 540, 793, 0.36) + court(t, bow=1.0)
        u = ease(t / 1.6)
        bow = ease((t - 1.6) / 0.5) * (1 - 0.6 * ease((t - 3.4) / 0.5))
        q = tp(LB, t, 4, legs="walk" if u < 1 else "stand", phase=t * 5.6, turn=0.35, gx=0.7, gy=-0.5 + 0.4 * bow, nod=16 * bow, smile=0.6, brow=0.3,
               armR="chest" if t > 1.4 else "relaxed", armL="relaxed")
        return o + at_feet(IBLIS_COOK, q, t, lerp(330, 540, u), lerp(1520, 1460, u), 0.43)
    B = Shot(5.0, hall, midB, cam=camB, bg_par=1.0, light=HALLDAY, sun=SUNBEAM)

    close = bg("palace_hall_close", zbg.palace_hall_close)
    LC = [("p2s3d", 0.3), ("p2s3e", 2.4)]
    TOSS = 4.3

    def midC(t):
        raise_ = ease((t - 2.4) / 0.5)
        throw = ease((t - TOSS) / 0.25)
        hx, hy = lerp(200, 320, throw), lerp(250, -40, raise_) + 40 * throw
        z = tp(LC, t, 5, legs="sit", turn=0.2, gx=0.5, gy=0.0, smile=0.45, brow=0.35, furrow=-0.2, armL=("ik", hx, hy, "down") if raise_ > 0.01 else "relaxed",
               armR="relaxed", snake_rise=0.0)
        o = at_neck(ZAHHAK_YOUNG_KING, z, t, 500, 1040, 1.3)
        if raise_ > 0.01 and t < TOSS:
            o += keys_svg(500 + hx * 1.3 + 10, 1040 + hy * 1.3 - 30, 20 * math.sin(t * 6), 1.0)
        elif t >= TOSS:
            k = (t - TOSS) / 0.9
            if k < 1:
                o += keys_svg(lerp(500 + 260 * 1.3, 1250, k), 1040 - 60 - 380 * math.sin(k * math.pi * 0.8), 400 * k, 1.0)
        return o
    C = Shot(5.6, close, midC, cam=cam_push(1.0, 1.04, 500, 820, 5.6), light=HALLDAY, sun=SUNBEAM)

    def midD(t):
        catch = ease((t - 0.1) / 0.3)
        q = tp([], t, 6, turn=-0.2, gx=-0.3 + 0.5 * catch, gy=-0.3 + 0.4 * catch, smile=0.4 + 0.3 * catch, brow=0.3, armL=("ik", lerp(-200, 120, catch), lerp(-200, 120, catch), "down"),
               armR="relaxed")
        o = at_neck(IBLIS_COOK, q, t, 600, 1060, 1.45)
        kx, ky = 600 + lerp(-200, 120, catch) * 1.45 * 1.0, 1060 + lerp(-200, 120, catch) * 1.45 - 30
        if t < 0.1:
            kx, ky = lerp(-100, kx, t / 0.1), ky
        return o + keys_svg(kx, ky, 30 * (1 - catch), 1.3)
    camD = cam_push(1.0, 1.05, 600, 860, 2.6)
    D = Shot(2.6, close, midD, cam=camD, light=HALLDAY, sun=SUNBEAM, fx=[glint(camD, eyes_of(600, 1060, 1.45, -0.2), 1.0, 2.0)], fade_out=0.4)
    return [A1, A2, B, C, D]


# ================================================================ S4 the four meals (33.8-73.0)
def s4():
    tab = bg("table_cloth", zbg.table_cloth)

    def insert(fn, dur, fade_in=0.0, fade_out=0.0):
        def mid(t):
            return f'<g transform="translate(540,900) scale(1.38) translate(-540,-900)">{fn(540, 900, t)}</g>'
        return Shot(dur, tab, mid, cam=cam_push(1.0, 1.06, 540, 880, dur), light=TABLE, sun=(540, 400, 800, (0.08, 0.06, 0.03)), fade_in=fade_in, fade_out=fade_out)
    A = insert(dish_plants, 6.8, fade_in=0.4)

    kit = bg("kitchen", zbg.kitchen)
    camB = cam_push(1.0, 1.05, 520, 900, 3.8)

    def midB(t):
        st = math.sin(t * 4.0)
        hx, hy = -320 + 40 * st, 60 + 16 * math.cos(t * 4.0)
        q = tp([], t, 7, turn=-0.35, gx=-0.6, gy=0.5, smile=0.5, brow=0.2, furrow=0.1, armR=("ik", hx, hy), armL="relaxed")
        wx, wy = 660 + hx * 0.7, 817 + hy * 0.7
        ladle = (f'<path d="M {wx:.1f} {wy:.1f} L {wx - 120:.1f} {wy + 60:.1f}" stroke="#5a3a1c" stroke-width="9" stroke-linecap="round"/>')
        return (fire_svg(300, 1176, 80, t, 2) + steam(320, 820, t, 4, 260, 5) + ladle + at_neck(IBLIS_COOK, q, t, 660, 817, 0.7))
    B = Shot(3.8, kit, midB, cam=camB, light=KITCH, fx=[Embers(30, 22, (180, 900, 440, 1170), (60, 150)), glint(camB, eyes_of(660, 817, 0.7, -0.35), 2.4, 3.3)],
             grade="fire", bloom=0.6)

    C1 = insert(dish_eggs, 4.0)
    close = bg("palace_hall_close", zbg.palace_hall_close)
    LC2 = [("p2s4d", 0.4)]

    def midC2(t):
        spoon = ease(t / 0.4) * (1 - ease((t - 1.0) / 0.4))
        joy = ease((t - 1.0) / 0.5)
        z = tp(LC2, t, 8, legs="sit", turn=0.15, gx=0.3 * joy, gy=0.1, smile=0.3 + 0.5 * joy, brow=0.2 + 0.5 * joy, furrow=-0.3, armL=("ik", lerp(120, 40, spoon), lerp(300, -60, spoon), "down"),
               armR="relaxed", snake_rise=0.0)
        if spoon > 0.6:
            z["blink"] = 1.0
        o = at_neck(ZAHHAK_YOUNG_KING, z, t, 540, 1040, 1.3)
        sx, sy = 540 + lerp(120, 40, spoon) * 1.3, 1040 + lerp(300, -60, spoon) * 1.3
        o += (f'<path d="M {sx:.1f} {sy:.1f} L {sx + 20:.1f} {sy - 70:.1f}" stroke="#c9a24a" stroke-width="9" stroke-linecap="round"/>'
              f'<ellipse cx="{sx + 24:.1f}" cy="{sy - 84:.1f}" rx="20" ry="13" fill="#c9a24a" stroke="#5a3a14" stroke-width="3"/>')
        return o
    C2 = Shot(4.6, close, midC2, cam=cam_push(1.0, 1.04, 540, 820, 4.6), light=HALLDAY, sun=SUNBEAM)

    D1 = insert(dish_birds, 3.0)
    LD2 = [("p2s4f", 0.3)]

    def midD2(t):
        bang = max(0.0, math.sin(t * 7)) if 0.3 < t < 1.8 else 0.0
        z = tp(LD2, t, 9, legs="sit", turn=0.05, gx=0.0, gy=0.1, smile=0.6, brow=0.5, furrow=-0.1, armL=("ik", 200, 120 - 80 * bang, "down"),
               armR=("ik", -140, -20 + 30 * math.sin(t * 5), "down"), snake_rise=0.0)
        o = at_neck(ZAHHAK_YOUNG_KING, z, t, 540, 1040, 1.3)
        lx, ly = 540 - 140 * 1.3, 1040 + (-20 + 30 * math.sin(t * 5)) * 1.3
        o += (f'<path d="M {lx:.1f} {ly:.1f} C {lx - 10:.1f} {ly - 50:.1f}, {lx - 30:.1f} {ly - 80:.1f}, {lx - 60:.1f} {ly - 100:.1f}" stroke="#9a5a24" stroke-width="40" stroke-linecap="round" fill="none"/>'
              f'<path d="M {lx:.1f} {ly:.1f} C {lx - 10:.1f} {ly - 50:.1f}, {lx - 30:.1f} {ly - 80:.1f}, {lx - 60:.1f} {ly - 100:.1f}" stroke="#3a1a08" stroke-width="3" fill="none"/>'
              f'<circle cx="{lx + 6:.1f}" cy="{ly + 14:.1f}" r="12" fill="#f4ecdc" stroke="#3a1a08" stroke-width="3"/>')
        return o
    D2 = Shot(3.0, close, midD2, cam=cam_push(1.03, 1.07, 540, 820, 3.0), light=HALLDAY, sun=SUNBEAM)

    E = insert(dish_chicken_lamb, 2.6)
    F = insert(dish_stew, 5.6)

    hall = bg("palace_hall", zbg.palace_hall)
    LG = [("p2s4i", 0.4)]

    def midG(t):
        z = tp(LG, t, 10, legs="sit", turn=0.25, gx=0.6, gy=0.3, smile=0.75, brow=0.45, furrow=-0.3, armL="both_out" if t > 1.4 else "relaxed",
               armR="both_out" if t > 1.4 else "relaxed", snake_rise=0.0)
        q = tp([], t, 11, turn=-0.4, gx=-0.8, gy=-0.4, smile=0.55, nod=10, armR="chest", armL="relaxed")
        return at_neck(ZAHHAK_YOUNG_KING, z, t, 540, 793, 0.36) + at_feet(IBLIS_COOK, q, t, 760, 1380, 0.4)
    G = Shot(5.8, hall, midG, cam=cam_push(1.6, 1.68, 600, 1000, 5.8), bg_par=1.0, light=HALLDAY, sun=SUNBEAM, fade_out=0.4)
    return [A, B, C1, C2, D1, D2, E, F, G]


# ================================================================ S5 the wish, the kiss, the vanishing (73.0-97.4)
def s5():
    hallb = bg("palace_hall", zbg.palace_hall, 8)
    LA = [("p2s5a", 0.4), ("p2s5b", 4.2)]
    camA = cam_push(1.0, 1.05, 560, 860, 7.4)

    def midA(t):
        q = tp(LA, t, 12, turn=-0.3, gx=-0.5, gy=0.2 - 0.4 * ease((t - 4.0) / 0.4), smile=0.5, brow=0.35, furrow=-0.3, nod=8,
               armR="chest", armL="relaxed")
        return at_neck(IBLIS_COOK, q, t, 560, 1060, 1.45)
    A = Shot(7.4, hallb, midA, cam=camA, light=HALLDAY, sun=SUNBEAM, fx=[glint(camA, eyes_of(560, 1060, 1.45, -0.3), 5.0, 6.0)])

    close = bg("palace_hall_close", zbg.palace_hall_close)
    LB = [("p2s5c", 0.3)]

    def midB(t):
        laugh = ease((t - 0.8) / 0.3) * (1 - ease((t - 2.0) / 0.5))
        z = tp(LB, t, 13, legs="sit", turn=0.2, gx=0.5, gy=-0.1, smile=0.8, brow=0.4, furrow=-0.3, nod=-10 * laugh, tilt=3 * laugh,
               armL=("ik", 260, 160, "down") if t > 2.0 else "relaxed", armR="relaxed", snake_rise=0.0)
        return at_neck(ZAHHAK_YOUNG_KING, z, t, 520, 1040, 1.3)
    B = Shot(3.8, close, midB, cam=cam_push(1.0, 1.04, 520, 820, 3.8), light=HALLDAY, sun=SUNBEAM)

    def kiss_shot(side):
        """side +1: Iblis comes from the right to the king's right shoulder (in the picture); -1: mirrored"""
        zx = 430 if side > 0 else 650

        def mid(t):
            u = ease(t / 1.0)
            kiss = ease((t - 0.9) / 0.3) * (1 - ease((t - 1.9) / 0.3))
            z = tp([], t, 14, legs="sit", turn=0.25 * side, gx=0.6 * side, gy=0.4, smile=0.4, brow=0.2, armL="relaxed", armR="relaxed", snake_rise=0.0)
            q = tp([], t, 15, turn=-0.5 * side, gx=-0.8 * side, gy=0.5, smile=0.3, brow=0.2, tilt=-10 * side * u, nod=12 * u,
                   armR="chest" if side > 0 else "relaxed", armL="chest" if side < 0 else "relaxed")
            if kiss > 0.3:
                q["blink"] = 1.0
            ix = lerp(zx + side * 360, zx + side * 205, u)
            # Iblis leans in from behind: drawn first, his lips come down on the king's shoulder
            return at_neck(IBLIS_COOK, q, t, ix, 1080 + 22 * kiss, 0.9) + at_neck(ZAHHAK_YOUNG_KING, z, t, zx, 960, 0.95)
        return Shot(2.4, hallb, mid, cam=cam_push(1.0, 1.04, 540, 900, 2.4), light=HALLDAY, sun=SUNBEAM)
    C1 = kiss_shot(1)
    C2 = kiss_shot(-1)

    hall = bg("palace_hall", zbg.palace_hall)

    def midD(t):
        fade = 1 - ease((t - 1.6) / 1.4)
        sink = 70 * ease((t - 1.6) / 1.6)
        z = tp([], t, 16, legs="sit", turn=0.1, gx=0.2, gy=0.5, smile=0.4 * (1 - ease((t - 2.2) / 0.4)), brow=0.7 * ease((t - 2.4) / 0.4), armL="relaxed", armR="relaxed",
               snake_rise=0.0)
        o = at_neck(ZAHHAK_YOUNG_KING, z, t, 540, 793, 0.36)
        q = tp([], t, 17, turn=0.4, gx=0.6, gy=-0.2, smile=0.7, brow=0.4, furrow=-0.3, armR="relaxed", armL="relaxed")
        if fade > 0.01:
            o += f'<g opacity="{fade:.3f}">' + at_feet(IBLIS_COOK, q, t, 680, 1400 + sink, 0.42) + '</g>'
        if t > 1.2:                                                            # dark smoke swirling down into the floor
            r = random.Random(5)
            for k in range(26):
                age = (t - 1.2) * 0.7 + r.uniform(0, 0.6)
                if age <= 0 or age > 1.6:
                    continue
                a = r.uniform(0, 6.28) + age * 3
                rad = 60 + 120 * (1 - min(1, age))
                x = 680 + math.cos(a) * rad * 0.8; y = 1250 - 330 * r.random() + age * 160
                rr = 30 + 40 * age
                o += f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="{rr:.1f}" ry="{rr * 0.7:.1f}" fill="#1a141e" opacity="{max(0, 0.55 * (1 - age / 1.6)):.2f}"/>'
        return o
    D = Shot(4.4, hall, midD, cam=cam_push(1.5, 1.56, 610, 1050, 4.4), bg_par=1.0, light=HALLDAY, sun=SUNBEAM)

    LE = [("p2s5d", 0.4)]

    def midE(t):
        look = math.sin(t * 2.2)
        z = tp(LE, t, 18, legs="sit", turn=0.35 * look, gx=0.9 * look, gy=0.0, brow=0.7, furrow=0.2, armL="relaxed", armR="relaxed", snake_rise=0.0)
        return at_neck(ZAHHAK_YOUNG_KING, z, t, 540, 1040, 1.3)
    E = Shot(4.0, close, midE, cam=cam_push(1.0, 1.04, 540, 820, 4.0), light=HALLDAY, sun=SUNBEAM)
    return [A, B, C1, C2, D, E]


# ================================================================ S6 the snakes (97.4-120.4)
def s6():
    close = bg("palace_hall_close", zbg.palace_hall_close)

    def midA(t):
        pain = ease((t - 0.8) / 0.5)
        jit = 3 * math.sin(t * 40) * pain
        z = tp([], t, 19, legs="sit", turn=0.25, gx=0.6, gy=0.5, brow=0.6 * pain, furrow=0.9 * pain, sad=0.3 * pain, mouth_o=0.0,
               armR=("ik", lerp(-60, 200, pain), lerp(380, 120, pain)) if pain > 0.05 else "relaxed", armL="relaxed", snake_rise=0.12 * ease((t - 2.0) / 2.5), hisses=(0.0, 0.0))
        z["blink"] = max(z["blink"], 0.5 * pain)
        return at_neck(ZAHHAK_YOUNG_KING, z, t, 540 + jit, 1020, 1.25)
    A = Shot(5.0, close, midA, cam=cam_push(1.0, 1.05, 540, 820, 5.0), light=dict(HALLDAY, ambient=(0.92, 0.88, 0.9)), sun=SUNBEAM,
             fx=[darken(0.15, 1.0, 9.0, (20, 10, 30))])

    LB = [("p2s6a", 2.4)]

    def midB(t):
        rise = lerp(0.12, 1.0, ease((t - 0.4) / 2.4))
        h = ease((t - 2.0) / 0.4)
        fear = ease((t - 0.8) / 0.6)
        z = tp(LB, t, 20, legs="sit", turn=0.15, gx=0.8, gy=-0.5, brow=0.4 + 1.4 * fear, furrow=-0.4 * fear, sad=0.15, nod=-8 * fear, armL="relaxed", armR="relaxed",
               snake_rise=rise, snake_looks=(0.6 + 0.4 * math.sin(t), -0.4 + 0.3 * math.sin(t * 1.3)), hisses=(0.6 * h, 0.9 * h))
        z["mouth_o"] = max(z["mouth_o"], 0.45 * fear)
        z["blink"] = 0.0 if fear > 0.5 else z["blink"]
        return at_neck(ZAHHAK_YOUNG_KING, z, t, 540, 1000, 1.05)
    B = Shot(7.0, close, midB, cam=cam_push(1.0, 1.06, 540, 800, 7.0), light=dict(HALLDAY, ambient=(0.86, 0.8, 0.86)), sun=SUNBEAM,
             fx=[darken(0.25, -1.0, 9.0, (20, 10, 30))])

    hall = bg("palace_hall", zbg.palace_hall)

    def midC(t, tt=0.0):
        T = t + tt
        z = tp([], T, 21, legs="sit", turn=0.0, gx=0.0, gy=0.0, brow=0.9, furrow=0.4, armL="both_out", armR="both_out",
               snake_looks=(1.0, 1.0), hisses=(0.5 + 0.5 * math.sin(T * 2), 0.5 + 0.5 * math.sin(T * 2 + 1)))
        return at_neck(ZAHHAK_YOUNG_KING, z, T, 540, 793, 0.36) + court(T, back=ease(T / 1.5))
    C = Shot(6.0, hall, midC, cam=cam_push(1.0, 1.05, 540, 1000, 6.0), light=dict(HALLDAY, ambient=(0.84, 0.78, 0.84)), sun=SUNBEAM,
             fx=[darken(0.25, -1.0, 9.0, (20, 10, 30))])
    END = Shot(5.0, hall, lambda t: midC(t, 6.0), cam=cam_push(1.05, 1.12, 540, 980, 5.0), light=dict(HALLDAY, ambient=(0.8, 0.74, 0.8)), sun=SUNBEAM,
               fx=[darken(0.4, -1.0, 9.0, (20, 10, 30))], fade_out=0.8)
    return [A, B, C, END]


SCENES = {"s1": s1, "s2": s2, "s3": s3, "s4": s4, "s5": s5, "s6": s6}
