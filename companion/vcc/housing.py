"""Hand-calculable housing model (book: The Housing Case, Theorems H1, H2).

All quantities are integers in currency units and months, no discounting.
Tenant: liquid resources x >= 0, monthly net surplus e >= 0 after rent r on a
monthly contract. Exit within H months needs resources >= c at the exit date
(c = moving cost + new deposit + first month). Prepaid lease: T > H months at
discount delta, prepayment P = (1-delta) r T, non-refundable, paid at date 0.
Use delta as a Fraction so that P is exact.
"""
from fractions import Fraction


def prepay(r, T, delta):
    return (1 - Fraction(delta)) * r * T


def exit_ok_monthly(x, e, c, H):
    """Brute force: some exit date t in 0..H with resources x + t e >= c."""
    return any(x + t * e >= c for t in range(H + 1))


def exit_ok_prepaid(x, e, r, c, H, T, delta):
    P = prepay(r, T, delta)
    if x < P:
        return None  # not eligible for the prepaid contract
    return any(x - P + t * (e + r) >= c for t in range(H + 1))


def lost_interval(e, r, c, H, T, delta):
    """Closed form of H1(b): eligible tenants who lose the executable exit
    are those with x in [max(P, c-He), c-He+P-rH)."""
    P = prepay(r, T, delta)
    lo = max(P, c - H * e)
    hi = c - H * e + P - r * H
    return (lo, hi) if lo < hi else None


def lost_nonempty_condition(e, r, c, H, T, delta):
    """H1(c): nonempty iff H < (1-delta) T and c > H (e + r)."""
    return H < (1 - Fraction(delta)) * T and c > H * (e + r)


def min_transfer(x, e, r, c, T, delta, t_bar):
    """H2(iii): minimal immediate-usable transfer restoring exit by t_bar."""
    P = prepay(r, T, delta)
    return max(Fraction(0), c - (x - P) - t_bar * (e + r))


def restored(x, m, tau, a, E, e, r, c, H, T, delta):
    """Brute force H2: exit dates t with a <= t <= min(H, E); the transfer m
    counts only at dates t >= tau."""
    P = prepay(r, T, delta)
    for t in range(max(a, 0), min(H, E) + 1):
        res = x - P + t * (e + r) + (m if tau <= t else 0)
        if res >= c:
            return True
    return False
