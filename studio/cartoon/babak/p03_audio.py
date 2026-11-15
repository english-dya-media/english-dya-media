"""Part 3 · Twenty Years of Fire — timing, music and sound. Scene starts: s1 0, s2 13.0, s3 17.6, s4 57.0, s5 93.6, end 121.0"""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import series; series.from_folder(__file__)
from paths import AUDIO
from audio import *
from mix import build
from p02_audio import chirp, snort, clash, whoosh, tanbur, THEME
TOTAL = 121.0
S = {"s1": 0.0, "s2": 13.0, "s3": 17.6, "s4": 57.0, "s5": 93.6}


def thud(amp=0.3, f0=70, seed=0):
    r = np.random.default_rng(seed)
    n = int(0.5 * SR); t = np.arange(n) / SR
    body = np.sin(2 * np.pi * f0 * t * (1 + 0.5 * np.exp(-t * 30))) * np.exp(-t * 14)
    nz = lowpass(r.standard_normal(n).astype(np.float32), 700) * np.exp(-t * 25)
    return ((body + 0.6 * nz) * amp).astype(np.float32)


def splash(amp=0.25, seed=0):
    r = np.random.default_rng(seed)
    n = int(0.7 * SR); t = np.arange(n) / SR
    x = bandpass(r.standard_normal(n).astype(np.float32), 300, 2600) * np.exp(-t * 7) * (0.6 + 0.4 * np.sin(2 * np.pi * 23 * t))
    return (x * amp * 2.5).astype(np.float32)


def hooves(m, t0, t1, step=0.42, amp=0.07, pan=0.2, seed=0):
    r = np.random.default_rng(seed)
    t = t0
    while t < t1:
        for k, dt in enumerate((0.0, 0.11)):
            n = int(0.09 * SR); tt = np.arange(n) / SR
            x = bandpass(r.standard_normal(n).astype(np.float32), 500, 3000) * np.exp(-tt * 70)
            x += np.sin(2 * np.pi * (180 + 40 * k) * tt) * np.exp(-tt * 50) * 0.5
            place(m, (x * amp * r.uniform(0.7, 1.1)).astype(np.float32), t + dt, pan=pan)
        t += step


def steps(m, t0, t1, step=0.5, amp=0.05, seed=0, pan=0.0):
    r = np.random.default_rng(seed)
    t = t0
    while t < t1:
        n = int(0.12 * SR); tt = np.arange(n) / SR
        x = lowpass(r.standard_normal(n).astype(np.float32), 1200) * np.exp(-tt * 35)
        place(m, (x * amp * r.uniform(0.6, 1.0)).astype(np.float32), t + r.uniform(-0.04, 0.04), pan=pan + r.uniform(-0.3, 0.3))
        t += step


def rumble(dur, amp=0.3, seed=0, a=0.3, r_=1.5):
    r = np.random.default_rng(seed)
    n = int(dur * SR)
    x = lowpass(r.standard_normal(n).astype(np.float32), 160, order=4)
    x = x / (np.abs(x).max() + 1e-6)
    return stereo(x * env(n, a, r_) * amp, 0)


def rockfall(m, t0, dur, amp=0.25, seed=0):
    place(m, rumble(dur, amp, seed), t0)
    r = np.random.default_rng(seed + 1)
    for k in range(int(dur * 5)):
        place(m, thud(amp * r.uniform(0.4, 1.0), f0=r.uniform(45, 90), seed=seed + k), t0 + r.uniform(0, dur - 0.3), pan=r.uniform(-0.6, 0.6))


def cheer(dur, amp=0.12, seed=0):
    x = noise_bed(dur, amp=amp, lo=350, hi=2600, lfo=2.2, seed=seed)
    n = len(x)
    return x * env(n, 0.5, 1.2)[:, None]


def scrape(dur=0.6, amp=0.08, seed=0):
    r = np.random.default_rng(seed)
    n = int(dur * SR); t = np.arange(n) / SR
    x = bandpass(r.standard_normal(n).astype(np.float32), 1200, 5000) * (0.5 + 0.5 * np.sin(2 * np.pi * 9 * t)) * env(n, 0.05, 0.15)
    return (x * amp * 2).astype(np.float32)


