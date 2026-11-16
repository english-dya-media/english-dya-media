"""Part 8 · The Red Face (episode 4, half 2; the last part of Babak) — 2D cartoon. Timing matches p08_audio.py:
s1 0-10.8 the hook: the parade in Samarra again, part 1's opening (the boy and his father) · s2 10.8-15.4 title (Babak on the elephant) ·
s3 15.4-27.0 "Then why isn't he afraid?"; Babak looks down at the boy; Abdullah on a camel · s4 27.0-67.0 the courtyard at dusk: the herald,
the shadow on the wall, the red face · s5 67.0-93.4 after: dawn outside Samarra, Baghdad, Afshin's tower prison (840) · s6 93.4-124.0 today:
the ruins of Bazz above the clouds (end card from 119.0).
No violence is shown: the punishment is a shadow on a wall cut before the blow, a drum and the crowd turning away; deaths are a far post at
dawn, a door shutting and a lamp going out. The red face is a smear wiped on with a sleeve, no wounds."""
import math, random
import numpy as np
from PIL import Image, ImageFilter, ImageDraw
from film import Shot, W, H, ease, lerp, talk_pose, blink_at, cam_push, cam_static, Snow, Motes, Embers, svg_render
from chars import pose, elephant, camel, Ctx, FEET, CAMEL_SADDLE_Y, person, ik_angles, arm_pts
from stage import at_neck, at_feet, crowd_row, back_heads, lw_for, howdah
import bgs
from cast import *
from p01_scenes import P, blur_bg, WARM
from p02_scenes import birds
from p03_scenes import enemy_spec, red_cloth
from p05_scenes import flame, glow, GLOWDEF, smoke
from p07_scenes import captive_q, babak_in_howdah, open_letter

SAMARRA = dict(rim=(-5, -2), rim_col=WARM, ramp=(0, W, 1.06, 0.84))
SAMARRA_SUN = (150, 1250, 700, (0.10, 0.06, 0.02))
DUSK = dict(ambient=(0.80, 0.68, 0.62), rim=(4, -3), rim_col=(1.0, 0.62, 0.32), rim_str=0.9)
TORCH_R = dict(ambient=(0.9, 0.8, 0.74), rim=(6, -2), rim_col=(1.0, 0.62, 0.32), rim_str=0.95, ramp=(0, W, 0.7, 1.06))     # a torch at the right
TORCH_L = dict(ambient=(0.9, 0.8, 0.74), rim=(-6, -2), rim_col=(1.0, 0.62, 0.32), rim_str=0.95, ramp=(0, W, 1.06, 0.7))
TORCH_SUN_R = (1000, 760, 900, (0.12, 0.05, 0.0))
TORCH_SUN_L = (80, 760, 900, (0.12, 0.05, 0.0))
TORCHES = [(170, 724), (910, 724)]
SEAT_Y = 852                     # the cushion of the caliph's raised seat in court_dusk
CS = 0.3                         # the caliph's size in the wide shots
NIGHT = dict(ambient=(0.55, 0.6, 0.85), rim=(4, -3), rim_col=(0.75, 0.82, 1.0), rim_str=0.6)
TOWER = dict(ambient=(0.7, 0.66, 0.8), point=(540, 900, 700, 0.6, 1.15, (1.0, 0.6, 0.3)), rim=(0, -3), rim_col=(1.0, 0.66, 0.36), rim_str=0.8)
CELL = dict(ambient=(0.62, 0.66, 0.86), point=(700, 1250, 620, 0.5, 1.2, (1.0, 0.6, 0.3)), rim_point=(700, 5), rim_col=(1.0, 0.7, 0.4), rim_str=0.7)
MORN = dict(rim=(5, -3), rim_col=(1.0, 0.88, 0.7), rim_str=0.8, ramp=(0, W, 0.9, 1.06))


# ------------------------------------------------------------------ helpers
def dim(img, f=0.55, tint=(1.0, 0.82, 0.7)):
    """darken an RGBA layer (crowds at dusk)"""
    a = np.asarray(img).astype(np.float32)
    a[..., :3] *= np.array(tint, np.float32) * f
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), "RGBA")


def zoom_bg(name, fn, cx, cy, k, blur=0):
    """a cached close view of a background: the region around (cx, cy) enlarged k times (and blurred)"""
    def mk():
        im = bgs.cached(name, fn)
        w, h = W / k, H / k
        x0 = min(max(0, cx - w / 2), W - w); y0 = min(max(0, cy - h / 2), H - h)
        out = im.crop((int(x0), int(y0), int(x0 + w), int(y0 + h))).resize((W, H), Image.BICUBIC)
        return out.filter(ImageFilter.GaussianBlur(blur)) if blur else out
    return bgs.cached(f"{name}_z{int(cx)}_{int(cy)}_{int(k * 100)}_b{blur}", mk)


def torches(t, pts=TORCHES, s=0.9, r=190):
    o = GLOWDEF
    for k, (x, y) in enumerate(pts):
        o += glow(x, y - 30, r, 0.8 + 0.2 * math.sin(t * 9 + k)) + flame(x, y, s, t, 80 + k)
    return o


CAMEL_K = 0.66                   # the camel drawing next to a rider of stage.rider's size (rider_rel 0.31): hump ~1.3 x a horse's withers


def camel_rider(S, q, t, x, y, s, flip=False, walk=True, rate=2.6, k=0.0, col="#c49a64", blanket="#3a2e26"):
    """a camel with a rider on the saddle on its hump; sizes as stage.rider (a person standing beside it: at_feet scale 0.31 * s)"""
    c = Ctx(lw_for(s * CAMEL_K))
    rs = 0.31
    qq = dict(q); qq["legs"] = "none"
    neck_y = CAMEL_SADDLE_Y * CAMEL_K - 330 * rs * S["bs"]
    rid = f'<g transform="translate(10,{neck_y + FEET * S["bs"] * rs:.1f}) scale({rs})">{person(S, qq, t, lw_for(s * rs))}</g>'
    sx = -s if flip else s
    return (f'<g transform="translate({x:.1f},{y:.1f}) scale({sx:.4f},{s:.4f})"><g transform="scale({CAMEL_K})">'
            f'{camel(c, col=col, dark="#9a7448", walk=walk, phase=t * rate + k, t=t + k, blanket=blanket)}</g>{rid}</g>')


