"""Parts 17-18 (row 9 of OUTLINE.md, "Gordafarid"): every shot as a shadow-play scene.

Importing this module registers part 17's shots; p18_scenes.py imports it and registers part 18's.
New here, to reuse: GORD_HID (Gordafarid in armour, helmeted, her hair hidden: the Turanians take her for a man),
gh() / colt() (her horse / Sohrab's colt with the rider on it, one call), duo() (the two of them on a set, each
with their own rim, extra props drawn in the same pass from anchors computed for both: ropes, lances, helmets),
waist() (a rider's belt from the "pneck" anchor), shield() (a round shield at a hand, arrows stuck in it),
loop_at() (a lasso loop round a waist), lifted() (a rider raised out of the saddle), gallop_bg() (sky + scrolling
plain for a gallop to the LEFT), sun_head() (a face that "shines like the sun"), prisoner_led() (Hojir bound,
led through the camp), turk_two() (two Turanian soldiers in close-up, the plain between them).
Line timings come from pNN/audio/timeline.json (LN), so the action follows the voices.
"""
import math, random
import skia
import anim
from anim import C, mix, mixc, clamp, ease, sstep, Cam, Pen, ANCH, rope, spath, ppath, paint, fillp, taper, bez, W, H
from puppets import person, horse, LOOKS
import sets as S
import p15_scenes as M
import p16_scenes as P16
from ep01_scenes import loc, jaw, get, vig, tag, A, ground, INK, Scroller, tufts_list
from p05_scenes import register
from p07_scenes import LN, dissolve, DAY
from p09_scenes import arrow, bow_string
from p11_scenes import COLT, army_band, draw_band, camp
from p13_scenes import HOOMAN, BARMAN, cuts

HOJIR, GAZH, GORD, MORN = M.HOJIR, M.GAZH, M.GORD, M.MORN
GORD_BARE, GORD_ARM = P16.GORD_BARE, P16.GORD_ARM
GORD_HID = dict(LOOKS["gordafarid"], hair=False)        # helmeted, the long hair hidden under the armour
GY, SG = P16.GY, P16.SG                                  # ground lines: wide shots / medium shots
MOOD = 0.9
TURK = dict(LOOKS["warrior_tu"])


# ------------------------------------------------------------------ riders
def gh(rp, t, look=GORD_HID, gait="stand", phase=0.0, rear=0.0, **kw):
    """Gordafarid's horse, saddled, with her on it (look=None: riderless)."""
    if rear > 1:
        P = {"gait": "rear", "rear": rear}
    else:
        P = {"gait": gait, "phase": phase}
        if gait == "stand":
            P.update(neck=6 * math.sin(t * 1.5 + 0.6), head=3 * math.sin(t * 1.2))
    P.update(saddle=True, wind=0.7)
    if look:
        P.update(rider=look, rider_pose=rp)
    P.update(kw)
    return P


def colt(rp, t, gait="stand", phase=0.0, rear=0.0, rider="sohrab", **kw):
    """Sohrab's colt of Rakhsh's line, saddled, with him on it."""
    if rear > 1:
        P = {"gait": "rear", "rear": rear}
    else:
        P = {"gait": gait, "phase": phase}
        if gait == "stand":
            P.update(neck=5 * math.sin(t * 1.9 + 1), head=4 * math.sin(t * 1.3))
    P.update(saddle=True, wind=0.8)
    if rider:
        P.update(rider=rider, rider_scale=0.92, rider_pose=rp)
    P.update(kw)
    return P


def duo(an, c, t, focus, zoom, setf, G=None, Sd=None, eg=None, es=None, anchors=False, box=(0, 100, 1080, 1300),
        front=None, sa=200):
    """A set (setf(cam)) with Gordafarid's horse G and Sohrab's colt Sd, each (x, y, s, face, P); her rim MORN, his
    the colt's rose. eg(cc) / es(cc) draw extra things in her / his pass. anchors=True computes the anchors of both
    first ("g:..." and "s:..."), so a rope can run from his hand to her waist. front(cam) draws over everything."""
    cam = Cam(c, focus, zoom)
    setf(cam)

    def fg(cc):
        if G:
            with Cam(cc, focus, zoom)(1.0):
                tag("g:")
                horse(cc, G[0], G[1], G[2], G[3], G[4], t)
                tag("")
        if eg:
            eg(cc)

    def fs(cc):
        if Sd:
            with Cam(cc, focus, zoom)(1.0):
                tag("s:")
                horse(cc, Sd[0], Sd[1], Sd[2], Sd[3], Sd[4], t)
                tag("")
        if es:
            es(cc)
    if anchors:
        ANCH.clear()
        Pen.mode = "anchor"
        fg(c)
        fs(c)
        Pen.mode = "fill"
    if G or eg:
        an.figures(c, fg, MORN, box)
    if Sd or es:
        an.figures(c, fs, COLT, box, alpha=sa)
    if front:
        front(cam)
    return cam


def waist(name, se):
    """A rider's belt, from the neck anchor (se = the figure's scale on screen)."""
    p = A(name + "pneck")
    return None if p is None else (p[0], p[1] + 112 * se)


def shield(cc, p, r, stuck=(), face=-1):
    """A round shield of radius r at p (a hand); stuck = arrows in it, as (angle deg, length) pointing at the archer."""
    if p is None or Pen.mode == "anchor":
        return
    x, y = p
    disc = skia.Path()
    disc.addCircle(x, y, r)
    fillp(cc, disc)
    if Pen.mode == "fill":
        ring = skia.Paint(AntiAlias=True, Color=C(70, 40, 40))
        ring.setStyle(skia.Paint.kStroke_Style)
        ring.setStrokeWidth(max(1.5, r * 0.05))
        cc.drawCircle(x, y, r * 0.78, ring)
        cc.drawCircle(x, y, r * 0.16, ring)
    for (a, ln) in stuck:
        ang = math.radians(a)
        bx, by = x + 0.55 * r * math.cos(ang + 1.2), y + 0.55 * r * math.sin(ang + 1.2)
        ex, ey = bx - face * ln * math.cos(math.radians(a * 0.3)), by - ln * math.sin(math.radians(a * 0.3)) * 0.4 - ln * 0.25
        rope(cc, (bx, by), (ex, ey), 0, max(2.0, r * 0.045))
        fillp(cc, ppath([(ex, ey), (ex - face * 10, ey - 7), (ex - face * 14, ey - 1), (ex - face * 4, ey + 4)]))


