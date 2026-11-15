"""Render a 9:16 episode from script.json + audio/timeline.json + scene images.

usage:
  python3 -I render.py full    <ep_dir> <images_dir> <out.mp4>
  python3 -I render.py preview <ep_dir> <images_dir> <out.mp4> <t0:t1> [<t0:t1> ...]
  python3 -I render.py still   <ep_dir> <images_dir> <out.jpg> <t>
Images are looked up as <images_dir>/<SCENE_ID>.(jpg|jpeg|png|webp); a missing
image gets a labelled placeholder so layout and timing can be checked first.
"""
import importlib, json, math, os, random, subprocess, sys
from multiprocessing import Pool
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
try:
    import anim
except ImportError:
    anim = None

W, H, FPS = 1080, 1920, 30
S = 1.12                      # source oversize for the slow camera move
FD = os.path.join(HERE, "fonts")
EN = f"{FD}/EBGaramond[wght].ttf"
TI = f"{FD}/Cinzel[wght].ttf"
FA = f"{FD}/Vazirmatn-Medium.ttf"
FAB = f"{FD}/Vazirmatn-Bold.ttf"
VE = f"{FD}/Amiri-Bold.ttf"
GOLD = (236, 200, 122)
VGOLD = (246, 216, 142)
CREAM = (246, 236, 214)
RTL = {"direction": "rtl", "language": "fa"}
ROLE_FA = {"ROSTAM": "رستم", "SOHRAB": "سهراب", "TAHMINEH": "تهمینه",
           "KING_SAMANGAN": "شاه سمنگان", "KAVUS": "کاووس", "GORDAFARID": "گردآفرید",
           "HOJIR": "هجیر", "AFRASIAB": "افراسیاب", "HOOMAN": "هومان", "GUDARZ": "گودرز",
           "ZHENDEH": "ژنده‌رزم", "RIDER": "سوار تورانی", "RIDER2": "سوار تورانی",
           "HERDSMAN": "گله‌بان پیر", "GUARD": "نگهبان", "MAID": "ندیمه", "MOBED": "موبد"}
ROLE_EN = {"KING_SAMANGAN": "KING OF SAMANGAN", "RIDER": "TURANIAN RIDER",
           "RIDER2": "TURANIAN RIDER", "ZHENDEH": "ZHENDEH RAZM", "HERDSMAN": "OLD HERDSMAN"}
FA_DIGITS = str.maketrans("0123456789", "۰۱۲۳۴۵۶۷۸۹")


def font(path, size, wght=None):
    f = ImageFont.truetype(path, size)
    if wght:
        try:
            f.set_variation_by_axes([wght])
        except Exception:
            pass
    return f


def _greedy(text, f, maxw, kw):
    lines, cur = [], ""
    for w in text.split():
        cand = (cur + " " + w).strip()
        if not cur or f.getlength(cand, **kw) <= maxw:
            cur = cand
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


PUNCT = tuple(".,;:!?،؛…")
WEAK = {"و", "به", "از", "را", "که", "در", "با", "تا", "a", "an", "the", "to", "and", "of",
        "in", "on", "at", "or", "his", "her", "my"}


def wrap(text, f, maxw, rtl=False):
    """Fewest lines that fit maxw; two-line breaks prefer punctuation and balance."""
    kw = RTL if rtl else {}
    n = len(_greedy(text, f, maxw, kw))
    words = text.split()
    if n == 2:
        best = None
        for i in range(1, len(words)):
            a, b = " ".join(words[:i]), " ".join(words[i:])
            wa, wb = f.getlength(a, **kw), f.getlength(b, **kw)
            if max(wa, wb) > maxw:
                continue
            score = max(wa, wb)
            if words[i - 1].endswith(PUNCT):
                score -= maxw * 0.25
            elif words[i - 1].lower() in WEAK:
                score += maxw * 0.2
            if best is None or score < best[0]:
                best = (score, [a, b])
        if best:
            return best[1]
    lo, hi = maxw * 0.4, maxw
    for _ in range(14):
        mid = (lo + hi) / 2
        if len(_greedy(text, f, mid, kw)) <= n:
            hi = mid
        else:
            lo = mid
    return _greedy(text, f, hi, kw)


