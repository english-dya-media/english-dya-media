"""Part 6 · The Fall of Bazz (episode 3, half 2) — 2D cartoon. Timing matches p06_audio.py:
s1 0-6.6 Bazz burning (hook) · s2 6.6-11.2 title · s3 11.2-36.6 still standing: Bugha in the mist, the letter to Byzantium, the side gate ·
s4 36.6-73.4 the fall of Bazz, 15 August 837 · s5 73.4-100.8 two letters in the forest · s6 100.8-124.4 bread; Sahl's gate in Armenia."""
import math, random
from PIL import Image, ImageFilter, ImageDraw, ImageEnhance
from film import Shot, W, H, ease, lerp, talk_pose, blink_at, cam_push, cam_static, Snow, Motes, Embers, svg_render
from chars import pose, horse, cow, Ctx, FEET, fmt
from stage import at_neck, at_feet, back_heads, fire_svg, rider, Glow, lw_for, glow_img
import bgs, wallbg
from cast import *
from p01_scenes import P, blur_bg, WARM
from p02_scenes import bazz_shot, banner_svg
from p03_scenes import NOON, NOON_SUN, enemy_spec, column, villager_spec, pole_flag, sil, DUSTDEF
from p05_scenes import jitter, flame, glow, GLOWDEF, smoke, MOON, DAWN, TORCH

ORANGE = dict(ambient=(0.92, 0.82, 0.78), rim=(5, -3), rim_col=(1.0, 0.55, 0.25), rim_str=1.0, ramp=(0, W, 0.85, 1.08))
CANDLE = dict(point=(540, 520, 1150, 0.55, 1.15, (1.0, 0.6, 0.3)), rim=(0, -4), rim_col=(1.0, 0.72, 0.42), rim_str=0.7)
CLOSE_CANDLE = dict(rim=(0, -4), rim_col=(1.0, 0.7, 0.4), rim_str=0.8, ramp=(0, W, 0.9, 1.0))
FOREST = dict(rim=(4, -3), rim_col=(0.95, 0.95, 0.85), rim_str=0.6, ambient=(0.92, 0.97, 0.95), ramp=(0, W, 0.9, 1.04))
TOWERS = [(485, 610), (630, 580), (765, 630)]


def ride(S, q, t, x, y, s, col, k=0, gallop=False, flip=False, blanket=None, head_down=0.0):
    return rider(S, q, t, lambda c: horse(c, col=col, mane="#0a0808", walk=gallop, phase=t * (9.0 if gallop else 4.0) + k, t=t + k,
                                         blanket=blanket, head_down=head_down), x, y, s, flip=flip)


def falling_banner(t, x, y, t0, k=0):
    """a red banner on a tower: it sways, then (after t0) tips over and drops behind the wall"""
    a = ease((t - t0) / 0.7) if t0 is not None else 0.0
    drop = 160 * max(0.0, t - t0 - 0.5) ** 2 * 6 if t0 is not None and t > t0 + 0.5 else 0.0
    if drop > 400:
        return ""
    top = y - 96
    pts_t = [(x + 3 + 56 * u, top + 6 * math.sin(t * 5 - u * 6 + k) * u) for u in [i / 8 for i in range(9)]]
    pts_b = [(x + 3 + 54 * u, top + 38 + 6 * math.sin(t * 5 - u * 6 + k) * u + 4 * u) for u in [i / 8 for i in range(8, -1, -1)]]
    return (f'<g transform="translate(0,{drop:.1f}) rotate({-80 * a:.1f},{x:.1f},{y:.1f})">'
            f'<rect x="{x - 3}" y="{top - 6}" width="6" height="{y - top + 6}" fill="#1e1a26"/>'
            f'<path d="M ' + " L ".join(f"{px:.1f} {py:.1f}" for px, py in pts_t + pts_b) + ' Z" fill="#b5161b" stroke="#2a0a0a" stroke-width="2"/></g>')


def bazz_burning(dur, fall=(0.8, 1.6, 2.4), cam=None, fade_in=0.4, fade_out=0.0, smoke_a=1.0):
    """Bazz at dusk with smoke rising and its red banners falling"""
    base = bgs.cached("bazz_dusk", lambda: bgs.bazz("dusk"))
    back = bgs.cached("cloud_back_dusk", lambda: bgs.cloud_sea(1180, 30))
    front = bgs.cached("cloud_front_dusk", lambda: bgs.cloud_sea(1330, 31, hi="#fffaf6", mid="#f0e4e6", lo="#d7cfe0"))
    def bg(t):
        im = base.copy(); im.alpha_composite(back, (int(-300 + 5 * t), 0)); return im
    def mid(t):
        o = DUSTDEF + GLOWDEF
        for k, (x, y) in enumerate([(520, 700), (640, 640), (760, 690), (600, 760)]):
            o += glow(x, y + 20, 120, 0.7 + 0.3 * math.sin(t * 7 + k))
        for k, (x, y, s) in enumerate([(520, 690, 0.9), (650, 620, 1.2), (760, 680, 0.8), (590, 760, 0.7)]):
            o += smoke(t + 3 * k, x, y, 860 + k, s * 1.1, n=8, col="#4a3e44", a=0.7 * smoke_a)
        for k, ((x, y), t0) in enumerate(zip(TOWERS, fall)):
            o += falling_banner(t, x, y, t0, k)
        return o
    def fg(t):
        im = Image.new("RGBA", (W, H)); im.alpha_composite(front, (int(-300 - 9 * t), 0)); return im
    return Shot(dur, bg, mid, fg=[fg], cam=cam or cam_push(1.0, 1.08, 620, 760, dur), light=dict(rim=(0, 0)), sun=(240, 1120, 700, (0.12, 0.06, 0.03)),
                fade_in=fade_in, fade_out=fade_out, fx=[Embers(60, 861, (430, 560, 820, 820), (40, 110))])


def orange_tint(a0=0.0, a1=1.0, dur=1.0):
    def fx(im, t):
        a = lerp(a0, a1, ease(t / dur))
        im.alpha_composite(Image.new("RGBA", (W, H), (255, 110, 40, int(30 * a + 6 * a * math.sin(t * 8)))))
    return fx


