"""Parts 13-14 (row 7 of OUTLINE.md, "Afrasiab's Plot"): every shot as a shadow-play scene.

Importing this module registers part 13's shots; p14_scenes.py imports it and registers part 14's.
New here, to reuse: HOOMAN / BARMAN (looks of the two Turanian commanders: Hooman with a long beard, a cape and a
mace; Barman with a short beard and a spear), cuts() (shot / reverse shot with short dissolves at the given
times), afr_close() (Afrasiab on his throne by the brazier, close), hb_two() (Hooman and Barman facing him, close),
trio() (the three of them leaning in by the fire), hall_wide(), held() (a person lifted by the belt at a hand
anchor), turan_bank() (the river and the city of Turan at dusk), battle_plain() (a red sunset battlefield with a
bright dusty ground, so fallen figures read), treasury(), scribe_wall() (a scribe writing by a candle against the
lit curtain), dawn_march() (the Turanian army leaving at dawn), white_fortress() (the White Fortress on its hill
under the moon).
Line timings come from pNN/audio/timeline.json (LN), so the action follows the voices.
"""
import math, random
import skia
import anim
from anim import C, mix, mixc, clamp, ease, sstep, Cam, Pen, rope, spath, ppath, paint, fillp, W, H
from puppets import person, horse, LOOKS
import sets as S
from ep01_scenes import loc, jaw, get, vig, tag, A, ground, INK, hall, Scroller, tufts_list, reed_list
from p05_scenes import MOON, shadow_layer, ghost_layer, register, standing_candle
from p07_scenes import LN, dissolve, seated, DAWN, DAY
from p09_scenes import flick, chest, scroll, SUNSET
from p11_scenes import (EMBER, COLT, throne, sit_throne, crown_shape, brazier, curtain, army_band, draw_band, camp,
                        dark_hall, croup, to_local)

HOOMAN = dict(LOOKS["warrior_tu"], beard="long", cape=True, b=1.08)   # fur cap, long beard, cape, mace
BARMAN = dict(LOOKS["warrior_tu"])                                      # fur cap, short beard, spear
GOLD = (255, 204, 120)                                                  # lamp-lit treasury


# ------------------------------------------------------------------ helpers
def cuts(c, lt, seq, d=0.35):
    """Shot / reverse shot: seq = [(t0, draw), ...] in time order; a d-second dissolve at each cut."""
    k = 0
    for i, (t0, _) in enumerate(seq):
        if lt >= t0:
            k = i
    t0, fn = seq[k]
    if k > 0 and lt < t0 + d:
        seq[k - 1][1]()
        c.saveLayerAlpha(None, int(255 * ease((lt - t0) / d)))
        fn()
        c.restore()
    else:
        fn()


def world(p, focus, zoom):
    """A screen point (an anchor) back in the camera's world coordinates."""
    return focus[0] + (p[0] - focus[0]) / zoom, focus[1] + (p[1] - focus[1]) / zoom


def held(cc, x, y, s, ang, face, P, t, look):
    """A person lifted by the belt: the belt (local y -262) at (x, y), the body turned by ang degrees."""
    cc.save()
    cc.translate(x, y)
    cc.rotate(ang)
    person(cc, 0, 262 * s, s, face, P, t, look)
    cc.restore()


def motes(an, c, t, key, a=110):
    get(an, key, lambda: S.Motes(50, 131, 300, 1100)).draw(c, t, (255, 150, 90), a, rise=30, drift=0.2)


# ------------------------------------------------------------------ Afrasiab's hall (dark_hall of p11)
def afr_close(an, c, t, PA, zoom, fire=1.0, vision=None, focus=(640, 640), key="ac"):
    """Afrasiab on his throne, close, the brazier on the left (vision(cam) draws in the smoke above it)."""
    cam = Cam(c, focus, zoom)
    dark_hall(an, c, t, cam, fire)
    if vision:
        vision(cam)

    def figs(cc):
        with Cam(cc, focus, zoom)(1.0):
            sit_throne(cc, 760, 1330, 1.75, -1, PA, t, "afrasiab")
    an.figures(c, figs, EMBER, (0, 100, 1080, 1500), alpha=180)
    with cam(1.0):
        brazier(c, 170, 1240, 1.2, t, fire)
    motes(an, c, t, key + "mo")
    vig(an, c, 200)


def hb_two(an, c, t, PH, PB, zoom, fire=1.0, focus=(440, 660), PB_face=1, key="hb"):
    """Hooman and Barman standing before the king (off screen right), close; the brazier on the right."""
    cam = Cam(c, focus, zoom)
    dark_hall(an, c, t, cam, fire)

    def figs(cc):
        with Cam(cc, focus, zoom)(1.0):
            person(cc, 190, 1330, 1.5, 1, PH, t, HOOMAN)
            person(cc, 610, 1330, 1.36, PB_face, PB, t, BARMAN)
    an.figures(c, figs, EMBER, (0, 100, 1080, 1500), alpha=180)
    with cam(1.0):
        brazier(c, 905, 1240, 1.2, t, fire)
    motes(an, c, t, key + "mo")
    vig(an, c, 200)


def trio(an, c, t, PH, PB, PA, zoom, fire=1.0, focus=(520, 640), key="tr"):
    """Hooman and Barman (left) lean in to Afrasiab on his throne (right); the brazier low between them."""
    cam = Cam(c, focus, zoom)
    dark_hall(an, c, t, cam, fire)
    with cam(0.85):
        brazier(c, 540, 1080, 0.75, t, fire)

    def figs(cc):
        with Cam(cc, focus, zoom)(1.0):
            person(cc, 85, 1330, 1.45, 1, PH, t, HOOMAN)
            person(cc, 380, 1330, 1.28, 1, PB, t, BARMAN)
            sit_throne(cc, 870, 1330, 1.55, -1, PA, t, "afrasiab")
    an.figures(c, figs, EMBER, (0, 100, 1080, 1500), alpha=180)
    motes(an, c, t, key + "mo")
    vig(an, c, 200)


def hall_wide(an, c, t, PA, extra, zoom, focus=(560, 680), fire=1.0, bx=560, throne_x=850):
    """The hall, wide: Afrasiab on his throne at the right, the brazier, and extra(cc) for the others."""
    cam = Cam(c, focus, zoom)
    dark_hall(an, c, t, cam, fire)

    def figs(cc):
        with Cam(cc, focus, zoom)(1.0):
            sit_throne(cc, throne_x, 900, 1.0, -1, PA, t, "afrasiab")
            extra(cc)
    an.figures(c, figs, EMBER, (0, 150, 1080, 1100), alpha=170)
    if bx is not None:
        with cam(1.0):
            brazier(c, bx, 900, 0.8, t, fire)
    vig(an, c, 190)


def smoke_vision(c, cam, a, draw, col=(255, 170, 130), box=(0, 260, 620, 980), blur=3.0):
    """A pale vision rising in the smoke over the brazier of afr_close."""
    if a <= 0.01:
        return
    with cam(0.8):
        ghost_layer(c, box, a, col, blur)
        draw(c)
        c.restore()


# ------------------------------------------------------------------ outdoor sets
def turan_bank(an, c, t, cam, key):
    """The great river at dusk; beyond it the city of Turan under a red moon; reeds on the near bank."""
    S.lin(c, 0, 900, [(0, (22, 8, 30)), (0.4, (88, 24, 52)), (0.72, (188, 72, 62)), (0.9, (234, 130, 82)),
                      (1, (244, 160, 98))])
    with cam(0.12):
        get(an, key + "st", lambda: S.Stars(70, 380, 141)).draw(c, t, 0.5, 380)
        S.moon(c, 770, 450, 44, (255, 214, 186), (200, 80, 70))
    with cam(0.2):
        get(an, key + "cl", lambda: S.Clouds([(330, 12), (400, 9), (480, 14)], 142, 300, 600)).draw(c, t, (72, 20, 46), 170)
    rg = get(an, key + "rg", lambda: S.make_ridge(-600, 1700, 700, 70, 143, 8, 4, 0.5))
    with cam(0.3):
        S.ridge(c, rg, (74, 26, 48))
    img, lights = get(an, key + "city", lambda: S.city(1500, 700, 690, 144, (34, 10, 22), True, None))
    with cam(0.45):
        c.save()
        c.translate(90, 406)
        c.scale(0.6, 0.6)
        c.drawImage(img, 0, 0)
        for k, (x, y) in enumerate(lights):
            if k % 2 == 0:
                c.drawRect(skia.Rect.MakeXYWH(x - 5, y - 10, 10, 16), paint(C(255, 170, 100, 150 + 60 * math.sin(t * 2 + k))))
        c.restore()
        S.lin(c, 760, 822, [(0, (230, 120, 80, 0)), (1, (230, 120, 80, 90))], (-300, 760, 1400, 822))
    with cam(0.7):
        S.water(c, 820, 876, t, (214, 104, 76), (120, 40, 52), (255, 200, 150), 145, 30)
    with cam(1.0):
        ground(c, 874, (30, 10, 16), (6, 2, 4), 10)
        S.reeds(c, get(an, key + "rd", lambda: reed_list(146, 26, -260, 330, 884, 80, 190)), t, INK, 0.3)
        S.reeds(c, get(an, key + "rd2", lambda: reed_list(147, 14, 900, 1350, 884, 60, 150)), t, INK, 0.3)


def battle_plain(an, c, t, cam, key):
    """A red sunset battlefield: big low sun, two ridges, a bright dusty ground (fallen figures read on it)."""
    S.lin(c, 0, 880, [(0, (58, 16, 30)), (0.38, (170, 62, 50)), (0.72, (240, 142, 82)), (1, (252, 196, 124))])
    with cam(0.2):
        S.sun(c, 600, 770, 130, (255, 232, 186), (255, 140, 80), 640, 170)
        get(an, key + "cl", lambda: S.Clouds([(280, 16), (360, 12), (450, 18)], 151)).draw(c, t, (90, 24, 40), 180)
    rg = get(an, key + "rg", lambda: (S.make_ridge(-600, 1700, 776, 46, 152, 8, 4, 0.4),
                                      S.make_ridge(-600, 1700, 824, 18, 153)))
    with cam(0.4):
        S.ridge(c, rg[0], (140, 60, 62))
    with cam(0.55):
        S.ridge(c, rg[1], (110, 44, 46))
    with cam(0.85):
        ground(c, 858, (214, 140, 90), (76, 36, 28))


