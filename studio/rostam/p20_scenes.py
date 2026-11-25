"""Part 20 (The Empty Fortress; row 10 of OUTLINE.md, second half): every shot as a shadow-play scene.

Importing this module imports p19_scenes (and through it parts 15-18) and registers part 20's shots.
New here, to reuse: court_night() (the courtyard inside the gate at night: stars, torches, the dark mouth of the secret
passage), tunnel() (the secret passage seen from the side: rough rock overhead, old wooden props, lit only by the lamps
the people carry), hills_dawn() (before dawn in the hills behind the fortress: the fortress small on its hill, the
enemy's fires on the plain), camp_sunrise() (the Turanian tents at sunrise, for the war drums), gate_burst() (the gate
of the White Fortress smashed open: doors fly back, dust and splinters), him_court() (Sohrab close on his colt inside
the court), sky_ghost() (a person as a soft shadow in the sky: what he remembers), ride_bg() (sunset sky and a plain
scrolling for a gallop to the LEFT).
Line timings come from p20/audio/timeline.json (LN), so the action follows the voices.
"""
import math, random
import skia
import anim
from anim import C, mix, mixc, clamp, ease, sstep, Cam, Pen, ANCH, rope, spath, ppath, paint, fillp, W, H
from puppets import person, horse, LOOKS
import sets as S
import p15_scenes as M
import p16_scenes as P16
import p17_scenes as Q
import p18_scenes as R
import p19_scenes as N
from ep01_scenes import loc, jaw, get, vig, tag, A, ground, INK, torch, Scroller
from p05_scenes import register, shadow_layer, candle_light, MOON
from p07_scenes import LN, dissolve, DAY
from p09_scenes import flick, NIGHT, WARM
from p11_scenes import COLT, drummer, drum_rings
from p13_scenes import cuts, HOOMAN

GAZH, MORN, STONE = M.GAZH, M.MORN, M.STONE
GORD_BARE, TURK = Q.GORD_BARE, Q.TURK
LAMP = (255, 176, 100)                         # lamplight rim
TORCHLIT = mixc(MOON, (255, 170, 96), 0.6)     # torches under the moon


# ------------------------------------------------------------------ sets
def court_night(an, c, t, cam, key, door=0.0):
    """The courtyard inside the gate at night (gate_court darkened): stars over the wall, two torches, and when door > 0
    the dark mouth of the secret passage in the inner wall at the right, lamplight inside it."""
    M.gate_court(an, c, t, cam, key, 0.0, 540)
    c.drawRect(skia.Rect.MakeLTRB(-300, -300, W + 300, H + 300), paint(C(10, 12, 30, 206)))
    with cam(0.1):
        get(an, key + "st", lambda: S.Stars(70, 330, 205)).draw(c, t, 0.9, 330)
        S.moon(c, 880, 290, 30)
    with cam(0.6):
        for k, x in enumerate((300, 960)):
            torch(c, x, 560, t, 1.0, k)
        if door > 0.01:
            arch = S.arch_path(830, 872, 140, 220)
            c.drawPath(arch, paint(C(6, 4, 6)))
            S.glow(c, 830, 790, 170, (255, 160, 80), 70 * door * flick(t))
            edge = skia.Paint(AntiAlias=True, Color=C(60, 50, 60))
            edge.setStyle(skia.Paint.kStroke_Style)
            edge.setStrokeWidth(12)
            c.drawPath(arch, edge)


def rock_path(seed, y0=390, x0=-400, x1=1500):
    rnd = random.Random(seed)
    path = skia.Path()
    path.moveTo(x0, -300)
    x = x0
    while x <= x1:
        y = y0 + 22 * math.sin(x * 0.011 + seed) + 12 * math.sin(x * 0.037) + rnd.uniform(-8, 8)
        if rnd.random() < 0.12:
            path.lineTo(x, y)
            path.lineTo(x + 12, y + rnd.uniform(26, 60))
            path.lineTo(x + 26, y)
        else:
            path.lineTo(x, y)
        x += 34
    path.lineTo(x1, -300)
    path.close()
    return path


def tunnel(an, c, t, cam, key, glows, lt=0.0, gy=1000):
    """The secret passage seen from the side: rough rock overhead, old wooden props going by, a low dark corridor lit
    only by the lamps the people carry (glows = [(x, y, a)])."""
    S.lin(c, 0, H, [(0, (12, 7, 7)), (0.45, (36, 22, 17)), (1, (6, 3, 3))])
    with cam(0.8):
        for (x, y, a) in glows:
            S.glow(c, x, y, 480, (255, 150, 70), 125 * a * flick(t, x * 0.01))
        props = paint(C(40, 24, 18))
        for k in range(6):
            x = (k * 360 - lt * 26) % 2160 - 400
            c.drawRect(skia.Rect.MakeLTRB(x - 14, 380, x + 14, gy + 10), props)
            c.drawRect(skia.Rect.MakeLTRB(x - 80, 392, x + 80, 418), props)
    with cam(1.0):
        c.drawPath(get(an, key + "rk", lambda: rock_path(211)), paint(C(*INK)))
        ground(c, gy, (46, 28, 20), (6, 3, 3))


