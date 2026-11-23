"""Part 3 · Arash's Arrow — timing, music and sound.
Scene starts: s1 0 (hook: the arrow over a desert and over a wide river: "Over mountains, over deserts, over rivers… and no one knew where
it would fall."), s2 7.8 (title: the summit at sunrise), s3 12.4 (sunrise; the king and the general below; Arash: "All my strength… into
this one arrow"; the draw; the release; he becomes light and wind; the bow on the snow; the boy and his mother; Arash's mother),
s4 62.4 (the witnesses gallop after the arrow; the desert; the great river: the arrow strikes a walnut tree on the far bank),
s5 87.0 (Afrasiab's tent: "Then the river is the border… We are going home."; the tired soldier: "Home…"),
s6 112.0 (dawn: the tents are gone; bread in the fortress; Tirgan: water and coloured threads; "some say the arrow is still flying"),
end card 141.4, end 147.0"""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import series; series.from_folder(__file__)
from paths import AUDIO
from audio import *
from mix import build
from asfx import *

TOTAL = 147.0
S = {"s1": 0.0, "s2": 7.8, "s3": 12.4, "s4": 62.4, "s5": 87.0, "s6": 112.0}
END_CARD = 141.4
NOCK = 31.6                                        # he sets the arrow on the string (s3 D)
DRAW = (32.0, 36.4)                                # the draw, slow, to full strength
RELEASE = 37.6                                     # the string is let go (s3 E)
GLOW = 41.8                                        # the light begins to fill him (s3 G)
FADE = (43.0, 46.6)                                # he turns into light and wind
BOWFALL = 45.6                                     # the bow lands on the snow
HOOK_ARROW = (0.0, 3.8, 7.8)                       # the arrow crosses the desert (0-3.8) and the river (3.8-7.8)
GALLOP = (62.4, 67.6)                              # the witnesses ride (s4 A)
IMPACT = 76.0                                      # the arrow strikes the walnut tree (s4 C)
REIN = 80.4                                        # the witnesses rein in on the near bank (s4 E)
SPLASHES = (123.6, 124.5, 125.6, 126.4, 127.6, 128.6)   # water thrown at Tirgan (s6 C)


