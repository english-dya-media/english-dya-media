"""Parts 5-6 (row 3 of OUTLINE.md, "Tahmineh"): every shot as a shadow-play scene.

Importing this module registers part 5's shots; p06_scenes.py imports it and registers part 6's.
Shared sets: Rostam's bedchamber (door that opens, bed, a sit-up pose), the moonlit corridor,
Samangan at night, the candle-lit curtain with shadow stories, the moon window, the king's room.
"""
import math, random
import skia
import anim
from anim import C, mix, mixc, clamp, ease, sstep, _k, Cam, Pen, ANCH, rope, spath, ppath, paint, fillp, W, H
import puppets
from puppets import person, horse, LOOKS
import sets as S
from ep01_scenes import loc, jaw, get, vig, tag, A, ground, INK

TAHM = dict(LOOKS["tahmineh"], hair=True)          # veil with a small crown, long tresses showing
WARM = (255, 182, 104)                             # candle light
MOON = (176, 200, 255)                             # moonlight rim


# ------------------------------------------------------------------ props and helpers
def candle_light(c, an, name, t, r=520, a=120, seed=3.0, s=0.26):
    """Glow and flame at a puppet's 'flame' anchor (needs figures(..., anchors=True))."""
    p = A(name)
    if not p:
        return None
    fl = 0.86 + 0.1 * math.sin(t * 8 + seed) + 0.05 * math.sin(t * 17 + seed)
    S.glow(c, p[0], p[1], r, (255, 170, 80), a * fl)
    S.flame(c, p[0], p[1] + 10, s, t, seed)
    return p


def standing_candle(c, x, y, t, s=1.0, seed=1.0, glow=True):
    """A tall candle on a stand (drawn as a plain silhouette, then the flame)."""
    pt = paint(C(*INK))
    c.drawPath(spath([(x - 40 * s, y, 0), (x - 10 * s, y - 20 * s), (x - 6 * s, y - 230 * s, 0), (x + 6 * s, y - 230 * s, 0),
                      (x + 10 * s, y - 20 * s), (x + 40 * s, y, 0)]), pt)
    c.drawPath(spath([(x - 30 * s, y - 230 * s, 0), (x + 30 * s, y - 230 * s, 0), (x + 20 * s, y - 244 * s, 0),
                      (x - 20 * s, y - 244 * s, 0)]), pt)
    c.drawRect(skia.Rect.MakeLTRB(x - 9 * s, y - 300 * s, x + 9 * s, y - 244 * s), paint(C(240, 214, 170)))
    fl = 0.86 + 0.1 * math.sin(t * 8 + seed) + 0.05 * math.sin(t * 17 + seed)
    if glow:
        S.glow(c, x, y - 320 * s, 620 * s, (255, 170, 80), 130 * fl)
    S.flame(c, x, y - 298 * s, 0.34 * s, t, seed)


def mace_at(cc, x, y, ang, s, t):
    """A mace lying or leaning on its own (puppet pen)."""
    cc.save()
    cc.translate(x, y)
    cc.scale(s, s)
    puppets.prop(cc, "mace", (0, 0), 0.0, {"mace": ang}, t)
    cc.restore()


def in_bed(cc, t, hx, hy, s, ang, P, look="rostam_robe", face=-1):
    """Upper body of a person sitting up in bed, hips at (hx, hy); ang 0 = upright,
    ~84 = lying back on the pillow (behind the person). The legs are left to the blanket."""
    cc.save()
    cc.translate(hx, hy)
    cc.rotate(ang * -face)
    cc.clipRect(skia.Rect.MakeLTRB(-3000, -3000, 3000, 14 * s))
    fx = (-230 * s, -24 * s) if face < 0 else (24 * s, 230 * s)
    cc.clipRect(skia.Rect.MakeLTRB(fx[0], -48 * s, fx[1], 60 * s), skia.ClipOp.kDifference)
    cc.translate(-hx, -hy)
    person(cc, hx, hy + 62 * s, s, face, dict(P, mode="sit"), t, look)
    cc.restore()


def bed(cc, x0, x1, ytop, ybot, pillow="right"):
    """Low bed: frame, legs, mattress, a pillow at one end."""
    fillp(cc, spath([(x0, ybot, 0), (x0, ytop + 14), (x0 + 16, ytop, 0), (x1 - 16, ytop, 0), (x1, ytop + 14),
                     (x1, ybot, 0)]))
    for x in (x0 + 6, x1 - 20):
        fillp(cc, ppath([(x, ybot - 4), (x + 14, ybot - 4), (x + 16, ybot + 10), (x - 2, ybot + 10)]))
    if pillow == "right":
        fillp(cc, spath([(x1 - 110, ytop + 4), (x1 - 104, ytop - 26), (x1 - 60, ytop - 34), (x1 - 14, ytop - 24),
                         (x1 - 8, ytop + 4)]))
    else:
        fillp(cc, spath([(x0 + 110, ytop + 4), (x0 + 104, ytop - 26), (x0 + 60, ytop - 34), (x0 + 14, ytop - 24),
                         (x0 + 8, ytop + 4)]))


def blanket(cc, xh, xf, ytop, s, knee=0.0):
    """Blanket over the legs from the hips (xh) to the feet (xf); knee raises a bump."""
    d = 1 if xf > xh else -1
    L = abs(xf - xh)
    fillp(cc, spath([(xh, ytop + 6, 0), (xh, ytop - 52 * s), (xh + d * L * 0.3, ytop - (44 + 30 * knee) * s),
                     (xh + d * L * 0.62, ytop - (36 + 50 * knee) * s), (xh + d * L * 0.9, ytop - 40 * s),
                     (xf + d * 14, ytop - 18 * s), (xf + d * 26, ytop + 6, 0)]))


def wall_panel(c, x0, x1, y0, y1, col0=(96, 54, 50), col1=(156, 96, 72), fold=74):
    """A warm lit curtain behind beds and people (so silhouettes read), with soft vertical folds."""
    S.lin(c, y0, y1, [(0, col0), (1, col1)], (x0, y0, x1, y1))
    p = skia.Paint(AntiAlias=True)
    p.setShader(skia.GradientShader.MakeLinear([skia.Point(x0, 0), skia.Point(x0 + fold, 0)],
                                               [C(40, 16, 20, 120), C(255, 220, 180, 26), C(40, 16, 20, 120)],
                                               [0.0, 0.5, 1.0], skia.TileMode.kRepeat))
    c.drawRect(skia.Rect.MakeLTRB(x0, y0, x1, y1), p)
    c.drawRect(skia.Rect.MakeLTRB(x0 - 10, y0 - 12, x1 + 10, y0 + 4), paint(C(*INK)))


def door(c, x, yb, w, h, u, glow=0.0, t=0.0):
    """Arched door; u = how far it is open (0..1). Through it: the moonlit corridor."""
    arch = S.arch_path(x, yb, w, h)
    c.save()
    c.clipPath(arch, skia.ClipOp.kIntersect, True)
    S.lin(c, yb - h, yb, [(0, (40, 54, 96)), (0.7, (66, 82, 124)), (1, (84, 96, 132))], (x - w, yb - h - 20, x + w, yb))
    # the corridor beyond: a far pillar and a moonlit window
    c.drawRect(skia.Rect.MakeLTRB(x - w * 0.18, yb - h, x - w * 0.08, yb), paint(C(20, 22, 40)))
    c.drawPath(S.arch_path(x + w * 0.2, yb - h * 0.3, w * 0.28, h * 0.45), paint(C(120, 140, 190)))
    if glow > 0:
        S.glow(c, x, yb - h * 0.45, w * 1.2, (255, 170, 90), 220 * glow)
    lw = w * (1 - 0.88 * ease(u))
    if lw > 1:
        x0 = x - w / 2
        c.drawRect(skia.Rect.MakeLTRB(x0, yb - h - 20, x0 + lw, yb), paint(C(28, 17, 20)))
        for k in range(1, 4):
            xx = x0 + lw * k / 4
            c.drawRect(skia.Rect.MakeLTRB(xx - 1.5, yb - h, xx + 1.5, yb), paint(C(14, 8, 10)))
        for yy in (yb - h * 0.25, yb - h * 0.62):
            c.drawRect(skia.Rect.MakeLTRB(x0, yy - 5, x0 + lw, yy + 5), paint(C(14, 8, 10)))
            for k in range(4):
                c.drawCircle(x0 + lw * (k + 0.5) / 4, yy, 3, paint(C(120, 90, 60, 160)))
    c.restore()
    edge = skia.Paint(AntiAlias=True, Color=C(*INK))
    edge.setStyle(skia.Paint.kStroke_Style)
    edge.setStrokeWidth(16)
    c.drawPath(arch, edge)
    if u > 0.02:
        # light spilling from the door across the floor
        a = 70 * ease(u) + 60 * glow
        p = skia.Paint(AntiAlias=True)
        p.setShader(skia.GradientShader.MakeLinear([skia.Point(0, yb), skia.Point(0, yb + 260)],
                                                   [C(150, 160, 200, a), C(150, 160, 200, 0)]))
        c.drawPath(ppath([(x - w / 2, yb), (x + w / 2, yb), (x + w * 1.6, yb + 260), (x - w * 0.2, yb + 260)]), p)


