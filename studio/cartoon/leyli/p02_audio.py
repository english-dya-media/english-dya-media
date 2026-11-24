"""Part 2 · The Proposal — timing, music and sound.
Scene starts: s1 0 (hook: Majnun at the door of the Kaaba at night: "God… take whatever is left of my life… and give it to Leyli"), s2 8.0
(title: a caravan on the dunes at dawn), s3 12.6 (years later: Majnun in the desert; the chief and the elder: "I will ask for her hand"),
s4 40.0 (Leyli's tribe at dusk: the gifts; "your son is mad"; "he is in love"; Leyli listens; "cure him first"), s5 71.0 (Mecca: the
Kaaba; "pray to be free of this love"; "make my love even greater"; the father knows there is no cure), s6 103.4 (Leyli's tribe before
the ruler: "stop him any way you can"; the messenger: "they want to kill your son!"; the father runs into the desert), end card 135.4,
end 140.6"""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import series; series.from_folder(__file__)
from paths import AUDIO
from audio import *
from mix import build
from lsfx import *

TOTAL = 140.6
S = {"s1": 0.0, "s2": 8.0, "s3": 12.6, "s4": 40.0, "s5": 71.0, "s6": 103.4}
END_CARD = 135.4
REFUSE = 66.4           # "Cure him first. Then we will talk."
PRAYER = 82.2           # Majnun at the door of the Kaaba
RULER = 112.3           # "Then stop him… any way you can."
RUN = 118.0             # the messenger runs in