def crows(t, cx, cy, n=5, r=130, seed=0):
    """crows circling high over a point"""
    o = ""
    for k in range(n):
        a = t * (0.45 + 0.08 * k) + k * 2 * math.pi / n + seed
        x = cx + r * (1 + 0.35 * k / n) * math.cos(a); y = cy + 0.3 * r * math.sin(a) - 26 * k
        fl = 13 * math.sin(t * 8 + k * 1.3); sc = 1.4 + 0.3 * math.sin(a)
        o += (f'<path d="M {x - 17 * sc:.1f} {y - fl:.1f} Q {x - 6 * sc:.1f} {y - 4:.1f} {x:.1f} {y:.1f} Q {x + 6 * sc:.1f} {y - 4:.1f} {x + 17 * sc:.1f} {y - fl:.1f}" '
              f'stroke="#141014" stroke-width="5.5" fill="none" stroke-linecap="round"/>')
    return o


def boat(x, y, s, t):
    """a small sailing boat with a boatman on the Tigris"""
    rock = 1.6 * math.sin(t * 1.5)
    return (f'<ellipse cx="{x:.1f}" cy="{y + 14 * s:.1f}" rx="{150 * s:.1f}" ry="{10 * s:.1f}" fill="#2a2430" opacity="0.35"/>'
            f'<g transform="translate({x:.1f},{y:.1f}) rotate({rock:.2f}) scale({s:.3f})">'
            '<path d="M -130 -14 C -90 26, 90 26, 140 -18 L 118 -22 L -112 -22 Z" fill="#3a2a22" stroke="#1a0e08" stroke-width="4"/>'
            '<path d="M 0 -20 L 0 -190" stroke="#2a1c14" stroke-width="6"/><path d="M 6 -184 L 86 -40 L 6 -34 Z" fill="#eadfc6" stroke="#6a5a4a" stroke-width="3"/>'
            '<circle cx="-64" cy="-74" r="15" fill="#2a2024"/><path d="M -80 -58 L -48 -58 L -42 -22 L -86 -22 Z" fill="#2a2024"/>'
            '<path d="M -52 -50 L 26 34" stroke="#2a1c14" stroke-width="5"/></g>')


def tower_door(u):
    """the tower's door swinging shut (u 0 open .. 1 shut), hinged at the left side of the opening (tower_night)"""
    arch = "M 450 1180 L 450 880 Q 540 780, 630 880 L 630 1180 Z"
    x1 = lerp(462, 630, u)
    o = f'<defs><clipPath id="tdc8"><path d="{arch}"/></clipPath></defs><g clip-path="url(#tdc8)">'
    o += f'<path d="M 450 760 L {x1:.1f} {760 + 30 * (1 - u):.1f} L {x1:.1f} {1180 + 10 * (1 - u):.1f} L 450 1180 Z" fill="#4a2e1a" stroke="#1a0e06" stroke-width="4"/>'
    for k in range(1, 4):
        xx = lerp(450, x1, k / 4)
        o += f'<path d="M {xx:.1f} 760 L {xx:.1f} 1180" stroke="#2e1c10" stroke-width="3"/>'
    for yy in (900, 1060):
        o += f'<path d="M 450 {yy} L {x1:.1f} {yy}" stroke="#2a2a30" stroke-width="12"/>'
    return o + '</g>'


def clay_lamp(x, y, s, t, lit=1.0, seed=0):
    """a small clay oil lamp on the floor, its flame going out as lit goes from 1 to 0"""
    o = (f'<g transform="translate({x:.1f},{y:.1f}) scale({s:.3f})">'
         '<path d="M -60 0 C -64 -30, 30 -40, 60 -22 L 96 -30 C 104 -26, 102 -16, 92 -14 L 60 -6 C 40 10, -50 12, -60 0 Z" fill="#8a5a36" stroke="#1b0f0a" stroke-width="4"/>'
         '<ellipse cx="-6" cy="-26" rx="26" ry="7" fill="#3a2214"/><path d="M -50 -8 C -20 0, 30 0, 56 -10" stroke="#b07a4a" stroke-width="4" fill="none" opacity="0.6"/></g>')
    if lit > 0.02:
        o += f'<g opacity="{min(1.0, lit * 1.4):.2f}">' + flame(x + 92 * s, y - 30 * s, 0.32 * s * (0.4 + 0.6 * lit), t, seed) + '</g>'
    return o


def hand_at(target, side=-1, build=1.0):
    """where the rig puts the hand for an ("ik", x, y) arm (body coords) and the forearm's angle (as chars.arm)"""
    sh = (side * 172 * build * 0.92, 60)
    a1, a2 = ik_angles(sh, target, 300, 270, side, False)
    e, h = arm_pts(sh, a1, a2, 300, 270, side)
    fa = a1 - a2
    return (h[0] + side * math.sin(math.radians(fa)) * 26, h[1] + math.cos(math.radians(fa)) * 26), fa


def sleeve_end(x, y, s, ang):
    """a long sleeve's end hanging over the hand (world x, y; scale s) — the hand is never seen in the wipe"""
    return (f'<g transform="translate({x:.1f},{y:.1f}) rotate({ang:.1f}) scale({s:.3f})">'
            '<path d="M -46 -30 C -60 20, -40 70, 0 76 C 40 70, 60 20, 46 -30 Z" fill="#c79a3c" stroke="#1b0f0a" stroke-width="5"/>'
            '<path d="M -44 -18 C -20 -6, 20 -6, 44 -18" stroke="#f0d080" stroke-width="12" fill="none"/>'
            '<path d="M -30 30 C -20 50, 20 50, 30 30" stroke="#8a6420" stroke-width="5" fill="none" opacity="0.6"/></g>')


