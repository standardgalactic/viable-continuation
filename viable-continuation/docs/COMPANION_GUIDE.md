# Companion guide

`companion/vcc/` is a standard-library Python package for finite models.

- `viability.py`: `System`, `phi`, `kernel`, `kernel_by_postfixed_points`, `product_system`, `random_system`, worked examples.
- `graph_prices.py`: Bellman-Ford potential and negative-cycle search, spreads, cycle holonomies (P22).
- `housing.py`: closed forms and brute-force predicates for the prepaid-lease model (P28, P29).
- `checks.py`: named checks returning `(passed, detail)`; the list `ALL` drives `run.py` and the tests.
- `run.py`: `python3 -m vcc.run all` or a single check with toggles `--infinite`, `--coupling`, `--spread`.

## Rules

1. Every numerical example in a chapter has a check. Record the seed, the parameters, and the claim checked.
2. Classify each check: exhaustive (all cases of a small model), random (sampled; evidence only), or counterexample (a hypothesis removed). Say which in `appendices/companion.tex`.
3. Include deliberately failing cases that expose shared capacity, omitted obligations, or insufficient history, and make the check pass only when the counterexample is actually found.
4. A random test never proves a universal theorem. State the proof in the text and use the code to catch errors.
5. After any change run `python3 -m vcc.run all > companion/EXPECTED_OUTPUT.txt` (keep the header comment lines) and `python3 -m unittest discover tests`.
6. Use exact arithmetic (`Fraction`, integers) wherever the book states exact numbers.

## Checks to add as chapters are written

Condition and cash-flow divergence (P12); obligation feasibility and the restoration schedule (P07); repair discharge with evidence and reopening; crew scheduling counterexample (P09); circular assume-guarantee on a two-component model (P27); typed commitment that is well-typed but not executable (P20); a presheaf that fails gluing and a sheaf that glues (P21); dynamic-programming benchmark recovered from the common model.
