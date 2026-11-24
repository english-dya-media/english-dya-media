"""Part 18 (Gordafarid's Trick; row 9 of OUTLINE.md, second half): every shot as a shadow-play scene.

Importing this module imports p17_scenes (the riders, sets and helpers of part 17) and registers part 18's shots.
New here, to reuse: gate_outside() (the White Fortress from outside, close: the sunlit wall fills the frame, a great
arched gate whose doors open on the shaded court and slam shut), wall_low() (looking up at the battlements against
the sky: a person standing on the wall, the parapet in front), lasso_throw() (a rope flying from a hand to a waist,
its loop closing round it), people_running().
Line timings come from p18/audio/timeline.json (LN), so the action follows the voices.
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
from ep01_scenes import loc, jaw, get, vig, tag, A, ground, INK
from p05_scenes import register
from p07_scenes import LN, dissolve, DAY
from p11_scenes import COLT
from p13_scenes import cuts

GAZH, MORN = M.GAZH, M.MORN
GORD_BARE = Q.GORD_BARE
GY, SG, MOOD = Q.GY, Q.SG, Q.MOOD
gh, colt, duo, waist, loop_at, trail, her_set = Q.gh, Q.colt, Q.duo, Q.waist, Q.loop_at, Q.trail, Q.her_set


# ------------------------------------------------------------------ sets
def gate_outside(an, c, t, cam, key, gate=0.0, gx=540, mood=1.0, top=300, gy=872):
    """The White Fortress from outside, close: the sunlit wall fills the frame (merlons at top), a great arched gate at
    gx whose doors open (gate 0..1) on the shaded court inside, the road in front (ground at gy)."""
    M.sky_day(c, mood, top + 60)
    with cam(0.6):
        wall = M.STONE
        pw = skia.Paint(AntiAlias=True)
        pw.setShader(skia.GradientShader.MakeLinear([skia.Point(0, top - 80), skia.Point(0, gy + 20)],
                                                    [C(*mixc(wall, (255, 226, 190), 0.25)), C(*mixc(wall, (120, 108, 120), 0.35)),
                                                     C(*mixc(wall, (60, 50, 60), 0.55))], [0.0, 0.6, 1.0]))
        path = skia.Path()
        path.addRect(skia.Rect.MakeLTRB(-500, top, 1600, gy + 40))
        for k in range(-8, 30):
            path.addRect(skia.Rect.MakeLTRB(k * 96, top - 70, k * 96 + 58, top + 1))
        c.drawPath(path, pw)
        seam = paint(C(*mixc(wall, (90, 80, 96), 0.5), 70))
        for row in range(1, 9):
            y = top + row * 62
            c.drawRect(skia.Rect.MakeLTRB(-500, y, 1600, y + 2), seam)
        for tx in (gx - 330, gx + 330):
            tw = paint(C(*mixc(wall, (110, 100, 120), 0.3)))
            c.drawRect(skia.Rect.MakeLTRB(tx - 80, top - 150, tx + 80, gy + 40), tw)
            for k in range(3):
                c.drawRect(skia.Rect.MakeLTRB(tx - 80 + k * 60, top - 210, tx - 80 + k * 60 + 40, top - 149), tw)
            c.drawRect(skia.Rect.MakeLTRB(tx - 10, top - 60, tx + 10, top - 10), paint(C(60, 46, 56)))
        arch = S.arch_path(gx, gy, 300, 430)
        p = skia.Paint(AntiAlias=True)
        p.setShader(skia.GradientShader.MakeLinear([skia.Point(0, gy - 430), skia.Point(0, gy)],
                                                   [C(70, 56, 62), C(120, 96, 84), C(170, 140, 112)], [0.0, 0.6, 1.0]))
        c.drawPath(arch, p)
        if gate < 0.999:
            c.save()
            c.clipPath(arch, skia.ClipOp.kIntersect, True)
            w = 150 * (1 - ease(gate))
            wood = paint(C(120, 86, 62))
            c.drawRect(skia.Rect.MakeLTRB(gx - 150, gy - 440, gx - 150 + w, gy), wood)
            c.drawRect(skia.Rect.MakeLTRB(gx + 150 - w, gy - 440, gx + 150, gy), wood)
            stud = paint(C(190, 160, 120))
            plank = paint(C(76, 52, 38))
            for k in range(1, 4):
                c.drawRect(skia.Rect.MakeLTRB(gx - 150, gy - k * 110, gx - 150 + w, gy - k * 110 + 6), plank)
                c.drawRect(skia.Rect.MakeLTRB(gx + 150 - w, gy - k * 110, gx + 150, gy - k * 110 + 6), plank)
                for j in range(4):
                    if w > 30:
                        c.drawCircle(gx - 150 + w * (0.15 + 0.23 * j), gy - k * 110 + 24, 4, stud)
                        c.drawCircle(gx + 150 - w * (0.15 + 0.23 * j), gy - k * 110 + 24, 4, stud)
            c.restore()
        edge = skia.Paint(AntiAlias=True, Color=C(80, 66, 74))
        edge.setStyle(skia.Paint.kStroke_Style)
        edge.setStrokeWidth(16)
        c.drawPath(arch, edge)
    with cam(1.0):
        ground(c, gy, (206, 176, 140), (70, 52, 42))
        S.tufts(c, get(an, key + "tf", lambda: Q.tufts_list(181, 24, -300, 1400, gy + 22, 8, 18)), t, (70, 46, 34), 0.2)


def wall_low(an, c, t, cam, key, figs, top=1150, mood=1.0, sun=(560, 520)):
    """Looking up at the battlements from the foot of the wall: open sky, the sun behind the person on the wall, the
    parapet in front of their legs (merlons up to top - 82)."""
    S.lin(c, 0, top, [(0, mixc((60, 92, 156), (70, 104, 164), mood)), (0.6, (160, 178, 206)), (1, (236, 222, 196))])
    with cam(0.12):
        S.sun(c, sun[0], sun[1], 70, (255, 248, 222), (255, 214, 150), 620, 170)
        get(an, key + "cl", lambda: S.Clouds([(320, 12), (420, 9), (560, 14)], 182, 300, 700)).draw(c, t, (176, 176, 200), 150)
    an.figures(c, figs, MORN, (0, 0, 1080, 1500))
    with cam(1.0):
        M.parapet(c, top, merlon=110, gap=70, mood=mood)


def lasso_throw(cc, hand, target, u, se, tight=1.0):
    """A thrown lasso: the rope from hand flies to target (a waist) over u = 0..1, then its loop closes round it."""
    if hand is None or target is None:
        return
    if u < 1:
        p = (mix(hand[0], target[0], ease(u)), mix(hand[1], target[1], ease(u)) - 70 * math.sin(u * math.pi))
        rope(cc, hand, p, 30 * (1 - u), 2.6)
        loop_at(cc, p, 34 * se, 18 * se, 2.6)
    else:
        rope(cc, hand, (target[0], target[1]), mix(60, 6, tight), 2.8)
        loop_at(cc, target, 30 * se, 9 * se, 3.0)


def people_running(cc, lt, t, x0, x1, dur, y, s):
    """People of the fortress running to her (two women, a warrior), arriving one after the other."""
    for i, (look, dx, d0) in enumerate((("maid", 0, 0.0), ("warrior_ir", -190, 0.5), ("maid", -380, 0.9))):
        u = clamp((lt - d0) / dur)
        x = mix(x0 + dx, x1 + dx, ease(u))
        moving = 0 < u < 1
        P = {"mode": "walk" if moving else "stand", "phase": lt * 5.0 + i, "stride": 22 if moving else 0, "lean": 8 * moving,
             "hand": (mix(40, 120, 1 - moving * 0.0), -400 if not moving else -300), "hand_kind": "open",
             "rhand": (-30, -300 if moving else -480), "rhand_kind": "open", "head": -6 + 3 * math.sin(t * 2.2 + i), "seed": i}
        person(cc, x, y, s * (0.96 + 0.04 * i), 1, P, t, look)


# ================================================================== S01 + TITLE (hook)
def rope_two(an, c, t, lt, dur, key, rpG, faceG, rpS, tight, gx=330, sx=800, zoom=None, focus=(540, 660), rr=0.0,
             host_x=760, fs=0.34):
    """Medium two-shot: Gordafarid caught (the lasso round her waist), Sohrab on his colt holding the rope."""
    zoom = (1.02 + 0.06 * ease(lt / dur)) if zoom is None else zoom

    def setf(cam):
        her_set(an, c, t, cam, key, fs=fs, fx=-170, fy=600, host_x=host_x, gy=SG - 120)
    se = 0.76 * zoom

    def eg(cc):
        loop_at(cc, waist("g:", se), 30 * se, 9 * se, 3.0)

    def es(cc):
        h, w = A("s:hand"), waist("g:", se)
        if h and w:
            rope(cc, h, w, mix(70, 8, tight), 2.8)
    duo(an, c, t, focus, zoom, setf, G=(gx, SG, 0.76, faceG, gh(rpG, t, look=GORD_BARE, rear=rr, wind=1.1)),
        Sd=(sx, SG, 0.8, -1, colt(rpS, t)), eg=eg, es=es, anchors=True, box=(0, 100, 1080, 1100), sa=180)
    vig(an, c, 150)


def p18_s01(an, c, t):
    """Hook + title: the lasso round her waist. Sohrab: 'You cannot escape me, moon-face.' -- she turns back to him with
    a smile: 'Escape? Who said I want to escape?'"""
    lt = t - an.start["S01"]
    dur = an.end["TITLE"] - an.start["S01"]
    a0, a1 = LN("p18", "S01", 0)
    b0, b1 = LN("p18", "S01", 1)
    turn = lt > b0 - 0.3
    rr = 20 * math.sin(clamp((lt - b0 + 0.6) / 1.0) * math.pi) if b0 - 0.6 < lt < b0 + 0.4 else 0.0
    tug = sstep(a0, a0 + 0.5, lt)
    rpG = {"hand": (60, -330), "rhand": (30, -318), "hand_kind": "fist", "rhand_kind": "fist",
           "head": (4 * math.sin(t * 6) * (1 - tug * 0.5)) if not turn else (6 + 2 * math.sin(t * 0.8)),
           "jaw": jaw(an, "GORDAFARID", t, 7), "lean": 4 if not turn else -2, "wind": 1.2}
    rpS = {"hand": (mix(150, 100, tug), mix(-360, -330, tug)), "hand_kind": "fist", "rhand": (30, -300),
           "head": 6 + math.sin(t * 0.8), "jaw": jaw(an, "SOHRAB", t, 8), "lean": -4 * tug, "wind": 0.9}
    rope_two(an, c, t, lt, dur, "f181", rpG, 1 if turn else -1, rpS, tug, rr=rr)


# ================================================================== S02 a girl
def p18_s02(an, c, t):
    """'Gordafarid had fought Sohrab like a lion. But when her helmet came off, he saw that she was a girl.' Sohrab,
    her helmet in his hand: 'If the girls of Iran fight like this... then what are its men like?' -- 'Sohrab could not
    take his eyes off her.'"""
    lt, dur = loc(an, "S02", t)
    L = [LN("p18", "S02", k) for k in range(5)]
    c1 = L[2][0] - 0.4
    c2 = L[4][0] - 0.3

    def her():
        look = sstep(L[1][0] + 1.0, L[1][0] + 2.0, lt)
        rp = {"hand_kind": "sword", "sword": 20, "hand": (90, -330), "rhand": (-10, -300),
              "head": 2 - 8 * look + math.sin(t * 0.7), "wind": 1.2}
        Q.her_close(an, c, t, lt, c1 + 0.4, "f182", rp, 0.7 + 0.3 * sstep(0.0, 2.0, lt))

    def him():
        lt2 = lt - c1
        q = sstep(L[3][0] - 0.2, L[3][0] + 0.4, lt)
        rp = {"hand_kind": "fist", "hand": (mix(210, 190, q), mix(-590, -540, q)), "rhand": (mix(30, 90, q), mix(-300, -330, q)),
              "rhand_kind": "open" if q > 0.3 else "fist", "head": 6 - 4 * q + math.sin(t * 0.7),
              "jaw": jaw(an, "SOHRAB", t, 8), "wind": 0.9}
        Q.him_close(an, c, t, lt2, c2 - c1 + 0.4, "f182b", rp)

    def gaze():
        lt3 = lt - c2
        away = sstep(1.6, 2.6, lt3)
        rp = {"hand_kind": "sword", "sword": 20, "hand": (90, -330), "rhand": (-10, -300),
              "head": -6 + 12 * away + math.sin(t * 0.7), "wind": 1.3}
        Q.her_close(an, c, t, lt3, dur - c2, "f182c", rp, 1.0, 0.05)

    cuts(c, lt, [(0.0, her), (c1, him), (c2, gaze)], 0.4)


