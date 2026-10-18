# Polishing, source verification, and framework testing

## 1. Source verification (do first; nothing below has been verified)
- Every entry in `refs.bib` was written from memory or from the author's prompts. For each: confirm title, authors, year, venue, and that it supports the sentence citing it. Entries written from memory and flagged for particular suspicion: `hicks1939`, `nerode1958`, `shavell1986`, `arrow1974`, `dushnik1941`.
- Candidates cited by name but possibly not yet in `refs.bib`: Coase, Ostrom, Sen, Dixit and Pindyck, Aubin (viability theory), Knaster and Tarski, Myhill and Nerode, Dushnik and Miller, Slater, Rockafellar.
- Remove `\nocite{*}` in `main.tex` once citations in the text are complete, so only cited works appear.
- The concordance (`appendices/concordance.tex`) has three rows marked "source to be assigned". Assign sources from the author's papers or remove the rows.
- Chapters 44 and 54 contain candidate imports from repository READMEs. Their implementations were not tested; keep the wording at the level of the concept.

## 2. Mathematical audit
For each chapter read the brief in `docs/chapter_briefs/`, then check: (a) every proof by hand; (b) every numerical example against the companion entry named in the text; (c) that every use of a result states its hypotheses. Known weaknesses to attack first:
- Chapter 1's restoration cost ignores decay during repair (corrected in Chapter 19).
- Chapter 43 failure-probability table assumes independent shocks with probability 1/10 and failure after 11 shocks: confirm the failure criterion against the model.
- Chapter 44's equality of the static-split union with the joint kernel is an exhaustive observation for this pair, not a theorem.
- Chapters 47 and 54: the interchange failure and certificate are small examples; check whether the general statements are over-claimed.
- Chapter 58's penalized reconstruction numbers are stipulated, not derived.
- Parts XI and XII are the least developed theoretically: P20 (progress) and P21/P22 beyond the finite cases remain specifications.

## 3. Testing the frameworks
Each "framework" in the concordance should be tested by asking what it predicts that the standard treatment does not.
- Pick a chapter claim and write the benchmark version (standard dynamic programme, Hicksian accounting, standard principal-agent) in the companion; compare outputs.
- Vary one assumption per run in the simulator (shock size, ceiling, review depth) and see whether the book's qualitative claims survive. Note the breakpoints; the book uses break-even parameters, not probabilities, deliberately.
- Add counterexample checks: remove each hypothesis of a proposition and look for a failing instance (the companion does this for P03 and P10).
- Where a claim depends on an assumed rate (erosion, deterioration, switching-cost growth), list it in a table and mark which study would estimate it (see Chapter 45).

## 4. Editorial polish
Follow `docs/EDITORIAL_RULES.md`: long academic paragraphs, no em dashes, titles that are not questions, no invented probabilities. Check overfull boxes (`grep Overfull main.log`), consistency of notation with `frontmatter/notation.tex`, and that each chapter has: setting, theorem or calculation, companion check, what was established, exercises.

## 5. Still to write
Worked solutions (`solutions/` holds only a README), a benchmark chapter in standard theory, a scope statement, the index, and complete prerequisites. See `docs/TASKS.md`.
