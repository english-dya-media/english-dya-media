"""2D cartoon cast for the Babak film. Pure SVG generators.
Character local coords: origin at the base of the neck, +y down; feet at y = FEET (scaled by body scale)."""
import math, itertools

OUT = "#1b0f0a"
RIM = "#ffb877"
_uid = itertools.count()

def fmt(v): return f"{v:.1f}"
def lerp(a, b, t): return a + (b - a) * t
def P(pts): return " L ".join(f"{fmt(x)} {fmt(y)}" for x, y in pts)

def smooth_path(pts, closed=True):
    n = len(pts)
    d = f"M {fmt(pts[0][0])} {fmt(pts[0][1])} "
    rng = range(n) if closed else range(n - 1)
    for i in rng:
        p0 = pts[(i - 1) % n] if (closed or i > 0) else pts[i]
        p1 = pts[i]; p2 = pts[(i + 1) % n]
        p3 = pts[(i + 2) % n] if (closed or i + 2 < n) else p2
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d += f"C {fmt(c1[0])} {fmt(c1[1])}, {fmt(c2[0])} {fmt(c2[1])}, {fmt(p2[0])} {fmt(p2[1])} "
    return d + ("Z" if closed else "")

class Ctx:
    """per-character drawing context (line width and unique ids)"""
    def __init__(self, lw=1.0):
        self.lw = lw; self.id = next(_uid)
    def sw(self, w): return fmt(w * self.lw)
    def uid(self, name): return f"{name}{self.id}"

def rimmed(c, path, fill, rim=RIM, dx=3.0, dy=-1.5, sw=2.6, extra="", rim_on=True):
    r = f'<path d="{path}" fill="{rim}" transform="translate({dx},{dy})"/>' if rim_on else ""
    return r + f'<path d="{path}" fill="{fill}" stroke="{OUT}" stroke-width="{c.sw(sw)}" stroke-linejoin="round" {extra}/>'

def bumpy(pts, amp, every=1):
    """insert outward bumps between points (curls / fur)"""
    out = []
    n = len(pts)
    cx = sum(p[0] for p in pts) / n; cy = sum(p[1] for p in pts) / n
    for i in range(n):
        (x0, y0), (x1, y1) = pts[i], pts[(i + 1) % n]
        out.append((x0, y0))
        if i % every == 0:
            mx, my = (x0 + x1) / 2, (y0 + y1) / 2
            vx, vy = mx - cx, my - cy; L = math.hypot(vx, vy) or 1
            out.append((mx + vx / L * amp, my + vy / L * amp))
    return out

# ============================================================== palettes / specs
SKINS = {
    "tan": ("#c98a5e", "#9a5f3f", "#e2a676"),
    "light": ("#d9a07a", "#ad7253", "#efbd96"),
    "olive": ("#b98256", "#8a5838", "#d49c70"),
    "old": ("#c08661", "#8f5a3e", "#d9a37f"),
}

def spec(**kw):
    base = dict(kind="man", skin="tan", hair="long_curly", hair_col="#17100c", beard="full", beard_col="#17100c",
                head="none", head_col="#7a5a3a", garment="tunic", col="#4a3017", col2="#2d1c0c", pattern="brocade",
                cloak=None, trousers="#2a2018", boots="#24150c", build=1.0, hs=1.0, bs=1.0, belt="#2b190c",
                sash=None, fur=None, grey=0.0, scarf_col="#2a3b6a", scarf_edge="#c9a24a", diadem=False, iris="#4a2a17")
    base.update(kw)
    return base

def pose(**kw):
    base = dict(turn=0.15, tilt=0.0, nod=0.0, blink=0.0, gx=0.2, gy=0.0, brow=0.0, furrow=0.3, mouth_o=0.0, mouth_w=1.0,
                smile=0.0, wind=0.4, breathe=0.0, armL=(8, 10), armR=(8, 10), legs="stand", phase=0.0, propL=None, propR=None,
                sad=0.0, chains=False, glow=0.0, red=0.0, red_reveal=1.0)
    base.update(kw)
    return base

# ============================================================== head parts
def hair_back(c, S, p, t):
    st = S["hair"]
    if st not in ("long_curly", "teen_curly") or S["head"] == "scarf":
        return ""
    wind = p["wind"]
    L = [(-96, -250), (-118, -214), (-126, -172), (-138, -128), (-136, -86), (-150, -46), (-148, -6), (-166, 30), (-160, 70), (-186, 96)]
    R = [(96, -250), (116, -214), (124, -172), (134, -128), (130, -86), (142, -46), (138, -6), (152, 28), (140, 62), (150, 88)]
    if st == "teen_curly":
        L = L[:6] + [(-132, -20)]; R = R[:6] + [(126, -20)]
    def wv(pts, ph):
        n = len(pts); out = []
        for i, (x, y) in enumerate(pts):
            f = (i / (n - 1)) ** 1.6
            out.append((x - 10 * wind * f * (1.6 + math.sin(t * 3.1 + i * 0.9 + ph)) , y + 3 * wind * f * math.sin(t * 2.3 + i)))
        return out
    L = wv(L, 0.0); R = wv(R, 1.3)
    def curl_edge(pts, side):
        out = []
        for i in range(len(pts) - 1):
            (x0, y0), (x1, y1) = pts[i], pts[i + 1]
            out.append((x0, y0)); out.append(((x0 + x1) / 2 + side * 11, (y0 + y1) / 2))
        out.append(pts[-1]); return out
    yb = L[-1][1] + 18
    pts = curl_edge(L, -1) + [(L[-1][0] + 40, yb + 6), (0, yb + 10), (R[-1][0] - 30, yb)] + list(reversed(curl_edge(R, 1)))
    d = smooth_path(pts)
    hi = S.get("hair_hi", "#3b2a1f")
    strands = ""
    for i, (x0, y0, x1, y1) in enumerate([(-112, -150, -132, yb - 50), (110, -150, 122, yb - 60)]):
        sw_ = 6 * math.sin(t * 2.6 + i)
        strands += (f'<path d="M {x0} {y0} C {x0-14+sw_} {y0+60}, {x1+14+sw_} {y1-60}, {fmt(x1+sw_-16*wind)} {y1}" '
                    f'stroke="{hi}" stroke-width="{c.sw(3)}" fill="none" stroke-linecap="round" opacity="0.8"/>')
    return rimmed(c, d, S["hair_col"], dx=3.5, dy=-1) + strands

def face_d(S, p):
    """the outline of the face (head coords)"""
    s = p["turn"]; k = S["kind"]
    if k == "woman":
        return (f"M -88 -262 C -94 -210, -96 -168, -88 -130 C -80 -98, -50 -66, {fmt(4*s)} -60 C 52 -66, 80 -98, 88 -130 "
                f"C 96 -168, 94 -210, 88 -262 Z")
    if k == "boy":
        return (f"M -94 -262 C -102 -214, -104 -166, -96 -132 C -86 -98, -54 -72, {fmt(4*s)} -68 C 58 -72, 88 -98, 96 -132 "
                f"C 104 -166, 102 -214, 94 -262 Z")
    return (f"M -94 -262 C -100 -205, -102 -160, -94 -122 C -86 -88, -56 -58, {fmt(4*s)} -52 "
            f"C 60 -58, 88 -88, 96 -122 C 104 -160, 102 -205, 96 -262 Z")

def face_shape(c, S, p):
    sk, sh, hi = SKINS[S["skin"]]
    s = p["turn"]; k = S["kind"]
    d = face_d(S, p)
    gid = c.uid("fg")
    out = rimmed(c, d, sk, dx=3, dy=-1)
    out += (f'<defs><linearGradient id="{gid}" x1="-100" y1="0" x2="100" y2="0" gradientUnits="userSpaceOnUse">'
            f'<stop offset="0" stop-color="{sh}" stop-opacity="0.75"/><stop offset="0.38" stop-color="{sh}" stop-opacity="0.0"/>'
            f'<stop offset="1" stop-color="{sh}" stop-opacity="0.0"/></linearGradient></defs><path d="{d}" fill="url(#{gid})"/>')
    out += f'<path d="M 70 -240 C 90 -200, 94 -160, 88 -128" stroke="{hi}" stroke-width="{c.sw(5)}" fill="none" stroke-linecap="round" opacity="0.6"/>'
    if S["head"] not in ("none",) or S["hair"] in ("short", "boy_curly", "teen_curly", "long_curly"):
        out += '<path d="M -94 -252 C -40 -258, 40 -258, 94 -252 L 94 -228 C 40 -236, -40 -236, -94 -228 Z" fill="#7a4630" opacity="0.35"/>'
    blush = 0.32 if k in ("woman", "boy") else 0.22
    out += (f'<ellipse cx="{fmt(56+6*s)}" cy="-150" rx="22" ry="12" fill="#e07a6a" opacity="{blush}"/>'
            f'<ellipse cx="{fmt(-52+6*s)}" cy="-150" rx="20" ry="11" fill="#c0705a" opacity="{blush*0.6:.2f}"/>')
    if k == "old":
        out += (f'<path d="M -60 -232 C -30 -238, 30 -238, 60 -232 M -50 -220 C -20 -225, 20 -225, 50 -220" stroke="{sh}" stroke-width="{c.sw(2.4)}" fill="none" opacity="0.8"/>'
                f'<path d="M -70 -170 l -10 6 M -70 -164 l -9 9 M 72 -170 l 10 6 M 72 -164 l 9 9" stroke="{sh}" stroke-width="{c.sw(2)}" opacity="0.8"/>')
    return out

def ears(c, S, p):
    if S["head"] in ("scarf",) or S["hair"] in ("long_curly",):
        return ""
    sk, sh, hi = SKINS[S["skin"]]
    o = ""
    for side in (-1, 1):
        x = side * (98 + (2 if S["kind"] == "boy" else 0))
        d = f"M {x} -196 C {x+side*22} -204, {x+side*24} -160, {x+side*4} -146 Z"
        o += rimmed(c, d, sk, dx=2, dy=-1, sw=2.2) + f'<path d="M {x+side*6} -186 C {x+side*14} -182, {x+side*14} -166, {x+side*6} -160" stroke="{sh}" stroke-width="{c.sw(2)}" fill="none"/>'
    return o

def eye(c, S, cx, cy, w, blink, gx, gy, side, sad=0.0):
    k = S["kind"]
    big = 1.12 if k == "boy" else (1.04 if k == "woman" else 1.0)
    hw = 23 * w * big
    if blink > 0.86:
        return (f'<path d="M {fmt(cx-hw-2)} {fmt(cy+1)} C {fmt(cx-hw*0.4)} {fmt(cy+7)}, {fmt(cx+hw*0.4)} {fmt(cy+7)}, {fmt(cx+hw+2)} {fmt(cy)}" '
                f'stroke="{OUT}" stroke-width="{c.sw(4.2)}" fill="none" stroke-linecap="round"/>' +
                (f'<path d="M {fmt(cx+side*hw)} {fmt(cy+2)} l {fmt(side*7)} 3" stroke="{OUT}" stroke-width="{c.sw(2.6)}" stroke-linecap="round"/>' if k == "woman" else ""))
    o = 1 - blink
    top = cy + 1 - 12 * o * big
    al = (f"M {fmt(cx-hw)} {fmt(cy+1)} C {fmt(cx-hw*0.55)} {fmt(top)}, {fmt(cx+hw*0.45)} {fmt(top-1)}, {fmt(cx+hw)} {fmt(cy-1)} "
          f"C {fmt(cx+hw*0.5)} {fmt(cy+8*o*big+1)}, {fmt(cx-hw*0.5)} {fmt(cy+8*o*big+1)}, {fmt(cx-hw)} {fmt(cy+1)} Z")
    cid = c.uid(f"ec{side+1}")
    r = 11.5 * min(1, w + 0.1) * big
    ix, iy = cx + gx * 8 * w, cy - 1 + gy * 4
    out = (f'<clipPath id="{cid}"><path d="{al}"/></clipPath><path d="{al}" fill="#f4ece2"/>'
           f'<g clip-path="url(#{cid})">'
           f'<circle cx="{fmt(ix)}" cy="{fmt(iy)}" r="{fmt(r)}" fill="{S["iris"]}"/>'
           f'<circle cx="{fmt(ix)}" cy="{fmt(iy)}" r="{fmt(r*0.63)}" fill="#2a170c"/>'
           f'<circle cx="{fmt(ix)}" cy="{fmt(iy)}" r="{fmt(r*0.38)}" fill="#090403"/>'
           f'<circle cx="{fmt(ix+3.2)}" cy="{fmt(iy-3.4)}" r="{fmt(2.6*big)}" fill="#fff"/>'
           f'<path d="M {fmt(cx-hw)} {fmt(cy-16)} L {fmt(cx+hw)} {fmt(cy-16)} L {fmt(cx+hw)} {fmt(top+5)} L {fmt(cx-hw)} {fmt(top+5)} Z" fill="#000" opacity="0.18"/>'
           f'</g>'
           f'<path d="M {fmt(cx-hw-2)} {fmt(cy+2)} C {fmt(cx-hw*0.55)} {fmt(top-1)}, {fmt(cx+hw*0.45)} {fmt(top-2)}, {fmt(cx+hw+3)} {fmt(cy-2)}" '
           f'stroke="{OUT}" stroke-width="{c.sw(4.6)}" fill="none" stroke-linecap="round"/>')
    if k == "woman":
        out += f'<path d="M {fmt(cx+side*(hw+1))} {fmt(cy-2)} l {fmt(side*9)} -6 M {fmt(cx+side*(hw-4))} {fmt(top+3)} l {fmt(side*6)} -7" stroke="{OUT}" stroke-width="{c.sw(2.8)}" stroke-linecap="round"/>'
    else:
        out += f'<path d="M {fmt(cx+side*(hw+1))} {fmt(cy-1)} l {fmt(side*6)} -4" stroke="{OUT}" stroke-width="{c.sw(3)}" stroke-linecap="round"/>'
    sk, sh, hi = SKINS[S["skin"]]
    out += (f'<path d="M {fmt(cx-hw*0.8)} {fmt(top-6)} C {fmt(cx-hw*0.3)} {fmt(top-12)}, {fmt(cx+hw*0.4)} {fmt(top-12)}, {fmt(cx+hw*0.85)} {fmt(top-5)}" '
            f'stroke="#7a4630" stroke-width="{c.sw(2.2)}" fill="none" stroke-linecap="round" opacity="0.7"/>'
            f'<path d="M {fmt(cx-hw*0.7)} {fmt(cy+8*o+3)} C {fmt(cx-hw*0.2)} {fmt(cy+9*o+5)}, {fmt(cx+hw*0.3)} {fmt(cy+9*o+5)}, {fmt(cx+hw*0.75)} {fmt(cy+8*o+2)}" '
            f'stroke="{sh}" stroke-width="{c.sw(2.2)}" fill="none" stroke-linecap="round"/>')
    if sad > 0.05:
        out += f'<path d="M {fmt(cx-hw*0.5)} {fmt(cy+12)} C {fmt(cx)} {fmt(cy+16)}, {fmt(cx+hw*0.5)} {fmt(cy+15)}, {fmt(cx+hw*0.6)} {fmt(cy+12)}" stroke="#bfe0f0" stroke-width="{c.sw(3)}" fill="none" opacity="{min(0.9,sad):.2f}"/>'
    return out

