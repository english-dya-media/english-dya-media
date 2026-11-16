"""Part 7 · The Betrayal (episode 4, half 1) — 2D cartoon. Timing matches p07_audio.py:
s1 0-14 the hook: Sahl's castle at night (the caliph's letter, Babak asleep, the rider to Afshin) · s2 14-18.6 title (the autumn valley) ·
s3 18.6-53.6 the hunt, 15 September 837 · s4 53.6-84.2 the winter road; Samarra, 4 January 838 · s5 84.2-112.2 the robe, the elephant,
the gates of the palace (end card from 107.6)."""
import math, random
import numpy as np
from PIL import Image, ImageFilter, ImageDraw
from film import Shot, W, H, ease, lerp, talk_pose, blink_at, cam_push, cam_static, Snow, Motes, Embers, svg_render
from chars import pose, horse, dog, elephant, kneel_drop, Ctx, FEET, fmt
from stage import at_neck, at_feet, lying_at, crowd_row, back_heads, rider, Glow, lw_for, glow_img, howdah
import bgs
from cast import *
from p01_scenes import P, blur_bg, WARM
from p02_scenes import birds
from p03_scenes import enemy_spec, pole_flag, DUSTDEF, dust
from p05_scenes import flame, glow, GLOWDEF

RS = 0.31                        # rider size relative to the horse (stage.rider)
ROOM = dict(point=(720, 760, 1000, 0.55, 1.15, (1.0, 0.6, 0.3)), rim_point=(760, 5), rim_col=(1.0, 0.7, 0.4), rim_str=0.6)
ROOM_CLOSE = dict(rim=(5, -3), rim_col=(1.0, 0.68, 0.38), rim_str=0.8, ramp=(0, W, 0.8, 1.08))
BEDLIGHT = dict(point=(880, 1050, 800, 0.45, 1.15, (1.0, 0.6, 0.3)), rim_point=(880, 5), rim_col=(1.0, 0.7, 0.4), rim_str=0.6)
GATE = dict(point=(540, 1250, 900, 0.5, 1.2, (1.0, 0.6, 0.3)), rim_point=(540, 5), rim_col=(1.0, 0.7, 0.4))
NIGHTRIDE = dict(ambient=(0.55, 0.62, 0.9), rim=(-4, -3), rim_col=(0.75, 0.82, 1.0), rim_str=0.6)
MORNING = dict(rim=(5, -3), rim_col=(1.0, 0.86, 0.62), rim_str=0.8, ramp=(0, W, 0.92, 1.05))
MORNING_SUN = (880, 760, 900, (0.10, 0.07, 0.03))
SNOWL = dict(rim=(4, -2), rim_col=(0.9, 0.92, 1.0), rim_str=0.5, ambient=(0.93, 0.95, 1.0), ramp=(0, W, 0.94, 1.02))
SAMARRA = dict(rim=(-5, -2), rim_col=WARM, ramp=(0, W, 1.06, 0.84))
SAMARRA_SUN = (150, 1250, 700, (0.10, 0.06, 0.02))
HALL = dict(rim=(0, -4), rim_col=(1.0, 0.85, 0.55), ramp=(0, W, 0.95, 1.02), ambient=(1.02, 0.96, 0.86))
COURT = dict(rim=(5, -3), rim_col=(1.0, 0.86, 0.66), rim_str=0.7, ramp=(0, W, 0.95, 1.05))
COURT_SUN = (300, 700, 900, (0.10, 0.07, 0.04))


# ------------------------------------------------------------------ helpers
def ride7(S, q, t, x, y, s, col, k=0.0, gait="walk", flip=False, blanket=None, mane="#0a0808", head_down=0.0):
    rate = {"walk": 4.2, "trot": 6.5, "gallop": 9.5}.get(gait, 0.0)
    return rider(S, q, t, lambda c: horse(c, col=col, mane=mane, walk=gait != "stand", phase=t * rate + k, t=t + k, blanket=blanket,
                                          head_down=head_down), x, y, s, flip=flip)


def rider_xy(x, y, s, ax, ay, flip=False, bs=1.0):
    """world position of a rider's body point (arm coords) for ride7/rider(x, y, s)"""
    neck_y = -404 - 330 * RS * bs
    return x + (-s if flip else s) * (10 + RS * bs * ax), y + s * (neck_y + RS * bs * ay)


def rider_tf(x, y, s, flip=False):
    """SVG transform that maps a rider's body coords to the world (for things drawn on a rider, e.g. his sword)"""
    neck_y = -404 - 330 * RS
    sx = -s if flip else s
    return f"translate({x + sx * 10:.1f},{y + s * neck_y:.1f}) scale({sx * RS:.4f},{s * RS:.4f})"


def feet_xy(x, y, s, ax, ay, flip=False, bs=1.0):
    """world position of a body point of a person placed with at_feet(x, y, s)"""
    return x + (-s if flip else s) * bs * ax, y + s * bs * (ay - FEET)


def to_body(x, y, s, wx, wy):
    """inverse of feet_xy (no flip, bs 1): a world point in the body coords of a person at_feet(x, y, s), for ("ik", …) targets"""
    return (wx - x) / s, (wy - y) / s + FEET


class Leaves:
    """autumn leaves tumbling across the frame"""
    def __init__(self, n=40, seed=7, box=(0, 250, W, 1650), drift=(-140, 70), size=(8, 15),
                 cols=((206, 102, 38), (232, 168, 58), (168, 62, 26), (240, 196, 90))):
        r = np.random.default_rng(seed)
        self.p = [(r.uniform(box[0], box[2]), r.uniform(box[1], box[3]), r.uniform(*size), r.uniform(0, 6.3), r.uniform(0.6, 1.4),
                   cols[int(r.integers(len(cols)))]) for _ in range(n)]
        self.box, self.dr = box, drift

    def __call__(self, im, t):
        d = ImageDraw.Draw(im, "RGBA")
        x0, y0, x1, y1 = self.box
        for x, y, s, ph, sp, col in self.p:
            px = x0 + (x - x0 + self.dr[0] * sp * t + 26 * math.sin(t * 1.4 + ph)) % (x1 - x0)
            py = y0 + (y - y0 + self.dr[1] * sp * t) % (y1 - y0)
            a = t * 2.6 * sp + ph; w = 0.25 + 0.45 * abs(math.cos(t * 3.1 * sp + ph))
            ca, sa = math.cos(a), math.sin(a)
            d.polygon([(px + ca * s, py + sa * s), (px - sa * s * w, py + ca * s * w), (px - ca * s, py - sa * s), (px + sa * s * w, py - ca * s * w)],
                      fill=col + (235,))


