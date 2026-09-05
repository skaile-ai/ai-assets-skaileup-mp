---
name: architecture-datamodel
description: "Use when the features are specified and the project needs a schema — derives entities, relationships and enums from the feature specs, writes the stack-neutral model with its seed scenarios, and pins the vocabulary it just named. Triggers on 'data model', 'design the schema', 'what entities do we need', 'seed data'."
version: "0.1.0"
metadata:
  artifacts:
    requires:
      - { id: brief }
      - { id: features }
      - { id: techstack }
      - { id: journeys }
  prerequisites:
    files:
      - { path: "_concept/05_features", gate: hard, min_entries: 1 }
      - { path: "_concept/10_blueprint/techstack.md", gate: soft }
      - { path: "_concept/04_journeys/stories.yaml", gate: soft }
      - { path: "_concept/06_behaviors", gate: soft, min_entries: 1 }
---

# architecture-datamodel

Derives the project's data model from its feature specs and writes it four ways under
`10_blueprint/datamodel/`: `model.dbml` to read, `model.json` for the editor canvas,
`seed.json` for everything that needs realistic data, and `feature-map.json` tracing each
model back to the features that asked for it. It is the only step that holds the whole
vocabulary at once, so it also settles the glossary and links the entities back into the
feature specs.

The model is **stack-neutral**. Types are `contracts/semantic_types.md`'s and never SQL or
Prisma types; naming is `contracts/golden_principles.md`'s; the seed scenarios and the rules
they obey are `contracts/seed_data.md`'s; paths are `contracts/concept_structure.md`'s.
Translating any of it into a stack is `build-database`'s step, and doing it here would freeze
a schema into the concept tree before the stack's migration tool has seen it.

## Steps

1. **Read every feature, not a sample.** Features and entities are not one-to-one: several
   features share an entity, and infrastructure entities — sessions, audit logs, job records —
   serve no single feature at all. Read `brief.md` for the domain, `10_blueprint/glossary.md`
   for the words already pinned, and `10_blueprint/techstack.md` for translation hints only.
   Where they exist: `04_journeys/stories.yaml` — EARS criteria carry state machines, event
   criteria becoming transitions and state criteria becoming guards;
   `10_blueprint/architecture.md` — a custom module or an integration usually needs its own
   entities; `06_behaviors/<featureset>.md` — its state tables are authoritative for enum
   values, and an enum here that disagrees with one there will be caught by whichever half is
   read second.
2. **Ask what the features left ambiguous**, one question per message per
   `contracts/agent_patterns.md`: what each feature stores, how things connect ("a user has
   many tasks"), and who may see or change what. The last one is already half-answered — each
   feature's `permissions:` block is in its frontmatter, and the model's job is to carry the
   fields those rules need to evaluate.
3. **Write `model.dbml` and `model.json`.** Semantic types only, PascalCase singular model
   names, snake_case fields, `_id` on the owning side of every `m2o`, PascalCase enum values,
   `label_field` on every model, `key_field` where there is a readable slug. Do not put `id`,
   `created_at` or `updated_at` in a fields list — `standard_fields` declares them and the
   translator injects them — and do not declare `o2m`, which is generated from its `m2o`. An
   `m2m` gets an explicit junction model. A raw SQL type here survives all the way into a
   migration that will not apply.
4. **Write `seed.json` with all four scenarios** — `empty`, `single_user`, `populated`,
   `edge_cases` — plus `permissions` when the app has role-based features. The format and the
   data-quality rules are `contracts/seed_data.md`'s: IDs consistent across entities so every
   relation resolves inside its own scenario, `created_at` and `updated_at` on every record in
   `single_user` and `populated`, statuses covering the enum, names from several locales, and
   string lengths from one character to a hundred. This file is what the mockups render, what
   the screens quote and what the E2E tests run against, so a thin `populated` scenario shows
   up as a design nobody could review.
5. **Write `feature-map.json`**, mapping each model to the feature files it came from. Every
   entity traces to at least one feature; one that traces to none is either an entity the app
   does not need or a feature nobody wrote down, and both are worth raising before the schema
   is built.
6. **Pin the vocabulary in `10_blueprint/glossary.md`**, per `contracts/domain_model.md`.
   Every model name and every enum vocabulary the design just settled gets an entry — one or
   two sentences saying what the thing *is*, with the words it beat listed under `_Avoid_`.
   Entries are updated in place and existing ones are left alone; where the glossary already
   has a term for a concept, the model renames to match it rather than the other way round,
   because the glossary is what the feature specs, the screens and the code are already using.
   Field names and types stay out — the glossary carries no implementation detail, and
   `model.json` is where the shape lives.
7. **Register the entities back into the features**, per `contracts/feedback_loop.md`: each
   feature's `data_entities[]` lists the entities that serve it, leaving its `screens:` array
   untouched. Without the back-link a feature and the entities it depends on can only be
   connected by reading the whole model.
8. **Approve it in plain language** — what the app keeps track of and how those things relate,
   in the user's words, with the counts underneath. Then write. If the user asks for a
   stack-specific export at this point, that is `build-database`'s pass and it runs against
   these files rather than replacing them.

**Done when** all four files exist under `10_blueprint/datamodel/`, every entity appears in
`feature-map.json` against at least one real feature file, every model name has a glossary
entry, and every feature's `data_entities[]` resolves.