def swish(dur=0.6, amp=0.12, seed=0):
    r = np.random.default_rng(seed)
    n = int(dur * SR); t = np.arange(n) / SR
    x = bandpass(r.standard_normal(n).astype(np.float32), 400, 4000) * np.sin(np.pi * t / dur) ** 2
    return (x * amp * 2).astype(np.float32)


def snap(amp=0.3):
    n = int(0.25 * SR); t = np.arange(n) / SR
    x = highpass(rng.standard_normal(n).astype(np.float32), 1500) * np.exp(-t * 45)
    x += np.sin(2 * np.pi * 140 * t) * np.exp(-t * 30) * 0.5
    return (x * amp).astype(np.float32)


def music(m):
    # S1 0-13: the pass. low drone, a slow march drum, tension; a shimmer when the red cloth shows
    place(m, drone(36.71, 13.4, amp=0.12, a=2.0, r=0.6), 0)
    place(m, drone(73.42, 12.8, amp=0.05, a=3.0, r=1.0), 0.3)
    for i, t in enumerate(np.arange(0.4, 12.5, 0.8)):
        place(m, drum(dur=0.8, f0=56, amp=0.16 + (0.06 if i % 4 == 0 else 0), noise=0.15), t)
    place(m, pad([shur(0, -1), shur(1, -1), shur(4, -1)], 8.0, amp=0.06, a=3.0, r=0.5, bright=4), 4.6)
    place(m, bell(880, 2.4, 0.05), 8.6); place(m, bell(1318, 2.0, 0.03), 8.75)
    place(m, pad([shur(0), shur(1)], 4.0, amp=0.05, a=0.3, r=1.0, bright=3), 8.4)
    # S2 13.0-17.6: title hit and the theme
    place(m, drum(dur=2.8, f0=46, amp=1.0, noise=0.45), 13.0)
    place(m, drone(36.71, 4.8, amp=0.12, a=0.05, r=2.0), 13.0)
    tanbur(m, THEME[:6], 13.3, amp=0.24, low=True, step=0.8)
    # S3 17.6-57.0: the village. tanbur motif, tension at the tax collector, warmth when Babak speaks, drums when the spears go up
    place(m, drone(73.42, 8.5, amp=0.07, a=2, r=2), 17.6)
    tanbur(m, [(0, 0), (2, 0.6), (1, 1.0), (0, 1.4), (3, 2.4), (2, 3.0), (1, 3.4), (0, 4.2)], 18.4, amp=0.16)
    place(m, drone(38.89, 11.0, amp=0.09, a=1.0, r=1.5), 25.4)
    for t in np.arange(25.6, 36.0, 1.2):
        place(m, drum(dur=0.7, f0=64, amp=0.12, noise=0.1), t)
    place(m, pad([shur(1, -1), shur(3, -1)], 5.0, amp=0.06, a=1.0, r=1.0, bright=3), 29.0)
    place(m, pad([shur(0), shur(2), shur(4)], 14.0, amp=0.07, a=2.5, r=2.0, bright=5), 36.2)
    tanbur(m, [(4, 0), (3, 0.6), (2, 1.2), (0, 2.0)], 41.2, amp=0.13)
    place(m, pad([shur(0), shur(4), shur(0, 1)], 6.0, amp=0.07, a=1.5, r=2.0, bright=5), 46.0)
    place(m, drum(dur=2.2, f0=48, amp=0.7, noise=0.35), 50.0)
    for i, t in enumerate(np.arange(50.6, 56.4, 0.6)):
        place(m, drum(dur=0.7, f0=62 if i % 2 else 52, amp=0.22, noise=0.2), t)
    tanbur(m, THEME, 50.4, amp=0.22, low=True, step=0.9)
    place(m, pad([shur(0), shur(4), shur(0, 1)], 6.6, amp=0.09, a=1.0, r=2.5, bright=6), 50.4)
    # S4 57.0-93.6: montage, a war drum under it all
    place(m, drone(36.71, 36.6, amp=0.10, a=1.5, r=1.0), 57.0)
    for i, t in enumerate(np.arange(57.2, 88.0, 0.6)):
        if 67.2 <= t < 70.6:      # quiet under the map
            continue
        place(m, drum(dur=0.7, f0=58 if i % 2 else 50, amp=0.20 + (0.08 if i % 4 == 0 else 0), noise=0.2), t)
    place(m, pad([shur(0, -1), shur(4, -1)], 6.0, amp=0.07, a=1.0, r=1.0, bright=3), 57.0)
    tanbur(m, [(0, 0), (1, 0.5), (2, 1.0), (3, 1.6), (2, 2.2), (1, 2.6), (0, 3.2)], 63.4, amp=0.15)
    tanbur(m, [(4, 0), (3, 0.6), (2, 1.2), (0, 2.0)], 67.4, amp=0.12)
    place(m, drum(dur=2.0, f0=44, amp=0.8, noise=0.4), 70.6)
    place(m, pad([shur(1, -1), shur(3, -1), shur(5, -1)], 5.4, amp=0.06, a=0.5, r=1.0, bright=4), 70.6)
    place(m, pad([shur(0), shur(2), shur(4)], 5.0, amp=0.06, a=1.5, r=1.5, bright=4), 76.0)
    place(m, drum(dur=2.0, f0=48, amp=0.7, noise=0.35), 81.4)
    tanbur(m, THEME[:5], 81.8, amp=0.16, step=0.8)
    place(m, pad([shur(0), shur(4), shur(0, 1)], 5.6, amp=0.08, a=1.0, r=2.0, bright=5), 88.4)
    tanbur(m, [(0, 0), (4, 0.4), (0, 1.0)], 91.0, amp=0.2, low=True)
    # S5 93.6-121: the ambush. heartbeat, held breath, the order
    place(m, drone(36.71, 21.0, amp=0.13, a=1.0, r=0.4), 93.6)
    place(m, drone(38.89, 10.0, amp=0.05, a=3.0, r=1.0), 103.4)
    for i, t in enumerate(np.arange(93.8, 111.0, 1.0 if True else 0)):
        place(m, drum(dur=0.9, f0=52, amp=0.22 + 0.012 * i, noise=0.12), t)
    place(m, pad([shur(0, -1), shur(1, -1)], 7.0, amp=0.07, a=2.0, r=0.5, bright=3), 96.6)
    place(m, pad([shur(0, -1), shur(4, -1), shur(0)], 3.0, amp=0.10, a=0.2, r=1.0, bright=6), 100.8)   # "Forward!"
    for t in np.arange(108.2, 112.5, 0.5):
        place(m, drum(dur=0.6, f0=60, amp=0.30, noise=0.2), t)
    place(m, pad([shur(1), shur(5)], 3.5, amp=0.05, a=2.5, r=0.1, bright=2), 109.0)
    place(m, drum(dur=3.0, f0=42, amp=1.0, noise=0.5), 112.6)                                    # "Now!"
    place(m, drone(36.71, 8.5, amp=0.14, a=0.05, r=2.0), 112.6)
    place(m, drum(dur=3.0, f0=40, amp=1.0, noise=0.5), 116.6)
    tanbur(m, THEME[:5], 117.0, amp=0.18, low=True, step=0.8)
    place(m, pad([shur(0), shur(4), shur(0, 1)], 4.4, amp=0.07, a=0.5, r=2.0, bright=5), 116.6)


