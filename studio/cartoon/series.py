"""Helpers to pick the series before anything else is imported.
Entry scripts:  import series; series.from_argv()      (python3 render.py babak p03 all  ->  SERIES=babak)
Series scripts: import series; series.from_folder(__file__)"""
import json, os, sys

ENGINE = os.path.dirname(os.path.abspath(__file__))


def _set(name):
    os.environ["SERIES"] = name
    if ENGINE not in sys.path:
        sys.path.insert(0, ENGINE)
    d = os.path.join(ENGINE, name)
    if not os.path.isdir(d):
        raise SystemExit(f"unknown series '{name}' (no folder {d})")
    if d not in sys.path:
        sys.path.insert(0, d)
    return name


def from_argv():
    if len(sys.argv) < 2:
        raise SystemExit(f"usage: {os.path.basename(sys.argv[0])} <series> …")
    return _set(sys.argv.pop(1))


def from_folder(path):
    return _set(os.path.basename(os.path.dirname(os.path.abspath(path))))


def config(name=None):
    name = name or os.environ["SERIES"]
    return json.load(open(os.path.join(ENGINE, name, "parts.json"), encoding="utf-8"))


def queue():
    return json.load(open(os.path.join(ENGINE, "queue.json"), encoding="utf-8"))