def white_fortress(an, c, t, cam, key):
    """The White Fortress on its hill under the moon: pale walls and towers, torches, a road up to the gate."""
    S.lin(c, 0, 900, [(0, (8, 10, 30)), (0.5, (30, 36, 80)), (0.85, (80, 74, 120)), (1, (120, 100, 130))])
    with cam(0.12):
        get(an, key + "st", lambda: S.Stars(150, 700, 171)).draw(c, t, 0.9, 700)
        S.moon(c, 250, 380, 56)
    with cam(0.2):
        get(an, key + "cl", lambda: S.Clouds([(420, 12), (500, 9), (580, 14)], 172, 300, 600)).draw(c, t * 1.6, (34, 40, 76), 190)
    rg = get(an, key + "rg", lambda: S.make_ridge(-600, 1700, 760, 60, 173, 8, 4, 0.4))
    with cam(0.3):
        S.ridge(c, rg, (30, 30, 58))
    with cam(0.5):
        hill = spath([(-200, 1400, 0), (-200, 900), (200, 860), (420, 760), (560, 724), (760, 724), (900, 770), (1100, 840),
                      (1400, 880), (1400, 1400, 0)])
        c.drawPath(hill, paint(C(16, 14, 28)))
        img, lights = get(an, key + "fort", lambda: S.city(800, 560, 540, 174, (226, 222, 212), True, 400))
        c.save()
        c.translate(420, 470)
        c.scale(0.5, 0.5)
        S.glow(c, 400, 400, 700, (190, 200, 255), 90)
        c.drawImage(img, 0, 0)
        S.lin(c, 200, 560, [(0, (30, 30, 60, 0)), (1, (30, 30, 60, 150))], (0, 200, 800, 560))
        for k, (x, y) in enumerate(lights):
            if k % 2 == 0:
                c.drawRect(skia.Rect.MakeXYWH(x - 6, y - 12, 12, 18), paint(C(255, 190, 110, 170 + 60 * math.sin(t * 2 + k))))
        c.restore()
        for k, x in enumerate((470, 640, 790)):
            S.glow(c, x, 690, 60, (255, 160, 80), 150 + 30 * math.sin(t * 7 + k))
            S.flame(c, x, 690, 0.18, t, k * 1.3)
        road = spath([(470, 1400, 0), (520, 1000), (600, 880), (620, 800), (620, 744, 0), (640, 744, 0), (650, 800),
                      (660, 880), (640, 1000), (600, 1400, 0)])
        c.drawPath(road, paint(C(70, 64, 96)))
    with cam(1.0):
        ground(c, 1000, (12, 10, 20), (4, 3, 8), -20)


# ================================================================== part 13 shots
def p13_s01(an, c, t):
    """Hook + title: 'A weapon that can kill Rostam? What weapon, my king?' -- 'His own son.'"""
    lt = t - an.start["S01"]
    dur = an.end["TITLE"] - an.start["S01"]
    a0, a1 = LN("p13", "S01", 0)
    b0, b1 = LN("p13", "S01", 1)
    ask = sstep(a0 + 0.3, a0 + 0.9, lt) * (1 - sstep(a1, a1 + 0.6, lt))
    lean = sstep(b0 - 0.9, b0 + 0.1, lt)
    grip = sstep(b0 + 0.3, b1 + 0.5, lt)
    shock = sstep(b1 - 0.1, b1 + 0.6, lt)
    fire = 1.0 + 0.6 * sstep(b0 + 0.1, b1 + 0.6, lt)
    PH = {"jaw": jaw(an, "HOOMAN", t, 8), "hand": (mix(40, 100, ask), mix(-262, -450, ask)),
          "hand_kind": "open" if ask > 0.3 else "fist", "rprop": "mace", "rhand": (-24, -300), "mace": -6,
          "head": 2 - 3 * ask - 5 * shock + 1.2 * math.sin(t * 0.7), "lean": 3 * ask - 4 * shock, "wind": 0.2}
    PB = {"hand_kind": "spear", "hand": (60, -330), "head": 3 - 4 * shock + 1.2 * math.sin(t * 0.6 + 1.0),
          "lean": -3 * shock, "wind": 0.2}
    PA = {"jaw": jaw(an, "AFRASIAB", t, 7), "hand": (mix(110, 160, lean) - 30 * grip, mix(-320, -380, lean) - 50 * grip),
          "hand_kind": "fist" if grip > 0.4 else "open", "rhand": (-30, -262),
          "head": 4 - 6 * lean + 3 * grip + 1.2 * math.sin(t * 0.5), "lean": 9 * lean}
    trio(an, c, t, PH, PB, PA, 1.0 + 0.09 * ease(lt / dur), fire, key="tr131")


def p13_s02(an, c, t):
    """Turan beyond the great river at dusk; a ghost host rides out against Iran; then the ghost of Rostam on Rakhsh."""
    lt, dur = loc(an, "S02", t)
    L = [LN("p13", "S02", k) for k in range(3)]
    focus = (540, 700)
    zoom = 1.0 + 0.07 * ease(lt / dur)
    cam = Cam(c, focus, zoom)
    turan_bank(an, c, t, cam, "tb132")
    host = sstep(L[1][0] + 0.2, L[1][0] + 1.4, lt) * (1 - sstep(L[2][0] - 0.6, L[2][0] + 0.3, lt))
    ro = sstep(L[2][0] - 0.3, L[2][0] + 0.5, lt)
    if host > 0.01:
        with cam(0.3):
            ghost_layer(c, (0, 280, W, 800), 0.5 * host, (255, 170, 140), 2.6)
            u = lt - L[1][0]
            for i in range(7):
                x = 1180 - 70 * u - i * 110 + 30 * (i % 2)
                horse(c, x, 600 + (i % 3) * 16, 0.19, -1, {"gait": "gallop", "phase": t * 1.9 + i * 0.37, "saddle": True,
                                                         "rider": "warrior_tu",
                                                         "rider_pose": {"hand_kind": "spear", "hand": (110, -340), "lean": 8}}, t)
            c.restore()
    if ro > 0.01:
        with cam(0.3):
            ghost_layer(c, (0, 200, W, 860), 0.72 * ro, (255, 216, 160), 2.4)
            rr = 28 * math.sin(clamp((lt - L[2][0] - 0.1) / 1.6) * math.pi) if lt > L[2][0] + 0.1 else 0.0
            g = {"gait": "rear", "rear": rr} if rr > 1 else {"gait": "stand", "neck": 10, "head": 4}
            horse(c, 360, 780, 0.6, 1, dict(g, saddle=True, rider="rostam", wind=1.0,
                                           rider_pose={"hand_kind": "oxmace", "hand": (70, -540), "mace": -10, "head": -3,
                                                       "wind": 1.0}), t)
            c.restore()
    vig(an, c, 160)