def falcon_fly(x, y, s, t, ang=-25.0, d=1):
    """a falcon in flight, facing right (d=-1: left), wings beating"""
    up = -80 * math.sin(t * 15)
    return (f'<g transform="translate({x:.1f},{y:.1f}) scale({d},1) rotate({ang:.1f}) scale({s:.3f})">'
            f'<path d="M -6 -4 C -30 {up * 0.4 - 12:.1f}, -60 {up - 24:.1f}, -96 {up - 44:.1f} C -56 {up * 0.5:.1f}, -24 8, 12 4 Z" fill="#3e342c" stroke="#1b0f0a" stroke-width="4"/>'
            f'<path d="M -60 0 L -122 -16 L -126 16 Z" fill="#5a4a3e" stroke="#1b0f0a" stroke-width="4"/>'
            f'<ellipse cx="0" cy="0" rx="64" ry="20" fill="#6a5a4c" stroke="#1b0f0a" stroke-width="4"/>'
            f'<path d="M 4 12 C 26 18, 48 14, 60 6" stroke="#efe4cc" stroke-width="8" fill="none"/>'
            f'<circle cx="62" cy="-8" r="18" fill="#5a4a3e" stroke="#1b0f0a" stroke-width="4"/>'
            f'<path d="M 78 -10 L 98 -2 L 78 3 Z" fill="#e0b040" stroke="#1b0f0a" stroke-width="3"/><circle cx="68" cy="-12" r="4" fill="#120a06"/>'
            f'<path d="M 14 -2 C -6 {up * 0.35 - 14:.1f}, -34 {up * 0.9 - 30:.1f}, -74 {up * 1.1 - 50:.1f} C -34 {up * 0.45:.1f}, -6 10, 24 6 Z" fill="#6a5a4c" stroke="#1b0f0a" stroke-width="4"/></g>')


def hip_sword(grip=False):
    """Babak's sword at his right hip, where his strap ends (body coords; draw it over the person with the person's transform)"""
    o = ('<path d="M -192 436 L -272 902 L -240 908 L -166 442 Z" fill="#3a2414" stroke="#1b0f0a" stroke-width="5"/>'
         '<path d="M -268 880 L -244 884" stroke="#b9832f" stroke-width="10"/>'
         '<path d="M -150 420 L -212 446" stroke="#b9832f" stroke-width="18" stroke-linecap="round"/>')
    if not grip:
        o += '<path d="M -178 430 L -154 338" stroke="#2a1a10" stroke-width="20" stroke-linecap="round"/>'
    return o + '<circle cx="-150" cy="326" r="16" fill="#b9832f" stroke="#1b0f0a" stroke-width="4"/>'


SWORD_GRIP = ("ik", -168, 388)           # the right hand on the hilt (body coords)


def open_letter(x, y, s=1.0, ang=0.0):
    """the caliph's letter, opened: a sheet with lines of writing and a black seal (centre x, y)"""
    rows = "".join(f'<path d="M -78 {-46 + 18 * k} L {60 - 14 * (k % 3)} {-46 + 18 * k}" stroke="#6a5a40" stroke-width="5" opacity="0.7"/>' for k in range(5))
    return (f'<g transform="translate({x:.1f},{y:.1f}) rotate({ang:.1f}) scale({s:.3f})"><path d="M -96 -70 L 96 -70 L 96 70 L -96 70 Z" fill="#f0e2c0" stroke="#1b0f0a" stroke-width="5"/>'
            f'{rows}<circle cx="58" cy="44" r="20" fill="#121216" stroke="#c9a24a" stroke-width="4"/></g>')


def folded_note(x, y, s=1.0, ang=0.0):
    return (f'<g transform="translate({x:.1f},{y:.1f}) rotate({ang:.1f}) scale({s:.3f})"><path d="M -40 -28 L 40 -28 L 40 28 L -40 28 Z" fill="#f2e8d0" stroke="#1b0f0a" stroke-width="5"/>'
            f'<path d="M -40 -28 L 0 4 L 40 -28" stroke="#8a7a5a" stroke-width="4" fill="none"/></g>')


def _bez(p0, p1, p2, p3, n=24):
    return [((1 - u) ** 3 * p0[0] + 3 * (1 - u) ** 2 * u * p1[0] + 3 * (1 - u) * u * u * p2[0] + u ** 3 * p3[0],
             (1 - u) ** 3 * p0[1] + 3 * (1 - u) ** 2 * u * p1[1] + 3 * (1 - u) * u * u * p2[1] + u ** 3 * p3[1]) for u in [i / n for i in range(n + 1)]]


_CREST = _bez((-40, 1020), (200, 960), (500, 1000), (700, 950)) + _bez((700, 950), (860, 915), (1000, 950), (1120, 930))[1:]


def crest_y(x):
    """the top of the wooded slope in forest_road (where riders appear on the hillside)"""
    for (xa, ya), (xb, yb) in zip(_CREST, _CREST[1:]):
        if xa <= x <= xb:
            return ya + (yb - ya) * (x - xa) / max(1e-6, xb - xa)
    return _CREST[-1][1]


def banner_on(t, hx, hy, s, d=1, col="#121216", k=0):
    """a black banner on a pole held at the hand (hx, hy) of a rider of horse scale s, trailing behind the direction d"""
    return pole_flag(t + k, hx, hy - 330 * s, h=420 * s, w=160 * s, fh=90 * s, col=col, d=d)


def enemy_rider(t, r, x, y, s, k, d=1, gait="gallop", banner=False, opacity=1.0):
    S = enemy_spec(r)
    q = P(turn=0.45 * d, gx=0.8 * d, gy=0.0, furrow=0.7, armR="forward", armL=("ik", 200, 160) if banner else "forward", legs="none", wind=0.7,
          blink=blink_at(t, 750 + k))
    o = ride7(S, q, t, x, y, s, r.choice(["#1e1a1c", "#2a2224", "#3a2a1e", "#141214"]), k=k, gait=gait, flip=d < 0, blanket="#121216")
    if banner:
        hx, hy = rider_xy(x, y, s, 200, 160, flip=d < 0)
        o += banner_on(t, hx, hy, s, d=d, k=k)
    return o if opacity >= 1 else f'<g opacity="{max(0.0, opacity):.2f}">{o}</g>'


