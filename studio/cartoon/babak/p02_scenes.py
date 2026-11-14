"""Part 2 — 2D cartoon version. Timing matches audio/part2.wav."""
import math, random
from PIL import Image, ImageFilter, ImageDraw
from film import Shot, W, H, ease, lerp, talk_pose, blink_at, cam_push, cam_static, Snow, Motes, Embers, svg_render
from chars import pose, horse, Ctx, FEET, fmt
from stage import at_neck, at_feet, lying_at, crowd_row, back_heads, fire_svg, rider, Glow, lw_for, random_spec
import bgs
from cast import *
from p01_scenes import P, blur_bg, WARM
import wallbg
NIGHT = dict(ambient=(0.62, 0.7, 0.95), rim=(0, -3), rim_col=(0.7, 0.8, 1.0), rim_str=0.6)

def banner_svg(t, x, y, w, h, col="#b5161b", edge="#e0b25a", speed=6.0):
    n = 14; top, bot = [], []
    for i in range(n + 1):
        u = i / n
        wave = (10 + 24 * u) * math.sin(t * speed - u * 7.0)
        top.append((x - w * u, y + wave + 6 * u)); bot.append((x - w * u * 0.96, y + h + wave * 1.1 + 14 * u))
    d = "M " + " L ".join(f"{a:.1f} {b:.1f}" for a, b in top + bot[::-1]) + " Z"
    stripe = "M " + " L ".join(f"{a:.1f} {b + h * 0.12:.1f}" for a, b in top[:-1])
    return (f'<rect x="{x-5}" y="{y-40}" width="10" height="{h+900}" fill="#2a1a12" stroke="#120a06" stroke-width="2"/>'
            f'<circle cx="{x}" cy="{y-46}" r="11" fill="#e0b25a" stroke="#120a06" stroke-width="2"/>'
            f'<path d="{d}" fill="{col}" stroke="#1a0606" stroke-width="2.5"/>' + (f'<path d="{stripe}" stroke="{edge}" stroke-width="5" fill="none" opacity="0.85"/>' if edge else ""))

def birds(t, x0=360, y0=520):
    s = ""
    for k in range(5):
        x = x0 - 26 * t + k * 54 + 12 * math.sin(k * 2.1); y = y0 + k * 22 + 8 * math.sin(t * 2 + k)
        fl = 9 * math.sin(t * 10 + k * 1.7)
        s += f'<path d="M {x-14:.1f} {y-fl:.1f} Q {x-6:.1f} {y-3:.1f} {x:.1f} {y:.1f} Q {x+6:.1f} {y-3:.1f} {x+14:.1f} {y-fl:.1f}" stroke="#2a1a2e" stroke-width="3.2" fill="none" stroke-linecap="round"/>'
    return s

FIRE = dict(point=(230, 1180, 900, 0.5, 1.15, (1.0, 0.55, 0.25)), rim_point=(230, 6), rim_col=(1.0, 0.65, 0.3))