def p13_s03(an, c, t):
    """Memory: young Rostam charges Afrasiab on Rakhsh, lifts him out of the saddle by the belt; the belt breaks,
    the king falls in the dust and his riders snatch him away."""
    lt, dur = loc(an, "S03", t)
    L = [LN("p13", "S03", k) for k in range(3)]
    cut = L[1][0] - 0.3
    band = get(an, "band133", lambda: army_band(False, 33))

    def wide():
        focus = (560, 660)
        zoom = 1.0 + 0.04 * ease(lt / (cut + 0.4))
        cam = Cam(c, focus, zoom)
        battle_plain(an, c, t, cam, "bp133")
        with cam(0.8):
            draw_band(c, band, 560, 552, (80, 30, 32), 1.0)
        run = clamp((lt - 0.2) / (cut - 0.2))
        rx = mix(-380, 470, run)
        r0 = cut - 1.5
        rr = 30 * math.sin(clamp((lt - r0) / 1.4) * math.pi) if lt > r0 else 0.0
        PH = {"gait": "rear", "rear": rr} if rr > 1 else {"gait": "stand", "neck": 6 * math.sin(t * 1.7), "head": 4 * math.sin(t * 1.3)}
        PH.update(saddle=True, rider="afrasiab", rider_pose={"hand_kind": "sword", "hand": (110, -380), "head": -2, "wind": 0.8})
        PR = {"gait": "gallop", "phase": t * 2.0, "saddle": True, "rider": "rostam", "wind": 1.0,
              "rider_pose": {"lean": 12, "hand_kind": "oxmace", "hand": (70, -540), "mace": -20, "head": 2, "wind": 1.2}}

        def figs(cc):
            with Cam(cc, focus, zoom)(1.0):
                horse(cc, 800, 872, 0.6, -1, PH, t)
        an.figures(c, figs, SUNSET, (0, 200, 1080, 1000))

        def rk(cc):
            with Cam(cc, focus, zoom)(1.0):
                horse(cc, rx, 880, 0.66, 1, PR, t)
        an.figures(c, rk, COLT, (0, 200, 1080, 1000), alpha=200)
        for k in range(4):
            u = (lt * 2.2 + k * 0.25) % 1.0
            S.dust(c, rx - 140 - u * 260, 864 - u * 30, 40 + u * 80, t, (236, 180, 130), 90 * (1 - u), k)
        vig(an, c, 150)

    def close():
        lt2 = lt - cut
        focus = (540, 600)
        zoom = 1.04 + 0.06 * ease(lt2 / (dur - cut))
        cam = Cam(c, focus, zoom)
        battle_plain(an, c, t, cam, "bp133")
        rescue0 = L[2][0] + 2.2
        with cam(0.8):
            draw_band(c, band, 600, 552, (80, 30, 32), 1.0)
        lift = sstep(cut + 0.05, cut + 1.3, lt)
        brk = L[2][0] + 0.3
        fall = clamp((lt - brk) / 0.65)
        landed = lt >= brk + 0.65
        rr = 34 * math.sin(clamp((lt - brk - 0.3) / 1.7) * math.pi) if brk + 0.3 < lt < brk + 2.0 else 0.0
        hand = (mix(170, 80, lift), mix(-360, -560, lift))
        PR = {"gait": "rear", "rear": rr} if rr > 1 else {"gait": "stand", "neck": 10 * math.sin(t * 2.2), "head": 5 * math.sin(t * 1.5)}
        PR.update(saddle=True, rider="rostam", wind=0.9,
                  rider_pose={"hand": hand, "hand_kind": "fist", "rprop": "oxmace", "rhand": (40, -300), "mace": 40,
                              "head": -7 * lift, "lean": -5 * lift, "wind": 1.0})
        run = clamp((lt - cut) / 2.4)
        ax = mix(700, 1450, run * run)
        kick = 1.0 - 0.6 * fall
        PA = {"mode": "walk", "phase": t * 5.0, "stride": 26 * kick, "hand": (120 + 30 * math.sin(t * 7), -470 + 40 * math.sin(t * 6)),
              "hand_kind": "open", "rhand": (-90 + 20 * math.sin(t * 8), -450), "rhand_kind": "open",
              "head": -12 + 6 * math.sin(t * 5), "wind": 1.0}
        riders = clamp((lt - rescue0) / 1.4)
        leave = clamp((lt - rescue0 - 1.9) / 2.0)

        def figs(cc):
            with Cam(cc, focus, zoom)(1.0):
                if run < 1:
                    horse(cc, ax, 872, 0.62, 1, {"gait": "gallop", "phase": t * 2.1, "saddle": True}, t)
                if lt > rescue0:
                    for i in range(3):
                        if leave <= 0:
                            x = mix(1400 + i * 160, 760 + i * 120, ease(riders))
                            horse(cc, x, 870 - i * 8, 0.5 - i * 0.03, -1,
                                  {"gait": "gallop" if riders < 1 else "stand", "phase": t * 2.0 + i * 0.4, "saddle": True,
                                   "rider": "warrior_tu", "rider_pose": {"hand": (120, -300), "lean": 8 if riders < 1 else 0}}, t)
                        else:
                            x = mix(760 + i * 120, 1500 + i * 120, leave * leave)
                            horse(cc, x, 870 - i * 8, 0.5 - i * 0.03, 1,
                                  {"gait": "gallop", "phase": t * 2.0 + i * 0.4, "saddle": True,
                                   "rider": "warrior_tu", "rider_pose": {"hand": (120, -300), "lean": 10}}, t)
        an.figures(c, figs, SUNSET, (0, 150, 1080, 1000))

        def rk(cc):
            with Cam(cc, focus, zoom)(1.0):
                tag("r:")
                horse(cc, 380, 880, 0.64, 1, PR, t)
                tag("")
            p = A("r:hand")
            if p is None:
                return
            hx, hy = world(p, focus, zoom)
            with Cam(cc, focus, zoom)(1.0):
                if lt < brk:
                    held(cc, hx + 6, hy + 8, 0.56, -22 + 8 * math.sin(t * 3), -1, PA, t, "afrasiab")
                elif not landed:
                    u = fall
                    x = mix(hx, 650, u)
                    y = mix(hy + 8, 860, u * u)
                    held(cc, x, y, 0.56, mix(-22, 70, u), -1, PA, t, "afrasiab")
                elif lt < rescue0 + 1.6:
                    person(cc, 650, 884, 0.56, -1, {"mode": "lie", "head": 6, "hand": (90, -300), "rhand": (-40, -270)}, t, "afrasiab")
                if lt >= brk:          # the torn belt still in Rostam's fist
                    cc.save()
                    cc.translate(hx, hy)
                    cc.rotate(20 * math.sin(t * 4))
                    fillp(cc, spath([(-4, 0), (6, 4), (10, 30), (4, 60), (-2, 62), (2, 30)]))
                    cc.restore()
        an.figures(c, rk, COLT, (0, 100, 1080, 1000), alpha=200, anchors=True)
        if lt > brk + 0.6:
            u = clamp((lt - brk - 0.6) / 1.6)
            for k in range(5):
                S.dust(c, 600 + k * 70, 880 - 30 * u, 50 + 120 * u, t, (236, 196, 150), 150 * (1 - u), k + 3)
        if lt > rescue0 + 0.8:
            u = clamp((lt - rescue0 - 0.8) / 2.6)
            a = math.sin(u * math.pi)
            for k in range(6):
                S.dust(c, 640 + k * 90, 860 - 40 * u, 90 + 120 * u, t, (230, 180, 136), 200 * a, k + 11)
        vig(an, c, 150)

    dissolve(c, lt, cut, 0.4, wide, close)


def p13_s04(an, c, t):
    """Afrasiab alone by the fire: 'he threw me in the dust like a child... I have never forgotten'; in the smoke,
    the vision of Sohrab riding with his army; 'Call Hooman and Barman!'"""
    lt, dur = loc(an, "S04", t)
    L = [LN("p13", "S04", k) for k in range(4)]
    down = sstep(L[0][0] + 1.4, L[0][0] + 2.2, lt) * (1 - sstep(L[0][1], L[0][1] + 0.6, lt))
    grip = sstep(L[1][0] + 0.6, L[1][0] + 1.2, lt) * (1 - sstep(L[1][1] + 0.6, L[1][1] + 1.2, lt))
    look = sstep(L[2][0] + 0.2, L[2][0] + 1.2, lt) * (1 - sstep(L[3][0] - 0.3, L[3][0] + 0.2, lt))
    call = sstep(L[3][0] - 0.1, L[3][0] + 0.4, lt)
    fire = 1.0 + 0.5 * grip + 0.4 * look
    if call > 0.01:
        h, hk = (mix(110, 70, call), mix(-330, -570, call)), "open"
    elif grip > 0.01:
        h, hk = (mix(110, 130, grip), mix(-330, -440, grip)), "fist"
    else:
        h, hk = (mix(110, 200, down), mix(-330, -260, down)), "open"
    PA = {"jaw": jaw(an, "AFRASIAB", t, 7), "hand": h, "hand_kind": hk, "rhand": (-30, -262),
          "head": 8 - 4 * down - 6 * grip + 4 * look - 12 * call + 1.2 * math.sin(t * 0.5),
          "lean": 2 + 5 * grip + 3 * look - 6 * call}

    def vision(cam):
        def draw(cv):
            u = clamp((lt - L[2][0]) / (L[2][1] - L[2][0] + 1.0))
            for i in range(4):
                horse(cv, 60 + 90 * u - i * 70, 760 + (i % 2) * 10, 0.16, 1,
                      {"gait": "gallop", "phase": t * 1.9 + i * 0.4, "saddle": True, "rider": "warrior_tu",
                       "rider_pose": {"hand_kind": "spear", "hand": (110, -340), "lean": 8}}, t)
            horse(cv, 300 + 90 * u, 800, 0.42, 1, {"gait": "gallop", "phase": t * 1.8, "saddle": True, "rider": "sohrab",
                                                  "rider_scale": 0.92, "wind": 1.0,
                                                  "rider_pose": {"hand_kind": "spear", "hand": (120, -360), "lean": 10, "wind": 1.0}}, t)
        smoke_vision(c, cam, 0.55 * look, draw, (255, 160, 130))
    afr_close(an, c, t, PA, 1.0 + 0.08 * ease(lt / dur), fire, vision, key="ac134")


def p13_s05(an, c, t):
    """Hooman and Barman come in and kneel: 'We are here, my king.' -- 'You have heard of this boy, Sohrab?' --
    'They say no man can stand against him.' Then, close: 'Choose twelve thousand...' -- 'To fight him?' -- 'No. To
    help him.'"""
    lt, dur = loc(an, "S05", t)
    L = [LN("p13", "S05", k) for k in range(7)]

    def wide():
        zoom = 1.0 + 0.06 * ease(lt / (L[4][0] + 0.4))
        walk = clamp((lt - 0.2) / 3.4)
        hx, bx = mix(-190, 150, ease(walk)), mix(-360, 368, ease(walk))
        kn = L[1][0] - 0.5 < lt < L[3][0] - 0.1
        kb = L[1][0] - 0.4 < lt < L[3][0] - 0.3
        ask = sstep(L[2][0], L[2][0] + 0.6, lt) * (1 - sstep(L[2][1] + 0.2, L[2][1] + 0.7, lt))
        bsp = sstep(L[3][0] + 0.1, L[3][0] + 0.7, lt) * (1 - sstep(L[3][1], L[3][1] + 0.5, lt))
        moving = 0 < walk < 1
        PH = {"mode": "kneel" if kn else ("walk" if moving else "stand"), "phase": lt * 4.0, "stride": 16,
              "jaw": jaw(an, "HOOMAN", t, 8), "rprop": "mace", "rhand": (-24, -300), "mace": -6,
              "hand": (90, -280) if kn else (40, -262), "hand_kind": "open" if kn else "fist",
              "head": 12 if kn else 2 + 1.2 * math.sin(t * 0.7), "lean": 14 if kn else 3 * moving}
        PB = {"mode": "kneel" if kb else ("walk" if moving else "stand"), "phase": lt * 4.0 + 1.3, "stride": 16,
              "jaw": jaw(an, "BARMAN", t, 8), "hand_kind": "spear",
              "hand": (90, -300) if kb else (mix(60, 110, bsp), mix(-330, -380, bsp)),
              "head": 12 if kb else 2 - 3 * bsp + 1.2 * math.sin(t * 0.6), "lean": 14 if kb else 3 * moving + 3 * bsp}
        PA = {"jaw": jaw(an, "AFRASIAB", t, 7), "hand": (mix(110, 160, ask), mix(-330, -380, ask)), "hand_kind": "open",
              "rhand": (-30, -262), "head": 4 + 3 * ask + 1.2 * math.sin(t * 0.5), "lean": 3 * ask}

        def extra(cc):
            person(cc, hx, 900, 0.92, 1, PH, t, HOOMAN)
            person(cc, bx, 900, 0.86, 1, PB, t, BARMAN)
        hall_wide(an, c, t, PA, extra, zoom, bx=560)

    def afr():
        order = sstep(L[4][0] + 0.2, L[4][0] + 0.8, lt) * (1 - sstep(L[4][1], L[4][1] + 0.5, lt))
        no = sstep(L[6][0], L[6][0] + 0.5, lt)
        sly = sstep(L[6][0] + 0.8, L[6][1] + 0.2, lt)
        if no > 0.01:
            h = (mix(110, 150, no), mix(-330, -360, no) - 20 * sly)
        else:
            h = (mix(110, 170, order), mix(-330, -420, order))
        PA = {"jaw": jaw(an, "AFRASIAB", t, 7), "hand": h, "hand_kind": "open", "rhand": (-30, -262),
              "head": 3 - 4 * order + 6 * sly + 1.2 * math.sin(t * 0.5), "lean": 4 * order + 5 * sly}
        afr_close(an, c, t, PA, 1.03 + 0.05 * ease((lt - L[4][0]) / 4.0), 1.0, key="ac135")

    def hb():
        ask = sstep(L[5][0] - 0.1, L[5][0] + 0.4, lt)
        PH = {"rprop": "mace", "rhand": (-24, -300), "mace": -6, "hand": (40, -262), "head": 2 + 1.2 * math.sin(t * 0.7),
              "wind": 0.2}
        PB = {"jaw": jaw(an, "BARMAN", t, 8), "hand_kind": "spear", "hand": (mix(60, 120, ask), mix(-330, -360, ask)),
              "head": 2 - 4 * ask + 1.2 * math.sin(t * 0.6), "lean": 4 * ask, "wind": 0.2}
        hb_two(an, c, t, PH, PB, 1.02 + 0.04 * ease((lt - L[5][0]) / 2.0), key="hb135")

    cuts(c, lt, [(0.0, wide), (L[4][0] - 0.3, afr), (L[5][0] - 0.25, hb), (L[6][0] - 0.25, afr)])


