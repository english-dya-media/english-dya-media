"""Part 2 · The Bow — timing, music and sound.
Scene starts: s1 0 (hook: sparks at the anvil, "a bow like no other"; Arash on the summit as a dark shape, "and a man like no other"), s2 7.8
(title: the besieged fortress at night), s3 12.4 (the king can't sleep; a green light; Spandarmad: the oldest tree, an eagle's feathers, the
finest iron; "He has already stepped forward"), s4 48.4 (the craftsmen: the old tree, the eagle's feather, the smith, the finished bow),
s5 72.0 (the bow is given to Arash: why he will do it), s6 89.8 (his mother), s7 105.6 (before dawn: a light climbs the mountain; both
armies wait below; the witnesses of Turan; the boy and his mother), s8 124.8 (the summit: the wind takes his cloak; "Look at me…"),
end card 144.8, end 150.0"""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import series; series.from_folder(__file__)
from paths import AUDIO
from audio import *
from mix import build
from asfx import *

TOTAL = 150.0
S = {"s1": 0.0, "s2": 7.8, "s3": 12.4, "s4": 48.4, "s5": 72.0, "s6": 89.8, "s7": 105.6, "s8": 124.8}
END_CARD = 144.8
HOOK_STRIKES = (0.5, 1.2, 1.9, 2.9, 3.6)          # hammer blows in s1 A (shot time = part time)
GREEN = 20.9                                       # the green light begins (s3 C)
APPEAR = 23.6                                      # Spandarmad appears (s3 D)
VANISH = 46.2                                      # she fades away (s3 I)
EAGLE = 57.5                                       # the eagle's cry (s4 C)
CATCH = 62.0                                       # the feather lands in the bowyer's hand (s4 D)
FORGE_STRIKES = (63.35, 63.85, 67.1)                # s4 E (the smith's blows, part time)
PLUCK = 67.9                                       # the bowyer plucks the new string (s4 F)
ENTER = 72.2                                       # Arash comes in (s5 A)
DOOR = 90.6                                        # the door of his mother's house (s6 A)
CLOAK = 130.2                                      # the wind takes his cloak (s8 B)