# ================================================================ S7 the guest (0-27)
def s7():
    inter = bgs.cached("interior", bgs.interior)
    LA = [("p2s7a", 3.5)]
    def midA(t):
        o = fire_svg(230, 1300, 62, t)
        for k, (x, sd) in enumerate([(640, 31), (90, 32)]):
            q = talk_pose([], t, sd, dict(turn=0.3, gx=0.5, legs="sit", armL=("ik", 60, 330), armR=("ik", -60, 330), blink=0.9 if k == 0 else 0.0))
            o += at_neck(SERVANT, P(**q), t, x, 1480 - 575 * 0.55, 0.55)
        jq = talk_pose([], t, 33, dict(turn=0.35 if t > 3.2 else -0.2, gx=0.8 if t > 3.2 else -0.5, legs="sit", armL=("ik", 60, 300), armR=("ik", -60, 300)))
        o += at_neck(JAVIDAN, P(**jq), t, 480, 1490 - 575 * 0.62, 0.62)
        m = talk_pose(LA, t, 34, dict(turn=-0.4, gx=-0.8, gy=0.3, sad=0.25, armL="chest", armR="relaxed"))
        o += at_neck(MAHRU, P(**m), t, 840, 1560 - FEET * 0.95 * 0.72, 0.72)
        return o
    A = Shot(6.4, inter, midA, cam=cam_push(1.0, 1.04, 560, 1150, 6.4), light=FIRE, fx=[Embers(20, 6, (170, 1100, 290, 1290), (40, 100))], grade="fire", fade_in=0.5)

    ib = blur_bg("interior", bgs.interior, 9)
    LA2 = [("p2s7b", 0.2)]
    def midA2(t):
        j = talk_pose(LA2, t, 35, dict(turn=0.2, gx=0.5, gy=0.1, smile=0.5, armL="relaxed", armR="relaxed"))
        return at_neck(JAVIDAN, P(**j), t, 540, 1080, 1.3)
    A2 = Shot(2.6, ib, midA2, cam=cam_push(1.0, 1.03, 540, 900, 2.6), light=dict(rim=(-6, -2), rim_col=WARM, ramp=(0, W, 1.08, 0.8)),
              sun=(0, 1100, 700, (0.12, 0.06, 0.02)), grade="fire")

    ns = bgs.cached("night_stable_snow", bgs.night_stable_snow)
    def babpos(t):
        u = ease(t / 3.5); return lerp(330, 560, u), lerp(1360, 1400, u)
    def midB(t):
        c = Ctx(lw_for(0.8))
        o = f'<g transform="translate(760,1330) scale(0.8)">{horse(c, col="#5a3a22", t=t, saddle=False, head_down=0.85)}</g>'
        o += f'<g transform="translate(960,1320) scale(0.72)">{horse(c, col="#3a2a1e", t=t + 2, saddle=False, head_down=0.6 + 0.3 * math.sin(t))}</g>'
        x, y = babpos(t)
        walking = t < 3.5
        q = talk_pose([], t, 36, dict(turn=0.4, gx=0.8, legs="walk" if walking else "stand", phase=t * 5.6, armR="hold_lantern", propR="lantern",
                                      armL="relaxed" if walking else ("ik", 230, 200 + 40 * math.sin(t * 3)), wind=0.9, furrow=0.5))
        o += at_feet(BABAK_YOUNG, P(**q), t, x, y, 0.5)
        return o
    lan = lambda t: (babpos(t)[0] - 0.5 * 150, babpos(t)[1] - 0.5 * 750)
    B = Shot(7.0, ns, midB, cam=cam_push(1.0, 1.05, 600, 1150, 7.0), light=NIGHT,
             fx=[Snow(600, 21, -220, (180, 420), (1.4, 4.6)), Glow(lan, 170, (255, 190, 110), 0.5)], grade="night")

    LC = [("p2s7c", 1.8)]; LCb = [("p2s7d", 4.3)]
    def midC(t):
        o = fire_svg(230, 1300, 62, t)
        q = talk_pose([], t, 37, dict(turn=0.3, gx=0.5, legs="sit", armL=("ik", 60, 330), armR=("ik", -60, 330), blink=0.92))
        o += at_neck(SERVANT, P(**q), t, 140, 1480 - 575 * 0.55, 0.55)
        j = talk_pose(LC, t, 38, dict(turn=0.4, gx=0.8, gy=-0.2, legs="sit", smile=0.6 * ease((t - 7.6) / 1.0), brow=0.5 if 1.6 < t < 3.8 else 0.1,
                                      armL=("ik", 60, 300), armR=("ik", -60, 300)))
        o += at_neck(JAVIDAN, P(**j), t, 420, 1500 - 575 * 0.66, 0.66)
        u = ease(t / 2.4)
        walking = t < 2.4
        b = talk_pose(LCb, t, 39, dict(turn=-0.4, gx=-0.8, gy=0.2, legs="walk" if walking else "stand", phase=t * 5.6,
                                       armR="hold_bread", propR="bread", armL="relaxed", smile=0.3 * ease((t - 8) / 1)))
        o += at_feet(BABAK_YOUNG, P(**b), t, lerp(1000, 770, u), 1560, 0.66)
        return o
    C = Shot(11.0, inter, midC, cam=cam_push(1.0, 1.06, 600, 1100, 11.0), light=FIRE, fx=[Embers(20, 7, (170, 1100, 290, 1290), (40, 100))], grade="fire")
    return [A, A2, B, C]