# ================================================================== S03 the lasso
def p18_s03(an, c, t):
    """'Gordafarid turned to flee. But Sohrab untied the lasso from his saddle... and threw it. The rope caught her
    around the waist.' -- 'Let me go!' -- 'You cannot escape me, moon-face. Why do you fight? No prey like you has ever
    come into my trap.' -- 'Gordafarid knew she was caught. Only a trick could save her now.'"""
    lt, dur = loc(an, "S03", t)
    L = [LN("p18", "S03", k) for k in range(6)]
    c1 = L[2][0] - 0.4
    c2 = L[3][0] - 0.35
    c3 = L[5][0] - 0.3
    throw0 = L[1][0] + 0.2
    caught = throw0 + 0.7

    def wide():
        focus = (540, 700)
        zoom = 1.0 + 0.05 * ease(lt / (c1 + 0.4))
        turn = lt > 0.9
        run = clamp((lt - 1.2) / 4.0)
        stop = lt > caught
        gx = 430 - 150 * run if not stop else 430 - 150 * clamp((caught - 1.2) / 4.0)
        rr = 26 * math.sin(clamp((lt - caught) / 1.3) * math.pi) if caught < lt < caught + 1.3 else 0.0
        untie = sstep(L[0][1] - 2.2, L[0][1] - 1.4, lt)
        swing = lt > L[0][1] - 1.4 and lt < throw0
        rpG = {"hand_kind": "fist", "hand": (100, -340), "rhand": (-10, -300), "head": 4 + math.sin(t * 0.8),
               "lean": 8 * (run > 0) * (not stop), "wind": 1.3}
        if stop:
            rpG.update(hand=(60, -330), rhand=(30, -318), lean=-6, head=-6 + 3 * math.sin(t * 6))
        if swing:
            rpS = {"hand_kind": "lasso", "loop": 40, "hand": (60, -560), "rhand": (30, -300), "head": -2, "wind": 1.0}
        elif lt >= throw0:
            rpS = {"hand_kind": "fist", "hand": (mix(190, 110, sstep(caught, caught + 0.6, lt)), mix(-400, -340, sstep(caught, caught + 0.6, lt))),
                   "rhand": (30, -300), "head": 4, "lean": -6 * sstep(caught, caught + 0.6, lt), "wind": 1.0}
        else:
            rpS = {"hand_kind": "fist", "hand": (mix(100, -40, untie), mix(-330, -300, untie)), "rhand": (30, -300),
                   "head": 4 + 8 * untie, "wind": 1.0}
        sx = 800 - 120 * run if not stop else 800 - 120 * clamp((caught - 1.2) / 4.0)

        def setf(cam):
            her_set(an, c, t, cam, "f183", fs=0.42, fx=-60, fy=560, host_x=720)
        se = 0.5 * zoom

        def eg(cc):
            if lt > caught:
                loop_at(cc, waist("g:", se), 30 * se, 9 * se, 2.6)

        def es(cc):
            if lt >= throw0:
                lasso_throw(cc, A("s:hand"), waist("g:", se), (lt - throw0) / (caught - throw0), se,
                            sstep(caught, caught + 0.8, lt))
        moving_g = run > 0 and not stop
        duo(an, c, t, focus, zoom, setf,
            G=(gx, GY, 0.5, -1 if turn else 1, gh(rpG, t, look=GORD_BARE, gait="gallop" if moving_g else "stand",
                                                  phase=t * 2.2, rear=rr, wind=1.2)),
            Sd=(sx, GY, 0.52, -1, colt(rpS, t, "gallop" if (run > 0 and not stop) else "stand", t * 2.1)),
            eg=eg, es=es, anchors=True)
        if moving_g:
            trail(c, gx, GY, lt, t, 1.0, 1, 0)
            trail(c, sx, GY, lt, t, 1.0, 1, 4)
        if stop:
            P16.dust_puff(c, gx, GY - 20, t, caught, lt, 0.6)
        vig(an, c, 140)

    def her_rope(look_down=0.0, shake=1.0, lt_=None, dur_=None, key="f183b"):
        lt2 = lt - (c1 if lt_ is None else lt_)
        rp = {"hand": (60, -330), "rhand": (30, -318), "hand_kind": "fist", "rhand_kind": "fist",
              "head": 6 * math.sin(t * 7) * shake + 14 * look_down + math.sin(t * 0.7), "jaw": jaw(an, "GORDAFARID", t, 8),
              "lean": 6 * shake - 4, "wind": 1.3}

        def eg(cc, zoom):
            w = waist("g:", 1.25 * zoom)
            if w:
                loop_at(cc, w, 30 * 1.25 * zoom, 9 * 1.25 * zoom, 4.0)
                rope(cc, w, (1300, w[1] - 140), 30, 4.0)
        Q.her_close(an, c, t, lt2, dur_ or (c2 - c1 + 0.4), key, rp, 0.5, 0.05, eg=eg)

    def him_rope():
        lt3 = lt - c2
        smile = sstep(L[4][0], L[4][0] + 0.6, lt)
        rp = {"hand_kind": "fist", "hand": (mix(110, 90, smile), -360), "rhand": (mix(30, 120, smile), mix(-300, -380, smile)),
              "rhand_kind": "open" if smile > 0.3 else "fist", "head": 6 - 6 * smile + math.sin(t * 0.7),
              "jaw": jaw(an, "SOHRAB", t, 8), "wind": 0.9}

        def extra(cc):
            a = A("s:hand")
            if a:
                rope(cc, a, (-120, a[1] + 200), 40, 4.0)
        Q.him_close(an, c, t, lt3, c3 - c2 + 0.4, "f183c", rp, helm=False, extra=extra)

    def her_think():
        q = sstep(c3 + 0.6, c3 + 2.4, lt) * (1 - sstep(L[5][1] - 1.4, L[5][1] - 0.4, lt))
        her_rope(q, 0.0, c3, dur - c3, "f183d")

    cuts(c, lt, [(0.0, wide), (c1, her_rope), (c2, him_rope), (c3, her_think)], 0.35)


