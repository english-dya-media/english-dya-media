"""Part 8 · The Red Face — timing, music and sound.
Scene starts: s1 0 (hook: the parade in Samarra, the boy and his father), s2 10.8 (title), s3 15.4 (the boy's question; Babak; Abdullah on
a camel), s4 27.0 (the courtyard at dusk: the decree, the shadow, the drum, the red face), s5 67.0 (after: dawn outside Samarra, Baghdad,
Afshin's prison in 840, the lamp), s6 93.4 (today: the ruins of Bazz above the clouds), end card 119.0, end 124.0"""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import series; series.from_folder(__file__)
from paths import AUDIO
from audio import *
from mix import build
from p02_audio import chirp, tanbur, whoosh, puff, THEME
from p03_audio import thud, steps, rumble, cheer, scrape, swish
from p04_audio import daf, water
from p05_audio import heartbeat, horn
from p06_audio import creak
from p07_audio import chains, trumpet, rustle, falcon_cry
TOTAL = 124.0
S = {"s1": 0.0, "s2": 10.8, "s3": 15.4, "s4": 27.0, "s5": 67.0, "s6": 93.4}
END_CARD = 119.0


def caw(amp=0.06, seed=0):
    """a crow's harsh 'kaah'"""
    r = np.random.default_rng(seed)
    n = int(0.32 * SR); t = np.arange(n) / SR
    f = (520 + 60 * r.random()) * (1 - 0.25 * t / 0.32)
    x = np.sign(np.sin(2 * np.pi * np.cumsum(f) / SR)) * 0.6 + 0.5 * r.standard_normal(n)
    x = bandpass(x.astype(np.float32), 500, 3200) * env(n, 0.02, 0.12)
    return (x * amp).astype(np.float32)


def gasp(amp=0.12, seed=0):
    """a crowd catching its breath at once"""
    r = np.random.default_rng(seed)
    n = int(0.7 * SR); t = np.arange(n) / SR
    x = bandpass(r.standard_normal(n).astype(np.float32), 700, 4200) * np.minimum(1, t / 0.05) * np.exp(-t * 5)
    return (x * amp * 3).astype(np.float32)


def drip(amp=0.05, f0=1400):
    n = int(0.18 * SR); t = np.arange(n) / SR
    f = f0 * (1 + 0.6 * np.exp(-t * 40))
    return (np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 28) * amp).astype(np.float32)


def flap(m, t0, t1, amp=0.04, seed=0):
    """cloth flapping in the wind"""
    r = np.random.default_rng(seed)
    t = t0
    while t < t1:
        place(m, rustle(amp * r.uniform(0.6, 1.0), r.uniform(0.42, 0.6), seed=int(r.integers(1000))), t, pan=r.uniform(-0.1, 0.4))
        t += r.uniform(0.18, 0.4)


LAMENT = [(4, 0), (3, 0.9), (2, 1.6), (1, 2.4), (2, 3.2), (1, 3.8), (0, 4.8)]


