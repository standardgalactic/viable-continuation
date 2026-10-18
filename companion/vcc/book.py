"""Hand-calculated numbers that appear in the chapters, recomputed exactly.

Each entry is (chapter, description, thunk returning True). The registry is
run by checks.check_book(). A failing entry means the text and the code
disagree and one of them must be corrected. These are arithmetic checks of
worked examples, not evidence about any real population."""
from fractions import Fraction as F
from . import housing2 as h2
from . import housing as hs

ENTRIES = []


def reg(ch, desc):
    def deco(fn):
        ENTRIES.append((ch, desc, fn))
        return fn
    return deco


# ---------------- Part I ----------------
@reg(1, "deferral over 28 months: surplus 19600, restoration 5200 vs 2800 saved")
def _():
    return h2.surplus_deferral() == (28, 19600) and h2.restore_cost(38) == 5200 \
        and 28 * 100 == 2800 and h2.deferral_net(15) == -500


@reg(2, "cash example: 500 + 1200 - 1000 = 700; 900 after income at -300")
def _():
    return 500 + 1200 - 1000 == 700 and -300 + 1200 == 900


def months_to_exit(x, e, c):
    t = 0
    while x + t * e < c:
        t += 1
    return t


@reg(3, "exit date: 3000 -> month 5, 3400 -> month 3, exit needs 4000")
def _():
    return months_to_exit(3000, 200, 4000) == 5 and months_to_exit(3400, 200, 4000) == 3


@reg(4, "search 150 + move 400 = 550; saving 200; payback 11/4; budget 500 leaves 350 < 400")
def _():
    return 150 + 400 == 550 and F(550, 200) == F(11, 4) and 500 - 150 == 350 < 400


@reg(5, "owner 3 x 700 = 2100 > 1500; longest protection for 1500 is 2 months")
def _():
    return 3 * 700 == 2100 > 1500 and max(m for m in range(10) if m * 700 <= 1500) == 2


# ---------------- Part II ----------------
@reg(6, "transition trace: surplus 600 (M=100) and 700 (M=0); defect 18 vs 13 months, loss 3500 vs saving 600")
def _():
    trace0 = [h2.k_after(n, 0) for n in range(4)]
    trace100 = [h2.k_after(n, 100) for n in range(4)]
    pi = lambda k, M: (h2.R - h2.C) * (k >= h2.HAB) - M
    a = h2.habitable_months_defect(80, 0)
    b = h2.habitable_months_defect(80, 1)
    return trace0 == [90, 89, 88, 87] and trace100 == [90] * 4 and pi(90, 100) == 600 \
        and pi(90, 0) == 700 and pi(38, 300) == -300 \
        and (a, b) == (18, 13) and (a - b) * 700 == 3500 and 3000 - 2400 == 600


def _run(k0, plan, T):
    k, n, tot = k0, 0, 0
    for t in range(T):
        if k >= h2.HAB:
            M = plan(t, k)
            n += 1
            tot += (h2.R - h2.C) - M
            k = h2.step(k, M)
    return n, tot, k


@reg(7, "identical unit at 60: full ceiling 36 months 18000; ceiling 100 14 months 8400; vendor exits at 12: 20 months 11600")
def _():
    full = _run(60, lambda t, k: h2.d(k) * 100, 36)
    low = _run(60, lambda t, k: 100, 36)
    vend = _run(60, lambda t, k: h2.d(k) * 100 if t < 12 else 0, 36)
    ex = _run(60, lambda t, k: h2.d(k) * 100 if t < 24 else 0, 36)
    return (full == (36, 18000, 60) and low == (14, 8400, 38) and vend == (20, 11600, 38)
            and ex == (24 + h2.habitable_months(60, 0), 24 * 500 + h2.habitable_months(60, 0) * 700, 38))


@reg(8, "thresholds 81/51/40; deferral safe through months 9/24/24/27; sqrt backlog")
def _():
    th = {b: h2.viable_threshold(b) for b in (0, 100, 199, 200, 399, 400)}
    ok = th == {0: None, 100: 81, 199: 81, 200: 51, 399: 51, 400: 40}
    ok = ok and all(min(h2.kernel1(b), default=None) == th[b] for b in th)
    last = {}
    for cap in (100, 200, 300, 400):
        K = h2.kernel1(cap)
        n = 0
        while h2.k_after(n + 1, 0) in K:
            n += 1
        last[cap] = (n, h2.k_after(n, 0))
    ok = ok and last == {100: (9, 81), 200: (24, 52), 300: (24, 52), 400: (27, 42)}
    D = lambda t: (1 + t) ** F(1, 2) - 1
    return ok and D(15) == 3 and D(99) == 9 and D(9999) == 99


