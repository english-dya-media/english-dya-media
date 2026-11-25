"""Part 5 · The Father — 2D cartoon. Timing matches leyli/p05_audio.py
(scene starts s1 0, s2 6.8, s3 11.4, s4 58.6, s5 70.8, s6 103.0, s7 137.8; end card 151.2; total 156.4).
The chief's death is never shown: his empty seat, a lamp that goes out, the tribe standing round his new grave."""
import math, random
from PIL import Image, ImageFilter, ImageDraw
from film import Shot, W, H, ease, lerp, blink_at, cam_push, Motes, svg_render
from chars import gazelle, Ctx, FEET
from stage import at_neck, at_feet, lw_for, Glow, random_spec
import bgs, lbg
from cast import *
from p01_scenes import P, tp, bg, cam_xy, seated, body_xy, birds, SandWind, DUSKL, SUN_DUSK, DAWNL, SUN_DAWN, DAYL, SUN_DAY
from p03_scenes import gazelles, seat_shadow, tear, majnun_sit_q
from p04_scenes import MOONIN
import p05_audio as AU

TENTL = dict(ambient=(0.74, 0.62, 0.66), rim=(5, -2), rim_col=(1.0, 0.66, 0.36), rim_str=0.9, ramp=(0, W, 0.9, 1.06))     # dusk in the tent
TWILIGHT = dict(ambient=(0.62, 0.62, 0.8), rim=(5, -2), rim_col=(0.78, 0.84, 1.0), rim_str=0.7, ramp=(0, W, 0.9, 1.04))  # dusk going to night (moon at the right)
GZ5 = [(600, 1262, 0.95, 0.2), (175, 1236, 0.74, 0.6)]        # gazelles near Majnun in the desert (x, feet y, scale, look)


def L(t0, *ids):
    """line ids -> [(id, start within a shot that begins at t0)]; a line said twice is taken at its first time after t0"""
    out = []
    for i in ids:
        ts_ = [t for lid, t in AU.LINES if lid == i and t >= t0 - 0.5]
        out.append((i, min(ts_) - t0))
    return out


def seat_ik(S, x, floor, s, X, Y, down=False):
    """an ("ik", …) arm that puts the hand of a person drawn with seated(S, …, x, floor, s) at the screen point (X, Y)"""
    yf = floor - 575 * S["bs"] * s + FEET * S["bs"] * s
    bx, by = body_xy(S, x, yf, s, X, Y)
    return ("ik", bx, by, "down") if down else ("ik", bx, by)


def feet_ik(S, x, yf, s, X, Y, down=False, flip=False):
    """the same for a person drawn with at_feet(S, …, x, yf, s)"""
    bx, by = body_xy(S, x, yf, s, X, Y)
    bx = -bx if flip else bx
    return ("ik", bx, by, "down") if down else ("ik", bx, by)


def gz(t, x, y, s, face=1.0, **kw):
    """one gazelle; face 1: facing left (as drawn), -1: facing right; values between turn her round (a cartoon squash)"""
    c = Ctx(lw_for(s))
    return f'<g transform="translate({x:.1f},{y:.1f}) scale({s * face:.4f},{s:.4f})">{gazelle(c, t=t, **kw)}</g>'


def staff_walk(t, rate=2.4, side=1):
    """an old man's arm with his walking stick, swinging with the steps (side 1: the stick in the hand on the right of the picture)"""
    return ("ik", side * (190 + 30 * math.sin(t * rate)), 520)


def walk_shadow(x, y, s, right=True, col="#3a2a40", a=0.25):
    d = "M 60 0 L -760 120 L -820 60 L -40 -20 Z" if right else "M -60 0 L 760 160 L 820 90 L 40 -20 Z"
    return f'<g transform="translate({x:.1f},{y:.1f}) scale({s:.4f})"><path d="{d}" fill="{col}" opacity="{a}"/></g>'


def cam_svg(cam, t, body):
    k, cx, cy, px, py = cam(t)
    return f'<g transform="translate({px:.2f},{py:.2f}) translate({cx:.2f},{cy:.2f}) scale({k:.5f}) translate({-cx:.2f},{-cy:.2f})">{body}</g>'


def silhouettes(cam, body_fn, fill=(26, 12, 24), glow=(255, 170, 110), blur=7, ga=0.8):
    """an fx drawing body_fn(t) as dark figures with a warm glowing edge (people far away against the sunset)"""
    def fx(im, t):
        body = body_fn(t)
        if body:
            A = svg_render(cam_svg(cam, t, body)).getchannel("A")
            g = A.filter(ImageFilter.GaussianBlur(blur)).point(lambda v: int(min(255, v * 1.6 * ga)))
            layer = Image.new("RGBA", (W, H), glow + (0,)); layer.putalpha(g)
            im.alpha_composite(layer)
            dark = Image.new("RGBA", (W, H), fill + (0,)); dark.putalpha(A)
            im.alpha_composite(dark)
    return fx


def rope(x0, y0, x1, y1, sag=40, col="#8a6a3a", w=5.0):
    """a rope hanging between two points"""
    mx, my = (x0 + x1) / 2, max(y0, y1) + sag
    return (f'<path d="M {x0:.1f} {y0:.1f} Q {mx:.1f} {my:.1f} {x1:.1f} {y1:.1f}" stroke="#2a1a0c" stroke-width="{w + 2.4:.1f}" fill="none" stroke-linecap="round"/>'
            f'<path d="M {x0:.1f} {y0:.1f} Q {mx:.1f} {my:.1f} {x1:.1f} {y1:.1f}" stroke="{col}" stroke-width="{w:.1f}" fill="none" stroke-linecap="round" '
            f'stroke-dasharray="{w * 1.6:.1f} {w * 0.7:.1f}"/>')


def hoof_xy(x, y, s, face=1.0, t=0.0, phase=0.0, walk=False, seed=0):
    """the screen point of a gazelle's outer hind foot (where the hunter's snare holds her) for gz(…, x, y, s, face, …): the same leg
    motion as chars.gazelle()"""
    a = 20 * math.sin(phase) if walk else 1.5 * math.sin(t * 1.1 + 3 + seed)
    r_ = math.radians(a)
    kx, ky = 84 + math.sin(r_) * 96 + 10, -196 + math.cos(r_) * 96
    fx_, fy_ = kx + math.sin(r_ * 0.6) * 96 - 12, min(-4, ky + 96 - (10 * max(0, math.sin(phase)) if walk else 0))
    return x + fx_ * s * face, y + fy_ * s


def snare(hx, hy, s):
    """the loop of the snare round the hind leg, just above the hoof"""
    return (f'<ellipse cx="{hx:.1f}" cy="{hy - 20 * s:.1f}" rx="{13 * s:.1f}" ry="{6 * s:.1f}" fill="none" stroke="#2a1a0c" stroke-width="{5 * s + 2:.1f}"/>'
            f'<ellipse cx="{hx:.1f}" cy="{hy - 20 * s:.1f}" rx="{13 * s:.1f}" ry="{6 * s:.1f}" fill="none" stroke="#8a6a3a" stroke-width="{4 * s + 1:.1f}"/>')


