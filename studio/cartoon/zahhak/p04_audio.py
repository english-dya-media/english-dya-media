"""Part 4 · The Two Cooks — timing, music and sound.
Scene starts: s1 0 (hook: the two cooks whisper by the fire), s2 7.4 (title), s3 12.0 (a thousand years; truth hides; the guards take
two young men every night; a mother at her door), s4 33.0 (Armayel and Garmayel at home: the plan; they become the king's cooks),
s5 60.6 (the kitchen at night: they save one, the back door, the sheep's brain), s6 89.0 (night after night; the saved go to the
mountains with goats; Zahhak's scream; Arnavaz), end card 116.2, end 121.2"""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import series; series.from_folder(__file__)
from paths import AUDIO
from audio import *
from mix import build
from zsfx import *
from p01_audio import daf
TOTAL = 121.2
S = {"s1": 0.0, "s2": 7.4, "s3": 12.0, "s4": 33.0, "s5": 60.6, "s6": 89.0}
END_CARD = 116.2
SCREAM = 104.6

HOPE = [(0, 0), (2, 0.5), (4, 1.0), (3, 1.6), (2, 2.1), (4, 2.6), (5, 3.2)]


def bang(amp=0.3, seed=0):
    """a heavy door thrown open"""
    return thud(amp, 55, seed)


def lid(s, t, amp=0.04):
    """a metal lid set on a dish"""
    place(s, bell(1320, 0.8, amp), t)
    place(s, bell(1760, 0.6, amp * 0.6), t + 0.01)


def rumble(dur=3.0, amp=0.3, seed=0):
    x = noise_bed(dur, amp=amp, lo=30, hi=180, lfo=3.0, seed=seed)
    return x


