"""Part 5 · Zahhak's Dream — timing, music and sound.
Scene starts: s1 0 (hook: the warrior of the dream raises the ox-headed mace; Zahhak asleep), s2 7.6 (title: Damavand at night),
s3 12.2 (the bedchamber; the dream: three warriors out of the palace gate, the mace, the rope, the drag to Damavand; Arnavaz's advice),
s4 46.4 (the wise men in the hall; three silent days; the fourth day), s5 66.0 (Zirak's prophecy; Zahhak faints and falls from the
throne), s6 101.4 (the search; Fereydun is born; Abtin on the road at dusk; Faranak waits), end card 135.6, end 140.6"""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import series; series.from_folder(__file__)
from paths import AUDIO
from audio import *
from mix import build
from zsfx import *
from p01_audio import daf
TOTAL = 140.6
S = {"s1": 0.0, "s2": 7.6, "s3": 12.2, "s4": 46.4, "s5": 66.0, "s6": 101.4}
END_CARD = 135.6
FLASH = 27.9          # the mace comes down in the dream (white flash)
FAINT = 96.3          # Zahhak hits the floor
GUARDS = 130.0        # the guards step onto Abtin's road

LULLABY = [(0, 0), (2, 0.6), (4, 1.2), (3, 1.9), (2, 2.5), (0, 3.2)]


def shimmer(m, t0, amp=0.04, n=6):
    """a glint of metal in the dream: a few high bell notes"""
    for k in range(n):
        place(m, bell(1500 + 260 * k, 1.2, amp * (1 - k / (n + 1))), t0 + 0.06 * k, pan=0.3 - 0.12 * k)


def murmur(dur, amp=0.05, seed=0):
    """a crowd far away"""
    return noise_bed(dur, amp=amp, lo=250, hi=900, lfo=1.8, seed=seed)


