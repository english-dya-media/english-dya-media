"""Batch 1: the three sample reels (one of each kind) for the owner to approve the style.
c001 concept: why the main rebar sits at the bottom of a beam (and on top in a cantilever)
c002 site tip: the slump test
c003 quiz: span x2 -> deflection x16 (simple beam, UDL)
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from kit import *  # noqa: F401,F403

CONC = 'url(#agg)'
TAGS_STRUCT = ["عمران", "مهندسی_عمران", "سازه", "دانشجوی_عمران", "مهندس_عمران", "civilengineering", "structuralengineering", "engineering"]


def harrow(x1, y1, x2, y2, color, w=7, head=22):
    """Arrow with a dark outline so it reads on any fill."""
    return arrow(x1, y1, x2, y2, "#0A2140", w + 6, head + 6) + arrow(x1, y1, x2, y2, color, w, head)


# ---------------------------------------------------------------- c001: rebar at the bottom
X0, X1, TOP, DEP, D = 100, 820, 250, 90, 45
straight, bent = beam_d(X0, X1, TOP, DEP, 0), beam_d(X0, X1, TOP, DEP, D)
TB = 2.4                                                     # bending starts
xs = list(range(130, 791, 60))                               # 12 load arrows
tail0 = "M" + " L".join(f"{x},140" for x in xs)
tail1 = "M" + " L".join(f"{x},{140 + sag_at(x, X0, X1, D):.1f}" for x in xs)
load = draw(tail0, 1.1, .45, INK, 4, inner=morph(tail0, tail1, TB, .9))
for i, x in enumerate(xs):
    load += g(g(arrow(x, 140, x, 240, INK, 5, 18), A(("dropIn", .4, 1.1 + i * .03))) + move([(0, 0), (0, sag_at(x, X0, X1, D))], TB, .9))
load += label(460, 84, "بار", "Load", INK, 1.35)
ss = g(load, A(dim(4.3)))
ss += draw(straight, .15, .7, INK, 6, fill=CONC, style="fill-opacity:.62", inner=morph(straight, bent, TB, .9))
ss += pin(110, 340, .6) + roller(810, 340, .7)
yc, yt = TOP + D + 24, TOP + DEP + D - 24
ss += g(harrow(360, yc, 445, yc, BLUE) + harrow(560, yc, 475, yc, BLUE), show(4.6), "tb")
ss += label(460, 206, "فشار", "Compression", BLUE, 4.75)
ss += g(harrow(445, yt, 360, yt, RED) + harrow(475, yt, 560, yt, RED), show(5.4), "tb")
ss += label(460, 455, "کشش", "Tension", RED, 5.55)
cr = "".join(crack(x, TOP + DEP + sag_at(x, X0, X1, D) - 1, 8.0 + k * .15, 38) for k, x in enumerate((320, 460, 600)))
ss += g(cr, A(dim(11.8, ".25")))
reb = "M112,327 C342,383 578,383 808,327"
ss += draw(reb, 11.2, .8, "#0A2140", 16) + draw(reb, 11.2, .8, ACC, 9)
ss += label(700, 455, "میلگرد", "Rebar", ACC, 11.9)
svg1 = defs() + g(ss, A(("fadeOut", .3, 17.1, "ease-in", "forwards")))

# cantilever (from 17.4): tension on top, main rebar on top
cs = "M110,265 C327,265 543,265 760,265 L760,365 C543,365 327,365 110,365 Z"
cb = "M110,265 C327,265 543,285 760,335 L760,435 C543,385 327,365 110,365 Z"
TB2 = 18.8
ca = f'<rect x="50" y="150" width="60" height="330" fill="url(#hatch)" stroke="{INK}" stroke-width="4"/>'
ca = g(ca, show(17.45, "fadeIn", .4))
ca += draw(cs, 17.6, .6, INK, 6, fill=CONC, style="fill-opacity:.62", inner=morph(cs, cb, TB2, .9))
ca += g(g(arrow(735, 145, 735, 253, INK, 6, 22) + label(812, 191, "بار", "Load", INK, 18.4, 36), A(("dropIn", .4, 18.25)))
        + move([(0, 0), (0, 64)], TB2, .9))
ca += g(g(harrow(320, 300, 232, 300, RED) + harrow(350, 300, 438, 300, RED), show(20.1), "tb"), A(dim(20.8, ".25")))
ca += g(harrow(232, 344, 320, 344, BLUE) + harrow(438, 344, 350, 344, BLUE), show(20.3), "tb")
ca += label(300, 212, "کشش", "Tension", RED, 20.15) + label(335, 434, "فشار", "Compression", BLUE, 20.35)
ca += "".join(crack(x, 266, 20.2 + k * .12, 32, up=False) for k, x in enumerate((128, 162, 196)))
reb2 = "M70,279 L110,279 C327,279 543,299 748,346"
ca += draw(reb2, 20.8, .8, "#0A2140", 16) + draw(reb2, 20.8, .8, ACC, 9)
ca += label(600, 200, f"میلگرد اصلی", "Main rebar", ACC, 21.45)
svg1 += ca

write_reel(
    "c001", 1, "concept",
    "چرا میلگرد اصلی پایینِ تیره؟", "Why is the main rebar at the bottom of a beam?",
    svg1, 560,
    [dict(t=1.0, fa="بار که میاد روی تیر…", en="When a load sits on the beam…"),
     dict(t=2.4, fa=f"…تیر خم میشه", en="…the beam bends"),
     dict(t=4.4, fa=f"بالای تیر <b>فشرده</b> میشه و پایینش <b>کشیده</b>", en="The top is squeezed, the bottom is stretched"),
     dict(t=7.8, fa=f"بتن توی کشش ضعیفه ← ترک می{ZW}خوره", en="Concrete is weak in tension → it cracks"),
     dict(t=11.0, fa=f"میلگرد فولادی کشش رو تحمل می{ZW}کنه :flexed_biceps:", en="Steel rebar carries the tension"),
     dict(t=14.2, html=('<div class="panel tk">'
                        '<div class="tkrow"><span>بتن</span>←<span style="color:var(--blue)">فشار</span><span class="en">Concrete → Compression</span></div>'
                        '<div class="tkrow"><span>فولاد</span>←<span style="color:var(--red)">کشش</span><span class="en">Steel → Tension</span></div></div>')),
     dict(t=17.4, fa="ولی توی تیر طره (کنسول)…", en="But in a cantilever…"),
     dict(t=20.0, fa="…کشش بالای تیره", en="…the tension is on top"),
     dict(t=21.4, fa="پس میلگرد اصلی میره <b>بالا</b>!", en="so the main rebar goes on top!")],
    24.6,
    f"""چرا میلگرد اصلی رو پایینِ تیر می{ZW}ذارن؟ 🤔

