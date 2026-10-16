# i-ssi-datamodel-first: The data model is built from journeys and glossary, before features

**What to build:** `architecture-datamodel` no longer depends on features or behaviors: it requires `stories.yaml` and `glossary.md` (hard) and techstack/architecture (soft), reads journeys + glossary, settles vocabulary before modelling, gets approval before any write, and no longer writes `feature-map.json` or registers back. Spec and experience skills never coin entity names: they read `model.json` when present, else the glossary; `spec-feature` writes `data_entities[]` into each spec.

**Plan:** `.scratch/plans/SSI_SKILL_SET_IMPROVEMENT_PLAN.md` — Phases › Phase 2 step 7 (F17, F18, F30, F31, F33, F34); Decisions already taken (data model); Decisions this plan takes 5.

**Blocked by:** i-ssi-soft-gates-profiles, i-ssi-concept-glossary

**Status:** resolved

- [x] `architecture-datamodel` prerequisites, step order and deletions as in the plan; contract `§` cites replace whole-file cites and restated rules.
- [x] `spec-feature`, `spec-featuresets`, `experience-journeys`, `experience-behaviors` read entity names, never coin them.
- [x] `spec-feature` step 5 writes `data_entities[]`.
- [x] `concept_structure.md`: `datamodel/` loses the feature cross-reference; one owner named for the stack-specific schema file.
- [x] `python scripts/check.py` exits 0 (collection + fixtures, not `--no-tests`); every skill body ≤ 140 lines; pushed run green per the `CLAUDE.md` watch rule.

**Resolution (2026-10-16):** architecture-datamodel: requires brief/journeys/glossary/techstack; glossary hard, stories.yaml soft (F35 rule; models from brief + glossary without journeys), techstack/architecture soft with stated use; vocabulary step before modelling, approval before writes, feature-map and register-back deleted, § cites. Spec/experience skills read entity names (model.json, else glossary) and hand back; spec-feature writes `data_entities[]` at step 5; ops-review checks the join. Contracts: tree + read order, feature-map gone, build-database owns the stack-specific schema (semantic_types.md too). Pre-existing snake_case vs PascalCase conflict between golden_principles and semantic_types left as is. check.py green.