def music(m):
    # S1 0-7.6: the dream warrior; Zahhak asleep
    place(m, drone(36.71, 7.9, amp=0.12, a=1.2, r=1.0), 0.0)
    place(m, pad([shur(1, -1), shur(5, -1), shur(1)], 3.6, amp=0.06, a=1.0, r=1.0, bright=6), 0.0)
    shimmer(m, 1.5, 0.035)
    place(m, pad([shur(0, -1), shur(3, -1)], 4.4, amp=0.05, a=1.0, r=1.0, bright=4), 3.4)
    heartbeat(m, 4.2, 7.4, bpm=84, amp=0.18)
    # S2 7.6-12.2: title over Damavand at night
    place(m, drum(dur=3.2, f0=40, amp=0.9, noise=0.4), 7.6)
    place(m, drone(36.71, 4.9, amp=0.12, a=0.1, r=1.4), 7.6)
    place(m, pad([shur(0), shur(4), shur(0, 1)], 4.8, amp=0.10, a=0.4, r=1.6, bright=6), 7.6)
    tanbur(m, ZTHEME, 8.0, amp=0.22, low=True, step=0.85)
    # S3 12.2-46.4: the bedchamber and the dream
    place(m, drone(55.0, 8.0, amp=0.06, a=1.5, r=1.0), 12.2)
    place(m, pad([shur(0, -1), shur(2, -1)], 7.6, amp=0.04, a=2.0, r=1.0, bright=4), 12.4)
    place(m, drone(36.71, 18.2, amp=0.12, a=1.0, r=1.5), 20.0)                    # the dream
    place(m, pad([shur(1, -1), shur(5, -1), shur(1)], 7.8, amp=0.06, a=1.5, r=1.0, bright=5), 20.0)
    for t in np.arange(20.4, 23.8, 0.85):                                           # the warriors' steps, like drums
        place(m, drum(dur=0.9, f0=48, amp=0.22, noise=0.15), t)
    shimmer(m, 24.6, 0.045)
    place(m, pad([shur(0), shur(3), shur(5)], 3.6, amp=0.05, a=1.5, r=0.4, bright=6), 24.2)
    place(m, drum(dur=3.0, f0=38, amp=1.0, noise=0.5), FLASH)
    place(m, pad([shur(1, -1), shur(5, -1), shur(1)], 3.0, amp=0.08, a=0.05, r=1.5, bright=6), FLASH)
    for i, t in enumerate(np.arange(31.8, 37.8, 0.75)):                            # the drag to Damavand
        place(m, drum(dur=0.8, f0=52, amp=0.2 + (0.08 if i % 4 == 0 else 0), noise=0.2), t)
    place(m, pad([shur(0, -1), shur(4, -1), shur(0)], 6.2, amp=0.07, a=1.0, r=1.5, bright=5), 31.8)
    tanbur(m, [(3, 0), (2, 0.6), (1, 1.2), (0, 2.0)], 34.0, amp=0.10, step=1.0)
    place(m, pad([shur(0, -1), shur(2, -1), shur(4, -1)], 8.4, amp=0.05, a=1.0, r=1.5, bright=4), 38.0)   # awake again
    tanbur(m, [(0, 0), (2, 0.7), (1, 1.4), (0, 2.1)], 42.4, amp=0.09)
    # S4 46.4-66.0: the wise men; three silent days; the fourth day
    place(m, drone(36.71, 19.4, amp=0.09, a=1.5, r=1.0), 46.4)
    place(m, pad([shur(1, -1), shur(0, -1)], 8.4, amp=0.05, a=2.0, r=1.0, bright=4), 46.6)
    for k, t in enumerate((58.6, 59.6, 60.6)):                                     # three days pass
        place(m, bell(196, 2.4, 0.05), t)
    place(m, drum(dur=2.4, f0=44, amp=0.8, noise=0.4), 61.4)
    place(m, pad([shur(1, -1), shur(5, -1), shur(1)], 4.0, amp=0.08, a=0.05, r=1.5, bright=6), 61.4)
    # S5 66.0-101.4: Zirak's prophecy; the faint
    place(m, pad([shur(0, -1), shur(4, -1)], 9.6, amp=0.05, a=2.0, r=1.0, bright=4), 66.0)
    tanbur(m, [(0, 0), (1, 0.6), (0, 1.2)], 66.6, amp=0.08)
    place(m, pad([shur(0), shur(4), shur(0, 1)], 9.0, amp=0.06, a=2.0, r=1.0, bright=6), 75.8)   # the prophecy: a brighter colour
    place(m, bell(587, 3.0, 0.04), 78.2); place(m, bell(880, 3.0, 0.03), 78.25)                     # "Fereydun"
    place(m, drone(36.71, 4.8, amp=0.10, a=0.6, r=1.0), 80.5)                                         # the dream again
    shimmer(m, 81.4, 0.035)
    place(m, pad([shur(1, -1), shur(5, -1)], 2.6, amp=0.06, a=0.3, r=1.0, bright=5), 85.1)
    place(m, drone(36.71, 9.0, amp=0.10, a=1.5, r=1.0), 87.7)
    place(m, pad([shur(1, -1), shur(0, -1), shur(4, -1)], 6.4, amp=0.05, a=2.0, r=1.0, bright=4), 88.0)
    place(m, drum(dur=3.0, f0=38, amp=0.95, noise=0.45), FAINT)
    place(m, pad([shur(1, -1), shur(5, -1), shur(1)], 2.6, amp=0.08, a=0.05, r=1.5, bright=6), FAINT)
    place(m, drone(36.71, 4.6, amp=0.08, a=0.5, r=1.5), 96.8)
    # S6 101.4-140.6: the search; the birth; the road; the end card
    place(m, drum(dur=2.0, f0=46, amp=0.6, noise=0.35), 101.6)
    for t in np.arange(104.6, 107.4, 0.5):                                          # the guards march out
        place(m, drum(dur=0.6, f0=56, amp=0.2, noise=0.2), t)
    place(m, pad([shur(1, -1), shur(0, -1)], 3.0, amp=0.04, a=1.0, r=1.0, bright=4), 107.4)
    place(m, pad([shur(0), shur(2), shur(4)], 10.0, amp=0.06, a=2.0, r=1.5, bright=5), 110.2)      # the baby
    tanbur(m, LULLABY, 110.8, amp=0.10, step=1.0)
    tanbur(m, LULLABY, 116.0, amp=0.09, step=1.05)
    place(m, pad([shur(0), shur(4), shur(0, 1)], 3.0, amp=0.05, a=1.0, r=1.5, bright=6), 118.4)
    place(m, drone(55.0, 10.0, amp=0.05, a=2.0, r=1.0), 120.9)                                       # Abtin in hiding; dusk
    place(m, pad([shur(0, -1), shur(2, -1), shur(4, -1)], 9.0, amp=0.05, a=2.0, r=1.0, bright=4), 121.2)
    tanbur(m, [(4, 0), (3, 0.7), (2, 1.4), (1, 2.1)], 123.0, amp=0.08, step=1.1)
    place(m, drum(dur=2.4, f0=42, amp=0.85, noise=0.4), GUARDS)
    place(m, pad([shur(1, -1), shur(5, -1), shur(1)], 2.0, amp=0.07, a=0.05, r=1.2, bright=6), GUARDS)
    place(m, drone(36.71, 4.2, amp=0.08, a=0.5, r=1.5), 131.8)
    tanbur(m, [(2, 0), (1, 0.9), (0, 1.8)], 132.4, amp=0.08, step=1.1)
    place(m, drum(dur=3.0, f0=40, amp=0.75, noise=0.4), END_CARD)
    place(m, drone(36.71, 5.0, amp=0.10, a=0.2, r=2.0), END_CARD)
    place(m, pad([shur(0), shur(4), shur(0, 1)], 5.0, amp=0.08, a=0.6, r=2.0, bright=5), END_CARD)
    tanbur(m, ZTHEME[:4], END_CARD + 0.6, amp=0.14, low=True, step=0.9)


