# i-ssi-reverse-findings-only: Reverse engineering writes findings; the owning skills seed from them

**What to build:** `concept-reverse` writes only `02_grounding/findings/*` (routes, screens, datamodel, stack, brand, brief-seeds, each value graded); its `Done when` lists only findings. `concept-brief`, `design-brand` and `architecture-techstack` gain a seed-from-findings step. Screenshots live only in `02_grounding/findings/`, indexed with a `step` field.

**Plan:** `.scratch/plans/SSI_SKILL_SET_IMPROVEMENT_PLAN.md` — Phases › Phase 3 step 10 (F09, F11); Decisions already taken (`concept-reverse`).

**Blocked by:** i-ssi-approved-answers, i-ssi-flow-rewrite

**Status:** resolved

- [x] `concept-reverse` steps 4–6 removed; step 7 writes the six graded findings files; `produces` updated.
- [x] Seed step in the three owner skills, conditional on findings existing.
- [x] `concept-research` and `design-brand` use `findings/index.md` with `step`.
- [x] `python scripts/check.py` exits 0 (collection + fixtures, not `--no-tests`); every skill body ≤ 140 lines; pushed run green per the `CLAUDE.md` watch rule.

**Resolution (2026-10-16):** concept-reverse writes only `02_grounding/findings/` (brief-seeds, stack, brand, routes, screens, datamodel; graded extracted/inferred/needs_review; approved: on findings). concept-brief, design-brand, architecture-techstack seed from findings as proposals. Screenshots in findings/ with `index.md` `step`; `03_brand/references/` left the tree. concept_structure.md also carries the dossier line from i-ssi-spec-truth (opened at the grill, frozen at the end). check.py green.