def music(m):
    # S1 0-7.8: the arrow over the world
    place(m, drone(36.71, 7.8, amp=0.08, a=0.3, r=1.0), 0.0)
    place(m, pad([shur(0), shur(4), shur(0, 1)], 7.4, amp=0.06, a=0.6, r=1.4, bright=6), 0.2)
    tanbur(m, ATHEME, 0.4, amp=0.13, step=0.8)
    for t in (0.4, 2.0, 3.8, 5.6):
        place(m, drum(dur=1.0, f0=52, amp=0.16, noise=0.2), t)
    # S2 7.8-12.4: title over the summit at sunrise
    place(m, drum(dur=3.2, f0=40, amp=0.9, noise=0.4), 7.8)
    place(m, drone(36.71, 4.9, amp=0.12, a=0.1, r=1.4), 7.8)
    place(m, pad([shur(0, -1), shur(4, -1), shur(0)], 4.8, amp=0.08, a=0.4, r=1.6, bright=5), 7.8)
    tanbur(m, ATHEME, 8.2, amp=0.2, low=True, step=0.55)
    # S3 12.4-62.4: the shot
    place(m, pad([shur(0), shur(2), shur(4)], 10.0, amp=0.05, a=2.0, r=1.5, bright=5), 12.4)           # sunrise
    place(m, drone(36.71, 18.8, amp=0.07, a=1.5, r=1.0), 12.4)
    tanbur(m, ATHEME[:5], 13.0, amp=0.1, step=0.9)
    tanbur(m, [(0, 0), (2, 0.6), (1, 1.2), (0, 1.8)], 23.4, amp=0.07, step=1.0)
    place(m, pad([shur(4), shur(0, 1), shur(2, 1)], 4.6, amp=0.04, a=1.5, r=1.0, bright=6), 26.4)
    heartbeat(m, NOCK - 0.4, DRAW[1] + 0.9, bpm=70, amp=0.08)                                          # the draw: the heart, the drums
    for i, t in enumerate(np.arange(DRAW[0], DRAW[1] + 0.6, 0.6)):
        place(m, drum(dur=0.9, f0=46, amp=0.12 + 0.05 * i, noise=0.25), t)
    place(m, drone(55.0, DRAW[1] - DRAW[0] + 1.2, amp=0.06, a=2.5, r=0.2), DRAW[0])
    place(m, pad([shur(0, -1), shur(4, -1), shur(0), shur(4)], DRAW[1] - DRAW[0] + 1.2, amp=0.06, a=3.5, r=0.15, bright=7), DRAW[0])
    place(m, drum(dur=3.4, f0=38, amp=1.0, noise=0.5), RELEASE)                                        # the release
    place(m, pad([shur(0), shur(4), shur(0, 1), shur(2, 1)], 4.0, amp=0.1, a=0.05, r=2.5, bright=7), RELEASE)
    tanbur(m, ATHEME, RELEASE + 0.3, amp=0.22, low=True, step=0.42)
    place(m, drone(36.71, 21.0, amp=0.07, a=2.0, r=2.5), GLOW)                                         # light and wind
    place(m, pad([shur(0), shur(4), shur(0, 1)], 10.6, amp=0.07, a=2.0, r=2.0, bright=7), GLOW)
    for k in range(6):
        place(m, bell(shur(7 - k, 1), 2.6, 0.03), FADE[0] + 0.5 * k)
    tanbur(m, [(4, 0), (3, 0.8), (2, 1.6), (1, 2.4), (0, 3.4)], 48.4, amp=0.07, step=1.0)
    place(m, pad([shur(0), shur(2), shur(4)], 9.6, amp=0.05, a=2.0, r=2.0, bright=4), 52.4)
    tanbur(m, ATHEME[:5], 58.9, amp=0.08, step=0.9)
    # S4 62.4-87.0: the flight
    for i, t in enumerate(np.arange(62.4, 72.2, 0.45)):
        place(m, drum(dur=0.6, f0=60 if i % 2 else 50, amp=0.16 + (0.06 if i % 4 == 0 else 0), noise=0.25), t)
    place(m, drone(36.71, 14.0, amp=0.08, a=0.5, r=1.0), 62.4)
    tanbur(m, ATHEME, 62.8, amp=0.14, low=True, step=0.5)
    tanbur(m, ATHEME, 67.8, amp=0.12, step=0.55, pan=0.4)
    place(m, pad([shur(0), shur(4), shur(0, 1)], 5.0, amp=0.06, a=1.0, r=1.5, bright=6), 72.2)
    tanbur(m, ATHEME[:5], 72.6, amp=0.1, step=0.7)
    place(m, drum(dur=2.6, f0=42, amp=0.8, noise=0.4), IMPACT)
    place(m, bell(shur(4, 1), 3.0, 0.05), IMPACT + 0.05)
    place(m, pad([shur(0), shur(4), shur(0, 1), shur(2, 1)], 10.6, amp=0.06, a=0.4, r=2.0, bright=6), IMPACT + 0.1)
    tanbur(m, [(0, 0), (2, 0.5), (4, 1.0), (5, 1.6), (4, 2.4)], 81.2, amp=0.1, step=1.0)
    # S5 87.0-112.0: Afrasiab's tent
    place(m, drone(36.71, 21.6, amp=0.08, a=1.0, r=1.0), 87.0)
    place(m, pad([shur(1, -1), shur(5, -1), shur(1)], 9.0, amp=0.04, a=1.5, r=1.2, bright=4), 87.0)
    for t in (91.6, 93.4, 95.2):
        place(m, drum(dur=1.0, f0=48, amp=0.14, noise=0.2), t)
    place(m, drum(dur=2.0, f0=44, amp=0.45, noise=0.3), 96.1)
    place(m, pad([shur(0), shur(2), shur(4)], 6.0, amp=0.05, a=1.5, r=2.0, bright=5), 102.4)
    place(m, drum(dur=2.4, f0=42, amp=0.55, noise=0.35), 105.7)
    place(m, pad([shur(0), shur(4), shur(0, 1)], 5.6, amp=0.07, a=0.8, r=2.5, bright=6), 108.6)       # "Home…"
    tanbur(m, [(0, 0), (1, 0.7), (2, 1.3), (1, 2.1), (0, 2.8)], 108.9, amp=0.08, step=1.0)
    # S6 112.0-147.0: peace; Tirgan; the arrow still flying; the end card
    place(m, pad([shur(0), shur(2), shur(4)], 11.0, amp=0.06, a=2.0, r=1.5, bright=5), 112.0)
    tanbur(m, ATHEME, 112.4, amp=0.1, step=0.9)
    tanbur(m, [(0, 0), (2, 0.5), (4, 1.0), (2, 1.5), (0, 2.0)], 117.8, amp=0.1, step=0.9)
    for i, t in enumerate(np.arange(123.0, 136.2, 0.4)):                                                 # Tirgan: a dance rhythm
        place(m, drum(dur=0.5, f0=70 if i % 2 else 58, amp=0.13 + (0.05 if i % 4 == 0 else 0), noise=0.3), t)
    tanbur(m, [(0, 0), (2, 0.25), (4, 0.5), (5, 0.75), (4, 1.0), (2, 1.25), (4, 1.5), (0, 2.0)], 123.2, amp=0.15, step=0.8)
    tanbur(m, [(4, 0), (5, 0.25), (7, 0.5), (5, 0.75), (4, 1.0), (2, 1.25), (0, 1.75)], 126.4, amp=0.14, step=0.8)
    place(m, pad([shur(0), shur(4), shur(0, 1)], 6.8, amp=0.05, a=1.0, r=1.5, bright=5), 129.6)
    tanbur(m, [(0, 0), (2, 0.6), (4, 1.2), (2, 2.0)], 130.2, amp=0.09, step=1.0)
    place(m, drone(36.71, 10.6, amp=0.08, a=1.5, r=2.0), 136.4)                                          # the arrow still flying
    place(m, pad([shur(0), shur(4), shur(0, 1), shur(2, 1)], 10.6, amp=0.07, a=1.5, r=2.5, bright=7), 136.4)
    tanbur(m, ATHEME, 136.9, amp=0.14, low=True, step=0.8)
    place(m, drum(dur=3.0, f0=40, amp=0.85, noise=0.4), END_CARD)
    place(m, drone(36.71, 5.6, amp=0.10, a=0.2, r=2.0), END_CARD)
    place(m, pad([shur(0), shur(4), shur(0, 1)], 5.4, amp=0.08, a=0.3, r=2.0, bright=6), END_CARD)
    tanbur(m, ATHEME[:5], END_CARD + 0.6, amp=0.12, step=0.7)


