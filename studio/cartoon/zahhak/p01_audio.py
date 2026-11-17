"""Part 1 · The Prince and the Stranger — timing, music and sound.
Scene starts: s1 0 (hook: the snake king on his throne at night), s2 9.9 (title), s3 14.5 (Mardas's land: the herds, milk for everyone,
"where is my son?", Zahhak riding), s4 50.6 (the horse yard: the stranger, the oath, the plan), s5 100.4 (the garden at night: the pit;
Zahhak at his window), s6 124.6 (before dawn: Mardas goes into the garden), end card 138.0, end 143.0"""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import series; series.from_folder(__file__)
from paths import AUDIO
from audio import *
from mix import build
from zsfx import *
TOTAL = 143.0
S = {"s1": 0.0, "s2": 9.9, "s3": 14.5, "s4": 50.6, "s5": 100.4, "s6": 124.6}
END_CARD = 138.0

SLY = [(0, 0), (1, 0.33), (0, 0.66), (3, 1.0), (2, 1.33), (1, 1.66), (0, 2.2)]


def daf(m, t0, t1, bpm=132, amp=0.16, pan=-0.15):
    beat = 60 / bpm; t = t0; i = 0
    while t < t1:
        place(m, drum(dur=0.5, f0=95 if i % 4 else 70, amp=amp * (1.0 if i % 4 == 0 else 0.6), noise=0.35), t, pan=pan)
        if i % 2 == 1:
            place(m, drum(dur=0.25, f0=180, amp=amp * 0.4, noise=0.6), t + beat / 2, pan=pan)
        t += beat; i += 1


