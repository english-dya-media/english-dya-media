"""Part 16 (The Prisoner; row 8 of OUTLINE.md, second half): every shot as a shadow-play scene.

Importing this module imports p15_scenes (the sets of the White Fortress) and registers part 16's shots.
New here, to reuse: field() (the duel plain with the fortress larger on its hill at the left), pinned() (a man on
his back on the bright ground, another kneeling on his chest with a dagger, drawn in two passes so the rim of the
one on top cuts him out of the one below), pole() (a long lance drawn between two screen points, bending under a
load), flying() (a man thrown out of the saddle, turning in the air), helmet_at() (the cone helmet with its plume
held in the hands), GORD_ARM / GORD_BARE (Gordafarid in armour, bare-headed with her hair loose, then helmeted).
Line timings come from p16/audio/timeline.json (LN), so the action follows the voices.
"""
import math, random
import skia
import anim
from anim import C, mix, mixc, clamp, ease, sstep, Cam, Pen, rope, spath, ppath, paint, fillp, taper, bez, W, H
from puppets import person, horse, LOOKS
import sets as S
import p15_scenes as M
from ep01_scenes import loc, jaw, get, vig, tag, A, ground, INK, Scroller, tufts_list
from p05_scenes import register
from p07_scenes import LN, dissolve, DAY
from p11_scenes import COLT, army_band, draw_band, camp
from p13_scenes import HOOMAN, BARMAN, cuts

HOJIR, GAZH, GORD, MORN = M.HOJIR, M.GAZH, M.GORD, M.MORN
GORD_BARE = dict(LOOKS["gordafarid"], head="bare", plume=False)       # in armour, hair loose, helmet in her hands
GORD_ARM = dict(LOOKS["gordafarid"])                                    # helmeted: cone, plume, hair
GY = 872                                                                # the duel field's ground line
MOOD = 0.9                                                              # morning on the plain


# ------------------------------------------------------------------ sets
def field(an, c, t, cam, key, mood=MOOD, fx=-40, fy=560, fs=0.42, host=1.0, host_x=640, gy=GY):
    """The plain under the White Fortress: morning sky, the fortress on its hill at the left (fs = its scale, None
    for none), the Turanian host far off at the right, bright dust on the ground so a fallen man reads."""
    M.sky_day(c, mood)
    with cam(0.12):
        M.sun_day(an, c, t, key, mood, 900, mix(760, 470, mood))
    rg = get(an, key + "rg", lambda: (S.make_ridge(-600, 1700, 760, 50, 193, 8, 4, 0.4), S.make_ridge(-600, 1700, 812, 18, 194)))
    with cam(0.25):
        S.ridge(c, rg[0], mixc((140, 100, 124), (134, 140, 164), mood))
    with cam(0.4):
        if fs:
            foot = fy + 540 * fs
            gx = fx + 400 * fs
            hill = spath([(gx - 700 * fs - 200, 920, 0), (gx - 520 * fs, foot + 60 * fs), (gx - 330 * fs, foot - 4),
                          (gx + 330 * fs, foot - 4), (gx + 520 * fs, foot + 60 * fs), (gx + 900 * fs + 200, 920, 0)])
            p = skia.Paint(AntiAlias=True)
            hc = mixc((116, 84, 90), (128, 114, 108), mood)
            p.setShader(skia.GradientShader.MakeLinear([skia.Point(0, foot), skia.Point(0, 900)],
                                                       [C(*mixc(hc, (255, 220, 180), 0.2)), C(*mixc(hc, (40, 30, 34), 0.3))]))
            c.drawPath(hill, p)
            M.fort(an, c, t, fx, fy, fs, 0.0, key + "f")
            road = spath([(gx - 14 * fs, foot, 0), (gx + 14 * fs, foot, 0), (gx + 40, foot + 40), (gx + 10, 900, 0),
                          (gx - 30, 900, 0), (gx - 4, foot + 40)])
            c.drawPath(road, paint(C(*mixc((190, 160, 130), (206, 184, 150), mood))))
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
        S.tufts(c, get(an, key + "tf", lambda: tufts_list(196, 30, -300, 1400, gy + 26, 8, 20)), t, (70, 46, 34), 0.2)


def dust_puff(c, x, y, t, t0, lt, size=1.0, col=(236, 200, 150)):
    """A burst of dust at (x, y) that rises and fades in ~1.6 s after lt = t0."""
    u = (lt - t0) / 1.6
    if 0 <= u <= 1:
        for k in range(5):
            S.dust(c, x + (k - 2) * 46 * size * (0.4 + u), y - 30 * u * size, (50 + 110 * u) * size, t, col,
                   150 * (1 - u), k + 11)


# ------------------------------------------------------------------ props in screen space
def pole(cc, p0, p1, w=6.0, sag=0.0, head=True):
    """A long lance from p0 (butt) to p1 (point) in screen coordinates, bowed by sag px; a leaf head at p1."""
    if Pen.mode == "anchor" or p0 is None or p1 is None:
        return
    rope(cc, p0, p1, sag, w)
    if head:
        dx, dy = p1[0] - p0[0], p1[1] - p0[1]
        d = math.hypot(dx, dy) or 1.0
        ux, uy = dx / d, dy / d
        nx, ny = -uy, ux
        L, Wd = 26 * w / 6, 7.5 * w / 6
        x, y = p1
        fillp(cc, spath([(x + ux * L, y + uy * L, 0), (x + ux * L * 0.35 + nx * Wd, y + uy * L * 0.35 + ny * Wd),
                         (x - ux * L * 0.2, y - uy * L * 0.2, 0), (x + ux * L * 0.35 - nx * Wd, y + uy * L * 0.35 - ny * Wd)]))


def along(p, ang, d):
    return p[0] + d * math.cos(math.radians(ang)), p[1] + d * math.sin(math.radians(ang))