def loop_at(cc, p, rx, ry, w=3.0):
    """A lasso loop round a waist at p."""
    if p is None or Pen.mode == "anchor":
        return
    base = anim.ink()
    pt = skia.Paint(AntiAlias=True, Color=base.getColor())
    pt.setStyle(skia.Paint.kStroke_Style)
    pt.setStrokeWidth(w + (3.2 if Pen.mode == "rim" else 0))
    cc.drawOval(skia.Rect.MakeLTRB(p[0] - rx, p[1] - ry, p[0] + rx, p[1] + ry), pt)


def lifted(cc, x, y, s, face, rp, lift, tilt, t, look):
    """A rider raised out of the saddle of a horse at (x, y, s, face): lift px up, turned by tilt degrees."""
    hx, hy = x + 30 * s * face, y - 62 * s - lift
    cc.save()
    cc.translate(hx, hy - 250 * s)
    cc.rotate(tilt * face)
    cc.translate(-hx, -(hy - 250 * s))
    person(cc, hx, hy, s, face, dict(rp, mode="ride"), t, look)
    cc.restore()


def gallop_bg(an, c, t, lt, key, speed=420, cols=((150, 146, 168), (176, 140, 120), (214, 172, 120)), dy=70):
    """Sky and a scrolling plain for a gallop to the LEFT (the plain runs to the right)."""
    M.sky_day(c, MOOD)
    S.sun(c, 880, 520, 56, (255, 248, 222), (255, 214, 150), 520, 150)
    c.save()
    c.translate(W, dy)
    c.scale(-1, 1)
    get(an, key, lambda: Scroller(171)).draw(c, lt + 3.0, speed, list(cols))
    c.restore()


def trail(c, x, y, lt, t, a=1.0, back=1, seed=0):
    """Dust thrown up behind a galloping horse (back = +1: behind is to the right)."""
    for k in range(3):
        u = (lt * 2.0 + k * 0.33) % 1.0
        S.dust(c, x + back * (110 + u * 180), y - 10 - u * 26, 36 + u * 70, t, (240, 214, 170), 110 * (1 - u) * a, k + seed)


def sun_head(c, x, y, a, t, r=120):
    """Light behind a head, so the face 'shines like the sun'."""
    if a <= 0.01:
        return
    pulse = 0.92 + 0.08 * math.sin(t * 1.7)
    S.glow(c, x, y, r * 4.2, (255, 214, 150), 120 * a * pulse)
    S.glow(c, x, y, r * 1.7, (255, 238, 196), 170 * a * pulse)


def her_set(an, c, t, cam, key, fs=0.42, fx=-40, fy=560, host=1.0, host_x=640, gy=GY):
    P16.field(an, c, t, cam, key, MOOD, fx=fx, fy=fy, fs=fs, host=host, host_x=host_x, gy=gy)


# ------------------------------------------------------------------ poses
def p_shout(t, jw, up=0.0, lance=0.0):
    """Gordafarid on horseback, the lance upright, raised as she shouts."""
    return M.lance_pose(lance, {"hand": (mix(100, 116, up), mix(-330, -470, up)), "lance": mix(0, -8, up) + lance * 84,
                                "rhand": (mix(-20, 30, up), mix(-280, -300, up)), "head": -2 - 4 * up + math.sin(t * 0.8),
                                "jaw": jw, "wind": 0.8})


def p_bow(t, raise_, draw_, jw=0.0):
    """Gordafarid on horseback with her bow: raise_ lifts it, draw_ pulls the string to her cheek."""
    return {"hand_kind": "bow", "hand": (mix(70, 170, raise_), mix(-300, -420, raise_)),
            "rhand": (mix(-20, mix(128, 26, draw_), raise_), mix(-280, -430, raise_)), "head": -3 * raise_ + math.sin(t * 0.7),
            "lean": -3 * draw_, "jaw": jw, "wind": 0.8}


def p_shieldup(t, up, jw=0.0, lance=1.0, lean=6.0):
    """Sohrab on his colt, the shield raised over his head (rhand), the lance couched in the other hand."""
    return {"hand_kind": "lance", "lance": mix(0, 84, lance), "hand": (mix(100, 112, lance), mix(-330, -346, lance)),
            "rhand": (mix(-20, 30, up), mix(-300, -600, up)), "rhand_kind": "fist", "head": 6 * up + math.sin(t * 0.9),
            "lean": lean, "jaw": jw, "wind": 1.1}


STUCK = [(-30, 44), (10, 52), (40, 40), (70, 48), (-60, 40), (100, 44)]


# ================================================================== part 17
def p17_s01(an, c, t):
    """Hook + title: Gordafarid (helmeted, the Turanians take her for a man) rears before the host: 'Turanians! Where
    are your heroes? Who will fight me?' -- Sohrab on his colt laughs: 'Ha! Another prey walks into my trap.'"""
    lt = t - an.start["S01"]
    dur = an.end["TITLE"] - an.start["S01"]
    a0, a1 = LN("p17", "S01", 0)
    b0, b1 = LN("p17", "S01", 1)
    rr = 24 * math.sin(clamp((lt - a0 - 0.1) / 1.5) * math.pi) if a0 + 0.1 < lt < a0 + 1.6 else 0.0
    up = sstep(a0 + 1.8, a0 + 2.4, lt) * (1 - sstep(b0, b0 + 0.6, lt))
    laugh = sstep(b0 - 0.1, b0 + 0.3, lt) * (1 - sstep(b1 + 0.2, b1 + 0.8, lt))
    rpG = p_shout(t, jaw(an, "GORDAFARID", t, 8), up)
    rpS = M.lance_pose(0.0, {"head": -9 * laugh + 3 * math.sin(t * 13) * laugh + math.sin(t * 0.8), "jaw": jaw(an, "SOHRAB", t, 8),
                             "rhand": (mix(-20, 40, laugh), mix(-300, -330, laugh)), "lean": -4 * laugh, "wind": 0.8})
    M.faceoff(an, c, t, gh(rpG, t, rear=rr), colt(rpS, t), 1.04 + 0.08 * ease(lt / dur), key="fo171", hs=0.72)


# ------------------------------------------------------------------ S02 the prisoner; she arms herself
def prisoner_led(an, c, t, lt, dur, key, sohrab_x=860):
    """The Turanian camp: a rider leads Hojir, his hands bound, on a rope; Sohrab watches with his lance."""
    focus = (560, 700)
    zoom = 1.0 + 0.05 * ease(lt / dur)
    cam = Cam(c, focus, zoom)
    camp(an, c, t, cam, key)
    walk = clamp(lt / (dur + 1.5))
    rx = mix(240, 620, walk)

    def figs(cc):
        with Cam(cc, focus, zoom)(1.0):
            tag("r:")
            M.rider(cc, rx, 872, 0.5, 1, "rider", t, {"rhand": (-120, -300), "rhand_kind": "fist", "hand": (100, -300),
                                                      "hand_kind": "spear", "head": -4}, gait="walk", phase=t * 0.8)
            tag("h:")
            person(cc, rx - 290, 872, 0.54, 1, {"mode": "walk", "phase": lt * 3.2, "stride": 16, "hand": (70, -276),
                                                "rhand": (62, -270), "head": 12, "lean": 7, "wind": 0.5}, t, HOJIR)
            tag("")
            person(cc, sohrab_x, 872, 0.6, -1, {"rprop": "lance", "lance": -8, "rhand": (-30, -262), "hand": (40, -262),
                                                "head": 4 + math.sin(t * 0.6), "wind": 0.7}, t, "sohrab")
        rope(cc, A("r:rhand"), A("h:hand"), 30, 2.4)
    an.figures(c, figs, DAY, (0, 200, 1080, 1000), anchors=True)
    vig(an, c, 140)


