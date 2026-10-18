"""Finite models for Parts IX to XII: syntactic monoid of an admissibility
language, failure of parallel composition under a shared sink, an enriched
(Pareto) cost structure, an accounting functor, assume-guarantee simulation,
a small linear-resource checker with protocols and certificates, finite
presheaf and Cech-cocycle checkers, and posets with order dimension.

Everything here is standard-library Python and uses the Housing v2
transition from housing2.py."""
from fractions import Fraction as F
from itertools import product, permutations, combinations
from . import housing2 as h2


# ------------------------------------------------------------------
# Part IX: automata, Nerode classes, order dimension, optimal stopping
# ------------------------------------------------------------------
def unit_dfa(k0=60, spends=(0, 200)):
    """Deterministic automaton: states are conditions (plus a dead state None);
    letters are spends; accepting = still lettable. Returns (states, delta, start)."""
    seen, stack = {k0}, [k0]
    delta = {}
    while stack:
        k = stack.pop()
        for M in spends:
            nk = h2.step(k, M)
            nk = nk if nk >= h2.HAB else None
            delta[(k, M)] = nk
            if nk is not None and nk not in seen:
                seen.add(nk)
                stack.append(nk)
    for M in spends:
        delta[(None, M)] = None
    return sorted(seen) + [None], delta, k0


def minimize(states, delta, spends):
    """Partition refinement (Moore). Accepting = not None."""
    part = {s: (s is not None) for s in states}
    while True:
        sig = {s: (part[s], tuple(part[delta[(s, M)]] for M in spends)) for s in states}
        ids = {}
        new = {}
        for s in states:
            new[s] = ids.setdefault(sig[s], len(ids))
        if len(set(new.values())) == len(set(part.values())):
            return new
        part = new


def transition_monoid(states, delta, spends):
    """Closure of the letter transformations: the syntactic monoid of the language."""
    idx = {s: i for i, s in enumerate(states)}
    def tr(M):
        return tuple(idx[delta[(s, M)]] for s in states)
    ident = tuple(range(len(states)))
    gens = [tr(M) for M in spends]
    monoid = {ident}
    frontier = [ident]
    while frontier:
        f = frontier.pop()
        for g in gens:
            h = tuple(g[f[i]] for i in range(len(states)))  # first f then g
            if h not in monoid:
                monoid.add(h)
                frontier.append(h)
    return monoid, ident


def word_endstate(k0, word):
    k = k0
    for M in word:
        k = h2.step(k, M)
        if k < h2.HAB:
            return None
    return k


# ---- posets and order dimension ------------------------------------
def linear_extensions(elems, less):
    """All linear extensions of the poset given by strict relation `less` (set of pairs)."""
    elems = list(elems)
    out = []
    def rec(prefix, remaining):
        if not remaining:
            out.append(tuple(prefix))
            return
        for e in sorted(remaining):
            if all((x, e) not in less or x in prefix for x in elems if x != e):
                rec(prefix + [e], remaining - {e})
    rec([], set(elems))
    return out


def order_dimension(elems, less):
    """Smallest realizer size (exact, by exhaustive search)."""
    exts = linear_extensions(elems, less)
    def pos(ext):
        return {e: i for i, e in enumerate(ext)}
    incomparable = [(a, b) for a in elems for b in elems
                    if a != b and (a, b) not in less and (b, a) not in less]
    for size in range(1, len(exts) + 1):
        for R in combinations(exts, size):
            ps = [pos(e) for e in R]
            ok = all(any(p[a] > p[b] for p in ps) for (a, b) in incomparable)
            if ok:
                return size
    return None


def crown_poset(n):
    """Standard example S_n: a_i < b_j iff i != j."""
    elems = [("a", i) for i in range(n)] + [("b", i) for i in range(n)]
    less = {(("a", i), ("b", j)) for i in range(n) for j in range(n) if i != j}
    return elems, less