def p13_s06(an, c, t):
    """Shot / reverse: 'Let him fight Kavus... and Rostam.' -- 'The son against his own father?' -- 'Whoever dies,
    Turan wins.' -- 'What if this boy becomes too strong?' -- 'Leave that to me.'"""
    lt, dur = loc(an, "S06", t)
    L = [LN("p13", "S06", k) for k in range(5)]

    def afr():
        sweep = sstep(L[0][0] + 0.3, L[0][0] + 1.0, lt) * (1 - sstep(L[0][1] - 0.6, L[0][1], lt))
        grip = sstep(L[2][0] + 1.0, L[2][0] + 1.6, lt) * (1 - sstep(L[3][0], L[3][0] + 0.4, lt))
        yes = sstep(L[2][0], L[2][0] + 0.4, lt) * (1 - sstep(L[2][0] + 1.0, L[2][0] + 1.4, lt))
        back = sstep(L[4][0], L[4][0] + 0.7, lt)
        if back > 0.01:
            h, hk = (mix(110, 40, back), mix(-330, -372, back)), "open"
        elif grip > 0.01:
            h, hk = (mix(110, 140, grip), mix(-330, -430, grip)), "fist"
        else:
            h, hk = (mix(110, 190, sweep), mix(-330, -380, sweep)), "open"
        PA = {"jaw": jaw(an, "AFRASIAB", t, 7), "hand": h, "hand_kind": hk, "rhand": (-30, -262),
              "head": 3 - 3 * sweep - 5 * grip + 5 * yes - 6 * back + 1.2 * math.sin(t * 0.5),
              "lean": 4 * sweep + 6 * grip - 7 * back}
        fire = 1.0 + 0.7 * grip
        afr_close(an, c, t, PA, 1.02 + 0.07 * ease(lt / dur), fire, key="ac136")

    def hb():
        q1 = sstep(L[1][0] + 0.2, L[1][0] + 0.8, lt) * (1 - sstep(L[1][1], L[1][1] + 0.5, lt))
        q2 = sstep(L[3][0] + 0.2, L[3][0] + 0.8, lt) * (1 - sstep(L[3][1], L[3][1] + 0.5, lt))
        q = max(q1, q2)
        PH = {"jaw": jaw(an, "HOOMAN", t, 8), "rprop": "mace", "rhand": (-24, -300), "mace": -6,
              "hand": (mix(40, 160, q), mix(-262, -390, q)), "hand_kind": "open" if q > 0.3 else "fist",
              "head": 2 - 4 * q + 1.2 * math.sin(t * 0.7), "lean": 4 * q2, "wind": 0.2}
        PB = {"hand_kind": "spear", "hand": (60, -330), "head": 4 + 1.2 * math.sin(t * 0.6), "wind": 0.2}
        hb_two(an, c, t, PH, PB, 1.02 + 0.06 * ease(lt / dur), key="hb136")

    cuts(c, lt, [(0.0, afr), (L[1][0] - 0.25, hb), (L[2][0] - 0.25, afr), (L[3][0] - 0.25, hb), (L[4][0] - 0.25, afr)])


def treasury(an, c, t, lt, zoom, focus=(540, 660)):
    """The treasury: three chests opening with gold light, a throne, a crown glowing on its stand; servants lead
    horses past the arch."""
    cam = Cam(c, focus, zoom)
    with cam(0.6):
        hall(an, c, t)
        for k, x in enumerate((260, 540, 820)):
            S.hanging_lamp(c, x, 300, 1.0, t, 160, k)
    with cam(0.9):
        ground(c, 900, (64, 32, 18), (10, 5, 6))
        S.glow(c, 540, 900, 520, (255, 170, 80), 50)
    lids = [sstep(0.6 + 0.8 * k, 1.5 + 0.8 * k, lt) for k in range(3)]
    xs = (330, 520, 710)

    def figs(cc):
        with Cam(cc, focus, zoom)(0.75):
            for i in range(2):
                x = -260 + 70 * lt + i * 330
                horse(cc, x, 790, 0.34, 1, {"gait": "walk", "phase": t * 0.9 + i * 0.4, "saddle": True}, t)
                person(cc, x + 0.34 * 330, 790, 0.38, 1, {"mode": "walk", "phase": t * 3.6 + i, "hand": (100, -300)}, t, "noble")
        with Cam(cc, focus, zoom)(1.0):
            throne(cc, 900, 900, 0.72, -1)
            for k, x in enumerate(xs):
                chest(cc, x, 900, 1.0, lids[k])
            fillp(cc, spath([(110, 900, 0), (122, 824), (140, 808), (160, 808), (178, 824), (190, 900, 0)]))
            fillp(cc, ppath([(104, 812), (196, 812), (190, 798), (110, 798)]))
    an.figures(c, figs, GOLD, (0, 300, 1080, 1000), alpha=160)
    with cam(1.0):
        for k, x in enumerate(xs):
            if lids[k] > 0.02:
                S.glow(c, x, 830, 230, (255, 200, 90), 140 * lids[k] * flick(t, k))
                S.glow(c, x, 836, 80, (255, 240, 170), 130 * lids[k])
        S.glow(c, 150, 760, 170, (255, 220, 140), 150 * flick(t, 5.0))
        crown_shape(c, 150, 768, 1.1)
    vig(an, c, 160)


def scribe_wall(an, c, t, PW, PA, zoom, grow=0.0, focus=(560, 700)):
    """A scribe writing by a candle against the lit curtain, Afrasiab standing and dictating; grow (0..1) swells
    his cast shadow on the curtain behind him."""
    cam = Cam(c, focus, zoom)
    curtain(c, t)
    if grow > 0.01:
        g = ease(grow)
        shadow_layer(c, (0, 0, W, 1700), 0.45 + 0.45 * grow, (36, 10, 8), 3.0)
        with cam(0.9):
            person(c, mix(800, 560, g), mix(1100, 1500, g), 1.35 * mix(1.0, 1.62, g), -1, PA, t, "afrasiab")
        c.restore()
    with cam(1.0):
        ground(c, 1100, (70, 30, 20), (12, 5, 4))

    def figs(cc):
        with Cam(cc, focus, zoom)(1.0):
            fillp(cc, ppath([(20, 860), (520, 860), (532, 876), (532, 1200), (20, 1200)]))     # the scribe's dais
            tag("w:")
            seated(cc, 210, 860, 1.25, 1, PW, t, "poet")
            tag("")
            fillp(cc, ppath([(372, 860), (384, 860), (430, 774), (418, 772)]))
            fillp(cc, ppath([(448, 860), (436, 860), (392, 774), (404, 772)]))
            fillp(cc, ppath([(360, 770), (450, 784), (456, 774), (366, 760)]))
            person(cc, 800, 1100, 1.35, -1, PA, t, "afrasiab")
    an.figures(c, figs, (255, 182, 104), (0, 200, 1080, 1300), alpha=170, anchors=True)
    with cam(1.0):
        pg = paint(C(250, 228, 180))
        c.drawPath(ppath([(364, 756), (408, 764), (408, 778), (362, 770)]), pg)
        c.drawPath(ppath([(408, 764), (454, 770), (452, 784), (408, 778)]), pg)
        standing_candle(c, 600, 1100, t, 0.9, 2.0)
    vig(an, c, 170)


def p13_s07(an, c, t):
    """The gifts (chests of gold, a throne, a crown) and the letter 'sweet as honey': a scribe writes while
    Afrasiab dictates; on 'Every word of it was a lie' his shadow swells on the curtain."""
    lt, dur = loc(an, "S07", t)
    L = [LN("p13", "S07", k) for k in range(5)]
    cut = L[1][0] - 0.4

    def gifts():
        treasury(an, c, t, lt, 1.0 + 0.06 * ease(lt / (cut + 0.6)))

    def letter():
        lt2 = lt - cut
        write = 1 - sstep(L[4][0] - 0.2, L[4][0] + 0.4, lt)
        look_up = sstep(L[4][0] - 0.2, L[4][0] + 0.6, lt)
        PW = {"hand_kind": "pen", "hand": (150 + 6 * math.sin(t * 5.1) * write, -262 + 4 * math.sin(t * 9.7) * write - 20 * look_up),
              "head": mix(10, -12, look_up) + 1.5 * math.sin(t * 1.3), "lean": mix(8, 0, look_up), "rhand": (-6, -262), "seed": 1.0}
        g1 = sstep(L[2][0] + 0.2, L[2][0] + 0.8, lt) * (1 - sstep(L[2][1], L[2][1] + 0.5, lt))
        g2 = sstep(L[3][0] + 0.2, L[3][0] + 0.8, lt) * (1 - sstep(L[3][1], L[3][1] + 0.5, lt))
        PA = {"jaw": jaw(an, "AFRASIAB", t, 7), "hand": (mix(mix(40, 150, g1), 110, g2), mix(mix(-262, -380, g1), -440, g2)),
              "hand_kind": "open", "rhand": (-30, -262), "head": 4 - 3 * g1 - 4 * g2 + 1.2 * math.sin(t * 0.5),
              "lean": 2 * g1 + 2 * g2, "wind": 0.3}
        grow = sstep(L[4][0] - 0.2, L[4][1] + 0.6, lt)
        scribe_wall(an, c, t, PW, PA, 1.0 + 0.06 * ease(lt2 / (dur - cut)), grow)

    dissolve(c, lt, cut, 0.5, gifts, letter)