def sleeve(xc, yc, ang, s=1.0):
    """Babak's gold brocade sleeve as it sweeps across his face (centre of its end at xc, yc; the arm runs back to the lower left)"""
    dots = "".join(f'<path d="M {x} {y - 8} L {x + 7} {y} L {x} {y + 8} L {x - 7} {y} Z" fill="#7a5418" opacity="0.45"/>'
                   for x in range(-520, 60, 46) for y in (-40, 0, 40))
    return (f'<g transform="translate({xc:.1f},{yc:.1f}) rotate({ang:.1f}) scale({s:.3f})">'
            '<path d="M -700 -96 L 30 -92 C 96 -92, 124 -46, 124 0 C 124 50, 96 96, 30 96 L -700 104 Z" fill="#c79a3c" stroke="#1b0f0a" stroke-width="6"/>'
            f'{dots}<path d="M -700 40 L 40 50 C 90 52, 116 30, 120 10" stroke="#8a6420" stroke-width="10" fill="none" opacity="0.5"/>'
            '<path d="M 70 -86 C 110 -60, 124 -20, 122 10 C 120 50, 104 76, 76 90" stroke="#f0d080" stroke-width="16" fill="none"/>'
            '<path d="M -40 -92 C -30 -40, -30 40, -40 98" stroke="#f0d080" stroke-width="10" fill="none" opacity="0.8"/></g>')


SHADOWDEF = ('<defs><filter id="shf8" x="-30%" y="-30%" width="160%" height="160%"><feColorMatrix type="matrix" values="0 0 0 0 0.05  0 0 0 0 0.03  0 0 0 0 0.02  0 0 0 1 0"/>'
             '<feGaussianBlur stdDeviation="3.5"/></filter></defs>')


def scimitar(gx, gy, ang, L=330):
    """a curved sword held at the grip (gx, gy) (body coords), pointing along ang (degrees, 0 = down, 180 = up)"""
    return (f'<g transform="translate({gx:.1f},{gy:.1f}) rotate({ang:.1f})">'
            f'<rect x="-9" y="-46" width="18" height="56" rx="5" fill="#000"/><rect x="-34" y="8" width="68" height="14" rx="5" fill="#000"/>'
            f'<path d="M -12 20 C -14 {L * 0.4:.0f}, -4 {L * 0.8:.0f}, 34 {L:.0f} C 30 {L * 0.78:.0f}, 30 {L * 0.4:.0f}, 14 20 Z" fill="#000"/></g>')


def old_stone():
    """a weathered stone block from the walls of Bazz, with an iron ring on top (the red cloth is tied at about (548, 952))"""
    o = ('<path d="M 300 1010 L 320 986 L 520 976 L 560 990 L 770 984 L 800 1010 L 812 1700 L 290 1700 Z" fill="#9a8a7c" stroke="#2a2018" stroke-width="5"/>'
         '<path d="M 300 1010 L 320 986 L 520 976 L 560 990 L 770 984 L 800 1010 L 790 1040 L 310 1044 Z" fill="#cdbba6" stroke="#2a2018" stroke-width="4"/>'
         '<path d="M 290 1700 L 300 1044 L 360 1044 L 340 1700 Z" fill="#5a4c42" opacity="0.6"/>'
         '<path d="M 640 1044 L 610 1160 L 650 1250 M 420 1044 L 440 1120" stroke="#3a2e26" stroke-width="5" fill="none" opacity="0.8"/>'
         '<path d="M 300 1200 L 806 1196 M 296 1420 L 808 1414" stroke="#6a5a4e" stroke-width="5" opacity="0.5"/>')
    r = random.Random(872)
    for _ in range(14):
        x = r.uniform(320, 780); y = r.uniform(1060, 1500)
        o += f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{r.uniform(10, 34):.0f}" ry="{r.uniform(6, 14):.0f}" fill="#6a7a52" opacity="0.35"/>'
    o += ('<path d="M 530 984 C 528 950, 568 950, 566 984" stroke="#3a3436" stroke-width="10" fill="none"/>'
          '<rect x="526" y="980" width="44" height="12" rx="4" fill="#2a2426"/>')
    return o


def shadow_person(S, q, t, x, y, s, a=0.6, skew=-8.0, extra=""):
    """a person as a soft black shadow on a wall (feet at x, y); extra: more shapes in the person's body coords (a sword);
    the shot's SVG must start with SHADOWDEF"""
    body = at_feet(S, q, t, x, y, s) + (f'<g transform="translate({x:.1f},{y:.1f}) scale({s:.4f}) translate(0,{-FEET * S["bs"]:.1f})">{extra}</g>' if extra else "")
    return (f'<g filter="url(#shf8)" opacity="{a:.2f}"><g transform="translate({x:.1f},{y:.1f}) skewX({skew:.1f}) translate({-x:.1f},{-y:.1f})">{body}</g></g>')


# ================================================================ S1 the hook: the parade in Samarra (0-10.8)
def s1():
    base = bgs.cached("samarra_wide", bgs.samarra_wide)
    row1 = bgs.cached("s1_row1", lambda: crowd_row(11, 15, 1236, 0.2))
    row2 = bgs.cached("s1_row2", lambda: crowd_row(12, 12, 1282, 0.24))
    fg = bgs.cached("s1_fg", lambda: back_heads(3, 7, 1720, 0.62, blur=4))
    def bgA(t):
        im = base.copy()
        im.alpha_composite(row1, (0, int(2 * math.sin(t * 2.1))))
        im.alpha_composite(row2, (0, int(2 * math.sin(t * 2.3 + 1))))
        return im
    def midA(t):
        return babak_in_howdah(t, 860 - 58 * t, 1468, 0.6, walk=True)
    A = Shot(4.0, bgA, midA, fg=fg, cam=cam_push(1.0, 1.05, 560, 1150, 4.0), light=dict(rim=(-5, -2), rim_col=WARM, ramp=(0, W, 1.06, 0.84)),
             fx=[Motes(50, 3, (255, 220, 170), (0, 500, W, 1500), (-10, -4))], sun=(300, 1040, 700, (0.12, 0.07, 0.02)), fade_in=0.6)
    # B: the boy and his father in the crowd (4.0-10.8)
    crowd_blur = bgs.cached("s1_crowdblur", lambda: crowd_row(21, 9, 1500, 0.5, kinds=("man", "woman", "man")).filter(ImageFilter.GaussianBlur(7)))
    closeb = bgs.cached("samarra_close", bgs.samarra_close)
    bgB = closeb.copy(); bgB.alpha_composite(crowd_blur, (0, -150))
    LB = [("p8s1b", 2.1)]; LBo = [("p8s1a", 0.4)]
    def midB(t):
        at_boy = (0.3 < t < 1.9) or (3.0 < t < 5.2)
        f = talk_pose(LB, t, 801, dict(turn=-0.3, gx=-0.6 if at_boy else -0.9, gy=0.6 if at_boy else 0.0, furrow=0.5, armL="relaxed", armR="relaxed"))
        up = t < 0.3 or t > 5.4
        b = talk_pose(LBo, t, 802, dict(turn=0.32, gx=-0.6 if up else 0.7, gy=-0.5 if up else -0.7, brow=0.4 + 0.3 * (t > 5.4),
                                        armR="point" if 0.3 < t < 1.9 else "relaxed", armL="relaxed"))
        father = at_neck(FATHER, P(**f), t, 690, 610, 0.85)
        boy = at_neck(SAM_BOY, P(**b), t, 330, 610 + FEET * 0.85 - FEET * 0.62 * 0.85, 0.85)
        return boy + father
    B = Shot(6.8, bgB, midB, cam=cam_push(1.0, 1.05, 520, 800, 6.8), light=dict(rim=(-5, -2), rim_col=WARM, ramp=(0, W, 1.05, 0.86)),
             sun=(150, 1250, 700, (0.10, 0.06, 0.02)))
    return [A, B]


