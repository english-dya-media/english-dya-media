"""Building blocks for the civil-engineering reels (new Instagram page, bilingual Persian + English).

A reel is one main scene (hook on top, an animated SVG diagram, a timeline of bottom captions) plus a short
follow card. Times are seconds on the main timeline (0 = first frame). Both kinds of animation used here are
seeked frame by frame by reel.py, so renders are deterministic:
  - CSS animations, written with A(...)
  - SMIL morphs and moves inside the SVG, written with morph(...) / move(...)
Never put a CSS transform animation and a SMIL animateTransform on the same element: nest two <g> instead.

write_reel(...) / write_quiz(...) check the input and save content/<tag>.json for reel.py and plan.py.
"""
import json, math, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
CONTENT = os.path.join(HERE, "content")
ZW = "‌"                                    # zero-width non-joiner: می‌گیرن، نکته‌ی، ها

INK, DIM, ACC, RED, BLUE, GREEN = "#E8F3FF", "#8FB3D9", "#FFD43B", "#FF5C7A", "#4FC3F7", "#2EE59D"
EZ, BO, IO = "cubic-bezier(.2,.8,.2,1)", "cubic-bezier(.2,.9,.3,1.3)", "cubic-bezier(.45,0,.2,1)"
KINDS = {  # badge: Persian, English, Fluent emoji
    "concept": (f"مفهوم روز", "Concept of the day", "light_bulb"),
    "site": (f"نکته{ZW}ی کارگاهی", "Site tip", "hammer_and_wrench"),
    "quiz": ("تست روز", "Daily quiz", "brain"),
}
FA_DIGITS = str.maketrans("0123456789", "۰۱۲۳۴۵۶۷۸۹")


def fa(s):
    """ASCII digits -> Persian digits (use in Persian text only)."""
    return str(s).translate(FA_DIGITS)


def A(*specs):
    """CSS animation list. Each spec: (name, dur, delay[, easing[, fill[, iterations]]]).
    A(("fadeIn", .3, 1.2), ("fadeOut", .3, 5, "ease-in", "forwards"))"""
    out = []
    for s in specs:
        name, dur, delay = s[0], s[1], s[2]
        ease = s[3] if len(s) > 3 and s[3] else EZ
        fill = s[4] if len(s) > 4 and s[4] else "both"
        it = s[5] if len(s) > 5 else 1
        out.append(f"{name} {dur:g}s {ease} {delay:g}s {it} normal {fill}")
    return "animation:" + ",".join(out) + ";"


def show(t, kind="popIn", dur=.35, until=None, ease=None):
    """Appear at t (and fade out at `until`)."""
    specs = [(kind, dur, t, ease or (BO if kind == "popIn" else EZ))]
    if until is not None:
        specs.append(("fadeOut", .3, until - .3, "ease-in", "forwards"))
    return A(*specs)


def dim(t, to=".18"):
    return ("dim" + to.replace(".", ""), .4, t, "ease", "forwards")


# ---------- SVG pieces ----------

def g(inner, style="", cls="", extra=""):
    c = f' class="{cls}"' if cls else ""
    s = f' style="{style}"' if style else ""
    return f"<g{c}{s}{(' ' + extra) if extra else ''}>{inner}</g>"


def pth(d, stroke=INK, w=6, fill="none", style="", extra="", inner=""):
    s = f' style="{style}"' if style else ""
    return (f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{w}" stroke-linecap="round" '
            f'stroke-linejoin="round"{s}{(" " + extra) if extra else ""}>{inner}</path>')


def draw(d, t, dur=.6, stroke=INK, w=6, fill="none", style="", extra="", inner=""):
    """A path that draws itself in at t."""
    return pth(d, stroke, w, fill, "stroke-dasharray:1;" + A(("drawIn", dur, t, "ease-out")) + style,
               'pathLength="1"' + ((" " + extra) if extra else ""), inner)


def morph(d0, d1, begin, dur=.8):
    """SMIL: morph a path's d (same commands in both) starting at `begin`."""
    return (f'<animate attributeName="d" begin="{begin:g}s" dur="{dur:g}s" fill="freeze" values="{d0};{d1}" '
            f'calcMode="spline" keyTimes="0;1" keySplines=".45 0 .2 1"/>')