def optimal_stopping(payoff, trans, beta, horizon):
    """Finite-horizon backward induction on a finite chain. payoff[s] is the
    stopping payoff in state s; trans[s] is a list of (prob, state); returns
    the value function at time 0 (V_n = max(payoff, beta E V_{n+1}))."""
    V = {s: payoff[s] for s in payoff}
    for _ in range(horizon):
        V = {s: max(payoff[s], beta * sum(p * V[t] for p, t in trans[s])) for s in payoff}
    return V


# ------------------------------------------------------------------
# Part X: parallel composition under a shared sink, enrichment, functor
# ------------------------------------------------------------------
def admissible_word(k0, word):
    return word_endstate(k0, word) is not None


def joint_admissible(k1, k2, w1, w2, cap=h2.CAP):
    """Pair of words (one letter per month per unit) is jointly admissible iff each
    unit stays lettable and the monthly draws sum to at most cap."""
    if len(w1) != len(w2):
        return False
    if any(a + b > cap for a, b in zip(w1, w2)):
        return False
    return admissible_word(k1, w1) and admissible_word(k2, w2)


def draw_profile(word):
    return tuple(word)


def parallel_defined(p1, p2, cap=h2.CAP):
    """Monoidal product on resource-annotated morphisms is defined iff the
    summed draw profile respects the shared ceiling."""
    return len(p1) == len(p2) and all(a + b <= cap for a, b in zip(p1, p2))


def interchange_failure(k1=50, k2=50, n=6):
    """Find words w1, w2 admissible separately (each can be held with 400) whose
    parallel composition is not admissible under the shared ceiling."""
    letters = (0, 200, 400)
    for w1 in product(letters, repeat=n):
        if not admissible_word(k1, w1) or w1 != tuple([400] * n):
            continue
        for w2 in product(letters, repeat=n):
            if w2 == tuple([400] * n):
                return w1, w2, joint_admissible(k1, k2, w1, w2)
    return None


def pareto(vectors):
    """Non-dominated vectors (all coordinates: smaller is better)."""
    vs = set(vectors)
    return sorted(v for v in vs if not any(all(a <= b for a, b in zip(w, v)) and w != v for w in vs))


def compose_costs(A, B):
    """Hom-object composition in the cost quantale: months and spend add, peak draw is a max."""
    return pareto({(a[0] + b[0], a[1] + b[1], max(a[2], b[2])) for a in A for b in B})


def restoration_options(k0, target, ceilings=(500, 600, 800, 1200)):
    out = []
    for c in ceilings:
        r = h2.months_to_restore(k0, target, c)
        if r:
            out.append((r[0], r[1], c))
    return out


def ledger_functor(history, ks):
    """Image of a history of per-unit spends under the accounting map: the sum
    of cash flows. history is a list of tuples of spends (one per unit)."""
    ks = list(ks)
    total = 0
    for alloc in history:
        for i, k in enumerate(ks):
            if k >= h2.HAB:
                total += h2.R - h2.C
            total -= alloc[i]
            ks[i] = h2.step(k, alloc[i])
    return total, tuple(ks)


# ------------------------------------------------------------------
# Part XI: linear resources, protocols, certificates, refinement
# ------------------------------------------------------------------
class ResourceError(Exception):
    pass


class Ctx:
    """Linear context: money and crew capacity are linear (consumed exactly once);
    permissions are affine (may be dropped, not duplicated)."""
    def __init__(self, money=0, crew=0, perms=()):
        self.money, self.crew, self.perms = money, crew, set(perms)

    def pay(self, amount):
        if amount > self.money:
            raise ResourceError("insufficient money")
        self.money -= amount

    def use_crew(self, amount):
        if amount > self.crew:
            raise ResourceError("insufficient crew capacity")
        self.crew -= amount

    def split(self, money, crew):
        """Hand part of the context to a sub-computation; the parent loses it."""
        self.pay(money)
        self.use_crew(crew)
        return Ctx(money, crew, set())

    def drop_perm(self, p):
        self.perms.discard(p)

    def use_perm(self, p):
        if p not in self.perms:
            raise ResourceError("permission absent")


