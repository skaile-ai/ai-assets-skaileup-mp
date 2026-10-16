# i-ssi-soft-gates-profiles: Gates on artifacts a profile never grows become soft, with a stated fallback

**What to build:** Projects whose profile never grows screens or stories are not blocked by `build-plan`, `build-implement` or `spec-featuresets`: those gates are `soft`, and the reading step says what the skill does without the file (plan from the featureset roster; implement from the spec alone). The gate reports a `hard` gate on any path a profile marks `not_grown`.

**Plan:** `.scratch/plans/SSI_SKILL_SET_IMPROVEMENT_PLAN.md` — Phases › Phase 1 step 3 (F35).

**Blocked by:** i-ssi-produces-list

**Status:** resolved

- [x] `07_screens` / `stories.yaml` gates in the three skills are `soft` where any profile marks them `not_grown`.
- [x] Each affected step states its no-file behaviour.
- [x] Gate rule: `hard` gate on a not-grown path is an error; failing + passing fixture.
- [x] `python scripts/check.py` exits 0 (collection + fixtures, not `--no-tests`); every skill body ≤ 140 lines; pushed run green per the `CLAUDE.md` watch rule.

**Resolution (2026-10-16):** `07_screens`/`stories.yaml`/datamodel gates soft in build-plan, build-implement, spec-featuresets, quality-e2e, build-database, each step stating its no-file fallback. Rule `_check_not_grown_gates`: profile `not_grown` entries resolve as artifact id, skill name or domain prefix; a hard gate overlapping a not-grown path is an error (skills covered by the entry are exempt per profile); unknown entry is an error. Five fixtures. build-plan cites root `glossary.md`. check.py green.
