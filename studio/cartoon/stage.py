"""staging helpers: placing characters, crowds, fire, foreground silhouettes"""
import math, random
from PIL import Image, ImageFilter
from chars import person, lying_person, horse, elephant, cow, Ctx, fmt, FEET, spec, pose, prop, tanbur, smooth_path
from film import svg_render, W, H

def lw_for(s):
    return 1.0 / max(0.3, s) ** 0.5

def at_neck(S, p, t, x, y, s, flip=False, lws=None):
    yf = y + FEET * S["bs"] * s
    sx = -s if flip else s
    return f'<g transform="translate({x:.1f},{yf:.1f}) scale({sx:.4f},{s:.4f})">{person(S, p, t, lw_for(lws or s))}</g>'

def at_feet(S, p, t, x, y, s, flip=False):
    sx = -s if flip else s
    return f'<g transform="translate({x:.1f},{y:.1f}) scale({sx:.4f},{s:.4f})">{person(S, p, t, lw_for(s))}</g>'

def lying_at(S, p, t, x, y, s, flip=False):
    sx = -s if flip else s
    return f'<g transform="translate({x:.1f},{y:.1f}) scale({sx:.4f},{s:.4f})">{lying_person(S, p, t, lw_for(s))}</g>'

PAL = ["#3a5a6a", "#6a2a1e", "#5a5040", "#4a3a5a", "#7a5a2a", "#2a4a3a", "#8a6a4a", "#5a3a2a", "#6a6a7a", "#9a4a2a"]
HEADC = ["#f0ead8", "#e8dcc0", "#2a2a2a", "#5a4a3a", "#7a2a2a", "#3a4a6a"]
SCARF = ["#2f3f6e", "#6a2a3a", "#3a5a4a", "#5a3a5a", "#7a5a3a", "#2a2a3a"]

def random_spec(r, kinds=("man", "man", "man", "woman", "boy")):
    k = r.choice(kinds)
    if k == "woman":
        return spec(kind="woman", hair="none", beard=None, head="scarf", scarf_col=r.choice(SCARF), scarf_edge=r.choice(["#c9a24a", "#d8c8a0", "#8a6a4a"]),
                    garment="dress", col=r.choice(PAL), col2="#2a1a1a", pattern="plain", hs=0.95, bs=0.95, belt=None, skin=r.choice(["tan", "light", "olive"]))
    if k == "boy":
        return spec(kind="boy", hair="short", beard=None, head=r.choice(["cap", "none"]), head_col=r.choice(HEADC), garment="child", col=r.choice(PAL),
                    col2="#2a1a1a", pattern="plain", hs=1.08, bs=0.62, belt="#4a3420", buckle=False, skin=r.choice(["tan", "olive"]))
    return spec(kind=r.choice(["man", "man", "old"]), hair="short", hair_col="#17100c", beard=r.choice(["father", "short", "full", "white"]),
                head=r.choice(["turban", "turban", "cap"]), head_col=r.choice(HEADC), garment="robe", col=r.choice(PAL), col2="#2a1a1a", pattern="plain",
                belt=r.choice(["#2b190c", None]), sash=r.choice([None, "#c9a24a", "#8a2a2a"]), buckle=False, skin=r.choice(["tan", "olive", "light", "old"]),
                build=r.uniform(0.95, 1.15))

def crowd_row(seed, n, y_feet, s, x0=-40, x1=W + 40, kinds=("man", "man", "man", "woman", "boy"), turn_to=0.0, arms=None):
    """static row of people -> RGBA image"""
    r = random.Random(seed)
    xs = sorted(r.uniform(x0, x1) for _ in range(n))
    body = ""
    for i, x in enumerate(xs):
        S = random_spec(r, kinds)
        ss = s * r.uniform(0.93, 1.07)
        armset = arms or r.choice([("down", "down"), ("relaxed", "down"), ("chest", "chest"), ("point", "down"), ("hip", "relaxed")])
        p = pose(turn=turn_to + r.uniform(-0.15, 0.15), gx=turn_to * 2 + r.uniform(-0.3, 0.3), armR=armset[0], armL=armset[1], blink=0.0,
                 furrow=r.uniform(0, 0.6), brow=r.uniform(0, 0.5))
        body += at_feet(S, p, r.uniform(0, 3), x, y_feet + r.uniform(-8, 8), ss)
    return svg_render(body)

