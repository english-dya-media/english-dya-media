"""Part 19 (Gazhdaham's Letter; row 10 of OUTLINE.md, first half): every shot as a shadow-play scene.

Importing this module imports p18_scenes (and through it parts 15-17) and registers part 19's shots; p20_scenes.py
imports it and registers part 20's.
New here, to reuse: wall_low2() (wall_low with a behind() hook drawn in the sky, behind the person), her_wall() /
him_gate() (shot / reverse shot: Gordafarid on the battlements against the sky, Sohrab at the shut gate looking up),
wall_two() (both in one frame: her on the wall walk, the merlons in front of her legs, him at the gate below),
sky_shadow() (a giant figure as a dark shadow in the sky: a vision), wall_dusk() (on the wall at sunset: the Turanian
camp on the plain below, tents and many fires), letter_room() (a scribe writing by a candle against the lit curtain,
Gazhdaham dictating), curtain_story() (the full lit curtain, the letter's story told in cast shadows), pen_insert()
(close-up of a reed pen writing a Persian letter, right to left), fort_window() (an arched window on the plain at
night: hills, moon and the enemy's fires), night_room() (two people at that window, a lamp in Gazhdaham's hand),
messenger_out() (a rider leaving the White Fortress by night).
Line timings come from p19/audio/timeline.json (LN), so the action follows the voices.
"""
import math, random
import skia
import anim
from anim import C, mix, mixc, clamp, ease, sstep, Cam, Pen, ANCH, rope, spath, ppath, paint, fillp, taper, W, H
from puppets import person, horse, LOOKS
import sets as S
import p15_scenes as M
import p16_scenes as P16
import p17_scenes as Q
import p18_scenes as R
from ep01_scenes import loc, jaw, get, vig, tag, A, ground, INK
from p05_scenes import register, shadow_layer, candle_light, standing_candle, MOON
from p07_scenes import LN, dissolve, seated, cypress
from p09_scenes import flick, NIGHT, WARM
from p11_scenes import COLT, curtain, army_band
from p13_scenes import cuts, white_fortress

GAZH, MORN, HOJIR, STONE = M.GAZH, M.MORN, M.HOJIR, M.STONE
GORD_BARE = Q.GORD_BARE
SUNSET = (255, 150, 104)                                         # rim light at sunset
SAM = dict(LOOKS["warrior_ir"], beard="long", heavy=True, b=1.12)  # Sam the rider, Rostam's grandfather (as in p09)
SHADOW = (70, 28, 16)                                             # cast shadows on the lit curtain


# ------------------------------------------------------------------ the wall by day
def wall_low2(an, c, t, cam, key, figs, top=1150, mood=1.0, sun=(560, 520), behind=None, rim=MORN):
    """R.wall_low (looking up at the battlements) with behind(cam) drawn in the sky, behind the person."""
    S.lin(c, 0, top, [(0, mixc((60, 92, 156), (70, 104, 164), mood)), (0.6, (160, 178, 206)), (1, (236, 222, 196))])
    with cam(0.12):
        S.sun(c, sun[0], sun[1], 70, (255, 248, 222), (255, 214, 150), 620, 170)
        get(an, key + "cl", lambda: S.Clouds([(320, 12), (420, 9), (560, 14)], 182, 300, 700)).draw(c, t, (176, 176, 200), 150)
    if behind:
        behind(cam)
    an.figures(c, figs, rim, (0, 0, 1080, 1500))
    with cam(1.0):
        M.parapet(c, top, merlon=110, gap=70, mood=mood)


def her_wall(an, c, t, lt, dur, key, P, x=430, face=1, zk=0.06, behind=None, sun=(500, 600), zoom0=0.0, focus=(540, 640)):
    """Gordafarid bare-headed on the battlements against the sky (close, looking down at Sohrab when face=1)."""
    zoom = 1.0 + zoom0 + zk * ease(lt / max(dur, 0.1))
    cam = Cam(c, focus, zoom)

    def figs(cc):
        with Cam(cc, focus, zoom)(1.0):
            person(cc, x, 1330, 1.36, face, P, t, GORD_BARE)
    wall_low2(an, c, t, cam, key, figs, top=1150, sun=sun, behind=(lambda cm: behind(cm)) if behind else None)
    vig(an, c, 150)


def him_gate(an, c, t, lt, dur, key, rp, zk=0.05, x=700, gait="stand", rear=0.0):
    """Sohrab on his colt at the shut gate, close (the wall fills the frame behind him)."""
    focus = (600, 660)
    zoom = 1.02 + zk * ease(lt / max(dur, 0.1))
    cam = Cam(c, focus, zoom)
    R.gate_outside(an, c, t, cam, key, 0.0, 400, 1.0, 440, 1000)

    def fs(cc):
        with Cam(cc, focus, zoom)(1.0):
            if rear > 1:
                M.rider(cc, x, 1000, 0.8, -1, "sohrab", t, rp, "rear", 0.0, rider_scale=0.92, rear=rear)
            else:
                M.rider(cc, x, 1000, 0.8, -1, "sohrab", t, rp, gait, t * 0.9, rider_scale=0.92,
                        neck=6 * math.sin(t * 1.4), head=4 * math.sin(t * 0.9))
    an.figures(c, fs, COLT, (0, 100, 1080, 1200), alpha=180)
    vig(an, c, 150)


def merlons(c, top, gy, wall=STONE):
    """The merlons of gate_outside() drawn again, in front of a person standing on the wall walk."""
    pw = skia.Paint(AntiAlias=True)
    pw.setShader(skia.GradientShader.MakeLinear([skia.Point(0, top - 80), skia.Point(0, gy + 20)],
                                                [C(*mixc(wall, (255, 226, 190), 0.25)), C(*mixc(wall, (120, 108, 120), 0.35)),
                                                 C(*mixc(wall, (60, 50, 60), 0.55))], [0.0, 0.6, 1.0]))
    path = skia.Path()
    for k in range(-8, 30):
        path.addRect(skia.Rect.MakeLTRB(k * 96, top - 70, k * 96 + 58, top + 1))
    path.addRect(skia.Rect.MakeLTRB(-500, top - 2, 1600, top + 40))
    c.drawPath(path, pw)


