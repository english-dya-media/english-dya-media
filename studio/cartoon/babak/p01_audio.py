import os, sys; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import series; series.from_folder(__file__)
from paths import AUDIO
from audio import *
from mix import build
TOTAL = 127.0

def music(m):
    # S1 0-16: low drone + heartbeat frame drum, swell into the title hit
    place(m, drone(73.42, 16.5, amp=0.16, a=2.5, r=0.6), 0)
    place(m, drone(110.0, 15.5, amp=0.07, a=4, r=1.0), 0.5)
    for i, t in enumerate(np.arange(1.0, 15.6, 2.0)):
        place(m, drum(f0=58, amp=0.25 + 0.03 * i, noise=0.15), t)
    place(m, pad([shur(0, -1), shur(4, -1), shur(0)], 6.0, amp=0.10, a=4.5, r=0.3), 10.2)
    # S2 16-21 title
    place(m, drum(dur=2.5, f0=48, amp=0.95, noise=0.4), 16.0)
    place(m, drone(73.42, 5.5, amp=0.14, a=0.05, r=2.5), 16.0)
    for k, (deg, dt) in enumerate([(0, 0.8), (4, 2.0), (0, 3.2)]):
        place(m, pluck_fast(shur(deg), 2.5, amp=0.30), 16.0 + dt, pan=-0.2)
    # S3 21-47 village: gentle tanbur over soft drone
    place(m, drone(73.42, 26.5, amp=0.08, a=3, r=2), 21.0)
    motif = [(0, 0.0), (2, 0.6), (1, 1.0), (0, 1.4), (3, 2.4), (2, 3.0), (1, 3.4), (0, 4.2)]
    for rep, t0 in enumerate([22.5, 28.5, 34.5, 40.5]):
        for deg, dt in motif:
            d = deg + (1 if rep == 2 and deg == 3 else 0)
            place(m, pluck_fast(shur(d), 2.2, amp=0.22), t0 + dt, pan=0.25)
            if dt in (0.0, 2.4): place(m, pluck_fast(shur(d, -1), 2.4, amp=0.14), t0 + dt, pan=-0.2)
    # S4 47-71 omen: shimmering high pad + heartbeat at the glow
    place(m, drone(73.42, 24.5, amp=0.07, a=3, r=2), 47.0)
    place(m, pad([shur(0, 2), shur(1, 2), shur(4, 1)], 10.0, amp=0.07, a=3.5, r=3.0, bright=3), 51.0)
    for t in np.arange(54.6, 58.6, 1.0):
        place(m, drum(dur=0.6, f0=52, amp=0.30, noise=0.05), t); place(m, drum(dur=0.6, f0=50, amp=0.20, noise=0.05), t + 0.28)
    for k, (deg, dt) in enumerate([(4, 0), (3, 1.2), (2, 2.0), (1, 2.6), (0, 3.6)]):
        place(m, pluck_fast(shur(deg), 2.6, amp=0.2), 62.0 + dt, pan=0.2)
    # S5 71-99 montage: ostinato (stable), solo lesson (fire), busy bazaar rhythm
    ost = [0, 0, 2, 0, 3, 2, 1, 0]
    t = 71.4
    while t < 79.5:
        for i, deg in enumerate(ost):
            place(m, pluck_fast(shur(deg), 1.2, amp=0.16), t + i * 0.3, pan=0.3)
        t += 2.4
    for deg, dt in [(0, 0.5), (1, 1.4), (2, 2.0), (1, 2.8), (0, 3.6), (0, 6.0), (2, 6.5), (3, 7.0), (2, 7.6)]:
        place(m, pluck_fast(shur(deg), 2.0, amp=0.2), 80.0 + dt, pan=-0.1)
    t = 89.2
    while t < 98.5:
        for i, deg in enumerate([0, 2, 3, 4, 3, 2, 1, 0]):
            place(m, pluck_fast(shur(deg), 1.0, amp=0.15), t + i * 0.25, pan=0.3)
        place(m, drum(dur=0.7, f0=90, amp=0.22, noise=0.35), t); place(m, drum(dur=0.7, f0=110, amp=0.14, noise=0.4), t + 1.0)
        t += 2.0
    place(m, drone(73.42, 28.5, amp=0.06, a=3, r=3), 71.0)
    # S6 99-127: cold drone, tension pad, swell on the door, CTA hit
    place(m, drone(36.71, 28.5, amp=0.15, a=3, r=2), 99.0)
    place(m, pad([shur(0, -1), shur(2, -1), shur(4, -1)], 16.0, amp=0.10, a=6, r=2, bright=4), 104.0)
    place(m, pad([shur(0), shur(2), shur(4), shur(0, 1)], 8.0, amp=0.12, a=2.0, r=4.0, bright=5), 115.0)
    place(m, drum(dur=2.5, f0=46, amp=0.8, noise=0.35), 115.4)
    place(m, drum(dur=2.5, f0=46, amp=0.9, noise=0.4), 123.5)
    place(m, pluck_fast(shur(0), 3.0, amp=0.3), 123.6)

def sfx(s):
    place(s, noise_bed(16.5, amp=0.07, lo=300, hi=2600, lfo=0.6, seed=1), 0)
    for t in np.arange(1.0, 15.5, 1.35):
        place(s, drum(dur=0.5, f0=42, amp=0.22, noise=0.1), t)
    place(s, noise_bed(26.5, amp=0.035, lo=200, hi=1500, lfo=0.1, seed=2), 21.0)
    for t in (24.5, 28.2, 31.9, 36.0, 41.3):
        place(s, bell(880, 2.0, 0.05), t, pan=0.4)
    place(s, noise_bed(24.5, amp=0.05, lo=800, hi=5000, lfo=0.2, seed=3), 47.0)
    place(s, noise_bed(3.5, amp=0.08, lo=100, hi=700, lfo=0.5, seed=4), 54.3)
    place(s, crackle(9.0, amp=0.16, seed=5), 80.0)
    place(s, noise_bed(10.5, amp=0.07, lo=300, hi=2500, lfo=0.7, seed=6), 89.0)
    for t in np.arange(92.0, 97.5, 0.32):
        place(s, knock(0.10), t, pan=-0.3)
    place(s, noise_bed(8.3, amp=0.26, lo=200, hi=3200, lfo=0.25, seed=7), 99.0)
    place(s, noise_bed(8.3, amp=0.07, lo=120, hi=600, lfo=0.2, seed=8), 107.0)
    place(s, crackle(8.0, amp=0.10, seed=9), 107.0)
    for t in (110.0, 111.0, 112.0):
        place(s, knock(0.95), t, pan=0.35)
    creak_t = np.arange(int(1.6 * SR)) / SR
    creak = (np.sin(2 * np.pi * (180 + 60 * creak_t) * creak_t) * np.exp(-creak_t * 1.5) * 0.08).astype(np.float32)
    place(s, bandpass(creak, 150, 2000), 115.2, pan=0.2)
    place(s, noise_bed(12.0, amp=0.20, lo=200, hi=3200, lfo=0.3, seed=10), 115.2)

LINES = [("p1s1a", 3.5), ("p1s1b", 5.1), ("p1s1c", 9.2), ("p1s3a", 24.0), ("p1s3b", 30.0), ("p1s3c", 33.5), ("p1s3d", 35.8),
         ("p1s4a", 57.0), ("p1s4b", 61.0), ("p1s4c", 63.6), ("p1s5a", 82.0), ("p1s5b", 95.5), ("p1s6a", 117.6)]
if __name__ == "__main__":
    build(1, TOTAL, music, sfx, LINES, f'{AUDIO}/part01.wav')
    print('done')