def music(m):
    # S1 0-7.4: two cooks by the fire at night
    place(m, drone(55.0, 7.8, amp=0.08, a=1.5, r=1.0), 0.0)
    place(m, pad([shur(0, -1), shur(2, -1), shur(4, -1)], 7.2, amp=0.05, a=2.0, r=1.0, bright=4), 0.2)
    tanbur(m, [(0, 0), (2, 0.7), (1, 1.3), (0, 2.0)], 0.8, amp=0.10)
    heartbeat(m, 4.6, 7.2, bpm=70, amp=0.18)
    # S2 7.4-12.0: title
    place(m, drum(dur=3.2, f0=40, amp=0.9, noise=0.4), 7.4)
    place(m, drone(36.71, 4.9, amp=0.12, a=0.1, r=1.4), 7.4)
    place(m, pad([shur(0), shur(4), shur(0, 1)], 4.8, amp=0.10, a=0.4, r=1.6, bright=6), 7.4)
    tanbur(m, ZTHEME, 7.8, amp=0.22, low=True, step=0.85)
    # S3 12.0-33.0: a thousand years of fear
    place(m, drone(36.71, 21.4, amp=0.10, a=1.5, r=1.5), 12.0)
    place(m, pad([shur(1, -1), shur(0, -1)], 7.6, amp=0.05, a=2.0, r=1.0, bright=4), 12.2)
    for t in np.arange(19.7, 24.2, 0.75):                                    # the guards' march
        place(m, drum(dur=0.7, f0=52, amp=0.16, noise=0.2), t)
    place(m, drum(dur=1.8, f0=48, amp=0.4, noise=0.3), 24.4)
    place(m, pad([shur(0, -1), shur(3, -1)], 8.6, amp=0.05, a=1.5, r=2.0, bright=4), 24.4)
    tanbur(m, [(4, 0), (3, 0.8), (2, 1.5), (1, 2.2), (0, 3.0)], 28.2, amp=0.10, step=1.1)
    # S4 33.0-60.6: the cooks' house; the plan; the king's kitchen
    place(m, pad([shur(0), shur(2), shur(4)], 9.4, amp=0.05, a=2.0, r=1.5, bright=4), 33.0)
    tanbur(m, [(0, 0), (2, 0.6), (1, 1.2), (0, 1.8)], 33.6, amp=0.09)
    place(m, drum(dur=1.4, f0=60, amp=0.25, noise=0.2), 39.4)
    place(m, pad([shur(0), shur(4), shur(0, 1)], 13.6, amp=0.06, a=2.0, r=1.0, bright=5), 42.6)
    tanbur(m, HOPE, 43.4, amp=0.10, step=1.0)
    place(m, bell(784, 2.0, 0.03), 54.2)
    daf(m, 56.3, 60.4, bpm=112, amp=0.10)
    t = 56.4
    while t < 60.2:
        for i, deg in enumerate([0, 2, 4, 3, 2, 3, 4, 2]):
            place(m, pluck_fast(shur(deg), 0.9, amp=0.08), t + i * 0.268, pan=0.3)
        t += 2.14
    # S5 60.6-89.0: the kitchen at night
    place(m, drone(36.71, 6.6, amp=0.10, a=0.3, r=0.8), 60.6)
    place(m, drum(dur=1.6, f0=55, amp=0.4, noise=0.3), 65.2)
    place(m, pad([shur(1, -1), shur(0, -1), shur(4, -1)], 8.0, amp=0.06, a=1.5, r=1.5, bright=4), 67.2)
    tanbur(m, [(2, 0), (1, 0.9), (0, 1.8)], 71.6, amp=0.09, step=1.1)
    place(m, drone(55.0, 7.4, amp=0.06, a=1.0, r=1.0), 75.0)
    tanbur(m, HOPE[:5], 79.6, amp=0.11, step=0.8)
    place(m, pad([shur(0), shur(2), shur(4)], 6.4, amp=0.05, a=1.0, r=2.0, bright=5), 82.4)
    place(m, pad([shur(0), shur(4), shur(0, 1)], 2.8, amp=0.07, a=0.3, r=1.5, bright=6), 86.4)
    # S6 89.0-121.2: the mountains; the scream; Arnavaz; the end card
    tanbur(m, [(0, 0), (2, 0.6), (4, 1.2)], 89.4, amp=0.09)
    place(m, pad([shur(0), shur(2), shur(4), shur(0, 1)], 8.4, amp=0.07, a=1.5, r=1.5, bright=6), 92.4)
    tanbur(m, HOPE, 92.9, amp=0.12, low=True, step=1.05)
    place(m, drone(36.71, 4.0, amp=0.08, a=1.0, r=0.5), 100.6)
    place(m, pad([shur(1, -1), shur(0, -1)], 3.8, amp=0.04, a=1.5, r=0.5, bright=4), 100.6)
    place(m, drum(dur=3.0, f0=38, amp=0.95, noise=0.45), SCREAM)
    place(m, pad([shur(1, -1), shur(5, -1), shur(1)], 2.6, amp=0.08, a=0.05, r=1.5, bright=6), SCREAM)
    place(m, drone(36.71, 9.0, amp=0.12, a=0.2, r=1.0), 107.2)
    heartbeat(m, 110.6, 116.0, bpm=96, amp=0.22)
    place(m, drum(dur=3.0, f0=40, amp=0.75, noise=0.4), END_CARD)
    place(m, drone(36.71, 5.0, amp=0.10, a=0.2, r=2.0), END_CARD)
    place(m, pad([shur(0), shur(4), shur(0, 1)], 5.0, amp=0.08, a=0.6, r=2.0, bright=5), END_CARD)
    tanbur(m, ZTHEME[:4], END_CARD + 0.6, amp=0.14, low=True, step=0.9)