def p13_s08(an, c, t):
    """Turn + end: 'Everyone, leave us!' -- the courtiers walk out; he calls the two commanders close: 'What I tell
    you now... no one must ever know.'"""
    lt = t - an.start["S08"]
    dur = an.end["END"] - an.start["S08"]
    L = [LN("p13", "S08", k) for k in range(3)]
    cut = L[2][0] - 0.5

    def wide():
        zoom = 1.0 + 0.05 * ease(lt / (cut + 0.5))
        shout = sstep(L[0][0] - 0.1, L[0][0] + 0.4, lt) * (1 - sstep(L[0][1] + 0.3, L[0][1] + 0.9, lt))
        beckon = sstep(L[1][0] + 1.0, L[1][0] + 1.6, lt)
        curl = 0.5 + 0.5 * math.sin(t * 6) if beckon > 0.5 else 0.0
        leave = clamp((lt - L[0][0] - 0.6) / 4.0)
        app = clamp((lt - L[1][0] - 1.6) / 2.2)
        hx, bx = mix(230, 380, ease(app)), mix(380, 545, ease(app))
        if shout > 0.01:
            h = (mix(110, 60, shout), mix(-330, -560, shout))
        else:
            h = (mix(110, 150, beckon) - 20 * curl, mix(-330, -390, beckon))
        PA = {"jaw": jaw(an, "AFRASIAB", t, 7), "hand": h, "hand_kind": "open", "rhand": (-30, -262),
              "head": 4 - 10 * shout + 3 * beckon + 1.2 * math.sin(t * 0.5), "lean": -5 * shout + 4 * beckon}
        mv = 0 < app < 1
        PH = {"mode": "walk" if mv else "stand", "phase": lt * 3.6, "stride": 14, "rprop": "mace", "rhand": (-24, -300),
              "mace": -6, "hand": (40, -262), "head": 3 + 1.2 * math.sin(t * 0.7), "lean": 3 * mv}
        PB = {"mode": "walk" if mv else "stand", "phase": lt * 3.6 + 1.1, "stride": 14, "hand_kind": "spear",
              "hand": (60, -330), "head": 3 + 1.2 * math.sin(t * 0.6), "lean": 3 * mv}

        def extra(cc):
            for i, x0 in enumerate((70, 520, 600, 680)):
                if leave < 1:
                    walking = leave > 0
                    x = x0 - 900 * leave * leave if walking else x0
                    person(cc, x, 872, 0.56, -1 if walking or i >= 1 else 1,
                           {"mode": "walk" if walking else "stand", "phase": lt * 4 + i, "stride": 14, "seed": i,
                            "hand": (40, -262), "head": 4}, t, "noble")
            person(cc, hx, 900, 0.92, 1, PH, t, HOOMAN)
            person(cc, bx, 900, 0.86, 1, PB, t, BARMAN)
        hall_wide(an, c, t, PA, extra, zoom, bx=None, throne_x=880)

    def close():
        lt2 = lt - cut
        end0 = an.start["END"] - an.start["S08"]
        zoom = 1.04 + 0.1 * ease(clamp(lt2 / (end0 - cut))) + 0.1 * ease(clamp((lt - end0) / (dur - end0)))
        whisper = sstep(L[2][0] - 0.2, L[2][0] + 0.6, lt)
        finger = sstep(L[2][0] + 0.2, L[2][0] + 0.8, lt) * (1 - sstep(L[2][1] - 1.2, L[2][1] - 0.6, lt))
        PA = {"jaw": jaw(an, "AFRASIAB", t, 6), "hand": (mix(120, 150, finger), mix(-330, -430, finger)), "hand_kind": "open",
              "rhand": (-30, -262), "head": 8 * whisper + 1.0 * math.sin(t * 0.5), "lean": 11 * whisper}
        PH = {"rprop": "mace", "rhand": (-24, -300), "mace": -6, "hand": (40, -262), "head": 6 * whisper + math.sin(t * 0.7),
              "lean": 7 * whisper, "wind": 0.2}
        PB = {"hand_kind": "spear", "hand": (60, -330), "head": 6 * whisper + math.sin(t * 0.6 + 1), "lean": 6 * whisper,
              "wind": 0.2}
        fire = mix(1.0, 0.65, sstep(L[2][0], L[2][1], lt))
        trio(an, c, t, PH, PB, PA, zoom, fire, focus=(600, 640), key="tr138")

    dissolve(c, lt, cut, 0.5, wide, close)


# ================================================================== part 14 shots
def p14_s01(an, c, t):
    """Hook + title: by the low fire Afrasiab whispers: 'The son must never know his father... and the father must
    never know his son.'"""
    lt = t - an.start["S01"]
    dur = an.end["TITLE"] - an.start["S01"]
    a0, a1 = LN("p14", "S01", 0)
    whisper = sstep(a0 - 0.6, a0 + 0.3, lt)
    apart = sstep(a0 + 0.6, a0 + 1.4, lt) * (1 - sstep(a1 + 0.4, a1 + 1.2, lt))
    PA = {"jaw": jaw(an, "AFRASIAB", t, 6), "hand": (mix(110, 160, apart), mix(-330, -400, apart)), "hand_kind": "open",
          "rhand": (mix(-30, 60, apart), mix(-262, -380, apart)), "rhand_kind": "open",
          "head": 8 * whisper + 1.0 * math.sin(t * 0.5), "lean": 11 * whisper}
    PH = {"rprop": "mace", "rhand": (-24, -300), "mace": -6, "hand": (40, -262), "head": 6 * whisper + math.sin(t * 0.7),
          "lean": 7 * whisper, "wind": 0.2}
    PB = {"hand_kind": "spear", "hand": (60, -330), "head": 6 * whisper + math.sin(t * 0.6 + 1), "lean": 6 * whisper, "wind": 0.2}
    fire = 0.7 + 0.6 * sstep(a1 - 0.3, a1 + 0.5, lt)
    trio(an, c, t, PH, PB, PA, 1.0 + 0.08 * ease(lt / dur), fire, focus=(540, 640), key="tr141")


def ghosts_apart(c, t, u, a):
    """Rostam and Sohrab as pale shadows in the smoke, face to face, drifting apart (u 0..1)."""
    def draw(cv):
        person(cv, 150 - 60 * u, 900, 0.5, 1, {"hand_kind": "oxmace", "hand": (110, -330), "mace": 10, "head": -2,
                                               "stance": (54, 46), "wind": 0.6}, t, "rostam")
        person(cv, 400 + 60 * u, 900, 0.46, -1, {"hand_kind": "spear", "hand": (100, -330), "head": -2,
                                                 "stance": (52, 44), "wind": 0.6}, t, "sohrab")
    return draw


def p14_s02(an, c, t):
    """By the fire, the secret order: 'Keep them apart. They must never find out that they are father and son.' --
    'Why, my king?' -- 'A son's heart always goes to his father.'"""
    lt, dur = loc(an, "S02", t)
    L = [LN("p14", "S02", k) for k in range(6)]

    def wide():
        zoom = 1.0 + 0.05 * ease(lt / (L[1][0] + 0.4))
        PA = {"hand": (110, -330), "hand_kind": "open", "rhand": (-30, -262), "head": 4 + 1.2 * math.sin(t * 0.5)}
        PH = {"rprop": "mace", "rhand": (-24, -300), "mace": -6, "hand": (40, -262), "head": 3 + 1.2 * math.sin(t * 0.7)}
        PB = {"hand_kind": "spear", "hand": (60, -330), "head": 3 + 1.2 * math.sin(t * 0.6)}

        def extra(cc):
            person(cc, 200, 900, 0.92, 1, PH, t, HOOMAN)
            person(cc, 370, 900, 0.86, 1, PB, t, BARMAN)
        hall_wide(an, c, t, PA, extra, zoom, bx=560)

    def trio_shot():
        lean = sstep(L[1][0], L[1][1], lt)
        PA = {"jaw": jaw(an, "AFRASIAB", t, 6), "hand": (110, -330), "hand_kind": "open", "rhand": (-30, -262),
              "head": 6 * lean + math.sin(t * 0.5), "lean": 9 * lean}
        PH = {"rprop": "mace", "rhand": (-24, -300), "mace": -6, "hand": (40, -262), "head": 5 * lean + math.sin(t * 0.7),
              "lean": 6 * lean}
        PB = {"hand_kind": "spear", "hand": (60, -330), "head": 5 * lean + math.sin(t * 0.6), "lean": 5 * lean}
        trio(an, c, t, PH, PB, PA, 1.0 + 0.06 * ease((lt - L[1][0]) / 4.0), 0.85, focus=(600, 640), key="tr142")

    def afr():
        point = sstep(L[2][0] + 0.2, L[2][0] + 0.8, lt) * (1 - sstep(L[2][1], L[2][1] + 0.4, lt))
        apart = sstep(L[3][0] + 0.3, L[3][0] + 1.2, lt) * (1 - sstep(L[3][1], L[3][1] + 0.6, lt))
        heart = sstep(L[5][0] + 0.3, L[5][0] + 0.9, lt) * (1 - sstep(L[5][1] - 1.6, L[5][1] - 1.0, lt))
        cutoff = sstep(L[5][1] - 1.4, L[5][1] - 0.8, lt)
        if heart > 0.01:
            h, rh = (mix(110, 40, heart), mix(-330, -372, heart)), (-30, -262)
        elif cutoff > 0.01:
            h, rh = (mix(110, 190, cutoff), mix(-330, -340, cutoff)), (-30, -262)
        else:
            h = (mix(mix(110, 170, point), 170, apart), mix(mix(-330, -420, point), -380, apart))
            rh = (mix(-30, 70, apart), mix(-262, -370, apart))
        PA = {"jaw": jaw(an, "AFRASIAB", t, 6), "hand": h, "hand_kind": "open", "rhand": rh, "rhand_kind": "open",
              "head": 4 - 3 * point + 3 * heart + 1.2 * math.sin(t * 0.5), "lean": 5 * point + 4 * apart + 3 * heart}
        va = sstep(L[3][0] + 0.2, L[3][0] + 1.0, lt) * (1 - sstep(L[3][1] + 0.2, L[3][1] + 1.0, lt))
        u = clamp((lt - L[3][0] - 0.6) / (L[3][1] - L[3][0]))

        def vision(cam):
            smoke_vision(c, cam, 0.6 * va, ghosts_apart(c, t, u, va), (255, 190, 150))
        afr_close(an, c, t, PA, 1.02 + 0.07 * ease((lt - L[2][0]) / (dur - L[2][0])), 0.9, vision, key="ac142")

    def hb():
        q = sstep(L[4][0] - 0.1, L[4][0] + 0.4, lt)
        PH = {"jaw": jaw(an, "HOOMAN", t, 8), "rprop": "mace", "rhand": (-24, -300), "mace": -6,
              "hand": (mix(40, 150, q), mix(-262, -380, q)), "hand_kind": "open", "head": 2 - 4 * q + math.sin(t * 0.7),
              "lean": 3 * q, "wind": 0.2}
        PB = {"hand_kind": "spear", "hand": (60, -330), "head": 4 + math.sin(t * 0.6), "wind": 0.2}
        hb_two(an, c, t, PH, PB, 1.03, 0.9, key="hb142")

    cuts(c, lt, [(0.0, wide), (L[1][0] - 0.3, trio_shot), (L[2][0] - 0.3, afr), (L[4][0] - 0.25, hb), (L[5][0] - 0.25, afr)])