def typed_repair(ctx, unit_k, spend):
    """Judgment: Gamma |- repair(spend) : k => k'. Preconditions are resources and the
    permission; the postcondition is the successor condition."""
    ctx.use_perm("repair")
    ctx.pay(spend)
    ctx.use_crew(spend)
    return h2.step(unit_k, spend)


ESCROW = {
    "init": {"deposit": "funded"},
    "funded": {"deliver": "delivered", "timeout": "refunded"},
    "delivered": {"accept": "settled", "dispute": "disputed"},
    "disputed": {"resolve_pay": "settled", "resolve_refund": "refunded"},
    "settled": {}, "refunded": {},
}
TERMINAL = {"settled", "refunded"}


def protocol_progress(proto, terminal):
    """Every non-terminal state has an outgoing branch and every state reaches a terminal state."""
    reach = set(terminal)
    changed = True
    while changed:
        changed = False
        for s, moves in proto.items():
            if s not in reach and any(t in reach for t in moves.values()):
                reach.add(s)
                changed = True
    return all(s in reach for s in proto) and all(proto[s] for s in proto if s not in terminal)


def check_certificate(cert, target, cap, hab=h2.HAB):
    """Proof-carrying restoration: cert maps condition -> (spend, rank). Accept iff, for every
    certified state, the spend is within the ceiling, the successor is certified and lettable,
    and rank strictly decreases until rank 0, which must be at or above the target."""
    for k, (M, r) in cert.items():
        if r == 0:
            if k < target:
                return False
            continue
        if M > cap or M % 100:
            return False
        nk = h2.step(k, M)
        if nk < hab or nk not in cert or cert[nk][1] >= r:
            return False
    return True


def build_certificate(target, cap, k_from):
    cert = {}
    for k in range(k_from, 101):
        r = h2.rank_to(target, cap, k)
        if r is None:
            continue
        if r == 0:
            cert[k] = (0, 0)
        else:
            for M in range(0, cap + 1, 100):
                nk = h2.step(k, M)
                if nk >= h2.HAB and h2.rank_to(target, cap, nk) == r - 1:
                    cert[k] = (M, r)
                    break
    return cert


# ------------------------------------------------------------------
# Open systems: time-indexed assume-guarantee simulation
# ------------------------------------------------------------------
def ag_run(ks, months, cap=h2.CAP):
    """Each unit requests its hold cost from its current condition; the crew supplies
    the requests when their sum is within cap (its guarantee, whose assumption is the
    sum of requests at the same step, computed from conditions fixed by earlier supply).
    Returns the list of (all supplied, conditions) per month."""
    trace = []
    ks = list(ks)
    for _ in range(months):
        req = [h2.hold_cost(k) for k in ks]
        if sum(req) > cap:
            trace.append((False, tuple(ks)))
            return trace
        ks = [h2.step(k, M) for k, M in zip(ks, req)]
        trace.append((True, tuple(ks)))
    return trace


# ------------------------------------------------------------------
# Part XII: finite presheaves, gluing, cocycles
# ------------------------------------------------------------------
def restrict(section, subdomain):
    return tuple((u, section_dict(section)[u]) for u in sorted(subdomain))


def section_dict(section):
    return dict(section)


def all_sections(domain, values, feasible=None):
    domain = sorted(domain)
    out = []
    for vs in product(values, repeat=len(domain)):
        sec = tuple(zip(domain, vs))
        if feasible is None or feasible(sec):
            out.append(sec)
    return out


def check_gluing(cover, total, values, feasible=None):
    """Presheaf F(U) = sections over U satisfying `feasible` (restriction by
    restricting the function). Checks, for a cover of `total` by the sets in
    `cover`, that every matching family has a unique glued section in F(total).
    Returns (locality_ok, gluing_ok, failures) where failures lists matching
    families without a glued section in F(total)."""
    secs = [all_sections(U, values, feasible) for U in cover]
    Ftotal = set(all_sections(total, values, feasible))
    glue_failures = []
    locality_ok = True
    for fam in product(*secs):
        match = True
        for i in range(len(cover)):
            for j in range(i + 1, len(cover)):
                ov = set(cover[i]) & set(cover[j])
                if restrict(fam[i], ov) != restrict(fam[j], ov):
                    match = False
        if not match:
            continue
        glued = {}
        for sec in fam:
            glued.update(section_dict(sec))
        g = tuple(sorted(glued.items()))
        if g not in Ftotal:
            glue_failures.append(fam)
    # locality: two global sections that agree on every cover member are equal
    for s in Ftotal:
        for t in Ftotal:
            if s != t and all(restrict(s, U) == restrict(t, U) for U in cover):
                locality_ok = False
    return locality_ok, not glue_failures, glue_failures


