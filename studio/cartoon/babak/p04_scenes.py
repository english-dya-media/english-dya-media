"""Part 4 · The Ambush (episode 2, half 2) — 2D cartoon. Timing matches p04_audio.py:
s1 0-21 the rockslide at Hashtadsar (hook) · s2 21-25.6 title · s3 25.6-50.2 the feast at Bazz · s4 50.2-66 al-Ma'mun's tent, 833 ·
s5 66-89.4 Baghdad, 835: Afshin · s6 89.4-108 the fires on the plain."""
import math, random
from PIL import Image, ImageFilter, ImageDraw, ImageEnhance
from film import Shot, W, H, ease, lerp, talk_pose, blink_at, cam_push, cam_static, Snow, Motes, Embers, svg_render
from chars import pose, horse, Ctx, FEET, fmt
from stage import at_neck, at_feet, lying_at, crowd_row, back_heads, fire_svg, rider, Glow, lw_for, random_spec
import bgs, wallbg
from cast import *
from p01_scenes import P, blur_bg, WARM
from p02_scenes import banner_svg, birds, bazz_shot
from p03_scenes import NOON, NOON_SUN, enemy_spec, column, red_cloth, villager_spec, pole_flag, sil, dust, DUSTDEF

FIRE = dict(point=(540, 1420, 900, 0.45, 1.2, (1.0, 0.55, 0.25)), rim_point=(540, 6), rim_col=(1.0, 0.65, 0.3))
LAMP = dict(point=(860, 760, 900, 0.4, 1.15, (1.0, 0.6, 0.3)), rim_point=(860, 5), rim_col=(1.0, 0.7, 0.4), rim_str=0.6)
GOLD = dict(rim=(0, -4), rim_col=(1.0, 0.85, 0.55), ramp=(0, W, 0.95, 1.02), ambient=(1.02, 0.96, 0.86))
MOON = dict(ambient=(0.55, 0.62, 0.9), rim=(-4, -3), rim_col=(0.75, 0.82, 1.0), rim_str=0.6)


def arrows(t, seed=0, n=6, box=(0, 300, W, 1300)):
    r = random.Random(seed); o = ""
    for k in range(n):
        ph = r.uniform(0, 1); sp = r.uniform(1.4, 2.2); y0 = r.uniform(box[1], box[3]); d = r.choice([-1, 1])
        u = (t * sp + ph) % 1.0
        x = -200 + u * (W + 400) if d > 0 else W + 200 - u * (W + 400)
        y = y0 + 120 * u
        o += f'<path d="M {x:.0f} {y:.0f} l {-90 * d:.0f} {-12:.0f}" stroke="#2a1a10" stroke-width="5" stroke-linecap="round"/><path d="M {x:.0f} {y:.0f} l {-14 * d:.0f} -8 l 0 16 Z" fill="#cfd4da"/>'
    return o


def dust_layer(t, a=1.0, seed=0, y0=900, y1=1700, n=10):
    r = random.Random(seed); o = DUSTDEF
    for k in range(n):
        x = (r.uniform(-200, 1300) + r.uniform(30, 80) * t) % 1500 - 200
        y = r.uniform(y0, y1); rad = r.uniform(120, 260)
        o += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{rad:.0f}" fill="#c8b090" opacity="{0.35 * a:.2f}" filter="url(#dustblur)"/>'
    return o


