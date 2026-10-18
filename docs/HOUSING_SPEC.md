# Housing case specification

Single source for the running example. Extend it here before using new features in a chapter.

## Conventions

Currency units, months, no discounting until a chapter introduces a discount factor $\beta$ explicitly. Flows are per month. Resources are nonnegative liquid balances. Signs: income and receipts positive, payments negative in accounts; in formulas $r$ is rent paid, $e\ge 0$ is net monthly surplus after rent and living costs.

## Participants

Tenant (resources $x$, surplus $e$), landlord, contractor (crew capacity), public authority (rules, inspections), financial accounts (ledger of the landlord), outside housing opportunities (units available in a window $[a,E]$ at exit cost $c$).

## Already specified (Theorems H1 and H2, `frontmatter/housing.tex`)

Prepaid lease: length $T$ months, discount $\delta$, prepayment $P=(1-\delta)rT$, non-refundable, landlord saves $\kappa$ per contract. Exit within horizon $H$ needs resources at least $c$ at the exit date. Worked numbers: $r=1000$, $T=12$, $\delta=0.05$, $e=200$, $c=4000$, $H=3$, $\kappa=800$, so $P=11400$; tenants with $11400\le x<11800$ lose an executable exit; $m^*(11500)=300$; full restoration for the worst case costs 400 against a landlord net gain of 200. Reproduced in `companion/vcc/housing.py`.

## To be added, in this order

1. **Physical condition.** A dwelling condition variable $k$ with deterioration $d(k)$ and maintenance expenditure $M$, $k_{t+1}=k_t-d(k_t)+g(M_t)$. Parameters chosen so a property has positive cash flow while $k$ falls (P12). Hand-calculable table over ten months.
2. **Obligations.** Repair duty with trigger, deadline, payer, and discharge condition; tenant duties; a rule that a unit below a habitability threshold may not be let. Compute joint feasibility.
3. **Accounts.** Landlord ledger balanced, maintenance backlog, restoration schedule side by side (Chapters 18 to 20).
4. **Contractor and shared crew.** Two jobs each feasible alone whose deadlines cannot both be met by one crew (P09, P10).
5. **Repair discharge.** Closure of a repair obligation requires procedural authorization (for example a waiting period) and specified evidence, with a route to reopen a failed repair. Model evidence reliability, incentives, and collusion explicitly.
6. **Disturbances.** Shocks to $x$, to deterioration, and to crew availability; robust and almost-sure versions of viability (P03, P25).
7. **Information problems.** Hidden condition, verification of repairs, inspection records (Chapters 22, 25).
8. **Institutional change.** Public authority changes a rule or a fee; compare kernels before and after (P04, P23); transition path (Chapter 40).
9. **Records across institutions.** Landlord, city, and contractor records as a presheaf; gluing succeeds or fails depending on whether the shared crew is represented (Part XII).

For every addition: list observed quantities, uncertain quantities, and which decisions belong to which participant; add a hand-calculable version; add a companion check; keep earlier numbers unchanged.