def brow(c, S, cx, cy, side, raise_, furrow, sad=0.0):
    k = S["kind"]
    th = {"woman": 0.55, "boy": 0.75, "old": 0.9}.get(k, 1.0)
    col = "#e9e3da" if k == "old" else S["hair_col"]
    y = cy - 6 * raise_
    inner = 7 * furrow - 8 * sad
    xo, xi = cx + side * 30, cx - side * 26
    d = (f"M {fmt(xo)} {fmt(y+6)} C {fmt(cx+side*14)} {fmt(y-10)}, {fmt(cx-side*8)} {fmt(y-11+inner*0.3)}, {fmt(xi)} {fmt(y-3+inner)} "
         f"L {fmt(xi)} {fmt(y-3+inner+9*th)} C {fmt(cx-side*8)} {fmt(y-11+inner*0.3+10*th)}, {fmt(cx+side*12)} {fmt(y-10+10*th)}, {fmt(xo)} {fmt(y+6+5*th)} Z")
    return f'<path d="{d}" fill="{col}" stroke="{col}" stroke-width="{c.sw(1)}"/>'

def nose(c, S, p):
    sk, sh, hi = SKINS[S["skin"]]
    s = p["turn"]; bx, tx = 8 * s, 16 * s
    sz = 0.82 if S["kind"] in ("woman", "boy") else 1.0
    yt = -133 + (1 - sz) * 30
    return (f'<path d="M {fmt(-8+bx)} -190 C {fmt(-12+bx)} -168, {fmt(-18*sz+tx)} {fmt(yt+13)}, {fmt(-20*sz+tx)} {fmt(yt)} '
            f'C {fmt(-12*sz+tx)} {fmt(yt+8)}, {fmt(-3+tx)} {fmt(yt+9)}, {fmt(2+tx)} {fmt(yt+6)} C {fmt(-6+tx)} {fmt(yt-7)}, {fmt(-4+bx)} -170, {fmt(-2+bx)} -190 Z" fill="{sh}" opacity="0.7"/>'
            f'<path d="M {fmt(-19*sz+tx)} {fmt(yt)} C {fmt(-14*sz+tx)} {fmt(yt+10)}, {fmt(10*sz+tx)} {fmt(yt+12)}, {fmt(18*sz+tx)} {fmt(yt+1)}" stroke="#6e3f28" stroke-width="{c.sw(3)}" fill="none" stroke-linecap="round"/>'
            f'<ellipse cx="{fmt(-9*sz+tx)}" cy="{fmt(yt+5)}" rx="{fmt(4.5*sz)}" ry="2.6" fill="#4a2414"/><ellipse cx="{fmt(9*sz+tx)}" cy="{fmt(yt+5)}" rx="{fmt(4.5*sz)}" ry="2.6" fill="#4a2414"/>'
            f'<path d="M {fmt(6+tx)} -168 C {fmt(10+tx)} -155, {fmt(12+tx)} -146, {fmt(10+tx)} -138" stroke="{hi}" stroke-width="{c.sw(3)}" fill="none" stroke-linecap="round" opacity="0.8"/>')

def lips(c, S, p):
    """beardless mouth (women, boys)"""
    s = p["turn"]; o = p["mouth_o"]; w = p["mouth_w"]; sm = p["smile"]
    mx = 10 * s; my = -98 if S["kind"] == "woman" else -100
    hw = (16 if S["kind"] == "woman" else 15) * w + 5 * o
    up = 4 * sm
    yb = my + 2 + 20 * o
    d = (f"M {fmt(mx-hw)} {fmt(my-up)} C {fmt(mx-hw*0.5)} {fmt(my-3)}, {fmt(mx+hw*0.5)} {fmt(my-3)}, {fmt(mx+hw)} {fmt(my-up)} "
         f"C {fmt(mx+hw*0.7)} {fmt(yb)}, {fmt(mx-hw*0.7)} {fmt(yb)}, {fmt(mx-hw)} {fmt(my-up)} Z")
    lipc = "#b55a52" if S["kind"] == "woman" else "#a85c4a"
    out = ""
    if o > 0.06:
        cid = c.uid("mc")
        out += (f'<path d="{d}" fill="#3a1110" stroke="{OUT}" stroke-width="{c.sw(2)}"/>'
                f'<clipPath id="{cid}"><path d="{d}"/></clipPath><g clip-path="url(#{cid})">'
                f'<rect x="{fmt(mx-hw)}" y="{fmt(my-4)}" width="{fmt(2*hw)}" height="{fmt(4+3*o)}" fill="#efe6da"/>'
                f'<ellipse cx="{fmt(mx)}" cy="{fmt(yb+2)}" rx="{fmt(hw*0.6)}" ry="{fmt(4+5*o)}" fill="#a3443c"/></g>')
    else:
        out += f'<path d="M {fmt(mx-hw)} {fmt(my-up)} C {fmt(mx-hw*0.4)} {fmt(my+2)}, {fmt(mx+hw*0.4)} {fmt(my+2)}, {fmt(mx+hw)} {fmt(my-up)}" stroke="{OUT}" stroke-width="{c.sw(2.6)}" fill="none" stroke-linecap="round"/>'
    # upper lip and lower lip
    out += (f'<path d="M {fmt(mx-hw-1)} {fmt(my-up)} C {fmt(mx-hw*0.5)} {fmt(my-8)}, {fmt(mx-3)} {fmt(my-9)}, {fmt(mx)} {fmt(my-6)} '
            f'C {fmt(mx+3)} {fmt(my-9)}, {fmt(mx+hw*0.5)} {fmt(my-8)}, {fmt(mx+hw+1)} {fmt(my-up)} C {fmt(mx+hw*0.4)} {fmt(my-2)}, {fmt(mx-hw*0.4)} {fmt(my-2)}, {fmt(mx-hw-1)} {fmt(my-up)} Z" fill="{lipc}" opacity="0.9"/>'
            f'<path d="M {fmt(mx-hw*0.7)} {fmt(yb+1)} C {fmt(mx-hw*0.4)} {fmt(yb+9)}, {fmt(mx+hw*0.4)} {fmt(yb+9)}, {fmt(mx+hw*0.7)} {fmt(yb+1)} '
            f'C {fmt(mx+hw*0.4)} {fmt(yb+3)}, {fmt(mx-hw*0.4)} {fmt(yb+3)}, {fmt(mx-hw*0.7)} {fmt(yb+1)} Z" fill="{lipc}"/>')
    if sm > 0.1:
        out += f'<path d="M {fmt(mx-hw-4)} {fmt(my-up-4)} q -4 6 0 10 M {fmt(mx+hw+4)} {fmt(my-up-4)} q 4 6 0 10" stroke="#8a4a36" stroke-width="{c.sw(2)}" fill="none" opacity="{min(1,sm):.2f}"/>'
    return out

def beard_mouth(c, S, p, t):
    """mouth under a mustache"""
    s = p["turn"]; o = p["mouth_o"]; w = p["mouth_w"]
    mx = 10 * s; hw = 15 * w + 6 * o; yb = -100 + 3 + 25 * o
    d = (f"M {fmt(mx-hw)} -100 C {fmt(mx-hw*0.6)} -103, {fmt(mx+hw*0.6)} -103, {fmt(mx+hw)} -100 "
         f"C {fmt(mx+hw*0.75)} {fmt(yb)}, {fmt(mx-hw*0.75)} {fmt(yb)}, {fmt(mx-hw)} -100 Z")
    out = f'<path d="{d}" fill="#3a1110" stroke="{OUT}" stroke-width="{c.sw(2)}"/>'
    if o > 0.2:
        cid = c.uid("bm")
        out += (f'<clipPath id="{cid}"><path d="{d}"/></clipPath><g clip-path="url(#{cid})">'
                f'<rect x="{fmt(mx-hw)}" y="-101" width="{fmt(2*hw)}" height="{fmt(4+3*o)}" fill="#efe6da"/>'
                f'<ellipse cx="{fmt(mx)}" cy="{fmt(yb+2)}" rx="{fmt(hw*0.6)}" ry="{fmt(4+5*o)}" fill="#a3443c"/></g>')
    out += (f'<path d="M {fmt(mx-hw*0.75)} {fmt(yb-1)} C {fmt(mx-hw*0.4)} {fmt(yb+7)}, {fmt(mx+hw*0.4)} {fmt(yb+7)}, {fmt(mx+hw*0.75)} {fmt(yb-1)} '
            f'C {fmt(mx+hw*0.4)} {fmt(yb+2)}, {fmt(mx-hw*0.4)} {fmt(yb+2)}, {fmt(mx-hw*0.75)} {fmt(yb-1)} Z" fill="#8b4a3c"/>')
    return out

