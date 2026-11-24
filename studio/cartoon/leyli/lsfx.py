"""Sound helpers shared by the parts of Leyli & Majnun (on top of audio.py): copies of the Arash helpers (arash/asfx.py), so that this
series does not import another series' modules, plus a ney (a breathy reed flute) for the love theme LTHEME, sand blown by the wind
and a camel's grumble."""
import numpy as np
from audio import SR, rng, env, bandpass, lowpass, highpass, stereo, place, drum, bell, noise_bed, pluck_fast, shur, drone, pad

# the love theme of the series (Shur on D): a slow question that rises and falls back, played by the ney
LTHEME = [(0, 0.0, 1.0), (1, 1.0, 0.6), (2, 1.6, 1.4), (4, 3.0, 0.8), (3, 3.8, 0.7), (2, 4.5, 1.6)]
ATHEME = [(0, 0), (2, 0.4), (4, 0.8), (5, 1.3), (7, 1.9), (5, 2.5), (4, 2.9), (2, 3.4)]


def ney_note(f, dur, amp=0.06, seed=0, vib=5.2):
    """one breathy reed-flute note: a soft fundamental with a few partials, slow vibrato that grows, and breath noise"""
    r = np.random.default_rng(seed)
    n = int(dur * SR); t = np.arange(n) / SR
    v = 1 + 0.006 * np.minimum(1, t / 0.6) * np.sin(2 * np.pi * vib * t)
    ph = 2 * np.pi * np.cumsum(f * v) / SR
    x = np.sin(ph) + 0.28 * np.sin(2 * ph) + 0.1 * np.sin(3 * ph)
    br = bandpass(r.standard_normal(n).astype(np.float32), f * 0.8, f * 4) * 0.35
    e = np.minimum(1, t / 0.12) * np.minimum(1, (dur - t) / 0.35).clip(0, 1)
    return ((x + br) * e * amp).astype(np.float32)


def ney(m, notes, t0, amp=0.06, octave=1, pan=-0.15, step=1.0):
    """notes: (scale degree, start, length) in beats of `step` seconds"""
    for k, (deg, st, ln) in enumerate(notes):
        place(m, ney_note(shur(deg, octave), ln * step + 0.3, amp=amp, seed=k), t0 + st * step, pan=pan)


def sand_hiss(dur, amp=0.05, seed=0):
    """sand blown over sand: a high soft hiss that swells"""
    x = noise_bed(dur, amp=amp, lo=2500, hi=9000, lfo=0.5, seed=seed)
    sw = np.sin(np.pi * np.linspace(0, 1, len(x))) ** 0.7
    return x * sw[:, None]


def camel_grumble(amp=0.08, seed=0):
    """a camel's low bubbling grumble"""
    r = np.random.default_rng(seed)
    n = int(1.2 * SR); t = np.arange(n) / SR
    f = 70 + 18 * np.sin(2 * np.pi * 3.1 * t)
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * (0.6 + 0.4 * np.sin(2 * np.pi * 11 * t))
    x = x + 0.6 * bandpass(r.standard_normal(n).astype(np.float32), 150, 700)
    e = np.minimum(1, t / 0.1) * np.exp(-t * 1.6)
    return (x * e * amp).astype(np.float32)


def tanbur(m, notes, t0, amp=0.2, pan=0.2, low=False, step=1.0, dur=2.2):
    for deg, dt in notes:
        place(m, pluck_fast(shur(deg), dur, amp=amp), t0 + dt * step, pan=pan)
        if low and dt == 0:
            place(m, pluck_fast(shur(deg, -1), dur, amp=amp * 0.6), t0 + dt * step, pan=-pan)


def chirp(f0=3200, dur=0.13, amp=0.05):
    n = int(dur * SR); t = np.arange(n) / SR
    f = f0 * (1 + 0.45 * t / dur)
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.sin(np.pi * t / dur) ** 2
    return (s * amp).astype(np.float32)


def snort(amp=0.14, seed=0):
    r = np.random.default_rng(seed)
    n = int(0.55 * SR); t = np.arange(n) / SR
    x = bandpass(r.standard_normal(n).astype(np.float32), 250, 1100)
    e = np.minimum(1, t / 0.03) * np.exp(-t * 5) * (0.7 + 0.3 * np.sin(2 * np.pi * 28 * t))
    return (x * e * amp * 3).astype(np.float32)


def neigh(amp=0.1, seed=0):
    n = int(0.9 * SR); t = np.arange(n) / SR
    f = 700 + 300 * np.sin(2 * np.pi * 9 * t) * np.exp(-t * 2) - 300 * t
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, 0.05, 0.4) * (0.6 + 0.4 * np.sin(2 * np.pi * 30 * t))
    return bandpass((x * amp).astype(np.float32), 300, 3000)


