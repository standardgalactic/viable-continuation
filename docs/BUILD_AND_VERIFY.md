# Build and verification

All commands run from the repository root. Requirements: a TeX distribution with `latexmk`, `pdflatex` and `bibtex`; Python 3 (standard library only); Node 18 or later (for the simulator test only).

## Build the book
```
make book          # or: latexmk -pdf main.tex
```
Run it twice if references change. Zero undefined references and no `!` lines in `main.log` is the target. `main.pdf` is the output. The preamble falls back when `lmodern` is missing.

## Run every check
```
make check
```
This runs, in order:
1. `python3 -m vcc.run all` in `companion/` (15 named checks, one of which, BOOK, recomputes 62 numerical calculations in Chapters 1 to 60).
2. `python3 -m unittest discover tests` in `companion/`.
3. `simulator/build.py` and `node simulator/test_simulator.js`, which compare the page's embedded specification with `spec/housing_v2.json`, run its reproduced checks, and replay traces from the Python companion.

Compare the first command's output with `companion/EXPECTED_OUTPUT.txt`. After changing any model number, update `spec/housing_v2.json` first, rebuild the simulator, run `make fixture`, regenerate `EXPECTED_OUTPUT.txt`, and fix the text.

## What a pass means
A pass means the stated numbers follow from the stated finite model. It does not prove any universal statement; those are proved in the text, and the status of each is in `docs/PROOF_PROGRAMME_STATUS.md`. The companion is a set of reported checks, not a formal verification.

## The simulator
Open `simulator/housing_v2_simulator.html` in any browser (no network needed). It is rebuilt from `simulator/template.html` by `simulator/build.py`; edit the template, not the output.
