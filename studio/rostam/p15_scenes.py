"""Parts 15-16 (row 8 of OUTLINE.md, "The White Fortress"): every shot as a shadow-play scene.

Importing this module registers part 15's shots; p16_scenes.py imports it and registers part 16's.
New here, to reuse: looks HOJIR (the keeper of the White Fortress), GAZH (old Gazhdaham: turban, long beard, cape,
staff), GORD (Gordafarid in a dress and veil, before she puts on armour); sky_day() (dawn -> morning), fort() (the
White Fortress image, lit from the sun, with gate doors that open), fortress_far() (the fortress on its hill by day,
road up to the gate), wall_top() (on the battlements at sunrise: the plain far below, the host coming in its dust,
the pale parapet in front of the people), gate_court() (inside the gate: the doors open on the bright plain),
plain_below() (the plain under the fortress, the duel field: bright dust so a fallen man reads, the fortress small
on its hill, the Turanian host far off), rider() (a person on a horse in one call). puppets.py got the props
"lance" (a spear that turns about the hand, anchors tip/butt) and "dagger".
Line timings come from pNN/audio/timeline.json (LN), so the action follows the voices.
"""
import math, random
import skia
import anim
from anim import C, mix, mixc, clamp, ease, sstep, Cam, Pen, rope, spath, ppath, paint, fillp, W, H
from puppets import person, horse, LOOKS
import sets as S
from ep01_scenes import loc, jaw, get, vig, tag, A, ground, INK, Scroller, reed_list, tufts_list
from p05_scenes import register
from p07_scenes import LN, dissolve, DAWN, DAY
from p09_scenes import SUNSET
from p11_scenes import COLT, army_band, draw_band, camp
from p13_scenes import HOOMAN, BARMAN, cuts, camp_far_host

HOJIR = dict(LOOKS["warrior_ir"])                                                   # cone helmet, short beard, armour
GAZH = dict(LOOKS["noble"], beard="long", cape=True, b=0.97)                        # old Gazhdaham (with a staff)
GORD = dict(LOOKS["gordafarid"], head="veil", plume=False, garment="dress")          # Gordafarid before her armour
MORN = (255, 212, 160)                                                              # morning sun rim
STONE = (236, 228, 210)                                                             # the white walls in the sun


# ------------------------------------------------------------------ sky and fortress
def sky_day(c, mood, y1=900):
    """mood 0 = dawn (rose and gold), 1 = clear morning."""
    top = mixc((38, 42, 96), (70, 104, 164), mood)
    mid = mixc((170, 112, 146), (150, 172, 204), mood)
    low = mixc((252, 182, 136), (238, 222, 194), mood)
    S.lin(c, 0, y1, [(0, top), (0.5, mid), (0.85, low), (1, low)])


def sun_day(an, c, t, key, mood, x=None, y=None):
    sx = mix(170, 250, mood) if x is None else x
    sy = mix(800, 520, mood) if y is None else y
    S.sun(c, sx, sy, mix(72, 56, mood), (255, 246, 222), mixc((255, 160, 110), (255, 214, 150), mood), 560, 150)
    get(an, key + "cl", lambda: S.Clouds([(320, 12), (400, 9), (490, 14)], 175, 300, 600)).draw(
        c, t, mixc((150, 84, 118), (176, 176, 200), mood), 150)


def fort_img(lit=1.0):
    """The White Fortress (800 x 560 inside a 900 x 660 image, offset 50): sunlit stone, shaded low and to the right,
    with a soft dark halo so the pale walls read against a pale sky."""
    img, _ = S.city(800, 560, 540, 174, STONE, False, None)
    surf = skia.Surface(900, 660)
    c = surf.getCanvas()
    c.clear(C(0, 0, 0, 0))
    halo = skia.Paint()
    halo.setImageFilter(skia.ImageFilters.Blur(7, 7, skia.TileMode.kDecal, None))
    halo.setColorFilter(skia.ColorFilters.Blend(C(70, 64, 96, 150), skia.BlendMode.kSrcIn))
    c.drawImage(img, 50, 50, skia.SamplingOptions(), halo)
    c.saveLayer(skia.Rect.MakeLTRB(40, 40, 860, 620), None)
    c.drawImage(img, 50, 50)
    p = skia.Paint(AntiAlias=True)
    p.setShader(skia.GradientShader.MakeLinear([skia.Point(0, 200), skia.Point(0, 610)],
                                               [C(255, 236, 200, 0), C(110, 100, 128, int(140 * lit))]))
    p.setBlendMode(skia.BlendMode.kSrcATop)
    c.drawRect(skia.Rect.MakeLTRB(40, 40, 860, 620), p)
    p2 = skia.Paint(AntiAlias=True)
    p2.setShader(skia.GradientShader.MakeLinear([skia.Point(50, 0), skia.Point(850, 0)],
                                                [C(255, 220, 170, int(60 * lit)), C(90, 84, 120, int(100 * lit))]))
    p2.setBlendMode(skia.BlendMode.kSrcATop)
    c.drawRect(skia.Rect.MakeLTRB(40, 40, 860, 620), p2)
    c.restore()
    return surf.makeImageSnapshot()


def fort(an, c, t, x, y, s, gate=0.0, key="ft", lit=1.0):
    """The White Fortress at (x, y) (top left of its 800 x 560 frame), scale s; wall foot at y + 540 s, gate at
    x + 400 s. gate 0 = doors shut, 1 = wide open (the lit plain shows through)."""
    img = get(an, ("fortimg", lit), lambda: fort_img(lit))
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    c.drawImage(img, -50, -50, skia.SamplingOptions(skia.FilterMode.kLinear))
    gx, gb = 400, 540
    arch = spath([(gx - 50, gb, 0), (gx - 50, gb - 96), (gx, gb - 138, 0), (gx + 50, gb - 96), (gx + 50, gb, 0)])
    c.drawPath(arch, paint(C(252, 224, 172)))
    if gate < 0.999:
        c.save()
        c.clipPath(arch, skia.ClipOp.kIntersect, True)
        w = 50 * (1 - ease(gate))
        wood = paint(C(66, 42, 34))
        c.drawRect(skia.Rect.MakeLTRB(gx - 50, gb - 140, gx - 50 + w, gb), wood)
        c.drawRect(skia.Rect.MakeLTRB(gx + 50 - w, gb - 140, gx + 50, gb), wood)
        stud = paint(C(150, 120, 96))
        for k in range(4):
            for j in range(3):
                if w > 14:
                    c.drawCircle(gx - 50 + w * (0.25 + 0.25 * j), gb - 24 - k * 28, 3, stud)
                    c.drawCircle(gx + 50 - w * (0.25 + 0.25 * j), gb - 24 - k * 28, 3, stud)
        c.restore()
    edge = skia.Paint(AntiAlias=True, Color=C(150, 140, 150))
    edge.setStyle(skia.Paint.kStroke_Style)
    edge.setStrokeWidth(8)
    c.drawPath(arch, edge)
    c.restore()


