# WARNING: parts/*.tex are now plain TeX that may have been hand-edited. Running this script OVERWRITES them.
# Use only to regenerate the skeleton from scratch, or read it as the source of the original chapter summaries.
"""Generate parts/partNN.tex and frontmatter/spine_table.tex from one data table."""
import os
import sys

ROOT = sys.argv[1]

PARTS = [
 ("I", "Economic Activity and the Establishment of Futures",
  "Part I fixes what an economy maintains and introduces the objects the rest of the book relies on: states, histories, continuations, and the distinction between what is possible, accessible, permitted, and acceptable.",
  "Define the building, its tenants, and the repair crew, and list the states and histories that matter: rent arrears, deferred work, and notices served."),
 ("II", "Production, Maintenance, and Irreversibility",
  "Part II treats production as the transformation of conditions, capital as maintained capability, and irreversibility as a symmetric property of action and inaction.",
  "Roof and plumbing deteriorate; producing a habitable unit transforms the building's conditions; the cost of deferred maintenance is traced forward."),
 ("III", "Obligations, Degradation, and Recovery",
  "Part III represents obligations through time and introduces viability kernels, safe degradation, compensating continuation, and corrective capacity.",
  "Tenancy and repair duties become obligations, an unheated unit may not be let, and viability is studied under a maintenance budget."),
 ("IV", "Value, Prices, Accounting, and Debt",
  "Part IV compares valuations, prices, profit, debt, and accounts as representations, and asks what each preserves of the underlying continuation structure.",
  "Rent, reserves, and the landlord's reported profit are set beside the maintenance backlog, which no conventional account records as a liability."),
 ("V", "Knowledge, Attention, and Productive Competence",
  "Part V studies representations, memory, skill, automation, and verification as supports for, or threats to, competent continued action.",
  "Inspection records, contractor knowledge, and automated scheduling are examined, along with what a passed inspection establishes."),
 ("VI", "Institutions, Power, and Distribution",
  "Part VI analyzes classifications, property, contracts, exit, and public authority as distinctions that alter which continuations are accessible and to whom.",
  "Tenure, deposits, notice periods, and a tenant's executable capacity to leave are placed in one model."),
 ("VII", "Markets, Firms, Commons, and Coordination",
  "Part VII asks when individually acceptable commitments compose into a feasible collective arrangement, in markets, firms, platforms, and commons.",
  "A shared crew serves several buildings, listings run through a platform, and a cooperative maintenance fund pools contributions."),
 ("VIII", "Ecology, Care, Technology, and Development",
  "Part VIII applies the framework to ecological reproduction, care, productive infrastructure, development, and coordinated transitions, and closes the economic text.",
  "An energy retrofit is a transition with a viable path, and damp and mould are ecological conditions of the dwelling."),
 ("IX", "Mathematical Foundations and Economic Results",
  "Part IX consolidates the formal machinery and states the principal results with hypotheses, organized by theorem family. It is the formal centre of the book.",
  "The housing model is stated formally, its viability kernel is computed, and the finite-state companion reproduces the results and their counterexamples."),
 ("X", "Categorical Interpretations",
  "Part X interprets economic processes as morphisms and states what the interpretation preserves. Its stated payoff is that parallel composition fails to be independent under shared sinks, and the structure needed to repair that is identified.",
  "Repair processes become morphisms between building interfaces, and accounting becomes a functor that forgets the backlog."),
 ("XI", "Type Theoretic Interpretations",
  "Part XI interprets states, permissions, and commitments as types. Its stated payoff is the precise gap between formal inhabitation and real-world executability, and the separate roles of preservation and progress.",
  "Repair commitments are typed with deadlines and explicit failure branches, and degraded operating modes carry evidence."),
 ("XII", "Sheaf Theoretic Interpretations",
  "Part XII interprets local knowledge and plans over overlapping contexts. Its stated payoff is the distinction between a presheaf of plans and a sheaf of feasible allocations, together with one genuine cohomological obstruction.",
  "Landlord, city, and contractor each hold local records, and gluing succeeds or fails depending on whether the shared crew is represented."),
]

# (num, part_index, title, summary, ptags, optional display equation)
CH = []
def ch(n, p, title, summary, tags=(), eq=None):
    CH.append((n, p, title, summary, list(tags), eq))