# ================================================================ S1 the hook: Bazz burning (0-6.6)
def s1():
    A = bazz_burning(3.8, fall=(1.0, 1.7, 2.5), fade_in=0.5)
    rvb = blur_bg("ridge_view", bgs.ridge_view, 8)
    def midB(t):
        turn = ease((t - 0.5) / 0.6)
        q = P(turn=0.3 - 0.6 * turn, gx=0.6 - 1.3 * turn, gy=-0.1, brow=0.2 + 0.7 * turn, furrow=0.6 - 1.0 * turn, mouth_o=0.15 * turn, wind=0.9,
              armL="relaxed", armR="relaxed", blink=blink_at(t, 862))
        return at_neck(BABAK, q, t, 540, 1075, 1.2)
    B = Shot(2.8, rvb, midB, cam=cam_push(1.0, 1.05, 540, 860, 2.8), light=ORANGE, sun=(900, 700, 800, (0.16, 0.06, 0.01)), grade="fire",
             fx=[orange_tint(0.3, 1.0, 1.0)], fade_out=0.5)
    return [A, B]


# ================================================================ S2 title (6.6-11.2)
def s2():
    return [bazz_shot(4.6, "dusk", 30, fade_in=0.4, fade_out=0.5)]


# ================================================================ S3 still standing (11.2-36.6)
def fog_layer():
    tex = bgs.cached("fog_tex", lambda: svg_render("".join(
        f'<ellipse cx="{random.Random(i).uniform(-200, 1700):.0f}" cy="{random.Random(i + 50).uniform(900, 1500):.0f}" rx="{random.Random(i + 9).uniform(200, 420):.0f}" ry="{random.Random(i + 3).uniform(50, 110):.0f}" fill="#d8dee4" opacity="0.5"/>'
        for i in range(26)), 1700, H).filter(ImageFilter.GaussianBlur(30)))
    soft = tex.copy(); soft.putalpha(tex.getchannel("A").point(lambda v: int(v * 0.6)))
    def fx(im, t):
        im.alpha_composite(soft.crop((int(300 + 30 * t), 0, int(300 + 30 * t) + W, H)))
        im.alpha_composite(Image.new("RGBA", (W, H), (220, 226, 232, 40)))
    return fx