def music(m):
    # S1 0-9.9: the snake king — a low drone, a pad that rubs on the koron second, a slow drum like a heart
    place(m, drone(36.71, 10.4, amp=0.16, a=1.5, r=0.6), 0.0)
    place(m, drone(73.42, 9.6, amp=0.06, a=2.5, r=1.0), 0.3)
    place(m, pad([shur(1, -1), shur(0, -1)], 9.2, amp=0.06, a=2.5, r=1.2, bright=4), 0.5)
    for t in (2.6, 4.9, 7.2):
        place(m, drum(dur=1.4, f0=50, amp=0.2, noise=0.05), t)
    place(m, bell(196, 3.0, 0.05), 8.9)
    # S2 9.9-14.5: title
    place(m, drum(dur=3.2, f0=40, amp=0.9, noise=0.4), 9.9)
    place(m, drone(36.71, 4.9, amp=0.12, a=0.1, r=1.4), 9.9)
    place(m, pad([shur(0), shur(4), shur(0, 1)], 4.8, amp=0.10, a=0.4, r=1.6, bright=6), 9.9)
    tanbur(m, ZTHEME, 10.3, amp=0.22, low=True, step=0.85)
    # S3 14.5-50.6: Mardas's land — warm morning, then the gallop, then a shadow
    place(m, drone(73.42, 14.4, amp=0.04, a=2.0, r=2.0), 14.5)
    place(m, pad([shur(0), shur(2), shur(4)], 14.2, amp=0.06, a=2.5, r=2.0, bright=5), 14.5)
    tanbur(m, [(0, 0), (2, 0.6), (4, 1.2), (3, 1.8), (2, 2.4), (0, 3.2)], 15.6, amp=0.13)
    tanbur(m, [(2, 0), (3, 0.5), (4, 1.0), (2, 1.7), (1, 2.2), (0, 2.8)], 21.5, amp=0.12)
    tanbur(m, [(4, 0), (3, 0.6), (2, 1.2), (0, 2.0)], 25.6, amp=0.11)
    place(m, pad([shur(0), shur(2), shur(4), shur(0, 1)], 11.8, amp=0.07, a=1.5, r=2.0, bright=5), 28.4)
    tanbur(m, [(4, 0), (3, 0.5), (2, 1.0), (0, 1.8)], 31.0, amp=0.12)
    tanbur(m, [(0, 0), (2, 0.5), (1, 1.0), (0, 1.6)], 36.0, amp=0.09)
    place(m, drone(73.42, 5.4, amp=0.07, a=0.4, r=1.0), 40.0)
    daf(m, 40.0, 45.0, bpm=132, amp=0.16)
    t = 40.3
    while t < 44.6:
        for i, deg in enumerate([0, 2, 4, 2, 3, 2, 1, 0]):
            place(m, pluck_fast(shur(deg), 0.8, amp=0.12), t + i * 0.2, pan=0.3)
        t += 1.6
    place(m, pad([shur(0), shur(4), shur(0, 1)], 5.6, amp=0.09, a=0.6, r=2.2, bright=6), 45.0)
    tanbur(m, ZTHEME[:4], 45.4, amp=0.15, low=True, step=0.8)
    place(m, pad([shur(1, -1), shur(3, -1)], 3.4, amp=0.05, a=1.0, r=1.6, bright=4), 47.4)
    place(m, bell(220, 2.6, 0.05), 49.0)
    # S4 50.6-100.4: the stranger
    place(m, pad([shur(0), shur(4)], 6.0, amp=0.05, a=1.5, r=1.5, bright=4), 50.6)
    tanbur(m, [(0, 0), (2, 0.7), (4, 1.4), (2, 2.4)], 51.4, amp=0.09)
    place(m, drone(36.71, 13.4, amp=0.05, a=2.0, r=1.0), 56.2)
    place(m, pad([shur(1, -1), shur(0, -1)], 13.4, amp=0.05, a=2.0, r=1.0, bright=4), 56.2)
    for t0 in (56.4, 59.4, 62.4, 65.4):
        for deg, dt in SLY:
            place(m, pluck_fast(shur(deg), 0.6, amp=0.10), t0 + dt, pan=0.35)
    place(m, drum(dur=2.6, f0=42, amp=0.85, noise=0.4), 71.5)
    place(m, pad([shur(1, -1), shur(5, -1)], 3.2, amp=0.08, a=0.2, r=2.0, bright=5), 71.5)
    place(m, drone(36.71, 10.0, amp=0.12, a=1.0, r=1.0), 72.8)
    place(m, pad([shur(0, -1), shur(1, -1), shur(4, -1)], 9.8, amp=0.06, a=2.0, r=1.0, bright=4), 72.8)
    for t in np.arange(73.0, 82.4, 1.2):
        place(m, drum(dur=0.9, f0=56, amp=0.14, noise=0.1), t)
    tanbur(m, [(0, 0), (1, 0.9)], 75.6, amp=0.08, low=True)
    tanbur(m, [(3, 0), (2, 0.6), (1, 1.2)], 79.6, amp=0.08)
    place(m, drone(36.71, 11.2, amp=0.09, a=0.5, r=1.0), 82.6)
    heartbeat(m, 83.0, 93.6, bpm=80, amp=0.22)
    place(m, drum(dur=2.0, f0=44, amp=0.45, noise=0.2), 87.5)
    place(m, bell(147, 3.0, 0.06), 91.6)
    place(m, drum(dur=2.0, f0=40, amp=0.5, noise=0.2), 91.5)
    place(m, pad([shur(0, -1), shur(3, -1)], 6.5, amp=0.07, a=1.0, r=2.0, bright=4), 93.9)
    tanbur(m, [(4, 0), (3, 0.7), (2, 1.4), (1, 2.1), (0, 3.0)], 94.0, amp=0.12, low=True)
    place(m, drum(dur=2.4, f0=40, amp=0.5, noise=0.3), 99.3)
    # S5 100.4-124.6: night in the garden
    place(m, drone(36.71, 24.4, amp=0.07, a=2.0, r=1.5), 100.4)
    place(m, pad([shur(0, -1), shur(3, -1), shur(5, -1)], 19.4, amp=0.05, a=3.0, r=2.0, bright=4), 100.4)
    for t, f in ((101.6, 880), (104.6, 740), (108.0, 659)):
        place(m, bell(f, 3.0, 0.025), t)
    for t in np.arange(110.3, 115.0, 0.9):
        place(m, drum(dur=0.7, f0=52, amp=0.12, noise=0.1), t)
    place(m, pad([shur(1, -1), shur(0, -1)], 4.6, amp=0.06, a=0.8, r=1.2, bright=4), 115.0)
    tanbur(m, [(2, 0), (1, 0.8), (0, 1.6)], 120.5, amp=0.10)
    heartbeat(m, 119.6, 124.0, bpm=60, amp=0.18)
    # S6 124.6-143.0: before dawn; the end card
    place(m, pad([shur(0), shur(2), shur(4)], 6.2, amp=0.06, a=1.5, r=2.0, bright=5), 125.6)
    tanbur(m, ZTHEME, 126.2, amp=0.09, step=1.1)
    place(m, bell(196, 2.5, 0.05), 129.9)
    place(m, drone(36.71, 4.6, amp=0.05, a=3.5, r=0.05), 132.0)
    place(m, drone(55.0, 4.6, amp=0.03, a=3.5, r=0.05), 132.0)
    heartbeat(m, 132.4, 136.4, bpm=56, amp=0.28)
    place(m, drum(dur=3.0, f0=40, amp=0.75, noise=0.4), 138.0)
    place(m, drone(36.71, 5.0, amp=0.10, a=0.2, r=2.0), 138.0)
    place(m, pad([shur(0), shur(4), shur(0, 1)], 5.0, amp=0.08, a=0.6, r=2.0, bright=5), 138.0)
    tanbur(m, ZTHEME[:4], 138.6, amp=0.14, low=True, step=0.9)


