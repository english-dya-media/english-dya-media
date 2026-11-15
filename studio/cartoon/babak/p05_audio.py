"""Part 5 · The Silver Trap — timing, music and sound. Scene starts: s1 0, s2 21.8, s3 26.4, s4 65.6, s5 99.0, end card 116.4, end 121.0"""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import series; series.from_folder(__file__)
from paths import AUDIO
from audio import *
from mix import build
from p02_audio import chirp, snort, clash, whoosh, tanbur, THEME
from p03_audio import thud, hooves, steps, rumble, cheer, scrape, swish, splash
from p04_audio import arrow, neigh, clap, daf
TOTAL = 121.0
S = {"s1": 0.0, "s2": 21.8, "s3": 26.4, "s4": 65.6, "s5": 99.0}
END_CARD = 116.4


def coins(m, t0, n=7, amp=0.035, pan=0.1, seed=0):
    """silver coins: small bright clinks"""
    r = np.random.default_rng(seed)
    for k in range(n):
        place(m, bell(2200 + 900 * r.random(), 0.5, amp * r.uniform(0.6, 1.0)), t0 + 0.045 * k + r.uniform(0, 0.03), pan=pan + r.uniform(-0.2, 0.2))


def heartbeat(m, t0, t1, bpm=72, amp=0.35):
    t = t0
    while t < t1:
        place(m, drum(dur=0.4, f0=48, amp=amp, noise=0.05), t)
        place(m, drum(dur=0.35, f0=44, amp=amp * 0.7, noise=0.05), t + 0.22)
        t += 60 / bpm


def breath(m, t0, t1, rate=0.7, amp=0.05, seed=0):
    """heavy breathing after running"""
    r = np.random.default_rng(seed)
    t = t0
    while t < t1:
        n = int(0.42 * SR); tt = np.arange(n) / SR
        x = bandpass(r.standard_normal(n).astype(np.float32), 500, 2500) * np.sin(np.pi * tt / 0.42) ** 2
        place(m, (x * amp * r.uniform(0.8, 1.1)).astype(np.float32), t, pan=r.uniform(-0.2, 0.2))
        t += rate


def horn(dur=2.5, amp=0.12, f0=110.0):
    """a low war horn"""
    n = int(dur * SR); t = np.arange(n) / SR
    f = f0 * (1 + 0.02 * np.minimum(1, t / 0.3))
    ph = 2 * np.pi * np.cumsum(f) / SR
    x = sum(w * np.sin(k * ph) for k, w in ((1, 1.0), (2, 0.6), (3, 0.45), (4, 0.25), (5, 0.15)))
    return lowpass((x * env(n, 0.25, 0.8) * amp).astype(np.float32), 1800)


