"""Part 7 · The Betrayal — timing, music and sound.
Scene starts: s1 0 (hook: Sahl's castle at night), s2 14.0 (title), s3 18.6 (the hunt, 15 September 837), s4 53.6 (the road to Samarra),
s5 84.2 (the elephant), end card 107.6, end 112.2"""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import series; series.from_folder(__file__)
from paths import AUDIO
from audio import *
from mix import build
from p02_audio import chirp, snort, clash, tanbur, whoosh, THEME
from p03_audio import thud, hooves, steps, rumble, cheer, scrape, swish
from p04_audio import neigh, daf
from p05_audio import heartbeat, breath, horn
from p06_audio import creak
TOTAL = 112.2
S = {"s1": 0.0, "s2": 14.0, "s3": 18.6, "s4": 53.6, "s5": 84.2}
END_CARD = 107.6


def bark(amp=0.12, seed=0):
    """a hunting dog's bark: two quick formant bursts with a falling pitch"""
    r = np.random.default_rng(seed)
    out = np.zeros(int(0.42 * SR), np.float32)
    for k, (t0, d) in enumerate(((0.0, 0.16), (0.2, 0.12))):
        n = int(d * SR); t = np.arange(n) / SR
        f = (420 + 80 * r.random()) * (1.25 - 0.45 * t / d)
        x = np.sin(2 * np.pi * np.cumsum(f) / SR) + 0.6 * np.sin(4 * np.pi * np.cumsum(f) / SR) + 0.5 * r.standard_normal(n)
        x = bandpass(x.astype(np.float32), 300, 2600) * np.minimum(1, t / 0.01) * np.exp(-t * 14)
        i = int(t0 * SR); out[i:i + n] += x * (1.0 if k == 0 else 0.7)
    return (out / (np.abs(out).max() + 1e-6) * amp).astype(np.float32)


def falcon_cry(amp=0.06):
    """a falcon's high 'kee-ee'"""
    n = int(0.55 * SR); t = np.arange(n) / SR
    f = 2700 - 700 * t / 0.55 + 90 * np.sin(2 * np.pi * 26 * t)
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) + 0.3 * np.sin(4 * np.pi * np.cumsum(f) / SR)
    return (x * env(n, 0.03, 0.2) * amp).astype(np.float32)


def wings(m, t0, n=4, rate=0.16, amp=0.05, seed=0):
    r = np.random.default_rng(seed)
    for k in range(n):
        k_ = int(0.12 * SR); tt = np.arange(k_) / SR
        x = bandpass(r.standard_normal(k_).astype(np.float32), 300, 1800) * np.sin(np.pi * tt / 0.12) ** 2
        place(m, (x * amp * (1 - 0.15 * k)).astype(np.float32), t0 + k * rate, pan=0.2)


def chains(m, t0, t1, step=0.55, amp=0.03, seed=0, pan=0.0):
    """iron chains clinking with each step of a horse"""
    r = np.random.default_rng(seed)
    t = t0
    while t < t1:
        for j in range(r.integers(2, 4)):
            place(m, bell(1700 + 1500 * r.random(), 0.35, amp * r.uniform(0.5, 1.0)), t + 0.03 * j + r.uniform(0, 0.02), pan=pan + r.uniform(-0.15, 0.15))
        t += step * r.uniform(0.85, 1.15)


def trumpet(amp=0.16, dur=1.5, seed=0):
    """an elephant's trumpet: a rough brassy call that rises and falls"""
    r = np.random.default_rng(seed)
    n = int(dur * SR); t = np.arange(n) / SR
    f = 430 + 260 * np.sin(np.pi * np.minimum(1, t / (dur * 0.8))) + 25 * np.sin(2 * np.pi * 7 * t)
    ph = 2 * np.pi * np.cumsum(f) / SR
    x = sum(w * np.sin(k * ph) for k, w in ((1, 1.0), (2, 0.7), (3, 0.5), (4, 0.35), (5, 0.2)))
    x = x * (1 + 0.35 * r.standard_normal(n) * 0.3)
    return (bandpass(x.astype(np.float32), 300, 4200) * env(n, 0.08, 0.4) * amp).astype(np.float32)


def rustle(amp=0.04, dur=0.7, seed=0):
    """silk and cloth being moved"""
    r = np.random.default_rng(seed)
    n = int(dur * SR); t = np.arange(n) / SR
    x = bandpass(r.standard_normal(n).astype(np.float32), 1500, 6000) * (0.5 + 0.5 * np.sin(2 * np.pi * 5 * t)) * env(n, 0.1, 0.3)
    return (x * amp * 2).astype(np.float32)


