# Copilot instructions

Follow `AGENTS.md` at the repository root; it is the source of truth. Short version:

- LaTeX book in `parts/`, results register in `frontmatter/spine.tex` (P01 to P29, stable labels), housing case in `frontmatter/housing.tex`, Python checks in `companion/`.
- Build with `make book`; test with `make check`.
- Keep definitions, theorems, and empirical claims distinct. Unproven results are conjectures, not theorems. State hypotheses, counterexamples, and interpretation separately.
- Every numerical example must be reproduced in `companion/` with a recorded seed or exhaustive enumeration.
- No em dashes. Long academic paragraphs. No invented probabilities or empirical magnitudes.
- Never run `tools/gen_parts.py` (it overwrites chapter files). Never commit or push.
