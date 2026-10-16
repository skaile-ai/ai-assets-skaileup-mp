# i-ssi-spec-truth: Acceptance criteria, permissions and scope each have one record

**What to build:** Every EARS criterion gets an id at `experience-journeys` (grammar in `contracts/acceptance_criteria.md`) and downstream skills cite ids, never retype text. `spec-feature` owns the role × action permissions table, which behaviors, featuresets and datamodel seeds cite. The spec's `## Scope` section is the scope record; the dossier links to it and is opened at `spec-feature` step 2 and appended after each step; `decisions.md` holds only three-test decisions.

**Plan:** `.scratch/plans/SSI_SKILL_SET_IMPROVEMENT_PLAN.md` — Phases › Phase 3 step 11 (F19, F20, F22, F23); Risks (140-line ceiling).

**Blocked by:** i-ssi-datamodel-first

**Status:** resolved

- [x] Criterion id grammar in the contract; `experience-journeys` step 5 assigns ids; `spec-feature`, `build-plan`, `quality-e2e`, `experience-behaviors` cite ids.
- [x] Permissions table owned by `spec-feature` and cited elsewhere (split into a reference file if the 140-line ceiling requires it).
- [x] Dossier opened early; `experience-behaviors` names the feature file it re-runs on a rule change.
- [x] `python scripts/check.py` exits 0 (collection + fixtures, not `--no-tests`); every skill body ≤ 140 lines; pushed run green per the `CLAUDE.md` watch rule.

**Resolution (2026-10-16):** `acceptance_criteria.md § Criterion ids` (`AC-<story-id>-<nn>`, stable, cite never retype); experience-journeys assigns ids; build-plan, quality-e2e, experience-behaviors, spec-feature cite ids. spec-feature owns `## Permissions` and `## Scope`, opens the dossier at step 2 (status open → frozen), decisions.md only three-test; spec-featuresets settles role names only; datamodel seeds grants only on re-run. artifact_frontmatter, slice_loop and ADR 0010 updated. spec-feature at 138 lines. AC-n mentions in build-implement/quality-review/ops-review move to i-ssi-build-quality-joins. check.py green.
