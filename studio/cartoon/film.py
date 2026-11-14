"""Shot / scene framework: painted background + per-frame SVG cast (resvg) + lighting + particles + film finish."""
import io, json, math, os, subprocess, time
import numpy as np, resvg_py
from PIL import Image, ImageDraw, ImageFilter

W, H, FPS = 1080, 1920, 30
from paths import LIPS as LIPDIR

def ease(u):
    u = min(1.0, max(0.0, u)); return u * u * (3 - 2 * u)

def lerp(a, b, u): return a + (b - a) * u

def svg_render(body, w=W, h=H):
    doc = f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">{body}</svg>'
    return Image.open(io.BytesIO(bytes(resvg_py.svg_to_bytes(svg_string=doc, skip_system_fonts=True)))).convert("RGBA")

# ------------------------------------------------------------------ lip sync
_LIPS = {}
def lips_data(lid):
    if lid not in _LIPS:
        _LIPS[lid] = json.load(open(f"{LIPDIR}/{lid}.json"))
    return _LIPS[lid]

def mouth(lines, t):
    """lines: list of (line_id, start_time). returns (open, width, talking)"""
    for lid, t0 in lines:
        d = lips_data(lid)
        i = (t - t0) * FPS
        if 0 <= i < len(d["db"]) - 1:
            k = int(i); f = i - k
            db = d["db"][k] * (1 - f) + d["db"][k + 1] * f
            o = max(0.0, min(1.0, (db + 30) / 18)) ** 1.2 * 0.9
            w = 0.9 + 0.35 * max(0, min(1, (d["cen"][k] - 1500) / 2500))
            return o, w, True
    return 0.0, 1.0, False

def blink_at(t, seed=0, period=3.3):
    """natural blinking"""
    r = (math.sin(seed * 12.9898) * 43758.5453) % 1
    ph = (t + r * period) % period
    if ph < 0.16:
        return math.sin(ph / 0.16 * math.pi)
    return 0.0

def talk_pose(lines, t, seed=0, base=None):
    """head motion, brows and mouth driven by speech"""
    o, w, talking = mouth(lines, t)
    q = dict(base or {})
    q["mouth_o"] = o; q["mouth_w"] = w
    q["nod"] = q.get("nod", 0) + (2.2 * math.sin(t * 5.1 + seed) * o if talking else 0) + 1.2 * math.sin(t * 0.9 + seed)
    q["tilt"] = q.get("tilt", 0) + (1.2 * math.sin(t * 1.9 + seed) if talking else 0.5 * math.sin(t * 0.7 + seed))
    q["brow"] = q.get("brow", 0) + (0.35 * o if talking else 0)
    q["blink"] = max(q.get("blink", 0), blink_at(t, seed))
    q["breathe"] = math.sin(t * 2.0 + seed)
    return q

# ------------------------------------------------------------------ camera helpers
def cam_static(k=1.0, cx=W / 2, cy=H / 2):
    return lambda t: (k, cx, cy, 0.0, 0.0)

def cam_push(k0, k1, cx, cy, dur, px0=0, px1=0, py0=0, py1=0):
    return lambda t: (lerp(k0, k1, ease(t / dur)), cx, cy, lerp(px0, px1, ease(t / dur)), lerp(py0, py1, ease(t / dur)))

def affine(img, k, cx, cy, px, py, size=(W, H)):
    return img.transform(size, Image.AFFINE, (1 / k, 0, cx - (px + cx) / k, 0, 1 / k, cy - (py + cy) / k), resample=Image.BICUBIC)