def whoosh(dur=1.6, amp=0.12, seed=3):
    x = noise_bed(dur, amp=amp, lo=300, hi=3200, lfo=0.3, seed=seed)
    ramp = np.linspace(0, 1, len(x)) ** 2
    return x * ramp[:, None]


def gust(dur=1.4, amp=0.16, seed=5):
    """a sudden gust of wind: swells and dies"""
    x = noise_bed(dur, amp=amp, lo=200, hi=2600, lfo=0.8, seed=seed)
    n = len(x); t = np.arange(n) / SR
    return x * (np.sin(np.pi * t / (dur)) ** 1.5)[:, None]


def thud(amp=0.3, f0=70, seed=0):
    r = np.random.default_rng(seed)
    n = int(0.5 * SR); t = np.arange(n) / SR
    body = np.sin(2 * np.pi * f0 * t * (1 + 0.5 * np.exp(-t * 30))) * np.exp(-t * 14)
    nz = lowpass(r.standard_normal(n).astype(np.float32), 700) * np.exp(-t * 25)
    return ((body + 0.6 * nz) * amp).astype(np.float32)


def steps(m, t0, t1, step=0.5, amp=0.05, seed=0, pan=0.0):
    r = np.random.default_rng(seed)
    t = t0
    while t < t1:
        n = int(0.12 * SR); tt = np.arange(n) / SR
        x = lowpass(r.standard_normal(n).astype(np.float32), 1200) * np.exp(-tt * 35)
        place(m, (x * amp * r.uniform(0.6, 1.0)).astype(np.float32), t + r.uniform(-0.04, 0.04), pan=pan + r.uniform(-0.3, 0.3))
        t += step


def hooves(m, t0, t1, step=0.42, amp=0.07, pan=0.2, seed=0, gallop=False):
    r = np.random.default_rng(seed)
    t = t0
    beats = (0.0, 0.07, 0.15) if gallop else (0.0, 0.11)
    while t < t1:
        for k, dt in enumerate(beats):
            n = int(0.09 * SR); tt = np.arange(n) / SR
            x = bandpass(r.standard_normal(n).astype(np.float32), 300 if gallop else 500, 2600) * np.exp(-tt * 60)
            x += np.sin(2 * np.pi * (120 + 40 * k) * tt) * np.exp(-tt * 40) * (0.9 if gallop else 0.5)
            place(m, (x * amp * r.uniform(0.7, 1.1)).astype(np.float32), t + dt, pan=pan)
        t += step


def scrape(dur=0.6, amp=0.08, seed=0):
    r = np.random.default_rng(seed)
    n = int(dur * SR); t = np.arange(n) / SR
    x = bandpass(r.standard_normal(n).astype(np.float32), 1200, 5000) * (0.5 + 0.5 * np.sin(2 * np.pi * 9 * t)) * env(n, 0.05, 0.15)
    return (x * amp * 2).astype(np.float32)


def rustle(amp=0.04, dur=0.7, seed=0):
    """cloth, leaves and twigs being moved"""
    r = np.random.default_rng(seed)
    n = int(dur * SR); t = np.arange(n) / SR
    x = bandpass(r.standard_normal(n).astype(np.float32), 1500, 6000) * (0.5 + 0.5 * np.sin(2 * np.pi * 5 * t)) * env(n, 0.1, 0.3)
    return (x * amp * 2).astype(np.float32)


def creak(dur=1.2, amp=0.08, seed=0):
    """a wooden door turning on its hinges"""
    r = np.random.default_rng(seed)
    n = int(dur * SR); t = np.arange(n) / SR
    f = 180 + 60 * np.sin(2 * np.pi * 0.7 * t) + 40 * r.standard_normal(n).cumsum() / np.sqrt(n)
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * (0.5 + 0.5 * np.sin(2 * np.pi * 23 * t)) * env(n, 0.1, 0.3)
    return bandpass((x * amp).astype(np.float32), 200, 2200)


def wings(m, t0, n=4, rate=0.16, amp=0.05, seed=0, pan=0.2):
    r = np.random.default_rng(seed)
    for k in range(n):
        k_ = int(0.12 * SR); tt = np.arange(k_) / SR
        x = bandpass(r.standard_normal(k_).astype(np.float32), 300, 1800) * np.sin(np.pi * tt / 0.12) ** 2
        place(m, (x * amp * (1 - 0.12 * k)).astype(np.float32), t0 + k * rate + r.uniform(0, 0.03), pan=pan + r.uniform(-0.3, 0.3))


