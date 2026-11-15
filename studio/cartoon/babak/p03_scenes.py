"""Part 3 · Twenty Years of Fire (episode 2, half 1) — 2D cartoon. Timing matches p03_audio.py:
s1 0-13 the pass (hook) · s2 13-17.6 title · s3 17.6-57 the village, 816 · s4 57-93.6 the generals, 819-824 · s5 93.6-121 Hashtadsar, 829."""
import math, random
from PIL import Image, ImageFilter, ImageDraw
from film import Shot, W, H, ease, lerp, talk_pose, blink_at, cam_push, cam_static, Snow, Motes, Embers, svg_render
from chars import pose, horse, Ctx, FEET, fmt, smooth_path
from stage import at_neck, at_feet, lying_at, crowd_row, back_heads, rider, Glow, lw_for, random_spec
import bgs
from cast import *
from p01_scenes import P, blur_bg, WARM
from p02_scenes import banner_svg, birds, red_crowd

NOON = dict(rim=(5, -3), rim_col=(1.0, 0.86, 0.62), ramp=(0, W, 0.9, 1.05))
NOON_SUN = (900, 420, 800, (0.10, 0.07, 0.03))
GREY = dict(rim=(4, -2), rim_col=(0.9, 0.9, 0.95), rim_str=0.5, ambient=(0.96, 0.96, 1.0), ramp=(0, W, 0.92, 1.03))


def enemy_spec(r):
    """one of the caliph's soldiers: black clothes, black turban or a plain steel helmet"""
    S = dict(GUARD)
    S["beard"] = r.choice(["full", "short", "father", "light", "full"])
    S["skin"] = r.choice(["olive", "tan", "light"])
    if r.random() < 0.35:
        S["head"] = "helmet"; S["helm"] = STEEL; S["plume"] = None
    S["col"] = r.choice(["#2a2a31", "#24242a", "#303038"])
    return S


def column(t, y, s, n, seed, speed=48.0, banners=(), x0=-150, x1=1230, face=1, ph0=0.0):
    """a row of marching soldiers with spears (and black banners), moving right; wraps off-screen"""
    r = random.Random(seed); out = ""
    span = x1 - x0; gap = span / n
    specs = [(enemy_spec(r), r.uniform(-0.25, 0.25) * gap, r.uniform(0, 6.3)) for _ in range(n)]
    for k, (S, jit, ph) in enumerate(specs):
        x = x0 + (k * gap + jit + speed * t) % span
        q = P(legs="walk", phase=t * 6.5 + ph + ph0, turn=0.42 * face, gx=0.7 * face, gy=0.1, furrow=0.5, wind=0.3,
              armL=("ik", 250, 560), propL="banner_black" if k in banners else "pike", armR="relaxed")
        out += at_feet(S, q, t + ph, x, y + 4 * math.sin(k * 1.3), s * r.uniform(0.95, 1.05))
    return out


def red_cloth(t, x, y, L=90, h=26, col="#c4161c", speed=9.0, amp=10):
    """a strip of red cloth tied at (x, y), blowing to the right"""
    n = 8; top, bot = [], []
    for i in range(n + 1):
        u = i / n; wv = amp * u * math.sin(t * speed - u * 5)
        top.append((x + L * u, y + wv)); bot.append((x + L * u * 0.95, y + h + wv * 1.1 - 4 * u))
    return '<path d="M ' + " L ".join(f"{a:.1f} {b:.1f}" for a, b in top + bot[::-1]) + f' Z" fill="{col}" stroke="#2a0606" stroke-width="2.5"/>'


# ================================================================ S1 the pass, June 829 (0-13)
def s1():
    floor = bgs.cached("gorge_floor_noon", lambda: bgs.gorge_floor("noon"))
    walls = bgs.cached("gorge_walls_noon", lambda: bgs.gorge_walls("noon"))
    def midA(t):
        return column(t, 1300, 0.235, 9, 11, banners=(2, 6), ph0=0.0) + column(t, 1430, 0.30, 7, 12, banners=(3,), ph0=1.0, speed=56)
    A = Shot(4.6, floor, midA, fg=walls, cam=cam_push(1.0, 1.07, 540, 1250, 4.6), light=NOON, sun=NOON_SUN, fade_in=0.6,
             fx=[Motes(50, 3, (255, 236, 200), (100, 500, 980, 1500), (14, -3), amax=90)])

    fb = blur_bg("gorge_floor_noon", lambda: bgs.gorge_floor("noon"), 8)
    LB = [("p3s1a", 0.5)]
    def midB(t):
        up = ease((t - 0.3) / 0.5)
        q = talk_pose(LB, t, 81, dict(turn=0.25 - 0.1 * up, gx=0.6 - 0.5 * up, gy=-1.0 * up, brow=0.2 + 0.8 * up, furrow=0.2 - 0.7 * up,
                                      nod=-12 * up, tilt=-3 * up, armL="relaxed", armR="relaxed", wind=0.3))
        bob = 6 * abs(math.sin(t * 3.2))
        back = ""
        for k in range(3):   # soldiers passing behind him
            x = (k * 420 + 130 * t) % 1300 - 160
            back += at_feet(enemy_spec(random.Random(40 + k)), P(legs="walk", phase=t * 6.5 + k, turn=0.42, gx=0.7, armL=("ik", 250, 560), propL="pike"),
                            t, x, 1460, 0.46)
        return back + at_neck(YOUNG_SOLDIER, P(**q), t, 520, 1090 + bob, 1.25)
    B = Shot(3.8, fb, midB, cam=cam_push(1.0, 1.04, 520, 900, 3.8), light=NOON, sun=NOON_SUN, mid_blur=0.0)

    cu = bgs.cached("cliff_up", bgs.cliff_up)
    def midC(t):
        o = ""
        vis = ease((t - 0.2) / 0.12) * (1 - ease((t - 1.1) / 0.2))
        if vis > 0.02:
            x = 600 + 50 * ease((t - 0.2) / 1.0)
            o += f'<g opacity="{vis:.2f}">' + red_cloth(t, x, 548, 130, 36, amp=14) + '</g>'
        o += bgs.boulder(590, 590, 56, 63, "#6a4c36", "#3a2818", "#c89a6a")   # the rock it slips behind
        return o
    C = Shot(1.8, cu, midC, cam=cam_push(1.0, 1.18, 640, 600, 1.8), light=dict(rim=(0, 0)), sun=(560, 300, 700, (0.14, 0.12, 0.08)))

    LD = [("p3s1b", 0.2)]
    def midD(t):
        q = talk_pose(LD, t, 82, dict(turn=-0.3, gx=-0.7, gy=0.1, furrow=0.9, brow=-0.2, armL="relaxed", armR="relaxed", wind=0.3))
        bob = 5 * abs(math.sin(t * 3.0))
        return at_neck(OFFICER, P(**q), t, 600, 1080 + bob, 1.15)
    D = Shot(2.8, fb, midD, cam=cam_push(1.02, 1.06, 600, 900, 2.8), light=NOON, sun=NOON_SUN, fade_out=0.5)
    return [A, B, C, D]


