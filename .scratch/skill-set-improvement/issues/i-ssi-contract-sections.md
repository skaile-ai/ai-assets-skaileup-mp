# i-ssi-contract-sections: Skills cite contract sections instead of restating them

**What to build:** `spec-feature`, `architecture-datamodel` and `experience-shell` cite `§` sections rather than whole files; the six "one question per message" restatements drop and the contract carries it; integrations live only in `architecture.md`, and `architecture-techstack` skips questions an input field already answered; release thresholds move to a table in `contracts/evaluator.md`, cited at `quality-release` step 7.

**Plan:** `.scratch/plans/SSI_SKILL_SET_IMPROVEMENT_PLAN.md` — Phases › Phase 4 step 15 (F07, F14, F32, F42).

**Blocked by:** i-ssi-spec-truth, i-ssi-screens-shell, i-ssi-build-quality-joins

**Status:** resolved

- [x] `§` cites in the three skills resolve to existing headings.
- [x] No skill body restates the one-question rule.
- [x] Integrations only in `architecture.md`; techstack question skipping described.
- [x] Thresholds table in `contracts/evaluator.md`, cited by `quality-release`.
- [x] `python scripts/check.py` exits 0 (collection + fixtures, not `--no-tests`); every skill body ≤ 140 lines; pushed run green per the `CLAUDE.md` watch rule.

**Resolution (2026-10-16):** § cites in spec-feature (136 lines), architecture-datamodel, experience-shell (elements_block § Schema, walkthrough_renderer § App-shell navigation, …); one-question rule cited from agent_patterns § Questions Are Standalone Messages in the six skills, restatements gone; integrations only in architecture.md (architecture-system § External Integrations), techstack step 3 skips locked answers; `evaluator.md § Release thresholds` table (metric/good/warn/block + verdicts; LCP > 4s alone and blocking findings now map to needs_iteration) cited by quality-release with no numbers. One whole-file cite remains in spec-feature step 5 (heading with backticks is not citable). check.py green.
