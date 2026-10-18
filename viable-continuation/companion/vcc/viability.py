"""Finite-state robust viability.

A system is given by states, an acceptable set G, actions per state, and for
each (state, action) the set of possible successor states (the image of the
disturbance set under T). Robust viability depends only on those sets.
"""
from itertools import product, combinations


class System:
    def __init__(self, states, good, actions, succ):
        self.states = tuple(states)
        self.good = frozenset(good)
        self.actions = {s: tuple(actions[s]) for s in self.states}
        self.succ = {k: frozenset(v) for k, v in succ.items()}
        self.validate()

    def validate(self):
        universe = set(self.states)
        assert self.good <= universe
        for s in self.states:
            assert self.actions[s], "A(s) must be nonempty: %r" % (s,)
            for a in self.actions[s]:
                nxt = self.succ[(s, a)]
                assert nxt, "W(s,a) must be nonempty: %r" % ((s, a),)
                assert nxt <= universe

    def with_good(self, good):
        return System(self.states, good, self.actions, self.succ)


def phi(sys_, X):
    """Robust predecessor: acceptable states with an action forcing X."""
    X = frozenset(X)
    return frozenset(
        s for s in sys_.good
        if any(sys_.succ[(s, a)] <= X for a in sys_.actions[s])
    )


def kernel(sys_):
    """Greatest fixed point by decreasing iteration from G (finite S)."""
    K = sys_.good
    steps = 0
    while True:
        nxt = phi(sys_, K)
        if nxt == K:
            return K, steps
        K = nxt
        steps += 1


def kernel_by_postfixed_points(sys_):
    """Knaster-Tarski: union of all X subset of G with X subset phi(X)."""
    good = sorted(sys_.good, key=repr)
    best = set()
    for r in range(len(good) + 1):
        for X in combinations(good, r):
            X = frozenset(X)
            if X <= phi(sys_, X):
                best |= X
    return frozenset(best)


def robust_actions(sys_, K, s):
    return [a for a in sys_.actions[s] if sys_.succ[(s, a)] <= K]


def product_system(s1, s2, joint_ok=None):
    """Product of two systems. joint_ok(a1, a2) may restrict joint actions
    (a shared resource); it must leave every pair state with an action."""
    states = list(product(s1.states, s2.states))
    good = set(product(s1.good, s2.good))
    actions, succ = {}, {}
    for (x, y) in states:
        pairs = [(a, b) for a in s1.actions[x] for b in s2.actions[y]
                 if joint_ok is None or joint_ok(a, b)]
        if not pairs:
            raise ValueError("coupling removes every joint action at %r" % ((x, y),))
        actions[(x, y)] = pairs
        for (a, b) in pairs:
            succ[((x, y), (a, b))] = set(product(s1.succ[(x, a)], s2.succ[(y, b)]))
    return System(states, good, actions, succ)


def random_system(rng, n=4, max_actions=3, max_dist=3, p_good=0.7):
    states = list(range(n))
    good = [s for s in states if rng.random() < p_good]
    actions, succ = {}, {}
    for s in states:
        k = rng.randint(1, max_actions)
        actions[s] = list(range(k))
        for a in range(k):
            m = rng.randint(1, min(max_dist, n))
            succ[(s, a)] = set(rng.sample(states, m))
    return System(states, good, actions, succ)


# ---------------------------------------------------------------- P05
def three_state_example():
    """s0 -> {s0 | s1}; s1 -> b; G = {s0, s1}."""
    return System(
        ["s0", "s1", "b"], ["s0", "s1"],
        {"s0": ["stay", "go"], "s1": ["only"], "b": ["only"]},
        {("s0", "stay"): {"s0"}, ("s0", "go"): {"s1"},
         ("s1", "only"): {"b"}, ("b", "only"): {"b"}},
    )


# ---------------------------------------------------------------- P03
def chain_in_kernel_iterate(n, s):
    """Is s in K_n for the infinite chain 0,1,2,... with state m moving to
    m-1 and state 0 moving to an unacceptable state? G = all naturals."""
    if n == 0:
        return True  # G contains every natural number
    if s == 0:
        return False  # its only successor is outside G
    return chain_in_kernel_iterate(n - 1, s - 1)


# ---------------------------------------------------------------- P10 coupling
def shared_crew_unit():
    """Needs repair / ok / bad. Repair is heavy (uses the shared crew)."""
    return System(
        ["need", "ok", "bad"], ["need", "ok"],
        {"need": ["repair", "idle"], "ok": ["repair", "idle"], "bad": ["idle"]},
        {("need", "repair"): {"ok"}, ("need", "idle"): {"bad"},
         ("ok", "repair"): {"ok"}, ("ok", "idle"): {"need"},
         ("bad", "idle"): {"bad"}},
    )


def one_crew(a, b):
    """Shared crew: at most one unit may use the heavy action at a time."""
    return not (a == "repair" and b == "repair")
