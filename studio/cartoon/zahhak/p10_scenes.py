"""Part 10 · Damavand — 2D cartoon. Timing matches zahhak/p10_audio.py
(scene starts s1 0, s2 7.8, s3 12.4, s4 42.6, s5 68.2, s6 94.4, s7 117.6; end card 146.6; total 152.0)."""
import math, random
from PIL import Image, ImageFilter, ImageDraw
from film import Shot, W, H, ease, lerp, talk_pose, blink_at, cam_push, cam_static, Motes, Embers, svg_render
from chars import pose, horse, camel, Ctx, FEET, fmt, prop, person, CAMEL_SADDLE_Y
from stage import at_neck, at_feet, lying_at, rider, Glow, lw_for, fire_svg, back_heads, random_spec
import bgs, zbg
from cast import *
from p01_scenes import P, bg, cam_xy, tp, darken, fade_to, torch_flame, hall_fx, TORCH, HALL, NIGHT
from p03_scenes import torches_wide, torches_close, night_of, farr_svg, head_of, svg_fx, cam_svg, jamshid_court, braziers, DAYHALL, DAYCLOSE, SUNTOP
from p05_scenes import shake, silhouette, flash
from p07_scenes import kaveh_q, Cheering
from p08_scenes import fq, big_banner, banner_glints, sorush, SORL
from p09_scenes import golrang, mounted
import p10_audio as A10

MOONW = dict(ambient=(0.6, 0.66, 0.92), rim=(5, -3), rim_col=(0.75, 0.84, 1.0), rim_str=0.75)
MOON_SUN = (850, 380, 700, (0.05, 0.06, 0.10))
WINL = dict(ambient=(0.66, 0.66, 0.9), rim=(-5, -2), rim_col=(1.0, 0.7, 0.4), rim_str=0.9, ramp=(0, W, 1.08, 0.84))
LAMPT = dict(ambient=(0.78, 0.72, 0.82), rim=(-5, -2), rim_col=(1.0, 0.65, 0.35), rim_str=0.9, ramp=(0, W, 1.05, 0.88))
GATEN = dict(ambient=(0.66, 0.64, 0.86), point=(540, 1150, 900, 0.6, 1.15, (1.0, 0.55, 0.25)), rim=(0, -3), rim_col=(1.0, 0.65, 0.35), rim_str=0.7)
CAVE = dict(ambient=(0.5, 0.46, 0.58), point=(550, 1000, 900, 0.45, 1.15, (1.0, 0.6, 0.35)), rim_point=(550, 6), rim_col=(1.0, 0.7, 0.45), rim_str=0.9)
DUSKD = dict(rim=(-5, -2), rim_col=(1.0, 0.72, 0.5), rim_str=0.9, ramp=(0, W, 1.06, 0.88), ambient=(0.96, 0.88, 0.88))
SUN_DUSKD = (170, 1030, 900, (0.12, 0.07, 0.04))
FIREN = dict(ambient=(0.6, 0.64, 0.9), point=(300, 1360, 800, 0.55, 1.2, (1.0, 0.55, 0.25)), rim_point=(300, 6), rim_col=(1.0, 0.65, 0.3), rim_str=0.9)
WALL_TOP, ROPE_X = zbg.WALL_TOP, zbg.ROPE_X
HOOK_AT = (ROPE_X, WALL_TOP - 62)          # where the grapnel bites, on top of a merlon


# ---------------------------------------------------------------- helpers
def soft_flash(t0, dur=0.4, col=(255, 250, 240), peak=0.75):
    """a quick flash of light that does not burn the whole frame white"""
    def fx(im, t):
        u = (t - t0) / dur
        if -0.15 < u < 1:
            a = ease((u + 0.15) / 0.15) if u < 0 else 1 - ease(u)
            im.alpha_composite(Image.new("RGBA", (W, H), col + (int(255 * peak * a),)))
    return fx


class FadeGlow:
    """a soft glow whose strength changes with time: afn(t) 0..1"""
    def __init__(self, posfn, r, col, afn):
        from stage import glow_img
        self.img = glow_img(r, col, 1.0); self.posfn, self.r, self.afn = posfn, r, afn

    def __call__(self, im, t):
        a = self.afn(t)
        if a <= 0.01:
            return
        x, y = self.posfn(t)
        g = self.img.copy(); g.putalpha(self.img.getchannel("A").point(lambda v: int(v * min(1.0, a))))
        im.alpha_composite(g, (int(x - self.r), int(y - self.r)))


def grapnel(x, y, ang=0.0, s=1.0):
    """the iron grapnel at the end of the rope, its ring at (x, y), prongs down (ang turns it)"""
    return (f'<g transform="translate({x:.1f},{y:.1f}) rotate({ang:.1f}) scale({s:.3f})">'
            '<path d="M 0 0 L 0 46" stroke="#3a3a44" stroke-width="9"/>'
            '<path d="M 0 46 C -26 46, -40 30, -44 8 M 0 46 C 26 46, 40 30, 44 8 M 0 46 L 0 70" stroke="#4a4a56" stroke-width="8" fill="none" stroke-linecap="round"/>'
            '<circle cx="0" cy="-4" r="8" fill="none" stroke="#4a4a56" stroke-width="5"/></g>')


def rope(x0, y0, x1, y1, sag=0.0, w=7):
    mx, my = (x0 + x1) / 2 + sag, (y0 + y1) / 2
    return (f'<path d="M {x0:.1f} {y0:.1f} Q {mx:.1f} {my:.1f} {x1:.1f} {y1:.1f}" stroke="#2a1a10" stroke-width="{w + 3}" fill="none"/>'
            f'<path d="M {x0:.1f} {y0:.1f} Q {mx:.1f} {my:.1f} {x1:.1f} {y1:.1f}" stroke="#7a5a36" stroke-width="{w}" fill="none" stroke-dasharray="6 5"/>')


def climber(t, x, feet, s, rise=0.0, phase=0.0, still=False):
    """Zahhak in iron on the rope, seen as a dark shape (from behind): hands over hands"""
    ph = phase * 2.2
    a = 0.0 if still else math.sin(ph)
    q = P(turn=0.0, gx=0.0, gy=-0.8, armL=("ik", 40, -610 + 80 * a), armR=("ik", -40, -500 - 80 * a), legs="walk" if not still else "stand",
          phase=ph * 0.5, wind=0.5, snake_rise=rise, snake_looks=(0.7, 0.7), hisses=(0.3 * rise, 0.3 * rise))
    return at_feet(ZAHHAK_IRON, q, t, x, feet, s)


