# The Economics of Viable Continuation

[Architectures of Mind](https://github.com/standardgalactic/viable-continuation/blob/main/architectures/README.md) — *Project*

[The Unit of Scrutiny](https://standardgalactic.github.io/viable-continuation/unit_of_scrutiny.pdf)

[Concealment Encryption](https://standardgalactic.github.io/viable-continuation/concealment_encryption.pdf)

[Distributed Material Archives](https://standardgalactic.github.io/viable-continuation/distributed-material-archives.pdf)

[The Relief of Explanation](https://standardgalactic.github.io/viable-continuation/relief_of_explanation.pdf)

[Terrestrial Oxygen History](https://standardgalactic.github.io/viable-continuation/terrestrial_oxygen_history.pdf)

[Viable Continuation](https://standardgalactic.github.io/viable-continuation/viable-continuation.pdf)

*Production, Obligation, Institutions, and the Organization of Feasible Futures*

A long graduate-level textbook in progress, by Flyxion (independent researcher). The book treats an economy as an organization of provisioning, transformation, and maintenance through time, and asks which futures each institutional arrangement keeps open, for whom, and at what cost to the conditions later activity depends on. It develops the economic theory in its own terms first, then gives categorical, type-theoretic, and sheaf-theoretic interpretations that recover structure the economic text has already established and state what each interpretation preserves and leaves out.

**Status: complete first draft, October 2026.** All 60 chapters are drafted. Citations, many proofs, and the exercises are unaudited, and no solutions are written. Nothing here is a claim about an actual economy until a chapter says so and gives evidence. See `docs/POLISHING_GUIDE.md` for what to verify first.

## Plan of the book

| Parts | Chapters | Content |
|---|---|---|
| I to III | 1 to 15 | Activity and the establishment of futures; production, maintenance, irreversibility; obligations, degradation, recovery |
| IV to V | 16 to 25 | Value, prices, accounting, debt; knowledge, attention, competence, verification |
| VI to VIII | 26 to 40 | Institutions, power, distribution; markets, firms, commons; ecology, care, technology, development, transition |
| IX | 41 to 45 | Rigorous consolidation of the principal results and their measurement |
| X to XII | 46 to 60 | Categorical, type-theoretic, and sheaf-theoretic interpretations |

Reading routes (economics only, formal core, full) and a dependency diagram are in the front matter of the PDF.

## The proof programme

Twenty-nine stable results, P01 to P29, are specified in `frontmatter/spine.tex` and grouped into six families: representation, viability, production and irreversibility, institutions, competence and automation, and composition. Each carries a status: *Elementary* (statement fixed, short proof indicated), *Hypotheses to fix*, or *Specification*. The central questions are when history can be compressed without losing consequential distinctions, when local admissibility supports continued viability, when commitments compose, when a valuation or accounting preserves the comparisons it is meant to support, and when compatible local descriptions determine a feasible collective arrangement. `docs/PROOF_PROGRAMME_STATUS.md` tracks what each unsettled result still needs.

## The housing case

A small housing economy runs through every part. It is first specified deterministically so that it can be calculated by hand. Two results are proved in it so far: that a prepaid-lease offer can raise aggregate surplus while shrinking a tenant's executable exit set (P28, Theorem H1), and that compensation restores a lost capability only if availability, timing, and sufficiency all hold (P29, Theorem H2). The general statements remain specifications. See `frontmatter/housing.tex` and `docs/HOUSING_SPEC.md`.

## Repository layout

```
main.tex, preamble.tex, refs.bib, Makefile   build entry point
frontmatter/    preface, reading paths, notation, housing case, proof programme
parts/          twelve parts containing the 60 chapters
appendices/     prerequisites, companion description, framework concordance
companion/      finite-state Python checks, tests, recorded output
docs/           editorial rules, housing spec, proof status, chapter briefs, prompts, roadmap, provenance
solutions/      worked solutions (not yet written)
simulator/      single-file Housing v2 simulator, its template, build script, and test
spec/           housing_v2.json, the shared specification
tools/          original skeleton generator (do not run; it overwrites chapter files)
AGENTS.md, CLAUDE.md, GEMINI.md, .github/copilot-instructions.md   instructions for AI assistants
NOTES.md        open decisions
main.pdf        last compiled draft
```

## Building

Requires a TeX Live installation with `pdflatex`, `latexmk`, and `bibtex`.

```
make book     # compile main.pdf (run twice if references are undefined)
make check    # companion checks, unit tests, and the simulator test (needs node)
make clean    # remove build artifacts
```

If `lmodern.sty` is not installed the preamble falls back to the default fonts and microtype font expansion is turned off.

Full build and verification instructions are in `docs/BUILD_AND_VERIFY.md`. Open `simulator/housing_v2_simulator.html` in a browser for the simulator.

## The computational companion

`companion/vcc/` is a standard-library Python package for finite models: robust viability kernels, price potentials on exchange graphs, and the housing-case closed forms with brute-force predicates. Each check is classified as exhaustive, random (with a recorded seed), or a counterexample with a hypothesis removed. Random checks are implementation evidence, not proofs. The recorded output is in `companion/EXPECTED_OUTPUT.txt`. These are reported checks until independently inspected.

```
cd companion
python3 -m vcc.run all
python3 -m unittest discover tests
```

## Contributing and working with assistants

Start with `AGENTS.md`, then `docs/EDITORIAL_RULES.md`. Each chapter has a brief in `docs/chapter_briefs/`, and `docs/PROMPTS.md` has ready-made prompts. The main rules: keep definitions, theorems, and empirical claims distinct; state hypotheses, counterexamples, and interpretation separately; reproduce every worked number in the companion; avoid em dashes and invented numbers; keep provenance for material drawn from other texts. Changes are prepared for the author to review and commit.

## License

Released into the public domain under the [CC0 1.0 Universal](LICENSE) dedication. This covers the text, the LaTeX sources, and the companion code.
