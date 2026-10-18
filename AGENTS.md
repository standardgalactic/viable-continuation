# Instructions for AI assistants (Claude, Copilot, Gemini, Codex, and others)

This repository is a LaTeX textbook skeleton, *The Economics of Viable Continuation*, by Flyxion (independent researcher). Your job is to help finish it as a long, detailed, rigorous graduate textbook. Read this file fully, then `docs/EDITORIAL_RULES.md`, then the brief for the chapter you are working on in `docs/chapter_briefs/`.

## What the book is

An economic theory in which the central object is the set of futures an economy keeps open. The economic theory is developed first (Parts I to VIII), then consolidated rigorously (Part IX), then interpreted categorically (X), type-theoretically (XI), and sheaf-theoretically (XII). Each interpretation must recover structure already established in the economic text and say what it preserves and what it leaves out.

## Layout

- `main.tex`, `preamble.tex`: build entry point and macros.
- `frontmatter/`: preface, reading paths, notation, **the housing case** (`housing.tex`), **the proof programme** (`spine.tex`, P01 to P29), and the generated result-to-chapter table (`spine_table.tex`).
- `parts/part01.tex` to `part12.tex`: twelve parts, 60 chapter stubs. Each stub has an outline paragraph and a one-line scaffold to replace.
- `appendices/`: prerequisites, companion description, framework concordance.
- `companion/`: Python finite-state checks (`vcc/`), tests, and `EXPECTED_OUTPUT.txt`.
- `docs/`: editorial rules, housing specification, per-chapter briefs, proof status, prompts, tasks, provenance.
- `tools/gen_parts.py`: the original generator. **Do not run it**: it overwrites the part files.

## Build and check

```
make book      # latexmk -pdf main.tex (run twice if references are undefined)
make check     # companion checks and unit tests
```

If `lmodern.sty` is missing, the preamble already falls back; microtype font expansion is disabled for that reason. Do not add packages that are not in a standard TeX Live without telling the author.

## Hard rules

1. **Stable labels.** P01 to P29 never change meaning. New results get the next number. Cite them with `\Pref{P03}`. Chapter references use `\chref{n}`.
2. **Three levels of claim stay distinct.** A definition fixes usage. A theorem is a consequence of stated assumptions. An empirical claim concerns an actual population or institution and needs evidence of the right kind. Anything not proved is a conjecture or a research question and must not wear theorem typography.
3. **Statuses.** Every spine entry carries Elementary, Hypotheses to fix, or Specification. Only promote an entry after the proof is written and checked. Never silently weaken a hypothesis or strengthen a conclusion. If a result needs a correction, say so in the text and in `docs/PROOF_PROGRAMME_STATUS.md`.
4. **Hypotheses are explicit.** For every formal result say which assumptions carry the conclusion, which only simplify the proof, and which are likely to fail in applications. Give a counterexample whenever removing an important assumption changes the result. Put the economic interpretation in its own paragraph after the proof.
5. **No invented numbers.** Do not invent probabilities, scores, or empirical magnitudes. Illustrative parameters must be labelled as such and live in the housing specification.
6. **Housing consistency.** Units are currency units and months, no discounting until a chapter says otherwise. Keep the signs and timing conventions in `docs/HOUSING_SPEC.md`. Outcomes such as positive cash flow with deterioration must arise from specified parameters, not be asserted as properties of housing markets.
7. **Companion discipline.** Every numerical example used in a chapter is reproduced in `companion/` with a recorded seed or an exhaustive enumeration and listed in `companion/EXPECTED_OUTPUT.txt`. Random checks are implementation evidence, not proofs. Describe unverified checks as "reported checks".
8. **Provenance.** Material from the author's other texts keeps its original attribution. Documentation-level reviews of other projects establish thematic overlap only. Exclude promotional claims (for example zero risk, general Sybil resistance) and claims about consciousness, universal entropy laws, or cosmological foundations. See `docs/SOURCES_AND_PROVENANCE.md`.
9. **Style.** Write long academic paragraphs, not strings of short clipped sentences. Avoid em dashes entirely; use commas, colons, parentheses, or separate sentences. Do not use first-person autobiographical framing. Avoid invented probabilities in satire or in analysis. Titles: no question titles, avoid the word "critique", avoid reusing the "X Before Y" pattern.
10. **Do not commit or push.** The author makes git commits personally. Prepare changes and leave them uncommitted.
11. **Do not narrate process in the text.** The book states findings and sources and the real limits of the material, not which tools or fetches were used.

## Working loop for one chapter

1. Read `docs/chapter_briefs/chNN.md`, the spine entries it lists, and the housing specification.
2. Write the chapter in `parts/partNN.tex` in the order: decision, mechanism in words, hand calculation, abstraction, results with hypotheses and counterexamples, interpretation, return to the decision, assessment of what is established.
3. Add or extend the companion check for every worked number. Run `make check`.
4. Update the spine entry (statement, hypotheses, status) and `docs/PROOF_PROGRAMME_STATUS.md` if a result changed.
5. Add exercises (calculation, proof or counterexample, institutional application) and put worked solutions in `solutions/chNN.tex`.
6. Run `make book` twice. Fix every undefined reference and overfull box that you introduced.
7. Run the definition-of-done checklist below.

## Definition of done for a chapter

- Opens with a decision, not with the programme's vocabulary.
- Has a hand-calculable example in the housing units, reproduced in the companion.
- Every important definition is followed by an example and a boundary case.
- Every result has hypotheses, a proof or a labelled conjecture, a counterexample where relevant, and a separate interpretation paragraph.
- Compares with established literature, citing primary sources for claims actually borrowed, and says whether it reproduces, extends, or reinterprets.
- Ends with what is established, the decision now enabled, assumptions still required, and the question passed to the next chapter.
- Contains at least a calculation, a proof or counterexample, and where relevant an institutional application as exercises.
- Passes a plain-language test: each claimed contribution survives translation into ordinary economic language. Passages that only restate the programme are removed.
- Builds cleanly, no em dashes, no unchecked numerical claims.

## Where to start

`docs/TASKS.md` gives the ordered roadmap. Highest priority: extend the housing case, then write Parts I to III as a connected argument before polishing Part IX.
