"""Part 4 · The Ambush — timing, music and sound. Scene starts: s1 0, s2 21.0, s3 25.6, s4 50.2, s5 66.0, s6 89.4, end 108.0"""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import series; series.from_folder(__file__)
from paths import AUDIO
from audio import *
from mix import build
from p02_audio import chirp, snort, clash, tanbur, THEME
from p03_audio import thud, hooves, steps, rumble, rockfall, cheer, swish, snap
TOTAL = 108.0
S = {"s1": 0.0, "s2": 21.0, "s3": 25.6, "s4": 50.2, "s5": 66.0, "s6": 89.4}


def arrow(amp=0.08, seed=0):
    r = np.random.default_rng(seed)
    n = int(0.35 * SR); t = np.arange(n) / SR
    f = 2600 - 1800 * t / 0.35
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * 0.3 + bandpass(r.standard_normal(n).astype(np.float32), 1500, 6000)
    return (x * np.sin(np.pi * t / 0.35) ** 2 * amp).astype(np.float32)


def neigh(amp=0.1, seed=0):
    n = int(0.9 * SR); t = np.arange(n) / SR
    f = 700 + 300 * np.sin(2 * np.pi * 9 * t) * np.exp(-t * 2) - 300 * t
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, 0.05, 0.4) * (0.6 + 0.4 * np.sin(2 * np.pi * 30 * t))
    return bandpass((x * amp).astype(np.float32), 300, 3000)


def clap(amp=0.06, seed=0):
    r = np.random.default_rng(seed)
    n = int(0.08 * SR); t = np.arange(n) / SR
    return (bandpass(r.standard_normal(n).astype(np.float32), 900, 4000) * np.exp(-t * 60) * amp * 2).astype(np.float32)


def water(dur, amp=0.05, seed=0):
    return noise_bed(dur, amp=amp, lo=600, hi=5000, lfo=1.8, seed=seed)


def daf(m, t0, t1, bpm=110, amp=0.18, pan=-0.15):
    beat = 60 / bpm; t = t0; i = 0
    while t < t1:
        place(m, drum(dur=0.5, f0=95 if i % 4 else 70, amp=amp * (1.0 if i % 4 == 0 else 0.6), noise=0.35), t, pan=pan)
        if i % 2 == 1:
            place(m, drum(dur=0.25, f0=180, amp=amp * 0.4, noise=0.6), t + beat / 2, pan=pan)
        t += beat; i += 1


