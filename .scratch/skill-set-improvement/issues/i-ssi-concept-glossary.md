# i-ssi-concept-glossary: A glossary skill writes the ubiquitous language right after the brief

**What to build:** A new `concept-glossary` skill reads the brief, research and findings, grills the user on the words, and writes `_concept/glossary.md` (root, beside `brief.md`) in `domain_model.md`'s format; it is re-enterable when a later skill meets a concept with no term. `concept-brief`, `spec-feature` and `architecture-datamodel` stop writing glossary text and read it; `concept-brief` writes comparables as a `brief.md` section.

**Plan:** `.scratch/plans/SSI_SKILL_SET_IMPROVEMENT_PLAN.md` — Phases › Phase 2 step 6 (F08, F10, F30, F34); Decisions already taken (glossary); Decisions this plan takes 1, 4; Target shape › `_concept/`.

**Blocked by:** i-ssi-adr-produces-glossary, i-ssi-produces-list

**Status:** ready-for-agent

- [ ] `skills/concept-glossary/SKILL.md` < 140 lines, with `produces` for `glossary.md`, grilling per `contracts/agent_patterns.md`, re-entry described as a flow re-entry (not a skill call).
- [ ] `concept_structure.md` tree: `glossary.md` at root; `10_blueprint/glossary.md` and `comparable.md` gone; read-direction table updated.
- [ ] `contracts/domain_model.md` path and ownership sentence updated.
- [ ] `concept-brief` steps 4/6, `spec-feature` step 3, `architecture-datamodel` step 6 read the glossary and hand new terms back instead of writing them.
- [ ] `skills/README.md` index lists the new skill.
- [ ] `python scripts/check.py` exits 0 (collection + fixtures, not `--no-tests`); every skill body ≤ 140 lines; pushed run green per the `CLAUDE.md` watch rule.