def p17_s02(an, c, t):
    """'Hojir ... was now Sohrab's prisoner. Sohrab ... had beaten him with one blow.' (Hojir led bound through the
    camp.) 'But one warrior in the fortress was not afraid...' Inside the gate Gordafarid, in armour, her hair loose,
    lifts her helmet; 'She hid her long hair under her armour, and tied on her helmet.' Gazhdaham: 'Be careful, my
    daughter. He is a young giant.' -- 'Then let the giant meet me. Open the gate!'"""
    lt, dur = loc(an, "S02", t)
    L = [LN("p17", "S02", k) for k in range(6)]
    c1 = L[2][0] - 0.4
    c2 = L[4][0] - 0.4

    def led():
        prisoner_led(an, c, t, lt, c1 + 0.4, "cp172")

    def helm():
        lt2 = lt - c1
        focus = (540, 560)
        zoom = 1.0 + 0.06 * ease(lt2 / (c2 - c1 + 0.4))
        cam = Cam(c, focus, zoom)
        M.gate_court(an, c, t, cam, "gc172", 0.0, 760)
        step = clamp(lt2 / 2.2)
        gx = mix(120, 360, ease(step))
        h0, h1 = L[3][0] + 0.9, L[3][0] + 2.6
        lift = sstep(L[3][0] - 0.2, L[3][0] + 0.8, lt)
        on = sstep(h0, h1, lt)
        worn = lt >= h1
        GS, GYH = 1.42, 1440
        hy_ = mix(mix(-290, -610, lift), -514, on)
        if not worn:
            P = {"mode": "walk" if step < 1 else "stand", "phase": lt2 * 3.6, "stride": 14,
                 "hand": (mix(96, 22, lift), hy_), "rhand": (mix(66, -4, lift), hy_ + 4), "hand_kind": "fist",
                 "rhand_kind": "fist", "head": -2 + 4 * on + math.sin(t * 0.7), "wind": 0.9}
        else:
            tie = sstep(h1, h1 + 0.8, lt)
            P = {"hand": (mix(22, 30, tie), mix(-514, -470, tie)), "rhand": (mix(-4, -20, tie), mix(-510, -270, tie)),
                 "hand_kind": "fist", "rhand_kind": "fist", "head": -4 + math.sin(t * 0.7), "wind": 0.9}

        def figs(cc):
            with Cam(cc, focus, zoom)(1.0):
                tag("g:")
                person(cc, gx, GYH, GS, 1, P, t, GORD_HID if worn else GORD_BARE)
                tag("")
            if not worn:
                a, b = A("g:hand"), A("g:rhand")
                if a and b:
                    P16.helmet_at(cc, (a[0] + b[0]) / 2 + 4, (a[1] + b[1]) / 2 + 6, GS * zoom, t, 1)
        an.figures(c, figs, DAY, (0, 0, 1080, 1500), anchors=True)
        vig(an, c, 160)

    def two():
        lt3 = lt - c2
        focus = (540, 640)
        zoom = 1.0 + 0.05 * ease(lt3 / (dur - c2))
        cam = Cam(c, focus, zoom)
        M.gate_court(an, c, t, cam, "gc172b", 0.0, 540)
        care = sstep(L[4][0], L[4][0] + 0.5, lt) * (1 - sstep(L[4][1], L[4][1] + 0.6, lt))
        proud = sstep(L[5][0], L[5][0] + 0.5, lt)
        call = sstep(L[5][1] - 1.3, L[5][1] - 0.7, lt)
        PZ = {"jaw": jaw(an, "GAZHDAHAM", t, 8), "hand_kind": "staff", "hand": (60, -300),
              "rhand": (mix(-20, 150, care), mix(-280, -400, care)), "rhand_kind": "open" if care > 0.3 else "fist",
              "head": 4 + math.sin(t * 0.6), "lean": 3 * care}
        PG = {"jaw": jaw(an, "GORDAFARID", t, 8), "hand_kind": "spear", "hand": (mix(60, 70, proud), mix(-300, -330, proud)),
              "rhand": (mix(-20, -170, call), mix(-270, -460, call)), "rhand_kind": "open" if call > 0.3 else "fist",
              "head": -2 - 3 * proud + math.sin(t * 0.8), "wind": 0.7}

        def figs(cc):
            with Cam(cc, focus, zoom)(1.0):
                person(cc, 300, 1330, 1.46, 1, PZ, t, GAZH)
                person(cc, 780, 1330, 1.36, -1, PG, t, GORD_HID)
        an.figures(c, figs, DAY, (0, 0, 1080, 1500))
        vig(an, c, 150)

    cuts(c, lt, [(0.0, led), (c1, helm), (c2, two)], 0.45)


# ------------------------------------------------------------------ S03 she rides out and calls them out
def turk_two(an, c, t, lt, dur, key, PL, PR, far, focus=(540, 680)):
    """Two Turanian soldiers in close-up at the edges of the frame; between them, far off on the plain, the fortress
    on its hill and far(cc, cam_zoom) (a small rider)."""
    zoom = 1.0 + 0.05 * ease(lt / dur)
    cam = Cam(c, focus, zoom)
    P16.field(an, c, t, cam, key, MOOD, fx=372, fy=560, fs=0.42, host=0.0)

    def ff(cc):
        with Cam(cc, focus, zoom)(1.0):
            far(cc)
    an.figures(c, ff, MORN, (0, 500, 1080, 1000))

    def figs(cc):
        with Cam(cc, focus, zoom)(1.0):
            person(cc, 150, 1330, 1.34, 1, PL, t, TURK)
            person(cc, 950, 1330, 1.3, -1, PR, t, "rider")
    an.figures(c, figs, DAY, (0, 0, 1080, 1500))
    vig(an, c, 150)


