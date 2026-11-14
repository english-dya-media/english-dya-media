"""Part 1 — 2D cartoon version. Scene timing matches the existing soundtrack (audio/part1.wav)."""
import math, random
from PIL import Image, ImageFilter
from film import Shot, W, H, ease, lerp, talk_pose, blink_at, cam_push, cam_static, Snow, Motes, Embers, svg_render, mouth
from chars import pose, elephant, cow, horse, Ctx, FEET
from stage import at_neck, at_feet, lying_at, crowd_row, back_heads, fire_svg, howdah, rider, Glow, lw_for
import bgs, cast
from cast import *

def P(**kw):
    return pose(**kw)

def merge(base, extra):
    q = dict(base); q.update(extra); return q

def blur_bg(name, fn, r=8):
    return bgs.cached(name + f"_b{r}", lambda: bgs.cached(name, fn).filter(ImageFilter.GaussianBlur(r)))

WARM = (1.0, 0.7, 0.4)

# ================================================================ S1 Samarra (0-16)
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
    def babak_on_elephant(t, turn=-0.25):
        q = P(chains=True, armL="chest", armR="chest", turn=turn, gx=-0.6, gy=-0.1, blink=max(0.2, blink_at(t, 4)), furrow=0.2, wind=0.3, legs="none")
        return at_neck(BABAK_CAPTIVE, q, t, 50, -912, 0.28, lws=0.17) + howdah(-80, -806, 260, 112)
    def midA(t):
        ex = 860 - 58 * t
        c = Ctx(lw_for(0.6))
        return f'<g transform="translate({ex:.1f},1468) scale(0.6)">{elephant(c, phase=t * 2.3, t=t)}{babak_on_elephant(t)}</g>'
    A = Shot(3.3, bgA, midA, fg=fg, cam=cam_push(1.0, 1.05, 560, 1150, 3.3), light=dict(rim=(-5, -2), rim_col=WARM, ramp=(0, W, 1.06, 0.84)),
             fx=[Motes(50, 3, (255, 220, 170), (0, 500, W, 1500), (-10, -4))], sun=(300, 1040, 700, (0.12, 0.07, 0.02)), fade_in=0.6)

    # 1B father & boy (3.3 - 9.0)
    crowd_blur = bgs.cached("s1_crowdblur", lambda: crowd_row(21, 9, 1500, 0.5, kinds=("man", "woman", "man")).filter(ImageFilter.GaussianBlur(7)))
    closeb = bgs.cached("samarra_close", bgs.samarra_close)
    bgB = closeb.copy(); bgB.alpha_composite(crowd_blur, (0, -150))
    LB = [("p1s1b", 1.8)]; LBo = [("p1s1a", 0.2)]
    def midB(t):
        asking = t < 1.6
        f = talk_pose(LB, t, 1, dict(turn=-0.32 if t < 0.4 else -0.3, gx=-0.6 if (0.5 < t < 3.4) else -0.9, gy=0.6 if (0.5 < t < 3.4) else 0.0,
                                     furrow=0.5, armL="relaxed", armR="relaxed"))
        b = talk_pose(LBo, t, 2, dict(turn=0.32, gx=0.7 if t < 4.0 else -0.6, gy=-0.7 if t < 4.0 else -0.2, brow=0.4,
                                      armR="point" if asking else "relaxed", armL="relaxed"))
        father = at_neck(FATHER, P(**f), t, 690, 610, 0.85)
        boy = at_neck(SAM_BOY, P(**b), t, 330, 610 + FEET * 0.85 - FEET * 0.62 * 0.85, 0.85)
        return boy + father
    B = Shot(5.7, bgB, midB, cam=cam_push(1.0, 1.04, 520, 800, 5.7), light=dict(rim=(-5, -2), rim_col=WARM, ramp=(0, W, 1.05, 0.86)),
             sun=(150, 1250, 700, (0.10, 0.06, 0.02)))

    # 1C boy close-up (9.0 - 11.2)
    LC = [("p1s1c", 0.2)]
    def midC(t):
        b = talk_pose(LC, t, 3, dict(turn=-0.22, gx=-0.6, gy=-0.5, brow=0.7, furrow=-0.2, armL="relaxed", armR="relaxed"))
        return at_neck(SAM_BOY, P(**b), t, 520, 1160, 1.6)
    C = Shot(2.2, blur_bg("samarra_close", bgs.samarra_close, 6), midC, cam=cam_push(1.0, 1.03, 520, 900, 2.2),
             light=dict(rim=(-6, -2), rim_col=WARM, ramp=(0, W, 1.05, 0.86)), sun=(150, 1250, 700, (0.10, 0.06, 0.02)))

    # 1D Babak close-up on the elephant (11.2 - 16.0)
    rail = bgs.cached("s1_rail", lambda: svg_render(howdah(-40, 1640, 1160, 300)))
    def midD(t):
        q = P(chains=True, armL="chest", armR="chest", turn=-0.12 + 0.06 * ease(t / 4.8), gx=-0.35 + 0.3 * ease((t - 2.5) / 1.5), gy=-0.2,
              blink=max(0.22, blink_at(t, 7)), furrow=0.1, brow=0.0, wind=0.35, breathe=math.sin(t * 1.6))
        return at_neck(BABAK_CAPTIVE, q, t, 560, 1030, 1.5)
    D = Shot(4.8, blur_bg("samarra_close", bgs.samarra_close, 6), midD, fg=rail, cam=cam_push(1.0, 1.07, 560, 860, 4.8),
             light=dict(rim=(-6, -2), rim_col=WARM, rim_str=1.0, ramp=(0, W, 1.06, 0.82)), sun=(150, 1250, 800, (0.12, 0.07, 0.02)), fade_out=1.2)
    return [A, B, C, D]

