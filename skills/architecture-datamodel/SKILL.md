---
name: architecture-datamodel
description: "Use when the glossary exists and the project needs a schema before any feature is specified — derives entities, relationships and enums from the journeys (or the brief where there are none), settles every name against the glossary, and writes the stack-neutral model with its seed scenarios. Triggers on 'data model', 'design the schema', 'what entities do we need', 'seed data'."
version: "0.2.0"
metadata:
  requires:
    - contract:@skaile-ai/shared-contracts
  artifacts:
    requires:
      - { id: brief }
      - { id: journeys }
      - { id: glossary }
      - { id: techstack }
    produces:
      - { id: datamodel, path: "_concept/10_blueprint/datamodel/" }
  prerequisites:
    files:
      - { path: "_concept/04_journeys/stories.yaml", gate: soft }
      - { path: "_concept/glossary.md", gate: hard }
      - { path: "_concept/10_blueprint/techstack.md", gate: soft }
      - { path: "_concept/10_blueprint/architecture.md", gate: soft }
---

# architecture-datamodel

Derives the project's data model from its journeys and its glossary and writes it three ways
under `10_blueprint/datamodel/`: `model.dbml` to read, `model.json` for the editor canvas, and
`seed.json` for everything that needs realistic data. It runs before any feature exists, so
the model is the vocabulary the feature specs, behaviors and screens are written against:
downstream skills read entity names from `model.json` and never coin their own, and each
feature spec lists the models it uses in its own `data_entities[]`.

The model is **stack-neutral**. Types come from `contracts/semantic_types.md § Scalar Types`
and are never SQL or Prisma types, and translating the model into a stack is `build-database`'s
step. Doing it here would freeze a schema into the concept tree before the stack's migration
tool has seen it. Paths are `contracts/concept_structure.md § The tree`.

## Steps

1. **Read what the model is built from.** `04_journeys/stories.yaml` is the main source:
   actors, stages, and EARS criteria — event criteria become transitions, state criteria become
   guards, and what a journey creates, changes or looks up is an entity or a field. Profiles
   that never grow journeys (`api-service`, `cli-tool`, `data-pipeline`, `library`) have no such
   file: the model then comes from the brief's hero flow and problem plus the glossary's terms,
   and the questions in step 3 carry what the journeys would have. `brief.md` gives the
   domain and `glossary.md` (always required) the words already pinned. Where `10_blueprint/techstack.md`
   exists it gives translation hints only (a stack that forces a join table, say); without it
   the model stays generic and nothing waits on it. Where `10_blueprint/architecture.md`
   exists, a custom module or an integration usually needs its own entities; without it, an
   entity that only an integration needs surfaces later and this step is re-run for it.
2. **Settle the vocabulary before modelling.** List every candidate entity and every enum
   vocabulary the journeys (or the brief) imply — each journey's `candidate_entities` is the starting list —
   and check each against `glossary.md` per
   `contracts/domain_model.md § Glossary format`. Where the glossary has a term, the model
   uses it; a word from a term's `_Avoid_` list is renamed to the term. A concept with no term
   is not appended here: name it and hand back, and the flow re-enters `concept-glossary`,
   which pins it before this step goes on. Entities with no journey behind them — sessions,
   audit logs, job records — are named in the same list and checked the same way.
3. **Ask what the journeys left ambiguous**, per
   `contracts/agent_patterns.md § Questions Are Standalone Messages`: what each
   journey stores, how things connect ("a user has many tasks"), and which roles may see or
   change what. The last answer, taken from the journeys' roles, is what the seed's
   `permissions` scenario and the fields that rules evaluate on come from. The grants
   themselves are the feature specs' `## Permissions` tables: this step runs before them, so
   it records no grants of its own, and on a re-run it reads those tables where they exist and
   seeds the roles and grants as written there.
4. **Approve it in plain language** — what the app keeps track of and how those things relate,
   in the user's words, with the counts underneath. Nothing is written before the user says
   yes, because a model that features, screens and seeds are all about to name is cheapest to
   change while it is still a paragraph.
5. **Write `model.dbml` and `model.json`.** Conventions are
   `contracts/semantic_types.md § Rules for Skills`; the mechanical checks that review applies
   are `contracts/golden_principles.md § Entity Rules`, `§ Field Rules`, `§ Enum Rules` and
   `§ Relation Rules`. An `m2m` gets an explicit junction model. A raw SQL type here survives
   all the way into a migration that will not apply.
6. **Write `seed.json` with all four scenarios** — `empty`, `single_user`, `populated`,
   `edge_cases` — plus `permissions` when the journeys name distinct roles. The scenarios are
   `contracts/seed_data.md § Standard Scenarios` and the data rules
   `contracts/seed_data.md § Data Quality Rules`, so every relation resolves inside its own
   scenario. This file is what the mockups render, what the screens quote and what the E2E
   tests run against, so a thin `populated` scenario shows up as a design nobody could review.
7. **Hand a stack export to `build-database`.** If the user asks for a stack-specific schema
   at this point, `build-database` writes it against these files rather than replacing them.

**Done when** `model.dbml`, `model.json` and `seed.json` exist under `10_blueprint/datamodel/`
with the model approved, every model name and enum vocabulary is a term in `glossary.md`, and
`seed.json` carries all four standard scenarios.