def wall_two(an, c, t, lt, dur, key, PG, rpS, gx=330, sx=790, zk=0.05, top=600, gy=1080, gs=0.5):
    """Both in one frame: Gordafarid on the wall walk (the merlons in front of her legs), Sohrab at the gate below."""
    focus = (560, 700)
    zoom = 1.0 + zk * ease(lt / max(dur, 0.1))
    cam = Cam(c, focus, zoom)
    R.gate_outside(an, c, t, cam, key, 0.0, 560, 1.0, top, gy)

    def fg(cc):
        with Cam(cc, focus, zoom)(0.6):
            person(cc, gx, top + 30, gs, 1, PG, t, GORD_BARE)
    an.figures(c, fg, MORN, (0, 100, 1080, 900))
    with cam(0.6):
        merlons(c, top, gy)

    def fs(cc):
        with Cam(cc, focus, zoom)(1.0):
            M.rider(cc, sx, gy, 0.56, -1, "sohrab", t, rpS, rider_scale=0.92, neck=6 * math.sin(t * 1.4))
    an.figures(c, fs, COLT, (0, 300, 1080, 1300), alpha=180)
    vig(an, c, 145)


def sky_shadow(c, cam, a, t, up=0.0, x=830, y=1250, s=1.45):
    """A vision: Rostam as a giant dark shadow in the sky, his ox-head mace rising (up 0..1)."""
    if a <= 0.01:
        return
    with cam(0.25):
        shadow_layer(c, (0, 0, W, H), 0.5 * a, (60, 66, 100), 5.0)
        person(c, x, y, s, -1, {"hand_kind": "oxmace", "hand": (mix(110, 60, up), mix(-330, -560, up)),
                                "mace": mix(10, -10, up), "head": -2, "wind": 0.9, "stance": (58, 48)}, t, "rostam")
        c.restore()


# ------------------------------------------------------------------ the wall at sunset
def camp_img(seed, horizon, par):
    """The Turanian camp on the plain below the wall: tents, smaller toward the horizon (cached image, 600 px wider
    than the frame), and the fire positions."""
    surf = skia.Surface(W + 600, H)
    cc = surf.getCanvas()
    cc.clear(C(0, 0, 0, 0))
    rnd = random.Random(seed)
    fires = []
    items = sorted([(rnd.uniform(-260, 1340), rnd.uniform(0.05, 1.0), rnd.uniform(0, 6.3)) for _ in range(40)], key=lambda q: q[1])
    for (x, u, ph) in items:
        y = horizon + 18 + u * u * (par - horizon - 70)
        s = 0.07 + 0.2 * u * u
        S.tent(cc, x + 300 + 70 * s / 0.2, y, s, 0.0, (34, 18, 26))
        fires.append((x, y, s, ph))
    return surf.makeImageSnapshot(), fires


def wall_dusk(an, c, t, cam, key, figs=None, par=1040, horizon=700, box=(0, 100, 1080, 1400), rim=SUNSET, fires=1.0):
    """On the wall of the White Fortress at sunset: the sun going down, the Turanian camp on the plain below with its
    tents and many fires, the people (figs), the parapet in front of them (top at par)."""
    S.lin(c, 0, horizon + 40, [(0, (26, 22, 58)), (0.45, (112, 64, 98)), (0.8, (236, 128, 92)), (1, (252, 170, 110))])
    with cam(0.1):
        get(an, key + "st", lambda: S.Stars(50, horizon - 300, 197)).draw(c, t, 0.4, horizon - 300)
        S.sun(c, 860, horizon + 26, 62, (255, 226, 170), (255, 120, 80), 520, 150)
    rg = get(an, key + "rg", lambda: (S.make_ridge(-600, 1700, horizon - 40, 40, 191, 8, 4, 0.4),
                                      S.make_ridge(-600, 1700, horizon, 14, 192)))
    with cam(0.2):
        S.ridge(c, rg[0], (96, 54, 84))
        S.ridge(c, rg[1], (74, 42, 66))
    with cam(0.3):
        S.lin(c, horizon + 6, par + 200, [(0, (120, 64, 70)), (1, (36, 20, 30))], (-600, horizon + 6, 1700, par + 200))
        img, fl = get(an, (key, "camp"), lambda: camp_img(198, horizon, par))
        c.drawImage(img, -300, 0)
        if fires > 0.01:
            for k, (x, y, s, ph) in enumerate(fl):
                S.glow(c, x, y - 6, 260 * s, (255, 150, 70), (150 + 40 * math.sin(t * 6 + ph)) * fires)
                S.flame(c, x, y - 2, 0.25 * s, t, ph, fires)
    if figs:
        an.figures(c, figs, rim, box)
    with cam(1.0):
        M.parapet(c, par, col=(172, 146, 150), mood=0.0)


# ------------------------------------------------------------------ the letter
def letter_room(an, c, t, PW, PZ, zoom, focus=(560, 700), zx=800):
    """A scribe writing by the candle against the lit curtain (on his dais at the left), Gazhdaham standing and
    dictating at the right (p13's scribe_wall with Gazhdaham)."""
    cam = Cam(c, focus, zoom)
    curtain(c, t)
    with cam(1.0):
        ground(c, 1100, (70, 30, 20), (12, 5, 4))

    def figs(cc):
        with Cam(cc, focus, zoom)(1.0):
            fillp(cc, ppath([(20, 860), (520, 860), (532, 876), (532, 1200), (20, 1200)]))
            tag("w:")
            seated(cc, 210, 860, 1.25, 1, PW, t, "poet")
            tag("")
            fillp(cc, ppath([(372, 860), (384, 860), (430, 774), (418, 772)]))
            fillp(cc, ppath([(448, 860), (436, 860), (392, 774), (404, 772)]))
            fillp(cc, ppath([(360, 770), (450, 784), (456, 774), (366, 760)]))
            person(cc, zx, 1100, 1.35, -1, PZ, t, GAZH)
    an.figures(c, figs, WARM, (0, 200, 1080, 1300), alpha=170, anchors=True)
    with cam(1.0):
        pg = paint(C(250, 228, 180))
        c.drawPath(ppath([(364, 756), (408, 764), (408, 778), (362, 770)]), pg)
        c.drawPath(ppath([(408, 764), (454, 770), (452, 784), (408, 778)]), pg)
        standing_candle(c, 600, 1100, t, 0.9, 2.0)
    vig(an, c, 170)