def fortress_far(an, c, t, cam, key, mood=1.0, gate=0.0, fx=330, fy=430, fs=0.6, near=None):
    """The White Fortress on its hill by day, seen from the plain; a road winds up to the gate.
    near(cam) draws in front of the hill and behind the ground (people on the road)."""
    sky_day(c, mood)
    with cam(0.12):
        sun_day(an, c, t, key, mood)
    rg = get(an, key + "rg", lambda: (S.make_ridge(-600, 1700, 730, 60, 176, 8, 4, 0.4), S.make_ridge(-600, 1700, 790, 24, 177)))
    with cam(0.25):
        S.ridge(c, rg[0], mixc((130, 92, 124), (128, 136, 164), mood))
        S.lin(c, 680, 800, [(0, (*mixc((250, 190, 150), (232, 222, 200), mood), 0)),
                            (1, (*mixc((250, 190, 150), (232, 222, 200), mood), 150))], (-600, 680, 1700, 800))
    with cam(0.35):
        S.ridge(c, rg[1], mixc((104, 74, 96), (110, 112, 130), mood))
    gate_x, foot = fx + 400 * fs, fy + 540 * fs
    with cam(0.5):
        hill_col = mixc((86, 58, 66), (112, 98, 92), mood)
        hill = spath([(-300, 1500, 0), (-300, 1000), (gate_x - 560, 930), (gate_x - 330, foot + 30), (gate_x - 240, foot - 4),
                      (gate_x + 240, foot - 4), (gate_x + 330, foot + 30), (gate_x + 560, 930), (1400, 1000), (1400, 1500, 0)])
        p = skia.Paint(AntiAlias=True)
        p.setShader(skia.GradientShader.MakeLinear([skia.Point(0, foot), skia.Point(0, 1100)],
                                                   [C(*mixc(hill_col, (255, 220, 180), 0.25)), C(*mixc(hill_col, (20, 14, 20), 0.6))]))
        c.drawPath(hill, p)
        fort(an, c, t, fx, fy, fs, gate, key + "f")
        road = spath([(gate_x - 30 * fs, foot, 0), (gate_x + 30 * fs, foot, 0), (gate_x + 70, foot + 70), (gate_x + 40, foot + 150),
                      (gate_x + 140, 1500, 0), (gate_x - 60, 1500, 0), (gate_x - 30, foot + 150), (gate_x + 10, foot + 70)])
        c.drawPath(road, paint(C(*mixc((170, 126, 112), (198, 176, 146), mood))))
        if near:
            near(cam)
    with cam(1.0):
        ground(c, 1010, mixc((60, 40, 46), (80, 66, 58), mood), (14, 10, 12), -14)


# ------------------------------------------------------------------ the battlements
def parapet(c, top, x0=-300, x1=1400, merlon=88, gap=58, col=STONE, mood=0.0):
    """The pale parapet in front of the people on the wall walk: merlons from top - 82 to top, wall below."""
    lit = mixc(mixc(col, (110, 100, 120), 0.45), (255, 214, 170), 0.12 * (1 - mood))
    dark = mixc(col, (40, 32, 44), 0.8)
    p = skia.Paint(AntiAlias=True)
    p.setShader(skia.GradientShader.MakeLinear([skia.Point(0, top - 82), skia.Point(0, top + 520)],
                                               [C(*lit), C(*mixc(lit, dark, 0.5)), C(*dark)], [0.0, 0.35, 1.0]))
    path = skia.Path()
    path.addRect(skia.Rect.MakeLTRB(x0, top, x1, 2400))
    x = x0
    while x < x1:
        path.addRect(skia.Rect.MakeLTRB(x, top - 82, x + merlon, top + 1))
        x += merlon + gap
    c.drawPath(path, p)
    c.drawRect(skia.Rect.MakeLTRB(x0, top + 4, x1, top + 12), paint(C(*dark, 120)))
    rimc = paint(C(*mixc((255, 226, 186), col, 0.4), 230))
    x = x0
    while x < x1:
        c.drawRect(skia.Rect.MakeLTRB(x + merlon - 10, top - 82, x + merlon, top), paint(C(*dark, 90)))
        c.drawRect(skia.Rect.MakeLTRB(x, top - 84, x + merlon, top - 78), rimc)
        x += merlon + gap
    c.drawRect(skia.Rect.MakeLTRB(x0, top - 2, x1, top + 3), rimc)


def wall_top(an, c, t, cam, key, figs, mood=0.0, host_x=-200.0, host_a=0.0, rim=DAWN, par=1040, box=(0, 100, 1080, 1400),
             horizon=720):
    """On the wall of the White Fortress: sky, the plain far below with the host (army band at host_x, alpha host_a)
    raising dust, the people (figs(cc), drawn with Cam(cc, ...)), and the parapet (top at par) in front of them."""
    sky_day(c, mood, horizon + 40)
    with cam(0.1):
        sun_day(an, c, t, key, mood, mix(860, 820, mood), mix(horizon + 50, 520, mood))
    rg = get(an, key + "rg", lambda: (S.make_ridge(-600, 1700, horizon - 40, 40, 191, 8, 4, 0.4),
                                      S.make_ridge(-600, 1700, horizon, 14, 192)))
    with cam(0.2):
        S.ridge(c, rg[0], mixc((150, 104, 132), (140, 146, 170), mood))
        S.ridge(c, rg[1], mixc((176, 120, 128), (170, 164, 168), mood))
    with cam(0.3):
        S.lin(c, horizon + 6, par + 200, [(0, mixc((236, 170, 128), (220, 200, 168), mood)),
                                          (1, mixc((120, 76, 70), (150, 124, 100), mood))], (-600, horizon + 6, 1700, par + 200))
        if host_a > 0.01:
            band = get(an, key + "band", lambda: army_band(False, 46, 2400, 300))
            c.save()
            c.translate(host_x, horizon + 16)
            c.scale(0.22, 0.22)
            draw_band(c, band, 0, 0, mixc((90, 50, 60), (80, 70, 80), mood), host_a)
            c.restore()
            for k in range(6):
                S.dust(c, host_x + 60 + k * 90 + 20 * math.sin(t * 0.4 + k), horizon + 70, 70, t,
                       mixc((250, 200, 160), (240, 220, 190), mood), 120 * host_a, k)
    an.figures(c, figs, rim, box)
    with cam(1.0):
        parapet(c, par, mood=mood)