def s3():
    floor = bgs.cached("gorge_floor_dust", lambda: bgs.gorge_floor("dust"))
    walls = bgs.cached("gorge_walls_dust", lambda: bgs.gorge_walls("dust"))
    GREYL = dict(rim=(4, -2), rim_col=(0.9, 0.9, 0.95), rim_str=0.5, ambient=(0.9, 0.9, 0.95), ramp=(0, W, 0.92, 1.03))
    # A: Bugha's column marches into the mist
    def midA(t):
        o = column(t, 1300, 0.235, 9, 871, banners=(2, 6), ph0=0.0) + column(t, 1430, 0.30, 7, 872, banners=(3,), ph0=1.0, speed=56)
        q = P(turn=0.45, gx=0.8, gy=0.0, furrow=0.6, armR="forward", armL="forward", wind=0.6, legs="none", blink=blink_at(t, 873))
        o += ride(BUGHA, q, t, lerp(300, 520, ease(t / 4.6)), 1560, 0.62, "#1e1a1c", gallop=True, blanket="#121216")
        return o
    A = Shot(4.6, floor, midA, fg=walls, cam=cam_push(1.0, 1.05, 540, 1250, 4.6), light=GREYL, fx=[fog_layer()], fade_in=0.6)
    # B: Babak's men come down out of the mist; the column breaks and runs
    r = random.Random(874)
    reds = [(r.choice([FIGHTER, FIGHTER2, villager_spec(r, red=True), villager_spec(r, red=True)]), 1250 + 140 * k, 1330 + 60 * (k % 3), 0.3 + 0.04 * (k % 3), r.uniform(0, 6)) for k in range(7)]
    blacks = [(enemy_spec(r), 200 + 120 * k, 1340 + 50 * (k % 3), 0.28 + 0.04 * (k % 3), r.uniform(0, 6)) for k in range(7)]
    def midB(t):
        items = []
        for S, x0, y, sc, ph in blacks:
            run = ease((t - 0.6) / 0.4)
            x = x0 + 50 * t * (1 - run) - 320 * max(0.0, t - 0.6) * run
            q = P(legs="walk", phase=t * (6 + 6 * run) + ph, turn=0.45 if run < 0.5 else -0.45, gx=0.7 if run < 0.5 else -0.8, brow=0.8 * run, furrow=0.5 - 1.0 * run,
                  mouth_o=0.35 * run, armL=("ik", 250, 560), propL="pike" if run < 0.5 else None, armR="relaxed", wind=0.6, blink=blink_at(t, int(ph * 10)))
            items.append((y, at_feet(S, q, t, x, y, sc)))
        for S, x0, y, sc, ph in reds:
            x = x0 - 330 * t
            q = P(legs="walk", phase=t * 11 + ph, turn=-0.45, gx=-0.8, furrow=0.8, mouth_o=0.4, wind=0.8, armL=("ik", 300, -480), propL="spear_red", armR="relaxed",
                  blink=blink_at(t, int(ph * 10) + 1))
            items.append((y, at_feet(S, q, t, x, y, sc)))
        return "".join(svg for y, svg in sorted(items, key=lambda v: v[0]))
    B = Shot(4.4, floor, midB, fg=walls, cam=lambda t: (1.04, 540, 1250, 4 * math.sin(t * 13), 3 * math.sin(t * 11)), light=GREYL, fx=[fog_layer()])
    # C: Bugha turns his horse and flees into the mist; his banner lies in the dust
    def midC(t):
        o = '<g transform="rotate(-84,700,1500)">' + pole_flag(t * 0.2, 700, 1100, 400, 160, 90) + '</g>'
        q = P(turn=-0.45, gx=-0.8, gy=0.0, brow=0.7, furrow=-0.4, mouth_o=0.2, armR="forward", armL="forward", wind=1.0, legs="none", blink=blink_at(t, 875))
        o += ride(BUGHA, q, t, 760 - 300 * t, 1520, 0.6, "#1e1a1c", gallop=True, flip=True, blanket="#121216")
        return o
    C = Shot(2.8, floor, midC, fg=walls, cam=cam_push(1.0, 1.04, 540, 1250, 2.8), light=GREYL, fx=[fog_layer()], fade_out=0.5)
    # D1: Bazz by candlelight: Babak writes, Banu waits with the seal
    wr = bgs.cached("war_room", bgs.war_room)
    table = bgs.cached("war_table6", _table6)
    def midD1(t):
        b = P(turn=0.15, gx=0.3, gy=0.8, furrow=0.6, nod=6, armL=("ik", 160 + 30 * math.sin(t * 6), 420), armR=("ik", -120, 420), blink=blink_at(t, 876))
        n = P(turn=-0.3, gx=-0.6, gy=0.6, furrow=0.2, smile=0.1, armL="relaxed", armR=("ik", -180, 400), blink=blink_at(t, 877))
        return at_neck(BABAK, b, t, 430, 905, 0.62) + at_neck(BANU, n, t, 720, 915, 0.6)
    D1 = Shot(2.2, wr, midD1, fg=table, cam=cam_push(1.0, 1.04, 560, 1000, 2.2), light=CANDLE, grade="fire", fade_in=0.5)
    # D1b: the letter on the table; her hand presses the seal into red wax (voice: "Will the Byzantine emperor help us?")
    tm = bgs.cached("table_plain", lambda: _table_top())
    def midD1b(t):
        o = ('<g transform="rotate(-6,540,980)"><rect x="300" y="700" width="480" height="560" rx="10" fill="#efe2c2" stroke="#3a2a14" stroke-width="5"/>' +
             "".join(f'<path d="M 340 {760 + 40 * k} C 420 {752 + 40 * k}, 560 {768 + 40 * k}, {740 - 30 * (k % 3)} {758 + 40 * k}" stroke="#4a3a2a" stroke-width="5" fill="none" opacity="0.7"/>' for k in range(10)) +
             '</g>')
        press = ease((t - 0.9) / 0.35) * (1 - ease((t - 1.7) / 0.4))
        wax = ease((t - 0.5) / 0.4)
        if wax > 0:
            o += f'<ellipse cx="560" cy="1150" rx="{70 * wax:.0f}" ry="{58 * wax:.0f}" fill="#a8141a" stroke="#4a0606" stroke-width="4"/>'
        if t > 1.3:
            o += ('<circle cx="560" cy="1150" r="40" fill="none" stroke="#7a0a0e" stroke-width="5"/>'
                  '<path d="M 540 1150 L 580 1150 M 560 1130 L 560 1170" stroke="#7a0a0e" stroke-width="5"/>')
        hx, hy = 560, lerp(900, 1130, press) if t < 1.9 else lerp(1130, 860, ease((t - 1.9) / 0.6))
        o += (f'<g transform="translate({hx},{hy:.1f})">'
              f'<rect x="-26" y="-20" width="52" height="40" rx="8" fill="#6a4a2a" stroke="#1b0f0a" stroke-width="4"/>'
              f'<path d="M -60 -30 L 60 -30 L 50 -160 L -50 -160 Z" fill="#c98a5e" stroke="#1b0f0a" stroke-width="5"/>'
              f'<path d="M -70 -150 L 70 -150 L 90 -900 L -90 -900 Z" fill="#7a1a22" stroke="#1b0f0a" stroke-width="5"/>'
              f'<rect x="-74" y="-200" width="148" height="40" rx="10" fill="#e0b25a" stroke="#1b0f0a" stroke-width="4"/></g>')
        return o
    D1b = Shot(2.8, tm, midD1b, cam=cam_push(1.0, 1.05, 540, 1000, 2.8), light=dict(rim=(0, 0)), sun=(540, 900, 800, (0.10, 0.06, 0.02)), grade="fire")
    # D2: "If he is wise. If not, we will help ourselves."
    wrb = blur_bg("war_room", bgs.war_room, 9)
    LD2 = [("p6s3b", 0.4), ("p6s3c", 2.2)]
    def midD2(t):
        q = talk_pose(LD2, t, 878, dict(turn=0.1, gx=0.3, gy=0.0, furrow=0.6, smile=0.15 * ease((t - 3.9) / 0.5), brow=0.1, armL="relaxed", armR="relaxed"))
        return at_neck(BABAK, P(**q), t, 540, 1075, 1.2)
    D2 = Shot(4.6, wrb, midD2, cam=cam_push(1.0, 1.04, 540, 860, 4.6), light=CLOSE_CANDLE, sun=(540, 500, 700, (0.10, 0.06, 0.02)), grade="fire")
    # E: the side gate opens and a rider slips out into the night
    sg = bgs.cached("side_gate_night", bgs.side_gate_night)
    def midE(t):
        o = GLOWDEF + glow(600, 1060, 200, 0.9) + flame(600, 1080, 0.5, t, 1)
        op = ease((t - 0.2) / 0.8)
        w = 210 * (1 - 0.85 * op)
        o += f'<path d="M 320 1440 L 320 1130 Q {320 + w * 0.5:.0f} {1130 - 120 * (w / 210):.0f}, {320 + w:.0f} {1130 - 40 * (w / 210):.0f} L {320 + w:.0f} 1440 Z" fill="#3a2414" stroke="#140a04" stroke-width="5"/>'
        u = ease((t - 1.0) / 2.6)
        if t > 1.0:
            q = P(turn=0.45, gx=0.8, furrow=0.6, armR="forward", armL="forward", wind=0.8, legs="none", blink=blink_at(t, 879))
            o += ride(dict(MESSENGER, head="scarf", hair="none", scarf_col="#2a2a30", scarf_edge="#4a4a50"), q, t, lerp(420, 1250, u), lerp(1440, 1600, u), lerp(0.26, 0.4, u),
                      "#2a201c", gallop=True)
        return o
    E = Shot(4.0, sg, midE, cam=cam_push(1.0, 1.04, 540, 1250, 4.0), light=dict(MOON, rim_col=(1.0, 0.7, 0.45)), grade="night", fade_out=0.8)
    return [A, B, C, D1, D1b, D2, E]


def _table6():
    s = ('<defs><linearGradient id="wt" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8a5a30"/><stop offset="1" stop-color="#4a2a14"/></linearGradient></defs>'
         '<path d="M 20 1100 L 1060 1100 L 1140 1560 L -60 1560 Z" fill="url(#wt)" stroke="#1b0f0a" stroke-width="6"/>' +
         "".join(f'<path d="M {20 - k * 9} {1100 + k * 52} L {1060 + k * 9} {1100 + k * 52}" stroke="#3a2010" stroke-width="3" opacity="0.5"/>' for k in range(1, 9)) +
         '<g transform="rotate(-4,520,1180)"><rect x="390" y="1130" width="240" height="110" rx="6" fill="#efe2c2" stroke="#3a2a14" stroke-width="4"/>' +
         "".join(f'<path d="M 410 {1150 + 18 * k} L {600 - 20 * (k % 2)} {1150 + 18 * k}" stroke="#4a3a2a" stroke-width="3" opacity="0.6"/>' for k in range(5)) + '</g>'
         '<rect x="760" y="1150" width="40" height="70" rx="6" fill="#efe6d0"/><path d="M 780 1150 C 770 1130, 790 1120, 780 1100" stroke="#ffd080" stroke-width="10" fill="none"/>'
         '<path d="M -60 1560 L 1140 1560 L 1140 1920 L -60 1920 Z" fill="#2e1a0c"/><path d="M -60 1560 L 1140 1560" stroke="#a87444" stroke-width="8"/>')
    return svg_render(s)