# ================================================================ S2 title: Babak on the elephant, calm (10.8-15.4)
def babak_close(t, look=0.0, nod=0.0, smile=0.0, seed=7):
    q = P(chains=True, armL="chest", armR="chest", turn=-0.12 + 0.06 * ease(t / 4.8) + 0.3 * look, gx=-0.35 + 0.3 * ease((t - 2.5) / 1.5) + 0.7 * look,
          gy=-0.2 + 0.75 * look, blink=max(0.22 * (1 - look), blink_at(t, seed)), furrow=0.1 - 0.2 * look, brow=0.15 * look, smile=smile, nod=nod,
          wind=0.35, breathe=math.sin(t * 1.6))
    return at_neck(BABAK_CAPTIVE, q, t, 560, 1030, 1.5)


def s2():
    rail = bgs.cached("s1_rail", lambda: svg_render(howdah(-40, 1640, 1160, 300)))
    return [Shot(4.6, blur_bg("samarra_close", bgs.samarra_close, 6), lambda t: babak_close(t), fg=rail, cam=cam_push(1.0, 1.07, 560, 860, 4.6),
                 light=dict(rim=(-6, -2), rim_col=WARM, rim_str=1.0, ramp=(0, W, 1.06, 0.82)), sun=(150, 1250, 800, (0.12, 0.07, 0.02)), fade_in=0.3)]


# ================================================================ S3 the boy's question; Babak looks down; Abdullah on a camel (15.4-27.0)
def s3():
    LA = [("p8s3a", 0.3)]
    def midA(t):
        b = talk_pose(LA, t, 803, dict(turn=-0.22, gx=-0.6, gy=-0.5, brow=0.7, furrow=-0.2, armL="relaxed", armR="relaxed"))
        return at_neck(SAM_BOY, P(**b), t, 520, 1160, 1.6)
    A = Shot(3.2, blur_bg("samarra_close", bgs.samarra_close, 6), midA, cam=cam_push(1.0, 1.03, 520, 900, 3.2),
             light=dict(rim=(-6, -2), rim_col=WARM, ramp=(0, W, 1.05, 0.86)), sun=(150, 1250, 700, (0.10, 0.06, 0.02)))
    rail = bgs.cached("s1_rail", lambda: svg_render(howdah(-40, 1640, 1160, 300)))
    def midB(t):
        look = ease((t - 0.5) / 0.8)
        nod = 7 * ease((t - 2.1) / 0.3) * (1 - ease((t - 2.7) / 0.4))
        return babak_close(t + 4.6, look=look, nod=nod, smile=0.12 * ease((t - 2.4) / 0.6), seed=804)
    B = Shot(4.2, blur_bg("samarra_close", bgs.samarra_close, 6), midB, fg=rail, cam=cam_push(1.03, 1.08, 560, 860, 4.2),
             light=dict(rim=(-6, -2), rim_col=WARM, rim_str=1.0, ramp=(0, W, 1.06, 0.82)), sun=(150, 1250, 800, (0.12, 0.07, 0.02)))
    # C: behind the elephant, Abdullah in chains on a camel, among the caliph's men (22.8-27.0)
    closeb = bgs.cached("samarra_close", bgs.samarra_close)
    crowd_blur = bgs.cached("s1_crowdblur", lambda: crowd_row(21, 9, 1500, 0.5, kinds=("man", "woman", "man")).filter(ImageFilter.GaussianBlur(7)))
    bgC = closeb.copy(); bgC.alpha_composite(crowd_blur, (0, -150))
    def midC(t):
        lift = ease((t - 2.0) / 0.8)
        q = captive_q(t, 805, look=0.3, sad=0.4 * (1 - lift), head_down=0.6 * (1 - lift))
        o = camel_rider(ABDULLAH_CHAINED, q, t, 600 - 36 * t, 1560, 1.3, flip=True, k=0.4)
        g = P(turn=-0.4, gx=-0.7, furrow=0.5, legs="walk", phase=t * 5.2, armL=("ik", 250, 560), propL="banner_black", armR="relaxed", blink=blink_at(t, 806))
        o += at_feet(GUARD, g, t, 960 - 40 * t, 1640, 0.42, flip=True)
        return o
    C = Shot(4.2, bgC, midC, cam=cam_push(1.0, 1.04, 540, 950, 4.2), light=SAMARRA, sun=SAMARRA_SUN, fade_out=0.7)
    return [A, B, C]