def p17_s03(an, c, t):
    """'The gate opened, and she rode down from the fortress like a lioness.' Before the host she rears: 'Turanians!
    Where are your heroes? Who is brave enough to fight me?' Two Turanians: 'Another rider from the fortress!' --
    'Look at him. So small... and so bold!'"""
    lt, dur = loc(an, "S03", t)
    L = [LN("p17", "S03", k) for k in range(5)]
    c1 = L[1][0] - 0.4
    c2 = L[3][0] - 0.35

    def gate():
        focus = (580, 820)
        zoom = 1.0 + 0.06 * ease(lt / (c1 + 0.5))
        cam = Cam(c, focus, zoom)
        g = sstep(0.0, 1.4, lt)
        u = clamp((lt - 1.0) / 3.6)
        M.fortress_far(an, c, t, cam, "ff173", mood=0.8, gate=g, fx=170, fy=300, fs=1.0)

        def figs(cc):
            with Cam(cc, focus, zoom)(0.5):
                x = mix(570, 720, u)
                y = mix(842, 1010, u * u * 0.4 + u * 0.6)
                s = mix(0.15, 0.32, u)
                M.rider(cc, x, y, s, 1, GORD_HID, t, M.lance_pose(0.0, {"head": 2, "wind": 0.9}), "gallop", t * 2.0)
        if lt > 0.9:
            an.figures(c, figs, MORN, (0, 500, 1080, 1200))
            with cam(0.5):
                S.dust(c, mix(570, 720, u) - 60 * mix(0.15, 0.32, u) * 3, mix(842, 1010, u) - 10, 40 + 60 * u, t,
                       (236, 214, 180), 120, 3)
        vig(an, c, 140)

    def call():
        lt2 = lt - c1
        focus = (520, 700)
        zoom = 1.02 + 0.06 * ease(lt2 / (c2 - c1 + 0.4))
        rr = 26 * math.sin(clamp((lt - L[1][0] + 0.1) / 1.4) * math.pi) if L[1][0] - 0.1 < lt < L[1][0] + 1.3 else 0.0
        up = sstep(L[2][0] - 0.2, L[2][0] + 0.4, lt)
        rp = p_shout(t, jaw(an, "GORDAFARID", t, 8), up)

        def setf(cam):
            her_set(an, c, t, cam, "f173b", fs=None, host_x=420, gy=SG - 120)
        duo(an, c, t, focus, zoom, setf, G=(400, SG, 0.8, 1, gh(rp, t, rear=rr)))
        vig(an, c, 150)

    def turks():
        lt3 = lt - c2
        a = sstep(L[3][0], L[3][0] + 0.4, lt) * (1 - sstep(L[3][1], L[3][1] + 0.5, lt))
        b = sstep(L[4][0], L[4][0] + 0.4, lt)
        PL = {"jaw": jaw(an, "RIDER", t, 8), "hand_kind": "spear", "hand": (60, -330),
              "rhand": (mix(-20, 160, a), mix(-280, -430, a)), "rhand_kind": "open" if a > 0.3 else "fist",
              "head": 2 - 4 * a + math.sin(t * 0.7), "wind": 0.5}
        PR = {"jaw": jaw(an, "RIDER2", t, 8), "hand_kind": "spear", "hand": (60, -330),
              "rhand": (mix(-20, 40, b), mix(-280, -320, b)), "head": 3 - 6 * b + 2 * math.sin(t * 9) * b + math.sin(t * 0.6),
              "lean": -3 * b, "wind": 0.5}
        hx = 540 + 10 * math.sin(lt * 0.9)

        def far(cc):
            M.rider(cc, hx, 846, 0.17, 1, GORD_HID, t, p_shout(t, 0.0, 0.6 + 0.4 * math.sin(lt * 2.0)),
                    gait="stand", neck=6 * math.sin(t * 1.5))
        turk_two(an, c, t, lt3, dur - c2, "f173c", PL, PR, far)

    cuts(c, lt, [(0.0, gate), (c1, call), (c2, turks)], 0.4)


# ------------------------------------------------------------------ S04 Sohrab laughs
def p17_s04(an, c, t):
    """Sohrab on his colt before the host laughs and bites his lip: 'Ha! Another prey walks into my trap.' Hooman,
    on foot at his stirrup: 'Shall I send one of our men, Sohrab?' -- 'No, Hooman. This one is mine.' The colt rears."""
    lt, dur = loc(an, "S04", t)
    L = [LN("p17", "S04", k) for k in range(4)]
    cut = L[2][0] - 0.3
    laugh = sstep(L[0][1] - 1.8, L[0][1] - 1.4, lt) * (1 - sstep(L[1][1], L[1][1] + 0.5, lt))

    def solo():
        focus = (600, 640)
        zoom = 1.0 + 0.07 * ease(lt / (cut + 0.4))
        rp = M.lance_pose(0.0, {"head": 4 - 10 * laugh + 3 * math.sin(t * 12) * laugh * (lt < L[1][0]) + math.sin(t * 0.8),
                                "jaw": jaw(an, "SOHRAB", t, 8), "rhand": (mix(-20, 50, laugh), mix(-300, -320, laugh)),
                                "lean": -5 * laugh, "wind": 0.8})

        def setf(cam):
            her_set(an, c, t, cam, "f174", fs=None, host_x=60, gy=SG - 120)
        duo(an, c, t, focus, zoom, setf, Sd=(640, SG, 0.82, -1, colt(rp, t)))
        vig(an, c, 150)

    def two():
        lt2 = lt - cut
        focus = (540, 660)
        zoom = 1.0 + 0.04 * ease(lt2 / (dur - cut))
        ask = sstep(L[2][0], L[2][0] + 0.5, lt) * (1 - sstep(L[2][1] + 0.2, L[2][1] + 0.7, lt))
        mine = sstep(L[3][0] + 0.6, L[3][0] + 1.2, lt)
        rr = 30 * math.sin(clamp((lt - L[3][1] - 0.1) / 1.3) * math.pi) if L[3][1] + 0.1 < lt < L[3][1] + 1.4 else 0.0
        rp = M.lance_pose(0.0, {"hand": (mix(100, 112, mine), mix(-330, -450, mine)), "lance": -6 * mine,
                                "head": 6 - 2 * mine + math.sin(t * 0.8), "jaw": jaw(an, "SOHRAB", t, 8), "wind": 0.9})
        PH = {"jaw": jaw(an, "HOOMAN", t, 8), "rprop": "mace", "rhand": (-24, -300), "mace": -6,
              "hand": (mix(40, 150, ask), mix(-262, -400, ask)), "hand_kind": "open" if ask > 0.3 else "fist",
              "head": -8 + 2 * ask + math.sin(t * 0.7), "wind": 0.5}

        def setf(cam):
            her_set(an, c, t, cam, "f174b", fs=None, host_x=-40, gy=1330 - 380)

        def eg(cc):
            with Cam(cc, focus, zoom)(1.0):
                person(cc, 250, 1330, 1.12, 1, PH, t, HOOMAN)
        duo(an, c, t, focus, zoom, setf, Sd=(790, 1330, 1.16, -1, colt(rp, t, rear=rr)), eg=eg, box=(0, 0, 1080, 1500))
        vig(an, c, 150)

    dissolve(c, lt, cut, 0.4, solo, two)


