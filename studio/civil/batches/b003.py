"""Batch 3: c005 process: excavating next to a building with soil nailing (excavator digs lift by lift,
nails drilled and grouted, mesh + shotcrete, repeat; the nailed soil acts as one block).
"""
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from kit import *  # noqa: F401,F403

GY, FACE, EDGE = 260, 300, 640            # ground, excavation face, far edge of the pit
LIFTS = [(260, 370), (370, 480), (480, 590)]
P0, LB, LS = (770.0, 180.0), 320.0, 260.0  # boom pivot, boom and stick lengths


def ik(tx, ty):
    """Boom / stick rotations (deg) that put the bucket pin at (tx, ty); elbow up."""
    dx, dy = tx - P0[0], ty - P0[1]
    d = min(max(math.hypot(dx, dy), abs(LB - LS) + 1), LB + LS - 1)
    base, a = math.atan2(dy, dx), math.acos((LB * LB + d * d - LS * LS) / (2 * LB * d))
    sols = []
    for sg in (-1, 1):
        bd = base + sg * a
        sols.append((P0[1] + LB * math.sin(bd), bd))
    bd = min(sols)[1]
    p1 = (P0[0] + LB * math.cos(bd), P0[1] + LB * math.sin(bd))
    sd = math.atan2(ty - p1[1], tx - p1[0])
    phib = math.degrees(bd) - 180
    return phib, math.degrees(sd) - 90 - phib


def unwrap(vals):
    out = [vals[0]]
    for v in vals[1:]:
        while v - out[-1] > 180: v -= 360
        while v - out[-1] < -180: v += 360
        out.append(v)
    return out


def arm_anim(frames, total):
    """frames [(t, (x, y))] -> SMIL rotations for the boom (about P0) and the stick (about the boom tip)."""
    angs = [ik(*p) for _, p in frames]
    b, s = unwrap([a for a, _ in angs]), unwrap([a for _, a in angs])
    kt = ";".join(f"{t / total:.5f}" for t, _ in frames)
    ks = ";".join([".42 0 .58 1"] * (len(frames) - 1))
    mk = lambda vals, cx, cy: (f'<animateTransform attributeName="transform" type="rotate" begin="0s" dur="{total:g}s" fill="freeze" '
                               f'values="{";".join(f"{v:.2f} {cx:g} {cy:g}" for v in vals)}" keyTimes="{kt}" calcMode="spline" keySplines="{ks}"/>')
    return b[0], s[0], mk(b, *P0), mk(s, P0[0] - LB, P0[1])


# ---------------------------------------------------------------- timeline
REST = (600, 236)
DIG = [(2.7, 1), (9.8, 2), (13.9, 3)]          # (start, lift)
NAIL = [5.4, 12.45, 16.55]
SHOT = [7.6, 13.2, 17.3]
frames = [(0, REST)]
scoop_t = []
for t0, k in DIG:
    top, bot = LIFTS[k - 1]
    frames.append((t0, REST))
    t = t0
    for xr in (560, 440, 330):                  # three scoops, each closer to the face
        frames += [(t + .3, (xr, bot - 36)), (t + .62, (min(xr + 120, 600), bot - 44)), (t + .85, (600, 170))]
        scoop_t.append(t + .62)
        t += .85
    frames.append((t + .3, REST))
TOTAL = 23.6
frames.append((TOTAL, REST))
b0, s0, banim, sanim = arm_anim(frames, TOTAL)

# ---------------------------------------------------------------- scene
scene = (f'<rect x="0" y="{GY}" width="{FACE}" height="390" fill="url(#clay)"/>'
         f'<rect x="{EDGE}" y="{GY}" width="{920 - EDGE}" height="390" fill="url(#clay)"/>'
         f'<rect x="{FACE}" y="590" width="{EDGE - FACE}" height="60" fill="url(#clay)"/>'
         f'<line x1="0" y1="{GY}" x2="{FACE}" y2="{GY}" stroke="#9BD27A" stroke-width="6"/>'
         f'<line x1="{EDGE}" y1="{GY}" x2="920" y2="{GY}" stroke="#9BD27A" stroke-width="6"/>')
clips = ""
for k, (top, bot) in enumerate(LIFTS):
    t0 = DIG[k][0]
    w = EDGE - FACE
    vals = f"{w};{w * .68:.0f};{w * .68:.0f};{w * .33:.0f};{w * .33:.0f};0"
    kts = "0;.24;.35;.6;.7;1"
    clips += (f'<clipPath id="lift{k}"><rect x="{FACE}" y="{top - 4}" width="{w}" height="{bot - top + 4}">'
              f'<animate attributeName="width" begin="{t0 + .4:g}s" dur="{2.3:g}s" fill="freeze" values="{vals}" keyTimes="{kts}" calcMode="linear"/>'
              f'</rect></clipPath>')
    scene += f'<rect x="{FACE}" y="{top}" width="{w}" height="{bot - top}" fill="url(#clay)" clip-path="url(#lift{k})"/>'
    if k == 0:
        scene += (f'<line x1="{FACE}" y1="{GY}" x2="{EDGE}" y2="{GY}" stroke="#9BD27A" stroke-width="6" clip-path="url(#lift0)"/>')