# ================================================================ S4 the courtyard at dusk: the red face (27.0-67.0)
def court_bg():
    base = bgs.cached("court_dusk", bgs.court_dusk)
    left = bgs.cached("p08_crowdL", lambda: dim(crowd_row(811, 7, 1200, 0.25, x0=-60, x1=200, turn_to=0.35)))
    right = bgs.cached("p08_crowdR", lambda: dim(crowd_row(812, 7, 1200, 0.25, x0=880, x1=1140, turn_to=-0.35)))
    left2 = bgs.cached("p08_crowdL2", lambda: dim(crowd_row(813, 5, 1290, 0.3, x0=-80, x1=150, turn_to=0.35), 0.45))
    right2 = bgs.cached("p08_crowdR2", lambda: dim(crowd_row(814, 5, 1290, 0.3, x0=930, x1=1160, turn_to=-0.35), 0.45))
    def bg(t, flinch=0.0):
        im = base.copy()
        dy = int(2 * math.sin(t * 1.7)); fl = int(10 * flinch)
        for k, (layer, sgn) in enumerate(((left, -1), (right, 1), (left2, -1), (right2, 1))):
            im.alpha_composite(layer, (sgn * fl, dy + (k % 2)))
        return im
    return bg


def court_people(t, babak_q=None, herald_q=None, caliph_q=None, guards_close=0.0):
    o = ""
    for k, x in enumerate((330, 750)):                                  # guards beside the raised seat
        g = P(turn=0.0, gx=0.3 * (1 if k == 0 else -1), furrow=0.5, armL=("ik", 250, 560), propL="pike", armR="relaxed", blink=blink_at(t, 815 + k))
        o += at_feet(GUARD, g, t + k, x, 1100, 0.26, flip=k == 1)
    cq = caliph_q or P(turn=-0.1, gx=-0.4, gy=0.4, furrow=0.7, legs="sit", armL="relaxed", armR="relaxed", blink=blink_at(t, 817))
    o += at_neck(MUTASIM, cq, t, 540, SEAT_Y - 575 * CS, CS)
    hq = herald_q or P(turn=-0.2, gx=-0.5, gy=0.2, furrow=0.3, armL=("ik", 160, 240), armR=("ik", -160, 240), blink=blink_at(t, 818))
    o += at_feet(HERALD, hq, t, 840, 1110, 0.27)
    o += open_letter(*feet_point(840, 1110, 0.27, 0, 250), s=0.35, ang=-4)
    for k, x in enumerate((180, 690)):                                  # guards with Babak
        x = lerp(x, 330 + (x - 330) * 0.6, guards_close)
        g = P(turn=0.3 * (1 if k == 0 else -1), gx=0.6 * (1 if k == 0 else -1), furrow=0.6, armL=("ik", 250, 560), propL="pike", armR="relaxed",
              blink=blink_at(t, 819 + k))
        o += at_feet(enemy_spec(random.Random(820 + k)), g, t + k, x, 1390, 0.39, flip=k == 1)
    bq = babak_q or P(chains=True, armL="chest", armR="chest", turn=0.3, gx=0.6, gy=-0.4, furrow=0.2, blink=max(0.2, blink_at(t, 822)))
    o += at_feet(BABAK_CAPTIVE, bq, t, 360, 1400, 0.41)
    return o


def feet_point(x, y, s, bx, by):
    """world position of a body point of a person placed with at_feet(x, y, s) (body coords from the neck)"""
    return x + s * bx, y + s * (by - FEET)