def sfx(s):
    # S1: the arrow's whistle over the desert, then over the water
    place(s, whistle(3.4, 0.05, f0=2600, f1=1900, seed=1), 0.2, pan=-0.2)
    place(s, noise_bed(3.8, amp=0.03, lo=300, hi=2400, lfo=0.3, seed=2), 0.0)
    place(s, whistle(3.6, 0.05, f0=2300, f1=1700, seed=3), 4.0, pan=0.2)
    place(s, river(4.0, 0.035, seed=4), 3.8)
    # S2
    place(s, gust(3.0, 0.05, seed=5), 8.0)
    # S3: wind on the summit; below, the armies; the draw; the release; the light; the boy
    place(s, noise_bed(10.2, amp=0.045, lo=300, hi=3000, lfo=0.35, seed=6), 12.4)
    for k, t in enumerate((12.6, 22.8, 27.0)):
        place(s, gust(3.2, 0.06, seed=10 + k), t)
    place(s, murmur(5.8, 0.03, seed=7), 16.8)
    place(s, snort(0.05, seed=8), 18.4, pan=0.5)
    place(s, noise_bed(15.0, amp=0.035, lo=300, hi=3000, lfo=0.35, seed=9), 22.6)
    place(s, rustle(0.03, 0.5, seed=13), NOCK - 0.1)
    place(s, scrape(0.4, 0.04, seed=14), NOCK + 0.15)
    place(s, creak(DRAW[1] - DRAW[0] + 0.6, 0.05, seed=15), DRAW[0])                                      # the bow bends
    place(s, creak(1.4, 0.06, seed=16), DRAW[1] - 0.6)
    place(s, twang(0.3, f0=86.0), RELEASE, pan=-0.1)
    place(s, whoosh(1.2, 0.1, seed=17), RELEASE - 0.9)
    place(s, whistle(3.2, 0.07, f0=3000, f1=1800, seed=18), RELEASE + 0.1, pan=0.4)
    place(s, gust(2.6, 0.09, seed=19), RELEASE + 0.2)
    shimmer(s, GLOW, 2.0, amp=0.02, seed=20, base=1320)
    place(s, noise_bed(FADE[1] - FADE[0] + 1.0, amp=0.04, lo=1500, hi=6000, lfo=0.3, seed=21), FADE[0])
    shimmer(s, FADE[0] + 0.8, 3.0, amp=0.025, seed=22, base=1760)
    for k, t in enumerate((FADE[0] + 0.6, FADE[0] + 2.4, 47.8, 50.4)):
        place(s, gust(3.0, 0.08, seed=23 + k), t)
    place(s, thud(0.05, f0=110, seed=27), BOWFALL)
    place(s, noise_bed(14.8, amp=0.045, lo=300, hi=3000, lfo=0.3, seed=28), 47.6)
    place(s, murmur(6.4, 0.02, seed=29), 52.4)
    place(s, gust(2.8, 0.07, seed=30), 57.0)
    place(s, gust(3.0, 0.08, seed=31), 59.0)
    # S4: the gallop; the desert wind; the river; the strike
    hooves(s, GALLOP[0], GALLOP[1], step=0.34, amp=0.09, pan=0.2, seed=32, gallop=True)
    hooves(s, GALLOP[0] + 0.12, GALLOP[1], step=0.36, amp=0.07, pan=-0.2, seed=33, gallop=True)
    place(s, neigh(0.05, seed=34), 66.6, pan=0.4)
    place(s, whistle(2.8, 0.04, f0=2400, f1=1900, seed=35), 63.4, pan=0.3)
    place(s, noise_bed(4.6, amp=0.04, lo=300, hi=2800, lfo=0.4, seed=36), 67.6)
    place(s, whistle(3.6, 0.05, f0=2500, f1=1800, seed=37), 68.0, pan=-0.2)
    place(s, river(14.8, 0.035, seed=38), 72.2)
    place(s, whistle(3.6, 0.05, f0=2200, f1=1300, seed=39), IMPACT - 3.6, pan=0.2)
    place(s, thunk(0.3, seed=40), IMPACT, pan=0.15)
    place(s, rustle(0.05, 1.2, seed=41), IMPACT + 0.05)
    place(s, thunk(0.12, seed=42), 77.6)
    place(s, rustle(0.04, 1.0, seed=43), 77.7)
    hooves(s, REIN - 0.6, REIN + 0.6, step=0.4, amp=0.07, pan=-0.2, seed=44, gallop=True)
    place(s, snort(0.07, seed=45), REIN + 0.8, pan=-0.3)
    place(s, neigh(0.05, seed=46), REIN + 1.2, pan=0.3)
    # S5: the tent at night; the camp
    place(s, crackle(21.6, amp=0.04, rate=6, seed=47), 87.0)
    steps(s, 87.4, 89.6, step=0.5, amp=0.035, seed=48, pan=-0.3)
    crickets(s, 108.6, 112.0, amp=0.007, seed=49)
    place(s, crackle(3.4, amp=0.1, rate=10, seed=50), 108.6)
    # S6: dawn birds; the yard; the stream at Tirgan; the wind and the arrow
    for k, t in enumerate((112.4, 112.9, 113.8, 115.0, 115.3, 117.2, 120.4, 121.8)):
        place(s, chirp(2900 + 350 * (k % 3), amp=0.035), t, pan=0.5 - 0.3 * (k % 3))
    place(s, murmur(6.2, 0.03, seed=51), 116.8)
    steps(s, 117.0, 118.2, step=0.22, amp=0.035, seed=52, pan=0.2)
    place(s, river(13.4, 0.03, seed=53), 123.0)
    for k, t in enumerate(SPLASHES):
        place(s, splash(0.08, seed=60 + k), t, pan=0.3 - 0.2 * (k % 3))
    for k, t in enumerate((123.9, 125.9, 127.9)):
        place(s, kids_laugh(1.6, 0.045, seed=70 + k), t, pan=0.2 - 0.2 * k)
    for k, t in enumerate((129.8, 131.4, 134.0)):
        place(s, chirp(3100 + 250 * k, amp=0.03), t, pan=0.4)
    place(s, gust(3.0, 0.07, seed=80), 135.0)
    place(s, noise_bed(10.6, amp=0.04, lo=300, hi=3000, lfo=0.3, seed=81), 136.4)
    place(s, whistle(4.0, 0.05, f0=2500, f1=2000, seed=82), 137.0, pan=0.3)
    place(s, gust(3.2, 0.06, seed=83), 140.8)