def helmet_at(cc, x, y, s, t, face=1, wind=0.8):
    """Gordafarid's cone helmet with its plume, bottom centre at (x, y) on screen, at a person's scale s."""
    cc.save()
    cc.translate(x, y)
    cc.scale(s * face, s)
    cc.translate(-6, 500)
    fillp(cc, spath([(-25, -488, 0), (-27, -510), (-17, -532), (0, -550), (8, -564, 0), (16, -550), (31, -532), (38, -512),
                     (37, -505, 0), (8, -508), (-12, -500)]))
    fillp(cc, spath([(-29, -512, 0), (40, -514, 0), (40, -506, 0), (-27, -502, 0)]))
    fillp(cc, spath([(-25, -496), (-34, -470), (-36, -446, 0), (-18, -442, 0), (-12, -470)]))
    cc.save()
    cc.translate(10, -566)
    cc.rotate(3 * math.sin(t * 1.9 + 0.7))
    for k, (a, b2, e) in enumerate([((-6, -66), (-40, -112), (-92, -104)), ((-2, -54), (-34, -92), (-80, -76)),
                                    ((2, -42), (-26, -72), (-62, -52))]):
        taper(cc, bez((0, 0), a, b2, e, 12), 6 - k, 1.1)
    cc.restore()
    cc.restore()


def flying(cc, x, y, s, face, ang, P, t, look):
    """A man thrown out of the saddle: his hips at (x, y), the body turned by ang degrees."""
    cc.save()
    cc.translate(x, y)
    cc.rotate(ang)
    person(cc, 0, 250 * s, s, face, P, t, look)
    cc.restore()


# ------------------------------------------------------------------ the pin (S01, S05, S06)
HX, HS = 760, 0.92         # Hojir on his back: feet at HX, head toward the left (face 1: head at HX - 490 HS)
SX, SS = 490, 0.9          # Sohrab kneeling on his chest, facing the head (face -1)


def pinned(an, c, t, PS, PH, zoom, focus=(540, 660), key="f16p", sx=SX, sy=GY - 40, extra=None, colt=None):
    """Hojir flat on the bright ground, Sohrab kneeling on his chest; drawn in two passes so Sohrab's rim cuts him out
    of the man below. extra(cc) draws more people (with Hojir's pass); colt = (x, pose) for the riderless colt."""
    cam = Cam(c, focus, zoom)
    field(an, c, t, cam, key, MOOD, fx=-120, fy=600, fs=0.34, host_x=700)
    if colt:
        def cf(cc):
            with Cam(cc, focus, zoom)(1.0):
                horse(cc, colt[0], GY - 4, 0.62, -1, colt[1], t)
        an.figures(c, cf, COLT, (0, 200, 1080, 1000), alpha=200)

    def fh(cc):
        with Cam(cc, focus, zoom)(1.0):
            person(cc, HX, GY, HS, 1, PH, t, HOJIR)
            if extra:
                extra(cc)
    an.figures(c, fh, MORN, (0, 300, 1080, 1100))
    if PS is not None:
        def fs(cc):
            with Cam(cc, focus, zoom)(1.0):
                person(cc, sx, sy, SS, -1, PS, t, "sohrab")
        an.figures(c, fs, MORN, (0, 120, 1080, 1100), alpha=170)
    vig(an, c, 150)


def hojir_down(t, beg=0.0, lift=0.0, jw=0.0, turn=0.0):
    """Hojir's pose on his back: beg 0..1 raises both open hands toward the man above; lift raises his head."""
    return {"mode": "lie", "hand": (mix(40, 160, beg), mix(-300, -540, beg)), "hand_kind": "open" if beg > 0.3 else "fist",
            "rhand": (mix(-40, 120, beg), mix(-280, -500, beg)), "rhand_kind": "open" if beg > 0.3 else "fist",
            "head": -14 * lift + 8 * turn + 1.5 * math.sin(t * 1.1), "jaw": jw, "stance": (30, 26)}


def sohrab_knee(t, raise_=1.0, lean=0.0, jw=0.0, dagger=True, look=0.0):
    """Sohrab kneeling on Hojir's chest: raise_ 0..1 lifts the dagger high over him; look tilts his head down."""
    P = {"mode": "kneel", "hand": (mix(110, 60, raise_), mix(-300, -560, raise_)), "dagger": mix(80, 112, raise_),
         "rhand": (mix(60, 130, raise_), mix(-240, -250, raise_)), "rhand_kind": "fist",
         "head": 10 + 6 * look + 1.2 * math.sin(t * 0.9), "lean": 2 + 8 * lean, "jaw": jw, "wind": 1.1}
    P["hand_kind"] = "dagger" if dagger else "fist"
    return P


# ================================================================== S01 + TITLE (hook)
def p16_s01(an, c, t):
    """Hook + title: Sohrab on Hojir's chest, dagger high: 'You wanted my head, Hojir? Now I will take yours!' --
    'Mercy! Spare my life!'"""
    lt = t - an.start["S01"]
    dur = an.end["TITLE"] - an.start["S01"]
    a0, a1 = LN("p16", "S01", 0)
    b0, b1 = LN("p16", "S01", 1)
    up = sstep(0.0, 0.9, lt)
    strike = sstep(a1 - 1.0, a1 - 0.2, lt)
    beg = sstep(b0 - 0.6, b0 + 0.1, lt)
    PS = sohrab_knee(t, mix(0.55, 1.0, up) + 0.06 * strike, lean=0.6 * strike - 0.2 * beg, jw=jaw(an, "SOHRAB", t, 8))
    PH = hojir_down(t, beg=beg, lift=0.6 * beg, jw=jaw(an, "HOJIR", t, 8), turn=0.6 * (1 - beg))
    pinned(an, c, t, PS, PH, 1.0 + 0.08 * ease(lt / dur), focus=(540, 640), key="f161")