# ================================================================== S04 the trick
def p18_s04(an, c, t):
    """She turns to him with a smile: 'Escape? Who said I want to escape? Brave hero, look around you. Two armies are
    watching us. (the fortress wall full of people, the host) If your men see you fighting a girl, they will laugh at
    you. Let us make peace quietly, just the two of us. The fortress and all its treasure will be yours. Come with me to
    the gate. It will open for you.'"""
    lt, dur = loc(an, "S04", t)
    L = [LN("p18", "S04", k) for k in range(6)]
    i0 = L[1][0] + 1.2
    i1 = L[2][0] - 0.3

    def two():
        look = sstep(L[1][0] + 0.2, L[1][0] + 0.8, lt) * (1 - sstep(i0 - 0.4, i0, lt))
        laugh = sstep(L[2][0] + 1.4, L[2][0] + 2.0, lt) * (1 - sstep(L[2][1], L[2][1] + 0.5, lt))
        heart = sstep(L[3][0], L[3][0] + 0.5, lt) * (1 - sstep(L[3][1], L[3][1] + 0.4, lt))
        point = sstep(L[4][0], L[4][0] + 0.5, lt) * (1 - sstep(L[4][1], L[4][1] + 0.4, lt))
        come = sstep(L[5][0], L[5][0] + 0.5, lt)
        beck = math.sin(t * 5) * come
        if heart > 0.01:
            hand, kind = (mix(110, 40, heart), mix(-330, -400, heart)), "open"
        elif point > 0.01:
            hand, kind = (mix(110, -160, point), mix(-330, -460, point)), "open"
        elif come > 0.01:
            hand, kind = (mix(110, 170, come) - 20 * beck, mix(-330, -420, come) + 10 * beck), "open"
        elif laugh > 0.01:
            hand, kind = (mix(110, 200, laugh), mix(-330, -470, laugh)), "open"
        else:
            hand, kind = (mix(110, 190, look), mix(-330, -480, look)), "open" if look > 0.3 else "fist"
        rpG = {"hand": hand, "hand_kind": kind, "rhand": (30, -318), "rhand_kind": "fist",
               "head": -4 + 4 * heart - 6 * look + 3 * math.sin(t * 0.8) * (1 - heart), "jaw": jaw(an, "GORDAFARID", t, 8),
               "lean": -2 + 3 * come, "wind": 1.1}
        doubt = sstep(L[2][0], L[2][0] + 0.6, lt)
        rpS = {"hand": (110, -340), "hand_kind": "fist", "rhand": (30, -300), "head": 8 - 4 * doubt + math.sin(t * 0.6),
               "lean": -2, "wind": 0.9}
        rope_two(an, c, t, lt, dur, "f184", rpG, 1, rpS, 0.2, gx=330, sx=790, focus=(540, 640))

    def armies():
        lt2 = lt - i0
        focus = (540, 720)
        zoom = 1.0 + 0.05 * ease(lt2 / (i1 - i0 + 0.3))
        cam = Cam(c, focus, zoom)
        M.plain_below(an, c, t, cam, "pb184", 0.85, 1.0, True, -60, 640, 872)
        with cam(0.4):
            dots = paint(C(60, 44, 50))
            for k in range(16):
                c.drawCircle(-10 + k * 15 + 6, 640 - 6 + 2 * math.sin(t * 2 + k), 2.6, dots)

        def figs(cc):
            with Cam(cc, focus, zoom)(1.0):
                M.rider(cc, 470, 872, 0.3, 1, GORD_BARE, t, {"hand": (110, -360), "rhand": (30, -318), "wind": 1.1}, wind=1.0)
                M.rider(cc, 620, 872, 0.31, -1, "sohrab", t, {"hand": (110, -340), "rhand": (30, -300)}, rider_scale=0.92)
        an.figures(c, figs, MORN, (0, 300, 1080, 1000))
        vig(an, c, 140)

    cuts(c, lt, [(0.0, two), (i0, armies), (i1, two)], 0.4)