# ---- Part I
ch(1,0,"What an Economy Maintains",
 "Introduces an economy as an organization of provisioning, transformation, and maintenance through time, using a household, a construction firm, a hospital, and a watershed to show the range of relevant processes. Separates current output from the reproduction of the conditions that make output possible, and shows how one transaction can generate income while exhausting productive capacity elsewhere.")
ch(2,0,"States, Histories, and Continuations",
 "Introduces economic states, histories, actions, and transition relations. States when a present-state description is sufficient and when accumulated obligations, deterioration, learning, or institutional commitments require history to remain explicit. The basic object is a set of possible trajectories, not a single forecast. The first theorem characterizes sufficient state augmentation: a compressed history is adequate when histories with the same summary have equivalent consequences for the future questions at issue.",
 ["P01"], r"x_{t+1}\in T(x_t,h_t,a_t),\qquad h_{t+1}=U(h_t,x_t,a_t,x_{t+1}).")
ch(3,0,"Feasibility, Accessibility, and Admissibility",
 "Separates physically possible actions, practically accessible actions, institutionally permitted actions, and actions consistent with stated obligations. Examines why formal eligibility does not establish effective access and why an available choice need not be an acceptable continuation. Examples are housing, employment, medical treatment, and access to credit.",
 ["P08"])
ch(4,0,"Establishing the Domain of Choice",
 "Examines the work required to make alternatives available before selection can occur. Search, education, infrastructure, legal recognition, invention, and interface design become explicit economic activities. A two-stage model distinguishes expenditures that establish an opportunity domain from expenditures that select within it.",
 ["P02"])
ch(5,0,"Welfare Without Counting Options",
 "Addresses the normative foundations directly. More possible trajectories do not automatically make a better life, and constraints can protect some people while excluding others. Develops plural assessments involving substantive achievement, security, burden, access, and corrective freedom, and makes disagreements about those assessments explicit.")

# ---- Part II
ch(6,1,"Production as Transformation of Conditions",
 "Represents production through its outputs, consumed inputs, residuals, new obligations, and changes to future productive capacity. Compares a production function with a richer transition description and shows which questions each representation can answer.")
ch(7,1,"Capital as Maintained Capability",
 "Examines machines, buildings, knowledge, networks, and institutional arrangements as capabilities that require continued support. Capital valuation depends on complementary inputs, repairability, skills, and access, not on possession alone. A worked example compares two machines with identical output but different maintenance dependencies.")
ch(8,1,"Maintenance and the Reproduction of Capacity",
 "Develops maintenance schedules, deterioration processes, deferred work, and critical thresholds. A formal model shows how short-run expenditure reductions can reduce long-run feasible output when deterioration is nonlinear. Preventive maintenance is distinguished from restoration after failure.",
 ["P12"])
ch(9,1,"Irreversible Decisions and the Value of Waiting",
 "Connects continuation economics to established work on irreversible investment and option value. Examines when waiting preserves useful information and when delay itself destroys opportunities. The result is a symmetric treatment of action and inaction as potentially irreversible.",
 ["P26"])
ch(10,1,"Residuals, Waste, and the Afterlives of Production",
 "Investigates demolition, abandoned infrastructure, pollution, obsolete software, and administrative residues. Asks what persists after an activity's advertised purpose has ended, and extends responsibility to the disposition of those residuals.")

# ---- Part III
ch(11,2,"Obligations Through Time",
 "Represents contracts, promises, legal duties, maintenance commitments, and informal responsibilities as obligations with bearers, beneficiaries, triggers, deadlines, and discharge conditions. Explains why obligations cannot generally be inferred from a balance sheet or a snapshot of resources.")
ch(12,2,"Required Functions and Optional Capabilities",
 "Distinguishes functions that must continue from capabilities that can be reduced or suspended, and examines how these classifications are established, challenged, and revised. A public-service example shows that declaring a function optional is itself a consequential institutional decision.",
 ["P06","P20"])
ch(13,2,"Viability Under Scarcity",
 "Introduces viability kernels and constrained reachability, and distinguishes a desirable target from the set of states from which obligations can still be fulfilled. Uncertainty is treated separately for deterministic, robust, and probabilistic models. Comparative statics for added duties, capacity, and exposure are stated together.",
 ["P03","P04","P23","P25"],
 r"K=\bigl\{x:\exists\pi\ \text{such that all trajectories permitted by the model under }\pi\ \text{satisfy the continuation constraints}\bigr\}.")