def music(m):
    # S1 0-14: the hook, Sahl's castle at night
    place(m, drone(36.71, 14.0, amp=0.10, a=1.5, r=1.5), 0.0)
    place(m, pad([shur(1, -1), shur(3, -1), shur(5, -1)], 5.8, amp=0.06, a=0.8, r=1.5, bright=4), 0.2)
    tanbur(m, [(0, 0), (1, 0.9), (0, 1.8)], 1.0, amp=0.10)
    place(m, drum(dur=2.4, f0=42, amp=0.55, noise=0.25), 3.9)
    place(m, pad([shur(0), shur(4)], 2.6, amp=0.04, a=0.6, r=1.2, bright=3), 5.6)
    place(m, bell(220, 2.5, 0.04), 5.9)
    tanbur(m, [(4, 0), (3, 0.6), (1, 1.2), (0, 2.0)], 8.4, amp=0.10)
    for i, t in enumerate(np.arange(12.0, 13.9, 0.3)):
        place(m, drum(dur=0.6, f0=58 if i % 2 else 48, amp=0.22 + 0.03 * i, noise=0.3), t)
    # S2 14-18.6: title
    place(m, drum(dur=3.0, f0=40, amp=1.0, noise=0.45), 14.0)
    tanbur(m, THEME[:6], 14.3, amp=0.22, low=True, step=0.8)
    place(m, drone(73.42, 4.6, amp=0.09, a=0.05, r=2.0), 14.0)
    # S3 18.6-53.6: the hunt
    place(m, pad([shur(0), shur(2), shur(4)], 14.2, amp=0.06, a=2.0, r=1.5, bright=5), 18.8)
    daf(m, 19.0, 29.0, bpm=96, amp=0.09)
    tanbur(m, THEME, 19.4, amp=0.12, step=0.9)
    tanbur(m, [(4, 0), (5, 0.4), (4, 0.8), (2, 1.2), (0, 2.0)], 25.2, amp=0.11)
    tanbur(m, [(0, 0), (2, 0.15), (4, 0.3), (7, 0.45)], 29.8, amp=0.13)
    place(m, drone(36.71, 21.0, amp=0.10, a=0.4, r=2.5), 32.6)
    place(m, pad([shur(1, -1), shur(3, -1), shur(5, -1)], 8.6, amp=0.07, a=0.6, r=1.5, bright=4), 33.0)
    for i, t in enumerate(np.arange(34.0, 38.6, 0.6)):
        place(m, drum(dur=0.9, f0=55, amp=0.20 + 0.01 * i, noise=0.2), t)
    for i, t in enumerate(np.arange(38.6, 41.5, 0.32)):
        place(m, drum(dur=0.6, f0=60 if i % 2 else 48, amp=0.28 + 0.01 * i, noise=0.3), t)
    place(m, drum(dur=2.0, f0=42, amp=0.6, noise=0.3), 41.6)
    place(m, pad([shur(0, -1), shur(1, -1)], 4.8, amp=0.05, a=0.8, r=1.0, bright=3), 41.7)
    heartbeat(m, 42.0, 46.0, bpm=66, amp=0.2)
    place(m, pad([shur(1, -1), shur(3, -1), shur(5, -1)], 3.0, amp=0.05, a=0.5, r=1.0, bright=3), 46.3)
    place(m, drum(dur=2.6, f0=40, amp=0.85, noise=0.4), 49.4)
    place(m, pad([shur(1, -1), shur(3, -1)], 4.2, amp=0.07, a=0.1, r=2.0, bright=4), 49.4)
    tanbur(m, [(4, 0), (3, 0.9), (1, 1.8), (0, 2.8)], 50.6, amp=0.10)
    # S4 53.6-84.2: the winter road; Samarra
    place(m, pad([shur(0, -1), shur(4, -1), shur(0)], 8.2, amp=0.05, a=2.0, r=1.5, bright=3), 53.8)
    tanbur(m, [(0, 0), (2, 0.8), (3, 1.6), (2, 2.4), (0, 3.4)], 54.0, amp=0.10)
    tanbur(m, [(4, 0), (3, 0.8), (2, 1.6), (1, 2.4), (0, 3.2)], 58.6, amp=0.10)
    place(m, pad([shur(0), shur(4), shur(0, 1)], 8.8, amp=0.07, a=1.0, r=1.5, bright=5), 61.9)
    daf(m, 61.8, 70.6, bpm=100, amp=0.15)
    place(m, horn(2.6, 0.09, 98.0), 62.0)
    tanbur(m, THEME, 62.4, amp=0.12, step=0.7)
    place(m, horn(2.2, 0.08, 110.0), 66.9)
    place(m, drone(36.71, 11.2, amp=0.08, a=1.0, r=1.5), 70.6)
    place(m, pad([shur(0, -1), shur(2, -1), shur(4, -1)], 11.0, amp=0.05, a=1.5, r=1.5, bright=3), 70.8)
    tanbur(m, [(0, 0)], 71.2, amp=0.10)
    tanbur(m, [(1, 0), (0, 0.8)], 76.6, amp=0.10)
    place(m, drum(dur=2.4, f0=42, amp=0.6, noise=0.3), 81.3)
    place(m, bell(220, 3.0, 0.05), 81.8)
    place(m, pad([shur(1, -1), shur(3, -1)], 2.6, amp=0.05, a=0.4, r=1.5, bright=3), 81.7)
    # S5 84.2-112.2: three days later; the elephant; the gates
    place(m, pad([shur(0), shur(2), shur(4)], 4.6, amp=0.05, a=1.0, r=1.0, bright=4), 84.3)
    tanbur(m, [(4, 0), (3, 0.9), (2, 1.8)], 84.8, amp=0.08)
    place(m, drone(36.71, 7.6, amp=0.08, a=1.0, r=1.0), 88.8)
    heartbeat(m, 89.0, 93.0, bpm=66, amp=0.18)
    place(m, drum(dur=2.4, f0=42, amp=0.55, noise=0.3), 93.2)
    place(m, pad([shur(0, -1), shur(4, -1)], 3.2, amp=0.05, a=0.5, r=1.0, bright=3), 93.3)
    for i, t in enumerate(np.concatenate([np.arange(96.6, 99.6, 0.5), np.arange(99.6, 102.0, 0.3)])):
        place(m, drum(dur=0.7, f0=56 if i % 2 else 46, amp=0.18 + 0.012 * i, noise=0.25), t)
    place(m, pad([shur(0), shur(4), shur(0, 1)], 5.6, amp=0.08, a=2.0, r=1.0, bright=5), 96.5)
    place(m, drum(dur=3.0, f0=40, amp=1.0, noise=0.5), 103.0)
    daf(m, 103.0, 107.6, bpm=120, amp=0.18)
    tanbur(m, THEME, 103.2, amp=0.2, low=True, step=0.7)
    place(m, pad([shur(0), shur(4), shur(0, 1)], 4.6, amp=0.08, a=0.4, r=1.0, bright=6), 103.0)
    place(m, drum(dur=2.5, f0=46, amp=0.85, noise=0.4), END_CARD - 0.1)
    tanbur(m, THEME, END_CARD + 0.1, amp=0.18, low=True, step=0.8)
    place(m, pad([shur(0), shur(4), shur(0, 1)], 4.6, amp=0.07, a=1.0, r=2.0, bright=5), END_CARD)