def sfx(s):
    # S1: the kitchen fire at night
    place(s, crackle(7.4, amp=0.10, rate=10, seed=401), 0.0)
    # S3: the hall; the guards; the mother; the night
    place(s, crackle(7.6, amp=0.05, rate=8, seed=402), 12.0)
    place(s, hiss(1.4, 0.05, seed=41), 13.0, pan=-0.3); place(s, hiss(1.4, 0.05, seed=42), 17.4, pan=0.3)
    steps(s, 19.6, 24.2, step=0.42, amp=0.05, seed=41, pan=-0.2)
    place(s, noise_bed(9.0, amp=0.04, lo=200, hi=1500, lfo=0.3, seed=403), 24.2)
    crickets(s, 24.2, 33.0, amp=0.012, seed=41)
    place(s, owl(0.04), 29.6, pan=0.4)
    # S4: the cooks' house; the kitchen by day
    place(s, crackle(23.2, amp=0.09, rate=10, seed=404), 33.0)
    place(s, noise_bed(4.4, amp=0.03, lo=200, hi=900, lfo=2.5, seed=405), 56.2)   # a pot bubbling
    # S5: the kitchen at night
    place(s, crackle(28.4, amp=0.09, rate=10, seed=406), 60.6)
    place(s, bang(0.3, seed=41), 60.9)
    steps(s, 60.9, 63.6, step=0.32, amp=0.05, seed=42, pan=-0.4)
    place(s, creak(1.4, 0.07, seed=41), 75.0, pan=0.5)
    crickets(s, 75.0, 82.2, amp=0.01, seed=42)
    steps(s, 80.9, 82.2, step=0.2, amp=0.04, seed=43, pan=0.6)               # he runs out
    lid(s, 84.4, 0.05)
    # S6: out the back door; the mountains; the bedchamber; the scream; the palace shakes
    place(s, creak(1.2, 0.06, seed=42), 89.2, pan=0.5)
    steps(s, 89.8, 92.0, step=0.4, amp=0.035, seed=44, pan=0.5)
    place(s, noise_bed(8.2, amp=0.05, lo=200, hi=1600, lfo=0.3, seed=407), 92.4)
    for k, t in enumerate((93.6, 95.3, 97.8, 99.2)):
        place(s, bleat(0.05, seed=41 + k, f0=480 + 60 * (k % 2)), t, pan=0.3 - 0.2 * k)
    crickets(s, 100.6, 104.6, amp=0.012, seed=43)
    place(s, hiss(1.4, 0.09, seed=43), SCREAM + 0.2, pan=-0.3); place(s, hiss(1.6, 0.10, seed=44), SCREAM + 0.5, pan=0.3)
    place(s, rumble(3.4, 0.35, seed=41), 107.2)
    for k, t in enumerate((107.5, 108.1, 108.6, 109.3)):
        place(s, bell(1400 + 300 * k, 0.5, 0.03), t, pan=0.4 - 0.25 * k)
    place(s, rustle(0.05, 0.8, seed=41), 110.6)
    place(s, noise_bed(5.0, amp=0.03, lo=200, hi=1500, lfo=0.2, seed=408), END_CARD)


LINES = [("p4s1a", 0.6), ("p4s1b", 4.9),
         ("p4s3a", 12.4), ("p4s3e", 16.1), ("p4s3b", 19.9), ("p4s3c", 24.5), ("p4s3d", 28.0),
         ("p4s4a", 33.4), ("p4s4b", 39.4), ("p4s4c", 42.8), ("p4s4d", 47.0), ("p4s4e", 49.2), ("p4s4g", 52.0), ("p4s4h", 54.0), ("p4s4f", 56.5),
         ("p4s5a", 60.9), ("p4s5b", 65.2), ("p4s5c", 67.5), ("p4s5h", 71.4), ("p4s5d", 75.3), ("p4s5e", 79.4), ("p4s5f", 82.5), ("p4s5g", 86.6),
         ("p4s6a", 89.3), ("p4s6b", 92.7), ("p4s6c", 96.9), ("p4s6d", 100.9), ("p4s6e", 104.6), ("p4s6g", 107.4), ("p4s6f", 110.8)]
if __name__ == "__main__":
    build(4, TOTAL, music, sfx, LINES, f'{AUDIO}/part04.wav')
    print('done')