# ------------------------------------------------------------------ inside the gate
def gate_court(an, c, t, cam, key, gate=0.0, gx=540):
    """The courtyard inside the fortress, facing the gate: shaded inner wall with a walkway, the gate arch whose
    doors open on the bright plain (gate 0..1), stairs at the left."""
    S.lin(c, 0, 640, [(0, (84, 116, 172)), (1, (190, 200, 214))])
    with cam(0.6):
        wall = (150, 140, 150)
        pw = skia.Paint(AntiAlias=True)
        pw.setShader(skia.GradientShader.MakeLinear([skia.Point(0, 360), skia.Point(0, 900)],
                                                    [C(*mixc(wall, (255, 230, 200), 0.3)), C(*mixc(wall, (40, 30, 40), 0.5))]))
        path = skia.Path()
        path.addRect(skia.Rect.MakeLTRB(-400, 400, 1500, 900))
        for k in range(-6, 30):
            path.addRect(skia.Rect.MakeLTRB(k * 70, 360, k * 70 + 42, 401))
        c.drawPath(path, pw)
        arch = S.arch_path(gx, 880, 320, 460)
        p = skia.Paint(AntiAlias=True)
        p.setShader(skia.GradientShader.MakeLinear([skia.Point(0, 420), skia.Point(0, 880)],
                                                   [C(150, 172, 206), C(238, 220, 186), C(226, 180, 124)], [0.0, 0.62, 1.0]))
        c.drawPath(arch, p)
        if gate < 0.999:
            c.save()
            c.clipPath(arch, skia.ClipOp.kIntersect, True)
            w = 160 * (1 - ease(gate))
            wood = paint(C(132, 96, 70))
            c.drawRect(skia.Rect.MakeLTRB(gx - 160, 400, gx - 160 + w, 880), wood)
            c.drawRect(skia.Rect.MakeLTRB(gx + 160 - w, 400, gx + 160, 880), wood)
            stud = paint(C(200, 170, 130))
            plank = paint(C(86, 58, 42))
            for k in range(1, 4):
                c.drawRect(skia.Rect.MakeLTRB(gx - 160, 880 - k * 120, gx - 160 + w, 874 - k * 120), plank)
                c.drawRect(skia.Rect.MakeLTRB(gx + 160 - w, 880 - k * 120, gx + 160, 874 - k * 120), plank)
                for j in range(4):
                    if w > 30:
                        c.drawCircle(gx - 160 + w * (0.15 + 0.23 * j), 880 - k * 120 + 20, 4, stud)
                        c.drawCircle(gx + 160 - w * (0.15 + 0.23 * j), 880 - k * 120 + 20, 4, stud)
            c.restore()
        edge = skia.Paint(AntiAlias=True, Color=C(70, 60, 70))
        edge.setStyle(skia.Paint.kStroke_Style)
        edge.setStrokeWidth(18)
        c.drawPath(arch, edge)
        st = paint(C(*mixc(wall, (30, 22, 30), 0.45)))
        for k in range(9):
            c.drawRect(skia.Rect.MakeLTRB(-120 + k * 34, 880 - (k + 1) * 52, 260, 880 - k * 52), st)
    with cam(1.0):
        ground(c, 872, (176, 156, 134), (44, 34, 32))
        S.glow(c, gx, 870, 380, (255, 220, 160), 70 * ease(gate))


# ------------------------------------------------------------------ the plain below
def plain_below(an, c, t, cam, key, mood=1.0, host=1.0, fort_on=True, fx=-40, host_x=640, gy=872):
    """The plain under the White Fortress (the duel field): morning sky, the fortress small on its hill at the left,
    the Turanian host far off at the right, a bright dusty ground so a fallen man reads."""
    sky_day(c, mood)
    with cam(0.12):
        sun_day(an, c, t, key, mood, 900, mix(760, 470, mood))
    rg = get(an, key + "rg", lambda: (S.make_ridge(-600, 1700, 760, 50, 193, 8, 4, 0.4), S.make_ridge(-600, 1700, 812, 18, 194)))
    with cam(0.25):
        S.ridge(c, rg[0], mixc((140, 100, 124), (134, 140, 164), mood))
    with cam(0.4):
        if fort_on:
            c.drawPath(spath([(fx - 200, 900, 0), (fx - 120, 820), (fx + 40, 772), (fx + 120, 764), (fx + 300, 770),
                              (fx + 420, 800), (fx + 560, 860), (fx + 700, 900, 0)]), paint(C(*mixc((116, 84, 90), (130, 116, 110), mood))))
            fort(an, c, t, fx, 610, 0.3, 0.0, key + "f")
        S.lin(c, 740, 830, [(0, (*mixc((250, 200, 160), (236, 224, 200), mood), 0)),
                            (1, (*mixc((250, 200, 160), (236, 224, 200), mood), 130))], (-600, 740, 1700, 830))
        if host > 0.01:
            band = get(an, key + "band", lambda: army_band(False, 47, 1500, 300))
            c.save()
            c.translate(host_x, 734)
            c.scale(0.3, 0.3)
            draw_band(c, band, 0, 0, mixc((110, 70, 80), (104, 92, 100), mood), host)
            c.restore()
    with cam(0.55):
        S.ridge(c, rg[1], mixc((176, 120, 110), (176, 150, 124), mood))
    with cam(0.85):
        ground(c, gy, mixc((232, 172, 116), (226, 190, 136), mood), (92, 62, 44))
        S.tufts(c, get(an, key + "tf", lambda: tufts_list(195, 30, -300, 1400, gy + 26, 8, 20)), t, (70, 46, 34), 0.2)


# ------------------------------------------------------------------ people
def rider(cc, x, y, s, face, look, t, rp, gait="stand", phase=0.0, **hp):
    """A person (look, pose rp) on a saddled horse (gait, phase; extra horse params in hp)."""
    P = {"gait": gait, "phase": phase, "saddle": True, "rider": look, "rider_pose": rp}
    P.update(hp)
    horse(cc, x, y, s, face, P, t)


def lance_pose(level, extra=None, back=False):
    """Rider pose holding a lance: level 0 = upright, 1 = couched (pointing forward); back=True holds it reversed."""
    ang = mix(0, 84, level) if not back else mix(0, -96, level)
    P = {"hand_kind": "lance", "lance": ang, "hand": (mix(100, 112, level), mix(-330, -346, level))}
    if extra:
        P.update(extra)
    return P


# ================================================================== part 15 shots
FGY = 1000                                       # ground line of the close face-off (hooves under the subtitles)