def sfx(s):
    # hook: the lamp, the letter, the sleeping guest, the gate, the rider
    place(s, noise_bed(14.0, amp=0.03, lo=200, hi=1400, lfo=0.2, seed=701), 0.0)
    place(s, crackle(8.0, amp=0.05, rate=6, seed=702), 0.0)
    place(s, scrape(0.5, amp=0.05, seed=703), 0.3)
    place(s, scrape(0.4, amp=0.04, seed=704), 5.0)
    breath(s, 5.7, 8.0, rate=0.35, amp=0.03, seed=705)
    place(s, crackle(4.0, amp=0.08, seed=706), 8.0)
    place(s, snort(seed=11, amp=0.06), 8.6, pan=0.4)
    place(s, scrape(0.3, amp=0.04, seed=707), 10.9)
    place(s, neigh(0.06, seed=3), 12.05, pan=0.3)
    hooves(s, 12.1, 14.2, step=0.24, amp=0.08, pan=0.5, seed=708)
    place(s, whoosh(1.6, amp=0.10, seed=709), 12.6)
    # the hunt: morning, birds, horses walking, dogs, the falcon
    place(s, noise_bed(14.0, amp=0.03, lo=300, hi=2500, lfo=0.15, seed=710), 18.6)
    for k, t in enumerate((18.9, 19.6, 21.3, 22.4, 24.6, 27.8, 31.0)):
        place(s, chirp(2900 + 300 * (k % 3), amp=0.04), t, pan=0.5 - 0.25 * (k % 4))
    hooves(s, 18.6, 32.6, step=0.42, amp=0.045, pan=-0.1, seed=711)
    hooves(s, 18.8, 32.6, step=0.44, amp=0.035, pan=0.2, seed=712)
    for k, t in enumerate((20.4, 21.1, 27.2, 30.4, 30.9)):
        place(s, bark(0.08, seed=713 + k), t, pan=0.3 - 0.2 * (k % 3))
    wings(s, 29.9, n=5, rate=0.15, amp=0.06, seed=718)
    place(s, falcon_cry(0.05), 30.4, pan=0.3)
    place(s, falcon_cry(0.035), 31.8, pan=0.5)
    # the trap
    place(s, horn(2.6, 0.15, 98.0), 32.8, pan=-0.3)
    place(s, horn(2.2, 0.11, 110.0), 35.0, pan=0.4)
    for k, t in enumerate((33.5, 34.1)):
        place(s, bark(0.09, seed=720 + k), t, pan=0.2)
    place(s, noise_bed(9.0, amp=0.06, lo=200, hi=2400, lfo=1.2, seed=722), 33.0)
    place(s, scrape(0.35, amp=0.06, seed=723), 36.5)
    hooves(s, 36.0, 41.6, step=0.2, amp=0.06, pan=-0.5, seed=724)
    hooves(s, 37.0, 41.6, step=0.19, amp=0.06, pan=0.5, seed=725)
    place(s, rumble(3.4, 0.18, seed=726), 38.4)
    place(s, noise_bed(12.0, amp=0.03, lo=200, hi=1200, lfo=0.2, seed=727), 41.6)
    place(s, snort(seed=12, amp=0.05), 44.9, pan=-0.3)
    place(s, snort(seed=13, amp=0.05), 48.4, pan=0.3)
    hooves(s, 50.2, 53.4, step=0.3, amp=0.05, pan=0.0, seed=728)
    place(s, scrape(0.3, amp=0.04, seed=729), 51.4)
    # the winter road: wind, hooves in the snow, chains
    place(s, noise_bed(8.4, amp=0.08, lo=200, hi=1800, lfo=0.3, seed=730), 53.6)
    hooves(s, 53.8, 61.6, step=0.5, amp=0.03, pan=0.1, seed=731)
    chains(s, 53.9, 61.6, step=0.5, amp=0.025, seed=732)
    # Samarra: the crowd, the reception
    place(s, cheer(9.0, amp=0.10, seed=733), 61.8)
    hooves(s, 61.8, 66.8, step=0.4, amp=0.05, pan=-0.2, seed=734)
    place(s, cheer(3.6, amp=0.08, seed=735), 66.9)
    place(s, cheer(11.0, amp=0.035, seed=736), 70.6)
    hooves(s, 70.6, 81.6, step=0.5, amp=0.03, pan=0.0, seed=737)
    chains(s, 70.8, 81.4, step=0.9, amp=0.02, seed=738)
    place(s, noise_bed(2.6, amp=0.04, lo=200, hi=1600, lfo=0.2, seed=739), 81.6)
    # the palace: silk, chains, the elephant, the gates, the roar
    place(s, noise_bed(4.6, amp=0.02, lo=200, hi=1200, lfo=0.2, seed=740), 84.2)
    for k, t in enumerate((85.0, 86.5, 87.6)):
        place(s, rustle(0.05, 0.7, seed=741 + k), t, pan=0.2 * (k - 1))
    chains(s, 85.6, 86.2, step=0.3, amp=0.02, seed=744)
    steps(s, 88.9, 90.8, step=0.5, amp=0.05, seed=745)
    chains(s, 88.9, 90.8, step=0.5, amp=0.025, seed=746)
    place(s, rumble(2.4, 0.12, seed=747), 89.0)
    place(s, cheer(7.4, amp=0.025, seed=748), 88.8)
    place(s, thud(0.2, 60, seed=749), 97.0)
    place(s, trumpet(0.14, 1.5, seed=750), 98.3)
    place(s, thud(0.25, 55, seed=751), 99.8)
    place(s, rumble(2.6, 0.14, seed=752), 99.0)
    place(s, creak(2.0, 0.10, seed=753), 102.4)
    place(s, thud(0.3, 50, seed=754), 103.0)
    place(s, cheer(9.2, amp=0.20, seed=755), 102.9)
    place(s, noise_bed(9.0, amp=0.06, lo=150, hi=900, lfo=0.8, seed=756), 103.0)
    for k, t in enumerate((104.4, 105.6, 106.8, 108.0)):
        place(s, thud(0.22, 55, seed=757 + k), t)
    place(s, trumpet(0.12, 1.4, seed=761), 106.0)


LINES = [("p7s1a", 0.6), ("p7s1b", 3.9), ("p7s1c", 8.3), ("p7s1d", 10.0),
         ("p7s3a", 24.4), ("p7s3b", 26.0), ("p7s3c", 42.2), ("p7s3d", 44.0), ("p7s3e", 46.6),
         ("p7s4a", 54.2), ("p7s4b", 71.0), ("p7s4c", 73.5), ("p7s4d", 76.4), ("p7s4e", 78.6),
         ("p7s5a", 84.6), ("p7s5b", 89.4), ("p7s5c", 93.6)]
if __name__ == "__main__":
    build(7, TOTAL, music, sfx, LINES, f'{AUDIO}/part07.wav')
    print('done')
