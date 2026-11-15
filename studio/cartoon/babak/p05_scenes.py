"""Part 5 · The Silver Trap (episode 3, half 1) — 2D cartoon. Timing matches p05_audio.py:
s1 0-21.8 Afshin buys a spy (hook) · s2 21.8-26.4 title · s3 26.4-65.6 the slow cage, 835 (forts, Barzand, trenches, drums, watch fires, Bazz) ·
s4 65.6-99.0 the silver bait: the convoy, the fire, the night attack, the trap, the ravine · s5 99.0-121.0 dawn: the face on the ridge."""
import math, random
from PIL import Image, ImageFilter, ImageDraw, ImageEnhance
from film import Shot, W, H, ease, lerp, talk_pose, blink_at, cam_push, cam_static, Snow, Motes, Embers, svg_render
from chars import pose, horse, Ctx, FEET, fmt, prop
from stage import at_neck, at_feet, crowd_row, back_heads, fire_svg, rider, Glow, lw_for, random_spec
import bgs
from cast import *
from p01_scenes import P, blur_bg, WARM
from p03_scenes import NOON, NOON_SUN, enemy_spec, column, villager_spec, pole_flag, sil, dust, DUSTDEF
from p04_scenes import chest, sweat

LAMP_R = dict(point=(840, 620, 1050, 0.5, 1.15, (1.0, 0.6, 0.3)), rim_point=(840, 5), rim_col=(1.0, 0.7, 0.4), rim_str=0.6)
CLOSE_R = dict(rim=(6, -2), rim_col=(1.0, 0.65, 0.35), ramp=(0, W, 0.74, 1.08))      # lamp on the right of the frame
CLOSE_L = dict(rim=(-6, -2), rim_col=(1.0, 0.65, 0.35), ramp=(0, W, 1.08, 0.74))     # lamp on the left
MOON = dict(ambient=(0.55, 0.62, 0.9), rim=(-4, -3), rim_col=(0.75, 0.82, 1.0), rim_str=0.6)
TORCH = dict(ambient=(0.75, 0.62, 0.62), rim=(4, -3), rim_col=(1.0, 0.6, 0.3), rim_str=0.9, ramp=(0, W, 0.9, 1.05))
DAWN = dict(ambient=(0.88, 0.84, 0.92), rim=(5, -3), rim_col=(1.0, 0.75, 0.55), rim_str=0.8, ramp=(0, W, 0.86, 1.05))
WARROOM = dict(point=(540, 520, 1150, 0.55, 1.15, (1.0, 0.6, 0.3)), rim=(0, -4), rim_col=(1.0, 0.72, 0.42), rim_str=0.7)


def jitter(t, amp=2.5, f=23.0, seed=0.0):
    return amp * math.sin(t * f + seed) * math.sin(t * f * 0.37 + 1.3 + seed)


def stone_block(x, y, w=110, h=70, seed=0, col="#9a8a76", sh="#6a5c4c", hi="#c8b8a2"):
    r = random.Random(seed); a = r.uniform(-6, 6)
    return (f'<g transform="rotate({a:.1f},{x:.1f},{y:.1f})"><rect x="{x - w / 2:.1f}" y="{y - h / 2:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{h * 0.18:.1f}" fill="{col}" stroke="#1b0f0a" stroke-width="{max(2, w * 0.035):.1f}"/>'
            f'<rect x="{x - w / 2:.1f}" y="{y + h * 0.12:.1f}" width="{w:.1f}" height="{h * 0.38:.1f}" rx="{h * 0.15:.1f}" fill="{sh}" opacity="0.6"/>'
            f'<path d="M {x - w * 0.38:.1f} {y - h * 0.3:.1f} L {x + w * 0.2:.1f} {y - h * 0.3:.1f}" stroke="{hi}" stroke-width="{max(2, w * 0.05):.1f}" stroke-linecap="round" opacity="0.8"/></g>')


def coin(x, y, r, ph=0.0, lit=1.0):
    """a silver coin seen at an angle (ph turns it)"""
    w = max(0.15, abs(math.cos(ph)))
    return (f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="{r * w:.1f}" ry="{r * 0.62:.1f}" fill="#c8ccd4" stroke="#3a3c44" stroke-width="{max(1.2, r * 0.12):.1f}"/>'
            f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="{r * w * 0.62:.1f}" ry="{r * 0.38:.1f}" fill="none" stroke="#8a8e98" stroke-width="{max(1, r * 0.08):.1f}"/>'
            f'<ellipse cx="{x - r * w * 0.3:.1f}" cy="{y - r * 0.22:.1f}" rx="{r * w * 0.22:.1f}" ry="{r * 0.12:.1f}" fill="#ffffff" opacity="{0.75 * lit:.2f}"/>')


def flame(x, y, s, t, seed=0):
    """a small torch flame, base at (x, y), ~110*s tall"""
    k = 0.85 + 0.15 * math.sin(t * 17 + seed) * math.sin(t * 7 + seed)
    tip = y - 110 * s * k; sw = 10 * s * math.sin(t * 9 + seed)
    return (f'<path d="M {x - 28 * s:.1f} {y:.1f} C {x - 34 * s:.1f} {y - 50 * s:.1f}, {x - 12 * s + sw:.1f} {tip + 40 * s:.1f}, {x + sw * 0.6:.1f} {tip:.1f} '
            f'C {x + 14 * s + sw:.1f} {tip + 40 * s:.1f}, {x + 34 * s:.1f} {y - 50 * s:.1f}, {x + 28 * s:.1f} {y:.1f} Z" fill="#ff8a1a"/>'
            f'<path d="M {x - 13 * s:.1f} {y:.1f} C {x - 16 * s:.1f} {y - 30 * s:.1f}, {x - 4 * s:.1f} {tip + 45 * s:.1f}, {x + sw * 0.3:.1f} {tip + 30 * s:.1f} '
            f'C {x + 6 * s:.1f} {tip + 45 * s:.1f}, {x + 16 * s:.1f} {y - 30 * s:.1f}, {x + 13 * s:.1f} {y:.1f} Z" fill="#ffd84a"/>')


GLOWDEF = ('<defs><radialGradient id="tglow"><stop offset="0" stop-color="#ffb060" stop-opacity="0.55"/><stop offset="0.45" stop-color="#ff8a30" stop-opacity="0.18"/>'
           '<stop offset="1" stop-color="#ff8a30" stop-opacity="0"/></radialGradient></defs>')


def glow(x, y, r, a=1.0):
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="url(#tglow)" opacity="{a:.2f}"/>'


def smoke(t, x, y, seed=0, s=1.0, n=7, col="#d8d4cc", a=0.45):
    r = random.Random(seed); o = ""
    for k in range(n):
        u = ((t * 0.12 + k / n + r.uniform(0, 0.1)) % 1.0)
        yy = y - u * 520 * s; xx = x + (40 * u + 12 * math.sin(t * 0.8 + k)) * s; rr = (24 + 70 * u) * s
        o += f'<circle cx="{xx:.1f}" cy="{yy:.1f}" r="{rr:.1f}" fill="{col}" opacity="{a * (1 - u) * min(1, u * 5):.2f}"/>'
    return f'<g filter="url(#dustblur)">{o}</g>'


def mule_chest(t, x, y, s, walk=True, phase=0.0, col="#6a5646", flip=False):
    c = Ctx(lw_for(s))
    sx = -s if flip else s
    return (f'<g transform="translate({x:.1f},{y:.1f}) scale({sx:.4f},{s:.4f})">'
            f'{horse(c, col=col, mane="#2a2018", t=t, saddle=False, packs=None, mule=True, walk=walk, phase=phase, head_down=0.1)}'
            f'<path d="M -70 -404 L 110 -404 L 104 -350 L -64 -350 Z" fill="#7a2a1a" stroke="#1b0f0a" stroke-width="4"/>'
            f'{chest(20, -396, 1.12)}</g>')


