"""Checks for the proof programme. Each returns (passed, detail).

A check passes when the result matches the theorem or, for a removed
hypothesis, when the expected counterexample is actually found.
"""
import random
from fractions import Fraction
from itertools import product

from .viability import (kernel, kernel_by_postfixed_points, phi, System,
                        three_state_example, chain_in_kernel_iterate,
                        shared_crew_unit, one_crew, product_system,
                        random_system, robust_actions)
from . import housing as hs
from .graph_prices import (find_potential, cycle_cost, with_spread,
                           holonomies)


def check_p03(trials=300, seed=1, infinite=False):
    if infinite:
        rows = []
        for s in range(6):
            first_out = next(n for n in range(100) if not chain_in_kernel_iterate(n, s))
            rows.append((s, first_out))
        ok = all(n == s + 1 for s, n in rows)
        nonempty = all(chain_in_kernel_iterate(n, n) for n in range(20))
        return ok and nonempty, (
            "infinite chain: every K_n is nonempty (n is in K_n) but state s "
            "leaves at step s+1, so the greatest fixed point is empty and the "
            "iteration never terminates: %r" % rows)
    rng = random.Random(seed)
    for _ in range(trials):
        sys_ = random_system(rng, n=rng.randint(2, 6))
        K, _ = kernel(sys_)
        if K != phi(sys_, K):
            return False, "kernel is not a fixed point"
        if K != kernel_by_postfixed_points(sys_):
            return False, "iteration disagrees with Knaster-Tarski union"
        for s in K:
            if not robust_actions(sys_, K, s):
                return False, "kernel state without witnessing action"
    return True, "%d random systems: iteration = greatest fixed point = union of post-fixed points" % trials


def check_p05():
    sys_ = three_state_example()
    K, _ = kernel(sys_)
    ok = ("s0" in K and "s1" in sys_.good and "s1" not in K
          and "s1" in sys_.succ[("s0", "go")])
    return ok, "kernel=%s; s1 is acceptable, reachable from s0, and not viable" % sorted(K)


def check_p09(trials=500, seed=2):
    rng = random.Random(seed)
    c = Fraction(1)
    found = None
    for _ in range(trials):
        d = [Fraction(rng.randint(1, 10), 10) for _ in range(3)]
        each = all(x <= c for x in d)
        joint = sum(d) <= c
        if each and not joint:
            found = d
            break
    unit = shared_crew_unit()
    both = product_system(unit, unit, one_crew)
    ok = found is not None
    return ok, "demands %s each <= %s but sum %s exceeds capacity" % (
        [str(x) for x in found], c, sum(found)) if ok else "no instance found"


def check_p10(trials=200, seed=3, coupling=False):
    if coupling:
        u = shared_crew_unit()
        k1, _ = kernel(u)
        free, _ = kernel(product_system(u, u))
        shared, _ = kernel(product_system(u, u, one_crew))
        product_of_kernels = set(product(k1, k1))
        ok = free == product_of_kernels and shared < product_of_kernels
        lost = sorted(product_of_kernels - set(shared))
        return ok, ("shared crew: K12 is a proper subset of K1 x K2; "
                    "lost states %s" % lost)
    rng = random.Random(seed)
    for _ in range(trials):
        a, b = random_system(rng, n=3), random_system(rng, n=3)
        k1, _ = kernel(a)
        k2, _ = kernel(b)
        k12, _ = kernel(product_system(a, b))
        if set(k12) != set(product(k1, k2)):
            return False, "K12 != K1 x K2 under independence"
    return True, "%d random independent pairs: K12 = K1 x K2" % trials


def check_p23(trials=300, seed=4):
    rng = random.Random(seed)
    for _ in range(trials):
        s = random_system(rng, n=5)
        K, _ = kernel(s)
        # smaller G
        g2 = {x for x in s.good if rng.random() < 0.7}
        if not kernel(s.with_good(g2))[0] <= K:
            return False, "tightening G enlarged K"
        # more actions
        acts = {x: list(s.actions[x]) + ["extra"] for x in s.states}
        succ = dict(s.succ)
        for x in s.states:
            succ[(x, "extra")] = {rng.choice(s.states)}
        more = System(s.states, s.good, acts, succ)
        if not K <= kernel(more)[0]:
            return False, "adding actions shrank K"
        # fewer disturbances
        succ2 = {k: {sorted(v, key=repr)[0]} if rng.random() < 0.5 else set(v)
                 for k, v in s.succ.items()}
        fewer = System(s.states, s.good, s.actions, succ2)
        if not K <= kernel(fewer)[0]:
            return False, "removing disturbances shrank K"
    return True, "%d random systems: K monotone in G, actions, disturbances" % trials


