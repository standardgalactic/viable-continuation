"""P22 worked case: price potentials on an exchange graph.

Each directed pair (i, j) has an upper bound u_ij on the log rate, requiring
p_j - p_i <= u_ij. A potential exists iff there is no negative cycle
(shortest-path duality). The frictionless case is u_ji = -u_ij, where the two
inequalities force p_j - p_i = c_ij and the condition becomes: every cycle
sums to zero, i.e. the class [c] in H^1(graph; R) vanishes.
"""
from fractions import Fraction


def find_potential(nodes, ub):
    """Bellman-Ford from a virtual source. Returns ("potential", p) or
    ("negative_cycle", cycle_nodes)."""
    n = len(nodes)
    dist = {v: Fraction(0) for v in nodes}
    pred = {v: None for v in nodes}
    for _ in range(n):
        changed = False
        for (i, j), u in ub.items():
            if dist[i] + u < dist[j]:
                dist[j] = dist[i] + u
                pred[j] = i
                changed = True
        if not changed:
            return "potential", dist
    last = None
    for (i, j), u in ub.items():
        if dist[i] + u < dist[j]:
            dist[j] = dist[i] + u
            pred[j] = i
            last = j
    x = last
    for _ in range(n):
        x = pred[x]
    cycle, y = [x], pred[x]
    while y != x:
        cycle.append(y)
        y = pred[y]
    cycle.reverse()
    return "negative_cycle", cycle


def cycle_cost(ub, cycle):
    total = Fraction(0)
    for k, i in enumerate(cycle):
        total += ub[(i, cycle[(k + 1) % len(cycle)])]
    return total


def with_spread(c, spread):
    """Bounds from log rates c (one orientation per edge) and a symmetric
    spread: u_ij = c_ij + s, u_ji = -c_ij + s."""
    s = Fraction(spread)
    ub = {}
    for (i, j), v in c.items():
        v = Fraction(v)
        ub[(i, j)] = v + s
        ub[(j, i)] = -v + s
    return ub


def holonomies(nodes, c):
    """Cycle sums of c around the fundamental cycles of a spanning tree
    (coordinates of [c] in H^1). All zero iff c is exact."""
    c = {k: Fraction(v) for k, v in c.items()}
    adj = {v: [] for v in nodes}
    for (i, j), v in c.items():
        adj[i].append((j, v))
        adj[j].append((i, -v))
    root = nodes[0]
    p = {root: Fraction(0)}
    stack = [root]
    tree = set()
    while stack:
        i = stack.pop()
        for j, v in adj[i]:
            if j not in p:
                p[j] = p[i] + v
                tree.add(frozenset((i, j)))
                stack.append(j)
    out = {}
    for (i, j), v in c.items():
        if frozenset((i, j)) not in tree:
            out[(i, j)] = v - (p[j] - p[i])
    return out
