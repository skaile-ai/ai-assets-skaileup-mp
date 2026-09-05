---
name: build-database
description: "Use when the data model is settled and the app needs a real database — translates the model into the stack's schema, migrates it, and generates one runnable seed script per scenario. Triggers on 'migrate', 'generate the schema', 'seed the database', 'set up the data layer'."
version: "0.1.0"
metadata:
  requires:
    - contract:@skaile-ai/shared-contracts
  artifacts:
    requires:
      - { id: datamodel }
      - { id: techstack }
  prerequisites:
    files:
      - { path: "_concept/10_blueprint/datamodel", gate: hard, min_entries: 1 }
      - { path: "_concept/10_blueprint/techstack.md", gate: hard }
---

# build-database

One pass over `10_blueprint/datamodel/`: the schema first, then the seed scripts that fill
it. Migration and seeding used to be two skills and one of them was written three times over;
they are one pass because they share the same read of the model and the same dependency
order, and splitting them is what let the three copies drift.

Almost all of this is stack-neutral. What is not lives in two sections of the chosen
template — `## Migration / ORM` for the schema file and the migrate commands, `## Seed` for
the seed layout and its run command — which this skill cites rather than restates. Types come
from `contracts/semantic_types.md`, the scenarios and their rules from
`contracts/seed_data.md`.

It is optional by flow. `appbuilder-mvp` designs no data model and grows its schema inside
`build-implement`, so nothing downstream should read a missing migration as a gap.

## Steps

1. **Read the model and cross-check its two halves.** `model.dbml` is authoritative for
   structure, `model.json` for relationship and enum metadata. Both came out of one skill, so
   they diverge only where something was hand-edited — name every disagreement to the user
   rather than silently preferring one, because the edit was somebody's intent and picking
   wrong here propagates into the schema and the seeds at once.
2. **Resolve the target from the template.** `10_blueprint/techstack.md` names
   `tech_stack_skill`; that template's `## Migration / ORM` gives the schema file, its
   location and the migrate commands, and its `seed_format` atom — `prisma`, `drizzle` or
   `sql` — selects the layout described in its `## Seed`. Where a `prog-expert-<orm>` skill
   happens to be installed, consult it for idiomatic patterns; nothing here waits on one,
   since those ship in a different collection that this one has no way to depend on.
3. **Translate every semantic type** through
   `contracts/semantic_types.md § Stack Translation Table`. A semantic type left in the output
   is a schema that will not migrate, and it fails at the tool rather than at the model.
4. **Apply the conventions the model deliberately leaves out.** `standard_fields` expands to
   an auto-generating UUID primary key plus `created_at`, and `updated_at` wherever the model
   declares it. Columns are snake_case. `on_delete` comes from the relationship in
   `model.json` and defaults to SET NULL where it is unset — the default that orphans a row
   rather than deleting one nobody asked to delete. Every `m2m` gets its junction table with
   the two foreign keys; `o2m` is generated from its `m2o` and never written by hand.
5. **Validate the schema six ways, then migrate.** Every entity in `model.json` has a table;
   every relationship is present as a foreign key or a junction table; every enum is defined;
   no semantic type survives anywhere in the output; primary keys auto-generate; on-delete
   behaviour matches `model.json`. Then run the migrate command — confirming first when the
   target is anything but a local development database, since a migration is not a proposal.
6. **Build the insert order before writing a single seed.** Walk the relationships into a
   dependency graph: entities with no foreign keys first, then each entity after everything it
   points at. The reverse of that list is the cleanup order. Deleting parents first is what
   leaves the dangling references that make a re-seed fail on the second run rather than the
   first.
7. **Generate the seeds at the paths `## Seed` names.** One file per scenario in `seed.json` —
   `empty`, `single_user`, `populated`, `edge_cases`, and any the model added — plus one entry
   point that takes the scenario name as its argument and defaults to `populated`. The
   entry point clears in reverse dependency order, then inserts. One file per scenario is what
   makes a scenario switchable mid-session; a single dump can only be run whole.
8. **Validate the seeds six ways.** Every id from `seed.json` is preserved — that is what the
   relations resolve through, so a regenerated id breaks every reference to it. Every foreign
   key value exists as a primary key. Every enum value matches `model.json`. Required fields
   are populated in every scenario. `empty` actively clears all data rather than inserting
   nothing. And `edge_cases` reaches the database intact — its special characters, its
   hundred-character strings and its null optionals are the whole point of the scenario, and a
   column that silently truncates them is the finding.
9. **Run each scenario end to end, then report**: the target, the counts of tables,
   relationships and enums, the scenarios and the files behind them, and the command that
   switches between them. A seed script that has never run is a script that does not work yet.

**Done when** the migration has applied, every scenario runs clean from the entry point, and
switching scenarios leaves behind no rows from the one before it.