# ================================================================ S1 the rockslide (0-21)
def s1():
    cu = bgs.cached("cliff_up", bgs.cliff_up)
    rr = random.Random(71)
    rocks = [(rr.uniform(120, 960), 0.1 + 0.35 * k, rr.uniform(40, 70), rr.uniform(-1, 1)) for k in range(8)]
    def midA(t):
        o = DUSTDEF
        for k in range(5):
            x = 140 + 200 * k
            a = ease((t - 0.1 * k) / 0.6)
            o += f'<circle cx="{x}" cy="{600 - 40 * a:.0f}" r="{60 + 120 * a:.0f}" fill="#d8c0a0" opacity="{0.5 * a:.2f}" filter="url(#dustblur)"/>'
        for k, (x0, t0, rad, drift) in enumerate(rocks):
            a = t - t0
            if a < 0:
                continue
            y = 590 + 250 * a + 700 * a * a; grow = 1 + 1.6 * a
            o += bgs.boulder(x0 + drift * 140 * a, y, rad * grow, 300 + k, "#6a4c36", "#3a2818", "#c89a6a", rot=t * 300 * (1 if drift > 0 else -1))
        return o
    shake = lambda t: (1.0 + 0.04 * ease(t / 3.6), 540, 800, 9 * math.sin(t * 43), 7 * math.sin(t * 31))
    A = Shot(3.6, cu, midA, cam=shake, light=dict(rim=(0, 0)), sun=(560, 300, 700, (0.14, 0.12, 0.08)),
             fx=[Motes(80, 72, (220, 200, 170), (0, 500, W, 1500), (10, 60), (2, 5), 140)])
    fb = blur_bg("gorge_floor_noon", lambda: bgs.gorge_floor("noon"), 8)
    LB = [("p4s1a", 0.6)]
    def midB(t):
        q = talk_pose(LB, t, 101, dict(turn=0.1, gx=-0.4, gy=-0.3, furrow=1.0, brow=-0.4, wind=1.0, armL="fist_up", propL=("sword", 180), armR="relaxed"))
        q["mouth_o"] = max(q["mouth_o"], 0.25 if t < 2.2 else 0.0)
        o = dust_layer(t, 0.8, 73, 300, 1600, 8) + arrows(t, 74, 5)
        o += at_neck(MUHAMMAD, P(**q), t, 540, 1080, 1.1)
        return o
    dust_tex = bgs.cached("dust_tex", lambda: svg_render("".join(
        f'<circle cx="{random.Random(i).uniform(-100, 1180):.0f}" cy="{random.Random(i + 70).uniform(-100, 2020):.0f}" r="{random.Random(i + 9).uniform(150, 320):.0f}" fill="#cdb594" opacity="0.8"/>'
        for i in range(40))).filter(ImageFilter.GaussianBlur(40)))
    def cover(im, t):
        a = ease((t - 2.0) / 0.9)
        if a > 0:
            layer = dust_tex.copy(); layer.putalpha(dust_tex.getchannel("A").point(lambda v: int(v * a)))
            im.alpha_composite(Image.new("RGBA", (W, H), (205, 181, 148, int(200 * a))))
            im.alpha_composite(layer)
    B = Shot(3.6, fb, midB, cam=lambda t: (1.04, 540, 900, 6 * math.sin(t * 37), 4 * math.sin(t * 29)), light=NOON, sun=NOON_SUN, fx=[cover])
    floor = bgs.cached("gorge_floor_noon", lambda: bgs.gorge_floor("noon"))
    walls = bgs.cached("gorge_walls_noon", lambda: bgs.gorge_walls("noon"))
    r = random.Random(75)
    runners = [(enemy_spec(r), r.uniform(200, 1200), r.choice([1330, 1420, 1500]), r.uniform(0.25, 0.33), r.uniform(0, 6)) for _ in range(7)]
    def midC(t):
        o = dust_layer(t, 0.6, 76, 900, 1500, 7)
        rear = ease(t / 0.6) * (1 - ease((t - 2.4) / 0.6))
        c = Ctx(lw_for(0.7))
        o += (f'<g transform="rotate({28 * rear:.1f},860,1470)"><g transform="translate(700,1470) scale(-0.62,0.62)">'
              f'{horse(c, col="#6a4428", mane="#1a100a", t=t, head_bob=-60 * rear, saddle=True, blanket="#121216")}</g></g>')
        for S, x0, y, sc, ph in sorted(runners, key=lambda v: v[2]):
            x = x0 - 260 * t
            q = P(legs="walk", phase=t * 11 + ph, turn=-0.45, gx=-0.8, gy=0.0, brow=0.8, furrow=-0.5, mouth_o=0.4, armL="relaxed", armR=("ik", -300, 100), wind=0.8)
            o += at_feet(S, q, t, x, y, sc)
        fall = ease((t - 1.0) / 1.4)
        o += f'<g transform="rotate({-70 * fall:.1f},560,1480)">' + pole_flag(t, 560, 1480 - 520, 520, 200, 120) + '</g>'
        return o + arrows(t, 77, 6, (0, 500, W, 1300))
    C = Shot(3.8, floor, midC, fg=walls, cam=lambda t: (1.03, 540, 1250, 5 * math.sin(t * 31), 3 * math.sin(t * 23)), light=NOON, sun=NOON_SUN)
    st = bgs.cached("stream", bgs.stream_bg)
    def midD(t):
        o = ""
        for k in range(14):
            x = (k * 97 + 120 * t) % 1200 - 60; y = 1270 + (k * 53) % 280
            o += f'<path d="M {x:.0f} {y:.0f} q 30 -8 60 0" stroke="#a8c8d8" stroke-width="4" fill="none" opacity="0.6"/>'
        x = 300 + 80 * t; y = 1400 + 5 * math.sin(t * 3)
        sink = ease((t - 1.4) / 1.8)
        wv = [(x - 20 + 30 * k, y + 8 * math.sin(t * 4 + k)) for k in range(9)]
        flag = "M " + " L ".join(f"{a:.0f} {b:.0f}" for a, b in wv) + " L " + " L ".join(f"{a + 10:.0f} {b + 46:.0f}" for a, b in wv[::-1]) + " Z"
        o += (f'<g opacity="{1 - 0.75 * sink:.2f}"><path d="M {x - 260:.0f} {y + 30:.0f} L {x - 10:.0f} {y + 6:.0f}" stroke="#3a2414" stroke-width="9"/>'
              f'<circle cx="{x - 262:.0f}" cy="{y + 30:.0f}" r="9" fill="#c9a24a"/><path d="{flag}" fill="#121216" stroke="#000" stroke-width="2"/></g>')
        a = (t * 0.7) % 1.0
        o += f'<ellipse cx="{x + 100:.0f}" cy="{y + 26:.0f}" rx="{120 + 200 * a:.0f}" ry="{18 + 30 * a:.0f}" fill="none" stroke="#d8e8f0" stroke-width="4" opacity="{0.7 * (1 - a):.2f}"/>'
        return o
    D = Shot(3.2, st, midD, cam=cam_push(1.0, 1.06, 560, 1300, 3.2), light=dict(rim=(0, 0)), sun=(800, 300, 800, (0.08, 0.06, 0.03)),
             fx=[Motes(40, 78, (230, 210, 180), (0, 400, W, 1300), (12, -6), amax=90)])
    rvb = blur_bg("ridge_view", bgs.ridge_view, 8)
    LE = [("p4s1b", 0.4)]
    def midE(t):
        o = ""
        for k, (x, y, sc) in enumerate([(150, 1260, 0.34), (930, 1250, 0.33), (300, 1230, 0.3), (800, 1225, 0.3)]):
            up = ease((t - 2.4 - 0.15 * k) / 0.5)
            q = P(turn=0.2, gx=0.3, gy=-0.3, smile=0.5 * up, armL=("ik", 320, lerp(560, -470, up)), propL="spear_red", armR="relaxed", wind=0.6)
            o += at_feet(FIGHTER2 if k % 2 else FIGHTER, q, t + k, x, y + FEET * sc, sc)
        q = talk_pose(LE, t, 102, dict(turn=0.15, gx=0.3, gy=0.0, brow=0.5, smile=0.5 * ease((t - 2.4) / 0.6), wind=0.7, armL="fist_up" if t > 0.3 else "relaxed", armR="relaxed"))
        q["mouth_o"] = max(q["mouth_o"] * 1.2, 0.0)
        return o + at_neck(FIGHTER, P(**q), t, 540, 1070, 1.2)
    E = Shot(4.8, rvb, midE, cam=cam_push(1.0, 1.05, 540, 900, 4.8), light=dict(rim=(5, -2), rim_col=(1.0, 0.82, 0.55)), sun=(880, 760, 700, (0.12, 0.07, 0.03)))
    rv = bgs.cached("ridge_view", bgs.ridge_view)
    def midF(t):
        o = dust_layer(t, 0.5, 79, 1150, 1350, 6)
        for k, (x, y, sc) in enumerate([(110, 1330, 0.3), (260, 1300, 0.27), (420, 1320, 0.29), (640, 1300, 0.27), (800, 1325, 0.3), (960, 1305, 0.28)]):
            q = P(turn=0.1, gx=0.2, gy=-0.2, smile=0.5, armL=("ik", 320, -470 + 40 * math.sin(t * 6 + k)), propL="spear_red", armR="fist_up" if k % 2 else "relaxed", wind=0.7)
            o += at_feet(FIGHTER2 if k % 2 else FIGHTER, q, t + k, x, y + FEET * sc * 0.0, sc)
        return o
    F = Shot(2.0, rv, midF, cam=cam_push(1.0, 1.04, 540, 1100, 2.0), light=dict(rim=(5, -2), rim_col=(1.0, 0.82, 0.55)), sun=(880, 760, 700, (0.12, 0.07, 0.03)), fade_out=0.6)
    return [A, B, C, D, E, F]