def music(m):
    # S1 0-21: the rockslide, the battle, the cheer
    place(m, drum(dur=3.0, f0=40, amp=1.0, noise=0.5), 0.0)
    place(m, drone(36.71, 21.0, amp=0.12, a=0.1, r=1.5), 0.0)
    for i, t in enumerate(np.arange(0.6, 14.0, 0.375)):
        place(m, drum(dur=0.5, f0=62 if i % 2 else 50, amp=0.30, noise=0.3), t)
    place(m, pad([shur(1, -1), shur(3, -1), shur(5, -1)], 8.0, amp=0.07, a=0.5, r=1.0, bright=5), 3.6)
    place(m, drum(dur=2.5, f0=44, amp=0.8, noise=0.4), 14.2)
    tanbur(m, THEME, 14.6, amp=0.22, low=True, step=0.75)
    place(m, pad([shur(0), shur(4), shur(0, 1)], 6.6, amp=0.09, a=0.8, r=2.0, bright=6), 14.4)
    # S2 21-25.6: title
    place(m, drum(dur=2.8, f0=46, amp=1.0, noise=0.45), 21.0)
    tanbur(m, THEME[:6], 21.3, amp=0.24, low=True, step=0.8)
    place(m, drone(73.42, 4.8, amp=0.10, a=0.05, r=2.0), 21.0)
    # S3 25.6-50.2: the feast at Bazz: daf, tanbur dance tune, then Babak's tune alone
    daf(m, 25.6, 32.6, bpm=116, amp=0.20)
    dance = [(0, 0), (2, 0.25), (3, 0.5), (4, 0.75), (3, 1.0), (2, 1.25), (1, 1.5), (0, 1.75)]
    for t0 in np.arange(25.8, 32.4, 2.07):
        tanbur(m, dance, t0, amp=0.17, step=1.0, dur=1.2)
    place(m, drone(73.42, 24.6, amp=0.06, a=1.5, r=2.0), 25.6)
    tanbur(m, [(0, 0), (2, 0.7), (1, 1.2), (0, 1.8), (4, 3.0), (3, 3.6), (2, 4.2), (0, 5.0)], 32.8, amp=0.20, low=True)
    tanbur(m, [(0, 0), (2, 0.7), (1, 1.2), (0, 1.8), (4, 3.0), (3, 3.6), (2, 4.2), (0, 5.0)], 38.6, amp=0.20, low=True)
    daf(m, 44.0, 49.6, bpm=116, amp=0.18)
    for t0 in np.arange(44.1, 49.5, 2.07):
        tanbur(m, dance, t0, amp=0.16, step=1.0, dur=1.2)
    # S4 50.2-66: the dying caliph
    place(m, drone(36.71, 15.8, amp=0.10, a=2.0, r=2.5), 50.2)
    place(m, pad([shur(0, -1), shur(1, -1), shur(3, -1)], 10.0, amp=0.06, a=3.0, r=2.0, bright=3), 50.6)
    place(m, bell(196, 4.0, 0.04), 54.6)
    place(m, drum(dur=2.0, f0=48, amp=0.6, noise=0.3), 61.2)
    place(m, pad([shur(0, -1), shur(4, -1)], 4.6, amp=0.07, a=0.5, r=3.0, bright=3), 61.2)
    # S5 66-89.4: Baghdad, the gold, the banner
    place(m, drone(36.71, 23.4, amp=0.11, a=1.0, r=2.0), 66.0)
    for i, t in enumerate(np.arange(66.2, 80.4, 1.2)):
        place(m, drum(dur=1.0, f0=55, amp=0.20 + (0.06 if i % 4 == 0 else 0), noise=0.2), t)
    place(m, pad([shur(0), shur(2), shur(5)], 6.0, amp=0.06, a=1.0, r=1.5, bright=6), 66.2)
    for k, t in enumerate((66.8, 68.0, 69.2)):
        place(m, bell(880 + 110 * k, 1.8, 0.03), t)
    place(m, drum(dur=2.4, f0=44, amp=0.8, noise=0.4), 79.0)
    place(m, pad([shur(1, -1), shur(3, -1), shur(5, -1)], 9.0, amp=0.08, a=1.0, r=2.0, bright=4), 80.4)
    place(m, drone(38.89, 9.0, amp=0.06, a=2.0, r=2.0), 80.4)
    # S6 89.4-108: night on the wall; the fires on the plain; end card
    place(m, drone(36.71, 18.6, amp=0.10, a=2.0, r=2.0), 89.4)
    place(m, pad([shur(0, -1), shur(4, -1), shur(0)], 13.0, amp=0.06, a=3.0, r=2.0, bright=3), 89.6)
    tanbur(m, [(4, 0), (3, 0.8), (2, 1.6), (0, 2.6)], 90.2, amp=0.14)
    place(m, drum(dur=2.5, f0=46, amp=0.8, noise=0.4), 100.6)
    tanbur(m, THEME, 100.8, amp=0.18, low=True, step=0.8)
    place(m, pad([shur(0), shur(4), shur(0, 1)], 7.0, amp=0.08, a=1.0, r=2.5, bright=5), 101.0)