# ================================================================ S1 the hook (0-6.8): Majnun at his father's grave at dusk
def grave_bg(pal="dusk", blur=0):
    return bg(f"grave_{pal}", lambda: lbg.grave_close(pal), blur)


def mourner(t, lines, seed, u=0.0, s=0.52, reach=True, bow=0.0, lean=0.0, **kw):
    """Majnun sitting behind his father's grave, one hand on the headstone (reach) or on the mound, the other on the mound;
    bow 0..1 lowers his head; lean (degrees, < 0: towards the headstone at the left) leans him over, pivoting at his seat"""
    x, fl = lbg.GRAVE_SEAT
    hx, hy = lbg.GRAVE_HEAD
    rr = (hx + 34, hy + 64) if reach else (x - 105, 964)
    ll = (x + 100, 962)
    a = math.radians(-lean)                 # the hands' targets turned back by the lean, so that they land on the grave after it

    def unlean(X, Y):
        dx, dy = X - x, Y - fl
        return x + dx * math.cos(a) - dy * math.sin(a), fl + dx * math.sin(a) + dy * math.cos(a)
    base = dict(legs="sit", turn=-0.12, gx=-0.45 if reach else 0.0, gy=0.55, sad=0.85, brow=0.9, furrow=-0.5,
                armR=seat_ik(MAJNUN, x, fl, s, *unlean(*rr), down=True), armL=seat_ik(MAJNUN, x, fl, s, *unlean(*ll), down=True), wind=0.5)
    base.update(kw)
    q = tp(list(lines), t, seed, **base)
    q["nod"] += 40 * bow
    q["tilt"] += -8 * bow
    q["blink"] = max(q["blink"], 0.75 * bow)
    body = seated(MAJNUN, q, t, x, fl, s)
    if lean:
        body = f'<g transform="rotate({lean:.2f},{x},{fl})">{body}</g>'
    return lbg.grave_mound(u) + body + lbg.grave_mound(u, "front")


def majnun_face(t, lines, seed, tear_t=None, mouth=0.0, **kw):
    """Majnun close (head and shoulders), crying when tear_t is given; mouth: a mouth left open (surprise)"""
    base = dict(turn=0.15, gx=0.0, gy=0.4, sad=0.85, brow=0.95, furrow=-0.5, armL="relaxed", armR="relaxed", wind=0.6)
    base.update(kw)
    q = tp(list(lines), t, seed, **base)
    q["mouth_o"] = max(q["mouth_o"], mouth)
    o = at_neck(MAJNUN, q, t, 540, 1000, 1.05)
    if tear_t is not None:
        fx_ = 12 * q["turn"]
        ey = 1000 + 1.05 * (q["nod"] - 178) + 20
        o += tear(540 + (-40 + fx_ - 6) * 1.05, ey, t, tear_t, 0.75) + tear(540 + (40 + fx_ + 6) * 1.05, ey, t, tear_t + 1.1, 0.75)
    return o


def s1():
    gd = grave_bg("dusk")
    camA = cam_push(1.1, 1.17, 540, 900, 3.0)

    def midA(t):
        return mourner(t, L(0.0, "p5s1a"), 1)
    A = Shot(3.0, gd, midA, cam=camA, bg_par=1.0, light=DUSKL, sun=SUN_DUSK, bloom=0.6, fade_in=0.4,
             fx=[SandWind(120, 101, (0, 700, W, 1300), (400, 800), strength=lambda t: 0.3)])
    gdb = grave_bg("dusk", 6)
    camB = cam_push(1.0, 1.05, 540, 880, 3.8)

    def midB(t):
        return majnun_face(t, L(3.0, "p5s1b"), 2, tear_t=0.6, gy=0.5)
    B = Shot(3.8, gdb, midB, cam=camB, light=DUSKL, sun=SUN_DUSK, bloom=0.5, fade_out=0.6,
             fx=[SandWind(100, 102, (0, 300, W, 1900), (500, 900), strength=lambda t: 0.3)])
    return [A, B]


# ================================================================ S2 title (6.8-11.4): the old chief walks alone over the dunes at sunrise
def s2():
    dw = bg("dunes_dawn", lambda: lbg.dunes("dawn"))

    def mid(t):
        x = lerp(200, 420, t / 4.6); y = 1262; s = 0.34
        q = P(legs="walk", phase=t * 2.4, turn=0.35, gx=0.7, gy=0.2, sad=0.6, brow=0.8, furrow=-0.2, armL=staff_walk(t), propL="staff",
              armR="relaxed", wind=0.8, blink=blink_at(t, 21), breathe=math.sin(t * 2))
        return birds(t, 860, 520, n=4, s=0.8) + walk_shadow(x, y, s) + at_feet(CHIEF_OLD, q, t, x, y, s)
    return [Shot(4.6, dw, mid, cam=cam_push(1.0, 1.04, 540, 1150, 4.6), sun=SUN_DAWN, light=DAWNL, bloom=0.7, fade_in=0.4, fade_out=0.5,
                 fx=[SandWind(140, 201, (0, 1000, W, 1900), (500, 900), strength=lambda t: 0.4), Motes(30, 202, (255, 230, 210), (0, 900, W, 1600), (-8, -4), amax=70)])]


# ================================================================ S3 the father finds his son (11.4-58.6)
M_AT = (330, 1222, 0.62)          # Majnun sitting on the dune (as in parts 3-4)
D_M, D_F = (290, 1250, 0.7), (740, 1250, 0.72)     # the two-shot: Majnun and his father sitting side by side