# ================================================================== S05 his heart is lost
def p18_s05(an, c, t):
    """'Then she smiled... and Sohrab's heart was lost. She was tall as a cypress, with eyes like a deer's.' Sohrab:
    'Very well. But do not break your promise. You have seen how I fight. And don't trust those walls. They are not
    higher than the clouds. One blow of my mace, and they fall.'"""
    lt, dur = loc(an, "S05", t)
    L = [LN("p18", "S05", k) for k in range(6)]
    cut = L[2][0] - 0.4

    def her():
        rp = {"hand_kind": "fist", "hand": (100, -330), "rhand": (30, -318), "head": 8 + 2 * math.sin(t * 0.6), "wind": 1.0}
        Q.her_close(an, c, t, lt, cut + 0.4, "f185", rp, 1.0, 0.08, sstep(L[1][0], L[1][0] + 1.2, lt))

    def him():
        lt2 = lt - cut
        warn = sstep(L[2][0] + 0.8, L[2][0] + 1.3, lt) * (1 - sstep(L[3][1], L[3][1] + 0.4, lt))
        wall = sstep(L[4][0], L[4][0] + 0.6, lt) * (1 - sstep(L[4][1], L[4][1] + 0.4, lt))
        blow = sstep(L[5][0], L[5][0] + 0.4, lt)
        down = sstep(L[5][0] + 1.0, L[5][0] + 1.25, lt)
        rp = {"hand_kind": "fist", "hand": (110, -340), "rhand": (30, -300), "head": 4 + math.sin(t * 0.7),
              "jaw": jaw(an, "SOHRAB", t, 8), "wind": 0.9}
        if warn > 0.01:
            rp.update(rhand=(mix(30, 160, warn), mix(-300, -520, warn)), rhand_kind="open")
        if wall > 0.01:
            rp.update(rhand=(mix(30, 250, wall), mix(-300, -470, wall)), rhand_kind="open", head=4 - 4 * wall)
        if blow > 0.01:
            rp.update(rhand=(mix(30, mix(80, 190, down), blow), mix(-300, mix(-640, -400, down), blow)), rhand_kind="fist",
                      head=4 - 6 * blow * (1 - down), lean=-4 * blow * (1 - down) + 6 * down)
        Q.him_close(an, c, t, lt2, dur - cut, "f185b", rp, helm=False)

    cuts(c, lt, [(0.0, her), (cut, him)], 0.45)