def beard(c, S, p, t):
    b = S["beard"]
    if not b:
        return ""
    s = p["turn"]; j = 9 * p["mouth_o"]; wind = p["wind"]
    col = S["beard_col"]; hi = "#9b948c" if b == "white" else S.get("hair_hi", "#3b2a1f")
    if b == "white":
        col = "#e9e4dc"
    if b == "light":
        band = ("M -97 -178 C -100 -130, -90 -95, -60 -70 C -40 -56, -20 -50, 0 -48 C 20 -50, 40 -56, 60 -70 C 90 -95, 100 -130, 97 -178 "
                "L 86 -178 C 88 -138, 80 -106, 56 -86 C 38 -74, 18 -68, 0 -66 C -18 -68, -38 -74, -56 -86 C -80 -106, -88 -138, -86 -178 Z")
        chin = f"M -24 {-60+j} C -20 {-44+j}, 20 {-44+j}, 24 {-60+j} C 14 {-70+j}, -14 {-70+j}, -24 {-60+j} Z"
        must = (f"M {fmt(12*s-4)} -124 C {fmt(12*s-18)} -125, {fmt(12*s-32)} -119, {fmt(12*s-40)} -104 C {fmt(12*s-30)} -108, {fmt(12*s-18)} -110, {fmt(12*s-6)} -110 "
                f"L {fmt(12*s+6)} -110 C {fmt(12*s+18)} -110, {fmt(12*s+30)} -108, {fmt(12*s+40)} -104 C {fmt(12*s+32)} -119, {fmt(12*s+18)} -125, {fmt(12*s+4)} -124 Z")
        return (f'<path d="{band}" fill="{col}" opacity="0.92"/>' + beard_mouth(c, S, p, t) +
                f'<path d="{chin}" fill="{col}" opacity="0.9"/>' + rimmed(c, must, col, dx=1.5, dy=-1, sw=1.4))
    if b == "short":
        up = ("M -96 -170 C -96 -140, -88 -122, -72 -114 C -60 -108, -46 -104, -36 -102 L 36 -102 C 46 -104, 60 -108, 72 -114 "
              "C 88 -122, 96 -140, 96 -170 C 102 -130, 102 -100, 96 -80 L -96 -80 C -102 -100, -102 -130, -96 -170 Z")
        bot = [(-96, -86), (-90, -60 + j), (-70, -40 + j), (-40, -28 + j), (0, -22 + j), (40, -28 + j), (70, -40 + j), (90, -60 + j), (96, -86)]
        chin = smooth_path(bot + [(40, -100), (-40, -100)])
        must = (f"M {fmt(12*s-4)} -126 C {fmt(12*s-20)} -127, {fmt(12*s-38)} -120, {fmt(12*s-46)} -100 C {fmt(12*s-38)} -104, {fmt(12*s-24)} -106, {fmt(12*s-8)} -105 "
                f"L {fmt(12*s+8)} -105 C {fmt(12*s+24)} -106, {fmt(12*s+38)} -104, {fmt(12*s+46)} -100 C {fmt(12*s+38)} -120, {fmt(12*s+20)} -127, {fmt(12*s+4)} -126 Z")
        return (rimmed(c, up, col, dx=2, dy=-1, sw=2) + rimmed(c, chin, col, dx=2, dy=-1, sw=2) +
                beard_mouth(c, S, p, t) + rimmed(c, must, col, dx=2, dy=-1, sw=1.8))
    long_ = {"full": 42, "white": 120, "javidan": 60, "father": 6, "grey": 42}.get(b, 42)
    up = ("M -96 -164 C -96 -140, -88 -122, -72 -114 C -60 -108, -46 -104, -36 -102 L 36 -102 C 46 -104, 60 -108, 72 -114 "
          "C 88 -122, 96 -140, 96 -164 C 104 -130, 108 -100, 104 -76 L -104 -76 C -108 -100, -104 -130, -96 -164 Z")
    burns = ("M -101 -238 L -84 -238 C -86 -210, -86 -184, -84 -160 L -98 -150 C -102 -180, -103 -210, -101 -238 Z "
             "M 101 -238 L 84 -238 C 86 -210, 86 -184, 84 -160 L 98 -150 C 102 -180, 103 -210, 101 -238 Z")
    w = 5 * math.sin(t * 2.4) - 8 * wind
    L = long_
    wid = 1.15 if b == "javidan" else 1.0
    bot = [(-104 * wid, -84), (-98 * wid, -46 + j + L * 0.1), (-82 * wid, -14 + j + L * 0.4), (-62 * wid, 10 + j + L * 0.62), (-40, 26 + j + L * 0.82),
           (-16, 36 + j + L * 0.95), (6 + w * 0.5, 42 + j + L), (28 + w * 0.6, 34 + j + L * 0.92), (50, 20 + j + L * 0.8),
           (74 * wid, -2 + j + L * 0.55), (94 * wid, -34 + j + L * 0.25), (104 * wid, -84)]
    edge = []
    for i in range(len(bot) - 1):
        (x0, y0), (x1, y1) = bot[i], bot[i + 1]
        edge.append((x0, y0))
        if 1 <= i <= len(bot) - 3:
            mx, my = (x0 + x1) / 2, (y0 + y1) / 2
            nx, ny = (y1 - y0), -(x1 - x0); ln = math.hypot(nx, ny) or 1
            edge.append((mx - nx / ln * 9, my - ny / ln * 9))
    edge.append(bot[-1])
    if b == "father":
        edge = [(-104, -84), (-96, -50 + j), (-70, -24 + j), (-30, -10 + j), (0, -6 + j), (30, -10 + j), (70, -24 + j), (96, -50 + j), (104, -84)]
    chin = smooth_path(edge + [(60, -100), (-60, -100)])
    strands = "".join(f'<path d="M {fmt(x0+6*s)} {fmt(y0+j*0.6)} C {x0-8} {fmt(y0+25+j)}, {x1+8} {fmt(y1-20+j)}, {fmt(x1+6*s)} {fmt(y1+j)}" stroke="{hi}" '
                      f'stroke-width="{c.sw(2.6)}" fill="none" stroke-linecap="round" opacity="0.75"/>'
                      for (x0, y0, x1, y1) in [(-70, -70, -56, L * 0.2), (-40, -50, -30, 22 + L * 0.5), (0, -40, 4, 30 + L * 0.7), (36, -50, 30, 20 + L * 0.5), (70, -72, 62, -6 + L * 0.2)])
    greys = ""
    if b in ("grey", "javidan") or S["grey"] > 0:
        greys = "".join(f'<path d="M {x} {y+j} c 4 14, -2 26, 2 40" stroke="#bdb6ad" stroke-width="{c.sw(2.4)}" fill="none" opacity="{0.4+0.5*S["grey"]:.2f}"/>'
                        for x, y in [(-60, -60), (-20, -30), (30, -40), (66, -64), (0, 0)])
    must = (f"M {fmt(12*s-4)} -126 C {fmt(12*s-22)} -128, {fmt(12*s-44)} -120, {fmt(12*s-56+(-3*wind))} {fmt(-94+3*p['mouth_o'])} "
            f"C {fmt(12*s-46)} {fmt(-100+3*p['mouth_o'])}, {fmt(12*s-30)} -104, {fmt(12*s-10)} -103 L {fmt(12*s+10)} -103 "
            f"C {fmt(12*s+30)} -104, {fmt(12*s+46)} {fmt(-100+3*p['mouth_o'])}, {fmt(12*s+56-3*wind)} {fmt(-94+3*p['mouth_o'])} "
            f"C {fmt(12*s+44)} -120, {fmt(12*s+22)} -128, {fmt(12*s+4)} -126 Z")
    curls = "" if b == "father" else "".join(
        f'<path d="M {x} {fmt(y+j)} c 6 -8, 14 -2, 10 6 c -3 6, -12 4, -10 -3" stroke="{hi}" stroke-width="{c.sw(2.4)}" fill="none" opacity="0.8"/>'
        for x, y in [(-60, -40 + L * 0.3), (-24, -10 + L * 0.5), (14, 4 + L * 0.5), (48, -24 + L * 0.3), (-80, -70), (76, -66)])
    hiside = (f"M 70 -104 C 88 -110, 98 -126, 100 -150 C 106 -110, 104 -60, 86 {fmt(-14+j+L*0.4)} C 74 {fmt(4+j+L*0.6)}, 60 {fmt(16+j+L*0.7)}, 48 {fmt(22+j+L*0.7)} "
              f"C 66 0, 80 -40, 70 -104 Z")
    hicol = "#ffffff" if b == "white" else "#33251c"
    return (rimmed(c, burns, col, dx=2, dy=-1, sw=1.6) + rimmed(c, up, col, dx=3, dy=-1) + rimmed(c, chin, col, dx=3, dy=-1) +
            f'<path d="{hiside}" fill="{hicol}" opacity="0.55"/>' + strands + greys + curls +
            beard_mouth(c, S, p, t) + rimmed(c, must, col, dx=2, dy=-1, sw=2))

# ---------------------------------------------------------------- hair (top) & headwear
def hair_top(c, S, p, t):
    st = S["hair"]; col = S["hair_col"]
    if S["head"] in ("helmet", "fur_hat", "turban", "scarf"):
        return ""
    if st in ("long_curly", "teen_curly", "boy_curly"):
        pts = [(-104, -236), (-112, -290), (-80, -336), (-30, -356), (30, -356), (80, -336), (112, -290), (104, -236), (70, -262), (20, -270), (-30, -268), (-74, -258)]
        pts = bumpy(pts, 12)
        d = smooth_path(pts)
        return rimmed(c, d, col, dx=3, dy=-2) + "".join(
            f'<path d="M {x} {y} c 8 -10, 18 -2, 12 8" stroke="{S.get("hair_hi","#3b2a1f")}" stroke-width="{c.sw(2.6)}" fill="none"/>' for x, y in [(-60, -310), (-10, -330), (40, -318), (70, -290)])
    if st == "short":
        d = smooth_path([(-100, -226), (-106, -290), (-70, -338), (0, -352), (70, -338), (106, -290), (100, -226), (84, -258), (30, -268), (-30, -268), (-84, -258)])
        return rimmed(c, d, col, dx=3, dy=-2)
    return ""

def headwear(c, S, p, t):
    h = S["head"]; s = p["turn"]; wind = p["wind"]; rx = 10 * s
    if h == "helmet":
        hc = S.get("helm", ("#6e4519", "#b9832f", "#f0c66a")); plume = S.get("plume", "#b3181d")
        cone = f"M -104 -256 C -100 -312, -52 -362, {fmt(rx)} -396 C 52 -362, 100 -312, 104 -256 Z"
        shade = f"M -104 -256 C -100 -312, -52 -362, {fmt(rx)} -396 C -24 -350, -50 -300, -56 -256 Z"
        spec_ = f"M {fmt(26+rx*0.5)} -364 C 50 -336, 66 -300, 70 -262 L 84 -262 C 80 -304, 62 -342, {fmt(34+rx*0.5)} -372 Z"
        band = "M -110 -262 C -60 -272, 60 -272, 110 -262 L 108 -232 C 60 -242, -60 -242, -108 -232 Z"
        zig = "M -100 -248 " + " ".join(f"L {-100 + i * 10} {-254 if i % 2 else -244}" for i in range(1, 21))
        rivets = "".join(f'<circle cx="{x}" cy="{fmt(-249 + abs(x) * 0.07)}" r="3.4" fill="{hc[2]}" stroke="{OUT}" stroke-width="{c.sw(1.2)}"/>' for x in (-88, -44, 0, 44, 88))
        px, py = rx, -400; pl = [(px, py)]
        for i in range(1, 8):
            u = i / 7
            pl.append((px - 17 * i - 26 * wind * u, py - 10 * math.sin(u * 2.4) + 6 * math.sin(t * 5 + i) * u))
        top = [(x, y - 11 * (1 - i / 7) ** 0.7 - 2) for i, (x, y) in enumerate(pl)]
        bot = [(x, y + 13 * (1 - i / 7) ** 0.7 + 2) for i, (x, y) in enumerate(pl)]
        gid = c.uid("bz")
        return (f'<defs><linearGradient id="{gid}" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{hc[0]}"/><stop offset="0.55" stop-color="{hc[1]}"/>'
                f'<stop offset="1" stop-color="{hc[2]}"/></linearGradient></defs>' +
                (rimmed(c, smooth_path(top + list(reversed(bot))), plume, dx=2, dy=-2) if plume else "") +
                f'<circle cx="{fmt(rx)}" cy="-402" r="7" fill="{hc[2]}" stroke="{OUT}" stroke-width="{c.sw(2)}"/>' +
                rimmed(c, cone, f"url(#{gid})", dx=3.5, dy=-2) + f'<path d="{shade}" fill="{hc[0]}" opacity="0.55"/>'
                f'<path d="{spec_}" fill="#fff3c8" opacity="0.55"/>'
                f'<path d="M {fmt(rx)} -394 C {fmt(rx*0.8-2)} -340, {fmt(rx*0.5-2)} -300, {fmt(rx*0.3)} -266" stroke="{OUT}" stroke-width="{c.sw(2.4)}" fill="none"/>' +
                rimmed(c, band, hc[1], dx=3, dy=-1) + f'<path d="{zig}" stroke="{S.get("helm_zig", "#f6d488")}" stroke-width="{c.sw(2)}" fill="none" opacity="0.85"/>' + rivets)
    if h == "fur_hat":
        pts = [(-112, -238), (-124, -300), (-112, -370), (-60, -404), (0, -412), (60, -404), (112, -370), (124, -300), (112, -238), (60, -228), (0, -226), (-60, -228)]
        d = smooth_path(bumpy(pts, 9))
        strokes = "".join(f'<path d="M {x} {y} q {4+3*math.sin(i)} 14 0 26" stroke="#4a3a2e" stroke-width="{c.sw(2.4)}" fill="none" opacity="0.7"/>'
                          for i, (x, y) in enumerate([(-80, -360), (-40, -380), (0, -386), (40, -380), (80, -360), (-90, -310), (-50, -330), (-10, -340), (30, -336), (70, -320), (96, -290), (-60, -280), (-20, -290), (20, -292), (60, -282)]))
        return rimmed(c, d, S["head_col"], dx=3, dy=-2) + f'<path d="M -110 -300 C -60 -320, 60 -320, 112 -300" stroke="#5b4a3c" stroke-width="{c.sw(3)}" fill="none" opacity="0.6"/>' + strokes
    if h == "turban":
        col = S["head_col"]
        dome = smooth_path([(-114, -236), (-124, -290), (-96, -350), (-40, -380), (20, -384), (80, -360), (118, -310), (116, -240), (60, -230), (0, -228), (-60, -230)])
        wraps = "".join(f'<path d="M -116 {y} C -60 {y-30-k*6}, 60 {y-40+k*4}, 118 {y-22}" stroke="#000" stroke-width="{c.sw(3)}" fill="none" opacity="0.18"/>'
                        for k, y in enumerate([-250, -280, -310, -336]))
        tail = f'<path d="M 90 -300 C 130 -280, 136 -230, {fmt(150-14*wind)} -170 L {fmt(130-14*wind)} -168 C 120 -220, 110 -260, 84 -280 Z" fill="{col}" stroke="{OUT}" stroke-width="{c.sw(2)}"/>' if S.get("turban_tail") else ""
        return tail + rimmed(c, dome, col, dx=3, dy=-2) + wraps
    if h == "cap":
        col = S["head_col"]
        d = smooth_path([(-104, -240), (-108, -300), (-70, -346), (0, -360), (70, -346), (108, -300), (104, -240), (0, -252)])
        return (rimmed(c, d, col, dx=3, dy=-2) +
                f'<path d="M -106 -250 C -50 -264, 50 -264, 106 -250 L 104 -236 C 50 -248, -50 -248, -104 -236 Z" fill="#000" opacity="0.25"/>')
    return ""

def scarf_back(c, S, p, t):
    if S["head"] != "scarf":
        return ""
    wind = p["wind"]
    w = 8 * wind * math.sin(t * 2.2)
    pts = [(-118, -250), (-124, -330), (-80, -382), (0, -398), (80, -382), (124, -330), (118, -250), (126, -150), (150, -40),
           (172 + w * 0.3, 60), (150, 120), (0, 130), (-150, 120), (-176 + w, 60), (-152, -40), (-128, -150)]
    return rimmed(c, smooth_path(pts), S["scarf_col"], dx=3, dy=-2)