# ================================================================ S2 title over Bazz at dusk (21-25.6)
def s2():
    return [bazz_shot(4.6, "dusk", 30, fade_in=0.4, fade_out=0.5)]


# ================================================================ S3 the feast at Bazz (25.6-50.2)
def dancers(t, seed=81, n=8, cx=540, cy=1440, rx=420, ry=150, s0=0.31, front=None):
    r = random.Random(seed); o_back, o_front = "", ""
    specs = [(DANCER_W if k % 2 else villager_spec(r, red=True)) for k in range(n)]
    for k in range(n):
        th = 2 * math.pi * k / n + 0.55 * t
        x = cx + rx * math.cos(th); y = cy + ry * math.sin(th); sc = s0 + 0.08 * math.sin(th)
        d = -math.sin(th)          # moving direction on screen (counter-clockwise seen from above)
        q = P(legs="walk", phase=t * 7 + k, turn=0.4 * (1 if d > 0 else -1), gx=0.6 * (1 if d > 0 else -1), smile=0.6, wind=0.5,
              armL=("ik", 470, -280 + 50 * math.sin(t * 7 + k)), armR=("ik", -470, -280 + 50 * math.sin(t * 7 + k + 1)))
        svg = at_feet(specs[k], q, t + k, x, y, sc)
        if math.sin(th) < 0:
            o_back += svg
        else:
            o_front += svg
    return o_back, o_front