# ================================================================== S02 the charge (recap)
def p16_s02(an, c, t):
    """The plain under the White Fortress: Hojir and Sohrab face each other far apart; 'Now the two riders charged'
    -- close on Hojir at full gallop, lance down: 'For Iran!'"""
    lt, dur = loc(an, "S02", t)
    L = [LN("p16", "S02", k) for k in range(4)]
    go = L[2][0] - 0.2
    cut = L[3][0] - 0.8

    def wide():
        focus = (540, 700)
        zoom = 1.0 + 0.05 * ease(lt / (cut + 0.4))
        cam = Cam(c, focus, zoom)
        field(an, c, t, cam, "f162", MOOD, fx=-10, fy=500, fs=0.5, host_x=690)
        run = clamp((lt - go) / 4.2)
        hx = 250 + 260 * run * run * 0.7 + 60 * run
        sx = 830 - 230 * run * run * 0.7 - 50 * run
        lift_h = sstep(L[0][0] + 1.0, L[0][0] + 1.8, lt)
        rr = 26 * math.sin(clamp((lt - L[1][0] - 1.0) / 1.5) * math.pi) if L[1][0] + 1.0 < lt < L[1][0] + 2.5 else 0.0
        couch = sstep(go - 0.2, go + 0.6, lt)
        PH = dict(gait="gallop" if run > 0 else "stand", phase=t * 2.1, neck=0 if run > 0 else 6 * math.sin(t * 1.7),
                  head=0 if run > 0 else 4 * math.sin(t * 1.3), wind=0.8)
        rpH = M.lance_pose(couch, {"head": 2, "lean": 6 * couch, "wind": 0.9})
        if couch < 0.01:
            rpH["hand"] = (mix(100, 80, lift_h), mix(-330, -420, lift_h))
        rpS = M.lance_pose(0.75 * couch, {"head": 2, "lean": 4 * couch, "wind": 0.9})
        PS = {"gait": "rear", "rear": rr} if rr > 1 else {"gait": "gallop" if run > 0 else "stand", "phase": t * 2.0 + 0.4,
                                                          "neck": 0 if run > 0 else 6 * math.sin(t * 1.9)}

        def fh(cc):
            with Cam(cc, focus, zoom)(1.0):
                M.rider(cc, hx, GY + 2, 0.44, 1, HOJIR, t, rpH, **PH)
        an.figures(c, fh, MORN, (0, 200, 1080, 1000))

        def fs(cc):
            with Cam(cc, focus, zoom)(1.0):
                M.rider(cc, sx, GY, 0.46, -1, "sohrab", t, rpS, rider_scale=0.92, **PS)
        an.figures(c, fs, COLT, (0, 200, 1080, 1000), alpha=200)
        if run > 0:
            for k in range(3):
                u = (lt * 1.8 + k * 0.33) % 1.0
                S.dust(c, hx - 120 - u * 160, GY - 10 - u * 20, 30 + u * 60, t, (240, 214, 170), 100 * (1 - u) * run, k)
                S.dust(c, sx + 120 + u * 160, GY - 10 - u * 20, 30 + u * 60, t, (240, 214, 170), 100 * (1 - u) * run, k + 5)
        vig(an, c, 140)

    def close():
        lt2 = lt - cut
        M.sky_day(c, MOOD)
        S.sun(c, 160, 520, 56, (255, 248, 222), (255, 214, 150), 520, 150)
        c.save()
        c.translate(0, 70)
        sc = get(an, "sc162", lambda: Scroller(163))
        sc.draw(c, lt2 + 3.0, 420, [(150, 146, 168), (176, 140, 120), (214, 172, 120)])
        PH = M.lance_pose(1.0, {"head": -4 + 2 * math.sin(t * 9), "lean": 8, "wind": 1.3, "jaw": jaw(an, "HOJIR", t, 10),
                                "rhand": (60, -320), "rhand_kind": "open"})

        def fh(cc):
            M.rider(cc, 560, 870, 0.8, 1, HOJIR, t, PH, gait="gallop", phase=t * 2.2, wind=1.2)
        an.figures(c, fh, MORN, (0, 150, 1080, 1000))
        for k in range(3):
            u = (lt2 * 2.0 + k * 0.33) % 1.0
            S.dust(c, 300 - u * 420, 860 - u * 30, 40 + u * 90, t, (240, 214, 170), 120 * (1 - u), k)
        c.restore()
        vig(an, c, 150)

    dissolve(c, lt, cut, 0.4, wide, close)


# ================================================================== S03 the clash
SG = 1000                    # ground line of the clash (medium shot: the hooves under the subtitles)
CS = 0.8                     # horses' scale in the clash


def clash_set(an, c, t, cam, key):
    field(an, c, t, cam, key, MOOD, fx=-160, fy=600, fs=0.34, host_x=760, gy=SG - 120)