def faceoff(an, c, t, PH, PS, zoom, focus=(540, 700), key="fo", hx=250, sx=840, hs=0.74, ss=0.78, extra=None):
    """Hojir (left, facing right) and Sohrab on his colt (right, facing left) face each other on the plain; the
    fortress small on its hill behind Hojir, the Turanian host behind Sohrab. PH / PS are the horses' P dicts."""
    cam = Cam(c, focus, zoom)
    plain_below(an, c, t, cam, key, 0.9, 1.0, True, -60, 650, FGY)

    def fh(cc):
        with Cam(cc, focus, zoom)(1.0):
            horse(cc, hx, FGY, hs, 1, PH, t)
    an.figures(c, fh, MORN, (0, 120, 1080, 1300))

    def fs(cc):
        with Cam(cc, focus, zoom)(1.0):
            horse(cc, sx, FGY, ss, -1, PS, t)
    an.figures(c, fs, COLT, (0, 120, 1080, 1300), alpha=200)
    if extra:
        extra(cam)
    vig(an, c, 150)


def hojir_horse(rp, t, rear=0.0):
    P = {"gait": "rear", "rear": rear} if rear > 1 else {"gait": "stand", "neck": 6 * math.sin(t * 1.6), "head": 3 * math.sin(t * 1.1)}
    P.update({"saddle": True, "rider": HOJIR, "rider_pose": rp, "wind": 0.6})
    return P


def sohrab_colt(rp, t, rear=0.0):
    P = {"gait": "rear", "rear": rear} if rear > 1 else {"gait": "stand", "neck": 5 * math.sin(t * 1.9 + 1), "head": 4 * math.sin(t * 1.3)}
    P.update({"saddle": True, "rider": "sohrab", "rider_scale": 0.92, "rider_pose": rp, "wind": 0.8})
    return P


def p15_s01(an, c, t):
    """Hook + title: on the plain, face to face. Sohrab: 'Who are you, to ride out alone against my army?' --
    Hojir: 'I am Hojir... and I will send your head to King Kavus!'"""
    lt = t - an.start["S01"]
    dur = an.end["TITLE"] - an.start["S01"]
    a0, a1 = LN("p15", "S01", 0)
    b0, b1 = LN("p15", "S01", 1)
    ask = sstep(a0 + 0.2, a0 + 0.8, lt) * (1 - sstep(a1 + 0.2, a1 + 0.8, lt))
    shake = sstep(b0 + 1.4, b0 + 1.9, lt)
    rpS = M_lance(0.0, {"rhand": (mix(-20, 150, ask), mix(-300, -430, ask)), "rhand_kind": "open",
                        "head": 2 - 3 * ask + math.sin(t * 0.8), "jaw": jaw(an, "SOHRAB", t, 8), "wind": 0.8})
    rpH = M_lance(0.25 * shake, {"head": -2 - 4 * shake + math.sin(t * 0.7), "jaw": jaw(an, "HOJIR", t, 9), "lean": -3 * shake,
                                 "wind": 0.6})
    if shake > 0:
        rpH["hand"] = (mix(100, 90, shake), mix(-330, -420, shake) + 6 * math.sin(t * 9) * shake)
    faceoff(an, c, t, hojir_horse(rpH, t), sohrab_colt(rpS, t), 1.04 + 0.08 * ease(lt / dur), key="fo151")


def M_lance(level, extra):
    return lance_pose(level, extra)


# ------------------------------------------------------------------ S02 the White Fortress at dawn
def p15_s02(an, c, t):
    """'On the border of Iran stood the White Fortress... the hope of the Iranians.' Push in at dawn. Then on the wall:
    Hojir, its keeper, walks the battlements; old Gazhdaham and his daughter Gordafarid at the parapet."""
    lt, dur = loc(an, "S02", t)
    L = [LN("p15", "S02", k) for k in range(5)]
    c1 = L[3][0] - 0.5
    c2 = L[4][0] - 0.4

    def wide():
        focus = (570, 760)
        zoom = 1.0 + 0.16 * ease(lt / (c1 + 0.6))
        cam = Cam(c, focus, zoom)
        fortress_far(an, c, t, cam, "ff152", mood=mix(0.0, 0.25, lt / (c1 + 0.6)), gate=0.0)
        get(an, "bd152", lambda: None)
        with cam(0.45):
            S.birds(c, t, get(an, "bdl152", lambda: [(random.Random(k).uniform(0, 1300), random.Random(k + 9).uniform(420, 560),
                                                          -30, random.Random(k + 3).uniform(5, 8), k) for k in range(6)]), (40, 26, 50))
        vig(an, c, 140)

    def keeper():
        lt2 = lt - c1
        focus = (540, 700)
        zoom = 1.0 + 0.05 * ease(lt2 / (c2 - c1 + 0.6))
        cam = Cam(c, focus, zoom)
        walk = clamp(lt2 / 3.4)
        hx = mix(-120, 400, ease(walk))
        look = sstep(3.0, 4.0, lt2)

        def figs(cc):
            with Cam(cc, focus, zoom)(1.0):
                person(cc, hx, 1330, 1.5, 1, {"mode": "walk" if walk < 1 else "stand", "phase": lt2 * 3.4, "stride": 16,
                                              "hand_kind": "spear", "hand": (100, -330), "head": -4 * look + math.sin(t * 0.6),
                                              "wind": 0.5, "rhand": (-20, -262)}, t, HOJIR)
        wall_top(an, c, t, cam, "wt152", figs, mood=0.18, host_a=0.0)
        vig(an, c, 150)

    def family():
        lt3 = lt - c2
        focus = (540, 700)
        zoom = 1.0 + 0.05 * ease(lt3 / (dur - c2))
        cam = Cam(c, focus, zoom)
        turn = sstep(1.8, 2.6, lt3)

        def figs(cc):
            with Cam(cc, focus, zoom)(1.0):
                person(cc, 300, 1330, 1.42, 1, {"hand_kind": "staff", "hand": (70, -300), "head": 6 + math.sin(t * 0.5),
                                                "lean": 3, "wind": 0.5, "rhand": (-24, -262)}, t, GAZH)
                person(cc, 790, 1330, 1.36, 1 if turn < 0.5 else -1, {"hand": (40, -262), "rhand": (-26, -262),
                                                                      "head": 2 + math.sin(t * 0.7), "wind": 0.7}, t, GORD)
        wall_top(an, c, t, cam, "wt152", figs, mood=0.22, host_a=0.0)
        vig(an, c, 150)

    dissolve(c, lt, c1, 0.6, wide, lambda: dissolve(c, lt, c2, 0.5, keeper, family))


