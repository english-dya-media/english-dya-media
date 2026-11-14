import numpy as np, wave, subprocess, json, math
SR = 48000
rng = np.random.default_rng(7)

def silence(dur): return np.zeros((int(dur * SR), 2), np.float32)

def env(n, a, r, sustain=True):
    e = np.ones(n, np.float32)
    na, nr = int(a * SR), int(r * SR)
    if na > 0: e[:na] = np.linspace(0, 1, na) ** 1.5
    if nr > 0: e[-nr:] *= np.linspace(1, 0, nr) ** 1.5
    return e

def onepole_lp(x, fc):
    a = math.exp(-2 * math.pi * fc / SR)
    from scipy.signal import lfilter
    return lfilter([1 - a], [1, -a], x, axis=0).astype(np.float32)

def bandpass(x, lo, hi):
    from scipy.signal import butter, sosfilt
    sos = butter(2, [lo, hi], btype="band", fs=SR, output="sos")
    return sosfilt(sos, x, axis=0).astype(np.float32)

def lowpass(x, fc, order=2):
    from scipy.signal import butter, sosfilt
    sos = butter(order, fc, btype="low", fs=SR, output="sos")
    return sosfilt(sos, x, axis=0).astype(np.float32)

def highpass(x, fc, order=2):
    from scipy.signal import butter, sosfilt
    sos = butter(order, fc, btype="high", fs=SR, output="sos")
    return sosfilt(sos, x, axis=0).astype(np.float32)

def stereo(m, pan=0.0):
    l = math.cos((pan + 1) * math.pi / 4); r = math.sin((pan + 1) * math.pi / 4)
    return np.stack([m * l, m * r], 1).astype(np.float32)

def drone(f0, dur, amp=0.18, a=3, r=3, partials=((1, 1), (2, 0.35), (1.5, 0.25), (3, 0.12))):
    n = int(dur * SR); t = np.arange(n) / SR
    out = np.zeros((n, 2), np.float32)
    for k, (m, w) in enumerate(partials):
        for ch, det in ((0, -0.15), (1, 0.15)):
            out[:, ch] += w * np.sin(2 * np.pi * (f0 * m + det) * t + k).astype(np.float32)
    lfo = 0.85 + 0.15 * np.sin(2 * np.pi * 0.07 * t)
    return out * (amp * env(n, a, r) * lfo)[:, None]

def pad(freqs, dur, amp=0.08, a=2.5, r=3, bright=6):
    n = int(dur * SR); t = np.arange(n) / SR
    out = np.zeros((n, 2), np.float32)
    for f in freqs:
        for ch, det in ((0, 0.997), (1, 1.003)):
            s = np.zeros(n, np.float32)
            for h in range(1, bright + 1):
                s += (np.sin(2 * np.pi * f * det * h * t) / h ** 1.3).astype(np.float32)
            out[:, ch] += s
    out = lowpass(out, 2200)
    return out * (amp / max(1, len(freqs)) * env(n, a, r))[:, None]

def pluck(f, dur=2.2, amp=0.35, damp=0.996, bright=0.6):
    n = int(dur * SR); N = int(SR / f)
    buf = (rng.random(N) * 2 - 1).astype(np.float32)
    buf = lowpass(buf, 2000 + 6000 * bright)
    out = np.zeros(n, np.float32)
    for i in range(n):
        j = i % N
        v = buf[j]
        out[i] = v
        buf[j] = damp * 0.5 * (v + buf[(j + 1) % N])
    out = highpass(out, 80)
    out *= np.exp(-np.arange(n) / SR * 1.3)
    return out * amp

def pluck_fast(f, dur=2.0, amp=0.35, damp=0.996):
    # vectorised Karplus-Strong via repeated averaging of the delay line
    N = max(2, int(round(SR / f)))
    reps = int(dur * SR / N) + 1
    buf = (rng.random(N) * 2 - 1).astype(np.float32)
    rows = [buf]
    for _ in range(reps - 1):
        buf = damp * 0.5 * (buf + np.roll(buf, -1)); rows.append(buf)
    out = np.concatenate(rows)[: int(dur * SR)]
    out = highpass(out, 90)
    body = bandpass(out, 180, 1400) * 0.6 + out * 0.5
    return (body * amp).astype(np.float32)