def p16_s03(an, c, t):
    """The clash: Hojir's lance hits Sohrab's belt with all his strength; Sohrab does not move in the saddle. 'What?!
    What kind of man are you?' -- 'Is that all, hero of Iran? Now it is my turn.'"""
    lt, dur = loc(an, "S03", t)
    L = [LN("p16", "S03", k) for k in range(4)]
    hit = 2.0
    focus = (560, 640)
    zoom = 1.0 + 0.06 * ease(lt / dur)
    shake = 7 * math.sin(lt * 61) * math.exp(-max(0.0, lt - hit) * 6) * (lt > hit)
    c.save()
    c.translate(shake, shake * 0.4)
    cam = Cam(c, focus, zoom)
    clash_set(an, c, t, cam, "f163")
    sx = 945
    run = clamp(lt / hit)
    hx = mix(-340, 285, run) - 30 * sstep(L[2][0] - 0.2, L[2][0] + 0.8, lt)
    recoil = sstep(hit, hit + 0.25, lt) * (1 - 0.5 * sstep(hit + 0.6, hit + 1.4, lt))
    push = sstep(hit, hit + 0.3, lt) * (1 - sstep(L[1][1] + 0.6, L[1][1] + 1.2, lt))
    swat = sstep(L[1][1] - 0.4, L[1][1] + 0.3, lt)
    shock = sstep(L[2][0] - 0.3, L[2][0] + 0.3, lt)
    grin = sstep(L[3][0], L[3][0] + 0.5, lt) * (1 - sstep(L[3][0] + 1.6, L[3][0] + 2.2, lt))
    turn = sstep(L[3][1] - 1.0, L[3][1] + 0.4, lt)
    rr = 22 * math.sin(clamp((lt - hit) / 1.2) * math.pi) if hit < lt < hit + 1.2 else 0.0
    PHh = {"gait": "rear", "rear": rr} if rr > 1 else {"gait": "gallop" if run < 1 else "stand", "phase": t * 2.2,
                                                       "neck": 0 if run < 1 else 5 * math.sin(t * 1.9), "wind": 0.8}
    rpH = {"hand_kind": "fist", "hand": (mix(150, 120, shock), mix(-340, -320, shock)),
           "rhand": (mix(-10, 80, shock), mix(-300, -420, shock)), "rhand_kind": "open" if shock > 0.3 else "fist",
           "lean": 8 * (1 - recoil) - 12 * recoil - 6 * shock, "head": 2 + 6 * recoil - 6 * shock + math.sin(t * 0.8),
           "jaw": jaw(an, "HOJIR", t, 9), "wind": 0.9}
    rpS = {"hand_kind": "lance", "lance": mix(0, -60, turn), "hand": (100, -330),
           "rhand": (mix(-20, 110, swat * (1 - turn)), mix(-262, -300, swat * (1 - turn))), "rhand_kind": "open" if swat > 0.3 else "fist",
           "head": 8 * sstep(L[0][1] - 1.5, L[0][1], lt) * (1 - swat) - 6 * grin + math.sin(t * 0.7),
           "jaw": jaw(an, "SOHRAB", t, 8), "wind": 0.8}

    def fh(cc):
        with Cam(cc, focus, zoom)(1.0):
            tag("h:")
            M.rider(cc, hx, SG, CS, 1, HOJIR, t, rpH, **PHh)
            tag("")
        a = A("h:hand")
        if a is not None:
            a = (a[0] - shake, a[1] - shake * 0.4)
            belt = (focus[0] + (sx - 30 * CS - focus[0]) * zoom, focus[1] + (SG - 335 * CS - focus[1]) * zoom)
            if lt < hit:
                tip = along(a, 4, 470)
            elif swat < 0.5:
                tip = (belt[0] - 6, belt[1] + 4)
            else:
                drop = sstep(L[1][1] - 0.1, L[1][1] + 0.7, lt)
                tip = along(a, mix(10, -58, drop), 440)
            d = math.hypot(tip[0] - a[0], tip[1] - a[1]) or 1
            butt = (a[0] - (tip[0] - a[0]) / d * 200, a[1] - (tip[1] - a[1]) / d * 200)
            pole(cc, butt, tip, 6.5, -18 * push * (1 + 0.2 * math.sin(lt * 30)))
    an.figures(c, fh, MORN, (0, 150, 1080, 1100), anchors=True)

    def fs(cc):
        with Cam(cc, focus, zoom)(1.0):
            M.rider(cc, sx, SG, CS, -1, "sohrab", t, rpS, gait="stand", rider_scale=0.92,
                    neck=4 * math.sin(t * 1.3), head=3 * math.sin(t * 1.1), wind=0.7)
    an.figures(c, fs, COLT, (0, 120, 1080, 1100), alpha=200)
    if run < 1:
        for k in range(3):
            u = (lt * 2.0 + k * 0.33) % 1.0
            S.dust(c, hx - 200 - u * 200, SG - 120 - u * 20, 40 + u * 70, t, (240, 214, 170), 110 * (1 - u), k)
    dust_puff(c, 700, SG - 150, t, hit, lt, 0.8)
    c.restore()
    vig(an, c, 150)


# ================================================================== S04 unhorsed
def p16_s04(an, c, t):
    """Sohrab turns his lance around; they ride at each other and its end strikes Hojir out of the saddle; he flies
    back over his horse's croup and falls like a stone; the horse bolts. Cut to the wall: Gordafarid: 'Get up,
    Hojir... get up!'"""
    lt, dur = loc(an, "S04", t)
    L = [LN("p16", "S04", k) for k in range(3)]
    cut = L[2][0] - 0.45
    go, v = 2.3, 240.0
    hit = go + 0.9
    land = hit + 1.0
    s_h, s_s = 0.55, 0.57

    def duel():
        focus = (540, 680)
        zoom = 1.0 + 0.05 * ease(lt / cut)
        cam = Cam(c, focus, zoom)
        field(an, c, t, cam, "f164", MOOD, fx=-80, fy=560, fs=0.4, host_x=720)
        turn = sstep(0.3, 2.0, lt)
        ride = max(0.0, min(lt, hit) - go)
        hx = 200 + v * ride
        brake = clamp((lt - hit) / 0.9)
        sx = 900 - v * ride - v * 0.45 * (lt > hit) * (brake - 0.5 * brake * brake) * 0.9 * 2
        thrust = sstep(hit - 0.3, hit, lt) * (1 - sstep(hit + 0.3, hit + 0.9, lt))
        rpS = {"hand_kind": "lance", "lance": mix(-20, -98, turn), "hand": (mix(100, 165, thrust), mix(-330, -338, thrust)),
               "lean": 9 * thrust, "head": 2 + 8 * sstep(land, land + 0.6, lt) + math.sin(t * 0.7), "wind": 1.0}
        moving = go < lt < hit + 0.8
        PS = dict(gait="gallop" if moving else "stand", phase=t * 2.1, rider_scale=0.92, wind=0.9,
                  neck=0 if moving else 6 * math.sin(t * 1.4))
        x0 = hx + 30 * s_h
        y0 = GY - 330 * s_h
        fly = clamp((lt - hit) / (land - hit))
        # Hojir's horse: rears when the rider is struck, then bolts to the right behind Sohrab's colt
        rr = 30 * math.sin(clamp((lt - hit) / 1.1) * math.pi) if hit < lt < hit + 1.1 else 0.0
        bolt = clamp((lt - hit - 1.0) / 2.4)
        hpose = {"hand_kind": "fist", "hand": (150, -340), "rhand": (-10, -300), "lean": 8, "head": 2, "wind": 1.0}

        def fh(cc):
            with Cam(cc, focus, zoom)(1.0):
                if lt < hit:
                    M.rider(cc, hx, GY, s_h, 1, HOJIR, t, hpose, gait="gallop" if lt > go else "stand",
                            phase=t * 2.2, neck=0 if lt > go else 6 * math.sin(t * 1.6), wind=0.8)
                else:
                    if bolt < 1:
                        bx = hx + 1300 * bolt * bolt
                        bs = mix(s_h, 0.42, clamp(bolt * 2))
                        P = {"gait": "rear", "rear": rr} if rr > 1 else {"gait": "gallop", "phase": t * 2.4}
                        P.update(saddle=True, wind=1.0)
                        horse(cc, bx, GY - 30 * clamp(bolt * 2), bs, 1, P, t)
                    if fly < 1:
                        x = mix(x0, x0 - 170, fly)
                        y = y0 - 110 * math.sin(fly * math.pi * 0.85) + (GY - 50 - y0) * fly * fly
                        flying(cc, x, y, s_h, 1, -100 * ease(fly), {"hand": (150, -470), "hand_kind": "open",
                               "rhand": (-80, -440), "rhand_kind": "open", "stance": (60, 30), "head": -10}, t, HOJIR)
                    else:
                        person(cc, x0 - 170 + 250 * s_h, GY + 4, s_h, 1,
                               hojir_down(t, 0.0, 0.4 * sstep(land + 1.6, land + 2.6, lt)), t, HOJIR)
        an.figures(c, fh, MORN, (0, 200, 1080, 1000))

        def fs(cc):
            with Cam(cc, focus, zoom)(1.0):
                M.rider(cc, sx, GY, s_s, -1, "sohrab", t, rpS, **PS)
        an.figures(c, fs, COLT, (0, 200, 1080, 1000), alpha=200)
        if go < lt < hit + 0.5:
            for k in range(3):
                u = (lt * 2.0 + k * 0.33) % 1.0
                S.dust(c, hx - 150 - u * 160, GY - 10 - u * 20, 30 + u * 60, t, (240, 214, 170), 100 * (1 - u), k)
                S.dust(c, sx + 150 + u * 160, GY - 10 - u * 20, 30 + u * 60, t, (240, 214, 170), 100 * (1 - u), k + 4)
        dust_puff(c, x0 - 170, GY - 30, t, land - 0.05, lt, 1.0)
        if 0 < bolt < 1:
            for k in range(2):
                S.dust(c, hx + 1300 * bolt * bolt - 160, GY - 30, 60, t, (240, 214, 170), 90 * (1 - bolt), k + 8)
        vig(an, c, 145)

    def wall():
        lt2 = lt - cut
        focus = (520, 700)
        zoom = 1.0 + 0.05 * ease(lt2 / (dur - cut))
        cam = Cam(c, focus, zoom)
        lean = sstep(L[2][0] - 0.2, L[2][0] + 0.5, lt)
        PG = {"jaw": jaw(an, "GORDAFARID", t, 8), "hand": (mix(80, 150, lean), mix(-300, -420, lean)), "hand_kind": "open",
              "rhand": (40, -300), "rhand_kind": "fist", "lean": 8 * lean, "head": 6 - 4 * lean + math.sin(t * 0.9),
              "wind": 0.6}

        def figs(cc):
            with Cam(cc, focus, zoom)(1.0):
                person(cc, 420, 1330, 1.5, 1, PG, t, GORD)
        M.wall_top(an, c, t, cam, "w164", figs, mood=0.95, host_x=420, host_a=1.0, rim=MORN, par=1060)
        vig(an, c, 150)

    dissolve(c, lt, cut, 0.4, duel, wall)