def curtain_story(an, c, t, lt, dur, draw, zk=0.05, extra=None):
    """The lit curtain filling the frame; draw(c) casts the story on it as soft shadows."""
    focus = (540, 600)
    zoom = 1.0 + zk * ease(lt / max(dur, 0.1))
    cam = Cam(c, focus, zoom)
    curtain(c, t)
    with cam(1.0):
        shadow_layer(c, (0, 0, W, H), 0.86, SHADOW, 2.4)
        draw(c)
        c.restore()
        if extra:
            extra(c)
    vig(an, c, 165)


def writing(c, x0, x1, y, u, seed):
    """One line of Persian handwriting, written right to left (u = 0..1 of the line)."""
    if u <= 0:
        return
    rnd = random.Random(seed)
    p = skia.Paint(AntiAlias=True, Color=C(54, 28, 18))
    p.setStyle(skia.Paint.kStroke_Style)
    p.setStrokeWidth(3.2)
    p.setStrokeCap(skia.Paint.kRound_Cap)
    xs = x1
    xend = x1 - u * (x1 - x0)
    dots = paint(C(54, 28, 18))
    while xs > xend:
        wlen = rnd.uniform(40, 96)
        xe = max(xend, xs - wlen)
        path = skia.Path()
        path.moveTo(xs, y)
        n = max(2, int((xs - xe) / 6))
        for i in range(1, n + 1):
            xx = xs - (xs - xe) * i / n
            yy = y + 3.5 * math.sin(xx * 0.21 + seed) + 2.5 * math.sin(xx * 0.53)
            if rnd.random() < 0.12:
                yy -= rnd.uniform(8, 18)
            path.lineTo(xx, yy)
        c.drawPath(path, p)
        if rnd.random() < 0.6:
            c.drawCircle(xs - (xs - xe) * rnd.uniform(0.2, 0.8), y + rnd.choice((-14, 12)), 2.6, dots)
        xs = xe - rnd.uniform(12, 20)


def pen_insert(an, c, t, lt, dur, rows=2):
    """Close-up by candlelight: a reed pen writing a Persian letter, line after line, right to left."""
    focus = (540, 600)
    zoom = 1.0 + 0.06 * ease(lt / max(dur, 0.1))
    cam = Cam(c, focus, zoom)
    S.lin(c, 0, H, [(0, (26, 12, 10)), (0.5, (74, 38, 24)), (1, (14, 6, 6))])
    with cam(1.0):
        S.glow(c, 900, 330, 760, (255, 170, 90), 120 * flick(t))
        x0, x1, y0, y1 = 150, 930, 420, 800
        sheet = skia.Rect.MakeLTRB(x0, y0, x1, y1)
        c.drawRect(sheet, paint(C(244, 222, 176)))
        S.lin(c, y0, y1, [(0, (255, 236, 200, 0)), (1, (120, 70, 40, 90))], (x0, y0, x1, y1))
        prog = clamp((lt - 0.3) / max(dur - 0.6, 0.5)) * rows
        tip = (x1 - 60, y0 + 70)
        for r in range(rows):
            u = clamp(prog - r)
            if u <= 0:
                break
            y = y0 + 70 + r * 58
            xl = x0 + 60 + (r * 53 % 7) * 14
            writing(c, xl, x1 - 60, y, u, 19 + r)
            tip = (x1 - 60 - u * (x1 - 60 - xl), y)
    # the reed pen (a dark silhouette with a warm rim), the writing hand just out of the frame

    def figs(cc):
        with Cam(cc, focus, zoom)(1.0):
            tx, ty = tip
            bob = 3 * math.sin(t * 9.0)
            taper(cc, [(tx, ty), (tx + 70, ty - 70 + bob), (tx + 200, ty - 180 + bob * 2), (tx + 310, ty - 235 + bob * 3)],
                  2.4, 10.0)
    an.figures(c, figs, WARM, (0, 0, 1080, 1300), alpha=160)
    vig(an, c, 175)