def p14_s03(an, c, t):
    """'Perhaps the old lion will die by the young lion's hand.' -- 'And then? What about Sohrab?' -- 'Then one night,
    while he sleeps... make sure he never wakes up. Without Rostam, Iran will be ours.' -- 'It will be done.'"""
    lt, dur = loc(an, "S03", t)
    L = [LN("p14", "S03", k) for k in range(6)]

    def afr():
        hold = sstep(L[2][0] + 0.2, L[2][0] + 1.0, lt) * (1 - sstep(L[3][1], L[3][1] + 0.4, lt))
        grip = sstep(L[3][0] + 0.4, L[3][0] + 1.2, lt) * (1 - sstep(L[4][0] + 0.6, L[4][0] + 1.2, lt))
        back = sstep(L[4][0] + 0.6, L[4][0] + 1.4, lt)
        let = sstep(L[0][0] + 0.2, L[0][0] + 0.8, lt) * (1 - sstep(L[0][1], L[0][1] + 0.5, lt))
        if back > 0.01:
            h, hk = (mix(130, 150, back), mix(-400, -330, back)), "open"
        elif hold > 0.01:
            h, hk = (mix(110, 200, hold), mix(-330, -400, hold)), ("fist" if grip > 0.4 else "open")
        else:
            h, hk = (mix(110, 170, let), mix(-330, -360, let)), "open"
        PA = {"jaw": jaw(an, "AFRASIAB", t, 6), "hand": h, "hand_kind": hk, "rhand": (-30, -262),
              "head": 5 + 5 * hold - 4 * back + 1.2 * math.sin(t * 0.5), "lean": 4 * let + 8 * hold - 6 * back}
        fire = mix(1.0, 0.45, sstep(L[2][0], L[2][1], lt)) + 1.1 * sstep(L[3][0] + 0.6, L[3][0] + 1.0, lt) * (1 - sstep(L[4][1], L[4][1] + 1.0, lt))
        va = sstep(L[0][0] + 0.2, L[0][0] + 1.0, lt) * (1 - sstep(L[0][1] - 0.2, L[0][1] + 0.6, lt))
        u = clamp((lt - L[0][0] - 0.5) / (L[0][1] - L[0][0]))

        def vision(cam):
            def draw(cv):
                hit = sstep(0.45, 0.6, u)
                cv.save()
                if hit > 0:
                    cv.translate(140, 900)
                    cv.rotate(-70 * ease(clamp((u - 0.55) / 0.4)))
                    cv.translate(-140, -900)
                person(cv, 140, 900, 0.5, 1, {"hand_kind": "oxmace", "hand": (mix(70, 120, hit), mix(-540, -330, hit)), "mace": -10,
                                             "head": -2 + 10 * hit, "stance": (54, 46), "wind": 0.6}, t, "rostam")
                cv.restore()
                person(cv, 420 - 60 * sstep(0.3, 0.5, u), 900, 0.46, -1,
                       {"hand_kind": "spear", "hand": (mix(100, 170, sstep(0.35, 0.5, u)), mix(-330, -380, sstep(0.35, 0.5, u))),
                        "head": -2, "lean": 8 * sstep(0.35, 0.5, u), "stance": (60, 48), "wind": 0.6}, t, "sohrab")
            smoke_vision(c, cam, 0.6 * va, draw, (255, 170, 140))
        afr_close(an, c, t, PA, 1.03 + 0.09 * ease(lt / dur), fire, vision, key="ac143")

    def hb():
        q = sstep(L[1][0] - 0.1, L[1][0] + 0.4, lt) * (1 - sstep(L[1][1] + 0.2, L[1][1] + 0.7, lt))
        bow = sstep(L[5][0] + 0.2, L[5][0] + 1.0, lt)
        PH = {"jaw": jaw(an, "HOOMAN", t, 8), "rprop": "mace", "rhand": (-24, -300), "mace": -6,
              "hand": (mix(40, 30, bow), mix(-262, -372, bow)), "hand_kind": "open" if bow > 0.3 else "fist",
              "head": 2 + 12 * bow + math.sin(t * 0.7), "lean": 9 * bow, "wind": 0.2}
        PB = {"jaw": jaw(an, "BARMAN", t, 8), "hand_kind": "spear", "hand": (mix(60, 120, q), mix(-330, -360, q)),
              "head": 2 - 4 * q + 10 * bow + math.sin(t * 0.6), "lean": 4 * q + 7 * bow, "wind": 0.2}
        hb_two(an, c, t, PH, PB, 1.02 + 0.04 * ease(lt / dur), 0.8, key="hb143")

    cuts(c, lt, [(0.0, afr), (L[1][0] - 0.25, hb), (L[2][0] - 0.25, afr), (L[5][0] - 0.25, hb)])


def camp_far_host(an, c, t, cam, key, x, a):
    """camp() (p11) with a far host of riders and banners on the horizon, behind the tents."""
    S.lin(c, 0, 880, [(0, (84, 112, 162)), (0.5, (196, 184, 172)), (0.84, (248, 212, 158)), (1, (252, 224, 172))])
    with cam(0.2):
        S.sun(c, 250, 520, 56, (255, 248, 222), (255, 214, 150), 520, 150)
        get(an, key + "cl", lambda: S.Clouds([(250, 14), (330, 10), (420, 16)], 131, 300, 600)).draw(c, t, (160, 130, 150), 140)
    rg = get(an, key + "rg", lambda: (S.make_ridge(-600, 1700, 770, 50, 132, 8, 4, 0.4), S.make_ridge(-600, 1700, 816, 20, 133)))
    with cam(0.4):
        S.ridge(c, rg[0], (150, 130, 150))
        if a > 0.01:
            band = get(an, key + "band", lambda: army_band(False, 45))
            c.save()
            c.translate(x, 640)
            c.scale(0.4, 0.4)
            draw_band(c, band, 0, 0, (96, 70, 84), a)
            c.restore()
            for k in range(4):
                S.dust(c, x + 60 + k * 150, 756, 80, t, (244, 220, 180), 110 * a, k)
        S.lin(c, 740, 820, [(0, (250, 220, 170, 0)), (1, (250, 220, 170, 120))], (-600, 740, 1700, 820))
    with cam(0.55):
        S.ridge(c, rg[1], (110, 90, 96))
    with cam(0.8):
        ground(c, 866, (150, 116, 80), (36, 26, 18))
        for (tx, s_) in ((60, 0.7), (300, 0.9), (560, 0.62), (800, 0.85), (1040, 0.7)):
            S.tent(c, tx, 866, s_, t + tx, INK)


def dawn_march(an, c, t, lt, cam, key):
    """The Turanian army leaving at dawn: golden sky, far hills, the host moving to the right."""
    S.lin(c, 0, 880, [(0, (46, 54, 104)), (0.45, (190, 140, 160)), (0.8, (252, 196, 150)), (1, (255, 222, 172))])
    with cam(0.15):
        S.sun(c, 860, 800, 70, (255, 246, 214), (255, 190, 130), 560, 150)
        get(an, key + "cl", lambda: S.Clouds([(300, 12), (380, 9), (460, 14)], 181, 300, 600)).draw(c, t, (170, 110, 140), 150)
    rg = get(an, key + "rg", lambda: (S.make_ridge(-600, 1700, 760, 60, 182, 8, 4, 0.4), S.make_ridge(-600, 1700, 812, 22, 183)))
    with cam(0.35):
        S.ridge(c, rg[0], (150, 116, 140))
        S.lin(c, 720, 812, [(0, (252, 210, 170, 0)), (1, (252, 210, 170, 130))], (-600, 720, 1700, 812))
    with cam(0.5):
        S.ridge(c, rg[1], (110, 80, 96))
    band = get(an, key + "band", lambda: army_band(False, 44, 2400, 300))
    with cam(0.7):
        draw_band(c, band, -1500 + 26 * lt, 548, (80, 52, 64), 1.0)
        S.lin(c, 830, 870, [(0, (230, 180, 140, 0)), (1, (120, 80, 70, 200))], (-600, 830, 1700, 870))
    with cam(0.85):
        ground(c, 862, (196, 150, 110), (60, 40, 30))


def pack_horse(cc, x, y, s, t, ph):
    """A horse loaded with two chests (the gifts)."""
    horse(cc, x, y, s, 1, {"gait": "walk", "phase": ph, "saddle": False}, t)
    for k, lx in enumerate((-80, 40)):
        px, py = croup(x, y, s, 1, 0.0, lx)
        chest(cc, px, py + 6 * s, 0.55 * s * 1.6, 0.0)


