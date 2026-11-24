"""Part 3 · Nawfal — timing, music and sound.
Scene starts: s1 0 (hook: Nawfal on his horse before Leyli's tribe: "Give Leyli to Majnun… or we fight!"; her father: "Never!"; the
charge), s2 7.6 (title: Nawfal's riders on a dune at sunrise), s3 12.2 (Majnun among the gazelles; Nawfal comes hunting; "Tell me your
story"; "I swear it: Leyli will be yours!"; "For Leyli… I will wait"), s4 47.0 (Nawfal rides to Leyli's tribe; the demand; "Never! My
daughter is not for a madman!"; the battle; Majnun on a high dune), s5 68.6 (Majnun prays for Leyli's people; the warrior: "you pray for
them?"; "if they are hurt, my heart is hurt"; no one wins; Nawfal comes back with a bigger army and wins), s6 92.6 (Leyli's father in the
dust: "Kill her if you want… but I will never give my daughter to a madman"; Nawfal gives up; "you promised me!"; Majnun walks away),
s7 122.0 (Ibn Salam asks for Leyli's hand; "Then Leyli is yours"; Leyli hears, in her tent), end card 139.8, end 145.0"""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import series; series.from_folder(__file__)
from paths import AUDIO
from audio import *
from mix import build
from lsfx import *

TOTAL = 145.0
S = {"s1": 0.0, "s2": 7.6, "s3": 12.2, "s4": 47.0, "s5": 68.6, "s6": 92.6, "s7": 122.0}
END_CARD = 139.8
NEVER = 4.1             # the hook: "Never!"
CHARGE = 5.2            # the hook: the horn and the charge
RIDERS = 18.6           # Nawfal and his men come over the dune (s3)
SWEAR = 37.4            # "Then I will help you. I swear it…"
DEMAND = 51.2           # "Give Leyli to Majnun… or we fight!" (s4)
NEVER2 = 54.5
BATTLE1 = 58.4          # the first battle
DUNE = 64.6             # Majnun on the high dune, the battle far away
DUSK = 82.4             # that day no one won
BATTLE2 = 85.4          # the bigger army
FATHER = 92.6           # Leyli's father walks in the dust
KILL = 102.2            # "Kill her if you want…"
LEAVE = 117.5           # Majnun walks away
IBN = 122.0             # Ibn Salam's gifts
YOURS = 132.7           # "Then Leyli is yours, Ibn Salam."
TEAR = 136.4            # Leyli in her tent