def hills_dawn(an, c, t, cam, key, dawn=0.0, gy=1000, fort=(840, 600, 0.24), near=True):
    """Before dawn in the hills behind the fortress: the sky paling at the horizon, the White Fortress small on its
    hill with a few torches, the Turanian fires on the plain below it, the dark slope the people walk on."""
    top = mixc((8, 10, 30), (40, 46, 96), dawn)
    mid = mixc((24, 28, 66), (120, 96, 140), dawn)
    low = mixc((64, 58, 100), (240, 166, 142), dawn)
    S.lin(c, 0, 820, [(0, top), (0.55, mid), (0.9, low), (1, low)])
    with cam(0.1):
        get(an, key + "st", lambda: S.Stars(110, 620, 206)).draw(c, t, 1 - 0.8 * dawn, 620)
    rg = get(an, key + "rg", lambda: (S.make_ridge(-600, 1700, 700, 50, 207, 8, 4, 0.4), S.make_ridge(-600, 1700, 760, 20, 208)))
    with cam(0.25):
        S.ridge(c, rg[0], mixc((26, 26, 54), (80, 62, 96), dawn))
    with cam(0.4):
        S.ridge(c, rg[1], mixc((18, 16, 36), (56, 42, 66), dawn))
        S.lin(c, 770, 920, [(0, mixc((34, 28, 54), (96, 68, 84), dawn)), (1, (14, 10, 20))], (-600, 770, 1700, 920))
        rnd = random.Random(209)
        for k in range(30):
            fx = rnd.uniform(-100, 1200)
            fy = 792 + rnd.uniform(0, 1) ** 2 * 100
            S.glow(c, fx, fy, 14 + (fy - 780) * 0.3, (255, 140, 60), (150 + 40 * math.sin(t * 6 + k)) * (1 - 0.55 * dawn))
        fx, fy, fs = fort
        gate_x, foot = fx + 400 * fs, fy + 540 * fs
        c.drawPath(spath([(gate_x - 420 * fs * 2, foot + 120, 0), (gate_x - 300 * fs * 2, foot + 10), (gate_x, foot - 6),
                          (gate_x + 300 * fs * 2, foot + 10), (gate_x + 420 * fs * 2, foot + 120, 0)]),
                   paint(C(*mixc((20, 18, 38), (60, 46, 70), dawn))))
        tint = skia.Paint()
        tint.setColorFilter(skia.ColorFilters.Blend(C(*mixc((40, 44, 92), (150, 120, 150), dawn), int(200 * (1 - 0.6 * dawn))),
                                                    skia.BlendMode.kSrcATop))
        c.saveLayer(None, tint)
        M.fort(an, c, t, fx, fy, fs, 0.0, key + "f", 0.6)
        c.restore()
        for k in range(3):
            S.glow(c, fx + (160 + 240 * k) * fs, fy + 120 * fs, 40, (255, 150, 70), 140 + 40 * math.sin(t * 7 + k))
    if near:
        with cam(1.0):
            slope = spath([(-300, 2400, 0), (-300, gy + 50), (200, gy + 20), (600, gy - 6), (1000, gy - 40),
                           (1400, gy - 70), (1400, 2400, 0)])
            c.drawPath(slope, paint(C(*INK)))


def slope_y(x, gy):
    """Height of the near slope of hills_dawn() at x (approx.)."""
    return gy + 20 - (x - 200) * 0.065 if x > 200 else gy + 20 + (200 - x) * 0.06


def camp_sunrise(an, c, t, cam, key, gy=872):
    """The Turanian camp at sunrise: golden sky, the sun on the horizon, hazy tents behind, bright dusty ground."""
    S.lin(c, 0, 880, [(0, (46, 54, 104)), (0.45, (190, 140, 160)), (0.8, (252, 196, 150)), (1, (255, 222, 172))])
    with cam(0.15):
        S.sun(c, 820, 790, 70, (255, 246, 214), (255, 190, 130), 560, 150)
        get(an, key + "cl", lambda: S.Clouds([(300, 12), (380, 9), (460, 14)], 212, 300, 600)).draw(c, t, (170, 110, 140), 150)
    rg = get(an, key + "rg", lambda: (S.make_ridge(-600, 1700, 760, 60, 213, 8, 4, 0.4), S.make_ridge(-600, 1700, 812, 22, 214)))
    with cam(0.35):
        S.ridge(c, rg[0], (150, 116, 140))
        S.lin(c, 720, 812, [(0, (252, 210, 170, 0)), (1, (252, 210, 170, 130))], (-600, 720, 1700, 812))
    with cam(0.5):
        S.ridge(c, rg[1], (120, 88, 104))
    with cam(0.65):
        ground(c, 846, (200, 150, 112), (90, 60, 46))
        for (x, s_) in ((40, 0.6), (300, 0.78), (560, 0.52), (820, 0.72), (1080, 0.6)):
            S.tent(c, x, 850, s_, t + x, (112, 74, 78))
    with cam(1.0):
        ground(c, gy, (204, 156, 112), (60, 40, 30))


def gate_burst(an, c, t, cam, key, burst_t, lt, gx=330, top=440, gy=1000):
    """gate_outside() whose doors are smashed open at lt = burst_t: they fly back in 0.25 s, dust and splinters."""
    g = ease(clamp((lt - burst_t) / 0.25))
    R.gate_outside(an, c, t, cam, key, g, gx, 1.0, top, gy)
    u = lt - burst_t
    if 0 <= u < 1.4:
        with cam(0.6):
            rnd = random.Random(215)
            wood = paint(C(96, 66, 48))
            for k in range(12):
                vx, vy = rnd.uniform(-420, 420), rnd.uniform(-520, -160)
                x = gx + vx * u
                y = gy - 220 + vy * u + 700 * u * u
                c.save()
                c.translate(x, y)
                c.rotate(u * rnd.uniform(-500, 500))
                c.drawRect(skia.Rect.MakeLTRB(-16, -4, 16, 4), wood)
                c.restore()
    P16.dust_puff(c, gx, gy - 60, t, burst_t, lt, 1.3)


def him_court(an, c, t, lt, dur, key, rp, zk=0.06, gate=1.0):
    """Sohrab close on his colt inside the court of the empty fortress (the open gate behind him)."""
    focus = (640, 600)
    zoom = 1.0 + zk * ease(lt / max(dur, 0.1))
    cam = Cam(c, focus, zoom)
    M.gate_court(an, c, t, cam, key, gate, 380)

    def fs(cc):
        with Cam(cc, focus, zoom)(1.0):
            M.rider(cc, 720, 1400, 1.2, -1, "sohrab", t, rp, rider_scale=0.92, neck=5 * math.sin(t * 1.3),
                    head=3 * math.sin(t * 0.9))
    an.figures(c, fs, COLT, (0, 0, 1080, 1500), alpha=170)
    vig(an, c, 150)