def music(m):
    # S1 0-21.8: Afshin's tent: low drone, the spy's heartbeat, a dark pad
    place(m, drone(36.71, 21.8, amp=0.10, a=1.5, r=2.0), 0.0)
    place(m, pad([shur(0, -1), shur(1, -1), shur(3, -1)], 9.0, amp=0.06, a=2.5, r=2.0, bright=3), 0.4)
    heartbeat(m, 7.6, 10.6, bpm=84, amp=0.30)
    place(m, pad([shur(1, -1), shur(3, -1), shur(5, -1)], 8.0, amp=0.06, a=1.0, r=2.0, bright=3), 10.6)
    place(m, drum(dur=2.4, f0=44, amp=0.7, noise=0.3), 15.8)
    tanbur(m, [(4, 0), (3, 0.7), (1, 1.4), (0, 2.2)], 18.9, amp=0.12)
    # S2 21.8-26.4: title
    place(m, drum(dur=3.0, f0=42, amp=1.0, noise=0.45), 21.8)
    tanbur(m, THEME[:6], 22.1, amp=0.22, low=True, step=0.8)
    place(m, drone(73.42, 4.8, amp=0.09, a=0.05, r=2.0), 21.8)
    # S3 26.4-65.6: the slow cage: a patient march
    place(m, drone(36.71, 26.2, amp=0.08, a=1.5, r=1.5), 26.4)
    for i, t in enumerate(np.arange(26.6, 46.2, 1.1)):
        place(m, drum(dur=0.9, f0=56, amp=0.20 + (0.06 if i % 4 == 0 else 0), noise=0.2), t)
    place(m, pad([shur(0, -1), shur(2, -1), shur(4, -1)], 9.0, amp=0.06, a=2.0, r=2.0, bright=4), 27.0)
    place(m, pad([shur(1, -1), shur(3, -1), shur(5, -1)], 9.0, amp=0.06, a=2.0, r=2.0, bright=4), 36.0)
    for i, t in enumerate(np.arange(46.4, 49.0, 0.32)):                   # the war drums
        place(m, drum(dur=0.7, f0=50 if i % 2 else 42, amp=0.55, noise=0.35), t)
    place(m, horn(2.4, 0.10, 98.0), 46.6)
    place(m, pad([shur(0, -1), shur(4, -1), shur(0)], 4.0, amp=0.06, a=1.0, r=2.0, bright=3), 49.0)
    tanbur(m, [(4, 0), (3, 0.8), (2, 1.6), (0, 2.6)], 49.4, amp=0.10)
    place(m, drone(36.71, 13.0, amp=0.10, a=1.0, r=1.5), 52.6)
    place(m, pad([shur(0, -1), shur(1, -1), shur(3, -1)], 12.6, amp=0.06, a=2.0, r=2.0, bright=3), 52.8)
    place(m, drum(dur=2.4, f0=44, amp=0.7, noise=0.3), 63.2)
    # S4 65.6-99.0: the silver road, the fire, the trap
    place(m, drone(73.42, 7.8, amp=0.05, a=1.5, r=1.5), 65.6)
    tanbur(m, [(0, 0), (2, 0.6), (3, 1.2), (4, 1.8), (3, 2.6), (2, 3.2)], 66.0, amp=0.12, step=1.0)
    place(m, pad([shur(0), shur(2), shur(4)], 7.0, amp=0.05, a=2.0, r=2.0, bright=4), 66.0)
    place(m, drone(36.71, 9.6, amp=0.07, a=1.5, r=1.0), 73.4)
    tanbur(m, [(0, 0), (2, 0.7), (1, 1.2), (0, 1.8)], 78.6, amp=0.14, low=True)
    for i, t in enumerate(np.arange(83.0, 87.0, 0.375)):                 # the night attack
        place(m, drum(dur=0.6, f0=62 if i % 2 else 50, amp=0.28 + 0.03 * i, noise=0.3), t)
    place(m, pad([shur(1, -1), shur(3, -1), shur(5, -1)], 4.0, amp=0.06, a=0.5, r=0.5, bright=5), 83.0)
    place(m, drum(dur=2.5, f0=40, amp=1.0, noise=0.5), 87.0)                 # the trap
    place(m, horn(2.6, 0.14, 92.0), 87.1); place(m, horn(2.2, 0.10, 138.0), 87.4)
    place(m, drone(38.89, 7.8, amp=0.12, a=0.05, r=1.5), 87.0)
    for i, t in enumerate(np.arange(89.0, 95.0, 0.3)):
        place(m, drum(dur=0.5, f0=58 if i % 2 else 46, amp=0.36, noise=0.35), t)
    place(m, drone(36.71, 4.4, amp=0.08, a=0.3, r=2.5), 94.8)
    # S5 99.0-121.0: dawn in the ravine, the face on the ridge
    place(m, pad([shur(0, -1), shur(4, -1), shur(0)], 7.0, amp=0.05, a=3.0, r=2.0, bright=3), 99.2)
    tanbur(m, [(4, 0), (3, 0.9), (2, 1.8)], 100.0, amp=0.09)
    place(m, drone(36.71, 9.6, amp=0.08, a=1.5, r=1.0), 103.4)
    heartbeat(m, 106.0, 112.6, bpm=66, amp=0.26)
    place(m, pad([shur(1, -1), shur(3, -1), shur(5, -1)], 6.0, amp=0.07, a=1.0, r=1.5, bright=4), 106.4)
    place(m, drum(dur=2.6, f0=42, amp=0.8, noise=0.35), 110.0)
    place(m, drone(38.89, 6.0, amp=0.06, a=1.0, r=2.0), 110.0)
    place(m, drone(36.71, 8.4, amp=0.08, a=1.0, r=2.0), 112.6)
    place(m, drum(dur=2.5, f0=46, amp=0.85, noise=0.4), END_CARD - 0.1)
    tanbur(m, THEME, END_CARD + 0.1, amp=0.18, low=True, step=0.8)
    place(m, pad([shur(0), shur(4), shur(0, 1)], 4.6, amp=0.07, a=1.0, r=2.0, bright=5), END_CARD)