def heartbeat(m, t0, t1, bpm=72, amp=0.35):
    t = t0
    while t < t1:
        place(m, drum(dur=0.4, f0=48, amp=amp, noise=0.05), t)
        place(m, drum(dur=0.35, f0=44, amp=amp * 0.7, noise=0.05), t + 0.22)
        t += 60 / bpm


def hiss(dur=1.0, amp=0.08, seed=0):
    """a snake's hiss: bright noise that swells and fades"""
    r = np.random.default_rng(seed)
    n = int(dur * SR); t = np.arange(n) / SR
    x = highpass(r.standard_normal(n).astype(np.float32), 3200) * np.sin(np.pi * np.minimum(1, t / dur)) ** 0.8
    x = bandpass(x, 3000, 9000)
    return (x * amp * 2.2).astype(np.float32)


def crickets(m, t0, t1, amp=0.012, seed=0, rate=0.9):
    """night crickets: short trilled chirps far away"""
    r = np.random.default_rng(seed)
    t = t0
    while t < t1:
        f = r.uniform(4200, 5200); d = r.uniform(0.18, 0.3)
        n = int(d * SR); tt = np.arange(n) / SR
        x = np.sin(2 * np.pi * f * tt) * (0.5 + 0.5 * np.sign(np.sin(2 * np.pi * r.uniform(28, 36) * tt))) * np.sin(np.pi * tt / d) ** 2
        place(m, (x * amp * r.uniform(0.5, 1.0)).astype(np.float32), t, pan=r.uniform(-0.7, 0.7))
        t += rate * r.uniform(0.5, 1.4)


def owl(amp=0.05):
    """a soft owl's hoot: hoo… hoo-hoo"""
    out = np.zeros(int(1.6 * SR), np.float32)
    for t0, d in ((0.0, 0.42), (0.75, 0.22), (1.05, 0.38)):
        n = int(d * SR); tt = np.arange(n) / SR
        f = 390 * (1 - 0.06 * tt / d)
        x = np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, 0.06, 0.15) * (1 + 0.06 * np.sin(2 * np.pi * 7 * tt))
        i = int(t0 * SR); out[i:i + n] += x
    return lowpass(out * amp, 1200)


def bleat(amp=0.06, seed=0, f0=520):
    """a goat's bleat: a shaky 'meh-eh-eh'"""
    r = np.random.default_rng(seed)
    d = 0.55; n = int(d * SR); t = np.arange(n) / SR
    f = f0 * (1 + 0.04 * r.standard_normal()) * (1 - 0.1 * t / d)
    am = 0.55 + 0.45 * np.sin(2 * np.pi * 11 * t)
    ph = 2 * np.pi * np.cumsum(f) / SR
    x = (np.sin(ph) + 0.6 * np.sin(2 * ph) + 0.4 * np.sin(3 * ph) + 0.25 * np.sin(4 * ph)) * am * env(n, 0.03, 0.15)
    return bandpass((x * amp).astype(np.float32), 400, 3200)


def grunt(amp=0.08, seed=0):
    """a camel's low grumble"""
    r = np.random.default_rng(seed)
    d = 0.8; n = int(d * SR); t = np.arange(n) / SR
    f = 95 + 15 * np.sin(2 * np.pi * 3 * t)
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * (0.6 + 0.4 * np.sin(2 * np.pi * 21 * t)) + 0.5 * lowpass(r.standard_normal(n).astype(np.float32), 500)
    return (lowpass(x.astype(np.float32), 900) * env(n, 0.08, 0.3) * amp).astype(np.float32)


def pour(dur=1.6, amp=0.05, seed=0):
    """milk poured into a bowl: a soft bubbling stream"""
    r = np.random.default_rng(seed)
    n = int(dur * SR); t = np.arange(n) / SR
    x = bandpass(r.standard_normal(n).astype(np.float32), 500, 2400)
    bub = 0.6 + 0.4 * np.sin(2 * np.pi * (9 + 3 * np.sin(2 * np.pi * 1.3 * t)) * t)
    return (x * bub * env(n, 0.08, 0.3) * amp * 2).astype(np.float32)


def dig(amp=0.12, seed=0):
    """a spade cutting into earth and the earth thrown aside"""
    r = np.random.default_rng(seed)
    n = int(0.7 * SR); t = np.arange(n) / SR
    cut = bandpass(r.standard_normal(n).astype(np.float32), 900, 4000) * np.exp(-t * 18) * 0.8
    cut += np.sin(2 * np.pi * 160 * t) * np.exp(-t * 40) * 0.4
    toss = np.zeros(n, np.float32)
    i = int(0.32 * SR)
    m = n - i; tt = np.arange(m) / SR
    toss[i:] = lowpass(r.standard_normal(m).astype(np.float32), 1400) * np.exp(-tt * 9) * 0.7
    return ((cut + toss) * amp).astype(np.float32)