LINES = [("p3s1a", 0.2), ("p3s1b", 5.35),
         ("p3s3a", 12.8), ("p3s3b", 17.1), ("p3s3c", 19.9), ("p3s3d", 23.0), ("p3s3e", 26.5), ("p3s3f", 31.3), ("p3s3g", 34.9), ("p3s3h", 42.8),
         ("p3s3i", 48.2), ("p3s3j", 52.8), ("p3s3k", 54.8), ("p3s3l", 59.5),
         ("p3s4a", 62.9), ("p3s4b", 65.0), ("p3s4c", 68.0), ("p3s4d", 72.4), ("p3s4e", 80.8), ("p3s4f", 83.9),
         ("p3s5a", 87.3), ("p3s5b", 91.9), ("p3s5c", 96.1), ("p3s5d", 98.5), ("p3s5e", 102.6), ("p3s5f", 105.7), ("p3s5g", 109.6),
         ("p3s6a", 112.3), ("p3s6b", 117.9), ("p3s6c", 119.5), ("p3s6d", 123.3), ("p3s6e", 129.9), ("p3s6f", 132.6), ("p3s6g", 134.3),
         ("p3s6h", 137.0)]
if __name__ == "__main__":
    build(3, TOTAL, music, sfx, LINES, f'{AUDIO}/part03.wav')
    print('done')