def music(m):
    # S1 0-8.0: the Kaaba at night; the prayer (ney, a low drone)
    place(m, drone(36.71, 8.2, amp=0.07, a=1.0, r=1.6), 0.0)
    place(m, pad([shur(0, -1), shur(4, -1), shur(0)], 8.0, amp=0.05, a=1.5, r=1.6, bright=5), 0.0)
    ney(m, [(0, 0, 1.2), (2, 1.4, 1.0), (1, 2.6, 0.8), (0, 3.4, 2.0)], 0.4, amp=0.045, step=0.9)
    shimmer(m, 4.4, 2.6, amp=0.02, seed=1)
    # S2 8.0-12.6: title: the caravan at dawn
    place(m, drum(dur=2.8, f0=44, amp=0.7, noise=0.35), 8.0)
    place(m, drone(36.71, 4.9, amp=0.10, a=0.2, r=1.4), 8.0)
    place(m, pad([shur(0, -1), shur(4, -1), shur(0)], 4.8, amp=0.07, a=0.4, r=1.6, bright=5), 8.0)
    tanbur(m, [(0, 0), (2, 0.5), (4, 1.0), (3, 1.6), (2, 2.1), (0, 2.8)], 8.3, amp=0.2, low=True, step=0.6)
    ney(m, LTHEME, 8.6, amp=0.04, step=0.62)
    # S3 12.6-40.0: Majnun in the desert; the chief and the elder
    place(m, drone(36.71, 13.6, amp=0.06, a=1.0, r=1.2), 12.6)
    place(m, pad([shur(0), shur(2), shur(4)], 13.0, amp=0.04, a=1.5, r=1.5, bright=5), 12.6)
    ney(m, LTHEME, 13.2, amp=0.05, step=0.95)
    ney(m, [(4, 0, 1.0), (3, 1.0, 0.6), (2, 1.6, 1.6)], 19.6, amp=0.04, step=0.9)
    shimmer(m, 22.4, 2.4, amp=0.02, seed=2)
    place(m, drone(36.71, 13.6, amp=0.05, a=1.0, r=1.5), 26.6)
    tanbur(m, [(0, 0), (1, 0.6), (0, 1.2)], 27.0, amp=0.07, step=0.9)
    tanbur(m, [(2, 0), (3, 0.5), (4, 1.0), (2, 1.8)], 31.0, amp=0.08, step=0.9)
    tanbur(m, [(4, 0), (5, 0.5), (4, 1.0), (2, 1.6), (0, 2.4)], 36.4, amp=0.1, step=0.8)
    # S4 40.0-71.0: the gifts; the refusal (drums for the proud father)
    place(m, drone(36.71, 6.0, amp=0.06, a=0.8, r=1.0), 40.0)
    for i, t in enumerate(np.arange(40.2, 45.4, 0.65)):
        place(m, drum(dur=0.8, f0=70 if i % 2 else 60, amp=0.14, noise=0.15), t)
    tanbur(m, [(0, 0), (2, 0.4), (4, 0.8), (2, 1.4), (0, 2.0)], 40.6, amp=0.1, step=0.8)
    place(m, drone(36.71, 12.6, amp=0.05, a=1.0, r=1.0), 45.4)
    place(m, pad([shur(1, -1), shur(5, -1)], 12.0, amp=0.04, a=1.0, r=1.0, bright=4), 50.2)
    place(m, drum(dur=1.8, f0=46, amp=0.4, noise=0.3), 54.0)
    place(m, pad([shur(0), shur(2), shur(4)], 4.0, amp=0.04, a=0.8, r=1.0, bright=5), 58.4)
    ney(m, [(2, 0, 1.0), (1, 1.0, 0.6), (0, 1.6, 1.8)], 62.8, amp=0.05, step=0.85)
    place(m, drum(dur=2.2, f0=42, amp=0.6, noise=0.35), REFUSE)
    place(m, drone(36.71, 4.8, amp=0.08, a=0.2, r=2.0), REFUSE)
    place(m, pad([shur(1, -1), shur(5, -1), shur(1)], 4.6, amp=0.05, a=0.4, r=2.0, bright=4), REFUSE)
    # S5 71.0-103.4: Mecca; the prayer
    place(m, drone(36.71, 11.2, amp=0.06, a=1.2, r=1.0), 71.0)
    place(m, pad([shur(0, -1), shur(4, -1), shur(0)], 11.0, amp=0.04, a=1.5, r=1.2, bright=5), 71.0)
    tanbur(m, [(0, 0), (2, 0.8), (1, 1.6), (0, 2.4)], 71.4, amp=0.06, step=1.0)
    place(m, drone(36.71, 21.2, amp=0.07, a=1.5, r=2.0), PRAYER)
    place(m, pad([shur(0), shur(4), shur(0, 1)], 15.6, amp=0.05, a=2.5, r=2.5, bright=5), PRAYER)
    ney(m, LTHEME, PRAYER + 0.3, amp=0.045, step=1.1)
    shimmer(m, 87.8, 3.0, amp=0.02, seed=3)
    ney(m, [(4, 0, 1.4), (3, 1.4, 0.8), (2, 2.2, 1.2), (0, 3.4, 2.4)], 92.2, amp=0.055, step=0.95)
    place(m, bell(440, 3.0, 0.03), 97.8)
    ney(m, [(2, 0, 1.2), (1, 1.2, 1.0), (0, 2.2, 2.0)], 98.4, amp=0.04, step=0.9)
    # S6 103.4-140.6: the ruler; the messenger; the father runs; end card
    place(m, drone(36.71, 14.0, amp=0.07, a=0.8, r=1.0), 103.4)
    place(m, pad([shur(1, -1), shur(5, -1), shur(1)], 13.8, amp=0.05, a=1.0, r=1.0, bright=4), 103.4)
    for i, t in enumerate(np.arange(103.8, 111.8, 0.8)):
        place(m, drum(dur=1.0, f0=52 if i % 2 else 46, amp=0.18, noise=0.25), t)
    place(m, drum(dur=2.6, f0=40, amp=0.8, noise=0.4), RULER + 2.9)
    heartbeat(m, RUN - 0.6, 124.4, bpm=96, amp=0.12)
    place(m, drone(36.71, 11.0, amp=0.08, a=0.4, r=1.0), RUN)
    place(m, pad([shur(1, -1), shur(5, -1)], 11.0, amp=0.05, a=0.6, r=1.0, bright=4), RUN)
    for i, t in enumerate(np.arange(129.4, 135.2, 0.4)):            # the father hurries into the desert
        place(m, drum(dur=0.6, f0=60 if i % 2 else 50, amp=0.2 + 0.01 * i, noise=0.25), t)
    tanbur(m, [(0, 0), (1, 0.25), (2, 0.5), (3, 0.75), (4, 1.0), (3, 1.5), (2, 1.75), (1, 2.0)], 129.8, amp=0.11, step=0.6)
    place(m, drum(dur=3.0, f0=40, amp=0.85, noise=0.4), END_CARD)
    place(m, drone(36.71, 5.2, amp=0.09, a=0.2, r=2.0), END_CARD)
    place(m, pad([shur(1, -1), shur(5, -1), shur(1)], 5.0, amp=0.06, a=0.3, r=2.0, bright=5), END_CARD)
    tanbur(m, [(0, 0), (2, 0.5), (4, 1.0), (3, 1.6), (2, 2.1), (0, 2.8)], END_CARD + 0.5, amp=0.13, low=True, step=0.6)