# ================================================================== S06 the gate
def p18_s06(an, c, t):
    """'Gordafarid rode back to the fortress, and Sohrab rode beside her.' (up the road to the gate) 'At the gate, the
    doors opened, just a little... and Gordafarid slipped inside. Then, with a great crash, the gate closed... in
    Sohrab's face!' -- 'What...? Open the gate! You promised me!'"""
    lt, dur = loc(an, "S06", t)
    L = [LN("p18", "S06", k) for k in range(5)]
    c1 = L[1][0] - 0.4
    crash = L[3][0] + 1.5
    c2 = L[4][0] - 0.35

    def road():
        focus = (580, 820)
        zoom = 1.0 + 0.06 * ease(lt / (c1 + 0.4))
        cam = Cam(c, focus, zoom)
        u = clamp(lt / (c1 + 1.0))
        M.fortress_far(an, c, t, cam, "ff186", mood=0.95, gate=0.0, fx=170, fy=300, fs=1.0)

        def figs(cc):
            with Cam(cc, focus, zoom)(0.5):
                x = mix(780, 610, u)
                y = mix(1010, 860, u)
                s = mix(0.3, 0.17, u)
                M.rider(cc, x, y, s, -1, GORD_BARE, t, {"hand": (100, -340), "rhand": (30, -318), "wind": 1.0}, "walk", t * 0.9)
                M.rider(cc, x + 120 * s / 0.3, y + 6, s * 1.04, -1, "sohrab", t, {"hand": (110, -340), "rhand": (30, -300)},
                        "walk", t * 0.9 + 0.4, rider_scale=0.92)
        an.figures(c, figs, MORN, (0, 500, 1080, 1200))
        vig(an, c, 140)

    def gate():
        lt2 = lt - c1
        focus = (560, 640)
        sh = 9 * math.sin(lt * 63) * math.exp(-max(0.0, lt - crash) * 5) * (lt > crash)
        c.save()
        c.translate(sh, sh * 0.5)
        zoom = 1.0 + 0.04 * ease(lt2 / (dur - c1))
        cam = Cam(c, focus, zoom)
        g = 0.36 * sstep(L[1][0] + 0.4, L[1][0] + 1.8, lt) * (1 - sstep(crash - 0.25, crash, lt))
        gate_outside(an, c, t, cam, "go186", g, 540, 1.0, 440, 900)
        arrive = clamp((lt - c1) / (L[2][0] - c1 - 0.2))
        inside = clamp((lt - L[2][0] + 0.2) / 2.0)
        gx = mix(800, 540, ease(arrive))
        gs = mix(0.5, 0.36, inside)
        ga = 1 - sstep(0.5, 1.0, inside)
        rr = 26 * math.sin(clamp((lt - crash) / 1.3) * math.pi) if crash < lt < crash + 1.3 else 0.0
        sxp = 900
        rpS = {"hand": (110, -340), "rhand": (30, -300), "head": 4 + 6 * sstep(crash, crash + 0.4, lt) + math.sin(t * 0.7),
               "wind": 0.9}

        def setf(cam_):
            pass

        def fg(cc):
            if ga > 0.01:
                with Cam(cc, focus, zoom)(1.0):
                    M.rider(cc, gx, mix(900, 880, inside), gs, -1, GORD_BARE, t,
                            {"hand": (100, -340), "rhand": (30, -318), "head": -2, "wind": 1.0},
                            "walk" if arrive < 1 or 0 < inside < 1 else "stand", t * 0.9)
        if ga > 0.01:
            c.saveLayerAlpha(None, int(255 * ga))
            an.figures(c, fg, MORN, (0, 200, 1080, 1100))
            c.restore()
            if inside > 0:
                # the doors in front of her as she goes in (redraw them over the rider)
                with cam(0.6):
                    c.save()
                    c.clipPath(S.arch_path(540, 900, 300, 430), skia.ClipOp.kIntersect, True)
                    w = 150 * (1 - ease(g))
                    wood = paint(C(120, 86, 62))
                    c.drawRect(skia.Rect.MakeLTRB(390, 460, 390 + w, 900), wood)
                    c.drawRect(skia.Rect.MakeLTRB(690 - w, 460, 690, 900), wood)
                    c.restore()

        def fs(cc):
            with Cam(cc, focus, zoom)(1.0):
                if rr > 1:
                    M.rider(cc, sxp, 900, 0.52, -1, "sohrab", t, rpS, "rear", 0.0, rider_scale=0.92, rear=rr)
                else:
                    M.rider(cc, sxp, 900, 0.52, -1, "sohrab", t, rpS, "stand", 0.0, rider_scale=0.92, neck=5 * math.sin(t * 1.4))
        an.figures(c, fs, COLT, (0, 200, 1080, 1100), alpha=190)
        P16.dust_puff(c, 540, 890, t, crash, lt, 1.0)
        c.restore()
        vig(an, c, 145)

    def shout():
        lt3 = lt - c2
        focus = (600, 660)
        zoom = 1.02 + 0.05 * ease(lt3 / (dur - c2))
        cam = Cam(c, focus, zoom)
        gate_outside(an, c, t, cam, "go186b", 0.0, 400, 1.0, 440, 1000)
        up = sstep(L[4][0] + 0.6, L[4][0] + 1.1, lt)
        rp = {"hand": (110, -340), "rhand": (mix(30, 120, up), mix(-300, -620, up)), "rhand_kind": "fist",
              "head": -10 - 4 * up + math.sin(t * 0.7), "jaw": jaw(an, "SOHRAB", t, 9), "lean": -4, "wind": 0.9}

        def fs(cc):
            with Cam(cc, focus, zoom)(1.0):
                M.rider(cc, 700, 1000, 0.8, -1, "sohrab", t, rp, rider_scale=0.92, neck=6 * math.sin(t * 1.5))
        an.figures(c, fs, COLT, (0, 100, 1080, 1200), alpha=180)
        vig(an, c, 150)

    cuts(c, lt, [(0.0, road), (c1, gate), (c2, shout)], 0.4)


