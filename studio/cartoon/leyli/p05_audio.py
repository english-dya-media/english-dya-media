"""Part 5 · The Father — timing, music and sound.
Scene starts: s1 0 (hook: Majnun at his father's grave at dusk: "Father… forgive me." "I never came home."), s2 6.8 (title: the old
chief walks alone over the dunes at sunrise), s3 11.4 (the father finds Majnun among the gazelles: "Qays… my son!"; "Come home with me…
I don't have much time"; "I am not Qays anymore… my heart went with Leyli"; the purse "for bread"; "Goodbye, my son…"; he walks away),
s4 58.6 (the chief's empty seat at the tent at dusk, the lamp goes out: "A few days later… he died"; the tribe round his new grave at
sunset), s5 70.8 (a young man of the tribe brings Majnun the news; Majnun at the grave: "Father… forgive me"; "You looked for me
everywhere…"; the stars come out), s6 103.0 (the hunter and the gazelle in his trap: "Wait! Please… don't hurt her!"; the gold; "Look at
her eyes"; set free, she stays; the animals are his family), s7 137.8 (an old man comes over the dunes: "I have a letter for you… from
Leyli."), end card 151.2, end 156.4"""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import series; series.from_folder(__file__)
from paths import AUDIO
from audio import *
from mix import build
from lsfx import *

TOTAL = 156.4
S = {"s1": 0.0, "s2": 6.8, "s3": 11.4, "s4": 58.6, "s5": 70.8, "s6": 103.0, "s7": 137.8}
END_CARD = 151.2
FOUND = 18.6            # the father: "Qays… my son!"
PLEA = 30.7             # "Come home with me. I am old…"
NOT_QAYS = 35.9         # Majnun: "Father, I love you. But I am not Qays anymore."
PURSE = 43.2            # "Then take this, at least… for bread."
GOODBYE = 47.7          # "Goodbye, my son. I don't think we will meet again."
LEAVES = 52.3           # "Goodbye… Father." — the old man walks away
SEAT = 58.6             # the empty seat
LAMP_OUT = 63.4         # the lamp goes out
FUNERAL = 64.8          # the tribe round the new grave at sunset
RUNNER = 70.8           # the young man runs to Majnun
NEWS = 73.8             # "Majnun… your father has died."
GRAVE = 82.6            # Majnun at the grave
STARS = 96.8            # night falls on the grave
HUNTER = 103.0          # the hunter and the gazelle
GOLD = 115.0            # "Then take this gold…"
EYES = 120.8            # "Look at her eyes…"
FREE = 124.6            # the rope comes off
FAMILY = 131.0          # the animals are his family
OLD_MAN = 137.8         # an old man comes over the dunes
LETTER = 143.1          # "Are you Majnun? I have a letter for you…"
FROM_LEYLI = 146.5      # "…from Leyli."


def coins(m, t, amp=0.03, seed=0, n=7):
    """a purse of gold coins: a short bright jingle"""
    r = np.random.default_rng(seed)
    for k in range(n):
        place(m, bell(r.uniform(2600, 4200), 0.35, amp * r.uniform(0.5, 1.0)), t + r.uniform(0, 0.25), pan=r.uniform(-0.3, 0.3))


def puff(amp=0.1, seed=0):
    """a small flame blown out"""
    r = np.random.default_rng(seed)
    n = int(0.45 * SR); t = np.arange(n) / SR
    x = lowpass(r.standard_normal(n).astype(np.float32), 900)
    return (x * np.minimum(1, t / 0.02) * np.exp(-t * 9) * amp * 3).astype(np.float32)


def panting(m, t0, t1, amp=0.02, seed=0, rate=0.55):
    """quick breaths after running"""
    r = np.random.default_rng(seed)
    t = t0
    while t < t1:
        n = int(0.28 * SR); tt = np.arange(n) / SR
        x = bandpass(r.standard_normal(n).astype(np.float32), 500, 2600) * np.sin(np.pi * tt / 0.28) ** 2
        place(m, (x * amp * r.uniform(0.7, 1.0)).astype(np.float32), t, pan=0.1)
        t += rate * r.uniform(0.85, 1.15)


