# Ticket 03 — skill body shape: what the two ports showed

Prototype, branch `prototype/skill-body-shape`. Two real skills ported into the candidate
shape: `concept-brief` (small, conversational) and `mockup-walkthrough-astro` (1,133 lines,
the collection's worst case). Both ports are here to be read, not merged.

## Measurements

| | source | port | body only |
|---|---|---|---|
| `concept-brief` | 289 (87 frontmatter) | **80** (15 fm) | 202 → **65** (−68%) |
| `mockup-walkthrough-astro` | 1,133 (51 fm) | **110** (18 fm) | 1,082 → **92** (−91%) |

The astro port's displaced content, all of it still present:

- `references/scaffold/` — the 7 verbatim file bodies, now **295 lines of real files** the
  skill copies instead of writing out from a fence.
- `references/specs-json.md` — 130 lines of schema plus the specs→manifest projection rules.
- `contracts/walkthrough_renderer.md` — **nothing moved here**; it was already there. The
  removed ~200 lines of STEP 2 were restating the contract's § Target resolution, § Auto-slug
  fallback and § Spec reference panel almost verbatim.
- `validator.py` — nothing moved here either. All 20 CHECKLIST items are already mechanical
  checks in the 37 KB validator (verified: `app_nav`, `spec-panel`, `data-spec-provisional`,
  `dist`, `schema_version`, `data-spec-index`, `sample_rows`, `stylesheet`, `canonical` all
  appear as checks). Item 20 was literally "Validator exits 0".

Collection-wide, measured across the 88 `SKILL.md` files (24,646 lines), before rewriting a
single line of prose:

| | lines | share |
|---|---|---|
| frontmatter | 4,562 | 18% |
| inside code fences | 2,250 | 9% |
| the ten boilerplate sections | 3,972 | 16% |
| **mechanically removable subtotal** | **10,784** | **44%** |

Per-section: `Overview` 1,068 lines / 79 skills · `Common Mistakes` 578 / 55 ·
`Context Budget` 450 / 39 · `Prerequisites` 428 / 50 · `When to Use` 426 / 63 ·
`When NOT to Use` 384 / 60 · `Depth Behavior` 272 / 30 · `Integration` 192 / 28 ·
`Standalone Mode` 128 / 24 · `Research Mode` 46 / 5.

**Extrapolation.** That 44% needs no judgement — it is deletion, extraction and frontmatter
pruning. The ports went considerably further (−68% / −91%) because the remaining prose was
itself duplicating shared contracts. At 30 skills averaging the ports' ~95 lines, `-mp` lands
near **3,000 lines against today's 24,646** — the same order as mp's 2,945 for 25 skills.

## The ticket's questions, answered

**Does the DSL's disappearance lose anything an agent needed?** No. Every DSL construct in
the astro skill resolved to something that already existed elsewhere:
`ROLE`/`READS`/`WRITES`/`REFERENCES` restated frontmatter and the contracts list;
`CHECKLIST` restated `validator.py`; `MUST`/`NEVER` restated constraints already stated in
the steps; `EMIT` is consumed by nothing — grepping the two consumers (`forge-concept`,
`@skaile/workspaces`) finds `EMIT` only inside other `SKILL.md` files. The DSL is a fourth
instruction register laid over three others, and the same fact appearing in three registers
is how the astro config constraints ended up stated three times.

Only **4 of 88** skills carry `## MUST / NEVER`, `## CHECKLIST` or `## ROLE / READS / …`
at all — so the grammar is a cost `contracts/skill_grammar.md` charges to all 88 and four
actually spend.

**Where does the 1,133-line skill's content go, and does an agent know when to load it?**
Two reference files, and yes. `references/scaffold/` is reached by exactly one branch — the
init run, step 3 — and a copy needs no reading at all. `references/specs-json.md` is reached
at steps 4 and 6, named at both. Neither is loaded by an update run that only regenerates
data, which is the common case.

**Frontmatter against the read-set.** Prototyped against ticket 01's read-set plus
`name`/`description`: `concept-brief` 87 → 15 lines, astro 51 → 18. Nothing was missed —
but the cut is uneven, and the reason is worth a ticket. Astro's 18 lines are all real gates.
`concept-brief`'s 15 are almost entirely `prerequisites.inputs_optional`: an 8-field **input
dialog spec**, which is UI data that forge-concept renders, sitting in a prose file. It is
the single thing standing between the concept-side skills and mp's 4–6 line frontmatter.
Moving the dialog specs into the machine layer would take `concept-brief`'s frontmatter to
**4 lines**. → raise with tickets 09 and 11.

**Do constraints survive without a MUST/NEVER block?** Yes, and two of them got sharper.
Every constraint in both skills re-expressed positively, at the step it binds:

| original | became |
|---|---|
| `MUST set emptyOutDir/outDir/build.format` ×3, restated again in the fence and the checklist | one section naming what the four settings buy, pointing at the scaffold file that encodes them — stated once, in the file that is copied |
| `MUST pre-resolve every target … the templates never resolve` | the "What is different about Astro" paragraph: templates run at build time, after the agent is gone, so resolution happens up front |
| `NEVER regenerate astro.config/tailwind.config/.astro on update` | "the scaffold is the user's" — a reason, in the update branch |
| `NEVER create a dist/ subdirectory` | kept as a failure with its message, because it is a real guardrail with a check behind it |
| `NEVER use a separate auto_slugged[] array` | stated as the positive shape: `provisional: true` sits on the element object |
| `NEVER invent comparable products` (brief) | "A fabricated competitor is indistinguishable from a real one by the time `concept-comparable` and `product-spec-features` read this file" |
| `NEVER block on missing input` (brief) | "carry on with gaps — the user reviews in step 3, a cheaper place to fill a gap than an interview" |
| `MUST wait for explicit human approval` (brief) | the approval loop plus its consequence: an unapproved brief propagates into work that costs far more to redo |

**Map premise 4 is amended: `-mp` skills carry no `MUST`/`NEVER` block.** Hard guardrails
survive as named failures with a check behind them (`dist/` must not exist, the validator
must exit 0), which is `writing-for-agents`' allowance — a prohibition paired with the
positive target — rather than a block of nine.

## Two findings for other tickets

1. **The `items[]` id-derivation rule belongs in the shared contract, not in each renderer.**
   The astro skill spends ~30 lines deriving it and says outright that it "follows directly
   from" `walkthrough_renderer.md`'s `data-spec-*` table. Every renderer needs the same rule
   and must agree on it. Putting it in the contract removes those lines five times over.
   → ticket 06.
2. **`prerequisites.inputs_optional` is UI data living in prose.** See above. → tickets 09, 11.

## Verdict

The shape holds, at 110 lines for the collection's worst skill. The template is in
`TEMPLATE.md`. The ceiling is mp's measured **140 lines**, and the astro port suggests it is
reachable even where the map expected it not to be — which weakens, but does not settle, the
argument that the five renderers must collapse to survive. That remains ticket 06's call.