def music(m):
    # S1 0-7.8: the forge in the dark; the man on the summit
    place(m, drone(36.71, 7.8, amp=0.09, a=0.4, r=1.0), 0.0)
    for t in HOOK_STRIKES:
        place(m, drum(dur=0.8, f0=50, amp=0.18, noise=0.2), t)
    place(m, pad([shur(0, -1), shur(4, -1), shur(0)], 3.8, amp=0.06, a=0.6, r=1.4, bright=5), 4.2)
    tanbur(m, ATHEME[:5], 4.6, amp=0.13, step=0.7)
    # S2 7.8-12.4: title over the fortress at night
    place(m, drum(dur=3.2, f0=40, amp=0.9, noise=0.4), 7.8)
    place(m, drone(36.71, 4.9, amp=0.12, a=0.1, r=1.4), 7.8)
    place(m, pad([shur(0, -1), shur(4, -1), shur(0)], 4.8, amp=0.08, a=0.4, r=1.6, bright=5), 7.8)
    tanbur(m, ATHEME, 8.2, amp=0.2, low=True, step=0.55)
    # S3 12.4-48.4: night; the green light; Spandarmad
    place(m, drone(36.71, 8.6, amp=0.07, a=1.0, r=1.2), 12.4)
    place(m, pad([shur(1, -1), shur(5, -1)], 8.4, amp=0.04, a=1.5, r=1.2, bright=4), 12.4)
    tanbur(m, [(0, 0), (1, 0.6), (0, 1.2), (3, 1.9), (2, 2.6)], 13.0, amp=0.07, step=1.0)
    place(m, pad([shur(4), shur(0, 1), shur(2, 1)], 3.2, amp=0.05, a=2.6, r=0.6, bright=7), GREEN)          # the light grows
    place(m, pad([shur(0), shur(4), shur(0, 1), shur(2, 1)], 23.0, amp=0.07, a=1.2, r=2.0, bright=7), APPEAR)
    place(m, drone(73.42, 23.0, amp=0.05, a=1.5, r=2.0), APPEAR)
    for k, t in enumerate((APPEAR, 28.0, 31.8, 35.0, 37.6, 41.6)):
        place(m, bell(shur(4 + k % 3, 1), 3.0, 0.03), t + 0.1)
    place(m, pad([shur(2), shur(4), shur(0, 1)], 3.0, amp=0.05, a=0.3, r=2.5, bright=6), VANISH)
    for k in range(5):
        place(m, bell(shur(7 - k, 1), 2.2, 0.025), VANISH + 0.25 * k)
    # S4 48.4-72.0: the craftsmen
    place(m, pad([shur(0), shur(2), shur(4)], 8.6, amp=0.05, a=1.2, r=1.5, bright=5), 48.4)
    tanbur(m, ATHEME, 49.0, amp=0.1, step=0.9)
    place(m, pad([shur(0), shur(4), shur(0, 1)], 6.2, amp=0.06, a=1.2, r=1.5, bright=6), 57.0)
    tanbur(m, ATHEME[:5], 57.4, amp=0.08, step=0.7, pan=0.4)
    place(m, bell(shur(4, 1), 2.4, 0.04), CATCH)
    place(m, drone(36.71, 8.8, amp=0.08, a=0.6, r=1.2), 63.2)
    place(m, pad([shur(1, -1), shur(5, -1), shur(1)], 4.2, amp=0.04, a=0.8, r=1.0, bright=4), 63.2)
    place(m, pad([shur(0), shur(4), shur(0, 1)], 4.6, amp=0.06, a=0.8, r=1.6, bright=5), 67.4)
    place(m, drum(dur=1.6, f0=46, amp=0.4, noise=0.3), 71.0)
    # S5 72.0-89.8: the bow and the king
    place(m, drone(36.71, 17.8, amp=0.07, a=1.0, r=1.5), 72.0)
    place(m, pad([shur(0), shur(2), shur(4)], 9.0, amp=0.04, a=1.5, r=1.5, bright=4), 72.0)
    tanbur(m, [(0, 0), (2, 0.6), (1, 1.2), (0, 1.8)], 73.0, amp=0.08, step=1.0)
    tanbur(m, [(4, 0), (3, 0.7), (2, 1.3), (1, 2.0), (0, 2.8)], 79.4, amp=0.07, step=1.0)
    place(m, drum(dur=2.4, f0=44, amp=0.6, noise=0.35), 86.6)
    place(m, pad([shur(0), shur(4), shur(0, 1)], 3.4, amp=0.08, a=0.6, r=1.8, bright=6), 86.6)
    # S6 89.8-105.6: the mother
    place(m, drone(73.42, 15.8, amp=0.05, a=2.0, r=2.0), 89.8)
    place(m, pad([shur(0), shur(2), shur(4)], 15.0, amp=0.05, a=2.0, r=2.5, bright=4), 90.4)
    tanbur(m, [(0, 0), (1, 0.7), (2, 1.3), (1, 2.1), (0, 2.8)], 94.6, amp=0.07, step=1.0)
    tanbur(m, [(4, 0), (2, 0.8), (1, 1.6), (0, 2.6)], 100.0, amp=0.08, step=1.0)
    # S7 105.6-124.8: before dawn
    place(m, drone(36.71, 19.2, amp=0.08, a=1.0, r=1.2), 105.6)
    place(m, pad([shur(1, -1), shur(5, -1), shur(1)], 9.0, amp=0.04, a=1.5, r=1.2, bright=4), 105.6)
    for i, t in enumerate(np.arange(109.8, 120.0, 1.2)):
        place(m, drum(dur=1.0, f0=48 if i % 2 else 44, amp=0.16 + (0.05 if i % 4 == 0 else 0), noise=0.25), t)
    heartbeat(m, 120.2, 124.6, bpm=66, amp=0.09)
    place(m, pad([shur(0), shur(2), shur(4)], 4.6, amp=0.04, a=1.0, r=1.5, bright=4), 120.2)
    # S8 124.8-150.0: the summit
    place(m, drone(36.71, 20.0, amp=0.09, a=1.5, r=1.0), 124.8)
    place(m, pad([shur(0, -1), shur(4, -1), shur(0)], 7.4, amp=0.05, a=2.0, r=1.0, bright=5), 124.8)
    tanbur(m, ATHEME[:5], 125.6, amp=0.1, step=0.9, low=True)
    place(m, drum(dur=2.2, f0=44, amp=0.55, noise=0.35), CLOAK)
    place(m, pad([shur(0), shur(4), shur(0, 1)], 12.0, amp=0.07, a=0.8, r=1.5, bright=6), 132.2)
    place(m, drum(dur=2.6, f0=42, amp=0.7, noise=0.4), 132.3)
    place(m, drone(36.71, 4.0, amp=0.05, a=0.5, r=1.5), 139.6)                                # "After this shot…": only a hum
    tanbur(m, ATHEME, 143.0, amp=0.12, low=True, step=0.8)
    place(m, drum(dur=3.0, f0=40, amp=0.85, noise=0.4), END_CARD)
    place(m, drone(36.71, 5.2, amp=0.10, a=0.2, r=2.0), END_CARD)
    place(m, pad([shur(0), shur(4), shur(0, 1)], 5.0, amp=0.08, a=0.3, r=2.0, bright=6), END_CARD)


