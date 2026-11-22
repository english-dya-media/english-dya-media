"""Part 9 · Crossing the Arvand — timing, music and sound.
Scene starts: s1 0 (hook: "We don't need his boats!"; Fereydun rides into the river), s2 7.4 (title: Zahhak's black palace at dusk),
s3 12.0 (the crossing: Golrang, the army swimming, Kaveh with the banner, the far bank), s4 35.6 (Gang Dezhhukht higher than the clouds;
"full of dark magic"; through the gate; the talisman pulled down; Fereydun on the snake king's throne), s5 60.0 (Arnavaz and Shahrnaz set
free: "who are you?" — "the son of Abtin"; Zahhak has gone to India), s6 83.4 (Kondrow bows to the new king, is told to prepare a feast,
rides to Zahhak before dawn), s7 106.8 (Zahhak's tent in India: "a young man with an ox-headed mace sits on your throne!" — "What?!"),
end card 118.6, end 124.0"""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import series; series.from_folder(__file__)
from paths import AUDIO
from audio import *
from mix import build
from zsfx import *
from p07_audio import murmur
from p08_audio import rumble, gravel, water, shimmer

TOTAL = 124.0
S = {"s1": 0.0, "s2": 7.4, "s3": 12.0, "s4": 35.6, "s5": 60.0, "s6": 83.4, "s7": 106.8}
END_CARD = 118.6
PLUNGE = 4.6            # Golrang jumps into the river (part time)
FALL = 51.6             # the talisman starts to fall …
CRASH = 53.0            # … and hits the roof
WHAT = 115.2


def splash(amp=0.3, seed=0, dur=1.6):
    """a big splash: a burst of white noise that falls back as drops"""
    r = np.random.default_rng(seed)
    n = int(dur * SR); t = np.arange(n) / SR
    x = bandpass(r.standard_normal(n).astype(np.float32), 300, 6000) * np.exp(-t * 3.2) * np.minimum(1, t / 0.02)
    drops = (r.random(n) < 0.003).astype(np.float32) * r.uniform(0.2, 1.0, n).astype(np.float32)
    drops = bandpass(drops, 1500, 7000) * 6 * np.exp(-t * 1.5)
    return ((x + drops) * amp).astype(np.float32)


def swim(dur, amp=0.06, seed=0):
    """horses swimming: water pushed in slow waves"""
    x = noise_bed(dur, amp=amp, lo=250, hi=2200, lfo=0.9, seed=seed)
    n = len(x); t = np.arange(n) / SR
    return x * (0.6 + 0.4 * np.sin(2 * np.pi * 1.3 * t))[:, None]


def crack(amp=0.25, seed=0):
    r = np.random.default_rng(seed)
    n = int(0.4 * SR); t = np.arange(n) / SR
    x = highpass(r.standard_normal(n).astype(np.float32), 1800) * np.exp(-t * 18)
    return (x * amp).astype(np.float32)