# ================================================================ S1 the hook: Sahl's castle at night (0-14)
def s1():
    room = bgs.cached("sahl_room", bgs.sahl_room)
    # A: the steward reads the caliph's letter; Sahl listens (0-5.6)
    LA = [("p7s1a", 0.6), ("p7s1b", 3.9)]
    def midA(t):
        o = ""
        up = ease((t - 3.6) / 0.4)
        st = talk_pose(LA, t, 701, dict(turn=0.3, gx=0.4 + 0.4 * up, gy=0.6 - 0.6 * up, furrow=0.3, brow=0.2 + 0.3 * up,
                                        armL=("ik", 70, 370), armR=("ik", -70, 370)))
        o += at_feet(STEWARD, P(**st), t, 300, 1620, 0.74)
        lx, ly = feet_xy(300, 1620, 0.74, 0, 330)
        o += open_letter(lx, ly, 0.8, -3 + 2 * math.sin(t * 1.3))
        cold = ease((t - 4.0) / 0.8)
        sq = talk_pose([], t, 702, dict(turn=-0.3, gx=-0.6, gy=0.25 - 0.25 * cold, furrow=0.2 + 0.7 * cold, brow=0.3 - 0.5 * cold, smile=0.0,
                                        nod=6 * ease((t - 5.0) / 0.3), armL="relaxed", armR="chest" if t < 2.2 else "relaxed"))
        o += at_feet(SAHL, P(**sq), t, 740, 1630, 0.75)
        return o
    A = Shot(5.6, room, midA, cam=cam_push(1.0, 1.06, 540, 950, 5.6), light=ROOM, grade="fire", fade_in=0.4,
             fx=[Motes(30, 701, (255, 210, 150), (300, 300, 1000, 1300), (4, -6), amax=70)])
    # B: Babak asleep in the guest room (5.6-8.0)
    bed = bgs.cached("bedroom", bgs.bedroom)
    def midB(t):
        o = GLOWDEF + glow(880, 1040, 150, 0.85) + flame(880, 1050, 0.45, t, 7)
        o += lying_at(BABAK_SLEEP, P(blink=1.0, armL="relaxed", armR="relaxed", wind=0.1, breathe=math.sin(t * 1.3), turn=0.0, furrow=0.0, gx=0.0), t, 650, 1150, 0.42)
        o += '<path d="M 470 1080 C 560 990, 800 986, 856 1036 L 856 1176 L 470 1176 Z" fill="#5a2a3a" stroke="#1b0f0a" stroke-width="4"/>'
        o += '<path d="M 476 1096 C 562 1012, 796 1008, 852 1054" stroke="#c9a24a" stroke-width="6" fill="none" opacity="0.8"/>'
        return o
    B = Shot(2.4, bed, midB, cam=cam_push(1.3, 1.4, 560, 1090, 2.4), light=BEDLIGHT, grade="fire")
    # C: at the gate, Sahl gives the rider a folded note (8.0-12.0)
    ag = bgs.cached("armenia_gate", bgs.armenia_gate)
    LC = [("p7s1c", 0.3), ("p7s1d", 2.0)]
    def midC(t):
        o = GLOWDEF
        for x in (330, 750):
            o += glow(x, 1010, 160, 0.9) + flame(x, 1030, 0.6, t, x)
        c = Ctx(lw_for(0.5))
        o += f'<g transform="translate(1010,1450) scale(-0.5,0.5)">{horse(c, col="#4a3a32", mane="#0a0808", t=t, head_down=0.3, blanket="#26262e")}</g>'
        give = ease((t - 1.0) / 0.5); take = t > 2.9
        sq = talk_pose(LC, t, 703, dict(turn=0.3, gx=0.7, gy=0.0, furrow=0.6, brow=-0.1, smile=0.0,
                                        armL=("ik", lerp(60, 400, give), lerp(330, 150, give)) if not take else ("ik", lerp(400, 120, ease((t - 2.9) / 0.5)), lerp(150, 330, ease((t - 2.9) / 0.5))),
                                        armR="relaxed"))
        o += at_feet(SAHL, P(**sq), t, 300, 1700, 0.64)
        rq = talk_pose([], t, 704, dict(turn=-0.3, gx=-0.6, gy=0.1, furrow=0.4, nod=8 * ease((t - 3.3) / 0.3),
                                        armR=("ik", -380, 170) if 2.3 < t < 3.2 else (("ik", -60, 300) if t >= 3.2 else "relaxed"), armL="relaxed"))
        o += at_feet(NIGHT_RIDER, P(**rq), t, 790, 1700, 0.62)
        if not take:
            nx, ny = feet_xy(300, 1700, 0.64, lerp(60, 400, give) + 20, lerp(330, 150, give) - 10)
        else:
            u = ease((t - 2.9) / 0.4)
            nx, ny = feet_xy(790, 1700, 0.62, lerp(-380, -60, u) - 20, lerp(170, 300, u) - 10)
        o += folded_note(nx, ny, 0.6, -10)
        return o
    C = Shot(4.0, ag, midC, cam=cam_push(1.0, 1.04, 540, 1100, 4.0), light=GATE, grade="fire")
    # D: the rider gallops off into the dark (12.0-14.0)
    fn = bgs.cached("forest_road_night", lambda: bgs.forest_road("night"))
    def midD(t):
        x = 380 + 470 * t
        q = P(turn=0.45, gx=0.8, furrow=0.7, armR="forward", armL="forward", legs="none", wind=1.0, blink=blink_at(t, 705))
        return ride7(NIGHT_RIDER, q, t, x, 1380, 0.46, "#2a2224", gait="gallop", blanket="#26262e")
    D = Shot(2.0, fn, midD, cam=cam_push(1.0, 1.03, 540, 1200, 2.0), light=NIGHTRIDE, grade="night", fade_out=0.7)
    return [A, B, C, D]


# ================================================================ S2 title: the autumn valley at sunrise (14.0-18.6)
def s2():
    au = bgs.cached("forest_road_autumn", lambda: bgs.forest_road("autumn"))
    return [Shot(4.6, au, lambda t: birds(t, 700, 520), cam=cam_push(1.0, 1.05, 540, 1000, 4.6), light=MORNING, sun=MORNING_SUN,
                 fx=[Leaves(30, 711)], fade_in=0.4, fade_out=0.5)]


