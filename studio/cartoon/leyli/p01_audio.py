"""Part 1 · The School — timing, music and sound.
Scene starts: s1 0 (hook: a thin man writes a name in the sand at dusk; the wind takes it away; he writes it again), s2 8.4 (title: the
camp of the Banu Amir at dawn), s3 13.0 (the Banu Amir; the chief and his son; "his name was Qays"; "today you go to school"), s4 41.0
(the tent school: Leyli; alif, ba, ta; the whispers; "…Leyli?"; "except you two"), s5 84.6 (the talk reaches Leyli's tent; her father:
"from tomorrow, she stays at home"), s6 108.2 (her place is empty; Qays walks among the tents calling her name; the boys shout "Majnun!";
he walks into the dunes), end card 138.2, end 143.4"""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import series; series.from_folder(__file__)
from paths import AUDIO
from audio import *
from mix import build
from lsfx import *

TOTAL = 143.4
S = {"s1": 0.0, "s2": 8.4, "s3": 13.0, "s4": 41.0, "s5": 84.6, "s6": 108.2}
END_CARD = 138.2
WRITE = (0.6, 3.6)      # the finger writes the name in the sand (s1 A)
GUST = 5.0              # the wind blows the name away (s1 B)
LEYLI_IN = 45.4         # Leyli's close-up (s4 B)
LOOK = 49.8             # Qays looks at her (s4 C)
LAUGH = 71.2            # the children laugh at "…Leyli?"
DOOR = 97.8             # Leyli's father in the doorway
EMPTY = 108.2           # the empty place on the rug