def room(an, c, t, cam, u=0.0, glow=0.0, lamp=1.0, bedx=(600, 1060)):
    """Rostam's bedchamber: dark walls, door on the left, warm curtain behind the bed, a hanging lamp."""
    with cam(0.7):
        S.lin(c, 0, H, [(0, (14, 10, 22)), (0.4, (32, 20, 32)), (0.6, (26, 16, 24)), (1, (6, 3, 5))])
        wall_panel(c, bedx[0] - 50, bedx[1] + 60, 520, 800)
        c.drawRect(skia.Rect.MakeLTRB(-200, 120, 1300, 150), paint(C(*INK)))
        for i in range(16):
            c.drawPath(spath([(i * 80 - 40, 150, 0), (i * 80, 192), (i * 80 + 40, 150, 0)]), paint(C(*INK)))
        for x in (bedx[0] - 70, bedx[1] + 80):
            c.drawRect(skia.Rect.MakeLTRB(x - 22, 150, x + 22, 862), paint(C(*INK)))
        if lamp > 0:
            S.hanging_lamp(c, (bedx[0] + bedx[1]) / 2 + 40, 330, 0.9, t, 180, 1.0)
            S.glow(c, (bedx[0] + bedx[1]) / 2, 700, 520, (255, 160, 80), 50 * lamp)
    with cam(0.85):
        door(c, 190, 862, 230, 480, u, glow, t)
    with cam(1.0):
        ground(c, 862, (34, 20, 24))


def bedroom_figs(cc, t, ang, P, hx=800, ytop=784, s=0.86, knee=0.0, x0=600, x1=1060, mace=None, ybot=None):
    """Bed + Rostam (lying back at ang ~84, sitting at 0) + blanket; optional leaning mace."""
    if mace:
        mace_at(cc, *mace, t)
    in_bed(cc, t, hx, ytop - 4, s, ang, P)
    bed(cc, x0, x1, ytop, ybot if ybot is not None else ytop + 80 * max(1.0, s), "right")
    blanket(cc, hx + 6, x0 + 30, ytop, s, knee)


# ------------------------------------------------------------------ corridor and city
def corridor(an, c, t, cam, pan=0.0, door_x=None, door_u=0.0):
    """Moonlit arcade of the palace (as in part 4), scrolling with pan."""
    S.lin(c, 0, H, [(0, (8, 8, 18)), (0.5, (16, 16, 32)), (1, (4, 3, 6))])
    pt = paint(C(*INK))
    with cam(0.8):
        off = (pan * 0.8) % 370
        for k in range(-1, 5):
            x = 170 + k * 370 - off
            c.drawPath(S.arch_path(x, 620, 170, 380), paint(C(70, 90, 140)))
            p = skia.Paint(AntiAlias=True)
            p.setShader(skia.GradientShader.MakeLinear([skia.Point(0, 620), skia.Point(0, 870)],
                                                       [C(120, 140, 200, 70), C(120, 140, 200, 0)]))
            c.drawPath(ppath([(x - 85, 620), (x + 85, 620), (x + 190, 870), (x + 20, 870)]), p)
            c.drawRect(skia.Rect.MakeLTRB(x + 185 - 40, 150, x + 185 + 40, 900), pt)
        c.drawRect(skia.Rect.MakeLTRB(-100, 100, 1200, 200), pt)
    with cam(1.0):
        ground(c, 866, (20, 18, 30))
        if door_x is not None:
            dx = door_x - pan
            c.drawPath(S.arch_path(dx, 866, 170, 340), paint(C(30, 18, 20)))
            edge = skia.Paint(AntiAlias=True, Color=C(*INK))
            edge.setStyle(skia.Paint.kStroke_Style)
            edge.setStrokeWidth(12)
            c.drawPath(S.arch_path(dx, 866, 170, 340), edge)
            c.drawRect(skia.Rect.MakeLTRB(dx - 80, 860, dx + 80, 866), paint(C(255, 180, 100, 90)))


def night_sky(an, c, t, cam, key, moon=(780, 430, 70)):
    S.lin(c, 0, 900, [(0, (6, 8, 24)), (0.5, (20, 26, 62)), (1, (46, 50, 90))])
    with cam(0.2):
        get(an, key + "st", lambda: S.Stars(200, 800, 31)).draw(c, t, 1.0, 800)
        S.moon(c, *moon)
        get(an, key + "cl", lambda: S.Clouds([(380, 12), (470, 9), (560, 14)], 33, 300, 600)).draw(c, t * 2.0, (30, 34, 60), 190)


def palace(c, x, yb, t, lit=1.0):
    """The king's palace in the middle of the city: a great dome and a tall lit window."""
    pt = paint(C(*INK))
    c.drawRect(skia.Rect.MakeLTRB(x - 210, yb - 330, x + 210, yb), pt)
    c.drawPath(spath([(x - 170, yb - 330, 0), (x - 160, yb - 430), (x - 90, yb - 520), (x, yb - 548, 0), (x + 90, yb - 520),
                      (x + 160, yb - 430), (x + 170, yb - 330, 0)]), pt)
    c.drawRect(skia.Rect.MakeLTRB(x - 3, yb - 600, x + 3, yb - 546), pt)
    c.drawCircle(x, yb - 606, 9, pt)
    for sx in (-1, 1):
        mx = x + sx * 250
        c.drawRect(skia.Rect.MakeLTRB(mx - 26, yb - 470, mx + 26, yb), pt)
        c.drawPath(ppath([(mx - 34, yb - 470), (mx, yb - 530), (mx + 34, yb - 470)]), pt)
    for k in range(-3, 4):
        if k:
            c.drawPath(S.arch_path(x + k * 52, yb - 60, 22, 46), paint(C(255, 180, 100, 150 if abs(k) % 2 else 90)))
    win = S.arch_path(x, yb - 120, 120, 200)
    c.save()
    c.clipPath(win, skia.ClipOp.kIntersect, True)
    S.lin(c, yb - 320, yb - 120, [(0, (255, 170, 80)), (1, (255, 214, 140))], (x - 70, yb - 330, x + 70, yb - 110))
    c.restore()
    S.glow(c, x, yb - 220, 260, (255, 170, 80), 120 * lit)


def city_night(an, c, t, cam, key, show=0.0):
    """Samangan under the moon; show fades in a woman's silhouette in the palace window."""
    night_sky(an, c, t, cam, key)
    img, lights = get(an, key + "city", lambda: S.city(1500, 900, 880, 24, INK, True, None))
    with cam(0.6):
        c.drawImage(img, -200, 0)
        for k, (x, y) in enumerate(lights):
            if k % 3 == 0:
                a = 150 + 60 * math.sin(t * 2 + k)
                c.drawRect(skia.Rect.MakeXYWH(x - 200 - 4, y - 8, 8, 14), paint(C(255, 190, 110, a)))
    with cam(1.0):
        palace(c, 560, 880, t)
        if show > 0:
            c.save()
            c.clipPath(S.arch_path(560, 760, 120, 200), skia.ClipOp.kIntersect, True)
            c.saveLayerAlpha(None, int(255 * show))
            Pen.mode = "fill"
            person(c, 556, 790, 0.36, 1, {"hand": (40, -300), "hand_kind": "open", "rhand": (-30, -262), "head": 6}, t, TAHM)
            c.restore()
            c.restore()
        c.save()
        c.clipPath(S.arch_path(560, 760, 120, 200), skia.ClipOp.kIntersect, True)
        c.drawImage(get(an, "lat_pal", lambda: S.lattice(140, 90, 26, 4)), 490, 690)
        c.drawRect(skia.Rect.MakeLTRB(490, 684, 630, 692), paint(C(*INK)))
        c.restore()
        ground(c, 880, (10, 8, 14))