# ------------------------------------------------------------------ night
def fort_window(an, c, t, cam, x, yb, w, h, key, fires=1.0):
    """Dark wall with a tall arched window on the plain at night: stars, the moon, far hills, the enemy's fires."""
    S.lin(c, 0, H, [(0, (10, 10, 22)), (0.5, (22, 22, 40)), (1, (5, 4, 8))])
    arch = S.arch_path(x, yb, w, h)
    with cam(0.5):
        c.save()
        c.clipPath(arch, skia.ClipOp.kIntersect, True)
        S.lin(c, yb - h, yb, [(0, (10, 14, 40)), (0.6, (34, 44, 92)), (1, (70, 76, 120))], (x - w, yb - h - 40, x + w, yb + 10))
        get(an, key + "st", lambda: S.Stars(80, 900, 199)).draw(c, t, 1.0, 900)
        S.moon(c, x + w * 0.16, yb - h * 0.66, w * 0.12)
        get(an, key + "cl", lambda: S.Clouds([(yb - h * 0.38, 10), (yb - h * 0.28, 7)], 201, 200, 420)).draw(
            c, t * 2, (20, 24, 50), 170)
        rg = get(an, key + "rg", lambda: S.make_ridge(x - w, x + w, yb - 230, 40, 202, 8, 4, 0.3))
        S.ridge(c, rg, (24, 24, 46))
        S.lin(c, yb - 190, yb, [(0, (40, 30, 46)), (1, (14, 10, 18))], (x - w, yb - 190, x + w, yb))
        rnd = random.Random(203)
        for k in range(16):
            fx = x - w * 0.46 + rnd.uniform(0, w * 0.92)
            fy = yb - 170 + rnd.uniform(0, 1) ** 2 * 140
            S.glow(c, fx, fy, 22 + (fy - yb + 170) * 0.25, (255, 140, 60), (160 + 50 * math.sin(t * 7 + k)) * fires)
            c.drawCircle(fx, fy, 2.0 + (fy - yb + 170) * 0.02, paint(C(255, 210, 140, int(230 * fires))))
        c.restore()
        edge = skia.Paint(AntiAlias=True, Color=C(*INK))
        edge.setStyle(skia.Paint.kStroke_Style)
        edge.setStrokeWidth(26)
        c.drawPath(arch, edge)
        pt = paint(C(*INK))
        c.drawRect(skia.Rect.MakeLTRB(x - w / 2 - 40, yb, x + w / 2 + 40, yb + 26), pt)
    p = skia.Paint(AntiAlias=True)
    p.setShader(skia.GradientShader.MakeLinear([skia.Point(x, yb - h), skia.Point(x - w * 1.4, yb + 500)],
                                               [C(150, 170, 230, 60), C(150, 170, 230, 0)]))
    c.drawPath(ppath([(x - w / 2, yb - h * 0.7), (x + w / 2, yb - h * 0.5), (x + w * 0.1, yb + 700),
                      (x - w * 1.6, yb + 700)]), p)


def night_room(an, c, t, lt, dur, PG, PZ, key, gx=260, zx=830, zk=0.06, face_g=1, face_z=-1, focus=(540, 700),
               zoom0=0.0, floor=0.0, fires=1.0):
    """Gordafarid (left) and Gazhdaham (right, a lamp in his hand) at the window at night; floor (0..1) brightens
    the floor where he lowers the lamp."""
    zoom = 1.0 + zoom0 + zk * ease(lt / max(dur, 0.1))
    cam = Cam(c, focus, zoom)
    fort_window(an, c, t, cam, 540, 1010, 400, 720, key, fires)
    with cam(1.0):
        ground(c, 1330, (30, 20, 24), (6, 4, 6))

    def figs(cc):
        with Cam(cc, focus, zoom)(1.0):
            tag("g:")
            person(cc, gx, 1330, 1.4, face_g, PG, t, GORD_BARE)
            tag("z:")
            person(cc, zx, 1330, 1.46, face_z, PZ, t, GAZH)
            tag("")
    an.figures(c, figs, NIGHT, (0, 150, 1080, 1500), anchors=True)
    p = candle_light(c, an, "z:flame", t, 560, 115)
    if p and floor > 0.01:
        S.glow(c, p[0] - 40, p[1] + 380, 420, (255, 170, 90), 90 * floor)
    vig(an, c, 170)


def messenger_out(an, c, t, lt, dur, key):
    """The White Fortress under the moon: a rider leaves the gate at a gallop and vanishes into the dark."""
    focus = (560, 720)
    zoom = 1.0 + 0.05 * ease(lt / max(dur, 0.1))
    cam = Cam(c, focus, zoom)
    white_fortress(an, c, t, cam, key)
    u = clamp((lt - 0.4) / max(dur - 0.8, 1.0))

    def figs(cc):
        with Cam(cc, focus, zoom)(0.5):
            if u < 0.62:
                v = u / 0.62
                x, y, s = mix(632, 600, v), mix(752, 900, v), mix(0.05, 0.13, v)
            else:
                v = (u - 0.62) / 0.38
                x, y, s = mix(600, 120, v), mix(900, 940, v), mix(0.13, 0.15, v)
            M.rider(cc, x, y, s, -1, "guard", t, {"hand": (110, -340), "rhand": (30, -320), "lean": 10}, "gallop", t * 2.2)
    an.figures(c, figs, MOON, (0, 500, 1080, 1100), alpha=200)
    vig(an, c, 160)


# ================================================================== S01 + TITLE (hook)
def p19_s01(an, c, t):
    """Hook + title: Gordafarid on the wall, laughing down at him: 'Why so sad, Turk? Did you think a girl of Iran would
    be yours?' -- Sohrab at the shut gate, looking up: 'Laugh, moon-face. Laugh while you can.'"""
    lt = t - an.start["S01"]
    dur = an.end["TITLE"] - an.start["S01"]
    a0, a1 = LN("p19", "S01", 0)
    b0, b1 = LN("p19", "S01", 1)
    cut = b0 - 0.35

    def her():
        laugh = sstep(a0 + 0.2, a0 + 0.8, lt)
        point = sstep(a0 + 1.6, a0 + 2.2, lt)
        P = {"hand": (mix(50, 175, point), mix(-290, -330, point)), "hand_kind": "open" if point > 0.3 else "fist",
             "rhand": (mix(-20, 130, laugh * (1 - point)), mix(-270, -440 + 16 * math.sin(t * 5), laugh * (1 - point))),
             "rhand_kind": "open", "head": 8 * point - 10 * laugh * (1 - point) + 3 * math.sin(t * 10) * laugh,
             "lean": -3 * laugh + 4 * point, "jaw": jaw(an, "GORDAFARID", t, 8), "wind": 1.4}
        her_wall(an, c, t, lt, cut + 0.4, "w191", P)

    def him():
        lt2 = lt - cut
        down = sstep(b1 + 1.0, b1 + 2.6, lt)
        rp = {"hand": (110, -340), "rhand": (mix(30, 70, 1 - down), mix(-300, -360, 1 - down)), "rhand_kind": "fist",
              "head": -16 + 18 * down + math.sin(t * 0.7), "jaw": jaw(an, "SOHRAB", t, 9), "lean": -3, "wind": 0.9}
        him_gate(an, c, t, lt2, dur - cut, "g191", rp, 0.08)

    cuts(c, lt, [(0.0, her), (cut, him)], 0.35)