def sfx(s):
    # S1: the anvil in the dark; wind on the summit
    place(s, crackle(4.2, amp=0.08, rate=10, seed=1), 0.0)
    for k, t in enumerate(HOOK_STRIKES):
        place(s, clang(0.11, seed=k), t, pan=0.1)
    place(s, gust(3.6, 0.07, seed=2), 4.2)
    place(s, noise_bed(3.6, amp=0.03, lo=300, hi=2400, lfo=0.3, seed=3), 4.2)
    # S2
    place(s, gust(2.6, 0.05, seed=4), 8.0)
    crickets(s, 8.0, 12.4, amp=0.006, seed=5)
    # S3: night in the council room; the light; her voice
    crickets(s, 12.4, GREEN + 0.6, amp=0.008, seed=6)
    place(s, crackle(GREEN - 12.4, amp=0.04, rate=6, seed=7), 12.4)
    steps(s, 13.0, 15.0, step=0.7, amp=0.025, seed=8)
    place(s, owl(0.025), 19.0, pan=-0.6)
    shimmer(s, GREEN, 2.8, amp=0.02, seed=9)
    place(s, gust(1.6, 0.04, seed=10), GREEN + 0.4)
    shimmer(s, APPEAR, 1.6, amp=0.03, seed=11, base=1320)
    place(s, noise_bed(VANISH - APPEAR, amp=0.012, lo=1500, hi=6000, lfo=0.3, seed=12), APPEAR)
    shimmer(s, VANISH, 1.6, amp=0.025, seed=13, base=1760)
    place(s, crackle(2.0, amp=0.04, rate=6, seed=14), VANISH + 0.2)
    # S4: the forest; the eagle; the forge; the finished bow
    place(s, noise_bed(8.6, amp=0.03, lo=400, hi=2600, lfo=0.25, seed=15), 48.4)
    for k, t in enumerate((48.9, 49.3, 50.6, 52.2, 52.4, 55.0, 56.2)):
        place(s, chirp(2900 + 350 * (k % 3), amp=0.035), t, pan=0.5 - 0.3 * (k % 3))
    steps(s, 48.8, 52.8, step=0.55, amp=0.03, seed=16, pan=0.2)
    place(s, rustle(0.03, 0.8, seed=17), 54.4)
    place(s, gust(4.0, 0.05, seed=18), 57.0)
    place(s, eagle_cry(0.05, seed=19), EAGLE, pan=-0.3)
    place(s, eagle_cry(0.03, seed=20), EAGLE + 2.2, pan=0.3)
    place(s, crackle(8.8, amp=0.09, rate=12, seed=21), 63.2)
    for k, t in enumerate(FORGE_STRIKES):
        place(s, clang(0.12, seed=30 + k), t, pan=0.15)
    place(s, creak(0.9, 0.05, seed=22), PLUCK - 1.0)
    place(s, twang(0.22), PLUCK, pan=-0.1)
    # S5: the council room
    place(s, crackle(17.8, amp=0.04, rate=6, seed=23), 72.0)
    steps(s, ENTER, ENTER + 1.6, step=0.5, amp=0.04, seed=24, pan=0.3)
    place(s, scrape(0.5, 0.05, seed=25), 76.2)
    # S6: the mother's house
    place(s, crackle(15.8, amp=0.10, rate=10, seed=26), 89.8)
    place(s, creak(1.4, 0.07, seed=27), DOOR)
    steps(s, DOOR + 0.8, DOOR + 2.6, step=0.5, amp=0.035, seed=28, pan=0.3)
    place(s, rustle(0.03, 0.7, seed=29), 103.1)
    # S7: night wind; the waiting armies; horses
    place(s, gust(4.0, 0.05, seed=31), 105.8)
    place(s, noise_bed(19.0, amp=0.025, lo=200, hi=1600, lfo=0.15, seed=32), 105.8)
    crickets(s, 105.6, 112.0, amp=0.006, seed=33)
    place(s, murmur(6.0, 0.035, seed=34), 109.8)
    place(s, crackle(15.0, amp=0.05, rate=8, seed=35), 109.8)
    for t in (114.2, 118.6):
        place(s, snort(0.07, seed=int(t)), t, pan=0.4)
    place(s, neigh(0.04, seed=36), 117.0, pan=0.5)
    # S8: the summit: wind and snow; the cloak
    place(s, noise_bed(20.0, amp=0.05, lo=300, hi=3000, lfo=0.35, seed=37), 124.8)
    for k, t in enumerate((125.0, 128.0, 133.4, 138.0, 141.6, 145.4)):
        place(s, gust(3.2, 0.06, seed=40 + k), t)
    steps(s, 125.2, 128.4, step=0.55, amp=0.04, seed=38, pan=0.2)
    place(s, flap(0.12, seed=39), CLOAK + 0.1)
    place(s, whoosh(1.6, 0.08, seed=41), CLOAK - 0.6)