def sfx(s):
    # tent: wind on the canvas, the lamps
    place(s, noise_bed(21.8, amp=0.05, lo=150, hi=900, lfo=0.2, seed=501), 0.0)
    place(s, crackle(21.8, amp=0.03, rate=4, seed=502), 0.0)
    steps(s, 0.8, 3.6, step=0.6, amp=0.05, seed=503)
    place(s, snort(seed=4, amp=0.03), 2.4, pan=0.6)
    place(s, swish(0.4, amp=0.05, seed=504), 11.0)                         # the dagger
    place(s, snap_(0.12), 11.6)                                             # the rope parts
    coins(s, 12.7, 8, 0.04, seed=505)                                       # the purse in his hands
    coins(s, 20.2, 4, 0.025, seed=506)
    # title: silver falling
    for k in range(10):
        coins(s, 22.0 + 0.32 * k, 3, 0.03, pan=-0.3 + 0.06 * k, seed=510 + k)
    # forts: stones set down, a hammer
    place(s, noise_bed(4.4, amp=0.04, lo=300, hi=2500, lfo=0.3, seed=520), 26.4)
    for k, t in enumerate((27.3, 28.5, 29.4, 30.2)):
        place(s, thud(0.14, 80, seed=521 + k), t, pan=0.2)
    for t in np.arange(26.8, 30.6, 0.55):
        place(s, knock(0.10), t, pan=-0.4)
    # the camp: voices far away, horses, a smith
    place(s, cheer(11.2, amp=0.05, seed=530), 30.8)
    place(s, neigh(0.05), 31.6, pan=-0.5)
    for t in np.arange(31.0, 42.0, 1.3):
        place(s, bell(1800, 0.6, 0.012), t, pan=0.6)
    # the trenches: picks and shovels
    for k, t in enumerate(np.arange(42.3, 46.2, 0.62)):
        place(s, thud(0.12, 120, seed=540 + k), t, pan=-0.3)
        place(s, scrape(0.35, amp=0.05, seed=550 + k), t + 0.3, pan=0.3)
    # the drums are music; dusk: wind
    place(s, noise_bed(3.8, amp=0.08, lo=200, hi=1600, lfo=0.25, seed=560), 49.0)
    # the war room at Bazz: the lamp, then pebbles on the table
    place(s, crackle(13.0, amp=0.04, rate=5, seed=561), 52.6)
    place(s, noise_bed(13.0, amp=0.03, lo=150, hi=800, lfo=0.2, seed=562), 52.6)
    for k, t in enumerate((60.1, 60.6, 61.1, 61.6, 62.1, 62.6)):
        place(s, knock(0.07), t, pan=0.2)
    # the silver road: mule bells, hooves, steps
    place(s, noise_bed(7.8, amp=0.04, lo=300, hi=3000, lfo=0.4, seed=570), 65.6)
    hooves(s, 65.7, 73.2, step=0.5, amp=0.04, pan=0.2, seed=571)
    for t in np.arange(65.9, 73.2, 0.5):
        place(s, bell(1500 + 300 * ((t * 2) % 2), 0.7, 0.014), t, pan=0.1)
    for k, t in enumerate((70.4, 71.1, 72.6)):
        place(s, chirp(3100 + 250 * k, amp=0.04), t, pan=-0.5)
    # the fire at night
    place(s, crackle(9.6, amp=0.10, seed=580), 73.4)
    for k, t in enumerate((74.2, 76.1, 79.5, 81.8)):
        place(s, chirp(4300 + 150 * k, dur=0.05, amp=0.012), t, pan=0.6)
    # the attack
    steps(s, 83.0, 87.0, step=0.18, amp=0.06, seed=581)
    place(s, noise_bed(4.0, amp=0.08, lo=300, hi=2600, lfo=1.2, seed=582), 83.0)
    for k in range(6):
        place(s, swish(0.7, amp=0.09, seed=583 + k), 87.4 + 0.15 * k, pan=-0.6 + 0.24 * k)      # the torches flare up
    hooves(s, 87.2, 98.5, step=0.22, amp=0.07, pan=-0.3, seed=590)
    hooves(s, 87.5, 98.5, step=0.25, amp=0.06, pan=0.4, seed=591)
    place(s, cheer(8.0, amp=0.10, seed=592), 88.5)
    for k, t in enumerate((89.0, 90.0, 91.2, 92.4, 93.6)):
        place(s, clash(0.07, seed=593 + k), t, pan=(-0.4 if k % 2 else 0.4))
    for k, t in enumerate((88.4, 89.7, 92.0)):
        place(s, neigh(0.06, seed=k), t, pan=(0.5 if k % 2 else -0.5))
    steps(s, 94.8, 99.0, step=0.2, amp=0.06, seed=595)
    # dawn: breathing, birds, wind; then riders on the ridge
    breath(s, 99.0, 104.0, rate=0.75, amp=0.06, seed=600)
    place(s, noise_bed(22.0, amp=0.04, lo=200, hi=1800, lfo=0.15, seed=601), 99.0)
    for k, t in enumerate((99.6, 100.2, 101.5, 104.2, 105.0, 117.0)):
        place(s, chirp(3000 + 300 * (k % 3), amp=0.035), t, pan=0.5 - 0.3 * (k % 4))
    hooves(s, 106.0, 110.0, step=0.8, amp=0.03, pan=0.0, seed=602)
    place(s, snort(seed=6, amp=0.06), 107.6, pan=0.2)
    place(s, snort(seed=7, amp=0.05), 111.2, pan=-0.2)


def snap_(amp=0.12):
    from p03_audio import snap
    return snap(amp)


LINES = [("p5s1a", 4.8), ("p5s1b", 8.3), ("p5s1c", 13.2), ("p5s1d", 16.7),
         ("p5s3a", 35.6), ("p5s3b", 38.7), ("p5s3c", 53.6), ("p5s3d", 57.4), ("p5s3e", 59.9),
         ("p5s4a", 74.0), ("p5s4b", 75.6), ("p5s4c", 78.8), ("p5s4d", 80.7), ("p5s4e", 90.5), ("p5s4f", 92.9),
         ("p5s5a", 113.4)]
if __name__ == "__main__":
    build(5, TOTAL, music, sfx, LINES, f'{AUDIO}/part05.wav')
    print('done')