# ================================================================ S8 dawn (27-49)
def s8():
    dh = bgs.cached("dawn_house", bgs.dawn_house)
    DAWN = dict(rim=(5, -2), rim_col=(1.0, 0.78, 0.7), ambient=(0.96, 0.94, 1.0), ramp=(0, W, 0.88, 1.04))
    def horses_bg(t):
        c = Ctx(lw_for(0.5))
        return (f'<g transform="translate(700,1300) scale(0.5)">{horse(c, col="#5a3a22", t=t, head_down=0.2)}</g>'
                f'<g transform="translate(900,1290) scale(0.46)">{horse(c, col="#3a2a1e", t=t + 1.3)}</g>')
    LA = [("p2s8a", 3.0)]
    def midA(t):
        j = talk_pose(LA, t, 41, dict(turn=0.4, gx=0.8, gy=0.1, smile=0.3, armL="relaxed", armR="relaxed", wind=0.4))
        b = talk_pose([], t, 42, dict(turn=-0.4, gx=-0.8, gy=-0.1, armL="relaxed", armR="relaxed", wind=0.4))
        return horses_bg(t) + at_feet(JAVIDAN, P(**j), t, 360, 1560, 0.7) + at_feet(BABAK_YOUNG, P(**b), t, 770, 1560, 0.7)
    A = Shot(6.2, dh, midA, cam=cam_push(1.0, 1.05, 560, 1150, 6.2), light=DAWN, sun=(820, 1000, 700, (0.10, 0.07, 0.05)), fade_in=0.6,
             fx=[Motes(30, 12, (255, 240, 235), (0, 400, W, 1300), (-8, -2), amax=80)])
    dhb = blur_bg("dawn_house", bgs.dawn_house, 9)
    LB = [("p2s8b", 0.2)]
    def midB(t):
        j = talk_pose(LB, t, 43, dict(turn=0.15, gx=0.3, gy=-0.2, brow=0.3, tilt=-2.0, armL="relaxed", armR="relaxed", wind=0.4))
        return at_neck(JAVIDAN, P(**j), t, 540, 1080, 1.3)
    B = Shot(3.2, dhb, midB, cam=cam_push(1.0, 1.04, 540, 900, 3.2), light=DAWN, sun=(820, 1000, 700, (0.10, 0.07, 0.05)))
    LC = [("p2s8c", 0.2)]
    def midC(t):
        j = talk_pose(LC, t, 44, dict(turn=-0.4, gx=-0.8, gy=0.1, smile=0.2, armR="offer" if t > 1.2 else "relaxed", propR="purse" if t > 1.2 else None, armL="relaxed", wind=0.4))
        m = talk_pose([], t, 45, dict(turn=0.4, gx=0.8 if t < 4.0 else 0.2, gy=0.0 if t < 4.0 else 0.6, sad=0.3 + 0.3 * ease((t - 3) / 2), armL="chest", armR="relaxed", wind=0.4))
        return at_feet(MAHRU, P(**m), t, 300, 1580, 0.75) + at_feet(JAVIDAN, P(**j), t, 760, 1580, 0.75)
    C = Shot(7.2, dh, midC, cam=cam_push(1.0, 1.06, 540, 1100, 7.2), light=DAWN, sun=(820, 1000, 700, (0.10, 0.07, 0.05)))
    LD = [("p2s8d", 0.4)]
    def midD(t):
        m = talk_pose(LD, t, 46, dict(turn=0.25, gx=0.6, gy=0.2, sad=0.9, smile=0.4 * ease((t - 1.0) / 0.6), armL="chest", armR="relaxed", wind=0.4))
        return at_neck(MAHRU, P(**m), t, 520, 1060, 1.45)
    D = Shot(2.2, dhb, midD, cam=cam_push(1.0, 1.03, 520, 900, 2.2), light=DAWN, sun=(820, 1000, 700, (0.10, 0.07, 0.05)))
    def midE(t):
        o = ""
        m = P(turn=0.4, gx=0.8, armR="wave" if int(t * 2) % 2 == 0 else (110, -40), armL="relaxed", sad=0.5)
        o += at_feet(MAHRU, m, t, 230, 1330, 0.3)
        for k, (S, col, dx) in enumerate([(BABAK_YOUNG, "#5a3a22", -230), (JAVIDAN, "#3a2a1e", 0)]):
            x = 520 + dx + 60 * t
            q = P(turn=0.4, gx=0.8, armR="forward", armL="forward", wind=0.6)
            o += rider(S, q, t, lambda c, col=col, k=k: horse(c, col=col, walk=True, phase=t * 4.2 + k, t=t + k), x, 1420 + 20 * k, 0.42)
        return o
    E = Shot(3.2, dh, midE, cam=cam_push(1.0, 1.04, 560, 1150, 3.2), light=DAWN, sun=(820, 1000, 700, (0.10, 0.07, 0.05)), fade_out=0.6)
    return [A, B, C, D, E]

