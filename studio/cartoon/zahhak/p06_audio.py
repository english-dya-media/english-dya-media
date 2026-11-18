"""Part 6 · The Cow Barmayeh — timing, music and sound.
Scene starts: s1 0 (hook: the peacock cow in the misty meadow; Faranak's plea), s2 8.0 (title: the meadow at dawn), s3 12.6 (Faranak runs at
night; the meadow at dusk; Barmayeh; the keeper takes the baby), s4 41.0 (three years; the spy; Zahhak), s5 59.4 (Faranak's warning; the
climb up Alborz; the holy man), s6 86.8 (the soldiers in the meadow; the empty meadow; the burning house; sixteen years later: Fereydun
comes down: "Who was my father?"), end card 114.4, end 119.4"""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import series; series.from_folder(__file__)
from paths import AUDIO
from audio import *
from mix import build
from zsfx import *
from p01_audio import daf
TOTAL = 119.4
S = {"s1": 0.0, "s2": 8.0, "s3": 12.6, "s4": 41.0, "s5": 59.4, "s6": 86.8}
END_CARD = 114.4
STORM = 86.8          # the riders burst into the meadow

MEADOW = [(0, 0), (2, 0.5), (4, 1.0), (5, 1.5), (4, 2.0), (2, 2.6), (3, 3.1), (0, 3.8)]
LULLABY = [(0, 0), (2, 0.6), (4, 1.2), (3, 1.9), (2, 2.5), (0, 3.2)]


def sparkle(m, t0, amp=0.03, n=5, base=1800):
    for k in range(n):
        place(m, bell(base + 330 * k, 1.4, amp * (1 - k / (n + 1))), t0 + 0.09 * k, pan=-0.3 + 0.15 * k)


def moo(amp=0.08, seed=0, f0=150):
    """a soft, low moo"""
    r = np.random.default_rng(seed)
    n = int(1.2 * SR); t = np.arange(n) / SR
    f = f0 * (1 + 0.15 * np.sin(np.pi * t / 1.2)) * (1 + 0.01 * r.standard_normal())
    ph = 2 * np.pi * np.cumsum(f) / SR
    x = np.sin(ph) + 0.5 * np.sin(2 * ph) + 0.25 * np.sin(3 * ph)
    e = np.minimum(1, t / 0.15) * np.minimum(1, (1.2 - t) / 0.4)
    return lowpass((x * e * amp).astype(np.float32), 1200)


def fire_roar(dur=4.0, amp=0.2, seed=0):
    return noise_bed(dur, amp=amp, lo=80, hi=900, lfo=2.4, seed=seed)