def move(points, begin, dur=.8):
    """SMIL: translate a <g> through points [(x0,y0),(x1,y1),...] (equal time per leg) starting at `begin`."""
    n = len(points) - 1
    kt = ";".join(f"{i / n:g}" for i in range(n + 1))
    ks = ";".join([".45 0 .2 1"] * n)
    vals = ";".join(f"{x:g} {y:g}" for x, y in points)
    return (f'<animateTransform attributeName="transform" type="translate" begin="{begin:g}s" dur="{dur:g}s" '
            f'fill="freeze" values="{vals}" calcMode="spline" keyTimes="{kt}" keySplines="{ks}"/>')


def bob(dy, begin, period, count):
    """SMIL: up-down strokes (e.g. a tamping rod)."""
    return (f'<animateTransform attributeName="transform" type="translate" begin="{begin:g}s" dur="{period:g}s" '
            f'repeatCount="{count}" values="0 0;0 {dy:g};0 0" keyTimes="0;.45;1" calcMode="linear" additive="sum"/>')


def arrow(x1, y1, x2, y2, color=INK, w=6, head=20):
    ang = math.atan2(y2 - y1, x2 - x1)
    bx, by = x2 - head * math.cos(ang), y2 - head * math.sin(ang)
    px, py, hw = -math.sin(ang), math.cos(ang), head * .62
    return (f'<line x1="{x1:g}" y1="{y1:g}" x2="{bx:.1f}" y2="{by:.1f}" stroke="{color}" stroke-width="{w}" stroke-linecap="round"/>'
            f'<polygon points="{x2:g},{y2:g} {bx + px * hw:.1f},{by + py * hw:.1f} {bx - px * hw:.1f},{by - py * hw:.1f}" '
            f'fill="{color}" stroke="{color}" stroke-width="2" stroke-linejoin="round"/>')


def tfa(x, y, s, size=40, color=INK, weight=800, anchor="middle", style=""):
    st = f' style="{style}"' if style else ""
    return (f'<text x="{x:g}" y="{y:g}" font-family="Vaz" font-size="{size}" font-weight="{weight}" fill="{color}" '
            f'text-anchor="{anchor}" direction="rtl" class="halo"{st}>{s}</text>')


def ten(x, y, s, size=28, color=DIM, weight=600, anchor="middle", style="", font="Pop"):
    st = f' style="{style}"' if style else ""
    return (f'<text x="{x:g}" y="{y:g}" font-family="{font}" font-size="{size}" font-weight="{weight}" fill="{color}" '
            f'text-anchor="{anchor}" class="halo"{st}>{s}</text>')


def label(x, y, fa_s, en_s, color, t, size=40, until=None, kind="popIn"):
    """Persian word over its English term, appearing at t."""
    return g(tfa(x, y, fa_s, size, color) + ten(x, y + size * .9, en_s, int(size * .72), color, 600),
             show(t, kind, until=until), "tb")


def ground(x1, x2, y, step=18, t=None):
    s = f'<line x1="{x1:g}" y1="{y:g}" x2="{x2:g}" y2="{y:g}" stroke="{DIM}" stroke-width="4" stroke-linecap="round"/>'
    x = x1 + 6
    while x < x2:
        s += f'<line x1="{x:g}" y1="{y + 2:g}" x2="{x - 12:g}" y2="{y + 16:g}" stroke="{DIM}" stroke-width="3" stroke-linecap="round"/>'
        x += step
    return s


def pin(x, y, t, k=1.0):
    """Pinned support, apex at (x, y), ground at y + 60k."""
    h, b = 60 * k, 34 * k
    tri = f'<polygon points="{x:g},{y:g} {x - b:g},{y + h:g} {x + b:g},{y + h:g}" fill="rgba(143,179,217,.18)" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
    return g(tri + ground(x - b - 14 * k, x + b + 14 * k, y + h), show(t), "tb")


