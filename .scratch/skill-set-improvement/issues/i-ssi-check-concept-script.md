# i-ssi-check-concept-script: ops-review runs a mechanical concept check script first

**What to build:** `skills/ops-review/scripts/check_concept.py` (stdlib + yaml) checks a project's `_concept/` mechanically: frontmatter fields, `screens:`/`implements:` resolution, `data_entities[]` against `model.json`, criterion ids against `stories.yaml`, the ledger rule; it reports old paths (`comparable.md`, `10_blueprint/glossary.md`) as unowned. `ops-review` calls it at its first step and keeps judgement and the trace; its body drops under 100 lines.

**Plan:** `.scratch/plans/SSI_SKILL_SET_IMPROVEMENT_PLAN.md` — Phases › Phase 4 step 16 (F41); Verification (`check_concept.py`); Risks (existing `_concept/` trees).

**Blocked by:** i-ssi-build-quality-joins

**Status:** resolved

- [x] Script exists and runs against a throwaway `_concept/` built from the skills' `Done when` lists.
- [x] Fixture: a tmp `_concept/` with one broken link → exactly one error.
- [x] `ops-review` calls it at step 1; body < 100 lines.
- [x] `python scripts/check.py` exits 0 (collection + fixtures, not `--no-tests`); every skill body ≤ 140 lines; pushed run green per the `CLAUDE.md` watch rule.

**Resolution (2026-10-16):** `skills/ops-review/scripts/check_concept.py` (stdlib + PyYAML): layout vs tree (retired comparable.md, 10_blueprint/glossary.md, feature-map.json reported unowned), frontmatter fields, screens:/implements: both ways, data_entities vs model.json, criterion ids vs stories.yaml, ledger rows/evidence. ops-review runs it at step 1 (98 lines). Three tests in scripts/test_check.py (valid tree clean, one broken screens: link → one error, comparable.md → unowned). Smoke: an old-shape tree reports the three retired paths and missing brief fields, exit 1. check.py green (164 fixtures).
