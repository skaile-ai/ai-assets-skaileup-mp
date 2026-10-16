# i-ssi-reverse-findings-only: Reverse engineering writes findings; the owning skills seed from them

**What to build:** `concept-reverse` writes only `02_grounding/findings/*` (routes, screens, datamodel, stack, brand, brief-seeds, each value graded); its `Done when` lists only findings. `concept-brief`, `design-brand` and `architecture-techstack` gain a seed-from-findings step. Screenshots live only in `02_grounding/findings/`, indexed with a `step` field.

**Plan:** `.scratch/plans/SSI_SKILL_SET_IMPROVEMENT_PLAN.md` — Phases › Phase 3 step 10 (F09, F11); Decisions already taken (`concept-reverse`).

**Blocked by:** i-ssi-approved-answers, i-ssi-flow-rewrite

**Status:** ready-for-agent

- [ ] `concept-reverse` steps 4–6 removed; step 7 writes the six graded findings files; `produces` updated.
- [ ] Seed step in the three owner skills, conditional on findings existing.
- [ ] `concept-research` and `design-brand` use `findings/index.md` with `step`.
- [ ] `python scripts/check.py` exits 0 (collection + fixtures, not `--no-tests`); every skill body ≤ 140 lines; pushed run green per the `CLAUDE.md` watch rule.
