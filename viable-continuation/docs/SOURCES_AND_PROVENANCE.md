# Sources and provenance

Material from the author's other texts keeps its original attribution. Do not cite an organization or repository collection as the intellectual origin of ideas attributed to the author.

## Candidate imports (from source reviews; none copied)

- Replay integrity versus historical authority (Chapters 22, 25, 54). A self-consistent checkpoint is not an independently trusted history; branch selection is not evidence the branch is true.
- The identity KL(P(.|B) || P) = -log P(B), 0 < P(B) <= 1, as a measure of probabilistic restriction (Chapter 16). It does not give a monetary cost, a dissipation, or a conservation law.
- Expenditure versus damage to regenerative capacity (Chapters 7, 23).
- Allocation of finite maintenance capacity: max sum V_i(r_i) subject to sum r_i <= B, with the budget as an explicit assumption and the shadow price as the dual variable (Chapters 17, 23). No universal conservation of ambiguity.
- Conditional platform revenue R(q) = (alpha q + beta) M(q), R'(q) = alpha M + (alpha q + beta) M' (Chapter 33). Narrow conditional incentive result only.

## Corrections to carry over

- A nonpositive long-run average net accumulation rate does not ensure bounded debt: D(t) = sqrt(1+t) - 1 is unbounded while its average rate tends to zero. Use the cumulative-excess condition sup_t integral (rho_M - rho_R) du < infinity, or a reflected-backlog formulation (Chapter 8).
- A non-convergence argument that reverses an inequality (an upper bound on next-period error cannot give the lower bound later used) must be rebuilt, not imported.

## Counterexamples and exercises from reviews

- A ledger verifier that checks seals against stored roots without recomputing them from contents, and checks debits one at a time without aggregating repeated postings: individually permissible debits can jointly exceed the balance restriction (Chapter 25).
- Sheaf repair claims: a local-repair condition need not produce a global section; a lower-energy imperfect candidate can beat an exact match under a penalized reconstruction; a circle example must not state contradictory overlap values (Chapter 58).

## Documentation-level cases (README only; not inspected, not run)

- Civic-maintenance verification design with separate official and observed ledgers and a verification period before closure (Chapters 20, 25, 30). Grouping reports by location suppresses duplicate influence but does not establish independent witnesses; a minimum cluster size does not by itself defeat differencing attacks. Present as a proposed design, not evidence of deployment.
- Commerce system with stock reservations and a transactional outbox (Chapters 31, 44; P09, P20, P27). An outbox prevents one class of omission but does not guarantee eventual delivery or prevent duplicate effects.
- Agent-automation tool (Chapter 24). Isolated working copies are not a security boundary; a command filter and stop control cannot recover effects already produced. Exclude zero-risk language.

Thematic resemblance establishes no influence or borrowing. Do not import claims about consciousness, universal entropy laws, cosmological foundations, or unverified performance.

## Placeholders to resolve with the author

Concordance sources for admissible degradation, continuous intervention, and semantic frameworks (Appendix C).