# ================================================================ S1 Afshin's tent: the spy (0-21.8)
def s1():
    tent = bgs.cached("command_tent", bgs.command_tent)
    tentb = blur_bg("command_tent", bgs.command_tent, 9)
    motes = lambda seed: Motes(40, seed, (255, 220, 170), (100, 300, 1000, 1300), (4, -5), amax=90)
    # A: the spy kneels between two guards; Afshin walks in
    def spy_kneel(t, x, floor, s, gy=0.5):
        q = P(turn=0.25, gx=0.5, gy=gy, sad=0.35, brow=0.5, furrow=-0.5, legs="sit", armL="chest", armR="chest", chains="rope",
              blink=blink_at(t, 501), breathe=math.sin(t * 4.0))
        return at_neck(SPY, q, t, x + jitter(t, 2.0), floor - 575 * s, s)
    def midA(t):
        o = ""
        for k, (x, turn) in enumerate([(230, 0.35), (660, -0.35)]):
            g = P(turn=turn, gx=turn * 2, gy=0.4, furrow=0.6, armL=("ik", 250, 560), propL="pike", armR="relaxed", blink=blink_at(t, 510 + k))
            o += at_feet(GUARD if k == 0 else dict(GUARD, beard="short", skin="tan"), g, t, x, 1380, 0.42)
        o += spy_kneel(t, 440, 1440, 0.6)
        u = ease(t / 2.4); walking = t < 2.4
        a = P(legs="walk" if walking else "stand", phase=t * 5.5, turn=-0.4, gx=-0.8, gy=0.5, furrow=0.5, armL="hip", armR="relaxed",
              blink=blink_at(t, 512), smile=0.15 * ease((t - 2.8) / 0.6))
        o += at_feet(AFSHIN, a, t, lerp(1040, 810, u), 1520, 0.52)
        return o
    A = Shot(4.2, tent, midA, cam=cam_push(1.0, 1.05, 560, 1150, 4.2), light=LAMP_R, grade="fire", fade_in=0.6, fx=[motes(511)])
    # B: Afshin, crouching: "How much does Babak pay you?"
    LB = [("p5s1a", 0.6)]
    def midB(t):
        q = talk_pose(LB, t, 513, dict(turn=-0.3, gx=-0.7, gy=0.45, furrow=0.4, brow=0.1, smile=0.1, armL="relaxed", armR="relaxed"))
        return at_neck(AFSHIN, P(**q), t, 560, 1070, 1.2)
    B = Shot(3.4, tentb, midB, cam=cam_push(1.0, 1.04, 560, 880, 3.4), light=CLOSE_R, sun=(1000, 700, 600, (0.10, 0.05, 0.02)), grade="fire")
    # C: the spy, trembling: "Enough to live."
    LC = [("p5s1b", 0.7)]
    def midC(t):
        q = talk_pose(LC, t, 514, dict(turn=0.3, gx=0.7, gy=-0.45, sad=0.55, brow=0.8, furrow=-0.7, armL="chest", armR="chest", chains="rope"))
        q["tilt"] += jitter(t, 1.5, 19.0); q["mouth_o"] *= 0.8
        x = 520 + jitter(t, 3.0, 27.0, 1.0)
        return at_neck(SPY, P(**q), t, x, 1075, 1.25) + sweat(x, 1075, 1.25, t)
    C = Shot(3.0, tentb, midC, cam=cam_push(1.0, 1.04, 520, 880, 3.0), light=CLOSE_L, sun=(80, 700, 600, (0.10, 0.05, 0.02)), grade="fire")
    # D: Afshin cuts the rope, puts a purse of silver in his hands: "I will pay you double."
    LD = [("p5s1c", 2.6)]
    SX, AX, FLOOR, S = 380, 735, 1350, 0.66
    NY = FLOOR - 575 * S
    def to_local(px, py, x):        # screen point -> arm-space point of a person drawn with at_neck at (x, NY), scale S
        return (px - x) / S, (py - NY) / S
    HANDS = (SX + 4, NY + 200 * S)    # the spy's tied hands (screen)
    RECV = (SX + 112 * S, NY + 236 * S)
    def midD(t):
        o = ""
        cut = t >= 1.0
        give = ease((t - 1.5) / 0.7); took = t >= 2.25
        lift = ease((t - 3.4) / 0.6)
        # the spy
        if not cut:
            sq = P(turn=0.3, gx=0.7, gy=0.35, sad=0.5, brow=0.7, furrow=-0.6, legs="sit", armL="chest", armR="chest", chains="rope", blink=blink_at(t, 515))
        else:
            open_ = ease((t - 1.0) / 0.4)
            hold = ease((t - 2.3) / 0.5)
            rl = to_local(lerp(lerp(HANDS[0] + 20, RECV[0], open_), RECV[0] - 34, hold), lerp(lerp(HANDS[1], RECV[1], open_), RECV[1] - 8, hold), SX)
            rr = to_local(lerp(HANDS[0] - 30, RECV[0] - 70, hold), lerp(HANDS[1] + 10, RECV[1] + 4, hold), SX)
            sq = P(turn=0.3, gx=0.7 if not took else 0.25 + 0.45 * lift, gy=0.35 if not took else 0.85 - 0.65 * lift, sad=0.5 - 0.3 * give, brow=0.7, furrow=-0.6 + 0.4 * give,
                   legs="sit", armL=("ik", rl[0], rl[1]), armR=("ik", rr[0], rr[1]), propL="purse" if took else None, blink=blink_at(t, 515))
        o += at_neck(SPY, sq, t, SX + (jitter(t, 1.5) if not took else 0), NY, S)
        if cut:                     # the two ends of the rope fall to the carpet
            u = ease((t - 1.0) / 0.45)
            for k, dx in enumerate((-26, 22)):
                x = HANDS[0] + dx + 30 * u * (1 if dx > 0 else -1); y = lerp(HANDS[1] + 10, FLOOR - 8, u)
                o += f'<path d="M {x - 22:.1f} {y:.1f} C {x - 8:.1f} {y - 14 + 10 * u:.1f}, {x + 8:.1f} {y + 12 - 6 * u:.1f}, {x + 24:.1f} {y + 2:.1f}" stroke="#8a6a3a" stroke-width="7" fill="none" stroke-linecap="round"/>'
        # Afshin
        reach = ease((t - 0.35) / 0.55) * (1 - ease((t - 1.05) / 0.35))
        if t < 1.4:
            tl = to_local(HANDS[0] + 46, HANDS[1] - 30, AX)
            arm = ("ik", lerp(-230, tl[0], reach), lerp(330, tl[1], reach), "down")
            prp = ("dagger", 50) if t < 1.25 else None
        else:
            tl = to_local(RECV[0] + 30, RECV[1] - 18, AX)
            back = ease((t - 2.3) / 0.5)
            arm = ("ik", lerp(lerp(-230, tl[0], give), -230, back), lerp(lerp(330, tl[1], give), 330, back), "down")
            prp = "purse" if not took else None
        talk = talk_pose(LD, t, 516, dict(turn=-0.35, gx=-0.7, gy=0.4 if t < 2.4 else 0.2, furrow=0.3, smile=0.2 * ease((t - 4.6) / 0.6), legs="sit",
                                         armR=arm, propR=prp, armL="relaxed"))
        o += at_neck(AFSHIN, P(**talk), t, AX, NY, S)
        return o
    D = Shot(5.6, tent, midD, cam=cam_push(1.15, 1.2, 560, 1000, 5.6), light=LAMP_R, grade="fire", fx=[motes(517)])
    # E: "From now on, you watch him."
    LE = [("p5s1d", 0.5)]
    def midE(t):
        q = talk_pose(LE, t, 518, dict(turn=-0.25, gx=-0.6, gy=0.35, furrow=0.5, brow=-0.1, smile=0.25 * ease((t - 2.6) / 0.6), armL="relaxed", armR="relaxed"))
        return at_neck(AFSHIN, P(**q), t, 560, 1070, 1.2)
    E = Shot(3.4, tentb, midE, cam=cam_push(1.0, 1.05, 560, 860, 3.4), light=CLOSE_R, sun=(1000, 700, 600, (0.10, 0.05, 0.02)), grade="fire")
    # F: the spy looks at the silver in his hand
    def midF(t):
        up = ease((t - 1.0) / 0.5)
        q = P(turn=0.25, gx=0.3 + 0.4 * up, gy=0.9 - 1.0 * up, sad=0.25, brow=0.4 + 0.2 * up, furrow=-0.2, nod=6 * ease((t - 1.6) / 0.3) + 8 * (1 - up),
              armL="relaxed", armR="relaxed", blink=blink_at(t, 519), breathe=math.sin(t * 3))
        return at_neck(SPY, q, t, 500, 1075, 1.25)
    F = Shot(2.2, tentb, midF, cam=cam_push(1.0, 1.04, 520, 860, 2.2), light=CLOSE_L, sun=(80, 700, 600, (0.10, 0.05, 0.02)), grade="fire", fade_out=0.6)
    return [A, B, C, D, E, F]


