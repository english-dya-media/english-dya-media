"""Part 4 · Leyli's Wedding — timing, music and sound.
Scene starts: s1 0 (hook: a traveller on a camel: "Haven't you heard? Leyli is married now!"; Majnun: "Married…?"), s2 7.6 (title: the
bride's litter on a camel crosses the dunes at dusk, with lanterns), s3 12.2 (the wedding at night: music and feasting; two women: "as
beautiful as the moon" — "then why are her eyes so sad?"; the bride beside Ibn Salam), s4 35.6 (Ibn Salam's tent at night: "this house is
yours"; "my heart belongs to another… stay away from me"; "I will not force you… I will wait"), s5 60.2 (Leyli alone at night by the
door, the moon: "Majnun… wherever you are… I am still yours"), s6 74.2 (the desert: the traveller tells Majnun; "Can the desert forget the
rain?"; "the moon is far away, but its light still finds me"; Majnun goes deeper into the wild), s7 111.4 (an old man with a stick walks
into the desert: "Qays! My son! Where are you?"), end card 121.4, end 126.6"""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import series; series.from_folder(__file__)
from paths import AUDIO
from audio import *
from mix import build
from lsfx import *

TOTAL = 126.6
S = {"s1": 0.0, "s2": 7.6, "s3": 12.2, "s4": 35.6, "s5": 60.2, "s6": 74.2, "s7": 111.4}
END_CARD = 121.4
MARRIED = 87.0          # Majnun: "Married…?" (s6 D)
SAD_EYES = 25.9         # "Then why are her eyes so sad?"
TRUTH = 46.2            # "My heart belongs to another…"
WAIT = 53.6             # Ibn Salam: "I will not force you…"
NIGHT = 60.2            # Leyli alone at night
WHISPER = 67.4          # "Majnun… wherever you are… I am still yours."
RAIN = 94.2             # "Can the desert forget the rain?"
MOON = 98.0             # "The moon is far away…"
WILD = 104.0            # Majnun walks into the wild
OLD = 111.4             # the old man with a stick
CALL = 117.4            # "Qays! My son! Where are you?"


def clap(amp=0.06, seed=0):
    """one hand clap: a short bright burst"""
    r = np.random.default_rng(seed)
    n = int(0.09 * SR); t = np.arange(n) / SR
    x = bandpass(r.standard_normal(n).astype(np.float32), 900, 4200) * np.exp(-t * 55)
    return (x * amp * 2.2).astype(np.float32)


def claps(m, t0, t1, beat=0.5, amp=0.05, seed=0, people=6):
    """a crowd clapping on the beat (a little loose)"""
    r = np.random.default_rng(seed)
    t = t0
    while t < t1:
        for p in range(people):
            place(m, clap(amp * r.uniform(0.5, 1.0), seed=int(t * 100) + p), t + r.uniform(-0.025, 0.025), pan=r.uniform(-0.6, 0.6))
        t += beat


def daf(m, t0, t1, beat=0.5, amp=0.2, seed=0, pattern=(1, 0, 0.6, 0.6)):
    """a frame drum: low "dum" on the first beat, bright "tak"s after"""
    k = 0
    t = t0
    while t < t1:
        w = pattern[k % len(pattern)]
        if w:
            if k % len(pattern) == 0:
                place(m, drum(dur=0.6, f0=78, amp=amp * w, noise=0.35), t)
            else:
                place(m, clap(amp * 0.6 * w, seed=seed + k), t, pan=0.15)
                place(m, drum(dur=0.25, f0=150, amp=amp * 0.35 * w, noise=0.6), t)
        t += beat / 2
        k += 1


def trill(dur=1.6, amp=0.03, f0=880.0, seed=0):
    """a women's joyful trill at a wedding (a fast warble, far off)"""
    n = int(dur * SR); t = np.arange(n) / SR
    f = f0 * (1 + 0.06 * np.sign(np.sin(2 * np.pi * 9.0 * t)) * 0.5 + 0.02 * np.sin(2 * np.pi * 2.0 * t))
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) + 0.3 * np.sin(4 * np.pi * np.cumsum(f) / SR)
    e = np.minimum(1, t / 0.1) * np.minimum(1, (dur - t) / 0.3).clip(0, 1)
    return lowpass((x * e * amp).astype(np.float32), 3000)