# ------------------------------------------------------------------ S05 the rain of arrows
def p17_s05(an, c, t):
    """'But Gordafarid was a great archer. No bird could fly past her arrows.' -- 'Take this, Turanian!' Arrow after
    arrow at Sohrab as he gallops in, his shield over his head; 'Arrows?! You will pay for this!' He charges."""
    lt, dur = loc(an, "S05", t)
    L = [LN("p17", "S05", k) for k in range(5)]
    c1 = L[2][0] - 0.3
    c2 = L[3][0] - 0.3

    def archer():
        focus = (520, 660)
        zoom = 1.02 + 0.05 * ease(lt / (c1 + 0.3))
        shots = [(2.4, 4.0), (L[1][0] - 0.2, L[1][0] + 0.7)]
        raise_ = sstep(0.6, 1.5, lt)
        draw_ = 0.0
        for (d0, r) in shots:
            if d0 <= lt < r + 0.1:
                draw_ = sstep(d0, d0 + 1.0 if r - d0 > 1.2 else r - 0.1, lt) * (1 - sstep(r, r + 0.08, lt))
        nock = any(d0 - 0.4 <= lt < r for (d0, r) in shots)
        rp = p_bow(t, raise_, draw_, jaw(an, "GORDAFARID", t, 7))

        def setf(cam):
            her_set(an, c, t, cam, "f175", fs=0.34, fx=-170, fy=600, host_x=720, gy=SG - 120)

        def eg(cc):
            bow_string(cc, "g:", draw_, nock)
        duo(an, c, t, focus, zoom, setf, G=(380, SG, 0.82, 1, gh(rp, t)), eg=eg, anchors=True)
        hd = A("g:hand")
        if hd:
            for (d0, r) in shots:
                if r <= lt < r + 0.6:
                    arrow(c, hd[0] + 20, hd[1], 1300, hd[1] - 40, (lt - r) / 0.6, 1.0)
        vig(an, c, 150)

    def rain():
        lt2 = lt - c1
        focus = (540, 680)
        zoom = 1.0 + 0.04 * ease(lt2 / (c2 - c1 + 0.3))
        sx = 1180 - 60 * lt2 * 1.0
        up = sstep(0.3, 1.0, lt2)
        rels = [0.2 + 0.85 * k for k in range(6)]
        cyc = (lt2 % 0.85) / 0.85
        draw_ = sstep(0.1, 0.7, cyc) * (1 - sstep(0.92, 1.0, cyc))
        rp = p_bow(t, 1.0, draw_, 0.0)
        hit = [r for r in rels if lt2 >= r + 0.55]
        stuck = [STUCK[k] for k in range(len(hit)) if k % 3 != 1][:4]

        def setf(cam):
            her_set(an, c, t, cam, "f175b", fs=0.4, fx=-120, fy=560, host_x=760)

        def eg(cc):
            bow_string(cc, "g:", draw_, True)

        def es(cc):
            shield(cc, A("s:rhand"), 34 * zoom, stuck, -1)
        duo(an, c, t, focus, zoom, setf, G=(240, GY, 0.46, 1, gh(rp, t)),
            Sd=(sx, GY, 0.48, -1, colt(p_shieldup(t, up, 0.0, 0.3), t, "gallop", t * 2.1)), eg=eg, es=es, anchors=True)
        hd, sh = A("g:hand"), A("s:rhand")
        if hd and sh:
            for k, r in enumerate(rels):
                u = (lt2 - r) / 0.55
                if 0 <= u < 1:
                    ty = sh[1] + (0 if k % 3 != 1 else -90)
                    tx = sh[0] + (0 if k % 3 != 1 else 60)
                    arrow(c, hd[0] + 10, hd[1], tx, ty, u, 0.6)
        trail(c, sx, GY, lt2, t, 1.0, 1)
        vig(an, c, 140)

    def charge():
        lt3 = lt - c2
        couch = sstep(L[4][0] + 1.0, L[4][0] + 2.4, lt)
        rp = p_shieldup(t, 1.0, jaw(an, "SOHRAB", t, 9), couch, 8 + 4 * couch)
        rp["head"] = 4 + 2 * math.sin(t * 9) + math.sin(t * 0.9)
        gallop_bg(an, c, t, lt3, "sc175")
        c.save()
        c.translate(0, 70)

        def es(cc):
            shield(cc, A("s:rhand"), 58, STUCK[:4], -1)
        ANCH.clear()
        Pen.mode = "anchor"
        tag("s:")
        M.rider(c, 560, 870, 0.8, -1, "sohrab", t, rp, gait="gallop", phase=t * 2.2, rider_scale=0.92, wind=1.2)
        tag("")
        Pen.mode = "fill"

        def fs(cc):
            M.rider(cc, 560, 870, 0.8, -1, "sohrab", t, rp, gait="gallop", phase=t * 2.2, rider_scale=0.92, wind=1.2)
            es(cc)
        an.figures(c, fs, COLT, (0, 100, 1080, 1000), alpha=140)
        trail(c, 560, 860, lt3, t, 1.0, 1)
        c.restore()
        for k in range(3):
            u = (lt3 * 1.3 + k * 0.37) % 1.0
            if lt3 < L[4][0] + 1.0:
                arrow(c, -80, 380 + 90 * k, 1300, 300 + 120 * k, u, 0.7)
        vig(an, c, 150)

    cuts(c, lt, [(0.0, archer), (c1, rain), (c2, charge)], 0.35)