# ================================================================== S02 the gate shut in his face
def p19_s02(an, c, t):
    """'Gordafarid had tricked Sohrab and escaped into the White Fortress.' (the fortress, Sohrab small at the gate)
    'Now the gate was shut in his face.' (Sohrab at the gate) 'And high on the wall, she laughed down at him.'"""
    lt, dur = loc(an, "S02", t)
    L = [LN("p19", "S02", k) for k in range(3)]
    c1 = L[1][0] - 0.35
    c2 = L[2][0] + 1.2

    def wide():
        focus = (580, 820)
        zoom = 1.0 + 0.05 * ease(lt / (c1 + 0.4))
        cam = Cam(c, focus, zoom)
        M.fortress_far(an, c, t, cam, "ff192", mood=0.9, gate=0.0, fx=170, fy=300, fs=1.0)

        def figs(cc):
            with Cam(cc, focus, zoom)(0.5):
                M.rider(cc, 676, 858, 0.15, -1, "sohrab", t, {"hand": (110, -340), "rhand": (30, -300)}, rider_scale=0.92,
                        neck=6 * math.sin(t * 1.5))
        an.figures(c, figs, MORN, (0, 500, 1080, 1100))
        vig(an, c, 140)

    def gate():
        lt2 = lt - c1
        up = sstep(L[2][0] + 0.2, L[2][0] + 1.0, lt)
        rp = {"hand": (110, -340), "rhand": (30, -300), "head": 6 * math.sin(t * 2.2) * (1 - up) - 18 * up + 4,
              "lean": -2 * up, "wind": 0.9}
        him_gate(an, c, t, lt2, c2 - c1 + 0.4, "g192", rp)

    def wall():
        lt3 = lt - c2
        laugh = sstep(0.0, 0.5, lt3)
        P = {"hand": (60, -300), "hand_kind": "fist",
             "rhand": (mix(-20, 140, laugh), mix(-270, -470 + 20 * math.sin(t * 5), laugh)), "rhand_kind": "open",
             "head": -6 - 10 * laugh + 3 * math.sin(t * 11) * laugh, "lean": -4 * laugh, "wind": 1.4}
        her_wall(an, c, t, lt3, dur - c2, "w192", P, sun=(520, 560))

    cuts(c, lt, [(0.0, wide), (c1, gate), (c2, wall)], 0.4)


# ================================================================== S03 her mockery
def p19_s03(an, c, t):
    """Gordafarid: 'Why so sad, Turk? Did you think a girl of Iran would be yours?' (pointing down at him) -- (on
    Sohrab) 'Don't be sad. It was not meant to be.' -- 'But listen to me, young hero. I don't think you are a Turk at
    all.' -- (both of them) 'With those arms and shoulders, no hero in the world is your equal.'"""
    lt, dur = loc(an, "S03", t)
    L = [LN("p19", "S03", k) for k in range(4)]
    c1 = L[1][0] - 0.3
    c2 = L[2][0] - 0.35
    c3 = L[3][0] - 0.35

    def taunt():
        point = sstep(0.4, 1.0, lt)
        P = {"hand": (mix(50, 180, point), mix(-290, -320, point)), "hand_kind": "open",
             "rhand": (-30, -262), "rhand_kind": "fist", "head": 10 * point + 2 * math.sin(t * 9) * point,
             "lean": 5 * point, "jaw": jaw(an, "GORDAFARID", t, 8), "wind": 1.3}
        her_wall(an, c, t, lt, c1 + 0.4, "w193", P, sun=(560, 560))

    def him():
        lt2 = lt - c1
        rp = {"hand": (110, -340), "rhand": (30, -300), "rhand_kind": "fist", "head": -18 + math.sin(t * 0.6),
              "lean": -2, "wind": 0.9}
        him_gate(an, c, t, lt2, c2 - c1 + 0.4, "g193", rp)

    def listen():
        lt3 = lt - c2
        open_ = sstep(L[2][0] + 0.8, L[2][0] + 1.4, lt)
        P = {"hand": (mix(60, 150, open_), mix(-300, -380, open_)), "hand_kind": "open",
             "rhand": (mix(-20, 40, open_), mix(-270, -330, open_)), "rhand_kind": "open",
             "head": 8 + 3 * math.sin(t * 0.8), "lean": 6, "jaw": jaw(an, "GORDAFARID", t, 8), "wind": 1.2}
        her_wall(an, c, t, lt3, c3 - c2 + 0.4, "w193b", P, zoom0=0.04, sun=(560, 560))

    def both():
        lt4 = lt - c3
        arms = sstep(L[3][0] + 0.3, L[3][0] + 0.9, lt) * (1 - sstep(L[3][1] - 0.6, L[3][1], lt))
        PG = {"hand": (mix(60, 160, arms), mix(-290, -420, arms)), "hand_kind": "open",
              "rhand": (mix(-20, 110, arms), mix(-270, -440, arms)), "rhand_kind": "open",
              "head": 12 + 2 * math.sin(t * 0.8), "lean": 6, "jaw": jaw(an, "GORDAFARID", t, 8), "wind": 1.2}
        rpS = {"hand": (110, -340), "rhand": (30, -300), "head": -16 + math.sin(t * 0.7), "lean": -2, "wind": 0.9}
        wall_two(an, c, t, lt4, dur - c3, "t193", PG, rpS)

    cuts(c, lt, [(0.0, taunt), (c1, him), (c2, listen), (c3, both)], 0.35)