ch(14,2,"Compensating Continuation",
 "Links suspension to restoration obligations, deadlines, and reserved resources. Distinguishes credible compensation from promises that depend on capabilities already being consumed. Worked cases are deferred building repairs, reduced hospital services, and temporary infrastructure closures.",
 ["P07"])
ch(15,2,"Corrective Capacity and Recoverability",
 "Defines the resources, permissions, knowledge, and time required to correct a course of action. Examines systems that remain operational while losing the ability to recover from foreseeable disturbances. A theorem gives conditions under which locally admissible steps leave the admissible region over a longer horizon.",
 ["P05","P14"])

# ---- Part IV
ch(16,3,"Valuing Feasible Futures",
 "Develops valuations over trajectories, capability bundles, and contingent opportunities. Monetary valuation is one representation among several. Identifies circumstances in which scalar representations exist and circumstances in which relevant comparisons remain partial.",
 ["P13"])
ch(17,3,"Prices as Compressed Coordination Signals",
 "Studies prices as economical representations that permit decentralized coordination while omitting much of the underlying causal structure. Asks which omissions are tolerable for a given decision and which require supplementary records, standards, or institutions. Scarcity prices appear as dual variables, and an exchange-rate graph gives the first obstruction example.",
 ["P22","P24"])
ch(18,3,"Profit and the Location of Costs",
 "Decomposes financial profitability into revenues, recognized costs, transfers of burden, and changes in maintained capacity. A worked enterprise model distinguishes profit supported by reproducible productivity from profit supported by deferred replacement or unpriced damage.",
 ["P12"])
ch(19,3,"Monetary Debt and Restoration Obligations",
 "Distinguishes financial liabilities from duties to repair ecological, infrastructural, or social damage. Explores when obligations can be transferred or monetized and when substitution fails because the relevant beneficiary, place, or lost capability matters.",
 ["P29"])
ch(20,3,"Accounting for Continuation",
 "Proposes supplementary accounts for maintenance backlogs, recovery reserves, critical dependencies, and outstanding disposition duties. These accompany conventional accounts without presuming that every dimension can be aggregated into one number. The practical aim is auditable visibility.",
 ["P11","P19"])

# ---- Part V
ch(21,4,"Economic Representations and Semantic Compression",
 "Examines the representations used in planning, forecasting, classification, and coordination. A useful representation preserves distinctions relevant to action while compressing others. Defines task-relative representational adequacy.",
 ["P11"])
ch(22,4,"Memory as Organizational Capital",
 "Examines records, provenance, routines, and institutional memory as supports for continued competent action. Distinguishes retained information from retrievable and usable knowledge, and investigates when forgetting reduces costs without erasing obligations.",
 ["P21"])
ch(23,4,"Aspect Relegation and the Economics of Skill",
 "Models practice and routine as changes in the attention required to perform a task adequately. Relegation frees resources while creating dependence on stable conditions. Develops the economic significance of recognizing when a task must return to explicit supervision.",
 ["P16"])
ch(24,4,"Automation and the Preservation of Intervention",
 "Assesses automation through output, error, oversight burden, retained competence, and recovery time. A formal example shows why removing human involvement can lower immediate costs while raising the cost of rare failures, with response time made endogenous to retained competence.",
 ["P16"])
ch(25,4,"Verification, Proxies, and Institutional Confidence",
 "Distinguishes what an audit, benchmark, certification, or formal proof actually establishes. Examines the economic effects of treating a passed check as broader evidence than its specification warrants.",
 ["P17"])

# ---- Part VI
ch(26,5,"Distinctions That Allocate Futures",
 "Examines property categories, employment classifications, citizenship, credit status, and professional credentials as distinctions that alter accessible continuations. Connects the theory of distinction and continuation to institutional economics.")
ch(27,5,"Property as Structured Authority",
 "Analyzes property through permissions to use, exclude, modify, transfer, encumber, and abandon. Distinguishes ownership from the practical capacity to exercise those permissions and from the burdens imposed on others.")
ch(28,5,"Contracts and the Evolution of Dependence",
 "Studies contracts as trajectory-shaping arrangements. Examines how repeated agreements alter bargaining positions, switching costs, and the conditions of later consent, and analyzes cumulative dependence under continuing intervention.")
