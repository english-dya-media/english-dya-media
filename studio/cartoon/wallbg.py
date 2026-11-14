"""painted backgrounds for the sample (sunrise on the fortress wall)"""
import io, random, math
import resvg_py
from PIL import Image, ImageFilter

def render(svgtxt, w, h):
    doc = f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">{svgtxt}</svg>'
    return Image.open(io.BytesIO(bytes(resvg_py.svg_to_bytes(svg_string=doc, skip_system_fonts=True)))).convert("RGBA")

def ridge(w, base, amp, seed, n=40, rough=0.35):
    r = random.Random(seed)
    ys = []
    y = 0
    for i in range(n + 1):
        y = y * 0.6 + r.uniform(-1, 1)
        ys.append(y)
    pts = []
    for i in range(n + 1):
        x = w * i / n
        yy = base - amp * (0.5 + 0.5 * math.sin(i * 0.37 + seed)) - amp * rough * ys[i]
        pts.append((x, yy))
    d = f"M 0 {base+2000} L " + " L ".join(f"{x:.0f} {y:.0f}" for x, y in pts) + f" L {w} {base+2000} Z"
    return d

def sky_defs(sx, sy):
    return (f'<defs><linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">'
            '<stop offset="0" stop-color="#1b2550"/><stop offset="0.22" stop-color="#3e3d78"/><stop offset="0.38" stop-color="#9a5a7a"/>'
            '<stop offset="0.47" stop-color="#e57f62"/><stop offset="0.53" stop-color="#ffc07a"/><stop offset="0.6" stop-color="#ffd9a0"/></linearGradient>'
            f'<radialGradient id="sun" cx="{sx}" cy="{sy}" r="520" gradientUnits="userSpaceOnUse">'
            '<stop offset="0" stop-color="#fff6dc" stop-opacity="1"/><stop offset="0.08" stop-color="#ffe7b0" stop-opacity="0.95"/>'
            '<stop offset="0.3" stop-color="#ffb46a" stop-opacity="0.45"/><stop offset="1" stop-color="#ff8a50" stop-opacity="0"/></radialGradient>'
            '<linearGradient id="haze" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffb47a" stop-opacity="0"/>'
            '<stop offset="1" stop-color="#ffb47a" stop-opacity="0.75"/></linearGradient>'
            '<filter id="b6"><feGaussianBlur stdDeviation="6"/></filter><filter id="b14"><feGaussianBlur stdDeviation="14"/></filter>'
            '<filter id="b30"><feGaussianBlur stdDeviation="30"/></filter></defs>')

def clouds(w, seed, ys):
    r = random.Random(seed); out = ""
    for y in ys:
        x = r.uniform(-200, w)
        for k in range(3):
            L = r.uniform(260, 520); hh = r.uniform(10, 22)
            out += (f'<path d="M {x:.0f} {y:.0f} C {x+L*0.3:.0f} {y-hh:.0f}, {x+L*0.7:.0f} {y-hh*1.3:.0f}, {x+L:.0f} {y:.0f} '
                    f'C {x+L*0.6:.0f} {y+hh*0.6:.0f}, {x+L*0.3:.0f} {y+hh*0.5:.0f}, {x:.0f} {y:.0f} Z" fill="#f7a58a" opacity="0.55" filter="url(#b6)"/>'
                    f'<path d="M {x+L*0.1:.0f} {y+hh*0.25:.0f} C {x+L*0.4:.0f} {y+hh*0.5:.0f}, {x+L*0.7:.0f} {y+hh*0.4:.0f}, {x+L*0.95:.0f} {y+hh*0.1:.0f}" '
                    f'stroke="#ffd2a0" stroke-width="4" fill="none" opacity="0.7" filter="url(#b6)"/>')
            x += L * r.uniform(0.6, 1.1); y += r.uniform(-14, 14)
    return out

def wide_sky(W=1080, H=1920, sx=900, sy=1000):
    s = sky_defs(sx, sy) + f'<rect width="{W}" height="{H}" fill="url(#sky)"/>'
    s += clouds(W, 3, [420, 560, 700, 820])
    s += f'<rect width="{W}" height="{H}" fill="url(#sun)"/>'
    s += f'<circle cx="{sx}" cy="{sy}" r="58" fill="#fff4d6"/>'
    # mountains: far -> near with haze between
    s += f'<path d="{ridge(W, 1040, 120, 5)}" fill="#b07a8a"/>'
    s += f'<rect x="0" y="880" width="{W}" height="260" fill="url(#haze)" opacity="0.6"/>'
    s += f'<path d="{ridge(W, 1110, 140, 9)}" fill="#7d4f6c"/>'
    s += f'<rect x="0" y="960" width="{W}" height="230" fill="url(#haze)" opacity="0.45"/>'
    s += f'<path d="{ridge(W, 1190, 120, 13)}" fill="#4a2d47"/>'
    # rim of sunlight on the near ridge facing the sun
    s += f'<path d="{ridge(W, 1190, 120, 13)}" fill="none" stroke="#ff9a62" stroke-width="3" opacity="0.6" transform="translate(2,-2)"/>'
    # valley mist glowing
    s += f'<ellipse cx="{W*0.55}" cy="1215" rx="{W*0.8}" ry="70" fill="#ffc290" opacity="0.55" filter="url(#b30)"/>'
    # distant fortress tower at the left
    s += ('<path d="M 40 1250 L 40 840 L 30 840 L 30 800 L 52 800 L 52 818 L 76 818 L 76 800 L 100 800 L 100 818 L 124 818 L 124 800 L 146 800 L 146 840 L 136 840 L 136 1250 Z" fill="#2e1c2c"/>'
          '<rect x="80" y="900" width="16" height="30" fill="#ffb25e"/>')
    # god rays
    for a in range(-40, 41, 16):
        ang = math.radians(200 + a); L = 900
        x2 = sx + L * math.cos(ang); y2 = sy + L * math.sin(ang)
        s += f'<path d="M {sx} {sy} L {x2:.0f} {y2-40:.0f} L {x2:.0f} {y2+40:.0f} Z" fill="#ffcf9a" opacity="0.06" filter="url(#b14)"/>'
    return render(s, W, H)