def sky_ghost(c, cam, a, t, P, x=430, y=1330, s=1.36, look=GORD_BARE, face=1):
    """A person as a soft blue-grey shadow in the sky: what he remembers (drawn between the sky and the parapet)."""
    if a <= 0.01:
        return
    with cam(1.0):
        shadow_layer(c, (0, 0, W, H), 0.5 * a, (70, 80, 118), 3.0)
        person(c, x, y, s, face, P, t, look)
        c.restore()


def empty_wall(an, c, t, lt, dur, key, ghost=0.0, P=None, zk=0.06):
    """The battlements where she stood, empty against the sky; birds go over; ghost (0..1) shows her there as a soft
    shadow, laughing."""
    focus = (540, 640)
    zoom = 1.0 + zk * ease(lt / max(dur, 0.1))
    cam = Cam(c, focus, zoom)

    def behind(cm):
        with cm(0.3):
            S.birds(c, t, get(an, key + "bd", lambda: [(random.Random(k).uniform(-200, 900), random.Random(k + 7).uniform(380, 560),
                                                        46, random.Random(k + 3).uniform(7, 11), k) for k in range(5)]),
                    (60, 66, 90))
        if ghost > 0.01:
            sky_ghost(c, cm, ghost, t, P or {}, 430, 1330, 1.36)
    N.wall_low2(an, c, t, cam, key, lambda cc: None, top=1150, sun=(520, 580), behind=behind)
    vig(an, c, 150)


def ride_bg(an, c, t, lt, key, speed=520):
    """Sunset sky and a plain scrolling to the right, for a gallop to the LEFT (towards Iran)."""
    S.lin(c, 0, 900, [(0, (34, 26, 66)), (0.4, (150, 70, 90)), (0.75, (246, 140, 90)), (1, (255, 196, 130))])
    S.sun(c, 260, 760, 90, (255, 230, 180), (255, 130, 80), 560, 160)
    get(an, key + "cl", lambda: S.Clouds([(330, 12), (420, 9), (520, 14)], 216, 300, 620)).draw(c, t, (120, 50, 80), 170)
    c.save()
    c.translate(W, 70)
    c.scale(-1, 1)
    get(an, key, lambda: Scroller(217)).draw(c, lt + 3.0, speed, [(150, 80, 110), (110, 50, 70), (70, 30, 40)])
    c.restore()


# ================================================================== S01 + TITLE (hook)
def p20_s01(an, c, t):
    """Hook + title: inside the fortress, its gate smashed open, Sohrab on his colt shouts into the empty court:
    'Gordafarid! Where are you?!' -- a Turanian soldier runs to him: 'They are gone, my lord. All of them.'"""
    lt = t - an.start["S01"]
    dur = an.end["TITLE"] - an.start["S01"]
    a0, a1 = LN("p20", "S01", 0)
    b0, b1 = LN("p20", "S01", 1)
    focus = (600, 700)
    zoom = 1.06 + 0.06 * ease(lt / dur)
    cam = Cam(c, focus, zoom)
    M.gate_court(an, c, t, cam, "gc201", 1.0, 540)
    shout = sstep(a0 - 0.2, a0 + 0.3, lt) * (1 - sstep(a1 + 0.2, a1 + 0.8, lt))
    sag = sstep(b1 + 0.4, b1 + 2.0, lt)
    rp = {"hand": (110, -340), "rhand": (mix(30, 150, shout), mix(-300, -520, shout)), "rhand_kind": "open",
          "head": -14 * shout + 12 * sag + math.sin(t * 0.8), "jaw": jaw(an, "SOHRAB", t, 10), "lean": -4 * shout + 4 * sag,
          "wind": 0.6}
    run = clamp((lt - a1 + 0.2) / 2.2)
    sx = mix(-120, 300, ease(run))
    PT = {"mode": "walk" if 0 < run < 1 else "stand", "phase": lt * 5.0, "stride": 22 * (run < 1), "lean": 8 * (run < 1),
          "hand": (mix(40, 150, sstep(b0, b0 + 0.5, lt)), mix(-262, -380, sstep(b0, b0 + 0.5, lt))), "hand_kind": "open",
          "rhand_kind": "spear", "rhand": (-10, -300), "jaw": jaw(an, "RIDER", t, 9), "head": 4}

    def ft(cc):
        with Cam(cc, focus, zoom)(1.0):
            person(cc, sx, 900, 0.86, 1, PT, t, TURK)
    an.figures(c, ft, DAY, (0, 200, 1080, 1100))

    def fs(cc):
        with Cam(cc, focus, zoom)(1.0):
            M.rider(cc, 760, 900, 0.62, -1, "sohrab", t, rp, rider_scale=0.92, neck=6 * math.sin(t * 1.4))
    an.figures(c, fs, COLT, (0, 200, 1080, 1100), alpha=180)
    vig(an, c, 150)


