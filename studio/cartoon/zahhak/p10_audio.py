"""Part 10 · Damavand — timing, music and sound.
Scene starts: s1 0 (hook: a rope on the black palace wall at night; "My palace… my throne…"), s2 7.8 (title: Mount Damavand at night),
s3 12.4 (India: "maybe he is only a guest" — "a guest with an ox-headed mace?"; "we ride home tonight"; the city stands with Fereydun,
Kaveh at the gate), s4 42.6 (Zahhak in iron; he climbs the wall with a rope; Shahrnaz and Fereydun in the hall; "Free? In my palace?"),
s5 68.2 (he drops into the hall; "Zahhak!"; the mace breaks his helmet; Sorush: "do not strike again… bind him"; "As you say"),
s6 94.4 (the road to Damavand; the cave; "Here you will stay"; the mountain at night), s7 117.6 (the first of Mehr: Fereydun crowned;
Faranak; "no one will live in fear"; the fires of Mehregan; Kaveh: "We are free!"; the banner over a free land),
end card 146.6, end 152.0"""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import series; series.from_folder(__file__)
from paths import AUDIO
from audio import *
from mix import build
from zsfx import *
from p07_audio import murmur, cheer, gasp
from p08_audio import rumble, gravel, shimmer

TOTAL = 152.0
S = {"s1": 0.0, "s2": 7.8, "s3": 12.4, "s4": 42.6, "s5": 68.2, "s6": 94.4, "s7": 117.6}
END_CARD = 146.6
HOOK = 1.3              # the rope's hook bites on the battlement (s1 A)
HOOK2 = 50.0            # … and again in s4 B
LAND = 68.8             # Zahhak lands on the floor of the hall
STRIKE = 74.4           # the mace rings on his helmet
SORUSH_IN = 81.0        # the light of Sorush
CHAINS = (102.6, 103.5, 104.7)
HOPE = [(0, 0), (2, 0.5), (4, 1.0), (5, 1.5), (4, 2.0), (5, 2.4), (7, 2.9), (4, 3.6)]
DANCE = [(0, 0), (2, 0.25), (4, 0.5), (2, 0.75), (5, 1.0), (4, 1.25), (2, 1.5), (0, 1.75)]


def swish(dur=0.8, amp=0.1, seed=0):
    """a short rush of air (a rope thrown, a blow): rises to the end"""
    r = np.random.default_rng(seed)
    n = int(dur * SR); t = np.arange(n) / SR
    x = bandpass(r.standard_normal(n).astype(np.float32), 400, 3600)
    e = np.sin(np.pi * np.clip(t / dur, 0, 1) * 0.92) ** 2 * (t / dur)
    return (x * e * amp * 3).astype(np.float32)


def clang(amp=0.3, seed=0):
    """steel ringing on a steel helmet"""
    r = np.random.default_rng(seed)
    n = int(0.15 * SR); t = np.arange(n) / SR
    nz = highpass(r.standard_normal(n).astype(np.float32), 2200) * np.exp(-t * 35)
    b = bell(f=1240, dur=1.8, amp=amp * 0.5)
    for f, d, a in ((1850, 1.6, amp), (2630, 1.2, amp * 0.6)):
        x = bell(f=f, dur=d, amp=a); b[:len(x)] += x
    b[:n] += nz * amp * 2.0
    return b


def clink(amp=0.08, seed=0):
    """a small metal clink: the hook, a chain link"""
    r = np.random.default_rng(seed)
    n = int(0.05 * SR); t = np.arange(n) / SR
    b = bell(f=2900 + 500 * r.random(), dur=0.5, amp=amp)
    x = bell(f=4100 + 300 * r.random(), dur=0.35, amp=amp * 0.5); b[:len(x)] += x
    b[:n] += highpass(r.standard_normal(n).astype(np.float32), 3000) * np.exp(-t * 60) * amp
    return b


def chain(amp=0.08, seed=0, n=5):
    """a chain pulled tight: a run of clinks"""
    r = np.random.default_rng(seed)
    out = np.zeros(int(0.9 * SR), np.float32)
    for k in range(n):
        c = clink(amp * r.uniform(0.6, 1.0), seed=seed * 10 + k)
        i = int((0.06 * k + r.uniform(0, 0.03)) * SR)
        m_ = min(len(c), len(out) - i)
        out[i:i + m_] += c[:m_]
    return out