# ================================================================ S9 Bazz, battle, deathbed (49-77)
def bazz_shot(dur, palette, seed, fade_in=0.8, fade_out=0.3, riders=True, cam=None):
    base = bgs.cached(f"bazz_{palette}", lambda: bgs.bazz(palette))
    back = bgs.cached(f"cloud_back_{palette}", lambda: bgs.cloud_sea(1180, seed))
    front = bgs.cached(f"cloud_front_{palette}", lambda: bgs.cloud_sea(1330, seed + 1, hi="#fffaf6", mid="#f0e4e6", lo="#d7cfe0"))
    def bg(t):
        im = base.copy()
        im.alpha_composite(back, (int(-300 + 5 * t), 0))
        return im
    trail = [(300, 1290), (440, 1220), (380, 1150), (470, 1080), (430, 1010), (490, 940), (455, 870), (480, 810), (520, 780)]
    def along(u):
        seg = [math.dist(trail[i], trail[i + 1]) for i in range(len(trail) - 1)]
        s_ = u * sum(seg)
        for i, l in enumerate(seg):
            if s_ <= l:
                f = s_ / l; return lerp(trail[i][0], trail[i + 1][0], f), lerp(trail[i][1], trail[i + 1][1], f)
            s_ -= l
        return trail[-1]
    def mid(t):
        o = birds(t, 900, 420)
        for i, (x, y) in enumerate([(485, 610), (630, 580), (765, 630)]):
            top = y - 96
            pts_t = [(x + 3 + 56 * u, top + 6 * math.sin(t * 5 - u * 6 + i) * u) for u in [k / 8 for k in range(0, 9)]]
            pts_b = [(x + 3 + 54 * u, top + 38 + 6 * math.sin(t * 5 - u * 6 + i) * u + 4 * u) for u in [k / 8 for k in range(8, -1, -1)]]
            o += (f'<rect x="{x-3}" y="{top-6}" width="6" height="{y-top+6}" fill="#1e1a26"/>'
                  f'<path d="M ' + " L ".join(f"{px:.1f} {py:.1f}" for px, py in pts_t + pts_b) + ' Z" fill="#b5161b" stroke="#2a0a0a" stroke-width="2"/>')
        if riders:
            for k in range(5):
                x, y = along((t * 0.05 + k * 0.08) % 1.0)
                o += f'<ellipse cx="{x:.1f}" cy="{y-8:.1f}" rx="6" ry="9" fill="#1a1420"/><circle cx="{x:.1f}" cy="{y-20:.1f}" r="4.5" fill="#1a1420"/>'
        return o
    def fg(t):
        im = Image.new("RGBA", (W, H))
        im.alpha_composite(front, (int(-300 - 9 * t), 0))
        return im
    return Shot(dur, bg, mid, fg=[fg], cam=cam or cam_push(1.0, 1.06, 620, 900, dur), light=dict(rim=(0, 0)), sun=(240, 1120, 700, (0.10, 0.07, 0.04)) if palette == "dusk" else (860, 1240, 700, (0.12, 0.07, 0.04)),
                fade_in=fade_in, fade_out=fade_out)