# ================================================================ S2 title: silver falling on the table (21.8-26.4)
def s2():
    base = bgs.cached("title5_table", lambda: _title_table())
    r = random.Random(520)
    drops = [(r.uniform(380, 760), r.uniform(0.0, 3.6), r.uniform(34, 44), r.uniform(0, 6.3), r.uniform(-1, 1)) for _ in range(30)]
    pile = sorted([(560 + r.gauss(0, 150), 1520 + abs(r.gauss(0, 60)), r.uniform(36, 46), r.uniform(0, 3)) for _ in range(46)], key=lambda v: v[1])
    def mid(t):
        o = ('<path d="M 230 1400 C 180 1460, 200 1540, 280 1556 C 360 1570, 420 1530, 430 1480 L 380 1420 C 330 1380, 270 1370, 230 1400 Z" fill="#7a4e26" stroke="#1b0f0a" stroke-width="5"/>'
              '<path d="M 380 1420 L 430 1480 L 470 1452 L 420 1396 Z" fill="#5a3818" stroke="#1b0f0a" stroke-width="4"/><path d="M 236 1430 C 260 1500, 330 1530, 400 1500" stroke="#e8c070" stroke-width="5" fill="none"/>')
        n = 16 + int(30 * ease(t / 4.0))
        for k, (x, y, rr, ph) in enumerate(pile):
            if k < n:
                o += coin(x, y, rr, ph * 0.3 + 1.2, 0.6 + 0.4 * math.sin(t * 3 + k))
        for x, t0, rr, ph, dr in drops:
            a = t - t0
            if a < 0 or a > 0.9:
                continue
            y = -80 + 2400 * a * a
            if y > 1520:
                continue
            o += coin(x + 30 * dr * a, y, rr, ph + a * 14)
        return o
    return [Shot(4.6, base, mid, cam=cam_push(1.0, 1.05, 540, 1300, 4.6), light=dict(rim=(0, -3), rim_col=(1.0, 0.85, 0.6)), sun=(540, 1000, 900, (0.10, 0.06, 0.02)),
                 bloom=0.9, grade="fire", fade_in=0.3, fade_out=0.5, fx=[Motes(50, 521, (255, 220, 170), (100, 300, 1000, 1500), (3, -6), amax=100)])]


def _title_table():
    im = blur_bg("command_tent", bgs.command_tent, 14).copy()
    im = ImageEnhance.Brightness(im).enhance(0.7)
    s = ('<defs><linearGradient id="tb" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#6a4022"/><stop offset="1" stop-color="#2a160a"/></linearGradient>'
         '<radialGradient id="tl" cx="540" cy="1500" r="700" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#ffb060" stop-opacity="0.35"/>'
         '<stop offset="1" stop-color="#000" stop-opacity="0"/></radialGradient></defs>'
         '<path d="M -40 1280 L 1120 1280 L 1120 1920 L -40 1920 Z" fill="url(#tb)"/>' +
         "".join(f'<path d="M -40 {1300 + k * 70} C 300 {1295 + k * 70}, 700 {1310 + k * 70}, 1120 {1302 + k * 70}" stroke="#2a1608" stroke-width="3" opacity="0.5" fill="none"/>' for k in range(9)) +
         '<path d="M -40 1280 L 1120 1280" stroke="#a87444" stroke-width="6"/><rect x="0" y="1280" width="1080" height="640" fill="url(#tl)"/>')
    im.alpha_composite(svg_render(s))
    return im