def whistle(dur=1.6, amp=0.06, f0=2400, f1=1500, seed=0):
    """an arrow in flight: a thin whistle falling in pitch, with a breath of air"""
    r = np.random.default_rng(seed)
    n = int(dur * SR); t = np.arange(n) / SR
    f = f0 + (f1 - f0) * (t / dur)
    tone = np.sin(2 * np.pi * np.cumsum(f) / SR) * (0.7 + 0.3 * np.sin(2 * np.pi * 7 * t))
    air = bandpass(r.standard_normal(n).astype(np.float32), 1200, 6000) * 0.6
    e = np.sin(np.pi * np.clip(t / dur, 0, 1)) ** 1.5
    return ((tone * 0.6 + air) * e * amp).astype(np.float32)


def murmur(dur, amp=0.05, seed=0):
    """a crowd talking low"""
    return noise_bed(dur, amp=amp, lo=250, hi=900, lfo=1.8, seed=seed)


def laugh(dur=2.4, amp=0.1, seed=0, voices=5):
    """men laughing together: bursts of 'ha' at 4-6 a second"""
    r = np.random.default_rng(seed)
    n = int(dur * SR); t = np.arange(n) / SR
    out = np.zeros(n, np.float32)
    for v in range(voices):
        rate = r.uniform(4.0, 6.0); f0 = r.uniform(110, 190); ph = r.uniform(0, 6.3)
        gate = np.maximum(0.0, np.sin(2 * np.pi * rate * t + ph)) ** 2 * np.exp(-t * r.uniform(0.3, 0.9))
        voice = np.sin(2 * np.pi * f0 * t) + 0.5 * np.sin(2 * np.pi * 2 * f0 * t) + 0.25 * np.sin(2 * np.pi * 3 * f0 * t)
        breath = bandpass(r.standard_normal(n).astype(np.float32), 600, 2600)
        out += (voice * 0.35 + breath * 0.8) * gate
    out = bandpass(out.astype(np.float32), 150, 3200)
    return (out / (np.abs(out).max() + 1e-6) * amp).astype(np.float32)


# ---- part 2: the forge, the bowstring, the eagle, the light of Spandarmad
def clang(amp=0.12, seed=0, f0=1900):
    """a hammer on hot iron at the anvil: a short metal ring with a hard knock"""
    r = np.random.default_rng(seed)
    n = int(0.9 * SR); t = np.arange(n) / SR
    f = f0 * (1 + 0.06 * r.random())
    ring = sum(w * np.sin(2 * np.pi * f * m * t) * np.exp(-t * d) for m, w, d in ((1, 1.0, 7), (2.32, 0.5, 9), (3.9, 0.3, 13), (5.6, 0.15, 18)))
    k = int(0.03 * SR)
    knock = np.zeros(n, np.float32)
    knock[:k] = highpass(r.standard_normal(k).astype(np.float32), 1500) * np.exp(-np.arange(k) / SR * 120)
    low = np.sin(2 * np.pi * 180 * t) * np.exp(-t * 30)
    return ((ring * 0.5 + knock * 1.2 + low * 0.4) * amp).astype(np.float32)


def twang(amp=0.2, f0=98.0, seed=0):
    """a big bowstring plucked: a low string that drops a little in pitch, with a buzz"""
    n = int(1.4 * SR); t = np.arange(n) / SR
    f = f0 * (1 + 0.12 * np.exp(-t * 18))
    ph = 2 * np.pi * np.cumsum(f) / SR
    x = (np.sin(ph) + 0.45 * np.sin(2 * ph) + 0.25 * np.sin(3 * ph) + 0.12 * np.sign(np.sin(ph)) * np.exp(-t * 20)) * np.exp(-t * 3.2)
    x *= np.minimum(1, t / 0.004)
    return lowpass((x * amp).astype(np.float32), 2400)


def eagle_cry(amp=0.06, seed=0):
    """the high, thin scream of an eagle far up: a falling whistle with a rough edge, twice"""
    r = np.random.default_rng(seed)
    out = np.zeros(int(1.6 * SR), np.float32)
    for k, (t0, dur, fa, fb) in enumerate(((0.0, 0.55, 3400, 2300), (0.7, 0.75, 3600, 2100))):
        n = int(dur * SR); t = np.arange(n) / SR
        f = fa + (fb - fa) * (t / dur) ** 0.7 + 90 * np.sin(2 * np.pi * 38 * t)
        x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.sin(np.pi * t / dur) ** 0.6
        x += 0.3 * bandpass(r.standard_normal(n).astype(np.float32), 2000, 5000) * np.sin(np.pi * t / dur)
        i = int(t0 * SR); out[i:i + n] += x.astype(np.float32)
    return (out * amp).astype(np.float32)


