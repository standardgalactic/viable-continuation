# Proof programme status

Generated from `frontmatter/spine.tex`. The spine is the source of truth; edit it, then update this table.

| Label | Family | Title | Status | Chapters |
|---|---|---|---|---|
| P01 | REP | History sufficiency and continuation equivalence | Elementary. Congruence requires the residual property. | 2, 41, 46 |
| P02 | INS | Establishment precedes selection | Elementary. | 4, 39, 41, 51 |
| P03 | VIA | Robust viability as a greatest fixed point | Elementary for the fixed point and the witnessing action. Convergence needs finiteness. | 13, 43, 54 |
| P04 | VIA | Obligation tightening cannot enlarge viability | Elementary on a common state space. Hypotheses to fix for the simulation version. | 13, 43, 50 |
| P05 | VIA | Local acceptability does not imply viable continuation | Elementary. Reported check in the companion (Appendix ref{app:companion}). | 15, 43, 46 |
| P06 | VIA | Safe degradation requires successor viability | Elementary, from P03. | 12, 43, 54 |
| P07 | VIA | A constructive certificate for compensating continuation | Elementary. | 14, 43, 53 |
| P08 | INS | Nominal exit and executable exit are distinct | Elementary. | 3, 29, 43, 53 |
| P09 | CMP | Local feasibility is insufficient under shared scarcity | Elementary. Reported check in the companion (Appendix ref{app:companion}). | 31, 44, 47, 58 |
| P10 | CMP | Independent viability composes under explicit independence | Hypotheses to fix. Reported check in the companion, with and without coupling. | 31, 44, 47 |
| P11 | REP | Accounting sufficiency requires factorization | Elementary. | 20, 21, 41, 49 |
| P12 | PRD | Financial improvement can accompany capability depletion | (a) elementary. (b) specification. | 8, 18, 45, 49 |
| P13 | REP | Scalar representation fails for genuine incomparability | (a) elementary; (b) hypotheses to fix, in particular the infinite case. | 16, 42, 48 |
| P14 | VIA | Corrective control has weak option value | Elementary. | 15, 43, 54 |
| P15 | REP | Proxy rewards underdetermine substantive contribution | Elementary. | 35, 45, 55 |
| P16 | CPT | Safe aspect relegation requires a detection-and-return margin | Fixed-tau form elementary. Endogenous form hypotheses to fix. | 23, 24, 45, 54 |
| P17 | REP | Verification transfers only through an adequate interpretation | Hypotheses to fix. | 25, 45, 55 |
| P18 | CMP | Economic processes form a category when interfaces compose | Hypotheses to fix. | 31, 44, 46, 47, 60 |
| P19 | CMP | Categorical accounting preserves specified composition laws | Elementary for a given posting system. | 20, 41, 49 |
| P20 | CMP | Typed execution: preservation and progress | Preservation elementary. Progress hypotheses to fix. | 12, 51, 52, 53, 54, 60 |
| P21 | CMP | Compatible local records glue exactly under the sheaf condition | Hypotheses to fix, per record system. | 22, 56, 57, 58, 60 |
| P22 | CMP | A cohomological obstruction in an affine coordination model | Graph case elementary, with a reported check in the companion. General sheaf case specification. | 17, 59, 60 |
| P23 | VIA | Comparative statics of viability | Elementary. | 13, 43, 50 |
| P24 | REP | Scarcity prices as dual variables | Hypotheses to fix. | 17, 44, 48 |
| P25 | VIA | Almost-sure and risk-constrained viability | Countable case: elementary. General-state version: research specification until the measurable domain and selection theorem are fixed. | 13, 43 |
| P26 | PRD | When waiting improves attainable value | Two-period form elementary. General form specification. | 9, 40, 43 |
| P27 | CMP | Circular assume-guarantee composition | Specification. The inductive form is the target statement. | 32, 44, 50 |
| P28 | INS | Surplus gain with a shrunken safe exit set | Proved in the hand-calculable housing model (Theorem H1 in the housing case). General statement: specification. | 29, 45, 53 |
| P29 | INS | When compensation restores capability | Proved in the housing model (Theorem H2 in the housing case): restoration requires availability, timing, and sufficiency. General statement: specification. | 19, 45, 49 |

Status vocabulary: *Elementary* (statement fixed, short proof indicated); *Hypotheses to fix* (statement fixed in outline, hypotheses to be pinned down where proved); *Specification* (result described, exact statement unsettled).

## What each unsettled item needs

- **P25** (Almost-sure and risk-constrained viability): Fix the measurable domain and a policy-selection theorem before stating the general-state result. Keep the countable case as the settled statement.
- **P26** (When waiting improves attainable value): General waiting theorem: compare information value against deterioration, forgone returns, and expiry, with survival possibly dependent on the payoff.
- **P27** (Circular assume-guarantee composition): State the circular assume-guarantee rule for safety properties with the step-indexed discipline and a time-indexed shared-capacity assumption; prove it by induction.
- **P28** (Surplus gain with a shrunken safe exit set): Generalize beyond the deterministic prepaid-lease model (Theorem H1): stochastic shocks, heterogeneous exit costs, a priced exit option.
- **P29** (When compensation restores capability): Generalize beyond Theorem H2: markets with search frictions, in-kind compensation, irreversible loss.
- **P12** (Financial improvement can accompany capability depletion): Part (b): the viability threshold k*(M) and conditions for a jump or kink. Nonlinear deterioration alone is not sufficient.
- **P16** (Safe aspect relegation requires a detection-and-return margin): Endogenous competence version: state the monotonicity hypotheses and derive the minimal practice expenditure.
- **P13** (Scalar representation fails for genuine incomparability): Infinite case of the multi-utility representation; confirm the order-dimension statement.
- **P18** (Economic processes form a category when interfaces compose): Write the quotient construction in full and verify the congruence and category laws.
- **P20** (Typed execution: preservation and progress): Fix the progress hypotheses (resources, counterparties, environment).
- **P21** (Compatible local records glue exactly under the sheaf condition): Prove the sheaf property for one concrete record system and exhibit a presheaf that fails gluing.
- **P22** (A cohomological obstruction in an affine coordination model): Develop graph price potentials completely before the torsor formulation; state coefficient sheaf, cocycle, equivalence, and the meaning of trivialization.
- **P10** (Independent viability composes under explicit independence): Write the simulation argument for the reverse inclusion in full.
- **P17** (Verification transfers only through an adequate interpretation): State the soundness relation precisely and treat liveness and probabilistic claims separately.
- **P24** (Scarcity prices as dual variables): Separability and decentralization hypotheses; worked small allocation problem.
- **P04** (Obligation tightening cannot enlarge viability): Simulation-relation version for obligations that enlarge the state.