def drum(dur=1.6, f0=72, amp=0.7, noise=0.25):
    n = int(dur * SR); t = np.arange(n) / SR
    f = f0 * (1 + 0.6 * np.exp(-t * 18))
    ph = 2 * np.pi * np.cumsum(f) / SR
    body = np.sin(ph) * np.exp(-t * 3.2)
    nz = lowpass(rng.standard_normal(n).astype(np.float32), 900) * np.exp(-t * 28) * noise
    return ((body + nz) * amp).astype(np.float32)

def knock(amp=0.9):
    n = int(0.35 * SR); t = np.arange(n) / SR
    s = np.sin(2 * np.pi * 95 * t) * np.exp(-t * 24) + 0.5 * np.sin(2 * np.pi * 210 * t) * np.exp(-t * 40)
    nz = bandpass(rng.standard_normal(n).astype(np.float32), 200, 2500) * np.exp(-t * 60) * 0.6
    return ((s + nz) * amp).astype(np.float32)

def bell(f=620, dur=2.5, amp=0.12):
    n = int(dur * SR); t = np.arange(n) / SR
    s = sum(w * np.sin(2 * np.pi * f * m * t) * np.exp(-t * d) for m, w, d in ((1, 1, 2.2), (2.76, 0.5, 3.5), (5.4, 0.25, 6), (8.9, 0.12, 9)))
    return (s * amp).astype(np.float32)

def noise_bed(dur, kind="wind", amp=0.1, lo=150, hi=1200, lfo=0.12, seed=0):
    r = np.random.default_rng(seed)
    n = int(dur * SR); t = np.arange(n) / SR
    out = np.zeros((n, 2), np.float32)
    for ch in range(2):
        x = r.standard_normal(n).astype(np.float32)
        x = bandpass(x, lo, hi)
        mod = 0.6 + 0.4 * np.sin(2 * np.pi * lfo * t + ch + seed) * np.sin(2 * np.pi * lfo * 0.37 * t + 2 * ch)
        out[:, ch] = x * mod
    out /= (np.abs(out).max() + 1e-6)
    return out * amp * env(n, 1.0, 1.0)[:, None]

def crackle(dur, amp=0.25, rate=14, seed=1):
    r = np.random.default_rng(seed)
    n = int(dur * SR); out = np.zeros(n, np.float32)
    k = int(dur * rate)
    for p in r.integers(0, n - 2000, k):
        L = int(r.uniform(80, 900)); a = r.uniform(0.2, 1.0)
        out[p:p + L] += (r.standard_normal(L) * np.exp(-np.arange(L) / (L / 4)) * a).astype(np.float32)
    base = lowpass(r.standard_normal(n).astype(np.float32), 500) * 0.25
    return stereo(highpass(out, 600) * amp + base * amp * 0.5, 0)

def reverb(x, secs=2.4, wet=0.28, seed=3):
    r = np.random.default_rng(seed)
    n = int(secs * SR); t = np.arange(n) / SR
    from scipy.signal import fftconvolve
    out = np.zeros_like(x)
    for ch in range(2):
        ir = (r.standard_normal(n) * np.exp(-t * 3.0 / secs * 2.3)).astype(np.float32)
        ir = lowpass(ir, 5000); ir /= np.sqrt((ir ** 2).sum())
        out[:, ch] = fftconvolve(x[:, ch], ir)[: len(x)].astype(np.float32)
    return x * (1 - wet) + out * wet * 1.6

def place(buf, sig, t, gain=1.0, pan=0.0):
    if sig.ndim == 1: sig = stereo(sig, pan)
    i = int(t * SR); j = min(len(buf), i + len(sig))
    if i >= len(buf): return
    buf[i:j] += sig[: j - i] * gain

def read_wav(path):
    with wave.open(path, "rb") as w:
        sr = w.getframerate(); x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
        ch = w.getnchannels()
    if ch > 1: x = x.reshape(-1, ch).mean(1)
    assert sr == SR, sr
    return x

def write_wav(path, x):
    x = np.clip(x, -1, 1)
    with wave.open(path, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((x * 32767).astype(np.int16).tobytes())

# Shur-like scale on D (koron second)
D3 = 146.83
def shur(deg, octave=0):
    cents = [0, 150, 300, 500, 700, 800, 1000, 1200]
    o, d = divmod(deg, 7)
    return D3 * 2 ** ((cents[d] + 1200 * (o + octave)) / 1200)