def music(m):
    # S1 0-7.8: night at the black wall
    place(m, drone(36.71, 8.0, amp=0.10, a=0.8, r=1.0), 0.0)
    place(m, pad([shur(1, -1), shur(5, -1), shur(1)], 7.6, amp=0.05, a=1.0, r=1.2, bright=4), 0.0)
    heartbeat(m, 1.6, 7.4, bpm=70, amp=0.14)
    # S2 7.8-12.4: title over Damavand
    place(m, drum(dur=3.2, f0=40, amp=0.9, noise=0.4), 7.8)
    place(m, drone(36.71, 4.9, amp=0.12, a=0.1, r=1.4), 7.8)
    place(m, pad([shur(0, -1), shur(4, -1), shur(0)], 4.8, amp=0.08, a=0.4, r=1.6, bright=5), 7.8)
    tanbur(m, ZTHEME, 8.2, amp=0.22, low=True, step=0.85)
    # S3 12.4-42.6: India; the ride home; the city
    place(m, drone(36.71, 14.0, amp=0.08, a=1.0, r=1.0), 12.4)
    place(m, pad([shur(1, -1), shur(5, -1)], 13.6, amp=0.04, a=1.5, r=1.0, bright=4), 12.4)
    heartbeat(m, 17.2, 26.0, bpm=80, amp=0.12)
    place(m, drum(dur=2.4, f0=44, amp=0.7, noise=0.4), 26.9)                                  # "Enough!"
    place(m, pad([shur(1, -1), shur(5, -1), shur(1)], 4.0, amp=0.08, a=0.1, r=1.4, bright=6), 26.9)
    place(m, drone(36.71, 11.4, amp=0.09, a=0.6, r=1.2), 31.2)                                 # the march back
    for i, t in enumerate(np.arange(31.4, 37.2, 0.4)):
        place(m, drum(dur=0.6, f0=58 if i % 2 else 48, amp=0.2 + (0.06 if i % 4 == 0 else 0), noise=0.25), t)
    tanbur(m, [(0, 0), (0, 0.5), (1, 1.0), (0, 1.5), (3, 2.0), (2, 2.5), (1, 3.0), (0, 3.5)], 31.6, amp=0.12, low=True, step=0.75)
    place(m, pad([shur(0), shur(4), shur(0, 1)], 5.0, amp=0.08, a=0.4, r=1.2, bright=6), 37.4)      # Kaveh at the gate
    tanbur(m, HOPE[:5], 37.8, amp=0.13, low=True, step=0.8)
    # S4 42.6-68.2: iron; the climb; the hall; "Free?"
    place(m, drone(36.71, 12.6, amp=0.10, a=1.0, r=1.0), 42.6)
    place(m, pad([shur(1, -1), shur(5, -1), shur(1)], 12.2, amp=0.05, a=1.0, r=1.0, bright=4), 42.6)
    heartbeat(m, 49.2, 54.8, bpm=84, amp=0.14)
    place(m, pad([shur(0), shur(2), shur(4)], 9.0, amp=0.05, a=1.2, r=1.2, bright=5), 55.0)        # the hall, free
    tanbur(m, [(2, 0), (1, 0.8), (0, 1.6), (1, 2.6), (2, 3.4)], 55.6, amp=0.08, step=1.0)
    place(m, drone(36.71, 4.4, amp=0.10, a=0.3, r=0.6), 64.0)                                  # Zahhak at the window
    place(m, pad([shur(1, -1), shur(5, -1), shur(1)], 4.0, amp=0.07, a=0.3, r=0.6, bright=5), 64.2)
    for i, t in enumerate(np.arange(66.2, 68.2, 0.25)):
        place(m, drum(dur=0.4, f0=62 if i % 2 else 52, amp=0.16 + 0.03 * i, noise=0.25), t)
    # S5 68.2-94.4: the fight; Sorush
    place(m, drum(dur=2.0, f0=42, amp=0.8, noise=0.45), LAND)
    place(m, drone(36.71, 6.0, amp=0.12, a=0.1, r=0.8), LAND)
    for i, t in enumerate(np.arange(71.4, STRIKE, 0.2)):
        place(m, drum(dur=0.35, f0=64 if i % 2 else 54, amp=0.2 + 0.03 * i, noise=0.3), t)
    place(m, drum(dur=3.4, f0=38, amp=1.0, noise=0.5), STRIKE)
    place(m, pad([shur(0, -1), shur(4, -1), shur(0)], 5.4, amp=0.09, a=0.1, r=1.5, bright=6), STRIKE)
    place(m, drone(36.71, 5.4, amp=0.08, a=0.4, r=1.0), 75.6)
    heartbeat(m, 78.6, 80.8, bpm=96, amp=0.14)
    shimmer(m, SORUSH_IN, 3.4, amp=0.03, seed=101, base=880)                                     # the light
    place(m, pad([shur(0), shur(4), shur(0, 1), shur(2, 1)], 11.0, amp=0.08, a=0.6, r=2.0, bright=7), SORUSH_IN)
    place(m, bell(880, 3.0, 0.05), SORUSH_IN + 0.2)
    tanbur(m, [(4, 0), (5, 0.8), (4, 1.6), (2, 2.4), (0, 3.4)], 86.4, amp=0.08, step=1.0)
    place(m, pad([shur(0), shur(2), shur(4)], 3.2, amp=0.05, a=0.5, r=1.2, bright=5), 91.2)
    # S6 94.4-117.6: the road to Damavand; the cave; the mountain
    place(m, drone(36.71, 7.0, amp=0.09, a=0.8, r=1.0), 94.4)
    place(m, pad([shur(0, -1), shur(4, -1), shur(0)], 6.6, amp=0.05, a=1.0, r=1.0, bright=4), 94.4)
    for i, t in enumerate(np.arange(94.6, 101.0, 0.8)):
        place(m, drum(dur=0.9, f0=52, amp=0.16 + (0.05 if i % 2 == 0 else 0), noise=0.2), t)
    tanbur(m, ZTHEME, 95.4, amp=0.09, step=1.1)
    place(m, drone(36.71, 10.6, amp=0.11, a=0.5, r=1.2), 101.2)                                # the cave
    place(m, pad([shur(1, -1), shur(5, -1), shur(1)], 10.0, amp=0.05, a=0.8, r=1.0, bright=4), 101.2)
    place(m, drum(dur=2.6, f0=40, amp=0.7, noise=0.4), 104.7)
    place(m, drone(36.71, 6.4, amp=0.10, a=0.8, r=2.0), 111.4)                                 # the mountain at night
    place(m, pad([shur(0, -1), shur(4, -1), shur(0)], 6.0, amp=0.06, a=1.0, r=2.0, bright=4), 111.4)
    tanbur(m, ZTHEME[:4], 112.2, amp=0.09, low=True, step=1.1)
    place(m, bell(440, 3.0, 0.04), 116.0)
    # S7 117.6-152.0: the crown, the fires, the banner
    place(m, drum(dur=2.6, f0=46, amp=0.7, noise=0.35), 117.6)
    place(m, pad([shur(0), shur(2), shur(4), shur(0, 1)], 14.4, amp=0.08, a=1.0, r=1.5, bright=7), 117.6)
    tanbur(m, HOPE, 118.2, amp=0.15, low=True, step=0.9)
    shimmer(m, 118.0, 3.0, amp=0.02, seed=102, base=1320)
    tanbur(m, [(4, 0), (2, 0.6), (0, 1.2), (2, 1.9)], 123.8, amp=0.08, step=1.0)
    tanbur(m, [(0, 0), (2, 0.5), (4, 1.0), (5, 1.6), (7, 2.3)], 128.2, amp=0.1, low=True, step=0.9)
    for i, t in enumerate(np.arange(132.2, 146.6, 0.375)):                                     # Mehregan: drums and a dance
        place(m, drum(dur=0.5, f0=66 if i % 2 else 54, amp=0.16 + (0.08 if i % 4 == 0 else 0), noise=0.22), t)
    for k, t0 in enumerate((133.0, 136.0, 139.0, 142.0)):
        tanbur(m, DANCE, t0, amp=0.1 + 0.02 * k, low=(k % 2 == 0), step=1.0, dur=1.4)
    place(m, pad([shur(0), shur(4), shur(0, 1)], 14.0, amp=0.07, a=1.0, r=1.5, bright=6), 132.2)
    place(m, drum(dur=3.0, f0=42, amp=0.85, noise=0.4), 141.4)                                  # the banner
    place(m, pad([shur(0), shur(2), shur(4), shur(0, 1)], 5.4, amp=0.10, a=0.3, r=1.5, bright=7), 141.4)
    tanbur(m, HOPE, 141.8, amp=0.16, low=True, step=0.75)
    place(m, drum(dur=3.0, f0=40, amp=0.85, noise=0.4), END_CARD)
    place(m, drone(36.71, 5.4, amp=0.10, a=0.2, r=2.0), END_CARD)
    place(m, pad([shur(0), shur(4), shur(0, 1)], 5.2, amp=0.08, a=0.3, r=2.0, bright=6), END_CARD)
    tanbur(m, ZTHEME, END_CARD + 0.6, amp=0.13, low=True, step=0.7)