# ------------------------------------------------------------------ S06 the clash: lifted out of the saddle
def p17_s06(an, c, t):
    """'Gordafarid hung her bow on her arm and lowered her spear. But Sohrab came at her like a leopard. His spear
    struck her belt, tore her armour... and lifted her out of the saddle like a ball!' -- 'Not yet!' She draws her
    sword, cuts his spear in two and drops back into the saddle. -- 'What?!'"""
    lt, dur = loc(an, "S06", t)
    L = [LN("p17", "S06", k) for k in range(7)]
    c1 = L[1][0] - 0.3
    c2 = L[2][0] - 0.6

    def swap():
        focus = (520, 660)
        zoom = 1.02 + 0.05 * ease(lt / (c1 + 0.3))
        sling = sstep(0.3, 1.2, lt)
        take = sstep(1.3, 2.0, lt)
        couch = sstep(2.4, 3.6, lt)
        if take < 0.5:
            rp = {"hand_kind": "bow" if sling < 0.6 else "fist", "hand": (mix(70, 20, sling), mix(-300, -430, sling)),
                  "rhand": (-20, -280), "head": 2 + math.sin(t * 0.7), "wind": 0.8}
        else:
            rp = M.lance_pose(couch, {"head": 2 - 3 * couch + math.sin(t * 0.7), "lean": 4 * couch, "wind": 0.9})

        def setf(cam):
            her_set(an, c, t, cam, "f176", fs=0.34, fx=-170, fy=600, host_x=720, gy=SG - 120)
        duo(an, c, t, focus, zoom, setf, G=(380, SG, 0.82, 1, gh(rp, t)))
        vig(an, c, 150)

    def charge():
        lt2 = lt - c1
        focus = (540, 700)
        zoom = 1.0 + 0.04 * ease(lt2 / (c2 - c1 + 0.6))
        run = clamp(lt2 / 3.2)
        gx = 200 + 120 * run
        sx = 980 - 300 * run

        def setf(cam):
            her_set(an, c, t, cam, "f176b", fs=0.5, fx=-10, fy=500, host_x=690)

        def es(cc):
            shield(cc, A("s:rhand"), 26 * zoom, STUCK[:3], -1)
        duo(an, c, t, focus, zoom, setf, G=(gx, GY + 2, 0.46, 1, gh(M.lance_pose(1.0, {"lean": 6, "wind": 0.9}), t, gait="gallop", phase=t * 2.1)),
            Sd=(sx, GY, 0.48, -1, colt(p_shieldup(t, 0.4, 0.0, 1.0, 9), t, "gallop", t * 2.2)), es=es, anchors=True)
        trail(c, gx, GY, lt2, t, 1.0, -1, 0)
        trail(c, sx, GY, lt2, t, 1.0, 1, 5)
        vig(an, c, 140)

    def clash():
        lt3 = lt - c2
        hit = L[2][0] + 0.45
        lift0, lift1 = L[3][0] + 0.1, L[3][0] + 1.3
        cut_t = L[5][0] + 0.35
        drop1 = cut_t + 0.9
        focus = (560, 640)
        zoom = 1.0 + 0.05 * ease(lt3 / (dur - c2))
        shake = 7 * math.sin(lt * 61) * math.exp(-max(0.0, lt - hit) * 6) * (lt > hit)
        shake += 6 * math.sin(lt * 57) * math.exp(-max(0.0, lt - cut_t) * 7) * (lt > cut_t)
        c.save()
        c.translate(shake, shake * 0.4)
        gx, gs, ss = 330, 0.76, 0.8
        run = clamp((lt - c2) / (hit - c2))
        sx = mix(1250, 820, run)
        lift = (sstep(lift0, lift1, lt) - sstep(cut_t, drop1, lt)) * 150
        tilt = (sstep(lift0, lift1, lt) - sstep(cut_t, drop1, lt)) * -16
        draw_sw = sstep(L[4][0] - 0.3, L[4][0] + 0.3, lt)
        slash = sstep(cut_t - 0.25, cut_t + 0.1, lt)
        broken = lt >= cut_t
        rrG = 18 * math.sin(clamp((lt - lift0) / 1.4) * math.pi) if lift0 < lt < lift0 + 1.4 else 0.0
        stare = sstep(L[6][0] - 0.3, L[6][0] + 0.2, lt)
        rpG = {"hand_kind": "sword" if draw_sw > 0.4 else "fist", "sword": mix(-40, 120, slash),
               "hand": (mix(mix(110, 60, draw_sw), 170, slash), mix(mix(-320, -560, draw_sw), -400, slash)),
               "rhand": (mix(40, 90, sstep(lift0, lift1, lt)), mix(-300, -340, sstep(lift0, lift1, lt))),
               "rhand_kind": "fist", "head": 4 - 8 * draw_sw + 6 * sstep(lift0, lift1, lt) * (1 - draw_sw) + math.sin(t * 0.8),
               "lean": -4 * slash + 6 * draw_sw, "jaw": jaw(an, "GORDAFARID", t, 8), "stance": (40, 30), "wind": 1.0}
        if lt < lift0 - 0.4:
            rpG = M.lance_pose(1.0, {"head": 2, "lean": 4, "wind": 0.9})
            if lt > hit:
                rpG.update(hand=(mix(112, 60, sstep(hit, hit + 0.4, lt)), -330), lance=mix(84, 30, sstep(hit, hit + 0.4, lt)))
        rpS = {"hand_kind": "fist", "hand": (150, -340), "rhand": (30, -560), "rhand_kind": "fist",
               "head": 2 + 8 * stare + math.sin(t * 0.8), "lean": 8 * (1 - stare) - 4 * stare, "jaw": jaw(an, "SOHRAB", t, 9),
               "wind": 0.9}
        moving = lt < hit + 0.3
        PS = colt(rpS, t, "gallop" if moving else "stand", t * 2.2)
        lifted_now = lift > 1

        def eg(cc):
            if lifted_now:
                with Cam(cc, focus, zoom)(1.0):
                    tag("gl:")
                    lifted(cc, gx, SG, gs, 1, rpG, lift, tilt, t, GORD_HID)
                    tag("")
            if lt > hit - 0.6 and not broken:
                pass

        def es(cc):
            shield(cc, A("s:rhand"), 44 * zoom, STUCK[:3], -1)
            a = A("s:hand")
            if a is None:
                return
            belt = waist("gl:" if lifted_now else "g:", gs * zoom)
            if lt < hit or belt is None:
                tip = P16.along(a, 182, 470)
            else:
                tip = (belt[0] + 46 * gs * zoom, belt[1] + 4)
            d = math.hypot(tip[0] - a[0], tip[1] - a[1]) or 1
            ux, uy = (tip[0] - a[0]) / d, (tip[1] - a[1]) / d
            butt = (a[0] - ux * 190, a[1] - uy * 190)
            if not broken:
                sag = -26 * sstep(lift0, lift1, lt) * (1 + 0.15 * math.sin(lt * 30))
                P16.pole(cc, butt, tip, 6.5, sag)
            else:
                mid = (a[0] + ux * d * 0.45, a[1] + uy * d * 0.45)
                P16.pole(cc, butt, mid, 6.5, 0, head=False)
                u = clamp((lt - cut_t) / 1.1)
                fx_ = mix(mid[0] + ux * d * 0.3, mid[0] - 60, u)
                fy_ = mix(mid[1], SG - 116, u * u)
                ang = math.atan2(uy, ux) + 2.6 * u
                p0 = (fx_ - math.cos(ang) * d * 0.28, fy_ - math.sin(ang) * d * 0.28)
                p1 = (fx_ + math.cos(ang) * d * 0.28, fy_ + math.sin(ang) * d * 0.28)
                P16.pole(cc, p0, p1, 6.5, 0)

        def setf(cam):
            P16.clash_set(an, c, t, cam, "f176c")
        G = (gx, SG, gs, 1, gh(rpG, t, look=None if lifted_now else GORD_HID, rear=rrG, wind=0.9))
        duo(an, c, t, focus, zoom, setf, G=G, Sd=(sx, SG, ss, -1, PS), eg=eg, es=es, anchors=True, box=(0, 100, 1080, 1100))
        if hit <= lt < hit + 1.0:
            b = waist("g:", gs * zoom)
            if b:
                for k in range(6):
                    u = (lt - hit) / 1.0
                    ang = -0.6 + k * 0.5
                    c.drawCircle(b[0] + math.cos(ang) * 120 * u, b[1] + math.sin(ang) * 80 * u + 140 * u * u, 4.5 * (1 - u) + 1,
                                 paint(C(*INK)))
        if broken:
            P16.dust_puff(c, 700, SG - 130, t, cut_t + 1.0, lt, 0.6)
        if lt < hit + 0.3:
            trail(c, sx, SG - 120, lt3, t, 1.0 - run * 0.5, 1)
        P16.dust_puff(c, 560, SG - 150, t, hit, lt, 0.7)
        c.restore()
        vig(an, c, 150)

    cuts(c, lt, [(0.0, swap), (c1, charge), (c2, clash)], 0.35)


