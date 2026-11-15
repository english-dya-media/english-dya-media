"""Part 6 · The Fall of Bazz — timing, music and sound. Scene starts: s1 0, s2 6.6, s3 11.2, s4 36.6, s5 73.4, s6 100.8, end card 120.0, end 124.4"""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import series; series.from_folder(__file__)
from paths import AUDIO
from audio import *
from mix import build
from p02_audio import chirp, snort, clash, tanbur, THEME
from p03_audio import thud, hooves, steps, rumble, rockfall, cheer, scrape, swish
from p04_audio import arrow, neigh, water
from p05_audio import coins, heartbeat, breath, horn
TOTAL = 124.4
S = {"s1": 0.0, "s2": 6.6, "s3": 11.2, "s4": 36.6, "s5": 73.4, "s6": 100.8}
END_CARD = 120.0


def creak(dur=1.2, amp=0.08, seed=0):
    """a heavy wooden door turning on its hinges"""
    r = np.random.default_rng(seed)
    n = int(dur * SR); t = np.arange(n) / SR
    f = 180 + 60 * np.sin(2 * np.pi * 0.7 * t) + 40 * r.standard_normal(n).cumsum() / np.sqrt(n)
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * (0.5 + 0.5 * np.sin(2 * np.pi * 23 * t)) * env(n, 0.1, 0.3)
    return bandpass((x * amp).astype(np.float32), 200, 2200)


def crash(amp=0.4, seed=0):
    """stone walls coming down"""
    r = np.random.default_rng(seed)
    n = int(2.4 * SR); t = np.arange(n) / SR
    x = lowpass(r.standard_normal(n).astype(np.float32), 900) * np.exp(-t * 1.6)
    return (x / (np.abs(x).max() + 1e-6) * amp).astype(np.float32)