def scarf_front(c, S, p, t):
    if S["head"] != "scarf":
        return ""
    col = S["scarf_col"]; ed = S["scarf_edge"]
    # band framing the face
    d = ("M -118 -250 C -116 -300, -70 -330, 0 -334 C 70 -330, 116 -300, 118 -250 C 116 -150, 100 -80, 60 -44 C 30 -30, -30 -30, -60 -44 "
         "C -100 -80, -116 -150, -118 -250 Z M -90 -262 C -96 -200, -98 -150, -88 -118 C -76 -84, -40 -58, 0 -56 C 40 -58, 76 -84, 88 -118 "
         "C 98 -150, 96 -200, 90 -262 C 60 -290, -60 -290, -90 -262 Z")
    out = f'<path d="{d}" fill="{col}" fill-rule="evenodd" stroke="{OUT}" stroke-width="{c.sw(2.6)}"/>'
    out += f'<path d="M -90 -262 C -60 -290, 60 -290, 90 -262" stroke="{ed}" stroke-width="{c.sw(5)}" fill="none"/>'
    if S["diadem"]:
        out += (f'<path d="M -92 -270 C -50 -294, 50 -294, 92 -270" stroke="#e8b84e" stroke-width="{c.sw(10)}" fill="none"/>'
                f'<path d="M -92 -270 C -50 -294, 50 -294, 92 -270" stroke="{OUT}" stroke-width="{c.sw(1.4)}" fill="none"/>' +
                "".join(f'<circle cx="{x}" cy="{fmt(-284+abs(x)*0.12)}" r="5" fill="#c4202a" stroke="{OUT}" stroke-width="{c.sw(1.2)}"/>' for x in (-50, 0, 50)))
    out += f'<path d="M 40 -300 C 70 -290, 96 -260, 104 -200" stroke="#ffffff" stroke-width="{c.sw(5)}" fill="none" opacity="0.18"/>'
    return out

def red_face(c, S, p):
    """Babak's red face (Samarra, 838): dark red smears wiped across the face with a sleeve, no wounds.
    p["red"] 0..1 strength; p["red_reveal"] 0..1 how far the wipe has gone (it runs from x -120 to x 120 of the head)"""
    a = max(0.0, min(1.0, p.get("red", 0.0))); rv = max(0.0, min(1.0, p.get("red_reveal", 1.0)))
    if a <= 0 or rv <= 0:
        return ""
    fx = 12 * p["turn"]
    fid = c.uid("rff"); wid = c.uid("rfw")
    xr = -126 + 252 * rv
    body = f'<path d="{face_d(S, p)}" fill="#9a2018" opacity="0.32"/>'
    for (x0, y0, x1, y1, w, op) in [(-104, -238, 104, -184, 34, 0.62), (-108, -176, 104, -124, 30, 0.58), (-70, -258, 60, -232, 16, 0.4)]:
        d = f"M {fmt(x0+fx)} {y0} C {fmt(x0*0.4+fx)} {fmt(y0+(y1-y0)*0.25-6)}, {fmt(x1*0.4+fx)} {fmt(y0+(y1-y0)*0.75-6)}, {fmt(x1+fx)} {y1}"
        body += (f'<path d="{d}" stroke="#7a120e" stroke-width="{w}" fill="none" stroke-linecap="round" opacity="{op}"/>'
                 f'<path d="{d}" stroke="#b4342a" stroke-width="{w*0.35:.1f}" fill="none" stroke-linecap="round" opacity="{op*0.6:.2f}" transform="translate(0,{-w*0.2:.1f})"/>')
    return (f'<defs><clipPath id="{fid}"><path d="{face_d(S, p)}"/></clipPath><clipPath id="{wid}"><rect x="-200" y="-400" width="{fmt(xr+200)}" height="500"/></clipPath></defs>'
            f'<g clip-path="url(#{fid})"><g clip-path="url(#{wid})"><g opacity="{a:.2f}">{body}</g></g></g>')

def head(c, S, p, t):
    turn = p["turn"]
    face_x = 12 * turn
    o = (face_shape(c, S, p) + ears(c, S, p) +
         f'<ellipse cx="{fmt(-40+face_x)}" cy="-182" rx="32" ry="19" fill="#7a4630" opacity="0.18"/>'
         f'<ellipse cx="{fmt(40+face_x)}" cy="-182" rx="30" ry="19" fill="#7a4630" opacity="0.12"/>')
    if p.get("red", 0) > 0:
        o += red_face(c, S, p)
    if S["beard"]:
        o += beard(c, S, p, t)
    else:
        o += lips(c, S, p)
    o += nose(c, S, p)
    o += eye(c, S, -40 + face_x, -178, 1 + 0.04 * turn, p["blink"], p["gx"], p["gy"], -1, p["sad"])
    o += eye(c, S, 40 + face_x, -178, 1 - 0.18 * turn, p["blink"], p["gx"], p["gy"], 1, p["sad"])
    o += brow(c, S, -40 + face_x, -206, -1, p["brow"], p["furrow"], p["sad"]) + brow(c, S, 40 + face_x, -206, 1, p["brow"], p["furrow"], p["sad"])
    o += hair_top(c, S, p, t) + headwear(c, S, p, t) + scarf_front(c, S, p, t)
    if p["glow"] > 0:   # the omen: blood-red glow at the roots of the hair
        g = p["glow"]
        o += (f'<path d="M -104 -236 C -112 -290, -80 -336, 0 -356 C 80 -336, 112 -290, 104 -236" stroke="#ff2a1a" stroke-width="{c.sw(14)}" fill="none" opacity="{0.55*g:.2f}" filter="url(#glowf)"/>'
              + "".join(f'<circle cx="{x}" cy="{y}" r="4" fill="#ff3020" opacity="{0.9*g:.2f}"/>' for x, y in [(-90, -262), (-60, -300), (-20, -322), (20, -326), (60, -306), (92, -266), (-100, -230), (100, -228)]))
    return o

# ============================================================== body
FEET = 1290

def arm_pts(shoulder, a1, a2, l1, l2, side):
    sx, sy = shoulder
    r1 = math.radians(a1); r2 = math.radians(a1 - a2)
    ex = sx + side * math.sin(r1) * l1; ey = sy + math.cos(r1) * l1
    hx = ex + side * math.sin(r2) * l2; hy = ey + math.cos(r2) * l2
    return (ex, ey), (hx, hy)

def limb(c, a, b, w0, w1, fill, sw=2.6):
    ax, ay = a; bx, by = b
    dx, dy = bx - ax, by - ay; L = math.hypot(dx, dy) or 1
    nx, ny = -dy / L, dx / L
    pts = [(ax + nx * w0, ay + ny * w0), (bx + nx * w1, by + ny * w1), (bx - nx * w1, by - ny * w1), (ax - nx * w0, ay - ny * w0)]
    return (f'<path d="M {P(pts)} Z" fill="{fill}" stroke="{OUT}" stroke-width="{c.sw(sw)}" stroke-linejoin="round"/>'
            f'<circle cx="{fmt(bx)}" cy="{fmt(by)}" r="{fmt(w1)}" fill="{fill}"/>')

def hand(c, S, x, y, ang, side, closed=True):
    sk, sh, hi = SKINS[S["skin"]]
    r = 24
    d = (f"M {fmt(x-r*0.9)} {fmt(y-r*0.4)} C {fmt(x-r)} {fmt(y+r*0.9)}, {fmt(x+r)} {fmt(y+r*0.9)}, {fmt(x+r*0.9)} {fmt(y-r*0.4)} "
         f"C {fmt(x+r*0.6)} {fmt(y-r)}, {fmt(x-r*0.6)} {fmt(y-r)}, {fmt(x-r*0.9)} {fmt(y-r*0.4)} Z")
    thumb = f'<ellipse cx="{fmt(x+side*-r*0.9)}" cy="{fmt(y-r*0.1)}" rx="{fmt(r*0.35)}" ry="{fmt(r*0.5)}" fill="{sk}" stroke="{OUT}" stroke-width="{c.sw(2)}"/>'
    return f'<g transform="rotate({fmt(ang)},{fmt(x)},{fmt(y)})">' + thumb + f'<path d="{d}" fill="{sk}" stroke="{OUT}" stroke-width="{c.sw(2.4)}"/>' + "</g>"

def garment(c, S, p, t):
    """torso + skirt of the garment, in neck-base coords (already body-scaled by the caller)"""
    g = S["garment"]; col = S["col"]; col2 = S["col2"]; b = S["build"]; k = S["kind"]
    shw = (150 if k == "woman" else 172) * b
    waist = (118 if k == "woman" else 150) * b
    hem_y = {"tunic": 640, "robe": 1130, "dress": 1210, "coat": 1080, "child": 700}.get(g, 640)
    hem_w = {"tunic": 170, "robe": 210, "dress": 230, "coat": 220, "child": 160}.get(g, 170) * b
    ph = p["phase"]; walking = p["legs"] == "walk"
    sway = (14 * math.sin(ph) if walking else 4 * math.sin(t * 1.7)) * (1 if g in ("robe", "dress", "coat") else 0.5)
    sit = p["legs"] == "sit"
    if sit:
        hem_y = 560; hem_w = 330 * b
    if p["legs"] == "none":
        hem_y = min(hem_y, 760); hem_w = min(hem_w, 200 * b)
    pts = [(-40, 2), (-shw * 0.55, 10), (-shw, 50), (-shw * 1.02, 160), (-waist, 400),
           (-hem_w + sway, hem_y), (-hem_w * 0.5 + sway, hem_y + 10), (hem_w * 0.5 + sway, hem_y + 10), (hem_w + sway, hem_y),
           (waist, 400), (shw * 1.02, 160), (shw, 50), (shw * 0.55, 10), (40, 2)]
    d = smooth_path(pts)
    out = rimmed(c, d, col, dx=3, dy=-1)
    cid = c.uid("gc")
    pat = ""
    if S["pattern"] == "brocade":
        for r in range(int(hem_y / 46)):
            for cc in range(-6, 7):
                x = cc * 38 + (19 if r % 2 else 0); y = 60 + r * 46
                pat += f'<path d="M {x} {y-9} L {x+7} {y} L {x} {y+9} L {x-7} {y} Z" fill="#d8a64a" opacity="0.5"/>'
    elif S["pattern"] == "scales":          # lamellar armour
        sc = S.get("scale_col", "#000000")
        for r in range(int(hem_y / 36)):
            for cc in range(-7, 8):
                x = cc * 36 + (18 if r % 2 else 0); y = 40 + r * 36
                pat += f'<path d="M {x-18} {y} C {x-18} {y+24}, {x+18} {y+24}, {x+18} {y}" stroke="{sc}" stroke-width="{c.sw(2.4)}" fill="none" opacity="0.5"/>'
    elif S["pattern"] == "stripes":
        for cc in range(-8, 9):
            pat += f'<path d="M {cc*34} 0 L {cc*34 + 20} {hem_y+20}" stroke="{col2}" stroke-width="{c.sw(6)}" opacity="0.5"/>'
    shade = smooth_path([(-shw, 50), (-shw * 1.02, 160), (-waist, 400), (-hem_w + sway, hem_y), (-hem_w * 0.55 + sway, hem_y + 8), (-waist * 0.55, 400), (-shw * 0.6, 120)])
    folds = ""
    if g in ("robe", "dress", "coat") and not sit:
        for fx in (-0.5, 0.0, 0.45):
            folds += f'<path d="M {fmt(fx*waist)} 420 C {fmt(fx*waist+sway*0.3)} 700, {fmt(fx*hem_w*0.9+sway*0.6)} 900, {fmt(fx*hem_w+sway)} {fmt(hem_y)}" stroke="{col2}" stroke-width="{c.sw(5)}" fill="none" opacity="0.55"/>'
    out += f'<clipPath id="{cid}"><path d="{d}"/></clipPath><g clip-path="url(#{cid})">{pat}<path d="{shade}" fill="{col2}" opacity="0.55"/>{folds}</g>'
    # collar / front opening
    if g in ("robe", "coat"):
        out += f'<path d="M -40 4 L 30 400 L {fmt(30+sway*0.6)} {fmt(hem_y)}" stroke="{col2}" stroke-width="{c.sw(4)}" fill="none"/>'
    out += f'<path d="M -58 4 C -40 34, 40 34, 58 4" stroke="{S.get("trim","#d8a64a")}" stroke-width="{c.sw(10)}" fill="none" stroke-linecap="round"/>'
    if S["fur"]:
        fpts = bumpy([(-shw * 0.9, 30), (-60, -6), (0, 10), (60, -6), (shw * 0.9, 30), (shw * 0.6, 70), (0, 60), (-shw * 0.6, 70)], 8)
        out += rimmed(c, smooth_path(fpts), S["fur"], dx=2, dy=-2)
        out += f'<path d="M -50 60 L -30 {hem_y} M 50 60 L 30 {hem_y}" stroke="{S["fur"]}" stroke-width="{c.sw(22)}" opacity="0.95"/>' if g == "coat" else ""
    belt_y = 380
    if S["belt"] and not sit:
        out += f'<path d="M {fmt(-waist*1.02)} {belt_y} L {fmt(waist*1.02)} {belt_y} L {fmt(waist*1.02)} {belt_y+30} L {fmt(-waist*1.02)} {belt_y+30} Z" fill="{S["belt"]}" stroke="{OUT}" stroke-width="{c.sw(2)}"/>'
        if S.get("buckle", True):
            out += f'<rect x="-18" y="{belt_y-4}" width="36" height="38" rx="6" fill="#b9832f" stroke="{OUT}" stroke-width="{c.sw(2.2)}"/>'
    if S["sash"]:
        out += f'<path d="M {fmt(-waist)} {belt_y-6} L {fmt(waist)} {belt_y-6} L {fmt(waist)} {belt_y+34} L {fmt(-waist)} {belt_y+34} Z" fill="{S["sash"]}" stroke="{OUT}" stroke-width="{c.sw(2)}"/>'
        out += f'<path d="M 30 {belt_y+30} l 10 90 l 26 -6 l -10 -84 Z" fill="{S["sash"]}" stroke="{OUT}" stroke-width="{c.sw(2)}"/>'
    if S.get("strap"):
        out += (f'<path d="M 120 40 L 150 70 L -110 330 L -150 300 Z" fill="#3a2414" stroke="{OUT}" stroke-width="{c.sw(2)}"/>'
                f'<circle cx="18" cy="190" r="17" fill="#b9832f" stroke="{OUT}" stroke-width="{c.sw(2.4)}"/>')
    return out, hem_y, hem_w, sway