# ------------------------------------------------------------------ S07 she flees; the helmet
def p17_s07(an, c, t):
    """'But she knew she could not beat him. She turned and raced for the fortress.' -- 'Run if you can! You will not
    escape me!' -- 'Sohrab flew after her. Closer... and closer...' -- 'He reached out, and pulled the helmet from her
    head.'"""
    lt, dur = loc(an, "S07", t)
    L = [LN("p17", "S07", k) for k in range(4)]
    c1 = L[1][0] - 0.3
    c2 = L[2][0] - 0.3

    def wheel():
        focus = (540, 700)
        zoom = 1.0 + 0.04 * ease(lt / (c1 + 0.3))
        turn = lt > 2.0
        rr = 22 * math.sin(clamp((lt - 1.4) / 1.2) * math.pi) if 1.4 < lt < 2.6 else 0.0
        run = clamp((lt - 2.4) / 3.0)
        gx = 360 - 700 * run * run
        go = clamp((lt - 3.6) / 2.0)
        sx = 760 - 300 * go * go
        throw = sstep(0.6, 1.1, lt)
        rpG = {"hand_kind": "sword", "sword": 10, "hand": (100, -340), "rhand": (-10, -300), "head": 2 + math.sin(t * 0.8),
               "lean": 6 * run, "wind": 1.0}
        rpS = {"hand_kind": "fist", "hand": (mix(150, 230, throw), mix(-340, -420, throw)), "rhand": (30, -300),
               "head": 2 + math.sin(t * 0.8), "lean": 6 * go, "wind": 1.0}

        def setf(cam):
            her_set(an, c, t, cam, "f177", fs=0.42, fx=-60, fy=560, host_x=720)
        gp = gh(rpG, t, gait="gallop" if run > 0 else "stand", phase=t * 2.2, rear=rr)

        def es(cc):
            if throw < 1:
                a = A("s:hand")
                if a:
                    P16.pole(cc, (a[0] + 60, a[1] + 30), (a[0] - 120, a[1] - 20), 6, 0, head=False)
            else:
                u = clamp((lt - 1.1) / 0.8)
                x0, y0 = 760 + 140, 560
                P16.pole(cc, (x0 + 260 * u, y0 + 300 * u * u), (x0 + 260 * u + 150, y0 + 300 * u * u + 60 * u), 6, 0, head=False)
        duo(an, c, t, focus, zoom, setf, G=(gx, GY, 0.5, -1 if turn else 1, gp),
            Sd=(sx, GY, 0.52, -1, colt(rpS, t, "gallop" if go > 0 else "stand", t * 2.1)), es=es, anchors=True)
        if run > 0:
            trail(c, gx, GY, lt, t, run, 1, 0)
        if go > 0:
            trail(c, sx, GY, lt, t, go, 1, 4)
        vig(an, c, 140)

    def solo():
        lt2 = lt - c1
        gallop_bg(an, c, t, lt2, "sc177")
        c.save()
        c.translate(0, 70)
        reach = sstep(L[1][0], L[1][0] + 0.6, lt)
        rp = {"hand_kind": "open", "hand": (mix(150, 220, reach), mix(-340, -450, reach)), "rhand": (40, -300),
              "head": 2 + 2 * math.sin(t * 9) + math.sin(t * 0.8), "lean": 10, "jaw": jaw(an, "SOHRAB", t, 9), "wind": 1.3}

        def fs(cc):
            M.rider(cc, 560, 870, 0.8, -1, "sohrab", t, rp, gait="gallop", phase=t * 2.2, rider_scale=0.92, wind=1.2)
        an.figures(c, fs, COLT, (0, 100, 1080, 1000), alpha=140)
        trail(c, 560, 860, lt2, t, 1.0, 1)
        c.restore()
        vig(an, c, 150)

    def two():
        lt3 = lt - c2
        grab = L[3][0] + 1.5
        g = clamp((lt - c2) / (grab - c2))
        sx = mix(1080, 585, ease(g))
        gx = 330 + 8 * math.sin(lt * 1.3)
        off = lt >= grab
        reach = sstep(L[3][0] + 0.2, grab, lt)
        pull = sstep(grab, grab + 0.6, lt)
        rpG = {"hand_kind": "sword", "sword": 20, "hand": (100, -340), "rhand": (-10, -300),
               "head": 4 + (math.sin(t * 0.8) if not off else -10 * pull), "lean": 10, "wind": 1.3}
        rpS = {"hand_kind": "open" if not off else "fist", "hand": (mix(mix(150, 300, reach), 150, pull), mix(mix(-340, -540, reach), -520, pull)),
               "rhand": (40, -300), "head": 2 + math.sin(t * 0.8) + 4 * reach, "lean": 10 + 6 * reach * (1 - pull), "wind": 1.3}
        gallop_bg(an, c, t, lt3, "sc177b", 520)
        c.save()
        c.translate(0, 70)

        def eg(cc):
            pass

        def es(cc):
            if off:
                a = A("s:hand")
                if a:
                    P16.helmet_at(cc, a[0] - 4, a[1] + 18, 0.66 * 0.92, t, -1, 1.3)

        def fg(cc):
            M.rider(cc, gx, 870, 0.66, -1, GORD_BARE if off else GORD_HID, t, rpG, gait="gallop", phase=t * 2.3, wind=1.3)

        def fs(cc):
            tag("s:")
            M.rider(cc, sx, 870, 0.68, -1, "sohrab", t, rpS, gait="gallop", phase=t * 2.2 + 0.3, rider_scale=0.92, wind=1.3)
            tag("")
            es(cc)
        ANCH.clear()
        Pen.mode = "anchor"
        fs(c)
        Pen.mode = "fill"
        an.figures(c, fg, MORN, (0, 100, 1080, 1000))
        an.figures(c, fs, COLT, (0, 100, 1080, 1000), alpha=150)
        trail(c, gx, 860, lt3, t, 1.0, 1, 0)
        trail(c, sx, 860, lt3, t, 1.0, 1, 4)
        c.restore()
        vig(an, c, 150)

    cuts(c, lt, [(0.0, wheel), (c1, solo), (c2, two)], 0.35)