# ---------- overlays ----------
F_EN = font(EN, 50, 500)
F_FA = font(FA, 41)
F_LAB = font(TI, 30, 700)
F_LABFA = font(FAB, 30)


def subtitle(role, en, fa):
    """Film-style subtitle: no box, soft shadow; speaker named only for dialogue."""
    text = subtitle_text(role, en, fa)
    a = text.getchannel("A").filter(ImageFilter.GaussianBlur(7))
    shadow = Image.new("RGBA", text.size, (0, 0, 0, 0))
    shadow.putalpha(a.point(lambda v: min(255, int(v * 1.6))))
    shadow.alpha_composite(text)
    return shadow


def subtitle_text(role, en, fa):
    en_l = wrap(en, F_EN, 880)
    fa_l = wrap(fa, F_FA, 880, rtl=True)
    lab = 54 if role != "NARRATOR" else 0
    pad = 22
    h = pad + lab + len(en_l) * 62 + 16 + len(fa_l) * 66 + pad
    im = Image.new("RGBA", (W, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    y = pad
    if lab:
        a_txt, b_txt = ROLE_EN.get(role, role), ROLE_FA.get(role, "")
        a = F_LAB.getlength(a_txt)
        b = F_LABFA.getlength(b_txt, **RTL)
        gap = 44
        x0 = (W - (a + gap + b)) / 2
        d.text((x0, y + 8), a_txt, font=F_LAB, fill=GOLD + (255,))
        d.ellipse([x0 + a + gap / 2 - 4, y + 22, x0 + a + gap / 2 + 4, y + 30], fill=GOLD + (255,))
        d.text((x0 + a + gap, y + 2), b_txt, font=F_LABFA, fill=GOLD + (255,), **RTL)
        y += lab
    for ln in en_l:
        d.text((W / 2, y), ln, font=F_EN, fill=(255, 255, 255, 255), anchor="ma",
               stroke_width=2, stroke_fill=(0, 0, 0, 180))
        y += 62
    y += 16
    for ln in fa_l:
        d.text((W / 2, y), ln, font=F_FA, fill=CREAM + (255,), anchor="ma",
               stroke_width=2, stroke_fill=(0, 0, 0, 180), **RTL)
        y += 66
    return im


def verse_card(h1, h2):
    size = 68
    f = font(VE, size)
    while max(f.getlength(h1, **RTL), f.getlength(h2, **RTL)) > W - 240 and size > 44:
        size -= 2
        f = font(VE, size)
    tw = max(f.getlength(h1, **RTL), f.getlength(h2, **RTL))
    pw = int(min(W - 80, tw + 170))
    ph = int(size * 4.7)
    # film-style: gold verse over a soft shadow, thin ornament lines, no box
    txt = Image.new("RGBA", (W, ph + 40), (0, 0, 0, 0))
    d = ImageDraw.Draw(txt)
    d.text((W / 2, 20 + ph * 0.29), h1, font=f, fill=VGOLD + (255,), anchor="mm", **RTL)
    d.text((W / 2, 20 + ph * 0.73), h2, font=f, fill=VGOLD + (255,), anchor="mm", **RTL)
    half = min(tw / 2 + 30, W / 2 - 60)
    for yy in (20 + ph * 0.02, 20 + ph * 0.98):
        d.line([(W / 2 - half, yy), (W / 2 - 16, yy)], fill=GOLD + (170,), width=2)
        d.line([(W / 2 + 16, yy), (W / 2 + half, yy)], fill=GOLD + (170,), width=2)
        d.regular_polygon((W / 2, yy, 7), 4, fill=GOLD + (220,))
    a = txt.getchannel("A").filter(ImageFilter.GaussianBlur(10))
    im = Image.new("RGBA", txt.size, (0, 0, 0, 0))
    im.putalpha(a.point(lambda v: min(255, int(v * 2.2))))
    im.alpha_composite(txt)
    return im


def title_card(ep, en_title, fa_title, word="EPISODE"):  # ep: episode or part number
    im = Image.new("RGBA", (W, H), (0, 0, 0, 120))
    d = ImageDraw.Draw(im)
    d.text((W / 2, 690), "ROSTAM & SOHRAB", font=font(TI, 82, 700), fill=GOLD + (255,), anchor="mm")
    d.text((W / 2, 830), "رستم و سهراب", font=font(VE, 128), fill=VGOLD + (255,), anchor="mm", **RTL)
    d.line([(W / 2 - 200, 950), (W / 2 + 200, 950)], fill=GOLD + (180,), width=2)
    d.text((W / 2, 1015), f"{word} {ep}  ·  {en_title.upper()}", font=font(TI, 40, 600),
           fill=CREAM + (255,), anchor="mm")
    d.text((W / 2, 1090), f"قسمت {str(ep).translate(FA_DIGITS)}  ·  {fa_title}", font=font(FA, 46),
           fill=CREAM + (255,), anchor="mm", **RTL)
    return im


def end_card(en_next, fa_next, handle, label="NEXT EPISODE"):
    im = Image.new("RGBA", (W, H), (0, 0, 0, 150))
    d = ImageDraw.Draw(im)
    d.text((W / 2, 420), label, font=font(TI, 38, 600), fill=CREAM + (255,), anchor="mm")
    d.text((W / 2, 510), en_next.upper(), font=font(TI, 88, 700), fill=GOLD + (255,), anchor="mm")
    d.text((W / 2, 610), f"قسمت بعد: {fa_next}", font=font(FAB, 50), fill=VGOLD + (255,),
           anchor="mm", **RTL)
    d.line([(W / 2 - 200, 690), (W / 2 + 200, 690)], fill=GOLD + (180,), width=2)
    d.text((W / 2, 790), "برای دیدن بقیه فالو کن", font=font(FAB, 66), fill=(255, 255, 255, 255),
           anchor="mm", **RTL)
    d.text((W / 2, 870), "Follow to see the rest", font=font(EN, 48, 500), fill=CREAM + (255,),
           anchor="mm")
    bw, bh, by = 400, 100, 980
    d.rounded_rectangle([(W - bw) / 2, by - bh / 2, (W + bw) / 2, by + bh / 2], radius=50,
                        fill=GOLD + (255,))
    d.text((W / 2, by), "+ FOLLOW", font=font(TI, 42, 800), fill=(24, 18, 10, 255), anchor="mm")
    if handle:
        d.text((W / 2, 1095), handle, font=font(FA, 46), fill=CREAM + (255,), anchor="mm")
    return im


def part_header(n):
    """Top line on every frame of a part: «قسمت N از داستان رستم و سهراب»."""
    txt = f"قسمت {str(n).translate(FA_DIGITS)} از داستان رستم و سهراب"
    f = font(FAB, 46)
    im = Image.new("RGBA", (W, 300), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    y = 218
    tw = f.getlength(txt, **RTL)
    d.text((W / 2, y), txt, font=f, fill=CREAM + (255,), anchor="mm", **RTL)
    for sgn in (-1, 1):
        d.regular_polygon((W / 2 + sgn * (tw / 2 + 30), y + 4, 7), 4, fill=GOLD + (235,))
    a = im.getchannel("A").filter(ImageFilter.GaussianBlur(8))
    out = Image.new("RGBA", (W, 300), (0, 0, 0, 0))
    out.putalpha(a.point(lambda v: min(200, int(v * 1.8))))
    out.alpha_composite(im)
    return out


def watermark(handle):
    f = font(FA, 30)
    w = int(f.getlength(handle)) + 16
    im = Image.new("RGBA", (w, 52), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.text((w / 2 + 2, 28), handle, font=f, fill=(0, 0, 0, 90), anchor="mm")
    d.text((w / 2, 26), handle, font=f, fill=(255, 255, 255, 150), anchor="mm")
    return im


# watermark stops (text centre); it rests ~10 s at each and glides 2 s to the next,
# always clear of the verse card (y 370-690), the subtitles (y > ~830) and
# Instagram's top bar, caption and button rail
WM_POS = [(175, 300), (540, 300), (905, 300), (905, 770), (175, 770), (175, 300), (905, 770)]


def wm_pos(t, period=12.0, glide=2.0):
    k = int(t // period)
    u = t - k * period
    a, b = WM_POS[k % len(WM_POS)], WM_POS[(k + 1) % len(WM_POS)]
    e = ease((u - (period - glide)) / glide) if u > period - glide else 0.0
    x = a[0] + (b[0] - a[0]) * e + 9 * math.sin(t * 0.8)
    y = a[1] + (b[1] - a[1]) * e + 5 * math.sin(t * 1.1)
    return x, y


def bottom_grad():
    g = Image.new("L", (1, 980))
    for y in range(980):
        g.putpixel((0, y), int(215 * (y / 979) ** 1.5))
    im = Image.new("RGBA", (W, 980), (0, 0, 0, 0))
    im.putalpha(g.resize((W, 980)))
    return im


# ---------- backgrounds ----------
PAL = [((38, 30, 64), (214, 120, 58)), ((26, 34, 52), (120, 140, 160)),
       ((20, 22, 40), (190, 110, 60)), ((14, 18, 34), (60, 70, 110)),
       ((40, 52, 70), (226, 170, 96))]


def placeholder(label, seed):
    rnd = random.Random(seed)
    top, bot = PAL[seed % len(PAL)]
    tw, th = int(W * S), int(H * S)
    g = Image.new("RGB", (1, th))
    for y in range(th):
        t = y / (th - 1)
        g.putpixel((0, y), tuple(int(top[i] + (bot[i] - top[i]) * t ** 1.2) for i in range(3)))
    im = g.resize((tw, th))
    d = ImageDraw.Draw(im)
    base = int(th * 0.62)
    for k, shade in enumerate((0.55, 0.38, 0.22)):
        y = base + k * int(th * 0.08)
        pts, x = [(0, th)], 0
        h = y
        while x <= tw:
            h = max(int(th * 0.35), min(th - 40, h + rnd.randint(-38, 38)))
            pts.append((x, h))
            x += rnd.randint(30, 70)
        pts += [(tw, th)]
        col = tuple(int(c * shade) for c in bot)
        d.polygon(pts, fill=col)
    lab = f"تصویر {label} اینجا قرار می‌گیرد"
    d.text((tw / 2, th * 0.16), lab, font=font(FA, 38), fill=(255, 255, 255), anchor="mm", **RTL)
    return im


def find_image(images, sid):
    for ext in ("jpg", "jpeg", "png", "webp", "JPG", "PNG", "JPEG"):
        p = os.path.join(images or "", f"{sid}.{ext}")
        if images and os.path.exists(p):
            return p
    return None


def compose_fit(img):
    """Landscape picture in a vertical frame: whole picture across the width,
    over a blurred, darkened enlargement of itself."""
    tw, th = int(W * S), int(H * S)
    r = max(tw / img.width, th / img.height)
    bg = img.resize((round(img.width * r), round(img.height * r)), Image.BILINEAR)
    l, t = (bg.width - tw) // 2, (bg.height - th) // 2
    bg = bg.crop((l, t, l + tw, t + th)).filter(ImageFilter.GaussianBlur(45))
    bg = Image.blend(bg, Image.new("RGB", bg.size, (0, 0, 0)), 0.5)
    fh = round(img.height * tw / img.width)
    fg = img.resize((tw, fh), Image.LANCZOS)
    y = int(th * 0.45 - fh / 2)
    bg.paste(fg, (0, y))
    d = ImageDraw.Draw(bg)
    for yy in (y - 3, y + fh + 1):
        d.line([(0, yy), (tw, yy)], fill=GOLD, width=3)
    return bg


def load_bg(images, sid, seed):
    """Returns (picture at S times the frame size, is_fit)."""
    p = find_image(images, sid)
    if p:
        img = Image.open(p).convert("RGB")
        if img.width / img.height > 0.8:
            return compose_fit(img), True
        tw, th = int(W * S), int(H * S)
        r = max(tw / img.width, th / img.height)
        img = img.resize((round(img.width * r), round(img.height * r)), Image.LANCZOS)
        l, t = (img.width - tw) // 2, (img.height - th) // 2
        return img.crop((l, t, l + tw, t + th)), False
    num = sid[1:].lstrip("0") if sid.startswith("S") else sid
    return placeholder(f"صحنه {num.translate(FA_DIGITS)}", seed), False


def ease(p):
    p = max(0.0, min(1.0, p))
    return p * p * (3 - 2 * p)


def kb(src, p, mode):
    """Slow camera move: window shrinks/grows/pans over the oversized source."""
    e = ease(p)
    if mode == 0:
        z, fx, fy = 1.0 + (S - 1) * e, 0.5, 0.5
    elif mode == 1:
        z, fx, fy = S - (S - 1) * e, 0.5, 0.45
    elif mode == 2:
        z, fx, fy = 1.06, 0.30 + 0.40 * e, 0.5
    else:
        z, fx, fy = 1.06, 0.5, 0.65 - 0.30 * e
    ww, wh = src.width / z, src.height / z
    cx = ww / 2 + (src.width - ww) * fx
    cy = wh / 2 + (src.height - wh) * fy
    return src.resize((W, H), Image.BILINEAR, box=(cx - ww / 2, cy - wh / 2, cx + ww / 2, cy + wh / 2))


# ---------- timeline ----------
def build(ep_dir):
    script = json.load(open(f"{ep_dir}/script.json", encoding="utf-8"))
    tl = json.load(open(f"{ep_dir}/audio/timeline.json", encoding="utf-8"))
    scenes = []
    for i, (sc, ts) in enumerate(zip(script["scenes"], tl["scenes"])):
        start = 0.0 if i == 0 else ts["start"]
        end = tl["scenes"][i + 1]["start"] if i + 1 < len(tl["scenes"]) else tl["duration"]
        items = []
        for k, (ln, lt) in enumerate(zip(sc["lines"], ts["lines"])):
            nl = ts["lines"][k + 1] if k + 1 < len(ts["lines"]) else None
            nxt = (nl["verse_start"] or nl["start"]) if nl else end
            items.append({"role": ln["role"], "en": ln["en"], "fa": ln["fa"],
                          "verse": ln.get("verse"), "vs": lt["verse_start"],
                          "start": lt["start"], "end": lt["end"], "hold": nxt})
        scenes.append({"id": sc["id"], "card": sc.get("card"), "start": start, "end": end,
                       "items": items, "idx": i})
    return script, scenes


class Ctx:
    def __init__(self, ep_dir, images):
        self.script, self.scenes = build(ep_dir)
        self.images = images
        self.grad = bottom_grad()
        self._bg, self._ov = {}, {}
        self.anim = None
        if anim:
            mod = os.path.basename(os.path.abspath(ep_dir)) + "_scenes"     # e.g. p03 -> p03_scenes.py
            if os.path.exists(os.path.join(HERE, mod + ".py")):
                importlib.import_module(mod)
            self.anim = anim.Anim(ep_dir)
        part = self.script.get("part")
        self.header = part_header(part) if part else None

    def bg_src(self, sc):
        sid = sc["id"]
        if sc["card"] == "title" and not find_image(self.images, "TITLE"):
            sid = self.scenes[0]["id"]
        elif sc["card"] == "end" and not find_image(self.images, "END"):
            sid = self.scenes[-2]["id"]
        if sid not in self._bg:
            self._bg[sid] = load_bg(self.images, sid, len(self._bg) + sc["idx"])
        return self._bg[sid]

    def overlay(self, key, make, alpha):
        lv = max(0, min(10, round(alpha * 10)))
        if lv == 0:
            return None
        k = (key, lv)
        if k not in self._ov:
            base = self._ov.get((key, 10)) or make()
            self._ov[(key, 10)] = base
            if lv < 10:
                a = base.getchannel("A").point(lambda v: v * lv // 10)
                im = base.copy()
                im.putalpha(a)
                self._ov[k] = im
        return self._ov[k]

    def bg_frame(self, sc, t):
        if self.anim and self.anim.has(sc["id"]):
            return self.anim.frame(sc["id"], t)
        p = (t - sc["start"]) / max(0.01, sc["end"] - sc["start"])
        src, fit = self.bg_src(sc)
        # a fitted landscape picture only zooms; panning would push it off the frame
        return kb(src, p, sc["idx"] % 2 if fit else sc["idx"] % 4)

    def frame(self, sc, t):
        img = self._frame(sc, t)
        if self.header is not None:
            img = img.convert("RGBA")
            img.alpha_composite(self.header)
            img = img.convert("RGB")
        return img

    def _frame(self, sc, t):
        img = self.bg_frame(sc, t)
        # crossfade from the previous scene's last frame
        if sc["idx"] > 0 and t - sc["start"] < 0.6:
            prev = self.scenes[sc["idx"] - 1]
            a = (t - sc["start"]) / 0.6
            img = Image.blend(self.bg_frame(prev, prev["end"]), img, ease(a))
        img = img.convert("RGBA")
        ep = self.script["episode"]
        if sc["card"] == "title":
            a = min(1, (t - sc["start"]) / 0.8, (sc["end"] - t) / 0.6)
            num, word = (self.script["part"], "PART") if self.script.get("part") else (ep, "EPISODE")
            ov = self.overlay(("title",), lambda: title_card(num, self.script["title_en"],
                                                              self.script["title_fa"], word), a)
            if ov:
                img.alpha_composite(ov)
            return img.convert("RGB")
        if sc["card"] == "end":
            a = min(1, (t - sc["start"]) / 0.8)
            ov = self.overlay(("end",), lambda: end_card(self.script["next_en"],
                                                          self.script["next_fa"],
                                                          self.script.get("handle"),
                                                          self.script.get("next_label", "NEXT EPISODE")), a)
            if ov:
                img.alpha_composite(ov)
            return img.convert("RGB")
        for n, it in enumerate(sc["items"]):
            if it["verse"] and it["vs"] is not None:
                t0, t1 = it["vs"], min(it["hold"], it["end"] + 0.8)
                if t0 - 0.05 <= t < t1:
                    a = min(1, (t - t0) / 0.35, (t1 - t) / 0.35)
                    ov = self.overlay(("v", sc["id"], n), lambda it=it: verse_card(*it["verse"]), a)
                    if ov:
                        img.alpha_composite(ov, (0, 350))
            t0, t1 = it["start"] - 0.08, it["hold"] - 0.04
            if t0 <= t < t1:
                a = min(1, (t - t0) / 0.15, (t1 - t) / 0.15)
                ov = self.overlay(("s", sc["id"], n),
                                  lambda it=it: subtitle(it["role"], it["en"], it["fa"]), a)
                if ov:
                    img.alpha_composite(ov, (0, 1240 - ov.height))
        if self.script.get("handle"):
            if not hasattr(self, "_wm"):
                self._wm = watermark(self.script["handle"])
            x, y = wm_pos(t)
            img.alpha_composite(self._wm, (round(x - self._wm.width / 2), round(y - self._wm.height / 2)))
        return img.convert("RGB")


def encode(ctx, sc, t0, t1, out):
    tmp = out + ".part.mp4"
    ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
                           "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264",
                           "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p",
                           "-threads", "1", tmp], stdin=subprocess.PIPE)
    n = round((t1 - t0) * FPS)
    for i in range(n):
        ff.stdin.write(ctx.frame(sc, t0 + i / FPS).tobytes())
    ff.stdin.close()
    if ff.wait() != 0:
        sys.exit(f"ffmpeg failed for {out}")
    os.replace(tmp, out)
    return n


_ctx = None


def _job(args):
    global _ctx
    ep_dir, images, idx, t0, t1, out = args
    if _ctx is None:
        _ctx = Ctx(ep_dir, images)
    return encode(_ctx, _ctx.scenes[idx], t0, t1, out)


def concat(parts, out, audio=None, a0=None, a1=None):
    lst = out + ".txt"
    with open(lst, "w") as f:
        for p in parts:
            f.write(f"file '{os.path.abspath(p)}'\n")
    vid = out + ".v.mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst,
                    "-c", "copy", vid], check=True)
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-i", vid]
    af = []
    if a0 is not None:
        cmd += ["-ss", f"{a0:.3f}", "-to", f"{a1:.3f}"]
        af = ["-af", f"afade=t=in:d=0.15,afade=t=out:st={max(0, a1 - a0 - 0.25):.3f}:d=0.25"]
    cmd += ["-i", audio, "-map", "0:v", "-map", "1:a", "-c:v", "copy"] + af + [
            "-c:a", "aac", "-b:a", "160k", "-ar", "48000", "-ac", "2",
            "-shortest", "-movflags", "+faststart", out + ".part.mp4"]
    subprocess.run(cmd, check=True)
    os.replace(out + ".part.mp4", out)
    os.remove(vid)
    os.remove(lst)


def main():
    mode, ep_dir, images, out = sys.argv[1:5]
    ctx = Ctx(ep_dir, images)
    wav = f"{ep_dir}/audio/episode.wav"
    work = os.path.join(os.path.dirname(os.path.abspath(out)), "parts")
    os.makedirs(work, exist_ok=True)
    if mode == "still":
        t = float(sys.argv[5])
        sc = next(s for s in ctx.scenes if s["start"] <= t < s["end"])
        ctx.frame(sc, t).save(out, quality=90)
        return
    if mode == "full":
        ranges = [(s["start"], s["end"]) for s in ctx.scenes]
    else:
        ranges = [tuple(map(float, r.split(":"))) for r in sys.argv[5:]]
    jobs, owner = [], []
    for k, (r0, r1) in enumerate(ranges):
        for s in ctx.scenes:
            a, b = max(r0, s["start"]), min(r1, s["end"])
            if b - a > 1 / FPS:
                jobs.append((ep_dir, images, s["idx"], a, b,
                             os.path.join(work, f"p{len(jobs):03d}.mp4")))
                owner.append(k)
    with Pool(2) as pool:
        frames = pool.map(_job, jobs, chunksize=1)
    print(f"{sum(frames)} frames in {len(jobs)} parts")
    parts = [j[5] for j in jobs]
    if mode == "full":
        concat(parts, out, wav)
    else:
        # preview: each range gets its own audio cut, then all ranges are joined
        seg_files = []
        for k, (r0, r1) in enumerate(ranges):
            ps = [j[5] for j, o in zip(jobs, owner) if o == k]
            seg = os.path.join(work, f"seg{k}.mp4")
            concat(ps, seg, wav, r0, r1)
            seg_files.append(seg)
        lst = out + ".txt"
        with open(lst, "w") as f:
            for p in seg_files:
                f.write(f"file '{os.path.abspath(p)}'\n")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst,
                        "-c", "copy", "-movflags", "+faststart", out + ".part.mp4"], check=True)
        os.replace(out + ".part.mp4", out)
        os.remove(lst)


if __name__ == "__main__":
    main()