def legs(c, S, p, t, hem_y, hem_w, sway):
    st = p["legs"]
    if st in ("sit", "none"):
        if st == "sit":
            # crossed legs / knees as a wide base with boots peeking
            return (f'<ellipse cx="-200" cy="575" rx="46" ry="22" fill="{S["boots"]}" stroke="{OUT}" stroke-width="{c.sw(2.4)}"/>'
                    f'<ellipse cx="200" cy="575" rx="46" ry="22" fill="{S["boots"]}" stroke="{OUT}" stroke-width="{c.sw(2.4)}"/>')
        return ""
    ph = p["phase"]
    out = ""
    for side in (-1, 1):
        lift = max(0, math.sin(ph + (0 if side < 0 else math.pi))) * 26 if st == "walk" else 0
        fx = side * 58 + (18 * math.cos(ph + (0 if side < 0 else math.pi)) if st == "walk" else 0)
        top = hem_y - 40
        out += (f'<path d="M {fmt(fx-30)} {fmt(top)} L {fmt(fx+30)} {fmt(top)} L {fmt(fx+28)} {fmt(FEET-60-lift)} L {fmt(fx-28)} {fmt(FEET-60-lift)} Z" fill="{S["trousers"]}" stroke="{OUT}" stroke-width="{c.sw(2.4)}"/>'
                f'<path d="M {fmt(fx-32)} {fmt(FEET-80-lift)} L {fmt(fx+30)} {fmt(FEET-80-lift)} C {fmt(fx+36)} {fmt(FEET-30-lift)}, {fmt(fx+side*70)} {fmt(FEET-18-lift)}, {fmt(fx+side*66)} {fmt(FEET-lift)} '
                f'L {fmt(fx-side*34)} {fmt(FEET-lift)} Z" fill="{S["boots"]}" stroke="{OUT}" stroke-width="{c.sw(2.4)}"/>')
    return out

# ---------------------------------------------------------------- props
def prop(c, name, x, y, ang, t, S=None):
    g = f'<g transform="translate({fmt(x)},{fmt(y)}) rotate({fmt(ang)})">'
    if name == "lantern":
        fl = 0.85 + 0.15 * math.sin(t * 13) * math.sin(t * 7)
        return (g + f'<path d="M 0 -20 L 0 20" stroke="{OUT}" stroke-width="{c.sw(4)}"/>'
                f'<rect x="-30" y="20" width="60" height="80" rx="8" fill="#ffcf6a" stroke="{OUT}" stroke-width="{c.sw(3)}"/>'
                f'<rect x="-30" y="20" width="60" height="80" rx="8" fill="#fff2b0" opacity="{0.5*fl:.2f}"/>'
                f'<path d="M -36 20 L 36 20 L 24 4 L -24 4 Z M -34 100 L 34 100 L 30 112 L -30 112 Z" fill="#3a2a1a" stroke="{OUT}" stroke-width="{c.sw(2.4)}"/>'
                f'<path d="M -10 20 L -10 100 M 10 20 L 10 100" stroke="#3a2a1a" stroke-width="{c.sw(3)}"/>'
                f'<ellipse cx="0" cy="62" rx="8" ry="{fmt(14*fl)}" fill="#fff8e0"/></g>')
    if name == "bread":
        return (g + f'<ellipse cx="0" cy="0" rx="70" ry="30" fill="#d39a52" stroke="{OUT}" stroke-width="{c.sw(2.6)}"/>'
                f'<path d="M -40 -6 C -20 -16, 20 -16, 40 -6" stroke="#9a6a30" stroke-width="{c.sw(3)}" fill="none"/>'
                f'<ellipse cx="10" cy="-10" rx="30" ry="8" fill="#f2c27a" opacity="0.7"/></g>')
    if name == "baby":
        sk = SKINS["light"]
        return (g + f'<path d="M -90 -30 C -96 -60, -60 -76, -20 -70 C 40 -70, 96 -40, 92 0 C 88 34, 40 46, -20 40 C -70 36, -86 10, -90 -30 Z" fill="#efe2c8" stroke="{OUT}" stroke-width="{c.sw(2.6)}"/>'
                f'<path d="M -40 -60 C 0 -40, 40 -10, 80 0" stroke="#c9b48e" stroke-width="{c.sw(4)}" fill="none"/>'
                f'<circle cx="-56" cy="-40" r="34" fill="{sk[0]}" stroke="{OUT}" stroke-width="{c.sw(2.4)}"/>'
                f'<path d="M -66 -42 q 5 4 10 0 M -50 -44 q 5 4 10 0" stroke="{OUT}" stroke-width="{c.sw(2)}" fill="none"/>'
                f'<ellipse cx="-50" cy="-28" rx="6" ry="3" fill="#c76a5a"/></g>')
    if name == "stick":
        return g + f'<path d="M 0 -260 L 0 220" stroke="#5a3a1c" stroke-width="{c.sw(12)}" stroke-linecap="round"/><path d="M 0 -260 L 0 220" stroke="{OUT}" stroke-width="{c.sw(2)}" fill="none"/></g>'
    if name == "brush":
        return (g + f'<rect x="-34" y="-14" width="68" height="28" rx="10" fill="#7a5130" stroke="{OUT}" stroke-width="{c.sw(2.4)}"/>'
                f'<path d="M -30 14 L 30 14 L 30 30 L -30 30 Z" fill="#c9b07a" stroke="{OUT}" stroke-width="{c.sw(2)}"/></g>')
    if name == "sack":
        return (g + f'<path d="M -70 -90 C -110 -40, -100 70, -40 90 C 20 104, 90 80, 96 10 C 100 -50, 60 -96, 20 -100 C -10 -104, -40 -110, -70 -90 Z" fill="#b89664" stroke="{OUT}" stroke-width="{c.sw(2.6)}"/>'
                f'<path d="M -40 -96 l -10 -30 l 30 6 Z" fill="#b89664" stroke="{OUT}" stroke-width="{c.sw(2)}"/></g>')
    if name == "purse":
        return (g + f'<path d="M -26 -10 C -40 20, -30 50, 0 52 C 30 50, 40 20, 26 -10 Z" fill="#7a4e26" stroke="#e8c070" stroke-width="{c.sw(3)}"/>'
                f'<path d="M -20 -10 L 20 -10 L 14 -22 L -14 -22 Z" fill="#5a3818" stroke="{OUT}" stroke-width="{c.sw(2)}"/><circle cx="-8" cy="14" r="6" fill="#f0d08a" opacity="0.8"/></g>')
    if name == "sword":
        return (g + f'<rect x="-6" y="-40" width="12" height="60" fill="#3a2414" stroke="{OUT}" stroke-width="{c.sw(2)}"/>'
                f'<rect x="-30" y="16" width="60" height="12" rx="4" fill="#b9832f" stroke="{OUT}" stroke-width="{c.sw(2)}"/>'
                f'<path d="M -8 28 L 8 28 L 6 360 L 0 380 L -6 360 Z" fill="#d9dde2" stroke="{OUT}" stroke-width="{c.sw(2.4)}"/></g>')
    if name == "spear":
        return (g + f'<path d="M 0 -520 L 0 380" stroke="#4a3018" stroke-width="{c.sw(10)}"/>'
                f'<path d="M 0 -600 L 16 -520 L -16 -520 Z" fill="#cfd4da" stroke="{OUT}" stroke-width="{c.sw(2.4)}"/></g>')
    if name == "scroll":
        return (g + f'<rect x="-15" y="-74" width="30" height="148" rx="10" fill="#eadbb4" stroke="{OUT}" stroke-width="{c.sw(2.4)}"/>'
                f'<path d="M -8 -50 L 8 -50 M -8 -26 L 8 -26 M -8 -2 L 6 -2 M -8 22 L 8 22" stroke="#8a6a3a" stroke-width="{c.sw(2)}"/>'
                f'<rect x="-20" y="-86" width="40" height="17" rx="6" fill="#8a5a2a" stroke="{OUT}" stroke-width="{c.sw(2)}"/>'
                f'<rect x="-20" y="69" width="40" height="17" rx="6" fill="#8a5a2a" stroke="{OUT}" stroke-width="{c.sw(2)}"/></g>')
    if name in ("spear_red", "banner_black", "banner_red"):
        tall = name != "spear_red"
        out = g + f'<path d="M 0 {-1190 if tall else -560} L 0 {320 if tall else 380}" stroke="#4a3018" stroke-width="{c.sw(10)}"/>'
        if name == "spear_red":
            out += f'<path d="M 0 -640 L 16 -560 L -16 -560 Z" fill="#cfd4da" stroke="{OUT}" stroke-width="{c.sw(2.4)}"/>'
            n = 7; top, bot = [], []
            for i in range(n + 1):
                u = i / n; wv = 16 * u * math.sin(t * 7 - u * 5)
                top.append((-6 - 120 * u, -548 + wv)); bot.append((-6 - 112 * u, -520 + wv * 1.1 + 6 * u))
            out += f'<path d="M {P(top + bot[::-1])} Z" fill="#c4161c" stroke="{OUT}" stroke-width="{c.sw(2)}"/>'
        else:
            col = "#121216" if name == "banner_black" else "#b5161b"
            out += f'<circle cx="0" cy="-1200" r="14" fill="#c9a24a" stroke="{OUT}" stroke-width="{c.sw(2)}"/>'
            n = 10; top, bot = [], []
            for i in range(n + 1):
                u = i / n; wv = (6 + 24 * u) * math.sin(t * 5.5 - u * 6)
                top.append((-6 - 340 * u, -1180 + wv)); bot.append((-6 - 326 * u, -950 + wv * 1.1 + 14 * u))
            out += f'<path d="M {P(top + bot[::-1])} Z" fill="{col}" stroke="{OUT}" stroke-width="{c.sw(2.4)}"/>'
        return out + '</g>'
    if name == "pike":   # long spear held low (hand hanging at the side)
        return (g + f'<path d="M 0 -1080 L 0 320" stroke="#4a3018" stroke-width="{c.sw(10)}"/>'
                f'<path d="M 0 -1170 L 17 -1080 L -17 -1080 Z" fill="#cfd4da" stroke="{OUT}" stroke-width="{c.sw(2.4)}"/></g>')
    if name == "bowl":
        return g + f'<path d="M -50 -10 L 50 -10 C 46 30, -46 30, -50 -10 Z" fill="#8a5a32" stroke="{OUT}" stroke-width="{c.sw(2.4)}"/></g>'
    if name == "dagger":     # short curved knife, blade pointing down (+y) from the fist
        return (g + f'<rect x="-7" y="-34" width="14" height="44" rx="4" fill="#3a2414" stroke="{OUT}" stroke-width="{c.sw(2)}"/>'
                f'<rect x="-22" y="8" width="44" height="10" rx="4" fill="#c9a24a" stroke="{OUT}" stroke-width="{c.sw(2)}"/>'
                f'<path d="M -7 18 L 7 18 C 12 70, 10 110, -4 150 C -4 110, -10 70, -7 18 Z" fill="#dfe3e8" stroke="{OUT}" stroke-width="{c.sw(2.2)}"/></g>')
    if name == "torch":      # a burning torch held upright (flame above the fist)
        fl = [(0, -150 - 70 * (0.8 + 0.2 * math.sin(t * 17)) - 20 * math.sin(t * 11)), (34, -150), (20, -120), (-20, -120), (-34, -150)]
        return (g + f'<path d="M -9 -120 L 9 -120 L 7 170 L -7 170 Z" fill="#5a3a1c" stroke="{OUT}" stroke-width="{c.sw(2.2)}"/>'
                f'<path d="M -16 -140 L 16 -140 L 13 -110 L -13 -110 Z" fill="#3a2a1a" stroke="{OUT}" stroke-width="{c.sw(2)}"/>'
                f'<path d="M -30 -136 C -40 -170, {fmt(-14 + 8 * math.sin(t * 13))} {fmt(fl[0][1] + 40)}, {fmt(4 * math.sin(t * 9))} {fmt(fl[0][1])} '
                f'C {fmt(14 + 8 * math.sin(t * 15))} {fmt(fl[0][1] + 40)}, 40 -170, 30 -136 Z" fill="#ff8a1a"/>'
                f'<path d="M -16 -136 C -20 -160, -6 -190, {fmt(2 * math.sin(t * 9))} {fmt(fl[0][1] + 34)} C 6 -190, 20 -160, 16 -136 Z" fill="#ffd84a"/></g>')
    if name == "shovel":     # held with the blade down; the hand grips the shaft
        return (g + f'<path d="M 0 -230 L 0 250" stroke="#6a4424" stroke-width="{c.sw(12)}"/><path d="M -30 -236 L 30 -236" stroke="#6a4424" stroke-width="{c.sw(12)}" stroke-linecap="round"/>'
                f'<path d="M -46 250 L 46 250 L 40 360 C 20 400, -20 400, -40 360 Z" fill="#8e949e" stroke="{OUT}" stroke-width="{c.sw(2.4)}"/></g>')
    if name == "pick":       # pickaxe: the handle runs from the fist (+y) to the iron head
        return (g + f'<path d="M 0 -40 L 0 300" stroke="#6a4424" stroke-width="{c.sw(12)}"/>'
                f'<path d="M -130 330 C -60 290, 60 290, 130 330 L 120 300 C 60 266, -60 266, -120 300 Z" fill="#8e949e" stroke="{OUT}" stroke-width="{c.sw(2.4)}"/></g>')
    if name == "falcon":     # a falcon perched on a leather-gloved fist, facing right (+x)
        return (g + f'<path d="M -46 -20 C -50 30, -40 60, -30 90 L 34 90 C 44 60, 50 30, 44 -20 Z" fill="#8a5a2a" stroke="{OUT}" stroke-width="{c.sw(2.4)}"/>'
                f'<path d="M -40 70 L 40 70" stroke="#5a3a1a" stroke-width="{c.sw(5)}"/>'
                f'<path d="M -18 -62 C -40 0, -64 70, -78 140 L -46 146 C -30 80, -6 20, 10 -40 Z" fill="#5a4a3e" stroke="{OUT}" stroke-width="{c.sw(2.2)}"/>'
                f'<ellipse cx="0" cy="-118" rx="50" ry="88" fill="#6a5a4c" stroke="{OUT}" stroke-width="{c.sw(2.6)}"/>'
                f'<path d="M 14 -180 C 46 -150, 50 -80, 30 -40 C 14 -24, -2 -40, 2 -80 Z" fill="#efe4cc" stroke="{OUT}" stroke-width="{c.sw(2)}"/>'
                f'<path d="M 18 -150 l 16 4 M 16 -126 l 20 4 M 14 -102 l 18 4 M 14 -78 l 14 3" stroke="#8a7a62" stroke-width="{c.sw(3)}"/>'
                f'<path d="M -44 -150 C -64 -100, -56 -40, -30 -10 C -10 -30, -6 -110, -20 -170 Z" fill="#4a3e34" stroke="{OUT}" stroke-width="{c.sw(2.2)}"/>'
                f'<circle cx="8" cy="-214" r="40" fill="#5a4a3e" stroke="{OUT}" stroke-width="{c.sw(2.6)}"/>'
                f'<path d="M 18 -236 C 40 -226, 46 -196, 30 -180 C 20 -190, 12 -204, 14 -222 Z" fill="#efe4cc"/>'
                f'<path d="M 22 -214 C 26 -200, 26 -188, 20 -180" stroke="#2a221c" stroke-width="{c.sw(6)}" fill="none" stroke-linecap="round"/>'
                f'<path d="M 42 -222 C 62 -222, 70 -210, 62 -196 L 46 -206 Z" fill="#e0b040" stroke="{OUT}" stroke-width="{c.sw(2)}"/>'
                f'<circle cx="26" cy="-222" r="8" fill="#120a06"/><circle cx="28" cy="-224" r="2.6" fill="#fff"/>'
                f'<path d="M -12 -30 l -6 22 M 8 -30 l 4 22" stroke="#e0b040" stroke-width="{c.sw(5)}" stroke-linecap="round"/></g>')
    if name == "drumstick":
        return g + f'<path d="M 0 -20 L 0 170" stroke="#6a4424" stroke-width="{c.sw(9)}" stroke-linecap="round"/><circle cx="0" cy="176" r="15" fill="#d8c8a8" stroke="{OUT}" stroke-width="{c.sw(2)}"/></g>'
    return ""

