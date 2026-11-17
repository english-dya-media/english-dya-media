"""Part 3 · The Doctor — timing, music and sound.
Scene starts: s1 0 (hook: the doctor's one cure; the snake shadow), s2 7.4 (title), s3 12.0 (the snakes give the king no rest; cut off,
they grow back; the doctors fail), s4 42.6 (Iblis comes as a doctor: feed them; the reveal), s5 71.8 (Jamshid's pride; the light of God
leaves him; the nobles turn away), s6 108.2 (the riders of Iran choose Zahhak; Jamshid runs; Arnavaz and Shahrnaz), end card 145.4,
end 150.4"""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import series; series.from_folder(__file__)
from paths import AUDIO
from audio import *
from mix import build
from zsfx import *
from p01_audio import SLY, daf
TOTAL = 150.4
S = {"s1": 0.0, "s2": 7.4, "s3": 12.0, "s4": 42.6, "s5": 71.8, "s6": 108.2}
END_CARD = 145.4
SWING = 21.7          # the sword comes down (s3 C); the picture cuts at 22.0
FARR = 99.4           # the light of God rises out of Jamshid (s5 F)

ROYAL = [(0, 0), (2, 0.4), (4, 0.8), (5, 1.2), (4, 1.8), (2, 2.2), (4, 2.6), (0, 3.4)]