def music(m):
    # S1 0-8.4: dusk in the desert; the ney alone
    place(m, drone(36.71, 8.6, amp=0.07, a=1.0, r=1.6), 0.0)
    place(m, pad([shur(0, -1), shur(4, -1)], 8.2, amp=0.04, a=1.5, r=1.6, bright=4), 0.0)
    ney(m, LTHEME[:4], 0.6, amp=0.05, step=0.9)
    ney(m, [(2, 0, 1.2), (1, 1.2, 0.8), (0, 2.0, 1.8)], 5.4, amp=0.045, step=0.8)
    # S2 8.4-13.0: title over the camp at dawn
    place(m, drum(dur=2.8, f0=44, amp=0.7, noise=0.35), 8.4)
    place(m, drone(36.71, 4.9, amp=0.10, a=0.2, r=1.4), 8.4)
    place(m, pad([shur(0, -1), shur(4, -1), shur(0)], 4.8, amp=0.07, a=0.4, r=1.6, bright=5), 8.4)
    tanbur(m, [(0, 0), (2, 0.5), (4, 1.0), (3, 1.6), (2, 2.1), (0, 2.8)], 8.7, amp=0.2, low=True, step=0.6)
    ney(m, LTHEME, 9.0, amp=0.04, step=0.62)
    # S3 13.0-41.0: the camp, the chief and his son (warm, light)
    place(m, drone(36.71, 9.0, amp=0.06, a=1.0, r=1.0), 13.0)
    place(m, pad([shur(0), shur(2), shur(4)], 9.0, amp=0.04, a=1.5, r=1.5, bright=5), 13.0)
    tanbur(m, [(0, 0), (1, 0.5), (2, 1.0), (4, 1.6), (2, 2.2), (1, 2.6), (0, 3.2)], 13.6, amp=0.11, step=0.9)
    tanbur(m, [(2, 0), (3, 0.5), (4, 1.0), (2, 1.8), (0, 2.6)], 18.4, amp=0.1, step=0.9)
    place(m, pad([shur(0), shur(4), shur(0, 1)], 6.4, amp=0.05, a=1.0, r=1.5, bright=5), 21.9)
    ney(m, [(0, 0, 1.0), (2, 1.2, 1.2), (4, 2.6, 2.0)], 23.6, amp=0.045, step=0.9)
    place(m, drone(36.71, 12.6, amp=0.05, a=1.0, r=1.6), 28.4)
    tanbur(m, [(0, 0), (2, 0.5), (1, 1.0), (0, 1.6)], 28.8, amp=0.08, step=0.9)
    tanbur(m, [(2, 0), (4, 0.5), (5, 1.0), (4, 1.5), (2, 2.0)], 35.8, amp=0.09, step=0.8)
    tanbur(m, [(4, 0), (2, 0.4), (0, 0.9)], 39.6, amp=0.12, step=0.7)
    # S4 41.0-84.6: the school; Leyli; the lesson; the whispers; love
    place(m, drone(36.71, 4.4, amp=0.05, a=0.8, r=1.0), 41.0)
    tanbur(m, [(0, 0), (2, 0.6), (1, 1.2)], 41.4, amp=0.07, step=0.9)
    place(m, pad([shur(2), shur(4), shur(0, 1)], 8.0, amp=0.06, a=1.2, r=2.0, bright=6), LEYLI_IN)
    shimmer(m, LEYLI_IN + 0.2, 2.4, amp=0.025, seed=1)
    ney(m, LTHEME, LEYLI_IN + 0.4, amp=0.05, step=0.75)
    shimmer(m, LOOK + 0.3, 2.0, amp=0.02, seed=2, base=1046.5)
    place(m, drone(36.71, 8.4, amp=0.04, a=1.0, r=1.0), 52.6)
    tanbur(m, [(0, 0), (0, 0.5), (1, 1.0), (0, 1.5)], 52.8, amp=0.06, step=0.8)
    place(m, pad([shur(0), shur(2)], 5.4, amp=0.03, a=1.0, r=1.0, bright=4), 61.0)
    tanbur(m, [(2, 0), (1, 0.3), (2, 0.6)], 66.4, amp=0.07, step=0.6)
    place(m, bell(880, 1.6, 0.02), 70.0)
    tanbur(m, [(4, 0), (3, 0.25), (2, 0.5), (1, 0.75), (0, 1.0)], LAUGH + 0.2, amp=0.1, step=0.5)
    place(m, pad([shur(0), shur(4), shur(0, 1)], 7.0, amp=0.06, a=1.5, r=2.5, bright=5), 78.0)
    ney(m, LTHEME, 78.4, amp=0.055, step=0.85)
    shimmer(m, 82.6, 2.0, amp=0.02, seed=3)
    # S5 84.6-108.2: the talk travels; Leyli's tent; her father (low, darker)
    place(m, drone(36.71, 5.2, amp=0.06, a=0.6, r=1.0), 84.6)
    place(m, pad([shur(1, -1), shur(5, -1)], 5.0, amp=0.04, a=0.8, r=1.0, bright=4), 84.6)
    place(m, drone(36.71, 8.4, amp=0.05, a=1.0, r=1.0), 89.6)
    tanbur(m, [(0, 0), (1, 0.8), (0, 1.6)], 90.0, amp=0.06, step=1.0)
    place(m, drum(dur=1.8, f0=46, amp=0.45, noise=0.3), DOOR)
    place(m, drone(36.71, 10.4, amp=0.08, a=0.4, r=2.0), DOOR)
    place(m, pad([shur(1, -1), shur(5, -1), shur(1)], 10.0, amp=0.05, a=0.6, r=2.0, bright=4), DOOR)
    place(m, drum(dur=1.6, f0=44, amp=0.35, noise=0.3), 102.6)
    ney(m, [(2, 0, 1.2), (1, 1.3, 1.0), (0, 2.5, 2.4)], 104.6, amp=0.045, step=0.9)
    # S6 108.2-143.4: the empty place; "Leyli!"; "Majnun!"; into the dunes; end card
    place(m, drone(36.71, 7.4, amp=0.05, a=0.8, r=1.0), EMPTY)
    place(m, bell(440, 3.0, 0.03), EMPTY + 0.8)
    place(m, pad([shur(0), shur(2)], 7.0, amp=0.03, a=1.0, r=1.0, bright=4), EMPTY + 0.4)
    place(m, drone(36.71, 12.6, amp=0.07, a=0.8, r=1.0), 115.6)
    tanbur(m, [(0, 0), (1, 0.4), (2, 0.8), (1, 1.4), (0, 2.0)], 116.0, amp=0.08, step=0.9)
    for i, t in enumerate(np.arange(121.6, 128.0, 0.4)):              # the boys: quick light drum
        place(m, drum(dur=0.5, f0=90 if i % 2 else 70, amp=0.12, noise=0.2), t)
    place(m, pad([shur(0), shur(4), shur(0, 1)], 10.0, amp=0.06, a=2.0, r=2.0, bright=5), 128.2)
    ney(m, LTHEME, 128.6, amp=0.055, step=0.9)
    ney(m, LTHEME[:3], 134.0, amp=0.045, step=0.9)
    place(m, drum(dur=3.0, f0=40, amp=0.8, noise=0.4), END_CARD)
    place(m, drone(36.71, 5.2, amp=0.09, a=0.2, r=2.0), END_CARD)
    place(m, pad([shur(0), shur(4), shur(0, 1)], 5.0, amp=0.07, a=0.3, r=2.0, bright=6), END_CARD)
    tanbur(m, [(0, 0), (2, 0.5), (4, 1.0), (3, 1.6), (2, 2.1), (0, 2.8)], END_CARD + 0.5, amp=0.14, low=True, step=0.6)


