"""Contact sheet of a few frames of one scene, to check it before rendering.
python3 prev.py babak p03_scenes s2 0.5,3,6.2   -> build/babak/prev/pv_p03_scenes_s2.png"""
import os, sys, time, importlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import series; series.from_argv()
from film import stills
mod = importlib.import_module(sys.argv[1]); name = sys.argv[2]
t0 = time.time()
shots = mod.SCENES[name]()
print("build", round(time.time() - t0, 1), "dur", sum(s.dur for s in shots))
t0 = time.time()
times = [float(x) for x in sys.argv[3].split(",")]
import os
from paths import BUILD
os.makedirs(f"{BUILD}/prev", exist_ok=True)
out = f"{BUILD}/prev/pv_{sys.argv[1]}_{name}.png"
stills(shots, times, out)
print(out)
print("frames", round((time.time() - t0) / len(times), 2), "s/frame")