# ------------------------------------------------------------------ particles
class Snow:
    def __init__(self, n=420, seed=1, wind=-160, fall=(160, 420), size=(1.4, 4.5), alpha=(120, 235), y0=0, y1=H):
        r = np.random.default_rng(seed)
        self.x = r.uniform(0, W, n); self.y = r.uniform(y0, y1, n); self.v = r.uniform(*fall, n)
        self.s = r.uniform(*size, n); self.a = r.uniform(*alpha, n); self.wind = wind; self.ph = r.uniform(0, 6.3, n); self.y0, self.y1 = y0, y1
    def __call__(self, im, t):
        d = ImageDraw.Draw(im, "RGBA")
        span = self.y1 - self.y0
        for x, y, v, s, a, ph in zip(self.x, self.y, self.v, self.s, self.a, self.ph):
            xx = (x + self.wind * t * (v / 300) + 14 * math.sin(t * 1.3 + ph)) % W
            yy = self.y0 + (y - self.y0 + v * t) % span
            d.ellipse((xx - s, yy - s, xx + s, yy + s), fill=(255, 255, 255, int(a)))

class Motes:
    def __init__(self, n=60, seed=5, color=(255, 226, 180), box=(0, 300, W, 1500), drift=(-20, -6), size=(1.2, 3.4), amax=120):
        r = np.random.default_rng(seed)
        x0, y0, x1, y1 = box
        self.p = [(r.uniform(x0, x1), r.uniform(y0, y1), r.uniform(*size), r.uniform(0, 6.3)) for _ in range(n)]
        self.c = color; self.dr = drift; self.amax = amax; self.box = box
    def __call__(self, im, t):
        d = ImageDraw.Draw(im, "RGBA")
        x0, y0, x1, y1 = self.box
        for x, y, s, ph in self.p:
            px = x0 + (x - x0 + self.dr[0] * t + 30 * math.sin(t * 0.7 + ph)) % (x1 - x0)
            py = y0 + (y - y0 + self.dr[1] * t + 14 * math.sin(t * 0.9 + ph)) % (y1 - y0)
            a = int(self.amax * (0.55 + 0.45 * math.sin(t * 2 + ph)))
            d.ellipse((px - s, py - s, px + s, py + s), fill=self.c + (max(0, a),))

class Embers:
    def __init__(self, n=50, seed=2, box=(300, 900, 700, 1300), rise=(60, 160), color=(255, 160, 70)):
        r = np.random.default_rng(seed)
        x0, y0, x1, y1 = box
        self.p = [(r.uniform(x0, x1), r.uniform(0, 1), r.uniform(*rise), r.uniform(1.5, 3.5), r.uniform(0, 6.3)) for _ in range(n)]
        self.box = box; self.c = color
    def __call__(self, im, t):
        d = ImageDraw.Draw(im, "RGBA")
        x0, y0, x1, y1 = self.box
        for x, u, v, s, ph in self.p:
            life = (u + t * v / (y1 - y0)) % 1
            yy = y1 - life * (y1 - y0); xx = x + 30 * math.sin(t * 1.7 + ph) * life
            a = int(230 * (1 - life))
            d.ellipse((xx - s, yy - s, xx + s, yy + s), fill=self.c + (a,))