# ------------------------------------------------------------------ S08 + END: a girl
def her_close(an, c, t, lt, dur, key, rp, sun=1.0, zk=0.07, cyp=0.0, eg=None):
    """Gordafarid bare-headed on her horse in close-up, her hair in the wind, light behind her face ('her face shone
    like the sun'); cyp > 0 shows a cypress on the rise behind her."""
    focus = (420, 600)
    zoom = 1.0 + zk * ease(lt / dur)

    def setf(cam):
        her_set(an, c, t, cam, key, fs=None, host_x=760, gy=1400 - 380)
        if cyp > 0:
            with cam(0.5):
                c.saveLayerAlpha(None, int(255 * cyp))
                for k, (x, h) in enumerate(((800, 230), (868, 290), (930, 210))):
                    sw = 3 * math.sin(t * 0.8 + k)
                    w = h * 0.15
                    c.drawPath(spath([(x - 5, 846, 0), (x - w, 846 - h * 0.2), (x - w * 0.9, 846 - h * 0.55),
                                      (x - w * 0.5 + sw * 0.5, 846 - h * 0.82), (x + sw, 846 - h, 0),
                                      (x + w * 0.5 + sw * 0.5, 846 - h * 0.82), (x + w * 0.9, 846 - h * 0.55),
                                      (x + w, 846 - h * 0.2), (x + 5, 846, 0)]), paint(C(96, 90, 104)))
                c.restore()
        with cam(1.0):
            sun_head(c, 380 + 60 * 1.25, 1400 - 640 * 1.25, sun, t, 130)
    duo(an, c, t, focus, zoom, setf, G=(380, 1400, 1.25, 1, gh(rp, t, look=GORD_BARE, wind=1.2)), box=(0, 0, 1080, 1500),
        eg=(lambda cc: eg(cc, zoom)) if eg else None, anchors=eg is not None)
    vig(an, c, 150)


def him_close(an, c, t, lt, dur, key, rp, helm=True, zk=0.06, extra=None):
    """Sohrab on his colt in close-up (her helmet in his hand when helm), the host far behind."""
    focus = (640, 600)
    zoom = 1.0 + zk * ease(lt / dur)

    def setf(cam):
        her_set(an, c, t, cam, key, fs=None, host_x=60, gy=1400 - 380)

    def es(cc):
        a = A("s:hand")
        if helm and a:
            P16.helmet_at(cc, a[0] - 4, a[1] + 30, 1.2 * zoom * 0.92, t, -1, 0.9)
        if extra:
            extra(cc)
    duo(an, c, t, focus, zoom, setf, Sd=(720, 1400, 1.2, -1, colt(rp, t)), es=es, anchors=True, box=(0, 0, 1080, 1500),
        sa=170)
    vig(an, c, 150)


def p17_s08(an, c, t):
    """'Her long hair fell loose, and her face shone like the sun.' Sohrab, her helmet in his hand: 'A girl?! The warrior
    who fought me like a lion... is a girl?' -- 'And now she was alone on the plain... face to face with Sohrab.'"""
    lt = t - an.start["S08"]
    dur = an.end["END"] - an.start["S08"]
    L = [LN("p17", "S08", k) for k in range(4)]
    c1 = L[1][0] - 0.4
    c2 = L[3][0] - 0.5

    def her():
        look = sstep(1.0, 2.2, lt)
        rp = {"hand_kind": "sword", "sword": 20, "hand": (90, -330), "rhand": (-10, -300),
              "head": 6 - 10 * look + math.sin(t * 0.7), "wind": 1.2}
        her_close(an, c, t, lt, c1 + 0.4, "f178", rp, sstep(0.0, 1.4, lt))

    def him():
        lt2 = lt - c1
        low = sstep(L[2][1] - 0.6, L[2][1] + 0.6, lt)
        tilt = sstep(L[1][0] - 0.1, L[1][0] + 0.3, lt)
        rp = {"hand_kind": "fist", "hand": (mix(210, 180, low), mix(-590, -480, low)), "rhand": (30, -300),
              "head": 4 + 8 * tilt - 6 * low + math.sin(t * 0.7), "jaw": jaw(an, "SOHRAB", t, 8), "wind": 0.9}
        him_close(an, c, t, lt2, c2 - c1 + 0.5, "f178b", rp)

    def alone():
        lt3 = lt - c2
        focus = (540, 640)
        zoom = 1.0 + 0.1 * ease(lt3 / (dur - c2))
        rpG = {"hand_kind": "sword", "sword": 20, "hand": (90, -330), "rhand": (-10, -300), "head": 2 + math.sin(t * 0.7),
               "wind": 1.2}
        rpS = {"hand_kind": "fist", "hand": (150, -420), "rhand": (30, -300), "head": 4 + math.sin(t * 0.7), "wind": 0.9}

        def setf(cam):
            her_set(an, c, t, cam, "f178c", fs=0.42, fx=-60, fy=560, host_x=720)

        def es(cc):
            a = A("s:hand")
            if a:
                P16.helmet_at(cc, a[0] - 3, a[1] + 14, 0.52 * zoom * 0.92, t, -1, 0.9)
        duo(an, c, t, focus, zoom, setf, G=(330, GY, 0.5, 1, gh(rpG, t, look=GORD_BARE, wind=1.2)),
            Sd=(770, GY, 0.52, -1, colt(rpS, t)), es=es, anchors=True)
        vig(an, c, 150)

    cuts(c, lt, [(0.0, her), (c1, him), (c2, alone)], 0.45)


P17 = {"S01": p17_s01, "TITLE": p17_s01, "S02": p17_s02, "S03": p17_s03, "S04": p17_s04, "S05": p17_s05,
       "S06": p17_s06, "S07": p17_s07, "S08": p17_s08, "END": p17_s08}
SHIFT17 = {}

register(P17, SHIFT17)