def music(m):
    # S1 0-6.6: the hook, Bazz burning
    place(m, drum(dur=3.0, f0=40, amp=1.0, noise=0.5), 0.0)
    place(m, drone(36.71, 6.6, amp=0.12, a=0.1, r=1.5), 0.0)
    place(m, pad([shur(1, -1), shur(3, -1), shur(5, -1)], 6.4, amp=0.08, a=0.4, r=1.5, bright=4), 0.2)
    place(m, drum(dur=2.4, f0=44, amp=0.7, noise=0.3), 3.8)
    # S2 6.6-11.2: title
    place(m, drum(dur=3.0, f0=42, amp=1.0, noise=0.45), 6.6)
    tanbur(m, THEME[:6], 6.9, amp=0.22, low=True, step=0.8)
    place(m, drone(73.42, 4.8, amp=0.09, a=0.05, r=2.0), 6.6)
    # S3 11.2-36.6: mist and the ambush; Bazz by candlelight; the rider at the gate
    place(m, drone(36.71, 11.8, amp=0.09, a=1.5, r=1.0), 11.2)
    for i, t in enumerate(np.arange(11.4, 15.8, 1.1)):
        place(m, drum(dur=0.9, f0=56, amp=0.18, noise=0.2), t)
    for i, t in enumerate(np.arange(15.8, 21.0, 0.375)):
        place(m, drum(dur=0.6, f0=62 if i % 2 else 50, amp=0.32, noise=0.3), t)
    place(m, pad([shur(0), shur(4), shur(0, 1)], 5.0, amp=0.07, a=0.5, r=2.0, bright=5), 16.0)
    tanbur(m, THEME[:5], 16.3, amp=0.18, low=True, step=0.7)
    place(m, drum(dur=2.5, f0=44, amp=0.8, noise=0.4), 20.2)
    place(m, pad([shur(0, -1), shur(2, -1), shur(4, -1)], 13.6, amp=0.06, a=2.5, r=2.0, bright=3), 23.0)
    tanbur(m, [(0, 0), (2, 0.7), (1, 1.2), (0, 1.8)], 23.4, amp=0.12)
    tanbur(m, [(4, 0), (3, 0.6), (2, 1.2), (0, 2.0)], 32.8, amp=0.12)
    # S4 36.6-73.4: the fall
    place(m, drone(36.71, 9.4, amp=0.10, a=1.5, r=1.0), 36.6)
    for i, t in enumerate(np.arange(36.8, 46.0, 1.2)):
        place(m, drum(dur=1.0, f0=55, amp=0.20 + (0.06 if i % 4 == 0 else 0), noise=0.2), t)
    place(m, horn(2.6, 0.10, 98.0), 37.2)
    place(m, pad([shur(1, -1), shur(3, -1), shur(5, -1)], 9.0, amp=0.07, a=1.0, r=2.0, bright=4), 41.0)
    place(m, drone(38.89, 9.0, amp=0.06, a=2.0, r=1.0), 41.4)
    for i, t in enumerate(np.arange(50.6, 60.4, 0.32)):
        place(m, drum(dur=0.6, f0=58 if i % 2 else 46, amp=0.30 + 0.01 * i, noise=0.35), t)
    place(m, pad([shur(1, -1), shur(3, -1), shur(5, -1)], 10.0, amp=0.08, a=0.5, r=1.5, bright=5), 50.6)
    place(m, drum(dur=3.0, f0=40, amp=1.0, noise=0.5), 57.8)
    place(m, drone(36.71, 10.8, amp=0.12, a=0.2, r=1.5), 57.8)
    place(m, pad([shur(0, -1), shur(1, -1), shur(3, -1)], 10.4, amp=0.06, a=1.0, r=2.0, bright=3), 63.0)
    place(m, drone(36.71, 4.8, amp=0.08, a=1.0, r=2.0), 68.6)
    tanbur(m, [(4, 0), (3, 0.9), (1, 1.8), (0, 2.8)], 69.0, amp=0.11)
    # S5 73.4-100.8: the forest, two letters
    place(m, pad([shur(0, -1), shur(4, -1), shur(0)], 10.0, amp=0.05, a=3.0, r=2.0, bright=3), 73.6)
    tanbur(m, [(0, 0), (2, 0.8), (3, 1.6), (2, 2.4), (0, 3.4)], 74.0, amp=0.10)
    place(m, drone(36.71, 16.8, amp=0.08, a=2.0, r=2.0), 84.0)
    place(m, pad([shur(1, -1), shur(3, -1), shur(5, -1)], 6.0, amp=0.06, a=1.0, r=1.5, bright=4), 84.4)
    place(m, drum(dur=2.4, f0=44, amp=0.7, noise=0.3), 88.8)
    place(m, pad([shur(0), shur(4), shur(0, 1)], 6.6, amp=0.07, a=1.0, r=2.0, bright=5), 89.0)
    tanbur(m, THEME, 95.6, amp=0.13, low=True, step=0.8)
    # S6 100.8-124.4: bread; Sahl's gate
    place(m, pad([shur(0), shur(2), shur(4)], 7.0, amp=0.04, a=2.0, r=2.0, bright=3), 100.8)
    tanbur(m, [(4, 0), (3, 0.9), (2, 1.8)], 101.2, amp=0.08)
    heartbeat(m, 105.8, 112.0, bpm=70, amp=0.24)
    place(m, drum(dur=2.4, f0=42, amp=0.8, noise=0.35), 109.2)
    place(m, drone(36.71, 12.4, amp=0.08, a=1.0, r=2.0), 112.0)
    place(m, pad([shur(0, -1), shur(2, -1), shur(4, -1)], 8.0, amp=0.06, a=2.0, r=1.0, bright=4), 112.2)
    place(m, pad([shur(1, -1), shur(3, -1), shur(5, -1)], 4.0, amp=0.06, a=0.5, r=1.5, bright=4), 118.6)
    place(m, drum(dur=2.5, f0=46, amp=0.85, noise=0.4), END_CARD - 0.1)
    tanbur(m, THEME, END_CARD + 0.1, amp=0.18, low=True, step=0.8)
    place(m, pad([shur(0), shur(4), shur(0, 1)], 4.4, amp=0.07, a=1.0, r=2.0, bright=5), END_CARD)