ch(29,5,"Distribution of Exit and Refusal",
 "Treats inequality as including unequal capacities to leave employment, housing, platforms, financial relationships, and harmful environments. Distinguishes nominal exit rights from executable exit paths, and states when an intervention can raise surplus while shrinking a participant's safe exit set.",
 ["P08","P28"])
ch(30,5,"Public Authority and the Admissibility of Constraints",
 "Addresses democratic authorization, contestability, rights, and institutional revision. Examines who establishes continuation constraints, how conflicts among them are adjudicated, and what prevents preservation language from legitimating domination.")

# ---- Part VII
ch(31,6,"Exchange and Compatible Commitments",
 "Models exchange as a transformation of resources, permissions, and obligations among participants. Identifies conditions under which individually acceptable exchanges compose into a feasible collective arrangement.",
 ["P09","P10","P18"])
ch(32,6,"Firms as Organizations of Complementary Continuation",
 "Treats firms as coordinating tasks, assets, knowledge, and promises that cannot be maintained through isolated transactions alone. Boundaries of the firm are examined through coordination costs, authority, dependence, and the distribution of residual responsibilities.",
 ["P27"])
ch(33,6,"Platforms and Infrastructural Dependence",
 "Studies platforms as institutions that establish opportunity domains while controlling access to them. Examines interoperability, portability, unilateral rule changes, and the appropriation of complementary investment.")
ch(34,6,"Commons and Shared Maintenance",
 "Analyzes shared resources through contribution rules, monitoring, access, replenishment, and conflict resolution. Distinguishes common ownership from the actual organization of maintenance.")
ch(35,6,"Contribution, Reward, and Measurement",
 "Uses work-backed currencies, contribution scores, and automated reward systems as worked cases. Shows how reward mechanisms change the activity they measure and why maintenance and preventive work are particularly hard to recognize through simple activity counts.",
 ["P15"])

# ---- Part VIII
ch(36,7,"Ecological Reproduction and Economic Time",
 "Introduces ecosystems as dynamic conditions of provisioning with thresholds, regeneration rates, and spatial dependencies. Investigates conflicts between financial horizons and ecological restoration times.")
ch(37,7,"Care and the Maintenance of Persons",
 "Treats care as skilled, materially supported work that sustains people's capacities and relationships. Addresses unpaid labour, dependency, exhaustion, and the danger of valuing persons solely through productive contribution.")
ch(38,7,"Local AI and the Ownership of Productive Infrastructure",
 "Uses local inference, rented cloud services, persistent agents, and open software as a sustained case study. Compares total costs, supplier dependence, maintenance burdens, portability, and the distribution of control.")
ch(39,7,"Development as the Establishment of Capabilities",
 "Treats development as building accessible domains of action through education, health, infrastructure, legal security, and collective competence. Examines the tension between increasing output and preserving communities' authority over the conditions of their lives.",
 ["P02"])
ch(40,7,"Crisis, Transition, and Institutional Repair",
 "Culminates the economic text in coordinated transitions involving energy, housing, public finance, and industrial change. Explains why a viable destination is insufficient without a viable path, and examines transition funding, temporary protections, restoration duties, and mechanisms for revising a failing plan.",
 ["P26"])

# ---- Part IX
ch(41,8,"Transition Systems and History Compression",
 "Consolidates the formal machinery used throughout the book. Establishes sufficient-state conditions, observational equivalence, and history-dependent constraints, with careful treatment of what a chosen state representation forgets. The representation family is stated here as a single factorization lemma with a dynamic congruence version.",
 ["P01","P02","P11","P19"])
ch(42,8,"Orders, Dominance, and Incomparability",
 "Equips continuation profiles with partial orders reflecting specified dimensions of improvement. Establishes conditions for dominance and explains why inclusion, cardinality, and scalar utility are different comparisons. Any impossibility result concerning scalarization states the preservation requirements that generate it, and the multi-utility companion is given.",
 ["P13"])
ch(43,8,"Reachability, Robustness, and Recovery",
 "Develops finite-state algorithms and selected continuous models for viability and corrective reachability, with the fixed-point theorem and comparative statics. Compares worst-case guarantees with probabilistic guarantees and analyzes the effects of model uncertainty, including almost-sure and risk-budget variants. Includes the waiting theorem.",
 ["P03","P04","P05","P06","P07","P08","P14","P23","P25","P26"])