def s3():
    dd = bg("dunes_day", lambda: lbg.dunes("day"))
    ddb = bg("dunes_day", lambda: lbg.dunes("day"), 6)

    # A: the old chief searches the desert (narration)
    camA = cam_push(1.0, 1.05, 540, 1050, 5.6)

    def midA(t):
        stop = 3.9
        walking = t < stop
        x = lerp(120, 470, min(t, stop) / stop); y = 1268; s = 0.36
        look = ease((t - stop - 0.2) / 0.5)
        q = P(legs="walk" if walking else "stand", phase=t * 2.4, turn=0.35 - 0.6 * look, gx=0.7 - 1.3 * look, gy=-0.2, sad=0.6, brow=0.8, furrow=-0.3,
              armL=staff_walk(t if walking else stop), propL="staff", armR="relaxed", wind=0.8, blink=blink_at(t, 31), breathe=math.sin(t * 2))
        return birds(t, 980, 470, n=4, s=0.8) + walk_shadow(x, y, s) + at_feet(CHIEF_OLD, q, t, x, y, s)
    A = Shot(5.6, dd, midA, cam=camA, light=DAYL, sun=SUN_DAY, bloom=0.5,
             fx=[SandWind(160, 301, (0, 1000, W, 1900), (500, 900), strength=lambda t: 0.5)])

    # B: Majnun among the gazelles; the father comes over the sand: "Qays… my son!"
    LB = L(17.0, "p5s3b")
    camB = cam_push(1.02, 1.0, 560, 1080, 4.6)
    arrive = 1.5

    def midB(t):
        u = ease(t / arrive)
        o = gazelles(t, GZ5, startle=0.7)
        x, y, s = M_AT
        look = ease((t - 1.7) / 0.5)
        o += seat_shadow(x, y, 170)
        o += seated(MAJNUN, majnun_sit_q(t, 32, look=0.3 + 0.6 * look, gy=0.3 - 0.4 * look, brow=0.4 + 0.5 * look, sad=0.4 - 0.2 * look), t, x, y, s)
        walking = t < arrive
        fx_ = lerp(1160, 840, u)
        q = tp(LB, t, 33, legs="walk" if walking else "stand", phase=t * 2.6, turn=-0.35, gx=-0.8, gy=0.2, sad=0.5, brow=0.9, furrow=-0.3,
               armL=staff_walk(t if walking else arrive), propL="staff",
               armR="relaxed" if t < 1.6 else "offer", openR=True, wind=0.8)
        return o + walk_shadow(fx_, 1330, 0.56, right=False) + at_feet(CHIEF_OLD, q, t, fx_, 1330, 0.56)
    B = Shot(4.6, dd, midB, cam=camB, light=DAYL, sun=SUN_DAY, bloom=0.5,
             fx=[SandWind(140, 302, (0, 1000, W, 1900), (500, 900), strength=lambda t: 0.35)])

    # C: Majnun close: "Father…? You came all this way?"
    LC = L(21.6, "p5s3c")
    camC = cam_push(1.0, 1.05, 540, 880, 3.8)

    def midC(t):
        soft = ease((t - 1.8) / 0.8)
        return majnun_face(t, LC, 34, turn=0.25, gx=0.6, gy=-0.1, sad=0.3 + 0.4 * soft, brow=0.9, furrow=-0.3, smile=0.25 * soft, armR="chest" if t > 1.6 else "relaxed")
    C = Shot(3.8, ddb, midC, cam=camC, light=DAYL, sun=SUN_DAY,
             fx=[SandWind(100, 303, (0, 300, W, 1900), (500, 900), strength=lambda t: 0.3)])

    # D1: they sit together; the father's hand on his son's shoulder: "Look at you… so thin, and your clothes are torn."
    LD1 = L(25.4, "p5s3d")
    camD1 = cam_push(1.0, 1.05, 520, 1000, 5.0)

    def two_shot(t, lines_f=(), lines_m=(), seed=0, f_arm=None, m_arm=None, f_kw=None, m_kw=None, extra=""):
        mx, my, ms = D_M
        fx_, fy, fs = D_F
        o = seat_shadow(mx, my, 160) + seat_shadow(fx_, fy, 170)
        mq = dict(legs="sit", turn=0.35, gx=0.7, gy=0.4, sad=0.7, brow=0.8, furrow=-0.3, armL=m_arm or ("ik", 60, 330), armR="relaxed", wind=0.6)
        mq.update(m_kw or {})
        fq = dict(legs="sit", turn=-0.35, gx=-0.8, gy=0.2, sad=0.6, brow=0.8, furrow=-0.3, armR=f_arm or ("ik", -60, 330), armL=("ik", 60, 330),
                  wind=0.5, cloak_len=0.6)
        fq.update(f_kw or {})
        o += seated(MAJNUN, tp(list(lines_m), t, seed, **mq), t, mx, my, ms)
        o += seated(CHIEF_OLD, tp(list(lines_f), t, seed + 1, **fq), t, fx_, fy, fs)
        return o + extra

    shoulder = (D_M[0] + 95, D_M[1] - 575 * D_M[2] + 52)

    def midD1(t):
        reach = ease((t - 0.4) / 0.8)
        f_arm = seat_ik(CHIEF_OLD, D_F[0], D_F[1], D_F[2], lerp(D_F[0] - 150, shoulder[0], reach), lerp(D_F[1] - 120, shoulder[1], reach), down=True)
        return two_shot(t, LD1, (), 35, f_arm=f_arm, m_kw=dict(gy=0.5 + 0.2 * ease((t - 2.0) / 0.6), gx=0.4))
    D1 = Shot(5.0, dd, midD1, cam=camD1, light=DAYL, sun=SUN_DAY, bloom=0.5)

    # D2: the father close: "Come home with me. I am old… I don't have much time."
    LD2 = L(30.4, "p5s3e")
    camD2 = cam_push(1.0, 1.06, 540, 860, 5.2)

    def midD2(t):
        q = tp(LD2, t, 36, turn=-0.25, gx=-0.6, gy=0.1, sad=0.6 + 0.2 * ease((t - 2.0) / 0.6), brow=0.9, furrow=-0.4,
               armL="chest" if t > 2.2 else "relaxed", armR="offer" if 0.4 < t < 2.4 else "relaxed", openR=True, wind=0.5)
        return at_neck(CHIEF_OLD, q, t, 540, 960, 1.0)
    D2 = Shot(5.2, ddb, midD2, cam=camD2, light=DAYL, sun=SUN_DAY)

    # E: Majnun close: "Father, I love you. But I am not Qays anymore." "My heart went with Leyli… and it never came back."
    LE = L(35.6, "p5s3f", "p5s3g")
    camE = cam_push(1.0, 1.07, 540, 880, 7.3)

    def midE(t):
        away = ease((t - 4.6) / 0.8)
        return majnun_face(t, LE, 37, turn=0.25 - 0.4 * away, gx=0.6 - 1.2 * away, gy=0.2 - 0.4 * away, sad=0.7, brow=0.9, furrow=-0.4,
                           smile=0.2 * (1 - away), armR="chest" if t > 0.6 else "relaxed", tear_t=5.0)
    E = Shot(7.3, ddb, midE, cam=camE, light=DAYL, sun=SUN_DAY,
             fx=[SandWind(100, 304, (0, 300, W, 1900), (500, 900), strength=lambda t: 0.25)])

    # F: the father gives him his purse: "Then take this, at least… for bread."
    LF = L(42.9, "p5s3h")
    camF = cam_push(1.04, 1.08, 520, 1000, 4.5)

    def midF(t):
        out = ease((t - 0.5) / 0.7)
        give = t > 2.3
        px = lerp(D_F[0] - 40, D_M[0] + 230, out); py = lerp(D_F[1] - 170, D_F[1] - 230, out)
        f_arm = seat_ik(CHIEF_OLD, D_F[0], D_F[1], D_F[2], px + 20, py)
        take = ease((t - 1.6) / 0.6)
        mpos = (lerp(D_M[0] + 120, px - 10, take), lerp(D_M[1] - 150, py + 6, take)) if not give else (lerp(px - 10, D_M[0] + 150, ease((t - 2.3) / 0.8)),
                                                                                                         lerp(py + 6, D_M[1] - 160, ease((t - 2.3) / 0.8)))
        m_arm = seat_ik(MAJNUN, D_M[0], D_M[1], D_M[2], *mpos)
        o = two_shot(t, LF, (), 38, f_arm=f_arm if t < 3.0 else seat_ik(CHIEF_OLD, D_F[0], D_F[1], D_F[2], lerp(px + 20, D_F[0] - 60, ease((t - 3.0) / 0.6)),
                                                                     lerp(py, D_F[1] - 130, ease((t - 3.0) / 0.6))),
                     m_arm=m_arm, f_kw=dict(propR=None if give else ("purse" if t > 0.3 else None), gx=-0.8, gy=0.4),
                     m_kw=dict(propL="purse" if give else None, gy=0.5, gx=0.6, sad=0.8))
        return o
    F = Shot(4.5, dd, midF, cam=camF, light=DAYL, sun=SUN_DAY, bloom=0.5)

    # G: the father stands with his stick, his hand on his son's head: "Goodbye, my son. I don't think we will meet again."
    LG = L(47.4, "p5s3i")
    camG = cam_push(1.0, 1.05, 520, 1000, 4.6)
    GM = (330, 1300, 0.7)
    GF = (690, 1312, 0.64)

    def midG(t):
        mx, my, ms = GM
        fx_, fy, fs = GF
        head = (mx + 20, my - 575 * ms - 285 * ms)
        bless = ease((t - 0.3) / 0.7) * (1 - ease((t - 3.9) / 0.6))
        hand = (lerp(fx_ - 160, head[0] + 30, bless), lerp(fy - 640, head[1], bless))
        q = tp(LG, t, 39, turn=-0.3, gx=-0.7, gy=0.5, sad=0.7, brow=0.9, furrow=-0.4, armR=feet_ik(CHIEF_OLD, fx_, fy, fs, *hand),
               openR=True, armL=("ik", 190, 520), propL="staff", wind=0.6)
        m = tp([], t, 40, legs="sit", turn=0.35, gx=0.7, gy=-0.5, sad=0.8, brow=0.9, furrow=-0.4, armL=("ik", 60, 330), propL="purse",
               armR="relaxed", wind=0.6)
        m["nod"] += 10 * bless
        return (seat_shadow(mx, my, 160) + seated(MAJNUN, m, t, mx, my, ms)
                + walk_shadow(fx_, fy, fs, right=True, a=0.18) + at_feet(CHIEF_OLD, q, t, fx_, fy, fs))
    G = Shot(4.6, dd, midG, cam=camG, light=DAYL, sun=SUN_DAY, bloom=0.5)

    # H: "Goodbye… Father." — the old man walks away over the sand
    LH = L(52.0, "p5s3j")
    camH = cam_push(1.0, 1.04, 560, 1080, 6.6)

    def midH(t):
        x, y, s = M_AT
        o = gazelles(t, [(560, 1250, 0.8, 0.4)]) + seat_shadow(x, y, 170)
        q = tp(LH, t, 41, legs="sit", turn=0.35, gx=0.8, gy=-0.1, sad=0.85, brow=0.95, furrow=-0.5, armL=("ik", 60, 330), propL="purse",
               armR="chest" if t < 3.0 else "relaxed", wind=0.6)
        o += seated(MAJNUN, q, t, x, y, s)
        u = ease((t - 0.6) / 6.0)
        fx_ = lerp(640, 990, u); fy = lerp(1300, 1198, u); fs = lerp(0.5, 0.24, u)
        fq = P(legs="walk", phase=t * 2.4, turn=0.35, gx=0.7, gy=0.3, sad=0.7, brow=0.8, armL=staff_walk(t), propL="staff", armR="relaxed",
               wind=0.9, blink=blink_at(t, 42), breathe=math.sin(t * 2))
        return o + walk_shadow(fx_, fy, fs) + at_feet(CHIEF_OLD, fq, t, fx_, fy, fs)
    H = Shot(6.6, dd, midH, cam=camH, light=DAYL, sun=SUN_DAY, bloom=0.5, fade_out=0.6,
             fx=[SandWind(220, 305, (0, 1000, W, 1900), (600, 1000), strength=lambda t: 0.3 + 0.4 * ease((t - 2.0) / 1.5))])
    return [A, B, C, D1, D2, E, F, G, H]