# ================================================================ S2 title (16-21)
def s2():
    return [Shot(5.0, bgs.cached("title_bg", bgs.title_bg), None, cam=cam_push(1.0, 1.04, 540, 1100, 5.0),
                 fx=[Embers(70, 4, (60, 600, 1020, 1600), (60, 150))], bloom=0.7, grade="fire", fade_in=0.5, fade_out=0.6)]

# ================================================================ S3 Belalabad (21-47)
def s3():
    wide = bgs.cached("belalabad_wide", bgs.belalabad_wide)
    cows = [(620, 1246, 0.62, 0.0), (800, 1206, 0.55, 1.7), (930, 1176, 0.48, 3.1)]
    def midA(t):
        o = ""
        c = Ctx(lw_for(0.3))
        for x, y, s, ph in cows:
            g = 0.5 + 0.5 * math.sin(t * 0.8 + ph)
            o += f'<g transform="translate({x},{y}) scale({s})">{cow(c, t=t + ph, graze=g)}</g>'
        u = t / 8.5
        bx = lerp(150, 400, u); by = lerp(1430, 1300, u); bs_ = lerp(0.27, 0.24, u)
        q = P(legs="walk", phase=t * 6.0, armR="relaxed", propR="stick", armL="relaxed", turn=0.3, gx=0.6, wind=0.3)
        o += at_feet(BABAK_BOY, q, t, bx, by, bs_)
        return o
    A = Shot(8.5, wide, midA, cam=cam_push(1.12, 1.12, 470, 1150, 8.5, 0, -110, 0, 0), light=dict(rim=(5, -3), rim_col=WARM, ramp=(0, W, 0.86, 1.05)),
             sun=(1000, 600, 800, (0.08, 0.06, 0.02)), fade_in=0.6, fx=[Motes(40, 6, (255, 240, 200), (0, 600, W, 1400), (-6, -3), amax=90)])

    door = bgs.cached("house_door", bgs.house_door)
    LB = [("p1s3b", 0.5)]
    def midB(t):
        m = talk_pose(LB, t, 5, dict(turn=0.35, gx=0.8, gy=-0.4, brow=0.6, armL="hold_baby", armR="hold_baby", propL="baby", wind=0.2))
        return at_neck(MAHRU, P(**m), t, 440, 700, 0.9)
    B = Shot(3.7, door, midB, cam=cam_push(1.0, 1.04, 470, 900, 3.7), light=dict(rim=(5, -2), rim_col=WARM, ramp=(0, W, 0.85, 1.05)),
             sun=(1080, 700, 800, (0.08, 0.06, 0.02)))

    LC = [("p1s3c", 0.3)]
    def midC(t):
        b = talk_pose(LC, t, 6, dict(turn=-0.28, gx=-0.6, gy=0.3, brow=0.5, armR="relaxed", propR="stick", armL="relaxed", wind=0.2))
        return at_neck(BABAK_BOY, P(**b), t, 560, 1130, 1.55)
    C = Shot(2.4, blur_bg("house_door", bgs.house_door, 8), midC, cam=cam_push(1.0, 1.03, 540, 900, 2.4),
             light=dict(rim=(5, -2), rim_col=WARM, ramp=(0, W, 0.85, 1.05)), sun=(1080, 700, 800, (0.08, 0.06, 0.02)))

    LD = [("p1s3d", 0.2)]
    def midD(t):
        sad = 0.5 * ease((t - 1.6) / 0.6) * (1 - ease((t - 4.0) / 0.8))
        smile = 0.7 * ease((t - 5.4) / 1.0)
        m = talk_pose(LD, t, 8, dict(turn=0.3, gx=0.6, gy=0.5, sad=sad, smile=smile, furrow=0.3 - 0.8 * sad, armL="hold_baby", armR="hold_baby", propL="baby", wind=0.2))
        b = talk_pose([], t, 9, dict(turn=-0.3, gx=-0.6 if (t < 1.4 or t > 6.0) else -0.8, gy=0.3 if (t < 1.4 or t > 6.0) else -0.6, smile=0.6 * ease((t - 6.2) / 1.0),
                                    armR="relaxed", propR="stick", armL="relaxed", sad=0.3 * sad, wind=0.2))
        Fm = 720 + FEET * 0.95 * 0.8
        return at_neck(BABAK_BOY, P(**b), t, 740, Fm - FEET * 0.62 * 0.8, 0.8) + at_neck(MAHRU, P(**m), t, 390, 720, 0.8)
    D = Shot(11.4, door, midD, cam=cam_push(1.0, 1.1, 560, 900, 11.4), light=dict(rim=(5, -2), rim_col=WARM, ramp=(0, W, 0.84, 1.06)),
             sun=(1080, 700, 900, (0.10, 0.07, 0.02)), fade_out=1.0)
    return [A, B, C, D]