def tanbur(c, x, y, ang, t):
    return (f'<g transform="translate({fmt(x)},{fmt(y)}) rotate({fmt(ang)})">'
            f'<path d="M 0 0 C -40 -6, -70 -40, -60 -76 C -50 -110, 20 -110, 40 -80 C 56 -56, 40 -10, 0 0 Z" fill="#a4652e" stroke="{OUT}" stroke-width="{c.sw(2.6)}"/>'
            f'<ellipse cx="-12" cy="-58" rx="18" ry="16" fill="#3a2010"/>'
            f'<rect x="-6" y="-560" width="16" height="500" fill="#7a4a20" stroke="{OUT}" stroke-width="{c.sw(2.4)}"/>'
            f'<path d="M -4 -560 L -14 -600 L 18 -600 L 12 -560 Z" fill="#5a3418" stroke="{OUT}" stroke-width="{c.sw(2)}"/>'
            + "".join(f'<path d="M -2 {-520+i*60} L 12 {-520+i*60}" stroke="#e8d3a0" stroke-width="{c.sw(2)}"/>' for i in range(7)) +
            '</g>')

# ---------------------------------------------------------------- person
def cloak_back(c, S, p, t):
    if not S["cloak"]:
        return ""
    wind = p["wind"]
    pts = [(-150, 30), (-210, 40), (-270 - 30 * wind, 100), (-320 - 40 * wind, 220), (-346 - 46 * wind, 400),
           (-350 - 44 * wind, 620), (-330 - 36 * wind, 860), (-240, 920), (-170, 900)]
    pts = [(x + (6 + 10 * wind) * math.sin(t * 3.4 + i * 0.8) * (i / 8), y + 4 * math.sin(t * 2.7 + i) * (i / 8)) for i, (x, y) in enumerate(pts)]
    d = smooth_path(pts + [(-150, 400)])
    return rimmed(c, d, S.get("cloak2", "#6c0f12"), dx=2, dy=-2)

def cloak_front(c, S, p, t):
    if not S["cloak"]:
        return ""
    col = S["cloak"]
    Lp = (f"M -40 0 C -96 4, -160 18, -186 60 C -200 160, -204 500, -200 {fmt(880+4*math.sin(t*2.8))} "
          f"L -140 {fmt(892+5*math.sin(t*3.1+1))} C -136 500, -134 150, -116 70 C -96 40, -66 20, -40 12 Z")
    Rp = (f"M 40 0 C 96 4, 160 18, 186 60 C 198 160, 202 500, 198 {fmt(876+4*math.sin(t*2.6+2))} "
          f"L 144 {fmt(886+5*math.sin(t*3.0))} C 140 500, 138 150, 120 70 C 100 40, 70 20, 40 12 Z")
    br = "".join(f'<circle cx="{x}" cy="40" r="20" fill="#b9832f" stroke="{OUT}" stroke-width="{c.sw(2.6)}"/><circle cx="{x}" cy="40" r="11" fill="#7a1010"/>'
                 for x in (-112, 112))
    return (rimmed(c, Lp, col, dx=2, dy=-2) + f'<path d="M -186 60 C -200 160, -204 500, -200 880 L -170 886 C -176 500, -172 140, -150 70 Z" fill="{S.get("cloak2", "#6c0f12")}" opacity="0.7"/>' +
            rimmed(c, Rp, col, dx=3.5, dy=-1.5) + f'<path d="M 150 40 C 176 70, 186 200, 188 800 L 176 800 C 174 200, 166 80, 140 48 Z" fill="{S.get("cloak_hi", "#d8402e")}" opacity="0.6"/>' + br +
            f'<path d="M -112 40 C -60 70, 60 70, 112 40" stroke="#d8a64a" stroke-width="{c.sw(4)}" fill="none"/>')

ARM_PRESETS = {  # (upper-arm angle from straight down, + = outward/up ; inward bend of the forearm)
    "down": (6, 4), "relaxed": (10, 18), "hip": (35, 100), "raise": (160, -10), "fist_up": (165, -15), "forward": (40, 90),
    "offer": (48, 18), "hold_lantern": (30, 62), "hold_bread": (28, 112), "hold_baby": (22, 122), "chest": (16, 136),
    "wave": (120, -30), "point": (82, 0), "brush": (62, 28), "reach": (62, 8), "strum": (26, 108), "neck": (72, -38),
    "carry": (165, 95), "touch": (46, 72), "both_out": (40, -10), "bless": (70, 60),
}

def ik_angles(sh, target, l1, l2, side, elbow_down=False):
    sx, sy = sh; tx, ty = target
    dx, dy = tx - sx, ty - sy
    d = max(abs(l1 - l2) + 1, min(math.hypot(dx, dy), (l1 + l2) * 0.995))
    base = math.atan2(side * dx, dy)
    A = math.acos(max(-1, min(1, (l1 * l1 + d * d - l2 * l2) / (2 * l1 * d))))
    a1 = base - A if elbow_down else base + A
    ex, ey = sx + side * math.sin(a1) * l1, sy + math.cos(a1) * l1
    fa = math.atan2(side * (tx - ex), (ty - ey))
    return math.degrees(a1), math.degrees(a1 - fa)

def arm(c, S, p, t, side, preset, bs):
    shw = (150 if S["kind"] == "woman" else 172) * S["build"]
    sh = (side * shw * 0.92, 60)
    if isinstance(preset, tuple) and preset and preset[0] == "ik":      # ("ik", x, y) or ("ik", x, y, "down"): the other elbow solution
        a1, a2 = ik_angles(sh, (preset[1], preset[2]), 300, 270, side, len(preset) > 3 and preset[3] == "down")
    else:
        a1, a2 = ARM_PRESETS.get(preset, preset) if isinstance(preset, str) else preset
    e, h = arm_pts(sh, a1, a2, 300, 270, side)
    sleeve = S["col"] if S["garment"] != "dress" else S["col"]
    out = limb(c, sh, e, 46 * S["build"], 40 * S["build"], sleeve) + limb(c, e, h, 40 * S["build"], 32, sleeve)
    cuff = f'<circle cx="{fmt(h[0])}" cy="{fmt(h[1])}" r="34" fill="{S.get("cuff","#d8a64a")}" stroke="{OUT}" stroke-width="{c.sw(2)}"/>'
    fa = a1 - a2
    hx, hy = h[0] + side * math.sin(math.radians(fa)) * 26, h[1] + math.cos(math.radians(fa)) * 26
    out += cuff + hand(c, S, hx, hy, side * fa * 0.5, side)
    return out, (hx, hy), fa

def person(S, p, t, lw=1.0):
    """returns SVG with the feet at (0,0)"""
    c = Ctx(lw)
    bs = S["bs"]; hs = S["hs"]
    tilt, nod = p["tilt"], p["nod"]
    bob = (-10 * abs(math.cos(p["phase"])) if p["legs"] == "walk" else 0) + 3 * p["breathe"]
    hdrop = 34 if S["kind"] == "boy" else (14 if S["kind"] == "woman" else 0)
    htr = f"translate(0,{fmt(nod + bob * 0.4 + hdrop)}) rotate({fmt(tilt)},0,-60) scale({hs:.3f})"
    gar, hem_y, hem_w, sway = garment(c, S, p, t)
    body = f'<g transform="scale({bs:.3f})">'
    body += cloak_back(c, S, p, t)
    body += legs(c, S, p, t, hem_y, hem_w, sway)
    # arms behind the body if they hang down? draw after the garment so they read
    body += gar
    body += f'<path d="M -42 -70 L -40 6 C -20 16, 20 16, 40 6 L 42 -70 Z" fill="{SKINS[S["skin"]][1]}"/>'
    body += "</g>"
    arms = ""; hands = {}
    for side, key, pkey in ((-1, "armR", "propR"), (1, "armL", "propL")):
        a, hpos, ang = arm(c, S, p, t, side, p[key], bs)
        hands[side] = hpos
        pr = p[pkey]; pang = 0
        if isinstance(pr, tuple):
            pr, pang = pr
        prop_svg = ""
        if pr:
            if pr == "tanbur":
                prop_svg = f'<g transform="translate(-60,430) scale(1.45) translate(60,-430)">' + tanbur(c, -60, 430, 34, t) + '</g>'
            else:
                prop_svg = prop(c, pr, hpos[0] + (side * 60 if pr == "baby" else 0), hpos[1] + (40 if pr == "lantern" else (-10 if pr == "baby" else 0)), pang, t)
        arms += f'<g transform="scale({bs:.3f})">' + (prop_svg + a if pr in ("lantern",) else a + prop_svg) + '</g>'
    sk = SKINS[S["skin"]]
    neck = (f'<path d="M -44 -110 L -46 30 C -20 40, 20 40, 46 30 L 44 -110 Z" fill="{sk[0]}" stroke="{OUT}" stroke-width="{c.sw(2.4)}"/>'
            f'<path d="M -44 -110 L -46 30 C -30 36, -10 38, 0 38 L 0 -60 C -20 -64, -36 -80, -44 -110 Z" fill="{sk[1]}" opacity="0.6"/>')
    headg = (f'<g transform="translate(0,{fmt(bob)})">' +
             f'<g transform="{htr}">' + hair_back(c, S, p, t) + scarf_back(c, S, p, t) + neck + '</g>' +
             '</g>')
    front = f'<g transform="translate(0,{fmt(bob)})"><g transform="{htr}">' + head(c, S, p, t) + '</g></g>'
    cf = f'<g transform="scale({bs:.3f})">' + cloak_front(c, S, p, t) + '</g>'
    chains = ""
    if p["chains"] == "rope" and len(hands) == 2:
        (x1, y1), (x2, y2) = hands[-1], hands[1]
        x1 *= bs; y1 *= bs; x2 *= bs; y2 *= bs
        my = max(y1, y2) + 30
        chains = (f'<path d="M {fmt(x1)} {fmt(y1)} C {fmt(x1)} {fmt(my)}, {fmt(x2)} {fmt(my)}, {fmt(x2)} {fmt(y2)}" stroke="#8a6a3a" stroke-width="{c.sw(11)}" fill="none"/>'
                  + "".join(f'<ellipse cx="{fmt(x)}" cy="{fmt(y + dy)}" rx="{fmt(30*bs)}" ry="{fmt(9*bs)}" fill="none" stroke="#7a5a2e" stroke-width="{c.sw(8)}"/>'
                            for x, y in ((x1, y1), (x2, y2)) for dy in (-10 * bs, 6 * bs)))
        if p.get("lead"):
            lx, ly = p["lead"]; mx = (x1 + x2) / 2; my2 = max(y1, y2) + 18
            chains += f'<path d="M {fmt(mx)} {fmt(my2)} Q {fmt((mx + lx) / 2)} {fmt(max(my2, ly) + 60)}, {fmt(lx)} {fmt(ly)}" stroke="#8a6a3a" stroke-width="{c.sw(9)}" fill="none"/>'
    elif p["chains"] and len(hands) == 2:
        (x1, y1), (x2, y2) = hands[-1], hands[1]
        x1 *= bs; y1 *= bs; x2 *= bs; y2 *= bs
        my = max(y1, y2) + 40
        chains = (f'<path d="M {fmt(x1)} {fmt(y1)} C {fmt(x1)} {fmt(my)}, {fmt(x2)} {fmt(my)}, {fmt(x2)} {fmt(y2)}" stroke="#9a9ea4" stroke-width="{c.sw(10)}" fill="none" stroke-dasharray="{c.sw(14)} {c.sw(6)}"/>'
                  f'<circle cx="{fmt(x1)}" cy="{fmt(y1)}" r="{fmt(30*bs)}" fill="none" stroke="#7a7e84" stroke-width="{c.sw(9)}"/>'
                  f'<circle cx="{fmt(x2)}" cy="{fmt(y2)}" r="{fmt(30*bs)}" fill="none" stroke="#7a7e84" stroke-width="{c.sw(9)}"/>')
    defs = ('<defs><filter id="glowf" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="6"/></filter></defs>')
    whole = defs + headg + body + front + cf + arms + chains
    return f'<g transform="translate(0,{fmt(-FEET*bs)})">{whole}</g>'