def shimmer(m, t0, dur=3.0, amp=0.03, seed=0, base=880.0, pan=0.3):
    """the soft sparkle of a light from another world: many small high bells"""
    r = np.random.default_rng(seed)
    for k in range(int(dur * 5)):
        f = base * 2 ** (r.integers(0, 12) / 12) * (2 if r.random() < 0.3 else 1)
        place(m, bell(f, 2.0, amp * r.uniform(0.5, 1.0)), t0 + r.uniform(0, dur), pan=r.uniform(-pan, pan))


def flap(amp=0.1, seed=0, dur=0.9):
    """a cloak snatched by the wind: cloth flapping fast, then gone"""
    r = np.random.default_rng(seed)
    n = int(dur * SR); t = np.arange(n) / SR
    x = bandpass(r.standard_normal(n).astype(np.float32), 300, 2600)
    e = (0.55 + 0.45 * np.sign(np.sin(2 * np.pi * (14 - 6 * t / dur) * t))) * np.exp(-t * 2.4) * np.minimum(1, t / 0.02)
    return (x * e * amp * 2).astype(np.float32)


# ---- part 3: the shot, the flight, the river, Tirgan
def splash(amp=0.1, seed=0, dur=0.7):
    """water thrown by hand: a bright wet burst, then droplets falling back"""
    r = np.random.default_rng(seed)
    n = int(dur * SR); t = np.arange(n) / SR
    x = bandpass(r.standard_normal(n).astype(np.float32), 700, 7000) * np.exp(-t * 9) * np.minimum(1, t / 0.01)
    drops = np.zeros(n, np.float32)
    for k in range(14):
        i = int(r.uniform(0.12, dur - 0.08) * SR); m = int(0.03 * SR); tt = np.arange(m) / SR
        f = r.uniform(900, 2600)
        drops[i:i + m] += (np.sin(2 * np.pi * f * tt * (1 + 2.5 * tt)) * np.exp(-tt * 140) * r.uniform(0.2, 0.6)).astype(np.float32)
    return ((x * 1.4 + drops) * amp).astype(np.float32)


def kids_laugh(dur=2.0, amp=0.06, seed=0, voices=3):
    """children laughing and shrieking with joy: quick high bursts"""
    r = np.random.default_rng(seed)
    n = int(dur * SR); t = np.arange(n) / SR
    out = np.zeros(n, np.float32)
    for v in range(voices):
        rate = r.uniform(5.0, 7.0); f0 = r.uniform(300, 430); ph = r.uniform(0, 6.3)
        gate = np.maximum(0.0, np.sin(2 * np.pi * rate * t + ph)) ** 2 * np.exp(-t * r.uniform(0.4, 1.0))
        f = f0 * (1 + 0.08 * np.sin(2 * np.pi * 1.3 * t + ph))
        voice = np.sin(2 * np.pi * np.cumsum(f) / SR) + 0.4 * np.sin(4 * np.pi * np.cumsum(f) / SR)
        breath = bandpass(r.standard_normal(n).astype(np.float32), 1200, 4500)
        out += (voice * 0.4 + breath * 0.6) * gate
    out = bandpass(out.astype(np.float32), 250, 5000)
    return (out / (np.abs(out).max() + 1e-6) * amp).astype(np.float32)


def river(dur, amp=0.04, seed=0):
    """a wide river flowing: a low rush with small lapping waves"""
    return noise_bed(dur, amp=amp, lo=120, hi=1400, lfo=0.25, seed=seed)


def thunk(amp=0.25, seed=0):
    """an arrow striking deep into a tree: a hard wooden knock and a short quiver"""
    r = np.random.default_rng(seed)
    n = int(0.8 * SR); t = np.arange(n) / SR
    knock = np.sin(2 * np.pi * 210 * t * (1 + 0.3 * np.exp(-t * 60))) * np.exp(-t * 28)
    crack = highpass(r.standard_normal(n).astype(np.float32), 1800) * np.exp(-t * 70)
    quiver = np.sin(2 * np.pi * 34 * t) * np.sin(2 * np.pi * 420 * t) * np.exp(-t * 6) * 0.25
    return ((knock + 0.5 * crack + quiver) * amp).astype(np.float32)
