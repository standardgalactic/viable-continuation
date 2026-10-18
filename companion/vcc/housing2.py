"""Housing model v2: physical condition, maintenance, and a shared repair crew.

Parameters come from spec/housing_v2.json (see docs/HOUSING_V2_SPEC.md); the
text below describes their current values.


Condition k is measured in tenths of a condition point (integers), 0..100.
A unit is habitable (rent is collected, the state is acceptable) iff k >= 40.
Monthly deterioration d(k): 1 tenth if k > 80, 2 tenths if 50 < k <= 80,
4 tenths if k <= 50. Maintenance spending M (currency per month, multiples of
100) restores M/100 tenths. Rent r = 1000, running cost C = 300. The crew can
supply at most CAP = 400 of maintenance per month across all units it serves.
"""
from itertools import product

from .spec import CORE as _C

R, C, CAP, HAB, KMAX = (_C["rent"], _C["running_cost"], _C["crew_ceiling"],
                        _C["k_lettable_min"], _C["k_max"])
_TIERS = _C["deterioration_tiers"]


def d(k):
    for t in _TIERS:
        if t["k_above"] is None or k > t["k_above"]:
            return t["d"]


def step(k, M):
    return max(0, min(KMAX, k - d(k) + M // 100))


def habitable_months(k0, M=0):
    """Number of rent months (months t = 0, 1, ... with k_t >= HAB) when the
    unit receives constant maintenance M."""
    k, n = k0, 0
    while k >= HAB:
        n += 1
        k = step(k, M)
        if n > 10000:
            return None  # holds forever
    return n


def surplus_deferral(k0=90):
    n = habitable_months(k0, 0)
    return n, n * (R - C)


def restore_cost(k_from, k_to=90):
    """Cost of restoring from k_from to k_to ignoring concurrent decay:
    1000 per condition point, i.e. 100 per tenth."""
    return (k_to - k_from) * 100


def holds_forever(k, cap=CAP):
    return d(k) * 100 <= cap


def fail_time_one(k0, cap=CAP):
    """Max number of rent months for one unit under a total cap (best policy).
    Returns None if viable forever. Exhaustive search over policies by
    dynamic programming on k (the unit is the only user)."""
    best = {}

    def f(k, depth):
        if k < HAB:
            return 0
        if depth > 400:
            return None
        res = 0
        for M in range(0, cap + 1, 100):
            nk = step(k, M)
            v = f(nk, depth + 1) if nk != k else None
            if v is None:
                return None
            res = max(res, 1 + v)
        return res
    return f(k0, 0)


def kernel2(cap=CAP):
    """Greatest fixed point on pairs (k1, k2) with allocation M1 + M2 <= cap."""
    states = {(a, b) for a in range(HAB, KMAX + 1) for b in range(HAB, KMAX + 1)}
    allocs = [(m1, m2) for m1 in range(0, cap + 1, 100)
              for m2 in range(0, cap + 1, 100) if m1 + m2 <= cap]
    while True:
        new = set()
        for (a, b) in states:
            for (m1, m2) in allocs:
                s2 = (step(a, m1), step(b, m2))
                if s2 in states:
                    new.add((a, b))
                    break
        if new == states:
            return states
        states = new


def kernel1(cap=CAP):
    states = set(range(HAB, KMAX + 1))
    allocs = range(0, cap + 1, 100)
    while True:
        new = {k for k in states if any(step(k, M) in states for M in allocs)}
        if new == states:
            return states
        states = new


def max_joint_delay(a, b, cap=CAP):
    """Longest time until the first unit falls below HAB under the best
    allocation (exhaustive search, horizon 60)."""
    allocs = [(m1, m2) for m1 in range(0, cap + 1, 100)
              for m2 in range(0, cap + 1, 100) if m1 + m2 <= cap]
    memo = {}

    def f(a, b, t):
        if a < HAB or b < HAB:
            return t
        if t >= 60:
            return t
        key = (a, b, t)
        if key in memo:
            return memo[key]
        v = max(f(step(a, m1), step(b, m2), t + 1) for m1, m2 in allocs)
        memo[key] = v
        return v
    return f(a, b, 0)


def k_after(n, M=0, k0=90):
    k = k0
    for _ in range(n):
        k = step(k, M)
    return k


def deferral_net(n, k0=90):
    """Net value of deferring maintenance (M = 0 instead of 100) for n months
    and then restoring: saved spending minus restoration cost."""
    return 100 * n - restore_cost(k_after(n, 0, k0), k0)


def habitable_months_defect(k0, extra_tier2=0, M=0):
    """As habitable_months, but deterioration in the middle tier (50 < k <= 80)
    is increased by extra_tier2 tenths (a hidden defect left by a contractor)."""
    k, n = k0, 0
    while k >= HAB:
        n += 1
        dd = d(k) + (extra_tier2 if 50 < k <= 80 else 0)
        k = max(0, min(KMAX, k - dd + M // 100))
        if n > 10000:
            return None
    return n


def viable_threshold(budget):
    """Smallest condition k such that k and every k' >= k can be held forever
    with a maintenance budget ceiling `budget` (None if no state is viable)."""
    ks = [k for k in range(HAB, KMAX + 1) if d(k) * 100 <= budget]
    return min(ks) if ks else None


def kernel_hab(cap, hab=HAB, shock=0):
    """Robust kernel of one unit with maintenance ceiling cap, lettable
    threshold hab, and an adversarial extra deterioration of 0..shock tenths."""
    states = set(range(hab, KMAX + 1))
    while True:
        new = {k for k in states
               if any(all(max(step(k, M) - w, 0) in states for w in range(shock + 1))
                      for M in range(0, cap + 1, 100))}
        if new == states:
            return states
        states = new


def survival_chain(cap):
    """K_0 = G and K_{n+1} = states with an action whose successor lies in K_n."""
    Kn = [set(range(HAB, KMAX + 1))]
    while True:
        nxt = {k for k in Kn[-1]
               if any(step(k, M) in Kn[-1] for M in range(0, cap + 1, 100))}
        Kn.append(nxt)
        if nxt == Kn[-2]:
            return Kn[:-1]


def reach_target(cap, target):
    """States (lettable throughout) from which condition `target` is reached."""
    R = set(range(target, KMAX + 1))
    while True:
        new = R | {k for k in range(HAB, KMAX + 1)
                   if any(step(k, M) in R for M in range(0, cap + 1, 100))}
        if new == R:
            return R
        R = new


def rank_to(target, cap, k):
    """Fewest months to reach `target` from k, or None."""
    n = 0
    seen = set()
    layer = {k}
    while layer:
        if any(x >= target for x in layer):
            return n
        seen |= layer
        layer = {step(x, M) for x in layer for M in range(0, cap + 1, 100)
                 if step(x, M) >= HAB} - seen
        n += 1
    return None


def both_reach(a, b, target, cap=CAP, horizon=60):
    allocs = [(m1, m2) for m1 in range(0, cap + 1, 100)
              for m2 in range(0, cap + 1, 100) if m1 + m2 <= cap]
    frontier, seen, t = {(a, b)}, {(a, b)}, 0
    while frontier and t <= horizon:
        if any(x >= target and y >= target for x, y in frontier):
            return t
        t += 1
        nxt = set()
        for (x, y) in frontier:
            for m1, m2 in allocs:
                s = (step(x, m1), step(y, m2))
                if s[0] >= HAB and s[1] >= HAB and s not in seen:
                    seen.add(s)
                    nxt.add(s)
        frontier = nxt
    return None


# ---------------- building of several units (Parts IV and V) ----------------
BUILDING = (90, 70, 55, 50)


def hold_cost(k):
    return d(k) * 100


def simulate_building(ks, alloc, months):
    """Constant allocation per unit (tuple of spends). Returns
    (cumulative surplus, lettable units at the end, final conditions,
    lettable unit-months)."""
    ks = list(ks)
    surplus = 0
    lettable_months = 0
    for _ in range(months):
        for i, k in enumerate(ks):
            if k >= HAB:
                surplus += (R - C)
                lettable_months += 1
            surplus -= alloc[i]
            ks[i] = step(k, alloc[i])
    return surplus, sum(1 for k in ks if k >= HAB), tuple(ks), lettable_months


def backlog(ks, target=90):
    """Cost of restoring each unit to `target`, ignoring decay during repair."""
    return sum(max(0, target - k) * 100 for k in ks)


def allocations(cap=CAP, n=4):
    out = []
    def rec(i, left, cur):
        if i == n:
            out.append(tuple(cur)); return
        for m in range(0, left + 1, 100):
            rec(i + 1, left - m, cur + [m])
    rec(0, cap, [])
    return out


def months_to_restore(k0, target, ceiling):
    """Months of full spending at `ceiling` to bring a unit from k0 to target,
    and the total spent. None if the condition never rises."""
    k, n, spent = k0, 0, 0
    while k < target:
        nk = step(k, ceiling)
        if nk <= k and n > 0 and nk == k and d(k) * 100 >= ceiling:
            return None
        if nk <= k:
            return None
        spent += ceiling
        k = nk
        n += 1
        if n > 1000:
            return None
    return n, spent