def music(m):
    # S1 0-8.0: the peacock cow at dawn; Faranak's plea
    place(m, pad([shur(0), shur(4), shur(0, 1)], 4.8, amp=0.07, a=1.5, r=1.0, bright=6), 0.0)
    tanbur(m, MEADOW[:5], 0.6, amp=0.11, step=0.9)
    sparkle(m, 1.2, 0.03)
    place(m, drone(55.0, 3.4, amp=0.08, a=0.3, r=0.8), 4.8)
    heartbeat(m, 4.9, 7.8, bpm=96, amp=0.18)
    # S2 8.0-12.6: title
    place(m, drum(dur=3.2, f0=40, amp=0.9, noise=0.4), 8.0)
    place(m, drone(36.71, 4.9, amp=0.12, a=0.1, r=1.4), 8.0)
    place(m, pad([shur(0), shur(4), shur(0, 1)], 4.8, amp=0.10, a=0.4, r=1.6, bright=6), 8.0)
    tanbur(m, ZTHEME, 8.4, amp=0.22, low=True, step=0.85)
    # S3 12.6-41.0: the night run; the meadow; Barmayeh; the keeper
    place(m, drone(36.71, 4.8, amp=0.09, a=0.5, r=0.8), 12.6)
    for t in np.arange(12.8, 17.2, 0.4):                                         # running
        place(m, drum(dur=0.5, f0=60, amp=0.14, noise=0.2), t)
    place(m, pad([shur(0), shur(2), shur(4)], 9.6, amp=0.06, a=2.0, r=1.5, bright=5), 17.4)
    tanbur(m, MEADOW, 18.0, amp=0.10, step=1.0)
    sparkle(m, 22.6, 0.035); sparkle(m, 24.4, 0.025, base=2200)
    place(m, pad([shur(0), shur(4), shur(0, 1), shur(2, 1)], 5.0, amp=0.07, a=1.5, r=1.5, bright=7), 22.2)
    place(m, pad([shur(1, -1), shur(0, -1), shur(4, -1)], 6.4, amp=0.05, a=1.5, r=1.5, bright=4), 27.2)
    tanbur(m, [(2, 0), (1, 0.8), (0, 1.6)], 28.0, amp=0.08, step=1.1)
    place(m, pad([shur(0), shur(2), shur(4)], 7.6, amp=0.06, a=1.5, r=2.0, bright=5), 33.4)
    tanbur(m, LULLABY, 36.9, amp=0.09, step=1.0)
    # S4 41.0-59.4: three years; the spy; Zahhak
    place(m, pad([shur(0), shur(4), shur(0, 1)], 7.0, amp=0.06, a=1.5, r=1.5, bright=6), 41.0)
    tanbur(m, MEADOW, 41.4, amp=0.11, step=0.8)
    tanbur(m, MEADOW[:4], 44.8, amp=0.08, step=0.8)
    place(m, drone(36.71, 11.4, amp=0.10, a=0.3, r=1.2), 48.0)                   # the spy
    place(m, pad([shur(1, -1), shur(0, -1)], 7.0, amp=0.05, a=0.6, r=1.0, bright=4), 48.0)
    place(m, drum(dur=2.0, f0=44, amp=0.7, noise=0.35), 55.2)
    place(m, pad([shur(1, -1), shur(5, -1), shur(1)], 3.6, amp=0.08, a=0.05, r=1.5, bright=6), 55.2)
    # S5 59.4-86.8: the warning; Alborz; the holy man
    place(m, drone(55.0, 10.6, amp=0.07, a=1.0, r=1.0), 59.4)
    place(m, pad([shur(0, -1), shur(2, -1), shur(4, -1)], 10.4, amp=0.05, a=1.5, r=1.0, bright=4), 59.6)
    heartbeat(m, 63.8, 69.8, bpm=92, amp=0.14)
    place(m, pad([shur(0), shur(4), shur(0, 1)], 6.4, amp=0.07, a=2.0, r=1.5, bright=6), 70.0)   # dawn on the mountain
    tanbur(m, [(0, 0), (2, 0.7), (4, 1.4), (5, 2.1), (4, 2.8), (2, 3.5)], 70.6, amp=0.10, step=1.0)
    place(m, pad([shur(0), shur(2), shur(4), shur(0, 1)], 10.8, amp=0.06, a=2.0, r=2.0, bright=6), 76.0)
    tanbur(m, LULLABY, 80.8, amp=0.09, step=1.05)
    place(m, bell(587, 3.0, 0.03), 84.0)
    # S6 86.8-119.4: the storm; the empty meadow; the burning house; sixteen years later; the question
    for i, t in enumerate(np.arange(STORM, 91.0, 0.3)):
        place(m, drum(dur=0.5, f0=52 if i % 2 else 64, amp=0.3 + (0.1 if i % 4 == 0 else 0), noise=0.3), t)
    place(m, drone(36.71, 4.2, amp=0.12, a=0.1, r=0.6), STORM)
    place(m, drone(36.71, 9.6, amp=0.08, a=1.0, r=1.5), 91.0)
    place(m, pad([shur(1, -1), shur(0, -1)], 5.6, amp=0.05, a=1.5, r=1.0, bright=4), 91.2)
    tanbur(m, [(2, 0), (1, 1.0), (0, 2.0)], 92.4, amp=0.08, step=1.2)
    place(m, drum(dur=2.0, f0=44, amp=0.5, noise=0.35), 96.6)
    place(m, pad([shur(0), shur(4), shur(0, 1)], 6.4, amp=0.08, a=1.5, r=1.0, bright=6), 100.6)   # sixteen years later
    tanbur(m, ZTHEME, 101.2, amp=0.16, low=True, step=0.95)
    place(m, drone(55.0, 7.4, amp=0.06, a=1.0, r=1.0), 107.0)
    place(m, pad([shur(0), shur(2), shur(4)], 7.4, amp=0.05, a=1.0, r=1.5, bright=5), 107.0)
    place(m, bell(440, 2.6, 0.03), 111.2)
    place(m, drum(dur=3.0, f0=40, amp=0.75, noise=0.4), END_CARD)
    place(m, drone(36.71, 5.0, amp=0.10, a=0.2, r=2.0), END_CARD)
    place(m, pad([shur(0), shur(4), shur(0, 1)], 5.0, amp=0.08, a=0.6, r=2.0, bright=5), END_CARD)
    tanbur(m, ZTHEME[:4], END_CARD + 0.6, amp=0.14, low=True, step=0.9)


