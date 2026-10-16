# i-ssi-datamodel-first: The data model is built from journeys and glossary, before features

**What to build:** `architecture-datamodel` no longer depends on features or behaviors: it requires `stories.yaml` and `glossary.md` (hard) and techstack/architecture (soft), reads journeys + glossary, settles vocabulary before modelling, gets approval before any write, and no longer writes `feature-map.json` or registers back. Spec and experience skills never coin entity names: they read `model.json` when present, else the glossary; `spec-feature` writes `data_entities[]` into each spec.

**Plan:** `.scratch/plans/SSI_SKILL_SET_IMPROVEMENT_PLAN.md` — Phases › Phase 2 step 7 (F17, F18, F30, F31, F33, F34); Decisions already taken (data model); Decisions this plan takes 5.

**Blocked by:** i-ssi-soft-gates-profiles, i-ssi-concept-glossary

**Status:** ready-for-agent

- [ ] `architecture-datamodel` prerequisites, step order and deletions as in the plan; contract `§` cites replace whole-file cites and restated rules.
- [ ] `spec-feature`, `spec-featuresets`, `experience-journeys`, `experience-behaviors` read entity names, never coin them.
- [ ] `spec-feature` step 5 writes `data_entities[]`.
- [ ] `concept_structure.md`: `datamodel/` loses the feature cross-reference; one owner named for the stack-specific schema file.
- [ ] `python scripts/check.py` exits 0 (collection + fixtures, not `--no-tests`); every skill body ≤ 140 lines; pushed run green per the `CLAUDE.md` watch rule.