def sfx(s):
    # S1: torches, hissing
    place(s, crackle(10.2, amp=0.08, rate=8, seed=101), 0.0)
    place(s, noise_bed(10.0, amp=0.025, lo=150, hi=900, lfo=0.15, seed=102), 0.0)
    place(s, hiss(1.2, 0.06, seed=1), 0.3, pan=0.4)
    place(s, hiss(0.8, 0.04, seed=2), 3.4, pan=-0.4)
    place(s, hiss(1.5, 0.08, seed=3), 8.2, pan=0.3)
    place(s, crackle(4.8, amp=0.06, rate=6, seed=103), 9.9)
    # S3: morning plain, herds, milk, the gallop
    place(s, noise_bed(14.0, amp=0.035, lo=300, hi=2400, lfo=0.25, seed=104), 14.5)
    for k, t in enumerate((15.0, 16.4, 19.9, 23.6, 26.4, 29.6, 36.2, 38.8)):
        place(s, chirp(2900 + 300 * (k % 3), amp=0.035), t, pan=0.5 - 0.3 * (k % 4))
    for k, t in enumerate((17.6, 22.2, 23.9, 38.4)):
        place(s, bleat(0.05, seed=k, f0=480 + 60 * (k % 3)), t, pan=-0.3 + 0.2 * k)
    place(s, grunt(0.07, seed=1), 19.2, pan=0.4); place(s, grunt(0.06, seed=2), 23.0, pan=-0.2)
    steps(s, 21.6, 24.8, step=0.55, amp=0.03, seed=11)
    place(s, noise_bed(10.0, amp=0.03, lo=300, hi=2000, lfo=1.5, seed=105), 25.0)    # people waiting
    place(s, pour(1.8, amp=0.05, seed=1), 33.1)
    place(s, noise_bed(5.0, amp=0.04, lo=300, hi=2500, lfo=0.3, seed=106), 35.0)
    hooves(s, 40.0, 45.0, step=0.36, amp=0.10, pan=0.1, seed=12, gallop=True)
    hooves(s, 40.2, 45.0, step=0.31, amp=0.04, pan=-0.4, seed=13, gallop=True)
    place(s, noise_bed(5.0, amp=0.10, lo=300, hi=3200, lfo=0.8, seed=107), 40.0)
    place(s, neigh(0.09, seed=1), 44.3, pan=0.2)
    place(s, snort(seed=3, amp=0.10), 45.6, pan=-0.2)
    place(s, noise_bed(5.4, amp=0.05, lo=300, hi=2600, lfo=0.4, seed=108), 45.2)
    # S4: the horse yard
    place(s, noise_bed(49.8, amp=0.025, lo=300, hi=2400, lfo=0.2, seed=109), 50.6)
    for k, t in enumerate((51.0, 52.6, 57.4, 63.6, 75.0)):
        place(s, chirp(3100 + 250 * (k % 3), amp=0.03), t, pan=-0.5 + 0.25 * (k % 4))
    for k, t in enumerate(np.arange(51.0, 55.8, 0.62)):
        place(s, scrape(0.4, 0.03, seed=k), t, pan=-0.2)                     # the brush
    place(s, snort(seed=4, amp=0.08), 52.4, pan=-0.3)
    steps(s, 53.2, 56.0, step=0.5, amp=0.045, seed=14, pan=0.4)
    place(s, snort(seed=5, amp=0.07), 60.2, pan=-0.4)
    place(s, gust(1.6, amp=0.16, seed=6), 71.2)
    place(s, neigh(0.10, seed=2), 71.9, pan=-0.4)
    place(s, snort(seed=6, amp=0.09), 72.6, pan=-0.3)
    place(s, rustle(0.04, 0.8, seed=3), 95.4, pan=0.2)                          # the hand on the shoulder
    # S5: night garden
    crickets(s, 100.4, 124.4, amp=0.012, seed=15)
    place(s, owl(0.05), 102.6, pan=-0.5)
    place(s, owl(0.04), 117.9, pan=0.5)
    place(s, noise_bed(24.0, amp=0.02, lo=150, hi=900, lfo=0.1, seed=110), 100.4)
    steps(s, 108.0, 109.8, step=0.6, amp=0.025, seed=16, pan=-0.3)
    for k, t in enumerate(np.arange(110.3, 114.9, 0.92)):
        place(s, dig(0.12, seed=k), t, pan=0.1)
    for k, t in enumerate((115.2, 115.7, 116.3, 117.0)):
        place(s, rustle(0.05, 0.6, seed=10 + k), t, pan=0.1 - 0.1 * k)
    # S6: before dawn
    crickets(s, 124.6, 131.0, amp=0.008, seed=17, rate=1.3)
    place(s, creak(1.3, 0.07, seed=2), 124.9)
    steps(s, 125.8, 126.6, step=0.6, amp=0.035, seed=18)
    place(s, noise_bed(18.4, amp=0.018, lo=150, hi=900, lfo=0.1, seed=111), 124.6)
    steps(s, 132.2, 136.4, step=0.62, amp=0.035, seed=19)
    wings(s, 136.6, n=9, rate=0.09, amp=0.07, seed=4, pan=0.1)
    place(s, noise_bed(5.0, amp=0.03, lo=200, hi=1500, lfo=0.2, seed=112), 138.0)


