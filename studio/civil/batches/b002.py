"""Batch 2: schematic process reels (owner's request, 15 Nov 2026: "machines doing the work").
c004 process: pile driving (rig drives in, raises the leader, drives a precast pile; skin friction + end bearing)
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from kit import *  # noqa: F401,F403

# ---------------------------------------------------------------- c004: pile driving
GY = 380                                   # ground level
T_IN, D_IN, T_UP, T_PILE, T_DRIVE, T_DIM = .4, 1.9, 2.6, 4.2, 6.0, 14.2

ground = (f'<rect x="0" y="{GY}" width="920" height="220" fill="url(#clay)"/>'
          f'<rect x="0" y="600" width="920" height="190" fill="url(#sand)"/>'
          f'<line x1="0" y1="600" x2="920" y2="600" stroke="#2B1F16" stroke-width="3" stroke-dasharray="14 10"/>'
          f'<line x1="0" y1="{GY}" x2="920" y2="{GY}" stroke="#9BD27A" stroke-width="6"/>')
ground = g(ground, show(0, "fadeIn", .4))
ground += label(790, 480, "رس نرم", "Soft clay", "#F0DCC2", .7, 38)
ground += label(780, 690, f"ماسه{ZW}ی متراکم", "Dense sand", "#F6E6BC", .9, 38)

# truck-mounted rig, drawn in its working position; it arrives from the left
body = (f'<rect x="440" y="318" width="322" height="28" rx="6" fill="{YEL}" stroke="{DARK}" stroke-width="4"/>'
        f'<rect x="440" y="288" width="92" height="32" rx="4" fill="{YEL2}" stroke="{DARK}" stroke-width="4"/>'
        f'<rect x="556" y="284" width="112" height="36" rx="5" fill="{YEL2}" stroke="{DARK}" stroke-width="4"/>'
        f'<path d="M574,296 h76 M574,308 h76" stroke="{DARK}" stroke-width="3" opacity=".5"/>'
        f'<path d="M676,318 L676,246 L738,246 L764,284 L764,318 Z" fill="{YEL}" stroke="{DARK}" stroke-width="4" stroke-linejoin="round"/>'
        f'<path d="M688,256 L732,256 L751,284 L688,284 Z" fill="#9FD3FF" stroke="{DARK}" stroke-width="3" stroke-linejoin="round"/>'
        f'<rect x="756" y="300" width="12" height="10" rx="2" fill="#FFF3B0" stroke="{DARK}" stroke-width="2"/>')
body += "".join(wheel(cx, 355, 25, T_IN, D_IN, -3) for cx in (482, 548, 718))
lead = (f'<rect x="446" y="10" width="20" height="280" fill="url(#lattice)" stroke="{DARK}" stroke-width="4"/>'
        f'<rect x="439" y="2" width="34" height="14" rx="3" fill="{STEEL}" stroke="{DARK}" stroke-width="3"/>')
lead = f'<g transform="rotate(-90 456 290)">{lead}{turn(456, 290, -90, 0, T_UP, 1.2)}</g>'
rig = g(g(body + lead + move([(-720, 0), (0, 0)], T_IN, D_IN, ".2 .8 .2 1")), A(dim(T_DIM)))
rig += label(560, 150, f"دکل (لیدر)", "Leader", "#C9D8E8", 3.6, 32, until=5.9)

# blows: (period, penetration). Soft clay: easy; dense sand: little per blow.
blows = [(.30, 20.0)] * 11 + [(.45, 8.0)] * 10
pile_k, ham_k, impacts, s, y = [(0, (0, 0))], [(0, (0, 0))], [], 0.0, 0.0
for p, pen in blows:
    hit = s + .8 * p
    ham_k += [(s, (0, y)), (s + .5 * p, (0, y - 46)), (hit, (0, y))]
    pile_k += [(hit, (0, y))]
    y += pen
    pile_k += [(hit + .04, (0, y))]
    ham_k += [(hit + .04, (0, y))]
    impacts.append(T_DRIVE + hit)
    s += p
ham_k = [k for i, k in enumerate(ham_k) if i == 0 or k[0] > 0]
pile = (f'<rect x="415" y="80" width="30" height="300" fill="url(#agg)" stroke="{INK}" stroke-width="4"/>'
        f'<path d="M415,380 L445,380 L430,396 Z" fill="{STEEL}" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>')
pile = g(g(pile, A(("dropIn", .6, T_PILE))) + keyed("translate", pile_k, T_DRIVE))
hammer = (f'<rect x="403" y="26" width="54" height="54" rx="5" fill="{ORANGE}" stroke="{DARK}" stroke-width="4"/>'
          f'<path d="M403,44 h54 M403,62 h54" stroke="{DARK}" stroke-width="3"/>')
hammer = g(g(g(hammer, A(("dropIn", .5, T_PILE + .35))) + keyed("translate", ham_k, T_DRIVE)), A(dim(T_DIM)))
lab = label(285, 230, "شمع بتنی", "Concrete pile", INK, T_PILE + .4, 36, until=T_DRIVE + 1.2)
lab += label(290, 64, "چکش", "Hammer", "#FFC27A", T_PILE + .7, 36, until=T_DRIVE + 1.2)
flash = ""
yk = 0.0
for i, (p, pen) in enumerate(blows):
    yk += pen
    yy = 80 + yk
    burst = "".join(f'<line x1="{430 + 20 * dx:g}" y1="{yy + 8 * dy:g}" x2="{430 + 42 * dx:g}" y2="{yy + 18 * dy:g}" stroke="#FFF3B0" stroke-width="5" stroke-linecap="round"/>'
                    for dx, dy in ((-1, -.6), (-1, .4), (1, -.6), (1, .4)))
    flash += g(burst, A(("flash", .22, impacts[i] - .02, "ease-out")), "tb")
counter = g(tfa(745, 118, f'<tspan {steps_count([(t, i + 1) for i, t in enumerate(impacts)])}>۰</tspan> ضربه', 60, ACC, 900)
            + ten(745, 160, "blows", 28, ACC), show(T_DRIVE - .2, "popIn", until=T_DIM + .2))

# after driving: how the load goes down
xs_f = range(440, 661, 55)
fr = "".join(harrow(397, y0 + 20, 397, y0 - 20, BLUE, 5, 16) + harrow(463, y0 + 20, 463, y0 - 20, BLUE, 5, 16) for y0 in xs_f)
load = g(harrow(430, 232, 430, 368, INK, 10, 30), show(T_DIM + .3, "dropIn", .45))
load += label(250, 290, "بار ساختمون", "Building load", INK, T_DIM + .45, 36)
load += g(fr, show(15.7))
load += label(235, 520, f"اصطکاک جداری", "Skin friction", BLUE, 15.95, 36)
load += g(harrow(430, 772, 430, 708, GREEN, 10, 28), show(17.3))
load += label(232, 728, f"باربری نوک", "End bearing", GREEN, 17.5, 36)
svg4 = defs() + soil_defs() + ground + rig + pile + hammer + flash + lab + counter + load

write_reel(
    "c004", 4, "process",
    f"شمع{ZW}کوبی چطوری انجام میشه؟", "How is a pile driven?",
    svg4, 790,
    [dict(t=.8, fa=f"دستگاه شمع{ZW}کوب میاد سر جاش", en="The piling rig drives into position"),
     dict(t=T_UP, fa=f"دکل (لیدر) رو عمودی می{ZW}کنه", en="It raises the leader upright"),
     dict(t=T_PILE, fa=f"شمع بتنی پیش{ZW}ساخته میره زیر چکش", en="A precast concrete pile goes under the hammer"),
     dict(t=T_DRIVE, fa=f"چکش، شمع رو ضربه{ZW}به{ZW}ضربه می{ZW}کوبه توی زمین", en="The hammer drives the pile in, blow by blow"),
     dict(t=T_DRIVE + 3.3, fa=f"توی لایه{ZW}ی محکم، هر ضربه کمتر فرو می{ZW}ره", en="In firm ground each blow drives it less"),
     dict(t=T_DIM, fa=f"بار ساختمون از دو راه به زمین می{ZW}رسه:", en="The building load reaches the ground two ways:"),
     dict(t=15.6, fa=f"{fa(1)}. اصطکاکِ بدنه{ZW}ی شمع با خاک", en="1. Friction along the pile shaft"),
     dict(t=17.2, fa=f"{fa(2)}. باربری نوکِ شمع روی لایه{ZW}ی محکم", en="2. End bearing at the pile tip"),
     dict(t=19.2, fa=f":light_bulb: شمع بار رو از خاک سست می{ZW}بره به لایه{ZW}ی محکم",
          en="Piles carry loads down to firm ground")],
    22.6,
    f"""شمع{ZW}کوبی چطوری انجام میشه؟ 🏗️