# ------------------------------------------------------------------ part 5 shots
def p5_s01(an, c, t):
    """Hook: the door is open, two women in the doorway; Rostam jolts up and grabs his mace."""
    lt = t - an.start["S01"]
    focus = (620, 640)
    zoom = 1.06 + 0.07 * ease(lt / 11.6)
    cam = Cam(c, focus, zoom)
    room(an, c, t, cam, u=1.0, glow=1.0, lamp=0.6)
    up = sstep(0.35, 1.0, lt)
    grab = sstep(1.0, 1.6, lt)
    ang = mix(84, 0, up)
    step = sstep(4.2, 5.6, lt)
    P = {"jaw": jaw(an, "ROSTAM", t, 6), "head": mix(8, 2, up) + 2 * math.sin(t * 0.8),
         "hand": (mix(40, 120, grab), mix(-262, -330, grab)), "hand_kind": "mace" if grab > 0.5 else "fist",
         "mace": mix(40, 10, grab), "rhand": (-40, -250), "lean": 6 * grab}

    def back(cc):
        with Cam(cc, focus, zoom)(0.85):
            tag("m:")
            person(cc, 128, 862, 0.6, 1, {"hand_kind": "candle", "hand": (96, -380), "head": -2}, t, "maid")
            tag("")
            person(cc, mix(262, 330, step), 862, 0.64, 1, {"mode": "walk" if 0 < step < 1 else "stand",
                                                        "phase": lt * 3.6, "stride": 14,
                                                        "hand": (60, -330), "hand_kind": "open",
                                                        "jaw": jaw(an, "TAHMINEH", t, 6), "wind": 0.3}, t, TAHM)
    an.figures(c, back, WARM, (0, 200, 1080, 1000), anchors=True)
    with cam(0.85):
        candle_light(c, an, "m:flame", t, 360, 110, 3.0, 0.2)

    def front(cc):
        with Cam(cc, focus, zoom)(1.0):
            bedroom_figs(cc, t, ang, P, hx=820, ytop=800, s=1.0, knee=0.4 * up, x0=560, x1=1080,
                         mace=None if grab > 0.5 else (1040, 842, -14, 0.95))
    an.figures(c, front, WARM, (0, 200, 1080, 1100))
    vig(an, c, 170)


def p5_s02(an, c, t):
    """Samangan under the moon; a woman appears in the lit palace window."""
    lt, dur = loc(an, "S02", t)
    focus = (560, 650)
    zoom = 1 + 0.32 * ease(lt / dur)
    cam = Cam(c, focus, zoom)
    city_night(an, c, t, cam, "c02", sstep(15.0, 16.5, lt))
    get(an, "mo02", lambda: S.Motes(40, 7, 300, 900)).draw(c, t, (200, 210, 255), 70, rise=2, drift=0.2)
    vig(an, c, 160)


def p5_s03(an, c, t):
    """The corridor: the maid with her candle and Tahmineh walk to Rostam's door."""
    lt, dur = loc(an, "S03", t)
    walk = clamp(lt / 9.6)
    wk = ease(walk) * 0.35 + walk * 0.65
    pan = -420 * wk
    focus = (540, 640)
    zoom = 1.08 + 0.06 * ease(lt / dur)
    cam = Cam(c, focus, zoom)
    corridor(an, c, t, cam, pan, door_x=-235)
    walking = lt < 9.6
    mx = mix(1000, 400, wk)
    tx = mx + 250
    turn = 10.1 < lt < 13.4
    reach = sstep(16.4, 17.4, lt)
    PM = {"mode": "walk" if walking else "stand", "phase": lt * 3.6, "stride": 15, "hand_kind": "candle",
          "hand": (mix(96, 120, reach), mix(-380, -330, reach)), "jaw": jaw(an, "MAID", t, 7),
          "head": -4 if turn else 0, "wind": 0.3}
    PT = {"mode": "walk" if walking else "stand", "phase": lt * 3.6 + 1.2, "stride": 15, "hand": (60, -330),
          "hand_kind": "open", "jaw": jaw(an, "TAHMINEH", t, 6), "wind": 0.3,
          "head": 2 + 4 * sstep(13.6, 14.2, lt) * (1 - sstep(16.4, 17.0, lt))}

    def figs(cc):
        with Cam(cc, focus, zoom)(1.0):
            tag("m:")
            person(cc, mx, 872, 0.92, 1 if turn else -1, PM, t, "maid")
            tag("")
            person(cc, tx, 872, 0.97, -1, PT, t, TAHM)
    an.figures(c, figs, WARM, (0, 200, 1080, 1100), anchors=True)
    candle_light(c, an, "m:flame", t, 560, 130, 3.0, 0.28)
    vig(an, c, 170)


def p5_s04(an, c, t):
    """Inside: the door opens, the maid comes in with the candle, then Tahmineh; Rostam sleeps."""
    lt, dur = loc(an, "S04", t)
    focus = (560, 640)
    zoom = 1.0 + 0.05 * ease(lt / dur)
    cam = Cam(c, focus, zoom)
    u = sstep(0.1, 1.2, lt)
    mw = clamp((lt - 1.5) / 6.2)
    mx = mix(150, 430, ease(mw))
    tw = clamp((lt - 7.6) / 4.4)
    tx = mix(130, 300, ease(tw))
    glow = sstep(0.5, 1.3, lt) * (1 - 0.6 * mw)
    room(an, c, t, cam, u=u, glow=glow, lamp=0.5)
    breath = 3 * math.sin(t * 1.4)
    P = {"head": 8 + breath * 0.3, "hand": (60, -280), "rhand": (-20, -270), "jaw": 0.0}

    def figs(cc):
        with Cam(cc, focus, zoom)(1.0):
            bedroom_figs(cc, t, 84 + breath * 0.2, P, hx=800, ytop=786, s=0.86, mace=(1046, 838, -14, 0.8))
            if lt > 1.25:
                tag("m:")
                person(cc, mx, 866, 0.8, 1, {"mode": "walk" if 0 < mw < 1 else "stand", "phase": lt * 3.4, "stride": 14,
                                             "hand_kind": "candle", "hand": (96, -380), "wind": 0.3}, t, "maid")
                tag("")
            if lt > 7.4:
                person(cc, tx, 866, 0.85, 1, {"mode": "walk" if 0 < tw < 1 else "stand", "phase": lt * 3.4 + 1.1,
                                              "stride": 14, "hand": (60, -330), "hand_kind": "open", "wind": 0.3,
                                              "head": 3}, t, TAHM)
    an.figures(c, figs, WARM, (0, 200, 1080, 1000), anchors=lt > 1.25)
    if lt > 1.25:
        candle_light(c, an, "m:flame", t, 520, 120, 3.0, 0.24)
    vig(an, c, 170)


def p5_s04b(an, c, t):
    """Close: Tahmineh in the candle light."""
    lt, dur = loc(an, "S04b", t)
    S.lin(c, 0, H, [(0, (16, 8, 12)), (0.45, (60, 30, 30)), (0.7, (40, 20, 22)), (1, (6, 3, 5))])
    wall_panel(c, 380, 1180, 260, 1100, (70, 36, 34), (130, 76, 60))
    S.glow(c, 860, 760, 700, (255, 160, 80), 90 + 10 * math.sin(t * 7))
    get(an, "mo04b", lambda: S.Motes(50, 4, 250, 1100)).draw(c, t, (255, 200, 140), 90, rise=5, drift=0.3)
    push = ease(lt / dur)
    P = {"hand": (70, -330), "hand_kind": "open", "head": 4 + 2 * math.sin(t * 0.7), "wind": 0.45, "rhand": (-30, -262),
         "lean": 2}

    def figs(cc):
        cc.save()
        cc.translate(-20 * push, -14 * push)
        person(cc, 430, 1560, 2.15 + 0.06 * push, 1, P, t, TAHM)
        cc.restore()
    an.figures(c, figs, WARM, (0, 0, 1080, 1600))
    vig(an, c, 170)


