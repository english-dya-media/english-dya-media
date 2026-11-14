import sys, json, numpy as np, subprocess
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paths import VOICES_DIR
from audio import *

def build(part, total, cues_music, cues_sfx, lines, out):
    mus = silence(total); sfx = silence(total); vox = silence(total)
    cues_music(mus); cues_sfx(sfx)
    for lid, t in lines:
        v = read_wav(f'{VOICES_DIR}/{lid}.wav')
        place(vox, v, t, gain=0.95, pan=0.0)
    vox = reverb(vox, secs=0.9, wet=0.10, seed=5)
    mus = reverb(mus, secs=2.8, wet=0.32, seed=2)
    # duck music under voice
    e = np.abs(vox).mean(1)
    k = int(0.25 * SR)
    e = np.convolve(e, np.ones(k) / k, mode='same')
    e = np.clip(e / (e.max() + 1e-6) * 3, 0, 1)
    mus *= (1 - 0.5 * e)[:, None]
    sfx *= (1 - 0.35 * e)[:, None]
    mix = mus * 0.85 + sfx + vox
    write_wav(out + '.raw.wav', mix / (np.abs(mix).max() + 1e-6) * 0.9)
    subprocess.run(['ffmpeg', '-y', '-hide_banner', '-loglevel', 'error', '-i', out + '.raw.wav',
                    '-af', 'loudnorm=I=-14:TP=-1.5:LRA=11', '-ar', '48000', '-c:a', 'pcm_s16le', out], check=True)