ch(44,8,"Composition and Systemic Failure",
 "Assembles local contracts into networks with shared resources and timing constraints. Counterexamples show how individually feasible commitments become jointly infeasible. Positive results identify sufficient compatibility and resource conditions, including independent composition, scarcity prices, and circular assume-guarantee reasoning.",
 ["P09","P10","P18","P24","P27"])
ch(45,8,"Measurement and Empirical Identification",
 "Translates theoretical quantities into observable indicators and study designs. Maintenance records, switching costs, recovery times, service interruptions, and obligation fulfillment provide evidence. Explains which causal claims require experiments, natural experiments, longitudinal data, or structural assumptions.",
 ["P12","P15","P16","P17","P28","P29"])

# ---- Part X
ch(46,9,"Economic Processes as Morphisms",
 "Takes specified economic interfaces or states as objects and admissible transformations, carrying explicit resource and obligation effects, as morphisms. Identity and composition are defined before any categorical claim. The construction begins with the syntactic congruence of the admissible-history language, and where ordinary composition is inadequate the chapter states the extra structure required.",
 ["P01","P05","P18"])
ch(47,9,"Parallel Production and Monoidal Structure",
 "Represents processes performed alongside one another through a monoidal structure. Shared labour, ecological sinks, or scarce machinery complicate the interpretation of independence. String-diagram notation stays optional, and algebraic presentations suffice for the arguments.",
 ["P09","P10","P18"])
ch(48,9,"Resources, Obligations, and Enriched Categories",
 "Motivates enrichment over appropriate ordered structures by costs, delays, risks, and resource requirements. Develops multidimensional cost composition and identifies when a single numerical distance suppresses economically relevant distinctions.",
 ["P13","P24"])
ch(49,9,"Accounting as a Structure-Preserving Map",
 "Connects operational processes to accounting representations by functors. The central question is what information an accounting map preserves, identifies, or loses. Two economically different processes can have the same financial image, which gives a precise form of accounting insufficiency relative to a stated task.",
 ["P11","P12","P19","P29"])
ch(50,9,"Open Systems, Institutions, and Compositional Guarantees",
 "Describes households, firms, and infrastructures through interfaces in an open-systems formalism. Develops an assume-guarantee treatment of institutional composition and identifies conditions under which local guarantees support a global continuation claim. Categorical language organizes the proof obligations while empirical premises remain independently necessary.",
 ["P04","P23","P27"])

# ---- Part XI
ch(51,10,"Economic States and Admissible Actions as Types",
 "Describes states, resources, permissions, and actions with specified preconditions as types. Dependent types express actions whose availability depends on current resources or established authority. Distinguishes formal inhabitation from real-world executability.",
 ["P02","P20"], r"\operatorname{Act}:\operatorname{State}\rightarrow\operatorname{Type}.")
ch(52,10,"Linear and Affine Resources",
 "Models resources that cannot be duplicated freely, or that may be discarded under specified rules, with linear and affine type systems. Money, physical goods, permissions, information, and obligations need different treatments, and no single resource discipline is imposed on all economic objects.",
 ["P20"])
ch(53,10,"Obligations, Deadlines, and Protocols",
 "Expresses exchanges and institutional procedures over time with session types and indexed judgments. Examines escrow, delivery, payment, default, and repair protocols, including explicit failure branches.",
 ["P07","P08","P20","P28"])
ch(54,10,"Proof-Carrying Commitments and Verified Degradation",
 "Commitments carry evidence of specified properties, and degraded operating modes require evidence that required functions remain supported. Small formal examples show how proofs depend on resource models, trusted observations, and assumptions about counterparties.",
 ["P03","P06","P14","P16","P20"])
ch(55,10,"Refinement, Interpretation, and the Limits of Formal Assurance",
 "Connects abstract economic obligations with executable checks through refinement types. Distinguishes a verified implementation from a justified specification and explains why formal consistency cannot establish fairness, truthful input data, or ecological adequacy by itself.",
 ["P15","P17"])

# ---- Part XII
ch(56,11,"Local Economic Knowledge and Overlapping Contexts",
 "Introduces a base of contexts such as jurisdictions, organizations, regions, or information domains. Restriction maps describe how a claim or plan appears within a narrower context. The choice of base is economically motivated and explicit.",
 ["P21"])