def music(m):
    # S1 0-7.6: the hook: drums under the demand, a hit on "Never!", the charge
    place(m, drone(36.71, 4.4, amp=0.08, a=0.3, r=1.0), 0.0)
    for i, t in enumerate(np.arange(0.2, 3.9, 0.46)):
        place(m, drum(dur=0.7, f0=64 if i % 2 else 54, amp=0.16 + 0.01 * i, noise=0.25), t)
    place(m, drum(dur=2.0, f0=42, amp=0.7, noise=0.35), NEVER)
    place(m, pad([shur(1, -1), shur(5, -1), shur(1)], 1.6, amp=0.05, a=0.1, r=1.0, bright=4), NEVER)
    for i, t in enumerate(np.arange(CHARGE, 7.4, 0.2)):
        place(m, drum(dur=0.45, f0=70 if i % 2 else 58, amp=0.2 + 0.015 * i, noise=0.3), t)
    place(m, drone(36.71, 2.6, amp=0.09, a=0.1, r=0.8), CHARGE)
    # S2 7.6-12.2: title: the riders on the dune at sunrise
    place(m, drum(dur=2.8, f0=44, amp=0.75, noise=0.35), 7.6)
    place(m, drone(36.71, 4.9, amp=0.10, a=0.2, r=1.4), 7.6)
    place(m, pad([shur(0, -1), shur(4, -1), shur(0)], 4.8, amp=0.07, a=0.4, r=1.6, bright=5), 7.6)
    tanbur(m, [(0, 0), (2, 0.5), (4, 1.0), (3, 1.6), (2, 2.1), (0, 2.8)], 7.9, amp=0.2, low=True, step=0.6)
    ney(m, LTHEME, 8.2, amp=0.04, step=0.62)
    # S3 12.2-47.0: Majnun among the gazelles; Nawfal comes; the promise
    place(m, drone(36.71, 7.0, amp=0.06, a=1.0, r=1.2), 12.2)
    place(m, pad([shur(0), shur(2), shur(4)], 6.8, amp=0.04, a=1.5, r=1.5, bright=5), 12.2)
    ney(m, [(4, 0, 1.0), (3, 1.0, 0.6), (2, 1.6, 1.6), (1, 3.4, 0.8), (0, 4.2, 1.8)], 12.6, amp=0.045, step=0.95)
    tanbur(m, [(0, 0), (2, 0.4), (4, 0.8), (5, 1.3), (4, 1.9), (2, 2.4)], RIDERS, amp=0.12, low=True, step=0.7)     # Nawfal's theme
    place(m, drone(36.71, 11.6, amp=0.05, a=1.0, r=1.0), RIDERS)
    tanbur(m, [(0, 0), (1, 0.6), (0, 1.2)], 24.0, amp=0.06, step=0.9)
    place(m, pad([shur(1, -1), shur(5, -1)], 6.0, amp=0.035, a=1.2, r=1.2, bright=4), 30.4)
    ney(m, [(2, 0, 1.0), (1, 1.0, 0.6), (0, 1.6, 1.8)], 33.4, amp=0.045, step=0.85)
    place(m, drum(dur=2.0, f0=46, amp=0.45, noise=0.3), SWEAR)
    place(m, drone(36.71, 9.6, amp=0.07, a=0.4, r=1.6), SWEAR)
    place(m, pad([shur(0), shur(4), shur(0, 1)], 9.4, amp=0.05, a=0.8, r=2.0, bright=5), SWEAR)
    tanbur(m, [(0, 0), (2, 0.4), (4, 0.8), (5, 1.3), (7, 1.9), (5, 2.5)], SWEAR + 0.4, amp=0.13, low=True, step=0.65)
    ney(m, LTHEME, 43.4, amp=0.05, step=0.6)
    # S4 47.0-68.6: the ride; the demand; the refusal; the battle; Majnun on the dune
    place(m, drone(36.71, 11.4, amp=0.07, a=0.6, r=0.8), 47.0)
    for i, t in enumerate(np.arange(47.2, 50.9, 0.4)):
        place(m, drum(dur=0.6, f0=62 if i % 2 else 52, amp=0.18, noise=0.25), t)
    place(m, pad([shur(1, -1), shur(5, -1)], 7.0, amp=0.04, a=0.6, r=1.0, bright=4), DEMAND)
    place(m, drum(dur=2.2, f0=42, amp=0.7, noise=0.35), NEVER2)
    place(m, drum(dur=1.8, f0=46, amp=0.5, noise=0.3), 55.4)
    for i, t in enumerate(np.arange(BATTLE1, DUNE, 0.25)):
        place(m, drum(dur=0.5, f0=68 if i % 2 else 56, amp=0.2 + 0.006 * i, noise=0.3), t)
    place(m, drone(36.71, DUNE - BATTLE1 + 0.6, amp=0.09, a=0.3, r=0.6), BATTLE1)
    place(m, pad([shur(1, -1), shur(5, -1), shur(1)], DUNE - BATTLE1, amp=0.05, a=0.4, r=0.8, bright=4), BATTLE1)
    place(m, drone(36.71, 18.0, amp=0.06, a=1.0, r=1.4), DUNE)
    ney(m, [(4, 0, 1.4), (3, 1.4, 0.8), (2, 2.2, 1.6)], DUNE + 0.6, amp=0.045, step=0.9)
    # S5 68.6-92.6: the prayer; the warrior; no one wins; the bigger army
    place(m, pad([shur(0, -1), shur(4, -1), shur(0)], 13.4, amp=0.045, a=2.0, r=2.0, bright=5), 68.6)
    ney(m, LTHEME, 69.2, amp=0.05, step=0.85)
    place(m, drum(dur=1.4, f0=50, amp=0.35, noise=0.3), 74.0)
    ney(m, [(2, 0, 1.2), (1, 1.2, 0.8), (0, 2.0, 2.4)], 77.8, amp=0.05, step=0.95)
    shimmer(m, 79.6, 2.6, amp=0.018, seed=31)
    place(m, drone(36.71, 3.4, amp=0.06, a=0.6, r=1.4), DUSK)
    place(m, pad([shur(1, -1), shur(5, -1)], 3.0, amp=0.04, a=0.6, r=1.4, bright=4), DUSK)
    place(m, drum(dur=2.6, f0=44, amp=0.7, noise=0.35), BATTLE2)
    for i, t in enumerate(np.arange(BATTLE2 + 0.6, 91.8, 0.22)):
        place(m, drum(dur=0.45, f0=70 if i % 2 else 58, amp=0.2 + 0.006 * i, noise=0.3), t)
    place(m, drone(36.71, 7.4, amp=0.09, a=0.3, r=1.2), BATTLE2)
    tanbur(m, [(0, 0), (2, 0.4), (4, 0.8), (5, 1.3), (7, 1.9), (5, 2.5), (4, 2.9), (7, 3.6)], 88.0, amp=0.15, low=True, step=0.55)
    # S6 92.6-122.0: the father in the dust; Nawfal gives up; Majnun walks away
    place(m, drone(36.71, 9.8, amp=0.06, a=1.5, r=1.0), FATHER)
    place(m, pad([shur(1, -1), shur(5, -1), shur(1)], 9.4, amp=0.04, a=2.0, r=1.0, bright=4), FATHER)
    tanbur(m, [(2, 0), (1, 0.8), (0, 1.6)], FATHER + 0.6, amp=0.06, step=1.0)
    place(m, drum(dur=2.4, f0=40, amp=0.75, noise=0.4), KILL + 3.0)
    place(m, drone(36.71, 6.6, amp=0.08, a=0.2, r=2.0), KILL + 3.0)
    place(m, pad([shur(0), shur(2), shur(4)], 5.0, amp=0.04, a=1.0, r=1.6, bright=5), 109.0)
    heartbeat(m, 113.4, 117.2, bpm=84, amp=0.12)
    place(m, drone(36.71, 4.8, amp=0.06, a=0.6, r=1.6), LEAVE - 0.4)
    ney(m, LTHEME, LEAVE, amp=0.05, step=0.7)
    # S7 122.0-139.8: Ibn Salam; "Then Leyli is yours"; Leyli's tear; end card
    place(m, drone(36.71, 10.8, amp=0.05, a=1.0, r=1.0), IBN)
    tanbur(m, [(4, 0), (5, 0.4), (4, 0.8), (2, 1.2), (4, 1.8), (5, 2.2), (7, 2.6)], IBN + 0.4, amp=0.1, step=0.6)
    tanbur(m, [(2, 0), (4, 0.5), (2, 1.0), (0, 1.6)], 128.6, amp=0.07, step=0.8)
    place(m, drum(dur=2.4, f0=42, amp=0.6, noise=0.35), YOURS + 2.2)
    place(m, drone(36.71, 7.4, amp=0.07, a=0.3, r=1.6), YOURS + 2.2)
    place(m, pad([shur(1, -1), shur(5, -1), shur(1)], 5.0, amp=0.05, a=0.5, r=1.6, bright=4), TEAR)
    ney(m, [(4, 0, 1.0), (3, 1.0, 0.6), (2, 1.6, 1.8)], TEAR + 0.3, amp=0.05, step=0.8)
    place(m, drum(dur=3.0, f0=40, amp=0.85, noise=0.4), END_CARD)
    place(m, drone(36.71, 5.2, amp=0.09, a=0.2, r=2.0), END_CARD)
    place(m, pad([shur(1, -1), shur(5, -1), shur(1)], 5.0, amp=0.06, a=0.3, r=2.0, bright=5), END_CARD)
    tanbur(m, [(0, 0), (2, 0.5), (4, 1.0), (3, 1.6), (2, 2.1), (0, 2.8)], END_CARD + 0.5, amp=0.13, low=True, step=0.6)