@reg(9, "unit at 55: I=3500, I'=3700; act 600, wait 828, q* 40/69, dependent 414, forced 216, no-decay 900")
def _():
    beta = F(9, 10)
    X = (2000, 6000)
    I = 100 * (90 - 55)
    I2 = 100 * (90 - h2.k_after(1, 0, 55))
    mu = F(sum(X), 2)
    act = (mu - I) + 100
    opt = sum(F(1, 2) * max(x - I2, 0) for x in X)
    wait = beta * F(4, 5) * opt
    qstar = act / (beta * opt)
    dep = beta * (F(1, 2) * F(2, 5) * max(6000 - I2, 0))
    forced = beta * F(4, 5) * (mu - I2)
    nodecay = beta * F(4, 5) * sum(F(1, 2) * max(x - I, 0) for x in X)
    return (I, I2, act, opt, wait, qstar, dep, forced, nodecay) == \
        (3500, 3700, 600, 1150, 828, F(40, 69), 414, 216, 900) \
        and act / (beta * sum(F(1, 2) * max(x - I, 0) for x in X)) == F(8, 15) \
        and (800 / (beta * opt)) == F(160, 207)


@reg(10, "abandonment L = 2850, private 500, community 2350; replacement residual 550; bond example 2500")
def _():
    L = 2000 + 550 + 300
    a = 500
    profit, L2 = 1000, 3000
    return L == 2850 and min(L, a) == 500 and L - min(L, a) == 2350 and 400 + 150 == 550 \
        and 5200 - min(L, a) == 4700 and 5200 - L == 2350 \
        and profit - min(L2, a) == 500 and profit - L2 == -2000 and L2 - a == 2500 \
        and profit - min(L2, a + 2500) == -2000


# ---------------- Part III ----------------
def feasible_deadlines(duties, supplies):
    """duties: list of (deadline, cost); supplies: list of (date, amount) incl. initial cash at 0.
    Necessary and sufficient: for each deadline T, cost due by T <= supply received by T."""
    for T, _ in duties:
        due = sum(c for t, c in duties if t <= T)
        have = sum(a for t, a in supplies if t <= T)
        if due > have:
            return False
    return True


@reg(11, "deadline feasibility: cash 2500 passes, 2400 fails; cumulative 600/1500/3500")
def _():
    duties = [(3, 600), (14, 900), (30, 2000)]
    cum = [sum(c for t, c in duties if t <= T) for T, _ in duties]
    return cum == [600, 1500, 3500] and feasible_deadlines(duties, [(0, 2500), (30, 1000)]) \
        and not feasible_deadlines(duties, [(0, 2400), (30, 1000)])


@reg(12, "safe degradation: with a restoration-to-60 duty the safe set is 51..100, A_K(52) = M >= 100")
def _():
    R = h2.reach_target(400, 60)
    AK = [M for M in range(0, 401, 100) if h2.step(52, M) in R]
    return min(R) == 51 and 50 not in R and AK == [100, 200, 300, 400] and h2.step(52, 0) == 50


@reg(13, "P04/P05/P23 on one unit; robust threshold 51; shock probability 109e-12")
def _():
    t = {hab: min(h2.kernel_hab(100, hab)) for hab in (40, 60, 85)}
    ok4 = t == {40: 81, 60: 81, 85: 85}
    K100, K200, K400 = (h2.kernel_hab(c) for c in (100, 200, 400))
    ok23 = K100 < K200 < K400 and (min(K100), min(K200), min(K400)) == (81, 51, 40)
    ok5 = 70 in range(40, 101) and 70 not in K100 and h2.k_after(20) == 60 and h2.k_after(11) == 78
    rob = min(h2.kernel_hab(400, 40, shock=1)) == 51
    from math import comb
    p = F(1, 10)
    pr = sum(comb(12, j) * p ** j * (1 - p) ** (12 - j) for j in (11, 12))
    return ok4 and ok23 and ok5 and rob and pr == F(109, 10 ** 12)


@reg(14, "restoration rank: 5 months from 51 to 60 at +2 per month; two units cannot both reach 60 from (51,51)")
def _():
    ranks = {k: h2.rank_to(60, 400, k) for k in (51, 52, 55, 58, 59)}
    return ranks == {51: 5, 52: 4, 55: 3, 58: 1, 59: 1} and h2.rank_to(60, 400, 50) is None \
        and h2.both_reach(51, 51, 60) is None


@reg(15, "lookahead depth: survival chain stabilizes at 34 steps; 12-month review certifies k >= 59")
def _():
    ch = h2.survival_chain(100)
    return len(ch) - 1 == 34 and min(ch[34]) == 81 and min(ch[12]) == 59 and min(ch[1]) == 43 \
        and all(ch[i] != ch[i + 1] for i in range(34)) \
        and min(h2.kernel_hab(300)) == 51 and min(h2.kernel_hab(400)) == 40


# ---------------- Part IV ----------------
def _pareto(ks=h2.BUILDING, months=24):
    res = {}
    for a in h2.allocations():
        sp, l, fin, _ = h2.simulate_building(ks, a, months)
        res[a] = (sp, l, -h2.backlog(fin))
    dom = lambda x, y: all(p >= q for p, q in zip(x, y)) and x != y
    front = [a for a in res if not any(dom(res[b], res[a]) for b in res)]
    return res, front