# ================================================================== S02 the night before
def p20_s02(an, c, t):
    """'That night, the White Fortress was dark and silent. But no one inside was asleep.' (the court by torchlight,
    people carrying bundles and lamps) -- Gazhdaham: 'Take only what you can carry. And not a sound.' -- a guard: 'And
    the fortress, my lord? Do we leave it to the Turks?' -- 'Walls can be built again. People cannot.'"""
    lt, dur = loc(an, "S02", t)
    L = [LN("p20", "S02", k) for k in range(5)]
    cut = L[2][0] - 0.4

    def wide():
        focus = (540, 720)
        zoom = 1.0 + 0.05 * ease(lt / (cut + 0.4))
        cam = Cam(c, focus, zoom)
        court_night(an, c, t, cam, "cn202")
        people = [(-260, "maid", 0.0, 1, True), (-120, "noble", 0.6, 1, False), (40, "warrior_ir", 1.3, 1, True),
                  (1260, "maid", 0.3, -1, False), (1420, "boy", 0.9, -1, False)]

        def figs(cc):
            with Cam(cc, focus, zoom)(1.0):
                for i, (x0, look, d0, face, lamp) in enumerate(people):
                    u = clamp((lt - d0) / 7.0)
                    x = x0 + face * 520 * u
                    P = {"mode": "walk" if u < 1 else "stand", "phase": lt * 3.8 + i, "stride": 14, "seed": i,
                         "head": 4 + 2 * math.sin(t * 0.7 + i), "carry": "saddle" if (i % 2 == 1 and look != "boy") else None}
                    if lamp:
                        P.update(hand_kind="lamp", hand=(100, -330))
                    tag(f"p{i}:")
                    person(cc, x, 880, 0.62 if look != "boy" else 0.48, face, P, t, look)
                tag("")
        an.figures(c, figs, TORCHLIT, (0, 300, 1080, 1100), anchors=True)
        for i in (0, 2):
            candle_light(c, an, f"p{i}:flame", t, 300, 90, i * 1.7, 0.2)
        vig(an, c, 160)

    def two():
        lt2 = lt - cut
        focus = (540, 700)
        zoom = 1.0 + 0.06 * ease(lt2 / (dur - cut))
        cam = Cam(c, focus, zoom)
        court_night(an, c, t, cam, "cn202b")
        firm = sstep(L[2][0] + 0.3, L[2][0] + 0.8, lt) * (1 - sstep(L[2][1], L[2][1] + 0.5, lt))
        calm = sstep(L[4][0] + 0.2, L[4][0] + 0.9, lt)
        ask = sstep(L[3][0] + 0.3, L[3][0] + 0.9, lt) * (1 - sstep(L[3][1], L[3][1] + 0.5, lt))
        PZ = {"hand_kind": "staff", "hand": (60, -300),
              "rhand": (mix(mix(-20, 140, firm), 110, calm), mix(mix(-280, -360, firm), -430, calm)),
              "rhand_kind": "open" if (firm > 0.3 or calm > 0.3) else "fist",
              "head": 4 - 3 * firm + 4 * calm + math.sin(t * 0.6), "jaw": jaw(an, "GAZHDAHAM", t, 8), "lean": 2 * calm}
        PG = {"hand_kind": "spear", "hand": (90, -320), "rhand": (mix(-20, 120, ask), mix(-270, -420, ask)),
              "rhand_kind": "open", "head": 6 - 6 * ask + math.sin(t * 0.8), "jaw": jaw(an, "GUARD", t, 8), "lean": 3 * ask}

        def figs(cc):
            with Cam(cc, focus, zoom)(1.0):
                person(cc, 300, 1330, 1.4, 1, PZ, t, GAZH)
                person(cc, 810, 1330, 1.4, -1, PG, t, "warrior_ir")
        an.figures(c, figs, TORCHLIT, (0, 100, 1080, 1500))
        vig(an, c, 165)

    cuts(c, lt, [(0.0, wide), (cut, two)], 0.45)


# ================================================================== S03 the secret passage
def p20_s03(an, c, t):
    """'Under the fortress was a secret passage, as old as its walls. One by one, the people went down into the dark.'
    (the dark mouth in the inner wall; Gordafarid with a lamp sends them in) -- in the passage, a boy: 'I'm scared.
    It's so dark.' -- Gordafarid: 'Don't be afraid. Hold my hand, and walk with me. Keep the lamps low. The Turks must
    not see any light.'"""
    lt, dur = loc(an, "S03", t)
    L = [LN("p20", "S03", k) for k in range(5)]
    cut = L[2][0] - 0.45

    def mouth():
        focus = (640, 720)
        zoom = 1.0 + 0.07 * ease(lt / (cut + 0.4))
        cam = Cam(c, focus, zoom)
        court_night(an, c, t, cam, "cn203", door=1.0)
        line = [("maid", 0.0), ("noble", 1.1), ("boy", 2.2), ("warrior_ir", 3.3), ("maid", 4.4), ("noble", 5.5),
                ("maid", 6.6), ("warrior_ir", 7.7)]

        def figs(cc):
            with Cam(cc, focus, zoom)(1.0):
                tag("g:")
                person(cc, 190, 880, 0.64, 1, {"hand_kind": "lamp", "hand": (120, -400), "rhand": (-20, -270),
                                               "head": 4 + 2 * math.sin(t * 0.6), "wind": 0.3}, t, GORD_BARE)
                tag("")
            for i, (look, d0) in enumerate(line):
                u = clamp((lt - d0) / 3.2)
                if u <= 0 or u >= 1:
                    continue
                x = mix(360, 830, u)
                a = 1 - sstep(0.82, 1.0, u)
                s = (0.48 if look == "boy" else 0.6) * mix(1.0, 0.86, sstep(0.75, 1.0, u))
                if Pen.mode == "fill" or Pen.mode == "rim":
                    cc.saveLayerAlpha(None, int(255 * a))
                with Cam(cc, focus, zoom)(1.0):
                    person(cc, x, mix(880, 872, sstep(0.75, 1.0, u)), s, 1,
                           {"mode": "walk", "phase": lt * 4.0 + i, "stride": 14, "seed": i, "head": 6,
                            "carry": "saddle" if i % 3 == 1 else None}, t, look)
                if Pen.mode == "fill" or Pen.mode == "rim":
                    cc.restore()
        an.figures(c, figs, TORCHLIT, (0, 300, 1080, 1100), anchors=True)
        candle_light(c, an, "g:flame", t, 320, 100, 2.0, 0.22)
        vig(an, c, 165)

    def inside():
        lt2 = lt - cut
        focus = (540, 700)
        zoom = 1.0 + 0.05 * ease(lt2 / (dur - cut))
        cam = Cam(c, focus, zoom)
        hold = sstep(L[3][0] + 1.4, L[3][0] + 2.2, lt)
        low = sstep(L[4][0] + 0.6, L[4][0] + 1.4, lt)
        walk = sstep(L[3][1] - 0.2, L[3][1] + 0.6, lt)
        gx = 600 + 70 * clamp((lt - L[3][1]) / 6.0)
        PG = {"mode": "walk" if walk > 0.5 else "stand", "phase": lt * 3.0, "stride": 12 * walk, "hand_kind": "lamp",
              "hand": (mix(110, 120, low), mix(-340, -250, low)),
              "rhand": (mix(-20, -150, hold), mix(-270, -300, hold)), "rhand_kind": "open",
              "head": 4 + 8 * (1 - walk) * sstep(L[3][0], L[3][0] + 0.6, lt) + math.sin(t * 0.7),
              "jaw": jaw(an, "GORDAFARID", t, 8), "wind": 0.2}
        bx = gx - 150 - 0.7 * 140
        PB = {"mode": "walk" if walk > 0.5 else "stand", "phase": lt * 3.0 + 0.5, "stride": 10 * walk,
              "hand": (mix(40, 135, hold), mix(-262, -330, hold)), "hand_kind": "open",
              "rhand": (-20, -262), "head": -6 + 3 * math.sin(t * 3) * (1 - hold), "jaw": jaw(an, "BOY", t, 9)}
        back = [(gx - 470, "maid"), (gx - 700, "warrior_ir"), (gx - 930, "noble")]

        def figs(cc):
            with Cam(cc, focus, zoom)(1.0):
                tag("g:")
                person(cc, gx, 1000, 1.0, 1, PG, t, GORD_BARE)
                tag("b:")
                person(cc, bx, 1000, 0.68, 1, PB, t, "boy")
                for i, (x, look) in enumerate(back):
                    tag(f"q{i}:")
                    person(cc, x, 1000, 0.94, 1, {"mode": "walk" if walk > 0.5 else "stand", "phase": lt * 3.0 + i,
                                                   "stride": 12 * walk, "hand_kind": "lamp",
                                                   "hand": (110, mix(-330, -250, low)), "head": 6, "seed": i}, t, look)
                tag("")
        ANCH.clear()
        Pen.mode = "anchor"
        figs(c)
        Pen.mode = "fill"
        glows = [(p[0], p[1], 1.0 - 0.35 * low) for p in (A("g:flame"), A("q0:flame"), A("q1:flame"), A("q2:flame")) if p]
        tunnel(an, c, t, cam, "tn203", glows, lt2)
        an.figures(c, figs, LAMP, (0, 200, 1080, 1200), alpha=170)
        for i, nm in enumerate(("g:flame", "q0:flame", "q1:flame", "q2:flame")):
            candle_light(c, an, nm, t, 200, 70 * (1 - 0.4 * low), i * 1.3, 0.22)
        vig(an, c, 175)

    cuts(c, lt, [(0.0, mouth), (cut, inside)], 0.45)