def sfx(s):
    # S1: horses snorting, the restless army, the charge
    place(s, noise_bed(5.2, amp=0.03, lo=300, hi=2000, lfo=0.3, seed=301), 0.0)
    place(s, murmur(5.0, 0.03, seed=302), 0.0)
    place(s, snort(0.08, seed=303), 0.2, pan=0.3)
    place(s, neigh(0.06, seed=304), 3.4, pan=-0.4)
    place(s, horn(2.2, 0.12, seed=305), CHARGE)
    place(s, war_cry(2.2, 0.1, seed=306), CHARGE + 0.4)
    hooves(s, CHARGE + 0.2, 7.6, step=0.3, amp=0.08, pan=0.0, seed=307, gallop=True)
    # S2: wind at sunrise, horses walking on the dune
    place(s, noise_bed(4.6, amp=0.03, lo=300, hi=2000, lfo=0.2, seed=308), 7.6)
    hooves(s, 8.0, 12.0, step=0.5, amp=0.025, pan=0.2, seed=309)
    # S3: the desert by day (wind, sand, a few birds); horses arrive; a falcon's bells
    place(s, noise_bed(34.8, amp=0.022, lo=300, hi=2200, lfo=0.18, seed=310), 12.2)
    place(s, sand_hiss(3.0, 0.018, seed=311), 13.4)
    for k, t in enumerate((14.8, 15.0, 16.9)):
        place(s, chirp(3000 + 250 * k, amp=0.025), t, pan=0.4 - 0.3 * k)
    hooves(s, RIDERS, 23.0, step=0.5, amp=0.04, pan=0.3, seed=312)
    place(s, snort(0.07, seed=313), 23.2, pan=0.3)
    for k, t in enumerate(np.arange(20.0, 22.6, 0.35)):
        place(s, bell(2600 + 180 * (k % 3), 0.35, 0.01), t, pan=0.3)
    place(s, rustle(0.04, 0.8, seed=314), 30.2)
    place(s, sand_hiss(2.4, 0.015, seed=315), 41.2)
    # S4: the army rides; the demand before the tents; the first battle; the far battle from the dune
    hooves(s, 47.0, 50.9, step=0.3, amp=0.07, pan=0.0, seed=316, gallop=True)
    place(s, war_cry(1.6, 0.05, seed=317), 48.0)
    place(s, murmur(7.0, 0.03, seed=318), 50.9)
    place(s, snort(0.07, seed=319), 51.0, pan=0.4)
    place(s, horn(2.4, 0.12, seed=320), BATTLE1)
    place(s, war_cry(2.2, 0.1, seed=321), BATTLE1 + 0.3)
    battle(s, BATTLE1 + 0.4, DUNE, amp=0.75, seed=322)
    place(s, noise_bed(18.0, amp=0.02, lo=300, hi=2200, lfo=0.2, seed=323), DUNE)
    battle(s, DUNE, DUSK, amp=0.9, seed=324, far=True)
    # S5: the warrior's shout; dusk (wind, a lone horse); the second battle
    steps(s, 73.4, 74.2, step=0.2, amp=0.04, seed=325)
    place(s, noise_bed(3.4, amp=0.02, lo=300, hi=1800, lfo=0.15, seed=326), DUSK)
    place(s, neigh(0.04, seed=327), 83.4, pan=-0.5)
    place(s, horn(2.6, 0.13, seed=328), BATTLE2)
    place(s, war_cry(2.0, 0.1, seed=329), BATTLE2 + 0.2)
    battle(s, BATTLE2 + 0.5, 91.6, amp=0.85, seed=330)
    place(s, war_cry(1.8, 0.07, seed=331), 90.4)
    # S6: wind and dust; the old man's steps; Majnun walks away
    place(s, noise_bed(29.4, amp=0.024, lo=250, hi=1800, lfo=0.2, seed=332), FATHER)
    place(s, sand_hiss(4.0, 0.025, seed=333), FATHER + 0.4)
    steps(s, FATHER + 0.4, FATHER + 4.0, step=0.62, amp=0.03, seed=334)
    place(s, snort(0.05, seed=335), 108.4, pan=0.4)
    steps(s, LEAVE + 0.2, 121.6, step=0.55, amp=0.025, seed=336)
    place(s, gust(2.6, 0.05, seed=337), 119.0)
    # S7: Leyli's camp at dusk (a camel, the gifts set down, crickets); her tent at night
    place(s, camel_grumble(0.05, seed=338), IBN + 0.8, pan=-0.4)
    for t in (IBN + 2.6, IBN + 3.3):
        place(s, thud(0.1, f0=80, seed=int(t)), t, pan=0.2)
    place(s, murmur(4.0, 0.015, seed=339), IBN)
    place(s, noise_bed(14.4, amp=0.014, lo=300, hi=2000, lfo=0.15, seed=340), IBN)
    crickets(s, 128.0, END_CARD, amp=0.005, seed=341)
    place(s, rustle(0.025, 0.7, seed=342), TEAR + 0.2)


LINES = [("p3s1a", 0.5), ("p3s1b", NEVER),
         ("p3s3a", 12.6), ("p3s3b", 18.8), ("p3s3c", 23.4), ("p3s3d", 26.4), ("p3s3e", 30.8), ("p3s3f", 33.2), ("p3s3g", SWEAR),
         ("p3s3h", 41.0), ("p3s3i", 43.9),
         ("p3s4a", 47.4), ("p3s1a", DEMAND), ("p3s1b", NEVER2), ("p3s4b", 55.4), ("p3s4c", 59.6), ("p3s4d", 64.8),
         ("p3s5a", 69.0), ("p3s5b", 74.0), ("p3s5c", 77.5), ("p3s5d", 82.8), ("p3s5e", 86.4),
         ("p3s6a", 96.8), ("p3s6b", KILL), ("p3s6c", 109.0), ("p3s6d", 113.7), ("p3s6e", 116.0),
         ("p3s7a", 122.4), ("p3s7b", 128.4), ("p3s7c", YOURS)]
if __name__ == "__main__":
    build(3, TOTAL, music, sfx, LINES, f'{AUDIO}/part03.wav')
    print('done')