# ================================================================ S4 the empty seat; the lamp goes out; the funeral far away (58.6-70.8)
SEAT = (540, 1296)        # the chief's seat in front of his tent (chief_tent): a cushion with his folded cloak and his stick on it
LAMP = (720, 1300)        # a clay oil lamp on the rug beside it (the flame at LAMP + (40, -46))


def empty_seat():
    x, y = SEAT
    o = (f'<ellipse cx="{x}" cy="{y + 8}" rx="190" ry="20" fill="#000" opacity="0.25"/>'
         f'<path d="M {x - 150} {y - 150} C {x - 150} {y - 196}, {x + 150} {y - 196}, {x + 150} {y - 150} L {x + 150} {y - 40} L {x - 150} {y - 40} Z" '
         f'fill="#6a2a5a" stroke="#1b0f0a" stroke-width="4"/>'                                     # the bolster behind
         f'<path d="M {x - 130} {y - 176} C {x - 60} {y - 186}, {x + 60} {y - 186}, {x + 130} {y - 176}" stroke="#e0b060" stroke-width="5" fill="none"/>'
         f'<rect x="{x - 180}" y="{y - 64}" width="360" height="70" rx="26" fill="#8a2420" stroke="#1b0f0a" stroke-width="4"/>'   # the cushion
         f'<path d="M {x - 160} {y - 44} L {x + 160} {y - 44}" stroke="#e0b060" stroke-width="5"/>'
         + "".join(f'<path d="M {x + sx * 182} {y - 30} l {sx * 14} 18 l {sx * -6} 6 Z" fill="#e0b060" stroke="#1b0f0a" stroke-width="2"/>' for sx in (-1, 1))
         # his brown cloak, folded, with its gold edge
         + f'<path d="M {x - 120} {y - 62} C {x - 110} {y - 104}, {x + 40} {y - 112}, {x + 70} {y - 92} L {x + 80} {y - 62} Z" fill="#5a3a22" stroke="#1b0f0a" stroke-width="3"/>'
         f'<path d="M {x - 112} {y - 70} C {x - 90} {y - 96}, {x + 30} {y - 102}, {x + 66} {y - 86}" stroke="#c9a24a" stroke-width="5" fill="none"/>'
         # his walking stick lying across the cushion
         f'<path d="M {x - 220} {y - 20} L {x + 200} {y - 96}" stroke="#2a1608" stroke-width="16" stroke-linecap="round"/>'
         f'<path d="M {x - 220} {y - 20} L {x + 200} {y - 96}" stroke="#6a4424" stroke-width="11" stroke-linecap="round"/>'
         f'<path d="M {x + 200} {y - 96} C {x + 236} {y - 102}, {x + 250} {y - 140}, {x + 222} {y - 156}" stroke="#2a1608" stroke-width="16" fill="none" stroke-linecap="round"/>'
         f'<path d="M {x + 200} {y - 96} C {x + 236} {y - 102}, {x + 250} {y - 140}, {x + 222} {y - 156}" stroke="#6a4424" stroke-width="11" fill="none" stroke-linecap="round"/>')
    return o