def p14_s04(an, c, t):
    """Dawn: Hooman and Barman lead twelve thousand riders out, with the gifts, the letter and the secret; spears and
    banners cover the plain. Close: 'Remember, Barman. Not a word to the boy.' -- 'Not a word.'"""
    lt, dur = loc(an, "S04", t)
    L = [LN("p14", "S04", k) for k in range(5)]
    cut = L[3][0] - 0.5

    def wide():
        focus = (560, 700)
        zoom = 1.0 + 0.06 * ease(lt / (cut + 0.6))
        cam = Cam(c, focus, zoom)
        dawn_march(an, c, t, lt, cam, "dm144")
        x0 = 60 + 30 * lt

        def figs(cc):
            with Cam(cc, focus, zoom)(1.0):
                pack_horse(cc, x0 + 40, 868, 0.44, t, t * 0.9)
                pack_horse(cc, x0 - 210, 864, 0.4, t, t * 0.9 + 0.3)
                horse(cc, x0 + 300, 874, 0.5, 1, {"gait": "walk", "phase": t * 0.9 + 0.5, "saddle": True, "rider": BARMAN,
                                                  "rider_pose": {"hand_kind": "spear", "hand": (100, -330), "head": 2}}, t)
                horse(cc, x0 + 560, 880, 0.54, 1, {"gait": "walk", "phase": t * 0.9, "saddle": True, "rider": HOOMAN,
                                                   "rider_pose": {"hand_kind": "mace", "hand": (100, -300), "head": 2}}, t)
        an.figures(c, figs, DAWN, (0, 250, 1080, 1000))
        for k in range(4):
            u = ((lt * 0.8 + k * 0.25) % 1.0)
            S.dust(c, x0 - 300 + 220 * k, 860, 50 + 60 * u, t, (240, 210, 170), 70 * (1 - u), k)
        vig(an, c, 140)

    def close():
        lt2 = lt - cut
        sc = get(an, "sc144", lambda: Scroller(161))
        S.lin(c, 0, 880, [(0, (60, 70, 120)), (0.45, (200, 150, 160)), (0.8, (252, 200, 150)), (1, (255, 224, 172))])
        S.sun(c, 900, 780, 70, (255, 246, 214), (255, 190, 130), 520, 150)
        sc.draw(c, lt2, 120, [(170, 130, 150), (120, 90, 104), (60, 40, 40)])
        band = get(an, "dm144band", lambda: army_band(False, 44, 2400, 300))
        draw_band(c, band, -1300 + 40 * lt2, 556, (110, 80, 92), 0.9)
        rem = sstep(L[3][0] + 0.2, L[3][0] + 0.8, lt) * (1 - sstep(L[3][1], L[3][1] + 0.5, lt))
        nod = sstep(L[4][0], L[4][0] + 0.4, lt) * (1 - sstep(L[4][1], L[4][1] + 0.4, lt))
        PH = {"gait": "walk", "phase": t * 0.9, "saddle": True, "rider": HOOMAN,
              "rider_pose": {"hand_kind": "mace", "hand": (100, -300), "rhand": (mix(-20, 40, rem), mix(-300, -420, rem)),
                             "rhand_kind": "open", "head": 2 - 4 * rem + math.sin(t * 0.7), "jaw": jaw(an, "HOOMAN", t, 8),
                             "wind": 0.6}}
        PB = {"gait": "walk", "phase": t * 0.9 + 0.5, "saddle": True, "rider": BARMAN,
              "rider_pose": {"hand_kind": "spear", "hand": (100, -330), "head": 2 + 8 * nod + math.sin(t * 0.6),
                             "jaw": jaw(an, "BARMAN", t, 8), "wind": 0.6}}

        def figs(cc):
            horse(cc, 290, 866, 0.7, 1, PB, t)
            horse(cc, 720, 880, 0.78, 1, PH, t)
        an.figures(c, figs, DAWN, (0, 200, 1080, 1000))
        vig(an, c, 140)

    dissolve(c, lt, cut, 0.5, wide, close)


def p14_s05(an, c, t):
    """Sohrab's camp: a lookout sees Turanian banners; Sohrab: 'Let us see what they want.' Hooman rides in:
    'King Afrasiab sends you friends... and gifts.' -- 'Then you are welcome in my camp.'"""
    lt, dur = loc(an, "S05", t)
    L = [LN("p14", "S05", k) for k in range(4)]
    cut = L[2][0] - 0.6

    def lookout():
        focus = (620, 700)
        zoom = 1.0 + 0.06 * ease(lt / (cut + 0.6))
        cam = Cam(c, focus, zoom)
        camp_far_host(an, c, t, cam, "cf145", 660 - 18 * lt, sstep(0.0, 1.2, lt))
        point = sstep(L[0][0] - 0.2, L[0][0] + 0.4, lt)
        walk = clamp((lt - L[1][0] + 1.4) / 2.0)
        sx = mix(-120, 430, ease(walk))
        look = sstep(L[1][0], L[1][0] + 0.6, lt)
        PG = {"jaw": jaw(an, "GUARD", t, 9), "hand": (mix(40, 190, point), mix(-262, -440, point)), "hand_kind": "open",
              "rprop": "spear", "rhand": (-10, -300), "head": -3 * point + math.sin(t * 0.7), "lean": 4 * point}
        PS = {"mode": "walk" if 0 < walk < 1 else "stand", "phase": lt * 4.0, "stride": 18, "jaw": jaw(an, "SOHRAB", t, 8),
              "hand_kind": "spear", "hand": (100, -330), "head": -3 * look + math.sin(t * 0.8), "lean": 3 * (0 < walk < 1), "wind": 0.6}

        def figs(cc):
            with Cam(cc, focus, zoom)(1.0):
                person(cc, 800, 872, 0.9, 1, PG, t, "guard")
                person(cc, sx, 872, 0.86, 1, PS, t, "sohrab")
        an.figures(c, figs, DAY, (0, 200, 1080, 1000))
        vig(an, c, 140)

    def meet():
        lt2 = lt - cut
        focus = (560, 700)
        zoom = 1.0 + 0.06 * ease(lt2 / (dur - cut))
        cam = Cam(c, focus, zoom)
        camp(an, c, t, cam, "cp145")
        ride = clamp(lt2 / 2.6)
        hx = mix(1350, 770, ease(ride))
        bxr = mix(1600, 1000, ease(ride))
        greet = sstep(L[2][0] + 0.2, L[2][0] + 0.8, lt) * (1 - sstep(L[2][1] + 0.4, L[2][1] + 1.0, lt))
        welcome = sstep(L[3][0] + 0.2, L[3][0] + 1.0, lt)
        PH = {"gait": "walk" if ride < 1 else "stand", "phase": t * 0.9, "saddle": True, "rider": HOOMAN,
              "neck": 6 * math.sin(t * 1.1), "head": 3 * math.sin(t * 1.3),
              "rider_pose": {"hand_kind": "open", "hand": (mix(100, 130, greet), mix(-300, -520, greet)), "rprop": "mace",
                             "rhand": (20, -300), "jaw": jaw(an, "HOOMAN", t, 8), "head": -2 * greet + math.sin(t * 0.7)}}
        PB = {"gait": "walk" if ride < 1 else "stand", "phase": t * 0.9 + 0.4, "saddle": True, "rider": BARMAN,
              "rider_pose": {"hand_kind": "spear", "hand": (100, -330), "head": 2 + math.sin(t * 0.6)}}
        PS = {"jaw": jaw(an, "SOHRAB", t, 8), "hand_kind": "open" if welcome > 0.3 else "fist",
              "hand": (mix(40, 170, welcome), mix(-262, -420, welcome)), "rprop": "spear", "rhand": (-10, -300),
              "head": -2 + 2 * welcome + math.sin(t * 0.8), "lean": -2 * welcome, "stance": (56, 48), "wind": 0.6}

        def figs(cc):
            with Cam(cc, focus, zoom)(1.0):
                horse(cc, bxr, 864, 0.6, -1, PB, t)
                horse(cc, hx, 874, 0.72, -1, PH, t)
                person(cc, 300, 874, 0.9, 1, PS, t, "sohrab")
        an.figures(c, figs, DAY, (0, 200, 1080, 1000))
        if ride < 1:
            for k in range(3):
                S.dust(c, hx + 160 + k * 80, 866, 50 + 30 * k, t, (240, 214, 170), 80 * (1 - ride), k)
        vig(an, c, 140)

    dissolve(c, lt, cut, 0.5, lookout, meet)


def p14_s06(an, c, t):
    """Hooman stares at Sohrab's arms and shoulders: 'This boy could lift a mountain.' -- 'Then Rostam will finally
    meet his match.'"""
    lt, dur = loc(an, "S06", t)
    L = [LN("p14", "S06", k) for k in range(3)]
    focus = (540, 680)
    zoom = 1.0 + 0.07 * ease(lt / dur)
    cam = Cam(c, focus, zoom)
    camp(an, c, t, cam, "cp146")
    stare = sstep(L[0][0] + 0.4, L[0][0] + 1.4, lt)
    whisper = sstep(L[1][0], L[1][0] + 0.5, lt)
    bturn = lt > L[2][0] - 0.2
    PH = {"jaw": jaw(an, "HOOMAN", t, 8), "rprop": "mace", "rhand": (-24, -300), "mace": -6,
          "hand": (mix(40, 70, whisper), mix(-262, -420, whisper)), "hand_kind": "open" if whisper > 0.3 else "fist",
          "head": -8 * stare * (1 - whisper) + 4 * whisper + math.sin(t * 0.7), "lean": -3 * stare * (1 - whisper) + 3 * whisper,
          "wind": 0.5}
    PB = {"jaw": jaw(an, "BARMAN", t, 8), "hand_kind": "spear", "hand": (60, -330),
          "head": (4 if bturn else -5 * stare) + math.sin(t * 0.6), "wind": 0.5}
    PS = {"rprop": "spear", "rhand": (-10, -300), "hand": (40, -262), "head": 2 + math.sin(t * 0.8),
          "stance": (60, 50), "wind": 0.7}

    def figs(cc):
        with Cam(cc, focus, zoom)(1.0):
            person(cc, 160, 1330, 1.42, 1, PH, t, HOOMAN)
            person(cc, 455, 1330, 1.3, -1 if bturn else 1, PB, t, BARMAN)
            person(cc, 840, 1450, 1.72, -1, PS, t, "sohrab")
    an.figures(c, figs, DAY, (0, 100, 1080, 1500))
    vig(an, c, 150)