def s3():
    fn = bgs.cached("feast_night", bgs.feast_night)
    def midA(t, k0=1.0):
        back, front = dancers(t)
        return back + fire_svg(540, 1440, 150, t) + front
    A = Shot(7.0, fn, midA, cam=cam_push(1.0, 1.06, 540, 1300, 7.0), light=FIRE, fx=[Embers(70, 82, (420, 1000, 660, 1440), (80, 200))], grade="fire", bloom=0.7, fade_in=0.4)
    def strum(tt):
        return ("ik", -60 + 14 * math.sin(tt * 9), 360)
    LB1 = [("p4s3a", 0.8), ("p4s3b", 3.3)]
    def midB1(t):
        o = fire_svg(90, 1420, 110, t)
        b = talk_pose([], t, 83, dict(turn=0.3, gx=0.6, gy=0.3 if t < 2.4 else -0.1, smile=0.3 + 0.3 * ease((t - 4.2) / 0.8), legs="sit", armR=strum(t), armL=("ik", 210, 20), propR="tanbur"))
        n = talk_pose(LB1, t, 84, dict(turn=-0.35, gx=-0.8, gy=0.1, smile=0.6, brow=0.2, legs="sit", armL="relaxed", armR="chest"))
        o += at_neck(BABAK_LEADER, P(**b), t, 380, 960, 0.7) + at_neck(BANU, P(**n), t, 790, 975, 0.66)
        return o
    fnb = blur_bg("feast_night", bgs.feast_night, 8)
    B1 = Shot(5.8, fnb, midB1, cam=cam_push(1.0, 1.05, 580, 1150, 5.8), light=dict(point=(110, 1400, 1000, 0.5, 1.15, (1.0, 0.55, 0.25)), rim_point=(110, 6), rim_col=(1.0, 0.65, 0.3)),
              fx=[Embers(30, 83, (40, 1300, 200, 1500), (60, 160))], grade="fire")
    LB2 = [("p4s3c", 0.5), ("p4s3d", 2.5)]
    def midB2(t):
        b = talk_pose(LB2, t, 85, dict(turn=0.25, gx=0.5, gy=0.0, smile=0.35, brow=0.1, armR=strum(t), armL=("ik", 240, 100), propR="tanbur"))
        return at_neck(BABAK_LEADER, P(**b), t, 560, 1060, 1.2)
    B2 = Shot(5.6, fnb, midB2, cam=cam_push(1.0, 1.05, 560, 880, 5.6), light=dict(point=(60, 1300, 1100, 0.5, 1.15, (1.0, 0.55, 0.25)), rim_point=(60, 6), rim_col=(1.0, 0.65, 0.3)),
              grade="fire")
    def midC(t):
        back, front = dancers(t + 7.0, rx=430, ry=130, s0=0.4, cy=1470)
        return back + fire_svg(540, 1480, 170, t) + front
    C = Shot(6.2, fn, midC, cam=cam_push(1.06, 1.0, 540, 1350, 6.2), light=FIRE, fx=[Embers(90, 86, (400, 900, 680, 1480), (90, 220))], grade="fire", bloom=0.8, fade_out=0.9)
    return [A, B1, B2, C]


