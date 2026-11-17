"""Part 2 · The King's Cook — timing, music and sound.
Scene starts: s1 0 (hook: the cook's one small wish), s2 8.0 (title), s3 12.6 (the empty garden; Zahhak on his father's throne; the cook
comes; the keys), s4 33.8 (only plants in those days; the kitchen; the four meals), s5 73.0 (the wish, the kiss, the cook vanishes),
s6 97.4 (the snakes), end card 115.4, end 120.4"""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import series; series.from_folder(__file__)
from paths import AUDIO
from audio import *
from mix import build
from zsfx import *
from p01_audio import SLY, daf
TOTAL = 120.4
S = {"s1": 0.0, "s2": 8.0, "s3": 12.6, "s4": 33.8, "s5": 73.0, "s6": 97.4}
END_CARD = 115.4


def keys(m, t0, amp=0.03, pan=0.1, seed=0):
    """a ring of keys jingling"""
    r = np.random.default_rng(seed)
    for k in range(9):
        place(m, bell(1800 + 1600 * r.random(), 0.4, amp * r.uniform(0.6, 1.0)), t0 + 0.03 * k + r.uniform(0, 0.02), pan=pan + r.uniform(-0.2, 0.2))


def sizzle(dur=2.0, amp=0.04, seed=0):
    x = noise_bed(dur, amp=amp, lo=2500, hi=8000, lfo=3.0, seed=seed)
    return x


def gasp(amp=0.12, seed=0):
    """a crowd catching its breath at once"""
    r = np.random.default_rng(seed)
    n = int(0.7 * SR); t = np.arange(n) / SR
    x = bandpass(r.standard_normal(n).astype(np.float32), 700, 4200) * np.minimum(1, t / 0.05) * np.exp(-t * 5)
    return (x * amp * 3).astype(np.float32)


def music(m):
    # S1 0-8.0: the cook's wish — low drone, the sly plucks, a bell
    place(m, drone(36.71, 8.4, amp=0.12, a=1.0, r=0.6), 0.0)
    place(m, pad([shur(1, -1), shur(0, -1)], 7.6, amp=0.05, a=2.0, r=1.0, bright=4), 0.3)
    for deg, dt in SLY:
        place(m, pluck_fast(shur(deg), 0.6, amp=0.10), 0.6 + dt, pan=0.35)
    place(m, bell(196, 3.0, 0.05), 6.9)
    # S2 8.0-12.6: title
    place(m, drum(dur=3.2, f0=40, amp=0.9, noise=0.4), 8.0)
    place(m, drone(36.71, 4.9, amp=0.12, a=0.1, r=1.4), 8.0)
    place(m, pad([shur(0), shur(4), shur(0, 1)], 4.8, amp=0.10, a=0.4, r=1.6, bright=6), 8.0)
    tanbur(m, ZTHEME, 8.4, amp=0.22, low=True, step=0.85)
    # S3 12.6-33.8: the empty garden, the new king, the cook
    place(m, pad([shur(0, -1), shur(3, -1)], 4.2, amp=0.06, a=1.0, r=1.5, bright=4), 12.6)
    tanbur(m, [(2, 0), (1, 0.8), (0, 1.6)], 13.2, amp=0.09)
    place(m, drum(dur=1.6, f0=60, amp=0.3, noise=0.2), 16.4)
    place(m, pad([shur(0), shur(4), shur(0, 1)], 4.4, amp=0.08, a=0.5, r=1.5, bright=6), 16.4)
    tanbur(m, [(0, 0), (4, 0.4), (0, 1.0)], 16.6, amp=0.18, low=True)
    place(m, drone(36.71, 13.2, amp=0.05, a=1.5, r=1.0), 20.6)
    for t0 in (20.8, 23.8, 27.4):
        for deg, dt in SLY:
            place(m, pluck_fast(shur(deg), 0.6, amp=0.09), t0 + dt, pan=0.35)
    place(m, bell(784, 2.0, 0.04), 31.6)
    # S4 33.8-73.0: plants, the kitchen, four meals
    place(m, pad([shur(0), shur(2), shur(4)], 6.8, amp=0.06, a=1.5, r=1.5, bright=5), 33.8)
    tanbur(m, [(0, 0), (2, 0.6), (4, 1.2), (2, 1.9), (0, 2.6)], 34.4, amp=0.11)
    place(m, drone(36.71, 3.8, amp=0.08, a=0.5, r=0.6), 40.6)
    for deg, dt in SLY:
        place(m, pluck_fast(shur(deg, -1), 0.7, amp=0.11), 40.8 + dt, pan=-0.2)
    daf(m, 44.4, 67.2, bpm=112, amp=0.13)
    place(m, drone(73.42, 22.8, amp=0.04, a=1.0, r=1.0), 44.4)
    t = 44.6
    while t < 66.8:
        for i, deg in enumerate([0, 2, 4, 3, 2, 3, 4, 2]):
            place(m, pluck_fast(shur(deg), 0.9, amp=0.09), t + i * 0.268, pan=0.3)
        t += 2.14
    for t in (44.4, 53.0, 59.0, 61.6):
        place(m, bell(988, 1.6, 0.045), t)
    place(m, pad([shur(0), shur(4), shur(0, 1)], 5.8, amp=0.09, a=0.4, r=2.0, bright=6), 67.2)
    tanbur(m, ZTHEME[:4], 67.4, amp=0.15, low=True, step=0.8)
    # S5 73.0-97.4: the wish, the kiss, the vanishing
    place(m, drone(36.71, 11.2, amp=0.07, a=1.5, r=1.0), 73.0)
    place(m, pad([shur(1, -1), shur(0, -1)], 11.2, amp=0.05, a=2.0, r=1.0, bright=4), 73.0)
    for t0 in (73.4, 77.0):
        for deg, dt in SLY:
            place(m, pluck_fast(shur(deg), 0.6, amp=0.08), t0 + dt * 1.2, pan=0.35)
    place(m, bell(1175, 2.5, 0.035), 85.2); place(m, bell(1047, 2.5, 0.035), 87.6)
    place(m, drone(55.0, 4.4, amp=0.06, a=2.0, r=0.3), 84.2)
    place(m, drum(dur=3.0, f0=38, amp=0.8, noise=0.45), 91.0)
    place(m, pad([shur(1, -1), shur(5, -1)], 3.0, amp=0.07, a=0.2, r=2.0, bright=5), 91.0)
    # S6 97.4-120.4: the snakes
    heartbeat(m, 97.6, 102.4, bpm=84, amp=0.26)
    place(m, drone(36.71, 18.0, amp=0.12, a=1.0, r=1.0), 97.4)
    place(m, pad([shur(0, -1), shur(1, -1), shur(4, -1)], 7.0, amp=0.07, a=1.5, r=0.5, bright=5), 102.4)
    place(m, drum(dur=3.0, f0=40, amp=0.85, noise=0.4), 103.4)
    tanbur(m, ZTHEME, 109.6, amp=0.12, low=True, step=0.9)
    place(m, drum(dur=3.0, f0=40, amp=0.75, noise=0.4), 115.4)
    place(m, drone(36.71, 5.0, amp=0.10, a=0.2, r=2.0), 115.4)
    place(m, pad([shur(0), shur(4), shur(0, 1)], 5.0, amp=0.08, a=0.6, r=2.0, bright=5), 115.4)
    tanbur(m, ZTHEME[:4], 116.0, amp=0.14, low=True, step=0.9)