وقتی لایه{ZW}های بالایی خاک سست باشن، بار ساختمون رو با شمع به لایه{ZW}های محکم{ZW}ترِ پایین می{ZW}رسونن.

۱. دستگاه شمع{ZW}کوب مستقر میشه و دکل (لیدر) رو عمودی می{ZW}کنه
۲. شمع بتنی پیش{ZW}ساخته زیر چکش قرار می{ZW}گیره
۳. چکش شمع رو ضربه به ضربه می{ZW}کوبه. هرچی خاک محکم{ZW}تر باشه، شمع با هر ضربه کمتر فرو میره؛ برای همین تعداد ضربه{ZW}ها رو ثبت می{ZW}کنن تا معلوم بشه شمع به لایه{ZW}ی مقاوم رسیده
۴. بار از دو راه به زمین می{ZW}رسه: اصطکاک جداری (بدنه{ZW}ی شمع با خاک) و باربری نوک

📘 اصطلاحات:
Pile driving = شمع{ZW}کوبی
Leader = دکل راهنما (لیدر)
Skin friction = اصطکاک جداری
End bearing = باربری نوک

👷 هر روز یه درس عمران | فالو کن و برای همکارت بفرست""",
    ["عمران", "مهندسی_عمران", "ژئوتکنیک", "شمع", "پی", "مهندس_عمران", "civilengineering", "geotechnicalengineering", "piledriving", "construction"],
    sfx=[(T_IN, "rumble", .55), (T_UP, "whoosh", .25), (T_PILE, "whoosh", .2), (T_PILE + .4, "pop", .25)]
        + [(t, "thud", .55 if i < 11 else .62) for i, t in enumerate(impacts)]
        + [(T_DIM + .3, "whoosh", .25), (15.7, "pop", .3), (17.3, "pop", .3), (19.2, "ding", .3)],
    cover=7.0, topic="pile driving")
