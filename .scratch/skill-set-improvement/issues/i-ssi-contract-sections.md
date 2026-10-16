# i-ssi-contract-sections: Skills cite contract sections instead of restating them

**What to build:** `spec-feature`, `architecture-datamodel` and `experience-shell` cite `§` sections rather than whole files; the six "one question per message" restatements drop and the contract carries it; integrations live only in `architecture.md`, and `architecture-techstack` skips questions an input field already answered; release thresholds move to a table in `contracts/evaluator.md`, cited at `quality-release` step 7.

**Plan:** `.scratch/plans/SSI_SKILL_SET_IMPROVEMENT_PLAN.md` — Phases › Phase 4 step 15 (F07, F14, F32, F42).

**Blocked by:** i-ssi-spec-truth, i-ssi-screens-shell, i-ssi-build-quality-joins

**Status:** ready-for-agent

- [ ] `§` cites in the three skills resolve to existing headings.
- [ ] No skill body restates the one-question rule.
- [ ] Integrations only in `architecture.md`; techstack question skipping described.
- [ ] Thresholds table in `contracts/evaluator.md`, cited by `quality-release`.
- [ ] `python scripts/check.py` exits 0 (collection + fixtures, not `--no-tests`); every skill body ≤ 140 lines; pushed run green per the `CLAUDE.md` watch rule.
