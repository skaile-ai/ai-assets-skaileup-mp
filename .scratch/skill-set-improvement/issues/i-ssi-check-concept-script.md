# i-ssi-check-concept-script: ops-review runs a mechanical concept check script first

**What to build:** `skills/ops-review/scripts/check_concept.py` (stdlib + yaml) checks a project's `_concept/` mechanically: frontmatter fields, `screens:`/`implements:` resolution, `data_entities[]` against `model.json`, criterion ids against `stories.yaml`, the ledger rule; it reports old paths (`comparable.md`, `10_blueprint/glossary.md`) as unowned. `ops-review` calls it at its first step and keeps judgement and the trace; its body drops under 100 lines.

**Plan:** `.scratch/plans/SSI_SKILL_SET_IMPROVEMENT_PLAN.md` — Phases › Phase 4 step 16 (F41); Verification (`check_concept.py`); Risks (existing `_concept/` trees).

**Blocked by:** i-ssi-build-quality-joins

**Status:** ready-for-agent

- [ ] Script exists and runs against a throwaway `_concept/` built from the skills' `Done when` lists.
- [ ] Fixture: a tmp `_concept/` with one broken link → exactly one error.
- [ ] `ops-review` calls it at step 1; body < 100 lines.
- [ ] `python scripts/check.py` exits 0 (collection + fixtures, not `--no-tests`); every skill body ≤ 140 lines; pushed run green per the `CLAUDE.md` watch rule.