# ================================================================ S4 al-Ma'mun's tent, 833 (50.2-66)
def bed_front(x0=140, x1=840, y=1180):
    return (f'<rect x="{x0 - 20}" y="{y}" width="{x1 - x0 + 40}" height="110" fill="#4a2a18" stroke="#140a04" stroke-width="5"/>'
            f'<path d="M {x0 - 20} {y + 20} L {x1 + 20} {y + 20}" stroke="#c9a24a" stroke-width="6"/>'
            f'<rect x="{x0 - 30}" y="{y + 100}" width="{x1 - x0 + 60}" height="30" fill="#2a1408" stroke="#140a04" stroke-width="4"/>')


def sweat(x, y, s, t):
    return "".join(f'<path d="M {x + dx * s:.1f} {y + (dy + 6 * ((t * 0.6 + k * 0.3) % 1)) * s:.1f} q {4 * s:.1f} {9 * s:.1f} 0 {12 * s:.1f} q {-4 * s:.1f} {-3 * s:.1f} 0 {-12 * s:.1f} Z" fill="#d8f0ff" opacity="0.8"/>'
                   for k, (dx, dy) in enumerate([(-60, -250), (50, -236), (-84, -200)]))


def s4():
    tn = bgs.cached("tent_interior", bgs.tent_interior)
    pillow = '<rect x="170" y="1010" width="300" height="140" rx="60" fill="#d8ccb4" stroke="#1b0f0a" stroke-width="4"/>'
    def midA(t):
        m = P(blink=0.6, sad=0.4, furrow=-0.2, armL="relaxed", armR="relaxed", turn=0.2, gx=0.4, gy=0.0)
        o = '<rect x="160" y="1080" width="200" height="90" rx="40" fill="#d8ccb4" stroke="#1b0f0a" stroke-width="4"/>'
        o += lying_at(MAMUN, P(**m), t, 560, 1185, 0.42)
        o += '<path d="M 330 1110 C 430 1060, 800 1060, 860 1100 L 860 1190 L 330 1190 Z" fill="#3a1e18" stroke="#1b0f0a" stroke-width="3"/>'
        o += '<path d="M 335 1125 C 440 1080, 790 1080, 855 1118" stroke="#c9a24a" stroke-width="6" fill="none"/>'
        o += bed_front(140, 860, 1185)
        k = P(turn=-0.4, gx=-0.8, gy=0.4, sad=0.2, furrow=0.6, legs="sit", armR=("ik", -420, 260), armL="relaxed")
        o += at_neck(MUTASIM, k, t, 820, 1040, 0.56)
        return o
    A = Shot(4.4, tn, midA, cam=cam_push(1.0, 1.06, 520, 1100, 4.4), light=LAMP, grade="fire", fade_in=0.6, sun=(860, 760, 600, (0.10, 0.05, 0.02)))
    tb = blur_bg("tent_interior", bgs.tent_interior, 9)
    pillow2 = '<rect x="250" y="800" width="580" height="260" rx="110" fill="#d8ccb4" stroke="#1b0f0a" stroke-width="4"/>'
    blanket = bgs.cached("blanket_fg4", lambda: svg_render('<path d="M -40 1330 C 200 1290, 800 1280, 1120 1320 L 1120 1920 L -40 1920 Z" fill="#3a1e18" stroke="#1b0f0a" stroke-width="5"/>'
                                                           '<path d="M -40 1360 C 200 1320, 800 1310, 1120 1350" stroke="#c9a24a" stroke-width="10" fill="none"/>'))
    LB = [("p4s4a", 0.4), ("p4s4b", 3.0)]
    def midB(t):
        m = talk_pose(LB, t, 103, dict(turn=0.15, gx=0.5, gy=0.0, sad=0.5, furrow=-0.3, brow=0.3, armL="relaxed", armR="relaxed"))
        m["blink"] = max(0.35, m["blink"]); m["mouth_o"] *= 0.75
        return pillow2 + at_neck(MAMUN, P(**m), t, 540, 1150, 1.22) + sweat(540, 1150, 1.22, t)
    B = Shot(6.0, tb, midB, fg=blanket, cam=cam_push(1.0, 1.05, 540, 900, 6.0), light=dict(rim=(5, -2), rim_col=(1.0, 0.65, 0.35), ramp=(0, W, 0.72, 1.08)),
             sun=(1000, 900, 600, (0.10, 0.05, 0.02)), grade="fire")
    LC = [("p4s4c", 0.6)]
    OUT_T = 3.0
    def midC(t):
        k = talk_pose(LC, t, 104, dict(turn=-0.2, gx=-0.4, gy=0.4, furrow=1.0, brow=-0.3, armL="relaxed", armR="relaxed"))
        return at_neck(MUTASIM, P(**k), t, 540, 1060, 1.2)
    def dark(im, t):
        if t >= OUT_T:
            d = ImageDraw.Draw(im, "RGBA")
            for k in range(6):
                age = t - OUT_T - k * 0.18
                if age > 0:
                    y = 760 - age * 60 - k * 6; x = 1000 + 12 * math.sin(age * 2.2 + k); rr = 5 + age * 6
                    d.ellipse((x - rr, y - rr, x + rr, y + rr), fill=(150, 140, 135, int(max(0, 60 - age * 18))))
            im.alpha_composite(Image.new("RGBA", (W, H), (0, 0, 0, int(255 * min(0.65, (t - OUT_T) * 0.8)))))
    C = Shot(5.4, tb, midC, cam=cam_push(1.0, 1.05, 540, 880, 5.4), light=dict(rim=(5, -2), rim_col=(1.0, 0.65, 0.35), ramp=(0, W, 0.72, 1.08)),
             sun=(1000, 760, 500, (0.12, 0.06, 0.02)), fx=[dark], grade="fire", fade_out=1.0)
    return [A, B, C]