# ================================================================== S07 inside: a lion and a fox
def p18_s07(an, c, t):
    """Inside the gate: 'the people of the fortress ran to her, laughing and weeping.' Gazhdaham: 'My daughter! My brave
    lioness, you are alive! You fought him... and you tricked him too!' -- 'A lion's strength was not enough, Father.
    So I used a fox's trick.'"""
    lt, dur = loc(an, "S07", t)
    L = [LN("p18", "S07", k) for k in range(4)]
    cut = L[1][0] - 0.4

    def wide():
        focus = (540, 700)
        zoom = 1.0 + 0.05 * ease(lt / (cut + 0.4))
        cam = Cam(c, focus, zoom)
        M.gate_court(an, c, t, cam, "gc187", 0.0, 720)

        def figs(cc):
            with Cam(cc, focus, zoom)(1.0):
                horse(cc, 930, 872, 0.6, -1, {"gait": "stand", "saddle": True, "neck": 6 * math.sin(t * 1.4)}, t)
                person(cc, 640, 872, 0.82, -1, {"hand": (40, -262), "rhand": (-20, -270), "head": 2 + math.sin(t * 0.8),
                                                "wind": 0.8}, t, GORD_BARE)
                people_running(cc, lt, t, -160, 480, 3.0, 872, 0.74)
        an.figures(c, figs, DAY, (0, 200, 1080, 1000))
        vig(an, c, 145)

    def two():
        lt2 = lt - cut
        focus = (540, 640)
        zoom = 1.0 + 0.05 * ease(lt2 / (dur - cut))
        cam = Cam(c, focus, zoom)
        M.gate_court(an, c, t, cam, "gc187b", 0.0, 540)
        hold = sstep(L[1][0], L[1][0] + 0.6, lt) * (1 - sstep(L[2][1], L[2][1] + 0.5, lt))
        proud = sstep(L[3][0], L[3][0] + 0.5, lt)
        sly = sstep(L[3][1] - 1.6, L[3][1] - 1.0, lt)
        PZ = {"jaw": jaw(an, "GAZHDAHAM", t, 8), "hand_kind": "staff", "hand": (60, -300),
              "rhand": (mix(-20, 190, hold), mix(-280, -430, hold)), "rhand_kind": "open" if hold > 0.3 else "fist",
              "head": 4 - 4 * hold + math.sin(t * 0.6), "lean": 4 * hold}
        PG = {"jaw": jaw(an, "GORDAFARID", t, 8), "hand": (mix(40, 120, proud * (1 - sly)), mix(-262, -330, proud * (1 - sly))),
              "hand_kind": "fist", "rhand": (mix(-20, 60, sly), mix(-270, -500, sly)), "rhand_kind": "open" if sly > 0.3 else "fist",
              "head": 2 - 4 * proud + 6 * sly + math.sin(t * 0.8), "wind": 0.8}

        def figs(cc):
            with Cam(cc, focus, zoom)(1.0):
                person(cc, 300, 1330, 1.46, 1, PZ, t, GAZH)
                person(cc, 790, 1330, 1.34, -1, PG, t, GORD_BARE)
        an.figures(c, figs, DAY, (0, 0, 1080, 1500))
        vig(an, c, 150)

    cuts(c, lt, [(0.0, wide), (cut, two)], 0.45)