def oil_lamp(t, out_t):
    """a clay oil lamp on the rug; its flame shrinks and goes out at out_t, then a thread of smoke rises"""
    x, y = LAMP
    o = (f'<ellipse cx="{x + 6}" cy="{y + 4}" rx="62" ry="10" fill="#000" opacity="0.3"/>'
         f'<path d="M {x - 50} {y - 20} C {x - 50} {y - 54}, {x + 30} {y - 58}, {x + 46} {y - 40} L {x + 60} {y - 46} L {x + 50} {y - 26} '
         f'C {x + 40} {y - 6}, {x - 44} {y + 2}, {x - 50} {y - 20} Z" fill="#a8643a" stroke="#2a1408" stroke-width="4"/>'
         f'<ellipse cx="{x - 8}" cy="{y - 46}" rx="18" ry="6" fill="#4a2410"/>'
         f'<path d="M {x - 52} {y - 30} C {x - 76} {y - 34}, {x - 76} {y - 10}, {x - 50} {y - 14}" stroke="#2a1408" stroke-width="7" fill="none"/>'
         f'<path d="M {x - 40} {y - 40} C {x - 10} {y - 48}, {x + 20} {y - 48}, {x + 36} {y - 40}" stroke="#d8945a" stroke-width="4" fill="none" opacity="0.7"/>')
    k = 1.0 - ease((t - out_t + 0.5) / 0.5)
    if k > 0.02:
        fx, fy = x + 56, y - 48
        h = (40 + 7 * math.sin(t * 13) + 5 * math.sin(t * 7.7)) * k
        o += (f'<path d="M {fx - 10 * k:.1f} {fy:.1f} C {fx - 13 * k:.1f} {fy - h * 0.5:.1f}, {fx + 2:.1f} {fy - h * 0.8:.1f}, {fx:.1f} {fy - h:.1f} '
              f'C {fx + 6 * k:.1f} {fy - h * 0.7:.1f}, {fx + 13 * k:.1f} {fy - h * 0.4:.1f}, {fx + 10 * k:.1f} {fy:.1f} Z" fill="#ffc050"/>'
              f'<path d="M {fx - 4 * k:.1f} {fy:.1f} C {fx - 5 * k:.1f} {fy - h * 0.3:.1f}, {fx:.1f} {fy - h * 0.5:.1f}, {fx:.1f} {fy - h * 0.55:.1f} '
              f'C {fx + 3 * k:.1f} {fy - h * 0.4:.1f}, {fx + 5 * k:.1f} {fy - h * 0.2:.1f}, {fx + 4 * k:.1f} {fy:.1f} Z" fill="#fff4c0"/>')
    return o


def s4():
    ct = bg("chief_tent_dusk", lambda: lbg.chief_tent("dusk"))
    out_t = AU.LAMP_OUT - AU.SEAT
    camA = cam_push(1.5, 1.58, 540, 1920, 6.2)

    def midA(t):
        return empty_seat() + oil_lamp(t, out_t)

    def lamp_light(im, t):
        k = 1.0 - ease((t - out_t + 0.5) / 0.5)
        x, y = cam_xy(camA, t, LAMP[0] + 56, LAMP[1] - 70)
        if k > 0.02:
            g = Glow(lambda _: (x, y), 300, (255, 170, 90), 0.42 * k)
            g(im, t)
        if t > out_t:          # smoke, and the evening darkens
            d = ImageDraw.Draw(im, "RGBA")
            for j in range(8):
                age = t - out_t - j * 0.16
                if age > 0:
                    yy = y + 10 - age * 70 - j * 4; xx = x + 16 * math.sin(age * 2.4 + j); rr = 6 + age * 7
                    d.ellipse((xx - rr, yy - rr, xx + rr, yy + rr), fill=(170, 160, 160, int(max(0, 70 - age * 24))))
            im.alpha_composite(Image.new("RGBA", (W, H), (8, 4, 16, int(255 * min(0.42, (t - out_t) * 0.5)))))
    A = Shot(6.2, ct, midA, cam=camA, bg_par=1.0, light=TENTL, sun=SUN_DUSK, grade="fire", bloom=0.6, fade_in=0.5, fx=[lamp_light])

    # B: the tribe stands round the chief's new grave at sunset, heads bowed
    gd = grave_bg("dusk")
    camB = cam_push(1.0, 1.04, 540, 900, 6.0)
    r = random.Random(4605)
    tribe = [ELDER, dict(MESSENGER, skin="olive", beard="full"), GOSSIP_A, SERVANT_A, dict(ELDER, kufiya_pat=None, beard="full", beard_col="#8a8680",
             skin="tan", col="#5a4a3a"), GOSSIP_B, MESSENGER, SERVANT_B]
    mourners = []
    for k, (S, x) in enumerate(zip(tribe, (205, 300, 400, 500, 605, 705, 805, 915))):
        mourners.append((S, x + r.uniform(-12, 12), 1004 + r.uniform(-8, 8), 0.4 * r.uniform(0.96, 1.04), r.random()))

    def midB(t):
        o = ""
        for k, (S, x, y, s_, rr) in enumerate(sorted(mourners, key=lambda m: m[2])):
            sd = 1 if x < 540 else -1
            q = P(turn=0.15 * sd, gx=0.25 * sd, gy=0.9, sad=0.85, brow=0.85, furrow=-0.4, armR="chest" if rr > 0.5 else "relaxed",
                  armL="relaxed" if rr > 0.3 else "chest", wind=0.4, nod=14, blink=max(blink_at(t, 90 + k), 0.45), breathe=math.sin(t * 1.5 + k))
            o += at_feet(S, q, t, x, y, s_)
        return o + lbg.grave_mound(0.0)
    B = Shot(6.0, gd, midB, cam=camB, bg_par=1.0, light=DUSKL, sun=SUN_DUSK, bloom=0.6, fade_in=0.3, fade_out=0.7,
             fx=[SandWind(140, 401, (0, 700, W, 1300), (400, 800), strength=lambda t: 0.35),
                 Motes(30, 402, (255, 220, 190), (0, 400, W, 1100), (-8, -4), amax=60)])
    return [A, B]