def s9():
    A = bazz_shot(9.0, "dusk", 30)
    fb = bgs.cached("fog_battle", bgs.fog_battle)
    fogtex = bgs.cached("fog_tex", lambda: svg_render("".join(
        f'<ellipse cx="{random.Random(i).uniform(-200, 1700):.0f}" cy="{random.Random(i + 50).uniform(900, 1500):.0f}" rx="{random.Random(i + 9).uniform(200, 420):.0f}" ry="{random.Random(i + 3).uniform(50, 110):.0f}" fill="#d8dee4" opacity="0.5"/>'
        for i in range(26)), 1700, H).filter(ImageFilter.GaussianBlur(30)))
    r = random.Random(9)
    from cast import SOLDIER
    ENEMY = dict(SOLDIER, col="#1c1c22", col2="#0e0e12", head="turban", head_col="#141418", cuff="#2a2a30", trim="#2a2a30")
    FRIEND = dict(SOLDIER, col="#5a2a1e", col2="#3a1a12", head="cap", head_col="#4a2a1a", cuff="#7a4a2a", trim="#7a4a2a")
    sold = []
    for side, S in ((-1, FRIEND), (1, ENEMY)):
        for j in range(4):
            sold.append((S, side, j, r.uniform(0, 6), r.uniform(-1, 1)))
    def midB(t):
        o = ""
        back = [(S, sd, j, ph, ji) for (S, sd, j, ph, ji) in sold if j >= 2]
        front = [(S, sd, j, ph, ji) for (S, sd, j, ph, ji) in sold if j < 2]
        for group, y0, sc in ((back, 1330, 0.34), (front, 1460, 0.44)):
            for S, side, j, ph, ji in group:
                adv = min(t, 2.4) * 60
                x = 540 + side * (330 - adv + 120 * (j % 2) + 18 * ji)
                thrust = 30 * max(0.0, math.sin(t * 6 + ph))
                q = P(turn=-0.55 * side, gx=-0.9 * side, armL=(60 + thrust, -20), propL="spear", armR=(50 + thrust * 0.6, 60),
                      legs="walk" if t < 2.4 else "stand", phase=t * 6 + ph, furrow=1.0, mouth_o=0.4 + 0.3 * math.sin(t * 7 + ph))
                o += at_feet(S, q, t, x, y0 + 10 * (j % 2) + 6 * math.sin(t * 5 + ph), sc, flip=(side > 0))
            if group is back:
                fall = ease((t - 3.2) / 0.9)
                swing = 140 + 20 * math.sin(t * 7) if t < 3.1 else 20
                jq = P(turn=0.2, gx=0.3, armL=(swing, -10), propL="sword", armR="forward", furrow=1.0, wind=0.9, blink=0.85 * fall, mouth_o=0.5 if t < 3.1 else 0.2)
                o += (f'<g transform="translate(0,{110 * fall:.1f}) rotate({-50 * fall:.1f},560,1430)">' +
                      rider(JAVIDAN, jq, t, lambda c: horse(c, col="#2a2a2e", walk=t < 3.1, phase=t * 6, t=t, head_bob=-30 * max(0, math.sin(t * 3))), 520, 1430, 0.66) + '</g>')
        return o
    fog_soft = fogtex.copy(); fog_soft.putalpha(fogtex.getchannel("A").point(lambda v: int(v * 0.65)))
    def fogfx(im, t):
        im.alpha_composite(fog_soft.crop((int(300 + 40 * t), 0, int(300 + 40 * t) + W, H)))
    def flash(im, t):
        a = max(0.0, 1 - abs(t - 3.1) / 0.2)
        if a > 0:
            im.alpha_composite(Image.new("RGBA", (W, H), (255, 255, 255, int(190 * a))))
    B = Shot(6.0, fb, midB, cam=cam_push(1.04, 1.0, 540, 1150, 6.0), light=dict(ambient=(0.72, 0.76, 0.82), rim=(0, -3), rim_col=(0.85, 0.9, 1.0), rim_str=0.5),
             fx=[fogfx, flash], grade="night", fade_in=0.2)

    room = bgs.cached("bedroom", bgs.bedroom)
    rb = blur_bg("bedroom", bgs.bedroom, 9)
    CANDLE = dict(rim=(5, -2), rim_col=(1.0, 0.65, 0.35), ramp=(0, W, 0.7, 1.08))
    pillow = '<rect x="250" y="800" width="580" height="260" rx="110" fill="#e8dcc8" stroke="#1b0f0a" stroke-width="4"/><path d="M 290 1000 C 420 1030, 660 1030, 790 1000" stroke="#c8b89c" stroke-width="10" fill="none"/>'
    blanket = bgs.cached("blanket_fg", lambda: svg_render('<path d="M -40 1330 C 200 1290, 800 1280, 1120 1320 L 1120 1920 L -40 1920 Z" fill="#6a2a1e" stroke="#1b0f0a" stroke-width="5"/>'
                                                          '<path d="M -40 1360 C 200 1320, 800 1310, 1120 1350" stroke="#d8a64a" stroke-width="10" fill="none"/>'))
    LC1 = [("p2s9a", 2.0)]
    def midC1(t):
        j = talk_pose(LC1, t, 51, dict(turn=0.1, gx=0.2, gy=-0.2, sad=0.4, furrow=-0.2, armL="relaxed", armR="relaxed"))
        j["blink"] = max(0.3, j["blink"]); j["mouth_o"] *= 0.7
        return pillow + at_neck(JAVIDAN_ILL, P(**j), t, 540, 1150, 1.25)
    C1 = Shot(5.6, rb, midC1, fg=blanket, cam=cam_push(1.0, 1.05, 540, 900, 5.6), light=CANDLE, sun=(1000, 1000, 600, (0.12, 0.06, 0.02)), grade="fire", fade_in=0.3)
    LC2 = [("p2s9b", 0.4)]
    def midC2(t):
        b = talk_pose(LC2, t, 52, dict(turn=-0.25, gx=-0.6, gy=0.5, sad=0.7, armL="relaxed", armR="relaxed"))
        return at_neck(BANU, P(**b), t, 540, 1060, 1.45)
    C2 = Shot(2.7, rb, midC2, cam=cam_push(1.0, 1.03, 540, 900, 2.7), light=CANDLE, sun=(1000, 1000, 600, (0.12, 0.06, 0.02)), grade="fire")
    OUT_T = 1.7
    def midC3(t):
        o = lying_at(JAVIDAN_ILL, P(blink=1.0, armL="relaxed", armR="relaxed"), t, 660, 1150, 0.42)
        o += '<path d="M 470 1085 C 560 1040, 900 1040, 950 1080 L 950 1160 L 470 1160 Z" fill="#6a2a1e" stroke="#1b0f0a" stroke-width="3"/>'
        b = talk_pose([], t, 53, dict(turn=-0.3, gx=-0.6, gy=0.5, sad=0.7, legs="sit", armL="chest", armR="relaxed"))
        o += at_neck(BANU, P(**b), t, 880, 1420 - 575 * 0.95 * 0.5, 0.5)
        o += at_feet(BABAK_YOUNG, P(turn=0.3, gx=0.6, gy=0.3, sad=0.4, armL="relaxed", armR="relaxed"), t, 175, 1300, 0.42)
        if t < OUT_T:
            o += fire_svg(880, 1050, 12, t * 0.7)
        return o
    def dark(im, t):
        if t >= OUT_T:
            d = ImageDraw.Draw(im, "RGBA")
            for k in range(7):
                age = t - OUT_T - k * 0.18
                if age > 0:
                    y = 1040 - age * 55 - k * 6; x = 880 + 14 * math.sin(age * 2.2 + k); rr = 5 + age * 6
                    d.ellipse((x - rr, y - rr, x + rr, y + rr), fill=(150, 140, 135, int(max(0, 60 - age * 18))))
            im.alpha_composite(Image.new("RGBA", (W, H), (0, 0, 0, int(255 * min(0.6, (t - OUT_T) * 0.9)))))
    C3 = Shot(4.7, room, midC3, cam=cam_push(1.0, 1.05, 560, 1100, 4.7), light=dict(rim=(5, -2), rim_col=(1.0, 0.65, 0.35), point=(880, 1050, 800, 0.55, 1.1, (1.0, 0.55, 0.25))),
              fx=[dark], grade="fire", fade_out=1.4)
    return [A, B, C1, C2, C3]