@reg(16, "70 allocations, 3 Pareto plans; weighted totals 63800 / 84600 / 65200; building start 9500, 900 vs 400")
def _():
    res, front = _pareto()
    B = h2.BUILDING
    zero = h2.simulate_building(B, (0, 0, 0, 0), 24)
    w = lambda a: res[a][0] + 20000 * res[a][1] + res[a][2]
    fr = sorted(front)
    return len(res) == 70 and fr == [(0, 100, 200, 0), (0, 200, 200, 0), (100, 100, 200, 0)] \
        and [res[a] for a in fr] == [(45300, 2, -21500), (42900, 3, -18300), (42900, 2, -17700)] \
        and [w(a) for a in fr] == [63800, 84600, 65200] \
        and (zero[0], zero[1], h2.backlog(zero[2])) == (32200, 1, 30800) \
        and sum(h2.hold_cost(k) for k in B) == 900 and h2.backlog(B) == 9500


@reg(17, "allocation (16,64,64,256), lambda 1/8; cycle product 5/4; fees 8% no arbitrage, 5% arbitrage")
def _():
    a = (1, 2, 2, 4)
    tot = sum(x * x for x in a)
    r = [F(400 * x * x, tot) for x in a]
    from math import isqrt
    roots = [isqrt(int(ri)) for ri in r]
    lam = [F(x, 2 * s) for x, s in zip(a, roots)] if all(s * s == ri for s, ri in zip(roots, r)) else None
    cyc = F(1, 40) * F(5, 2) * 20
    return r == [16, 64, 64, 256] and sum(r) == 400 and lam == [F(1, 8)] * 4 and cyc == F(5, 4) \
        and cyc * F(92, 100) ** 3 < 1 and cyc * F(95, 100) ** 3 > 1 \
        and abs(1 - 0.8 ** (1 / 3) - 0.0717) < 1e-4


@reg(18, "year 1: profit 24600, restoration 8400, adjusted 16200; alt 20400/7400/13000; year 2 12700")
def _():
    B = h2.BUILDING
    sp, l, fin, lm = h2.simulate_building(B, (0, 0, 0, 400), 12)
    rest = sum(max(0, b - k) * 100 for b, k in zip(B, fin))
    sp2, l2, fin2, _ = h2.simulate_building(B, (100, 200, 100, 0), 12)
    rest2 = sum(max(0, b - k) * 100 for b, k in zip(B, fin2))
    y2 = h2.simulate_building(fin, (0, 0, 0, 400), 12)
    return (sp, l, fin, lm, rest, sp - rest) == (24600, 3, (76, 42, 13, 50), 42, 8400, 16200) \
        and (sp2, l2, fin2, rest2, sp2 - rest2) == (20400, 2, (90, 70, 29, 2), 7400, 13000) \
        and y2[0] == 12700 and lm * 1000 == 42000 and lm * 300 == 12600


@reg(19, "restoration from 38: ceiling 400 never; 500: 26 months 13000; 600: 17, 10200; 800: 10, 8000; 1200: 6, 7200")
def _():
    got = {c: h2.months_to_restore(38, 90, c) for c in (400, 500, 600, 800, 1200)}
    return got == {400: None, 500: (26, 13000), 600: (17, 10200), 800: (10, 8000), 1200: (6, 7200)}