def roller(x, y, t, k=1.0):
    """Roller support, apex at (x, y), ground at y + 60k."""
    h, b, r = 44 * k, 30 * k, 8 * k
    s = f'<polygon points="{x:g},{y:g} {x - b:g},{y + h:g} {x + b:g},{y + h:g}" fill="rgba(143,179,217,.18)" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
    for cx in (x - b * .55, x + b * .55):
        s += f'<circle cx="{cx:g}" cy="{y + h + r:g}" r="{r:g}" fill="none" stroke="{INK}" stroke-width="4"/>'
    return g(s + ground(x - b - 14 * k, x + b + 14 * k, y + h + 2 * r), show(t), "tb")


def crack(x, y, t, h=42, up=True, color=RED):
    sgn = -1 if up else 1
    pts = [(x, y), (x - 7, y + sgn * h * .3), (x + 6, y + sgn * h * .56), (x - 5, y + sgn * h * .8), (x + 2, y + sgn * h)]
    return draw("M" + " L".join(f"{a:.1f},{b:.1f}" for a, b in pts), t, .3, color, 5)


def dimline(x1, y1, x2, y2, text, t, color=DIM, tw=None, off=0, size=30, font="Pop", fa_text=False, until=None):
    """Dimension line with end ticks and a centred label (Latin text by default)."""
    ang = math.atan2(y2 - y1, x2 - x1)
    px, py = -math.sin(ang) * 12, math.cos(ang) * 12
    s = f'<line x1="{x1:g}" y1="{y1:g}" x2="{x2:g}" y2="{y2:g}" stroke="{color}" stroke-width="3"/>'
    for x, y in ((x1, y1), (x2, y2)):
        s += f'<line x1="{x - px:.1f}" y1="{y - py:.1f}" x2="{x + px:.1f}" y2="{y + py:.1f}" stroke="{color}" stroke-width="3"/>'
    s += arrow((x1 + x2) / 2, (y1 + y2) / 2, x1, y1, color, 3, 14) + arrow((x1 + x2) / 2, (y1 + y2) / 2, x2, y2, color, 3, 14)
    mx, my = (x1 + x2) / 2 + (off if abs(ang) > 1 else 0), (y1 + y2) / 2 + size * .35 + (0 if abs(ang) > 1 else off)
    s += (tfa(mx, my, text, size, color) if fa_text else ten(mx, my, text, size, color, 700, font=font))
    return g(s, show(t, "fadeIn", .4, until=until))


def defs():
    """Patterns: concrete with aggregate (agg), hatching for walls/soil (hatch)."""
    return ('<defs>'
            '<pattern id="agg" width="30" height="30" patternUnits="userSpaceOnUse">'
            '<rect width="30" height="30" fill="#8E9BA8"/><circle cx="6" cy="8" r="3.2" fill="#6E7B88"/>'
            '<circle cx="20" cy="18" r="4.2" fill="#ABB6C1"/><circle cx="25" cy="5" r="2.2" fill="#5E6A76"/>'
            '<circle cx="10" cy="23" r="2.6" fill="#B9C3CC"/><circle cx="16" cy="9" r="1.6" fill="#7A8794"/></pattern>'
            '<pattern id="hatch" width="18" height="18" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
            '<rect width="18" height="18" fill="rgba(143,179,217,.10)"/><line x1="0" y1="0" x2="0" y2="18" stroke="#8FB3D9" stroke-width="3"/></pattern>'
            '</defs>')


def sag(x0, x1, y, d):
    """Cubic for an edge from x0 to x1 at height y that sags d at midspan (d=0 -> straight). Returns 'C ...'."""
    a, b, c = (2 * x0 + x1) / 3, (x0 + 2 * x1) / 3, y + d / .75
    return f"{x0:g},{y:g} C{a:g},{c:g} {b:g},{c:g} {x1:g},{y:g}"


def beam_d(x0, x1, top, depth, d=0.0):
    """Closed outline of a simply supported beam sagging d at midspan (same commands for any d, so it morphs)."""
    a, b = (2 * x0 + x1) / 3, (x0 + 2 * x1) / 3
    c = d / .75
    return (f"M{x0:g},{top:g} C{a:g},{top + c:g} {b:g},{top + c:g} {x1:g},{top:g} L{x1:g},{top + depth:g} "
            f"C{b:g},{top + depth + c:g} {a:g},{top + depth + c:g} {x0:g},{top + depth:g} Z")