# ================================================================== S08 + END laughter on the wall
def p18_s08(an, c, t):
    """'Outside, Sohrab waited at the closed gate. Then, from high on the wall, he heard someone laughing.' He looks up:
    'and there stood Gordafarid' -- on the battlements against the sky, laughing, her hair in the wind."""
    lt = t - an.start["S08"]
    dur = an.end["END"] - an.start["S08"]
    L = [LN("p18", "S08", k) for k in range(3)]
    cut = L[2][0] - 0.3

    def wait():
        focus = (600, 660)
        zoom = 1.0 + 0.05 * ease(lt / (cut + 0.4))
        cam = Cam(c, focus, zoom)
        gate_outside(an, c, t, cam, "go188", 0.0, 400, 1.0, 440, 1000)
        up = sstep(L[1][1] - 1.2, L[1][1] - 0.4, lt)
        rp = {"hand": (110, -340), "rhand": (30, -300), "head": 8 - 22 * up + math.sin(t * 0.6), "lean": -3 * up, "wind": 0.9}

        def fs(cc):
            with Cam(cc, focus, zoom)(1.0):
                M.rider(cc, 700, 1000, 0.8, -1, "sohrab", t, rp, rider_scale=0.92, neck=6 * math.sin(t * 1.3),
                        head=4 * math.sin(t * 0.9))
        an.figures(c, fs, COLT, (0, 100, 1080, 1200), alpha=180)
        vig(an, c, 150)

    def wall():
        lt2 = lt - cut
        focus = (540, 640)
        zoom = 1.0 + 0.08 * ease(lt2 / (dur - cut))
        cam = Cam(c, focus, zoom)
        laugh = sstep(0.6, 1.2, lt2)
        P = {"hand": (mix(40, 60, laugh), mix(-262, -300, laugh)), "hand_kind": "fist",
             "rhand": (mix(-20, 140, laugh), mix(-270, -470 + 20 * math.sin(t * 5), laugh)), "rhand_kind": "open",
             "head": -4 - 12 * laugh + 3 * math.sin(t * 11) * laugh, "lean": -4 * laugh, "wind": 1.4}

        def figs(cc):
            with Cam(cc, focus, zoom)(1.0):
                person(cc, 470, 1330, 1.36, -1, P, t, GORD_BARE)
        wall_low(an, c, t, cam, "wl188", figs, top=1150, sun=(500, 560))
        vig(an, c, 150)

    dissolve(c, lt, cut, 0.5, wait, wall)


P18 = {"S01": p18_s01, "TITLE": p18_s01, "S02": p18_s02, "S03": p18_s03, "S04": p18_s04, "S05": p18_s05,
       "S06": p18_s06, "S07": p18_s07, "S08": p18_s08, "END": p18_s08}
SHIFT18 = {}

register(P18, SHIFT18)