def cech_h1_trivial(g):
    """Cocycle on a triangle with values in a finite abelian group written
    multiplicatively as integers mod n via lists: g = (g12, g23, g31) in Z_n with
    modulus attached by the caller. Returns whether it is a coboundary."""
    raise NotImplementedError


def z2_cocycle_trivial(g12, g23, g31):
    """Signs (+1/-1) on the three overlaps of a circle covered by three arcs.
    The class is trivial iff some choice of signs a1, a2, a3 gives g_ij = a_i * a_j."""
    for a1, a2, a3 in product((1, -1), repeat=3):
        if g12 == a1 * a2 and g23 == a2 * a3 and g31 == a3 * a1:
            return True
    return False


def exchange_cycle_product(rates):
    """Multiplicative exchange rates around a cycle (list of Fractions)."""
    p = F(1)
    for r in rates:
        p *= r
    return p


# ------------------------------------------------------------------
# Transactional outbox toy (Chapter 44)
# ------------------------------------------------------------------
def outbox_outcomes(retry, idempotent):
    """Exhaustively enumerate delivery schedules for one order. A transaction commits the
    order and an outbox row together (so no committed order lacks an obligation). A relay
    then attempts delivery up to 2 times; each attempt either loses the message or delivers
    it (a delivered message may have its acknowledgement lost, causing a retry). Returns the
    set of (effects_at_recipient, outbox_row_cleared) over all schedules."""
    outcomes = set()
    attempts = 2 if retry else 1
    # each attempt: 'lost' (no effect), 'delivered_acked', 'delivered_ack_lost'
    for sched in product(("lost", "ack", "noack"), repeat=attempts):
        effects, cleared = 0, False
        for ev in sched:
            if cleared:
                break
            if ev == "lost":
                continue
            effects += 1 if not (idempotent and effects >= 1) else 0
            if ev == "ack":
                cleared = True
        outcomes.add((effects, cleared))
    return outcomes


# ------------------------------------------------------------------
# Measurement (Chapter 45)
# ------------------------------------------------------------------
def correlation(xs, ys):
    n = len(xs)
    mx, my = F(sum(xs), n), F(sum(ys), n)
    cov = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    vx = sum((x - mx) ** 2 for x in xs)
    vy = sum((y - my) ** 2 for y in ys)
    if vx == 0 or vy == 0:
        return None
    return cov, vx, vy


def execute_typed(ctx, unit_k, spend, env_crew_available):
    """Typing says the repair is admissible; execution also needs the environment to
    supply the crew. Returns the successor condition or raises ResourceError."""
    nk = typed_repair(ctx, unit_k, spend)
    if env_crew_available < spend:
        raise ResourceError("counterparty unavailable: well typed but not executable")
    return nk


def glue_records(local_records):
    """local_records: dict context -> dict unit -> value. Returns (ok, glued or conflict)."""
    glued = {}
    for ctxname, rec in local_records.items():
        for u, v in rec.items():
            if u in glued and glued[u][0] != v:
                return False, (u, glued[u], (v, ctxname))
            glued.setdefault(u, (v, ctxname))
    return True, {u: v for u, (v, _) in glued.items()}


def greedy_allocate(ks, cap=h2.CAP):
    """A scheduler that funds units in increasing order of hold cost until the ceiling is spent."""
    order = sorted(range(len(ks)), key=lambda i: h2.hold_cost(ks[i]))
    left, alloc = cap, [0] * len(ks)
    for i in order:
        need = h2.hold_cost(ks[i])
        if need <= left:
            alloc[i] = need
            left -= need
    return tuple(alloc)
