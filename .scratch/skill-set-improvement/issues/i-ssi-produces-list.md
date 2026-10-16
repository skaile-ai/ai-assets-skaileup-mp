# i-ssi-produces-list: Every skill declares what it produces and the gate checks it

**What to build:** Each of the 30 skills states, in frontmatter, which artifacts it writes; the gate fails when a skill that writes under `_concept/` declares nothing, when a produced path is not in the tree fence, or when a `requires[].id` names an artifact no skill produces. The skill template shows the block.

**Plan:** `.scratch/plans/SSI_SKILL_SET_IMPROVEMENT_PLAN.md` — Phases › Phase 1 step 2; Constraints (no `metadata` allowlist, fixtures).

**Blocked by:** i-ssi-adr-produces-glossary

**Status:** ready-for-agent

- [ ] `metadata.artifacts.produces` present on all 30 skills, sourced from the report's writer map (`writes.json`).
- [ ] `docs/skill-template.md` shows the `produces` block.
- [ ] Three gate rules: non-empty `produces` for every `_concept/` writer; each `path` in the tree fence; each `requires[].id` resolves to some `produces[].id`.
- [ ] One failing fixture per rule plus a passing fixture in `scripts/test_check.py`, asserting on message text.
- [ ] `python scripts/check.py` exits 0 (collection + fixtures, not `--no-tests`); every skill body ≤ 140 lines; pushed run green per the `CLAUDE.md` watch rule.