# ================================================================ S4 the omen (47-71)
def tree_hill_tree():
    im = bgs.cached("tree_hill", bgs.tree_hill).copy()
    im.alpha_composite(svg_render(f'<g transform="translate(640,1196)">{bgs.big_tree(0.95)}</g>'))
    return im

def s4():
    th = bgs.cached("tree_hill_tree", tree_hill_tree)
    def midA(t):
        boy = lying_at(BABAK_BOY, P(blink=1.0, armL="relaxed", armR="relaxed", wind=0.1, breathe=math.sin(t * 1.5)), t, 520, 1214, 0.24)
        u = t / 6.0
        mx = lerp(960, 780, u); my = lerp(1760, 1430, u); ms = lerp(0.42, 0.33, u)
        q = P(legs="walk", phase=t * 5.5, armL="hold_bread", propL="bowl", armR="relaxed", turn=-0.3, gx=-0.5, gy=-0.2, wind=0.3)
        return boy + at_feet(MAHRU, q, t, mx, my, ms)
    A = Shot(6.0, th, midA, cam=cam_push(1.0, 1.1, 600, 1180, 6.0), light=dict(rim=(5, -2), rim_col=WARM, ramp=(0, W, 0.85, 1.06)),
             sun=(900, 900, 700, (0.12, 0.09, 0.03)), fx=[Motes(30, 8, (230, 190, 90), (100, 400, 1100, 1300), (-12, 34), (2, 4), 200)], fade_in=0.6)

    gc = bgs.cached("ground_close", bgs.ground_close)
    def midB(t):
        g = ease((t - 0.8) / 1.8)
        return lying_at(BABAK_BOY, P(blink=1.0, glow=g, armL="relaxed", armR="relaxed", wind=0.1, breathe=math.sin(t * 1.5), turn=0.0), t, 1150, 1010, 1.3)
    B = Shot(3.5, gc, midB, cam=cam_push(1.0, 1.06, 540, 900, 3.5), light=dict(rim=(5, -2), rim_col=WARM, ramp=(0, W, 0.88, 1.05)),
             sun=(1000, 500, 700, (0.10, 0.08, 0.03)), fx=[Motes(20, 9, (230, 190, 90), (0, 300, W, 1300), (-10, 30), (2, 4), 200)])

    LC = [("p1s4a", 0.5)]
    def midC(t):
        m = talk_pose(LC, t, 10, dict(turn=0.05, gx=-0.2, gy=0.6, brow=0.9, furrow=-0.4, blink=0.0, armL="chest", armR="relaxed", wind=0.2))
        m["blink"] = 0.0 if t < 3.2 else m["blink"]
        return at_neck(MAHRU, P(**m), t, 540, 1050, 1.5)
    C = Shot(4.0, blur_bg("tree_hill", bgs.tree_hill, 10), midC, cam=cam_push(1.0, 1.06, 540, 850, 4.0), light=dict(rim=(5, -2), rim_col=WARM, ramp=(0, W, 0.86, 1.05)),
             sun=(950, 700, 700, (0.10, 0.08, 0.03)))

    LD = [("p1s4b", 0.5)]
    def midD(t):
        bl = 1.0 if t < 0.25 else (0.5 if t < 0.4 else 0.0)
        b = talk_pose(LD, t, 11, dict(turn=0.3, gx=0.6, gy=-0.6, brow=0.5, blink=bl, armL="relaxed", armR="relaxed", legs="sit", wind=0.1))
        b["blink"] = max(bl, b["blink"])
        return at_neck(BABAK_BOY, P(**b), t, 520, 1150, 1.3)
    gfg = bgs.cached("grass_fg", bgs.grass_fg)
    D = Shot(2.8, gc, midD, fg=gfg, cam=cam_push(1.0, 1.03, 520, 900, 2.8), light=dict(rim=(5, -2), rim_col=WARM, ramp=(0, W, 0.86, 1.05)),
             sun=(1000, 500, 700, (0.10, 0.08, 0.03)))

    LE = [("p1s4c", 0.3)]
    def midE(t):
        smile = 0.6 * ease((t - 1.0) / 1.0)
        m = talk_pose(LE, t, 12, dict(turn=0.3, gx=0.7, gy=0.4, smile=smile, sad=0.4 * (1 - ease((t - 1.5) / 1.5)), armL="touch", armR="relaxed", wind=0.2))
        b = talk_pose([], t, 13, dict(turn=-0.3, gx=-0.7, gy=-0.5, smile=0.5 * ease((t - 4.0) / 1.0), brow=0.3, armL="relaxed", armR="relaxed", legs="sit"))
        return at_neck(BABAK_BOY, P(**b), t, 740, 1130, 1.0) + at_neck(MAHRU, P(**m), t, 380, 960, 1.0)
    E = Shot(7.7, blur_bg("tree_hill", bgs.tree_hill, 10), midE, fg=gfg, cam=cam_push(1.0, 1.08, 560, 900, 7.7), light=dict(rim=(5, -2), rim_col=WARM, ramp=(0, W, 0.84, 1.06)),
             sun=(950, 700, 800, (0.12, 0.09, 0.03)), fade_out=1.2)
    return [A, B, C, D, E]