def p5_s05(an, c, t):
    """Two-shot: Rostam wakes and sits up; Tahmineh and the maid stand before him."""
    lt, dur = loc(an, "S05", t)
    focus = (560, 700)
    zoom = 1.0 + 0.05 * ease(lt / dur)
    cam = Cam(c, focus, zoom)
    with cam(0.7):
        S.lin(c, 0, H, [(0, (14, 10, 22)), (0.45, (34, 22, 34)), (1, (6, 3, 5))])
        wall_panel(c, 560, 1180, 330, 1060)
        door(c, 100, 1040, 300, 640, 1.0, 0.25, t)
        S.hanging_lamp(c, 760, 250, 1.2, t, 110, 2.0)
    up = sstep(1.0, 3.6, lt)
    praise = sstep(4.0, 4.6, lt) * (1 - sstep(5.8, 6.4, lt))
    ask = sstep(6.6, 7.1, lt)
    P = {"jaw": jaw(an, "ROSTAM", t, 7), "head": mix(-24, 6, up) - 4 * praise + 2 * math.sin(t * 0.7),
         "hand": (mix(40, 100, max(praise, ask)), mix(-262, -400 + 60 * ask, max(praise, ask))),
         "hand_kind": "open" if max(praise, ask) > 0.3 else "fist", "rhand": (-20, -250), "lean": -4 * praise}

    def figs(cc):
        with Cam(cc, focus, zoom)(1.0):
            tag("m:")
            person(cc, 120, 1110, 1.0, 1, {"hand_kind": "candle", "hand": (100, -380), "head": 2}, t, "maid")
            tag("")
            person(cc, 360, 1110, 1.12, 1, {"hand": (40, -270), "hand_kind": "open", "head": 4, "wind": 0.35,
                                            "rhand": (-30, -262)}, t, TAHM)
            bedroom_figs(cc, t, mix(84, 0, up), P, hx=900, ytop=1046, s=1.62, knee=0.5 * up, x0=600, x1=1320,
                         mace=(1050, 1090, -16, 1.4))
    an.figures(c, figs, WARM, (0, 150, 1080, 1300), anchors=True)
    candle_light(c, an, "m:flame", t, 640, 130, 3.0, 0.3)
    vig(an, c, 170)


def shadow_layer(c, bounds, alpha=0.86, col=(44, 20, 14), blur=2.2):
    """Begin a layer whose content lands as a soft cast shadow (end with c.restore())."""
    p = skia.Paint()
    p.setAlphaf(clamp(alpha))
    p.setColorFilter(skia.ColorFilters.Blend(C(*col), skia.BlendMode.kSrcIn))
    if blur:
        p.setImageFilter(skia.ImageFilters.Blur(blur, blur, skia.TileMode.kDecal, None))
    c.saveLayer(skia.Rect.MakeLTRB(*bounds), p)
    Pen.mode = "fill"


def eagle(cc, x, y, s, t, face=1, flap=1.0, speed=6.0):
    """An eagle in flight (puppet pen): hooked beak, broad fingered wings, fan tail, talons."""
    cc.save()
    cc.translate(x, y)
    cc.scale(s * face, s)
    f = math.sin(t * speed) * flap

    def wing(amp, dx):
        tip = (-70 + dx, -12 - 200 * amp)
        lead = anim.bez((34 + dx, -12), (24 + dx, -12 - 120 * amp), (-26 + dx, -12 - 180 * amp), tip, 9)
        trail = []
        for i in range(1, 8):
            u = i / 7
            trail.append((mix(tip[0], -36 + dx, u) + (12 if i % 2 else 0), mix(tip[1], 0, u ** 0.8) + (12 if i % 2 else 0), 0))
        fillp(cc, spath(lead + trail + [(0 + dx, 6), (40 + dx, -2)]))
    wing(0.8 * f, 16)
    fillp(cc, spath([(-60, -2), (-24, -18), (40, -16), (80, -10), (100, -22, 0), (116, -18), (124, -8, 0), (106, 0),
                     (80, 10), (30, 18), (-36, 14)]))
    fillp(cc, spath([(114, -16, 0), (134, -12), (138, 0, 0), (126, -4), (114, -2, 0)]))
    fillp(cc, spath([(-52, -6, 0), (-118, -26), (-134, -2), (-118, 22), (-52, 10, 0)]))
    for k in (0, 1):
        fillp(cc, ppath([(10 + k * 16, 14), (16 + k * 16, 14), (4 + k * 16, 44), (-2 + k * 16, 44)]))
        fillp(cc, ppath([(-6 + k * 16, 42), (12 + k * 16, 40), (14 + k * 16, 50), (-8 + k * 16, 50)]))
    wing(f, 0)
    cc.restore()


def p5_s06(an, c, t):
    """Over Rostam's shoulder: Tahmineh tells him who she is."""
    lt, dur = loc(an, "S06", t)
    focus = (420, 640)
    zoom = 1.0 + 0.05 * ease(lt / dur)
    cam = Cam(c, focus, zoom)
    with cam(0.7):
        S.lin(c, 0, H, [(0, (16, 10, 22)), (0.45, (38, 24, 36)), (1, (6, 3, 5))])
        door(c, 170, 1000, 300, 640, 1.0, 0.2, t)
        wall_panel(c, 380, 1180, 300, 1040, (70, 40, 44), (120, 76, 64))
    proud = sstep(6.2, 6.8, lt) * (1 - sstep(9.0, 9.6, lt))
    self_ = sstep(9.2, 9.8, lt) * (1 - sstep(12.0, 12.6, lt))
    modest = sstep(12.4, 13.2, lt)
    PT = {"jaw": jaw(an, "TAHMINEH", t, 6), "head": 3 - 6 * proud + 8 * modest + 1.5 * math.sin(t * 0.7),
          "hand": (mix(mix(70, 40, self_), 30, modest), mix(mix(-330, -380, self_), -390, modest)),
          "hand_kind": "open", "rhand": (-30, -262), "wind": 0.4, "lean": -2 * proud + 3 * modest}
    PR = {"jaw": jaw(an, "ROSTAM", t, 7), "head": 2 - 5 * sstep(3.4, 3.9, lt) * (1 - sstep(5.8, 6.4, lt)),
          "hand": (60, -300), "rhand": (-30, -262)}

    def back(cc):
        with Cam(cc, focus, zoom)(1.0):
            tag("m:")
            person(cc, 110, 1150, 1.05, 1, {"hand_kind": "candle", "hand": (100, -380)}, t, "maid")
            tag("")
            person(cc, 410, 1360, 1.62, 1, PT, t, TAHM)
    an.figures(c, back, WARM, (0, 150, 1080, 1500), anchors=True)
    candle_light(c, an, "m:flame", t, 600, 130, 3.0, 0.3)

    def front(cc):
        with Cam(cc, focus, zoom)(1.25):
            in_bed(cc, t, 1000, 1330, 2.5, 4 + 2 * math.sin(t * 0.5), PR)
    an.figures(c, front, WARM, (500, 300, 1080, 1700), alpha=120)
    vig(an, c, 180)


VIG = [(0.0, 3.7), (3.6, 8.0), (7.9, 12.7), (12.6, 17.0)]