def sfx(s):
    # S1: dream wind; the sleeping king
    place(s, gust(2.4, 0.08, seed=501), 0.2)
    place(s, noise_bed(3.4, amp=0.04, lo=300, hi=2400, lfo=0.4, seed=502), 0.0)
    crickets(s, 3.4, 7.6, amp=0.01, seed=51)
    place(s, hiss(1.2, 0.05, seed=51), 4.6, pan=-0.3); place(s, hiss(1.2, 0.05, seed=52), 5.8, pan=0.3)
    # S3: the bedchamber; the dream
    crickets(s, 12.2, 20.0, amp=0.01, seed=52)
    place(s, hiss(1.0, 0.04, seed=53), 17.6, pan=0.3)
    place(s, whoosh(1.8, 0.10, seed=51), 19.0)                                    # into the dream
    place(s, noise_bed(18.0, amp=0.05, lo=200, hi=1800, lfo=0.25, seed=503), 20.0)
    place(s, scrape(0.6, 0.05, seed=51), 25.6, pan=0.2)                           # the mace is raised
    place(s, whoosh(1.0, 0.16, seed=52), 26.9)
    place(s, thud(0.25, 60, seed=51), FLASH + 0.05)
    place(s, rustle(0.06, 1.0, seed=51), 28.8); place(s, creak(1.0, 0.06, seed=51), 29.6, pan=0.3)   # the rope
    steps(s, 31.8, 37.8, step=0.3, amp=0.03, seed=51, pan=0.2)
    place(s, murmur(6.0, 0.05, seed=504), 31.8)
    place(s, gust(2.0, 0.08, seed=505), 35.0)
    place(s, whoosh(1.6, 0.08, seed=53), 37.3)                                     # out of the dream
    crickets(s, 38.0, 46.4, amp=0.01, seed=53)
    place(s, hiss(1.0, 0.05, seed=54), 39.8, pan=-0.3)
    # S4: the hall; the wise men walk in; three days; the fourth day
    place(s, crackle(19.6, amp=0.06, rate=8, seed=506), 46.4)
    steps(s, 46.6, 50.6, step=0.36, amp=0.04, seed=52, pan=-0.3)
    steps(s, 46.8, 50.8, step=0.38, amp=0.04, seed=53, pan=0.3)
    place(s, hiss(1.2, 0.07, seed=55), 52.4, pan=-0.3); place(s, hiss(1.2, 0.07, seed=56), 53.8, pan=0.3)
    place(s, rustle(0.04, 0.8, seed=52), 56.2)
    place(s, hiss(1.4, 0.10, seed=57), 61.6, pan=-0.3); place(s, hiss(1.4, 0.10, seed=58), 61.9, pan=0.3)
    # S5: Zirak steps forward; the faint
    place(s, crackle(35.4, amp=0.05, rate=8, seed=507), 66.0)
    steps(s, 67.6, 70.2, step=0.5, amp=0.04, seed=54)
    place(s, whoosh(1.4, 0.08, seed=54), 80.2)
    place(s, hiss(1.2, 0.09, seed=59), 85.3, pan=-0.3); place(s, hiss(1.2, 0.08, seed=60), 86.2, pan=0.3)
    place(s, whoosh(1.4, 0.14, seed=55), 95.0)                                      # he falls
    place(s, thud(0.4, 55, seed=52), FAINT)
    place(s, murmur(4.0, 0.06, seed=508), 96.8)
    steps(s, 96.9, 99.6, step=0.22, amp=0.05, seed=55, pan=0.3)
    # S6: the guards go out; the night; the house; the road; the door
    place(s, crackle(3.2, amp=0.05, rate=8, seed=509), 101.4)
    place(s, hiss(1.0, 0.08, seed=61), 102.0, pan=0.3)
    steps(s, 104.6, 107.4, step=0.25, amp=0.06, seed=56, pan=-0.2)
    steps(s, 104.75, 107.4, step=0.25, amp=0.05, seed=57, pan=0.2)
    place(s, noise_bed(2.8, amp=0.04, lo=200, hi=1500, lfo=0.3, seed=510), 107.4)
    crickets(s, 107.4, 110.2, amp=0.012, seed=54)
    place(s, owl(0.035), 108.6, pan=0.4)
    place(s, crackle(10.7, amp=0.07, rate=10, seed=511), 110.2)
    place(s, noise_bed(6.5, amp=0.05, lo=200, hi=2200, lfo=0.3, seed=512), 120.9)   # dusk wind
    place(s, creak(1.2, 0.07, seed=52), 122.2, pan=0.3)
    steps(s, 124.6, 127.0, step=0.42, amp=0.04, seed=58)
    steps(s, 127.4, 129.9, step=0.42, amp=0.045, seed=59)
    place(s, noise_bed(4.4, amp=0.05, lo=200, hi=2200, lfo=0.3, seed=513), 127.4)
    steps(s, 129.6, 130.6, step=0.2, amp=0.06, seed=60, pan=0.5)
    for k, t in enumerate((130.1, 130.4)):
        place(s, bell(2600 + 300 * k, 0.4, 0.03), t, pan=0.5)
    crickets(s, 131.8, 140.6, amp=0.012, seed=55)
    place(s, noise_bed(8.8, amp=0.03, lo=200, hi=1500, lfo=0.2, seed=514), 131.8)


LINES = [("p5s1a", 0.6), ("p5s1b", 3.0),
         ("p5s3a", 12.5), ("p5s3b", 16.4), ("p5s3c", 20.3), ("p5s3d", 24.1), ("p5s3e", 28.5), ("p5s3f", 31.8), ("p5s3g", 35.9),
         ("p5s3h", 38.4), ("p5s3i", 42.1),
         ("p5s4a", 46.8), ("p5s4b", 51.8), ("p5s4c", 55.4), ("p5s4d", 61.5),
         ("p5s5a", 66.3), ("p5s5b", 71.3), ("p5s5c", 75.9), ("p5s5d", 80.7), ("p5s5e", 85.2), ("p5s5f", 87.9), ("p5s5g", 92.1),
         ("p5s5h", 96.9),
         ("p5s6a", 101.7), ("p5s6b", 104.9), ("p5s6c", 110.4), ("p5s6d", 115.9), ("p5s6e", 118.6), ("p5s6f", 121.1), ("p5s6g", 127.6),
         ("p5s6h", 130.2), ("p5s6i", 132.1)]
if __name__ == "__main__":
    build(5, TOTAL, music, sfx, LINES, f'{AUDIO}/part05.wav')
    print('done')