scene = f"<defs>{clips}</defs>" + g(scene, show(0, "fadeIn", .4))

# neighbouring building on the left
bld = (f'<rect x="24" y="112" width="214" height="148" fill="#1D3B60" stroke="{INK}" stroke-width="4"/>'
       f'<path d="M14,112 L248,112" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>'
       f'<rect x="20" y="258" width="222" height="16" fill="#6D7C8C" stroke="{INK}" stroke-width="3"/>')
for r in range(2):
    for c in range(4):
        bld += f'<rect x="{44 + c * 50}" y="{130 + r * 58}" width="30" height="36" rx="3" fill="#FFE58A" opacity=".85"/>'
bld = g(bld, show(.1, "fadeIn", .4)) + label(131, 72, f"ساختمون همسایه", "Neighbouring building", INK, .5, 32, until=4.0)

# excavator on the far side, facing the pit
exc = (f'<rect x="650" y="{GY - 32}" width="232" height="32" rx="16" fill="#2E3B4E" stroke="{DARK}" stroke-width="4"/>'
       + "".join(f'<circle cx="{x}" cy="{GY - 16}" r="10" fill="#55667A" stroke="{DARK}" stroke-width="2"/>' for x in (670, 712, 754, 796, 838, 864))
       + f'<rect x="680" y="170" width="190" height="58" rx="6" fill="{YEL}" stroke="{DARK}" stroke-width="4"/>'
       f'<rect x="832" y="178" width="56" height="48" rx="8" fill="{YEL2}" stroke="{DARK}" stroke-width="4"/>'
       f'<path d="M690,170 L690,112 L742,112 L758,140 L758,170 Z" fill="{YEL}" stroke="{DARK}" stroke-width="4" stroke-linejoin="round"/>'
       f'<path d="M698,120 L738,120 L750,142 L698,142 Z" fill="#9FD3FF" stroke="{DARK}" stroke-width="3" stroke-linejoin="round"/>')
px1 = P0[0] - LB
stick = (f'<path d="M{px1 - 7},{P0[1]} L{px1 + 7},{P0[1]} L{px1 + 5},{P0[1] + LS} L{px1 - 5},{P0[1] + LS} Z" fill="{YEL2}" stroke="{DARK}" stroke-width="4" stroke-linejoin="round"/>'
         f'<path d="M{px1 - 12},{P0[1] + LS - 8} Q{px1 + 30},{P0[1] + LS - 4} {px1 + 22},{P0[1] + LS + 30} L{px1 - 10},{P0[1] + LS + 32} Z" fill="#3A4A5E" stroke="{DARK}" stroke-width="4" stroke-linejoin="round"/>'
         f'<circle cx="{px1}" cy="{P0[1]}" r="7" fill="{STEEL}" stroke="{DARK}" stroke-width="3"/>')
boom = (f'<path d="M{P0[0]},{P0[1] - 13} C{P0[0] - 90},{P0[1] - 40} {px1 + 80},{P0[1] - 30} {px1},{P0[1] - 8} L{px1},{P0[1] + 8} '
        f'C{px1 + 80},{P0[1] - 12} {P0[0] - 90},{P0[1] - 16} {P0[0]},{P0[1] + 13} Z" fill="{YEL}" stroke="{DARK}" stroke-width="4" stroke-linejoin="round"/>')
arm = (f'<g transform="rotate({b0:.2f} {P0[0]:g} {P0[1]:g})">{banim}{boom}'
       f'<g transform="rotate({s0:.2f} {px1:g} {P0[1]:g})">{sanim}{stick}</g></g>')
exc = g(exc + arm + f'<circle cx="{P0[0]}" cy="{P0[1]}" r="9" fill="{STEEL}" stroke="{DARK}" stroke-width="3"/>', show(.2, "fadeIn", .4))
exc += label(820, 62, "بیل مکانیکی", "Excavator", "#FFE58A", .7, 32, until=4.0)

# nails, grout, shotcrete for each lift
work = ""
for k, (top, bot) in enumerate(LIFTS):
    yn, tn, ts = bot - 55, NAIL[k], SHOT[k]
    ex, ey = FACE - 230 * math.cos(math.radians(15)), yn + 230 * math.sin(math.radians(15))
    d = f"M{FACE},{yn} L{ex:.1f},{ey:.1f}"
    work += draw(d, tn + .55, .25, "#C9D3DC", 16, style="opacity:.75")                 # grout column
    work += draw(d, tn, .6, "#E7EEF5", 5)                                               # steel bar
    work += (f'<rect x="{FACE}" y="{top}" width="14" height="{bot - top}" fill="#AEB8C2" stroke="{INK}" stroke-width="3" class="gd" '
             f'style="{A(("growUp", .6, ts, "ease-out"))}"/>')
    work += g(f'<rect x="{FACE + 8}" y="{yn - 13}" width="10" height="26" rx="2" fill="{STEEL}" stroke="{DARK}" stroke-width="2"/>', show(tn + .6))