# ------------------------------------------------------------------ S03 dust on the road
def host_view(an, c, t, lt, key, mood=0.3, zoom=1.0):
    """What they see from the wall: the host coming over the plain in its dust, Sohrab on his colt in front."""
    focus = (560, 720)
    cam = Cam(c, focus, zoom)
    sky_day(c, mood)
    with cam(0.12):
        sun_day(an, c, t, key, mood, 880, mix(800, 600, mood))
    rg = get(an, key + "rg", lambda: (S.make_ridge(-600, 1700, 640, 40, 196, 8, 4, 0.4), S.make_ridge(-600, 1700, 680, 16, 197)))
    with cam(0.25):
        S.ridge(c, rg[0], mixc((150, 104, 132), (140, 146, 170), mood))
        S.ridge(c, rg[1], mixc((176, 120, 128), (170, 164, 168), mood))
    with cam(0.5):
        S.lin(c, 686, 1100, [(0, mixc((236, 170, 128), (220, 200, 168), mood)), (1, mixc((150, 96, 80), (160, 130, 104), mood))],
              (-600, 686, 1700, 1100))
        band = get(an, key + "band", lambda: army_band(False, 48, 2400, 300))
        bx = 700 - 18 * lt
        c.save()
        c.translate(bx, 600)
        c.scale(0.5, 0.5)
        draw_band(c, band, 0, 0, mixc((96, 54, 64), (84, 70, 84), mood), 1.0)
        c.restore()
        for k in range(7):
            S.dust(c, bx + 40 + k * 150 + 20 * math.sin(t * 0.5 + k), 760, 90, t, mixc((250, 200, 160), (240, 220, 190), mood), 110, k)
    sx = 560 - 14 * lt

    def figs(cc):
        with Cam(cc, focus, zoom)(0.5):
            rider(cc, sx, 772, 0.34, -1, "sohrab", t, lance_pose(0.0, {"head": 2, "wind": 0.8}), "walk", t * 0.9,
                  rider_scale=0.92, wind=0.8)
    an.figures(c, figs, COLT, (0, 300, 1080, 1100), alpha=200)
    with cam(0.5):
        S.dust(c, sx + 80, 772, 50, t, (250, 214, 170), 90, 3)
    vig(an, c, 150)


def p15_s03(an, c, t):
    """On the wall at sunrise. Hojir: 'Gazhdaham, look! Dust, all along the road.' -- 'Those are banners... of Turan.'
    The host in its dust, a young giant riding in front; 'tall as a cypress, and so young!' -- 'Close the gate!'"""
    lt, dur = loc(an, "S03", t)
    L = [LN("p15", "S03", k) for k in range(5)]
    c1 = L[2][0] + 0.6
    c2 = L[4][0] - 0.4
    hx0 = 700

    def wall(lt_, zoom0, gaz_turn):
        focus = (560, 700)
        zoom = zoom0
        cam = Cam(c, focus, zoom)
        point = sstep(L[0][0] + 0.2, L[0][0] + 0.8, lt_) * (1 - sstep(L[1][0] + 0.6, L[1][0] + 1.4, lt_))
        look = sstep(L[1][0] - 0.2, L[1][0] + 0.6, lt_)
        order = sstep(L[4][0] - 0.1, L[4][0] + 0.5, lt_)
        PHj = {"jaw": jaw(an, "HOJIR", t, 9), "hand": (mix(40, 150, point), mix(-262, -560, point)),
               "hand_kind": "open" if point > 0.3 else "fist", "rprop": "spear", "rhand": (-14, -300),
               "head": -5 * point - 3 * look + math.sin(t * 0.6), "lean": 3 * point, "wind": 0.6}
        gface = -1 if (lt_ < L[1][0] - 0.3 or order > 0.5) else 1
        PG = {"jaw": jaw(an, "GAZHDAHAM", t, 7), "hand_kind": "staff" if order < 0.5 else "open",
              "hand": (70, -300) if order < 0.5 else (mix(70, 150, order), mix(-300, -470, order)),
              "rprop": "staff" if order > 0.5 else None, "rhand": (-24, -280),
              "head": (3 if gface < 0 else -3) + math.sin(t * 0.5), "lean": 2, "wind": 0.6}

        def figs(cc):
            with Cam(cc, focus, zoom)(1.0):
                person(cc, 260, 1330, 1.5, 1, PHj, t, HOJIR)
                person(cc, 790, 1330, 1.4, gface, PG, t, GAZH)
        wall_top(an, c, t, cam, "wt153", figs, mood=0.3, host_x=hx0 - 14 * lt_, host_a=1.0)
        vig(an, c, 150)

    def a():
        wall(lt, 1.0 + 0.04 * ease(lt / c1), 0)

    def b():
        host_view(an, c, t, lt - c1 + 4.0, "hv153", 0.32, 1.0 + 0.1 * ease((lt - c1) / (c2 - c1)))

    def d():
        wall(lt, 1.06, 1)

    dissolve(c, lt, c1, 0.6, a, lambda: dissolve(c, lt, c2, 0.5, b, d))