# ================================================================== S05 pinned
def p16_s05(an, c, t):
    """'In a moment, Sohrab jumped down and sat on his chest.' -- 'You wanted my head, Hojir? Now I will take yours!'
    -- 'Wait! Mercy... I beg you, spare my life!' -- 'Mercy? A moment ago you wanted to send my head to Kavus!'"""
    lt, dur = loc(an, "S05", t)
    L = [LN("p16", "S05", k) for k in range(4)]
    jump0, jump1 = 0.5, 1.15
    j = clamp((lt - jump0) / (jump1 - jump0))
    draw = sstep(L[0][1] - 1.2, L[0][1] - 0.2, lt)
    up = sstep(L[1][0] - 0.2, L[1][0] + 0.6, lt)
    beg = sstep(L[2][0] - 0.5, L[2][0] + 0.2, lt)
    anger = sstep(L[3][0], L[3][0] + 0.5, lt)
    colt_x = 1010
    PH = hojir_down(t, beg=beg, lift=0.5 * sstep(0.2, 0.8, lt) * (1 - j) + 0.5 * beg, jw=jaw(an, "HOJIR", t, 8))
    if lt < jump0:
        colt = (colt_x, {"gait": "stand", "neck": 4 * math.sin(t * 1.4), "saddle": True, "rider": "sohrab", "rider_scale": 0.92,
                         "rider_pose": {"hand_kind": "lance", "lance": -30, "hand": (100, -330), "head": 8}})
        PS = None
    else:
        colt = (colt_x + 40 * sstep(jump1, jump1 + 2.0, lt), {"gait": "walk" if jump1 < lt < jump1 + 2.0 else "stand",
                                                             "phase": t * 0.9, "neck": 8 * math.sin(t * 1.2), "saddle": True})
        PS = sohrab_knee(t, mix(0.0, 0.55, draw) + 0.45 * up, lean=0.3 * up + 0.7 * anger - 0.2 * beg * (1 - anger),
                         jw=jaw(an, "SOHRAB", t, 8), dagger=draw > 0.15, look=0.5 * beg)
    focus = (560, 650)
    zoom = 1.0 + 0.07 * ease(lt / dur)
    if PS is not None and j < 1:
        # the leap: from the saddle to the man on the ground
        cam = Cam(c, focus, zoom)
        x0, y0 = colt_x - 30 * 0.62, GY + 16
        x1, y1 = SX, GY - 40
        x = mix(x0, x1, ease(j))
        y = mix(y0, y1, j) - 26 * math.sin(j * math.pi)
        PJ = {"mode": "stand", "hand": (90, -380), "hand_kind": "fist", "rhand": (-60, -380), "stance": (50, 50),
              "lean": 10, "head": 8, "wind": 1.0}

        def ex(cc):
            pass
        field(an, c, t, cam, "f165", MOOD, fx=-120, fy=600, fs=0.34, host_x=700)

        def cf(cc):
            with Cam(cc, focus, zoom)(1.0):
                horse(cc, colt[0], GY - 4, 0.62, -1, colt[1], t)
        an.figures(c, cf, COLT, (0, 200, 1080, 1000), alpha=200)

        def fh(cc):
            with Cam(cc, focus, zoom)(1.0):
                person(cc, HX, GY, HS, 1, PH, t, HOJIR)
        an.figures(c, fh, MORN, (0, 300, 1080, 1100))

        def fs(cc):
            with Cam(cc, focus, zoom)(1.0):
                person(cc, x, y, 0.84, -1, PJ, t, "sohrab")
        an.figures(c, fs, MORN, (0, 120, 1080, 1100), alpha=170)
        vig(an, c, 150)
        return
    pinned(an, c, t, PS, PH, zoom, focus, "f165", colt=colt)


