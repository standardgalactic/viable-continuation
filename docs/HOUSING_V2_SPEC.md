# Housing v2: shared specification

The machine-readable source of truth is `spec/housing_v2.json`. The LaTeX chapters, the companion (`companion/vcc/spec.py`, `housing2.py`, `book.py`), and the browser simulator (`simulator/`) all take their parameters and rules from it. Do not copy a parameter into a chapter, a script, or the simulator by hand; change the JSON and re-run `make check`.

## Units and state

Money is in currency units, time in months, condition `k` in tenths of a condition point (integers, 0 to `k_max` = 100). A unit is lettable iff `k >= 40`.

## Transition order within month t

1. Observe `k_t`.
2. Choose maintenance `M_t`, a multiple of 100, with the sum over all units at most the crew ceiling (400).
3. If `k_t >= 40`, collect rent (1000) and pay running cost (300). Otherwise neither occurs.
4. Pay `M_t`.
5. `k_{t+1} = max(0, min(100, k_t - d(k_t) + M_t/100))`, with `d = 1` for `k > 80`, `2` for `50 < k <= 80`, `4` for `k <= 50`.

Monthly surplus: `pi_t = 700 * [k_t >= 40] - M_t`.

## Obligation rules

Notice is served after two consecutive missed rents and runs one month. A restoration duty after degradation means returning to condition 60. The example repair duties are (deadline 3 days, 600), (14 days, 900), (30 days, 2000).

## Scenario parameters used in particular chapters

Owner cash 1500 and mortgage 700 per month (Chapter 5); tenant income 1200 before rent (Chapter 2); tenant exit cost 4000 and monthly-contract surplus 200 (Chapters 3 and 4 and the front chapter); prepaid lease `r=1000, T=12, delta=1/20, e=200, c=4000, H=3, kappa=800`.

## Rules for extension

Add new parameters to the JSON with a comment in this file. Any new worked number in a chapter needs an entry in `companion/vcc/book.py` that recomputes it exactly. A change to the transition order or to a tier requires re-running every check and updating every chapter number that moves. The checks report which entries fail.