# ================================================================ S3 the slow cage, 835 (26.4-65.6)
def s3():
    # A: the old forts on the road are rebuilt
    fr = bgs.cached("fort_road", bgs.fort_road)
    r = random.Random(530)
    gap = [(490 + 52 * k, 1078 - 0 * k) for k in range(6)] + [(516 + 52 * k, 1036) for k in range(5)] + [(490 + 52 * k, 994) for k in range(6)]
    def midA(t):
        o = DUSTDEF + pole_flag(t, 230, 590, 150, 120, 70)
        n = min(len(gap), 5 + int(t / 0.32))
        for k in range(n):
            x, y = gap[k]
            drop = ease((t - (k - 5) * 0.32) / 0.25) if k >= 5 else 1.0
            o += stone_block(x + 26, y - 30 * (1 - drop), 50, 40, 600 + k)
        # the mason lifts a stone up to the wall
        lift = 0.5 + 0.5 * math.sin(t * 2.4 - 1.0)
        mq = P(turn=0.1, gx=0.2, gy=-0.6, furrow=0.6, armL=("ik", 110, lerp(140, -200, lift)), armR=("ik", -110, lerp(140, -200, lift)), blink=blink_at(t, 531))
        o += at_feet(enemy_spec(random.Random(532)), mq, t, 640, 1300, 0.3)
        o += stone_block(640, 1300 - (FEET - lerp(160, -190, lift)) * 0.3 - 6, 54, 40, 533)
        # two men carry stones up the road
        for k, (x0, x1, y, sc, ph) in enumerate([(1120, 770, 1470, 0.38, 0.0), (-80, 300, 1520, 0.4, 1.3)]):
            u = ((t + ph) / 4.4) % 1.0
            x = lerp(x0, x1, u); d = -1 if x1 < x0 else 1
            q = P(legs="walk", phase=t * 5.5 + ph, turn=0.4 * d, gx=0.7 * d, gy=0.1, furrow=0.6, armL=("ik", 110, 330), armR=("ik", -110, 330), blink=blink_at(t, 534 + k))
            o += at_feet(enemy_spec(random.Random(535 + k)), q, t, x, y, sc) + stone_block(x, y - (FEET - 300) * sc, 130 * sc / 0.38 * 0.38 * 2.2, 80 * sc * 2.2 / 1.0 * 0.5, 536 + k)
        oq = P(turn=-0.35, gx=-0.7, gy=0.0, furrow=0.6, armR="point", armL="hip", blink=blink_at(t, 538))
        o += at_feet(OFFICER, oq, t, 930, 1600, 0.46)
        return o
    A = Shot(4.4, fr, midA, cam=cam_push(1.0, 1.06, 560, 1200, 4.4), light=NOON, sun=NOON_SUN, fade_in=0.5,
             fx=[Motes(40, 539, (255, 236, 200), (100, 500, 980, 1500), (10, -4), amax=80)])
    # B: the great camp at Barzand
    ac = bgs.cached("army_camp", bgs.army_camp)
    def midB(t):
        o = DUSTDEF
        for k, (x, y, s) in enumerate([(180, 1040, 0.5), (520, 1060, 0.6), (860, 1030, 0.45), (690, 1150, 0.8)]):
            o += smoke(t, x, y, 540 + k, s)
        for k in range(12):          # columns of men on the camp road
            x = (k * 110 + 40 * t) % 1300 - 100
            o += sil(x, 1235 + 12 * (k % 2), 0.42, t, k * 0.7, col="#18181e")
        for k in range(8):
            x = 1180 - ((k * 150 + 34 * t) % 1400)
            o += sil(x, 1330 + 10 * (k % 2), 0.55, t, k * 1.1, col="#141418", d=-1)
        return o
    B = Shot(4.0, ac, midB, cam=cam_push(1.0, 1.06, 540, 1150, 4.0), light=dict(rim=(0, 0)), sun=(900, 500, 900, (0.08, 0.06, 0.03)))
    # C1: Afshin and an officer in the camp: "We dig. We wait."
    acb = blur_bg("army_camp", bgs.army_camp, 8)
    LC1 = [("p5s3a", 0.8)]
    def midC1(t):
        oq = P(turn=0.4, gx=0.8, gy=-0.1, furrow=0.4, armL="relaxed", armR="relaxed", blink=blink_at(t, 541), nod=4 * ease((t - 2.4) / 0.4))
        a = talk_pose(LC1, t, 542, dict(turn=-0.35, gx=-0.7, gy=0.0, furrow=0.5, armR=("ik", -260, 230) if 0.9 < t < 2.6 else "relaxed", armL="hip"))
        return at_feet(OFFICER, oq, t, 300, 1620, 0.6) + at_feet(dict(OFFICER, beard="full", skin="olive"), P(turn=0.3, gx=0.7, armL="relaxed", armR="relaxed", blink=blink_at(t, 543)), t, 110, 1560, 0.52) + \
            at_feet(AFSHIN, P(**a), t, 760, 1640, 0.64)
    C1 = Shot(3.6, acb, midC1, cam=cam_push(1.0, 1.04, 560, 1050, 3.6), light=NOON, sun=NOON_SUN)
    # C2: "Every road we take, we keep."
    LC2 = [("p5s3b", 0.3)]
    def midC2(t):
        q = talk_pose(LC2, t, 544, dict(turn=-0.25, gx=-0.5, gy=0.05, furrow=0.6, brow=-0.1, nod=5 * ease((t - 1.9) / 0.3), armL="relaxed", armR="relaxed"))
        return at_neck(AFSHIN, P(**q), t, 560, 1070, 1.18)
    C2 = Shot(3.6, acb, midC2, cam=cam_push(1.0, 1.05, 560, 860, 3.6), light=NOON, sun=NOON_SUN)
    # D: roads blocked with stones, trenches dug behind them
    floor = bgs.cached("gorge_floor_noon", lambda: bgs.gorge_floor("noon"))
    def midD(t):
        o = DUSTDEF
        for k in range(9):                                       # the barricade across the road
            o += bgs.boulder(70 + 120 * k, 1300 + 8 * math.sin(k * 1.7), 62 + 10 * math.sin(k * 2.3), 620 + k, "#9a7c5c", "#5a4432", "#c8aa86")
        for k, x in enumerate((230, 690)):                       # men set more stones on it
            lift = 0.5 + 0.5 * math.sin(t * 2.2 + k * 2)
            q = P(turn=0.1 if k else -0.1, gx=0.2, gy=0.2, furrow=0.6, armL=("ik", 120, lerp(330, 60, lift)), armR=("ik", -120, lerp(330, 60, lift)), blink=blink_at(t, 621 + k))
            o += at_feet(enemy_spec(random.Random(622 + k)), q, t, x, 1250, 0.27)
            o += stone_block(x, 1250 - (FEET - lerp(300, 30, lift)) * 0.27, 70, 44, 623 + k)
        o += pole_flag(t, 960, 900, 400, 150, 90)
        for k in range(10):                                      # dirt thrown out of the trench, behind the diggers
            x = 60 + 110 * k
            o += f'<ellipse cx="{x}" cy="{1500 - 4 * math.sin(k)}" rx="{74 + 8 * (k % 3)}" ry="30" fill="#8a6a4a" stroke="#4a3220" stroke-width="3"/>'
        o += ('<path d="M -40 1590 C 300 1576, 760 1580, 1120 1570 L 1120 1660 C 760 1676, 300 1672, -40 1690 Z" fill="#3a2414"/>'
              '<path d="M -40 1590 C 300 1576, 760 1580, 1120 1570" stroke="#6a4a30" stroke-width="8" fill="none"/>'
              '<path d="M -40 1640 C 300 1630, 760 1634, 1120 1622" stroke="#24160c" stroke-width="16" fill="none" opacity="0.6"/>')
        for k, (x, tool) in enumerate([(220, "pick"), (520, "shovel"), (830, "pick")]):
            ph = t * (3.2 if tool == "pick" else 2.6) + k * 1.7
            sw = 0.5 + 0.5 * math.sin(ph)
            if tool == "pick":
                q = P(turn=0.15, gx=0.3, gy=0.5, furrow=0.8, armL=("ik", lerp(40, 60, sw), lerp(-260, 300, sw)), armR=("ik", lerp(-40, 0, sw), lerp(-240, 320, sw)),
                      propL=("pick", lerp(170, 20, sw)), blink=blink_at(t, 624 + k))
            else:
                q = P(turn=-0.2, gx=-0.3, gy=0.6, furrow=0.6, armL=("ik", 170, lerp(380, 250, sw)), armR=("ik", -80, lerp(250, 120, sw)),
                      propL=("shovel", lerp(-20, 30, sw)), blink=blink_at(t, 624 + k))
            o += at_feet(enemy_spec(random.Random(625 + k)), q, t, x, 1572, 0.42)
            if tool == "shovel" and sw > 0.75:
                a = (sw - 0.75) * 4
                o += "".join(f'<circle cx="{x + 120 + 60 * a + 20 * j:.0f}" cy="{1380 - 120 * a + 40 * a * a + 10 * j:.0f}" r="{11 - j * 2}" fill="#6a4a30"/>' for j in range(3))
        return o
    D = Shot(4.4, floor, midD, cam=cam_push(1.0, 1.05, 540, 1250, 4.4), light=NOON, sun=NOON_SUN,
             fx=[Motes(40, 626, (230, 210, 180), (0, 900, W, 1600), (10, -16), (2, 4), 100)])
    # E: the drums give the signal to march
    def midE(t):
        o = column(t, 1330, 0.24, 9, 627, banners=(2, 6), ph0=0.5, speed=60)
        beat = abs(math.sin(t * math.pi / 0.32))
        q = P(turn=0.0, gx=0.0, gy=0.3, furrow=0.9, brow=-0.2, mouth_o=0.2, armL=("ik", 180, lerp(-60, 260, beat)), armR=("ik", -180, lerp(260, -60, beat)),
              propL=("drumstick", 20), propR=("drumstick", -20), blink=blink_at(t, 628))
        o += at_feet(DRUMMER, q, t, 540, 1700, 0.62)
        dx, dy = 540, 1700 - (FEET - 420) * 0.62          # the kettle drum in front of his belly
        o += (f'<path d="M {dx - 120} {dy + 150} L {dx - 170} {1720} M {dx + 120} {dy + 150} L {dx + 170} {1720} M {dx} {dy + 170} L {dx} {1730}" stroke="#4a2e16" stroke-width="16"/>'
              f'<path d="M {dx - 190} {dy} C {dx - 180} {dy + 200}, {dx + 180} {dy + 200}, {dx + 190} {dy} Z" fill="#7a4a22" stroke="#1b0f0a" stroke-width="5"/>'
              f'<ellipse cx="{dx}" cy="{dy}" rx="190" ry="44" fill="#d8c8a0" stroke="#1b0f0a" stroke-width="5"/>'
              f'<path d="M {dx - 170} {dy + 40} C {dx - 100} {dy + 110}, {dx + 100} {dy + 110}, {dx + 170} {dy + 40}" stroke="#c9a24a" stroke-width="8" fill="none"/>')
        return o
    E = Shot(2.6, acb, midE, cam=lambda t: (1.02, 540, 1100, 0, 2.5 * abs(math.sin(t * math.pi / 0.32))), light=NOON, sun=NOON_SUN)
    # F: watch fires along the ridges at dusk
    rd = bgs.cached("ridges_dusk", bgs.ridges_dusk)
    def midF(t):
        o = ""
        for k, (x, y, a) in enumerate(bgs.RIDGE_FIRES):
            o += flame(x, y, 0.16 * a, t, k)
            if a > 1.2 and k % 2 == 0:
                o += sil(x + 22, y + 4, 0.22, t * 0.2, k, col="#08060a", spear=True)
        return o
    F = Shot(3.6, rd, midF, cam=cam_push(1.0, 1.06, 540, 1250, 3.6), light=dict(rim=(0, 0)), grade="night", bloom=0.8, fade_out=0.4)
    # G1: Bazz: Babak and his commanders around the map table
    wr = bgs.cached("war_room", bgs.war_room)
    table = bgs.cached("war_table5", _war_table)
    LG1 = [("p5s3c", 1.0)]
    def midG1(t):
        o = ""
        c = talk_pose(LG1, t, 631, dict(turn=0.3, gx=0.6, gy=0.4 if t < 1.8 else 0.0, furrow=0.6, armR="relaxed",
                                        armL=("ik", 300, 380) if 1.0 < t < 3.6 else "relaxed"))
        o += at_neck(COMMANDER, P(**c), t, 250, 930, 0.6)
        f = P(turn=-0.3, gx=-0.6, gy=0.3, furrow=0.5, armL="relaxed", armR="relaxed", blink=blink_at(t, 632))
        o += at_neck(FIGHTER2, f, t, 850, 935, 0.58)
        b = talk_pose([], t, 633, dict(turn=0.0, gx=0.0, gy=0.75, furrow=0.8, armL=("ik", 160, 420), armR=("ik", -160, 420)))
        o += at_neck(BABAK, P(**b), t, 545, 900, 0.62)
        return o
    G1 = Shot(4.4, wr, midG1, fg=table, cam=cam_push(1.0, 1.05, 545, 1000, 4.4), light=WARROOM, grade="fire", fade_in=0.4)
    wrb = blur_bg("war_room", bgs.war_room, 9)
    LG2 = [("p5s3d", 0.4)]
    def midG2(t):
        up = ease((t - 1.0) / 0.5)
        q = talk_pose(LG2, t, 634, dict(turn=0.1, gx=0.2, gy=0.7 - 0.8 * up, furrow=0.8, brow=-0.1, armL="relaxed", armR="relaxed"))
        return at_neck(BABAK, P(**q), t, 540, 1075, 1.2)
    G2 = Shot(2.6, wrb, midG2, cam=cam_push(1.0, 1.03, 540, 860, 2.6), light=dict(rim=(0, -4), rim_col=(1.0, 0.7, 0.4), rim_str=0.8, ramp=(0, W, 0.9, 1.0)),
              sun=(540, 500, 700, (0.10, 0.06, 0.02)), grade="fire")
    # G3: the map: black stones close a ring round Bazz (voice: "He is building a wall around us.")
    tm = bgs.cached("table_map", bgs.table_map)
    ring = [(540 + 250 * math.cos(a), 975 + 290 * math.sin(a)) for a in [i * math.pi / 4 - math.pi / 2 for i in range(8)]]
    placed0 = [ring[0], ring[4]]
    order = [ring[1], ring[2], ring[3], ring[5], ring[6], ring[7]]
    def pebble(x, y, col="#16161a", r=40):
        return (f'<ellipse cx="{x + 4:.1f}" cy="{y + 6:.1f}" rx="{r:.1f}" ry="{r * 0.8:.1f}" fill="#000" opacity="0.35"/>'
                f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="{r:.1f}" ry="{r * 0.8:.1f}" fill="{col}" stroke="#000" stroke-width="3"/>'
                f'<ellipse cx="{x - r * 0.3:.1f}" cy="{y - r * 0.3:.1f}" rx="{r * 0.3:.1f}" ry="{r * 0.18:.1f}" fill="#fff" opacity="0.35"/>')
    def midG3(t):
        o = pebble(540, 975, "#b5161b", 46)
        for x, y in placed0:
            o += pebble(x, y)
        hx, hy = 1200, 1500
        for k, (x, y) in enumerate(order):
            t0 = 0.5 * (k + 1)
            if t >= t0:
                o += pebble(x, y)
            if t0 - 0.45 <= t < t0 + 0.05:
                u = ease((t - (t0 - 0.45)) / 0.45)
                px, py = (1150, 1600) if k == 0 else order[k - 1]
                hx, hy = lerp(px, x, u), lerp(py, y, u) - 60 * math.sin(u * math.pi)
        if t >= 0.5 * len(order) + 0.05:
            u = ease((t - 0.5 * len(order) - 0.05) / 0.6)
            lx, ly = order[-1]
            hx, hy = lerp(lx, 1250, u), lerp(ly, 1700, u)
        # Babak's arm and hand (from the lower right edge), the pebble in his fingers
        sx, sy = 1260, 1900
        ang = math.degrees(math.atan2(hy - sy, hx - sx))
        L = math.hypot(hx - sx, hy - sy)
        o += (f'<g transform="translate({sx},{sy}) rotate({ang:.1f})">'
              f'<path d="M 0 -62 L {L - 60:.1f} -46 L {L - 60:.1f} 46 L 0 62 Z" fill="#4a3017" stroke="#1b0f0a" stroke-width="5"/>'
              f'<rect x="{L - 92:.1f}" y="-52" width="34" height="104" rx="10" fill="#d8a64a" stroke="#1b0f0a" stroke-width="4"/>'
              f'<ellipse cx="{L - 20:.1f}" cy="0" rx="62" ry="48" fill="#c98a5e" stroke="#1b0f0a" stroke-width="5"/>'
              f'<ellipse cx="{L + 22:.1f}" cy="-26" rx="30" ry="15" fill="#c98a5e" stroke="#1b0f0a" stroke-width="4"/></g>')
        holding = any(0.5 * (k + 1) - 0.45 <= t < 0.5 * (k + 1) for k in range(len(order)))
        if holding:
            o += pebble(hx, hy, r=36)
        return o
    G3 = Shot(3.6, tm, midG3, cam=cam_push(1.0, 1.06, 540, 1000, 3.6), light=dict(rim=(0, 0)), sun=(540, 900, 900, (0.10, 0.06, 0.02)), grade="fire")
    # G4: Babak looks up from the map
    def midG4(t):
        q = P(turn=0.05, gx=0.1, gy=-0.1, furrow=0.95, brow=-0.2, armL="relaxed", armR="relaxed", blink=blink_at(t, 635), breathe=math.sin(t * 2))
        return at_neck(BABAK, q, t, 540, 1075, 1.2)
    G4 = Shot(2.4, wrb, midG4, cam=cam_push(1.03, 1.07, 540, 860, 2.4), light=dict(rim=(0, -4), rim_col=(1.0, 0.7, 0.4), rim_str=0.8, ramp=(0, W, 0.9, 1.0)),
              sun=(540, 500, 700, (0.10, 0.06, 0.02)), grade="fire", fade_out=0.6)
    return [A, B, C1, C2, D, E, F, G1, G2, G3, G4]