def lying_person(S, p, t, lw=1.0):
    """person rotated to lie on the back, head to the left; origin at the ground under the hips"""
    q = dict(p); q["legs"] = "stand"; q["armL"] = (6, 0); q["armR"] = (6, 0)
    inner = person(S, q, t, lw)
    F = FEET * S["bs"]
    return f'<g transform="translate(0,{fmt(-175*S["bs"])}) rotate(-90) translate(0,{fmt(F*0.55)})">{inner}</g>'

# ============================================================== animals
def horse(c, col="#6b4426", mane="#1d120c", phase=0.0, walk=False, t=0.0, head_bob=0.0, saddle=True, blanket=None, head_down=0.0, packs=None, mule=False):
    """side view facing right; origin on the ground under the belly; ~ 640 wide x 600 tall"""
    out = ""
    dark = "#3a2414"
    legs_def = [(-130, 0.0, True), (-100, math.pi, False), (150, math.pi * 0.5, True), (178, math.pi * 1.5, False)]
    leg_svg = ["", ""]
    for i, (lx, ph, hind) in enumerate(legs_def):
        far = i in (0, 2)
        s_ = math.sin(phase + ph) if walk else 0.0
        a = (24 * s_) if walk else 1.5 * math.sin(t * 1.3 + i)
        lift = max(0.0, -math.cos(phase + ph)) if walk else 0.0
        r = math.radians(a)
        top = (lx, -300)
        knee = (lx + math.sin(r) * 140 + (-10 if hind else 6), -300 + math.cos(r) * 140)
        bend = math.radians(a + (30 if hind else -30) * lift)
        foot = (knee[0] + math.sin(bend) * 130, min(-4, knee[1] + math.cos(bend) * 130))
        fill = dark if far else col
        seg = (limb(c, top, knee, 38 if hind else 32, 20, fill) + limb(c, knee, foot, 19, 15, fill) +
               f'<path d="M {fmt(foot[0]-17)} {fmt(foot[1]-6)} L {fmt(foot[0]+17)} {fmt(foot[1]-6)} L {fmt(foot[0]+21)} {fmt(foot[1]+4)} L {fmt(foot[0]-19)} {fmt(foot[1]+4)} Z" '
               f'fill="#1e1410" stroke="{OUT}" stroke-width="{c.sw(2)}"/>')
        leg_svg[0 if far else 1] += seg
    hb = head_bob + 5 * math.sin(t * 1.6) + 120 * head_down
    hx = -40 * head_down
    tail = smooth_path([(-196, -372), (-232 - 10 * math.sin(t * 2.6), -330), (-252 - 16 * math.sin(t * 2.6 + 0.8), -250), (-244 - 12 * math.sin(t * 2.6 + 1.6), -170),
                        (-226 - 6 * math.sin(t * 2.6 + 2.2), -150), (-216, -240), (-200, -330)])
    body = smooth_path([(-200, -360), (-170, -400), (-90, -404), (40, -392), (120, -404), (170, -392), (212, -350), (214, -300), (180, -262),
                        (60, -246), (-80, -250), (-170, -270), (-206, -310)])
    neck = smooth_path([(120, -400), (190 + hx * 0.3, -470 + hb * 0.4), (250 + hx, -548 + hb), (290 + hx, -566 + hb), (300 + hx, -520 + hb), (266 + hx * 0.6, -430 + hb * 0.6), (214, -330), (150, -340)])
    headp = smooth_path([(262 + hx, -562 + hb), (292 + hx, -584 + hb), (330 + hx, -556 + hb), (392 + hx, -498 + hb), (398 + hx, -474 + hb), (376 + hx, -462 + hb),
                         (336 + hx, -476 + hb), (300 + hx, -496 + hb), (276 + hx, -520 + hb)])
    out += rimmed(c, tail, mane, dx=2, dy=-2) + leg_svg[0]
    out += rimmed(c, body, col, dx=3, dy=-2) + rimmed(c, neck, col, dx=3, dy=-2) + rimmed(c, headp, col, dx=3, dy=-2)
    out += leg_svg[1]
    out += f'<path d="M -150 -262 C -40 -246, 80 -248, 180 -266" stroke="#000" stroke-width="{c.sw(18)}" opacity="0.14" fill="none"/>'
    mpts = [(124, -404), (170, -460 + hb * 0.3), (214 + hx * 0.6, -520 + hb * 0.8), (256 + hx, -566 + hb), (276 + hx, -594 + hb), (246 + hx, -540 + hb), (204 + hx * 0.5, -486 + hb * 0.6), (160, -420)]
    out += rimmed(c, smooth_path(bumpy(mpts, 8)), mane, dx=2, dy=-2)
    ear = "l 2 -66 l 20 62" if mule else "l 4 -34 l 16 30"
    out += (f'<path d="M {fmt(284+hx)} {fmt(-580+hb)} {ear} Z" fill="{col}" stroke="{OUT}" stroke-width="{c.sw(2)}"/>'
            f'<ellipse cx="{fmt(318+hx)}" cy="{fmt(-544+hb)}" rx="8" ry="7" fill="#120a06"/><circle cx="{fmt(320+hx)}" cy="{fmt(-547+hb)}" r="2.4" fill="#fff"/>'
            f'<ellipse cx="{fmt(384+hx)}" cy="{fmt(-488+hb)}" rx="5" ry="4" fill="#120a06"/>'
            f'<path d="M {fmt(372+hx)} {fmt(-468+hb)} q -14 4 -26 -2" stroke="{OUT}" stroke-width="{c.sw(2)}" fill="none"/>'
            f'<path d="M {fmt(300+hx)} {fmt(-560+hb)} L {fmt(380+hx)} {fmt(-490+hb)} M {fmt(300+hx)} {fmt(-500+hb)} L {fmt(340+hx)} {fmt(-500+hb)}" stroke="#2a1a10" stroke-width="{c.sw(4)}" opacity="0.8"/>')
    if saddle:
        out += (f'<path d="M -60 -404 C -50 -444, 70 -444, 90 -404 L 80 -360 L -50 -360 Z" fill="#5a3418" stroke="{OUT}" stroke-width="{c.sw(2.4)}"/>'
                f'<path d="M -40 -360 L 70 -360 L 76 -320 L -46 -320 Z" fill="#8a2a20" stroke="{OUT}" stroke-width="{c.sw(2)}"/>')
    if packs:
        out += (f'<path d="M -120 -416 C -142 -366, -132 -296, -70 -288 C -10 -282, 30 -300, 40 -350 C 46 -400, 10 -430, -50 -432 Z" fill="{packs}" stroke="{OUT}" stroke-width="{c.sw(2.4)}"/>'
                f'<path d="M -10 -436 C 6 -470, 70 -472, 92 -440 C 112 -400, 100 -334, 50 -326 C 0 -322, -24 -380, -10 -436 Z" fill="{packs}" stroke="{OUT}" stroke-width="{c.sw(2.4)}"/>'
                f'<path d="M -100 -380 C -60 -372, 0 -372, 90 -390" stroke="#5a3a1c" stroke-width="{c.sw(5)}" fill="none"/>'
                f'<path d="M -70 -420 C -60 -400, -40 -396, -20 -404 M 20 -450 C 30 -436, 50 -434, 70 -446" stroke="#000" stroke-width="{c.sw(3)}" fill="none" opacity="0.25"/>')
    if blanket:
        out += f'<path d="M -80 -400 L 100 -400 L 110 -300 L -90 -300 Z" fill="{blanket}" stroke="{OUT}" stroke-width="{c.sw(2.4)}"/>'
    return out

def kneel_drop(kneel):
    """how far (elephant units) a kneeling elephant's back comes down; riders and howdahs move with it"""
    return 300.0 * max(0.0, min(1.0, kneel))

def elephant(c, phase=0.0, t=0.0, blanket="#7a1a1a", kneel=0.0):
    """side view facing left; origin at the ground under the belly; ~ 900 wide, 760 tall.
    kneel 0..1: the body comes down by kneel_drop(kneel) on folded legs (knees on the ground, feet tucked back, trunk on the ground)"""
    col = "#7d7a80"; dark = "#5d5a62"
    out = ""
    k = max(0.0, min(1.0, kneel)); D = kneel_drop(k)
    for i, (lx, ph) in enumerate([(-260, math.pi), (220, 0.0), (-200, 0.0), (280, math.pi)]):
        a = 10 * math.sin(phase + ph) * (1 - k)
        far = i < 2
        r = math.radians(a)
        x1 = lx + math.sin(r) * 260
        fill = dark if far else col
        lift = max(0, 18 * math.sin(phase + ph)) * (1 - k)
        if k <= 0:
            out += (f'<path d="M {fmt(lx-58)} -420 L {fmt(lx+58)} -420 L {fmt(x1+52)} {fmt(-6 - lift)} L {fmt(x1-52)} {fmt(-6 - lift)} Z" '
                    f'fill="{fill}" stroke="{OUT}" stroke-width="{c.sw(3)}" stroke-linejoin="round"/>'
                    f'<path d="M {fmt(x1-46)} {fmt(-10 - lift)} l 20 -10 M {fmt(x1)} {fmt(-12 - lift)} l 0 -12" stroke="#d8d4cc" stroke-width="{c.sw(4)}"/>')
            continue
        hip = (lx, -420 + D)
        knee = (lerp((lx + x1) / 2, lx - 46 - 8 * (i % 2), k), lerp(-213 - lift / 2, -50, k))
        foot = (lerp(x1, lx + 150, k), lerp(-6 - lift, -38, k))
        out += limb(c, hip, knee, 58, 55, fill, 3) + limb(c, knee, foot, 55, 50, fill, 3)
        ang = math.degrees(math.atan2(foot[1] - knee[1], foot[0] - knee[0])) - 90
        out += (f'<g transform="rotate({fmt(ang)},{fmt(foot[0])},{fmt(foot[1])})"><path d="M {fmt(foot[0]-40)} {fmt(foot[1]+38)} l 20 -10 '
                f'M {fmt(foot[0]+6)} {fmt(foot[1]+36)} l 0 -12" stroke="#d8d4cc" stroke-width="{c.sw(4)}"/></g>')
    tr = 30 * math.sin(t * 1.4) * (1 - 0.8 * k)
    stand = [(-520, -400 + tr * 0.2), (-540, -260 + tr * 0.6), (-520, -150 + tr), (-500, -170 + tr), (-470, -300 + tr * 0.5)]
    down = [(-525, -405), (-592, -342), (-668, -324 + tr * 0.2), (-660, -302 + tr * 0.2), (-560, -320)]   # minus D: the trunk lies on the ground, curled forward
    trunk = [(lerp(a[0], b[0], k), lerp(a[1], b[1], k)) for a, b in zip(stand, down)]
    body = smooth_path([(380, -620), (300, -760), (60, -800), (-220, -780), (-400, -700), (-470, -620), (-500, -520)] + trunk +
                       [(-450, -420), (-400, -470), (-300, -420), (300, -400), (400, -480)])
    up = f'<g transform="translate(0,{fmt(D)})">' if D else "<g>"
    out += up + rimmed(c, body, col, dx=4, dy=-3)
    ear = 12 * math.sin(t * 2.2)
    out += rimmed(c, smooth_path([(-300, -700), (-200 - ear, -720), (-150 - ear, -600), (-200 - ear * 0.5, -470), (-300, -520)]), "#8c8890", dx=3, dy=-2)
    out += (f'<circle cx="-410" cy="-610" r="9" fill="#120a06"/><circle cx="-412" cy="-613" r="3" fill="#fff"/>'
            f'<path d="M -470 -500 C -500 -470, -500 -440, -470 -420" stroke="#f2ede4" stroke-width="{c.sw(16)}" fill="none" stroke-linecap="round"/>')
    out += (f'<path d="M -140 -790 L 260 -790 L 290 -560 L -170 -560 Z" fill="{blanket}" stroke="{OUT}" stroke-width="{c.sw(3)}"/>'
            f'<path d="M -170 -580 L 290 -580" stroke="#e0b25a" stroke-width="{c.sw(14)}"/>'
            + "".join(f'<circle cx="{x}" cy="-560" r="10" fill="#e0b25a" stroke="{OUT}" stroke-width="{c.sw(2)}"/>' for x in range(-160, 290, 40)))
    return out + "</g>"

CAMEL_SADDLE_Y = -800        # a rider's seat on the camel's hump (camel units), see camel_rider in babak/p08_scenes.py

