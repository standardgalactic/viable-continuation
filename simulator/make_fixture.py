"""Write simulator/trace_fixture.json from the Python companion (run from repo root)."""
import json, random, sys, pathlib
root = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root / "companion"))
from vcc import housing2 as h
rng = random.Random(2026)
cases = []
for _ in range(300):
    n = rng.randint(1, 4)
    init = [rng.randint(0, 100) for _ in range(n)]
    months = rng.randint(1, 40)
    spends = [[rng.choice([0, 100, 200, 300, 400]) for _ in range(n)] for _ in range(months)]
    ks, total = list(init), 0
    for alloc in spends:
        for i, k in enumerate(ks):
            if k >= h.HAB:
                total += h.R - h.C
            total -= alloc[i]
            ks[i] = h.step(k, alloc[i])
    cases.append({"init": init, "spends": spends, "final": ks, "total": total})
kern = {"%d,%d" % (c, s): sorted(h.kernel_hab(c, shock=s)) for c in (0, 100, 200, 300, 400) for s in (0, 1, 2)}
(pathlib.Path(__file__).parent / "trace_fixture.json").write_text(json.dumps({"cases": cases, "kernel1": kern}))
print(len(cases), "cases,", len(kern), "kernels")