def _war_table():
    s = ('<defs><linearGradient id="wt" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8a5a30"/><stop offset="1" stop-color="#4a2a14"/></linearGradient></defs>'
         '<path d="M 20 1100 L 1060 1100 L 1140 1560 L -60 1560 Z" fill="url(#wt)" stroke="#1b0f0a" stroke-width="6"/>' +
         "".join(f'<path d="M {20 - k * 9} {1100 + k * 52} L {1060 + k * 9} {1100 + k * 52}" stroke="#3a2010" stroke-width="3" opacity="0.5"/>' for k in range(1, 9)) +
         '<path d="M 300 1180 l 40 -36 l 40 36 M 650 1170 l 46 -40 l 46 40 M 200 1330 l 50 -44 l 50 44 M 820 1320 l 50 -42 l 50 42" stroke="#e8c898" stroke-width="5" fill="none" opacity="0.7"/>'
         '<path d="M 120 1150 C 300 1250, 450 1260, 540 1300 C 650 1350, 800 1420, 1000 1470" stroke="#e8c898" stroke-width="4" fill="none" stroke-dasharray="14 10" opacity="0.6"/>'
         '<ellipse cx="540" cy="1290" rx="18" ry="12" fill="#b5161b" stroke="#000" stroke-width="3"/>' +
         "".join(f'<ellipse cx="{540 + 200 * math.cos(a):.0f}" cy="{1290 + 120 * math.sin(a):.0f}" rx="15" ry="10" fill="#16161a" stroke="#000" stroke-width="3"/>'
                 for a in (-2.6, -1.2, 0.3, 1.5, 2.6)) +
         '<path d="M -60 1560 L 1140 1560 L 1140 1920 L -60 1920 Z" fill="#2e1a0c"/><path d="M -60 1560 L 1140 1560" stroke="#a87444" stroke-width="8"/>')
    return svg_render(s)


