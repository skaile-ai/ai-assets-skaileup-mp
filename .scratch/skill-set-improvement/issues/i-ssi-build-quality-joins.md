# i-ssi-build-quality-joins: Build and quality share one trace and one ledger rule

**What to build:** `build-implement` writes `11_build/trace.yaml` as the single feature→commit join, read by `ops-review`, `quality-release` and `quality-review`; spec review stays only in `quality-review`. The ledger rule: later evaluation overwrites the row and stamps evidence, `FAIL` beats `PASS`. `quality-e2e` stops on a missing ledger and writes per-journey verdicts into ledger rows that `quality-release` reads rather than re-walking. `build-plan` cites `domain_model.md`; `build-branch` states its two rules; `concept_structure.md` names `design-brand` as owner of tone and copy.

**Plan:** `.scratch/plans/SSI_SKILL_SET_IMPROVEMENT_PLAN.md` — Phases › Phase 3 step 14 (F36–F39, F43); Ownership table.

**Blocked by:** i-ssi-spec-truth

**Status:** resolved

- [x] `trace.yaml` in the tree and written by `build-implement`; three readers cite it.
- [x] Ledger overwrite rule in `contracts/acceptance_criteria.md`.
- [x] `quality-e2e` / `quality-release` ledger hand-off as described; scaffold/branch stay git-only (ADR 0010).
- [x] `build-plan`, `build-branch`, tone owner edits done.
- [x] `python scripts/check.py` exits 0 (collection + fixtures, not `--no-tests`); every skill body ≤ 140 lines; pushed run green per the `CLAUDE.md` watch rule.

**Resolution (2026-10-16):** build-implement writes `11_build/trace.yaml` (features.<slug>.slices[] id/commits/code) and the ledger rows after commit; the spec back-link (slice_ref/commits/source_files) is gone, trace is the one join. ops-review (soft trace gate, coverage computed at report time), quality-review (hard trace gate, sole spec review, re-checks and overwrites PASS rows), quality-release (reads trace + ledger rows, no journey re-walk) read it. `acceptance_criteria.md § Ledger updates`: build-plan creates rows, evaluations overwrite with `<pointer> · <evaluator> · <commit> · <date>`, FAIL beats PASS at the same commit; quality-e2e stops without a ledger and writes verdict rows. build-plan cites domain_model; build-branch names its two rules; design-brand owns tone and copy (identity.md). Also carries artifact_frontmatter's `stages:` key from i-ssi-screens-shell. check.py green.
