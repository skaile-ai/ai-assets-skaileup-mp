# i-ssi-build-quality-joins: Build and quality share one trace and one ledger rule

**What to build:** `build-implement` writes `11_build/trace.yaml` as the single feature→commit join, read by `ops-review`, `quality-release` and `quality-review`; spec review stays only in `quality-review`. The ledger rule: later evaluation overwrites the row and stamps evidence, `FAIL` beats `PASS`. `quality-e2e` stops on a missing ledger and writes per-journey verdicts into ledger rows that `quality-release` reads rather than re-walking. `build-plan` cites `domain_model.md`; `build-branch` states its two rules; `concept_structure.md` names `design-brand` as owner of tone and copy.

**Plan:** `.scratch/plans/SSI_SKILL_SET_IMPROVEMENT_PLAN.md` — Phases › Phase 3 step 14 (F36–F39, F43); Ownership table.

**Blocked by:** i-ssi-spec-truth

**Status:** ready-for-agent

- [ ] `trace.yaml` in the tree and written by `build-implement`; three readers cite it.
- [ ] Ledger overwrite rule in `contracts/acceptance_criteria.md`.
- [ ] `quality-e2e` / `quality-release` ledger hand-off as described; scaffold/branch stay git-only (ADR 0010).
- [ ] `build-plan`, `build-branch`, tone owner edits done.
- [ ] `python scripts/check.py` exits 0 (collection + fixtures, not `--no-tests`); every skill body ≤ 140 lines; pushed run green per the `CLAUDE.md` watch rule.