# ================================================================ S5 the news; the grave; night (70.8-103.0)
def s5():
    dd = bg("dunes_day", lambda: lbg.dunes("day"))
    ddb = bg("dunes_day", lambda: lbg.dunes("day"), 6)

    # A1: a young man of the tribe runs over the sand to Majnun
    camA1 = cam_push(1.02, 1.0, 560, 1080, 2.8)
    arrive = 1.9

    def midA1(t):
        u = ease(t / arrive)
        o = gazelles(t, GZ5, startle=0.5)
        x, y, s = M_AT
        look = ease((t - 0.9) / 0.5)
        o += seat_shadow(x, y, 170) + seated(MAJNUN, majnun_sit_q(t, 51, look=0.3 + 0.6 * look, gy=0.2 - 0.3 * look, brow=0.4 + 0.4 * look), t, x, y, s)
        running = t < arrive
        mx = lerp(1200, 840, u)
        q = P(legs="walk" if running else "stand", phase=t * 9.0, turn=-0.35, gx=-0.8, gy=0.1, brow=0.8, furrow=-0.3, sad=0.5,
              armL="forward" if running else "chest", armR="forward" if running else "relaxed", wind=1.0, blink=blink_at(t, 52),
              breathe=math.sin(t * (14 if running else 9)), mouth_o=0.0 if running else 0.25 + 0.15 * math.sin(t * 9), tilt=-4 if running else 0)
        return o + walk_shadow(mx, 1330, 0.56, right=False) + at_feet(MESSENGER, q, t, mx, 1330, 0.56)
    A1 = Shot(2.8, dd, midA1, cam=camA1, light=DAYL, sun=SUN_DAY, bloom=0.5,
             fx=[SandWind(160, 501, (0, 1000, W, 1900), (500, 900), strength=lambda t: 0.4)])

    # A2: the young man close: "Majnun… your father has died." "Until the end, he called your name."
    LA2 = L(73.6, "p5s5a", "p5s5b")
    camA2 = cam_push(1.0, 1.06, 540, 860, 6.4)

    def midA2(t):
        q = tp(LA2, t, 53, turn=-0.25, gx=-0.6, gy=0.2, sad=0.8, brow=0.9, furrow=-0.4, armL="chest", armR="relaxed", wind=0.6)
        q["breathe"] = math.sin(t * (8 if t < 2.0 else 4))
        return at_neck(MESSENGER, q, t, 540, 960, 1.0)
    A2 = Shot(6.4, ddb, midA2, cam=camA2, light=DAYL, sun=SUN_DAY)

    # C: Majnun hears it
    camC = cam_push(1.0, 1.08, 540, 880, 2.6)

    def midC(t):
        sh = ease((t - 0.2) / 0.25)
        down = ease((t - 1.2) / 0.8)
        return majnun_face(t, [], 54, turn=0.25, gx=0.6 - 0.4 * down, gy=0.1 + 0.5 * down, sad=0.3 + 0.6 * down, brow=0.6 + 0.4 * sh, furrow=-0.5,
                           mouth=0.3 * sh * (1 - down), tear_t=1.5)
    C = Shot(2.6, ddb, midC, cam=camC, light=DAYL, sun=SUN_DAY, fade_out=0.4,
             fx=[SandWind(140, 502, (0, 300, W, 1900), (600, 1000), strength=lambda t: 0.3 + 0.5 * ease((t - 0.2) / 0.4))])

    # D: the grave at dusk: "Father… forgive me."
    gd = grave_bg("dusk")
    LD = L(82.6, "p5s1a")
    camD = cam_push(1.0, 1.06, 540, 960, 4.4)

    def midD(t):
        return mourner(t, LD, 55)
    D = Shot(4.4, gd, midD, cam=camD, bg_par=1.0, light=DUSKL, sun=SUN_DUSK, bloom=0.6, fade_in=0.4,
             fx=[SandWind(140, 503, (0, 700, W, 1300), (400, 800), strength=lambda t: 0.3)])

    # E: close: "I never came home." "You looked for me everywhere… and I let you go home alone."
    gdb = grave_bg("dusk", 6)
    LE = L(87.0, "p5s1b", "p5s5c")
    camE = cam_push(1.0, 1.08, 540, 880, 9.8)

    def midE(t):
        low = ease((t - 7.4) / 1.2)
        return majnun_face(t, LE, 56, tear_t=0.4, gy=0.4 + 0.3 * low, gx=-0.1, armR="chest" if 2.6 < t < 7.6 else "relaxed")
    E = Shot(9.8, gdb, midE, cam=camE, light=DUSKL, sun=SUN_DUSK, bloom=0.5,
             fx=[SandWind(100, 504, (0, 300, W, 1900), (500, 900), strength=lambda t: 0.25)])

    # F: night falls on the grave; the stars come out
    gn = grave_bg("night")
    camF = cam_push(1.0, 1.05, 540, 900, 6.2)

    def bgF(t):
        return Image.blend(gd, gn, ease((t - 0.4) / 3.2))

    def midF(t):
        u = ease((t - 0.4) / 3.2)
        return mourner(t, [], 57, u=u, reach=True, bow=ease((t - 0.2) / 1.6), lean=-9 * ease((t - 0.2) / 1.8), gx=-0.3, gy=0.8)
    F = Shot(6.2, bgF, midF, cam=camF, bg_par=1.0, light=TWILIGHT, grade="night", bloom=0.6, fade_out=0.7)
    return [A1, A2, C, D, E, F]


# ================================================================ S6 the hunter and the gazelle (103.0-137.8)
HG = (520, 1268, 0.9)          # the trapped gazelle (x, feet y, scale), facing left
HU = (840, 1300, 0.52)         # the hunter (x, feet y, scale), facing left