# ================================================================ S5 Baghdad, 835: Afshin (66-89.4)
def chest(x, y, s=1.0, open_=0.0):
    w, h = 170 * s, 110 * s
    o = (f'<rect x="{x - w / 2:.1f}" y="{y - h:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{8 * s:.1f}" fill="#5a3418" stroke="#1b0f0a" stroke-width="{4 * s:.1f}"/>'
         f'<path d="M {x - w / 2:.1f} {y - h * 0.55:.1f} L {x + w / 2:.1f} {y - h * 0.55:.1f}" stroke="#c9a24a" stroke-width="{7 * s:.1f}"/>'
         f'<rect x="{x - 12 * s:.1f}" y="{y - h * 0.7:.1f}" width="{24 * s:.1f}" height="{26 * s:.1f}" fill="#c9a24a" stroke="#1b0f0a" stroke-width="{2 * s:.1f}"/>')
    o += "".join(f'<circle cx="{x + dx * s:.1f}" cy="{y - h - 6 * s + dy * s:.1f}" r="{9 * s:.1f}" fill="#e8ecf2" stroke="#7a7e88" stroke-width="{1.5 * s:.1f}"/>' for dx, dy in [(-50, 0), (-20, -6), (10, 0), (40, -4), (-35, -12), (25, -12)])
    return o