# ================================================================ S5 montage (71-99)
def s5():
    st = bgs.cached("stable", bgs.stable)
    def midA(t):
        c = Ctx(lw_for(1.05))
        bx = 330 + 60 * math.sin(t * 3.6); by = 200 + 40 * math.sin(t * 7.2)
        q = P(armL=("ik", bx, by), propL="brush", armR="relaxed", turn=0.45, gx=0.8, gy=0.1, smile=0.3, wind=0.0)
        teen = at_feet(BABAK_TEEN, q, t, 470, 1560, 0.42)
        h = f'<g transform="translate(560,1500) scale(1.3)">{horse(c, col="#7a4a2a", t=t, saddle=False, head_down=0.15 + 0.1 * math.sin(t * 0.8))}</g>'
        return h + teen
    A = Shot(9.0, st, midA, cam=cam_push(1.0, 1.06, 560, 1150, 9.0), light=dict(rim=(-4, -4), rim_col=(1.0, 0.85, 0.6), ambient=(0.95, 0.9, 0.85)),
             fx=[Motes(80, 10, (255, 230, 170), (0, 300, W, 1400), (8, 10), amax=110)], grade="warm", fade_in=0.5)

    nf = bgs.cached("night_fire", bgs.night_fire)
    LB = [("p1s5a", 2.0)]
    def midB(t):
        old_plays = t < 4.6
        strum = lambda tt: ("ik", -60 + 14 * math.sin(tt * 9), 360)
        neck = ("ik", 210, 20)
        o = talk_pose(LB, t, 14, dict(turn=0.35, gx=0.7, gy=0.1, furrow=0.2, legs="sit",
                                      armR=strum(t) if old_plays else "relaxed", armL=neck if old_plays else ("ik", 120, 330), propR="tanbur" if old_plays else None))
        tq = talk_pose([], t, 15, dict(turn=-0.35, gx=-0.7, gy=0.1, legs="sit", smile=0.4 * ease((t - 6) / 1.5),
                                       armR=strum(t) if not old_plays else "relaxed", armL=neck if not old_plays else "relaxed", propR=None if old_plays else "tanbur"))
        return (at_neck(STABLE_HAND, P(**o), t, 290, 1300 - 575 * 0.5, 0.5) + at_neck(BABAK_TEEN, P(**tq), t, 800, 1300 - 575 * 0.5 * 0.86, 0.5, flip=True) +
                fire_svg(540, 1300, 70, t))
    B = Shot(9.0, nf, midB, cam=cam_push(1.0, 1.05, 540, 1150, 9.0), light=dict(point=(540, 1240, 650, 0.5, 1.15, (1.0, 0.55, 0.25)), rim_point=(540, 6), rim_col=(1.0, 0.65, 0.3)),
             fx=[Embers(40, 5, (440, 900, 640, 1290), (60, 160))], grade="fire", bloom=0.6)

    bz = bgs.cached("bazaar", bgs.bazaar)
    r = random.Random(4)
    walkers = []
    import stage
    for k in range(4):
        S = stage.random_spec(r, ("man", "man", "woman"))
        walkers.append((S, r.uniform(-1, 1), lerp(1330, 1460, k / 3), lerp(0.3, 0.4, k / 3), r.choice([-1, 1]), r.uniform(0, 6)))
    def midC(t):
        o = ""
        for S, x0, y, s, d, ph in walkers:
            x = (540 + x0 * 500 + d * 70 * t) % 1300 - 110
            q = P(legs="walk", phase=t * 6 + ph, turn=0.4 * d, gx=0.6 * d, armL="relaxed", armR="relaxed", wind=0.1)
            o += at_feet(S, q, t, x, y, s)
        u = t / 6.3
        q = P(legs="walk", phase=t * 6.2, armL=("ik", 150, -50), propL="sack", armR="relaxed", turn=-0.1, gx=-0.2, wind=0.1)
        o += at_feet(BABAK_TEEN, q, t, lerp(600, 560, u), lerp(1300, 1520, u), lerp(0.3, 0.46, u))
        return o
    C = Shot(6.3, bz, midC, cam=cam_push(1.02, 1.06, 540, 1100, 6.3), light=dict(rim=(0, -5), rim_col=(1.0, 0.85, 0.55), ambient=(1.0, 0.93, 0.84)),
             fx=[Motes(60, 11, (255, 230, 170), (200, 300, 880, 1300), (4, 6), amax=100)], grade="warm")

    vw = bgs.cached("village_winter_dusk", bgs.village_winter_dusk)
    def midD(t):
        u = min(1, t / 2.6)
        q = P(legs="walk" if t < 2.6 else "stand", phase=t * 5.6, armL=("ik", 150, -50), propL="sack", armR="relaxed",
              turn=-0.1 if t < 2.6 else -0.45, gx=-0.2 if t < 2.6 else -0.9, smile=0.5 * ease((t - 2.8) / 0.6), wind=0.4)
        return at_feet(BABAK_YOUNG, q, t, lerp(580, 540, u), lerp(1330, 1450, u), lerp(0.3, 0.37, u))
    D = Shot(3.7, vw, midD, cam=cam_push(1.0, 1.04, 540, 1150, 3.7), light=dict(rim=(-4, -2), rim_col=(1.0, 0.75, 0.7), ambient=(0.9, 0.92, 1.02)),
             fx=[Snow(160, 12, -40, (60, 140), (1.0, 2.6), (90, 180))], grade="night", fade_out=0.5)
    return [A, B, C, D]