def p5_s07(an, c, t):
    """The stories she heard, as shadows cast by the candle on a curtain."""
    lt, dur = loc(an, "S07", t)
    fl = 0.9 + 0.07 * math.sin(t * 8) + 0.04 * math.sin(t * 17)
    S.lin(c, 0, H, [(0, (60, 26, 18)), (0.2, (170, 96, 52)), (0.45, (236, 168, 96)), (0.62, (214, 140, 80)),
                    (0.8, (110, 50, 30)), (1, (16, 6, 6))])
    pf = skia.Paint(AntiAlias=True)
    pf.setShader(skia.GradientShader.MakeLinear([skia.Point(0, 0), skia.Point(96, 0)],
                                                [C(90, 36, 20, 90), C(255, 230, 190, 30), C(90, 36, 20, 90)],
                                                [0.0, 0.5, 1.0], skia.TileMode.kRepeat))
    c.drawRect(skia.Rect.MakeLTRB(0, 0, W, H), pf)
    S.glow(c, 160, 900, 900, (255, 190, 110), 110 * fl)
    sway = 6 * math.sin(t * 1.3)
    a = [min(sstep(a0, a0 + 0.5, lt), 1 - sstep(b - 0.4, b, lt)) if b < dur + 1 else sstep(a0, a0 + 0.5, lt)
         for a0, b in VIG]
    B = (0, 240, W, 1000)
    if a[0] > 0.01:
        shadow_layer(c, B, 0.86 * a[0])
        c.save()
        c.translate(sway, 0)
        person(c, 430, 860, 0.95, 1, {"hand_kind": "oxmace", "hand": (110, -330), "mace": 10, "head": -3, "wind": 0.8,
                                      "stance": (60, 50)}, t, "rostam")
        horse(c, 830, 866, 0.7, -1, {"gait": "stand", "neck": 12 + 4 * math.sin(t), "saddle": True}, t)
        c.restore()
        c.restore()
    if a[1] > 0.01:
        u = lt - VIG[1][0]
        hit = sstep(1.9, 2.3, u)
        shadow_layer(c, B, 0.86 * a[1])
        c.save()
        c.translate(sway, 0)
        person(c, 340 + 40 * hit, 860, 0.9, 1, {"hand_kind": "mace", "hand": (mix(40, 160, hit), mix(-580, -360, hit)),
                                                "mace": mix(-40, 70, hit), "lean": 8 * hit, "head": -4, "wind": 0.8,
                                                "stance": (64, 52)}, t, "rostam")
        person(c, 780 + 50 * hit, 860, 0.82, -1, {"hand_kind": "club", "hand": (70, -560), "mace": -30 - 30 * hit,
                                                  "lean": -16 * hit, "head": -10 * hit, "jaw": 8,
                                                  "rhand": (-80, -420), "rhand_kind": "open", "stance": (60, 56)}, t, "div")
        c.restore()
        c.restore()
    if a[2] > 0.01:
        u = lt - VIG[2][0]
        shadow_layer(c, B, 0.86 * a[2])
        c.drawPath(spath([(770, 380, 0), (820, 330), (860, 400), (830, 470, 0), (848, 404), (822, 360)]), ink_paint())
        horse(c, mix(120, 960, u / 4.8), 862, 0.8, 1, {"gait": "gallop", "phase": t * 1.9, "saddle": True, "rider": "rostam",
                                                     "rider_pose": {"lean": 12, "hand": (120, -330), "hand_kind": "mace",
                                                                    "mace": 60, "head": 4, "wind": 1.2}}, t)
        c.restore()
        c.save()
        c.translate(0, 0)
        c.restore()
    if a[3] > 0.01:
        u = lt - VIG[3][0]
        up = sstep(0.3, 1.0, u)
        swoop = clamp(u / 1.8)
        away = sstep(1.8, 3.4, u)
        ex = mix(mix(1060, 720, ease(swoop)), 1180, away)
        ey = mix(mix(300, 470, ease(swoop)), 230, away)
        shadow_layer(c, B, 0.86 * a[3])
        person(c, 400, 860, 0.95, 1, {"hand_kind": "sword", "hand": (mix(60, 70, up), mix(-300, -600, up)),
                                      "sword": mix(60, 8, up), "head": -8 * up, "wind": 0.8, "stance": (60, 50)}, t, "rostam")
        eagle(c, ex, ey, 0.9, t, -1 if away < 0.5 else 1, 1.0, 7.0)
        c.restore()
    standing_candle(c, 120, 1010, t, 0.95, 1.5)
    vig(an, c, 200)


def ink_paint():
    return Pen.FILL


def p5_s08(an, c, t):
    """Close on Rostam, sitting in bed, listening."""
    lt, dur = loc(an, "S08", t)
    focus = (640, 620)
    zoom = 1.0 + 0.06 * ease(lt / dur)
    cam = Cam(c, focus, zoom)
    with cam(0.6):
        S.lin(c, 0, H, [(0, (16, 10, 22)), (0.45, (40, 24, 34)), (1, (6, 3, 5))])
        wall_panel(c, 300, 1200, 280, 1100, (90, 50, 46), (150, 92, 70), 96)
        S.hanging_lamp(c, 940, 230, 1.3, t, 90, 4.0)
    S.glow(c, -60, 760, 900, (255, 170, 80), 120 + 12 * math.sin(t * 8))
    down = sstep(1.6, 2.6, lt) * (1 - sstep(4.3, 5.2, lt))
    look = sstep(4.4, 5.4, lt)
    P = {"jaw": 0.0, "head": 2 + 9 * down - 5 * look + 1.2 * math.sin(t * 0.6), "hand": (70, -300),
         "rhand": (-30, -262), "lean": -2 * look}

    def figs(cc):
        with Cam(cc, focus, zoom)(1.0):
            in_bed(cc, t, 700, 1250, 2.25, 2 + math.sin(t * 0.5), P)
            fillp(cc, spath([(-100, 1300, 0), (-100, 1150), (300, 1140), (600, 1150), (720, 1180), (760, 1300, 0)]))
    an.figures(c, figs, WARM, (0, 200, 1080, 1500))
    get(an, "mo08", lambda: S.Motes(40, 8, 250, 1000)).draw(c, t, (255, 200, 140), 80, rise=4, drift=0.2)
    vig(an, c, 180)


def p5_s09(an, c, t):
    """Two-shot: she steps closer -- three reasons."""
    lt = t - an.start["S09"]
    focus = (600, 680)
    zoom = 1.0 + 0.1 * ease(lt / 18.4)
    cam = Cam(c, focus, zoom)
    with cam(0.7):
        S.lin(c, 0, H, [(0, (14, 10, 22)), (0.45, (34, 22, 34)), (1, (6, 3, 5))])
        wall_panel(c, 560, 1180, 330, 1060)
        door(c, 100, 1040, 300, 640, 1.0, 0.2, t)
        S.hanging_lamp(c, 760, 250, 1.2, t, 110, 2.0)
    step = sstep(0.2, 2.0, lt)
    ask = sstep(3.3, 3.8, lt) * (1 - sstep(6.0, 6.8, lt))
    P = {"jaw": jaw(an, "ROSTAM", t, 7), "head": 2 - 4 * ask + 1.5 * math.sin(t * 0.7),
         "hand": (mix(50, 120, ask), mix(-270, -380, ask)), "hand_kind": "open" if ask > 0.3 else "fist",
         "rhand": (-20, -250), "lean": -5 * ask}
    PT = {"mode": "walk" if 0 < step < 1 else "stand", "phase": lt * 3.4, "stride": 12,
          "jaw": jaw(an, "TAHMINEH", t, 6), "hand": (mix(40, 80, step), mix(-270, -360, step)), "hand_kind": "open",
          "head": 3 + 1.5 * math.sin(t * 0.8), "wind": 0.35, "rhand": (-30, -262)}

    def figs(cc):
        with Cam(cc, focus, zoom)(1.0):
            tag("m:")
            person(cc, 110, 1110, 0.98, 1, {"hand_kind": "candle", "hand": (100, -380), "head": 2}, t, "maid")
            tag("")
            person(cc, mix(340, 450, step), 1110, 1.12, 1, PT, t, TAHM)
            bedroom_figs(cc, t, 0, P, hx=900, ytop=1046, s=1.62, knee=0.5, x0=600, x1=1320, mace=(1050, 1090, -16, 1.4))
    an.figures(c, figs, WARM, (0, 150, 1080, 1300), anchors=True)
    candle_light(c, an, "m:flame", t, 640, 130, 3.0, 0.3)
    vig(an, c, 170)