# ================================================================== S04 her warning: Rostam
def p19_s04(an, c, t):
    """'But when our king hears that an army has come from Turan...' (she points west) 'he will send Rostam. And no one
    can stand against Rostam.' (a vision: Rostam's giant shadow in the sky, his mace rising) -- (on Sohrab) 'Not one of
    your men will go home alive.' -- 'Don't trust your strength too much. Go back to Turan, while you can.'"""
    lt, dur = loc(an, "S04", t)
    L = [LN("p19", "S04", k) for k in range(4)]
    c1 = L[2][0] - 0.3
    c2 = L[3][0] - 0.35
    vis = sstep(L[1][0] + 0.2, L[1][0] + 1.4, lt)
    up = sstep(L[1][0] + 2.0, L[1][0] + 3.0, lt)

    def warn():
        point = sstep(0.3, 1.0, lt) * (1 - sstep(L[1][0] + 1.6, L[1][0] + 2.4, lt))
        P = {"hand": (mix(50, 200, point), mix(-290, -520, point)), "hand_kind": "open",
             "rhand": (-30, -262), "rhand_kind": "fist", "head": -4 * point + 6 * (1 - point) + math.sin(t * 0.8),
             "lean": -2 * point, "jaw": jaw(an, "GORDAFARID", t, 8), "wind": 1.3}
        her_wall(an, c, t, lt, c1 + 0.4, "w194", P, x=380, sun=(470, 600),
                 behind=lambda cam: sky_shadow(c, cam, vis, t, up, 800, 1300, 1.45))

    def him():
        lt2 = lt - c1
        rp = {"hand": (110, -340), "rhand": (30, -300), "rhand_kind": "fist", "head": -12 + 4 * sstep(0.4, 1.6, lt2),
              "lean": 0, "wind": 0.9}
        him_gate(an, c, t, lt2, c2 - c1 + 0.4, "g194", rp)

    def away():
        lt3 = lt - c2
        wave = sstep(L[3][0] + 1.6, L[3][0] + 2.0, lt)
        turn = lt > L[3][1] + 0.2
        flick_ = math.sin(t * 9) * wave * (1 - sstep(L[3][1] - 0.6, L[3][1], lt))
        P = {"hand": (mix(60, 170, wave) + 20 * flick_, mix(-300, -400, wave) - 10 * flick_), "hand_kind": "open",
             "rhand": (-30, -262), "rhand_kind": "fist", "head": 8 + math.sin(t * 0.8), "lean": 3,
             "jaw": jaw(an, "GORDAFARID", t, 8), "wind": 1.3}
        if turn:
            P = {"hand": (40, -262), "rhand": (-20, -270), "head": 2, "wind": 1.4}
        her_wall(an, c, t, lt3, dur - c2, "w194b", P, face=-1 if turn else 1, sun=(520, 580))

    cuts(c, lt, [(0.0, warn), (c1, him), (c2, away)], 0.35)


# ================================================================== S05 his shame, his threat
def p19_s05(an, c, t):
    """'Sohrab's face burned with shame.' (his head goes down) -- 'Laugh, moon-face. Laugh while you can. Tomorrow I
    will tear down these walls, stone by stone.' (fist raised) 'And then we will see who laughs.' -- 'He turned his
    horse and rode back to his camp.' (the plain: he gallops away towards the host)"""
    lt, dur = loc(an, "S05", t)
    L = [LN("p19", "S05", k) for k in range(5)]
    cut = L[4][0] - 0.3

    def him():
        shame = sstep(0.4, 1.4, lt) * (1 - sstep(L[1][0] - 0.4, L[1][0] + 0.2, lt))
        fist = sstep(L[2][0] + 0.2, L[2][0] + 0.7, lt) * (1 - sstep(L[3][1] - 0.2, L[3][1] + 0.3, lt))
        shake = math.sin(t * 13) * fist * (1 - sstep(L[2][1] - 0.4, L[2][1], lt))
        rear = 24 * math.sin(clamp((lt - L[3][1] - 0.1) / 1.0) * math.pi) if L[3][1] + 0.1 < lt < L[3][1] + 1.1 else 0.0
        rp = {"hand": (110, -340), "rhand": (mix(30, 110, fist) + 6 * shake, mix(-300, -630, fist) + 8 * shake),
              "rhand_kind": "fist", "head": -14 + 30 * shame - 4 * fist + math.sin(t * 0.7),
              "jaw": jaw(an, "SOHRAB", t, 9), "lean": 6 * shame - 3 * fist, "wind": 0.9}
        him_gate(an, c, t, lt, cut + 0.4, "g195", rp, 0.07, rear=rear)

    def ride():
        lt2 = lt - cut
        focus = (540, 720)
        zoom = 1.0 + 0.04 * ease(lt2 / (dur - cut))
        cam = Cam(c, focus, zoom)
        M.plain_below(an, c, t, cam, "pb195", 0.75, 1.0, True, -60, 700, 872)
        x = mix(260, 760, clamp(lt2 / (dur - cut + 1.0)))

        def figs(cc):
            with Cam(cc, focus, zoom)(1.0):
                M.rider(cc, x, 872, 0.32, 1, "sohrab", t, {"hand": (110, -340), "rhand": (30, -300), "lean": 8},
                        "gallop", t * 2.1, rider_scale=0.92)
        an.figures(c, figs, COLT, (0, 300, 1080, 1000), alpha=190)
        Q.trail(c, x, 872, lt2, t, 0.8, -1, 2)
        vig(an, c, 140)

    cuts(c, lt, [(0.0, him), (cut, ride)], 0.4)