# ================================================================ S2 title: red cloth on the ridge (13-17.6)
def s2():
    rv = bgs.cached("ridge_view", bgs.ridge_view)
    def mid(t):
        o = '<path d="M 250 1720 L 268 980" stroke="#3a2414" stroke-width="16" stroke-linecap="round"/><path d="M 268 980 L 280 930 L 256 930 Z" fill="#cfd4da" stroke="#1b0f0a" stroke-width="3"/>'
        o += red_cloth(t, 266, 1000, 300, 70, speed=7.0, amp=34)
        o += bgs.boulder(200, 1640, 150, 91, "#8a6040", "#4a3020", "#d8a878") + bgs.boulder(860, 1700, 190, 92, "#7a5434", "#40281a", "#c89868")
        return o
    return [Shot(4.6, rv, mid, cam=cam_push(1.0, 1.05, 400, 1100, 4.6), light=dict(rim=(5, -2), rim_col=(1.0, 0.8, 0.5)), sun=(880, 760, 700, (0.14, 0.08, 0.03)),
                 fx=[Embers(60, 4, (0, 900, 1080, 1900), (60, 160)), Motes(40, 5, (255, 220, 170), (0, 300, W, 1500), (30, -6))], bloom=0.7, grade="fire",
                 fade_in=0.3, fade_out=0.5)]



# ================================================================ S3 the village, 816 (17.6-57.0)
def villager_spec(r, red=False):
    S = random_spec(r, ("man", "man", "old", "man"))
    if red:
        S["col"] = r.choice(["#8a2a1e", "#7a2418", "#9a3424", "#6a1a14"])
    return S


def mule(c, t, x, y, s, flip=False, walk=False, phase=0.0, col="#6a5646"):
    sx = -s if flip else s
    return f'<g transform="translate({x:.1f},{y:.1f}) scale({sx:.4f},{s:.4f})">{horse(c, col=col, mane="#2a2018", t=t, saddle=False, packs="#b89664", mule=True, walk=walk, phase=phase, head_down=0.1)}</g>'


MUD = (330, 1690, 300, 70)    # the puddle in village_square (cx, cy, rx, ry)


def mud_front(cx=330, cy=1690, rx=300, ry=70, splash=0.0):
    """the front lip of the puddle, drawn over feet that stand in it"""
    o = (f'<path d="M {cx - rx:.0f} {cy:.0f} C {cx - rx * 0.8:.0f} {cy + ry * 1.0:.0f}, {cx + rx * 0.8:.0f} {cy + ry * 1.0:.0f}, {cx + rx:.0f} {cy:.0f} '
         f'C {cx + rx * 0.7:.0f} {cy + ry * 0.35:.0f}, {cx - rx * 0.7:.0f} {cy + ry * 0.35:.0f}, {cx - rx:.0f} {cy:.0f} Z" fill="#4a3624"/>'
         f'<path d="M {cx - rx * 0.7:.0f} {cy + ry * 0.35:.0f} C {cx - rx * 0.3:.0f} {cy + ry * 0.5:.0f}, {cx + rx * 0.3:.0f} {cy + ry * 0.5:.0f}, {cx + rx * 0.7:.0f} {cy + ry * 0.35:.0f}" '
         f'stroke="#6a5038" stroke-width="5" fill="none"/>')
    if splash > 0:
        r = random.Random(5)
        for k in range(14):
            a = r.uniform(-2.8, -0.3); v = r.uniform(120, 260)
            px = cx + 40 + math.cos(a) * v * splash; py = cy - 10 + math.sin(a) * v * splash + 300 * splash * splash
            o += f'<ellipse cx="{px:.1f}" cy="{py:.1f}" rx="{r.uniform(5, 10):.1f}" ry="{r.uniform(4, 8):.1f}" fill="#4a3624" opacity="{max(0, 1 - splash):.2f}"/>'
    return o