def camel(c, col="#c49a64", dark="#9a7448", phase=0.0, walk=False, t=0.0, blanket="#121216", trim="#c9a24a", saddle=True):
    """a dromedary, side view facing right; origin on the ground under the belly; ~ 800 wide x 860 tall.
    walk: a pacing gait (the two legs of one side move together); the head bobs with the step. The saddle sits on the hump (CAMEL_SADDLE_Y)."""
    out = ""
    legs_svg = ["", ""]
    for i, (lx, ph, hind) in enumerate([(-150, 0.0, True), (150, 0.0, False), (-118, math.pi, True), (182, math.pi, False)]):
        far = i < 2
        fill = dark if far else col
        s_ = math.sin(phase + ph) if walk else 0.0
        a = 18 * s_ if walk else 1.2 * math.sin(t * 1.1 + i)
        lift = max(0.0, -math.cos(phase + ph)) if walk else 0.0
        r = math.radians(a)
        top = (lx, -470)
        knee = (lx + math.sin(r) * 230, -470 + math.cos(r) * 230)
        bend = math.radians(a + (24 if hind else -24) * lift)
        foot = (knee[0] + math.sin(bend) * 220, min(-6, knee[1] + math.cos(bend) * 220))
        seg = (limb(c, top, knee, 40 if hind else 34, 22, fill) + f'<circle cx="{fmt(knee[0])}" cy="{fmt(knee[1])}" r="26" fill="{fill}" stroke="{OUT}" stroke-width="{c.sw(2.2)}"/>' +
               limb(c, knee, foot, 20, 17, fill) +
               f'<ellipse cx="{fmt(foot[0] + 8)}" cy="{fmt(foot[1] - 4)}" rx="34" ry="13" fill="{fill}" stroke="{OUT}" stroke-width="{c.sw(2.2)}"/>')
        legs_svg[0 if far else 1] += seg
    bob = (10 * math.sin(phase * 2) if walk else 0.0) + 6 * math.sin(t * 1.3)
    tail = smooth_path([(-236, -560), (-262 - 6 * math.sin(t * 2.2), -500), (-266 - 8 * math.sin(t * 2.2 + 0.7), -420), (-250, -400), (-246, -500)])
    body = smooth_path([(-240, -540), (-220, -610), (-150, -660), (-70, -760), (10, -800), (90, -770), (150, -690), (220, -640), (270, -600),
                        (276, -520), (230, -462), (120, -440), (-20, -440), (-150, -452), (-226, -480)])
    neck = smooth_path([(230, -650), (300, -610), (360, -570 + bob * 0.3), (410, -600 + bob * 0.6), (440, -680 + bob), (468, -700 + bob), (480, -640 + bob),
                        (466, -580 + bob * 0.6), (420, -520 + bob * 0.4), (340, -470), (260, -470)])
    headp = smooth_path([(430, -690 + bob), (446, -740 + bob), (490, -752 + bob), (540, -726 + bob), (578, -690 + bob), (576, -664 + bob), (540, -656 + bob),
                         (490, -662 + bob), (452, -664 + bob)])
    out += legs_svg[0] + rimmed(c, tail, dark, dx=2, dy=-2)
    out += rimmed(c, body, col, dx=3, dy=-2) + rimmed(c, neck, col, dx=3, dy=-2) + rimmed(c, headp, col, dx=3, dy=-2)
    out += f'<path d="M -190 -470 C -60 -446, 80 -446, 220 -470" stroke="#000" stroke-width="{c.sw(18)}" opacity="0.12" fill="none"/>'
    out += f'<path d="M -40 -790 C 20 -812, 80 -790, 120 -740" stroke="#ffe8c0" stroke-width="{c.sw(6)}" fill="none" opacity="0.35"/>'
    out += legs_svg[1]
    out += (f'<path d="M {fmt(456)} {fmt(-742 + bob)} l -6 -30 l 22 24 Z" fill="{col}" stroke="{OUT}" stroke-width="{c.sw(2)}"/>'
            f'<ellipse cx="{fmt(494)}" cy="{fmt(-724 + bob)}" rx="8" ry="6" fill="#120a06"/><circle cx="{fmt(496)}" cy="{fmt(-726 + bob)}" r="2.2" fill="#fff"/>'
            f'<path d="M {fmt(478)} {fmt(-736 + bob)} q 16 -8 30 -2" stroke="{OUT}" stroke-width="{c.sw(3)}" fill="none"/>'
            f'<ellipse cx="{fmt(566)}" cy="{fmt(-688 + bob)}" rx="5" ry="3.5" fill="#120a06"/>'
            f'<path d="M {fmt(574)} {fmt(-668 + bob)} q -18 6 -40 4" stroke="{OUT}" stroke-width="{c.sw(2)}" fill="none"/>'
            f'<path d="M {fmt(470)} {fmt(-700 + bob)} L {fmt(560)} {fmt(-680 + bob)} M {fmt(470)} {fmt(-668 + bob)} L {fmt(520)} {fmt(-700 + bob)}" stroke="#3a2414" stroke-width="{c.sw(4)}" opacity="0.8"/>')
    if saddle:
        out += (f'<path d="M -110 -760 C -80 -812, 110 -816, 140 -756 L 150 -640 L -120 -640 Z" fill="{blanket}" stroke="{OUT}" stroke-width="{c.sw(2.6)}"/>'
                f'<path d="M -118 -664 L 148 -664" stroke="{trim}" stroke-width="{c.sw(10)}"/>'
                + "".join(f'<path d="M {x} -644 l -7 24 l 14 0 Z" fill="{trim}" stroke="{OUT}" stroke-width="{c.sw(1.6)}"/>' for x in range(-104, 150, 32)) +
                f'<path d="M -70 -796 C -40 -826, 70 -830, 100 -796 L 92 -772 L -64 -772 Z" fill="#5a3418" stroke="{OUT}" stroke-width="{c.sw(2.4)}"/>'
                f'<path d="M -76 -800 L -88 -846 M 104 -800 L 116 -846" stroke="#5a3418" stroke-width="{c.sw(14)}" stroke-linecap="round"/>')
    return out

def dog(c, col="#d8b888", dark="#a87848", phase=0.0, run=False, t=0.0, seed=0):
    """a slim hunting dog (saluki), side view facing right; origin on the ground under the belly; ~ 420 wide x 300 tall.
    run: a gallop (front legs reach forward while the hind legs push back), ears and tail streaming back"""
    out = ""
    s_ = math.sin(phase) if run else 0.0
    bob = (-16 * abs(math.cos(phase)) if run else 2 * math.sin(t * 2.0 + seed))
    legs_svg = ["", ""]
    for i, (lx, front, ph) in enumerate([(92, True, 0.35), (-118, False, 0.35), (112, True, 0.0), (-98, False, 0.0)]):
        far = i < 2
        fill = dark if far else col
        if run:
            sw_ = math.sin(phase + ph)
            a = (38 * sw_ if front else -40 * sw_) + (8 if front else -8)
        else:
            a = 2 * math.sin(t * 1.3 + i + seed)
        r = math.radians(a)
        top = (lx, -168 + bob)
        knee = (lx + math.sin(r) * 86, -168 + bob + math.cos(r) * 86)
        bend = math.radians(a + (-28 if front else 38) * (1 if run else 0.25))
        foot = (knee[0] + math.sin(bend) * 82, min(-2, knee[1] + math.cos(bend) * 82))
        seg = (limb(c, top, knee, 17 if front else 22, 10, fill, 2.2) + limb(c, knee, foot, 9, 7, fill, 2.2) +
               f'<ellipse cx="{fmt(foot[0] + 7)}" cy="{fmt(foot[1])}" rx="13" ry="7" fill="{fill}" stroke="{OUT}" stroke-width="{c.sw(2)}"/>')
        legs_svg[0 if far else 1] += seg
    wag = 10 * math.sin(t * 7 + seed)
    if run:
        tail = [(-136, -190 + bob), (-190, -198 + bob), (-240, -190 + bob + 6 * s_), (-272, -168 + bob + 10 * s_)]
    else:
        tail = [(-136, -190 + bob), (-176, -186 + bob + wag * 0.3), (-206, -158 + bob + wag * 0.6), (-214, -116 + bob + wag), (-198, -96 + bob + wag)]
    td = "M " + " L ".join(f"{fmt(x)} {fmt(y)}" for x, y in tail)
    tail_svg = (f'<path d="{td}" stroke="{OUT}" stroke-width="{c.sw(17)}" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
                f'<path d="{td}" stroke="{col}" stroke-width="{c.sw(12)}" fill="none" stroke-linecap="round" stroke-linejoin="round"/>')
    stretch = 10 * s_
    body = smooth_path([(-140 - stretch, -188 + bob), (-120 - stretch, -212 + bob), (-40, -208 + bob), (40, -212 + bob), (100 + stretch, -222 + bob),
                        (136 + stretch, -205 + bob), (142 + stretch, -170 + bob), (120 + stretch, -134 + bob), (80, -118 + bob), (20, -130 + bob),
                        (-40, -148 + bob), (-100 - stretch, -152 + bob), (-140 - stretch, -166 + bob)])
    hx = 30 if run else 0; hy = 34 if run else 0
    neck = smooth_path([(96, -214 + bob), (128 + hx * 0.5, -252 + bob + hy * 0.6), (158 + hx, -276 + bob + hy), (178 + hx, -262 + bob + hy), (150 + hx * 0.5, -224 + bob + hy * 0.5), (136, -192 + bob)])
    hd = [(150, -282), (170, -296), (196, -293), (232, -280), (262, -268), (263, -258), (236, -253), (200, -255), (172, -258), (154, -266)]
    headp = smooth_path([(x + hx, y + bob + hy) for x, y in hd])
    ea = 34 if run else 4 * math.sin(t * 1.7 + seed)
    ear = smooth_path(bumpy([(172, -288), (152, -287), (138, -262), (132, -234), (146, -228), (158, -252), (174, -276)], 4))
    out += legs_svg[0] + tail_svg + rimmed(c, body, col, dx=3, dy=-2) + rimmed(c, neck, col, dx=3, dy=-2) + rimmed(c, headp, col, dx=3, dy=-2)
    out += f'<path d="M -110 {fmt(-160 + bob)} C -40 {fmt(-150 + bob)}, 40 {fmt(-140 + bob)}, 110 {fmt(-142 + bob)}" stroke="#000" stroke-width="{c.sw(10)}" opacity="0.10" fill="none"/>'
    out += legs_svg[1]
    out += f'<g transform="translate({fmt(hx)},{fmt(bob + hy)}) rotate({fmt(ea)},170,-285)">' + rimmed(c, ear, dark, dx=2, dy=-1) + '</g>'
    out += (f'<circle cx="{fmt(206 + hx)}" cy="{fmt(-282 + bob + hy)}" r="6" fill="#120a06"/><circle cx="{fmt(207 + hx)}" cy="{fmt(-284 + bob + hy)}" r="2" fill="#fff"/>'
            f'<ellipse cx="{fmt(261 + hx)}" cy="{fmt(-263 + bob + hy)}" rx="7" ry="6" fill="#120a06"/>'
            f'<path d="M {fmt(258 + hx)} {fmt(-254 + bob + hy)} q -16 6 -34 2" stroke="{OUT}" stroke-width="{c.sw(2)}" fill="none"/>')
    return out

def cow(c, col="#7a5a3e", spots="#efe6d6", t=0.0, graze=0.0, seed=0):
    """side view facing left; origin at the ground"""
    out = ""
    for i, lx in enumerate((-120, -80, 110, 150)):
        fill = "#4a3626" if i in (1, 3) else col
        out += limb(c, (lx, -200), (lx + 4 * math.sin(t + i), -6), 18, 14, fill) + f'<rect x="{lx-16}" y="-16" width="32" height="16" fill="#1e1410"/>'
    hy = 30 * graze
    body = smooth_path([(-170, -300), (40, -320), (190, -300), (220, -240), (190, -180), (-150, -170), (-190, -230)])
    out += rimmed(c, body, col, dx=3, dy=-2)
    out += f'<ellipse cx="40" cy="-260" rx="50" ry="30" fill="{spots}" opacity="0.9"/><ellipse cx="140" cy="-250" rx="30" ry="22" fill="{spots}" opacity="0.9"/>'
    out += f'<path d="M 200 -280 C 230 -300, 240 -200, 230 -180" stroke="{col}" stroke-width="{c.sw(10)}" fill="none"/>'
    hd = smooth_path([(-168, -306 + hy), (-206, -318 + hy), (-236, -300 + hy), (-268, -236 + hy), (-276, -208 + hy), (-254, -194 + hy), (-226, -200 + hy), (-200, -240 + hy), (-176, -250)])
    out += rimmed(c, hd, col, dx=2, dy=-2)
    out += (f'<path d="M -214 {-312+hy} c -6 -16, -18 -24, -30 -26 M -192 {-314+hy} c 4 -16, 14 -24, 26 -26" stroke="#e8dcc0" stroke-width="{c.sw(7)}" stroke-linecap="round" fill="none"/>'
            f'<ellipse cx="{-176}" cy="{-296+hy}" rx="20" ry="9" fill="{col}" stroke="{OUT}" stroke-width="{c.sw(2)}" transform="rotate(20,-176,{-296+hy})"/>'
            f'<circle cx="-226" cy="{-276+hy}" r="6" fill="#120a06"/><ellipse cx="-262" cy="{-210+hy}" rx="18" ry="13" fill="#e2b4a0" stroke="{OUT}" stroke-width="{c.sw(2)}"/>'
            f'<ellipse cx="-268" cy="{-212+hy}" rx="3" ry="4" fill="#5a3020"/>')
    return out