# ------------------------------------------------------------------ S04 the host below the fortress
def p15_s04(an, c, t):
    """'It was Sohrab, the young son of Rostam... marching on Iran to find his father.' The host halts below the
    fortress. Sohrab: 'So this is the White Fortress.' Hooman: 'The gate of Iran...' -- 'Tomorrow, the throne of Kavus!'"""
    lt, dur = loc(an, "S04", t)
    L = [LN("p15", "S04", k) for k in range(5)]
    cut = L[2][0] - 0.5

    def wide():
        focus = (640, 720)
        zoom = 1.0 + 0.1 * ease(lt / (cut + 0.6))
        cam = Cam(c, focus, zoom)
        sky_day(c, 0.55)
        with cam(0.12):
            sun_day(an, c, t, "pl154", 0.55, 880, 640)
        rg = get(an, "pl154rg", lambda: (S.make_ridge(-600, 1700, 760, 50, 198, 8, 4, 0.4), S.make_ridge(-600, 1700, 812, 18, 199)))
        with cam(0.25):
            S.ridge(c, rg[0], (136, 124, 150))
        with cam(0.4):
            c.drawPath(spath([(-400, 900, 0), (-300, 780), (-120, 700), (60, 690), (240, 720), (360, 800), (460, 900, 0)]),
                       paint(C(118, 100, 100)))
            fort(an, c, t, -230, 430, 0.5, 0.0, "pl154f")
            S.lin(c, 740, 830, [(0, (240, 216, 190, 0)), (1, (240, 216, 190, 120))], (-600, 740, 1700, 830))
        band = get(an, "pl154band", lambda: army_band(False, 49, 1800, 300))
        bx = 760 - 40 * min(lt, 5.0)
        with cam(0.6):
            S.ridge(c, rg[1], (180, 150, 124))
            draw_band(c, band, bx, 600, (92, 70, 80), 1.0)
            for k in range(6):
                S.dust(c, bx + 60 + k * 180, 880, 80, t, (240, 214, 176), 100, k)
        with cam(0.85):
            ground(c, 900, (222, 186, 134), (92, 62, 44))
        halt = sstep(4.2, 5.6, lt)
        sx = 760 - 70 * min(lt, 5.0) + 10 * halt

        def figs(cc):
            with Cam(cc, focus, zoom)(1.0):
                rider(cc, sx + 260, 896, 0.42, -1, HOOMAN, t, {"hand_kind": "mace", "hand": (100, -300), "head": 2}, "walk" if halt < 1 else "stand",
                      t * 0.9 + 0.4)
                rider(cc, sx + 470, 890, 0.4, -1, BARMAN, t, {"hand_kind": "spear", "hand": (100, -330), "head": 2}, "walk" if halt < 1 else "stand",
                      t * 0.9 + 0.8)
        an.figures(c, figs, DAY, (0, 200, 1080, 1100))

        def fs(cc):
            with Cam(cc, focus, zoom)(1.0):
                rider(cc, sx, 904, 0.5, -1, "sohrab", t, lance_pose(0.0, {"head": 2 - 3 * halt, "wind": 0.8}),
                      "walk" if halt < 1 else "stand", t * 0.9, rider_scale=0.92, wind=0.8, neck=4 * math.sin(t * 1.7) * halt)
        an.figures(c, fs, COLT, (0, 200, 1080, 1100), alpha=200)
        vig(an, c, 140)

    def two():
        lt2 = lt - cut
        focus = (520, 700)
        zoom = 1.02 + 0.06 * ease(lt2 / (dur - cut))
        cam = Cam(c, focus, zoom)
        fortress_far(an, c, t, cam, "ff154", mood=0.6, gate=0.0, fx=60, fy=420, fs=0.55)
        look = sstep(L[2][0] - 0.3, L[2][0] + 0.4, lt)
        up = sstep(L[4][0] + 0.2, L[4][0] + 0.8, lt)
        lean_h = sstep(L[3][0], L[3][0] + 0.5, lt) * (1 - sstep(L[3][1], L[3][1] + 0.6, lt))
        rpS = lance_pose(0.0, {"head": -3 * look - 5 * up + math.sin(t * 0.8), "jaw": jaw(an, "SOHRAB", t, 8), "wind": 0.8})
        if up > 0:
            rpS["hand"] = (mix(100, 70, up), mix(-330, -500, up))
        rpH = {"hand_kind": "open", "hand": (mix(60, 150, lean_h), mix(-300, -380, lean_h)), "rprop": "mace", "rhand": (-24, -300),
               "jaw": jaw(an, "HOOMAN", t, 8), "head": 3 + math.sin(t * 0.7), "lean": 5 * lean_h, "wind": 0.6}

        def fh(cc):
            with Cam(cc, focus, zoom)(1.0):
                rider(cc, 880, FGY, 0.62, -1, HOOMAN, t, rpH, neck=5 * math.sin(t * 1.4), head=3 * math.sin(t * 1.2))
        an.figures(c, fh, DAY, (0, 120, 1080, 1300))
        rr = 22 * math.sin(clamp((lt - L[4][0] - 0.6) / 1.4) * math.pi) if L[4][0] + 0.6 < lt < L[4][0] + 2.0 else 0.0

        def fs(cc):
            with Cam(cc, focus, zoom)(1.0):
                horse(cc, 420, FGY, 0.76, -1, sohrab_colt(rpS, t, rr), t)
        an.figures(c, fs, COLT, (0, 120, 1080, 1300), alpha=200)
        vig(an, c, 150)

    dissolve(c, lt, cut, 0.5, wide, two)


# ------------------------------------------------------------------ S05 Hojir arms himself
def p15_s05(an, c, t):
    """Inside the gate. Hojir: 'Bring me my armour, my spear and my horse!' Gazhdaham: 'You cannot fight a whole army
    alone... this boy fights like a lion.' -- 'I have hunted lions before.' Mounted: 'Only their leader. Cut off the
    head, and the body falls. If I don't come back, keep the gate closed.' From the wall, Gordafarid: 'Go, Hojir!'"""
    lt, dur = loc(an, "S05", t)
    L = [LN("p15", "S05", k) for k in range(8)]
    c1 = L[4][0] - 0.4
    c2 = L[7][0] - 0.4

    def talk():
        focus = (540, 700)
        zoom = 1.0 + 0.05 * ease(lt / c1)
        cam = Cam(c, focus, zoom)
        gate_court(an, c, t, cam, "gc155", 0.0)
        call = sstep(L[0][0], L[0][0] + 0.5, lt) * (1 - sstep(L[0][1], L[0][1] + 0.6, lt))
        plead = sstep(L[1][0] + 0.1, L[1][0] + 0.6, lt) * (1 - sstep(L[2][1], L[2][1] + 0.6, lt))
        proud = sstep(L[3][0], L[3][0] + 0.5, lt)
        PHj = {"jaw": jaw(an, "HOJIR", t, 9), "hand": (mix(40, 120, call), mix(-262, -520, call)), "hand_kind": "fist",
               "rhand": (-20, -262), "head": -4 * call - 6 * proud + math.sin(t * 0.6), "lean": -3 * proud, "wind": 0.4}
        PG = {"jaw": jaw(an, "GAZHDAHAM", t, 7), "hand_kind": "open", "hand": (mix(40, 150, plead), mix(-262, -400, plead)),
              "rprop": "staff", "rhand": (-24, -290), "head": 4 + math.sin(t * 0.5), "lean": 4 * plead, "wind": 0.4}

        def figs(cc):
            with Cam(cc, focus, zoom)(1.0):
                person(cc, 250, 1330, 1.48, 1, PHj, t, HOJIR)
                person(cc, 800, 1330, 1.36, -1, PG, t, GAZH)
        an.figures(c, figs, MORN, (0, 100, 1080, 1500))
        vig(an, c, 160)

    def mounted():
        lt2 = lt - c1
        focus = (560, 700)
        zoom = 1.0 + 0.05 * ease(lt2 / (c2 - c1))
        cam = Cam(c, focus, zoom)
        gate = sstep(L[6][1] - 0.4, L[6][1] + 1.6, lt)
        gate_court(an, c, t, cam, "gc155", gate, gx=520)
        raise_l = sstep(L[4][0] + 0.2, L[4][0] + 0.8, lt)
        chop = sstep(L[5][0] + 0.4, L[5][0] + 0.8, lt) * (1 - sstep(L[5][1], L[5][1] + 0.6, lt))
        down = sstep(L[6][0], L[6][0] + 0.5, lt)
        rpH = lance_pose(0.0, {"jaw": jaw(an, "HOJIR", t, 9), "head": -3 * raise_l + 7 * down + math.sin(t * 0.6),
                               "rhand": (mix(-20, 140, chop), mix(-262, -380, chop)), "rhand_kind": "open", "wind": 0.5})
        rpH["hand"] = (mix(100, 80, raise_l), mix(-330, -470, raise_l))
        PG = {"hand_kind": "staff", "hand": (70, -300), "head": -8 * down + 2 + math.sin(t * 0.5), "lean": 2, "wind": 0.4,
              "rhand": (-24, -262)}

        def figs(cc):
            with Cam(cc, focus, zoom)(1.0):
                rider(cc, 700, FGY, 0.74, -1, HOJIR, t, rpH, neck=6 * math.sin(t * 1.5), head=3 * math.sin(t * 1.1))
                person(cc, 180, FGY, 1.0, 1, PG, t, GAZH)
        an.figures(c, figs, MORN, (0, 100, 1080, 1300))
        vig(an, c, 160)

    def gord():
        lt3 = lt - c2
        focus = (540, 700)
        zoom = 1.0 + 0.05 * ease(lt3 / (dur - c2))
        cam = Cam(c, focus, zoom)
        cheer = sstep(L[7][0] + 0.1, L[7][0] + 0.6, lt)
        P = {"jaw": jaw(an, "GORDAFARID", t, 7), "hand": (mix(40, 120, cheer), mix(-262, -520, cheer)), "hand_kind": "fist",
             "rhand": (-26, -262), "head": 6 - 2 * cheer + math.sin(t * 0.7), "lean": 3, "wind": 0.9}

        def figs(cc):
            with Cam(cc, focus, zoom)(1.0):
                person(cc, 560, 1380, 1.6, -1, P, t, GORD)
        wall_top(an, c, t, cam, "wt155", figs, mood=0.7, host_x=640, host_a=0.75, rim=MORN, par=1080)
        vig(an, c, 160)

    dissolve(c, lt, c1, 0.5, talk, lambda: dissolve(c, lt, c2, 0.4, mounted, gord))