# ================================================================ S3 the hunt, 15 September 837 (18.6-53.6)
def hunters(t, xb, xs, yb, ys, sb, ss, gait="walk", babak_q=None, sahl_q=None, falcon=True):
    """Babak (far) and Sahl (near) side by side on their horses, facing right"""
    bq = babak_q or P(turn=0.4, gx=0.7, furrow=0.2, armR="forward", armL="forward", legs="none", wind=0.4, blink=blink_at(t, 721))
    sq = sahl_q or P(turn=0.35, gx=0.6, smile=0.4, armR="forward", armL=("ik", 250, 300), propL="falcon" if falcon else None, legs="none", wind=0.4,
                     blink=blink_at(t, 722))
    return (ride7(BABAK_GUEST, bq, t, xb, yb, sb, "#6a3a1e", k=1.3, gait=gait, blanket="#8e1c1c") +
            ride7(SAHL, sq, t, xs, ys, ss, "#d8d0c4", k=0.0, gait=gait, mane="#6a5a4a", blanket="#24466a"))


def dogs(t, x0, y, s, speed=150.0, run=True):
    c = Ctx(lw_for(s))
    o = ""
    for k, (dx, dy, col, dark) in enumerate([(0, 0, "#d8b888", "#a87848"), (-150, 26, "#6a5040", "#3a2a20")]):
        x = x0 + dx + speed * t
        o += f'<g transform="translate({x:.1f},{y + dy:.1f}) scale({s * (1 + 0.06 * k):.3f})">{dog(c, col=col, dark=dark, phase=t * 11 + k * 1.9, run=run, t=t + k, seed=k)}</g>'
    return o