def sag_at(x, x0, x1, d):
    """Deflection at x of the cubic used by beam_d (4·d·t·(1−t)·… exact for evenly spaced controls)."""
    t = (x - x0) / (x1 - x0)
    return 3 * t * (1 - t) * d / .75


# ---------- content files ----------

def _check_text(where, s, n):
    plain = re.sub(r"<[^>]+>|:[a-z0-9_]+:", "", s)
    if len(plain) > n:
        raise SystemExit(f"{where}: too long ({len(plain)} > {n} characters): {plain}")


def _common(tag, n, kind, date, slot, caption, hashtags):
    if kind not in KINDS:
        raise SystemExit(f"kind must be one of {list(KINDS)}")
    if not re.fullmatch(r"c\d{3}", tag):
        raise SystemExit("tag must look like c001")
    tags = " ".join("#" + h.lstrip("#") for h in hashtags)
    return dict(tag=tag, n=n, kind=kind, date=date, slot=slot, caption=caption.strip() + "\n\n" + tags)


def write_reel(tag, n, kind, hook_fa, hook_en, svg, svg_h, steps, dur, caption, hashtags, sfx=(),
               date=None, slot="19:30", cover=1.6, topic=""):
    """steps: [{"t": sec, "fa": "...", "en": "..."} or {"t": sec, "html": "<div class='panel'>...</div>"}], in order.
    sfx: [(sec, "whoosh"|"pop"|"ding"|"boop"|"tick"|"sting", gain), ...]"""
    _check_text("hook_fa", hook_fa, 34); _check_text("hook_en", hook_en, 60)
    last = -1
    for i, s in enumerate(steps):
        if s["t"] <= last or s["t"] >= dur:
            raise SystemExit(f"step {i}: times must increase and stay inside the reel")
        last = s["t"]
        if "html" not in s:
            _check_text(f"step {i} fa", s["fa"], 52); _check_text(f"step {i} en", s["en"], 70)
    d = _common(tag, n, kind, date, slot, caption, hashtags)
    d.update(hook_fa=hook_fa, hook_en=hook_en, svg=svg, svg_h=svg_h, steps=steps, dur=dur, sfx=list(sfx),
             cover=cover, topic=topic)
    _save(d)


def write_quiz(tag, n, q_fa, q_en, sub_fa, sub_en, options, answer, svg, svg_h, reveal_svg_t, t_opts, t_count,
               steps, dur, caption, hashtags, think=5, sfx=(), date=None, slot="19:30", cover=2.6, topic=""):
    """options: [(fa, en)] x4, answer: index. Countdown `think` s from t_count; reveal at t_count + think.
    steps after the reveal: like write_reel (shown under the right answer)."""
    if len(options) != 4 or not 0 <= answer < 4:
        raise SystemExit("4 options and a valid answer index")
    _check_text("q_fa", q_fa, 60); _check_text("q_en", q_en, 70)
    for i, (f, e) in enumerate(options):
        _check_text(f"option {i} fa", f, 26); _check_text(f"option {i} en", e, 26)
    t_rev = t_count + think
    for s in steps:
        if s["t"] < t_rev + .5:
            raise SystemExit("explanation steps start after the reveal")
    d = _common(tag, n, "quiz", date, slot, caption, hashtags)
    d.update(hook_fa=q_fa, hook_en=q_en, sub_fa=sub_fa, sub_en=sub_en, options=options, answer=answer,
             svg=svg, svg_h=svg_h, t_opts=t_opts, t_count=t_count, think=think, t_reveal=t_rev, steps=steps,
             dur=dur, sfx=list(sfx), cover=cover, topic=topic)
    _save(d)


def _save(d):
    os.makedirs(CONTENT, exist_ok=True)
    p = os.path.join(CONTENT, d["tag"] + ".json")
    json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("wrote", os.path.relpath(p, HERE))