تیر ساده زیر بار خم میشه: بالاش فشرده میشه و پایینش کشیده. بتن فشار رو خوب تحمل می{ZW}کنه ولی مقاومت کششی{ZW}ش حدوداً یک{ZW}دهمِ مقاومت فشاری{ZW}شه، برای همین پایینِ تیر ترک می{ZW}خوره. میلگرد فولادی این کشش رو می{ZW}گیره.

⚠️ ولی توی تیر طره (کنسول) کشش بالای تیره، پس میلگرد اصلی میره بالا!

📘 اصطلاحات:
Tension = کشش
Compression = فشار
Rebar = میلگرد
Cantilever = طره / کنسول

👷 هر روز یه درس عمران | فالو کن و برای همکلاسیت بفرست""",
    TAGS_STRUCT[:5] + ["بتن_آرمه", "civilengineering", "structuralengineering", "reinforcedconcrete"],
    sfx=[(1.1, "whoosh", .25), (TB, "whoosh", .2), (4.6, "pop", .3), (5.4, "pop", .3), (8.0, "boop", .35), (8.15, "boop", .25),
         (8.3, "boop", .25), (11.2, "ding", .3), (14.2, "pop", .35), (17.1, "whoosh", .3), (TB2, "whoosh", .2), (20.2, "boop", .3),
         (20.8, "ding", .3)],
    cover=1.6, topic="rebar position in beams")

# ---------------------------------------------------------------- c002: slump test
cone = (f'<path d="M340,560 L400,200 M520,200 L580,560 M400,200 L520,200 M380,308 h-36 v24 h33 M540,308 h36 v24 h-33 '
        f'M340,560 h-34 M580,560 h34" fill="none" stroke="{INK}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round" '
        f'pathLength="1" style="stroke-dasharray:1;{A(("drawIn", .8, .3, "ease-out"))}"/>')
cone = g(cone + move([(0, 0), (0, -190)], 9.9, 1.3) + move([(0, -190), (-288, -190), (-288, 0)], 12.6, 1.2))
lay = [((347, 558), (367, 440), (553, 440), (573, 558)), ((367, 440), (387, 320), (533, 320), (553, 440)),
       ((387, 320), (406.5, 203), (513.5, 203), (533, 320))]
layers = ""
for k, pts in enumerate(lay):
    pp = " ".join(f"{x:g},{y:g}" for x, y in pts)
    layers += f'<polygon points="{pp}" fill="{CONC}" class="gu" style="{A(("growUp", .6, 3.8 + .8 * k, "ease-out"))}"/>'
for k, y in enumerate((440, 320)):
    layers += (f'<line x1="{367 + 20 * k}" y1="{y}" x2="{553 - 20 * k}" y2="{y}" stroke="rgba(255,255,255,.55)" stroke-width="3" '
               f'stroke-dasharray="10 8" style="{A(("fadeIn", .3, 4.5 + .8 * k))}"/>')
layers = g(layers, A(("fadeOut", .05, 10.45, "linear", "forwards")))
body0 = "M347,558 L406.5,203 C442,203 478,203 513.5,203 L573,558 Z"
body1 = "M300,558 L352,345 C400,286 520,286 568,345 L620,558 Z"
body = pth(body0, "none", 0, CONC, A(("fadeIn", .05, 10.45, "linear")), inner=morph(body0, body1, 10.5, 1.2))
rod = (f'<line x1="460" y1="10" x2="460" y2="188" stroke="#0A2140" stroke-width="18" stroke-linecap="round"/>'
       f'<line x1="460" y1="10" x2="460" y2="188" stroke="#D3DEE9" stroke-width="12" stroke-linecap="round"/>')
rod = g(g(rod + bob(56, 6.95, .28, 8)), show(6.75, "fadeIn", .25, until=9.35))
count = g(tfa(710, 120, f'<tspan data-count="[6.95,9.1,1,25,1]">۱</tspan> ضربه', 60, ACC, 900)
          + ten(710, 164, "strokes per layer", 26, ACC), show(6.8, "popIn", until=9.4))
plate = g(f'<rect x="20" y="560" width="880" height="18" rx="4" fill="#1E3D63" stroke="{DIM}" stroke-width="3"/>', show(.15, "fadeIn", .4))
dims = (dimline(400, 162, 520, 162, "10 cm", .9, until=3.4) + dimline(660, 200, 660, 560, "30 cm", 1.1, until=3.4)
        + dimline(340, 616, 580, 616, "20 cm", 1.3, until=3.4)
        + label(190, 360, "مخروط آبرامز", "Abrams cone", INK, .8, 38, until=3.4))
meas = draw("M120,193 L560,193", 13.9, .45, "#0A2140", 18) + draw("M120,193 L560,193", 13.9, .45, "#D3DEE9", 12)
meas += dimline(460, 202, 460, 298, "", 14.35, ACC)
meas += label(705, 238, f"اسلامپ ≈ {fa(8)} سانت", "Slump ≈ 8 cm", ACC, 14.7, 40)
svg2 = defs() + plate + layers + body + cone + rod + count + dims + meas

write_reel(
    "c002", 2, "site",
    f"آزمایش اسلامپ رو چطوری انجام میدن؟", "How is a slump test done?",
    svg2, 660,
    [dict(t=.8, fa=f"مخروط رو روی یه سطح صاف و مرطوب می{ZW}ذاریم", en="Put the cone on a flat, damp base"),
     dict(t=3.6, fa=f"بتن رو در <b>{fa(3)} لایه</b> می{ZW}ریزیم", en="Fill it in 3 layers"),
     dict(t=6.6, fa=f"هر لایه رو <b>{fa(25)} بار</b> با میله می{ZW}کوبیم", en="Rod each layer 25 times"),
     dict(t=9.6, fa=f"مخروط رو صاف و آروم بالا می{ZW}کشیم (حدود {fa(5)} ثانیه)", en="Lift the cone straight up, slowly (about 5 s)"),
     dict(t=12.4, fa=f"افتِ بتن رو اندازه می{ZW}گیریم…", en="Measure how far the concrete dropped…"),
     dict(t=15.6, fa=f"این افت میشه <b>اسلامپ</b>: معیار کارایی بتن", en="That drop is the slump: a measure of workability"),
     dict(t=18.6, fa=f":warning: آب اضافه برای اسلامپ بیشتر = مقاومت کمتر", en="Extra water for more slump = lower strength")],
    21.8,
    f"""آزمایش اسلامپ (Slump Test) در ۲۰ ثانیه 🏗️