# ------------------------------------------------------------------ part 6 helpers
def moon_window(an, c, t, cam, x, yb, w, h, cover=0.0, key="mw"):
    """Dark wall with a tall arched window: night sky, moon, stars, clouds, far rooftops.
    cover (0..1) slides a dark cloud over the moon."""
    S.lin(c, 0, H, [(0, (10, 10, 22)), (0.5, (22, 22, 40)), (1, (5, 4, 8))])
    arch = S.arch_path(x, yb, w, h)
    with cam(0.5):
        c.save()
        c.clipPath(arch, skia.ClipOp.kIntersect, True)
        S.lin(c, yb - h, yb, [(0, (10, 14, 40)), (0.6, (34, 44, 92)), (1, (70, 76, 120))], (x - w, yb - h - 40, x + w, yb + 10))
        get(an, key + "st", lambda: S.Stars(90, 900, 41)).draw(c, t, 1.0, 900)
        mx, my = x + w * 0.12, yb - h * 0.62
        S.moon(c, mx, my, w * 0.14)
        if cover > 0:
            cx = mix(x - w * 0.9, mx, ease(cover))
            S.radial(c, cx, my + 8, w * 0.42, [(0, (14, 16, 34, 250)), (0.6, (16, 18, 38, 230)), (1, (16, 18, 38, 0))])
        get(an, key + "cl", lambda: S.Clouds([(yb - h * 0.35, 10), (yb - h * 0.25, 7)], 43, 200, 420)).draw(
            c, t * 2, (20, 24, 50), 170)
        img, _ = get(an, key + "city", lambda: S.city(900, 400, 380, 44, (8, 8, 16), False, None))
        c.drawImage(img, x - w * 0.9, yb - 330)
        c.restore()
        edge = skia.Paint(AntiAlias=True, Color=C(*INK))
        edge.setStyle(skia.Paint.kStroke_Style)
        edge.setStrokeWidth(26)
        c.drawPath(arch, edge)
        pt = paint(C(*INK))
        c.drawRect(skia.Rect.MakeLTRB(x - 4, yb - h + 20, x + 4, yb), pt)
        c.drawRect(skia.Rect.MakeLTRB(x - w / 2, yb - h * 0.45 - 4, x + w / 2, yb - h * 0.45 + 4), pt)
        c.drawRect(skia.Rect.MakeLTRB(x - w / 2 - 40, yb, x + w / 2 + 40, yb + 26), pt)
    p = skia.Paint(AntiAlias=True)
    p.setShader(skia.GradientShader.MakeLinear([skia.Point(x, yb - h), skia.Point(x - w * 1.4, yb + 500)],
                                               [C(150, 170, 230, 70 * (1 - 0.7 * cover)), C(150, 170, 230, 0)]))
    c.drawPath(ppath([(x - w / 2, yb - h * 0.7), (x + w / 2, yb - h * 0.5), (x + w * 0.1, yb + 700),
                      (x - w * 1.6, yb + 700)]), p)


def ghost_layer(c, bounds, alpha, col=(255, 226, 160), blur=3.0):
    """Begin a layer whose content lands as a pale, glowing vision (end with c.restore())."""
    p = skia.Paint()
    p.setAlphaf(clamp(alpha))
    p.setColorFilter(skia.ColorFilters.Blend(C(*col), skia.BlendMode.kSrcIn))
    p.setImageFilter(skia.ImageFilters.Blur(blur, blur, skia.TileMode.kDecal, None))
    c.saveLayer(skia.Rect.MakeLTRB(*bounds), p)
    Pen.mode = "fill"


def king_room(an, c, t, cam, lampk=1.0):
    """The king's bedchamber: cool walls, a lattice window, a canopy bed, a hanging lamp."""
    with cam(0.7):
        S.lin(c, 0, H, [(0, (8, 16, 22)), (0.45, (22, 40, 48)), (0.65, (16, 28, 34)), (1, (4, 6, 8))])
        arch = S.arch_path(330, 760, 260, 420)
        c.save()
        c.clipPath(arch, skia.ClipOp.kIntersect, True)
        S.lin(c, 340, 760, [(0, (30, 44, 90)), (1, (80, 96, 140))], (180, 330, 480, 770))
        c.drawImage(get(an, "lat_k", lambda: S.lattice(280, 440, 56, 7)), 190, 330)
        c.restore()
        edge = skia.Paint(AntiAlias=True, Color=C(*INK))
        edge.setStyle(skia.Paint.kStroke_Style)
        edge.setStrokeWidth(18)
        c.drawPath(arch, edge)
        wall_panel(c, 600, 1160, 360, 860, (40, 70, 70), (70, 110, 100), 84)
        c.drawRect(skia.Rect.MakeLTRB(560, 300, 1200, 330), paint(C(*INK)))
        for i in range(9):
            c.drawPath(spath([(560 + i * 74, 330, 0), (597 + i * 74, 368), (634 + i * 74, 330, 0)]), paint(C(*INK)))
        c.drawPath(spath([(560, 330, 0), (640, 520), (600, 862, 0), (560, 862, 0)]), paint(C(*INK)))
        S.hanging_lamp(c, 820, 210, 1.1, t, 130, 5.0)
        S.glow(c, 820, 600, 560, (255, 170, 90), 60 * lampk)
    with cam(1.0):
        ground(c, 862, (20, 26, 30))


def guard_door(c, x, yb):
    c.drawPath(S.arch_path(x, yb, 200, 380), paint(C(36, 22, 22)))
    edge = skia.Paint(AntiAlias=True, Color=C(*INK))
    edge.setStyle(skia.Paint.kStroke_Style)
    edge.setStrokeWidth(14)
    c.drawPath(S.arch_path(x, yb, 200, 380), edge)
    c.drawRect(skia.Rect.MakeLTRB(x - 90, yb - 6, x + 90, yb), paint(C(255, 180, 100, 110)))


# ------------------------------------------------------------------ part 6 shots
def p6_s01(an, c, t):
    """Hook + title: Tahmineh at the moonlit window."""
    lt = t - an.start["S01"]
    focus = (600, 620)
    zoom = 1.04 + 0.08 * ease(lt / 8.8)
    cam = Cam(c, focus, zoom)
    moon_window(an, c, t, cam, 780, 880, 440, 640, key="w1")
    lift = sstep(0.4, 1.4, lt)
    P = {"jaw": jaw(an, "TAHMINEH", t, 6), "head": -4 * lift + 1.5 * math.sin(t * 0.7),
         "hand": (mix(40, 60, lift), mix(-270, -400, lift)), "hand_kind": "open", "rhand": (-20, -330),
         "wind": 0.5, "lean": -2 * lift}

    def figs(cc):
        with Cam(cc, focus, zoom)(1.0):
            person(cc, 360, 1500, 2.0, 1, P, t, TAHM)
    an.figures(c, figs, MOON, (0, 200, 1080, 1600), alpha=170)
    get(an, "mo61", lambda: S.Motes(40, 11, 250, 1000)).draw(c, t, (200, 214, 255), 80, rise=3, drift=0.2)
    vig(an, c, 180)


def p6_s02(an, c, t):
    """Recap: the bedchamber, Rostam sitting up in bed, Tahmineh before him, the maid with her candle."""
    lt, dur = loc(an, "S02", t)
    focus = (560, 640)
    zoom = 1.0 + 0.07 * ease(lt / dur)
    cam = Cam(c, focus, zoom)
    room(an, c, t, cam, u=1.0, glow=0.2, lamp=0.6)
    P = {"jaw": 0.0, "head": 3 + 1.5 * math.sin(t * 0.6), "hand": (50, -280), "rhand": (-20, -260)}

    def figs(cc):
        with Cam(cc, focus, zoom)(1.0):
            tag("m:")
            person(cc, 300, 866, 0.8, 1, {"hand_kind": "candle", "hand": (96, -380)}, t, "maid")
            tag("")
            person(cc, 470, 866, 0.86, 1, {"hand": (60, -330), "hand_kind": "open", "wind": 0.3,
                                           "head": 3 + 1.2 * math.sin(t * 0.9)}, t, TAHM)
            bedroom_figs(cc, t, 0, P, hx=800, ytop=786, s=0.86, knee=0.5, mace=(1046, 838, -14, 0.8))
    an.figures(c, figs, WARM, (0, 200, 1080, 1000), anchors=True)
    candle_light(c, an, "m:flame", t, 520, 120, 3.0, 0.24)
    vig(an, c, 170)


def two_shot_bed(an, c, t, lt, sid_zoom, PT, PR, tx=450, maid=True):
    """Shared two-shot: Tahmineh (left) and Rostam sitting up in bed (right)."""
    focus = (600, 680)
    zoom = 1.0 + sid_zoom
    cam = Cam(c, focus, zoom)
    with cam(0.7):
        S.lin(c, 0, H, [(0, (14, 10, 22)), (0.45, (34, 22, 34)), (1, (6, 3, 5))])
        wall_panel(c, 560, 1180, 330, 1060)
        door(c, 100, 1040, 300, 640, 1.0, 0.2, t)
        S.hanging_lamp(c, 760, 250, 1.2, t, 110, 2.0)

    def figs(cc):
        with Cam(cc, focus, zoom)(1.0):
            if maid:
                tag("m:")
                person(cc, 110, 1110, 0.98, 1, {"hand_kind": "candle", "hand": (100, -380), "head": 2}, t, "maid")
                tag("")
            person(cc, tx, 1110, 1.12, 1, PT, t, TAHM)
            bedroom_figs(cc, t, 0, PR, hx=900, ytop=1046, s=1.62, knee=0.5, x0=600, x1=1320, mace=(1050, 1090, -16, 1.4))
    an.figures(c, figs, WARM, (0, 150, 1080, 1300), anchors=maid)
    if maid:
        candle_light(c, an, "m:flame", t, 640, 130, 3.0, 0.3)
    vig(an, c, 170)