def s3():
    vs = bgs.cached("village_square", bgs.village_square)
    left = bgs.cached("s3_left", lambda: crowd_row(31, 6, 1395, 0.27, -40, 330, kinds=("man", "woman", "man", "boy"), turn_to=0.3))
    right = bgs.cached("s3_right", lambda: crowd_row(32, 6, 1385, 0.26, 700, 1120, kinds=("man", "woman", "old", "man"), turn_to=-0.3))
    def vbg(t):
        im = vs.copy(); im.alpha_composite(left, (0, int(2 * math.sin(t * 2)))); im.alpha_composite(right, (0, int(2 * math.sin(t * 2 + 1)))); return im
    LIGHT = dict(rim=(4, -3), rim_col=(0.95, 0.9, 0.8), rim_str=0.6, ambient=(0.97, 0.97, 1.0), ramp=(0, W, 0.92, 1.03))
    # A: the tax collector's men load the village's grain on the mules
    def midA(t):
        c = Ctx(lw_for(0.42)); o = ""
        c = Ctx(lw_for(1.0))
        o += mule(c, t, 170, 1470, 1.0)
        lift = 0.5 + 0.5 * math.sin(t * 1.6)
        g2 = P(turn=-0.3, gx=-0.6, gy=-0.3, furrow=0.6, armL=("ik", 120, lerp(60, -160, lift)), armR=("ik", -120, lerp(60, -160, lift)))
        o += at_feet(GUARD, g2, t, 470, 1490, 0.34)
        sx, sy = 470, 1490 - (1290 - lerp(60, -160, lift)) * 0.34 - 20
        o += f'<g transform="translate({sx:.1f},{sy:.1f}) scale(0.34)"><path d="M -110 -60 C -150 -10, -120 70, -40 80 C 40 90, 120 60, 120 -10 C 120 -70, 60 -100, -10 -100 C -60 -100, -90 -90, -110 -60 Z" fill="#b89664" stroke="#1b0f0a" stroke-width="5"/></g>'
        u = (t * 0.16) % 1.0
        g1 = P(legs="walk", phase=t * 6, turn=-0.35, gx=-0.7, armL=("ik", 150, -50), propL="sack", armR="relaxed", furrow=0.3)
        o += at_feet(dict(GUARD, beard="short"), g1, t, lerp(1000, 700, u), lerp(1470, 1500, u), 0.38)
        f = P(turn=0.2, gx=-0.6, gy=0.1, sad=0.35, brow=0.4, furrow=-0.3, armL="chest", armR="chest")
        o += at_feet(FARMER, f, t, 610, 1650, 0.45)
        tq = talk_pose([], t, 83, dict(turn=-0.35, gx=-0.7, gy=0.1, smile=0.2, armL="chest", propL="scroll", armR="point", furrow=0.2))
        o += at_feet(TAX_COLLECTOR, P(**tq), t, 900, 1680, 0.47)
        return o
    A = Shot(7.8, vbg, midA, cam=cam_push(1.0, 1.06, 560, 1300, 7.8), light=LIGHT, sun=(900, 300, 800, (0.06, 0.05, 0.04)), fade_in=0.6,
             fx=[Motes(30, 31, (255, 245, 230), (0, 600, W, 1500), (8, -2), amax=70)])
    vb = blur_bg("village_square", bgs.village_square, 8)
    LB = [("p3s3b", 0.4)]
    def midB(t):
        q = talk_pose(LB, t, 84, dict(turn=-0.3, gx=-0.7, gy=0.0, smile=0.25, brow=-0.1, furrow=0.3, armL="chest", propL="scroll",
                                      armR=("ik", -700, -40) if t > 1.2 else "relaxed"))
        return at_neck(TAX_COLLECTOR, P(**q), t, 620, 990, 1.0)
    B = Shot(3.6, vb, midB, cam=cam_push(1.0, 1.04, 600, 900, 3.6), light=LIGHT, sun=(900, 300, 800, (0.06, 0.05, 0.04)))
    # C1: the farmer holds on to his sack; the guard pushes him into the mud
    def farmer_fall(t, x0=440):
        if t < 1.0:
            sway = 6 * math.sin(t * 9)
            f = P(turn=0.3, gx=0.7, brow=0.7, furrow=-0.6, sad=0.2, armL=("ik", 150 + sway, 300), armR=("ik", 30 + sway, 320), propL="sack", mouth_o=0.3)
            return at_feet(FARMER, f, t, x0, 1650, 0.62)
        if t < 1.6:
            u = ease((t - 1.0) / 0.6)
            f = P(turn=0.3, gx=0.7, gy=-0.6, brow=1.0, furrow=-0.8, armL=("ik", 260, 20), armR=("ik", -260, 20), mouth_o=0.6)
            return f'<g transform="rotate({-55 * u:.1f},{x0:.0f},{1650 + 40 * u:.0f})">' + at_feet(FARMER, f, t, x0 - 40 * u, 1650 + 60 * u, 0.62) + '</g>'
        f = P(turn=0.2, gx=0.6, gy=-0.3, brow=0.8, furrow=-0.7, sad=0.5, legs="sit", armL=("ik", 250, 330), armR=("ik", -250, 330))
        return at_neck(FARMER, f, t, x0 - 70, 1700 - 575 * 0.62, 0.62)
    def midC1(t):
        o = farmer_fall(t)
        push = ease((t - 0.85) / 0.2) * (1 - ease((t - 1.4) / 0.6))
        g = P(turn=-0.35, gx=-0.8, furrow=1.0, brow=-0.3, armR=("ik", -250 - 160 * push, 260 - 40 * push), armL=("ik", 120, 300) if t > 1.1 else ("ik", 200, 300),
              propL="sack" if t > 1.1 else None, mouth_o=0.3 * push)
        o += at_feet(GUARD, g, t, 760, 1650, 0.62)
        o += mud_front(330, 1690, 300, 70, splash=ease((t - 1.55) / 0.7) if t > 1.55 else 0.0)
        return o
    C1 = Shot(3.0, vs, midC1, cam=cam_push(1.06, 1.12, 500, 1350, 3.0), light=LIGHT, sun=(900, 300, 800, (0.06, 0.05, 0.04)))
    # C2: Babak walks in and pulls him up
    def midC2(t):
        o = ""
        rise = ease((t - 2.5) / 0.7)
        bx = lerp(1180, 650, ease(t / 1.6)); walking = t < 1.6
        reach = ease((t - 1.5) / 0.5) * (1 - ease((t - 3.4) / 0.5)); grab = ease((t - 1.8) / 0.4)
        lean = -11 * ease((t - 1.5) / 0.5) * (1 - rise)                  # Babak bends toward him
        M = (lerp(445, 490, rise), lerp(1250, 1120, rise))            # where the two hands meet (screen)
        a = math.radians(-lean); dx, dy = M[0] - bx, M[1] - 1690           # undo the lean to get the IK target
        Mu = (bx + dx * math.cos(a) - dy * math.sin(a), 1690 + dx * math.sin(a) + dy * math.cos(a))
        bl = ((Mu[0] - bx) / 0.64, (Mu[1] - 1690) / 0.64 + FEET)
        b = P(legs="walk" if walking else "stand", phase=t * 6, turn=-0.4, gx=-0.8, gy=0.6 - 0.5 * rise, furrow=0.5, smile=0.3 * rise, wind=0.4,
              armR=("ik", lerp(-200, bl[0], reach), lerp(560, bl[1], reach)) if t > 1.4 else "relaxed", armL="relaxed")
        if rise <= 0.0:
            fl = ((M[0] - 300) / 0.62, (M[1] - 1343) / 0.62)
            f = P(turn=0.3, gx=0.7, gy=-0.7 * reach, brow=0.6, sad=0.4, legs="sit", armL=("ik", lerp(250, fl[0], grab), lerp(330, fl[1], grab)), armR=("ik", -250, 330))
            o += at_neck(FARMER, f, t, 300, 1343, 0.62)
        else:
            fy = lerp(1748, 1690, rise)
            fl = ((M[0] - 300) / 0.62, (M[1] - fy) / 0.62 + FEET)
            f = P(turn=0.35, gx=0.8, gy=-0.3, brow=0.5, sad=0.4 * (1 - rise), smile=0.25 * rise, armL=("ik", fl[0], fl[1]) if t < 3.5 else "relaxed", armR="relaxed")
            o += at_feet(FARMER, f, t, 300, fy, 0.62)
        o += f'<g transform="rotate({lean:.2f},{bx:.1f},1690)">' + at_feet(BABAK_816, b, t, bx, 1690, 0.64) + '</g>'
        o += mud_front(330, 1690, 300, 70)
        return o
    C2 = Shot(4.2, vs, midC2, cam=cam_push(1.12, 1.08, 470, 1350, 4.2), light=LIGHT, sun=(900, 300, 800, (0.06, 0.05, 0.04)))
    # D: "These mountains are ours. The land belongs to the people who work it."
    heads = bgs.cached("s3_heads", lambda: back_heads(33, 7, 1760, 0.6, col="#2a1e18", blur=4))
    LD = [("p3s3c", 0.5), ("p3s3d", 2.6)]
    def midD(t):
        turn = ease((t - 2.2) / 0.6)
        q = talk_pose(LD, t, 85, dict(turn=-0.35 + 0.5 * turn, gx=-0.8 + 1.0 * turn, gy=0.0, furrow=0.6 - 0.3 * turn, brow=0.1, wind=0.4,
                                      armL=("ik", 260, 120) if 2.9 < t < 5.6 else "relaxed", armR="relaxed"))
        return at_neck(BABAK_816, P(**q), t, 560, 1030, 1.12)
    D = Shot(6.4, vb, midD, fg=heads, cam=cam_push(1.0, 1.06, 560, 900, 6.4), light=LIGHT, sun=(900, 300, 800, (0.06, 0.05, 0.04)))
    # E: the farmer, muddy: "And who will protect us from them?"
    LE = [("p3s3e", 0.3)]
    def midE(t):
        q = talk_pose(LE, t, 86, dict(turn=0.3, gx=0.7, gy=-0.2, brow=0.7, furrow=-0.5, sad=0.4, armL="relaxed", armR="relaxed"))
        mud = "".join(f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="#4a3624" opacity="0.75"/>' for x, y, rx, ry in [(-60, -128, 14, 9), (70, -150, 10, 7), (40, -60, 12, 8), (-90, 60, 22, 14), (120, 200, 26, 16)])
        body = at_neck(FARMER, P(**q), t, 520, 1060, 1.3)
        return body + f'<g transform="translate(520,1060) scale(1.3)">{mud}</g>'
    E = Shot(3.4, vb, midE, cam=cam_push(1.0, 1.04, 520, 900, 3.4), light=LIGHT, sun=(900, 300, 800, (0.06, 0.05, 0.04)))
    # F: Babak: "We will. Together."
    LF = [("p3s3f", 0.4)]
    def midF(t):
        q = talk_pose(LF, t, 87, dict(turn=-0.2, gx=-0.5, gy=0.1, furrow=0.5, smile=0.45 * ease((t - 2.1) / 0.8), brow=0.1, wind=0.4,
                                      armL="relaxed", armR="relaxed"))
        return at_neck(BABAK_816, P(**q), t, 540, 1050, 1.38)
    F = Shot(4.0, vb, midF, cam=cam_push(1.0, 1.05, 540, 880, 4.0), light=LIGHT, sun=(900, 300, 800, (0.06, 0.05, 0.04)))
    # G: red cloth on every spear; the caliph's men leave with nothing
    r = random.Random(34)
    vill = [(villager_spec(r), x, y, sc, r.uniform(0, 1.2)) for x, y, sc in [(130, 1700, 0.5), (300, 1640, 0.46), (800, 1650, 0.47), (960, 1710, 0.5), (210, 1560, 0.4), (880, 1560, 0.4)]]
    def midG(t):
        c = Ctx(lw_for(0.3)); o = ""
        u = ease(t / 6.0)
        o += mule(c, t, lerp(330, -200, u), 1440, 0.3, flip=True, walk=True, phase=t * 4)
        tq = P(legs="walk", phase=t * 6, turn=-0.4, gx=-0.8, furrow=0.6, armL="relaxed", armR="relaxed")
        o += at_feet(TAX_COLLECTOR, tq, t, lerp(520, -120, u), 1450, 0.3)
        o += at_feet(GUARD, P(legs="walk", phase=t * 6 + 1, turn=-0.4, gx=-0.8, armL="relaxed", armR="relaxed"), t, lerp(640, 0, u), 1440, 0.29)
        b = P(turn=0.0, gx=0.0, gy=0.1, furrow=0.6, smile=0.3, wind=0.6, armL="fist_up" if t > 1.4 else "relaxed", armR="relaxed")
        o += at_feet(BABAK_816, b, t, 545, 1600, 0.47)
        for k, (S, x, y, sc, d) in enumerate(sorted(vill, key=lambda v: v[2])):
            up = ease((t - 0.5 - d) / 0.7)
            q = P(turn=0.3 if x < 540 else -0.3, gx=0.5 if x < 540 else -0.5, gy=-0.2, smile=0.4 * up, brow=0.4, mouth_o=0.35 * up * (0.6 + 0.4 * math.sin(t * 6 + k)),
                  armL=("ik", lerp(300, 330, up), lerp(560, -470, up)), propL="spear_red", armR="relaxed", wind=0.5)
            o += at_feet(S, q, t + k, x, y, sc)
        return o
    G = Shot(7.0, vbg, midG, cam=cam_push(1.0, 1.07, 545, 1250, 7.0), light=LIGHT, sun=(900, 300, 800, (0.06, 0.05, 0.04)), fade_out=0.6,
             fx=[Motes(40, 35, (255, 245, 230), (0, 500, W, 1500), (10, -4), amax=80)])
    return [A, B, C1, C2, D, E, F, G]



# ================================================================ S4 the caliph's generals, 819-824 (57.0-93.6)
def pole_flag(t, x, y, h=260, w=120, fh=70, col="#121216", d=1):
    """a banner pole (top at x, y) with its flag trailing behind the direction of motion d"""
    n = 8; top, bot = [], []
    for i in range(n + 1):
        u = i / n; wv = (4 + 14 * u) * math.sin(t * 6 - u * 6)
        top.append((x - d * w * u, y + 6 + wv)); bot.append((x - d * w * u * 0.96, y + 6 + fh + wv * 1.1 + 6 * u))
    return (f'<path d="M {x:.1f} {y:.1f} L {x:.1f} {y + h:.1f}" stroke="#3a2414" stroke-width="5"/>'
            '<path d="M ' + " L ".join(f"{a:.1f} {b:.1f}" for a, b in top + bot[::-1]) + f' Z" fill="{col}" stroke="#0a0606" stroke-width="2"/>')


def sil(x, y, s, t, ph=0.0, col="#16141a", run=0.0, d=1, spear=True):
    """a tiny far-away soldier (feet at x, y; ~150*s px tall)"""
    k = math.sin(t * (8 + 6 * run) + ph)
    lx = 10 * k * s * (1 + run)
    o = (f'<path d="M {x - 8*s:.1f} {y - 70*s:.1f} L {x - 6*s - lx:.1f} {y:.1f} M {x + 8*s:.1f} {y - 70*s:.1f} L {x + 6*s + lx:.1f} {y:.1f}" stroke="{col}" stroke-width="{7*s:.1f}" stroke-linecap="round"/>'
         f'<path d="M {x - 22*s:.1f} {y - 66*s:.1f} L {x - 16*s:.1f} {y - 128*s:.1f} L {x + 16*s:.1f} {y - 128*s:.1f} L {x + 22*s:.1f} {y - 66*s:.1f} Z" fill="{col}"/>'
         f'<circle cx="{x:.1f}" cy="{y - 144*s:.1f}" r="{16*s:.1f}" fill="{col}"/>')
    if spear:
        o += f'<path d="M {x + 24*s*d:.1f} {y - 30*s:.1f} L {x + (30 + 30*run)*s*d:.1f} {y - 230*s:.1f}" stroke="{col}" stroke-width="{3.2*s:.1f}"/>'
    return o


def dust(x, y, r, a, seed=0):
    rr = random.Random(seed); o = ""
    for k in range(7):
        o += f'<circle cx="{x + rr.uniform(-1, 1) * r * 0.7:.1f}" cy="{y + rr.uniform(-0.5, 0.3) * r:.1f}" r="{r * rr.uniform(0.4, 0.75):.1f}" fill="#c8b090" opacity="{a * rr.uniform(0.4, 0.7):.2f}"/>'
    return f'<g filter="url(#dustblur)">{o}</g>'


DUSTDEF = '<defs><filter id="dustblur" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="9"/></filter></defs>'


def s4():
    # A: 819, deep snow: the caliph's cavalry cannot get through and turns back
    sp = bgs.cached("snow_pass", bgs.snow_pass); sfg = bgs.cached("snow_fg", bgs.snow_fg)
    r = random.Random(41)
    riders = [(enemy_spec(r), 640 - 330 * k, 1500 + 22 * (k % 2), 0.62 - 0.04 * k, ["#2a2a2e", "#3a2a1e", "#1e1a18", "#4a3a2a"][k], 2.5 + 0.45 * k) for k in range(4)]
    def midA(t):
        o = ""
        for k, (S, x0, y, sc, col, T) in enumerate(reversed(riders)):
            back = t > T
            x = x0 + 24 * min(t, T) - 34 * max(0.0, t - T)
            q = P(turn=-0.45 if back else 0.45, gx=0.8, gy=0.1, furrow=0.9, armR="forward", armL="forward", wind=1.0, legs="none")
            o += rider(S, q, t, lambda c, col=col, k=k: horse(c, col=col, walk=True, phase=t * 2.6 + k, t=t + k, head_down=0.55), x, y, sc, flip=back)
            if k == 1:
                d = -1 if back else 1
                o += pole_flag(t, x + 14 * sc * d, y - 900 * sc, 360 * sc / 0.4, 150, 90, d=d)
        return o
    A = Shot(6.0, sp, midA, fg=sfg, cam=cam_push(1.04, 1.12, 540, 1250, 6.0), light=GREY, grade="night", fade_in=0.4,
             fx=[Snow(700, 41, 260, (220, 480), (1.4, 4.6))])
    # B: Babak draws the mountain paths in the dirt
    cr = bgs.cached("camp_rocks", bgs.camp_rocks)
    def tip_path(u):
        return (lerp(470, 700, u), 1700 + 22 * math.sin(u * 9.0))
    LB = [("p3s4a", 0.5)]
    def midB(t):
        o = ""
        u = min(1.0, max(0.0, (t - 0.3) / 3.6))
        tip = tip_path(u)
        hand_s = (tip[0] - 150, 1300 + 10 * math.sin(t * 2))
        hl = ((hand_s[0] - 330) / 0.5, (hand_s[1] - 1640) / 0.5 + FEET)
        q = talk_pose(LB, t, 88, dict(turn=0.3, gx=0.6, gy=0.8, nod=6, furrow=0.6, wind=0.4, armL=("ik", hl[0], hl[1]), armR="relaxed"))
        # the lines already drawn
        pts = [tip_path(k / 40 * u) for k in range(41)]
        o += '<ellipse cx="590" cy="1712" rx="230" ry="62" fill="#6a4e34" opacity="0.25"/>'
        o += ('<path d="M 440 1700 l 40 -40 l 40 40 M 560 1676 l 50 -46 l 50 46 M 700 1702 l 40 -38 l 40 38 M 500 1748 l 34 -30 l 34 30" stroke="#3a2416" stroke-width="7" fill="none" stroke-linejoin="round" opacity="0.9"/>')
        o += '<path d="M ' + " L ".join(f"{a:.1f} {b:.1f}" for a, b in pts) + '" stroke="#2a180e" stroke-width="7" fill="none" stroke-dasharray="16 9" opacity="0.9"/>'
        o += at_feet(BABAK, P(**q), t, 330, 1640, 0.5)
        o += f'<path d="M {hand_s[0]:.1f} {hand_s[1]:.1f} L {tip[0]:.1f} {tip[1]:.1f}" stroke="#5a3a1c" stroke-width="7" stroke-linecap="round"/>'
        for k, (S, x, y, sc, fl) in enumerate([(COMMANDER, 770, 1630, 0.48, False), (FIGHTER2, 940, 1660, 0.5, False)]):
            c = talk_pose([], t, 89 + k, dict(turn=-0.35, gx=-0.6, gy=0.8, nod=5, furrow=0.4, armL="relaxed", armR="chest" if k == 0 else "relaxed"))
            o += at_feet(S, P(**c), t, x, y, sc)
        return o
    B = Shot(4.2, cr, midB, cam=cam_push(1.0, 1.05, 560, 1300, 4.2), light=NOON, sun=NOON_SUN)
    # B2: the map, from above
    md = bgs.cached("map_dirt", bgs.map_dirt)
    route = [(160, 1500), (260, 1380), (380, 1330), (470, 1200), (540, 1060), (610, 940), (720, 860), (860, 780), (960, 640)]
    def along(u):
        seg = [math.dist(route[i], route[i + 1]) for i in range(len(route) - 1)]
        s_ = u * sum(seg)
        for i, l in enumerate(seg):
            if s_ <= l:
                f = s_ / l; return lerp(route[i][0], route[i + 1][0], f), lerp(route[i][1], route[i + 1][1], f)
            s_ -= l
        return route[-1]
    def midB2(t):
        o = ""
        for x, y, sz in [(330, 1150, 120), (700, 1120, 140), (420, 860, 110), (800, 1000, 100), (250, 1640, 90), (880, 1450, 120), (560, 1520, 80)]:
            o += f'<path d="M {x - sz} {y + sz * 0.5} L {x} {y - sz * 0.6} L {x + sz} {y + sz * 0.5}" stroke="#4a3220" stroke-width="9" fill="none" stroke-linejoin="round" opacity="0.85"/>'
            o += f'<path d="M {x - sz*0.45} {y - sz*0.05} L {x} {y - sz * 0.6} L {x + sz*0.2} {y - sz*0.32}" stroke="#e8d0a8" stroke-width="5" fill="none" opacity="0.6"/>'
        u = min(1.0, max(0.0, (t - 0.2) / 2.6))
        pts = [along(k / 60 * u) for k in range(61)]
        o += '<path d="M ' + " L ".join(f"{a:.1f} {b:.1f}" for a, b in pts) + '" stroke="#3a2416" stroke-width="10" fill="none" stroke-dasharray="26 14" stroke-linecap="round"/>'
        ar = ease((t - 2.4) / 0.6)
        if ar > 0:   # the narrow place between two mountains: here
            o += f'<circle cx="540" cy="1000" r="{70 * ar:.1f}" stroke="#7a1a12" stroke-width="9" fill="none" opacity="{ar:.2f}"/>'
        tip = pts[-1]
        o += f'<path d="M {tip[0] + 420:.1f} {tip[1] - 760:.1f} L {tip[0]:.1f} {tip[1]:.1f}" stroke="#5a3a1c" stroke-width="22" stroke-linecap="round"/><path d="M {tip[0] + 420:.1f} {tip[1] - 760:.1f} L {tip[0]:.1f} {tip[1]:.1f}" stroke="#1b0f0a" stroke-width="3" fill="none"/>'
        return o
    B2 = Shot(3.4, md, midB2, cam=cam_push(1.0, 1.08, 560, 1100, 3.4), light=dict(rim=(0, 0), ramp=(0, W, 0.9, 1.05)), sun=(800, 600, 900, (0.08, 0.06, 0.03)))
    # C: 821, a gorge: the rocks come down on Isa's army
    gd = bgs.cached("gorge_down", bgs.gorge_down)
    rr = random.Random(43)
    men = [(rr.uniform(-60, 1140), rr.uniform(960, 1180), rr.uniform(0.5, 0.7), rr.uniform(0, 6.3), rr.choice([-1, 1])) for _ in range(26)]
    rocks = [(rr.uniform(150, 950), 0.35 + 0.55 * k, rr.uniform(45, 85), rr.uniform(-1, 1)) for k in range(7)]
    def rock_pos(x0, t0, rad, drift, t):
        a = t - t0
        if a < 0:
            return None
        y = -120 + 900 * a + 500 * a * a
        land = 1000 + (x0 % 140)
        if y > land:
            ta = (-900 + math.sqrt(900 ** 2 + 4 * 500 * (land + 120))) / 1000
            return x0 + drift * 160 * ta + drift * 90 * (a - ta), land, (a - ta)
        return x0 + drift * 160 * a, y, -1
    def midC(t):
        o = DUSTDEF
        panic = ease((t - 0.9) / 0.5)
        for x, y, sc, ph, d in sorted(men, key=lambda m: m[1]):
            run = panic
            xx = x + 30 * t * (1 - panic) + d * 160 * max(0.0, t - 0.9) * panic
            o += sil(xx % 1200 - 60 if panic < 0.5 else xx, y, sc, t, ph, run=run, d=d if panic > 0.5 else 1)
        for k, x in enumerate((120, 520, 900)):
            o += pole_flag(t, x + 30 * min(t, 0.9), 860 + 40 * k % 3, 150, 70, 40)
        for k, (x0, t0, rad, drift) in enumerate(rocks):
            pp = rock_pos(x0, t0, rad, drift, t)
            if pp:
                x, y, since = pp
                if since >= 0:
                    o += dust(x, y, rad * (1.4 + 2.2 * min(1.5, since)), max(0.0, 0.9 - 0.25 * since), seed=k)
                o += bgs.boulder(x, y - rad * 0.4, rad, 200 + k, "#8a6a4a", "#4a3424", "#c8a07a", rot=t * 240 * (1 if drift > 0 else -1))
        return o
    shake = lambda t: (1.0 + 0.04 * ease(t / 5.4), 540, 1000, 6 * math.sin(t * 37) * ease((t - 0.6) / 0.3), 5 * math.sin(t * 29) * ease((t - 0.6) / 0.3))
    C = Shot(5.4, gd, midC, cam=shake, light=dict(rim=(0, -2), rim_col=(1.0, 0.85, 0.6), rim_str=0.4), sun=(800, 200, 900, (0.10, 0.07, 0.03)),
             fx=[Motes(80, 44, (220, 200, 170), (0, 700, W, 1400), (20, -30), (2, 5), 120)])
    # D: the commander reports
    crb = blur_bg("camp_rocks", bgs.camp_rocks, 8)
    LD = [("p3s4c", 0.3), ("p3s4d", 3.3)]
    def midD(t):
        q = talk_pose(LD, t, 91, dict(turn=0.25, gx=0.5, gy=0.0, smile=0.45, brow=0.3, furrow=0.0, armL="relaxed", armR="relaxed"))
        return at_neck(COMMANDER, P(**q), t, 520, 1060, 1.3)
    D = Shot(5.4, crb, midD, cam=cam_push(1.0, 1.05, 520, 900, 5.4), light=NOON, sun=NOON_SUN)
    # E1: 824, Bazz: Ahmad ibn al-Junayd is led in, in ropes
    cy = bgs.cached("courtyard", bgs.courtyard)
    left = bgs.cached("s4_left", lambda: red_crowd(45, 8, 1450, 0.34, -40, 300, 0.4))
    right = bgs.cached("s4_right", lambda: red_crowd(46, 8, 1450, 0.34, 780, 1120, -0.4))
    def cbg(t):
        im = cy.copy(); im.alpha_composite(left, (0, int(2 * math.sin(t * 2)))); im.alpha_composite(right, (0, int(2 * math.sin(t * 2 + 1)))); return im
    COURT = dict(rim=(4, -4), rim_col=(1.0, 0.85, 0.6), ramp=(0, W, 0.9, 1.05))
    def midE1(t):
        u = ease(t / 3.6)
        ax, ay, asc = 620, lerp(1330, 1500, u), lerp(0.36, 0.44, u)
        fx, fy, fsc = 380, lerp(1390, 1560, u), lerp(0.38, 0.46, u)
        fq = P(legs="walk", phase=t * 5.5, turn=0.3, gx=0.9, gy=-0.1, furrow=0.4, armL=("ik", 420, 520), armR="relaxed")
        hand = (fx + 446 * fsc, fy - (FEET - 534) * fsc)                 # the fighter's hand holding the rope (screen)
        lead = ((hand[0] - ax) / asc, (hand[1] - ay) / asc + FEET)
        aq = P(legs="walk", phase=t * 5.5 + 1.5, turn=-0.2, gx=0.3, gy=-0.3, furrow=0.6, brow=-0.2, armL="chest", armR="chest", chains="rope", lead=lead)
        return at_feet(AHMAD, aq, t, ax, ay, asc) + at_feet(FIGHTER, fq, t, fx, fy, fsc)
    E1 = Shot(3.6, cbg, midE1, cam=cam_push(1.0, 1.06, 540, 1200, 3.6), light=COURT, sun=(900, 300, 900, (0.08, 0.06, 0.03)), fade_in=0.3)
    cyb = blur_bg("courtyard", bgs.courtyard, 9)
    LE = [("p3s4e", 0.6)]
    def midE2(t):
        q = talk_pose(LE, t, 92, dict(turn=-0.15, gx=-0.4, gy=-0.1, furrow=0.7, brow=-0.3, smile=0.15, nod=-4, armL="chest", armR="chest", chains="rope"))
        return at_neck(AHMAD, P(**q), t, 540, 1040, 1.25)
    E2 = Shot(3.6, cyb, midE2, cam=cam_push(1.0, 1.04, 540, 880, 3.6), light=COURT, sun=(900, 300, 900, (0.08, 0.06, 0.03)))
    LF = [("p3s4f", 0.4)]
    def midF(t):
        q = talk_pose(LF, t, 93, dict(turn=0.2, gx=0.4, gy=0.0, furrow=0.4, smile=0.2 + 0.4 * ease((t - 2.4) / 0.8), brow=0.1, wind=0.5, armL="relaxed", armR="relaxed"))
        return at_neck(BABAK, P(**q), t, 540, 1060, 1.3)
    F = Shot(5.0, cyb, midF, cam=cam_push(1.0, 1.06, 540, 860, 5.0), light=COURT, sun=(900, 300, 900, (0.08, 0.06, 0.03)), fade_out=0.6)
    return [A, B, B2, C, D, E1, E2, F]



# ================================================================ S5 Hashtadsar, June 829: "Now!" (93.6-121.0)
def rope_around(x, y, r, hx, hy, tight=1.0):
    """a rope tied round a boulder (centre x, y) running to a hand at (hx, hy)"""
    return (f'<ellipse cx="{x:.1f}" cy="{y - r * 0.05:.1f}" rx="{r * 1.08:.1f}" ry="{r * 0.28:.1f}" fill="none" stroke="#8a6a3a" stroke-width="{max(5, r * 0.07):.1f}" transform="rotate(-12,{x:.1f},{y:.1f})"/>'
            f'<path d="M {x + r * 0.7:.1f} {y - r * 0.3:.1f} Q {(x + hx) / 2:.1f} {min(y, hy) - 20 * tight + 30 * (1 - tight):.1f} {hx:.1f} {hy:.1f}" stroke="#8a6a3a" stroke-width="{max(5, r * 0.06):.1f}" fill="none"/>')


def s5():
    floor = bgs.cached("gorge_floor_noon", lambda: bgs.gorge_floor("noon"))
    walls = bgs.cached("gorge_walls_noon", lambda: bgs.gorge_walls("noon"))
    def midA(t):
        o = column(t, 1290, 0.22, 9, 51, banners=(1, 5), ph0=0.3) + column(t, 1400, 0.27, 7, 52, banners=(4,), ph0=1.2, speed=52)
        c = Ctx(lw_for(0.6))
        q = P(turn=0.45, gx=0.8, gy=0.0, furrow=0.6, smile=0.2, armR="forward", armL="forward", wind=0.8, legs="none")
        x = lerp(330, 560, ease(t / 3.0))
        o += rider(MUHAMMAD, q, t, lambda c: horse(c, col="#1e1a1c", mane="#0a0808", walk=True, phase=t * 4.0, t=t, blanket="#121216"), x, 1560, 0.62)
        return o
    A = Shot(3.0, floor, midA, fg=walls, cam=cam_push(1.0, 1.05, 540, 1250, 3.0), light=NOON, sun=NOON_SUN, fade_in=0.5,
             fx=[Motes(50, 53, (255, 236, 200), (100, 500, 980, 1500), (14, -3), amax=90)])
    # B: Muhammad ibn Humayd rides at the head of his army
    fbl = bgs.cached("gorge_floor_noon_wide_b8", lambda: bgs.cached("gorge_floor_noon", lambda: bgs.gorge_floor("noon")).resize((1166, 2074)).filter(ImageFilter.GaussianBlur(8)))
    def bgB(t):
        x0 = int(30 + 7 * t); return fbl.crop((x0, 77, x0 + W, 77 + H))
    LB = [("p3s5a", 0.6), ("p3s5b", 2.8)]
    def midB(t):
        fwd = ease((t - 4.0) / 0.35)
        q = talk_pose(LB, t, 94, dict(turn=0.3, gx=0.5, gy=0.0, furrow=0.7, smile=0.35 * (1 - fwd), brow=-0.1, wind=0.7,
                                      armL=("ik", 300, -520) if fwd > 0.5 else "relaxed", propL=("sword", 180) if fwd > 0.5 else None, armR="relaxed"))
        bob = 9 * abs(math.sin(t * 3.4))
        o = ""
        for k in range(3):     # spears and a banner going past behind him
            x = (k * 470 + 90 * t) % 1400 - 200
            o += f'<path d="M {x:.0f} 1900 L {x + 20:.0f} 560" stroke="#3a2414" stroke-width="8"/><path d="M {x + 20:.0f} 540 l 12 30 l -24 0 Z" fill="#cfd4da"/>'
        o += pole_flag(t, (260 + 90 * t) % 1400 - 200, 420, 1500, 220, 140)
        return o + at_neck(MUHAMMAD, P(**q), t, 560, 1060 + bob, 1.12)
    B = Shot(6.8, bgB, midB, cam=cam_push(1.0, 1.04, 560, 880, 6.8), light=NOON, sun=NOON_SUN)
    # C: on the ridge: Babak flat among the rocks, his men at the ropes
    rv = bgs.cached("ridge_view", bgs.ridge_view)
    ledge = bgs.cached("ledge_fg", bgs.ledge_fg)
    def ridge_people(t, whisper=None):
        o = ""
        hands = [(700, 1090), (930, 1100)]
        for k, (S, x, y, sc) in enumerate([(FIGHTER, 760, 1010, 0.5), (FIGHTER2, 960, 1030, 0.46)]):
            hx, hy = hands[k]
            hl = ((hx - x) / sc, (hy - y) / sc)
            q = talk_pose([], t, 95 + k, dict(turn=-0.4, gx=-0.9, gy=0.1, furrow=0.6, armR="forward", armL="forward", wind=0.5))
            o += at_neck(S, P(**q), t, x, y, sc)
        for k, (bx, by, br) in enumerate([(610, 1040, 92), (880, 1060, 80)]):
            o += bgs.boulder(bx, by, br, 130 + k, "#7a5a40", "#3a2818", "#c89a6a")
            o += rope_around(bx, by, br, *hands[k])
        q = talk_pose(whisper or [], t, 97, dict(turn=0.15, gx=0.3, gy=0.75, nod=8, furrow=0.9, brow=-0.2, wind=0.6, armL="relaxed", armR="relaxed"))
        o += at_neck(BABAK, P(**q), t, 300, 1075, 0.72)
        return o
    LC = [("p3s5c", 1.0)]
    C = Shot(4.8, rv, lambda t: ridge_people(t, LC), fg=ledge, cam=cam_push(1.0, 1.05, 520, 1000, 4.8), light=dict(rim=(5, -2), rim_col=(1.0, 0.82, 0.55)),
             sun=(880, 760, 700, (0.12, 0.07, 0.03)), fx=[Motes(40, 54, (255, 226, 180), (0, 300, W, 1100), (24, -4))])
    # D: what Babak sees: the army deep in the pass
    gd = bgs.cached("gorge_down", bgs.gorge_down)
    rr = random.Random(55)
    men = [(rr.uniform(-60, 1140), rr.uniform(950, 1190), rr.uniform(0.5, 0.72), rr.uniform(0, 6.3)) for _ in range(34)]
    def marching(t, panic_at=None):
        o = DUSTDEF
        for x, y, sc, ph in sorted(men, key=lambda m: m[1]):
            if panic_at is not None and t > panic_at:
                d = 1 if x > 540 else -1
                xx = x + 40 * panic_at + d * 170 * (t - panic_at)
                o += sil(xx, y, sc, t, ph, run=1.0, d=d)
            else:
                o += sil((x + 40 * t) % 1200 - 60, y, sc, t, ph)
        for k, x in enumerate((100, 420, 760)):
            xx = (x + 40 * t) % 1200 - 60
            o += pole_flag(t, xx, 850 + 30 * k, 160, 70, 42)
        return o
    rim_dark = '<path d="M -40 1920 L -40 1640 C 200 1600, 420 1660, 600 1620 C 780 1585, 940 1640, 1120 1610 L 1120 1920 Z" fill="#20140c"/>'
    D = Shot(3.0, gd, lambda t: marching(t) + rim_dark, cam=cam_push(1.0, 1.08, 560, 1080, 3.0), light=dict(rim=(0, 0)), sun=(800, 200, 900, (0.08, 0.06, 0.02)))
    # E: "Now!"
    rvb = blur_bg("ridge_view", bgs.ridge_view, 8)
    LE = [("p3s5d", 1.4)]
    def midE(t):
        up = ease((t - 1.25) / 0.3)
        q = talk_pose(LE, t, 98, dict(turn=0.1, gx=0.2, gy=0.5 - 0.6 * up, nod=6 - 8 * up, furrow=1.0, brow=-0.3 + 0.4 * up, wind=0.7,
                                      armL=("ik", lerp(200, 330, up), lerp(500, -540, up)) if up > 0 else "relaxed", armR="relaxed"))
        q["mouth_o"] = max(q["mouth_o"], 0.0)
        return at_neck(BABAK, P(**q), t, 520, 1080, 1.3)
    E = Shot(2.8, rvb, midE, fg=ledge, cam=cam_push(1.0, 1.06, 520, 900, 2.8), light=dict(rim=(5, -2), rim_col=(1.0, 0.82, 0.55)), sun=(880, 760, 700, (0.12, 0.07, 0.03)))
    # F: a blade cuts the rope; the rock tips over the edge
    def ledge_low():
        im = bgs.cached("ridge_view_b8", lambda: bgs.cached("ridge_view", bgs.ridge_view).filter(ImageFilter.GaussianBlur(8))).copy()
        im.alpha_composite(bgs.cached("ledge_fg", bgs.ledge_fg), (0, 180)); return im
    rvl = bgs.cached("ridge_ledge_low", ledge_low)
    def midF(t):
        o = ""
        tip = ease((t - 1.15) / 1.3)
        bx, by, br = 540 + 40 * tip, 1010 + 1100 * tip * tip, 240
        cut = t > 0.95
        if not cut:
            o += f'<path d="M {bx - 120:.0f} {by - 210:.0f} Q 300 700 -60 640" stroke="#8a6a3a" stroke-width="18" fill="none"/>'
        else:
            k = ease((t - 0.95) / 0.3)
            o += f'<path d="M -60 640 Q 120 {700 + 200 * k:.0f} {240 - 120 * k:.0f} {760 + 300 * k:.0f}" stroke="#8a6a3a" stroke-width="18" fill="none"/>'
        o += bgs.boulder(bx, by, br, 140, "#7a5a40", "#3a2818", "#c89a6a", rot=55 * tip)
        o += f'<g transform="rotate({55 * tip:.1f},{bx:.1f},{by:.1f})"><ellipse cx="{bx:.1f}" cy="{by - 30:.1f}" rx="{br * 1.08:.1f}" ry="{br * 0.26:.1f}" fill="none" stroke="#8a6a3a" stroke-width="18" transform="rotate(-12,{bx:.1f},{by:.1f})"/>'
        if not cut:
            o += f'<path d="M {bx - 120:.1f} {by - 210:.1f} L {bx - 60:.1f} {by - 60:.1f}" stroke="#8a6a3a" stroke-width="18"/>'
        o += '</g>'
        sw = ease((t - 0.55) / 0.45)
        if 0.0 < sw < 1.0 or (t > 0.55 and t < 1.4):
            a = lerp(-70, 40, sw)
            o += (f'<g transform="translate(1180,260) rotate({a:.1f})"><rect x="-14" y="-40" width="28" height="120" fill="#5a1a14" stroke="#1b0f0a" stroke-width="4"/>'
                  f'<rect x="-60" y="76" width="120" height="22" rx="8" fill="#c9a24a" stroke="#1b0f0a" stroke-width="4"/>'
                  f'<path d="M -18 98 L 18 98 L 14 820 L 0 860 L -14 820 Z" fill="#dfe3e8" stroke="#1b0f0a" stroke-width="5"/></g>')
        return o
    F = Shot(2.6, rvl, midF, cam=lambda t: (1.0 + 0.03 * ease(t / 2.6), 540, 1000, 7 * math.sin(t * 41) * ease((t - 1.6) / 0.3), 5 * math.sin(t * 33) * ease((t - 1.6) / 0.3)),
              light=dict(rim=(5, -2), rim_col=(1.0, 0.82, 0.55)), sun=(880, 760, 700, (0.12, 0.07, 0.03)))
    # G: the rocks come down into the pass (the end card comes up over it)
    rocks = [(rr.uniform(80, 1000), 0.1 + 0.3 * k, rr.uniform(60, 110), rr.uniform(-1, 1)) for k in range(9)]
    def midG(t):
        o = marching(t + 3.0, panic_at=3.6)
        for k, (x0, t0, rad, drift) in enumerate(rocks):
            a = t - t0
            if a < 0:
                continue
            y = -200 + 1000 * a + 700 * a * a
            land = 1020 + (x0 % 150)
            if y > land:
                ta = (-1000 + math.sqrt(1000 ** 2 + 4 * 700 * (land + 200))) / 1400
                since = a - ta
                o += dust(x0 + drift * 120 * ta, land, rad * (1.6 + 2.6 * min(1.5, since)), max(0.0, 0.95 - 0.2 * since), seed=k)
                x, y = x0 + drift * 120 * ta + drift * 60 * since, land
            else:
                x = x0 + drift * 120 * a
            o += bgs.boulder(x, y - rad * 0.4, rad, 210 + k, "#7a5a40", "#3a2818", "#c89a6a", rot=t * 260 * (1 if drift > 0 else -1))
        return o
    shake = lambda t: (1.02, 540, 1000, 8 * math.sin(t * 37), 6 * math.sin(t * 29))
    G = Shot(4.4, gd, midG, cam=shake, light=dict(rim=(0, -2), rim_col=(1.0, 0.85, 0.6), rim_str=0.4), sun=(800, 200, 900, (0.10, 0.07, 0.03)),
             fx=[Motes(90, 56, (220, 200, 170), (0, 600, W, 1500), (20, -40), (2, 5), 130)], fade_out=0.8)
    return [A, B, C, D, E, F, G]


SCENES = {"s1": s1, "s2": s2, "s3": s3, "s4": s4, "s5": s5}
