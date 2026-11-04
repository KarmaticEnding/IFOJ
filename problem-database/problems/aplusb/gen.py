"""Deterministic data generator and native tuack.dmk hooks for A + B."""
from pathlib import Path

DATA = [
    (0, 0), (1, 2), (-1, 1), (-5, -8), (0, 1000000000),
    (1000000000, 0), (1000000000, 1000000000),
    (-1000000000, -1000000000), (-1000000000, 1000000000),
    (1000000000, -1000000000), (-1000000000, 0),
    (0, -1000000000), (999999999, 1), (-999999999, -1),
    (123456789, 987654321), (-123456789, -987654321),
    (314159265, -271828182), (-765432100, 123456789),
    (42, -43), (-999999999, 999999998),
]
SAMPLES = [(1, 2), (-5, 8), (1000000000, 1000000000)]
PRE = [(0, 0), (-1000000000, 1000000000)]
DATASETS = {"data": DATA, "down": SAMPLES, "pre": PRE}


def gen(fin, args, cont):
    """Native tuack.dmk input generator (case identifiers are one based)."""
    a, b = DATASETS[cont["folder"]][int(cont["case"]) - 1]
    fin.write(f"{a} {b}\n")


def vali(fout, args, cont, fin):
    """Native tuack.dmk validator; require the declared bounds and layout."""
    fin.int(args["min_value"], args["max_value"])
    fin.int(args["min_value"], args["max_value"], end="\n")


def std(fout, args, cont, fin):
    a, b = map(int, fin.readline().split())
    fout.write(f"{a + b}\n")


def generate():
    root = Path(__file__).resolve().parent
    for folder, pairs in DATASETS.items():
        (root / folder).mkdir(exist_ok=True)
        for index, (a, b) in enumerate(pairs, 1):
            assert -10**9 <= a <= 10**9 and -10**9 <= b <= 10**9
            (root / folder / f"{index}.in").write_text(f"{a} {b}\n", encoding="utf-8")
            (root / folder / f"{index}.ans").write_text(f"{a + b}\n", encoding="utf-8")


if __name__ == "__main__":
    generate()