def p6_s03(an, c, t):
    """First reason: her heart."""
    lt, dur = loc(an, "S03", t)
    heart = sstep(0.0, 0.6, lt) * (1 - sstep(2.0, 2.8, lt)) + sstep(7.4, 8.0, lt) * (1 - sstep(9.6, 10.4, lt))
    ask = sstep(10.1, 10.6, lt) * (1 - sstep(13.2, 13.9, lt))
    PT = {"jaw": jaw(an, "TAHMINEH", t, 6), "head": 3 + 5 * heart + 1.5 * math.sin(t * 0.8), "wind": 0.35,
          "hand": (mix(70, 30, heart), mix(-330, -385, heart)), "hand_kind": "open", "rhand": (-30, -262),
          "lean": 2 * heart}
    PR = {"jaw": jaw(an, "ROSTAM", t, 7), "head": 2 - 5 * ask + 1.5 * math.sin(t * 0.7),
          "hand": (mix(50, 120, ask), mix(-270, -380, ask)), "hand_kind": "open" if ask > 0.3 else "fist",
          "rhand": (-20, -250), "lean": -4 * ask}
    two_shot_bed(an, c, t, lt, 0.05 * ease(lt / dur), PT, PR, 430)


def p6_s04(an, c, t):
    """Second reason, at the window: a vision of a young rider in the sky; then a cloud hides the moon."""
    lt, dur = loc(an, "S04", t)
    focus = (620, 620)
    zoom = 1.0 + 0.1 * ease(lt / dur)
    cam = Cam(c, focus, zoom)
    cover = sstep(10.6, 14.6, lt)
    moon_window(an, c, t, cam, 760, 900, 480, 680, cover, key="w4")
    vis = sstep(3.2, 4.8, lt) * (1 - sstep(10.4, 12.6, lt))
    if vis > 0.01:
        u = lt - 3.2
        with cam(0.5):
            c.save()
            c.clipPath(S.arch_path(760, 900, 480, 680), skia.ClipOp.kIntersect, True)
            ghost_layer(c, (500, 200, 1040, 900), 0.62 * vis, (255, 214, 140), 2.6)
            horse(c, mix(600, 860, clamp(u / 9.0)), 640, 0.42, 1, {"gait": "gallop", "phase": t * 1.6, "saddle": True,
                                                                  "rider": "sohrab", "rider_pose": {"lean": 8, "hand": (110, -360),
                                                                                                    "hand_kind": "spear",
                                                                                                    "head": -4, "wind": 1.0}}, t)
            c.restore()
            c.restore()
    pray = sstep(0.2, 1.0, lt)
    P = {"jaw": jaw(an, "TAHMINEH", t, 6), "head": -6 * pray + 6 * cover + 1.5 * math.sin(t * 0.7),
         "hand": (mix(40, 70, pray), mix(-270, -440, pray) + 60 * cover), "hand_kind": "open", "rhand": (-10, -360),
         "wind": 0.5, "lean": -2 * pray + 3 * cover}

    def figs(cc):
        with Cam(cc, focus, zoom)(1.0):
            person(cc, 330, 1520, 1.95, 1, P, t, TAHM)
    an.figures(c, figs, mixc(MOON, (120, 130, 170), cover), (0, 200, 1080, 1600), alpha=170 - 60 * cover)
    vig(an, c, 180 + 30 * cover)


def p6_s05(an, c, t):
    """Third reason: Rakhsh. Rostam leans forward; she swears by her father's crown."""
    lt, dur = loc(an, "S05", t)
    ask = sstep(5.9, 6.5, lt) * (1 - sstep(8.8, 9.6, lt))
    oath = sstep(8.9, 9.5, lt)
    point = sstep(0.2, 0.8, lt) * (1 - sstep(5.6, 6.2, lt))
    PT = {"jaw": jaw(an, "TAHMINEH", t, 6), "head": 3 - 3 * point + 5 * oath + 1.5 * math.sin(t * 0.8), "wind": 0.35,
          "hand": (mix(mix(70, 120, point), 30, oath), mix(mix(-330, -360, point), -385, oath)), "hand_kind": "open",
          "rhand": (-30, -262), "lean": 2 * oath}
    PR = {"jaw": jaw(an, "ROSTAM", t, 8), "head": 2 - 7 * ask + 1.5 * math.sin(t * 0.7),
          "hand": (mix(50, 150, ask), mix(-270, -370, ask)), "hand_kind": "open" if ask > 0.3 else "fist",
          "rhand": (-20, -250), "lean": -10 * ask}
    two_shot_bed(an, c, t, lt, 0.03 + 0.05 * ease(lt / dur), PT, PR, 450)


def p6_s06(an, c, t):
    """Over Tahmineh's shoulder: Rostam looks at her."""
    lt, dur = loc(an, "S06", t)
    focus = (640, 660)
    zoom = 1.0 + 0.06 * ease(lt / dur)
    cam = Cam(c, focus, zoom)
    with cam(0.6):
        S.lin(c, 0, H, [(0, (16, 10, 22)), (0.45, (40, 24, 34)), (1, (6, 3, 5))])
        wall_panel(c, 300, 1200, 300, 1100, (90, 50, 46), (150, 92, 70), 90)
        S.hanging_lamp(c, 900, 240, 1.2, t, 100, 4.0)
    hope = sstep(6.4, 7.6, lt)
    PR = {"jaw": 0.0, "head": 4 - 7 * hope + 1.2 * math.sin(t * 0.6), "hand": (mix(60, 90, hope), mix(-290, -330, hope)),
          "hand_kind": "open" if hope > 0.5 else "fist", "rhand": (-20, -250), "lean": -3 * hope}

    def figs(cc):
        with Cam(cc, focus, zoom)(1.0):
            bedroom_figs(cc, t, 0, PR, hx=760, ytop=1040, s=1.55, knee=0.5, x0=470, x1=1200, mace=(1150, 1080, -16, 1.3))
    an.figures(c, figs, WARM, (0, 200, 1080, 1300))
    S.glow(c, 120, 820, 700, (255, 170, 80), 110 + 10 * math.sin(t * 8))

    def fg(cc):
        with Cam(cc, focus, zoom)(1.2):
            person(cc, 90, 2080, 2.85, 1, {"head": 2 + math.sin(t * 0.6), "wind": 0.4, "hand": (40, -270),
                                           "rhand": (-30, -262)}, t, TAHM)
    an.figures(c, fg, WARM, (0, 200, 600, 1700), alpha=110)
    vig(an, c, 180)