# ------------------------------------------------------------------ S06 the gate opens
def p15_s06(an, c, t):
    """'The great gate opened, and Hojir rode out alone onto the plain. From the walls, and from the enemy camp,
    thousands of eyes were watching him.' Sohrab sees him; his blood boils; he spurs his colt and rides out."""
    lt, dur = loc(an, "S06", t)
    L = [LN("p15", "S06", k) for k in range(4)]
    c1 = L[1][0] - 0.3
    c2 = L[2][0] - 0.4

    def gate():
        focus = (580, 820)
        zoom = 1.0 + 0.06 * ease(lt / (c1 + 0.5))
        cam = Cam(c, focus, zoom)
        g = sstep(0.0, 1.6, lt)
        u = clamp((lt - 1.2) / 3.8)

        def near(cam_):
            def figs(cc):
                x = mix(570, 700, u)
                y = mix(842, 1004, u)
                s = mix(0.16, 0.3, u)
                rider(cc, x, y, s, 1, HOJIR, t, lance_pose(0.0, {"head": 2, "wind": 0.6}), "walk", t * 0.9)
            if lt > 1.0:
                an.figures(c, figs, MORN, (0, 500, 1080, 1200))
        fortress_far(an, c, t, cam, "ff156", mood=0.75, gate=g, fx=170, fy=300, fs=1.0, near=near)
        vig(an, c, 140)

    def eyes():
        lt2 = lt - c1
        focus = (540, 720)
        zoom = 1.0 + 0.05 * ease(lt2 / (c2 - c1 + 0.5))
        cam = Cam(c, focus, zoom)
        plain_below(an, c, t, cam, "pb156", 0.85, 1.0, True, -60, 640, 872)
        with cam(0.4):
            dots = paint(C(60, 44, 50))
            for k in range(14):
                x = -60 + 50 + k * 15
                c.drawCircle(x * 1.0 + 6, 618 + 0.3 * 130 - 6 + 2 * math.sin(t * 2 + k), 2.6, dots)
        hx = 360 + 22 * lt2

        def figs(cc):
            with Cam(cc, focus, zoom)(1.0):
                rider(cc, hx, 872, 0.34, 1, HOJIR, t, lance_pose(0.0, {"head": 2, "wind": 0.6}), "walk", t * 0.9)
        an.figures(c, figs, MORN, (0, 300, 1080, 1000))
        vig(an, c, 140)

    def sohrab():
        lt3 = lt - c2
        focus = (560, 700)
        zoom = 1.0 + 0.06 * ease(lt3 / (dur - c2))
        cam = Cam(c, focus, zoom)
        sky_day(c, 0.85)
        with cam(0.12):
            sun_day(an, c, t, "so156", 0.85, 880, 500)
        rg = get(an, "so156rg", lambda: (S.make_ridge(-600, 1700, 760, 50, 201, 8, 4, 0.4), S.make_ridge(-600, 1700, 812, 18, 202)))
        with cam(0.25):
            S.ridge(c, rg[0], (134, 140, 164))
        band = get(an, "so156band", lambda: army_band(False, 50, 1800, 300))
        with cam(0.5):
            S.ridge(c, rg[1], (176, 150, 124))
            draw_band(c, band, -300, 560, (100, 84, 96), 1.0)
            S.lin(c, 820, 880, [(0, (226, 200, 160, 0)), (1, (226, 200, 160, 200))], (-600, 820, 1700, 880))
        with cam(0.85):
            ground(c, FGY, (226, 190, 136), (92, 62, 44))
        angry = sstep(L[2][0] + 0.3, L[2][0] + 1.2, lt)
        spur = L[3][0] + 0.3
        rr = 30 * math.sin(clamp((lt - spur) / 1.2) * math.pi) if spur < lt < spur + 1.2 else 0.0
        go = clamp((lt - spur - 1.0) / 2.4)
        x = 640 - 900 * go * go
        rp = lance_pose(0.5 * go, {"head": -6 * angry + 4 * go + math.sin(t * 0.8), "lean": 6 * go, "wind": 1.0,
                                   "rhand": (mix(-20, 40, angry), mix(-262, -300, angry)), "rhand_kind": "fist"})
        if rr > 1:
            P = sohrab_colt(rp, t, rr)
        elif go > 0:
            P = {"gait": "gallop", "phase": t * 2.2, "saddle": True, "rider": "sohrab", "rider_scale": 0.92, "rider_pose": rp, "wind": 1.0}
        else:
            P = sohrab_colt(rp, t)

        def figs(cc):
            with Cam(cc, focus, zoom)(1.0):
                horse(cc, x, FGY, 0.8, -1, P, t)
        an.figures(c, figs, COLT, (0, 100, 1080, 1300), alpha=200)
        if go > 0:
            for k in range(3):
                u = (lt * 1.8 + k * 0.33) % 1.0
                S.dust(c, x + 300 + u * 200, FGY - 30 - u * 30, 40 + u * 80, t, (240, 214, 170), 110 * (1 - u) * min(1, go * 3), k)
        vig(an, c, 150)

    dissolve(c, lt, c1, 0.5, gate, lambda: dissolve(c, lt, c2, 0.5, eyes, sohrab))