def sfx(s):
    # S1: night at the Kaaba: a soft murmur of prayers, wind
    place(s, murmur(8.0, 0.025, seed=1), 0.0)
    place(s, noise_bed(8.0, amp=0.015, lo=300, hi=1800, lfo=0.15, seed=2), 0.0)
    # S2: the caravan at dawn: bells on the camels, wind
    place(s, noise_bed(4.6, amp=0.03, lo=300, hi=2000, lfo=0.2, seed=3), 8.0)
    for k, t in enumerate(np.arange(8.6, 12.4, 0.55)):
        place(s, bell(1600 + 200 * (k % 3), 0.5, 0.012), t, pan=0.3)
    # S3: the desert (wind, sand); the camp by day (birds, a camel)
    place(s, noise_bed(14.0, amp=0.03, lo=300, hi=2200, lfo=0.2, seed=4), 12.6)
    place(s, sand_hiss(3.0, 0.02, seed=5), 15.0)
    steps(s, 13.0, 21.8, step=0.55, amp=0.02, seed=6)
    place(s, noise_bed(13.4, amp=0.018, lo=300, hi=2500, lfo=0.15, seed=7), 26.6)
    for k, t in enumerate((27.4, 27.6, 31.2, 36.8, 37.0)):
        place(s, chirp(2900 + 300 * (k % 3), amp=0.03), t, pan=0.5 - 0.25 * (k % 4))
    place(s, camel_grumble(0.05, seed=8), 33.6, pan=0.5)
    # S4: Leyli's tribe at dusk: hooves, camels, the gifts set down; the tent
    hooves(s, 40.0, 44.6, step=0.5, amp=0.04, pan=0.3, seed=9)
    place(s, camel_grumble(0.06, seed=10), 41.6, pan=-0.4)
    for t in (42.8, 43.6):
        place(s, thud(0.12, f0=80, seed=int(t)), t, pan=0.2)
    place(s, murmur(5.0, 0.02, seed=11), 40.2)
    place(s, noise_bed(25.6, amp=0.016, lo=300, hi=2000, lfo=0.15, seed=12), 45.4)
    crickets(s, 58.0, 71.0, amp=0.005, seed=13)
    place(s, rustle(0.03, 0.8, seed=14), 62.8)
    # S5: Mecca at night: the murmur of pilgrims, steps on marble
    place(s, murmur(32.0, 0.025, seed=15), 71.0)
    steps(s, 71.2, 75.2, step=0.5, amp=0.025, seed=16)
    place(s, noise_bed(32.0, amp=0.012, lo=300, hi=1600, lfo=0.1, seed=17), 71.0)
    # S6: the court (torches); the camp at dusk; running feet; the desert
    place(s, crackle(14.0, amp=0.04, rate=8, seed=18), 103.4)
    place(s, murmur(8.0, 0.02, seed=19), 103.6)
    steps(s, RUN - 1.0, RUN + 1.6, step=0.22, amp=0.05, seed=20, pan=0.3)
    place(s, noise_bed(11.0, amp=0.02, lo=300, hi=2000, lfo=0.2, seed=21), RUN)
    steps(s, 129.6, 135.2, step=0.3, amp=0.04, seed=22)
    place(s, gust(3.0, 0.05, seed=23), 130.4)
    place(s, sand_hiss(4.0, 0.03, seed=24), 132.0)


LINES = [("p2s1a", 0.4), ("p2s1b", 4.1),
         ("p2s3a", 12.9), ("p2s3b", 17.8), ("p2s3c", 22.5), ("p2s3d", 26.9), ("p2s3e", 30.4), ("p2s3f", 35.9),
         ("p2s4a", 40.3), ("p2s4b", 45.6), ("p2s4c", 50.4), ("p2s4d", 54.0), ("p2s4e", 58.6), ("p2s4f", 66.4),
         ("p2s5a", 71.3), ("p2s5b", 75.6), ("p2s5c", 82.4), ("p2s5d", 87.8), ("p2s1a", 92.3), ("p2s1b", 95.8), ("p2s5f", 98.0),
         ("p2s6a", 103.7), ("p2s6b", 109.0), ("p2s6c", 112.3), ("p2s6d", 118.4), ("p2s6e", 124.8)]
if __name__ == "__main__":
    build(2, TOTAL, music, sfx, LINES, f'{AUDIO}/part02.wav')
    print('done')