def sfx(s):
    # S1: wind over the dunes; the finger in the sand; the gust
    place(s, noise_bed(8.4, amp=0.03, lo=300, hi=2000, lfo=0.2, seed=1), 0.0)
    for k, t in enumerate(np.arange(WRITE[0], WRITE[1], 0.32)):
        place(s, scrape(0.3, 0.018, seed=k), t, pan=0.1)
    place(s, gust(2.6, 0.08, seed=2), GUST - 0.3)
    place(s, sand_hiss(2.6, 0.05, seed=3), GUST)
    # S2/S3: dawn in the camp: birds, a camel, the fire, steps
    place(s, noise_bed(14.0, amp=0.02, lo=300, hi=2500, lfo=0.15, seed=4), 8.4)
    for k, t in enumerate((10.2, 10.4, 12.0, 14.6, 14.8, 17.2, 20.4, 20.6)):
        place(s, chirp(2900 + 300 * (k % 3), amp=0.03), t, pan=0.5 - 0.25 * (k % 4))
    place(s, camel_grumble(0.06, seed=5), 16.0, pan=0.4)
    place(s, crackle(8.0, amp=0.03, rate=6, seed=6), 13.0)
    steps(s, 22.4, 24.6, step=0.45, amp=0.03, seed=7)
    place(s, noise_bed(19.0, amp=0.015, lo=300, hi=2000, lfo=0.15, seed=8), 22.0)
    place(s, camel_grumble(0.04, seed=9), 33.8, pan=-0.5)
    steps(s, 39.8, 41.0, step=0.25, amp=0.03, seed=10, pan=0.3)
    # S4: the school: a breeze under the awning, children shifting, the laugh
    place(s, noise_bed(43.6, amp=0.015, lo=300, hi=2200, lfo=0.2, seed=11), 41.0)
    place(s, rustle(0.025, 0.8, seed=12), 41.6)
    place(s, rustle(0.02, 0.7, seed=13), 53.2)
    place(s, kids_laugh(2.2, 0.13, seed=14, voices=4), LAUGH)
    place(s, rustle(0.02, 0.7, seed=15), 74.0)
    place(s, gust(2.0, 0.03, seed=16), 80.0)
    # S5: the evening wind carries the talk; the tent; the lamp
    place(s, gust(3.2, 0.07, seed=17), 84.8)
    place(s, sand_hiss(3.0, 0.03, seed=18), 85.6)
    place(s, murmur(4.0, 0.03, seed=19), 85.0)
    crickets(s, 89.6, 108.2, amp=0.006, seed=20)
    place(s, crackle(18.6, amp=0.02, rate=5, seed=21), 89.6)
    steps(s, DOOR - 0.8, DOOR + 0.2, step=0.4, amp=0.04, seed=22, pan=0.4)
    place(s, rustle(0.04, 0.8, seed=23), DOOR - 0.2)
    # S6: the empty school; the camp at noon; the boys; the dunes at sunset
    place(s, noise_bed(7.4, amp=0.02, lo=300, hi=2200, lfo=0.2, seed=24), EMPTY)
    place(s, noise_bed(12.6, amp=0.02, lo=300, hi=2500, lfo=0.15, seed=25), 115.6)
    steps(s, 115.8, 121.4, step=0.5, amp=0.03, seed=26)
    place(s, murmur(3.0, 0.025, seed=27), 118.6)
    place(s, camel_grumble(0.05, seed=28), 119.8, pan=0.5)
    steps(s, 121.6, 128.0, step=0.22, amp=0.04, seed=29, pan=-0.2)
    place(s, kids_laugh(2.4, 0.11, seed=30, voices=3), 126.4)
    place(s, noise_bed(15.2, amp=0.03, lo=300, hi=2000, lfo=0.2, seed=31), 128.2)
    place(s, gust(3.0, 0.04, seed=32), 133.0)
    place(s, sand_hiss(4.0, 0.02, seed=33), 136.0)


LINES = [("p1s1a", 0.5), ("p1s1b", 4.7),
         ("p1s3a", 13.3), ("p1s3b", 19.6), ("p1s3c", 23.9), ("p1s3d", 28.6), ("p1s3e", 32.8), ("p1s3f", 35.9),
         ("p1s4a", 41.4), ("p1s4b", 45.6), ("p1s4c", 52.9), ("p1s4d", 56.8), ("p1s4d2", 56.85), ("p1s4d3", 56.9),
         ("p1s4e", 61.2), ("p1s4f", 64.0), ("p1s4g", 66.6), ("p1s4h", 70.2), ("p1s4i", 74.2), ("p1s4j", 78.8),
         ("p1s5a", 84.9), ("p1s5b", 89.9), ("p1s5c", 94.8), ("p1s5d", 98.0), ("p1s5e", 102.6),
         ("p1s6a", 109.8), ("p1s6b", 112.0), ("p1s6c", 116.6), ("p1s6d", 122.0), ("p1s6e", 124.8),
         ("p1s6f", 128.8), ("p1s6g", 132.6)]
if __name__ == "__main__":
    build(1, TOTAL, music, sfx, LINES, f'{AUDIO}/part01.wav')
    print('done')