def s3():
    au = bgs.cached("forest_road_autumn", lambda: bgs.forest_road("autumn"))
    aub = blur_bg("forest_road_autumn", lambda: bgs.forest_road("autumn"), 9)
    # A: wide, the hunting party rides along the valley (18.6-24.0)
    def midA(t):
        x = 230 + 52 * t
        return dogs(t, 560, 1430, 0.3, speed=60) + hunters(t, x, x + 70, 1370, 1405, 0.36, 0.38) + birds(t, 760, 600)
    A = Shot(5.4, au, midA, cam=cam_push(1.0, 1.05, 540, 1150, 5.4), light=MORNING, sun=MORNING_SUN, fx=[Leaves(34, 712)], fade_in=0.4)
    # B: two-shot on horseback: "Come, my friend. Today we hunt, like kings." (24.0-29.2)
    LB = [("p7s3a", 0.4), ("p7s3b", 2.0)]
    def midB(t):
        sq = talk_pose(LB, t, 723, dict(turn=-0.25, gx=-0.6, gy=-0.1, smile=0.55, brow=0.3, armR="forward", armL=("ik", 250, 300), propL="falcon",
                                        legs="none", wind=0.4))
        bq = talk_pose([], t, 724, dict(turn=0.35, gx=0.7, gy=0.1, smile=0.35 * ease((t - 3.4) / 0.6), furrow=0.1, armR="forward", armL="forward",
                                        legs="none", wind=0.4))
        return hunters(t, 430, 620, 1330, 1420, 0.88, 1.0, babak_q=P(**bq), sahl_q=P(**sq))
    B = Shot(5.2, aub, midB, cam=cam_push(1.0, 1.04, 540, 950, 5.2), light=MORNING, sun=MORNING_SUN, fx=[Leaves(40, 713, drift=(-420, 60))])
    # C: Sahl lifts his fist and lets the falcon go (29.2-32.6)
    def midC(t):
        lift = ease((t - 0.4) / 0.5) * (1 - ease((t - 1.9) / 0.6)); gone = t > 1.0
        sq = P(turn=0.2 - 0.5 * ease((t - 1.0) / 0.4), gx=0.5 - 1.1 * ease((t - 1.0) / 0.4), gy=-0.8 * ease((t - 0.4) / 0.5), smile=0.5, brow=0.4, armR="forward",
               armL=("ik", lerp(250, 330, lift), lerp(300, -210, lift)), propL=None if gone else "falcon", legs="none", wind=0.4, blink=blink_at(t, 725))
        o = ride7(SAHL, sq, t, 560, 1560, 1.3, "#d8d0c4", gait="walk", mane="#6a5a4a", blanket="#24466a")
        if gone:
            u = t - 1.0
            hx, hy = rider_xy(560, 1560, 1.3, 330, -210)
            o += falcon_fly(hx - 150 * u - 20 * u * u, hy - 50 - 210 * u - 40 * u * u, 0.9 + 0.25 * u, t, ang=-28, d=-1)
        return o
    C = Shot(3.4, aub, midC, cam=cam_push(1.0, 1.04, 560, 900, 3.4), light=MORNING, sun=MORNING_SUN, fx=[Leaves(30, 714, drift=(-380, 60))])
    # D: the horn: black banners rise along the hillside on every side (32.6-35.8)
    ridge = [(60 + 92 * k + random.Random(k).uniform(-20, 20), 0.12 + 0.18 * (k % 5) + 0.05 * random.Random(k + 9).random()) for k in range(11)]
    def ridge_riders(t, t0=0.0, descend=0.0):
        o = ""
        for k, (x, ap) in enumerate(ridge):
            u = ease((t - t0 - ap * 2.6) / 0.5)
            if u <= 0:
                continue
            y = crest_y(x) + 26 + 40 * descend
            o += enemy_rider(t, random.Random(760 + k), x + 20 * descend * (1 if x < 540 else -1), y + 18 * (1 - u), 0.13, k, d=1 if x < 540 else -1,
                             gait="walk" if descend else "stand", banner=k % 2 == 0, opacity=u)
        return o
    def stopped(t, look=0.0):
        bq = P(turn=0.4 - 0.4 * look, gx=0.7 - 0.7 * look, gy=-0.6 * look, furrow=0.2 + 0.6 * look, armR="forward", armL="forward", legs="none", wind=0.4,
               blink=blink_at(t, 726))
        sq = P(turn=0.35, gx=0.6, gy=-0.3 * look, furrow=0.3, armR="forward", armL="relaxed", legs="none", wind=0.4, blink=blink_at(t, 727))
        return hunters(t, 470, 540, 1370, 1405, 0.36, 0.38, gait="stand", babak_q=bq, sahl_q=sq, falcon=False)
    def midD(t):
        return ridge_riders(t) + dogs(0.0, 700, 1430, 0.3, speed=0, run=False) + stopped(t, ease((t - 0.3) / 0.6))
    D = Shot(3.2, au, midD, cam=cam_push(1.0, 1.06, 540, 1100, 3.2), light=MORNING, sun=MORNING_SUN, fx=[Leaves(20, 715)])
    # E: Babak's hand goes to his sword; his eyes count them (35.8-38.6)
    def bannerbg(seed, n=7):
        def mk():
            im = aub.copy()
            r = random.Random(seed)
            body = ""
            for k in range(n):
                x = r.uniform(40, 1040); y = r.uniform(820, 1000)
                body += pole_flag(r.uniform(0, 3), x, y, h=300, w=120, fh=70, col="#121216", d=r.choice([-1, 1]))
                body += f'<path d="M {x + 30:.0f} {y + 40:.0f} L {x + 34:.0f} {y - 120:.0f}" stroke="#2a2a30" stroke-width="5"/>'
            im.alpha_composite(svg_render(body).filter(ImageFilter.GaussianBlur(5)))
            return im
        return bgs.cached(f"p07_bannerbg_{seed}", mk)
    bb = bannerbg(731)
    def midE(t):
        g = ease((t - 0.3) / 0.6)
        look = math.sin(t * 2.4) if t > 0.9 else 0.0
        q = P(turn=0.1 + 0.25 * look, gx=0.8 * look, gy=-0.1, furrow=0.9, brow=-0.2, armR=SWORD_GRIP if g > 0.5 else ("ik", lerp(-40, -168, g), lerp(560, 388, g)),
              armL="forward", legs="none", wind=0.5, blink=blink_at(t, 728))
        hs = 1.0 / RS
        x, y = 540 - hs * 10, 700 - hs * (-404 - 330 * RS)
        return ride7(BABAK_GUEST, q, t, x, y, hs, "#6a3a1e", gait="stand", blanket="#8e1c1c") + f'<g transform="{rider_tf(x, y, hs)}">{hip_sword(grip=g > 0.5)}</g>'
    E = Shot(2.8, bb, midE, cam=cam_push(1.0, 1.05, 540, 820, 2.8), light=MORNING, sun=MORNING_SUN)
    # F: from both sides of the valley, the caliph's horsemen close in (38.6-41.6)
    def midF(t):
        o = DUSTDEF + ridge_riders(t + 3.2, descend=ease(t / 3.0))
        for k in range(4):
            r = random.Random(770 + k)
            xl = -90 - 170 * k + 190 * t; xr = 1170 + 170 * k - 190 * t
            o += dust(xl - 60, 1430, 70, 0.5, 780 + k) + dust(xr + 60, 1430, 70, 0.5, 790 + k)
            o += enemy_rider(t, r, xl, 1420 + 10 * (k % 2), 0.4, 771 + k, d=1, banner=k in (0, 2))
            o += enemy_rider(t, random.Random(800 + k), xr, 1420 + 10 * (k % 2), 0.4, 801 + k, d=-1, banner=k in (1, 3))
        o += stopped(t, 0.3)
        return o
    F = Shot(3.0, au, midF, cam=cam_push(1.04, 1.08, 540, 1150, 3.0), light=MORNING, sun=MORNING_SUN)
    # G: Babak turns to Sahl: "You sold me, Sahl. You sold your own guest." (41.6-46.2)
    LG = [("p7s3c", 0.6), ("p7s3d", 2.4)]
    def midG(t):
        turn = ease((t - 0.1) / 0.6)
        q = talk_pose(LG, t, 729, dict(turn=lerp(-0.1, 0.32, turn), gx=lerp(-0.5, 0.75, turn), gy=0.0, furrow=0.8, brow=-0.15, sad=0.2,
                                       armR=SWORD_GRIP, armL="relaxed", wind=0.5))
        return at_neck(BABAK_GUEST, P(**q), t, 540, 1075, 1.2) + f'<g transform="translate(540,1075) scale(1.2)">{hip_sword(grip=True)}</g>'
    G = Shot(4.6, bb, midG, cam=cam_push(1.0, 1.05, 540, 860, 4.6), light=MORNING, sun=MORNING_SUN)
    # H: Sahl, cold: "The caliph pays better than you, Babak." (46.2-50.2)
    bb2 = bannerbg(732)
    LH = [("p7s3e", 0.4)]
    def midH(t):
        q = talk_pose(LH, t, 730, dict(turn=-0.3, gx=-0.7, gy=0.05, furrow=0.7, brow=-0.3, smile=0.0, armL="relaxed", armR="relaxed", wind=0.4))
        q["blink"] = max(q["blink"], 0.15)
        return at_neck(SAHL, P(**q), t, 540, 1075, 1.15)
    H = Shot(4.0, bb2, midH, cam=cam_push(1.0, 1.05, 540, 860, 4.0), light=MORNING, sun=MORNING_SUN)
    # I: surrounded; Babak lets go of his sword (50.2-53.6)
    def midI(t):
        o = ""
        close = ease(t / 3.0)
        for k, (x0, d) in enumerate([(-10, 1), (1090, -1)]):          # the caliph's men step in from both sides, pikes up
            x = x0 + d * 70 * close
            S = enemy_spec(random.Random(820 + k))
            g = P(turn=0.35 * d, gx=0.7 * d, gy=0.0, furrow=0.8, armL=("ik", 250, 560), propL="pike", armR="relaxed", wind=0.5, blink=blink_at(t, 821 + k))
            o += at_neck(S, g, t, x, 860, 1.3, flip=d < 0)
        let = ease((t - 0.8) / 0.7)
        q = P(turn=-0.05, gx=0.2 * (1 - let), gy=0.3 * let, furrow=0.6, sad=0.3 * let, armR=("ik", lerp(-168, -60, let), lerp(388, 560, let)) if let < 1 else "relaxed",
              armL="relaxed", wind=0.5, blink=blink_at(t, 731))
        q["legs"] = "none"
        hs = 0.95 / RS
        x, y = 540 - hs * 10, 820 - hs * (-404 - 330 * RS)
        return ride7(BABAK_GUEST, q, t, x, y, hs, "#6a3a1e", gait="stand", blanket="#8e1c1c") + f'<g transform="{rider_tf(x, y, hs)}">{hip_sword(grip=let < 0.5)}</g>' + o
    I = Shot(3.4, bb, midI, cam=cam_push(1.0, 1.05, 540, 950, 3.4), light=MORNING, sun=MORNING_SUN, fade_out=0.8)
    return [A, B, C, D, E, F, G, H, I]