# ================================================================== S06 evening on the wall
def p19_s06(an, c, t):
    """'That evening, the fires of the Turanian army burned all over the plain.' -- on the wall, Gazhdaham: 'You made
    him angry, my daughter. Tomorrow he will come with his whole army.' -- 'Our walls are high, Father.' -- 'Not high
    enough. Not for him.' (closer) 'Bring me a scribe. King Kavus must know who has come to Iran.'"""
    lt, dur = loc(an, "S06", t)
    L = [LN("p19", "S06", k) for k in range(5)]
    c1 = L[1][0] - 0.4
    c2 = L[3][0] - 0.3

    def wide():
        focus = (540, 760)
        zoom = 1.0 + 0.06 * ease(lt / (c1 + 0.4))
        cam = Cam(c, focus, zoom)
        wall_dusk(an, c, t, cam, "d196", None, par=1250, horizon=640)
        vig(an, c, 150)

    def poses(zj, gj):
        worry = sstep(L[1][0] + 0.4, L[1][0] + 1.0, lt) * (1 - sstep(L[1][1], L[1][1] + 0.5, lt))
        proud = sstep(L[2][0], L[2][0] + 0.5, lt) * (1 - sstep(L[2][1] + 0.4, L[2][1] + 1.0, lt))
        PZ = {"hand_kind": "staff", "hand": (60, -300), "rhand": (mix(-20, 130, worry), mix(-280, -400, worry)),
              "rhand_kind": "open" if worry > 0.3 else "fist", "head": 6 - 2 * worry + math.sin(t * 0.6),
              "jaw": zj, "lean": 3}
        PG = {"hand": (mix(40, 120, proud), mix(-262, -480, proud)), "hand_kind": "open" if proud > 0.3 else "fist",
              "rhand": (-20, -270), "head": 2 - 4 * proud + math.sin(t * 0.8), "jaw": gj, "wind": 1.0}
        return PZ, PG

    def two():
        lt2 = lt - c1
        focus = (540, 700)
        zoom = 1.0 + 0.05 * ease(lt2 / (c2 - c1 + 0.4))
        cam = Cam(c, focus, zoom)
        PZ, PG = poses(jaw(an, "GAZHDAHAM", t, 8), jaw(an, "GORDAFARID", t, 8))

        def figs(cc):
            with Cam(cc, focus, zoom)(1.0):
                person(cc, 290, 1330, 1.4, 1, PZ, t, GAZH)
                person(cc, 800, 1330, 1.34, -1, PG, t, GORD_BARE)
        wall_dusk(an, c, t, cam, "d196b", figs, par=1040, horizon=700, box=(0, 0, 1080, 1500))
        vig(an, c, 150)

    def close():
        lt3 = lt - c2
        focus = (300, 640)
        zoom = 1.22 + 0.05 * ease(lt3 / (dur - c2))
        cam = Cam(c, focus, zoom)
        turn = sstep(L[4][0] + 0.6, L[4][0] + 1.2, lt)
        call = sstep(L[4][0] + 1.0, L[4][0] + 1.6, lt) * (1 - sstep(L[4][1] - 0.6, L[4][1], lt))
        PZ = {"hand_kind": "staff", "hand": (60, -300), "rhand": (mix(-20, 150, call), mix(-280, -470, call)),
              "rhand_kind": "open" if call > 0.3 else "fist", "head": 4 - 6 * call + math.sin(t * 0.6),
              "jaw": jaw(an, "GAZHDAHAM", t, 8), "lean": -2 * call}

        def figs(cc):
            with Cam(cc, focus, zoom)(1.0):
                person(cc, 290, 1330, 1.4, -1 if turn > 0.5 else 1, PZ, t, GAZH)
                person(cc, 800, 1330, 1.34, -1, {"hand": (40, -262), "rhand": (-20, -270), "head": 4 + math.sin(t * 0.8),
                                                  "wind": 1.0}, t, GORD_BARE)
        wall_dusk(an, c, t, cam, "d196c", figs, par=1040, horizon=700, box=(0, 0, 1080, 1500))
        vig(an, c, 155)

    cuts(c, lt, [(0.0, wide), (c1, two), (c2, close)], 0.4)


# ================================================================== S07 the letter
def letter_shadows(an, t, lt, L):
    """What the letter says, told on the curtain: the army; the young hero taller than a cypress; Sohrab riding with the
    great shadow of Sam riding behind him."""
    army = sstep(L[1][0] - 0.2, L[1][0] + 0.6, lt) * (1 - sstep(L[1][0] + 2.4, L[1][0] + 3.0, lt))
    hero = sstep(L[1][0] + 2.6, L[1][0] + 3.4, lt)

    def draw(c):
        if army > 0.01:
            band = get(an, "p19band", lambda: army_band(False, 48, 1500, 300))
            c.saveLayerAlpha(None, int(255 * army))
            c.save()
            c.translate(-80 + 34 * lt, 610)
            c.scale(0.62, 0.62)
            c.drawImage(band, 0, 0)
            c.restore()
            c.restore()
        if hero > 0.01:
            c.saveLayerAlpha(None, int(255 * hero))
            cypress(c, 700, 820, 390, t, 1.0)
            person(c, 430, 820, 0.84, 1, {"hand_kind": "spear", "hand": (100, -330), "rhand": (-20, -262), "head": -3,
                                          "wind": 0.9, "stance": (52, 44)}, t, "sohrab")
            c.restore()
    return draw


def ride_shadows(an, t, lt, L):
    """'When he rides, you would think he is Sam, Rostam's grandfather, come back to life.'"""
    sam = sstep(L[4][0] + 1.4, L[4][0] + 2.8, lt)

    def draw(c):
        ph = t * 1.7
        if sam > 0.01:
            c.saveLayerAlpha(None, int(255 * 0.55 * sam))
            horse(c, 450 + 10 * sam, 900, 0.8, 1, {"gait": "gallop", "phase": ph + 0.25, "saddle": True, "rider": SAM,
                                                  "rider_pose": {"hand_kind": "mace", "hand": (120, -400), "mace": 30,
                                                                 "head": -2, "wind": 1.0}}, t)
            c.restore()
        horse(c, 560, 862, 0.64, 1, {"gait": "gallop", "phase": ph, "saddle": True, "rider": "sohrab", "rider_scale": 0.92,
                                     "rider_pose": {"hand_kind": "spear", "hand": (110, -360), "rhand": (30, -300),
                                                    "lean": 8, "wind": 1.2}}, t)
    return draw


