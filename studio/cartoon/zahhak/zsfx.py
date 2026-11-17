"""Sound helpers shared by the parts of Zahhak & Fereydun (on top of audio.py). Some are copies of the Babak helpers
(babak/p02-p07_audio.py) so that this series does not import another series' modules."""
import numpy as np
from audio import SR, rng, env, bandpass, lowpass, highpass, stereo, place, drum, bell, noise_bed, pluck_fast, shur, drone, pad

# a short motif for the series (Shur on D; the koron second gives it its colour)
ZTHEME = [(0, 0), (1, 0.45), (2, 0.9), (3, 1.5), (2, 2.1), (1, 2.5), (0, 3.2)]


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
