"""Part 8 · The Blacksmith's Banner — timing, music and sound.
Scene starts: s1 0 (hook: a rock rolls down at Fereydun's tent in the night; he wakes and stops it: "Stop!"), s2 8.6 (title: the Kaviani banner
against the dawn sky), s3 13.2 (Kaveh and the people come to Fereydun's camp; the apron on the spear, a good sign; it is dressed in silk, gold
and jewels with red, yellow and violet ribbons: the Kaviani banner), s4 51.2 (the two older brothers; the mace drawn in the dust; the smiths
forge it; it shines like the sun, like the mace of Zahhak's dream), s5 84.8 (dawn: Fereydun leaves his mother; the army sets out),
s6 97.0 (night: Sorush teaches him secret words; the jealous brothers push the rock; he stops it with a word and says nothing),
s7 135.2 (the Arvand: the river keeper will not send the boats without the king's seal), end card 154.4, end 159.4"""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import series; series.from_folder(__file__)
from paths import AUDIO
from audio import *
from mix import build
from zsfx import *
from p07_audio import anvil, murmur, cheer

TOTAL = 159.4
S = {"s1": 0.0, "s2": 8.6, "s3": 13.2, "s4": 51.2, "s5": 84.8, "s6": 97.0, "s7": 135.2}
END_CARD = 154.4
ROLL1, STOP1 = 0.9, 4.0          # the hook: the rock starts rolling / the spell stops it (part time)
ROLL2, STOP2 = 121.2, 124.75     # … and in s6
FORGE_HITS = [71.45, 71.85, 72.25, 72.65, 73.05, 73.45, 73.85]
BANNER_POPS = [37.0, 37.7, 38.4, 39.1, 39.8, 40.5, 41.2]   # jewels set on the banner (s3 E)

KAV = [(0, 0), (2, 0.5), (4, 1.0), (5, 1.5), (4, 2.0), (5, 2.4), (7, 2.9), (4, 3.6)]
MARCH = [(0, 0), (0, 0.5), (2, 1.0), (4, 1.5), (3, 2.0), (2, 2.5), (1, 3.0), (0, 3.5)]


def rumble(dur, amp=0.2, seed=0):
    """a big rock rolling over stones: a low rolling roar with knocks"""
    r = np.random.default_rng(seed)
    n = int(dur * SR); t = np.arange(n) / SR
    x = lowpass(r.standard_normal(n).astype(np.float32), 180) * 3
    x *= (0.6 + 0.4 * np.sin(2 * np.pi * 3.1 * t) * np.sin(2 * np.pi * 1.3 * t))
    x *= np.minimum(1, t / 0.3) * np.minimum(1, (dur - t) / 0.15)
    out = (x * amp).astype(np.float32)
    for k in range(int(dur * 5)):
        tt = r.uniform(0, max(0.01, dur - 0.3))
        th = thud(amp * 0.35, f0=60 + 30 * r.random(), seed=seed * 50 + k)
        i = int(tt * SR); m = min(len(th), n - i)
        out[i:i + m] += th[:m]
    return out


def gravel(dur=1.2, amp=0.08, seed=0):
    """small stones and dust settling"""
    r = np.random.default_rng(seed)
    n = int(dur * SR); t = np.arange(n) / SR
    x = (r.random(n) < 0.004).astype(np.float32) * r.uniform(0.3, 1.0, n).astype(np.float32)
    x = bandpass(x, 1200, 6000) * 8 + bandpass(r.standard_normal(n).astype(np.float32), 300, 2000) * 0.3
    return (x * np.exp(-t * 2.2) * amp).astype(np.float32)


def shimmer(m, t0, dur=3.0, amp=0.03, seed=0, base=880):
    """a magic glitter: soft high bells"""
    r = np.random.default_rng(seed)
    for k in range(int(dur * 6)):
        place(m, bell(base * 2 ** (r.integers(0, 12) / 12) * (2 if r.random() < 0.3 else 1), 1.6, amp * r.uniform(0.5, 1.0)),
              t0 + r.uniform(0, dur), pan=r.uniform(-0.6, 0.6))


def water(dur, amp=0.05, seed=0):
    """a wide river lapping on the bank"""
    x = noise_bed(dur, amp=amp, lo=200, hi=1800, lfo=0.35, seed=seed)
    return x