def _table_top():
    s = "<defs>" + bgs.FILTERS + bgs.rg("lt", 520, 900, 1100, [(0, "#a06a3a", 1), (0.6, "#6a4222", 1), (1, "#2e1a0c", 1)]) + "</defs>"
    s += f'<rect width="{W}" height="{H}" fill="url(#lt)"/>'
    r = random.Random(880)
    for k in range(11):
        y = k * 180 + r.uniform(-10, 10)
        s += f'<path d="M 0 {y:.0f} L 1080 {y + r.uniform(-8, 8):.0f}" stroke="#1e1006" stroke-width="7" opacity="0.7"/>'
    return svg_render(s)


# ================================================================ S4 the fall of Bazz, 15 August 837 (36.6-73.4)
def s4():
    # A: Afshin's army at the foot of Bazz
    ac = bgs.cached("army_camp", bgs.army_camp)
    def midA(t):
        o = ('<path d="M 260 1010 L 420 760 L 470 620 L 520 560 L 640 560 L 690 640 L 760 760 L 900 1010 Z" fill="#5a4a5a"/>'
             '<path d="M 260 1010 L 420 760 L 470 620 L 520 560 L 560 700 L 520 1010 Z" fill="#7a6a76" opacity="0.6"/>'
             '<rect x="500" y="500" width="160" height="64" fill="#2a2430"/><rect x="490" y="460" width="40" height="104" fill="#2a2430"/><rect x="630" y="470" width="40" height="94" fill="#2a2430"/>'
             + "".join(f'<rect x="{500 + 18 * i}" y="490" width="9" height="12" fill="#2a2430"/>' for i in range(9)))
        for k, (x, y) in enumerate([(510, 462), (650, 472)]):
            o += f'<rect x="{x - 2}" y="{y - 60}" width="4" height="60" fill="#1e1a26"/><path d="M {x + 2} {y - 58} l 34 {4 + 3 * math.sin(t * 5 + k):.1f} l -2 18 l -32 -4 Z" fill="#b5161b"/>'
        for k in range(14):
            x = (k * 90 + 30 * t) % 1300 - 100
            o += sil(x, 1235 + 12 * (k % 2), 0.42, t, k * 0.7, col="#18181e")
        for k in range(10):
            x = 1180 - ((k * 130 + 24 * t) % 1400)
            o += sil(x, 1330 + 10 * (k % 2), 0.55, t, k * 1.1, col="#141418", d=-1)
        return o + pole_flag(t, 160, 1080, 420, 160, 90) + pole_flag(t, 930, 1100, 420, 160, 90)
    A = Shot(4.4, ac, midA, cam=cam_push(1.0, 1.05, 560, 1000, 4.4), light=dict(rim=(0, 0)), sun=(900, 500, 900, (0.10, 0.07, 0.03)), fade_in=0.5)
    # B: on two ridges across a narrow valley, Babak and Afshin face each other
    rv = bgs.cached("ridge_view", bgs.ridge_view)
    def midB(t):
        o = ""
        for k, x in enumerate((900, 980)):
            q = P(turn=-0.4, gx=-0.8, furrow=0.5, armR="forward", armL="relaxed", legs="none", blink=blink_at(t, 881 + k))
            o += ride(enemy_spec(random.Random(882 + k)), q, t, x, 1052, 0.2, ["#2a2420", "#16141a"][k], k=k, flip=True, blanket="#121216")
        o += pole_flag(t, 1010, 860, 190, 90, 50, d=-1)
        a = P(turn=-0.4, gx=-0.8, furrow=0.4, armR="forward", armL="relaxed", legs="none", blink=blink_at(t, 883))
        o += ride(AFSHIN, a, t, 800, 1046, 0.24, "#3a2a1e", flip=True, blanket="#121216")
        b = P(turn=0.4, gx=0.8, gy=-0.1, furrow=0.7, armR="forward", armL="relaxed", legs="none", wind=0.8, blink=blink_at(t, 884))
        o += ride(BABAK, b, t, 250, 1660, 0.82, "#5a3a22", blanket="#8a1a1a")
        return o
    B = Shot(5.0, rv, midB, cam=cam_push(1.0, 1.04, 540, 1200, 5.0), light=dict(rim=(5, -2), rim_col=(1.0, 0.82, 0.55)), sun=(880, 760, 700, (0.12, 0.07, 0.03)))
    # C: Afshin: "It is over, Babak. Come down, and live."
    rvb = blur_bg("ridge_view", bgs.ridge_view, 8)
    LC = [("p6s4a", 0.5), ("p6s4b", 2.2)]
    def midC(t):
        q = talk_pose(LC, t, 885, dict(turn=-0.25, gx=-0.6, gy=0.1, furrow=0.4, brow=0.0, smile=0.1, armL="relaxed", armR="relaxed", wind=0.6))
        return at_neck(AFSHIN, P(**q), t, 560, 1075, 1.18)
    C = Shot(4.6, rvb, midC, cam=cam_push(1.0, 1.04, 560, 860, 4.6), light=dict(rim=(5, -2), rim_col=(1.0, 0.82, 0.55), ramp=(0, W, 0.9, 1.05)),
             sun=(880, 760, 700, (0.12, 0.07, 0.03)))
    # D: behind Babak's back, soldiers climb into the fortress
    wo = bgs.cached("wall_outside", bgs.wall_outside)
    ladders = [(150, 0.0), (400, 0.7), (660, 0.3), (920, 1.1)]
    def ladder(x):
        return (f'<path d="M {x - 34} 1960 L {x - 24} 800 M {x + 34} 1960 L {x + 24} 800" stroke="#4a3018" stroke-width="10"/>' +
                "".join(f'<path d="M {x - 33 + 0.6 * k:.0f} {1910 - 56 * k} L {x + 33 - 0.6 * k:.0f} {1910 - 56 * k}" stroke="#4a3018" stroke-width="7"/>' for k in range(20)))
    def climber(x, y, t, ph):
        """a soldier seen from behind on a ladder: dark back, helmet, arms reaching up"""
        a = math.sin(t * 7 + ph)
        return (f'<path d="M {x - 26} {y + 70} L {x - 22 - 6 * a:.0f} {y + 150} M {x + 26} {y + 70} L {x + 22 + 6 * a:.0f} {y + 150}" stroke="#16161c" stroke-width="16" stroke-linecap="round"/>'
                f'<path d="M {x - 38} {y - 10} L {x - 30} {y + 80} L {x + 30} {y + 80} L {x + 38} {y - 10} Z" fill="#1e1e26"/>'
                f'<path d="M {x - 34} {y} L {x - 40 + 8 * a:.0f} {y - 80 - 20 * a:.0f} M {x + 34} {y} L {x + 40 - 8 * a:.0f} {y - 80 + 20 * a:.0f}" stroke="#1e1e26" stroke-width="15" stroke-linecap="round"/>'
                f'<circle cx="{x}" cy="{y - 34}" r="25" fill="#16161c"/><path d="M {x - 27} {y - 38} C {x - 24} {y - 76}, {x + 24} {y - 76}, {x + 27} {y - 38} Z" fill="#6a6e7a"/>')
    def midD(t):
        o = DUSTDEF
        for k, (x, y) in enumerate([(300, 760), (700, 740), (980, 780)]):
            o += smoke(t + 2 * k, x, y, 890 + k, 1.4, n=8, col="#3a3438", a=0.75)
        o += falling_banner(t, 640, 806, 2.6, 1).replace('fill="#1e1a26"', 'fill="#3a2414"')
        for k, (x, d) in enumerate(ladders):
            o += ladder(x)
            for j in range(2):
                u = ((t + d + 2.1 * j) / 4.2) % 1.0
                o += climber(x, lerp(1800, 860, u), t, j + k)
        return o
    D = Shot(4.2, wo, midD, cam=cam_push(1.0, 1.05, 540, 1100, 4.2), light=dict(rim=(0, -3), rim_col=(1.0, 0.75, 0.5), ambient=(0.9, 0.86, 0.84)),
             sun=(540, 300, 900, (0.08, 0.04, 0.02)), fx=[Embers(40, 896, (0, 700, W, 1000), (40, 120))])
    # E: the red banners fall over Bazz
    E = bazz_burning(3.0, fall=(0.4, 1.0, 1.6), cam=cam_push(1.1, 1.2, 620, 700, 3.0), fade_in=0.0)
    # F: Babak turns and sees the smoke
    def midF(t):
        turn = ease((t - 0.3) / 0.6)
        q = P(turn=0.3 - 0.65 * turn, gx=0.6 - 1.4 * turn, gy=-0.2, brow=0.1 + 0.8 * turn, furrow=0.7 - 1.2 * turn, mouth_o=0.2 * turn, wind=0.9,
              armL="relaxed", armR="relaxed", blink=blink_at(t, 897))
        return at_neck(BABAK, q, t, 540, 1075, 1.2)
    F = Shot(2.6, rvb, midF, cam=cam_push(1.0, 1.05, 540, 860, 2.6), light=ORANGE, sun=(900, 700, 800, (0.16, 0.06, 0.01)), grade="fire", fx=[orange_tint(0.2, 1.0, 0.9)])
    # G: Abdullah gallops up
    def midG(t):
        b = P(turn=-0.4, gx=-0.8, furrow=0.8, brow=0.5, armR="forward", armL="relaxed", legs="none", wind=0.8, blink=blink_at(t, 898))
        o = ride(BABAK, b, t, 300, 1560, 0.6, "#5a3a22", blanket="#8a1a1a")
        u = ease(t / 1.8)
        a = P(turn=-0.45, gx=-0.8, brow=0.8, furrow=-0.3, mouth_o=0.3, armR="forward", armL=("ik", 300, -200) if t > 1.6 else "relaxed", legs="none", wind=1.0,
              blink=blink_at(t, 899))
        o += ride(ABDULLAH, a, t, lerp(1300, 800, u), 1600, 0.62, "#3a2a1e", gallop=u < 1, flip=True, blanket="#8a1a1a")
        return o
    G = Shot(2.6, rvb, midG, cam=cam_push(1.0, 1.03, 540, 1200, 2.6), light=dict(rim=(5, -2), rim_col=(1.0, 0.7, 0.4)), sun=(880, 760, 700, (0.12, 0.07, 0.03)),
             fx=[orange_tint(0.5, 0.6, 1.0)])
    # H: "Brother, they are inside Bazz! If you die here, everything dies with you."
    LH = [("p6s4c", 0.3), ("p6s4d", 2.4)]
    def midH(t):
        q = talk_pose(LH, t, 900, dict(turn=-0.2, gx=-0.5, gy=0.0, brow=0.7, furrow=-0.4, sad=0.15, wind=0.9, armL="relaxed", armR="relaxed"))
        return at_neck(ABDULLAH, P(**q), t, 540, 1075, 1.2)
    H_ = Shot(5.6, rvb, midH, cam=cam_push(1.0, 1.05, 540, 860, 5.6), light=ORANGE, sun=(900, 700, 800, (0.14, 0.06, 0.01)), grade="fire", fx=[orange_tint(0.6, 0.6, 1.0)])
    # I: the next morning, Afshin's men pull down the palaces of Bazz
    cy = bgs.cached("courtyard", bgs.courtyard)
    def palace(t):
        fall = ease((t - 2.0) / 1.0)
        x0, y0 = 120, 1310
        body = ('<rect x="120" y="760" width="420" height="550" fill="#9a6c48" stroke="#2a180e" stroke-width="5"/>'
                '<path d="M 160 1310 L 160 1060 Q 220 980, 280 1060 L 280 1310 Z M 380 1310 L 380 1060 Q 440 980, 500 1060 L 500 1310 Z" fill="#3a2414"/>'
                '<path d="M 180 900 L 180 840 Q 230 790, 280 840 L 280 900 Z M 380 900 L 380 840 Q 430 790, 480 840 L 480 900 Z" fill="#3a2414"/>'
                '<path d="M 230 760 Q 330 600, 430 760 Z" fill="#b08458" stroke="#2a180e" stroke-width="5"/>'
                '<rect x="120" y="740" width="420" height="24" fill="#7a5034"/>')
        if fall >= 1.0:
            return ""
        return f'<g transform="translate({60 * fall:.1f},{300 * fall * fall:.1f}) rotate({28 * fall:.1f},540,1310)" opacity="{1 - 0.9 * fall:.2f}">{body}</g>'
    def midI(t):
        o = DUSTDEF
        for k, x in enumerate((388, 708)):      # Afshin's black banners now hang where Babak's red ones were
            wv = 4 * math.sin(t * 3 + k)
            o += f'<path d="M {x - 4} 374 l 124 16 l -8 {80 + wv:.1f} l 8 {80 - wv:.1f} l -124 -16 Z" fill="#121216" stroke="#000" stroke-width="2"/>'
        o += palace(t)
        pull = 0.5 + 0.5 * math.sin(t * 4)
        for k, (x, y) in enumerate([(600, 1560), (730, 1600), (860, 1570)]):
            lean = 10 * pull if t < 2.2 else 0
            q = P(turn=0.4, gx=-0.6, gy=-0.4, furrow=0.9, mouth_o=0.3 * pull, armL=("ik", -260, 300), armR=("ik", -320, 260), blink=blink_at(t, 901 + k))
            o += f'<g transform="rotate({lean:.1f},{x},{y})">' + at_feet(enemy_spec(random.Random(902 + k)), q, t, x, y, 0.4) + '</g>'
        if t < 2.2:
            o += '<path d="M 500 790 Q 560 1100, 560 1370 L 920 1420" stroke="#8a6a3a" stroke-width="8" fill="none"/>'
        dust_a = ease((t - 2.4) / 0.4) * (1 - ease((t - 3.6) / 1.2))
        if dust_a > 0:
            rr = random.Random(903)
            for k in range(12):
                x = rr.uniform(80, 760); y = rr.uniform(1050, 1450); rad = rr.uniform(120, 240) * (1 + 0.5 * (t - 2.4))
                o += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{rad:.0f}" fill="#c8b090" opacity="{0.6 * dust_a:.2f}" filter="url(#dustblur)"/>'
        return o
    I = Shot(4.8, cy, midI, cam=lambda t: (1.0, 540, 1200, 6 * math.sin(t * 31) * ease((t - 2.4) / 0.2) * (1 - ease((t - 3.2) / 0.4)), 0.0), bg_par=1.0,
             light=dict(rim=(4, -4), rim_col=(1.0, 0.85, 0.6), ramp=(0, W, 0.9, 1.05)), sun=(900, 300, 900, (0.08, 0.06, 0.03)), fade_out=0.8)
    return [A, B, C, D, E, F, G, H_, I]