def s6():
    dd = bg("dunes_day", lambda: lbg.dunes("day"))
    ddb = bg("dunes_day", lambda: lbg.dunes("day"), 6)

    def trapped(t, pull=1.0):
        gx_, gy_, gs = HG
        jx = -6 * abs(math.sin(t * 2.6)) * pull
        ph = 0.7 * math.sin(t * 5.2) * pull
        o = gz(t, gx_ + jx, gy_, gs, walk=True, phase=ph, look=-0.2, ear=0.8 * pull)
        hx, hy = hoof_xy(gx_ + jx, gy_, gs, t=t, phase=ph, walk=True)
        return o, (hx, hy - 18 * gs)

    def hunter_q(t, lines=(), seed=0, hold=None, **kw):
        base = dict(turn=-0.35, gx=-0.7, gy=0.3, brow=0.3, furrow=0.3, armL="relaxed", wind=0.6)
        base.update(kw)
        q = tp(list(lines), t, seed, **base)
        if hold:
            q["armR"] = feet_ik(HUNTER, HU[0], HU[1], HU[2], *hold, down=True)
        return q

    # A: the hunter holds the rope; the gazelle pulls; Majnun comes (narration)
    camA = cam_push(1.0, 1.05, 560, 1060, 6.4)

    def midA(t):
        o, (rx, ry) = trapped(t)
        hand = (HU[0] - 150, HU[1] - 560)
        hq = hunter_q(t, seed=61, hold=hand)
        rope_ = rope(rx, ry, hand[0] - 6, hand[1] + 12, sag=30)
        mu = ease((t - 2.6) / 3.0)
        mx = lerp(-120, 170, mu)
        walking = 2.6 < t < 5.6
        mq = P(legs="walk" if walking else "stand", phase=t * 4.4, turn=0.35, gx=0.8, gy=0.2, brow=0.4 + 0.5 * ease((t - 5.0) / 0.5), sad=0.4,
               armL="relaxed" if t < 5.4 else "offer", openL=True, armR="relaxed", wind=0.8, blink=blink_at(t, 62), breathe=math.sin(t * 2))
        return (o + snare(rx, ry + 18 * HG[2], HG[2]) + rope_ + walk_shadow(HU[0], HU[1], HU[2], right=False, a=0.18) + at_feet(HUNTER, hq, t, *HU)
                + at_feet(MAJNUN, mq, t, mx, 1330, 0.56))
    A = Shot(6.4, dd, midA, cam=camA, light=DAYL, sun=SUN_DAY, bloom=0.5,
             fx=[SandWind(140, 601, (0, 1000, W, 1900), (500, 900), strength=lambda t: 0.35)])

    # B: Majnun close: "Wait! Please… don't hurt her!"
    LB = L(109.4, "p5s6b")
    camB = cam_push(1.0, 1.05, 540, 880, 2.2)

    def midB(t):
        return majnun_face(t, LB, 63, turn=0.3, gx=0.7, gy=0.2, sad=0.5, brow=1.0, furrow=-0.4, armL="offer", openL=True)
    B = Shot(2.2, ddb, midB, cam=camB, light=DAYL, sun=SUN_DAY)

    # C: the hunter close: "I'm a poor man, friend. My children need to eat."
    LC = L(111.6, "p5s6c")
    camC = cam_push(1.0, 1.05, 540, 860, 3.2)

    def midC(t):
        q = tp(LC, t, 64, turn=-0.25, gx=-0.6, gy=0.1, sad=0.4, brow=0.5, furrow=0.3, armL="chest" if 1.2 < t < 3.0 else "relaxed", armR="relaxed",
               wind=0.5)
        return at_neck(HUNTER, q, t, 540, 960, 1.0)
    C = Shot(3.2, ddb, midC, cam=camC, light=DAYL, sun=SUN_DAY)

    # D: the purse: "Then take this gold… and let her go." — "All this gold… for one gazelle?"
    LDm = L(114.8, "p5s6d")
    LDh = L(114.8, "p5s6e")
    camD = cam_push(1.0, 1.05, 540, 1000, 5.8)
    DM, DH = (320, 1560, 0.66), (770, 1570, 0.66)

    def midD(t):
        give = ease((t - 0.4) / 0.6)
        handed = t > 2.0
        mid_x, mid_y = (DM[0] + DH[0]) / 2, DM[1] - 640
        m_hand = (lerp(DM[0] + 150, mid_x - 20, give), lerp(DM[1] - 560, mid_y, give)) if not handed else (lerp(mid_x - 20, DM[0] + 140, ease((t - 2.0) / 0.6)),
                                                                                                              lerp(mid_y, DM[1] - 540, ease((t - 2.0) / 0.6)))
        reach = ease((t - 1.3) / 0.5)
        lift_ = ease((t - 3.2) / 0.5)
        h_hand = (lerp(DH[0] - 150, mid_x + 20, reach), lerp(DH[1] - 560, mid_y, reach)) if not handed else (lerp(mid_x + 20, DH[0] - 90, lift_),
                                                                                                              lerp(mid_y, DH[1] - 820, lift_))
        mq = tp(LDm, t, 65, turn=0.35, gx=0.7, gy=0.2, sad=0.4, brow=0.6, furrow=-0.3,
                armL=feet_ik(MAJNUN, DM[0], DM[1], DM[2], *m_hand) if t < 2.5 else "relaxed",
                propL=None if handed else "purse", armR="relaxed", wind=0.6)
        amazed = ease((t - 2.9) / 0.4)
        hq = tp(LDh, t, 66, turn=-0.35, gx=-0.7 + 0.5 * amazed, gy=0.3 - 0.6 * amazed, brow=0.3 + 0.7 * amazed, furrow=0.3 - 0.6 * amazed,
                armR=feet_ik(HUNTER, DH[0], DH[1], DH[2], *h_hand, down=not handed), propR="purse" if handed else None, armL="relaxed", wind=0.6)
        return at_feet(MAJNUN, mq, t, *DM) + at_feet(HUNTER, hq, t, *DH)
    D = Shot(5.8, dd, midD, cam=camD, light=DAYL, sun=SUN_DAY, bloom=0.5)

    # E1: Majnun close: "Look at her eyes…"
    LE = L(120.6, "p5s6f")
    camE1 = cam_push(1.0, 1.04, 540, 880, 1.8)

    def midE1(t):
        return majnun_face(t, LE, 67, turn=-0.2, gx=-0.5, gy=0.5, sad=0.4, brow=0.7, furrow=-0.4, smile=0.3)
    E1 = Shot(1.8, ddb, midE1, cam=camE1, light=DAYL, sun=SUN_DAY)

    # E2: …"They are Leyli's eyes." — the gazelle's face, close
    camE2 = cam_push(1.0, 1.06, 560, 720, 2.2)

    def midE2(t):
        return gz(t, 930, 1826, 2.6, look=1.0, ear=0.3)

    def glint(im, t):
        x, y = cam_xy(camE2, t, 580, 717)
        a = ease((t - 0.5) / 0.4) * (1 - ease((t - 1.4) / 0.6))
        if a > 0.01:
            d = ImageDraw.Draw(im, "RGBA")
            rr = 10 + 22 * a
            d.polygon([(x - rr, y), (x - 3, y - 3), (x, y - rr), (x + 3, y - 3), (x + rr, y), (x + 3, y + 3), (x, y + rr), (x - 3, y + 3)],
                      fill=(255, 255, 240, int(220 * a)))
    E2 = Shot(2.2, ddb, midE2, cam=camE2, light=DAYL, sun=SUN_DAY, bloom=0.7, fx=[glint, Motes(20, 603, (255, 240, 210), (300, 400, 800, 1000), (6, -4), amax=80)])

    # F: Majnun loosens the snare; she steps away… looks back… and comes back to him (narration)
    camF = cam_push(1.3, 1.34, 540, 1920, 6.4)
    FM = (720, 1272, 0.5)

    def midF(t):
        gx0, gy0, gs = 450, HG[1], HG[2]
        # her path: still (0-1.6), a few steps away to the left (1.6-3.0), a look back (3.0-3.6), round (3.6-4.0), back to him (4.0-5.2)
        if t < 1.6:
            x, face, walk = gx0, 1.0, False
        elif t < 3.0:
            x, face, walk = lerp(gx0, gx0 - 150, ease((t - 1.6) / 1.4)), 1.0, True
        elif t < 3.76:
            x, face, walk = gx0 - 150, 1.0, False
        elif t < 4.0:
            x, face, walk = gx0 - 150, math.cos(math.pi * (t - 3.76) / 0.24), False
        else:
            x, face, walk = lerp(gx0 - 150, gx0 - 10, ease((t - 4.0) / 1.2)), -1.0, t < 5.2
        face = face if abs(face) > 0.3 else 0.3 * (1 if face >= 0 else -1)
        hop = 26 * math.sin(math.pi * min(1.0, max(0.0, (t - 3.7) / 0.36)))       # a little hop as she turns round
        look = 1.0 if 3.0 < t < 3.6 else (0.3 if t >= 5.2 else -0.2)
        graze = 0.35 * ease((t - 5.3) / 0.6)
        o = gz(t, x, gy0 - hop, gs, face=face, walk=walk, phase=t * 6.0, look=look, graze=graze, ear=0.6 if t < 1.2 else 0.0)
        hx, hy = hoof_xy(gx0, gy0, gs, t=t)
        loose = ease((t - 0.4) / 0.9)
        if t < 1.6:
            o += snare(hx, hy + 6 * loose, gs * (1 + 0.4 * loose))
        else:
            o += f'<path d="M {hx - 30:.0f} {hy + 4:.0f} q 30 10 70 0 q 30 -8 60 4" stroke="#8a6a3a" stroke-width="6" fill="none" stroke-linecap="round"/>'
        mx, my, ms = FM
        if t < 1.7:
            m_hand = (lerp(hx + 40, hx + 6, ease(t / 0.4)), hy - 26)
        elif t < 5.0:
            m_hand = (lerp(hx + 6, mx - 110, ease((t - 1.7) / 0.6)), lerp(hy - 26, my - 160, ease((t - 1.7) / 0.6)))
        else:
            m_hand = (lerp(mx - 110, x + 90, ease((t - 5.0) / 0.6)), lerp(my - 160, gy0 - 250 * gs, ease((t - 5.0) / 0.6)))
        smile = 0.5 * ease((t - 3.2) / 0.8)
        mq = P(legs="sit", turn=-0.3, gx=-0.7, gy=0.6 if t < 1.7 else 0.3, sad=0.4 * (1 - smile), brow=0.5, furrow=-0.3, smile=smile,
               armR=seat_ik(MAJNUN, mx, my, ms, *m_hand, down=t < 1.7), armL=("ik", 60, 330), wind=0.6, blink=blink_at(t, 71),
               breathe=math.sin(t * 1.6))
        return seat_shadow(mx, my, 120) + o + seated(MAJNUN, mq, t, mx, my, ms)
    F = Shot(6.4, dd, midF, cam=camF, bg_par=1.0, light=DAYL, sun=SUN_DAY, bloom=0.5,
             fx=[SandWind(100, 604, (0, 1000, W, 1900), (500, 900), strength=lambda t: 0.25)])

    # G: dusk: Majnun among his gazelles; the birds (narration: the animals of the desert were his only family)
    dn = bg("dunes_dusk", lambda: lbg.dunes("dusk"))
    camG = cam_push(1.0, 1.05, 520, 1080, 6.8)
    herd = [(600, 1262, 0.95, 0.4), (790, 1232, 0.8, 0.0), (190, 1238, 0.74, 0.6), (930, 1214, 0.62, 0.2)]

    def midG(t):
        o = ""
        for k, (x, y, s, lk) in sorted(enumerate(herd), key=lambda e: e[1][1]):
            o += gz(t + k * 1.3, x, y, s, seed=k, look=lk, graze=(0.5 if k in (1, 3) else 0.0) * (0.6 + 0.4 * math.sin(t * 0.5 + k)))
        x, y, s = M_AT
        hand = (540, 1012)
        q = P(legs="sit", turn=0.3, gx=0.6, gy=0.4, sad=0.1, smile=0.35, brow=0.4, furrow=-0.2, armL=seat_ik(MAJNUN, x, y, s, *hand), armR="relaxed",
              wind=0.6, blink=blink_at(t, 73), breathe=math.sin(t * 1.4))
        return birds(t, 960, 430, n=5, s=0.9) + seat_shadow(x, y, 170) + seated(MAJNUN, q, t, x, y, s) + o
    G = Shot(6.8, dn, midG, cam=camG, light=DUSKL, sun=SUN_DUSK, bloom=0.7, fade_out=0.6,
             fx=[SandWind(160, 605, (0, 1000, W, 1900), (500, 900), strength=lambda t: 0.35), Motes(30, 606, (255, 230, 210), (0, 800, W, 1500), (-8, -4), amax=70)])
    return [A, B, C, D, E1, E2, F, G]