۱. مخروط آبرامز (ارتفاع ۳۰، قطر بالا ۱۰ و پایین ۲۰ سانت) رو روی یه سطح صاف و مرطوب بذار
۲. بتن رو در ۳ لایه بریز و هر لایه رو ۲۵ بار با میله{ZW}ی تراکم بکوب
۳. سطح رو صاف کن و مخروط رو آروم و صاف بالا بکش (حدود ۵ ثانیه)
۴. افت بتن نسبت به ارتفاع مخروط = اسلامپ

⚠️ سر کارگاه برای روان{ZW}تر شدن به بتن آب اضافه نکنید: نسبت آب به سیمان بالا میره و مقاومت میاد پایین.

📘 اصطلاحات:
Slump test = آزمایش اسلامپ
Workability = کارایی
Tamping rod = میله{ZW}ی تراکم
Water-cement ratio = نسبت آب به سیمان

👷 هر روز یه درس عمران | سیو کن که سر کارگاه یادت بمونه""",
    ["عمران", "مهندسی_عمران", "بتن", "کارگاه", "اجرا", "مهندس_عمران", "civilengineering", "concrete", "construction"],
    sfx=[(.3, "whoosh", .2), (3.8, "pop", .25), (4.6, "pop", .25), (5.4, "pop", .25), (9.9, "whoosh", .3), (10.6, "boop", .3),
         (12.6, "whoosh", .25), (13.9, "pop", .3), (14.7, "ding", .3), (18.6, "pop", .3)],
    cover=1.6, topic="slump test")

# ---------------------------------------------------------------- c003: quiz, span x2
def small_beam(x0, x1, top, dep, d0, t, d1=None, tb=None):
    xs = list(range(x0 + 20, x1 - 19, 40))
    s0, s1 = beam_d(x0, x1, top, dep, d0), beam_d(x0, x1, top, dep, d1 if d1 is not None else d0)
    out = draw(s0, t, .5, INK, 5, fill=CONC, style="fill-opacity:.62", inner=morph(s0, s1, tb, .9) if tb else "")
    out += pin(x0 + 10, top + dep, t + .2, .6) + roller(x1 - 10, top + dep, t + .25, .6)
    tail = "M" + " L".join(f"{x},{top - 46}" for x in xs)
    tail1 = "M" + " L".join(f"{x},{top - 46 + (sag_at(x, x0, x1, d1) - sag_at(x, x0, x1, d0) if tb else 0):.1f}" for x in xs)
    out += draw(tail, t + .3, .3, INK, 3, inner=morph(tail, tail1, tb, .9) if tb else "")
    for i, x in enumerate(xs):
        a = g(arrow(x, top - 46, x, top - 6 + sag_at(x, x0, x1, d0), INK, 4, 13), A(("dropIn", .35, t + .3 + i * .02)))
        out += g(a + (move([(0, 0), (0, sag_at(x, x0, x1, d1) - sag_at(x, x0, x1, d0))], tb, .9) if tb else ""))
    return out


TR = 2.9 + 5
svg3 = defs() + small_beam(40, 320, 60, 22, 8, .3) + g(ten(352, 82, "L", 36, INK, 700), show(.6, "fadeIn"))
svg3 += g(ten(180, 118, "δ", 32, ACC, 700), show(.7, "popIn"))
svg3 += small_beam(40, 600, 210, 22, 8, .9, 60, TR + .1) + g(ten(642, 232, "2L", 36, INK, 700), show(1.2, "fadeIn"))
svg3 += g(ten(320, 272, "?", 46, ACC, 800), show(1.2, "popIn", until=TR + .2))
svg3 += g(ten(320, 340, "16δ", 46, GREEN, 800), show(TR + .9, "popIn"))

write_quiz(
    "c003", 3,
    f"اگه دهانه{ZW}ی تیر ۲ برابر بشه، خیزش چند برابر میشه؟", "If the span doubles, how many times bigger is the deflection?",
    "تیر ساده، همون مقطع، همون بار گسترده در هر متر", "simple beam · same section · same load per metre",
    [(f"{fa(2)} برابر", "2×"), (f"{fa(4)} برابر", "4×"), (f"{fa(8)} برابر", "8×"), (f"{fa(16)} برابر", "16×")], 3,
    svg3, 370, TR, 1.6, 2.9,
    [dict(t=TR + 1.0, html=(f'<div class="panel"><div class="sfa">خیز با <b>توان چهارمِ</b> دهانه زیاد میشه</div>'
                            f'<div class="fx">δ = 5wL<sup>4</sup> / 384EI</div><div class="sen">2<sup>4</sup> = 16 → the deflection grows 16 times</div></div>')),
     dict(t=TR + 4.7, fa=f"برای همین تیرهای بلندتر رو <b>عمیق{ZW}تر</b> می{ZW}گیرن", en="That's why longer spans need deeper beams")],
    TR + 7.9,
    f"""تست امروز 🧠 اگه دهانه{ZW}ی یه تیر ساده ۲ برابر بشه (همون مقطع و همون بار گسترده در هر متر)، خیزش چند برابر میشه؟

اول جوابتو کامنت کن، بعد ویدیو رو تا آخر ببین 👀 جواب و دلیلش آخرِ ویدیوئه.

📘 اصطلاحات:
Deflection = خیز
Span = دهانه
Uniformly distributed load = بار گسترده{ZW}ی یکنواخت
Moment of inertia = ممان اینرسی

👷 هر روز یه درس عمران | این تست رو برای همکلاسیت بفرست""",
    ["عمران", "مهندسی_عمران", "تحلیل_سازه", "مقاومت_مصالح", "کنکور_ارشد_عمران", "دانشجوی_عمران", "civilengineering", "structuralanalysis"],
    sfx=[(.3, "whoosh", .2), (1.6, "pop", .2), (1.78, "pop", .2), (1.96, "pop", .2), (2.14, "pop", .2), (TR + .1, "whoosh", .25),
         (TR + 1.0, "pop", .3), (TR + 4.7, "pop", .3)],
    cover=2.6, topic="deflection vs span")