def music(m):
    # S1 0-7.6: the desert; the news; a hit on "Married…?"
    place(m, drone(36.71, 4.8, amp=0.06, a=0.8, r=1.0), 0.0)
    ney(m, [(2, 0, 1.0), (1, 1.0, 0.6), (0, 1.6, 1.4)], 0.4, amp=0.04, step=0.9)
    place(m, drum(dur=2.4, f0=42, amp=0.6, noise=0.35), 4.6)
    place(m, pad([shur(1, -1), shur(5, -1), shur(1)], 3.0, amp=0.05, a=0.2, r=1.4, bright=4), 4.6)
    # S2 7.6-12.2: title: the bride's litter at dusk (a wedding drum, slow)
    place(m, drum(dur=2.8, f0=44, amp=0.75, noise=0.35), 7.6)
    place(m, drone(36.71, 4.9, amp=0.09, a=0.2, r=1.4), 7.6)
    place(m, pad([shur(0, -1), shur(4, -1), shur(0)], 4.8, amp=0.06, a=0.4, r=1.6, bright=5), 7.6)
    tanbur(m, [(0, 0), (2, 0.5), (4, 1.0), (3, 1.6), (2, 2.1), (0, 2.8)], 7.9, amp=0.18, low=True, step=0.6)
    ney(m, LTHEME, 8.2, amp=0.04, step=0.62)
    # S3 12.2-35.6: the wedding: daf and tanbur, a lively tune; it falls away to the bride's sadness
    daf(m, 12.4, 28.8, beat=0.48, amp=0.2, seed=401)
    tune = [(0, 0), (2, 0.5), (4, 1.0), (5, 1.5), (4, 2.0), (2, 2.5), (4, 3.0), (2, 3.5), (1, 4.0), (0, 4.5)]
    for k, t0 in enumerate((12.6, 17.4, 22.2)):
        tanbur(m, tune, t0, amp=0.13, low=(k == 0), step=0.48)
    place(m, drone(36.71, 16.6, amp=0.05, a=0.6, r=1.0), 12.2)
    place(m, pad([shur(1, -1), shur(5, -1)], 6.6, amp=0.035, a=1.2, r=1.6, bright=4), SAD_EYES)
    ney(m, [(4, 0, 1.0), (3, 1.0, 0.6), (2, 1.6, 1.6)], 29.0, amp=0.045, step=0.9)
    place(m, drone(36.71, 6.6, amp=0.06, a=1.0, r=1.4), 29.0)
    ney(m, LTHEME, 32.6, amp=0.045, step=0.55)
    # S4 35.6-60.2: Ibn Salam's tent: warm, then the truth; his patience
    place(m, drone(36.71, 10.6, amp=0.05, a=1.0, r=1.0), 35.6)
    tanbur(m, [(4, 0), (5, 0.5), (4, 1.0), (2, 1.6)], 36.0, amp=0.08, step=0.8)
    place(m, pad([shur(0), shur(2), shur(4)], 9.0, amp=0.035, a=1.4, r=1.4, bright=5), 37.0)
    place(m, drum(dur=1.8, f0=46, amp=0.4, noise=0.3), TRUTH)
    place(m, drone(36.71, 7.4, amp=0.07, a=0.3, r=1.6), TRUTH)
    place(m, pad([shur(1, -1), shur(5, -1), shur(1)], 7.0, amp=0.045, a=0.6, r=1.6, bright=4), TRUTH)
    ney(m, [(2, 0, 1.2), (1, 1.2, 0.8), (0, 2.0, 2.0)], WAIT - 0.6, amp=0.04, step=0.9)
    place(m, pad([shur(0), shur(4), shur(0, 1)], 6.4, amp=0.035, a=1.6, r=2.0, bright=5), WAIT + 2.0)
    # S5 60.2-74.2: Leyli alone at night: the love theme, very soft; a shimmer on the whisper
    place(m, drone(36.71, 14.0, amp=0.05, a=1.6, r=2.0), NIGHT)
    ney(m, LTHEME, NIGHT + 0.6, amp=0.045, step=0.95)
    shimmer(m, WHISPER + 0.4, 3.0, amp=0.016, seed=41)
    ney(m, [(4, 0, 1.4), (3, 1.4, 0.8), (2, 2.2, 1.2), (0, 3.4, 2.2)], WHISPER + 1.2, amp=0.04, step=0.9)
    # S6 74.2-111.4: the desert: the traveller; the news; Majnun's answer; into the wild
    place(m, drone(36.71, 12.4, amp=0.05, a=1.0, r=1.0), 74.2)
    tanbur(m, [(0, 0), (1, 0.6), (0, 1.2)], 74.6, amp=0.06, step=0.9)
    place(m, drum(dur=2.4, f0=42, amp=0.65, noise=0.35), MARRIED - 0.2)
    place(m, pad([shur(1, -1), shur(5, -1), shur(1)], 6.6, amp=0.05, a=0.2, r=1.6, bright=4), MARRIED - 0.2)
    heartbeat(m, MARRIED + 0.6, 93.6, bpm=70, amp=0.1)
    place(m, drone(36.71, 17.2, amp=0.06, a=1.2, r=1.6), RAIN)
    ney(m, [(2, 0, 1.0), (1, 1.0, 0.6), (0, 1.6, 1.8)], RAIN + 0.3, amp=0.045, step=0.85)
    place(m, pad([shur(0), shur(4), shur(0, 1)], 6.4, amp=0.04, a=1.6, r=2.0, bright=5), MOON)
    shimmer(m, MOON + 2.6, 2.6, amp=0.016, seed=42)
    ney(m, LTHEME, WILD + 0.4, amp=0.05, step=0.95)
    place(m, pad([shur(0, -1), shur(4, -1), shur(0)], 7.2, amp=0.04, a=1.4, r=1.6, bright=5), WILD)
    # S7 111.4-126.6: the old man with a stick; the call; end card
    place(m, drone(36.71, 10.2, amp=0.06, a=1.2, r=1.0), OLD)
    tanbur(m, [(2, 0), (1, 0.8), (0, 1.6), (1, 2.6), (0, 3.4)], OLD + 0.4, amp=0.07, step=1.0)
    place(m, pad([shur(1, -1), shur(5, -1)], 4.0, amp=0.04, a=0.6, r=1.0, bright=4), CALL)
    place(m, drum(dur=3.0, f0=40, amp=0.85, noise=0.4), END_CARD)
    place(m, drone(36.71, 5.2, amp=0.09, a=0.2, r=2.0), END_CARD)
    place(m, pad([shur(1, -1), shur(5, -1), shur(1)], 5.0, amp=0.06, a=0.3, r=2.0, bright=5), END_CARD)
    tanbur(m, [(0, 0), (2, 0.5), (4, 1.0), (3, 1.6), (2, 2.1), (0, 2.8)], END_CARD + 0.5, amp=0.13, low=True, step=0.6)


