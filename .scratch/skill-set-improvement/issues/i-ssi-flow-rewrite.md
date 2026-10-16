# i-ssi-flow-rewrite: All four flows run in hierarchy order

**What to build:** Every flow runs domain language → data model → features → screens → mockups → architecture → build → quality: glossary nodes inserted, datamodel before featuresets, techstack/system before mockups, research before brief, shell after the feature loop. `appbuilder-mvp` gains `experience-journeys`; `appbuilder-standard` gains `quality-standards` after scaffold; the reverse flow enters at `concept-scope`. `concept-research` is a pipeline step; `experience-shell` derives nav from existing screens.

**Plan:** `.scratch/plans/SSI_SKILL_SET_IMPROVEMENT_PLAN.md` — Target shape › flows; Phases › Phase 2 step 8 (F01, F02, F03, F12, F25, F40); Decisions this plan takes 3, 6.

**Blocked by:** i-ssi-soft-gates-profiles, i-ssi-concept-glossary, i-ssi-datamodel-first

**Status:** resolved

- [x] The four `flows/*/*.flow.yaml` match the target node orders in the plan, each node with `data.phase`.
- [x] `requires` lists and group memberships updated; `_check_requires` / `_check_reachability` clean.
- [x] `concept-research` intro no longer says "not a pipeline step"; `experience-shell` derives nav from screens.
- [x] `build-plan`/`build-implement` read the standards index when present.
- [x] `python scripts/check.py` exits 0 (collection + fixtures, not `--no-tests`); every skill body ≤ 140 lines; pushed run green per the `CLAUDE.md` watch rule.

**Resolution (2026-10-16):** Four flows at the target orders (standard 29 nodes, mvp 11 with journeys, concept-only 16, reverse 14 entering at scope); glossary nodes everywhere, standards after database in standard; requires exact; groups resized; flows/README lists the orders. concept-research is a pipeline step reading answers.json (brief soft); experience-shell derives nav from 07_screens specs (findings in reverse); build-plan/build-implement read the standards index when present; concept-scope names itself entry of every flow. quality-test kept in the review group as today. check.py green.