# ================================================================== S06 mercy
def p16_s06(an, c, t):
    """Sohrab lowers the dagger and puts it away; he stands; Hojir gets up on his knees: 'You... you will let me
    live?' -- 'Live, Hojir. But remember this: never boast before a battle.' -- 'Tie his hands, and take him to
    Hooman!' (two Turanian riders come at a gallop)."""
    lt, dur = loc(an, "S06", t)
    L = [LN("p16", "S06", k) for k in range(5)]
    cut = L[1][0] - 0.2

    def pin():
        low = sstep(1.2, 3.4, lt)
        away = sstep(L[0][1] - 0.9, L[0][1] - 0.2, lt)
        PS = sohrab_knee(t, mix(1.0, 0.0, low), lean=-0.3 * low, dagger=away < 0.5, look=1.0)
        if away > 0.5:
            PS.update(hand=(mix(60, 20, away), mix(-300, -270, away)))
        PH = hojir_down(t, beg=mix(1.0, 0.5, low), lift=0.5)
        pinned(an, c, t, PS, PH, 1.07 + 0.03 * ease(lt / cut), (560, 650), "f166",
               colt=(1050, {"gait": "stand", "neck": 8 * math.sin(t * 1.2), "saddle": True}))

    def two():
        lt2 = lt - cut
        focus = (560, 420)
        zoom = 1.0 + 0.05 * ease(lt2 / (dur - cut))
        cam = Cam(c, focus, zoom)
        field(an, c, t, cam, "f166b", MOOD, fx=-160, fy=600, fs=0.34, host_x=720)
        rise = sstep(cut + 0.6, cut + 2.4, lt)
        ask = sstep(L[2][0] - 0.2, L[2][0] + 0.4, lt)
        wag = sstep(L[3][0] + 1.0, L[3][0] + 1.5, lt) * (1 - sstep(L[3][1] - 0.2, L[3][1] + 0.3, lt))
        point = sstep(L[4][0] - 0.1, L[4][0] + 0.5, lt)
        riders = clamp((lt - L[4][0] - 0.4) / 2.2)
        PH = {"mode": "kneel", "jaw": jaw(an, "HOJIR", t, 8),
              "hand": (mix(80, 120, ask), mix(-300, -400, ask)), "hand_kind": "open",
              "rhand": (-20, -280), "head": -8 * ask + 4 * (1 - ask) + 1.2 * math.sin(t * 0.8), "lean": 10 - 8 * ask,
              "wind": 0.6}
        PS = {"jaw": jaw(an, "SOHRAB", t, 8), "rprop": "lance", "lance": -42, "rhand": (-30, -262),
              "hand": (mix(mix(40, 150, wag), 40, point), mix(mix(-262, -420, wag), -262, point)),
              "hand_kind": "open" if wag > 0.3 else "fist", "head": 6 + math.sin(t * 0.8) - 8 * point, "stance": (56, 48),
              "wind": 0.6}
        if point > 0.01:
            PS.update(rhand=(mix(-20, -170, point), mix(-300, -440, point)), rhand_kind="open", rprop=None)

        PL = hojir_down(t, 0.3, 0.6)
        PK = dict(PH, mode="kneel")
        mid = clamp((rise - 0.3) / 0.4)        # Hojir gets up: a short dissolve from lying to kneeling

        def fh(cc):
            with Cam(cc, focus, zoom)(1.0):
                if riders > 0:
                    for i in range(2):
                        x = mix(1300 + i * 140, 930 + i * 110, ease(riders))
                        M.rider(cc, x, GY - 22 - i * 6, 0.36, -1, "rider", t, {"hand_kind": "spear", "hand": (100, -330)},
                                gait="gallop" if riders < 1 else "stand", phase=t * 2.0 + i * 0.4)
                person(cc, 760, GY + 4, 0.88, -1, PS, t, "sohrab")
        an.figures(c, fh, MORN, (0, 150, 1080, 1100))

        def hj(P, x):
            def f(cc):
                with Cam(cc, focus, zoom)(1.0):
                    person(cc, x, GY + 4, 0.92, 1, P, t, HOJIR)
            return f
        if mid < 1:
            an.figures(c, hj(PL, 560), MORN, (0, 150, 1080, 1100))
        if mid > 0:
            if mid < 1:
                c.saveLayerAlpha(None, int(255 * ease(mid)))
            an.figures(c, hj(PK, 330), MORN, (0, 150, 1080, 1100))
            if mid < 1:
                c.restore()
        vig(an, c, 145)

    dissolve(c, lt, cut, 0.6, pin, two)


# ================================================================== S07 the prisoner in the camp
CAMP_Y = 872