def shimmer(m, t0, n=10, step=0.11, amp=0.05, down=True):
    """a run of small bells, high to low (the light leaving) or low to high"""
    degs = list(range(n))
    for i, d in enumerate(degs[::-1] if down else degs):
        place(m, bell(shur(d % 7, 2 + d // 7) * 1.0, 1.6, amp), t0 + i * step, pan=0.4 - 0.08 * i)


def breath(amp=0.06, dur=1.0, seed=0):
    """a long breath out"""
    x = noise_bed(dur, amp=amp, lo=300, hi=2200, lfo=0.2, seed=seed)
    ramp = np.sin(np.linspace(0, np.pi, len(x))) ** 1.5
    return x * ramp[:, None]


def music(m):
    # S1 0-7.4: the doctor's whisper, then the snake shadow
    place(m, drone(36.71, 7.8, amp=0.12, a=1.0, r=0.8), 0.0)
    place(m, pad([shur(1, -1), shur(0, -1)], 7.2, amp=0.05, a=2.0, r=1.0, bright=4), 0.3)
    for deg, dt in SLY:
        place(m, pluck_fast(shur(deg), 0.6, amp=0.09), 0.5 + dt, pan=0.35)
    heartbeat(m, 3.9, 7.0, bpm=80, amp=0.22)
    place(m, bell(196, 3.0, 0.05), 6.4)
    # S2 7.4-12.0: title
    place(m, drum(dur=3.2, f0=40, amp=0.9, noise=0.4), 7.4)
    place(m, drone(36.71, 4.9, amp=0.12, a=0.1, r=1.4), 7.4)
    place(m, pad([shur(0), shur(4), shur(0, 1)], 4.8, amp=0.10, a=0.4, r=1.6, bright=6), 7.4)
    tanbur(m, ZTHEME, 7.8, amp=0.22, low=True, step=0.85)
    # S3 12.0-42.6: no rest; the cut; the snakes grow back; the doctors
    place(m, drone(36.71, 7.6, amp=0.10, a=1.0, r=0.8), 12.0)
    place(m, pad([shur(0, -1), shur(1, -1)], 7.2, amp=0.05, a=1.5, r=1.0, bright=4), 12.2)
    place(m, drum(dur=1.8, f0=55, amp=0.45, noise=0.25), 17.6)
    for i, t in enumerate(np.arange(19.7, SWING, 0.16)):                    # a drum roll under the raised sword
        place(m, drum(dur=0.4, f0=70 + 4 * i, amp=0.10 + 0.02 * i, noise=0.3), t)
    place(m, drum(dur=2.4, f0=42, amp=0.8, noise=0.4), SWING + 0.2)
    place(m, pad([shur(0), shur(2), shur(4)], 2.6, amp=0.06, a=0.6, r=1.2, bright=5), 22.2)  # relief
    place(m, drone(36.71, 5.6, amp=0.10, a=1.5, r=0.5), 24.2)                # the snakes come back
    place(m, pad([shur(1, -1), shur(5, -1)], 5.2, amp=0.06, a=2.0, r=0.6, bright=5), 24.4)
    place(m, drum(dur=2.6, f0=40, amp=0.75, noise=0.4), 27.8)
    place(m, pad([shur(0, -1), shur(1, -1), shur(4, -1)], 2.4, amp=0.07, a=0.1, r=1.6, bright=5), 27.8)
    place(m, pad([shur(0), shur(2), shur(4)], 9.4, amp=0.05, a=1.5, r=1.5, bright=4), 29.8)  # the doctors
    tanbur(m, [(0, 0), (2, 0.6), (1, 1.2), (0, 1.8)], 30.0, amp=0.11)
    tanbur(m, [(3, 0), (2, 0.6), (1, 1.1), (0, 1.8)], 34.2, amp=0.09)
    place(m, bell(784, 2.0, 0.03), 36.4)
    place(m, drum(dur=1.8, f0=50, amp=0.5, noise=0.3), 39.2)
    place(m, drone(36.71, 3.4, amp=0.08, a=0.2, r=1.2), 39.2)
    # S4 42.6-71.8: the grey doctor
    place(m, drone(36.71, 29.4, amp=0.08, a=2.0, r=1.5), 42.6)
    place(m, pad([shur(1, -1), shur(0, -1)], 14.0, amp=0.05, a=2.5, r=1.5, bright=4), 42.8)
    for t0 in (43.4, 48.0, 53.6):
        for deg, dt in SLY:
            place(m, pluck_fast(shur(deg), 0.6, amp=0.08), t0 + dt * 1.15, pan=0.35)
    place(m, bell(1175, 2.5, 0.035), 46.2)
    heartbeat(m, 57.3, 64.6, bpm=66, amp=0.24)
    place(m, pad([shur(1, -1), shur(5, -1)], 7.2, amp=0.05, a=2.0, r=1.0, bright=4), 57.2)
    place(m, drum(dur=3.2, f0=36, amp=0.95, noise=0.45), 65.1)
    place(m, drone(55.0, 6.4, amp=0.07, a=0.2, r=1.8), 65.1)
    place(m, pad([shur(0, -1), shur(1, -1), shur(4, -1)], 6.0, amp=0.07, a=0.3, r=2.0, bright=5), 65.2)
    place(m, bell(196, 3.5, 0.05), 68.0)
    # S5 71.8-108.2: Jamshid's golden hall, the proud words, the light leaving
    place(m, pad([shur(0), shur(2), shur(4), shur(0, 1)], 10.0, amp=0.08, a=1.5, r=1.5, bright=6), 71.8)
    tanbur(m, ROYAL, 72.2, amp=0.16, low=True, step=0.9)
    daf(m, 72.6, 80.8, bpm=96, amp=0.07)
    tanbur(m, ROYAL[:5], 76.8, amp=0.11, step=0.9)
    place(m, pad([shur(0), shur(4), shur(0, 1)], 13.2, amp=0.07, a=1.0, r=1.0, bright=6), 81.4)
    for t in (81.5, 86.1, 90.9):
        place(m, drum(dur=1.6, f0=60, amp=0.3, noise=0.15), t)
    tanbur(m, [(0, 0), (4, 0.4), (0, 1.0)], 91.0, amp=0.18, low=True)
    place(m, drum(dur=2.4, f0=46, amp=0.6, noise=0.3), 94.2)
    place(m, drone(55.0, 8.0, amp=0.07, a=1.0, r=1.5), 94.8)                 # the silence of the nobles
    shimmer(m, FARR - 0.2, n=12, step=0.12, amp=0.05)
    place(m, pad([shur(1, -1), shur(0, -1)], 9.0, amp=0.06, a=2.0, r=2.0, bright=4), 100.0)
    tanbur(m, [(2, 0), (1, 0.9), (0, 1.8)], 103.2, amp=0.10, step=1.1)
    place(m, bell(220, 3.0, 0.04), 106.4)
    # S6 108.2-150.4: the riders, "gladly", the army, Jamshid runs, the princesses, the end card
    place(m, drone(36.71, 5.4, amp=0.10, a=0.6, r=0.6), 108.2)
    for i, t in enumerate(np.arange(108.4, 113.2, 0.5)):
        place(m, drum(dur=0.7, f0=58, amp=0.18 + (0.06 if i % 4 == 0 else 0), noise=0.2), t)
    place(m, drone(36.71, 7.8, amp=0.08, a=1.0, r=1.0), 113.4)
    for deg, dt in SLY:
        place(m, pluck_fast(shur(deg), 0.6, amp=0.10), 119.1 + dt, pan=0.35)
    for i, t in enumerate(np.arange(121.2, 126.0, 0.4)):                     # the march
        place(m, drum(dur=0.6, f0=50 if i % 2 else 62, amp=0.26 + (0.1 if i % 4 == 0 else 0), noise=0.3), t)
    place(m, pad([shur(0, -1), shur(4, -1)], 4.8, amp=0.07, a=0.5, r=0.5, bright=5), 121.2)
    place(m, drone(55.0, 6.0, amp=0.06, a=1.0, r=1.5), 126.0)                # Jamshid alone
    tanbur(m, [(4, 0), (3, 0.9), (2, 1.6), (1, 2.3), (0, 3.2)], 126.6, amp=0.10, step=1.1)
    place(m, drone(36.71, 13.6, amp=0.10, a=1.5, r=1.0), 132.2)              # the snake king's palace
    for t in np.arange(132.4, 140.0, 1.4):
        place(m, drum(dur=1.2, f0=48, amp=0.22, noise=0.15), t)
    place(m, pad([shur(1, -1), shur(0, -1)], 7.6, amp=0.05, a=2.0, r=1.0, bright=4), 132.4)
    heartbeat(m, 140.0, 142.6, bpm=84, amp=0.22)
    place(m, drum(dur=3.0, f0=40, amp=0.8, noise=0.4), 143.0)
    place(m, pad([shur(1, -1), shur(5, -1)], 2.4, amp=0.06, a=0.2, r=1.5, bright=5), 143.0)
    place(m, drum(dur=3.0, f0=40, amp=0.75, noise=0.4), END_CARD)
    place(m, drone(36.71, 5.0, amp=0.10, a=0.2, r=2.0), END_CARD)
    place(m, pad([shur(0), shur(4), shur(0, 1)], 5.0, amp=0.08, a=0.6, r=2.0, bright=5), END_CARD)
    tanbur(m, ZTHEME[:4], END_CARD + 0.6, amp=0.14, low=True, step=0.9)


def sfx(s):
    # S1: torches, the snakes on the wall
    place(s, crackle(7.4, amp=0.06, rate=8, seed=301), 0.0)
    place(s, hiss(1.2, 0.05, seed=31), 4.6, pan=-0.3); place(s, hiss(1.4, 0.06, seed=32), 5.8, pan=0.3)
    # S3: the hall at night; the cut; the regrowth; the doctors leave
    place(s, crackle(30.6, amp=0.05, rate=8, seed=302), 12.0)
    place(s, hiss(1.4, 0.06, seed=33), 12.6, pan=-0.3); place(s, hiss(1.6, 0.07, seed=34), 14.4, pan=0.3)
    place(s, hiss(1.2, 0.08, seed=35), 17.2, pan=0.0)
    place(s, scrape(0.7, 0.07, seed=31), 19.8)                                 # the sword drawn
    place(s, whoosh(1.0, amp=0.2, seed=31), SWING - 0.75)
    place(s, thud(0.25, 60, seed=31), SWING + 0.15)
    place(s, breath(0.05, 1.2, seed=31), 22.3)
    place(s, rustle(0.05, 1.0, seed=31), 24.4); place(s, rustle(0.05, 1.0, seed=32), 25.6)
    place(s, hiss(1.4, 0.08, seed=36), 26.6, pan=-0.3); place(s, hiss(1.6, 0.09, seed=37), 27.0, pan=0.3)
    steps(s, 29.9, 31.6, step=0.45, amp=0.03, seed=31, pan=-0.2)
    place(s, hiss(1.0, 0.06, seed=38), 37.0, pan=0.3)
    steps(s, 40.6, 42.4, step=0.22, amp=0.045, seed=32, pan=-0.4)              # the doctors hurry out
    # S4: a door, steps of the grey doctor; the whisper; his shadow
    place(s, crackle(29.2, amp=0.05, rate=8, seed=303), 42.6)
    place(s, creak(1.4, 0.07, seed=31), 42.8, pan=-0.5)
    steps(s, 43.4, 46.2, step=0.55, amp=0.04, seed=33, pan=-0.3)
    place(s, rustle(0.04, 0.8, seed=33), 46.6)
    place(s, hiss(1.0, 0.06, seed=39), 56.2, pan=0.2)
    place(s, hiss(1.6, 0.07, seed=40), 62.4, pan=-0.3); place(s, hiss(1.6, 0.07, seed=41), 63.0, pan=0.3)
    steps(s, 65.0, 70.2, step=0.6, amp=0.04, seed=34, pan=0.3)
    place(s, noise_bed(6.4, amp=0.03, lo=60, hi=400, lfo=0.2, seed=304), 65.1)
    # S5: the golden hall (birds outside), the light leaving, the nobles' steps
    for k, t in enumerate((72.0, 72.9, 74.1, 75.6, 78.2)):
        place(s, chirp(3000 + 250 * (k % 3), amp=0.025), t, pan=0.4 - 0.2 * k)
    place(s, crackle(36.4, amp=0.035, rate=6, seed=305), 71.8)
    place(s, rustle(0.04, 0.8, seed=34), 90.9)
    place(s, whoosh(2.4, amp=0.10, seed=32), FARR + 0.3)
    steps(s, 103.0, 107.8, step=0.5, amp=0.04, seed=35, pan=0.0)
    # S6: hooves; the king's hall; the army; wind in the empty hall; the princesses' steps
    hooves(s, 108.2, 113.4, step=0.21, amp=0.08, pan=0.1, seed=31, gallop=True)
    place(s, noise_bed(5.2, amp=0.05, lo=200, hi=1500, lfo=0.6, seed=306), 108.2)
    place(s, crackle(7.6, amp=0.05, rate=8, seed=307), 113.4)
    place(s, hiss(1.4, 0.07, seed=42), 119.6, pan=-0.3); place(s, hiss(1.2, 0.06, seed=43), 120.2, pan=0.3)
    hooves(s, 121.2, 126.0, step=0.3, amp=0.07, pan=-0.1, seed=32)
    steps(s, 121.2, 126.0, step=0.4, amp=0.05, seed=36, pan=0.2)
    place(s, noise_bed(4.8, amp=0.06, lo=150, hi=1200, lfo=0.4, seed=308), 121.2)
    place(s, noise_bed(6.2, amp=0.05, lo=200, hi=1600, lfo=0.25, seed=309), 126.0)   # wind in the empty hall
    place(s, thud(0.10, 140, seed=32), 128.35)                                  # the crown set down
    steps(s, 129.0, 131.6, step=0.5, amp=0.035, seed=37, pan=-0.4)
    place(s, crackle(18.2, amp=0.05, rate=8, seed=310), 132.2)
    steps(s, 133.2, 137.6, step=0.55, amp=0.04, seed=38, pan=-0.2)
    place(s, hiss(1.4, 0.07, seed=44), 143.6, pan=-0.3); place(s, hiss(1.6, 0.08, seed=45), 144.0, pan=0.3)
    place(s, noise_bed(5.0, amp=0.03, lo=200, hi=1500, lfo=0.2, seed=311), END_CARD)


LINES = [("p3s1a", 0.8), ("p3s1b", 4.2),
         ("p3s3a", 12.5), ("p3s3b", 17.6), ("p3s3c", 24.4), ("p3s3d", 27.9), ("p3s3e", 30.1), ("p3s3f", 33.8), ("p3s3g", 36.4), ("p3s3h", 39.2),
         ("p3s4a", 43.2), ("p3s4b", 47.9), ("p3s4c", 51.4), ("p3s4d", 53.6), ("p3s4e", 55.95), ("p3s4f", 57.5), ("p3s4g", 61.7), ("p3s4h", 65.3),
         ("p3s4i", 68.2),
         ("p3s5a", 72.4), ("p3s5b", 77.5), ("p3s5c", 81.6), ("p3s5d", 86.2), ("p3s5e", 91.0), ("p3s5f", 95.1), ("p3s5g", 97.5), ("p3s5h", 103.0),
         ("p3s6a", 108.6), ("p3s6b", 113.7), ("p3s6c", 119.0), ("p3s6d", 121.5), ("p3s6e", 126.4), ("p3s6f", 132.6), ("p3s6g", 137.5),
         ("p3s6h", 140.2), ("p3s6i", 142.9)]
if __name__ == "__main__":
    build(3, TOTAL, music, sfx, LINES, f'{AUDIO}/part03.wav')
    print('done')
