import os, sys; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import series; series.from_folder(__file__)
from paths import AUDIO
from audio import *
from mix import build
TOTAL = 124.0

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

def clash(amp=0.14, seed=0):
    r = np.random.default_rng(seed)
    n = int(0.12 * SR); t = np.arange(n) / SR
    nz = highpass(r.standard_normal(n).astype(np.float32), 2500) * np.exp(-t * 40)
    b = bell(f=2300 + 400 * r.random(), dur=0.6, amp=amp)
    b[:n] += nz * amp * 1.5
    return b

def puff(amp=0.12):
    n = int(0.45 * SR); t = np.arange(n) / SR
    x = lowpass(rng.standard_normal(n).astype(np.float32), 900)
    return (x * np.minimum(1, t / 0.02) * np.exp(-t * 9) * amp * 3).astype(np.float32)

def whoosh(dur=1.6, amp=0.12, seed=3):
    x = noise_bed(dur, amp=amp, lo=300, hi=3200, lfo=0.3, seed=seed)
    ramp = np.linspace(0, 1, len(x)) ** 2
    return x * ramp[:, None]

def tanbur(m, notes, t0, amp=0.2, pan=0.2, low=False, step=1.0, dur=2.2):
    for deg, dt in notes:
        place(m, pluck_fast(shur(deg), dur, amp=amp), t0 + dt * step, pan=pan)
        if low and dt == 0:
            place(m, pluck_fast(shur(deg, -1), dur, amp=amp * 0.6), t0 + dt * step, pan=-pan)

THEME = [(0, 0), (2, 0.5), (3, 1.0), (4, 1.5), (4, 2.25), (3, 2.75), (2, 3.25), (3, 3.75), (4, 4.5)]

def music(m):
    # S7 0-27: warm room / storm / bread
    place(m, drone(73.42, 9.3, amp=0.07, a=2, r=1.2), 0)
    tanbur(m, [(0, 0), (2, 0.7), (1, 1.2), (0, 1.8)], 1.0, amp=0.18)
    tanbur(m, [(3, 0), (2, 0.6), (1, 1.0), (0, 1.6)], 6.4, amp=0.12)
    place(m, drone(55.0, 7.5, amp=0.10, a=1.0, r=1.5), 9.0)
    place(m, pad([shur(0, -1), shur(2, -1)], 7.2, amp=0.07, a=2, r=1.5, bright=4), 9.0)
    place(m, drone(73.42, 11.3, amp=0.06, a=2, r=2), 16.0)
    place(m, pad([shur(0), shur(4)], 9.0, amp=0.05, a=3, r=2.5, bright=4), 18.0)
    tanbur(m, [(0, 0), (1, 0.5), (2, 1.0), (3, 1.6), (2, 2.2), (1, 2.6), (0, 3.2)], 23.8, amp=0.2, low=True)
    # S8 27-49: dawn and the offer
    place(m, pad([shur(0), shur(4), shur(0, 1)], 22.5, amp=0.08, a=3, r=3, bright=5), 27.0)
    tanbur(m, [(4, 0), (3, 0.8), (2, 1.4), (3, 2.2), (2, 3.0), (1, 3.6), (0, 4.4)], 27.6, amp=0.16, step=0.9)
    for t in (36.6, 38.6, 40.6):
        place(m, drum(dur=1.2, f0=60, amp=0.18, noise=0.05), t)
    place(m, pad([shur(2), shur(4), shur(0, 1)], 6.0, amp=0.07, a=2, r=2, bright=4), 37.0)
    tanbur(m, [(4, 0), (3, 0.6), (2, 1.2), (1, 1.8), (0, 2.6)], 45.3, amp=0.22, low=True)
    # S9 49-77: Bazz, the battle, the deathbed
    place(m, drone(36.71, 12.5, amp=0.16, a=1.5, r=0.3), 49.0)
    place(m, pad([shur(0, -1), shur(4, -1), shur(0)], 12.0, amp=0.11, a=2, r=0.3, bright=6), 49.0)
    for i, t in enumerate(np.arange(49.6, 58.0, 0.75)):
        place(m, drum(dur=0.9, f0=55, amp=0.30 + (0.12 if i % 4 == 0 else 0), noise=0.2), t)
    t = 52.0
    while t < 58.0:
        for i, deg in enumerate([0, 0, 2, 0, 3, 2, 1, 0]):
            place(m, pluck_fast(shur(deg), 0.9, amp=0.14), t + i * 0.1875, pan=0.3)
        t += 1.5
    for i, t in enumerate(np.arange(58.0, 61.0, 0.375)):
        place(m, drum(dur=0.6, f0=62 if i % 2 else 50, amp=0.38, noise=0.3), t)
    place(m, drum(dur=3.2, f0=40, amp=1.0, noise=0.5), 61.1)
    place(m, drone(36.71, 4.5, amp=0.08, a=0.05, r=3.5), 61.1)
    place(m, drone(73.42, 13.0, amp=0.05, a=2, r=3), 64.0)
    tanbur(m, [(0, 0)], 64.6, amp=0.13)
    tanbur(m, [(1, 0), (0, 0.8)], 72.0, amp=0.12)
    place(m, bell(220, 3.0, 0.05), 74.3)
    # S10 77-96: the successor
    place(m, pad([shur(0), shur(2), shur(4)], 15.0, amp=0.07, a=3, r=2, bright=5), 78.5)
    for t in np.arange(77.5, 92.0, 1.5):
        place(m, drum(dur=0.8, f0=70, amp=0.16, noise=0.15), t)
    place(m, pad([shur(0), shur(4), shur(0, 1)], 6.0, amp=0.09, a=1.5, r=2.5, bright=5), 84.8)
    place(m, drum(dur=2.4, f0=48, amp=0.75, noise=0.35), 92.0)
    place(m, pad([shur(0), shur(2), shur(4), shur(0, 1)], 4.5, amp=0.12, a=0.3, r=3, bright=6), 92.0)
    tanbur(m, [(0, 0), (4, 0.4), (0, 1.0)], 92.1, amp=0.24, low=True)
    # S11 96-124: the oath on the wall, the empty throne, the end card
    place(m, drone(36.71, 14.3, amp=0.12, a=2, r=0.5), 96.0)
    for i, t in enumerate(np.arange(96.5, 110.0, 1.0)):
        place(m, drum(dur=1.0, f0=58, amp=0.26 + (0.08 if i % 4 == 0 else 0), noise=0.2), t)
    tanbur(m, THEME, 96.8, amp=0.22, low=True)
    place(m, pad([shur(0), shur(4), shur(0, 1)], 11.0, amp=0.10, a=3, r=1.0, bright=6), 99.0)
    tanbur(m, THEME, 102.3, amp=0.13)
    tanbur(m, THEME[:5], 106.8, amp=0.15)
    place(m, drum(dur=3.0, f0=40, amp=0.9, noise=0.4), 110.0)
    place(m, drone(36.71, 7.5, amp=0.12, a=0.1, r=1.5), 110.0)
    place(m, drone(38.89, 7.5, amp=0.06, a=2.0, r=1.5), 110.0)
    place(m, pad([shur(1, -1), shur(0, -1)], 7.0, amp=0.07, a=2.5, r=1.0, bright=4), 110.2)
    place(m, pad([shur(0), shur(4), shur(0, 1)], 6.5, amp=0.08, a=2.0, r=3.0, bright=5), 117.4)
    place(m, drum(dur=2.5, f0=46, amp=0.9, noise=0.4), 119.3)
    place(m, pluck_fast(shur(0), 3.0, amp=0.3), 119.4)
    tanbur(m, [(4, 0), (3, 0.5), (2, 1.0), (0, 1.8)], 120.6, amp=0.14)