ch(57,11,"Presheaves of Plans, Accounts, and Commitments",
 "Local plans and records form presheaves when restriction is well defined. Asks whether accounts agree on overlaps, whether obligations receive consistent treatment across departments, and whether local descriptions omit shared dependencies.",
 ["P21"])
ch(58,11,"Gluing and Global Feasibility",
 "Interprets the sheaf condition as a compatibility-and-reconstruction property. Distinguishes agreement of descriptions from feasibility of the described activity: matching local plans can still compete for a globally scarce resource unless that resource is represented in the model. Examples show when gluing succeeds and when the proposed assignment is only a presheaf.",
 ["P09","P21"])
ch(59,11,"Obstructions, Inconsistency, and Institutional Boundaries",
 "Investigates failures of global coordination through carefully chosen mathematical models. Cohomological methods are introduced only where an appropriate coefficient structure and a justified obstruction interpretation exist. Distinguishes a genuine mathematical obstruction from a loose analogy about disagreement, beginning with the frictionless exchange graph.",
 ["P22"])
ch(60,11,"Descent, Federation, and the Organization of Collective Futures",
 "Examines how independently governed institutions can coordinate compatible records, rights, and obligations without one institution absorbing the others. Brings the three interpretations together: categorical composition for processes, type theoretic judgments for admissibility, and sheaf theoretic compatibility for local-to-global coordination.",
 ["P18","P20","P21","P22"])


NOTES = {
 16: r"Candidate import: the identity $D_{\mathrm{KL}}(P(\cdot\mid B)\,\|\,P)=-\log P(B)$ for $0<P(B)\le 1$ as a measure of probabilistic restriction. It does not by itself give a monetary cost, a physical dissipation, or a conservation law.",
 17: r"Candidate import: allocation of finite maintenance capacity, $\max_{r_i\ge 0}\sum_i V_i(r_i)$ subject to $\sum_i r_i\le B$, with the budget an explicit assumption and the shadow price as dual variable. No universal conservation of ambiguity is assumed.",
 22: r"Candidate import: separate replay integrity from historical authority. A self-consistent checkpoint is not an independently trusted history, and branch selection is not evidence that the chosen branch is true. An institution can keep reproducible accounts without establishing that inputs are truthful or commitments legitimate.",
 23: r"Candidate import: distinguish expenditure from damage to regenerative capacity, and allocate finite repair capacity through explicit response functions.",
 25: r"Candidate counterexample: a ledger verifier that checks seals against stored roots without recomputing them from contents, and checks debits one at a time without aggregating repeated postings, so that individually permissible debits jointly exceed the stated balance restriction. A check can succeed while omitting the relation a reader assumes it verifies.",
 33: r"Candidate import: revenue with a participation term, $R(q)=(\alpha q+\beta)M(q)$, so $R'(q)=\alpha M(q)+(\alpha q+\beta)M'(q)$. Revenue can fall as match quality rises if participation falls strongly enough with quality. This is a conditional incentive result only.",
 54: r"Candidate import: reconstruction by replay with canonical encoding, parent and tick validation, duplicate-operation handling, and refusal records, stated with the distinction between replay integrity and historical authority.",
 8: r"Correction to carry over from earlier manuscripts: a nonpositive long-run average net accumulation rate does not ensure bounded debt, since $D(t)=\sqrt{1+t}-1$ is unbounded with average rate tending to zero. A bounded-debt theorem needs $\sup_{t\ge 0}\int_0^t(\rho_M-\rho_R)\,du<\infty$, or a reflected-backlog formulation.",
 58: r"Repair exercises: a local-repair condition need not produce a global section; a lower-energy imperfect candidate can beat an exact match under a penalized reconstruction; and a circle example must not state contradictory overlap values.",
}

