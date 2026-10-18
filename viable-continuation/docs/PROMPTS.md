# Ready-to-paste prompts

Attach or open: `AGENTS.md`, `docs/EDITORIAL_RULES.md`, `docs/HOUSING_SPEC.md`, the chapter brief, and the spine entries listed in the brief. Replace N with the chapter number.

## 1. Draft a chapter
> Write Chapter N of this textbook in `parts/partNN.tex`, replacing the outline paragraph and scaffold line. Follow `docs/chapter_briefs/chN.md` and `docs/EDITORIAL_RULES.md`. Open with a decision, develop the mechanism in words, calculate a small example in the housing units, then state the abstraction. For each result give hypotheses, a counterexample where relevant, the proof or a labelled conjecture, and a separate interpretation paragraph. End with what is established, the decision enabled, the assumptions still required, and the question passed to the next chapter. Aim for 15 to 25 pages of substance. Use long academic paragraphs and no em dashes. Then add a companion check for every worked number and run `make check` and `make book`. Do not commit.

## 2. Prove or repair a spine result
> Take result PNN in `frontmatter/spine.tex`. Write a complete proof under the stated hypotheses, identify which hypotheses carry the conclusion and which only simplify the proof, give a counterexample for each important hypothesis removed, and state the economic interpretation separately. If the statement as written is false or too strong, say so, propose the corrected statement, and update the status in the spine and in `docs/PROOF_PROGRAMME_STATUS.md`. Do not promote the status until the proof is written out.

## 3. Extend the housing case
> Implement step K of `docs/HOUSING_SPEC.md`. Specify observed quantities, uncertain quantities, and who decides what. Give a hand-calculable version with a table, add closed forms and brute-force predicates in `companion/vcc/housing.py`, add a check in `checks.py`, update `EXPECTED_OUTPUT.txt`, and add the new section to `frontmatter/housing.tex`. Keep every earlier number unchanged.

## 4. Review a chapter adversarially
> Review Chapter N as a skeptical referee. List (a) statements that are stronger than their proofs, (b) hypotheses used but not stated, (c) claims about actual economies stated as theorems, (d) passages that restate the programme without advancing it, (e) numerical claims not reproduced in the companion, (f) places where the text is not understandable in plain economic language. Quote the passage and give a specific fix for each. Do not rewrite the chapter.

## 5. Write the benchmark chapter or appendix
> Derive a finite-horizon dynamic programme as a specialization of the common model in `frontmatter/notation.tex`: state the preferences, technology, and information structure that must be added, show the Bellman recursion, and show where history compression and slack viability constraints are used. Do not claim that competitive equilibrium or growth models follow from compressed history and slack constraints alone; list the extra assumptions each needs.

## 6. Write exercises and worked solutions
> For Chapter N write exercises: at least one calculation in the housing units, one proof or counterexample, and one empirical or institutional application where relevant. Put worked solutions in `solutions/chN.tex`. Verify every numerical solution with the companion.

## 7. Extend the companion
> Add a check named `check_X` for claim Y. State whether it is exhaustive, random (with seed), or a counterexample. Include a variant with the key hypothesis removed that reproduces the failure and passes only when the failure is found. Update `appendices/companion.tex` and `companion/EXPECTED_OUTPUT.txt`.

## 8. Build Part X, XI, or XII for the housing interfaces
> Following `docs/EDITORIAL_RULES.md`, write the chapter so that it answers a specific question left by the economic text. Construct the structure explicitly (category, judgment system, or site), prove the required closure or quotient or sheaf property, and give the housing interfaces as objects with actual mappings and verified laws. Include the failure case (shared crew, expressible-but-unexecutable commitment, or presheaf that fails gluing).