# ------------------------------------------------------------------ finishing
rng = np.random.default_rng(9)
_yy, _xx = np.mgrid[0:H, 0:W].astype(np.float32)
_VIG = (1 - np.clip((np.sqrt(((_xx - W / 2) / (W * 0.62)) ** 2 + ((_yy - H / 2) / (H * 0.62)) ** 2) - 0.55) / 0.6, 0, 1) ** 1.6 * 0.5)[..., None]
_GRAIN = [np.repeat(np.repeat(rng.normal(0, 2.4, (H // 2, W // 2, 1)), 2, 0), 2, 1).astype(np.float32) for _ in range(4)]

def finish(f, t, sun=None, bloom=0.5, grade="warm", fade=1.0):
    """f: float32 HxWx3 0..1"""
    small = Image.fromarray((np.clip(f, 0, 1) * 255).astype(np.uint8)).resize((W // 4, H // 4), Image.BILINEAR)
    a = np.asarray(small).astype(np.float32) / 255
    lum = a.max(2, keepdims=True)
    hi = np.clip((lum - 0.72) / 0.28, 0, 1) * a
    b = np.asarray(Image.fromarray((hi * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(10)).resize((W, H), Image.BILINEAR)).astype(np.float32) / 255
    f = 1 - (1 - f) * (1 - b * bloom)
    if sun:
        gx, gy, gr, col = sun
        g = np.clip(1 - np.sqrt((_xx - gx) ** 2 + (_yy - gy) ** 2) / gr, 0, 1) ** 2
        f = f + g[..., None] * np.array(col, np.float32)
    l = f.mean(2, keepdims=True)
    if grade == "warm":
        f = f + (1 - l) * np.array([0.0, -0.008, 0.025], np.float32) + l * np.array([0.022, 0.006, -0.018], np.float32)
    elif grade == "night":
        f = f * np.array([0.92, 0.97, 1.06], np.float32) + (1 - l) * np.array([0.0, 0.004, 0.03], np.float32)
    elif grade == "fire":
        f = f + l * np.array([0.03, 0.008, -0.025], np.float32) + (1 - l) * np.array([0.01, -0.004, 0.0], np.float32)
    f = f * _VIG * fade
    return np.clip(f * 255 + _GRAIN[int(t * 12) % 4], 0, 255).astype(np.uint8)

# ------------------------------------------------------------------ lighting of the cast layer
def light_mid(mid, L):
    a = np.asarray(mid).astype(np.float32) / 255
    A = a[..., 3]; C = a[..., :3]
    if A.max() <= 0:
        return C, A
    if L.get("ambient"):
        C = C * np.array(L["ambient"], np.float32)
    if L.get("ramp"):
        x0, x1, lo, hi = L["ramp"]
        f = lo + (hi - lo) * np.clip((np.arange(W, dtype=np.float32) - x0) / (x1 - x0), 0, 1)
        f = np.broadcast_to(f, A.shape)[..., None]
        C = C * f + (1 - f) * np.array(L.get("shadow", (-0.02, 0.0, 0.07)), np.float32)
    if L.get("point"):
        px, py, pr, lo, hi, col = L["point"]
        g = np.clip(1 - np.sqrt((_xx - px) ** 2 + (_yy - py) ** 2) / pr, 0, 1)
        f = (lo + (hi - lo) * g)[..., None]
        C = C * f + g[..., None] * np.array(col, np.float32) * 0.25
    if L.get("rim_point"):
        px, d = L["rim_point"]
        rr = np.zeros_like(A); rl = np.zeros_like(A)
        rr[:, :-d] = A[:, :-d] * (1 - A[:, d:]); rl[:, d:] = A[:, d:] * (1 - A[:, :-d])
        xs = np.arange(W)[None, :]
        rim = np.where(xs < px, rr, rl)
        rim = np.asarray(Image.fromarray((rim * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.3))).astype(np.float32) / 255
        C = C + rim[..., None] * np.array(L.get("rim_col", (1.0, 0.7, 0.4)), np.float32) * L.get("rim_str", 0.85)
        return np.clip(C, 0, 1), A
    dx, dy = L.get("rim", (5, -2))
    if dx or dy:
        rim = np.zeros_like(A)
        sx = slice(0, W - dx) if dx > 0 else slice(-dx, W)
        tx = slice(dx, W) if dx > 0 else slice(0, W + dx)
        rim[:, sx] = A[:, sx] * (1 - A[:, tx])
        if dy:
            up = abs(dy)
            if dy < 0:
                rim[up:, :] = np.maximum(rim[up:, :], A[up:, :] * (1 - A[:-up, :]) * 0.6)
            else:
                rim[:-up, :] = np.maximum(rim[:-up, :], A[:-up, :] * (1 - A[up:, :]) * 0.6)
        rim = np.asarray(Image.fromarray((rim * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.3))).astype(np.float32) / 255
        C = C + rim[..., None] * np.array(L.get("rim_col", (1.0, 0.7, 0.4)), np.float32) * L.get("rim_str", 0.85)
    return np.clip(C, 0, 1), A

# ------------------------------------------------------------------ shot
class Shot:
    def __init__(self, dur, bg, mid=None, fg=None, cam=None, light=None, fx=(), pre_fx=(), sun=None, bloom=0.5, grade="warm",
                 fade_in=0.0, fade_out=0.0, bg_par=0.6, mid_blur=0.0):
        self.dur, self.bg, self.mid, self.fg = dur, bg, mid, fg
        self.cam = cam or cam_static()
        self.light = light or {}
        self.fx, self.pre_fx = fx, pre_fx
        self.sun, self.bloom, self.grade = sun, bloom, grade
        self.fi, self.fo, self.bg_par, self.mid_blur = fade_in, fade_out, bg_par, mid_blur

    def frame(self, t):
        k, cx, cy, px, py = self.cam(t)
        kb = 1 + (k - 1) * self.bg_par
        bg = self.bg(t) if callable(self.bg) else self.bg
        bgi = affine(bg, kb, cx, cy, px * self.bg_par, py * self.bg_par, (W, H)) if (kb != 1 or px or py or bg.size != (W, H)) else bg
        f = np.asarray(bgi.convert("RGB")).astype(np.float32) / 255
        if self.pre_fx:
            im = Image.fromarray((f * 255).astype(np.uint8)).convert("RGBA")
            for fx in self.pre_fx:
                fx(im, t)
            f = np.asarray(im.convert("RGB")).astype(np.float32) / 255
        if self.mid:
            body = self.mid(t)
            if body:
                camt = f"translate({px:.2f},{py:.2f}) translate({cx:.2f},{cy:.2f}) scale({k:.5f}) translate({-cx:.2f},{-cy:.2f})"
                mid = svg_render(f'<g transform="{camt}">{body}</g>')
                if self.mid_blur:
                    mid = mid.filter(ImageFilter.GaussianBlur(self.mid_blur))
                C, A = light_mid(mid, self.light)
                f = f * (1 - A[..., None]) + C * A[..., None]
        if self.fg:
            for fgimg in (self.fg if isinstance(self.fg, (list, tuple)) else [self.fg]):
                g = fgimg(t) if callable(fgimg) else fgimg
                gi = affine(g, k, cx, cy, px, py, (W, H)) if (k != 1 or px or py) else g
                ga = np.asarray(gi).astype(np.float32) / 255
                f = f * (1 - ga[..., 3:4]) + ga[..., :3] * ga[..., 3:4]
        if self.fx:
            im = Image.fromarray((np.clip(f, 0, 1) * 255).astype(np.uint8)).convert("RGBA")
            for fx in self.fx:
                fx(im, t)
            f = np.asarray(im.convert("RGB")).astype(np.float32) / 255
        fade = 1.0
        if self.fi and t < self.fi: fade = ease(t / self.fi)
        if self.fo and t > self.dur - self.fo: fade = min(fade, ease((self.dur - t) / self.fo))
        return finish(f, t, self.sun, self.bloom, self.grade, fade)

def render_scene(shots, out, crf=18):
    tmp = out[:-4] + ".part.mp4"
    p = subprocess.Popen(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                          "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-crf", str(crf), "-pix_fmt", "yuv420p", tmp],
                         stdin=subprocess.PIPE)
    for sh in shots:
        n = int(round(sh.dur * FPS))
        for i in range(n):
            p.stdin.write(sh.frame(i / FPS).tobytes())
    p.stdin.close(); p.wait()
    if p.returncode == 0:
        os.replace(tmp, out)
    return p.returncode

def stills(shots, times, path):
    """contact sheet of frames at scene-global times"""
    ims = []
    for T in times:
        acc = 0.0
        for sh in shots:
            if T < acc + sh.dur or sh is shots[-1]:
                ims.append(Image.fromarray(sh.frame(min(T - acc, sh.dur - 1 / FPS))).resize((360, 640)))
                break
            acc += sh.dur
    sheet = Image.new("RGB", (360 * len(ims), 640))
    for i, im in enumerate(ims):
        sheet.paste(im, (i * 360, 0))
    sheet.save(path)