# ================================================================ S5 two letters (73.4-100.8)
def letter_svg(x, y, s=1.0, ang=0.0, sealed=False):
    """a small folded letter (or the caliph's sealed scroll) centred at (x, y)"""
    if sealed:
        return (f'<g transform="translate({x:.1f},{y:.1f}) rotate({ang:.1f}) scale({s:.3f})"><rect x="-26" y="-110" width="52" height="220" rx="18" fill="#eadbb4" stroke="#1b0f0a" stroke-width="5"/>'
                f'<rect x="-34" y="-128" width="68" height="26" rx="8" fill="#8a5a2a" stroke="#1b0f0a" stroke-width="4"/><rect x="-34" y="102" width="68" height="26" rx="8" fill="#8a5a2a" stroke="#1b0f0a" stroke-width="4"/>'
                f'<path d="M -30 -10 L 30 -10" stroke="#121216" stroke-width="10"/><circle cx="0" cy="-10" r="22" fill="#121216" stroke="#c9a24a" stroke-width="4"/></g>')
    return (f'<g transform="translate({x:.1f},{y:.1f}) rotate({ang:.1f}) scale({s:.3f})"><path d="M -60 -44 L 60 -44 L 60 44 L -60 44 Z" fill="#f2e8d0" stroke="#1b0f0a" stroke-width="5"/>'
            f'<path d="M -60 -44 L 0 6 L 60 -44" stroke="#8a7a5a" stroke-width="4" fill="none"/></g>')