def music(m):
    # S1 0-6.8: the grave at dusk: a low drone, the ney's lament
    place(m, drone(36.71, 6.8, amp=0.06, a=0.8, r=1.2), 0.0)
    place(m, pad([shur(1, -1), shur(5, -1), shur(1)], 6.0, amp=0.045, a=0.8, r=1.6, bright=4), 0.2)
    ney(m, [(2, 0, 1.2), (1, 1.2, 0.8), (0, 2.0, 2.2)], 1.6, amp=0.04, step=0.9)
    # S2 6.8-11.4: title: the old man alone at sunrise (a slow drum, the tanbur, the love theme)
    place(m, drum(dur=2.8, f0=44, amp=0.75, noise=0.35), 6.8)
    place(m, drone(36.71, 4.8, amp=0.09, a=0.2, r=1.4), 6.8)
    place(m, pad([shur(0, -1), shur(4, -1), shur(0)], 4.6, amp=0.06, a=0.4, r=1.6, bright=5), 6.8)
    tanbur(m, [(0, 0), (2, 0.5), (4, 1.0), (3, 1.6), (2, 2.1), (0, 2.8)], 7.1, amp=0.18, low=True, step=0.6)
    ney(m, LTHEME, 7.4, amp=0.04, step=0.62)
    # S3 11.4-58.6: the search; the meeting; the plea; the goodbye
    place(m, drone(36.71, 7.2, amp=0.05, a=1.0, r=1.0), 11.4)
    tanbur(m, [(2, 0), (1, 0.8), (0, 1.6), (1, 2.6), (0, 3.4)], 11.8, amp=0.07, step=1.0)
    place(m, drum(dur=2.0, f0=46, amp=0.45, noise=0.3), FOUND - 0.1)
    place(m, pad([shur(0), shur(2), shur(4)], 6.4, amp=0.04, a=0.6, r=1.8, bright=5), FOUND)
    ney(m, [(4, 0, 1.0), (3, 1.0, 0.6), (2, 1.6, 1.6)], FOUND + 2.6, amp=0.035, step=0.9)
    place(m, drone(36.71, 11.0, amp=0.05, a=1.4, r=1.2), 25.4)
    tanbur(m, [(0, 0), (1, 0.6), (2, 1.2), (1, 2.0), (0, 2.8)], 25.8, amp=0.06, step=0.9, low=True)
    place(m, pad([shur(1, -1), shur(5, -1), shur(1)], 7.6, amp=0.04, a=1.2, r=1.6, bright=4), PLEA - 0.4)
    ney(m, [(2, 0, 1.2), (1, 1.2, 0.8), (0, 2.0, 2.0)], PLEA + 1.6, amp=0.035, step=0.9)
    place(m, drum(dur=1.8, f0=46, amp=0.35, noise=0.3), NOT_QAYS)
    place(m, drone(36.71, 7.4, amp=0.06, a=0.3, r=1.6), NOT_QAYS)
    ney(m, LTHEME, NOT_QAYS + 3.4, amp=0.04, step=0.62)
    place(m, pad([shur(0), shur(4), shur(0, 1)], 5.0, amp=0.035, a=1.2, r=1.6, bright=5), PURSE)
    place(m, drone(36.71, 10.8, amp=0.06, a=1.0, r=2.0), GOODBYE)
    place(m, pad([shur(1, -1), shur(5, -1), shur(1)], 10.4, amp=0.045, a=1.0, r=2.4, bright=4), GOODBYE)
    ney(m, [(4, 0, 1.4), (3, 1.4, 0.8), (2, 2.2, 1.2), (1, 3.4, 0.8), (0, 4.2, 2.6)], LEAVES + 0.6, amp=0.045, step=0.9)
    # S4 58.6-70.8: the empty seat; the lamp goes out; the funeral far away (a slow drum like steps)
    place(m, drone(36.71, 4.8, amp=0.05, a=1.0, r=0.6), SEAT)
    tanbur(m, [(2, 0), (1, 1.0), (0, 2.0)], SEAT + 0.6, amp=0.05, step=1.0)
    place(m, bell(220, 3.4, 0.05), LAMP_OUT + 0.2)
    place(m, drone(36.71, 6.4, amp=0.07, a=0.6, r=1.6), FUNERAL)
    for k, t in enumerate(np.arange(FUNERAL + 0.2, 70.4, 1.25)):
        place(m, drum(dur=1.2, f0=50, amp=0.28 - 0.02 * k, noise=0.2), t)
    ney(m, [(1, 0, 1.4), (0, 1.4, 0.8), (1, 2.2, 0.6), (0, 2.8, 2.4)], FUNERAL + 0.6, amp=0.045, step=0.9)
    # S5 70.8-103.0: the news; the grave; night
    place(m, drone(36.71, 3.0, amp=0.04, a=0.6, r=0.6), RUNNER)
    place(m, drum(dur=2.4, f0=42, amp=0.6, noise=0.35), NEWS - 0.1)
    place(m, pad([shur(1, -1), shur(5, -1), shur(1)], 6.0, amp=0.05, a=0.2, r=1.6, bright=4), NEWS)
    heartbeat(m, 77.2, 82.4, bpm=66, amp=0.1)
    place(m, drone(36.71, 14.4, amp=0.06, a=1.2, r=1.6), GRAVE)
    ney(m, [(2, 0, 1.2), (1, 1.2, 0.8), (0, 2.0, 2.2)], GRAVE + 0.6, amp=0.045, step=0.9)
    place(m, pad([shur(0, -1), shur(4, -1), shur(0)], 8.0, amp=0.04, a=1.4, r=1.8, bright=4), 88.0)
    ney(m, [(4, 0, 1.0), (3, 1.0, 0.6), (2, 1.6, 1.0), (1, 2.6, 0.8), (0, 3.4, 2.4)], 92.2, amp=0.04, step=0.9)
    place(m, drone(36.71, 6.2, amp=0.05, a=1.6, r=2.0), STARS)
    shimmer(m, STARS + 1.6, 3.4, amp=0.012, seed=51)
    ney(m, LTHEME, STARS + 0.8, amp=0.035, step=0.8)
    # S6 103.0-137.8: the hunter; the gold; her eyes; free; the family of the desert
    place(m, drone(36.71, 8.4, amp=0.04, a=1.0, r=1.0), HUNTER)
    tanbur(m, [(0, 0), (1, 0.6), (0, 1.2), (2, 2.0), (1, 2.6), (0, 3.2)], HUNTER + 0.4, amp=0.07, step=0.8)
    place(m, drum(dur=1.6, f0=50, amp=0.4, noise=0.3), 109.4)
    place(m, pad([shur(0), shur(2), shur(4)], 5.6, amp=0.03, a=1.0, r=1.4, bright=5), GOLD)
    place(m, pad([shur(0), shur(4), shur(0, 1)], 5.8, amp=0.04, a=1.0, r=2.0, bright=5), EYES - 0.2)
    ney(m, LTHEME, EYES + 0.6, amp=0.045, step=0.7)
    shimmer(m, FREE + 1.3, 2.6, amp=0.014, seed=52)
    place(m, drone(36.71, 13.0, amp=0.05, a=1.4, r=2.0), FREE)
    tanbur(m, [(0, 0), (2, 0.5), (4, 1.0), (5, 1.5), (4, 2.0), (2, 2.5), (4, 3.0), (2, 3.5), (1, 4.0), (0, 4.5)], FAMILY + 0.4, amp=0.08, step=0.6)
    place(m, pad([shur(0), shur(2), shur(4), shur(0, 1)], 6.4, amp=0.035, a=1.6, r=2.0, bright=5), FAMILY)
    # S7 137.8-151.2: the old man with the letter; the end card
    place(m, drone(36.71, 13.4, amp=0.05, a=1.2, r=1.0), OLD_MAN)
    tanbur(m, [(2, 0), (1, 0.8), (0, 1.6), (1, 2.6), (0, 3.4)], OLD_MAN + 0.4, amp=0.06, step=1.0)
    place(m, pad([shur(1, -1), shur(5, -1), shur(1)], 4.0, amp=0.035, a=0.6, r=1.0, bright=4), LETTER)
    place(m, drum(dur=2.0, f0=46, amp=0.5, noise=0.3), FROM_LEYLI)
    shimmer(m, FROM_LEYLI + 0.1, 3.2, amp=0.02, seed=53)
    ney(m, LTHEME, FROM_LEYLI + 0.8, amp=0.045, step=0.55)
    place(m, drum(dur=3.0, f0=40, amp=0.85, noise=0.4), END_CARD)
    place(m, drone(36.71, 5.2, amp=0.09, a=0.2, r=2.0), END_CARD)
    place(m, pad([shur(1, -1), shur(5, -1), shur(1)], 5.0, amp=0.06, a=0.3, r=2.0, bright=5), END_CARD)
    tanbur(m, [(0, 0), (2, 0.5), (4, 1.0), (3, 1.6), (2, 2.1), (0, 2.8)], END_CARD + 0.5, amp=0.13, low=True, step=0.6)


