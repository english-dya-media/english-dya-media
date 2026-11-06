"""Soft, original background bed (pad + celesta-like arpeggio), ducked under the voice.

make_music(total_seconds, voice_ranges, out_wav)
voice_ranges: list of (start, end) seconds where the pronunciation voice plays.
"""
import numpy as np
import soundfile as sf

SR = 44100
PROG = [[48, 52, 55, 59], [45, 48, 52, 55], [41, 45, 48, 52], [43, 47, 50, 52]]  # Cmaj7 Am7 Fmaj7 G6


def hz(m):
    return 440.0 * 2 ** ((m - 69) / 12)


def make_music(total, voice_ranges, out, bpm=96, level_db=-27.0, prog=None, pluck_decay=0.22, pattern=None, pad_gain=0.62):
    beat = 60.0 / bpm
    bar = 4 * beat
    n = int(total * SR)
    t = np.arange(n) / SR
    pad = np.zeros(n)
    b = 0
    while b * bar < total:
        chord, start = (prog or PROG)[b % 4], b * bar
        i0, i1 = int(start * SR), min(n, int((start + bar + 0.9) * SR))
        tt = t[i0:i1] - start
        env = np.minimum(1, tt / 0.4) * np.where(tt < bar, 1.0, np.clip(1 - (tt - bar) / 0.9, 0, 1))
        s = np.zeros_like(tt)
        for m in chord:
            f = hz(m + 12)
            s += np.sin(2 * np.pi * f * tt) + 0.45 * np.sin(2 * np.pi * f * 1.004 * tt) + 0.12 * np.sin(4 * np.pi * f * tt)
        s += 0.9 * np.sin(2 * np.pi * hz(chord[0] - 12) * tt)
        pad[i0:i1] += env * s
        b += 1
    pluck = np.zeros(n)
    eighth, pattern = beat / 2, (pattern or [0, 1, 2, 3, 2, 1, 2, 3])
    for k in range(int(total / eighth) + 1):
        start = k * eighth
        chord = (prog or PROG)[int(start // bar) % 4]
        f = hz(chord[pattern[k % 8]] + 24)
        i0 = int(start * SR)
        if i0 >= n:
            break
        i1 = min(n, i0 + int(0.9 * SR))
        tt = t[i0:i1] - start
        env = np.exp(-tt / pluck_decay) * np.minimum(1, tt / 0.004)
        pluck[i0:i1] += env * (np.sin(2 * np.pi * f * tt) + 0.25 * np.sin(4 * np.pi * f * tt) * np.exp(-tt / 0.08))
    rms = lambda x: np.sqrt(np.mean(x ** 2)) + 1e-9
    mix = pad_gain * pad / rms(pad) + (1 - pad_gain) * pluck / rms(pluck)
    mix *= (10 ** (level_db / 20)) / rms(mix)
    # duck under the voice (about -8 dB) with short ramps
    g = np.ones(n)
    for s0, s1 in voice_ranges:
        a, z = max(0, int((s0 - 0.10) * SR)), min(n, int((s1 + 0.15) * SR))
        g[a:z] = np.minimum(g[a:z], 0.4)
    k = int(0.06 * SR)
    g = np.convolve(g, np.ones(k) / k, mode="same")
    mix *= g
    fi, fo = int(0.3 * SR), int(1.6 * SR)
    mix[:fi] *= np.linspace(0, 1, fi)
    mix[-fo:] *= np.linspace(1, 0, fo)
    sf.write(out, np.clip(mix, -1, 1).astype(np.float32), SR)
    return out