def s5():
    fs = bgs.cached("forest_stream", bgs.forest_stream)
    # A: by the stream: two of Babak's own men come out of the trees
    def midA(t):
        o = ""
        f = P(turn=0.2, gx=0.4, gy=0.3, furrow=0.5, legs="sit", armL=("ik", 60, 330), armR=("ik", -60, 330), blink=blink_at(t, 911))
        o += at_neck(FIGHTER, f, t, 110, 1500 - 575 * 0.4, 0.4)
        a = P(turn=0.3, gx=0.7 * ease((t - 1.0) / 0.5), furrow=0.6, armL="relaxed", armR="hip", blink=blink_at(t, 913))
        o += at_feet(ABDULLAH, a, t, 600, 1560, 0.48)
        b = P(turn=0.35 * ease((t - 1.2) / 0.6), gx=0.8 * ease((t - 1.2) / 0.6), gy=0.1, furrow=0.7, sad=0.15, armL="relaxed", armR="relaxed",
              blink=blink_at(t, 912), breathe=math.sin(t * 2.5))
        o += at_feet(BABAK, b, t, 370, 1640, 0.55)
        for k, (S, d) in enumerate([(MESSENGER, 0.0), (dict(FIGHTER2, scarf_col="#5a2a1a"), 0.5)]):
            u = ease((t - d) / 3.2)
            q = P(legs="walk" if u < 1 else "stand", phase=t * 5.5 + k, turn=-0.4, gx=-0.8, furrow=0.3, armL="relaxed", armR="relaxed", blink=blink_at(t, 914 + k))
            o += at_feet(S, q, t, lerp(1220 + 120 * k, 860 + 110 * k, u), 1560 + 40 * k, 0.5)
        return o
    A = Shot(4.4, fs, midA, cam=cam_push(1.0, 1.04, 560, 1200, 4.4), light=FOREST, sun=(800, 400, 900, (0.06, 0.06, 0.04)), fade_in=0.6,
             fx=[Motes(40, 916, (240, 250, 230), (0, 500, W, 1500), (6, -3), amax=70)])
    # B: the messenger holds out the caliph's scroll and a small letter
    fsb = blur_bg("forest_stream", bgs.forest_stream, 9)
    LB = [("p6s5a", 0.4), ("p6s5b", 2.4), ("p6s5c", 4.8)]
    MS, MX, MY = 0.62, 560, 1660
    def midB(t):
        show_letter = ease((t - 4.6) / 0.4)
        q = talk_pose(LB, t, 917, dict(turn=-0.2, gx=-0.4, gy=0.0, furrow=0.3, brow=0.2, armR=("ik", -230, 210, "down"), armL=("ik", 230 * show_letter + 20 * (1 - show_letter), lerp(560, 210, show_letter), "down")))
        o = at_feet(MESSENGER, P(**q), t, MX, MY, MS)
        o += letter_svg(MX - 262 * MS, MY - (FEET - 175) * MS, 0.62, -12, sealed=True)
        if show_letter > 0:
            o += letter_svg(MX + 262 * MS, MY - (FEET - 190) * MS, 0.55 * show_letter, 8)
        return o
    B = Shot(6.6, fsb, midB, cam=cam_push(1.0, 1.04, 560, 1000, 6.6), light=FOREST, sun=(800, 400, 900, (0.06, 0.06, 0.04)))
    # C: Babak reads only the small letter; he pushes the sealed scroll back
    def midC(t):
        o = ""
        read = ease((t - 0.3) / 0.5); push = ease((t - 2.6) / 0.6)
        mq = P(turn=-0.35, gx=-0.7, gy=0.1, furrow=0.3, brow=0.3 * push, armR=("ik", lerp(-230, -150, push), lerp(210, 300, push), "down"), armL="relaxed", blink=blink_at(t, 918))
        o += at_feet(MESSENGER, mq, t, 800, 1660, 0.6)
        o += letter_svg(800 - lerp(250, 175, push) * 0.6, 1660 - (FEET - lerp(175, 265, push)) * 0.6, 0.6, -12, sealed=True)
        bq = P(turn=0.3, gx=0.5 - 0.3 * read + 0.6 * push, gy=0.6 * read * (1 - push), furrow=0.5 + 0.5 * ease((t - 1.4) / 0.6), brow=-0.2, sad=0.15,
               armL=("ik", 120, 120, "down"), armR=("ik", lerp(-60, 330, push), lerp(330, 220, push), "down") if t > 2.4 else "relaxed", blink=blink_at(t, 919))
        o += at_feet(BABAK, bq, t, 330, 1650, 0.62)
        o += letter_svg(330 + 132 * 0.62, 1650 - (FEET - 150) * 0.62, 0.62, 4)
        return o
    C = Shot(4.4, fsb, midC, cam=cam_push(1.0, 1.04, 540, 1000, 4.4), light=FOREST, sun=(800, 400, 900, (0.06, 0.06, 0.04)))
    # D: "Tell my son: one day as a ruler is better than forty years as a slave."
    LD = [("p6s5d", 0.4), ("p6s5e", 1.5)]
    def midD(t):
        q = talk_pose(LD, t, 920, dict(turn=0.15, gx=0.3, gy=0.0, furrow=0.8, brow=-0.1, armL="relaxed", armR="relaxed", wind=0.3))
        return at_neck(BABAK, P(**q), t, 540, 1075, 1.2)
    D = Shot(6.6, fsb, midD, cam=cam_push(1.0, 1.06, 540, 860, 6.6), light=FOREST, sun=(800, 400, 900, (0.06, 0.06, 0.04)))
    # E: to Abdullah: "Go to a friend's castle and hide. We will meet again."
    LE = [("p6s5f", 0.4), ("p6s5g", 2.9)]
    def midE(t):
        o = ""
        nod = ease((t - 4.0) / 0.3) * (1 - ease((t - 4.6) / 0.3))
        a = P(turn=-0.3, gx=-0.7, gy=0.0, furrow=0.3, sad=0.4, nod=10 * nod, armL="relaxed", armR="relaxed", blink=blink_at(t, 921))
        o += at_feet(ABDULLAH, a, t, 760, 1650, 0.62)
        b = talk_pose(LE, t, 922, dict(turn=0.3, gx=0.7, gy=0.0, furrow=0.4, sad=0.2, smile=0.2 * ease((t - 3.4) / 0.5), armL=("ik", 640, -40, "down") if t > 2.6 else "relaxed", armR="relaxed"))
        o += at_feet(BABAK, P(**b), t, 330, 1660, 0.63)
        return o
    E = Shot(5.4, fsb, midE, cam=cam_push(1.0, 1.04, 540, 1000, 5.4), light=FOREST, sun=(800, 400, 900, (0.06, 0.06, 0.04)), fade_out=0.6)
    return [A, B, C, D, E]


