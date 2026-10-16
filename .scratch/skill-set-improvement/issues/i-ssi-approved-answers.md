# i-ssi-approved-answers: Approvals and onboarding answers live on disk, not in chat

**What to build:** A later session can tell that the brief, brand, onboarding and reverse findings were approved, and when, from the artifacts themselves; onboarding answers have one record. `concept-onboard` merges the host's per-step user input into `answers.json` once, `onboarding.yaml` is derived from it or dropped, and `architecture-techstack` reads the answers' confidence grade.

**Plan:** `.scratch/plans/SSI_SKILL_SET_IMPROVEMENT_PLAN.md` — Phases › Phase 1 step 4 (F06, F13, F16).

**Blocked by:** None (can start immediately)

**Status:** resolved

- [x] `contracts/artifact_frontmatter.md` universal fields gain `approved: <date>`.
- [x] `concept-brief`, `design-brand`, `concept-onboard`, `concept-reverse` write `approved:` at their approval step.
- [x] `concept-onboard` step 1 merges `_grounding/<step>/user_input.json` into `answers.json`; `answers.json` is the only answer record.
- [x] `host_facts.py` row `host:grounding-user-input` listing the rule id; `python scripts/verify_host.py` reports it.
- [x] `architecture-techstack` step 1 reads the confidence grade.
- [x] `python scripts/check.py` exits 0 (collection + fixtures, not `--no-tests`); every skill body ≤ 140 lines; pushed run green per the `CLAUDE.md` watch rule.

**Resolution (2026-10-16):** `approved:` universal field; four approval steps stamp it; `onboarding.yaml` dropped, `answers.json` is the single record (shape in artifact_frontmatter.md); host fact `host:grounding-user-input` (skaile-forge `server/utils/content.ts` L175) owns new rule `onboard-names-host-input` with fixtures. check.py green (124 fixtures); verify_host: new fact holds, the 16 pre-existing expired facts unchanged.