def eyes_glint(x, y, s, a):
    """two small yellow snake eyes (glowing) at a snake head's place (x, y)"""
    if a <= 0.01:
        return ""
    return (f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{22 * s:.1f}" fill="#f0c419" opacity="{0.25 * a:.2f}"/>'
            f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="{9 * s:.1f}" ry="{8 * s:.1f}" fill="#f0c419" opacity="{a:.2f}"/>'
            f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="{2.4 * s:.1f}" ry="{7 * s:.1f}" fill="#100806" opacity="{a:.2f}"/>')


def snake_heads(x, neck_y, s, bs=1.0):
    """screen places of the two snake heads of a person whose neck is at (x, neck_y), scale s (snakes fully risen, looking out)"""
    return [(x + sd * 340 * s * bs, neck_y - 300 * s * bs) for sd in (-1, 1)]


def zk_iron(lines, t, seed, **kw):
    base = dict(turn=0.15, gx=0.3, gy=0.0, furrow=1.0, brow=-0.3, armL="relaxed", armR="relaxed", wind=0.5,
                snake_looks=(0.6 + 0.3 * math.sin(t * 1.2), 0.5 + 0.4 * math.sin(t * 1.4 + 1)),
                hisses=(0.3 * max(0.0, math.sin(t * 1.6)), 0.3 * max(0.0, math.sin(t * 1.3 + 2))))
    base.update(kw)
    return tp(lines, t, seed, **base)


def torch_crowd(seed, spots):
    """people of the city at night, many with torches held high"""
    r = random.Random(seed)
    return [(random_spec(r, ("man", "man", "woman", "man")), x, y, sc, r.uniform(0, 6.3), r.random() < 0.6) for x, y, sc in spots]


def torch_people(t, people, look=(540, 900), cheer=0.6):
    o = ""
    for k, (S, x, y, sc, ph, torch) in enumerate(sorted(people, key=lambda p: p[2])):
        side = 1 if look[0] > x else -1
        up = cheer * (0.5 + 0.5 * math.sin(t * 2.6 + ph)) > 0.5
        q = P(turn=0.3 * side, gx=0.6 * side, gy=-0.5, brow=0.5, furrow=0.1, smile=0.2, mouth_o=cheer * max(0.0, 0.4 * math.sin(t * 6 + ph)),
              armR=("ik", -340, -170) if torch else ("fist_up" if up else "relaxed"), propR="torch" if torch else None,
              armL="fist_up" if (up and not torch) else "relaxed", blink=blink_at(t, 90 + k), breathe=math.sin(t * 2 + ph), wind=0.3)
        o += at_feet(S, q, t, x, y, sc)
    return o


# ================================================================ S1 the hook (0-7.8): the rope on the black wall
def s1():
    wall = bg("dezh_wall", zbg.dezh_wall)
    camA = cam_push(1.36, 1.42, 600, 760, 3.9)
    HK = A10.HOOK

    def midA(t):
        if t < HK:
            u = ease((t - 0.35) / (HK - 0.35))
            hx = lerp(700, HOOK_AT[0], u); hy = lerp(1750, HOOK_AT[1], u) - 260 * math.sin(math.pi * u) * 0.4
            ang = lerp(200, 0, u)
            return rope(hx, hy, 640, 2100, sag=80 * (1 - u)) + grapnel(hx, hy, ang)
        jerk = 6 * math.sin((t - HK) * 20) * math.exp(-(t - HK) * 4)
        taut = ease((t - 2.4) / 0.4)
        tug = 10 * taut * max(0.0, math.sin((t - 2.4) * 5))
        return (rope(HOOK_AT[0], HOOK_AT[1] + 46, HOOK_AT[0] + 10 * (1 - taut), 2100, sag=lerp(40, 0, taut) + jerk + tug) +
                grapnel(HOOK_AT[0], HOOK_AT[1] - 8 + 4 * jerk / 6, 0))
    A = Shot(3.9, wall, midA, cam=camA, bg_par=1.0, light=MOONW, sun=MOON_SUN, grade="night", fade_in=0.4,
             fx=[Motes(20, 101, (200, 210, 255), (0, 300, W, 1300), (-6, 2), amax=60)])

    camB = cam_push(1.0, 1.06, ROPE_X, 900, 3.9)

    def feetB(t):
        return lerp(1300, 980, ease(t / 3.4))

    def bodyB(t):
        return climber(t, ROPE_X, feetB(t), 0.34, rise=0.55 * ease((t - 2.6) / 0.8), phase=t * 1.4 if t < 3.4 else 3.4 * 1.4, still=t > 3.4)

    def midB(t):
        return rope(HOOK_AT[0], HOOK_AT[1] + 46, HOOK_AT[0], 2100) + grapnel(HOOK_AT[0], HOOK_AT[1] - 8, 0)

    def overB(t):
        a = ease((t - 3.0) / 0.5)
        neck = feetB(t) - FEET * ZAHHAK_IRON["bs"] * 0.34
        o = ""
        for k, (ex, ey) in enumerate(snake_heads(ROPE_X, neck, 0.34 * 0.55 + 0.34 * 0.45 * 0.6)):
            o += eyes_glint(ex, ey + 30, 1.2, a * (0.8 + 0.2 * math.sin(t * 9 + k)))
        return o
    B = Shot(3.9, wall, midB, cam=camB, bg_par=1.0, light=MOONW, sun=MOON_SUN, grade="night", fade_out=0.5,
             fx=[silhouette(camB, bodyB, fill=(8, 6, 12), glow=(150, 170, 235), blur=6, ga=0.8, over=overB)])
    return [A, B]


# ================================================================ S2 title (7.8-12.4): Mount Damavand at night
def s2():
    dn = bg("damavand_night", lambda: zbg.damavand("night"))
    cam = cam_push(1.0, 1.06, 610, 800, 4.6)
    return [Shot(4.6, dn, None, cam=cam, fx=[Motes(40, 201, (220, 230, 255), (0, 200, W, 1300), (-8, 3), amax=80)], grade="night",
                 bloom=0.6, fade_in=0.4, fade_out=0.5)]


# ================================================================ S3 India; the ride home; the city (12.4-42.6)
def s3():
    tent = bgs.cached("command_tent", bgs.command_tent)
    tentb = bgs.cached("command_tent_b6", lambda: bgs.cached("command_tent", bgs.command_tent).filter(ImageFilter.GaussianBlur(6)))
    # A: "Calm down, Kondrow. Maybe he is only a guest."
    LA = [("p10s3a", 0.4)]
    camA = cam_push(1.0, 1.05, 540, 860, 4.6)

    def midA(t):
        z = tp(LA, t, 1, turn=-0.3, gx=-0.7, gy=0.4, furrow=0.2, brow=0.2, smile=0.35 * ease((t - 0.3) / 0.6), armL="relaxed",
               armR="offer" if 0.8 < t < 3.6 else "relaxed", snake_looks=(0.4 + 0.3 * math.sin(t * 1.1), 0.5 + 0.3 * math.sin(t * 1.3 + 1)))
        k = P(turn=0.35, gx=0.8, gy=-0.4, brow=0.9, furrow=-0.5, sad=0.4, nod=6, armL="chest", armR="chest", blink=blink_at(t, 2), breathe=math.sin(t * 2.4))
        return at_neck(ZAHHAK_KING, z, t, 760, 900, 0.86) + at_neck(KONDROW, k, t, 300, 1120, 0.8)
    A = Shot(4.6, tent, midA, cam=camA, light=LAMPT, fx=[Glow(lambda t: cam_xy(camA, t, 290, 780), 200, (255, 170, 90), 0.35)], grade="fire",
             bloom=0.5, fade_in=0.4)

    # B: Kondrow: "A guest? With an ox-headed mace… on your throne?" — "He has your crown now, my king… and your palace."
    LB = [("p10s3b", 0.2), ("p10s3c", 5.0)]
    camB = cam_push(1.0, 1.05, 540, 860, 9.5)

    def midB(t):
        up = ease((t - 4.8) / 0.4)
        q = tp(LB, t, 3, turn=0.15, gx=0.4, gy=-0.4, brow=1.0, furrow=-0.6 + 0.4 * up, sad=0.2 + 0.3 * up,
               armL="offer" if 1.0 < t < 4.0 else "chest", armR="relaxed" if t < 6.0 else "chest", wind=0.2)
        return at_neck(KONDROW, q, t, 540, 960, 1.0)
    B = Shot(9.5, tentb, midB, cam=camB, light=dict(LAMPT, rim=(5, -2)), grade="fire", bloom=0.5)

    # C: Zahhak: "Enough! Get the horses ready. We ride home tonight!"
    LC = [("p10s3d", 0.4)]
    camC = cam_push(1.0, 1.1, 540, 860, 4.7)

    def midC(t):
        rage = ease((t - 0.3) / 0.3)
        q = tp(LC, t, 4, turn=0.0, gx=0.0, gy=0.1, furrow=1.4 * rage, brow=-0.4 * rage, armL="relaxed", armR="fist_up" if 0.4 < t < 1.6 else "relaxed",
               snake_looks=(1.0, 1.0), snake_rise=1.0, hisses=(0.9 * rage * (0.6 + 0.4 * math.sin(t * 5)), 0.9 * rage * (0.6 + 0.4 * math.sin(t * 4 + 1))))
        return at_neck(ZAHHAK_KING, q, t, 540, 1000, 1.0)
    C = Shot(4.7, tentb, midC, cam=shake(camC, 0.4, 0.9, 8), light=LAMPT, grade="fire", bloom=0.6, fx=[darken(0.3, 0.3, 5.0, (40, 0, 10))])

    # D1: the ride home at night (a tracking shot across the plain)
    def strip_night():
        im = bgs.cached("zh_ride_strip", zbg.ride_strip)
        out = Image.alpha_composite(im, Image.new("RGBA", im.size, (6, 10, 30, 178)))
        out.alpha_composite(svg_render(bgs.stars(311, 160, 700, w=im.size[0]), im.size[0], H))
        return out
    strip = bgs.cached("zh_ride_strip_night", strip_night)

    def bgD(t):
        x0 = int(1800 - 420 * t)
        return strip.crop((x0, 0, x0 + W, H))
    riders = [(ZAHHAK_KING, "#1a1a1e", 380, 1520, 0.95, 0.0), (ZGUARD, "#2a2a2e", 820, 1470, 0.78, 1.3), (ZGUARD, "#3a2a22", 1080, 1500, 0.82, 2.1),
              (ZGUARD, "#2a2a2e", 640, 1440, 0.66, 3.0)]

    def midD(t):
        o = ""
        for S, col, x, y, s, ph in sorted(riders, key=lambda e: e[3]):
            if S is ZAHHAK_KING:
                q = P(turn=-0.4, gx=-0.7, gy=-0.2, furrow=1.2, brow=-0.3, armR="forward", armL="forward", blink=blink_at(t, 11), wind=1.0,
                      snake_looks=(0.8, 0.9), hisses=(0.3, 0.3))
            else:
                q = P(turn=-0.4, gx=-0.7, gy=-0.2, furrow=0.8, armR="forward", armL=(20, 10), propL="pike", blink=blink_at(t, 12 + ph), wind=1.0)
            o += rider(S, q, t, lambda c, col=col, ph=ph: horse(c, col=col, walk=True, phase=t * 9 + ph, t=t + ph, head_bob=-20 * abs(math.sin(t * 4.5 + ph))),
                       x + 14 * math.sin(t * 3 + ph), y, s, flip=True)
        return o
    D1 = Shot(2.8, bgD, midD, cam=cam_push(1.0, 1.03, 540, 1100, 2.8), light=dict(MOONW, rim=(-5, -3)), grade="night", fade_in=0.3,
              fx=[Motes(30, 301, (200, 200, 220), (0, 900, W, 1700), (300, 0), amax=50)])

    # D2: the city at the palace gate: people with torches, the Kaviani banner
    dzn = bg("dezh_night", lambda: zbg.dezh("night"))
    crowd = torch_crowd(31, [(150, 1400, 0.27), (270, 1440, 0.29), (400, 1365, 0.25), (690, 1365, 0.25), (815, 1440, 0.29), (940, 1400, 0.27),
                             (60, 1460, 0.3), (1030, 1465, 0.3), (330, 1470, 0.3), (760, 1475, 0.3)])
    heads = bgs.cached("zh_p10_gate_heads", lambda: back_heads(1031, 9, 1760, 0.55, col="#100c14", blur=3))
    camD2 = cam_push(1.0, 1.05, 540, 1150, 3.4)

    def midD2(t):
        k = P(turn=-0.1, gx=-0.2, gy=-0.5, furrow=0.8, brow=0.2, armR="fist_up", propR="kaviani", armL="relaxed", blink=blink_at(t, 13), wind=0.6)
        return at_feet(KAVEH_NOAPRON, k, t, 545, 1335, 0.24) + torch_people(t, crowd, look=(540, 1200))
    D2 = Shot(3.4, dzn, midD2, fg=heads, cam=camD2, light=GATEN, grade="night", bloom=0.6,
              fx=[Glow(lambda t: cam_xy(camD2, t, 540, 1180), 260, (255, 170, 90), 0.35), Embers(30, 302, (0, 900, W, 1500), (40, 110))])

    # E: Kaveh at the gate: "Not one step closer, snake king! This city is free now!"
    dznb = bg("dezh_night", lambda: zbg.dezh("night"), 6)
    LE = [("p10s3f", 0.3)]
    camE = cam_push(1.0, 1.05, 540, 860, 5.2)

    def midE(t):
        q = kaveh_q(LE, t, 5, turn=0.0, gx=0.1, gy=-0.1, furrow=1.1, brow=-0.2, armR=("ik", -300, 60), propR="kaviani",
                    armL="fist_up" if 1.4 < t < 3.6 else "relaxed", wind=0.7)
        return torch_flame(110, 1060, t, 0.9, 3) + torch_flame(990, 1080, t + 0.7, 0.9, 4) + at_neck(KAVEH_NOAPRON, q, t, 560, 980, 0.95)
    E = Shot(5.2, dznb, midE, cam=camE, light=dict(GATEN, point=(540, 1100, 900, 0.65, 1.15, (1.0, 0.55, 0.25)), rim_point=(540, 6), rim=None),
             grade="fire", bloom=0.6, fx=[Glow(lambda t: cam_xy(camE, t, 110, 980), 200, (255, 170, 90), 0.4),
                                          Glow(lambda t: cam_xy(camE, t, 990, 1000), 200, (255, 170, 90), 0.4)], fade_out=0.3)
    return [A, B, C, D1, D2, E]



# ================================================================ S4 iron; the climb; the hall; the window (42.6-68.2)
def hall_win_bg(blur=0):
    return bg("hall_window", zbg.hall_window, blur)


def win_face(t, x, y, s, rise=0.0, gx=0.5, gy=0.5):
    """Zahhak's head in the high window of the hall (clipped to the opening): a dark iron helmet, a pale rim, glinting eyes"""
    q = P(turn=0.25, gx=gx, gy=gy, furrow=1.2, brow=-0.3, armL="relaxed", armR="relaxed", blink=blink_at(t, 61), wind=0.4,
          snake_rise=rise, snake_looks=(0.8, 0.8))
    return f'<clipPath id="hwclip"><path d="{zbg.HALL_WIN}"/></clipPath><g clip-path="url(#hwclip)">{at_neck(ZAHHAK_IRON, q, t, x, y, s)}</g>'


def hall_people(t, f_kw=None, sh_kw=None, ar_kw=None, sh_x=780, seed=0, sh_lines=(), f_lines=()):
    """Fereydun on the throne (mace upright), Shahrnaz and Arnavaz standing at the right"""
    fk = dict(legs="sit", turn=0.0, gx=0.6, gy=0.3, furrow=0.3, brow=0.2, smile=0.2, armL=("ik", 200, 300), propL="mace", armR="relaxed", wind=0.1,
              cloak_len=0.6)
    fk.update(f_kw or {})
    sk = dict(turn=-0.35, gx=-0.7, gy=-0.4, brow=0.6, furrow=-0.3, sad=0.2, armL="chest", armR="relaxed", wind=0.2)
    sk.update(sh_kw or {})
    ak = dict(turn=-0.35, gx=-0.7, gy=-0.4, brow=0.5, furrow=-0.2, smile=0.2, armL="relaxed", armR="chest", wind=0.2)
    ak.update(ar_kw or {})
    o = torches_wide(t) + at_neck(FEREYDUN, tp(list(f_lines), t, 1 + seed, **fk), t, 540, 793, 0.36)
    o += at_feet(ARNAVAZ, tp([], t, 3 + seed, **ak), t, sh_x + 130, 1440, 0.34)
    o += at_feet(SHAHRNAZ, tp(list(sh_lines), t, 2 + seed, **sk), t, sh_x, 1475, 0.38)
    return o


def s4():
    wallb = bg("dezh_wall", zbg.dezh_wall, 6)
    wall = bg("dezh_wall", zbg.dezh_wall)
    # A: "So Zahhak covered himself in iron, so that no one would know him." (the snakes sink under the cloak)
    camA = cam_push(1.0, 1.05, 540, 860, 6.2)

    def midA(t):
        hide = ease((t - 2.2) / 1.8)
        q = zk_iron([], t, 1, turn=0.2, gx=0.5 - 0.9 * ease((t - 4.6) / 0.6), gy=0.2 - 1.0 * ease((t - 4.6) / 0.6), furrow=0.9, brow=-0.2,
                    armL="chest" if 1.8 < t < 4.4 else "relaxed", armR="relaxed", snake_rise=1.0 - hide)
        return at_neck(ZAHHAK_IRON, q, t, 540, 980, 0.95)
    A = Shot(6.2, wallb, midA, cam=camA, light=dict(MOONW, ramp=(0, W, 0.9, 1.06)), sun=MOON_SUN, grade="night", bloom=0.5, fade_in=0.4,
             fx=[Glow(lambda t: cam_xy(camA, t, 60, 800), 260, (255, 170, 90), 0.25)])

    # B: he throws the rope and climbs
    camB = cam_push(1.0, 1.05, ROPE_X, 1000, 6.2)
    TH = A10.HOOK2 - 48.8                 # the hook bites (shot time)
    FOOT = zbg.WALL_FOOT

    def climbB(t):
        u = ease((t - 1.8) / 4.2)
        return lerp(FOOT, 1010, u)

    def bodyB(t):
        if t < TH + 0.4:
            sw = t * 7.0
            q = P(turn=0.0, gx=0.0, gy=-0.8, armR=("ik", -60 + 120 * math.cos(sw), -520 + 60 * math.sin(sw)) if t < TH - 0.5 else ("ik", -20, -560),
                  armL="relaxed", wind=0.5, snake_rise=0.0)
            return at_feet(ZAHHAK_IRON, q, t, ROPE_X - 10, FOOT, 0.34)
        return climber(t, ROPE_X, climbB(t), 0.34, rise=0.0, phase=t * 1.4)

    def midB(t):
        if t < TH - 0.5:                                         # the grapnel swings round above his head
            sw = t * 7.0
            hx = ROPE_X - 10 + 0.34 * (-60 + 120 * math.cos(sw)) + 70 * math.cos(sw * 1.0)
            hy = FOOT - 0.34 * (FEET * ZAHHAK_IRON["bs"]) + 0.34 * (-520 + 60 * math.sin(sw)) - 30 + 40 * math.sin(sw)
            return grapnel(hx, hy, math.degrees(sw) % 360, 0.9)
        if t < TH:
            u = ease((t - (TH - 0.5)) / 0.5)
            hx = lerp(ROPE_X - 20, HOOK_AT[0], u); hy = lerp(FOOT - 640, HOOK_AT[1], u) - 120 * math.sin(math.pi * u)
            return rope(hx, hy, ROPE_X - 10, FOOT - 600, sag=60) + grapnel(hx, hy, lerp(180, 0, u))
        jerk = 6 * math.sin((t - TH) * 20) * math.exp(-(t - TH) * 4)
        return rope(HOOK_AT[0], HOOK_AT[1] + 46, HOOK_AT[0] + 8, FOOT + 40, sag=jerk) + grapnel(HOOK_AT[0], HOOK_AT[1] - 8, 0)
    B = Shot(6.2, wall, midB, cam=camB, bg_par=1.0, light=MOONW, sun=MOON_SUN, grade="night",
             fx=[silhouette(camB, bodyB, fill=(8, 6, 12), glow=(150, 170, 235), blur=6, ga=0.8)])

    # C: in the hall: Shahrnaz: "For a thousand years we lived in fear. Now we are free." — a dark head appears in the high window
    hall = hall_win_bg()
    LC = [("p10s4c", 0.2)]
    camC = cam_push(1.0, 1.06, 560, 1000, 5.6)

    def midC(t):
        peek = ease((t - 2.6) / 1.0)
        o = hall_people(t, f_kw=dict(gx=0.7, gy=0.3, smile=0.3), sh_kw=dict(smile=0.35, sad=0.0, brow=0.5), sh_lines=LC)
        if peek > 0:
            o += win_face(t, 182, 700 - 120 * peek, 0.24, rise=0.0, gx=0.6, gy=0.6)
        return o

    def eyesC(t):
        a = ease((t - 3.2) / 0.5)
        return eyes_glint(187, 700 - 120 - 200 * 0.24 + 4, 0.6, a * (0.7 + 0.3 * math.sin(t * 7))) if a > 0 else ""
    C = Shot(5.6, hall, midC, cam=camC, light=HALL, fx=hall_fx(camC, [(80, 640), (1000, 640)], 401) + [svg_fx(camC, eyesC)], grade="fire", bloom=0.6)

    # D: Fereydun: "No more young men for the snakes. Never again."
    close = bg("hall_close", zbg.hall_close)
    LD = [("p10s4d", 0.1)]
    camD = cam_push(1.0, 1.04, 540, 860, 3.8)

    def midD(t):
        q = fq(LD, t, 4, turn=0.15, gx=0.5, gy=0.1, furrow=0.6, brow=0.2, smile=0.1, armL=("ik", 200, 300), propL="mace", armR="relaxed", wind=0.2)
        return torches_close(t) + at_neck(FEREYDUN, q, t, 540, 1030, 1.0)
    D = Shot(3.8, close, midD, cam=camD, light=TORCH, fx=hall_fx(camD, [(40, 740), (1040, 740)], 402), grade="fire", bloom=0.6)

    # E: Zahhak in the window, close: "Free? In my palace?" — the snakes rise, he draws his dagger and leaps
    def stone_wall():
        r = random.Random(1402)
        w = (f'<rect width="{W}" height="{H}" fill="#131018"/>' +
             "".join(f'<path d="M 0 {y} L {W} {y}" stroke="#050407" stroke-width="4" opacity="0.6"/>' for y in range(140, H, 110)) +
             "".join(f'<path d="M {x + (55 if (y // 110) % 2 else 0)} {y} L {x + (55 if (y // 110) % 2 else 0)} {y + 110}" stroke="#050407" stroke-width="4" opacity="0.6"/>'
                     for y in range(140, H, 110) for x in range(0, W, 220)) +
             "".join(f'<rect x="{r.uniform(0, W):.0f}" y="{r.uniform(150, H):.0f}" width="{r.uniform(60, 180):.0f}" height="90" fill="#2a2430" opacity="0.18"/>'
                     for _ in range(30)))
        return svg_render(w).filter(ImageFilter.GaussianBlur(4))
    wallE = bgs.cached("zh_p10_stone_wall", stone_wall)
    LE = [("p10s4e", 0.3)]
    OPEN = "M 170 1110 L 170 580 Q 540 200, 910 580 L 910 1110 Z"
    sky = ("<defs>" + bgs.lg("ws", [(0, "#060a1e", 1), (1, "#2a3060", 1)]) + "</defs>" +
           f'<rect x="150" y="200" width="780" height="920" fill="url(#ws)"/>' + bgs.stars(1401, 70, 1100) +
           '<circle cx="800" cy="470" r="40" fill="#f4f6ff"/>')
    camE = cam_push(1.0, 1.05, 540, 860, 3.8)

    def midE(t):
        rise = ease((t - 1.3) / 0.9)
        leap = ease((t - 3.3) / 0.5)
        draw = ease((t - 2.2) / 0.4)
        q = zk_iron(LE, t, 5, turn=0.15, gx=-0.2 + 0.2 * draw, gy=0.7 - 0.3 * draw, furrow=1.3 + 0.3 * draw, brow=-0.4, armL="relaxed",
                    armR="relaxed", snake_rise=rise, snake_looks=(0.5 + 0.4 * rise, 0.5 + 0.4 * rise),
                    hisses=(0.5 * rise * max(0.0, math.sin(t * 4)), 0.5 * rise * max(0.0, math.sin(t * 3.4 + 1))))
        body = at_neck(ZAHHAK_IRON, q, t, 540 - 80 * leap, 1010 + 900 * leap ** 2, 1.0)
        frame = (f'<path d="{OPEN}" fill="none" stroke="#08060a" stroke-width="30"/><path d="{OPEN}" fill="none" stroke="{zbg.GOLD}" stroke-width="14"/>'
                 f'<path d="M 140 1110 L 940 1110 L 965 1170 L 115 1170 Z" fill="#1a161e" stroke="{zbg.GOLD}" stroke-width="8"/>')
        return f'<clipPath id="weo"><path d="{OPEN}"/></clipPath><g clip-path="url(#weo)">{sky}{body}</g>' + frame
    E = Shot(3.8, wallE, midE, cam=camE, light=dict(ambient=(0.72, 0.68, 0.88), rim=(0, 4), rim_col=(1.0, 0.62, 0.3), rim_str=1.0),
             fx=[Glow(lambda t: cam_xy(camE, t, 540, 1260), 440, (255, 150, 70), 0.4)], grade="fire", bloom=0.5)
    return [A, B, C, D, E]


# ================================================================ S5 the fight; Sorush (68.2-94.4)
def helmet_half(x, y, ang, side, s=1.0):
    """one half of Zahhak's broken iron helmet"""
    d = "M 0 0 L 0 -150 C -60 -150, -110 -100, -120 -10 Z" if side < 0 else "M 0 0 L 0 -150 C 60 -150, 110 -100, 120 -10 Z"
    return (f'<g transform="translate({x:.1f},{y:.1f}) rotate({ang:.1f}) scale({s:.3f})">'
            f'<path d="{d}" fill="#2e2e38" stroke="#08070a" stroke-width="5"/>'
            f'<path d="M {-100 * (side < 0) + 0:.0f} -20 L {100 * (side > 0):.0f} -20" stroke="#5a5a68" stroke-width="6"/></g>')


def dagger_at(x, y, ang, s):
    c = Ctx(lw_for(s))
    return f'<g transform="translate({x:.1f},{y:.1f}) scale({s:.4f})">{prop(c, "dagger", 0, 0, ang, 0.0)}</g>'


def s5():
    hall = hall_win_bg()
    hallb = hall_win_bg(5)
    LAND_T = A10.LAND - 68.2
    # A: he drops from the window into the hall; "Zahhak!"
    LA = [("p10s5a", 1.2)]
    camA = cam_push(1.0, 1.05, 560, 1050, 3.8)

    def midA(t):
        fall = ease(t / LAND_T) if t < LAND_T else 1.0
        crouch = math.sin(math.pi * min(1.0, max(0.0, (t - LAND_T) / 0.5))) if t > LAND_T else 0.0
        rise = ease((t - LAND_T - 0.2) / 0.7)
        scared = ease((t - 1.1) / 0.3)
        f_kw = dict(gx=-0.8, gy=0.4, furrow=0.9 * scared, brow=0.6 * scared, smile=0.0, armL=("ik", 260, -260) if t > 2.0 else ("ik", 200, 300))
        o = hall_people(t, f_kw=f_kw, sh_x=lerp(780, 860, scared),
                        sh_kw=dict(gx=-0.9, gy=0.2, brow=1.0 * scared, furrow=-0.6 * scared, sad=0.3, armL="both_out" if scared > 0.5 else "chest",
                                   armR="chest" if scared > 0.5 else "relaxed"), sh_lines=LA)
        x = lerp(182, 300, fall); y = lerp(640 + FEET * 0.3, 1480, fall ** 1.6)
        q = zk_iron([], t, 6, turn=0.35, gx=0.8, gy=-0.2, furrow=1.4, brow=-0.4, legs="stand",
                    armL=("ik", 260, -380) if fall >= 1 else ("ik", 200, -300), armR=("ik", -260, -300) if fall < 1 else "relaxed",
                    propL=("dagger", 180), snake_rise=rise, snake_looks=(0.9, 0.9),
                    hisses=(0.7 * rise * max(0.0, math.sin(t * 5)), 0.7 * rise * max(0.0, math.sin(t * 4.4 + 1))))
        return o + at_feet(ZAHHAK_IRON, q, t, x, y + 26 * crouch, 0.38)
    A = Shot(3.8, hall, midA, cam=shake(camA, LAND_T, LAND_T + 0.4, 8), light=HALL, fx=hall_fx(camA, [(80, 640), (1000, 640)], 501), grade="fire",
             bloom=0.6)

    # B: Fereydun charges and strikes; the helmet breaks; Zahhak falls
    ST = A10.STRIKE - 72.0
    camB = cam_push(1.0, 1.04, 540, 1300, 3.2)

    def midB(t):
        run = ease(t / 1.5)
        up = ease((t - 1.1) / 0.6)
        hit = ease((t - ST + 0.18) / 0.18)
        fx_ = lerp(1040, 650, run)
        if t < ST - 0.18:
            armR = ("ik", lerp(-200, -120, up), lerp(200, -520, up)); mang = 0.0
        else:
            armR = ("ik", lerp(-120, -420, hit), lerp(-520, 40, hit)); mang = lerp(0, -95, hit)
        fqq = P(turn=-0.4, gx=-0.8, gy=0.1, furrow=1.3, brow=-0.3, mouth_o=0.4 if t > ST - 0.3 else 0.1, armR=armR, propR=("mace", mang),
                armL="forward", legs="walk" if t < 1.5 else "stand", phase=t * 9, blink=blink_at(t, 21), wind=0.9)
        o = at_feet(FEREYDUN, fqq, t, fx_, 1580, 0.5)
        down = ease((t - ST) / 0.55)
        S = ZAHHAK_IRON if t < ST else ZAHHAK_BARE
        zq = zk_iron([], t, 7, turn=0.35, gx=0.8, gy=-0.2, furrow=1.4 if t < ST else -0.4, brow=-0.4 if t < ST else 1.0, legs="stand",
                     armL=("ik", 230, -400) if t < ST else ("ik", 300, -200), propL=("dagger", 180) if t < ST else None,
                     armR=("ik", -200, -200) if t > ST else "relaxed", snake_rise=1.0 - 0.4 * down, snake_looks=(0.9, 0.9))
        if t >= ST:
            zq["blink"] = max(zq["blink"], 0.85)
        zb = at_feet(S, zq, t, 300, 1580, 0.5)
        o = (f'<g transform="rotate({-75 * down:.1f},250,1580) translate({-120 * down:.1f},{300 * down * down:.1f})">{zb}</g>') + o
        if t >= ST:                                              # the helmet halves and the dagger fly
            u = t - ST
            hx, hy = 300, 1580 - 0.5 * (FEET * ZAHHAK_IRON["bs"] + 330)
            o += helmet_half(hx - 260 * u, hy - 420 * u + 900 * u * u, -260 * u, -1, 0.5)
            o += helmet_half(hx + 60 + 200 * u, hy - 300 * u + 900 * u * u, 220 * u, 1, 0.5)
            o += dagger_at(380 - 300 * u, 1000 - 500 * u + 1300 * u * u, 600 * u, 0.5)
        return o
    B = Shot(3.2, hall, midB, cam=shake(camB, ST, ST + 0.6, 16), bg_par=1.0, light=HALL, fx=hall_fx(camB, [(80, 640), (1000, 640)], 502) +
             [soft_flash(ST, 0.4, (255, 246, 220), 0.75)], grade="fire", bloom=0.7)

    # C: Zahhak on the floor, the broken helmet; Fereydun raises the mace again
    LC = [("p10s5b", 0.4)]
    camC = cam_push(1.0, 1.05, 540, 1100, 5.8)

    def midC(t):
        o = torches_wide(t)
        o += at_feet(ARNAVAZ, P(turn=-0.35, gx=-0.9, gy=0.6, brow=0.8, furrow=-0.4, sad=0.5, armL="chest", armR="relaxed", blink=blink_at(t, 31)), t, 990, 1430, 0.34)
        o += at_feet(SHAHRNAZ, P(turn=-0.35, gx=-0.9, gy=0.6, brow=0.9, furrow=-0.5, sad=0.5, armL="chest", armR="chest", blink=blink_at(t, 32)), t, 870, 1460, 0.36)
        zq = P(blink=1.0 if t < 3.6 else 0.6, furrow=-0.3, brow=0.8, sad=0.6, snake_rise=0.55, snake_looks=(-0.6, -0.6), hisses=(0.0, 0.0))
        o += lying_at(ZAHHAK_BARE, zq, t, 380, 1400, 0.4)
        o += helmet_half(170, 1420, -80, -1, 0.4) + helmet_half(560, 1440, 95, 1, 0.4) + dagger_at(150, 1460, 100, 0.4)
        again = ease((t - 4.4) / 0.9)
        fqq = P(turn=-0.3, gx=-0.7, gy=0.6, furrow=1.0, brow=0.0, armR=("ik", lerp(-200, -120, again), lerp(250, -520, again)), propR="mace",
                armL="relaxed", blink=blink_at(t, 33), wind=0.4)
        o += at_feet(FEREYDUN, fqq, t, 700, 1440, 0.42)
        return o
    C = Shot(5.8, hall, midC, cam=camC, light=HALL, fx=hall_fx(camC, [(80, 640), (1000, 640)], 503), grade="fire", bloom=0.6)

    # D: light floods the hall: Sorush: "Do not strike again! His time has not come."
    LD = [("p10s5c", 0.7)]
    camD = cam_push(1.0, 1.05, 560, 950, 4.4)

    def midD(t):
        a = ease((t - 0.1) / 0.6)
        fqq = P(turn=0.3, gx=0.9, gy=-0.3, furrow=0.6 - 0.8 * a, brow=0.2 + 0.8 * a, armR=("ik", -120, -520), propR="mace", armL="relaxed",
                blink=blink_at(t, 41), wind=0.5)
        return torches_wide(t) + at_feet(FEREYDUN, fqq, t, 360, 1500, 0.5) + sorush(t, LD, 780, 720, 0.52, 42, a=a, gx=-0.6, gy=0.3,
                                                                                    armL="relaxed", armR="offer" if t > 1.0 else "relaxed")
    D = Shot(4.4, hallb, midD, cam=camD, light=dict(ambient=(0.86, 0.84, 0.92), rim=(6, -2), rim_col=(1.0, 0.95, 0.82), rim_str=1.0),
             fx=[FadeGlow(lambda t: cam_xy(camD, t, 780, 600), 420, (255, 244, 210), lambda t: 0.5 * ease(t / 0.6)),
                 Motes(60, 504, (255, 240, 200), (500, 200, W, 1300), (-6, -10), amax=120), flash(0.05, 0.4, (255, 250, 236))],
             grade="warm", bloom=0.8)

    # E: Sorush, close: "Bind him, and take him to the mountains, where no one can reach him."
    LE = [("p10s5d", 0.4)]
    camE = cam_push(1.0, 1.04, 540, 860, 6.0)
    bright = bgs.cached("zh_p10_hall_bright", lambda: Image.alpha_composite(hall_win_bg(9), Image.new("RGBA", (W, H), (255, 236, 200, 70))))

    def midE(t):
        return sorush(t, LE, 540, 900, 0.95, 43, a=1.0, gx=0.0, gy=0.2, armL="relaxed", armR="relaxed")
    E = Shot(6.0, bright, midE, cam=camE, light=SORL, fx=[Glow(lambda t: cam_xy(camE, t, 540, 700), 480, (255, 244, 210), 0.45),
                                                          Motes(50, 505, (255, 240, 200), (0, 300, W, 1400), (-6, -10), amax=110)],
              grade="warm", bloom=0.8)

    # F: Fereydun lowers the mace: "As you say."
    closeb = bg("hall_close", zbg.hall_close, 5)
    LF = [("p10s5e", 0.4)]
    camF = cam_push(1.0, 1.03, 540, 860, 3.0)

    def midF(t):
        low = ease((t - 0.2) / 0.8)
        q = fq(LF, t, 5, turn=0.3, gx=0.8, gy=-0.2 + 0.5 * ease((t - 1.6) / 0.5), nod=10 * ease((t - 1.6) / 0.5), furrow=0.0, brow=0.4, smile=0.1,
               armR=("ik", lerp(-120, -220, low), lerp(-520, 300, low)), propR="mace", armL="relaxed", wind=0.3)
        return at_neck(FEREYDUN, q, t, 540, 1000, 1.0)
    F = Shot(3.0, closeb, midF, cam=camF, light=dict(TORCH, rim_point=(1600, 6), rim_col=(1.0, 0.95, 0.82)), grade="fire", bloom=0.6,
             fx=[Glow(lambda t: (1100, 600), 420, (255, 244, 210), 0.35)], fade_out=0.4)
    return [A, B, C, D, E, F]



# ================================================================ S6 the road to Damavand; the cave; the mountain (94.4-117.6)
CAMEL_K = 0.66                   # the camel drawn next to a rider of stage.rider's size (rider_rel 0.31)


def camel_rider(S, q, t, x, y, s, flip=False, walk=True, rate=2.6, k=0.0, col="#c49a64", blanket="#3a2e26"):
    """a camel with a rider on the saddle on its hump (as in babak/p08_scenes.py; a person standing beside it: at_feet scale 0.31 * s)"""
    c = Ctx(lw_for(s * CAMEL_K))
    rs = 0.31
    qq = dict(q); qq["legs"] = "none"
    neck_y = CAMEL_SADDLE_Y * CAMEL_K - 330 * rs * S["bs"]
    rid = f'<g transform="translate(10,{neck_y + FEET * S["bs"] * rs:.1f}) scale({rs})">{person(S, qq, t, lw_for(s * rs))}</g>'
    sx = -s if flip else s
    return (f'<g transform="translate({x:.1f},{y:.1f}) scale({sx:.4f},{s:.4f})"><g transform="scale({CAMEL_K})">'
            f'{camel(c, col=col, dark="#9a7448", walk=walk, phase=t * rate + k, t=t + k, blanket=blanket)}</g>{rid}</g>')


def s6():
    road = bg("damavand_dusk_road", lambda: zbg.damavand("dusk", True))
    # A: the road to Damavand: Fereydun rides ahead; Zahhak bound on a camel; Kaveh with the banner
    camA = cam_push(1.0, 1.05, 560, 1000, 6.8)
    V = 150.0

    def midA(t):
        dx = -V * t
        o = ""
        k = P(turn=-0.3, gx=-0.6, gy=-0.3, furrow=0.4, brow=0.3, smile=0.2, armR="fist_up", propR="kaviani", armL="relaxed", legs="walk",
              phase=t * 5.5, blink=blink_at(t, 61), wind=0.6)
        o += at_feet(KAVEH_NOAPRON, k, t, 1720 + dx, 1330, 0.25, flip=False)
        sq = P(turn=-0.3, gx=-0.6, gy=-0.2, furrow=0.6, armL=(20, 10), propL="pike", armR="relaxed", legs="walk", phase=t * 5.5 + 1,
               blink=blink_at(t, 62), wind=0.5)
        o += at_feet(FSOLDIER, sq, t, 930 + dx, 1325, 0.24)
        zq = P(turn=-0.2, gx=-0.4, gy=0.6, furrow=0.9, brow=0.4, sad=0.6, armL=("ik", 60, 330), armR=("ik", -60, 330), chains="rope",
               snake_rise=0.6, snake_looks=(-0.6 + 0.2 * math.sin(t), -0.5 + 0.2 * math.sin(t * 1.3)), blink=blink_at(t, 63), wind=0.6)
        o += camel_rider(ZAHHAK_BARE, zq, t, 1270 + dx, 1400, 0.8, flip=True, walk=True, rate=4.2)
        fqq = P(turn=-0.4, gx=-0.6, gy=-0.4, armR="forward", armL=("ik", 230, 120), propL="mace", furrow=0.7, brow=0.2, blink=blink_at(t, 64), wind=0.7)
        o += rider(FEREYDUN, fqq, t, lambda c: golrang(c, t, walk=True, phase=t * 4.2), 420 + dx, 1385, 0.8, flip=True)
        return o
    A = Shot(6.8, road, midA, cam=camA, light=DUSKD, sun=SUN_DUSKD, fade_in=0.5,
             fx=[Motes(40, 601, (255, 220, 190), (0, 300, W, 1300), (-10, -4), amax=90)])

    # B: inside the cave: Zahhak chained to the rock; Fereydun in the mouth
    cave = bg("cave_in", zbg.cave_in)
    camB = cam_push(1.0, 1.05, 420, 1000, 6.0)
    RINGS = [(20, 1150), (470, 1120)]
    PULLS = [c - 101.2 for c in A10.CHAINS]

    def midB(t):
        pull = sum(ease((t - p) / 0.25) for p in PULLS) / len(PULLS)
        defeat = ease((t - 3.8) / 1.2)
        zq = P(legs="sit", turn=0.25, gx=0.6 - 0.8 * defeat, gy=-0.1 + 0.8 * defeat, furrow=1.2 - 0.8 * defeat, brow=-0.3 + 0.9 * defeat,
               sad=0.7 * defeat, armL=("ik", lerp(280, 330, pull), 420, "down"), armR=("ik", lerp(-280, -330, pull), 420, "down"), blink=blink_at(t, 65),
               snake_rise=0.8 - 0.3 * defeat, snake_looks=(0.4 - 0.9 * defeat, 0.4 - 0.9 * defeat),
               hisses=(0.4 * (1 - defeat) * max(0.0, math.sin(t * 3)), 0.4 * (1 - defeat) * max(0.0, math.sin(t * 2.6 + 1))), wind=0.2)
        from p05_scenes import hand_at
        o = ""
        hands = [hand_at(ZAHHAK_BARE, zq["armL"], 1, 210, 1000, 0.6, neck=True), hand_at(ZAHHAK_BARE, zq["armR"], -1, 210, 1000, 0.6, neck=True)]
        for (rx, ry), (hx, hy) in zip(RINGS[::-1], hands):
            o += (f'<circle cx="{rx}" cy="{ry}" r="22" fill="none" stroke="#2a2a30" stroke-width="13"/><circle cx="{rx}" cy="{ry}" r="22" fill="none" stroke="#8a8e98" stroke-width="7"/>'
                  f'<path d="M {rx} {ry + 20} Q {(rx + hx) / 2:.1f} {max(ry, hy) + 50 * (1 - pull):.1f} {hx:.1f} {hy:.1f}" stroke="#a8acb6" stroke-width="11" '
                  f'fill="none" stroke-dasharray="14 6"/>')
        body = at_neck(ZAHHAK_BARE, zq, t, 210, 1000, 0.6)
        fqq = P(turn=-0.35, gx=-0.8, gy=0.1, furrow=0.8, brow=0.1, armR="relaxed", armL=("ik", 200, 300), propL="mace", blink=blink_at(t, 66), wind=0.5)
        return body + o + at_feet(FEREYDUN, fqq, t, 600, 1318, 0.38)
    B = Shot(6.0, cave, midB, cam=camB, light=CAVE, grade="warm", bloom=0.6,
             fx=[Motes(40, 602, (255, 220, 190), (300, 600, 800, 1400), (-4, -6), amax=80)])

    # C: Fereydun in the mouth of the cave: "Here you will stay, far from the people you hurt."
    caveb = bg("cave_in", zbg.cave_in, 6)
    LC = [("p10s6c", 0.2)]
    camC = cam_push(1.0, 1.04, 540, 860, 4.2)

    def midC(t):
        q = fq(LC, t, 6, turn=-0.3, gx=-0.8, gy=0.3, furrow=0.9, brow=0.1, armL=("ik", 200, 300), propL="mace", armR="relaxed", wind=0.5)
        return at_neck(FEREYDUN, q, t, 560, 1000, 1.0)
    C = Shot(4.2, caveb, midC, cam=camC, light=dict(ambient=(0.66, 0.62, 0.72), rim_point=(560, 7), rim_col=(1.0, 0.72, 0.45), rim_str=1.0),
             grade="warm", bloom=0.6)

    # D: the mountain at night
    dn = bg("damavand_night", lambda: zbg.damavand("night"))
    D = Shot(6.2, dn, None, cam=cam_push(1.0, 1.1, 610, 700, 6.2), fx=[Motes(50, 603, (220, 230, 255), (0, 200, W, 1300), (-8, 3), amax=80)],
             grade="night", bloom=0.6, fade_out=0.9)
    return [A, B, C, D]


# ================================================================ S7 the crown; the fires of Mehregan; the banner (117.6-152.0)
def s7():
    from p03_scenes import nobles as court_nobles
    court = bgs.cached("zh_jamshid_hall_court", jamshid_court)
    closej = bg("jamshid_hall_close", zbg.jamshid_hall_close)
    closejb = bg("jamshid_hall_close", zbg.jamshid_hall_close, 5)
    # A: "On the first day of the month of Mehr, Fereydun put on the crown."
    camA = cam_push(1.0, 1.07, 540, 1050, 5.6)
    hx, hy = head_of(540, 793, 0.36)

    def midA(t):
        f = tp([], t, 1, legs="sit", turn=0.0, gx=0.0, gy=0.2, smile=0.4, brow=0.3, furrow=-0.1, armL=("ik", 200, 300), propL="mace", armR="relaxed",
               wind=0.05, cloak_len=0.6)
        fa = P(turn=0.35, gx=0.8, gy=-0.5, smile=0.6, sad=0.2, brow=0.5, armL="chest", armR="relaxed", blink=blink_at(t, 71))
        k = P(turn=-0.35, gx=-0.8, gy=-0.6, smile=0.5, brow=0.4, armR="fist_up", propR="kaviani", armL="relaxed", blink=blink_at(t, 72), wind=0.3)
        return (braziers(t) + at_neck(FEREYDUN_KING, f, t, 540, 793, 0.36) + at_feet(FARANAK, fa, t, 250, 1430, 0.34) +
                at_feet(KAVEH_NOAPRON, k, t, 845, 1440, 0.34))
    A = Shot(5.6, court, midA, cam=camA, light=DAYHALL, sun=SUNTOP, fade_in=0.5,
             pre_fx=[svg_fx(camA, lambda t: farr_svg(hx, hy, 70, t, ease((t - 0.6) / 1.2)), par=0.6)],
             fx=[Motes(50, 701, (255, 236, 190), (0, 300, W, 1500), (6, -6), amax=90)])

    # B: Faranak: "My son… your father would be so proud of you."
    LB = [("p10s7b", 0.2)]
    camB = cam_push(1.0, 1.04, 540, 860, 4.4)

    def midB(t):
        q = tp(LB, t, 2, turn=0.2, gx=0.5, gy=-0.4, smile=0.55, sad=0.35, brow=0.5, furrow=-0.3, armL="chest", armR="relaxed", wind=0.2)
        return at_neck(FARANAK, q, t, 540, 960, 1.0)
    B = Shot(4.4, closejb, midB, cam=camB, light=DAYCLOSE, sun=SUNTOP, bloom=0.6)

    # C: Fereydun crowned: "From today, no one in this land will live in fear."
    LC = [("p10s7c", 0.2)]
    camC = cam_push(1.0, 1.05, 540, 860, 4.6)
    chx, chy = head_of(540, 1030, 1.0)

    def midC(t):
        q = fq(LC, t, 3, turn=0.0, gx=0.1, gy=0.0, furrow=0.2, brow=0.3, smile=0.3, armL=("ik", 200, 300), propL="mace", armR="relaxed", wind=0.15)
        return at_neck(FEREYDUN_KING, q, t, 540, 1030, 1.0)
    C = Shot(4.6, closej, midC, cam=camC, light=DAYCLOSE, sun=SUNTOP, bloom=0.6,
             pre_fx=[svg_fx(camC, lambda t: farr_svg(chx, chy, 190, t, 0.8), par=1.0)])

    # D: the fires of Mehregan
    dn = bg("damavand_night", lambda: zbg.damavand("night"))
    far = [(120, 1150, 16), (330, 1135, 12), (470, 1160, 18), (690, 1140, 14), (880, 1165, 20), (1010, 1150, 15), (600, 1215, 28), (200, 1230, 32),
           (960, 1240, 30)]
    dancers = Cheering(705, [(130, 1390, 0.26), (470, 1395, 0.26), (210, 1405, 0.27), (400, 1410, 0.27), (640, 1335, 0.21), (735, 1340, 0.21),
                             (960, 1345, 0.22), (1040, 1400, 0.26), (560, 1405, 0.26)])
    heads = bgs.cached("zh_p10_fire_heads", lambda: back_heads(1705, 8, 1780, 0.6, col="#0c0810", blur=3))
    camD = cam_push(1.0, 1.05, 540, 1100, 6.0)

    def midD(t):
        o = "".join(fire_svg(x, y, sz, t + k, seed=k) for k, (x, y, sz) in enumerate(far))
        o += fire_svg(850, 1330, 60, t + 0.5, seed=12)
        o += dancers.svg(t, cheer=1.0, look=(300, 1200))
        return o + fire_svg(300, 1430, 120, t, seed=11)
    D = Shot(6.0, dn, midD, fg=heads, cam=camD, light=FIREN, grade="fire", bloom=0.7, fade_in=0.4,
             fx=[Glow(lambda t: cam_xy(camD, t, 300, 1300), 380, (255, 160, 80), 0.5), Glow(lambda t: cam_xy(camD, t, 850, 1270), 240, (255, 160, 80), 0.4),
                 Embers(60, 703, (160, 850, 460, 1400), (60, 170)), Embers(25, 704, (790, 950, 910, 1320), (50, 130))])

    # E: Kaveh by the fire: "The snake king is gone! We are free!"
    dnb = bg("damavand_night", lambda: zbg.damavand("night"), 6)
    LE = [("p10s7e", 0.1)]
    camE = cam_push(1.0, 1.05, 540, 860, 3.2)

    def midE(t):
        q = kaveh_q(LE, t, 7, turn=0.1, gx=0.2, gy=-0.2, furrow=-0.2, brow=0.6, smile=0.6, armR=("ik", -300, 60), propR="kaviani",
                    armL="fist_up" if t > 0.3 else "relaxed", wind=0.7)
        return at_neck(KAVEH_NOAPRON, q, t, 580, 980, 0.95)
    E = Shot(3.2, dnb, midE, cam=camE, light=dict(FIREN, point=(0, 1100, 900, 0.6, 1.2, (1.0, 0.55, 0.25)), rim_point=(0, 6)), grade="fire", bloom=0.6,
             fx=[Glow(lambda t: (40, 1150), 380, (255, 150, 70), 0.5), Embers(40, 705, (0, 700, 300, 1300), (60, 160))])

    # F: the Kaviani banner over a free land; the end card from 5.2
    dusk = bg("damavand_dusk", lambda: zbg.damavand("dusk"))
    camF = cam_push(1.0, 1.06, 540, 800, 10.6)

    def midF(t):
        return big_banner(540, 1230, 1.05, t + 2.0, ang=2 * math.sin(t * 0.8)) + banner_glints(t, 540, 1230, 1.05, t0s=(0.8, 2.0, 3.4, 4.6, 6.2, 7.8))
    F = Shot(10.6, dusk, midF, cam=camF, light=dict(DUSKD, ramp=None), sun=(170, 1030, 900, (0.14, 0.09, 0.05)),
             fx=[Motes(50, 706, (255, 230, 200), (0, 200, W, 1300), (-10, -6), amax=100)], bloom=0.7, fade_in=0.3, fade_out=0.8)
    return [A, B, C, D, E, F]


SCENES = {"s1": s1, "s2": s2, "s3": s3, "s4": s4, "s5": s5, "s6": s6, "s7": s7}