def s4():
    bg = court_bg()
    heads = bgs.cached("p08_heads", lambda: back_heads(823, 7, 1770, 0.62, col="#100806", blur=4))
    # A: wide: the caliph on his raised seat, the silent crowd, Babak in chains; the herald opens the decree (27.0-31.0)
    LA = [("p8s4a", 1.8)]
    def midA(t):
        hq = talk_pose(LA, t, 824, dict(turn=-0.2, gx=-0.5, gy=0.3, furrow=0.3, brow=0.2, armL=("ik", 160, 240), armR=("ik", -160, 240)))
        return torches(t) + court_people(t, herald_q=P(**hq))
    A = Shot(4.0, bg, midA, fg=heads, cam=cam_push(1.0, 1.06, 540, 900, 4.0), light=DUSK, grade="fire", fade_in=0.5, bloom=0.6,
             fx=[Embers(14, 825, (130, 560, 220, 720), (40, 90)), Embers(14, 826, (870, 560, 960, 720), (40, 90))])
    # B: the herald reads: "...his hands and feet shall be cut off." (31.0-34.2)
    hb = zoom_bg("court_dusk", bgs.court_dusk, 860, 780, 1.8, blur=8)
    LB = [("p8s4b", 0.2)]
    def midB(t):
        q = talk_pose(LB, t, 827, dict(turn=-0.15, gx=-0.3, gy=0.55, furrow=0.35, brow=0.25, armL=("ik", 100, 230), armR=("ik", -100, 230)))
        o = at_neck(HERALD, P(**q), t, 540, 750, 0.98)
        return o + open_letter(540, 750 + 0.98 * 236, 0.72, -2 + math.sin(t * 1.2))
    B = Shot(3.2, hb, midB, cam=cam_push(1.0, 1.04, 540, 850, 3.2), light=TORCH_R, sun=TORCH_SUN_R, grade="fire")
    # C: Babak does not move; he looks up at the caliph (34.2-37.4)
    bb = zoom_bg("court_dusk", bgs.court_dusk, 300, 820, 1.9, blur=9)
    def babak_cu(t, red=0.0, reveal=1.0, lines=(), seed=828, gx=0.45, gy=-0.3, blink=None, chains=True, **kw):
        base = dict(turn=0.12, gx=gx, gy=gy, furrow=0.35, brow=0.05, chains=chains, armL="chest" if chains else "down",
                    armR="chest" if chains else "down", red=red, red_reveal=reveal, wind=0.15)
        base.update(kw)
        q = talk_pose(list(lines), t, seed, base)
        if blink is not None:
            q["blink"] = blink
        else:
            q["blink"] = max(0.18, q["blink"])
        return at_neck(BABAK_CAPTIVE, P(**q), t, 540, 1075, 1.2)
    C = Shot(3.2, bb, lambda t: babak_cu(t), cam=cam_push(1.0, 1.05, 540, 860, 3.2), light=TORCH_L, sun=TORCH_SUN_L, grade="fire")
    # D: on the wall, the shadow of the executioner lifts his sword — cut before it falls (37.4-41.0)
    wall = bgs.cached("shadow_wall", bgs.shadow_wall)
    def midD(t):
        up = ease(t / 2.0); swing = ease((t - 3.25) / 0.35)
        hx = lerp(lerp(40, -40, up), 220, swing); hy = lerp(lerp(300, -440, up), -150, swing)
        ang = lerp(180, 115, swing)
        q = P(turn=0.4, gx=0.7, furrow=0.8, armR=("ik", hx - 18, hy + 20), armL=("ik", hx + 18, hy), blink=0.0)
        flick = 1.0 + 0.012 * math.sin(t * 11) * math.sin(t * 7)
        o = SHADOWDEF + shadow_person(GUARD, P(turn=0.3, gx=0.5, armL=("ik", 250, 560), propL="pike", armR="relaxed"), t, 880, 1560, 0.6 * flick, a=0.55, skew=-12)
        o += shadow_person(EXECUTIONER, q, t, 470, 1560, 0.66 * flick, a=0.8, skew=-10, extra=scimitar(hx, hy - 10, ang))
        return o
    D = Shot(3.6, wall, midD, cam=cam_push(1.0, 1.08, 520, 900, 3.6), light=dict(rim=(0, 0)), grade="fire", bloom=0.4)
    # E: the drum; the crowd turns away; the father hides the boy's eyes (41.0-43.8)
    eb = zoom_bg("court_dusk", bgs.court_dusk, 180, 900, 1.6, blur=9)
    crowd_e = bgs.cached("p08_crowdE", lambda: dim(crowd_row(829, 8, 1560, 0.5, kinds=("man", "woman", "man"), turn_to=0.0).filter(ImageFilter.GaussianBlur(6)), 0.5))
    ebg = eb.copy(); ebg.alpha_composite(crowd_e, (0, -160))
    def bgE(t):
        im = eb.copy(); im.alpha_composite(crowd_e, (0, -160 + int(14 * ease(t / 0.3)))); return im
    def midE(t):
        u = ease(t / 0.35)
        f = P(turn=lerp(-0.3, -0.45, u), gx=lerp(-0.9, -0.2, u), gy=lerp(0.0, 0.5, u), furrow=0.9, sad=0.3 * u, blink=0.9 * u, nod=10 * u,
              armR=("ik", lerp(-60, -250, u), lerp(330, 300, u)), armL="relaxed")
        b = P(turn=lerp(-0.2, 0.5, u), gx=lerp(-0.6, 0.6, u), gy=lerp(-0.5, 0.4, u), brow=0.7, furrow=0.2, blink=1.0 if t > 0.25 else 0.0, nod=12 * u, sad=0.2,
              armL="relaxed", armR="relaxed")
        boy = at_neck(SAM_BOY, b, t, 360 + 20 * u, 610 + FEET * 0.85 - FEET * 0.62 * 0.85, 0.85)
        father = at_neck(FATHER, f, t, 650, 610, 0.85)
        return boy + father
    def shake(im, t):
        a = max(0.0, 1 - t / 0.5)
        if a > 0:
            im.alpha_composite(Image.new("RGBA", (W, H), (255, 220, 180, int(40 * a))))
    E = Shot(2.8, bgE, midE, cam=lambda t: (1.04, 540, 800, 6 * math.sin(t * 40) * max(0.0, 1 - t / 0.4), 4 * math.sin(t * 33) * max(0.0, 1 - t / 0.4)),
             light=TORCH_R, sun=TORCH_SUN_R, grade="fire", fx=[shake])
    # F: Babak: eyes shut, then calm; his sleeve wipes across his face — it is red (43.8-47.6)
    def midF(t):
        shut = 1.0 if t < 1.0 else (1.0 - ease((t - 1.0) / 0.3) if t < 1.7 else ease((t - 1.7) / 0.15) * (1 - ease((t - 2.75) / 0.2)))
        up = ease((t - 1.4) / 0.35); u = ease((t - 1.75) / 0.85); dn = ease((t - 2.65) / 0.45)     # the arm comes up, wipes left to right, goes down
        tx, ty = lerp(-150, 175, u), lerp(-150, -205, u)
        tx, ty = lerp(-60, tx, up), lerp(330, ty, up)
        tx, ty = lerp(tx, -60, dn), lerp(ty, 330, dn)
        arm_on = 1.35 < t < 3.15
        reveal = (tx + 126) / 252 if t < 2.65 else 1.0
        o = babak_cu(t, red=1.0 if t > 1.75 else 0.0, reveal=reveal, gx=0.45 if t > 3.0 else 0.0, gy=-0.3 if t > 3.0 else 0.1, blink=shut,
                     chains=False, furrow=0.9 if t < 1.0 else 0.4, armR=("ik", tx, ty) if arm_on else "down")
        if arm_on:
            (hx, hy), fa = hand_at((tx, ty))
            o += sleeve_end(540 + 1.2 * hx, 1075 + 1.2 * hy, 1.2, fa)
        return o
    F = Shot(3.8, bb, midF, cam=cam_push(1.04, 1.1, 540, 860, 3.8), light=TORCH_L, sun=TORCH_SUN_L, grade="fire")
    # G: the caliph leans forward: "What is he doing?" (47.6-50.0)
    gb = zoom_bg("court_dusk", bgs.court_dusk, 540, 760, 2.2, blur=7)
    LG = [("p8s4c", 0.3)]
    def caliph_cu(t, lines=(), seed=830, lean=1.0, cold=0.0):
        q = talk_pose(list(lines), t, seed, dict(turn=lerp(-0.15, 0.2, cold), gx=lerp(-0.6, 0.4, cold), gy=lerp(0.45, 0.1, cold), furrow=0.5 + 0.4 * cold,
                                                 brow=0.55 * lean * (1 - cold) - 0.3 * cold, nod=8 * lean * (1 - cold), legs="sit", armL="relaxed", armR="relaxed"))
        if cold > 0:
            q["blink"] = max(q["blink"], 0.35 * cold)
        return at_neck(MUTASIM, P(**q), t, 540, 1080, 1.1)
    G = Shot(2.4, gb, lambda t: caliph_cu(t, LG, lean=ease(t / 0.4)), cam=cam_push(1.0, 1.06, 540, 860, 2.4), light=TORCH_R, sun=TORCH_SUN_R, grade="fire")
    # H: Babak, his face red: "When a man loses blood... I will not let you think I am pale from fear." (50.0-58.6)
    LH = [("p8s4d", 0.3), ("p8s4e", 4.8)]
    H_ = Shot(8.6, bb, lambda t: babak_cu(t, red=1.0, lines=LH, seed=831, chains=False, gx=0.45, gy=-0.25), cam=cam_push(1.0, 1.08, 540, 860, 8.6),
              light=TORCH_L, sun=TORCH_SUN_L, grade="fire")
    # I: the caliph says nothing; his eyes go cold; he looks away (58.6-61.0)
    I = Shot(2.4, gb, lambda t: caliph_cu(t + 2.4, cold=ease((t - 0.3) / 1.2), lean=0.0, seed=832), cam=cam_push(1.06, 1.1, 540, 860, 2.4),
             light=TORCH_R, sun=TORCH_SUN_R, grade="fire")
    # J: the boy looks at Babak; now he knows (61.0-63.8)
    def midJ(t):
        b = P(turn=-0.22, gx=-0.6, gy=-0.55, brow=0.8, furrow=-0.3, mouth_o=0.12, blink=blink_at(t, 833), armL="relaxed", armR="relaxed",
              breathe=math.sin(t * 2), nod=1.2 * math.sin(t * 0.9))
        return at_neck(SAM_BOY, b, t, 520, 1160, 1.6)
    J = Shot(2.8, ebg, midJ, cam=cam_push(1.0, 1.04, 520, 900, 2.8), light=TORCH_R, sun=TORCH_SUN_R, grade="fire")
    # K: wide: the courtyard in silence, Babak standing; the light goes (63.8-67.0)
    def midK(t):
        bq = P(chains=True, armL="chest", armR="chest", turn=0.3, gx=0.6, gy=-0.4, furrow=0.2, red=1.0, blink=max(0.2, blink_at(t, 834)))
        return torches(t) + court_people(t, babak_q=bq)
    K = Shot(3.2, bg, midK, fg=heads, cam=cam_push(1.06, 1.0, 540, 900, 3.2), light=DUSK, grade="fire", fade_out=1.6, bloom=0.6,
             fx=[Embers(14, 835, (130, 560, 220, 720), (40, 90)), Embers(14, 836, (870, 560, 960, 720), (40, 90))])
    return [A, B, C, D, E, F, G, H_, I, J, K]