# ================================================================ S6 the snow night (99-127)
def s6():
    bl = bgs.cached("blizzard", bgs.blizzard)
    riders = [(JAVIDAN, 0.0, 1330, 0.36, "#3a2a1e", True), (SERVANT, -260, 1300, 0.32, "#5a3a22", False),
              (SERVANT, -500, 1280, 0.29, "#2a2a2a", False), (SERVANT, -730, 1262, 0.27, "#6a4a2a", False)]
    def midA(t):
        o = ""
        for k, (S, dx, y, s, col, lead) in enumerate(reversed(riders)):
            x = 330 + dx + 70 * t
            q = P(turn=0.45, gx=0.8, gy=0.1, furrow=0.7, armR="hold_lantern" if lead else "forward", propR="lantern" if lead else None, armL="forward", wind=1.0)
            o += rider(S, q, t, lambda c, col=col, k=k: horse(c, col=col, walk=True, phase=t * 4.2 + k, t=t + k), x, y, s)
        return o
    lantern_pos = lambda t: (330 + 70 * t + 0.36 * 100, 1330 - 0.36 * 420)
    A = Shot(8.0, bl, midA, cam=cam_push(1.0, 1.05, 600, 1200, 8.0), light=dict(rim=(0, -3), rim_col=(0.7, 0.8, 1.0), ambient=(0.62, 0.68, 0.9)),
             fx=[Snow(800, 13, 320, (240, 520), (1.4, 5.0)), Glow(lantern_pos, 160, (255, 190, 110), 0.5)], grade="night", fade_in=0.6)

    inter = bgs.cached("interior", bgs.interior)
    knocks = (3.0, 4.0, 5.0)
    def midB(t):
        alert = t > 3.0
        m = talk_pose([], t, 16, dict(turn=0.5 if alert else -0.2, gx=0.9 if alert else -0.3, gy=0.3 if not alert else 0.0, legs="sit",
                                      armR=(26, 108 + 12 * math.sin(t * 6)) if not alert else "relaxed", armL="relaxed", brow=0.5 if alert else 0.0))
        o = at_neck(MAHRU, P(**m), t, 455, 1470 - 575 * 0.62 * 0.95, 0.62)
        if t < 5.6:
            b = talk_pose([], t, 17, dict(turn=0.5 if alert else 0.0, gx=0.9 if alert else 0.0, gy=0.0 if alert else 0.6, legs="sit",
                                          armR="hold_bread", armL="hold_bread", brow=0.4 if alert else 0.0))
            o += at_neck(BABAK_YOUNG, P(**b), t, 745, 1480 - 575 * 0.62, 0.62)
        else:
            u = ease((t - 6.2) / 2.0)
            b = talk_pose([], t, 17, dict(turn=0.45, gx=0.9, legs="walk" if t > 6.2 else "stand", phase=t * 5.5, armR="relaxed", armL="relaxed", brow=0.3))
            o += at_feet(BABAK_YOUNG, P(**b), t, lerp(745, 870, u), 1500, 0.62)
        o += fire_svg(230, 1300, 62, t)
        return o
    B = Shot(8.2, inter, midB, cam=cam_push(1.0, 1.05, 560, 1150, 8.2), light=dict(point=(230, 1180, 900, 0.5, 1.15, (1.0, 0.55, 0.25)), rim_point=(230, 6), rim_col=(1.0, 0.65, 0.3)),
             fx=[Embers(20, 6, (170, 1100, 290, 1290), (40, 100))], grade="fire")

    dw = bgs.cached("doorway", bgs.doorway)
    LC = [("p1s6a", 2.4)]
    def door_panel(t):
        u = ease(t / 1.1)
        if u >= 1:
            return ""
        x0 = lerp(250, 830, u)
        return (f'<path d="M {x0:.1f} {420 - 30*u:.1f} L 830 420 L 830 1520 L {x0:.1f} {1520 + 30*u:.1f} Z" fill="#5a3620" stroke="#2a180e" stroke-width="4"/>'
                + "".join(f'<path d="M {lerp(x0, 830, k/5):.1f} 420 L {lerp(x0, 830, k/5):.1f} 1520" stroke="#3a2214" stroke-width="3"/>' for k in range(1, 5)))
    def jav(t, lines):
        j = talk_pose(lines, t, 18, dict(turn=0.0, gx=0.0, gy=0.2, furrow=0.6, armR="hold_lantern", propR="lantern", armL="relaxed", wind=0.8))
        return at_neck(JAVIDAN, P(**j), t, 545, 760, 0.92)
    def midC(t):
        return jav(t, LC) + door_panel(t)
    lan = lambda t: (545 - 0.92 * 160, 760 + 0.92 * 560)
    C = Shot(6.3, dw, midC, cam=cam_push(1.0, 1.05, 540, 900, 6.3), light=dict(rim=(-5, -3), rim_col=(0.6, 0.75, 1.0), rim_str=0.7, ambient=(1.0, 0.92, 0.84)),
             fx=[Snow(260, 14, 60, (200, 420), (1.4, 4.0), (120, 220), 420, 1560), Glow(lan, 200, (255, 190, 110), 0.45)], grade="fire")

    ib = blur_bg("interior", bgs.interior, 9)
    def midD(t):
        b = talk_pose([], t, 19, dict(turn=0.25, gx=0.6, gy=-0.4, brow=0.6, furrow=0.0, armL="relaxed", armR="relaxed"))
        return at_neck(BABAK_YOUNG, P(**b), t, 500, 1070, 1.55)
    D = Shot(2.0, ib, midD, cam=cam_push(1.0, 1.04, 520, 900, 2.0), light=dict(rim=(5, -1), rim_col=WARM, ramp=(0, W, 0.78, 1.1)),
             sun=(1080, 800, 700, (0.12, 0.07, 0.02)), grade="fire")

    def midE(t):
        return jav(t + 6.3, [])
    E = Shot(3.5, dw, midE, cam=cam_push(1.05, 1.08, 540, 900, 3.5), light=dict(rim=(-5, -3), rim_col=(0.6, 0.75, 1.0), rim_str=0.7, ambient=(1.0, 0.92, 0.84)),
             fx=[Snow(260, 14, 60, (200, 420), (1.4, 4.0), (120, 220), 420, 1560), Glow(lan, 200, (255, 190, 110), 0.45)], grade="fire", fade_out=0.6)
    return [A, B, C, D, E]

SCENES = {"s1": s1, "s2": s2, "s3": s3, "s4": s4, "s5": s5, "s6": s6}