# ------------------------------------------------------------------ S07 face to face
def p15_s07(an, c, t):
    """Face to face. Sohrab: 'Who are you...? Tonight, your mother will weep for you.' Hojir: 'Don't be so proud,
    boy. I am Hojir, the hero of Iran! I will cut off your head and send it to King Kavus!'"""
    lt, dur = loc(an, "S07", t)
    L = [LN("p15", "S07", k) for k in range(4)]
    ask = sstep(L[0][0] + 0.2, L[0][0] + 0.8, lt) * (1 - sstep(L[1][1], L[1][1] + 0.6, lt))
    threat = sstep(L[1][0] + 0.6, L[1][0] + 1.2, lt) * (1 - sstep(L[1][1] + 0.2, L[1][1] + 0.8, lt))
    proud = sstep(L[2][0] + 1.6, L[2][0] + 2.4, lt)
    chop = sstep(L[3][0] + 0.3, L[3][0] + 0.8, lt)
    rpS = lance_pose(0.35 * threat, {"rhand": (mix(-20, 150, ask), mix(-300, -430, ask)), "rhand_kind": "open",
                                     "head": 2 - 3 * ask + math.sin(t * 0.8), "jaw": jaw(an, "SOHRAB", t, 8), "wind": 0.8})
    rpH = lance_pose(0.3 * chop, {"head": -6 * proud + math.sin(t * 0.7), "jaw": jaw(an, "HOJIR", t, 9), "lean": -3 * proud,
                                  "wind": 0.6, "rhand": (mix(-20, 60, proud), mix(-262, -330, proud)), "rhand_kind": "fist"})
    if chop > 0:
        rpH["hand"] = (mix(100, 130, chop), mix(-330, -360, chop) + 5 * math.sin(t * 8) * chop)
    faceoff(an, c, t, hojir_horse(rpH, t), sohrab_colt(rpS, t), 1.0 + 0.08 * ease(lt / dur), key="fo157")


# ------------------------------------------------------------------ S08 + END the charge
def p15_s08(an, c, t):
    """'Sohrab only laughed.' -- 'My head? Then come and take it, Hojir!' -- 'For Iran!' Then, wide: 'And the two
    riders charged at each other' -- they gallop at each other across the plain through the end card."""
    lt = t - an.start["S08"]
    dur = an.end["END"] - an.start["S08"]
    L = [LN("p15", "S08", k) for k in range(4)]
    cut = L[3][0] - 0.3

    def close():
        laugh = sstep(L[0][0] + 0.3, L[0][0] + 0.8, lt) * (1 - sstep(L[1][0], L[1][0] + 0.5, lt))
        dare = sstep(L[1][0] + 0.2, L[1][0] + 0.8, lt)
        cry = sstep(L[2][0] - 0.1, L[2][0] + 0.3, lt)
        rr = 28 * math.sin(clamp((lt - L[2][0] + 0.1) / 1.3) * math.pi) if L[2][0] - 0.1 < lt < L[2][0] + 1.2 else 0.0
        rpS = lance_pose(0.0, {"head": -10 * laugh + 2.5 * laugh * math.sin(t * 16) + math.sin(t * 0.8), "lean": -4 * laugh,
                               "rhand": (mix(-20, 160, dare), mix(-300, -400, dare) + 14 * math.sin(t * 5) * dare),
                               "rhand_kind": "open", "jaw": jaw(an, "SOHRAB", t, 8) + 4 * laugh, "wind": 0.8})
        rpH = lance_pose(0.0, {"head": -4 * cry + math.sin(t * 0.7), "jaw": jaw(an, "HOJIR", t, 10), "wind": 0.7})
        rpH["hand"] = (mix(100, 70, cry), mix(-330, -520, cry))
        faceoff(an, c, t, hojir_horse(rpH, t, rr), sohrab_colt(rpS, t), 1.08 + 0.04 * ease(lt / cut), key="fo158")

    def wide():
        lt2 = lt - cut
        focus = (540, 720)
        zoom = 1.0 + 0.05 * ease(lt2 / (dur - cut))
        cam = Cam(c, focus, zoom)
        plain_below(an, c, t, cam, "pb158", 0.9, 1.0, True, -60, 650, 872)
        run = clamp(lt2 / 1.2)
        k = run * 0.6 + 0.4
        hx = 140 + 30 * lt2 * k
        sx = 940 - 30 * lt2 * k
        couch = sstep(0.4, 1.4, lt2)
        PH = {"gait": "gallop", "phase": t * 2.1, "saddle": True, "rider": HOJIR, "wind": 1.0,
              "rider_pose": lance_pose(couch, {"head": 2, "lean": 6 * couch, "wind": 1.0})}
        PS = {"gait": "gallop", "phase": t * 2.0 + 0.4, "saddle": True, "rider": "sohrab", "rider_scale": 0.92, "wind": 1.0,
              "rider_pose": lance_pose(0.8 * couch, {"head": 2, "lean": 5 * couch, "wind": 1.0})}

        def fh(cc):
            with Cam(cc, focus, zoom)(1.0):
                horse(cc, hx, 874, 0.44, 1, PH, t)
        an.figures(c, fh, MORN, (0, 200, 1080, 1000))

        def fs(cc):
            with Cam(cc, focus, zoom)(1.0):
                horse(cc, sx, 872, 0.46, -1, PS, t)
        an.figures(c, fs, COLT, (0, 200, 1080, 1000), alpha=200)
        for j in range(3):
            u = (lt2 * 1.8 + j * 0.33) % 1.0
            S.dust(c, hx - 120 - u * 160, 862 - u * 20, 30 + u * 60, t, (240, 214, 170), 100 * (1 - u), j)
            S.dust(c, sx + 120 + u * 160, 862 - u * 20, 30 + u * 60, t, (240, 214, 170), 100 * (1 - u), j + 5)
        vig(an, c, 140)

    dissolve(c, lt, cut, 0.4, close, wide)


P15 = {"S01": p15_s01, "TITLE": p15_s01, "S02": p15_s02, "S03": p15_s03, "S04": p15_s04, "S05": p15_s05,
       "S06": p15_s06, "S07": p15_s07, "S08": p15_s08, "END": p15_s08}
SHIFT15 = {}

register(P15, SHIFT15)
