# i-ssi-flow-rewrite: All four flows run in hierarchy order

**What to build:** Every flow runs domain language → data model → features → screens → mockups → architecture → build → quality: glossary nodes inserted, datamodel before featuresets, techstack/system before mockups, research before brief, shell after the feature loop. `appbuilder-mvp` gains `experience-journeys`; `appbuilder-standard` gains `quality-standards` after scaffold; the reverse flow enters at `concept-scope`. `concept-research` is a pipeline step; `experience-shell` derives nav from existing screens.

**Plan:** `.scratch/plans/SSI_SKILL_SET_IMPROVEMENT_PLAN.md` — Target shape › flows; Phases › Phase 2 step 8 (F01, F02, F03, F12, F25, F40); Decisions this plan takes 3, 6.

**Blocked by:** i-ssi-soft-gates-profiles, i-ssi-concept-glossary, i-ssi-datamodel-first

**Status:** ready-for-agent

- [ ] The four `flows/*/*.flow.yaml` match the target node orders in the plan, each node with `data.phase`.
- [ ] `requires` lists and group memberships updated; `_check_requires` / `_check_reachability` clean.
- [ ] `concept-research` intro no longer says "not a pipeline step"; `experience-shell` derives nav from screens.
- [ ] `build-plan`/`build-implement` read the standards index when present.
- [ ] `python scripts/check.py` exits 0 (collection + fixtures, not `--no-tests`); every skill body ≤ 140 lines; pushed run green per the `CLAUDE.md` watch rule.