# ================================================================ S5 after: dawn outside Samarra; Baghdad; Afshin's prison (67.0-93.4)
def s5():
    sd = bgs.cached("samarra_dawn", bgs.samarra_dawn)
    A = Shot(5.0, sd, lambda t: crows(t, 760, 420, n=5, r=150), cam=cam_push(1.0, 1.08, 700, 800, 5.0), grade="warm", fade_in=0.8, bloom=0.4,
             fx=[Motes(40, 840, (240, 220, 210), (0, 600, W, 1500), (-14, -2), amax=60)])
    tg = bgs.cached("tigris_dawn", bgs.tigris_dawn)
    def shimmer(im, t):
        d = ImageDraw.Draw(im, "RGBA")
        r = random.Random(int(t * 6))
        for _ in range(26):
            y = r.uniform(1020, 1470); x = 760 + r.gauss(0, 40 + (y - 1000) * 0.25)
            d.ellipse((x - 18, y - 1.5, x + 18, y + 1.5), fill=(255, 244, 220, 140))
    def midB(t):
        return birds(t, 300, 640) + boat(330 + 22 * t, 1250, 0.9, t)
    B = Shot(5.2, tg, midB, cam=cam_push(1.0, 1.05, 560, 1000, 5.2), light=dict(rim=(5, -2), rim_col=(1.0, 0.8, 0.6), ambient=(0.85, 0.82, 0.9)), grade="warm",
             fx=[shimmer], fade_in=0.3)
    # C: 840. The guards push Afshin, in chains, into the narrow tower; the door slams (77.2-83.6)
    tw = bgs.cached("tower_night", bgs.tower_night)
    def midC(t):
        o = torches(t, [(410, 884), (670, 884)], s=0.75, r=150)
        walk = ease((t - 0.3) / 3.1)
        ax = lerp(820, 540, walk)
        inside = ease((t - 3.4) / 0.6)
        aq = P(turn=-0.35 + 0.35 * inside, gx=-0.6, gy=0.3, furrow=0.6, sad=0.3, chains=True, armL="chest", armR="chest", legs="walk" if 0.3 < t < 3.6 else "stand",
               phase=t * 5.4, blink=blink_at(t, 841), nod=6)
        if inside < 1:
            a = f'<g opacity="{1 - inside:.2f}">' + at_feet(AFSHIN_PRISONER, aq, t, ax, 1182 - 12 * inside, 0.2 * (1 - 0.08 * inside)) + '</g>'
        else:
            a = ""
        guards = ""
        for k in range(2):
            gx_ = lerp(940 + 120 * k, 650 + 110 * k, ease((t - 0.3) / 3.3))
            push = k == 0 and 0.4 < t < 3.4
            g = P(turn=-0.35, gx=-0.7, furrow=0.6, legs="walk" if 0.3 < t < 3.6 else "stand", phase=t * 5.4 + k,
                  armL=("ik", 250, 560) if k == 1 else "relaxed", propL="pike" if k == 1 else None, armR=("ik", -300, 200) if push else "relaxed", blink=blink_at(t, 842 + k))
            guards += at_feet(enemy_spec(random.Random(843 + k)), g, t + k, gx_, 1186, 0.21, flip=True)
        door = tower_door(ease((t - 4.4) / 0.5))
        return o + a + door + guards
    def thud_fx(im, t):
        a = max(0.0, 1 - abs(t - 4.95) / 0.15)
        if a > 0:
            im.alpha_composite(Image.new("RGBA", (W, H), (0, 0, 0, int(60 * a))))
    C = Shot(6.4, tw, midC, cam=cam_push(1.0, 1.06, 540, 960, 6.4), light=TOWER, grade="night", fx=[thud_fx], fade_in=0.4)
    # D: inside, in the dark, Afshin alone: "You were right, Babak." (83.6-88.4)
    cell = bgs.cached("prison_cell", bgs.prison_cell)
    LD = [("p8s5c", 1.6)]
    def midD(t):
        look = ease((t - 0.3) / 0.8) * (1 - ease((t - 1.4) / 0.4))
        q = talk_pose(LD, t, 844, dict(turn=0.1, gx=0.1, gy=-0.8 * look + 0.5 * (1 - look), furrow=0.5, sad=0.5, chains=True, armL=("ik", 60, 300), armR=("ik", -60, 300),
                                       legs="sit", nod=10 * (1 - look)))
        return at_neck(AFSHIN_PRISONER, P(**q), t, 520, 1300 - 575 * 0.5, 0.5) + clay_lamp(720, 1300, 0.9, t, 1.0, 845)
    D = Shot(4.8, cell, midD, cam=cam_push(1.0, 1.05, 540, 1050, 4.8), light=CELL, grade="night", fade_in=0.3)
    # E: the little lamp burns down and goes out (88.4-93.4)
    cb = zoom_bg("prison_cell", bgs.prison_cell, 600, 1200, 1.5, blur=10)
    def midE(t):
        lit = 1.0 - ease((t - 1.6) / 0.6)
        o = clay_lamp(540, 1000, 3.0, t, lit, 846)
        if t > 2.1:
            o += '<defs><filter id="dustblur" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="9"/></filter></defs>'
            o += smoke(t - 2.1 + 2.0, 540 + 92 * 3.0, 1000 - 30 * 3.0, 847, 0.6, n=6, col="#9a9aa8", a=0.5 * (1 - ease((t - 4.0) / 0.8)))
        return o
    def dark(im, t):
        d = ease((t - 1.6) / 0.8)
        if d > 0:
            im.alpha_composite(Image.new("RGBA", (W, H), (0, 0, 0, int(170 * d))))
    E = Shot(5.0, cb, midE, cam=cam_push(1.0, 1.06, 540, 960, 5.0), light=dict(point=(816, 900, 600, 0.55, 1.2, (1.0, 0.6, 0.3))), grade="night",
             fx=[dark], fade_out=1.2)
    return [A, B, C, D, E]