def sfx(s):
    # S1: dusk at the grave: wind, sand
    place(s, noise_bed(6.8, amp=0.022, lo=250, hi=1800, lfo=0.2, seed=501), 0.0)
    place(s, gust(2.4, 0.05, seed=502), 2.6)
    place(s, sand_hiss(2.6, 0.025, seed=503), 3.0)
    # S2: sunrise: wind, the old man's slow steps and his stick
    place(s, noise_bed(4.6, amp=0.02, lo=300, hi=2000, lfo=0.2, seed=504), 6.8)
    for k, t in enumerate(np.arange(7.2, 11.0, 1.1)):
        place(s, thud(0.04, f0=120, seed=505 + k), t, pan=0.1)
        steps(s, t + 0.35, t + 0.4, step=1.0, amp=0.015, seed=510 + k)
    # S3: the desert by day: wind; the old man's steps and stick; birds; the gazelles start; the goodbye steps fade
    place(s, noise_bed(47.2, amp=0.02, lo=300, hi=2200, lfo=0.18, seed=520), 11.4)
    t = 11.8
    while t < 16.8:
        place(s, thud(0.045, f0=120, seed=int(t * 10)), t, pan=-0.2)
        steps(s, t + 0.35, t + 0.4, step=1.0, amp=0.02, seed=int(t * 10) + 1, pan=-0.2)
        t += 1.1
    for k, t in enumerate((13.0, 13.3, 15.6)):
        place(s, chirp(2900 + 300 * k, amp=0.02), t, pan=0.4 - 0.3 * k)
    t = 17.2
    while t < 18.4:
        place(s, thud(0.045, f0=120, seed=int(t * 10)), t, pan=0.3)
        steps(s, t + 0.35, t + 0.4, step=1.0, amp=0.02, seed=int(t * 10) + 1, pan=0.3)
        t += 1.1
    steps(s, 18.0, 18.6, step=0.12, amp=0.025, seed=521, pan=0.2)          # the gazelles start
    place(s, rustle(0.03, 0.7, seed=522), 26.0)                              # the father sits down by his son
    place(s, rustle(0.025, 0.6, seed=523), PURSE + 0.4)
    coins(s, PURSE + 1.6, amp=0.025, seed=524)
    place(s, gust(2.6, 0.05, seed=525), LEAVES + 1.8)
    t = LEAVES + 0.4
    k = 0
    while t < 58.0:
        a = 0.04 * (1 - (t - LEAVES) / 6.0)
        place(s, thud(max(0.008, a), f0=120, seed=530 + k), t, pan=0.3 + 0.1 * k)
        t += 1.15; k += 1
    # S4: the tent at dusk: crickets, the lamp; it goes out; the funeral: wind, quiet voices
    crickets(s, SEAT, 64.8, amp=0.004, seed=540)
    place(s, crackle(4.8, amp=0.012, rate=4, seed=541), SEAT)
    place(s, puff(0.08, seed=542), LAMP_OUT)
    place(s, noise_bed(6.0, amp=0.024, lo=250, hi=1800, lfo=0.2, seed=543), FUNERAL)
    place(s, murmur(5.6, 0.012, seed=544), FUNERAL + 0.2)
    # S5: the young man runs in, panting; the grave at dusk: wind; night: crickets, an owl far away
    place(s, noise_bed(11.8, amp=0.02, lo=300, hi=2200, lfo=0.18, seed=550), RUNNER)
    steps(s, RUNNER + 0.1, RUNNER + 2.6, step=0.26, amp=0.03, seed=551, pan=0.3)
    steps(s, RUNNER + 0.6, RUNNER + 1.0, step=0.12, amp=0.02, seed=552, pan=-0.3)   # the gazelles start
    panting(s, RUNNER + 2.4, NEWS - 0.2, amp=0.02, seed=553)
    panting(s, 76.9, 77.3, amp=0.015, seed=554)
    place(s, noise_bed(14.2, amp=0.022, lo=250, hi=1800, lfo=0.2, seed=555), GRAVE)
    place(s, gust(2.6, 0.05, seed=556), 93.0)
    place(s, sand_hiss(3.0, 0.02, seed=557), 94.0)
    crickets(s, STARS + 1.0, 103.0, amp=0.006, seed=558)
    place(s, owl(0.025), 100.2, pan=0.5)
    # S6: the hunter and the gazelle: wind, her struggling hooves, a bleat; the rope; the coins; she steps away; birds
    place(s, noise_bed(34.8, amp=0.02, lo=300, hi=2200, lfo=0.18, seed=560), HUNTER)
    for k, t in enumerate(np.arange(HUNTER + 0.3, 109.0, 0.9)):
        place(s, scrape(0.4, 0.02, seed=561 + k), t, pan=-0.1)
    place(s, bleat(0.03, seed=570, f0=760), HUNTER + 2.2, pan=-0.1)
    place(s, bleat(0.025, seed=571, f0=820), 112.8, pan=-0.2)
    steps(s, HUNTER + 0.4, HUNTER + 4.0, step=0.5, amp=0.02, seed=572, pan=-0.4)  # Majnun walks in
    place(s, rustle(0.03, 0.5, seed=573), GOLD + 0.4)
    coins(s, GOLD + 1.0, amp=0.03, seed=574)
    coins(s, 117.9, amp=0.025, seed=575, n=5)
    place(s, rustle(0.025, 0.6, seed=576), FREE + 0.5)
    steps(s, FREE + 1.6, FREE + 3.0, step=0.22, amp=0.02, seed=577, pan=-0.3)    # she steps away…
    steps(s, FREE + 3.8, FREE + 5.0, step=0.24, amp=0.018, seed=579, pan=-0.1)   # …and comes back
    for k, t in enumerate((FAMILY + 0.8, FAMILY + 1.1, FAMILY + 3.4, FAMILY + 3.6)):
        place(s, chirp(2800 + 280 * k, amp=0.02), t, pan=-0.4 + 0.25 * k)
    wings(s, FAMILY + 2.0, n=4, amp=0.02, seed=579)
    # S7: dusk: wind, the old man's steps and stick
    place(s, noise_bed(13.4, amp=0.022, lo=250, hi=1800, lfo=0.2, seed=580), OLD_MAN)
    t = OLD_MAN + 0.8
    k = 0
    while t < LETTER - 0.4:
        place(s, thud(0.02 + 0.006 * k, f0=120, seed=581 + k), t, pan=0.4)
        t += 1.1; k += 1
    place(s, rustle(0.02, 0.6, seed=590), LETTER - 0.2)
    place(s, gust(2.4, 0.04, seed=591), 148.8)


LINES = [("p5s1a", 0.5), ("p5s1b", 3.3),
         ("p5s3a", 11.8), ("p5s3b", FOUND), ("p5s3c", 21.9), ("p5s3d", 25.7), ("p5s3e", PLEA), ("p5s3f", NOT_QAYS), ("p5s3g", 39.5),
         ("p5s3h", PURSE), ("p5s3i", GOODBYE), ("p5s3j", LEAVES),
         ("p5s4a", 59.0), ("p5s4b", 65.6),
         ("p5s5a", NEWS), ("p5s5b", 77.4), ("p5s1a", 84.2), ("p5s1b", 87.2), ("p5s5c", 89.8), ("p5s5d", 97.6),
         ("p5s6a", 103.4), ("p5s6b", 109.5), ("p5s6c", 111.8), ("p5s6d", GOLD), ("p5s6e", 118.1), ("p5s6f", EYES), ("p5s6g", FREE + 1.8),
         ("p5s6h", 131.4),
         ("p5s7a", 138.2), ("p5s7b", LETTER), ("p5s7c", FROM_LEYLI)]
if __name__ == "__main__":
    build(5, TOTAL, music, sfx, LINES, f'{AUDIO}/part05.wav')
    print('done')
