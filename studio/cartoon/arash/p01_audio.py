"""Part 1 · The Siege — timing, music and sound.
Scene starts: s1 0 (hook: an arrow flies over the mountains at sunrise; "This is the arrow that drew a border…"), s2 7.8 (title: the
besieged fortress in Tabaristan at dawn), s3 12.4 (the long war; Afrasiab surrounds Manuchehr; no bread in the fortress; "Mother, I'm
hungry"), s4 36.4 (Manuchehr on the wall at night: "their fires are everywhere"; the council: "ask for peace"), s5 52.8 (Turan's camp: a
tired soldier; the messenger before Afrasiab; "now that he is hungry…"; the advisor; one arrow; "how far can one arrow fly?"), s6 85.2 (the
yard at dusk: "Who can shoot that arrow?"; silence; Arash steps forward; "His name was Arash."), end card 116.0, end 121.4"""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import series; series.from_folder(__file__)
from paths import AUDIO
from audio import *
from mix import build
from asfx import *

TOTAL = 121.4
S = {"s1": 0.0, "s2": 7.8, "s3": 12.4, "s4": 36.4, "s5": 52.8, "s6": 85.2}
END_CARD = 116.0
ARROW = 0.6             # the arrow flies across the sky (s1 A)
LAUGH = 82.4            # Afrasiab and his men laugh
STEP = 99.0             # Arash steps forward


def music(m):
    # S1 0-7.8: sunrise, the arrow
    place(m, drone(36.71, 8.0, amp=0.09, a=0.8, r=1.0), 0.0)
    place(m, pad([shur(0, -1), shur(4, -1), shur(0)], 7.6, amp=0.06, a=1.0, r=1.4, bright=5), 0.0)
    shimmer_t = [0.5, 0.9, 1.4, 2.0]
    for k, t in enumerate(shimmer_t):
        place(m, bell(880 * (1.5 if k % 2 else 1.0), 2.0, 0.03), t)
    tanbur(m, ATHEME[:5], 3.6, amp=0.12, step=0.8)
    # S2 7.8-12.4: title over the besieged fortress
    place(m, drum(dur=3.2, f0=40, amp=0.9, noise=0.4), 7.8)
    place(m, drone(36.71, 4.9, amp=0.12, a=0.1, r=1.4), 7.8)
    place(m, pad([shur(0, -1), shur(4, -1), shur(0)], 4.8, amp=0.08, a=0.4, r=1.6, bright=5), 7.8)
    tanbur(m, ATHEME, 8.2, amp=0.22, low=True, step=0.55)
    # S3 12.4-36.4: the war, the siege, hunger
    place(m, drone(36.71, 13.4, amp=0.08, a=1.0, r=1.0), 12.4)
    place(m, pad([shur(0), shur(2), shur(4)], 5.0, amp=0.05, a=1.0, r=1.0, bright=5), 12.4)
    for i, t in enumerate(np.arange(17.2, 25.6, 0.8)):                                      # Turan's camp: slow war drums
        place(m, drum(dur=1.0, f0=52 if i % 2 else 46, amp=0.22 + (0.06 if i % 4 == 0 else 0), noise=0.25), t)
    place(m, pad([shur(1, -1), shur(5, -1), shur(1)], 8.4, amp=0.05, a=1.0, r=1.2, bright=4), 17.2)
    place(m, drone(36.71, 10.8, amp=0.07, a=1.0, r=2.0), 25.8)                               # hunger
    tanbur(m, [(2, 0), (1, 0.8), (0, 1.6), (1, 2.8), (0, 3.6)], 26.2, amp=0.08, step=1.0)
    place(m, pad([shur(0), shur(2), shur(4)], 6.0, amp=0.04, a=1.0, r=2.0, bright=4), 30.2)
    place(m, bell(440, 3.0, 0.03), 34.6)
    # S4 36.4-52.8: night on the wall; the council
    place(m, drone(36.71, 16.4, amp=0.08, a=1.0, r=1.2), 36.4)
    place(m, pad([shur(1, -1), shur(5, -1)], 16.0, amp=0.04, a=1.5, r=1.2, bright=4), 36.4)
    tanbur(m, [(0, 0), (1, 0.6), (0, 1.2), (3, 1.9), (2, 2.6)], 37.0, amp=0.07, step=1.0)
    place(m, drum(dur=1.6, f0=48, amp=0.4, noise=0.3), 49.6)
    # S5 52.8-85.2: Turan's camp; Afrasiab
    place(m, drone(36.71, 4.6, amp=0.07, a=0.8, r=0.8), 52.8)
    place(m, drone(36.71, 27.8, amp=0.09, a=0.6, r=1.2), 57.4)
    place(m, pad([shur(1, -1), shur(5, -1), shur(1)], 8.0, amp=0.05, a=0.8, r=1.0, bright=4), 57.4)
    heartbeat(m, 65.6, 70.2, bpm=70, amp=0.10)
    place(m, drum(dur=2.0, f0=44, amp=0.6, noise=0.35), 70.5)                               # "Very well…"
    place(m, pad([shur(0, -1), shur(4, -1), shur(0)], 10.4, amp=0.07, a=0.6, r=1.2, bright=5), 70.5)
    for t in (74.2, 77.4):
        place(m, drum(dur=1.2, f0=50, amp=0.35, noise=0.3), t)
    place(m, drum(dur=2.6, f0=42, amp=0.8, noise=0.4), 81.0)
    tanbur(m, [(1, 0), (0, 0.4), (1, 0.8), (3, 1.2), (2, 1.6), (1, 2.0), (0, 2.6)], 81.6, amp=0.1, step=0.9)
    # S6 85.2-121.4: the question; silence; Arash
    place(m, drone(36.71, 8.0, amp=0.08, a=0.8, r=1.0), 85.2)
    place(m, pad([shur(0), shur(2), shur(4)], 8.0, amp=0.05, a=1.0, r=1.0, bright=5), 85.2)
    place(m, drone(36.71, 5.0, amp=0.05, a=0.5, r=1.5), 93.2)                                # silence: only a low hum
    place(m, drum(dur=2.4, f0=44, amp=0.6, noise=0.35), STEP)
    place(m, pad([shur(0), shur(4), shur(0, 1)], 17.0, amp=0.08, a=1.5, r=2.0, bright=6), STEP)
    tanbur(m, ATHEME, 102.8, amp=0.12, low=True, step=0.9)
    tanbur(m, ATHEME[:5], 108.2, amp=0.14, step=0.9)
    place(m, drum(dur=3.0, f0=40, amp=0.8, noise=0.4), 112.4)
    place(m, drum(dur=3.0, f0=40, amp=0.85, noise=0.4), END_CARD)
    place(m, drone(36.71, 5.4, amp=0.10, a=0.2, r=2.0), END_CARD)
    place(m, pad([shur(0), shur(4), shur(0, 1)], 5.2, amp=0.08, a=0.3, r=2.0, bright=6), END_CARD)
    tanbur(m, ATHEME, END_CARD + 0.6, amp=0.13, low=True, step=0.6)