def sfx(s):
    place(s, noise_bed(8.0, amp=0.02, lo=150, hi=900, lfo=0.15, seed=201), 0.0)
    place(s, rustle(0.04, 0.8, seed=1), 0.6)
    # S3: dawn birds over the empty garden; the court; the cook; the keys
    for k, t in enumerate((12.9, 13.8, 14.9, 15.6)):
        place(s, chirp(3000 + 250 * (k % 3), amp=0.03), t, pan=0.4 - 0.25 * k)
    place(s, noise_bed(17.2, amp=0.03, lo=300, hi=2000, lfo=0.8, seed=202), 16.4)
    steps(s, 20.6, 22.6, step=0.5, amp=0.04, seed=21, pan=0.3)
    place(s, rustle(0.05, 0.7, seed=2), 22.8)
    keys(s, 29.9, amp=0.035, seed=1); keys(s, 31.5, amp=0.04, seed=2)
    # S4: kitchen fire and the pot; sizzling dishes
    place(s, crackle(4.0, amp=0.10, rate=10, seed=203), 40.6)
    place(s, noise_bed(3.8, amp=0.04, lo=200, hi=900, lfo=2.5, seed=204), 40.6)
    for t, d in ((44.4, 3.8), (53.0, 2.8), (59.0, 2.4), (61.6, 5.4)):
        place(s, sizzle(d, amp=0.03, seed=int(t)), t)
    place(s, noise_bed(28.8, amp=0.02, lo=300, hi=2000, lfo=1.0, seed=205), 44.4)
    # S5: the kisses, the vanishing
    place(s, rustle(0.05, 0.6, seed=3), 84.6); place(s, rustle(0.05, 0.6, seed=4), 87.0)
    place(s, whoosh(2.2, amp=0.16, seed=5), 89.4)
    place(s, noise_bed(2.6, amp=0.12, lo=60, hi=400, lfo=0.2, seed=206), 90.8)
    place(s, noise_bed(4.0, amp=0.02, lo=200, hi=1200, lfo=0.2, seed=207), 93.4)
    # S6: the snakes
    place(s, rustle(0.06, 1.0, seed=5), 98.2); place(s, rustle(0.06, 0.8, seed=6), 99.8)
    place(s, hiss(1.6, 0.07, seed=4), 103.4, pan=-0.3); place(s, hiss(1.8, 0.08, seed=5), 104.0, pan=0.3)
    place(s, gasp(0.12, seed=1), 109.6)
    place(s, noise_bed(6.0, amp=0.04, lo=300, hi=2400, lfo=1.2, seed=208), 109.4)
    place(s, hiss(1.4, 0.06, seed=6), 111.6, pan=0.2)
    place(s, noise_bed(5.0, amp=0.03, lo=200, hi=1500, lfo=0.2, seed=209), 115.4)


LINES = [("p2s1a", 1.0), ("p2s1b", 4.8),
         ("p2s3a", 13.1), ("p2s3b", 16.8), ("p2s3c", 21.0), ("p2s3d", 25.9), ("p2s3e", 28.0),
         ("p2s4a", 34.2), ("p2s4b", 40.9), ("p2s4c", 44.7), ("p2s4d", 48.8), ("p2s4e", 53.3), ("p2s4f", 56.3), ("p2s4g", 59.3),
         ("p2s4h", 61.9), ("p2s4i", 67.6),
         ("p2s5a", 73.4), ("p2s5b", 77.2), ("p2s5c", 80.7), ("p2s5d", 93.8),
         ("p2s6a", 104.8), ("p2s6b", 109.8)]
if __name__ == "__main__":
    build(2, TOTAL, music, sfx, LINES, f'{AUDIO}/part02.wav')
    print('done')