# ================================================================ S6 today: the ruins of Bazz above the clouds (93.4-124.0; end card from 119.0)
def ruins_shot(dur, cam, fade_in=0.0, fade_out=0.0, mid=None, fx=()):
    base = bgs.cached("bazz_ruins", bgs.bazz_ruins)
    back = bgs.cached("cloud_back_today", lambda: bgs.cloud_sea(1180, 860))
    front = bgs.cached("cloud_front_today", lambda: bgs.cloud_sea(1330, 861, hi="#ffffff", mid="#f2eef2", lo="#dcd8e6"))
    def bg(t):
        im = base.copy(); im.alpha_composite(back, (int(-300 + 6 * t), 0)); return im
    def fg(t):
        im = Image.new("RGBA", (W, H)); im.alpha_composite(front, (int(-300 - 10 * t), 0)); return im
    return Shot(dur, bg, mid or (lambda t: birds(t, 820, 520)), fg=[fg], cam=cam, light=MORN, sun=(860, 1150, 800, (0.10, 0.07, 0.03)),
                fade_in=fade_in, fade_out=fade_out, fx=list(fx), bloom=0.6)


def s6():
    # A: rising over the ruins of Bazz (93.4-101.0)
    A = ruins_shot(7.6, cam_push(1.22, 1.1, 620, 900, 7.6, 0, 0, -80, 50), fade_in=1.0)
    # B: an old stone near the walls; a strip of red cloth tied to it, in the wind (101.0-107.4)
    sky = zoom_bg("bazz_ruins", bgs.bazz_ruins, 800, 1000, 1.6, blur=10)
    back = bgs.cached("cloud_back_today", lambda: bgs.cloud_sea(1180, 860))
    def bgB(t):
        im = sky.copy(); im.alpha_composite(back, (int(-300 + 6 * t), 120)); return im
    stone = bgs.cached("p08_stone", lambda: svg_render(old_stone()))
    def midB(t):
        lift = -16 + 5 * math.sin(t * 1.3)
        return (f'<g transform="rotate({lift:.1f},548,956)">' + red_cloth(t, 548, 944, L=330, h=56, speed=7.5, amp=30) + '</g>'
                + '<circle cx="548" cy="958" r="13" fill="#a8141a" stroke="#2a0606" stroke-width="3"/>' + birds(t, 700, 420))
    B = Shot(6.4, bgB, midB, fg=stone, cam=cam_push(1.0, 1.06, 560, 950, 6.4), light=MORN, sun=(900, 700, 900, (0.10, 0.07, 0.03)), bloom=0.6, fade_in=0.3)
    # C: the broken tower against the morning light; the boy's question comes back (107.4-110.6)
    rz = zoom_bg("bazz_ruins", bgs.bazz_ruins, 610, 700, 1.9)
    def rays(im, t):
        lay = Image.new("RGBA", (W, H)); d = ImageDraw.Draw(lay, "RGBA")
        x0, y0 = 1080, 260
        for k in range(6):
            a = 0.3 + 0.16 * k + 0.02 * math.sin(t * 0.7 + k)           # down and to the left
            pts = [(x0, y0), (x0 - 2000 * math.cos(a - 0.03), y0 + 2000 * math.sin(a - 0.03)), (x0 - 2000 * math.cos(a + 0.03), y0 + 2000 * math.sin(a + 0.03))]
            d.polygon(pts, fill=(255, 244, 220, 30))
        im.alpha_composite(lay.filter(ImageFilter.GaussianBlur(14)))
    C = Shot(3.2, rz, lambda t: birds(t, 520, 380), cam=cam_push(1.0, 1.05, 540, 900, 3.2), light=MORN, sun=(1000, 300, 900, (0.12, 0.09, 0.05)), fx=[rays], bloom=0.8)
    # D: wide: the peak above the clouds in the sun (110.6-124.0)
    D = ruins_shot(13.4, cam_push(1.0, 1.12, 600, 860, 13.4), fade_out=1.0)
    return [A, B, C, D]


SCENES = {"s1": s1, "s2": s2, "s3": s3, "s4": s4, "s5": s5, "s6": s6}