def sfx(s):
    # S1: the desert: wind, sand, the camel
    place(s, noise_bed(7.6, amp=0.025, lo=300, hi=2200, lfo=0.2, seed=401), 0.0)
    place(s, camel_grumble(0.05, seed=402), 0.2, pan=-0.3)
    place(s, gust(2.4, 0.06, seed=403), 4.8)
    place(s, sand_hiss(2.6, 0.03, seed=404), 5.0)
    # S2: dusk: the camel's bells, steps
    place(s, noise_bed(4.6, amp=0.02, lo=300, hi=2000, lfo=0.2, seed=405), 7.6)
    for k, t in enumerate(np.arange(8.0, 12.0, 0.6)):
        place(s, bell(1700 + 220 * (k % 3), 0.5, 0.012), t, pan=0.2)
    steps(s, 8.0, 12.0, step=0.6, amp=0.015, seed=406)
    # S3: the wedding: claps, talk, a trill, the fire
    claps(s, 12.6, 21.0, beat=0.48, amp=0.03, seed=407)
    place(s, murmur(23.4, 0.03, seed=408), 12.2)
    place(s, trill(1.8, 0.03, seed=409), 14.4, pan=0.4)
    place(s, trill(1.4, 0.025, f0=990, seed=410), 19.6, pan=-0.4)
    place(s, crackle(23.4, amp=0.03, rate=8, seed=411), 12.2)
    crickets(s, 28.8, 35.6, amp=0.004, seed=412)
    # S4: Ibn Salam's tent: the lamp, cloth, crickets outside
    place(s, crackle(24.6, amp=0.015, rate=5, seed=413), 35.6)
    crickets(s, 35.6, 60.2, amp=0.004, seed=414)
    place(s, rustle(0.03, 0.7, seed=415), 36.2)
    place(s, rustle(0.025, 0.6, seed=416), 51.0)
    # S5: night: crickets, an owl far away, the lamp
    crickets(s, 60.2, 74.2, amp=0.006, seed=417)
    place(s, owl(0.03), 62.4, pan=0.5)
    place(s, crackle(14.0, amp=0.012, rate=4, seed=418), 60.2)
    # S6: the desert by day: wind, the camel's steps and bells; the wild at dusk
    place(s, noise_bed(37.2, amp=0.022, lo=300, hi=2200, lfo=0.18, seed=419), 74.2)
    for k, t in enumerate(np.arange(74.6, 78.6, 0.6)):
        place(s, bell(1700 + 220 * (k % 3), 0.5, 0.01), t, pan=0.3)
    steps(s, 74.6, 78.6, step=0.6, amp=0.02, seed=420)
    place(s, camel_grumble(0.05, seed=421), 79.4, pan=0.3)
    place(s, gust(2.6, 0.07, seed=422), MARRIED - 0.2)
    place(s, sand_hiss(3.0, 0.03, seed=423), MARRIED)
    for k, t in enumerate((105.0, 105.3, 108.2)):
        place(s, chirp(2900 + 300 * k, amp=0.02), t, pan=-0.3 + 0.3 * k)
    steps(s, WILD + 0.4, 110.8, step=0.55, amp=0.02, seed=424)
    # S7: dusk: wind, the old man's slow steps and his stick
    place(s, noise_bed(15.2, amp=0.022, lo=250, hi=1800, lfo=0.2, seed=425), OLD)
    t = OLD + 0.6
    while t < 121.0:
        place(s, thud(0.05, f0=120, seed=int(t * 10)), t, pan=0.1)
        steps(s, t + 0.35, t + 0.4, step=1.0, amp=0.02, seed=int(t * 10) + 1)
        t += 1.1
    place(s, gust(2.4, 0.05, seed=426), 119.6)


LINES = [("p4s1a", 0.5), ("p4s1b", 4.9),
         ("p4s3a", 13.0), ("p4s3b", 17.8), ("p4s3c", 21.2), ("p4s3d", SAD_EYES), ("p4s3e", 29.8),
         ("p4s4a", 36.0), ("p4s4b", 40.8), ("p4s4c", TRUTH), ("p4s4d", 50.8), ("p4s4e", WAIT), ("p4s4f", 57.0),
         ("p4s5a", 60.6), ("p4s5b", WHISPER),
         ("p4s6a", 74.6), ("p4s6b", 79.2), ("p4s1a", 82.8), ("p4s1b", MARRIED), ("p4s6c", 89.2), ("p4s6d", RAIN), ("p4s6e", MOON),
         ("p4s6f", 104.6),
         ("p4s7a", 111.8), ("p4s7b", CALL)]
if __name__ == "__main__":
    build(4, TOTAL, music, sfx, LINES, f'{AUDIO}/part04.wav')
    print('done')