def chime(amp=0.05, seed=0):
    """a jewel set in place: a short bright ping"""
    return bell(1760 + 220 * (seed % 4), 0.8, amp)


def music(m):
    # S1 0-8.6: night; the rock; "Stop!"
    place(m, drone(36.71, 8.8, amp=0.10, a=0.8, r=1.0), 0.0)
    place(m, pad([shur(1, -1), shur(5, -1), shur(1)], 4.0, amp=0.05, a=0.8, r=0.8, bright=4), 0.0)
    for i, t in enumerate(np.arange(ROLL1 + 0.3, STOP1, 0.3)):
        place(m, drum(dur=0.5, f0=60 if i % 2 else 52, amp=0.16 + 0.03 * i, noise=0.25), t)
    place(m, drum(dur=3.0, f0=40, amp=1.0, noise=0.45), STOP1)
    place(m, pad([shur(0), shur(4), shur(0, 1)], 4.4, amp=0.08, a=0.1, r=2.0, bright=6), STOP1)
    place(m, bell(587, 2.6, 0.05), STOP1 + 0.05)
    tanbur(m, [(2, 0), (1, 0.7), (0, 1.5)], 6.0, amp=0.08, step=1.0)
    # S2 8.6-13.2: title over the banner at dawn
    place(m, drum(dur=3.2, f0=40, amp=0.9, noise=0.4), 8.6)
    place(m, drone(36.71, 4.9, amp=0.12, a=0.1, r=1.4), 8.6)
    place(m, pad([shur(0), shur(4), shur(0, 1), shur(2, 1)], 4.8, amp=0.10, a=0.4, r=1.6, bright=7), 8.6)
    tanbur(m, ZTHEME, 9.0, amp=0.22, low=True, step=0.85)
    # S3 13.2-51.2: the people come; the sign; the banner
    place(m, pad([shur(0), shur(2), shur(4)], 7.4, amp=0.06, a=1.5, r=1.2, bright=5), 13.2)
    for t in np.arange(13.4, 20.4, 0.8):
        place(m, drum(dur=0.8, f0=62, amp=0.14, noise=0.15), t)
    tanbur(m, KAV, 14.0, amp=0.10, step=1.0)
    place(m, drum(dur=1.6, f0=48, amp=0.45, noise=0.3), 20.4)
    place(m, pad([shur(0, -1), shur(4, -1), shur(0)], 5.8, amp=0.05, a=0.8, r=1.0, bright=5), 20.4)
    place(m, pad([shur(2), shur(4), shur(0, 1)], 5.0, amp=0.06, a=1.0, r=1.0, bright=6), 26.2)     # the sign
    place(m, bell(880, 2.4, 0.03), 29.4)
    place(m, drum(dur=1.4, f0=52, amp=0.4, noise=0.25), 31.3)
    tanbur(m, [(0, 0), (2, 0.4), (4, 0.8), (5, 1.3), (4, 1.8)], 31.6, amp=0.12, step=0.9, low=True)
    place(m, pad([shur(0), shur(4), shur(0, 1), shur(2, 1)], 8.2, amp=0.07, a=1.0, r=1.5, bright=7), 35.6)   # dressing the banner
    tanbur(m, ZTHEME, 36.0, amp=0.09, step=1.1)
    place(m, drum(dur=3.0, f0=42, amp=0.9, noise=0.4), 43.6)                                  # the banner rises
    place(m, pad([shur(0), shur(4), shur(0, 1), shur(2, 1)], 7.6, amp=0.11, a=0.3, r=2.0, bright=7), 43.6)
    tanbur(m, KAV, 44.0, amp=0.18, low=True, step=0.75)
    for i, t in enumerate(np.arange(46.8, 50.8, 0.4)):
        place(m, drum(dur=0.6, f0=60 if i % 2 else 50, amp=0.24, noise=0.25), t)
    # S4 51.2-84.8: the brothers; the drawing; the forge; the mace
    place(m, pad([shur(0), shur(2), shur(4)], 11.0, amp=0.05, a=1.5, r=1.5, bright=5), 51.2)
    tanbur(m, [(0, 0), (2, 0.6), (1, 1.2), (0, 1.8)], 51.8, amp=0.09, step=1.0)
    tanbur(m, [(4, 0), (3, 0.6), (2, 1.2), (0, 2.0)], 57.0, amp=0.08, step=1.0)
    place(m, drone(55.0, 6.6, amp=0.06, a=1.0, r=1.0), 62.2)                                  # the drawing
    place(m, pad([shur(1, -1), shur(5, -1), shur(1)], 6.4, amp=0.04, a=1.0, r=1.0, bright=4), 62.2)
    for k, t in enumerate((65.2, 66.2, 67.2)):
        place(m, pluck_fast(shur(k + 2), 1.4, amp=0.10), t, pan=0.2)
    place(m, drum(dur=1.4, f0=50, amp=0.4, noise=0.3), 68.6)
    for i, t in enumerate(FORGE_HITS):                                                       # the forge
        place(m, drum(dur=0.5, f0=66 if i % 2 else 56, amp=0.25, noise=0.25), t)
    tanbur(m, [(0, 0), (2, 0.4), (4, 0.8), (2, 1.2), (4, 1.6), (5, 2.0), (7, 2.5)], 71.4, amp=0.12, step=0.85, low=True)
    place(m, drum(dur=3.0, f0=42, amp=0.95, noise=0.4), 74.2)                                 # it shines
    place(m, pad([shur(0), shur(4), shur(0, 1), shur(2, 1)], 3.8, amp=0.11, a=0.2, r=1.5, bright=7), 74.2)
    place(m, bell(1175, 2.4, 0.04), 74.6)
    place(m, drone(36.71, 3.6, amp=0.09, a=0.4, r=0.8), 77.8)                                 # the dream
    place(m, pad([shur(1, -1), shur(5, -1), shur(1)], 3.4, amp=0.07, a=0.3, r=0.8, bright=5), 77.8)
    heartbeat(m, 78.0, 81.0, bpm=78, amp=0.14)
    place(m, pad([shur(0), shur(2), shur(4)], 3.8, amp=0.06, a=0.5, r=1.5, bright=5), 81.2)
    tanbur(m, [(4, 0), (2, 0.5), (0, 1.2)], 82.6, amp=0.10, step=1.0)
    # S5 84.8-97.0: the mother; the march
    place(m, pad([shur(0), shur(2), shur(4)], 6.4, amp=0.06, a=1.5, r=1.5, bright=5), 84.8)
    tanbur(m, [(2, 0), (1, 0.8), (0, 1.6), (1, 2.6), (0, 3.4)], 85.4, amp=0.08, step=1.0)
    place(m, bell(659, 2.4, 0.03), 89.0)
    place(m, drum(dur=2.4, f0=44, amp=0.7, noise=0.35), 91.0)                                 # the march
    place(m, pad([shur(0), shur(4), shur(0, 1)], 6.0, amp=0.09, a=0.4, r=1.5, bright=6), 91.0)
    for i, t in enumerate(np.arange(91.2, 96.8, 0.5)):
        place(m, drum(dur=0.6, f0=60 if i % 2 else 50, amp=0.22 + (0.06 if i % 4 == 0 else 0), noise=0.2), t)
    tanbur(m, MARCH, 91.4, amp=0.16, low=True, step=0.7)
    # S6 97.0-135.2: Sorush; the brothers; the rock
    place(m, drone(36.71, 15.0, amp=0.06, a=1.5, r=1.5), 97.0)
    place(m, pad([shur(0, 1), shur(4, 1), shur(2, 1)], 14.6, amp=0.05, a=2.0, r=2.0, bright=8), 97.6)
    shimmer(m, 98.6, 13.0, amp=0.018, seed=81)
    place(m, drone(36.71, 9.6, amp=0.10, a=0.6, r=0.6), 112.0)                                # the brothers
    place(m, pad([shur(1, -1), shur(5, -1)], 9.0, amp=0.05, a=1.0, r=0.6, bright=4), 112.0)
    heartbeat(m, 117.6, 121.2, bpm=84, amp=0.16)
    for i, t in enumerate(np.arange(ROLL2 + 0.2, STOP2, 0.28)):
        place(m, drum(dur=0.5, f0=60 if i % 2 else 52, amp=0.16 + 0.025 * i, noise=0.25), t)
    place(m, drum(dur=3.0, f0=40, amp=1.0, noise=0.45), STOP2)
    place(m, pad([shur(0), shur(4), shur(0, 1)], 5.4, amp=0.09, a=0.1, r=2.0, bright=6), STOP2)
    place(m, bell(587, 2.6, 0.05), STOP2 + 0.05)
    place(m, pad([shur(1, -1), shur(0, -1), shur(4, -1)], 4.4, amp=0.05, a=1.0, r=1.5, bright=4), 130.8)
    tanbur(m, [(2, 0), (1, 0.9), (0, 1.8)], 131.4, amp=0.08, step=1.1)
    # S7 135.2-159.4: the river
    place(m, pad([shur(0), shur(2), shur(4)], 7.2, amp=0.06, a=1.5, r=1.2, bright=5), 135.2)
    tanbur(m, [(0, 0), (2, 0.6), (4, 1.2), (3, 1.9), (2, 2.5), (0, 3.2)], 135.8, amp=0.09, step=1.0)
    place(m, drum(dur=1.4, f0=54, amp=0.4, noise=0.25), 142.4)
    place(m, drone(36.71, 8.0, amp=0.10, a=0.3, r=1.0), 145.8)                               # the refusal
    place(m, pad([shur(1, -1), shur(5, -1), shur(1)], 6.4, amp=0.06, a=0.5, r=1.0, bright=5), 145.8)
    place(m, drum(dur=1.8, f0=46, amp=0.55, noise=0.3), 150.5)
    place(m, drum(dur=3.0, f0=42, amp=0.85, noise=0.4), 152.2)
    place(m, pad([shur(0), shur(4), shur(0, 1)], 7.0, amp=0.09, a=0.4, r=2.5, bright=6), 152.2)
    tanbur(m, ZTHEME[:5], 152.6, amp=0.14, low=True, step=0.9)
    place(m, drum(dur=3.0, f0=40, amp=0.8, noise=0.4), END_CARD)
    place(m, drone(36.71, 5.0, amp=0.10, a=0.2, r=2.0), END_CARD)
    tanbur(m, ZTHEME[:4], END_CARD + 0.8, amp=0.12, low=True, step=0.9)