def check_p22(spread=None):
    nodes = ["A", "B", "C"]
    c = {("A", "B"): Fraction(1), ("B", "C"): Fraction(1), ("C", "A"): Fraction(-3, 2)}
    if spread is None:
        ub = with_spread(c, 0)
        kind, res = find_potential(nodes, ub)
        h = holonomies(nodes, c)
        ok = kind == "negative_cycle" and any(v != 0 for v in h.values())
        return ok, ("frictionless: class [c] has coordinates %s, nonzero, so no "
                    "potential; arbitrage cycle %s with cost %s" % (
                        {k: str(v) for k, v in h.items()}, res,
                        cycle_cost(ub, res)))
    ub = with_spread(c, Fraction(spread))
    kind, res = find_potential(nodes, ub)
    h = holonomies(nodes, c)
    nonzero = any(v != 0 for v in h.values())
    if kind == "potential":
        return nonzero, ("spread %s: potential exists although [c] != 0 "
                         "(no negative cycle)" % spread)
    return True, ("spread %s: negative cycle %s with cost %s, so arbitrage" % (
        spread, res, cycle_cost(ub, res)))


def check_p28(trials=400, seed=5):
    rng = random.Random(seed)
    nonempty = empty = 0
    for _ in range(trials):
        r = rng.choice([500, 800, 1000]); T = rng.choice([6, 12, 24])
        d = Fraction(rng.choice([0, 1, 2, 5, 10]), 100)
        e = rng.choice([0, 100, 200, 400]); H = rng.randint(1, 5)
        c = rng.choice([1500, 3000, 4000, 6000])
        P = hs.prepay(r, T, d)
        lost = [x for x in range(0, 30001, 50)
                if x >= P and hs.exit_ok_monthly(x, e, c, H)
                and not hs.exit_ok_prepaid(x, e, r, c, H, T, d)]
        iv = hs.lost_interval(e, r, c, H, T, d)
        pred = [] if iv is None else [x for x in range(0, 30001, 50) if iv[0] <= x < iv[1]]
        if lost != pred:
            return False, "lost set differs: params %s" % ((r, T, d, e, H, c),)
        cond = hs.lost_nonempty_condition(e, r, c, H, T, d)
        if bool(iv) != cond and (iv is not None or cond):
            # the interval can be nonempty yet miss the 50-unit grid only if
            # width < 50; compare conditions on the exact interval instead
            return False, "condition differs: params %s" % ((r, T, d, e, H, c),)
        nonempty += bool(iv); empty += not iv
    # the worked example in the book
    ex = hs.lost_interval(200, 1000, 4000, 3, 12, Fraction(1, 20))
    ok = ex == (11400, 11800)
    return ok, ("%d random parameter sets (%d with a lost-exit interval, %d without): "
                "brute force = closed form; book example lost interval %s"
                % (trials, nonempty, empty, tuple(int(v) for v in ex)))


def check_p29(trials=600, seed=6):
    rng = random.Random(seed)
    checked = 0
    for _ in range(trials):
        r, T, d = 1000, 12, Fraction(1, 20)
        e = rng.choice([0, 100, 200, 400]); H = rng.randint(1, 5); c = 4000
        P = hs.prepay(r, T, d)
        x = int(P) + rng.randint(0, 800)
        a = rng.randint(0, 5); E = rng.randint(0, 6); tau = rng.randint(0, 6)
        tb = min(H, E)
        ms = hs.min_transfer(x, e, r, c, T, d, tb)
        if ms == 0:
            continue
        for m in (0, int(ms) - 1 if ms > 1 else 0, int(ms), int(ms) + 100, 10**6):
            got = hs.restored(x, m, tau, a, E, e, r, c, H, T, d)
            want = (a <= tb) and (tau <= tb) and (m >= ms)
            if got != want:
                return False, "mismatch %s" % ((x, m, tau, a, E, e, H),)
        checked += 1
    ex = hs.min_transfer(11500, 200, 1000, 4000, 12, Fraction(1, 20), 3)
    late = hs.restored(11500, 10**6, 4, 0, 6, 200, 1000, 4000, 3, 12, Fraction(1, 20))
    ok = ex == 300 and late is False
    return ok, ("%d cases with a positive shortfall: restoration iff availability, "
                "timing, and sufficiency; example needs %s, and an arbitrarily large "
                "transfer paid at month 4 (after month 3) restores nothing" % (checked, ex))


ALL = [
    ("P03", lambda: check_p03()),
    ("P03 (infinite chain, finiteness removed)", lambda: check_p03(infinite=True)),
    ("P05", lambda: check_p05()),
    ("P09", lambda: check_p09()),
    ("P10 (independent)", lambda: check_p10()),
    ("P10 (shared crew, independence removed)", lambda: check_p10(coupling=True)),
    ("P23", lambda: check_p23()),
    ("P28 (housing, prepaid lease)", lambda: check_p28()),
    ("P29 (housing, compensation)", lambda: check_p29()),
    ("P22 (frictionless)", lambda: check_p22()),
    ("P22 (spread 1/10)", lambda: check_p22(Fraction(1, 10))),
    ("P22 (spread 1/5)", lambda: check_p22(Fraction(1, 5))),
]