def sfx(s):
    # hook: fire and falling stone
    place(s, crackle(6.6, amp=0.14, seed=801), 0.0)
    place(s, noise_bed(6.6, amp=0.08, lo=200, hi=2400, lfo=0.6, seed=802), 0.0)
    place(s, cheer(4.0, amp=0.06, seed=803), 0.5)
    hooves(s, 3.8, 6.6, step=0.9, amp=0.03, pan=0.0, seed=804)
    # the ambush in the mist
    place(s, noise_bed(11.8, amp=0.06, lo=150, hi=1400, lfo=0.2, seed=805), 11.2)
    steps(s, 11.3, 15.8, step=0.45, amp=0.04, seed=806)
    place(s, cheer(5.0, amp=0.12, seed=807), 15.9)
    for k, t in enumerate((16.2, 16.9, 17.6, 18.4, 19.0, 19.8)):
        place(s, clash(0.07, seed=808 + k), t, pan=(-0.4 if k % 2 else 0.4))
    for k, t in enumerate((16.5, 17.3, 18.2)):
        place(s, arrow(0.06, seed=k), t, pan=0.3)
    hooves(s, 20.2, 23.0, step=0.25, amp=0.06, pan=0.4, seed=809)
    place(s, neigh(0.06), 20.4, pan=0.4)
    # candlelight, the wax, the gate
    place(s, crackle(9.6, amp=0.04, rate=5, seed=810), 23.0)
    place(s, knock(0.05), 26.6, pan=0.1)
    place(s, noise_bed(4.0, amp=0.05, lo=200, hi=1600, lfo=0.25, seed=811), 32.6)
    place(s, creak(1.4, 0.07, seed=812), 32.9)
    hooves(s, 34.0, 36.4, step=0.22, amp=0.06, pan=0.3, seed=813)
    # the fall
    place(s, cheer(9.4, amp=0.05, seed=814), 36.6)
    place(s, noise_bed(9.4, amp=0.05, lo=300, hi=2600, lfo=0.3, seed=815), 41.0)
    place(s, snort(seed=8, amp=0.05), 42.2, pan=-0.4)
    place(s, snort(seed=9, amp=0.04), 44.6, pan=0.4)
    for k, t in enumerate(np.arange(50.8, 54.6, 0.45)):
        place(s, knock(0.06), t, pan=0.2 * (k % 3 - 1))
    place(s, cheer(7.0, amp=0.13, seed=816), 50.8)
    place(s, crackle(9.8, amp=0.12, seed=817), 50.6)
    place(s, swish(0.5, amp=0.06, seed=818), 55.6); place(s, swish(0.5, amp=0.06, seed=819), 56.4)
    hooves(s, 60.4, 63.4, step=0.22, amp=0.08, pan=0.5, seed=820)
    place(s, neigh(0.06, seed=2), 62.4, pan=0.4)
    place(s, noise_bed(10.6, amp=0.06, lo=200, hi=2400, lfo=0.5, seed=821), 58.0)
    place(s, crash(0.35, seed=822), 70.6)
    place(s, rumble(3.0, 0.3, seed=823), 70.6)
    steps(s, 68.7, 70.5, step=0.6, amp=0.05, seed=824)
    # the forest stream
    place(s, water(27.4, amp=0.05, seed=825), 73.4)
    for k, t in enumerate((73.8, 75.4, 77.0, 86.2, 92.8, 99.2)):
        place(s, chirp(2900 + 300 * (k % 3), amp=0.035), t, pan=0.5 - 0.25 * (k % 4))
    steps(s, 75.0, 77.8, step=0.55, amp=0.05, seed=826, pan=0.4)
    place(s, scrape(0.4, amp=0.04, seed=827), 85.2)
    place(s, scrape(0.5, amp=0.05, seed=828), 87.4)
    # dawn, bread, the rider on the hill, Sahl's gate
    place(s, noise_bed(11.2, amp=0.04, lo=200, hi=1800, lfo=0.15, seed=829), 100.8)
    for k, t in enumerate((101.2, 102.6, 104.9, 106.6)):
        place(s, chirp(3100 + 250 * k, amp=0.035), t, pan=-0.4 + 0.3 * k)
    steps(s, 104.8, 108.6, step=0.6, amp=0.04, seed=830)
    place(s, snort(seed=10, amp=0.04), 107.0, pan=0.5)
    hooves(s, 109.6, 112.0, step=0.24, amp=0.06, pan=0.6, seed=831)
    place(s, noise_bed(12.4, amp=0.04, lo=150, hi=900, lfo=0.2, seed=832), 112.0)
    place(s, crackle(12.4, amp=0.08, seed=833), 112.0)
    place(s, creak(1.6, 0.09, seed=834), 112.3)
    steps(s, 113.6, 115.4, step=0.5, amp=0.05, seed=835)


LINES = [("p6s3a", 25.4), ("p6s3b", 28.4), ("p6s3c", 30.2),
         ("p6s4a", 46.5), ("p6s4b", 48.2), ("p6s4c", 63.3), ("p6s4d", 65.4),
         ("p6s5a", 78.2), ("p6s5b", 80.2), ("p6s5c", 82.6), ("p6s5d", 89.2), ("p6s5e", 90.3), ("p6s5f", 95.8), ("p6s5g", 98.3),
         ("p6s6a", 102.0), ("p6s6b", 116.5), ("p6s6c", 118.3)]
if __name__ == "__main__":
    build(6, TOTAL, music, sfx, LINES, f'{AUDIO}/part06.wav')
    print('done')