def p19_s07(an, c, t):
    """Night. The pen writes (right to left) while Gazhdaham dictates: 'To Kavus, the great King of Iran.' -- (on the
    curtain, the story) 'An army has come to us from Turan. Its leader is young, almost a boy... but he is taller than a
    cypress, and his face shines like the sun.' -- (Gazhdaham and the scribe) 'His name is Sohrab. Hojir fought him, and
    now Hojir is his prisoner.' -- (the curtain) 'When he rides, you would think he is Sam, Rostam's grandfather, come
    back to life.' -- (Gazhdaham, a fist) 'If the king waits, Iran is lost. Send help, and send it fast.'"""
    lt, dur = loc(an, "S07", t)
    L = [LN("p19", "S07", k) for k in range(6)]
    c1 = L[1][0] - 0.3
    c2 = L[3][0] - 0.3
    c3 = L[4][0] - 0.3
    c4 = L[5][0] - 0.3

    def pen():
        pen_insert(an, c, t, lt, c1 + 0.4)

    def story():
        lt2 = lt - c1
        hero = sstep(L[1][0] + 2.6, L[1][0] + 3.4, lt)
        shine = sstep(L[2][0] + 2.0, L[2][0] + 2.8, lt)

        def extra(cc):
            if shine > 0.01:
                Q.sun_head(cc, 430 + 18, 820 - 0.84 * 1.05 * 520, shine * hero, t, 70)
        curtain_story(an, c, t, lt2, c2 - c1 + 0.4, letter_shadows(an, t, lt, L), extra=extra)

    def dictate(lt_, d_, fist=0.0, name=0.0):
        write = 1 - sstep(L[5][1] - 1.2, L[5][1] - 0.4, lt)
        look_up = sstep(L[5][0] + 1.6, L[5][0] + 2.4, lt)
        PW = {"hand_kind": "pen", "hand": (150 + 6 * math.sin(t * 5.1) * write, -262 + 4 * math.sin(t * 9.7) * write - 20 * look_up),
              "head": mix(10, -12, look_up) + 1.5 * math.sin(t * 1.3), "lean": mix(8, 0, look_up), "rhand": (-6, -262), "seed": 1.0}
        PZ = {"hand_kind": "staff", "hand": (60, -300), "rhand": (mix(mix(-20, 150, name), 120, fist), mix(mix(-280, -400, name), -470, fist)),
              "rhand_kind": "fist" if fist > 0.3 else ("open" if name > 0.3 else "fist"),
              "head": 4 - 4 * name - 3 * fist + math.sin(t * 0.5), "jaw": jaw(an, "GAZHDAHAM", t, 8), "lean": 2 * name + 4 * fist}
        letter_room(an, c, t, PW, PZ, 1.0 + 0.06 * ease(lt_ / max(d_, 0.1)))

    def two_a():
        name = sstep(L[3][0] + 0.2, L[3][0] + 0.8, lt) * (1 - sstep(L[3][0] + 2.2, L[3][0] + 2.8, lt))
        dictate(lt - c2, c3 - c2 + 0.4, 0.0, name)

    def ride():
        curtain_story(an, c, t, lt - c3, c4 - c3 + 0.4, ride_shadows(an, t, lt, L))

    def two_b():
        fist = sstep(L[5][0] + 0.2, L[5][0] + 0.7, lt) * (1 - sstep(L[5][1], L[5][1] + 0.5, lt))
        dictate(lt - c4, dur - c4, fist, 0.0)

    cuts(c, lt, [(0.0, pen), (c1, story), (c2, two_a), (c3, ride), (c4, two_b)], 0.4)


# ================================================================== S08 + END the messenger; a secret way
def p19_s08(an, c, t):
    """'At midnight, a rider took the letter and galloped into the dark.' -- at the window, Gordafarid: 'And us, Father?
    What will we do?' -- 'We cannot stay here. Tonight, we leave the fortress.' -- 'Leave? But the Turks are all around
    us!' (she points at the fires) -- 'There is a secret way... under the fortress.' (he lowers the lamp to the floor)"""
    lt = t - an.start["S08"]
    dur = an.end["END"] - an.start["S08"]
    L = [LN("p19", "S08", k) for k in range(5)]
    cut = L[1][0] - 0.35

    def out():
        messenger_out(an, c, t, lt, cut + 0.4, "wf198")

    def room():
        lt2 = lt - cut
        ask = sstep(L[1][0] + 0.2, L[1][0] + 0.8, lt) * (1 - sstep(L[1][1], L[1][1] + 0.5, lt))
        point = sstep(L[3][0] + 0.6, L[3][0] + 1.1, lt) * (1 - sstep(L[3][1] + 0.2, L[3][1] + 0.7, lt))
        firm = sstep(L[2][0] + 0.4, L[2][0] + 1.0, lt) * (1 - sstep(L[2][1], L[2][1] + 0.5, lt))
        low = sstep(L[4][0] + 0.8, L[4][0] + 2.0, lt)
        PG = {"hand": (mix(mix(40, 130, ask), 230, point), mix(mix(-262, -380, ask), -520, point)),
              "hand_kind": "open" if (ask > 0.3 or point > 0.3) else "fist", "rhand": (-20, -270),
              "head": 2 - 4 * point + 6 * low + math.sin(t * 0.8), "jaw": jaw(an, "GORDAFARID", t, 8),
              "lean": 2 * ask, "wind": 0.3}
        PZ = {"hand_kind": "lamp", "hand": (mix(110, 150, low), mix(-360, -250, low)),
              "rhand": (mix(-20, 120, firm), mix(-280, -330, firm)), "rhand_kind": "fist",
              "head": 4 + 14 * low + math.sin(t * 0.5), "jaw": jaw(an, "GAZHDAHAM", t, 8), "lean": 4 * low}
        night_room(an, c, t, lt2, dur - cut, PG, PZ, "nr198", zk=0.1, floor=low,
                   focus=(mix(540, 700, sstep(L[4][0], dur, lt)), 700))

    cuts(c, lt, [(0.0, out), (cut, room)], 0.45)


P19 = {"S01": p19_s01, "TITLE": p19_s01, "S02": p19_s02, "S03": p19_s03, "S04": p19_s04, "S05": p19_s05,
       "S06": p19_s06, "S07": p19_s07, "S08": p19_s08, "END": p19_s08}
SHIFT19 = {}

register(P19, SHIFT19)