LINES = [("p2s1a", 0.3), ("p2s1b", 5.2),
         ("p2s3a", 12.7), ("p2s3b", 17.2), ("p2s3c", 22.2), ("p2s3d", 24.5), ("p2s3e", 28.2), ("p2s3f", 32.0), ("p2s3g", 35.1), ("p2s3h", 37.8),
         ("p2s3i", 41.8), ("p2s3j", 44.0),
         ("p2s4a", 48.7), ("p2s4b", 54.1), ("p2s4c", 64.3), ("p2s4d", 68.5),
         ("p2s5a", 72.8), ("p2s5b", 76.0), ("p2s5c", 79.3), ("p2s5d", 83.1), ("p2s5e", 86.7),
         ("p2s6a", 92.3), ("p2s6b", 94.2), ("p2s6c", 97.5), ("p2s6d", 100.3),
         ("p2s7a", 106.0), ("p2s7b", 110.0), ("p2s7c", 113.7), ("p2s7d", 116.2), ("p2s7e", 120.3), ("p2s7f", 122.5),
         ("p2s8a", 132.4), ("p2s8b", 136.1), ("p2s8c", 139.9)]
if __name__ == "__main__":
    build(2, TOTAL, music, sfx, LINES, f'{AUDIO}/part02.wav')
    print('done')