def p14_s07(an, c, t):
    """The letter: 'Take the throne of Iran... Samangan, Iran and Turan will be one.' -- 'Tell your king I thank
    him!' Then: 'He did not see the trap.'"""
    lt, dur = loc(an, "S07", t)
    L = [LN("p14", "S07", k) for k in range(4)]
    focus = (600, 660)
    zoom = 1.0 + 0.06 * ease(lt / L[3][0]) + 0.08 * ease(clamp((lt - L[3][0]) / (dur - L[3][0])))
    cam = Cam(c, focus, zoom)
    camp(an, c, t, cam, "cp147")
    opened = sstep(L[0][0] - 0.8, L[0][0] - 0.1, lt) * (1 - sstep(L[2][0] - 0.4, L[2][0] + 0.3, lt))
    joy = sstep(L[2][0] + 1.6, L[2][0] + 2.2, lt) * (1 - sstep(L[2][1] + 0.2, L[2][1] + 0.8, lt))
    thank = sstep(L[2][0] + 0.1, L[2][0] + 0.6, lt) * (1 - sstep(L[2][0] + 1.4, L[2][0] + 1.8, lt))
    glance = sstep(L[3][0] + 1.0, L[3][0] + 1.8, lt)
    PH = {"jaw": jaw(an, "HOOMAN", t, 8), "hand": (mix(40, 150, opened), mix(-262, -370, opened)),
          "rhand": (mix(-24, 110, opened), mix(-300, -330, opened)), "rhand_kind": "fist", "hand_kind": "fist",
          "rprop": None if opened > 0.05 else "mace", "mace": -6,
          "head": 4 * opened + 6 * glance + math.sin(t * 0.7), "lean": 3 * opened, "wind": 0.5}
    if joy > 0.01:
        sh, shk = (mix(30, 70, joy), mix(-372, -560, joy)), "fist"
    else:
        sh, shk = (mix(40, 30, thank), mix(-262, -372, thank)), ("open" if thank > 0.3 else "fist")
    PS = {"jaw": jaw(an, "SOHRAB", t, 8), "hand": sh, "hand_kind": shk, "rprop": "spear", "rhand": (-10, -300),
          "head": 2 - 5 * joy + 3 * thank + math.sin(t * 0.8), "lean": 2 * thank - 2 * joy, "stance": (56, 48), "wind": 0.6}

    def back(cc):
        with Cam(cc, focus, zoom)(0.8):
            chest(cc, 560, 884, 0.9, 1.0)
            throne(cc, 400, 884, 0.42, 1)
    an.figures(c, back, GOLD, (0, 400, 1080, 1100), alpha=150)
    with cam(0.8):
        S.glow(c, 560, 826, 230, (255, 200, 90), 150 * flick(t, 1.0))
        S.glow(c, 560, 770, 130, (255, 226, 150), 160 * flick(t, 2.0))
        crown_shape(c, 560, 786, 0.9)

    def figs(cc):
        with Cam(cc, focus, zoom)(1.0):
            tag("h:")
            person(cc, 230, 1330, 1.42, 1, PH, t, HOOMAN)
            tag("")
            person(cc, 850, 1380, 1.62, -1, PS, t, "sohrab")
    an.figures(c, figs, DAY, (0, 100, 1080, 1500), anchors=True)
    if opened > 0.05:
        a, b = A("h:hand"), A("h:rhand")
        if a and b:
            scroll(c, (a[0] + b[0]) / 2, (a[1] + b[1]) / 2 - 8, max(40.0, abs(a[0] - b[0]) + 30) * opened, 110 * zoom, 0, opened)
    vig(an, c, 150)


def p14_s08(an, c, t):
    """Turn + end: at sunset Sohrab on his colt: 'Tomorrow, we march to the border of Iran!' -- the spears go up;
    in front, Barman: 'He trusts us.' -- Hooman: 'Good. Let him trust us.' Then the White Fortress under the moon."""
    lt = t - an.start["S08"]
    dur = an.end["END"] - an.start["S08"]
    L = [LN("p14", "S08", k) for k in range(4)]
    c1 = L[1][0] - 0.4
    c2 = L[3][0] - 0.3

    def sunset(cam):
        S.lin(c, 0, 900, [(0, (40, 16, 46)), (0.35, (130, 40, 60)), (0.65, (226, 96, 60)), (0.85, (252, 160, 86)),
                          (1, (255, 196, 120))])
        with cam(0.2):
            S.sun(c, 330, 790, 120, (255, 230, 176), (255, 130, 70), 640, 170, 9, t)
            get(an, "cl148", lambda: S.Clouds([(260, 16), (340, 12), (430, 20)], 148)).draw(c, t, (80, 16, 40), 190)
        rg = get(an, "rg148", lambda: (S.make_ridge(-600, 1700, 790, 40, 149), S.make_ridge(-600, 1700, 830, 18, 150)))
        with cam(0.4):
            S.ridge(c, rg[0], (116, 36, 60))
        with cam(0.55):
            S.ridge(c, rg[1], (66, 18, 38))

    def army():
        focus = (600, 700)
        zoom = 1.0 + 0.06 * ease(lt / (c1 + 0.5))
        cam = Cam(c, focus, zoom)
        sunset(cam)
        cheer = sstep(L[0][1] - 0.6, L[0][1] + 0.2, lt)
        with cam(0.75):
            b0 = get(an, "army0", lambda: army_band(False))
            b1 = get(an, "army1", lambda: army_band(True))
            draw_band(c, b0, -760, 590, (40, 10, 22), 1 - cheer)
            draw_band(c, b1, -760, 590, (40, 10, 22), cheer)
            S.lin(c, 840, 900, [(0, (60, 18, 30, 0)), (1, (30, 8, 16, 255))], (-600, 840, 1700, 900))
        with cam(1.0):
            c.drawPath(spath([(-300, 2400, 0), (-300, 900), (300, 912), (620, 892), (820, 862), (1000, 858), (1400, 870),
                              (1400, 2400, 0)]), paint(C(*INK)))
        up = sstep(L[0][0], L[0][0] + 0.5, lt)
        point = sstep(L[0][0] + 1.0, L[0][0] + 1.6, lt)
        rr = 30 * math.sin(clamp((lt - L[0][1] + 0.4) / 1.6) * math.pi) if L[0][1] - 0.4 < lt < L[0][1] + 1.2 else 0.0
        rp = {"hand_kind": "spear", "hand": (mix(mix(110, 60, up), 170, point), mix(mix(-330, -540, up), -420, point)),
              "lean": 4 * point, "head": -3 * up, "wind": 1.0, "jaw": jaw(an, "SOHRAB", t, 8)}
        PC = {"gait": "rear", "rear": rr} if rr > 1 else {"gait": "stand", "neck": 6 * math.sin(t * 1.9), "head": 4 * math.sin(t * 1.2)}
        PC.update({"saddle": True, "rider": "sohrab", "rider_scale": 0.92, "rider_pose": rp, "wind": 0.9})

        def figs(cc):
            with Cam(cc, focus, zoom)(1.0):
                horse(cc, 830, 862, 0.66, -1, PC, t)
        an.figures(c, figs, COLT, (0, 150, 1080, 1000), alpha=200)
        vig(an, c, 150)

    def whisper():
        lt2 = lt - c1
        focus = (560, 700)
        zoom = 1.0 + 0.05 * ease(lt2 / (c2 - c1 + 0.5))
        cam = Cam(c, focus, zoom)
        sunset(cam)
        with cam(0.5):
            b1 = get(an, "army1", lambda: army_band(True))
            draw_band(c, b1, -600, 520, (60, 16, 30), 0.9)
            c.drawPath(spath([(400, 900), (700, 800), (860, 790), (1000, 800), (1300, 860), (1300, 1000, 0), (400, 1000, 0)]),
                       paint(C(30, 8, 16)))
            horse(c, 860, 796, 0.3, -1, {"gait": "stand", "saddle": True, "rider": "sohrab", "rider_scale": 0.92,
                                         "rider_pose": {"hand_kind": "spear", "hand": (60, -540)}}, t)
        b = sstep(L[1][0] - 0.1, L[1][0] + 0.4, lt) * (1 - sstep(L[1][1] + 0.2, L[1][1] + 0.7, lt))
        h = sstep(L[2][0] - 0.1, L[2][0] + 0.4, lt)
        PB = {"jaw": jaw(an, "BARMAN", t, 8), "hand_kind": "spear", "hand": (60, -330), "head": 4 + 2 * b + math.sin(t * 0.6),
              "wind": 0.7}
        PH = {"jaw": jaw(an, "HOOMAN", t, 8), "rprop": "mace", "rhand": (-24, -300), "mace": -6, "hand": (40, -262),
              "head": 2 + 6 * h + math.sin(t * 0.7), "lean": 2 * h, "wind": 0.7}

        def figs(cc):
            with Cam(cc, focus, zoom)(1.0):
                person(cc, 200, 1330, 1.42, 1, PB, t, BARMAN)
                person(cc, 560, 1330, 1.5, -1, PH, t, HOOMAN)
        an.figures(c, figs, SUNSET, (0, 100, 1080, 1500))
        vig(an, c, 160)

    def fortress():
        lt3 = lt - c2
        focus = (600, 700)
        zoom = 1.0 + 0.12 * ease(lt3 / (dur - c2))
        cam = Cam(c, focus, zoom)
        white_fortress(an, c, t, cam, "wf148")
        vig(an, c, 160)

    dissolve(c, lt, c1, 0.5, army, lambda: dissolve(c, lt, c2, 0.8, whisper, fortress))


P13 = {"S01": p13_s01, "TITLE": p13_s01, "S02": p13_s02, "S03": p13_s03, "S04": p13_s04, "S05": p13_s05,
       "S06": p13_s06, "S07": p13_s07, "S08": p13_s08, "END": p13_s08}
SHIFT13 = {}

P14 = {"S01": p14_s01, "TITLE": p14_s01, "S02": p14_s02, "S03": p14_s03, "S04": p14_s04, "S05": p14_s05,
       "S06": p14_s06, "S07": p14_s07, "S08": p14_s08, "END": p14_s08}
SHIFT14 = {}

register(P13, SHIFT13)
