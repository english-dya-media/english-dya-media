"""Part 7 · Kaveh the Blacksmith — timing, music and sound.
Scene starts: s1 0 (hook: Kaveh tears the paper in the hall; Zahhak's face as the pieces fall), s2 7.6 (title: the market at dawn, Kaveh's
forge), s3 12.2 (the meadow at dawn: Faranak tells Fereydun about Abtin, the cow and the burned house; he wants to fight; she asks him to
wait), s4 48.4 (Zahhak can't sleep: "Fereydun…"; the great men in his hall; the paper "I am a just king"; they all sign), s5 72.0 (Kaveh at
the door; eighteen sons; the son given back; "sign my paper"; he reads it, shames the nobles, tears it and walks out; "a mountain of iron"),
s6 129.4 (the market: the crowd; the apron on the spear: "Who wants to be free? Follow me!"), end card 143.6, end 148.6"""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import series; series.from_folder(__file__)
from paths import AUDIO
from audio import *
from mix import build
from zsfx import *
TOTAL = 148.6
S = {"s1": 0.0, "s2": 7.6, "s3": 12.2, "s4": 48.4, "s5": 72.0, "s6": 129.4}
END_CARD = 143.6
RIP1 = 2.5            # the paper tears in the hook (scene time)
RIP2 = 114.4 + 1.6    # … and in the hall
BANG = (72.25, 72.75, 73.25)   # fists on the hall door

FORGE = [(0, 0), (2, 0.4), (3, 0.8), (4, 1.3), (3, 1.9), (2, 2.3), (1, 2.7), (0, 3.4)]
RISE = [(0, 0), (2, 0.5), (4, 1.0), (5, 1.5), (4, 2.0), (5, 2.4), (6, 2.9), (7, 3.6)]


def anvil(amp=0.12, seed=0):
    """a hammer on the anvil: a bright metal ring with a hard click"""
    r = np.random.default_rng(seed)
    n = int(1.4 * SR); t = np.arange(n) / SR
    f0 = 1180 * (1 + 0.02 * r.standard_normal())
    x = sum(a * np.sin(2 * np.pi * f0 * k * t) * np.exp(-t * d) for k, a, d in ((1, 1.0, 5), (2.76, 0.5, 8), (5.4, 0.3, 12), (8.9, 0.15, 18)))
    click = highpass(r.standard_normal(n).astype(np.float32), 2500) * np.exp(-t * 90)
    return ((x * 0.6 + click * 0.8) * amp).astype(np.float32)


def rip(dur=0.55, amp=0.16, seed=0):
    """paper tearing: a dry crackle that rises and stops"""
    r = np.random.default_rng(seed)
    n = int(dur * SR); t = np.arange(n) / SR
    x = bandpass(r.standard_normal(n).astype(np.float32), 900, 6000)
    grit = (r.random(n) < 0.02).astype(np.float32) * r.uniform(0.5, 1.5, n).astype(np.float32)
    grit = bandpass(grit, 1500, 7000) * 6
    e = np.minimum(1, t / 0.05) * np.minimum(1, (dur - t) / 0.04) * (0.6 + 0.4 * t / dur)
    return ((x * 0.7 + grit) * e * amp * 2).astype(np.float32)


def flutter(dur=1.6, amp=0.04, seed=0):
    """scraps of paper falling"""
    r = np.random.default_rng(seed)
    n = int(dur * SR); t = np.arange(n) / SR
    x = bandpass(r.standard_normal(n).astype(np.float32), 1500, 5000) * (0.5 + 0.5 * np.sin(2 * np.pi * 13 * t + 3 * np.sin(2 * np.pi * 2 * t)))
    return (x * np.sin(np.pi * t / dur) * amp * 2).astype(np.float32)


def door_bang(amp=0.35, seed=0):
    return thud(amp, f0=58, seed=seed) + thud(amp * 0.4, f0=110, seed=seed + 1)