# ================================================================== S04 out in the hills
def p20_s04(an, c, t):
    """'Before dawn, they came out far away, in the hills behind the fortress.' (a line of lamps up the slope) 'Below
    them, the Turanian army was still asleep.' -- Gordafarid: 'In the morning he will come for us, Father...' --
    Gazhdaham: 'And he will find nothing but empty walls.' -- she looks back: 'Goodbye, White Fortress.' -- 'Come. The
    road to Iran is long.'"""
    lt, dur = loc(an, "S04", t)
    L = [LN("p20", "S04", k) for k in range(6)]
    cut = L[2][0] - 0.4
    c2 = L[4][0] - 0.3
    c3 = L[5][0] - 0.3

    def wide():
        focus = (540, 760)
        zoom = 1.0 + 0.05 * ease(lt / (cut + 0.4))
        cam = Cam(c, focus, zoom)
        dawn = 0.15 * clamp(lt / cut)
        hills_dawn(an, c, t, cam, "hd204", dawn, 1000, (760, 600, 0.22))
        looks = ["warrior_ir", "maid", "noble", "boy", "maid", GORD_BARE, GAZH, "warrior_ir"]

        def figs(cc):
            with Cam(cc, focus, zoom)(1.0):
                for i, look in enumerate(looks):
                    x = -40 + i * 120 + 34 * lt
                    if x < -80 or x > 1160:
                        continue
                    s = 0.34 if look == "boy" else 0.44
                    tag(f"w{i}:")
                    P = {"mode": "walk", "phase": lt * 3.4 + i, "stride": 14, "seed": i, "head": 4}
                    if i % 2 == 0:
                        P.update(hand_kind="lamp", hand=(100, -280))
                    if look == GAZH:
                        P.update(hand_kind="staff", hand=(60, -300))
                    person(cc, x, slope_y(x, 1000), s, 1, P, t, look)
                tag("")
        an.figures(c, figs, (190, 196, 240), (0, 400, 1080, 1100), anchors=True)
        for i in range(0, 8, 2):
            candle_light(c, an, f"w{i}:flame", t, 120, 70, i * 1.1, 0.12)
        vig(an, c, 160)

    def two(look_back=0.0, lt_=0.0, d_=1.0, zoom0=0.0, go=0.0):
        focus = (540, 700)
        zoom = 1.0 + zoom0 + 0.05 * ease(lt_ / max(d_, 0.1))
        cam = Cam(c, focus, zoom)
        dawn = 0.25 + 0.35 * clamp((lt - cut) / (dur - cut))
        hills_dawn(an, c, t, cam, "hd204b", dawn, 1330, (300, 560, 0.3), near=True)
        ask = sstep(L[2][0] + 0.2, L[2][0] + 0.8, lt) * (1 - sstep(L[2][1], L[2][1] + 0.5, lt))
        sure = sstep(L[3][0] + 0.3, L[3][0] + 0.9, lt) * (1 - sstep(L[3][1], L[3][1] + 0.5, lt))
        come = sstep(L[5][0] + 0.3, L[5][0] + 0.9, lt)
        PG = {"hand": (mix(40, 120, ask), mix(-262, -360, ask)), "hand_kind": "open" if ask > 0.3 else "fist",
              "rhand": (-20, -270), "head": 4 - 2 * ask + 6 * look_back + math.sin(t * 0.8),
              "jaw": jaw(an, "GORDAFARID", t, 8), "wind": 1.0}
        PZ = {"hand_kind": "staff", "hand": (60, -300),
              "rhand": (mix(mix(-20, 130, sure), 150, come), mix(mix(-280, -380, sure), -420, come)),
              "rhand_kind": "open" if (sure > 0.3 or come > 0.3) else "fist",
              "head": 4 - 2 * sure + math.sin(t * 0.6), "jaw": jaw(an, "GAZHDAHAM", t, 8), "lean": 2 * come}
        gx = 760 + 260 * go
        zx = 250 + 420 * go
        if go > 0.01:
            PG.update(mode="walk", phase=lt * 3.6, stride=16)
            PZ.update(mode="walk", phase=lt * 3.6 + 0.7, stride=16)

        def figs(cc):
            with Cam(cc, focus, zoom)(1.0):
                person(cc, zx, 1330, 1.42, 1, PZ, t, GAZH)
                person(cc, gx, 1330, 1.34, 1 if go > 0.01 else -1, PG, t, GORD_BARE)
        an.figures(c, figs, mixc((190, 196, 240), (255, 190, 150), dawn), (0, 100, 1080, 1500))
        vig(an, c, 160)

    def talk():
        two(0.0, lt - cut, c2 - cut + 0.4)

    def back():
        lt3 = lt - c2
        lb = sstep(L[4][0] - 0.2, L[4][0] + 0.6, lt)
        two(lb, lt3, c3 - c2 + 0.4, 0.12)

    def leave():
        go = sstep(L[5][1] - 0.2, dur, lt)
        two(0.0, lt - c3, dur - c3, 0.06, go)

    cuts(c, lt, [(0.0, wide), (cut, talk), (c2, back), (c3, leave)], 0.4)