def sfx(s):
    # S1: night crickets; the rock; the stop; the dust
    crickets(s, 0.0, 8.6, amp=0.01, seed=81)
    place(s, scrape(0.6, 0.08, seed=81), ROLL1 - 0.3, pan=0.4)
    place(s, rumble(STOP1 - ROLL1, 0.22, seed=81), ROLL1, pan=0.3)
    place(s, thud(0.4, f0=52, seed=81), STOP1)
    place(s, gravel(1.6, 0.08, seed=81), STOP1 + 0.1, pan=0.2)
    # S2: wind under the banner
    place(s, gust(2.4, 0.08, seed=81), 9.0)
    place(s, noise_bed(4.6, amp=0.03, lo=300, hi=2600, lfo=0.25, seed=801), 8.6)
    # S3: the crowd; the cheer
    steps(s, 13.4, 20.2, step=0.32, amp=0.03, seed=81, pan=-0.3)
    place(s, murmur(7.0, 0.04, seed=81), 13.4)
    place(s, noise_bed(38.0, amp=0.025, lo=300, hi=2600, lfo=0.2, seed=802), 13.2)
    for k, t in enumerate((13.9, 16.8, 22.9, 33.6, 45.2)):
        place(s, chirp(2900 + 300 * (k % 3), amp=0.03), t, pan=0.4 - 0.2 * (k % 4))
    place(s, murmur(4.0, 0.03, seed=82), 26.4)
    place(s, cheer(3.0, 0.07, seed=81), 35.1)
    place(s, rustle(0.05, 1.0, seed=81), 35.8)
    for k, t in enumerate(BANNER_POPS):
        place(s, chime(0.04, seed=k), t, pan=0.2 * ((k % 3) - 1))
    place(s, rustle(0.06, 1.2, seed=82), 39.6)
    place(s, gust(2.0, 0.08, seed=82), 43.6)
    place(s, cheer(6.0, 0.12, seed=82), 44.2)
    place(s, cheer(5.0, 0.07, seed=83), 46.0, pan=0.3)
    # S4: the camp; the drawing stick; the forge; the gold
    place(s, noise_bed(33.6, amp=0.025, lo=300, hi=2600, lfo=0.2, seed=803), 51.2)
    steps(s, 60.6, 62.0, step=0.36, amp=0.035, seed=82, pan=0.3)
    for k in range(9):
        place(s, scrape(0.35, 0.04, seed=90 + k), 62.9 + k * 0.6, pan=0.1)
    place(s, crackle(6.0, amp=0.08, rate=14, seed=804), 68.6)
    for k, t in enumerate(FORGE_HITS):
        place(s, anvil(0.09, seed=80 + k), t, pan=-0.3 if k % 2 else 0.3)
    place(s, hiss(0.9, 0.05, seed=81), 74.0, pan=0.2)
    place(s, noise_bed(3.4, amp=0.02, lo=200, hi=1200, lfo=0.3, seed=805), 77.8)
    for k in range(5):
        place(s, chime(0.025, seed=k + 3), 82.4 + 0.12 * k, pan=0.3)
    # S5: dawn birds; the march
    for k, t in enumerate((85.0, 86.4, 88.2, 90.0)):
        place(s, chirp(3000 + 250 * (k % 3), amp=0.035), t, pan=0.4 - 0.25 * (k % 3))
    steps(s, 91.2, 96.8, step=0.25, amp=0.045, seed=83)
    hooves(s, 91.6, 96.6, step=0.42, amp=0.06, pan=0.2, seed=81)
    place(s, gust(2.4, 0.07, seed=83), 92.0)
    # S6: night; the fire; Sorush; the hilltop; the rock
    crickets(s, 97.0, 135.2, amp=0.009, seed=82)
    place(s, crackle(15.0, amp=0.07, rate=10, seed=806), 97.0)
    wings(s, 100.6, n=5, rate=0.22, amp=0.035, seed=81)
    wings(s, 111.2, n=4, rate=0.24, amp=0.03, seed=82)
    place(s, gust(2.0, 0.07, seed=84), 112.0)
    place(s, owl(0.04), 113.6, pan=-0.5)
    for k, t in enumerate((119.4, 120.0, 120.6)):
        place(s, grunt(0.06, seed=80 + k), t, pan=0.2 * (k - 1))
        place(s, scrape(0.5, 0.06, seed=95 + k), t + 0.1, pan=0.2)
    place(s, rumble(STOP2 - ROLL2, 0.22, seed=82), ROLL2, pan=0.3)
    place(s, thud(0.4, f0=52, seed=82), STOP2)
    place(s, gravel(1.8, 0.08, seed=82), STOP2 + 0.1, pan=0.2)
    steps(s, 131.4, 133.4, step=0.4, amp=0.025, seed=84, pan=0.5)
    # S7: the river; the army; the shouts
    place(s, water(24.2, 0.05, seed=81), 135.2)
    hooves(s, 135.4, 141.0, step=0.45, amp=0.05, pan=-0.2, seed=82)
    steps(s, 135.4, 141.0, step=0.3, amp=0.03, seed=85, pan=0.2)
    place(s, murmur(6.0, 0.03, seed=84), 136.0)
    place(s, snort(0.08, seed=81), 143.0, pan=-0.3)
    place(s, gust(2.4, 0.07, seed=85), 152.2)
    place(s, neigh(0.07, seed=81), 153.4, pan=-0.3)


