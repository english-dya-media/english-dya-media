"""Render the scenes of a part, one mp4 per scene, in parallel.
python3 render.py babak p03 s1,s2,s3 [procs]   -> build/babak/scenes/p03_s1.mp4 …  (babak/p03_scenes.py, dict SCENES)
python3 render.py babak p03 all 2"""
import importlib, multiprocessing, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import series
if __name__ == "__main__":
    series.from_argv()
from paths import SCENES


def job(args):
    part, name = args
    import paths  # puts the series folder on sys.path in the worker too
    mod = importlib.import_module(f"{part}_scenes")
    from film import render_scene
    t0 = time.time()
    rc = render_scene(mod.SCENES[name](), f"{SCENES}/{part}_{name}.mp4")
    return name, rc, round(time.time() - t0, 1)


if __name__ == "__main__":
    part = sys.argv[1]
    names = sys.argv[2].split(",") if len(sys.argv) > 2 and sys.argv[2] != "all" else list(importlib.import_module(f"{part}_scenes").SCENES)
    with multiprocessing.get_context("fork").Pool(int(sys.argv[3]) if len(sys.argv) > 3 else 2) as p:
        for r in p.imap_unordered(job, [(part, n) for n in names]):
            print(r, flush=True)