# ================================================================== S05 the war drums
def p20_s05(an, c, t):
    """'At sunrise, the war drums woke the Turanian camp.' -- Sohrab on his colt before the tents: 'Today, that fortress
    falls!' -- Hooman: 'The men are ready, Sohrab.' -- 'Good. And remember: the girl is mine. Bring her to me alive.'"""
    lt, dur = loc(an, "S05", t)
    L = [LN("p20", "S05", k) for k in range(4)]
    cut = L[1][0] - 0.35

    def drums():
        focus = (540, 720)
        zoom = 1.0 + 0.06 * ease(lt / (cut + 0.4))
        cam = Cam(c, focus, zoom)
        camp_sunrise(an, c, t, cam, "cs205", 872)
        beat = sstep(0.2, 0.8, lt)

        def figs(cc):
            with Cam(cc, focus, zoom)(1.0):
                drummer(cc, 170, 872, 0.86, 1, t, beat, 0.0)
                drummer(cc, 900, 872, 0.86, -1, t, beat, 1.3)
        an.figures(c, figs, (255, 200, 150), (0, 200, 1080, 1100))
        with cam(1.0):
            drum_rings(c, 170 + 110 * 0.86, 872 - 80, t, beat, 0.0)
            drum_rings(c, 900 - 110 * 0.86, 872 - 80, t, beat, 0.4)
        vig(an, c, 150)

    def two():
        lt2 = lt - cut
        focus = (540, 700)
        zoom = 1.0 + 0.06 * ease(lt2 / (dur - cut))
        cam = Cam(c, focus, zoom)
        camp_sunrise(an, c, t, cam, "cs205b", 1000)
        up = sstep(L[1][0], L[1][0] + 0.4, lt) * (1 - sstep(L[1][1] + 0.3, L[1][1] + 0.9, lt))
        point = sstep(L[3][0] + 1.4, L[3][0] + 1.9, lt) * (1 - sstep(L[3][1], L[3][1] + 0.5, lt))
        rpS = {"hand": (110, -340), "hand_kind": "fist", "rhand": (mix(mix(30, 120, up), 230, point), mix(mix(-300, -640, up), -420, point)),
               "rhand_kind": "open" if point > 0.3 else "fist", "head": 4 - 6 * up + math.sin(t * 0.7),
               "jaw": jaw(an, "SOHRAB", t, 9), "lean": -3 * up, "wind": 0.9}
        rpH = {"hand_kind": "mace", "hand": (100, -330), "rhand": (30, -300), "head": 4 + 4 * sstep(L[2][1], L[2][1] + 0.5, lt),
               "jaw": jaw(an, "HOOMAN", t, 8), "wind": 0.7}

        def fh(cc):
            with Cam(cc, focus, zoom)(1.0):
                M.rider(cc, 270, 1000, 0.64, 1, HOOMAN, t, rpH, neck=5 * math.sin(t * 1.2), head=3 * math.sin(t * 0.8))
        an.figures(c, fh, (255, 200, 150), (0, 100, 1080, 1300))

        def fs(cc):
            with Cam(cc, focus, zoom)(1.0):
                M.rider(cc, 820, 1000, 0.66, -1, "sohrab", t, rpS, rider_scale=0.92, neck=6 * math.sin(t * 1.5))
        an.figures(c, fs, COLT, (0, 100, 1080, 1300), alpha=190)
        vig(an, c, 150)

    cuts(c, lt, [(0.0, drums), (cut, two)], 0.4)