LINES = [("p8s1a", 3.85), ("p8s1b", 5.3),
         ("p8s3a", 13.6), ("p8s3b", 17.7), ("p8s3c", 20.7), ("p8s3d", 24.1), ("p8s3e", 26.5), ("p8s3f", 29.5), ("p8s3g", 31.4),
         ("p8s3h", 35.9), ("p8s3i", 39.4), ("p8s3j", 43.9), ("p8s3k", 48.0),
         ("p8s4a", 51.4), ("p8s4b", 56.2), ("p8s4c", 60.4), ("p8s4d", 62.5), ("p8s4e", 65.0), ("p8s4f", 68.8), ("p8s4g", 74.4),
         ("p8s4h", 78.0), ("p8s4i", 81.5),
         ("p8s5a", 85.1), ("p8s5b", 88.8), ("p8s5c", 91.4),
         ("p8s6a", 97.3), ("p8s6b", 101.0), ("p8s6c", 107.8), ("p8s6d", 112.2), ("p8s6e", 114.6), ("p8s6f", 117.8), ("p8s6g", 121.4),
         ("p8s6h", 124.6), ("p8s6i", 126.0), ("p8s6j", 131.0),
         ("p8s7a", 135.6), ("p8s7b", 140.1), ("p8s7c", 142.6), ("p8s7d", 146.0), ("p8s7e", 150.5)]
if __name__ == "__main__":
    build(8, TOTAL, music, sfx, LINES, f'{AUDIO}/part08.wav')
    print('done')