work += label(470, 300, f"میخ (نیل) + دوغاب", "Soil nail + grout", "#E7EEF5", NAIL[0] + .5, 34, until=7.5)
work += g(arrow(372, 318, 318, 318, "#E7EEF5", 4, 14), show(NAIL[0] + .6, "fadeIn", until=7.5))
work += label(470, 300, f"مش + شاتکریت", "Mesh + shotcrete", "#D7DEE6", SHOT[0] + .2, 34, until=9.7)
work += g(arrow(384, 318, 316, 318, "#D7DEE6", 4, 14), show(SHOT[0] + .3, "fadeIn", until=9.7))
work += dimline(610, GY, 610, 370, f"{fa(1)} تا {fa(2)} متر", 3.2, ACC, size=28, fa_text=True, until=5.7)
zone = (f'<path d="M{FACE},{GY + 4} L60,{GY + 4} L60,612 L{FACE},590 Z" fill="rgba(46,229,157,.16)" stroke="{GREEN}" '
        f'stroke-width="4" stroke-dasharray="14 10"/>')
work += g(zone, show(18.2, "fadeIn", .5))
work += label(180, 470, f"خاک یکپارچه{ZW}شده", "One nailed soil block", GREEN, 18.6, 34)
work += label(470, 470, f"گود پایدار", "Stable excavation", "#BDF5DD", 19.2, 36)
svg5 = defs() + soil_defs() + '<g transform="translate(0,70)">' + scene + bld + work + exc + "</g>"

dig_sfx = [(t, "boop", .25) for t in scoop_t]
write_reel(
    "c005", 5, "process",
    f"چرا گود کنار ساختمون ریزش نمی{ZW}کنه؟", "Why doesn't a deep pit next to a building collapse?",
    svg5, 720,
    [dict(t=.6, fa=f"کنار یه ساختمون می{ZW}خوایم گود عمیق بکنیم", en="We need a deep pit right next to a building"),
     dict(t=2.6, fa=f"اول فقط {fa(1)} تا {fa(2)} متر خاکبرداری می{ZW}کنیم", en="First, dig only 1–2 m"),
     dict(t=5.2, fa=f"میخ{ZW}ها رو مایل توی خاک می{ZW}کاریم و دوغاب می{ZW}زنیم", en="Drill in inclined soil nails and grout them"),
     dict(t=7.4, fa=f"روی دیواره مش می{ZW}بندیم و شاتکریت می{ZW}زنیم", en="Fix mesh on the face and spray shotcrete"),
     dict(t=9.6, fa=f"و همین{ZW}طور مرحله به مرحله می{ZW}ریم پایین", en="Then repeat, lift by lift, going down"),
     dict(t=18.0, fa=f"میخ{ZW}ها خاک پشت دیواره رو یکپارچه نگه می{ZW}دارن", en="The nails bind the soil into one block"),
     dict(t=20.6, fa=f":warning: اول کل گود رو خالی نکنید؛ گام{ZW}به{ZW}گام!", en="Never dig the full depth first: step by step!")],
    TOTAL,
    f"""گودبرداری کنار ساختمون چطوری ایمن انجام میشه؟ 🏗️ (روش میخ{ZW}کوبی / نیلینگ)

۱. هر بار فقط یه مرحله{ZW}ی کم{ZW}عمق خاکبرداری میشه (معمولاً ۱ تا ۲ متر)
۲. میخ{ZW}ها با زاویه{ZW}ی رو به پایین (معمولاً حدود ۱۵ درجه) حفاری و کار گذاشته میشن و دوغاب تزریق میشه
۳. روی دیواره مش بسته میشه و شاتکریت اجرا میشه
۴. همین مراحل تا رسیدن به کف گود تکرار میشه

میخ{ZW}ها خاکِ پشت دیواره رو به یه بلوک یکپارچه تبدیل می{ZW}کنن که خودش پایدار می{ZW}مونه.

⚠️ خاکبرداری کل عمق قبل از اجرای سازه{ZW}ی نگهبان یکی از دلایل اصلی ریزش گودهاست.

📘 اصطلاحات:
Soil nailing = میخ{ZW}کوبی (نیلینگ)
Shotcrete = بتن پاششی (شاتکریت)
Grout = دوغاب
Excavation = گودبرداری

👷 هر روز یه درس عمران | برای همکارت بفرست""",
    ["عمران", "مهندسی_عمران", "ژئوتکنیک", "گودبرداری", "نیلینگ", "سازه_نگهبان", "civilengineering", "geotechnicalengineering", "soilnailing", "excavation"],
    sfx=[(.2, "rumble", .5)] + dig_sfx
        + [(t, "drill", .4) for t in NAIL] + [(t, "spray", .45) for t in SHOT]
        + [(18.2, "pop", .3), (19.2, "ding", .3), (20.6, "pop", .3)],
    cover=8.4, topic="soil nailing excavation")