# ================================================================ S4 the winter road; Samarra (53.6-84.2)
def captive_q(t, seed, look=0.4, sad=0.0, head_down=0.0):
    return P(turn=look, gx=look * 1.6, gy=0.2 + 0.6 * head_down, furrow=0.5, sad=sad, nod=10 * head_down, chains=True, armL=("ik", 50, 330), armR=("ik", -50, 330),
             legs="none", wind=0.6, blink=blink_at(t, seed))


def s4():
    wr = bgs.cached("winter_road", bgs.winter_road)
    # A: the column on the winter road; Babak and Abdullah in chains (53.6-58.8)
    def column(t, speed=26.0):
        o = ""
        order = [("afshin", 860), ("banner", 660), ("babak", 460), ("abdullah", 260), ("guard", 60)]
        for k, (who, x0) in enumerate(order):
            x = x0 + speed * t; y = 1082 + 6 * (k % 2)
            if who == "afshin":
                q = P(turn=0.45, gx=0.8, furrow=0.3, armR="forward", armL="forward", legs="none", wind=0.6, blink=blink_at(t, 741))
                o += ride7(AFSHIN, q, t, x, y, 0.38, "#6a6a72", k=k, mane="#2a2a30", blanket="#2e4a4a")
            elif who == "babak":
                o += ride7(BABAK_CHAINED, captive_q(t, 742), t, x, y, 0.38, "#5a3a22", k=k, blanket="#4a3a2a")
            elif who == "abdullah":
                o += ride7(ABDULLAH_CHAINED, captive_q(t, 743, look=0.3, head_down=0.6), t, x, y, 0.38, "#3a2a1e", k=k)
            else:
                o += enemy_rider(t, random.Random(744 + k), x, y, 0.38, 744 + k, d=1, gait="walk", banner=who == "banner")
        return o
    A = Shot(5.2, wr, column, cam=cam_push(1.12, 1.18, 520, 960, 5.2), light=SNOWL, grade="night", fade_in=0.6,
             fx=[Snow(420, 741, -60, (90, 200), (1.2, 3.6), (120, 220))])
    # B: closer: Babak, calm, in chains; Abdullah behind him with his head down (58.8-61.8)
    wrb = blur_bg("winter_road", bgs.winter_road, 8)
    def midB(t):
        o = ride7(ABDULLAH_CHAINED, captive_q(t, 745, look=0.3, sad=0.4, head_down=0.8), t, 160 + 20 * t, 1380, 0.78, "#3a2a1e", k=2.0)
        q = captive_q(t, 746, look=0.15)
        q["furrow"] = 0.3; q["gy"] = 0.0
        o += ride7(BABAK_CHAINED, q, t, 640 + 20 * t, 1500, 1.08, "#5a3a22", k=0.0, blanket="#4a3a2a")
        return o
    B = Shot(3.0, wrb, midB, cam=cam_push(1.0, 1.04, 560, 1000, 3.0), light=SNOWL, grade="night",
             fx=[Snow(300, 742, -60, (120, 260), (1.6, 4.4), (140, 230))], fade_out=0.4)
    # C: Samarra: the crowd in the street, the column comes in (61.8-66.8)
    base = bgs.cached("samarra_wide", bgs.samarra_wide)
    row1 = bgs.cached("s1_row1", lambda: crowd_row(11, 15, 1236, 0.2))
    row2 = bgs.cached("s1_row2", lambda: crowd_row(12, 12, 1282, 0.24))
    cheer = bgs.cached("p07_cheer2", lambda: crowd_row(751, 13, 1300, 0.23, arms=("raise", "down")))
    fg = bgs.cached("s1_fg", lambda: back_heads(3, 7, 1720, 0.62, blur=4))
    def bgC(t):
        im = base.copy()
        im.alpha_composite(row1, (0, int(2 * math.sin(t * 2.1))))
        im.alpha_composite(row2, (0, int(2 * math.sin(t * 2.3 + 1))))
        im.alpha_composite(cheer, (0, int(6 * abs(math.sin(t * 3.0)))))
        return im
    def midC(t):
        o = ""
        order = [("afshin", 800), ("babak", 330), ("abdullah", -140)]
        for k, (who, x0) in enumerate(order):
            x = x0 + 70 * t; y = 1450 + 10 * (k % 2)
            if who == "afshin":
                q = P(turn=0.3, gx=0.5, smile=0.4, furrow=0.0, armR="forward", armL="wave" if 0.6 < t < 2.4 else "forward", legs="none", wind=0.4, blink=blink_at(t, 751))
                o += ride7(AFSHIN, q, t, x, y, 0.7, "#6a6a72", k=k, mane="#2a2a30", blanket="#2e4a4a")
            elif who == "babak":
                o += ride7(BABAK_CHAINED, captive_q(t, 752, look=0.2), t, x, y, 0.7, "#5a3a22", k=k, blanket="#4a3a2a")
            else:
                o += ride7(ABDULLAH_CHAINED, captive_q(t, 753, look=0.3, head_down=0.5), t, x, y, 0.7, "#3a2a1e", k=k)
        return o
    C = Shot(5.0, bgC, midC, fg=fg, cam=cam_push(1.0, 1.05, 560, 1150, 5.0), light=SAMARRA, sun=(300, 1040, 700, (0.12, 0.07, 0.02)),
             fx=[Motes(50, 755, (255, 220, 170), (0, 500, W, 1500), (-10, -4))], fade_in=0.4)
    # D: the caliph's son rides out to meet Afshin; the officials bow (66.8-70.6)
    closeb = bgs.cached("samarra_close", bgs.samarra_close)
    crowd_blur = bgs.cached("s1_crowdblur", lambda: crowd_row(21, 9, 1500, 0.5, kinds=("man", "woman", "man")).filter(ImageFilter.GaussianBlur(7)))
    bgD = closeb.copy(); bgD.alpha_composite(crowd_blur, (0, -150))
    def midD(t):
        o = ""
        for k, x in enumerate((120, 980)):
            g = P(turn=0.0, gx=0.0, furrow=0.3, armL=("ik", 250, 560), propL="banner_black", armR="relaxed", blink=blink_at(t, 761 + k))
            o += at_feet(GUARD, g, t + k, x, 1420, 0.36)
        pq = P(turn=-0.35, gx=-0.7, gy=0.0, smile=0.6, brow=0.3, armL="relaxed", armR="wave" if 0.6 < t < 2.6 else "offer", legs="none", wind=0.3,
               blink=blink_at(t, 763))
        o += ride7(PRINCE, pq, t, 780, 1480, 0.95, "#f0ece4", gait="stand", mane="#c8c0b0", blanket="#121216", flip=True)
        for k, (S, x, s) in enumerate([(OFFICIAL, 250, 0.44), (OFFICIAL2, 410, 0.46)]):
            bow = ease((t - 0.5 - 0.3 * k) / 0.6) * (1 - ease((t - 2.8) / 0.6))
            oq = P(turn=-0.3, gx=-0.6, gy=0.6 * bow, nod=22 * bow, furrow=0.1, smile=0.3, armL="chest", armR="chest", blink=blink_at(t, 764 + k))
            o += at_feet(S, oq, t, x, 1660 + 20 * k, s)
        return o
    D = Shot(3.8, bgD, midD, cam=cam_push(1.0, 1.04, 560, 950, 3.8), light=SAMARRA, sun=SAMARRA_SUN)
    # E: Afshin, beside his prisoner: "You fought well, Babak. But I waited better." (70.6-76.0)
    sc = blur_bg("samarra_close", bgs.samarra_close, 6)
    scc = sc.copy(); scc.alpha_composite(crowd_blur, (0, -150))
    LE = [("p7s4b", 0.4), ("p7s4c", 2.9)]
    def midE(t):
        q = talk_pose(LE, t, 771, dict(turn=-0.3, gx=-0.7, gy=0.0, smile=0.35, brow=0.2, furrow=0.0, armL="relaxed", armR="relaxed", wind=0.3))
        return at_neck(AFSHIN, P(**q), t, 540, 1075, 1.15)
    E = Shot(5.4, scc, midE, cam=cam_push(1.0, 1.05, 540, 860, 5.4), light=SAMARRA, sun=SAMARRA_SUN)
    # F: Babak: "You serve the caliph, Afshin. One day you will see how he pays." (76.0-81.6)
    LF = [("p7s4d", 0.4), ("p7s4e", 2.6)]
    def midF(t):
        q = talk_pose(LF, t, 772, dict(turn=0.3, gx=0.7, gy=0.0, furrow=0.6, brow=0.0, sad=0.1, chains=True, armL=("ik", 50, 330), armR=("ik", -50, 330), wind=0.3))
        return at_neck(BABAK_CHAINED, P(**q), t, 540, 1075, 1.2)
    F = Shot(5.6, scc, midF, cam=cam_push(1.0, 1.05, 540, 860, 5.6), light=SAMARRA, sun=SAMARRA_SUN)
    # G: Afshin's smile fades; he looks up at the caliph's palace (81.6-84.2)
    def midG(t):
        fade_ = ease((t - 0.3) / 0.8)
        q = talk_pose([], t, 773, dict(turn=-0.3 + 0.35 * fade_, gx=-0.7 + 1.0 * fade_, gy=-0.4 * fade_, smile=0.35 * (1 - fade_), furrow=0.5 * fade_, brow=0.2,
                                       armL="relaxed", armR="relaxed", wind=0.3))
        return at_neck(AFSHIN, P(**q), t, 540, 1075, 1.15)
    G = Shot(2.6, scc, midG, cam=cam_push(1.05, 1.1, 540, 860, 2.6), light=SAMARRA, sun=SAMARRA_SUN, fade_out=0.8)
    return [A, B, C, D, E, F, G]