# ================================================================ S10 the successor (77-96)
REDS = ["#8a1a1a", "#a0261e", "#7a1414", "#b03424", "#6a1a1a"]
def red_crowd(seed, n, y, s, x0, x1, turn):
    r = random.Random(seed)
    body = ""
    import stage
    for i in range(n):
        S = stage.random_spec(r, ("man", "man", "woman", "man"))
        S["col"] = r.choice(REDS)
        if S["head"] == "scarf":
            S["scarf_col"] = r.choice(["#5a1010", "#2a1a1a", "#7a2a1a"])
        x = r.uniform(x0, x1)
        q = pose(turn=turn + r.uniform(-0.1, 0.1), gx=turn * 2, gy=-0.4, armL="relaxed", armR="relaxed", brow=0.3)
        body += at_feet(S, q, r.uniform(0, 3), x, y + r.uniform(-8, 8), s * r.uniform(0.94, 1.06))
    return svg_render(body)

def s10():
    cy = bgs.cached("courtyard", bgs.courtyard)
    left = bgs.cached("s10_left", lambda: red_crowd(5, 8, 1450, 0.34, -40, 300, 0.4))
    right = bgs.cached("s10_right", lambda: red_crowd(6, 8, 1450, 0.34, 780, 1120, -0.4))
    heads = bgs.cached("s10_heads", lambda: back_heads(8, 8, 1760, 0.62, col="#3a0e0e", blur=3))
    def bg(t, bow=0.0):
        im = cy.copy()
        im.alpha_composite(left, (0, int(2 * math.sin(t * 2) + 14 * bow)))
        im.alpha_composite(right, (0, int(2 * math.sin(t * 2 + 1) + 14 * bow)))
        return im
    LA = [("p2s10a", 2.5), ("p2s10b", 7.8)]
    def midA(t):
        b = talk_pose(LA, t, 61, dict(turn=0.0, gx=0.0, gy=0.3, brow=0.3, armL="offer" if 7.6 < t < 10.0 else "relaxed", armR="relaxed", wind=0.3))
        k = talk_pose([], t, 62, dict(turn=-0.1, gx=-0.2, gy=0.3, furrow=0.5, armL="relaxed", armR="relaxed", wind=0.3))
        return at_feet(BANU, P(**b), t, 470, 1080, 0.42) + at_feet(BABAK_LEADER, P(**k), t, 615, 1080, 0.43)
    A = Shot(10.6, bg, midA, fg=heads, cam=cam_push(1.0, 1.14, 545, 900, 10.6), light=dict(rim=(4, -4), rim_col=(1.0, 0.85, 0.6), ramp=(0, W, 0.9, 1.05)),
             sun=(900, 300, 900, (0.08, 0.06, 0.03)), fx=[Motes(50, 13, (255, 230, 190), (0, 300, W, 1400), (6, -4))], fade_in=0.5)
    cyb = blur_bg("courtyard", bgs.courtyard, 9)
    LB = [("p2s10c", 1.2)]
    def midB(t):
        bow = ease((t - 4.2) / 0.5)
        c = talk_pose(LB, t, 63, dict(turn=0.2, gx=0.5, gy=-0.4 + 1.0 * bow, brow=0.4, nod=24 * bow, tilt=3 * bow, armL="chest" if t > 4.0 else "relaxed", armR="relaxed"))
        c["blink"] = max(c["blink"], 0.7 * bow)
        return at_neck(OLD_CHIEF, P(**c), t, 530, 1060, 1.4)
    B = Shot(4.7, cyb, midB, cam=cam_push(1.0, 1.04, 540, 900, 4.7), light=dict(rim=(4, -4), rim_col=(1.0, 0.85, 0.6), ramp=(0, W, 0.9, 1.05)),
             sun=(900, 300, 900, (0.08, 0.06, 0.03)))
    def midC(t):
        b = talk_pose([], t, 64, dict(turn=0.2, gx=0.4, gy=0.4, smile=0.4, armL="relaxed", armR="relaxed", wind=0.3))
        k = talk_pose([], t, 65, dict(turn=0.0, gx=0.0, gy=0.4, furrow=0.6, armL="fist_up" if t > 1.2 else "relaxed", armR="relaxed", wind=0.3))
        return at_feet(BANU, P(**b), t, 470, 1080, 0.42) + at_feet(BABAK_LEADER, P(**k), t, 615, 1080, 0.43)
    C = Shot(3.7, lambda t: bg(t, ease(t / 0.8)), midC, fg=lambda t: _shift(heads, int(18 * ease(t / 0.8))), cam=cam_push(1.14, 1.06, 545, 900, 3.7),
             light=dict(rim=(4, -4), rim_col=(1.0, 0.85, 0.6), ramp=(0, W, 0.9, 1.05)), sun=(900, 300, 900, (0.08, 0.06, 0.03)), fade_out=0.5)
    return [A, B, C]