# ================================================================ S6 bread; Sahl's gate (100.8-124.4)
def s6():
    fd = bgs.cached("field_dawn", bgs.field_dawn)
    # A: at the edge of the forest: "Buy bread. Talk to no one."
    fdb = blur_bg("field_dawn", bgs.field_dawn, 8)
    LA = [("p6s6a", 1.2)]
    def midA(t):
        o = ""
        b = talk_pose(LA, t, 931, dict(turn=0.3, gx=0.7, gy=0.0, furrow=0.7, sad=0.25, armL=("ik", 420, 180, "down") if 0.6 < t < 1.6 else "relaxed", armR="relaxed", wind=0.3))
        b["blink"] = max(b["blink"], 0.2)
        o += at_feet(BABAK, P(**b), t, 330, 1660, 0.63)
        s = P(turn=-0.3, gx=-0.7, gy=0.0, furrow=0.2, nod=8 * ease((t - 3.0) / 0.3), armL="relaxed", armR=("ik", -180, 230, "down") if 0.9 < t < 1.8 else "relaxed",
              blink=blink_at(t, 932))
        o += at_feet(SERVANT, s, t, 760, 1660, 0.6)
        return o
    A = Shot(3.8, fdb, midA, cam=cam_push(1.0, 1.04, 540, 1000, 3.8), light=DAWN, sun=(760, 960, 800, (0.14, 0.09, 0.05)), fade_in=0.6)
    # B: the servant crosses the field to a ploughman; a rider watches from the hill
    def plough(x, y, s, t):
        return (f'<g transform="translate({x:.1f},{y:.1f}) scale({s:.3f})"><path d="M -40 -150 L 120 -10 M 120 -10 L 220 -10 M 60 -60 L 40 -150" stroke="#5a3a1c" stroke-width="14" fill="none"/>'
                f'<path d="M 120 -10 L 200 -10 L 170 20 Z" fill="#8e949e" stroke="#1b0f0a" stroke-width="4"/></g>')
    def midB(t):
        o = ""
        q = P(turn=0.0, gx=-0.3, gy=0.4, furrow=0.6, armR="forward", armL="relaxed", legs="none", blink=blink_at(t, 933))
        o += ride(enemy_spec(random.Random(934)), q, t, 880, 1032, 0.16, "#1e1a1c", flip=True, blanket="#121216")
        c = Ctx(lw_for(0.5)); px = 560 - 14 * t
        o += f'<g transform="translate({px:.1f},1350) scale(0.5)">{cow(c, col="#7a5a3e", t=t, graze=0.0)}</g>'
        o += f'<path d="M {px - 70:.1f} 1250 L {px + 150:.1f} 1300" stroke="#5a3a1c" stroke-width="6"/>' + plough(px + 120, 1352, 0.6, t)
        pq = P(legs="walk", phase=t * 4, turn=-0.4, gx=-0.7, furrow=0.5, armL=("ik", -150, 420, "down"), armR=("ik", -230, 400, "down"), blink=blink_at(t, 935))
        o += at_feet(PLOUGHMAN, pq, t, px + 290, 1360, 0.26)
        u = ease(t / 4.6)
        sq = P(legs="walk" if u < 0.98 else "stand", phase=t * 5, turn=0.4, gx=0.7, furrow=0.3, armL="relaxed", armR="relaxed", blink=blink_at(t, 936))
        o += at_feet(SERVANT, sq, t, lerp(160, 560, u), lerp(1640, 1430, u), lerp(0.42, 0.28, u))
        return o
    B = Shot(4.6, fd, midB, cam=cam_push(1.0, 1.04, 560, 1200, 4.6), light=DAWN, sun=(760, 960, 800, (0.14, 0.09, 0.05)))
    # C: the rider on the hill turns his horse and rides away
    def midC(t):
        go = ease((t - 0.6) / 0.3)
        q = P(turn=0.45, gx=0.8, gy=0.0, furrow=0.6, armR="forward", armL="relaxed", legs="none", blink=blink_at(t, 937), wind=0.8)
        if t < 0.6:
            q["turn"] = -0.2; q["gx"] = -0.4
        x = 880 + 260 * max(0.0, t - 0.7) ** 1.3
        return ride(enemy_spec(random.Random(934)), q, t, x, 1032 + 10 * max(0.0, t - 0.7), 0.16, "#1e1a1c", gallop=t > 0.7, flip=t < 0.6, blanket="#121216")
    C = Shot(2.8, fd, midC, cam=lambda t: (lerp(1.6, 1.7, ease(t / 2.8)), 1080, 1100, 0, 0), bg_par=1.0, light=DAWN, sun=(760, 960, 800, (0.14, 0.09, 0.05)), fade_out=0.6)
    # D1: night, Armenia: the gates open; Sahl ibn Sunbat comes out with his torch-bearers
    ag = bgs.cached("armenia_gate", bgs.armenia_gate)
    def cross(x, y, s):
        return f'<path d="M {x:.1f} {y - 22 * s:.1f} L {x:.1f} {y + 22 * s:.1f} M {x - 14 * s:.1f} {y - 8 * s:.1f} L {x + 14 * s:.1f} {y - 8 * s:.1f}" stroke="#e0b25a" stroke-width="{5 * s:.1f}"/>'
    def midD1(t):
        o = GLOWDEF
        for x in (330, 750):
            o += glow(x, 1010, 160, 0.9) + flame(x, 1030, 0.6, t, x)
        op = ease((t - 0.1) / 1.0)
        for side in (-1, 1):
            w = 150 * (1 - 0.88 * op)
            x0 = 540 + side * 150
            o += f'<path d="M {x0} 1400 L {x0} 1120 L {x0 - side * w:.1f} {1120 + 30 * op:.1f} L {x0 - side * w:.1f} 1400 Z" fill="#3a2414" stroke="#140a04" stroke-width="5"/>'
        u = ease((t - 1.0) / 1.4)
        if t > 0.9:
            for k, x in enumerate((420, 660)):
                g = P(turn=0.2 if x < 540 else -0.2, gx=0.0, furrow=0.3, armL="fist_up", propL="torch", armR="relaxed", blink=blink_at(t, 938 + k))
                o += at_feet(GUARD, g, t, x, lerp(1390, 1470, u), lerp(0.3, 0.36, u))
            sq = P(turn=0.0, gx=0.0, gy=0.1, smile=0.7, brow=0.3, armL="both_out" if u > 0.6 else "relaxed", armR="both_out" if u > 0.6 else "relaxed",
                   legs="walk" if u < 1 else "stand", phase=t * 5, blink=blink_at(t, 940))
            o += at_feet(SAHL, sq, t, 540, lerp(1400, 1560, u), lerp(0.34, 0.44, u))
            o += cross(540, lerp(1400, 1560, u) - (FEET - 150) * lerp(0.34, 0.44, u), lerp(0.34, 0.44, u) * 1.6)
        return o
    D1 = Shot(4.0, ag, midD1, cam=cam_push(1.0, 1.05, 540, 1200, 4.0), light=dict(point=(540, 1250, 900, 0.5, 1.2, (1.0, 0.6, 0.3)), rim_point=(540, 5), rim_col=(1.0, 0.7, 0.4)),
               grade="fire", fade_in=0.6)
    # D2: "Welcome, King Babak. My house is your house." (the end card comes up over it)
    agb = blur_bg("armenia_gate", bgs.armenia_gate, 10)
    tg = glow_img(170, (255, 150, 70), 0.6)
    def torchbg(t):
        im = agb.copy()
        for k, x in enumerate((150, 930)):
            im.alpha_composite(tg, (int(x - 170 + 5 * math.sin(t * 9 + k)), 650))
        return im
    LD2 = [("p6s6b", 0.5), ("p6s6c", 2.3)]
    def midD2(t):
        q = talk_pose(LD2, t, 941, dict(turn=0.05, gx=0.0, gy=0.1, smile=0.75, brow=0.35, furrow=-0.2, armL="relaxed", armR="relaxed"))
        q["smile"] = 0.75 - 0.5 * ease((t - 6.0) / 1.0)
        q["furrow"] = -0.2 + 0.8 * ease((t - 6.0) / 1.0)
        return at_neck(SAHL, P(**q), t, 540, 1075, 1.15)
    D2 = Shot(8.4, torchbg, midD2, cam=cam_push(1.0, 1.06, 540, 860, 8.4), light=dict(rim_point=(540, 5), rim_col=(1.0, 0.7, 0.4), ramp=(0, W, 1.0, 1.0), ambient=(0.95, 0.88, 0.85)),
               sun=(540, 1200, 800, (0.10, 0.05, 0.02)), grade="fire", fade_out=0.8)
    return [A, B, C, D1, D2]


SCENES = {"s1": s1, "s2": s2, "s3": s3, "s4": s4, "s5": s5, "s6": s6}