def sfx(s):
    rockfall(s, 0.0, 6.0, amp=0.42, seed=21)
    place(s, noise_bed(14.0, amp=0.10, lo=200, hi=2400, lfo=1.0, seed=60), 3.6)     # the shouting battle
    for k, t in enumerate((4.0, 5.2, 7.6, 8.3, 9.0, 9.9, 10.4)):
        place(s, arrow(0.07, seed=k), t, pan=(-0.5 if k % 2 else 0.5))
    for k, t in enumerate((3.9, 6.1, 8.0, 9.6, 10.8)):
        place(s, clash(0.08, seed=10 + k), t, pan=(-0.3 if k % 2 else 0.3))
    place(s, neigh(0.10), 8.2, pan=0.3)
    hooves(s, 7.4, 10.8, step=0.25, amp=0.06, pan=-0.3, seed=11)
    place(s, water(5.0, amp=0.06, seed=61), 10.6)
    place(s, splash_(0.2), 11.9)
    place(s, cheer(5.6, amp=0.13, seed=62), 15.0)
    # title, feast
    place(s, noise_bed(4.6, amp=0.08, lo=300, hi=3000, lfo=0.4, seed=63), 21.0)
    place(s, crackle(24.6, amp=0.10, seed=64), 25.6)
    for t in np.arange(25.9, 32.4, 0.517):
        place(s, clap(0.07, seed=int(t * 10)), t, pan=0.3); place(s, clap(0.05, seed=int(t * 10) + 1), t + 0.02, pan=-0.3)
    place(s, noise_bed(7.0, amp=0.05, lo=300, hi=2500, lfo=1.5, seed=65), 25.6)
    for t in np.arange(44.2, 49.6, 0.517):
        place(s, clap(0.06, seed=int(t * 10)), t, pan=0.25)
    place(s, noise_bed(6.0, amp=0.05, lo=300, hi=2500, lfo=1.5, seed=66), 44.0)
    # tent: wind on the canvas, the lamp
    place(s, noise_bed(15.8, amp=0.05, lo=150, hi=900, lfo=0.2, seed=67), 50.2)
    place(s, crackle(13.0, amp=0.03, rate=4, seed=68), 50.2)
    place(s, swish(0.6, amp=0.05, seed=9), 63.5)                                   # the lamp goes out
    # Baghdad: footsteps, chests set down, coins
    steps(s, 66.2, 70.6, step=0.5, amp=0.05, seed=12)
    for k, t in enumerate((67.6, 68.9, 70.1)):
        place(s, thud(0.14, 90, seed=30 + k), t)
        for j in range(5):
            place(s, bell(2400 + 300 * j, 0.4, 0.012), t + 0.05 + 0.04 * j, pan=0.2)
    place(s, noise_bed(23.0, amp=0.03, lo=200, hi=1500, lfo=0.2, seed=69), 66.0)
    place(s, swish(0.5, amp=0.06, seed=13), 79.2)
    # night on the wall
    place(s, noise_bed(18.6, amp=0.07, lo=200, hi=2000, lfo=0.25, seed=70), 89.4)
    for k, t in enumerate((91.0, 96.5, 102.0)):
        place(s, chirp(4200 + 200 * k, dur=0.06, amp=0.015), t, pan=-0.6)


def splash_(amp=0.2):
    from p03_audio import splash
    return splash(amp)


LINES = [("p4s1a", 4.2), ("p4s1b", 14.6),
         ("p4s3a", 33.4), ("p4s3b", 35.9), ("p4s3c", 38.9), ("p4s3d", 40.9),
         ("p4s4a", 55.0), ("p4s4b", 57.6), ("p4s4c", 61.2),
         ("p4s5a", 71.4), ("p4s5b", 74.8), ("p4s5c", 77.4), ("p4s5d", 81.0), ("p4s5e", 84.6),
         ("p4s6a", 95.0), ("p4s6b", 98.0)]
if __name__ == "__main__":
    build(4, TOTAL, music, sfx, LINES, f'{AUDIO}/part04.wav')
    print('done')