def music(m):
    # S1 0-7.4: the river; the plunge
    place(m, drone(36.71, 7.6, amp=0.10, a=0.6, r=1.0), 0.0)
    place(m, pad([shur(0, -1), shur(4, -1), shur(0)], 4.6, amp=0.06, a=0.6, r=0.8, bright=5), 0.0)
    for i, t in enumerate(np.arange(2.0, PLUNGE, 0.3)):
        place(m, drum(dur=0.5, f0=60 if i % 2 else 52, amp=0.18 + 0.03 * i, noise=0.25), t)
    place(m, drum(dur=3.0, f0=40, amp=1.0, noise=0.45), PLUNGE)
    place(m, pad([shur(0), shur(4), shur(0, 1)], 3.0, amp=0.09, a=0.1, r=1.6, bright=6), PLUNGE)
    # S2 7.4-12.0: title over the black palace
    place(m, drum(dur=3.2, f0=40, amp=0.9, noise=0.4), 7.4)
    place(m, drone(36.71, 4.9, amp=0.12, a=0.1, r=1.4), 7.4)
    place(m, pad([shur(1, -1), shur(5, -1), shur(1)], 4.8, amp=0.08, a=0.4, r=1.6, bright=5), 7.4)
    tanbur(m, ZTHEME, 7.8, amp=0.22, low=True, step=0.85)
    # S3 12.0-35.6: the crossing
    place(m, pad([shur(0), shur(2), shur(4)], 6.4, amp=0.06, a=1.0, r=1.0, bright=5), 12.0)
    tanbur(m, [(0, 0), (2, 0.5), (4, 1.0), (5, 1.6), (4, 2.2)], 12.6, amp=0.10, step=1.0)
    place(m, drum(dur=1.6, f0=50, amp=0.5, noise=0.3), 15.8)
    place(m, drone(36.71, 17.4, amp=0.08, a=0.5, r=1.5), 18.4)                            # the river
    place(m, pad([shur(0), shur(4), shur(0, 1)], 17.0, amp=0.07, a=1.0, r=1.5, bright=6), 18.4)
    for i, t in enumerate(np.arange(18.6, 35.0, 0.6)):
        place(m, drum(dur=0.7, f0=58 if i % 2 else 50, amp=0.2 + (0.08 if i % 4 == 0 else 0), noise=0.2), t)
    tanbur(m, [(0, 0), (0, 0.5), (2, 1.0), (4, 1.5), (3, 2.0), (2, 2.5), (1, 3.0), (0, 3.5)], 19.0, amp=0.14, low=True, step=0.8)
    tanbur(m, [(0, 0), (2, 0.4), (4, 0.8), (5, 1.3), (4, 1.8), (5, 2.2), (7, 2.7), (4, 3.4)], 26.0, amp=0.14, low=True, step=0.8)
    place(m, drum(dur=3.0, f0=42, amp=0.85, noise=0.4), 32.0)                               # the far bank
    place(m, pad([shur(0), shur(4), shur(0, 1), shur(2, 1)], 3.6, amp=0.10, a=0.2, r=1.5, bright=7), 32.0)
    # S4 35.6-60.0: the palace; the gate; the talisman; the throne
    place(m, drone(36.71, 9.4, amp=0.10, a=1.0, r=1.0), 35.6)
    place(m, pad([shur(1, -1), shur(5, -1), shur(1)], 9.0, amp=0.06, a=1.0, r=1.0, bright=4), 35.6)
    heartbeat(m, 41.0, 44.6, bpm=76, amp=0.14)
    for i, t in enumerate(np.arange(45.0, 49.8, 0.4)):                                      # through the gate
        place(m, drum(dur=0.6, f0=62 if i % 2 else 52, amp=0.24 + 0.02 * i, noise=0.25), t)
    place(m, drone(55.0, 5.4, amp=0.07, a=0.5, r=0.5), 49.8)
    shimmer(m, 49.8, 1.8, amp=0.02, seed=91, base=440)
    place(m, drum(dur=3.0, f0=38, amp=1.0, noise=0.5), CRASH)
    place(m, pad([shur(0), shur(4), shur(0, 1)], 3.0, amp=0.09, a=0.1, r=1.5, bright=6), CRASH)
    place(m, pad([shur(0), shur(2), shur(4), shur(0, 1)], 4.8, amp=0.08, a=0.6, r=1.5, bright=6), 55.2)   # the throne
    tanbur(m, ZTHEME[:5], 55.6, amp=0.14, low=True, step=0.9)
    # S5 60.0-83.4: the sisters
    place(m, pad([shur(0), shur(2), shur(4)], 9.0, amp=0.05, a=1.5, r=1.5, bright=5), 60.0)
    tanbur(m, [(2, 0), (1, 0.8), (0, 1.6), (1, 2.6), (0, 3.4)], 60.6, amp=0.08, step=1.0)
    place(m, drum(dur=1.4, f0=52, amp=0.35, noise=0.25), 69.0)
    place(m, pad([shur(0), shur(4), shur(0, 1)], 7.4, amp=0.06, a=0.8, r=1.2, bright=6), 69.0)
    tanbur(m, [(0, 0), (2, 0.6), (4, 1.2), (5, 1.9)], 72.4, amp=0.09, step=1.0)
    place(m, bell(880, 2.4, 0.04), 76.6)
    place(m, drone(36.71, 4.4, amp=0.08, a=0.5, r=1.0), 79.4)
    place(m, pad([shur(1, -1), shur(5, -1)], 4.0, amp=0.05, a=0.6, r=1.0, bright=4), 79.4)
    # S6 83.4-106.8: Kondrow
    place(m, drone(36.71, 7.4, amp=0.08, a=1.0, r=1.0), 83.4)
    tanbur(m, [(0, 0), (1, 0.5), (0, 1.0), (3, 1.5), (2, 2.0), (1, 2.5), (0, 3.2)], 84.0, amp=0.10, step=0.9)
    place(m, pad([shur(0), shur(2), shur(4)], 7.0, amp=0.05, a=1.0, r=1.0, bright=5), 90.4)
    place(m, drone(36.71, 8.0, amp=0.09, a=0.8, r=1.0), 98.8)                               # the ride
    place(m, pad([shur(1, -1), shur(5, -1), shur(1)], 7.6, amp=0.06, a=0.8, r=1.0, bright=5), 98.8)
    for i, t in enumerate(np.arange(99.2, 106.6, 0.35)):
        place(m, drum(dur=0.5, f0=60 if i % 2 else 50, amp=0.18 + (0.06 if i % 4 == 0 else 0), noise=0.25), t)
    # S7 106.8-124.0: India: "What?!"
    place(m, drone(36.71, 8.4, amp=0.10, a=0.5, r=0.8), 106.8)
    place(m, pad([shur(1, -1), shur(5, -1), shur(1)], 8.0, amp=0.06, a=0.6, r=0.8, bright=4), 106.8)
    heartbeat(m, 108.0, 115.0, bpm=84, amp=0.16)
    place(m, drum(dur=3.0, f0=40, amp=1.0, noise=0.45), WHAT)
    place(m, pad([shur(1, -1), shur(5, -1), shur(1)], 3.4, amp=0.09, a=0.1, r=1.5, bright=6), WHAT)
    place(m, drum(dur=3.0, f0=40, amp=0.8, noise=0.4), END_CARD)
    place(m, drone(36.71, 5.4, amp=0.10, a=0.2, r=2.0), END_CARD)
    tanbur(m, ZTHEME[:4], END_CARD + 0.8, amp=0.12, low=True, step=0.9)