def s5():
    gh = bgs.cached("gold_hall", bgs.gold_hall)
    def midA(t):
        o = ""
        k = P(turn=0.0, gx=-0.4, gy=0.3, furrow=0.6, legs="sit", armL="relaxed", armR="relaxed")
        o += at_neck(MUTASIM, k, t, 540, 1170 - 575 * 0.42, 0.42)
        a = P(turn=0.45, gx=0.8, gy=-0.2, furrow=0.3, legs="sit", armL="chest", armR="chest", nod=8)
        o += at_neck(AFSHIN, a, t, 360, 1560 - 575 * 0.5, 0.5)
        for k2, (x0, y, d) in enumerate([(1200, 1500, 0.0), (1260, 1600, 0.9)]):
            u = ease((t - d) / 2.4); x = lerp(x0, 820 - 90 * k2, u)
            walking = u < 1
            q = P(legs="walk" if walking else "stand", phase=t * 6, turn=-0.4, gx=-0.7, armL=("ik", 150, 330), armR=("ik", -150, 330), furrow=0.2)
            o += at_feet(SERVANT, q, t, x, y, 0.42) + chest(x, y - (FEET - 330) * 0.42 + 60, 0.42 * 1.6)
        return o
    A = Shot(5.0, gh, midA, cam=cam_push(1.0, 1.05, 540, 1250, 5.0), light=GOLD, sun=(540, 900, 900, (0.12, 0.09, 0.03)), bloom=0.7, fade_in=0.6,
             fx=[Motes(60, 91, (255, 230, 170), (200, 300, 880, 1300), (4, -6), amax=110)])
    ghb = blur_bg("gold_hall", bgs.gold_hall, 8)
    LB = [("p4s5a", 0.4), ("p4s5b", 3.8), ("p4s5c", 6.4)]
    def midB(t):
        give = ease((t - 7.9) / 0.6)
        k = talk_pose(LB, t, 105, dict(turn=0.25, gx=0.4, gy=0.2, furrow=0.7, brow=-0.1, armR="relaxed",
                                      armL=("ik", lerp(200, 380, give), lerp(420, 300, give)) if t > 7.6 else "relaxed", propL="banner_black" if t > 7.6 else None))
        return at_neck(MUTASIM, P(**k), t, 520, 1010, 1.0)
    B = Shot(9.4, ghb, midB, cam=cam_push(1.0, 1.05, 520, 860, 9.4), light=GOLD, sun=(540, 700, 900, (0.12, 0.09, 0.03)), bloom=0.6)
    LC = [("p4s5d", 0.6), ("p4s5e", 4.2)]
    def midC(t):
        a = talk_pose(LC, t, 106, dict(turn=-0.2, gx=-0.4, gy=0.0, furrow=0.5, smile=0.15 + 0.3 * ease((t - 6.6) / 0.8), brow=-0.2, armR="relaxed",
                                       armL=("ik", 260, 420), propL="banner_black"))
        return at_neck(AFSHIN, P(**a), t, 540, 1060, 1.2)
    C = Shot(9.0, ghb, midC, cam=cam_push(1.0, 1.06, 540, 880, 9.0), light=GOLD, sun=(540, 700, 900, (0.12, 0.09, 0.03)), bloom=0.6, fade_out=0.8)
    return [A, B, C]


# ================================================================ S6 the fires on the plain (89.4-108)
def s6():
    npl = bgs.cached("night_plain", bgs.night_plain)
    def flick(im, t):
        im.alpha_composite(Image.new("RGBA", (W, H), (255, 140, 60, int(6 + 4 * math.sin(t * 9)))))
    A = Shot(5.0, npl, None, cam=cam_push(1.0, 1.08, 600, 1250, 5.0), grade="night", fade_in=0.8, fx=[flick])
    sky = bgs.cached("night_sky_wall", bgs.night_sky_wall)
    wall = bgs.cached("wall_fg_night", lambda: ImageEnhance.Brightness(bgs.cached("wall_fg", lambda: wallbg.wall_fg()[0])).enhance(0.38))
    def babak_wall(t, lines=()):
        q = talk_pose(list(lines), t, 107, dict(turn=0.15, gx=0.6, gy=-0.05, furrow=0.7, wind=0.8, armL=("ik", 70, 300), armR=("ik", -70, 300)))
        return at_neck(BABAK, P(**q), t, 640, 995, 0.85)
    LB = [("p4s6a", 0.6)]; LBb = [("p4s6b", 3.6)]
    def midB(t):
        n = talk_pose(LB, t, 108, dict(turn=-0.2, gx=-0.5 if t < 3.3 else -0.8, gy=0.0, sad=0.15, furrow=0.2, armL="relaxed", armR="relaxed", wind=0.6))
        return babak_wall(t, LBb) + at_neck(BANU, P(**n), t, 900, 1010, 0.82)
    B = Shot(8.8, sky, midB, fg=wall, cam=cam_push(1.0, 1.07, 720, 1050, 8.8), light=MOON, grade="night")
    skyb = blur_bg("night_sky_wall", bgs.night_sky_wall, 6)
    def midC(t):
        q = talk_pose([], t, 109, dict(turn=0.1, gx=0.3, gy=-0.1, furrow=0.8, smile=0.15, wind=0.8, armL="relaxed", armR="relaxed"))
        q["blink"] = max(0.15, q["blink"])
        return at_neck(BABAK, P(**q), t, 520, 1080, 1.35)
    C = Shot(4.8, skyb, midC, cam=cam_push(1.0, 1.05, 520, 880, 4.8), light=MOON, grade="night", fade_out=0.8)
    return [A, B, C]


SCENES = {"s1": s1, "s2": s2, "s3": s3, "s4": s4, "s5": s5, "s6": s6}