def _shift(img, dy):
    im = Image.new("RGBA", img.size); im.alpha_composite(img, (0, dy)); return im

# ================================================================ S11 the wall, the throne, the end card (96-124)
def s11():
    sky = bgs.cached("wall_sky", wallbg.wide_sky)
    wall = bgs.cached("wall_fg", lambda: wallbg.wall_fg()[0])
    close = bgs.cached("wall_close", wallbg.close_bg)
    SUNL = dict(rim=(5, -2), rim_col=(1.0, 0.7, 0.4), ramp=(0, W, 0.82, 1.06))
    def babak_wall(t, x=670):
        q = talk_pose([], t, 71, dict(turn=0.15, gx=0.65, gy=-0.1, furrow=0.8, armL=("ik", 70, 300), armR=("ik", -70, 300), wind=1.0))
        q["blink"] = max(0.2, q["blink"])
        return at_neck(BABAK, P(**q), t, x, 995, 0.85)
    def midA(t):
        return birds(t) + banner_svg(t, 435, 560, 330, 210) + babak_wall(t)
    A = Shot(2.8, sky, midA, fg=wall, cam=cam_push(1.0, 1.04, 640, 1080, 2.8), light=SUNL, sun=(900, 1000, 700, (0.10, 0.06, 0.02)),
             fx=[Motes(50, 14, (255, 226, 180), (0, 300, W, 1500), (-22, 0))], fade_in=0.5)
    LB = [("p2s11a", 0.2)]
    def midB(t):
        u = t - 0.2
        lift = ease((u - 1.35) / 0.5) if u > 1.35 else 0.0
        q = talk_pose(LB, t, 72, dict(turn=0.24, gx=0.55, gy=-0.15 - 0.2 * lift, furrow=0.85 - 0.35 * lift, brow=0.1 + 0.6 * lift, nod=-7 * lift, tilt=-2.2 * lift,
                                      armL="relaxed", armR="relaxed", wind=0.9))
        q["blink"] = max(0.22 - 0.12 * lift, q["blink"])
        return at_neck(BABAK, P(**q), t, 470, 1060, 2.0)
    B = Shot(3.5, close, midB, cam=cam_push(1.0, 1.035, 470, 820, 3.5), light=dict(rim=(6, -2), rim_col=(1.0, 0.7, 0.4), ramp=(0, W, 0.8, 1.06)),
             sun=(880, 1180, 900, (0.10, 0.06, 0.02)), fx=[Motes(50, 15, (255, 226, 180), (0, 300, W, 1500), (-22, 0))])
    def midC(t):
        bq = talk_pose([], t, 73, dict(turn=-0.2, gx=-0.5, gy=0.0, smile=0.3, armL="relaxed", armR="relaxed", wind=0.8))
        return birds(t, 300, 480) + banner_svg(t, 435, 560, 330, 210) + babak_wall(t) + at_neck(BANU, P(**bq), t, 905, 1010, 0.82)
    C = Shot(7.7, sky, midC, fg=wall, cam=cam_push(1.0, 1.08, 700, 1050, 7.7), light=SUNL, sun=(900, 1000, 700, (0.10, 0.06, 0.02)),
             fx=[Motes(50, 16, (255, 226, 180), (0, 300, W, 1500), (-22, 0))])
    th = bgs.cached("throne_hall", bgs.throne_hall)
    def midD(t):
        sway = 10 * math.sin(t * 0.9)
        x0, x1, top, bot = 470, 610, 330, 720
        d = (f"M {x0} {top} L {x1} {top} L {x1 + sway:.1f} {bot - 40} L {(x0 + x1) / 2 + sway:.1f} {bot} L {x0 + sway:.1f} {bot - 40} Z")
        return (f'<rect x="{x0 - 30}" y="{top - 14}" width="{x1 - x0 + 60}" height="14" rx="6" fill="#3a3040"/>'
                f'<path d="M {x0 - 20} {top - 14} L 540 150 L {x1 + 20} {top - 14}" stroke="#2a2430" stroke-width="4" fill="none"/>'
                f'<path d="{d}" fill="#050406" stroke="#2a2430" stroke-width="3"/>')
    D = Shot(7.0, th, midD, cam=cam_push(1.0, 1.15, 540, 1000, 7.0), light=dict(rim=(0, -4), rim_col=(0.9, 0.85, 0.75), rim_str=0.5),
             fx=[Motes(90, 17, (240, 226, 200), (360, 200, 760, 1350), (3, 6), amax=120)], grade="night", fade_in=0.4, fade_out=0.6)
    E = bazz_shot(7.0, "rise", 40, fade_in=0.6, fade_out=0.8, riders=False, cam=cam_push(1.0, 1.04, 620, 1000, 7.0))
    return [A, B, C, D, E]

SCENES = {"s7": s7, "s8": s8, "s9": s9, "s10": s10, "s11": s11}