# ================================================================ S4 the silver bait (65.6-99.0)
def convoy(t, x0, y, s, n=3, speed=55.0, guards=True, run_at=None):
    o = ""
    for k in range(n):
        x = x0 + speed * t - k * 420 * s / 0.42
        o += mule_chest(t, x, y + 6 * (k % 2), s, walk=True, phase=t * 4 + k, col=["#6a5646", "#5a4a3c", "#7a6450"][k % 3])
        if guards:                  # a guard walks between each mule and the next one, on the near side
            gx = x + 205 * s / 0.42
            if run_at is not None and t > run_at:
                gx += 260 * (t - run_at)
            q = P(legs="walk", phase=t * (6 if run_at is None or t < run_at else 11) + k, turn=0.42, gx=0.7, furrow=0.5, armL=("ik", 250, 560), propL="pike",
                  armR="relaxed", blink=blink_at(t, 640 + k))
            o += at_feet(enemy_spec(random.Random(641 + k)), q, t, gx, y + 26, s * 0.62)
    return o


def s4():
    # A: mules with chests of silver on a mountain road
    fday = bgs.cached("forest_road_day", lambda: bgs.forest_road("day"))
    def midA(t):
        return pole_flag(t, 600 + 55 * t, 1080, 330, 140, 80) + convoy(t, 760, 1400, 0.42)
    A = Shot(3.6, fday, midA, cam=cam_push(1.0, 1.05, 560, 1250, 3.6), light=NOON, sun=NOON_SUN, fade_in=0.4)
    # B1: two scouts watch from the trees
    leaves = bgs.cached("leaves_fg_day", lambda: bgs.leaves_fg("day"))
    fdb = blur_bg("forest_road_day", lambda: bgs.forest_road("day"), 10)
    def midB1(t):
        o = ""
        for k, (S, x, y, sd) in enumerate([(SCOUT, 440, 1090, 651), (FIGHTER, 730, 1110, 652)]):
            q = P(turn=0.35, gx=0.8, gy=0.6, furrow=0.7, brow=-0.1, armL="relaxed", armR="relaxed", blink=blink_at(t, sd), nod=6)
            o += at_neck(S, q, t, x, y, 0.72)
        return o
    B1 = Shot(2.0, fdb, midB1, fg=leaves, cam=cam_push(1.0, 1.04, 580, 1000, 2.0), light=dict(rim=(5, -3), rim_col=(1.0, 0.86, 0.62), ramp=(0, W, 0.8, 0.95), ambient=(0.85, 0.9, 0.85)),
               sun=NOON_SUN)
    # B2: what they see: the convoy below, through the leaves
    leaves_top = bgs.cached("leaves_fg_day_top", lambda: bgs.cached("leaves_fg_day", lambda: bgs.leaves_fg("day")).transpose(Image.FLIP_TOP_BOTTOM))
    def midB2(t):
        return convoy(t + 4.0, 200, 1395, 0.36)
    B2 = Shot(2.2, fday, midB2, fg=leaves_top, cam=cam_push(1.08, 1.12, 560, 1350, 2.2), light=NOON, sun=NOON_SUN)
    # C1: night, by the fire: the scout reports
    wn = bgs.cached("woods_night", bgs.woods_night)
    LC1 = [("p5s4a", 0.6), ("p5s4b", 2.2)]
    FIRE5 = dict(point=(540, 1440, 900, 0.42, 1.2, (1.0, 0.55, 0.25)), rim_point=(540, 6), rim_col=(1.0, 0.65, 0.3), ambient=(0.8, 0.8, 0.95))
    def midC1(t):
        o = ""
        f = P(turn=0.0, gx=0.4, gy=0.0, furrow=0.5, legs="sit", armL=("ik", 60, 330), armR=("ik", -60, 330), blink=blink_at(t, 653))
        o += at_neck(FIGHTER2, f, t, 560, 1350 - 575 * 0.46, 0.46)
        o += fire_svg(540, 1450, 95, t, 1)
        b = talk_pose([], t, 654, dict(turn=0.35, gx=0.8, gy=-0.35, furrow=0.6, brow=0.1, legs="sit", armL=("ik", 60, 330), armR=("ik", -60, 330)))
        o += at_neck(BABAK, P(**b), t, 280, 1440 - 575 * 0.64, 0.64)
        sq = talk_pose(LC1, t, 655, dict(turn=-0.35, gx=-0.8, gy=0.3, brow=0.5, smile=0.2, armL="point" if 2.3 < t < 4.4 else "relaxed", armR="relaxed",
                                         breathe=math.sin(t * 5)))
        o += at_feet(SCOUT, P(**sq), t, 820, 1560, 0.6)
        return o
    C1 = Shot(5.0, wn, midC1, cam=cam_push(1.0, 1.05, 560, 1150, 5.0), light=FIRE5, grade="fire", fade_in=0.4,
              fx=[Embers(40, 656, (470, 1250, 610, 1440), (60, 150))])
    # C2: Babak by the fire: "If we take their silver, their soldiers will not fight."
    wnb = blur_bg("woods_night", bgs.woods_night, 9)
    LC2 = [("p5s4c", 0.4), ("p5s4d", 2.3)]
    def midC2(t):
        q = talk_pose(LC2, t, 657, dict(turn=0.25, gx=0.5, gy=0.1, furrow=0.7, smile=0.2 * ease((t - 3.9) / 0.5), armL="relaxed", armR="relaxed"))
        return at_neck(BABAK, P(**q), t, 520, 1075, 1.2)
    C2 = Shot(4.6, wnb, midC2, cam=cam_push(1.0, 1.05, 520, 860, 4.6),
              light=dict(point=(900, 1350, 1000, 0.45, 1.2, (1.0, 0.55, 0.25)), rim_point=(900, 6), rim_col=(1.0, 0.65, 0.3), ambient=(0.8, 0.8, 0.95)),
              grade="fire", fx=[Embers(30, 658, (860, 1300, 1080, 1700), (60, 150))], sun=(1000, 1300, 700, (0.12, 0.05, 0.01)))
    # D: the night attack: Babak's men run down on the convoy; its guards run away
    fnight = bgs.cached("forest_road_night", lambda: bgs.forest_road("night"))
    r = random.Random(660)
    raiders = [(r.choice([FIGHTER, FIGHTER2, SCOUT, villager_spec(r, red=True)]), -100 - 170 * k, 1395 + 30 * (k % 3), 0.36 + 0.02 * (k % 3), r.uniform(0, 6)) for k in range(6)]
    def raid(t, stop=None):
        o = ""
        for S, x0, y, sc, ph in sorted(raiders, key=lambda v: v[2]):
            tt = t if stop is None else min(t, stop)
            x = x0 + 230 * tt
            running = stop is None or t < stop
            q = P(legs="walk" if running else "stand", phase=t * 11 + ph, turn=0.45, gx=0.8, furrow=0.8, mouth_o=0.3 if running else 0.0, wind=0.8,
                  armL=("ik", 300, -480), propL="spear_red", armR="relaxed", blink=blink_at(t, int(ph * 10)))
            o += at_feet(S, q, t, x, y, sc)
        return o
    def midD(t):
        o = convoy(0.0, 760, 1390, 0.36, n=2, speed=0.0, guards=False)
        for k, x0 in enumerate((900, 1010)):
            gx = x0 + (300 * (t - 1.2) if t > 1.2 else 0)
            q = P(legs="walk" if t > 1.2 else "stand", phase=t * 11 + k, turn=0.42 if t > 1.2 else -0.3, gx=0.7 if t > 1.2 else -0.6, brow=0.6, furrow=-0.3,
                  armL=("ik", 250, 560), propL="pike", armR="relaxed", blink=blink_at(t, 661 + k))
            o += at_feet(enemy_spec(random.Random(662 + k)), q, t, gx, 1430, 0.34)
        return o + raid(t)
    D = Shot(4.0, fnight, midD, cam=cam_push(1.0, 1.05, 560, 1250, 4.0), light=MOON, grade="night", fade_in=0.2)
    # E1: torches flare up all around; riders in black close in
    torches = [(110, 1010, 0.4), (300, 985, 0.55), (960, 990, 0.7), (790, 1000, 0.85), (40, 1560, 1.0), (1040, 1580, 1.15), (200, 1030, 1.3), (880, 1020, 1.45), (570, 960, 1.6)]
    cluster = [(FIGHTER, 450, 1410, 0.3, 0.2), (FIGHTER2, 560, 1440, 0.31, 1.1), (SCOUT, 660, 1405, 0.3, 2.3), (villager_spec(random.Random(663), red=True), 770, 1445, 0.31, 3.1),
               (villager_spec(random.Random(664), red=True), 860, 1415, 0.3, 4.0)]
    def midE1(t):
        o = GLOWDEF
        for x, y, t0 in torches:
            a = ease((t - t0) / 0.25)
            if a > 0:
                o += glow(x + 20, y - 120, 210 * a, a) + sil(x, y, 0.5, t * 0.3, x, col="#0c0a0e", spear=False)
                o += f'<path d="M {x + 12:.0f} {y - 62:.0f} L {x + 20:.0f} {y - 116:.0f}" stroke="#2a1a10" stroke-width="6"/>' + flame(x + 20, y - 112, 0.7 * a, t, x)
        o += convoy(0.0, 760, 1390, 0.36, n=2, speed=0.0, guards=False)
        for k, (S, x, y, sc, ph) in enumerate(sorted(cluster, key=lambda v: v[2])):
            look = math.sin(t * 2.2 + ph)
            alarm = ease((t - 0.5 - 0.1 * k) / 0.4)
            q = P(turn=0.45 * look * alarm + 0.4 * (1 - alarm), gx=0.8 * look * alarm + 0.7 * (1 - alarm), gy=-0.3 * alarm, brow=0.8 * alarm, furrow=-0.5 * alarm,
                  mouth_o=0.3 * alarm, armL=("ik", 300, -480), propL="spear_red", armR="relaxed", wind=0.6, blink=blink_at(t, int(ph * 10)))
            o += at_feet(S, q, t, x, y, sc)
        for k, (side, y, sc, t0) in enumerate([(-1, 1560, 0.44, 1.2), (1, 1570, 0.46, 1.4), (-1, 1640, 0.52, 1.9), (1, 1650, 0.52, 2.1)]):
            u = ease((t - t0) / 1.2)
            if u <= 0:
                continue
            x = (-300 + 420 * u) if side < 0 else (1380 - 420 * u)
            q = P(turn=0.45 * -side, gx=0.8, furrow=0.9, armL="fist_up", propL="torch", armR="forward", wind=0.8, legs="none", blink=blink_at(t, 670 + k))
            o += rider(enemy_spec(random.Random(671 + k)), q, t, lambda c, k=k: horse(c, col=["#1e1a1c", "#2a2420", "#16141a", "#24201c"][k], mane="#0a0808", walk=u < 1,
                                                                                         phase=t * 6 + k, t=t + k, blanket="#121216"), x, y, sc, flip=side > 0)
        return o
    def orange(im, t):
        a = ease((t - 0.4) / 1.4)
        im.alpha_composite(Image.new("RGBA", (W, H), (255, 120, 40, int(16 * a + 4 * a * math.sin(t * 9)))))
    E1 = Shot(3.2, fnight, midE1, cam=cam_push(1.05, 1.0, 560, 1250, 3.2), light=dict(MOON, rim_col=(1.0, 0.6, 0.35)), grade="night", fx=[orange])
    # E2: "It's a trap! They knew!"
    fnb = blur_bg("forest_road_night", lambda: bgs.forest_road("night"), 10)
    from stage import glow_img
    tg = glow_img(170, (255, 140, 60), 0.55)
    def torchbg(t):
        im = fnb.copy()
        for k, (x, y) in enumerate([(120, 700), (330, 640), (760, 660), (980, 720), (60, 1000), (1020, 980)]):
            im.alpha_composite(tg, (int(x - 170 + 6 * math.sin(t * 9 + k)), int(y - 170)))
        d = ImageDraw.Draw(im, "RGBA")
        for k, (x, y) in enumerate([(120, 700), (330, 640), (760, 660), (980, 720), (60, 1000), (1020, 980)]):
            f = 1 + 0.15 * math.sin(t * 13 + k)
            d.ellipse((x - 9 * f, y - 16 * f, x + 9 * f, y + 9 * f), fill=(255, 220, 140, 230))
        return im.filter(ImageFilter.GaussianBlur(2))
    LE2 = [("p5s4e", 0.3)]
    def midE2(t):
        q = talk_pose(LE2, t, 672, dict(turn=0.2, gx=-0.6 if t < 0.25 else 0.7, gy=-0.2, brow=0.9, furrow=-0.7, wind=0.8, armL="relaxed", armR="relaxed"))
        q["mouth_o"] = min(1.0, q["mouth_o"] * 1.3)
        return at_neck(FIGHTER, P(**q), t, 540 + jitter(t, 2.0, 15.0), 1075, 1.2)
    E2 = Shot(2.4, torchbg, midE2, cam=lambda t: (1.03, 540, 880, 4 * math.sin(t * 13), 3 * math.sin(t * 11)), light=TORCH, grade="fire")
    # F: "The ravine! Go!"
    LF = [("p5s4f", 0.3)]
    def midF(t):
        q = talk_pose(LF, t, 673, dict(turn=0.35, gx=0.8, gy=0.0, brow=0.3, furrow=0.9, wind=0.9, armL="point" if t > 0.25 else "relaxed", armR="relaxed"))
        q["mouth_o"] = min(1.0, q["mouth_o"] * 1.3)
        return at_neck(BABAK, P(**q), t, 470, 1075, 1.2)
    F = Shot(2.2, torchbg, midF, cam=lambda t: (1.03, 520, 880, 4 * math.sin(t * 12), 3 * math.sin(t * 10)), light=TORCH, grade="fire")
    # G: Babak and a few men escape through the ravine
    rvn = bgs.cached("ravine_night", lambda: bgs.ravine("night"))
    runners = [(BABAK, 540, 0.0, 0.0), (FIGHTER, 380, 0.5, 1.0), (COMMANDER, 700, 0.8, 2.0), (FIGHTER2, 470, 1.3, 3.0)]
    def midG(t):
        o = ""
        items = []
        for S, x0, t0, ph in runners:
            u = (t - t0) / 3.6
            if u < 0:
                continue
            sc = lerp(0.22, 0.7, ease(u)); y = lerp(1430, 1980, ease(u) ** 1.3)
            x = lerp(x0, 540 + (x0 - 540) * 2.2, ease(u))
            q = P(legs="walk", phase=t * 10 + ph, turn=0.0 + 0.1 * math.sin(ph), gx=0.0, gy=-0.1, furrow=0.8, mouth_o=0.35, wind=1.0,
                  armL=("ik", 200, lerp(420, 200, 0.5 + 0.5 * math.sin(t * 10 + ph))), armR=("ik", -200, lerp(200, 420, 0.5 + 0.5 * math.sin(t * 10 + ph))),
                  blink=blink_at(t, int(ph * 7)))
            items.append((y, at_feet(S, q, t, x, y, sc)))
        for y, svg in sorted(items):
            o += svg
        return o
    G = Shot(4.2, rvn, midG, cam=lambda t: (1.0 + 0.04 * ease(t / 4.2), 540, 1250, 3 * math.sin(t * 9), 3 * math.sin(t * 7)), light=MOON, grade="night", fade_out=0.8)
    return [A, B1, B2, C1, C2, D, E1, E2, F, G]