def murmur(dur, amp=0.05, seed=0):
    """a crowd talking low"""
    return noise_bed(dur, amp=amp, lo=250, hi=900, lfo=1.8, seed=seed)


def cheer(dur, amp=0.12, seed=0):
    x = noise_bed(dur, amp=amp, lo=350, hi=2600, lfo=2.2, seed=seed)
    n = len(x)
    return x * env(n, 0.5, 1.2)[:, None]


def gasp(amp=0.05, seed=0):
    r = np.random.default_rng(seed)
    n = int(0.6 * SR); t = np.arange(n) / SR
    x = bandpass(r.standard_normal(n).astype(np.float32), 500, 3000) * np.minimum(1, t / 0.08) * np.exp(-t * 4)
    return (x * amp * 3).astype(np.float32)


def music(m):
    # S1 0-7.6: the paper torn; the snake king's face
    place(m, drone(36.71, 7.8, amp=0.11, a=0.8, r=1.0), 0.0)
    place(m, pad([shur(1, -1), shur(5, -1), shur(1)], 2.6, amp=0.06, a=0.6, r=0.6, bright=5), 0.0)
    place(m, drum(dur=2.4, f0=44, amp=0.8, noise=0.4), RIP1)
    place(m, pad([shur(0, -1), shur(4, -1), shur(0)], 4.4, amp=0.07, a=0.2, r=1.2, bright=6), RIP1)
    heartbeat(m, 4.2, 7.2, bpm=80, amp=0.16)
    # S2 7.6-12.2: title over the market at dawn
    place(m, drum(dur=3.2, f0=40, amp=0.9, noise=0.4), 7.6)
    place(m, drone(36.71, 4.9, amp=0.12, a=0.1, r=1.4), 7.6)
    place(m, pad([shur(0), shur(4), shur(0, 1)], 4.8, amp=0.10, a=0.4, r=1.6, bright=6), 7.6)
    tanbur(m, ZTHEME, 8.0, amp=0.22, low=True, step=0.85)
    # S3 12.2-48.4: the meadow at dawn; Faranak's story; the memories; the anger; the patience
    place(m, pad([shur(0), shur(2), shur(4)], 12.6, amp=0.06, a=2.0, r=1.5, bright=5), 12.2)
    tanbur(m, [(0, 0), (2, 0.6), (4, 1.2), (3, 1.9), (2, 2.5), (0, 3.2)], 12.8, amp=0.09, step=1.0)
    tanbur(m, [(2, 0), (1, 0.7), (0, 1.4)], 19.0, amp=0.07, step=1.1)
    place(m, drone(55.0, 9.0, amp=0.07, a=1.0, r=1.2), 25.0)                    # the memories
    place(m, pad([shur(1, -1), shur(0, -1), shur(4, -1)], 8.6, amp=0.05, a=1.0, r=1.2, bright=4), 25.0)
    tanbur(m, [(2, 0), (1, 1.0), (0, 2.0)], 26.0, amp=0.07, step=1.1)
    place(m, drum(dur=1.6, f0=50, amp=0.4, noise=0.3), 29.4)
    place(m, drum(dur=1.4, f0=60, amp=0.45, noise=0.25), 33.6)                 # Fereydun stands up
    place(m, drum(dur=1.0, f0=70, amp=0.3, noise=0.2), 34.4)
    place(m, pad([shur(0), shur(4), shur(0, 1)], 4.0, amp=0.07, a=0.3, r=1.0, bright=6), 33.6)
    place(m, pad([shur(0), shur(2), shur(4)], 10.6, amp=0.06, a=1.5, r=2.0, bright=5), 37.8)
    tanbur(m, [(0, 0), (2, 0.7), (4, 1.4), (5, 2.1), (4, 2.8), (2, 3.5)], 41.4, amp=0.09, step=1.0)
    place(m, bell(587, 2.6, 0.03), 45.6)
    # S4 48.4-72.0: the sleepless king; the great men; the paper
    place(m, drone(36.71, 6.8, amp=0.10, a=0.6, r=0.8), 48.4)
    place(m, pad([shur(1, -1), shur(5, -1)], 6.6, amp=0.05, a=1.0, r=0.8, bright=4), 48.4)
    heartbeat(m, 52.0, 54.8, bpm=76, amp=0.16)
    place(m, drone(36.71, 16.8, amp=0.09, a=1.0, r=1.0), 55.0)
    for t in np.arange(55.2, 61.2, 1.0):                                        # the procession
        place(m, drum(dur=0.8, f0=56, amp=0.18, noise=0.15), t)
    tanbur(m, [(0, 0), (1, 0.5), (0, 1.0), (3, 1.5), (2, 2.0), (1, 2.5), (0, 3.2)], 55.8, amp=0.10, step=0.9)
    place(m, drum(dur=1.8, f0=46, amp=0.55, noise=0.3), 61.4)
    place(m, pad([shur(1, -1), shur(5, -1), shur(1)], 5.0, amp=0.06, a=0.3, r=1.0, bright=5), 61.4)
    for k, t in enumerate((67.6, 68.9, 70.2)):                                  # one by one
        place(m, pluck_fast(shur(k), 1.6, amp=0.12), t, pan=0.2)
    place(m, drone(55.0, 5.0, amp=0.06, a=0.6, r=1.0), 67.0)
    # S5 72.0-129.4: Kaveh
    place(m, drum(dur=2.0, f0=44, amp=0.6, noise=0.35), 72.0)
    place(m, drone(36.71, 12.0, amp=0.10, a=0.3, r=1.0), 75.0)
    for i, t in enumerate(np.arange(78.6, 84.0, 0.6)):                          # Kaveh's march into the hall
        place(m, drum(dur=0.7, f0=58 if i % 2 else 50, amp=0.22 + (0.08 if i % 4 == 0 else 0), noise=0.2), t)
    place(m, pad([shur(0, -1), shur(4, -1), shur(0)], 13.0, amp=0.06, a=1.0, r=1.0, bright=5), 84.0)
    tanbur(m, FORGE, 88.0, amp=0.10, step=1.0, low=True)
    place(m, drum(dur=1.6, f0=48, amp=0.5, noise=0.3), 92.0)
    place(m, pad([shur(0), shur(2), shur(4)], 4.6, amp=0.06, a=0.8, r=1.5, bright=5), 99.4)   # the son
    tanbur(m, [(4, 0), (2, 0.5), (0, 1.2)], 101.8, amp=0.12, step=1.0)
    place(m, drone(36.71, 7.0, amp=0.09, a=0.5, r=0.8), 104.0)
    place(m, pad([shur(1, -1), shur(5, -1)], 6.0, amp=0.05, a=0.8, r=0.8, bright=4), 104.0)
    place(m, drum(dur=1.4, f0=54, amp=0.4, noise=0.25), 110.0)
    for i, t in enumerate(np.arange(110.2, 114.4, 0.5)):
        place(m, drum(dur=0.6, f0=60, amp=0.16 + 0.02 * i, noise=0.2), t)
    place(m, drum(dur=3.0, f0=40, amp=1.0, noise=0.45), RIP2)                  # the paper is torn
    place(m, pad([shur(0), shur(4), shur(0, 1)], 5.4, amp=0.10, a=0.1, r=2.0, bright=6), RIP2)
    tanbur(m, FORGE, RIP2 + 0.6, amp=0.16, low=True, step=0.8)
    place(m, drone(36.71, 7.6, amp=0.09, a=1.0, r=1.5), 121.8)
    place(m, pad([shur(1, -1), shur(0, -1)], 7.4, amp=0.05, a=1.0, r=1.5, bright=4), 121.8)
    place(m, bell(440, 2.6, 0.03), 127.8)
    # S6 129.4-148.6: the market; the banner
    place(m, pad([shur(0), shur(4), shur(0, 1)], 9.2, amp=0.06, a=1.5, r=1.0, bright=6), 129.4)
    for t in np.arange(129.8, 138.6, 0.8):
        place(m, drum(dur=0.8, f0=62, amp=0.14, noise=0.15), t)
    tanbur(m, ZTHEME, 130.2, amp=0.12, step=1.0)
    for i, t in enumerate(np.arange(136.2, 138.6, 0.3)):                         # building up
        place(m, drum(dur=0.5, f0=66 if i % 2 else 56, amp=0.2 + 0.03 * i, noise=0.25), t)
    place(m, drum(dur=3.0, f0=42, amp=0.95, noise=0.4), 138.6)                 # the banner rises
    place(m, pad([shur(0), shur(4), shur(0, 1), shur(2, 1)], 10.0, amp=0.11, a=0.3, r=2.5, bright=7), 138.6)
    tanbur(m, RISE, 139.0, amp=0.20, low=True, step=0.7)
    for i, t in enumerate(np.arange(142.0, END_CARD, 0.4)):
        place(m, drum(dur=0.6, f0=60 if i % 2 else 50, amp=0.3, noise=0.25), t)
    place(m, drum(dur=3.0, f0=40, amp=0.8, noise=0.4), END_CARD)
    place(m, drone(36.71, 5.0, amp=0.10, a=0.2, r=2.0), END_CARD)
    place(m, pad([shur(0), shur(4), shur(0, 1)], 5.0, amp=0.08, a=0.6, r=2.0, bright=5), END_CARD)
    tanbur(m, ZTHEME[:4], END_CARD + 0.6, amp=0.14, low=True, step=0.9)