def p6_s06b(an, c, t):
    """Rostam on his feet: 'Call a wise priest.' Tahmineh sends the maid running."""
    lt, dur = loc(an, "S06b", t)
    focus = (560, 640)
    zoom = 1.04 + 0.04 * ease(lt / dur)
    cam = Cam(c, focus, zoom)
    room(an, c, t, cam, u=1.0, glow=0.15, lamp=0.6)
    chest = sstep(0.2, 0.8, lt) * (1 - sstep(2.6, 3.2, lt))
    refuse = sstep(2.8, 3.4, lt) * (1 - sstep(5.0, 5.6, lt))
    point = sstep(5.8, 6.6, lt) * (1 - sstep(10.0, 10.8, lt))
    turn = lt > 10.8
    go = clamp((lt - 14.0) / 2.6)
    if point > 0.01:
        hand, hk = (mix(40, 170, point), mix(-262, -440, point)), "open"
    elif refuse > 0.01:
        hand, hk = (mix(40, 110, refuse), mix(-262, -460, refuse)), "open"
    else:
        hand, hk = (mix(40, 26, chest), mix(-262, -380, chest)), "open" if chest > 0.3 else "fist"
    PR = {"jaw": jaw(an, "ROSTAM", t, 7), "hand": hand, "hand_kind": hk, "head": 2 - 4 * point + 1.2 * math.sin(t * 0.6),
          "lean": 3 * chest - 3 * point, "stance": (48, 42)}
    PT = {"jaw": jaw(an, "TAHMINEH", t, 6), "head": 3, "wind": 0.35,
          "hand": (mix(60, 150, sstep(10.9, 11.4, lt) * (1 - sstep(12.8, 13.4, lt))),
                   mix(-330, -420, sstep(10.9, 11.4, lt) * (1 - sstep(12.8, 13.4, lt)))), "hand_kind": "open",
          "rhand": (-30, -262)}
    mx = mix(250, -120, ease(go))

    def figs(cc):
        with Cam(cc, focus, zoom)(1.0):
            bed(cc, 600, 1060, 786, 866, "right")
            fillp(cc, spath([(640, 790, 0), (660, 750), (760, 744), (860, 760), (900, 790, 0)]))
            mace_at(cc, 1046, 838, -14, 0.8, t)
            person(cc, 790, 866, 0.95, -1, PR, t, "rostam_robe")
            person(cc, 520, 866, 0.86, -1 if turn else 1, PT, t, TAHM)
            tag("m:")
            person(cc, mx, 866, 0.8, -1 if (lt > 13.6) else 1,
                   {"mode": "walk" if 0 < go < 1 else "stand", "phase": lt * 4.2, "stride": 16, "hand_kind": "candle",
                    "hand": (96, -380), "jaw": jaw(an, "MAID", t, 7), "head": -3 if lt > 13.2 else 0, "wind": 0.4}, t, "maid")
            tag("")
    an.figures(c, figs, WARM, (0, 200, 1080, 1000), anchors=True)
    candle_light(c, an, "m:flame", t, 520, 120 * (1 - 0.6 * go), 3.0, 0.24)
    vig(an, c, 170)


def p6_s07(an, c, t):
    """The old mobed with his lamp crosses the sleeping palace; a guard stops him."""
    lt, dur = loc(an, "S07", t)
    walk = clamp(lt / 5.6)
    wk = ease(walk) * 0.35 + walk * 0.65
    pan = -300 * wk
    focus = (540, 660)
    zoom = 1.1 + 0.05 * ease(lt / dur)
    cam = Cam(c, focus, zoom)
    corridor(an, c, t, cam, pan, None)
    with cam(1.0):
        guard_door(c, -110 - pan, 866)
    gx = mix(-140, 230, sstep(4.6, 5.6, lt))
    stop = sstep(5.3, 5.8, lt)
    PG = {"rprop": "spear", "rhand": (-10, -300), "hand": (mix(40, 150, stop), mix(-262, -330, stop)), "hand_kind": "open",
          "jaw": jaw(an, "GUARD", t, 9), "head": -2, "mode": "walk" if 4.6 < lt < 5.6 else "stand", "phase": lt * 5}
    walking = lt < 5.6
    PM = {"mode": "walk" if walking else "stand", "phase": lt * 3.2, "stride": 12, "hand_kind": "lamp",
          "hand": (110, -360), "rprop": "staff", "rhand": (-10, -300), "jaw": jaw(an, "MOBED", t, 7),
          "head": 4 if walking else -2, "lean": 4 if walking else 0}
    mx = mix(900, 560, wk)

    def figs(cc):
        with Cam(cc, focus, zoom)(1.0):
            tag("mo:")
            person(cc, mx, 872, 1.0, -1, PM, t, "mobed")
            tag("")
            if lt > 4.4:
                person(cc, gx, 872, 1.02, 1, PG, t, "guard")
    an.figures(c, figs, WARM, (0, 200, 1080, 1100), anchors=True)
    candle_light(c, an, "mo:flame", t, 600, 130, 5.0, 0.3)
    vig(an, c, 170)


def p6_s08(an, c, t):
    """The king's room: the mobed bows and gives Rostam's message; the king sits up."""
    lt, dur = loc(an, "S08", t)
    focus = (600, 640)
    zoom = 1.0 + 0.05 * ease(lt / dur)
    cam = Cam(c, focus, zoom)
    king_room(an, c, t, cam)
    up = sstep(0.0, 1.6, lt)
    shock = sstep(8.6, 9.2, lt)
    bow = sstep(0.0, 0.8, lt) * (1 - sstep(3.0, 3.8, lt))
    PK = {"jaw": jaw(an, "KING_SAMANGAN", t, 7), "head": mix(10, 2, up) - 6 * shock + 1.2 * math.sin(t * 0.6),
          "hand": (mix(50, 110, shock), mix(-280, -400, shock)), "hand_kind": "open" if shock > 0.3 else "fist",
          "rhand": (-20, -260), "lean": -6 * shock}
    PM = {"hand_kind": "lamp", "hand": (110, -360), "rprop": "staff", "rhand": (-10, -300), "jaw": jaw(an, "MOBED", t, 7),
          "head": 12 * bow + 2, "lean": 16 * bow + 4}

    def figs(cc):
        with Cam(cc, focus, zoom)(1.0):
            in_bed(cc, t, 830, 782, 0.9, mix(60, 0, up), PK, "king")
            bed(cc, 640, 1080, 786, 866, "right")
            blanket(cc, 836, 670, 786, 0.9, 0.5 * up)
            tag("mo:")
            person(cc, 380, 866, 0.86, 1, PM, t, "mobed")
            tag("")
    an.figures(c, figs, WARM, (0, 200, 1080, 1000), anchors=True)
    candle_light(c, an, "mo:flame", t, 520, 110, 5.0, 0.26)
    vig(an, c, 170)


def p6_s09(an, c, t):
    """Close on the king: what will he answer?"""
    lt = t - an.start["S09"]
    focus = (620, 640)
    zoom = 1.0 + 0.1 * ease(lt / 19.0)
    cam = Cam(c, focus, zoom)
    with cam(0.6):
        S.lin(c, 0, H, [(0, (8, 16, 22)), (0.45, (24, 42, 50)), (1, (4, 6, 8))])
        wall_panel(c, 300, 1200, 300, 1100, (40, 70, 70), (74, 112, 100), 90)
        S.hanging_lamp(c, 880, 220, 1.3, t, 90, 6.0)
    S.glow(c, -40, 760, 800, (255, 170, 80), 100 + 10 * math.sin(t * 8))
    turn = sstep(5.0, 7.0, lt)
    PK = {"jaw": jaw(an, "KING_SAMANGAN", t, 7), "head": 2 + 6 * turn + 1.2 * math.sin(t * 0.5),
          "hand": (mix(60, 40, turn), mix(-300, -380, turn)), "hand_kind": "open", "rhand": (-20, -260), "lean": 2 * turn}

    def figs(cc):
        with Cam(cc, focus, zoom)(1.0):
            in_bed(cc, t, 720, 1250, 2.2, 0, PK, "king")
            fillp(cc, spath([(-100, 1300, 0), (-100, 1160), (300, 1150), (600, 1160), (720, 1190), (760, 1300, 0)]))
    an.figures(c, figs, WARM, (0, 200, 1080, 1500))
    get(an, "mo69", lambda: S.Motes(40, 9, 250, 1000)).draw(c, t, (255, 210, 150), 70, rise=3, drift=0.2)
    vig(an, c, 180)


P06 = {"S01": p6_s01, "TITLE": p6_s01, "S02": p6_s02, "S03": p6_s03, "S04": p6_s04, "S05": p6_s05, "S06": p6_s06,
       "S06b": p6_s06b, "S07": p6_s07, "S08": p6_s08, "S09": p6_s09, "END": p6_s09}
SHIFT6 = {}


P05 = {"S01": p5_s01, "TITLE": p5_s01, "S02": p5_s02, "S03": p5_s03, "S04": p5_s04, "S04b": p5_s04b, "S05": p5_s05,
       "S06": p5_s06, "S07": p5_s07, "S08": p5_s08, "S09": p5_s09, "END": p5_s09}
SHIFT5 = {}


def register(scenes, shifts):
    anim.SCENES.clear()
    anim.SCENES.update(scenes)
    anim.SHIFTS.clear()
    anim.SHIFTS.update(shifts)


register(P05, SHIFT5)