def p16_s07(an, c, t):
    """'And so the keeper of the White Fortress was led into the enemy camp... a prisoner.' Hooman: 'Welcome to our
    camp, keeper of the White Fortress! Beaten by a boy, with one blow.' Hojir: 'Kill me if you want...' Barman:
    'Keep him alive, Hooman. A prisoner who knows Iran can be useful.'"""
    lt, dur = loc(an, "S07", t)
    L = [LN("p16", "S07", k) for k in range(5)]
    c1 = L[1][0] - 0.5

    def led():
        focus = (560, 700)
        zoom = 1.0 + 0.05 * ease(lt / (c1 + 0.4))
        cam = Cam(c, focus, zoom)
        camp(an, c, t, cam, "cp167")
        walk = clamp(lt / (c1 - 0.3))
        rx = mix(420, 860, walk)
        moving = walk < 1
        rp = {"rhand": (-120, -300), "rhand_kind": "fist", "hand": (100, -300), "hand_kind": "spear", "head": -4}

        def figs(cc):
            with Cam(cc, focus, zoom)(1.0):
                tag("r:")
                M.rider(cc, rx, CAMP_Y, 0.52, 1, "rider", t, rp, gait="walk" if moving else "stand", phase=t * 0.8)
                tag("h:")
                person(cc, rx - 300, CAMP_Y, 0.56, 1, {"mode": "walk" if moving else "stand", "phase": lt * 3.2, "stride": 16,
                                                      "hand": (70, -276), "rhand": (62, -270), "head": 12, "lean": 7,
                                                      "wind": 0.5}, t, HOJIR)
                tag("")
            rope(cc, A("r:rhand"), A("h:hand"), 30, 2.4)
        an.figures(c, figs, DAY, (0, 200, 1080, 1000), anchors=True)
        vig(an, c, 140)

    def hb():
        focus = (520, 680)
        zoom = 1.02 + 0.04 * ease((lt - c1) / (dur - c1))
        cam = Cam(c, focus, zoom)
        camp(an, c, t, cam, "cp167b")
        whisper = lt > L[4][0] - 0.4
        mock = sstep(L[1][0], L[1][0] + 0.5, lt) * (1 - sstep(L[2][1], L[2][1] + 0.5, lt))
        laugh = sstep(L[2][0], L[2][0] + 0.3, lt) * (1 - sstep(L[2][1] - 0.2, L[2][1] + 0.3, lt))
        listen = sstep(L[4][0], L[4][0] + 0.6, lt)
        PHo = {"jaw": jaw(an, "HOOMAN", t, 8), "rprop": "mace", "rhand": (-24, -300), "mace": -6,
               "hand": (mix(40, 150, mock), mix(-262, -380, mock)), "hand_kind": "open" if mock > 0.3 else "fist",
               "head": 3 - 6 * laugh + 6 * listen + math.sin(t * 0.7), "lean": -3 * laugh + 2 * listen, "wind": 0.5}
        PBa = {"jaw": jaw(an, "BARMAN", t, 8), "hand_kind": "spear", "hand": (60, -330), "wind": 0.5,
               "head": (4 if whisper else 2) + math.sin(t * 0.6), "lean": 4 * listen}

        def figs(cc):
            with Cam(cc, focus, zoom)(1.0):
                person(cc, 290, 1330, 1.34, 1 if whisper else -1, PBa, t, BARMAN)
                person(cc, 700, 1330, 1.44, -1, PHo, t, HOOMAN)
        an.figures(c, figs, DAY, (0, 100, 1080, 1500))
        vig(an, c, 150)

    def hj():
        focus = (520, 680)
        zoom = 1.04 + 0.04 * ease((lt - L[3][0]) / 4.0)
        cam = Cam(c, focus, zoom)
        camp(an, c, t, cam, "cp167c")
        defy = sstep(L[3][0] + 1.6, L[3][0] + 2.2, lt)
        PH = {"jaw": jaw(an, "HOJIR", t, 8), "hand": (70, -276), "rhand": (62, -270),
              "head": 4 - 10 * defy + math.sin(t * 0.8), "lean": -2 - 3 * defy, "wind": 0.5}

        def figs(cc):
            with Cam(cc, focus, zoom)(1.0):
                tag("h:")
                person(cc, 430, 1330, 1.5, 1, PH, t, HOJIR)
                tag("g:")
                person(cc, 110, 1330, 1.3, 1, {"rhand": (60, -320), "hand": (80, -300), "hand_kind": "spear", "head": 4},
                       t, "rider")
                tag("")
            rope(cc, A("g:rhand"), A("h:hand"), 40, 3.0)
        an.figures(c, figs, DAY, (0, 100, 1080, 1500), anchors=True)
        vig(an, c, 150)

    cuts(c, lt, [(0.0, led), (c1, hb), (L[3][0] - 0.35, hj), (L[4][0] - 0.4, hb)])


# ================================================================== S08 the wall mourns
MOURN = [(40, 1.1, 1, "warrior_ir", 0.0), (255, 1.06, 1, "maid", 1.7), (880, 1.12, -1, "warrior_ir", 3.1),
         (1065, 1.04, -1, "maid", 4.6)]


def p16_s08(an, c, t):
    """On the wall of the White Fortress: the people cry out and weep; old Gazhdaham: 'Hojir is taken... Who will
    defend us now?' -- 'Not one of our warriors can stand against that boy.'"""
    lt, dur = loc(an, "S08", t)
    L = [LN("p16", "S08", k) for k in range(3)]
    cut = L[1][0] - 0.5

    def mourners(cc, k0=1.0):
        for i, (x, s, f, look, ph) in enumerate(MOURN):
            w = math.sin(t * 2.2 + ph)
            if look == "maid":
                P = {"hand": (30 + 10 * w, -520), "hand_kind": "open", "rhand": (10, -530), "rhand_kind": "open",
                     "head": 16 + 4 * w, "lean": 8 + 3 * w, "seed": ph}
            else:
                P = {"hand": (40, -500 + 10 * w), "hand_kind": "open", "rprop": "spear", "rhand": (-10, -300),
                     "head": 18 + 3 * w, "lean": 6, "seed": ph}
            person(cc, x, 1290, s, f, P, t, look)

    def wide():
        focus = (540, 720)
        zoom = 1.0 + 0.04 * ease(lt / (cut + 0.5))
        cam = Cam(c, focus, zoom)
        PG = {"hand_kind": "staff", "hand": (60, -300), "rhand": (-20, -280), "head": 18 + 2 * math.sin(t * 0.7),
              "lean": 6}

        def figs(cc):
            with Cam(cc, focus, zoom)(1.0):
                mourners(cc)
                person(cc, 560, 1290, 1.2, -1, PG, t, GAZH)
        M.wall_top(an, c, t, cam, "w168", figs, mood=1.0, host_x=520, host_a=1.0, rim=MORN, par=1010)
        vig(an, c, 150)

    def close():
        lt2 = lt - cut
        focus = (560, 700)
        zoom = 1.0 + 0.05 * ease(lt2 / (dur - cut))
        cam = Cam(c, focus, zoom)
        look_up = sstep(L[2][0] - 0.2, L[2][0] + 0.6, lt)
        PG = {"jaw": jaw(an, "GAZHDAHAM", t, 8), "hand_kind": "staff", "hand": (60, -300),
              "rhand": (mix(-20, 70, look_up), mix(-280, -360, look_up)), "rhand_kind": "open" if look_up > 0.3 else "fist",
              "head": mix(16, 0, look_up) + 1.5 * math.sin(t * 0.7), "lean": mix(6, 0, look_up)}

        def figs(cc):
            with Cam(cc, focus, zoom)(1.0):
                person(cc, 460, 1420, 1.62, 1, PG, t, GAZH)
                person(cc, 1000, 1330, 1.2, -1, {"hand": (30, -520), "hand_kind": "open", "rhand": (10, -530),
                                                 "rhand_kind": "open", "head": 16 + 3 * math.sin(t * 2.0), "lean": 8}, t, "maid")
        M.wall_top(an, c, t, cam, "w168b", figs, mood=1.0, host_x=-200, host_a=1.0, rim=MORN, par=1080)
        vig(an, c, 155)

    dissolve(c, lt, cut, 0.45, wide, close)