def sfx(s):
    # S1: torches; the tear; the scraps; the snakes
    place(s, crackle(7.6, amp=0.05, rate=8, seed=701), 0.0)
    place(s, rip(0.55, 0.2, seed=71), RIP1 - 0.1, pan=0.1)
    place(s, flutter(2.4, 0.05, seed=71), RIP1 + 0.4)
    place(s, hiss(1.2, 0.08, seed=71), 4.6, pan=-0.3); place(s, hiss(1.2, 0.08, seed=72), 5.4, pan=0.3)
    # S2: the forge at dawn: a few hammer blows far away
    for k, t in enumerate((8.3, 8.9, 9.5, 10.6, 11.2)):
        place(s, anvil(0.05, seed=70 + k), t, pan=-0.4)
    place(s, crackle(4.6, amp=0.05, rate=10, seed=702), 7.6)
    # S3: birds and wind in the meadow; the road; the fire
    for k, t in enumerate((12.6, 13.5, 15.2, 18.8, 22.4, 38.6, 42.0, 46.0)):
        place(s, chirp(2900 + 300 * (k % 3), amp=0.035), t, pan=0.4 - 0.2 * (k % 4))
    place(s, noise_bed(12.8, amp=0.03, lo=300, hi=2600, lfo=0.2, seed=703), 12.2)
    steps(s, 25.2, 29.2, step=0.5, amp=0.035, seed=71)
    place(s, noise_bed(4.2, amp=0.12, lo=80, hi=900, lfo=2.4, seed=704), 29.4)       # the fire
    place(s, crackle(4.2, amp=0.16, rate=20, seed=705), 29.4)
    place(s, noise_bed(14.8, amp=0.03, lo=300, hi=2600, lfo=0.2, seed=706), 33.6)
    place(s, rustle(0.05, 0.8, seed=71), 33.7)
    # S4: night in the bedchamber; the hall; the procession; the pens
    crickets(s, 48.4, 55.0, amp=0.008, seed=71)
    place(s, hiss(1.0, 0.05, seed=73), 50.4, pan=-0.2); place(s, hiss(1.0, 0.05, seed=74), 53.6, pan=0.2)
    place(s, crackle(17.0, amp=0.04, rate=8, seed=707), 55.0)
    steps(s, 55.2, 60.0, step=0.38, amp=0.04, seed=72)
    place(s, murmur(5.0, 0.03, seed=71), 55.4)
    for k, t in enumerate((67.6, 68.9, 70.2)):
        place(s, scrape(0.5, 0.04, seed=71 + k), t, pan=0.1)
    # S5: the door; the march; the son; the tear; the scraps; the gasp
    for k, t in enumerate(BANG):
        place(s, door_bang(0.32, seed=71 + k), t, pan=-0.5)
    place(s, murmur(3.0, 0.04, seed=72), 72.6)
    place(s, crackle(57.0, amp=0.035, rate=8, seed=708), 72.0)
    steps(s, 78.8, 81.5, step=0.42, amp=0.06, seed=73, pan=-0.2)
    steps(s, 99.6, 101.4, step=0.24, amp=0.05, seed=74, pan=0.3)                    # the son runs
    place(s, rip(0.6, 0.22, seed=72), RIP2 - 0.1)
    place(s, flutter(2.6, 0.06, seed=72), RIP2 + 0.5)
    place(s, gasp(0.06, seed=71), RIP2 + 0.2, pan=-0.3); place(s, gasp(0.05, seed=72), RIP2 + 0.35, pan=0.3)
    steps(s, 117.9, 121.6, step=0.46, amp=0.05, seed=75, pan=-0.3)
    place(s, murmur(4.0, 0.035, seed=73), 118.0)
    place(s, hiss(1.2, 0.07, seed=75), 125.0, pan=-0.3); place(s, hiss(1.2, 0.07, seed=76), 126.4, pan=0.3)
    # S6: the market; the crowd; the cheer
    place(s, murmur(12.6, 0.05, seed=74), 129.4)
    for k, t in enumerate((130.0, 131.6, 133.6)):
        place(s, anvil(0.03, seed=80 + k), t, pan=-0.5)
    place(s, rustle(0.05, 0.8, seed=72), 134.6)
    place(s, rustle(0.05, 0.8, seed=73), 136.6)
    place(s, gust(2.0, 0.08, seed=71), 138.6)
    place(s, cheer(5.6, 0.12, seed=71), 141.6)
    place(s, cheer(5.0, 0.08, seed=72), 143.2, pan=0.3)
    place(s, noise_bed(5.0, amp=0.03, lo=200, hi=1500, lfo=0.2, seed=709), END_CARD)