# ================================================================== S06 silent walls; the gate breaks
def p20_s06(an, c, t):
    """'The army marched to the fortress... but the walls were silent.' -- (the empty battlements) Hooman: 'No guards on
    the walls... no arrows... Strange.' -- Sohrab: 'Another trick. I know her tricks now. Break the gate!' -- 'With one
    blow of his mace, Sohrab smashed the gate open.'"""
    lt, dur = loc(an, "S06", t)
    L = [LN("p20", "S06", k) for k in range(5)]
    c1 = L[1][0] - 0.35
    c2 = L[2][0] - 0.35
    c3 = L[4][0] - 0.3
    hit = L[4][0] + 1.6

    def march():
        focus = (540, 720)
        zoom = 1.0 + 0.05 * ease(lt / (c1 + 0.4))
        cam = Cam(c, focus, zoom)
        M.plain_below(an, c, t, cam, "pb206", 0.95, 1.0, True, -40, 700 - 22 * lt, 872)

        def figs(cc):
            with Cam(cc, focus, zoom)(1.0):
                M.rider(cc, 640 - 20 * lt, 872, 0.3, -1, HOOMAN, t, {"hand_kind": "mace", "hand": (100, -330)}, "walk", t * 0.9)
        an.figures(c, figs, MORN, (0, 300, 1080, 1000))

        def fs(cc):
            with Cam(cc, focus, zoom)(1.0):
                M.rider(cc, 500 - 20 * lt, 876, 0.31, -1, "sohrab", t, {"hand": (110, -340), "rhand": (30, -300)}, "walk",
                        t * 0.9 + 0.4, rider_scale=0.92)
        an.figures(c, fs, COLT, (0, 300, 1080, 1000), alpha=190)
        vig(an, c, 140)

    def wall():
        empty_wall(an, c, t, lt - c1, c2 - c1 + 0.4, "ew206")

    def gate():
        lt3 = lt - c2
        focus = (560, 680)
        sh = 10 * math.sin(lt * 63) * math.exp(-max(0.0, lt - hit) * 5) * (lt > hit)
        c.save()
        c.translate(sh, sh * 0.5)
        zoom = 1.0 + 0.04 * ease(lt3 / (dur - c2))
        cam = Cam(c, focus, zoom)
        gate_burst(an, c, t, cam, "gb206", hit, lt, 330, 440, 1000)
        order = sstep(L[3][0], L[3][0] + 0.3, lt) * (1 - sstep(L[3][1] + 0.2, L[3][1] + 0.6, lt))
        ride = clamp((lt - L[4][0]) / 1.2)
        swing = sstep(hit - 0.7, hit - 0.25, lt)
        strike = sstep(hit - 0.2, hit, lt)
        sx = mix(650, 530, ease(ride))
        rpS = {"hand": (110, -340), "rhand": (mix(30, 120, order), mix(-300, -600, order)), "rhand_kind": "fist",
               "head": -10 + 6 * ride + math.sin(t * 0.7), "jaw": jaw(an, "SOHRAB", t, 9), "lean": -2, "wind": 0.9}
        if lt > L[4][0]:
            rpS.update(hand_kind="mace", hand=(mix(mix(110, 50, swing), 230, strike), mix(mix(-340, -620, swing), -380, strike)),
                       mace=mix(mix(10, -40, swing), 80, strike), rhand=(30, -300), rhand_kind="fist",
                       lean=mix(-4 * swing, 10, strike))
        rpH = {"hand_kind": "mace", "hand": (100, -330), "head": -12 + math.sin(t * 0.6), "jaw": jaw(an, "HOOMAN", t, 8)}

        def fh(cc):
            with Cam(cc, focus, zoom)(1.0):
                M.rider(cc, 990, 1000, 0.6, -1, HOOMAN, t, rpH, neck=5 * math.sin(t * 1.2))
        an.figures(c, fh, MORN, (0, 100, 1080, 1200))

        def fs(cc):
            with Cam(cc, focus, zoom)(1.0):
                if 0 < ride < 1:
                    M.rider(cc, sx, 1000, 0.66, -1, "sohrab", t, rpS, "gallop", t * 2.0, rider_scale=0.92)
                else:
                    M.rider(cc, sx, 1000, 0.66, -1, "sohrab", t, rpS, rider_scale=0.92, neck=6 * math.sin(t * 1.4))
        an.figures(c, fs, COLT, (0, 100, 1080, 1200), alpha=190)
        c.restore()
        vig(an, c, 150)

    cuts(c, lt, [(0.0, march), (c1, wall), (c2, gate)], 0.4)