# ================================================================ S5 three days later: the robe, the elephant, the gates (84.2-112.2)
def babak_in_howdah(t, x, y, s, kneel=0.0, walk=False, look=0.0, seated=True):
    """the elephant (facing left) with Babak in the howdah on its back (seated=False: the howdah is still empty)"""
    c = Ctx(lw_for(s))
    D = kneel_drop(kneel)
    q = P(chains=True, armL="chest", armR="chest", turn=-0.25 + look, gx=-0.6 + 1.2 * look, gy=-0.1, blink=max(0.2, blink_at(t, 781)), furrow=0.2,
          wind=0.3, legs="none", breathe=math.sin(t * 1.6))
    return (f'<g transform="translate({x:.1f},{y:.1f}) scale({s:.4f})">{elephant(c, phase=t * 2.4 if walk else 0.0, t=t, kneel=kneel)}'
            f'<g transform="translate(0,{D:.1f})">{at_neck(BABAK_CAPTIVE, q, t, 50, -912, 0.28, lws=0.17 * s / 0.6) if seated else ""}{howdah(-80, -806, 260, 112)}</g></g>')


def gate_doors(op):
    """the two doors of the palace gate (palace_court), swinging open (op 0..1)"""
    arch = "M 80 1080 L 80 520 Q 80 360, 275 320 Q 470 360, 470 520 L 470 1080 Z"
    o = f'<defs><clipPath id="gd7"><path d="{arch}"/></clipPath></defs><g clip-path="url(#gd7)">'
    w = 195 * (1 - 0.86 * op)
    for side, x0 in ((-1, 80), (1, 470)):
        x1 = x0 - side * w
        xa, xb = min(x0, x1), max(x0, x1)
        o += f'<rect x="{xa:.1f}" y="300" width="{xb - xa:.1f}" height="780" fill="#4a2e1a" stroke="#1a0e06" stroke-width="5"/>'
        for k in range(1, 5):
            xx = lerp(x0, x1, k / 5)
            o += f'<path d="M {xx:.1f} 300 L {xx:.1f} 1080" stroke="#2e1c10" stroke-width="4"/>'
        for yy in (480, 720, 960):
            o += f'<path d="M {xa:.1f} {yy} L {xb:.1f} {yy}" stroke="#2a2a30" stroke-width="12"/>'
            o += "".join(f'<circle cx="{lerp(xa, xb, (j + 0.5) / 4):.1f}" cy="{yy}" r="6" fill="#8a8e96"/>' for j in range(4))
        o += f'<rect x="{xa:.1f}" y="300" width="{xb - xa:.1f}" height="780" fill="#000" opacity="{0.35 * op:.2f}"/>'
    return o + '</g>'