def sfx(s):
    # S1: birds at dawn; the cow; the night wind
    for k, t in enumerate((0.5, 1.4, 2.7, 3.9)):
        place(s, chirp(2900 + 300 * (k % 3), amp=0.04), t, pan=0.4 - 0.25 * k)
    place(s, moo(0.06, seed=61), 2.2, pan=-0.2)
    place(s, gust(2.6, 0.08, seed=61), 4.8)
    steps(s, 4.8, 7.8, step=0.24, amp=0.04, seed=61)
    # S3: running at night; the meadow at dusk; the cow; the hand-over
    place(s, noise_bed(4.8, amp=0.05, lo=200, hi=2000, lfo=0.4, seed=601), 12.6)
    steps(s, 12.7, 17.3, step=0.24, amp=0.05, seed=62)
    crickets(s, 17.4, 41.0, amp=0.01, seed=61)
    place(s, moo(0.07, seed=62), 19.6, pan=0.2); place(s, moo(0.05, seed=63, f0=140), 25.0, pan=0.1)
    for k, t in enumerate((18.6, 23.4, 31.2)):
        place(s, chirp(2600 + 200 * k, amp=0.03), t, pan=0.5)
    place(s, rustle(0.05, 0.8, seed=61), 37.0)
    # S4: day in the meadow; the spy; the hall
    for k, t in enumerate((41.4, 42.2, 43.9, 45.3, 46.6)):
        place(s, chirp(3000 + 250 * (k % 3), amp=0.04), t, pan=0.5 - 0.2 * k)
    place(s, moo(0.06, seed=64), 43.2, pan=-0.2)
    place(s, rustle(0.06, 0.9, seed=62), 48.3, pan=-0.4)
    place(s, crackle(8.4, amp=0.05, rate=8, seed=602), 51.0)
    place(s, hiss(1.2, 0.08, seed=61), 55.6, pan=-0.3); place(s, hiss(1.2, 0.08, seed=62), 56.4, pan=0.3)
    # S5: night in the meadow; the climb; the cave
    crickets(s, 59.4, 70.0, amp=0.011, seed=62)
    place(s, owl(0.03), 61.2, pan=0.4)
    place(s, noise_bed(6.0, amp=0.06, lo=300, hi=3000, lfo=0.3, seed=603), 70.0)      # mountain wind
    steps(s, 70.2, 75.8, step=0.5, amp=0.04, seed=63)
    for k, t in enumerate((71.2, 73.4)):
        place(s, chirp(3300 + 300 * k, amp=0.03), t, pan=-0.4)
    place(s, crackle(10.8, amp=0.05, rate=8, seed=604), 76.0)                        # the hermit's fire
    place(s, noise_bed(10.8, amp=0.03, lo=300, hi=2600, lfo=0.2, seed=605), 76.0)
    # S6: the riders; the empty meadow; the fire; the mountain; the meeting
    hooves(s, STORM, 91.0, step=0.18, amp=0.09, pan=-0.2, seed=61, gallop=True)
    hooves(s, STORM + 0.09, 91.0, step=0.19, amp=0.08, pan=0.3, seed=62, gallop=True)
    place(s, noise_bed(4.2, amp=0.12, lo=150, hi=1400, lfo=1.4, seed=606), STORM)    # dust and shouting
    place(s, neigh(0.08, seed=61), 88.2, pan=0.3)
    place(s, noise_bed(5.6, amp=0.05, lo=200, hi=2000, lfo=0.3, seed=607), 91.0)    # wind in the empty meadow
    place(s, fire_roar(4.0, 0.16, seed=61), 96.6)
    place(s, crackle(4.0, amp=0.2, rate=20, seed=608), 96.6)
    place(s, noise_bed(6.4, amp=0.05, lo=300, hi=3000, lfo=0.3, seed=609), 100.6)
    steps(s, 101.0, 106.6, step=0.46, amp=0.04, seed=64)
    for k, t in enumerate((101.4, 103.0, 104.6)):
        place(s, chirp(3100 + 300 * k, amp=0.03), t, pan=0.4 - 0.3 * k)
    place(s, noise_bed(7.4, amp=0.03, lo=200, hi=1600, lfo=0.2, seed=610), 107.0)
    place(s, noise_bed(5.0, amp=0.03, lo=200, hi=1500, lfo=0.2, seed=611), END_CARD)


LINES = [("p6s1a", 0.4), ("p6s1b", 4.9),
         ("p6s3a", 12.9), ("p6s3b", 17.6), ("p6s3c", 22.4), ("p6s3d", 27.4), ("p6s3e", 29.7), ("p6s3f", 33.6), ("p6s3g", 37.1),
         ("p6s4a", 41.3), ("p6s4e", 45.0), ("p6s4b", 48.2), ("p6s4c", 51.2), ("p6s4d", 55.2),
         ("p6s5a", 59.7), ("p6s5b", 64.0), ("p6s5c", 67.6), ("p6s5d", 70.3), ("p6s5e", 76.3), ("p6s5f", 80.8), ("p6s5g", 83.0),
         ("p6s6a", 87.0), ("p6s6b", 91.3), ("p6s6g", 96.8), ("p6s6c", 100.9), ("p6s6d", 107.2), ("p6s6e", 109.3)]
if __name__ == "__main__":
    build(6, TOTAL, music, sfx, LINES, f'{AUDIO}/part06.wav')
    print('done')
