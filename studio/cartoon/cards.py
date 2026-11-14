"""Rostam-style overlays for a cartoon series: part header (every frame), title card and end card.
Same look as studio/rostam/render.py (fonts from studio/rostam/fonts). Names come from <series>/parts.json.
python3 cards.py <series> <part> <outdir>   -> header.png, title.png, end.png (assemble.py calls make())"""
import os, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import series

HERE = os.path.dirname(os.path.abspath(__file__))
FD = os.path.join(HERE, "..", "rostam", "fonts")
EN = f"{FD}/EBGaramond[wght].ttf"
TI = f"{FD}/Cinzel[wght].ttf"
FA = f"{FD}/Vazirmatn-Medium.ttf"
FAB = f"{FD}/Vazirmatn-Bold.ttf"
VE = f"{FD}/Amiri-Bold.ttf"
GOLD, VGOLD, CREAM = (236, 200, 122), (246, 216, 142), (246, 236, 214)
RTL = {"direction": "rtl", "language": "fa"}
FA_DIGITS = str.maketrans("0123456789", "۰۱۲۳۴۵۶۷۸۹")
W, H = 1080, 1920


def names():
    c = series.config()
    return c["series_en"].upper(), c["series_fa"]


def fit(path, size, text, maxw, wght=None, **kw):
    while size > 30 and font(path, size, wght).getlength(text, **kw) > maxw:
        size -= 4
    return font(path, size, wght)


def font(path, size, wght=None):
    f = ImageFont.truetype(path, size)
    if wght:
        try:
            f.set_variation_by_axes([wght])
        except Exception:
            pass
    return f


def title_card(n, en_title, fa_title):
    im = Image.new("RGBA", (W, H), (0, 0, 0, 120))
    d = ImageDraw.Draw(im)
    sen, sfa = names()
    d.text((W / 2, 690), sen, font=fit(TI, 74, sen, W - 140, 700), fill=GOLD + (255,), anchor="mm")
    d.text((W / 2, 830), sfa, font=fit(VE, 128, sfa, W - 160, None, **RTL), fill=VGOLD + (255,), anchor="mm", **RTL)
    d.line([(W / 2 - 200, 950), (W / 2 + 200, 950)], fill=GOLD + (180,), width=2)
    pt = f"PART {n}  ·  {en_title.upper()}"
    d.text((W / 2, 1015), pt, font=fit(TI, 40, pt, W - 140, 600), fill=CREAM + (255,), anchor="mm")
    d.text((W / 2, 1090), f"قسمت {str(n).translate(FA_DIGITS)}  ·  {fa_title}", font=font(FA, 46), fill=CREAM + (255,), anchor="mm", **RTL)
    return im


def end_card(en_next, fa_next, handle="@english_dya", kind="part"):
    """kind "part": NEXT PART · title; "story": the series is over, NEXT STORY · next series; "end": THE END."""
    im = Image.new("RGBA", (W, H), (0, 0, 0, 150))
    d = ImageDraw.Draw(im)
    if kind in ("part", "story") and en_next:
        label = "NEXT PART" if kind == "part" else "NEXT STORY"
        d.text((W / 2, 420), label, font=font(TI, 38, 600), fill=CREAM + (255,), anchor="mm")
        d.text((W / 2, 510), en_next.upper(), font=fit(TI, 88, en_next.upper(), W - 120, 700), fill=GOLD + (255,), anchor="mm")
        fa = f"قسمت بعد: {fa_next}" if kind == "part" else f"داستان بعدی: {fa_next}"
        d.text((W / 2, 610), fa, font=fit(FAB, 50, fa, W - 140, None, **RTL), fill=VGOLD + (255,), anchor="mm", **RTL)
        line = "برای دیدن بقیه فالو کن" if kind == "part" else "فالو کن که از دستش ندی"
        line_en = "Follow to see the rest" if kind == "part" else "Follow so you don't miss it"
    else:
        d.text((W / 2, 510), "THE END", font=font(TI, 88, 700), fill=GOLD + (255,), anchor="mm")
        fa = f"پایان داستان {names()[1]}"
        d.text((W / 2, 610), fa, font=fit(FAB, 50, fa, W - 140, None, **RTL), fill=VGOLD + (255,), anchor="mm", **RTL)
        line = "برای داستان‌های بعدی فالو کن"; line_en = "Follow for more stories"
    d.line([(W / 2 - 200, 690), (W / 2 + 200, 690)], fill=GOLD + (180,), width=2)
    d.text((W / 2, 790), line, font=font(FAB, 66), fill=(255, 255, 255, 255), anchor="mm", **RTL)
    d.text((W / 2, 870), line_en, font=font(EN, 48, 500), fill=CREAM + (255,), anchor="mm")
    bw, bh, by = 400, 100, 980
    d.rounded_rectangle([(W - bw) / 2, by - bh / 2, (W + bw) / 2, by + bh / 2], radius=50, fill=GOLD + (255,))
    d.text((W / 2, by), "+ FOLLOW", font=font(TI, 42, 800), fill=(24, 18, 10, 255), anchor="mm")
    if handle:
        d.text((W / 2, 1095), handle, font=font(FA, 46), fill=CREAM + (255,), anchor="mm")
    return im


def part_header(n):
    """Top line on every frame: «قسمت N از داستان …» (full-frame PNG, transparent below)."""
    txt = f"قسمت {str(n).translate(FA_DIGITS)} از داستان {names()[1]}"
    f = font(FAB, 46)
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    y = 218
    tw = f.getlength(txt, **RTL)
    d.text((W / 2, y), txt, font=f, fill=CREAM + (255,), anchor="mm", **RTL)
    for sgn in (-1, 1):
        d.regular_polygon((W / 2 + sgn * (tw / 2 + 30), y + 4, 7), 4, fill=GOLD + (235,))
    a = im.getchannel("A").filter(ImageFilter.GaussianBlur(8))
    out = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    out.putalpha(a.point(lambda v: min(200, int(v * 1.8))))
    out.alpha_composite(im)
    return out


def make(n, outdir):
    """header.png, title.png and end.png for part n of the current series"""
    c = series.config()
    os.makedirs(outdir, exist_ok=True)
    fa, en = c["titles"][str(n)]
    part_header(n).save(f"{outdir}/header.png")
    title_card(n, en, fa).save(f"{outdir}/title.png")
    if str(n + 1) in c["titles"]:
        nfa, nen = c["titles"][str(n + 1)]
        end_card(nen, nfa, kind="part").save(f"{outdir}/end.png")
    else:
        q = series.queue()["order"]; i = q.index(os.environ["SERIES"])
        if i + 1 < len(q):
            nc = series.config(q[i + 1])
            end_card(nc["series_en"], nc["series_fa"], kind="story").save(f"{outdir}/end.png")
        else:
            end_card(None, None, kind="end").save(f"{outdir}/end.png")
    return outdir


if __name__ == "__main__":
    series.from_argv()
    print("cards ok", make(int(sys.argv[1]), sys.argv[2]))