def wall_fg(W=1080, H=1920, top=1250):
    r = random.Random(4)
    s = ('<defs><linearGradient id="st" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8a6250"/>'
         '<stop offset="1" stop-color="#3a241e"/></linearGradient>'
         '<linearGradient id="shade" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#000" stop-opacity="0"/>'
         '<stop offset="1" stop-color="#000" stop-opacity="0.6"/></linearGradient></defs>')
    merl_w, gap = 170, 300
    xs = [-120 + i * (merl_w + gap) for i in range(4)]
    # main wall
    s += f'<rect x="0" y="{top}" width="{W}" height="{H-top}" fill="url(#st)" stroke="#1b0f0a" stroke-width="3"/>'
    for x in xs:
        s += (f'<path d="M {x} {top+2} L {x} {top-120} L {x+merl_w} {top-120} L {x+merl_w} {top+2} Z" fill="url(#st)" stroke="#1b0f0a" stroke-width="3"/>'
              f'<path d="M {x+merl_w-18} {top-118} L {x+merl_w-2} {top-118} L {x+merl_w-2} {top} L {x+merl_w-18} {top} Z" fill="#ffb07a" opacity="0.35"/>'
              f'<path d="M {x+2} {top-118} L {x+merl_w-2} {top-118}" stroke="#ffc38f" stroke-width="5" opacity="0.6"/>')
    s += f'<path d="M 0 {top+2} L {W} {top+2}" stroke="#ffc38f" stroke-width="5" opacity="0.55"/>'
    # stones
    for row in range(14):
        y = top + 14 + row * 52
        off = (row % 2) * 60
        for c in range(-1, 10):
            x = c * 120 + off + r.uniform(-8, 8)
            s += (f'<rect x="{x+4:.0f}" y="{y:.0f}" width="{112:.0f}" height="46" rx="6" fill="#{r.randint(0x6a,0x80):02x}{r.randint(0x4a,0x56):02x}{r.randint(0x3c,0x46):02x}" '
                  f'opacity="0.55" stroke="#2a1812" stroke-width="2"/>')
    for x in xs:
        for row in range(2):
            y = top - 112 + row * 56
            s += f'<rect x="{x+8}" y="{y}" width="{merl_w-16}" height="48" rx="6" fill="#7a5644" opacity="0.5" stroke="#2a1812" stroke-width="2"/>'
    s += f'<rect x="0" y="{top}" width="{W}" height="{H-top}" fill="url(#shade)"/>'
    return render(s, W, H), xs, merl_w, gap

def close_bg(W=1080, H=1920):
    sx, sy = 880, 1180
    s = sky_defs(sx, sy) + f'<rect width="{W}" height="{H}" fill="url(#sky)"/>'
    s += clouds(W, 7, [360, 520, 690, 860, 1000])
    s += f'<rect width="{W}" height="{H}" fill="url(#sun)"/>'
    s += f'<circle cx="{sx}" cy="{sy}" r="80" fill="#fff4d6"/>'
    s += f'<path d="{ridge(W, 1460, 160, 21)}" fill="#a87386"/>'
    s += f'<rect x="0" y="1260" width="{W}" height="300" fill="url(#haze)" opacity="0.5"/>'
    s += f'<path d="{ridge(W, 1560, 150, 22)}" fill="#6a4060"/>'
    s += f'<ellipse cx="{W*0.5}" cy="1580" rx="{W}" ry="90" fill="#ffc290" opacity="0.5" filter="url(#b30)"/>'
    im = render(s, W, H)
    return im.filter(ImageFilter.GaussianBlur(7))

if __name__ == "__main__":
    import os; os.makedirs("out", exist_ok=True)
    a = wide_sky(); a.save("out/wide_sky.png")
    b, xs, mw, gap = wall_fg(); b.save("out/wall_fg.png"); print(xs)
    c = close_bg(); c.save("out/close_bg.png")
    comp = a.copy(); comp.alpha_composite(b)
    sheet = Image.new("RGB", (1080, 960))
    sheet.paste(comp.convert("RGB").resize((540, 960)), (0, 0)); sheet.paste(c.convert("RGB").resize((540, 960)), (540, 0))
    sheet.save("out/bg_sheet.png")