# ================================================================ S7 an old man with a letter (137.8-156.4, end card 151.2)
def s7():
    dn = bg("dunes_dusk", lambda: lbg.dunes("dusk"))
    dnb = bg("dunes_dusk", lambda: lbg.dunes("dusk"), 6)

    # A: an old man comes over the dunes towards Majnun and his gazelles (narration)
    camA = cam_push(1.0, 1.05, 560, 1080, 5.0)

    def midA(t):
        o = gazelles(t, [(600, 1262, 0.95, 0.3), (190, 1238, 0.74, 0.6)], startle=3.6)
        x, y, s = M_AT
        look = ease((t - 3.4) / 0.6)
        o += seat_shadow(x, y, 170) + seated(MAJNUN, majnun_sit_q(t, 81, look=0.3 + 0.6 * look, gy=0.3 - 0.4 * look, brow=0.4 + 0.4 * look), t, x, y, s)
        u = ease(t / 5.0)
        ox = lerp(1130, 860, u); oy = lerp(1210, 1300, u); os_ = lerp(0.3, 0.5, u)
        q = P(legs="walk", phase=t * 2.3, turn=-0.35, gx=-0.7, gy=0.1, brow=0.4, furrow=0.0, armR=staff_walk(t, side=-1), propR="staff",
              armL="relaxed", wind=0.8, blink=blink_at(t, 82), breathe=math.sin(t * 2))
        return o + walk_shadow(ox, oy, os_, right=False) + at_feet(OLD_MSG, q, t, ox, oy, os_)
    A = Shot(5.0, dn, midA, cam=camA, light=DUSKL, sun=SUN_DUSK, bloom=0.7,
             fx=[SandWind(160, 701, (0, 1000, W, 1900), (500, 900), strength=lambda t: 0.4)])

    # B: the old messenger close, holding out a rolled letter: "Are you Majnun? I have a letter for you…" "…from Leyli."
    LB = L(142.8, "p5s7b", "p5s7c")
    camB = cam_push(1.0, 1.05, 540, 860, 5.8)

    def midB(t):
        out = ease((t - 1.0) / 0.7)
        q = tp(LB, t, 83, turn=-0.25, gx=-0.6, gy=0.1, brow=0.5, furrow=-0.1, smile=0.25 * ease((t - 3.6) / 0.6),
               armR=("ik", lerp(-150, -270, out), lerp(330, 190, out)), propR=("scroll", 70), armL=("ik", 190, 520), propL="staff", wind=0.7)
        return at_neck(OLD_MSG, q, t, 580, 860, 0.85)
    B = Shot(5.8, dnb, midB, cam=camB, light=DUSKL, sun=SUN_DUSK, bloom=0.5,
             fx=[SandWind(100, 702, (0, 300, W, 1900), (500, 900), strength=lambda t: 0.3)])

    # C: Majnun hears her name (under the end card from 2.6 s)
    camC = cam_push(1.0, 1.1, 540, 880, 7.8)

    def midC(t):
        hope = ease((t - 0.3) / 1.0)
        return majnun_face(t, [], 84, turn=0.25, gx=0.6, gy=-0.1 + 0.2 * (1 - hope), sad=0.6 * (1 - hope), brow=0.7 + 0.3 * hope, furrow=-0.4,
                           smile=0.35 * ease((t - 1.0) / 1.0), mouth=0.15 * hope, armR="chest" if t > 1.4 else "relaxed")
    C = Shot(7.8, dnb, midC, cam=camC, light=DUSKL, sun=SUN_DUSK, bloom=0.6, fade_out=0.8,
             fx=[Motes(40, 703, (255, 230, 190), (0, 300, W, 1500), (6, -10), amax=90)])
    return [A, B, C]


SCENES = {"s1": s1, "s2": s2, "s3": s3, "s4": s4, "s5": s5, "s6": s6, "s7": s7}