def sfx(s):
    # S1: the river; the horse; the plunge
    place(s, water(7.4, 0.05, seed=91), 0.0)
    place(s, snort(0.08, seed=91), 1.9, pan=-0.2)
    place(s, neigh(0.09, seed=91), 3.6, pan=-0.2)
    hooves(s, 3.6, PLUNGE, step=0.22, amp=0.08, pan=-0.1, seed=91, gallop=True)
    place(s, splash(0.32, seed=91), PLUNGE)
    place(s, swim(2.8, 0.06, seed=91), PLUNGE + 0.3)
    # S2: wind at the black palace
    place(s, gust(2.6, 0.07, seed=91), 7.6)
    place(s, crackle(4.6, amp=0.04, rate=8, seed=901), 7.4)
    # S3: the crossing
    place(s, water(23.6, 0.05, seed=92), 12.0)
    place(s, snort(0.07, seed=92), 13.0, pan=0.3)
    for k, t in enumerate((18.6, 19.2, 19.9, 20.8, 21.6)):
        place(s, splash(0.16, seed=92 + k, dur=1.2), t, pan=0.4 - 0.2 * k)
    place(s, swim(16.4, 0.08, seed=93), 19.0)
    place(s, neigh(0.06, seed=92), 23.0, pan=0.4)
    place(s, gust(2.0, 0.06, seed=92), 26.0)
    place(s, murmur(4.0, 0.03, seed=91), 30.0)
    hooves(s, 32.2, 35.4, step=0.4, amp=0.06, pan=-0.2, seed=92)
    # S4: the palace; the gate; the talisman; the hall
    place(s, gust(3.0, 0.06, seed=93), 35.8)
    place(s, crackle(9.4, amp=0.04, rate=8, seed=902), 40.4)
    hooves(s, 45.0, 49.6, step=0.24, amp=0.08, pan=0.1, seed=93, gallop=True)
    place(s, murmur(3.0, 0.05, seed=92), 46.0)
    place(s, creak(1.2, 0.08, seed=91), 45.6, pan=-0.3)
    for k, t in enumerate((FALL - 0.8, FALL - 0.4, FALL)):
        place(s, crack(0.18 + 0.05 * k, seed=91 + k), t, pan=0.1)
    place(s, rumble(CRASH - FALL, 0.16, seed=91), FALL)
    place(s, thud(0.45, f0=48, seed=91), CRASH)
    place(s, gravel(2.4, 0.1, seed=91), CRASH + 0.1)
    place(s, crackle(4.8, amp=0.06, rate=8, seed=903), 55.2)
    # S5: the hall
    place(s, crackle(23.4, amp=0.05, rate=8, seed=904), 60.0)
    steps(s, 60.4, 63.6, step=0.45, amp=0.03, seed=91, pan=-0.3)
    # S6: Kondrow; the ride before dawn
    place(s, crackle(15.4, amp=0.05, rate=8, seed=905), 83.4)
    steps(s, 83.6, 86.4, step=0.32, amp=0.045, seed=92, pan=-0.4)
    place(s, rustle(0.05, 0.8, seed=91), 90.4)
    steps(s, 97.2, 98.6, step=0.3, amp=0.04, seed=93, pan=0.4)
    crickets(s, 98.8, 106.8, amp=0.008, seed=91)
    hooves(s, 99.2, 106.6, step=0.21, amp=0.08, pan=0.2, seed=94, gallop=True)
    place(s, owl(0.04), 100.6, pan=-0.5)
    # S7: the tent at night; the snakes
    crickets(s, 106.8, 124.0, amp=0.008, seed=92)
    place(s, crackle(17.2, amp=0.05, rate=8, seed=906), 106.8)
    steps(s, 106.9, 107.5, step=0.15, amp=0.05, seed=94, pan=-0.3)
    place(s, hiss(1.2, 0.07, seed=91), 111.6, pan=-0.3); place(s, hiss(1.2, 0.07, seed=92), 112.4, pan=0.3)
    place(s, hiss(1.4, 0.12, seed=93), WHAT + 0.1, pan=-0.3); place(s, hiss(1.4, 0.12, seed=94), WHAT + 0.2, pan=0.3)


LINES = [("p9s1a", 0.4), ("p9s1b", 3.8),
         ("p9s3a", 12.3), ("p9s3b", 15.8), ("p9s3c", 18.8), ("p9s3d", 26.0), ("p9s3e", 29.2),
         ("p9s4a", 35.9), ("p9s4b", 40.6), ("p9s4c", 45.2), ("p9s4d", 50.2), ("p9s4e", 55.6),
         ("p9s5a", 60.3), ("p9s5b", 65.0), ("p9s5c", 69.2), ("p9s5d", 72.4), ("p9s5e", 76.6), ("p9s5f", 79.6),
         ("p9s6a", 83.7), ("p9s6b", 90.6), ("p9s6c", 93.0), ("p9s6d", 96.8), ("p9s6e", 99.4),
         ("p9s7a", 107.6), ("p9s7b", WHAT)]
if __name__ == "__main__":
    build(9, TOTAL, music, sfx, LINES, f'{AUDIO}/part09.wav')
    print('done')