# ================================================================== S09 + END Gordafarid
def p16_s09(an, c, t):
    """Turn + end: Gordafarid steps up: 'I will, Father.' -- 'You? My daughter, he has just defeated Hojir!' -- 'Then
    he has not met me yet. Bring me my armour... and my horse.' Then, alone on the wall in armour, she puts on her
    helmet: 'And Sohrab did not know that the next warrior to face him... would be a woman.'"""
    lt = t - an.start["S09"]
    dur = an.end["END"] - an.start["S09"]
    L = [LN("p16", "S09", k) for k in range(4)]
    cut = L[3][0] - 0.4

    def talk():
        focus = (540, 700)
        zoom = 1.0 + 0.05 * ease(lt / (cut + 0.5))
        cam = Cam(c, focus, zoom)
        step = clamp(lt / 1.1)
        gx = mix(130, 330, ease(step))
        turn = lt > L[2][0] + 2.0
        call = sstep(L[2][0] + 2.0, L[2][0] + 2.5, lt)
        proud = sstep(L[2][0], L[2][0] + 0.5, lt)
        doubt = sstep(L[1][0], L[1][0] + 0.5, lt) * (1 - sstep(L[1][1], L[1][1] + 0.5, lt))
        PG = {"mode": "walk" if step < 1 else "stand", "phase": lt * 4.0, "stride": 15, "jaw": jaw(an, "GORDAFARID", t, 7),
              "hand": (mix(40, 120, proud * (1 - call)), mix(-262, -330, proud * (1 - call))),
              "hand_kind": "fist", "rhand": (-20, -270), "head": -4 * proud + math.sin(t * 0.8), "wind": 0.7}
        if turn:
            PG.update(hand=(mix(40, 170, call), mix(-262, -420, call)), hand_kind="open", head=-2 + math.sin(t * 0.8))
        PZ = {"jaw": jaw(an, "GAZHDAHAM", t, 8), "hand_kind": "staff", "hand": (60, -300),
              "rhand": (mix(-20, 140, doubt), mix(-280, -400, doubt)), "rhand_kind": "open" if doubt > 0.3 else "fist",
              "head": 2 + 6 * (1 - step) - 3 * doubt + math.sin(t * 0.6), "lean": 2 * doubt}

        def figs(cc):
            with Cam(cc, focus, zoom)(1.0):
                person(cc, gx if not turn else 330, 1330, 1.42, -1 if turn else 1, PG, t, GORD)
                person(cc, 790, 1330, 1.48, -1, PZ, t, GAZH)
        M.wall_top(an, c, t, cam, "w169", figs, mood=1.0, host_x=60, host_a=1.0, rim=MORN, par=1060)
        vig(an, c, 150)

    def helm():
        lt2 = lt - cut
        focus = (540, 520)
        zoom = 1.0 + 0.08 * ease(lt2 / (dur - cut))
        cam = Cam(c, focus, zoom)
        h0, h1 = L[3][0] + 1.3, L[3][0] + 2.9
        on = sstep(h0, h1, lt)
        worn = lt >= h1
        spear = sstep(h1 + 0.6, h1 + 1.4, lt)
        lift = sstep(cut + 0.2, cut + 1.0, lt)
        hy_ = mix(mix(-430, -600, lift), -512, on)
        P = {"hand": (mix(70, 22, lift), hy_), "rhand": (mix(-20, -4, lift), hy_ + 4), "hand_kind": "fist",
             "rhand_kind": "fist", "head": -2 + 4 * on + math.sin(t * 0.7), "wind": 1.1}
        if worn:
            P = {"hand": (mix(40, 62, spear), mix(-300, -330, spear)), "hand_kind": "spear" if spear > 0.5 else "fist",
                 "rhand": (-24, -262), "head": -4 + math.sin(t * 0.7), "wind": 1.2}
        GS, GYH = 1.45, 1440

        def figs(cc):
            with Cam(cc, focus, zoom)(1.0):
                tag("g:")
                person(cc, 470, GYH, GS, 1, P, t, GORD_ARM if worn else GORD_BARE)
                tag("")
            if not worn:
                a, b = A("g:hand"), A("g:rhand")
                if a and b:
                    helmet_at(cc, (a[0] + b[0]) / 2 + 4, (a[1] + b[1]) / 2 + 6, GS * zoom, t, 1)
        # wall_top draws the figures without an anchor pass: run it here so the helmet can find her hands
        anim.ANCH.clear()
        Pen.mode = "anchor"
        figs(c)
        Pen.mode = "fill"
        M.wall_top(an, c, t, cam, "w169b", figs, mood=1.0, host_x=520, host_a=1.0, rim=MORN, par=1090,
                   box=(0, 0, 1080, 1500))
        vig(an, c, 160)

    dissolve(c, lt, cut, 0.7, talk, helm)


P16 = {"S01": p16_s01, "TITLE": p16_s01, "S02": p16_s02, "S03": p16_s03, "S04": p16_s04, "S05": p16_s05,
       "S06": p16_s06, "S07": p16_s07, "S08": p16_s08, "S09": p16_s09, "END": p16_s09}
SHIFT16 = {}

register(P16, SHIFT16)