NOTES[20] = r"Candidate case (documentation-level only): a two-ledger design that keeps official spending commitments separate from community observations and reports their divergence instead of averaging them. Distinguish an obligation, a reported action, evidence of performance, and discharge of the obligation as four different institutional events."
NOTES[24] = r"Candidate case (documentation-level only): an agent-automation tool. Isolated working copies are not an operating-system security boundary, and a command filter or stop control cannot recover effects that have already occurred. The economic question is how much review, intervention time, and recoverability the automation actually preserves. Exclude any zero-risk claim."
NOTES[30] = r"Candidate question: what must happen before a repair obligation may legitimately be discharged? A waiting period is an enforceable procedural condition but elapsed time cannot establish successful repair. Closure should require procedural authorization and specified evidence, with a route for reopening a failed repair. Grouping reports by location suppresses duplicate influence but does not establish independent witnesses, and a minimum cluster size does not by itself protect against all differencing attacks. Present as a proposed institutional design, not evidence of deployment."
NOTES[31] = r"Candidate case (documentation-level only): two customers each receive an apparently feasible offer for the last item while one purchase can be fulfilled. Reservations add time: resources are withheld, expire, and return. Authorization and resource commitment must stay consistent under concurrent requests (P09)."
NOTES[44] = r"Candidate case: a transactional outbox records the obligation to send an event in the same transaction as the order, which prevents one class of omission. Without further assumptions it does not guarantee eventual delivery or prevent duplicate effects at the recipient, which separates accounting consistency from operational progress (P20, P27)."

assert [c[0] for c in CH] == list(range(1, 61))

ROMAN = [p[0] for p in PARTS]

def ptags_text(tags):
    return ", ".join(r"\Pref{%s}" % t for t in tags)

# ---- write part files
for pi, (rn, title, intro, housing) in enumerate(PARTS):
    lines = []
    lines.append(r"\part{%s}" % title)
    lines.append(r"\label{part:%s}" % rn)
    lines.append("")
    lines.append(intro)
    lines.append("")
    lines.append(r"\begin{housing}%s\end{housing}" % housing)
    lines.append("")
    for n, p, t, summ, tags, eq in CH:
        if p != pi:
            continue
        lines.append(r"\chapter{%s}\label{ch:%d}" % (t, n))
        lines.append(summ)
        if eq:
            lines.append(r"\[")
            lines.append(eq)
            lines.append(r"\]")
        if tags:
            lines.append(r"\chspec{%s.}" % ptags_text(tags))
        if n in NOTES:
            lines.append(r"\draftnote{%s}" % NOTES[n])
        lines.append(r"\scaffold")
        lines.append("")
    path = os.path.join(ROOT, "parts", "part%02d.tex" % (pi + 1))
    with open(path, "w") as f:
        f.write("\n".join(lines))

# ---- table P -> chapters
ptag_set = sorted({t for c in CH for t in c[4]})
band = lambda n: 0 if n <= 40 else (1 if n <= 45 else 2)
rows = []
fam = {}
# family tags parsed from the spine file
import re
spine = open(os.path.join(ROOT, "frontmatter", "spine.tex")).read()
for m in re.finditer(r"\\begin\{pspec\}\{(P\d\d)\}\{.*?\}\{(\w+)\}", spine):
    fam[m.group(1)] = m.group(2)
missing = [p for p in ("P%02d" % i for i in range(1, 30)) if p not in fam]
assert not missing, missing
for i in range(1, 30):
    p = "P%02d" % i
    bands = [[], [], []]
    for n, _, _, _, tags, _ in CH:
        if p in tags:
            bands[band(n)].append(n)
    cell = lambda b: ", ".join(r"\chref{%d}" % n for n in b) if b else "--"
    rows.append((p, fam[p], cell(bands[0]), cell(bands[1]), cell(bands[2])))

out = [r"\begin{center}", r"\small", r"\renewcommand{\arraystretch}{1.15}",
       r"\begin{longtable}{@{}llp{0.25\linewidth}p{0.12\linewidth}p{0.22\linewidth}@{}}",
       r"\toprule", r"Result & Family & Early (I--VIII) & Rigorous (IX) & Reinterpreted (X--XII)\\",
       r"\midrule", r"\endhead"]
for p, f, a, b, c in rows:
    out.append(r"\Pref{%s} & \textsc{%s} & %s & %s & %s\\" % (p, f, a, b, c))
out += [r"\bottomrule", r"\end{longtable}", r"\end{center}"]
with open(os.path.join(ROOT, "frontmatter", "spine_table.tex"), "w") as f:
    f.write("\n".join(out) + "\n")

print("chapters:", len(CH), "parts:", len(PARTS))
for p, f, a, b, c in rows:
    if a == "--" or b == "--" and c == "--":
        print("note: sparse", p, a, b, c)