LINES = [("p1s1a", 1.0), ("p1s1b", 4.3), ("p1s1c", 7.1),
         ("p1s3a", 15.2), ("p1s3b", 21.8), ("p1s3c", 25.3), ("p1s3d", 28.9), ("p1s3e", 30.9), ("p1s3f", 35.3), ("p1s3g", 37.3),
         ("p1s3h", 40.3), ("p1s3i", 45.4),
         ("p1s4a", 51.2), ("p1s4b", 56.5), ("p1s4c", 58.9), ("p1s4d", 61.2), ("p1s4e", 62.9), ("p1s4f", 65.8), ("p1s4g", 69.9),
         ("p1s4h", 73.1), ("p1s4i", 77.8), ("p1s4j", 82.9), ("p1s4k", 87.6), ("p1s4l", 91.6), ("p1s4m", 94.3), ("p1s4n", 96.1),
         ("p1s5a", 101.1), ("p1s5b", 107.1), ("p1s5c", 110.3), ("p1s5d", 116.6), ("p1s5e", 120.1),
         ("p1s6a", 126.9), ("p1s6b", 129.9), ("p1s6c", 132.4)]
if __name__ == "__main__":
    build(1, TOTAL, music, sfx, LINES, f'{AUDIO}/part01.wav')
    print('done')