def sfx(s):
    # S1: wind in the pass, marching feet, harness
    place(s, noise_bed(13.2, amp=0.07, lo=250, hi=2400, lfo=0.25, seed=41), 0)
    steps(s, 0.2, 12.8, step=0.4, amp=0.05, seed=1)
    for t in (1.2, 3.1, 6.4, 9.0, 11.2):
        place(s, clash(0.03, seed=int(t * 10)), t, pan=0.3)
    place(s, swish(1.4, amp=0.06, seed=5), 8.0)
    # S2: wind on the ridge
    place(s, noise_bed(4.8, amp=0.12, lo=300, hi=3200, lfo=0.6, seed=42), 13.0)
    # S3: village
    place(s, noise_bed(39.0, amp=0.035, lo=300, hi=2000, lfo=0.4, seed=43), 17.6)
    for k, t in enumerate((18.8, 21.0, 22.6, 24.4)):
        place(s, thud(0.16, 80, seed=k), t, pan=0.3)                     # sacks thrown on the mules
    for k, t in enumerate((19.6, 23.4, 31.0, 47.6)):
        place(s, chirp(2600 + 300 * (k % 3), amp=0.03), t, pan=-0.5)
    place(s, snort(seed=4, amp=0.09), 20.4, pan=0.4); place(s, snort(seed=5, amp=0.07), 33.0, pan=0.5)
    place(s, swish(0.7, amp=0.12, seed=6), 30.0)                          # the push
    place(s, thud(0.32, 60, seed=9), 30.6); place(s, splash(0.22, seed=3), 30.62)
    steps(s, 32.0, 33.6, step=0.42, amp=0.06, seed=2, pan=0.4)
    place(s, cheer(5.4, amp=0.09, seed=44), 51.0)
    steps(s, 51.0, 56.0, step=0.3, amp=0.05, seed=3)
    # S4: snow wind, camp, rockslide, the courtyard
    place(s, noise_bed(6.2, amp=0.20, lo=200, hi=3600, lfo=0.5, seed=45), 57.0)
    hooves(s, 57.2, 62.8, step=0.6, amp=0.05, pan=0.2, seed=4)
    place(s, snort(seed=6, amp=0.09), 59.8, pan=0.3)
    place(s, noise_bed(7.6, amp=0.04, lo=300, hi=2500, lfo=0.3, seed=46), 63.0)
    for k, t in enumerate((63.8, 65.2, 67.4, 68.3, 69.2)):
        place(s, scrape(0.5, 0.07, seed=k), t)                             # the stick in the dirt
    rockfall(s, 71.0, 5.0, amp=0.32, seed=7)
    place(s, noise_bed(5.4, amp=0.03, lo=300, hi=2500, lfo=0.3, seed=47), 76.0)
    place(s, noise_bed(7.2, amp=0.06, lo=300, hi=2200, lfo=1.2, seed=48), 81.4)
    steps(s, 81.6, 84.8, step=0.5, amp=0.06, seed=5)
    place(s, noise_bed(5.2, amp=0.04, lo=300, hi=2500, lfo=0.3, seed=49), 88.4)
    # S5: the army in the gorge, the ridge, the rope
    place(s, noise_bed(10.0, amp=0.06, lo=250, hi=2400, lfo=0.25, seed=50), 93.6)
    steps(s, 93.7, 96.5, step=0.4, amp=0.05, seed=6)
    hooves(s, 96.6, 103.3, step=0.55, amp=0.07, pan=0.1, seed=8)
    place(s, snort(seed=7, amp=0.08), 98.0, pan=0.2)
    place(s, clash(0.06, seed=3), 100.9)                                    # the sword comes out
    place(s, noise_bed(10.6, amp=0.10, lo=300, hi=3600, lfo=0.4, seed=51), 103.4)
    steps(s, 108.3, 111.1, step=0.4, amp=0.035, seed=9)
    place(s, swish(0.5, amp=0.16, seed=8), 114.5)                         # the blade
    place(s, snap(0.35), 114.95)
    rockfall(s, 115.6, 5.4, amp=0.36, seed=12)
    place(s, noise_bed(4.0, amp=0.08, lo=200, hi=1600, lfo=0.3, seed=52), 117.0)


LINES = [("p3s1a", 5.1), ("p3s1b", 10.4),
         ("p3s3a", 18.3), ("p3s3b", 25.8), ("p3s3c", 36.7), ("p3s3d", 38.8), ("p3s3e", 42.9), ("p3s3f", 46.4),
         ("p3s4a", 63.5), ("p3s4b", 67.5), ("p3s4c", 76.3), ("p3s4d", 79.3), ("p3s4e", 85.6), ("p3s4f", 89.0),
         ("p3s5a", 97.2), ("p3s5b", 99.4), ("p3s5c", 104.4), ("p3s5d", 112.6)]
if __name__ == "__main__":
    build(3, TOTAL, music, sfx, LINES, f'{AUDIO}/part03.wav')
    print('done')