def s5():
    hall = blur_bg("gold_hall", bgs.gold_hall, 8)
    # A: "Three days later." Palace servants dress Babak in a rich silk robe (84.2-88.8)
    BX, BY, BSC = 540, 1700, 0.68
    def midA(t):
        o = ""
        q = P(turn=0.0, gx=0.0, gy=0.1, furrow=0.4, chains=True, armL="chest", armR="chest", wind=0.1, blink=blink_at(t, 782))
        o += at_feet(BABAK_CAPTIVE, q, t, BX, BY, BSC)
        for k, (S, x, side) in enumerate([(PALACE_SERVANT, 250, -1), (PALACE_SERVANT2, 830, 1)]):
            u = 0.5 + 0.5 * math.sin(t * 1.6 + k * 1.7)
            sx, sy = feet_xy(BX, BY, BSC, side * 165, lerp(170, 330, u))
            bx, by = to_body(x, 1730, 0.62, sx, sy)
            sq = P(turn=-0.3 * side, gx=-0.6 * side, gy=0.3, furrow=0.2, armL=("ik", bx, by) if side < 0 else "relaxed",
                   armR=("ik", bx, by) if side > 0 else "relaxed", blink=blink_at(t, 783 + k))
            o += at_feet(S, sq, t, x, 1730, 0.62)
        return o
    A = Shot(4.6, hall, midA, cam=cam_push(1.0, 1.05, 540, 950, 4.6), light=HALL, sun=(540, 700, 900, (0.08, 0.06, 0.02)), fade_in=0.6,
             fx=[Motes(40, 784, (255, 230, 180), (100, 300, 980, 1500), (3, -5), amax=80)])
    # B: the palace court: the elephant kneels; a guard leads Babak out (88.8-93.2)
    court = bgs.cached("palace_court", bgs.palace_court)
    LB = [("p7s5b", 0.6)]
    def guards(t):
        o = ""
        for k, (x, y, s) in enumerate([(560, 1110, 0.3), (700, 1110, 0.3)]):
            g = P(turn=0.0, gx=0.2 * (-1) ** k, furrow=0.4, armL=("ik", 250, 560), propL="pike", armR="relaxed", blink=blink_at(t, 785 + k))
            o += at_feet(GUARD, g, t + k, x, y, s)
        return o
    def midB(t):
        o = guards(t) + babak_in_howdah(t, 430, 1160, 0.7, kneel=1.0, seated=False)
        u = ease(t / 2.2)
        gq = talk_pose(LB, t, 786, dict(turn=0.3 if t > 0.5 else -0.3, gx=0.7 if t > 0.5 else -0.6, furrow=0.5, legs="walk" if u < 1 else "stand", phase=t * 5.5,
                                        armL="relaxed", armR="point" if 1.0 < t < 2.6 else "relaxed"))
        o += at_feet(GUARD, P(**gq), t, lerp(1010, 840, u), 1230, 0.44)
        bq = P(turn=-0.3, gx=-0.7, gy=-0.2, furrow=0.3, chains=True, armL="chest", armR="chest", legs="walk" if u < 1 else "stand", phase=t * 5.5 + 1,
               blink=blink_at(t, 787))
        o += at_feet(BABAK_CAPTIVE, bq, t, lerp(1140, 980, u), 1215, 0.43)
        return o
    B = Shot(4.4, court, midB, cam=cam_push(1.0, 1.04, 560, 1000, 4.4), light=COURT, sun=COURT_SUN)
    # C: Babak: "Good. Let them see." (93.2-96.4)
    cb = blur_bg("palace_court", bgs.palace_court, 8)
    LC = [("p7s5c", 0.4)]
    def midC(t):
        q = talk_pose(LC, t, 788, dict(turn=-0.15, gx=-0.4, gy=0.0, furrow=0.5, smile=0.25 * ease((t - 0.3) / 0.4) * (1 - ease((t - 1.6) / 0.5)), brow=0.1,
                                       chains=True, armL="chest", armR="chest", wind=0.2))
        return at_neck(BABAK_CAPTIVE, P(**q), t, 540, 1075, 1.2)
    C = Shot(3.2, cb, midC, cam=cam_push(1.0, 1.05, 540, 860, 3.2), light=COURT, sun=COURT_SUN)
    # D: Babak in the howdah; the elephant rises (96.4-102.0)
    cb3 = blur_bg("palace_court", bgs.palace_court, 3)
    def midD(t):
        k = 1.0 - ease((t - 0.8) / 3.0)
        return babak_in_howdah(t, 560, 1500, 0.95, kneel=k, look=0.15 * ease((t - 3.8) / 0.8))
    D = Shot(5.6, cb3, midD, cam=lambda t: (lerp(1.0, 1.06, ease(t / 5.6)), 540, 1000, 0.0, lerp(60, -20, ease((t - 0.8) / 3.4))), light=COURT, sun=COURT_SUN)
    # E: the gates open onto the roaring crowd; the elephant walks towards them (102.0-112.2; end card from 107.6)
    flood = glow_img(420, (255, 236, 200), 0.75)
    def midE(t):
        op = ease((t - 0.6) / 1.6)
        walk = t > 2.4
        x = 760 - 32 * max(0.0, t - 2.4)
        return gate_doors(op) + guards(t) + babak_in_howdah(t, x, 1170, 0.62, kneel=0.0, walk=walk, look=0.0)
    def light_fx(im, t):
        op = ease((t - 0.6) / 1.6)
        if op > 0:
            g = flood.copy(); g.putalpha(g.getchannel("A").point(lambda v: int(v * op)))
            im.alpha_composite(g, (275 - 420, 760 - 420))
    E = Shot(10.2, court, midE, cam=cam_push(1.0, 1.06, 480, 900, 10.2), light=COURT, sun=COURT_SUN, fx=[light_fx], fade_out=0.6)
    return [A, B, C, D, E]


SCENES = {"s1": s1, "s2": s2, "s3": s3, "s4": s4, "s5": s5}