@reg(20, "X and Y both profit 2400; backlog 9500 vs 0; ratios 900/400 and 400/400; shortfall argument 1000")
def _():
    X, Y = h2.BUILDING, (90, 90, 90, 90)
    prof = lambda ks: sum(700 for k in ks if k >= h2.HAB) - 400
    holdY = [h2.step(90, 100) for _ in range(4)]
    shortfall_ok = h2.k_after(0, 0, 50) == 50 and all(
        h2.step(50 - (s // 100) + 0, 400) >= 0 for s in (0,)) and (50 - 10 >= h2.HAB) and (50 - 11 < h2.HAB)
    return prof(X) == prof(Y) == 2400 and h2.backlog(X) == 9500 and h2.backlog(Y) == 0 \
        and sum(h2.hold_cost(k) for k in X) == 900 and sum(h2.hold_cost(k) for k in Y) == 400 \
        and holdY == [90] * 4 and shortfall_ok and h2.step(50, 400) == 50 and h2.step(50, 300) == 49


# ---------------- Part V ----------------
@reg(21, "score round(k/10) merges 80/81 and 50/51 with different hold costs; tier grades exact; B lasts 18 vs 4 months")
def _():
    score = lambda k: (k + 5) // 10
    hold = h2.hold_cost
    inad = score(80) == score(81) and hold(80) != hold(81) and score(50) == score(51) and hold(50) != hold(51)
    grade = lambda k: "A" if k > 80 else ("B" if k > 50 else ("C" if k >= 40 else "D"))
    costs = {}
    for k in range(40, 101):
        costs.setdefault(grade(k), set()).add(hold(k))
    exact_cost = all(len(v) == 1 for v in costs.values())
    return inad and exact_cost and h2.habitable_months(80, 0) == 18 and h2.habitable_months(52, 0) == 4


@reg(22, "records worth 1600-900 = 700 per month; log costs 80; reinspection 600")
def _():
    B = h2.BUILDING
    with_log = sum(h2.hold_cost(k) for k in B)
    without = sum(max(h2.hold_cost(k) for k in range(40, 101)) for _ in B)
    return with_log == 900 and without == 1600 and without - with_log == 700 and 4 * 20 == 80 and 4 * 150 == 600


def _tau(c):
    from math import ceil
    return ceil(1 + 7 * (1 - c))


def _loss(tau):
    k = 60
    for _ in range(tau):
        k = h2.step(k, 0)
    return 100 * (60 - k) + (700 if k < h2.HAB else 0)


@reg(23, "margin c >= 4/7; competence below 4/7 at month 8; u* = 2/5; practice cost 80; break-even price 750")
def _():
    ok_tau = all(_tau(c) <= 4 for c in (F(4, 7), F(1))) and _tau(F(4, 7) - F(1, 100)) >= 5
    c, t = F(1), 0
    while c >= F(4, 7):
        c -= F(3, 50)
        t += 1
    ustar = F(3, 50) / F(3, 20)
    return ok_tau and t == 8 and float(c) == 0.52 and ustar == F(2, 5) and 200 * ustar == 80 \
        and 300 - 200 * ustar == 220 and F(300) / ustar == 750 and h2.habitable_months(60, 0) == 8 \
        and h2.k_after(7, 0, 60) == 42 and h2.k_after(8, 0, 60) == 38


@reg(24, "losses 200/800/1400/2900; break-even 16/15 failures per 36 months")
def _():
    loss = {t: _loss(t) for t in (1, 4, 6, 8)}
    c30 = max(F(0), 1 - F(3, 50) * 30)
    c17 = max(F(0), 1 - F(3, 50) * 17)
    diff = 300 * 36 - (300 - 80) * 36
    return loss == {1: 200, 4: 800, 6: 1400, 8: 2900} and _tau(c30) == 8 and _tau(c17) == 8 \
        and diff == 2880 and F(diff, 2900 - 200) == F(16, 15) and F(300 * 36 - (300 - 160) * 36, 2700) == F(32, 15)


@reg(25, "unit-by-unit check passes, joint check fails; ledger debits 600+600 vs 1000; stale root passes")
def _():
    B = h2.BUILDING
    each = all(h2.hold_cost(k) <= h2.CAP for k in B)
    joint = sum(h2.hold_cost(k) for k in B) <= h2.CAP
    debits, limit = [600, 600], 1000
    naive = all(x <= limit for x in debits)
    agg = sum(debits) <= limit
    entries = [("a", 100), ("b", 200)]
    stored_root = sum(v for _, v in entries)
    entries[1] = ("b", 900)  # tampered contents
    seal_ok_naive = stored_root == stored_root
    recomputed_ok = stored_root == sum(v for _, v in entries)
    return each and not joint and naive and not agg and seal_ok_naive and not recomputed_ok


# ---------------- Part VI ----------------
@reg(26, "exit date 5 vs 10 with deposit label; late payment costs 1000 = 5 months of surplus")
def _():
    return months_to_exit(3000, 200, 4000) == 5 and months_to_exit(3000, 200, 5000) == 10 \
        and F(1000, 200) == 5


@reg(27, "lien: 30000 - 28000 = 2000, with selling costs 1500 gives 500; unit at 60 let 36 vs 14 months")
def _():
    low = _run(60, lambda t, k: 100, 36)
    full = _run(60, lambda t, k: h2.d(k) * 100, 36)
    return 30000 - 28000 == 2000 and 30000 - 28000 - 1500 == 500 and low[0] == 14 and full[0] == 36


@reg(28, "extractable price q*_n = 125, 137.5, 150, 162.5, 175 then capped at 175; extraction 300")
def _():
    q = [100 + F(1200 + 600 * n, 48) for n in range(6)]
    cap = F(700, 4)
    capped = [min(x, cap) for x in q]
    return q[:5] == [125, F(275, 2), 150, F(325, 2), 175] and q[5] == F(375, 2) \
        and capped[4] == capped[5] == 175 and 4 * (175 - 100) == 300 == 700 - 400 \
        and 4 * (125 - 100) == 100


@reg(29, "ten applicants: 7 eligible, 3 lose exit, aggregate gain 5600; P28 general matches front-chapter interval")
def _():
    from fractions import Fraction
    xs = [3400, 5000, 9000, 11400, 11500, 11700, 11800, 12000, 15000, 20000]
    r, T, dl, e, c, H = 1000, 12, Fraction(1, 20), 200, 4000, 3
    P = (1 - dl) * r * T
    pre = [hs.exit_ok_monthly(x, e, c, H) for x in xs]
    elig = [x for x in xs if x >= P]
    lost = [x for x in elig if hs.exit_ok_monthly(x, e, c, H) and not hs.exit_ok_prepaid(x, e, r, c, H, T, dl)]
    lo, hi = hs.lost_interval(e, r, c, H, T, dl)
    return all(pre) and len(elig) == 7 and lost == [11400, 11500, 11700] and 7 * 800 == 5600 \
        and (lo, hi) == (11400, 11800)


@reg(30, "evidence vs waiting: 51 -> 57 after 3 months at full effort, 61 after 5, 41 and 33 at zero effort; differencing")
def _():
    def run(k, M, n):
        for _ in range(n):
            k = h2.step(k, M)
        return k
    ok = run(51, 400, 3) == 57 and run(51, 400, 5) == 61 and run(51, 0, 3) == 41 \
        and run(51, 0, 5) == 33 and h2.rank_to(60, 400, 53) == 4
    xs = [(x1, x2, x3, x4) for x1 in (0, 1) for x2 in (0, 1) for x3 in (0, 1) for x4 in (0, 1)
          if x1 + x2 + x3 == 2 and x2 + x3 + x4 == 1]
    return ok and all(x[0] == 1 and x[3] == 0 for x in xs) and len(xs) > 0


# ---------------- Part VII ----------------
@reg(31, "demands 300+300 > 400; (50,50) not viable, (51,51) viable; check-then-commit overcommits to 600")
def _():
    K2 = h2.kernel2()
    cap = 400
    stale = [300 <= cap, 300 <= cap]  # both read 400
    committed_stale = sum(300 for ok in stale if ok)
    left, committed_serial = cap, 0
    for d in (300, 300):
        if d <= left:
            left -= d
            committed_serial += d
    return (300 <= 400 and 600 > 400 and (51, 51) in K2 and (50, 50) not in K2
            and committed_stale == 600 and committed_serial == 300 and h2.max_joint_delay(50, 50) == 6)


@reg(32, "circular implications satisfied by all-fail; four units at 90 stay at 90 for 24 months at ceiling 400")
def _():
    from itertools import product
    sat = [(a, b) for a, b in product((0, 1), repeat=2) if ((not b) or a) and ((not a) or b)]
    ks = [90] * 4
    for _ in range(24):
        req = [h2.hold_cost(k) for k in ks]
        if sum(req) > h2.CAP:
            return False
        ks = [h2.step(k, M) for k, M in zip(ks, req)]
    return (0, 0) in sat and (1, 1) in sat and ks == [90] * 4


@reg(33, "R(q): 200000, 202500, 200000, 180000; R' sign change at 1/4; hold-up 10% never joins; 5% joins from 60 months")
def _():
    R = lambda q: (100 * q + 200) * (1000 - 400 * q)
    Rp = lambda q: 20000 - 80000 * q
    stay = [phi for phi in (F(k, 100) for k in range(0, 21)) if 700 - 1000 * phi >= 600]
    joins10 = [N for N in range(1, 500) if N * (700 - 100) - 3000 >= 600 * N]
    joins5 = [N for N in range(1, 500) if N * (700 - 50) - 3000 >= 600 * N]
    return [R(F(0)), R(F(1, 4)), R(F(1, 2)), R(F(1))] == [200000, 202500, 200000, 180000] \
        and Rp(F(1, 4)) == 0 and Rp(F(1, 5)) > 0 and Rp(F(1, 3)) < 0 \
        and max(stay) == F(1, 10) and joins10 == [] and min(joins5) == 60


@reg(34, "24-month profiles of the pooled allocations")
def _():
    B = h2.BUILDING
    out = {a: h2.simulate_building(B, a, 24) for a in
           [(100, 100, 100, 100), (0, 200, 200, 0), (0, 100, 100, 100)]}
    f = lambda a: (out[a][0], out[a][1], h2.backlog(out[a][2]))
    return f((100, 100, 100, 100)) == (33100, 1, 23200) and f((0, 200, 200, 0)) == (42900, 3, 18300) \
        and f((0, 100, 100, 100)) == (35500, 1, 27000)


@reg(35, "items: preventive 112 vs deferral-and-restore 208 over 28 months")
def _():
    prev = 4 * 28
    k = h2.k_after(28, 0)
    restore = 4 * ((90 - k) * 100 // 100)
    return prev == 112 and k == 38 and restore == 208


# ---------------- Part VIII ----------------
def _g(s):
    return 0 if s <= 20 else (s * (100 - s)) // 400


@reg(36, "regeneration values; sustainable harvest 6; harvest 10 collapses; managed beats liquidation iff rho < 1/5; damp: 28->18, 8->6, hold costs 1300")
def _():
    vals = {s: _g(s) for s in (30, 40, 50, 60, 70, 80)}
    s, path = 50, []
    for _ in range(12):
        s = s + _g(s) - 10
        path.append(s)
        if s < 0:
            break
    rho_star = F(60, 300)
    def months(k0, extra):
        k, n = k0, 0
        while k >= 40:
            n += 1
            k = max(0, k - (h2.d(k) + extra))
        return n
    damp = (months(90, 0), months(90, 1), months(60, 0), months(60, 1))
    holds = [(h2.d(k) + 1) * 100 for k in h2.BUILDING]
    return vals == {30: 5, 40: 6, 50: 6, 60: 6, 70: 5, 80: 4} and max(_g(x) for x in range(21, 101)) == 6 \
        and path == [46, 42, 38, 33, 28, 23, 17, 7, -3] and (80 - 20) * 10 == 600 and (80 - 50) * 10 == 300 \
        and rho_star == F(1, 5) and damp == (28, 18, 8, 6) and holds == [200, 300, 300, 500] and sum(holds) == 1300


@reg(37, "care: breakdown after 2 months at 150 hours; gap 30 hours = 750; unpaid 120 hours = 3000")
def _():
    x, t = 0, 0
    while x < 60:
        x = max(0, x + 150 - 120)
        t += 1
    from math import ceil
    return t == 2 and ceil(F(60 - 0, 30)) == 2 and 30 * 25 == 750 and 120 * 25 == 3000 and ceil(F(60 - 20, 20)) == 2


@reg(38, "local 560/3 per month; 3-year totals 6480 vs 6720; cumulative equal at month 38 (6960)")
def _():
    local_m = F(2400, 36) + 20 + 100
    cc, cl, first = 0, 2400, None
    for m in range(1, 121):
        cc += 150 + 30 * ((m - 1) // 12)
        cl += 120
        if cl <= cc and first is None:
            first = (m, cc, cl)
    return local_m == F(560, 3) and 12 * (150 + 180 + 210) == 6480 and 2400 + 36 * 120 == 6720 \
        and first == (38, 6960, 6960)


@reg(39, "village: road 600 reaches 3; with feeder 800 reaches 4; all five 1100")
def _():
    dist = [1, 1, 2, 4, 6]
    reach = lambda budget: sum(1 for x in dist if (x <= 2 and budget >= 600) or (x == 4 and budget >= 800)
                               or (x == 6 and budget >= 1100))
    return reach(600) == 3 and reach(800) == 4 and reach(1100) == 5 and 800 + 250 == 1050


def _retrofit(order_months, cash0=2500, outlay=2000, offline=1, simultaneous=False):
    cash, mn, done = cash0, cash0, []
    horizon = 12
    off_until = {}
    for t in range(horizon):
        let_units = 0
        running = 0
        out = 0
        for u in range(4):
            if simultaneous:
                start = 0
            else:
                start = order_months[u]
            is_off = start <= t < start + offline
            if t == start:
                out += outlay
            retro = t >= start + offline
            if not is_off:
                let_units += 1
                running += 200 if retro else 300
        net = let_units * 1000 - running - 400 - 700 - out
        cash += net
        mn = min(mn, cash)
    return cash, mn


@reg(40, "retrofit: simultaneous cash -6600 after month 0; sequential minimum 1500; tolerance 3500; wait 720 vs act 500, q* 25/36")
def _():
    simul_cash0 = 2500 + (0 - 400 - 700) - 8000
    seq_cash, seq_min = _retrofit([0, 3, 6, 9])
    slip_cash, slip_min = _retrofit([0, 3, 6, 9], offline=2)
    month0 = 2500 + (3000 - 900 - 400 - 700) - 2000
    act = (2400 - 2000) + 100
    opt = F(1, 2) * 1200 + F(1, 2) * 400
    wait = F(9, 10) * opt
    return simul_cash0 == -6600 and month0 == 1500 and seq_min == 1500 and 2500 + 1000 == 3500 \
        and act == 500 and wait == 720 and F(act) / wait == F(25, 36) and slip_min >= 0 \
        and _retrofit([0, 0, 0, 0], simultaneous=True)[1] < 0


# ---------------- Part IX ----------------
from . import structures as st


@reg(41, "unit automaton from 60 with spends {0,200}: 11 conditions + dead = 12 states, 12 Nerode classes, 108 syntactic transformations; s^7 ok, s^14 not")
def _():
    states, delta, s0 = st.unit_dfa(60, (0, 200))
    classes = st.minimize(states, delta, (0, 200))
    mon, _ = st.transition_monoid(states, delta, (0, 200))
    return (len(states) == 12 and len(set(classes.values())) == 12 and len(mon) == 108
            and st.word_endstate(60, [0] * 7) == 42 and st.word_endstate(60, [0] * 14) is None)


@reg(42, "antichain of 3 has dimension 2; crown S_3 has dimension 3; cardinality and inclusion disagree on {51..100} vs {40..90}")
def _():
    e, l = st.crown_poset(3)
    A, B = set(range(51, 101)), set(range(40, 91))
    return (st.order_dimension(["A", "B", "C"], set()) == 2 and st.order_dimension(e, l) == 3
            and len(A) == 50 and len(B) == 51 and not A <= B and not B <= A)


@reg(43, "stopping: act 600, wait 828 (q=4/5) and 1035 (q=1) by backward induction; survival chain length 34")
def _():
    out = {}
    for q in (F(4, 5), F(1)):
        payoff = {"u": 600, "H": 2300, "L": 0, "D": 0}
        trans = {"u": [(q / 2, "H"), (q / 2, "L"), (1 - q, "D")], "H": [(1, "H")],
                 "L": [(1, "L")], "D": [(1, "D")]}
        V = st.optimal_stopping(payoff, trans, F(9, 10), 1)
        out[q] = V["u"]
    return out[F(4, 5)] == 828 and out[F(1)] == 1035 and len(h2.survival_chain(100)) - 1 == 34


@reg(44, "outbox: no retry can lose delivery; retry without idempotence duplicates; retry with idempotence still allows no delivery")
def _():
    a = st.outbox_outcomes(False, False)
    b = st.outbox_outcomes(True, False)
    c = st.outbox_outcomes(True, True)
    return ((0, False) in a and max(e for e, _ in a) == 1 and max(e for e, _ in b) == 2
            and max(e for e, _ in c) == 1 and (0, False) in c)


@reg(45, "hold policy: spend negatively related to condition, condition change identically 0, intervention effect +1 tenth")
def _():
    ks = list(range(40, 101))
    spend = [h2.hold_cost(k) for k in ks]
    cov, vx, vy = st.correlation(ks, spend)
    dk = [h2.step(k, h2.hold_cost(k)) - k for k in ks]
    effect = h2.step(70, 200) - h2.step(70, 100)
    return cov < 0 and set(dk) == {0} and effect == 1 and st.correlation(spend, dk) is None


# ---------------- Part X ----------------
@reg(46, "Adm not closed under composition; 108 syntactic classes; membership depends only on class (words up to length 7)")
def _():
    from itertools import product
    states, delta, s0 = st.unit_dfa(60, (0, 200))
    idx = {s: i for i, s in enumerate(states)}
    def tr(word):
        out = []
        for s in states:
            k = s
            for M in word:
                k = delta[(k, M)]
            out.append(idx[k])
        return tuple(out)
    classes = {}
    for n in range(0, 8):
        for w in product((0, 200), repeat=n):
            t = tr(w)
            member = st.admissible_word(60, w)
            if t in classes and classes[t] != member:
                return False
            classes[t] = member
    return (st.admissible_word(60, [0] * 7) and not st.admissible_word(60, [0] * 14)
            and len(st.transition_monoid(states, delta, (0, 200))[0]) == 108)


@reg(47, "two units at 50: each admissible alone with 400, jointly inadmissible; draw profile makes product undefined")
def _():
    w1, w2, ok = st.interchange_failure()
    return (st.admissible_word(50, w1) and st.admissible_word(50, w2) and not ok
            and not st.parallel_defined(w1, w2) and st.parallel_defined((200,) * 6, (200,) * 6))


@reg(48, "restoration options form a 4-element Pareto set; composition 38->60->90 equals direct; weights select 4 different plans")
def _():
    O = st.restoration_options(38, 90)
    A, B = st.restoration_options(38, 60), st.restoration_options(60, 90)
    comp = st.compose_costs(A, B)
    pick = {}
    for b in (0, 10, 20, 30):
        pick[b] = min(O, key=lambda o: o[1] + b * o[2])[2]
    return len(st.pareto(O)) == 4 and sorted(comp) == sorted(O) and pick == {0: 1200, 10: 800, 20: 600, 30: 500}


@reg(49, "two histories with image 24600 and different end states; functor law on random concatenations")
def _():
    import random
    f1, e1 = st.ledger_functor([(0, 0, 0, 400)] * 12, h2.BUILDING)
    f2, e2 = st.ledger_functor([(0, 0, 200, 200)] * 12, h2.BUILDING)
    rng = random.Random(7)
    allocs = h2.allocations()
    ok = True
    for _ in range(200):
        h = [rng.choice(allocs) for _ in range(rng.randint(1, 5))]
        g = [rng.choice(allocs) for _ in range(rng.randint(1, 5))]
        a, mid = st.ledger_functor(h, h2.BUILDING)
        b, _ = st.ledger_functor(g, mid)
        c, _ = st.ledger_functor(h + g, h2.BUILDING)
        ok = ok and (a + b == c)
    r1 = sum(max(0, b - k) * 100 for b, k in zip(h2.BUILDING, e1))
    r2 = sum(max(0, b - k) * 100 for b, k in zip(h2.BUILDING, e2))
    return f1 == f2 == 24600 and e1 == (76, 42, 13, 50) and e2 == (76, 42, 55, 26) and ok and (r1, r2) == (8400, 6600)


@reg(50, "assume-guarantee: four units at 90 supplied for 24 months; building (90,70,55,50) violates the crew assumption at month 1")
def _():
    t = st.ag_run((90,) * 4, 24)
    u = st.ag_run(h2.BUILDING, 2)
    return len(t) == 24 and all(ok for ok, _ in t) and t[-1][1] == (90,) * 4 and u == [(False, h2.BUILDING)]


# ---------------- Part XI ----------------
@reg(51, "well typed repair of 51 with spend 300 gives 52; fails without permission; well typed but not executable if crew absent")
def _():
    ctx = st.Ctx(money=400, crew=400, perms={"repair"})
    ok = st.typed_repair(ctx, 51, 300) == 52 and ctx.money == 100 and ctx.crew == 100
    try:
        st.typed_repair(st.Ctx(400, 400, set()), 51, 300)
        no_perm = False
    except st.ResourceError:
        no_perm = True
    try:
        st.execute_typed(st.Ctx(400, 400, {"repair"}), 51, 300, env_crew_available=0)
        stuck = False
    except st.ResourceError:
        stuck = True
    return ok and no_perm and stuck


@reg(52, "linear money and crew cannot be reused after splitting; affine permission may be dropped but not used afterwards")
def _():
    c = st.Ctx(money=400, crew=400, perms={"repair"})
    sub = c.split(300, 300)
    try:
        c.pay(200)
        dup = False
    except st.ResourceError:
        dup = True
    c.drop_perm("repair")
    try:
        c.use_perm("repair")
        after = False
    except st.ResourceError:
        after = True
    return dup and after and sub.money == 300 and c.money == 100


@reg(53, "escrow protocol makes progress with failure branches; deleting accept/dispute breaks progress")
def _():
    import copy
    broken = copy.deepcopy(st.ESCROW)
    broken["delivered"] = {}
    return st.protocol_progress(st.ESCROW, st.TERMINAL) and not st.protocol_progress(broken, st.TERMINAL)


@reg(54, "certificate for restoring to 60 at ceiling 400 verifies (50 conditions, rank 5 at 51); forged rank rejected; unit at 50 has none")
def _():
    cert = st.build_certificate(60, 400, 51)
    bad = dict(cert)
    bad[51] = (0, 3)
    low = st.build_certificate(60, 400, 40)
    return (len(cert) == 50 and cert[51][1] == 5 and st.check_certificate(cert, 60, 400)
            and not st.check_certificate(bad, 60, 400) and 50 not in low and 51 in low)


@reg(55, "verified scheduler meets sum <= ceiling for every building state yet leaves units 3 and 4 unfunded on the sample building")
def _():
    import random
    rng = random.Random(11)
    ok = True
    for _ in range(500):
        ks = tuple(rng.randint(40, 100) for _ in range(4))
        ok = ok and sum(st.greedy_allocate(ks)) <= h2.CAP
    a = st.greedy_allocate(h2.BUILDING)
    return ok and a == (100, 200, 0, 0)


# ---------------- Part XII ----------------
@reg(56, "unconstrained spends form a sheaf on a cover with overlap: locality and gluing hold")
def _():
    loc, glue, fails = st.check_gluing([[1, 2, 3], [2, 3, 4]], [1, 2, 3, 4], (0, 200))
    return loc and glue and not fails


@reg(57, "per-unit records restrict; totals do not determine restrictions (two histories with equal total, different parts)")
def _():
    a = {1: 100, 2: 300}
    b = {1: 200, 2: 200}
    return sum(a.values()) == sum(b.values()) and a != b


@reg(58, "feasible allocations: 5 unglued matching families on a disjoint cover, 3 on an overlapping cover; penalized reconstruction picks imperfect; circle twist nontrivial")
def _():
    feas = lambda sec: sum(v for _, v in sec) <= 400
    r1 = st.check_gluing([[1, 2], [3, 4]], [1, 2, 3, 4], (0, 200), feas)
    r2 = st.check_gluing([[1, 2, 3], [3, 4]], [1, 2, 3, 4], (0, 200), feas)
    exact_energy, imperfect_energy = 10, 3 + 2 * 1
    return (r1[0] and not r1[1] and len(r1[2]) == 5 and not r2[1] and len(r2[2]) == 3
            and imperfect_energy < exact_energy
            and st.z2_cocycle_trivial(1, 1, -1) is False and st.z2_cocycle_trivial(1, 1, 1))


@reg(59, "exchange cycle product 5/4 is a nontrivial class; fee 8% removes arbitrage; twisted double cover has no global section")
def _():
    p = st.exchange_cycle_product([F(1, 40), F(5, 2), F(20)])
    return (p == F(5, 4) and p != 1 and p * F(92, 100) ** 3 < 1 and p * F(95, 100) ** 3 > 1
            and not st.z2_cocycle_trivial(1, 1, -1))


@reg(60, "federated records: agreeing overlaps glue; a 55 vs 53 disagreement on unit 3 does not; outputs identical for any context order")
def _():
    L = {1: 90, 2: 70, 3: 55}
    C = {2: 70, 3: 55, 4: 50}
    K = {3: 55, 4: 50}
    ok1, g1 = st.glue_records({"L": L, "C": C, "K": K})
    ok2, g2 = st.glue_records({"K": K, "C": C, "L": L})
    C2 = dict(C)
    C2[3] = 53
    ok3, conflict = st.glue_records({"L": L, "C": C2, "K": K})
    return ok1 and ok2 and g1 == g2 == {1: 90, 2: 70, 3: 55, 4: 50} and not ok3 and conflict[0] == 3


@reg(43, "failure probability within T months for the unit at 50 under the one-tenth shock with probability 1/10: T=12 109/10^12, T=24 ~7.2e-6, T=60 ~0.034, T=120 ~0.664")
def _():
    from math import comb
    p = F(1, 10)
    f = lambda T: sum(comb(T, j) * p ** j * (1 - p) ** (T - j) for j in range(11, T + 1))
    return (f(12) == F(109, 10 ** 12) and abs(float(f(24)) - 7.194e-6) < 1e-8
            and abs(float(f(60)) - 0.03421) < 1e-4 and abs(float(f(120)) - 0.66391) < 1e-4)


@reg(44, "static share splits: K1(c1) x K2(c2) is contained in the joint kernel for every split of 400, and their union equals it on the pair of units")
def _():
    K2 = h2.kernel2()
    U = set()
    for c1 in range(0, 401, 100):
        k1 = h2.kernel_hab(c1) if c1 > 0 else set()
        k2 = h2.kernel_hab(400 - c1) if c1 < 400 else set()
        prod = {(a, b) for a in k1 for b in k2}
        if not prod <= K2:
            return False
        U |= prod
    return U == K2 and len(K2) == 2500