def sfx(s):
    # S1: wind on the wall; the rope; the climb
    place(s, gust(3.0, 0.06, seed=101), 0.2)
    place(s, noise_bed(7.8, amp=0.02, lo=200, hi=1400, lfo=0.15, seed=101), 0.0)
    place(s, swish(0.9, 0.09, seed=101), HOOK - 0.85)
    place(s, clink(0.12, seed=101), HOOK)
    place(s, creak(1.0, 0.05, seed=101), HOOK + 0.8)
    for k, t in enumerate((2.4, 3.0, 3.6)):
        place(s, rustle(0.04, 0.5, seed=101 + k), t, pan=0.1)
    place(s, hiss(1.2, 0.05, seed=101), 5.6, pan=-0.3); place(s, hiss(1.2, 0.05, seed=102), 6.2, pan=0.3)
    place(s, owl(0.03), 6.6, pan=-0.6)
    # S2: wind on the mountain
    place(s, gust(3.0, 0.07, seed=102), 8.0)
    # S3: the tent at night; the march; the city
    crickets(s, 12.4, 31.2, amp=0.008, seed=101)
    place(s, crackle(18.8, amp=0.05, rate=8, seed=1001), 12.4)
    place(s, hiss(1.4, 0.10, seed=103), 26.9, pan=-0.3); place(s, hiss(1.4, 0.10, seed=104), 27.1, pan=0.3)
    hooves(s, 31.2, 37.2, step=0.2, amp=0.07, pan=0.2, seed=101, gallop=True)
    place(s, murmur(11.2, 0.05, seed=101), 31.4)
    place(s, crackle(5.2, amp=0.06, rate=10, seed=1002), 37.4)
    place(s, cheer(2.2, 0.08, seed=101), 40.4)
    # S4: iron; the climb; the hall; the window
    place(s, noise_bed(12.4, amp=0.02, lo=200, hi=1400, lfo=0.15, seed=102), 42.6)
    for k, t in enumerate((43.6, 44.3, 45.6)):
        place(s, clink(0.05, seed=110 + k), t, pan=-0.2)
    place(s, hiss(1.0, 0.05, seed=105), 45.0, pan=0.2)
    place(s, thud(0.12, f0=90, seed=101), 47.4)                                               # the helmet's visor
    place(s, swish(0.9, 0.08, seed=102), HOOK2 - 0.85)
    place(s, clink(0.1, seed=102), HOOK2)
    for k, t in enumerate(np.arange(51.0, 54.8, 0.6)):
        place(s, rustle(0.035, 0.45, seed=120 + k), t, pan=0.15)
        place(s, scrape(0.3, 0.03, seed=120 + k), t + 0.2, pan=0.15)
    place(s, crackle(9.4, amp=0.05, rate=8, seed=1003), 55.0)
    place(s, noise_bed(3.8, amp=0.03, lo=200, hi=1400, lfo=0.2, seed=103), 64.4)
    place(s, scrape(0.5, 0.06, seed=130), 66.9)                                                # the dagger drawn
    place(s, swish(0.8, 0.1, seed=103), 67.5)
    # S5: the fight in the hall
    place(s, crackle(26.2, amp=0.05, rate=8, seed=1004), 68.2)
    place(s, thud(0.4, f0=60, seed=102), LAND)
    place(s, hiss(1.4, 0.12, seed=106), LAND + 0.3, pan=-0.3); place(s, hiss(1.4, 0.12, seed=107), LAND + 0.4, pan=0.3)
    place(s, gasp(0.05, seed=101), 69.2)
    steps(s, 72.2, 74.2, step=0.2, amp=0.06, seed=101, pan=0.1)
    place(s, swish(0.7, 0.14, seed=104), STRIKE - 0.66)
    place(s, clang(0.32, seed=101), STRIKE)
    place(s, thud(0.35, f0=55, seed=103), STRIKE + 0.05)
    place(s, clink(0.1, seed=103), STRIKE + 0.7); place(s, clink(0.08, seed=104), STRIKE + 1.0)       # helmet pieces, the dagger
    place(s, thud(0.3, f0=50, seed=104), STRIKE + 0.9)
    place(s, scrape(0.4, 0.05, seed=131), 80.0)
    place(s, whoosh(2.0, 0.06, seed=105), SORUSH_IN - 1.2)
    wings(s, SORUSH_IN + 0.3, n=4, rate=0.4, amp=0.04, seed=101, pan=0.2)
    place(s, scrape(0.3, 0.04, seed=132), 92.0)
    # S6: the road; the cave; the mountain
    place(s, gust(6.6, 0.05, seed=103), 94.6)
    hooves(s, 94.6, 101.0, step=0.42, amp=0.06, pan=-0.2, seed=102)
    steps(s, 95.0, 101.0, step=0.5, amp=0.03, seed=102, pan=0.3)
    place(s, noise_bed(10.2, amp=0.03, lo=100, hi=700, lfo=0.1, seed=104), 101.2)             # the cave's hollow air
    for k, t in enumerate(CHAINS):
        place(s, chain(0.08, seed=101 + k), t, pan=-0.3)
    place(s, thud(0.2, f0=60, seed=105), CHAINS[-1] + 0.1)
    place(s, hiss(1.2, 0.05, seed=108), 105.6, pan=-0.4)
    steps(s, 109.4, 111.2, step=0.45, amp=0.03, seed=103, pan=0.2)
    place(s, gust(6.0, 0.06, seed=104), 111.6)
    # S7: the hall; the fires; the banner
    place(s, murmur(5.4, 0.03, seed=102), 117.8)
    place(s, cheer(3.0, 0.06, seed=102), 120.2)
    place(s, crackle(19.8, amp=0.09, rate=14, seed=1005), 132.2)
    place(s, cheer(5.0, 0.06, seed=103), 133.4)
    place(s, cheer(3.4, 0.10, seed=104), 140.6)
    place(s, gust(4.0, 0.06, seed=105), 141.6)
    place(s, cheer(3.0, 0.05, seed=105), 145.0)


LINES = [("p10s1a", 0.6), ("p10s1b", 4.3),
         ("p10s3a", 12.8), ("p10s3b", 17.2), ("p10s3c", 22.0), ("p10s3d", 26.9), ("p10s3e", 31.5), ("p10s3f", 37.7),
         ("p10s4a", 42.9), ("p10s4b", 49.1), ("p10s4c", 55.2), ("p10s4d", 60.7), ("p10s4e", 64.7),
         ("p10s5a", 69.4), ("p10s5b", 75.6), ("p10s5c", 81.7), ("p10s5d", 85.8), ("p10s5e", 91.8),
         ("p10s6a", 94.7), ("p10s6b", 101.4), ("p10s6c", 107.4), ("p10s6d", 111.6),
         ("p10s7a", 117.9), ("p10s7b", 123.4), ("p10s7c", 127.8), ("p10s7d", 132.5), ("p10s7e", 138.3), ("p10s7f", 141.5)]
if __name__ == "__main__":
    build(10, TOTAL, music, sfx, LINES, f'{AUDIO}/part10.wav')
    print('done')