def music(m):
    # S1 0-10.8: the parade (as part 1): low drone, frame drum like a heartbeat, a swell into the title
    place(m, drone(73.42, 11.2, amp=0.15, a=2.0, r=0.6), 0.0)
    place(m, drone(110.0, 10.6, amp=0.06, a=3.0, r=1.0), 0.4)
    for i, t in enumerate(np.arange(0.8, 10.6, 2.0)):
        place(m, drum(f0=58, amp=0.24 + 0.03 * i, noise=0.15), t)
    place(m, pad([shur(0, -1), shur(4, -1), shur(0)], 5.0, amp=0.09, a=3.5, r=0.3), 6.0)
    # S2 10.8-15.4: title
    place(m, drum(dur=2.8, f0=44, amp=1.0, noise=0.45), 10.8)
    place(m, drone(73.42, 4.8, amp=0.13, a=0.05, r=2.0), 10.8)
    tanbur(m, THEME[:6], 11.0, amp=0.22, low=True, step=0.75)
    # S3 15.4-27.0: the boy's question; Babak looks down at him; Abdullah
    place(m, drone(73.42, 11.6, amp=0.07, a=1.5, r=1.5), 15.4)
    place(m, pad([shur(0), shur(2), shur(4)], 6.0, amp=0.06, a=2.0, r=2.0, bright=4), 18.4)
    tanbur(m, [(0, 0), (2, 0.6), (4, 1.2), (3, 2.0), (2, 2.6), (0, 3.4)], 18.9, amp=0.13)
    place(m, pad([shur(0, -1), shur(1, -1), shur(3, -1)], 4.6, amp=0.06, a=1.0, r=1.5, bright=3), 22.8)
    tanbur(m, [(1, 0), (0, 0.9)], 23.6, amp=0.10)
    for i, t in enumerate(np.arange(23.0, 26.6, 1.2)):
        place(m, drum(dur=0.9, f0=52, amp=0.16, noise=0.15), t)
    # S4 27.0-67.0: the courtyard
    place(m, drone(36.71, 10.8, amp=0.11, a=1.5, r=1.2), 27.0)
    place(m, drum(dur=2.4, f0=42, amp=0.55, noise=0.25), 27.2)
    place(m, pad([shur(1, -1), shur(3, -1), shur(5, -1)], 6.6, amp=0.05, a=1.0, r=1.5, bright=3), 30.8)
    heartbeat(m, 34.3, 37.4, bpm=60, amp=0.18)
    for i, t in enumerate(np.concatenate([np.arange(37.4, 39.4, 0.4), np.arange(39.4, 40.9, 0.18)])):     # the drum roll
        place(m, drum(dur=0.5, f0=60 if i % 2 else 50, amp=0.18 + 0.012 * i, noise=0.35), t)
    place(m, drum(dur=3.4, f0=36, amp=1.0, noise=0.5), 41.0)                                             # the blow is a drum
    place(m, drone(36.71, 6.4, amp=0.09, a=0.05, r=2.5), 41.0)
    place(m, drone(38.89, 6.0, amp=0.05, a=1.0, r=2.5), 41.4)
    heartbeat(m, 44.0, 47.4, bpm=54, amp=0.14)
    place(m, pluck_fast(shur(4, 1), 3.0, amp=0.16), 46.2)                                               # the red face
    place(m, pad([shur(0, -1), shur(4, -1)], 3.4, amp=0.05, a=0.6, r=1.2, bright=3), 47.6)
    place(m, drone(73.42, 9.4, amp=0.07, a=1.5, r=1.5), 50.0)
    place(m, pad([shur(0), shur(4), shur(0, 1)], 8.6, amp=0.06, a=3.0, r=1.5, bright=5), 50.2)
    tanbur(m, THEME, 54.6, amp=0.11, step=0.8)
    place(m, drone(36.71, 2.6, amp=0.08, a=0.3, r=1.0), 58.6)
    place(m, pad([shur(1, -1), shur(3, -1)], 2.4, amp=0.05, a=0.4, r=1.0, bright=3), 58.6)
    tanbur(m, [(0, 0), (2, 0.5), (4, 1.0), (7, 1.6)], 61.2, amp=0.12)
    place(m, pad([shur(0), shur(4), shur(0, 1)], 4.4, amp=0.06, a=1.0, r=2.0, bright=5), 61.0)
    for i, t in enumerate((63.9, 64.9, 65.9)):
        place(m, drum(dur=1.6, f0=44, amp=0.6 - 0.12 * i, noise=0.3), t)
    # S5 67.0-93.4: after — the lament
    place(m, drone(73.42, 10.4, amp=0.07, a=2.0, r=2.0), 67.0)
    place(m, pad([shur(0, -1), shur(2, -1), shur(4, -1)], 10.0, amp=0.05, a=2.5, r=2.0, bright=3), 67.2)
    tanbur(m, LAMENT, 67.8, amp=0.13, step=0.9)
    tanbur(m, LAMENT[:5], 72.6, amp=0.10, step=0.9)
    place(m, drone(36.71, 6.6, amp=0.10, a=1.0, r=0.4), 77.2)
    place(m, pad([shur(1, -1), shur(3, -1), shur(5, -1)], 5.0, amp=0.05, a=1.0, r=1.0, bright=3), 77.4)
    place(m, drum(dur=3.0, f0=38, amp=0.8, noise=0.4), 82.15)                                          # the door shuts
    place(m, drone(55.0, 9.4, amp=0.05, a=2.0, r=2.0), 83.6)
    tanbur(m, [(4, 0), (3, 1.0), (1, 2.0), (0, 3.2)], 84.4, amp=0.08)
    place(m, bell(220, 3.5, 0.04), 90.5)
    place(m, drone(36.71, 3.0, amp=0.06, a=0.5, r=2.0), 90.4)
    # S6 93.4-124.0: today — the theme over the clouds
    place(m, drone(73.42, 13.8, amp=0.08, a=3.0, r=2.0), 93.4)
    place(m, pad([shur(0), shur(4), shur(0, 1)], 13.5, amp=0.07, a=3.0, r=2.0, bright=5), 93.6)
    tanbur(m, THEME, 95.6, amp=0.13, step=0.9)
    tanbur(m, THEME, 101.2, amp=0.11, step=0.9)
    place(m, pad([shur(2), shur(4), shur(0, 1)], 3.6, amp=0.05, a=0.6, r=1.5, bright=4), 107.4)
    place(m, drone(73.42, 13.4, amp=0.08, a=1.5, r=2.5), 110.6)
    place(m, pad([shur(0), shur(2), shur(4), shur(0, 1)], 13.4, amp=0.08, a=2.0, r=3.0, bright=6), 110.6)
    daf(m, 110.8, 118.8, bpm=84, amp=0.10)
    tanbur(m, THEME, 111.0, amp=0.18, low=True, step=0.85)
    place(m, drum(dur=3.0, f0=40, amp=0.9, noise=0.4), END_CARD - 0.1)
    tanbur(m, [(4, 0), (3, 0.5), (2, 1.0), (0, 1.8)], END_CARD + 0.2, amp=0.18, low=True)
    place(m, pluck_fast(shur(0), 4.0, amp=0.25), END_CARD + 2.2)