LINES = [("p7s1a", 0.4), ("p7s1b", 4.3),
         ("p7s3a", 12.6), ("p7s3b", 17.6), ("p7s3c", 21.6), ("p7s3d", 25.3), ("p7s3e", 29.6), ("p7s3f", 33.8), ("p7s3g", 37.9), ("p7s3h", 41.4),
         ("p7s3i", 45.0),
         ("p7s4a", 48.7), ("p7s4b", 52.3), ("p7s4c", 55.6), ("p7s4d", 61.6), ("p7s4e", 64.3), ("p7s4f", 67.1),
         ("p7s5a", 72.6), ("p7s5b", 75.1), ("p7s5c", 81.9), ("p7s5d", 84.2), ("p7s5e", 88.3), ("p7s5f", 92.0), ("p7s5g", 96.3), ("p7s5h", 101.8),
         ("p7s5i", 104.1), ("p7s5j", 108.3), ("p7s5k", 110.2), ("p7s5l", 114.5), ("p7s5m", 121.9), ("p7s5n", 124.6),
         ("p7s6a", 129.8), ("p7s6b", 134.2), ("p7s6c", 139.2)]
if __name__ == "__main__":
    build(7, TOTAL, music, sfx, LINES, f'{AUDIO}/part07.wav')
    print('done')