def back_heads(seed, n, y, s, col="#1a1014", blur=3):
    """foreground silhouettes: backs of heads and shoulders"""
    r = random.Random(seed)
    body = ""
    for i in range(n):
        x = r.uniform(-60, W + 60); yy = y + r.uniform(-30, 40); ss = s * r.uniform(0.85, 1.15)
        hat = r.choice(["turban", "cap", "scarf", "none"])
        g = (f'<path d="M -230 400 C -230 160, -150 90, 0 90 C 150 90, 230 160, 230 400 Z" fill="{col}"/>'
             f'<ellipse cx="0" cy="0" rx="100" ry="120" fill="{col}"/>')
        if hat == "turban":
            g += f'<ellipse cx="0" cy="-70" rx="118" ry="90" fill="{col}"/>'
        elif hat == "cap":
            g += f'<ellipse cx="0" cy="-80" rx="104" ry="64" fill="{col}"/>'
        elif hat == "scarf":
            g += f'<path d="M -130 300 C -150 0, -110 -150, 0 -150 C 110 -150, 150 0, 130 300 Z" fill="{col}"/>'
        body += f'<g transform="translate({x:.0f},{yy:.0f}) scale({ss:.3f})">{g}</g>'
    return svg_render(body).filter(ImageFilter.GaussianBlur(blur))

def fire_svg(x, y, size, t, seed=0):
    r = random.Random(seed)
    out = (f'<g transform="translate({x},{y}) scale({size/100:.3f})">'
           '<path d="M -120 10 L 110 -30 L 120 -5 L -110 35 Z" fill="#4a2a14" stroke="#1b0f0a" stroke-width="3"/>'
           '<path d="M -110 -30 L 120 15 L 110 40 L -120 -5 Z" fill="#5a3418" stroke="#1b0f0a" stroke-width="3"/>')
    for layer, col, sc in ((0, "#c8321a", 1.0), (1, "#ff8a1a", 0.72), (2, "#ffd84a", 0.45), (3, "#fff6c0", 0.22)):
        for k in range(5):
            dx = (k - 2) * 34 * sc
            hgt = (150 + 60 * math.sin(t * (7 + k) + k * 1.7 + layer) + 40 * math.sin(t * 13 + k)) * sc * (1.25 - abs(k - 2) * 0.18)
            sway = 16 * math.sin(t * 5 + k + layer) * sc
            wdt = 46 * sc
            out += (f'<path d="M {dx - wdt:.1f} 0 C {dx - wdt:.1f} {-hgt*0.45:.1f}, {dx + sway - wdt*0.2:.1f} {-hgt*0.7:.1f}, {dx + sway:.1f} {-hgt:.1f} '
                    f'C {dx + sway + wdt*0.25:.1f} {-hgt*0.65:.1f}, {dx + wdt:.1f} {-hgt*0.45:.1f}, {dx + wdt:.1f} 0 Z" fill="{col}"/>')
    return out + '</g>'

def howdah(x0, y0, w, h):
    return (f'<path d="M {x0} {y0} L {x0+w} {y0} L {x0+w-10} {y0+h} L {x0+10} {y0+h} Z" fill="#8a1a1a" stroke="#1b0f0a" stroke-width="4"/>'
            f'<path d="M {x0} {y0} L {x0+w} {y0}" stroke="#e0b25a" stroke-width="12"/>'
            + "".join(f'<circle cx="{x0 + 20 + k * (w - 40) / 5:.0f}" cy="{y0 + h * 0.55:.0f}" r="10" fill="#e0b25a" stroke="#1b0f0a" stroke-width="2"/>' for k in range(6)))

def rider(S, p, t, horse_svg_fn, x, y, s, rider_rel=0.31, flip=False):
    """horse (side view facing right) with a rider's upper body on the saddle"""
    c = Ctx(1 / max(0.3, s) ** 0.5)
    q = dict(p); q["legs"] = "none"
    rs = rider_rel
    # rider neck so that the waist sits on the saddle (~ y=-404 horse units)
    neck_y = -404 - 330 * rs * S["bs"]
    rid = f'<g transform="translate(10,{neck_y + FEET*S["bs"]*rs:.1f}) scale({rs:.4f})">{person(S, q, t, lw_for(s * rs))}</g>'
    sx = -s if flip else s
    return f'<g transform="translate({x:.1f},{y:.1f}) scale({sx:.4f},{s:.4f})">{horse_svg_fn(c)}{rid}</g>'

def glow_img(r, col, a):
    import numpy as np
    yy, xx = np.mgrid[0:2 * r, 0:2 * r].astype(np.float32)
    d = np.clip(1 - np.sqrt((xx - r) ** 2 + (yy - r) ** 2) / r, 0, 1) ** 2
    arr = np.zeros((2 * r, 2 * r, 4), np.uint8)
    arr[..., 0], arr[..., 1], arr[..., 2] = col
    arr[..., 3] = (d * 255 * a).astype(np.uint8)
    return Image.fromarray(arr, "RGBA")

class Glow:
    def __init__(self, posfn, r=220, col=(255, 190, 110), a=0.55):
        self.img = glow_img(r, col, a); self.posfn = posfn; self.r = r
    def __call__(self, im, t):
        p = self.posfn(t)
        if p:
            x, y = p
            fl = 0.9 + 0.1 * math.sin(t * 13) * math.sin(t * 7.1)
            g = self.img if fl > 0.99 else self.img.point(lambda v: v) 
            im.alpha_composite(g, (int(x - self.r), int(y - self.r)))