def sfx(s):
    # the parade: the crowd, the drums of the procession, the elephant's steps and the chains
    place(s, noise_bed(10.8, amp=0.07, lo=300, hi=2600, lfo=0.6, seed=801), 0.0)
    for t in np.arange(0.6, 10.6, 1.35):
        place(s, drum(dur=0.5, f0=42, amp=0.2, noise=0.1), t)
    for t in np.arange(0.3, 4.0, 0.9):
        place(s, thud(0.12, 50, seed=int(t * 10)), t, pan=0.1)
    chains(s, 0.3, 4.0, step=0.9, amp=0.012, seed=802)
    place(s, trumpet(0.07, 1.4, seed=803), 2.2, pan=-0.2)
    place(s, noise_bed(15.0, amp=0.05, lo=300, hi=2400, lfo=0.6, seed=804), 10.8)
    place(s, noise_bed(5.0, amp=0.03, lo=200, hi=1600, lfo=0.3, seed=805), 18.6)
    for t in np.arange(22.9, 26.8, 0.75):                                                          # the camel's soft steps
        place(s, thud(0.06, 60, seed=int(t * 7)), t, pan=-0.2)
    chains(s, 22.9, 26.6, step=0.75, amp=0.02, seed=806, pan=-0.1)
    # the courtyard: torches, a murmur, then silence
    place(s, crackle(40.0, amp=0.07, rate=7, seed=807), 27.0)
    place(s, noise_bed(14.0, amp=0.035, lo=250, hi=1800, lfo=0.3, seed=808), 27.0)
    place(s, rustle(0.04, 0.8, seed=809), 28.2)                                                    # the decree opens
    place(s, scrape(0.5, amp=0.05, seed=810), 38.6)                                                 # steel lifted
    place(s, swish(0.35, amp=0.10, seed=811), 40.65)
    place(s, gasp(0.16, seed=812), 41.05)
    place(s, rumble(1.6, 0.10, seed=813), 41.0)
    for k, t in enumerate((45.2, 45.6, 46.0)):
        place(s, rustle(0.06, 0.5, seed=814 + k), t, pan=-0.1 + 0.1 * k)                          # the sleeve
    place(s, noise_bed(9.0, amp=0.02, lo=200, hi=1200, lfo=0.2, seed=817), 58.0)
    # after: dawn wind and crows; the river; the tower; the cell; the lamp
    place(s, noise_bed(5.4, amp=0.08, lo=200, hi=2200, lfo=0.25, seed=820), 67.0)
    for k, t in enumerate((67.8, 69.1, 70.4, 71.2)):
        place(s, caw(0.05, seed=821 + k), t, pan=0.3 - 0.2 * k)
    place(s, water(5.4, amp=0.05, seed=825), 72.0)
    for k, t in enumerate((72.6, 74.8)):
        place(s, chirp(2600 + 400 * k, amp=0.03), t, pan=-0.3)
    place(s, noise_bed(6.6, amp=0.06, lo=150, hi=1500, lfo=0.2, seed=826), 77.2)
    place(s, crackle(6.4, amp=0.06, rate=6, seed=827), 77.2)
    steps(s, 77.6, 80.8, step=0.48, amp=0.05, seed=828)
    chains(s, 77.6, 80.8, step=0.48, amp=0.02, seed=829)
    place(s, creak(0.7, 0.08, seed=830), 81.5)
    place(s, thud(0.45, 48, seed=831), 82.15)
    place(s, noise_bed(9.8, amp=0.015, lo=100, hi=600, lfo=0.1, seed=832), 83.6)
    for t in (84.3, 86.1, 87.9, 89.3):
        place(s, drip(0.03), t, pan=0.3)
    chains(s, 86.9, 87.4, step=0.3, amp=0.015, seed=833)
    place(s, crackle(2.2, amp=0.03, rate=4, seed=834), 88.4)
    place(s, puff(0.08), 90.4)
    # today: the wind on the peak, the cloth, a falcon far away
    place(s, noise_bed(30.6, amp=0.07, lo=200, hi=2600, lfo=0.15, seed=840), 93.4)
    place(s, noise_bed(30.6, amp=0.03, lo=600, hi=5000, lfo=0.5, seed=841), 93.4)
    flap(s, 101.0, 107.4, amp=0.035, seed=842)
    place(s, falcon_cry(0.035), 96.4, pan=0.4)
    place(s, falcon_cry(0.03), 113.0, pan=-0.3)
    place(s, whoosh(2.0, amp=0.06, seed=843), 107.0)


LINES = [("p8s1a", 4.4), ("p8s1b", 6.1),
         ("p8s3a", 15.7),
         ("p8s4a", 28.8), ("p8s4b", 31.2), ("p8s4c", 47.9), ("p8s4d", 50.3), ("p8s4e", 54.8),
         ("p8s5a", 72.5), ("p8s5b", 77.6), ("p8s5c", 85.2), ("p8s5d", 88.8),
         ("p8s6a", 95.0), ("p8s6b", 98.4), ("p8s6c", 101.4), ("p8s6d", 107.9), ("p8s6e", 111.0), ("p8s6f", 114.7)]
if __name__ == "__main__":
    build(8, TOTAL, music, sfx, LINES, f'{AUDIO}/part08.wav')
    print('done')