def sfx(s):
    place(s, crackle(9.2, amp=0.14, seed=21), 0)
    place(s, noise_bed(9.2, amp=0.025, lo=200, hi=1200, lfo=0.2, seed=22), 0)
    place(s, noise_bed(7.4, amp=0.24, lo=200, hi=3200, lfo=0.3, seed=23), 9.0)
    place(s, snort(seed=1), 11.4, pan=0.3); place(s, snort(seed=2, amp=0.1), 13.9, pan=0.45)
    place(s, knock(0.55), 16.05, pan=0.35)
    place(s, noise_bed(1.6, amp=0.12, lo=200, hi=3000, lfo=0.5, seed=24), 15.7)
    place(s, crackle(11.0, amp=0.14, seed=25), 16.0)
    place(s, noise_bed(22.0, amp=0.04, lo=300, hi=2500, lfo=0.15, seed=26), 27.0)
    for k, t in enumerate((28.4, 28.6, 29.5, 31.1, 31.3, 38.2, 42.6, 42.8, 47.0)):
        place(s, chirp(2900 + 300 * (k % 3), amp=0.045), t, pan=0.5 - 0.25 * (k % 4))
    place(s, snort(seed=3, amp=0.07), 40.0, pan=0.6)
    place(s, whoosh(1.8, amp=0.12), 47.3)
    place(s, noise_bed(9.2, amp=0.12, lo=400, hi=4000, lfo=0.4, seed=27), 49.0)
    place(s, noise_bed(6.2, amp=0.20, lo=150, hi=1200, lfo=1.6, seed=28), 58.0)
    for k, t in enumerate((58.6, 59.1, 59.5, 60.2, 60.7, 61.0)):
        place(s, clash(0.13, seed=k), t, pan=(-0.4 if k % 2 else 0.4))
    place(s, noise_bed(13.0, amp=0.025, lo=100, hi=600, lfo=0.1, seed=29), 64.0)
    place(s, puff(0.13), 74.0)
    place(s, noise_bed(19.0, amp=0.07, lo=200, hi=1400, lfo=0.5, seed=30), 77.0)
    place(s, noise_bed(3.5, amp=0.20, lo=200, hi=2200, lfo=1.0, seed=31), 92.3)
    place(s, noise_bed(14.2, amp=0.08, lo=300, hi=3500, lfo=0.3, seed=32), 96.0)
    for t in np.arange(96.4, 110.0, 0.62):
        n = int(0.18 * SR)
        x = bandpass(rng.standard_normal(n).astype(np.float32), 400, 2500) * np.exp(-np.arange(n) / SR * 25) * 0.05
        place(s, x, t, pan=-0.4)
    place(s, noise_bed(7.0, amp=0.03, lo=80, hi=400, lfo=0.1, seed=33), 110.0)
    place(s, whoosh(2.0, amp=0.08, seed=4), 115.2)
    place(s, noise_bed(7.0, amp=0.07, lo=400, hi=4000, lfo=0.3, seed=34), 117.0)

LINES = [("p2s7a", 3.5), ("p2s7b", 6.6), ("p2s7c", 17.8), ("p2s7d", 20.3),
         ("p2s8a", 30.0), ("p2s8b", 33.4), ("p2s8c", 36.6), ("p2s8d", 44.0),
         ("p2s9a", 66.0), ("p2s9b", 70.0),
         ("p2s10a", 79.5), ("p2s10b", 84.8), ("p2s10c", 88.8),
         ("p2s11a", 99.0), ("p2s11b", 102.5), ("p2s11c", 111.0)]
if __name__ == "__main__":
    build(2, TOTAL, music, sfx, LINES, f'{AUDIO}/part02.wav')
    print('done')