def sfx(s):
    # S1: wind at sunrise; the arrow
    place(s, gust(3.0, 0.06, seed=1), 0.0)
    place(s, whistle(2.2, 0.07, seed=1), ARROW)
    place(s, gust(3.0, 0.05, seed=2), 4.4)
    place(s, whistle(1.8, 0.03, f0=2000, f1=1300, seed=2), 4.4)
    # S2
    place(s, gust(2.6, 0.06, seed=3), 8.0)
    # S3: wide valley; Turan's camp; the hungry yard
    place(s, noise_bed(4.8, amp=0.03, lo=300, hi=2000, lfo=0.2, seed=4), 12.4)
    for k, t in enumerate((13.2, 13.5, 15.1)):
        place(s, chirp(3000 + 300 * k, amp=0.03), t, pan=0.4)
    place(s, murmur(8.6, 0.05, seed=5), 17.2)
    hooves(s, 17.6, 24.8, step=0.45, amp=0.05, pan=0.3, seed=6)
    for t in (19.0, 22.6):
        place(s, neigh(0.05, seed=int(t)), t, pan=0.5)
    place(s, gust(4.0, 0.05, seed=7), 25.8)
    place(s, noise_bed(10.6, amp=0.02, lo=200, hi=1200, lfo=0.15, seed=8), 25.8)
    place(s, rustle(0.03, 0.6, seed=9), 32.0)
    # S4: night on the wall; the council room
    crickets(s, 36.4, 52.8, amp=0.008, seed=10)
    place(s, gust(3.0, 0.05, seed=11), 36.6)
    place(s, owl(0.03), 38.6, pan=-0.5)
    place(s, crackle(12.2, amp=0.05, rate=8, seed=12), 40.6)
    steps(s, 45.4, 46.4, step=0.4, amp=0.03, seed=13)
    # S5: Turan's camp at night; the tent
    crickets(s, 52.8, 57.4, amp=0.008, seed=14)
    place(s, crackle(4.6, amp=0.10, rate=14, seed=15), 52.8)
    place(s, crackle(27.8, amp=0.05, rate=8, seed=16), 57.4)
    steps(s, 57.4, 58.4, step=0.3, amp=0.04, seed=17, pan=-0.3)
    place(s, murmur(3.0, 0.04, seed=18), 81.0)
    place(s, laugh(2.8, 0.11, seed=19, voices=6), LAUGH)
    # S6: dusk in the yard; the silence; Arash
    place(s, murmur(4.6, 0.04, seed=20), 85.2)
    place(s, noise_bed(5.0, amp=0.03, lo=200, hi=1600, lfo=0.2, seed=21), 93.2)
    place(s, gust(3.0, 0.05, seed=22), 94.0)
    steps(s, STEP - 0.6, STEP + 1.6, step=0.5, amp=0.05, seed=23, pan=0.2)
    place(s, murmur(3.0, 0.035, seed=24), STEP + 0.4)
    place(s, gust(5.0, 0.05, seed=25), 108.0)


LINES = [("p1s1a", 0.4), ("p1s1b", 3.7),
         ("p1s3a", 12.6), ("p1s3b", 17.4), ("p1s3c", 22.6), ("p1s3d", 26.0), ("p1s3e", 30.5), ("p1s3f", 32.3),
         ("p1s4d", 36.8), ("p1s4a", 40.8), ("p1s4b", 45.6), ("p1s4c", 49.8),
         ("p1s5g", 53.1), ("p1s5a", 57.6), ("p1s5b", 61.8), ("p1s5h", 65.8), ("p1s5c", 70.6), ("p1s5d", 74.2), ("p1s5e", 77.4), ("p1s5f", 81.2),
         ("p1s6a", 85.5), ("p1s6b", 90.0), ("p1s6e", 94.6), ("p1s6c", 100.9), ("p1s6g", 102.8), ("p1s6h", 108.0), ("p1s6d", 110.2),
         ("p1s6f", 112.4)]
if __name__ == "__main__":
    build(1, TOTAL, music, sfx, LINES, f'{AUDIO}/part01.wav')
    print('done')