# ================================================================ S5 dawn in the ravine: the face on the ridge (99.0-121.0)
RIM5 = [(-40, 760), (80, 730), (200, 750), (330, 712), (460, 730), (600, 706), (740, 726), (880, 702), (1000, 730), (1120, 715)]


def rim_y(x):
    for (x0, y0), (x1, y1) in zip(RIM5, RIM5[1:]):
        if x0 <= x <= x1:
            return lerp(y0, y1, (x - x0) / (x1 - x0))
    return RIM5[-1][1]


def s5():
    rd = bgs.cached("ravine_dawn", lambda: bgs.ravine("dawn"))
    # A: Babak and the survivors catch their breath
    def midA(t):
        o = ""
        c = P(turn=-0.2, gx=-0.6, gy=-0.4, furrow=0.6, brow=0.2, armL="relaxed", armR="relaxed", blink=blink_at(t, 701), breathe=2.2 * math.sin(t * 4.2), mouth_o=0.15)
        o += at_feet(COMMANDER, c, t, 640, 1470, 0.42)
        bend = 6
        f = P(turn=-0.25, gx=-0.5, gy=0.6, furrow=0.7, sad=0.2, armL=("ik", 120, 640), armR=("ik", -120, 640), blink=blink_at(t, 702),
              breathe=2.5 * math.sin(t * 4.6 + 1), mouth_o=0.25 + 0.15 * math.sin(t * 4.6))
        o += f'<g transform="rotate({bend},{860},{1640})">' + at_feet(FIGHTER, f, t, 860, 1640, 0.55) + '</g>'
        b = P(turn=0.2, gx=0.3, gy=0.4, furrow=0.7, sad=0.15, legs="sit", armL=("ik", 160, 360), armR=("ik", -160, 360), blink=blink_at(t, 703),
              breathe=2.5 * math.sin(t * 4.0), mouth_o=0.2 + 0.15 * math.sin(t * 4.0))
        o += bgs.boulder(330, 1600, 150, 704, "#7a5a48", "#3e2c26", "#f0a878")
        o += at_neck(BABAK, b, t, 330, 1545 - 575 * 0.7, 0.7)
        return o
    A = Shot(4.4, rd, midA, cam=cam_push(1.0, 1.05, 520, 1150, 4.4), light=DAWN, sun=(560, 650, 800, (0.14, 0.09, 0.05)), fade_in=0.8,
             fx=[Motes(40, 705, (255, 236, 220), (200, 500, 900, 1400), (4, -6), amax=80)])
    # B: Babak hears horses and looks up
    rdb = blur_bg("ravine_dawn", lambda: bgs.ravine("dawn"), 9)
    def midB(t):
        up = ease((t - 0.7) / 0.6)
        q = P(turn=0.1, gx=0.2 - 0.1 * up, gy=0.4 - 1.4 * up, brow=0.1 + 0.6 * up, furrow=0.7 - 0.6 * up, nod=-10 * up, tilt=-2 * up,
              armL="relaxed", armR="relaxed", blink=blink_at(t, 706), breathe=1.5 * math.sin(t * 3.5))
        return at_neck(BABAK, q, t, 540, 1075, 1.2)
    B = Shot(2.6, rdb, midB, cam=cam_push(1.0, 1.04, 540, 860, 2.6), light=DAWN, sun=(700, 300, 800, (0.14, 0.09, 0.05)))
    # C: Afshin's riders on the rim against the morning sky; among them, the spy
    ru = bgs.cached("ravine_up", bgs.ravine_up)
    r = random.Random(707)
    line = [(x, enemy_spec(r)) for x in (150, 280, 410, 760, 880, 1000)]
    def midC(t):
        o = pole_flag(t, 470, rim_y(470) - 300, 300, 120, 70)
        for k, (x, S) in enumerate(line + [(600, SPY)]):
            q = P(turn=0.2 if x < 540 else -0.2, gx=0.3 if x < 540 else -0.3, gy=0.8, furrow=0.6, armL="relaxed", armR="forward", legs="none",
                  blink=blink_at(t, 708 + k), wind=0.6)
            col = ["#1e1a1c", "#2a2420", "#16141a", "#24201c", "#1a1618", "#2a221c", "#5a3a22"][k]
            o += rider(S, q, t, lambda c, col=col, k=k: horse(c, col=col, mane="#0a0808", t=t + k, head_down=0.3 + 0.1 * math.sin(t + k),
                                                                blanket=None if S is SPY else "#121216"), x, rim_y(x) + 6, 0.24, flip=x > 540)
        return o
    C = Shot(4.0, ru, midC, cam=cam_push(1.0, 1.55, 600, 690, 4.0), light=dict(ambient=(0.7, 0.66, 0.74), rim=(0, -4), rim_col=(1.0, 0.8, 0.6), rim_str=0.9),
             sun=(600, 650, 700, (0.16, 0.10, 0.06)))
    # D: the spy looks down at him
    rub = blur_bg("ravine_up", bgs.ravine_up, 10)
    def midD(t):
        q = P(turn=-0.1, gx=-0.2, gy=0.75, furrow=0.3, brow=-0.1, smile=0.0, armL="relaxed", armR="relaxed", blink=blink_at(t, 715),
              nod=3 * ease((t - 1.4) / 0.5))
        q["gx"] = -0.2 if t < 1.8 else -0.6
        return at_neck(SPY, q, t, 540, 1075, 1.2)
    D = Shot(2.6, rub, midD, cam=cam_push(1.0, 1.05, 540, 860, 2.6), light=dict(ambient=(0.82, 0.78, 0.86), rim=(0, -5), rim_col=(1.0, 0.8, 0.6), rim_str=1.0, ramp=(0, W, 0.92, 1.02)),
             sun=(540, 300, 700, (0.14, 0.09, 0.05)))
    # E: "So that is how he knew." (the end card comes up over it)
    LE = [("p5s5a", 0.8)]
    def midE(t):
        q = talk_pose(LE, t, 716, dict(turn=0.1, gx=0.1, gy=-0.75 if t < 3.6 else -0.2, brow=0.0, furrow=0.95, sad=0.1, armL="relaxed", armR="relaxed"))
        q["blink"] = max(q["blink"], 0.15)
        return at_neck(BABAK, P(**q), t, 540, 1075, 1.2)
    E = Shot(8.4, rdb, midE, cam=cam_push(1.0, 1.08, 540, 860, 8.4), light=DAWN, sun=(700, 300, 800, (0.14, 0.09, 0.05)), fade_out=0.8)
    return [A, B, C, D, E]


SCENES = {"s1": s1, "s2": s2, "s3": s3, "s4": s4, "s5": s5}