# ================================================================== S07 the empty fortress
def p20_s07(an, c, t):
    """Inside: 'Gordafarid! Where are you?!' -- a soldier: 'They are gone, my lord. All of them.' -- Sohrab, with a
    bitter laugh: 'She promised me this fortress... and she kept her word.' -- (the empty battlements) 'The fortress
    was empty. Gordafarid was gone.' -- (his hand on his heart) 'And Sohrab felt a pain in his heart that no sword had
    ever given him.' -- (he looks up; he sees her there again, laughing) 'Who are you, Gordafarid... and why can't I
    forget your face?'"""
    lt, dur = loc(an, "S07", t)
    L = [LN("p20", "S07", k) for k in range(6)]
    c1 = L[1][0] - 0.35
    c2 = L[2][0] - 0.35
    c3 = L[3][0] - 0.3
    c4 = L[4][0] - 0.3
    c5 = L[5][0] - 0.3

    def court():
        focus = (560, 700)
        zoom = 1.0 + 0.05 * ease(lt / (c1 + 0.4))
        cam = Cam(c, focus, zoom)
        M.gate_court(an, c, t, cam, "gc207", 1.0, 540)
        ride = clamp(lt / 1.6)
        shout = sstep(L[0][0] - 0.1, L[0][0] + 0.3, lt)
        rp = {"hand": (110, -340), "rhand": (mix(30, 150, shout), mix(-300, -520, shout)), "rhand_kind": "open",
              "head": -14 * shout + math.sin(t * 0.8), "jaw": jaw(an, "SOHRAB", t, 10), "lean": -3 * shout, "wind": 0.7}

        def ft(cc):
            with Cam(cc, focus, zoom)(1.0):
                for i, (x0, x1, d0) in enumerate(((120, 200, 0.0), (980, 860, 0.4))):
                    u = clamp((lt - d0) / 2.0)
                    person(cc, mix(x0, x1, u), 880, 0.6, 1 if x1 > x0 else -1,
                           {"mode": "walk" if u < 1 else "stand", "phase": lt * 4.4 + i, "stride": 16, "seed": i,
                            "rhand_kind": "spear", "rhand": (-10, -300), "head": -6 + 4 * math.sin(t * 0.9 + i)}, t, TURK)
        an.figures(c, ft, DAY, (0, 300, 1080, 1100))

        def fs(cc):
            with Cam(cc, focus, zoom)(1.0):
                M.rider(cc, mix(540, 640, ease(ride)), mix(872, 900, ride), mix(0.5, 0.6, ride), 1, "sohrab", t, rp,
                        "walk" if ride < 1 else "stand", t * 0.9, rider_scale=0.92)
        an.figures(c, fs, COLT, (0, 200, 1080, 1100), alpha=180)
        vig(an, c, 150)

    def report():
        lt2 = lt - c1
        focus = (540, 700)
        zoom = 1.0 + 0.05 * ease(lt2 / (c2 - c1 + 0.4))
        cam = Cam(c, focus, zoom)
        M.gate_court(an, c, t, cam, "gc207b", 1.0, 760)
        open_ = sstep(L[1][0] + 0.2, L[1][0] + 0.7, lt)
        PT = {"hand": (mix(40, 140, open_), mix(-262, -360, open_)), "hand_kind": "open",
              "rhand": (mix(-20, 60, open_), mix(-270, -330, open_)), "rhand_kind": "open",
              "head": 6 + math.sin(t * 0.9), "jaw": jaw(an, "RIDER", t, 9), "lean": 4}
        rp = {"hand": (110, -340), "rhand": (30, -300), "head": 8 + math.sin(t * 0.6), "wind": 0.7}

        def ft(cc):
            with Cam(cc, focus, zoom)(1.0):
                person(cc, 250, 1180, 1.06, 1, PT, t, TURK)
        an.figures(c, ft, DAY, (0, 100, 1080, 1300))

        def fs(cc):
            with Cam(cc, focus, zoom)(1.0):
                M.rider(cc, 790, 1180, 0.8, -1, "sohrab", t, rp, rider_scale=0.92, neck=5 * math.sin(t * 1.3))
        an.figures(c, fs, COLT, (0, 100, 1080, 1300), alpha=180)
        vig(an, c, 150)

    def bitter():
        laugh = sstep(L[2][0] + 1.6, L[2][0] + 2.2, lt)
        rp = {"hand": (110, -340), "rhand": (mix(30, 60, laugh), mix(-300, -330, laugh)), "rhand_kind": "fist",
              "head": 6 - 14 * laugh + 2 * math.sin(t * 9) * laugh * (1 - sstep(L[2][1], L[2][1] + 0.4, lt)),
              "jaw": jaw(an, "SOHRAB", t, 9), "lean": -3 * laugh, "wind": 0.7}
        him_court(an, c, t, lt - c2, c3 - c2 + 0.4, "hc207", rp)

    def empty():
        empty_wall(an, c, t, lt - c3, c4 - c3 + 0.4, "ew207")

    def heart():
        h = sstep(L[4][0] + 0.6, L[4][0] + 1.4, lt)
        rp = {"hand": (110, -340), "rhand": (mix(30, 70, h), mix(-300, -400, h)), "rhand_kind": "open",
              "head": 8 + 10 * h + math.sin(t * 0.6), "lean": 5 * h, "wind": 0.7}
        him_court(an, c, t, lt - c4, c5 - c4 + 0.4, "hc207b", rp, 0.08)

    def memory():
        lt6 = lt - c5
        ghost = sstep(L[5][0] + 0.6, L[5][0] + 2.0, lt) * (1 - sstep(dur - 0.6, dur, lt))
        laugh = 1.0
        P = {"hand": (60, -300), "hand_kind": "fist",
             "rhand": (140, -470 + 20 * math.sin(t * 5)), "rhand_kind": "open",
             "head": -14 + 3 * math.sin(t * 11) * laugh, "lean": -4, "wind": 1.4}
        empty_wall(an, c, t, lt6, dur - c5, "ew207b", ghost, P, 0.08)

    cuts(c, lt, [(0.0, court), (c1, report), (c2, bitter), (c3, empty), (c4, heart), (c5, memory)], 0.4)


# ================================================================== S08 + END I am coming; the letter rides
def p20_s08(an, c, t):
    """Sohrab on the wall of the empty fortress, looking west: 'Run, Gordafarid. Run to your king. I am coming. All the
    way to his throne.' -- 'But far away, Gazhdaham's letter was racing toward King Kavus...' (the messenger galloping
    into the sunset)."""
    lt = t - an.start["S08"]
    dur = an.end["END"] - an.start["S08"]
    L = [LN("p20", "S08", k) for k in range(3)]
    cut = L[2][0] - 0.35

    def wall():
        focus = (560, 660)
        zoom = 1.0 + 0.08 * ease(lt / (cut + 0.4))
        cam = Cam(c, focus, zoom)
        point = sstep(L[0][0] + 0.4, L[0][0] + 1.0, lt) * (1 - sstep(L[0][1] + 0.2, L[0][1] + 0.6, lt))
        fist = sstep(L[1][0] + 0.2, L[1][0] + 0.7, lt)
        P = {"hand_kind": "spear", "hand": (90, -320), "rhand": (mix(mix(-20, 200, point), 110, fist), mix(mix(-270, -460, point), -560, fist)),
             "rhand_kind": "open" if point > 0.3 else "fist", "head": 2 - 4 * point - 3 * fist + math.sin(t * 0.6),
             "jaw": jaw(an, "SOHRAB", t, 9), "wind": 1.2}

        def figs(cc):
            with Cam(cc, focus, zoom)(1.0):
                person(cc, 420, 1330, 1.36, 1, P, t, "sohrab")
        M.wall_top(an, c, t, cam, "wt208", figs, 0.35, -200, 0.0, (255, 176, 120), 1040, (0, 0, 1080, 1500), 720)
        vig(an, c, 150)

    def ride():
        lt2 = lt - cut
        ride_bg(an, c, t, lt2, "rb208", 560)
        zoom = 1.0 + 0.05 * ease(lt2 / (dur - cut))
        focus = (540, 760)

        def figs(cc):
            with Cam(cc, focus, zoom)(1.0):
                M.rider(cc, 560, 942, 0.7, -1, "guard", t, {"hand": (120, -360), "rhand": (40, -330), "lean": 12, "wind": 1.3},
                        "gallop", t * 2.3)
        an.figures(c, figs, (255, 170, 110), (0, 200, 1080, 1200))
        Q.trail(c, 560, 942, lt2, t, 0.9, 1, 3)
        vig(an, c, 150)

    cuts(c, lt, [(0.0, wall), (cut, ride)], 0.45)


P20 = {"S01": p20_s01, "TITLE": p20_s01, "S02": p20_s02, "S03": p20_s03, "S04": p20_s04, "S05": p20_s05,
       "S06": p20_s06, "S07": p20_s07, "S08": p20_s08, "END": p20_s08}
SHIFT20 = {}

register(P20, SHIFT20)
