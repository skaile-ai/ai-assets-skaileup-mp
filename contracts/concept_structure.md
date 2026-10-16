# `_concept/` — the artifact tree

Every skill in this collection reads and writes one directory inside the target project:
`_concept/`. These are the canonical paths; a skill that invents a path writes something
no reader will find.

`_concept/` is **one root**. There is no sibling `_implementation/` — the build half lives
at `11_build/`. The name `_concept/` is fixed by the host, not chosen here: forge-concept
resolves it in four places (`server/utils/project.ts`, `artifact-contract.ts` ×2,
`api/concepts/[...name].post.ts`), so it is a contract, not a word. It does **not** carry
the vocabulary meaning of *concept* (the design half) — see `CONTEXT.md`.

## The tree

```
_concept/
├── brief.md                        elevator pitch, audience, problem, hero flow, ## Comparables
├── goals.md                        success criteria, KPIs, constraints, non-goals
├── glossary.md                     the project's ubiquitous language: terms, definitions, _Avoid_ lists
│
├── 01_meta/
│   └── scope.yaml                  flow + project_type; every skill reads its depth from here
│
├── 02_grounding/                   everything that came from outside — read by every skill
│   ├── onboarding/
│   │   ├── answers.json            the one answer record: field values, confidence, seed inventory, approval
│   │   └── questions.md            open questions routed to someone who is not in the room
│   ├── research/
│   │   ├── domain.md               terminology, regulations, trends
│   │   ├── competitors.md          per-product analysis
│   │   ├── audiences.md            personas with design implications
│   │   ├── design-inspiration.md   layout, colour, typography, component patterns
│   │   ├── patterns.md             UX and architectural patterns for this domain
│   │   ├── colors-fonts.md         palette and typography research
│   │   ├── behavioral-patterns.md  state machines and lifecycles seen in the field
│   │   └── step/<skill-name>/      research dispatched alongside one skill
│   ├── seeds/                      material the user dropped in; nothing generates it
│   ├── standards/
│   │   ├── index.yml               fast matching by applies_to + keywords
│   │   └── <domain>/               conventions discovered in an existing codebase
│   └── findings/                   graded evidence and raw material from outside the room
│       ├── index.md                catalogue: file, source, date, `step` (the skill that took it)
│       ├── routes.md               concept-reverse — every route, the file defining it, what a user does there
│       ├── screens.md              concept-reverse — page components, bindings, interactions, states
│       ├── datamodel.md            concept-reverse — entities, fields, relations, enums
│       ├── stack.md                concept-reverse — detected technology, per dimension
│       ├── brand.md                concept-reverse — detected colours, type, radius, mode
│       ├── brief-seeds.md          concept-reverse — pitch, audience, problem, goals, comparables from the docs
│       └── *.png · *.md            screenshots, page saves, excerpts (concept-research, design-brand)
│
├── 03_brand/
│   ├── identity.md                 colours, fonts, tone of voice and copy guidelines (design-brand owns all of it)
│   ├── tokens.json                 machine-readable design tokens
│   └── brandbook.html              self-contained visual reference
│
├── 04_journeys/
│   └── stories.yaml                personas, story map (hero/vital/hygiene/backlog), EARS criteria
│
├── 05_features/
│   ├── featuresets.md              the roster: every featureset and the features in it
│   └── <featureset>/<feature>.md   one file per feature; featureset is the only grouping level
│
├── 06_behaviors/
│   └── <featureset>.md             state machines and lifecycle rules, as markdown state tables
│
├── 07_screens/
│   ├── shell.md                    the app shell: nav, sidebar, header, breakpoints, shared patterns
│   └── <feature_slug>/<screen>.md  one spec per screen, carrying the `elements:` block
│
├── 08_dossiers/
│   └── <feature_slug>/index.md     the working record behind one feature; opened at the grill, frozen at the end
│
├── 09_mockup/
│   ├── walkthrough/                the clickable walkthrough — one output tree, renderer-agnostic
│   ├── storybook/                  the standalone Storybook project
│   └── feedback/                   sessions · triage · patches · applied · devlog.md
│
├── 10_blueprint/
│   ├── techstack.md                chosen technologies and why
│   ├── architecture.md             system architecture, modules, data flow, protocols
│   ├── decisions.md                design-time decision records, append-only
│   └── datamodel/                  model.dbml · model.json · seed.json
│
└── 11_build/
    ├── slices/<slice_id>/          one vertical slice's dossier, frozen on commit
    ├── trace.yaml                  feature → slices → commits → code (build-implement writes it as each slice commits)
    ├── acceptance-criteria/        <featureset>/<feature_slug>.ac.md — the criteria status ledger
    ├── reviews/                    <feature_slug>.yaml — one feature's code-review verdict
    └── decisions.md                build-time decision records, append-only
```

## `02_grounding/findings/` — graded evidence

`concept-reverse` writes `findings/` and nothing else: the six files above, each value
graded `extracted`, `inferred` or `needs_review`. The skills that own the artifacts —
`concept-brief` (`brief-seeds.md`), `design-brand` (`brand.md`), `architecture-techstack`
(`stack.md`) — seed their drafts from them and show the graded values as proposals; the
routes, screens and datamodel files are evidence the journeys, the feature loop, the shell
and `architecture-datamodel` read. Screenshots and page saves live here and only here: each
gets a row in `findings/index.md` whose `step` field names the skill that took it.

## Numbering

The **first level is numbered and nothing below it is.** The number is the only ordering
signal the tree has — forge-concept's sidebar sorts `localeCompare` on the raw name and
strips `^\d+_` before display, so the prefix orders the tree and never reaches the reader.

Below the first level, order belongs to the artifact, not the path: a featureset's priority
is the story stage its features carry in frontmatter, and a screen belongs to a feature.
A `<featureset>` or `<feature_slug>` directory therefore carries no prefix.

Numbers are contiguous. Adding a twelfth kind renumbers the ones after it — a
collection-level change that already touches every skill that writes there.

## Naming

- Artifact filenames are lowercase and **hyphenated** — `design-inspiration.md`, never
  `design_inspiration.md`. One artifact has exactly one path.
- **No two siblings may differ only by singular and plural.** `review.yaml` beside
  `reviews/` reads as one artifact and its collection, and a skill author writing the path
  from memory gets it wrong in the direction that silently reads nothing. Where both a
  whole-tree fact and a per-thing collection are wanted, the two carry unrelated names.
- `shell` is a reserved slug under `07_screens/`.
- Directories under `05_features/` and `07_screens/` are slugs: lowercase, hyphenated,
  no spaces, no numeric prefix.
- `02_grounding/research/step/` subfolders are named for the skill that dispatched the
  research, character for character — the skill's `name:`, which is its whole identity.

## Read direction

A skill reads from anywhere earlier in the tree and writes only into the folder it owns.
`02_grounding/` is readable by every skill at any point.

| writes to | may read |
|---|---|
| `brief.md` · `goals.md` | `02_grounding/` |
| `glossary.md` | `02_grounding/`, `brief.md` |
| `03_brand/` | `02_grounding/`, `brief.md`, `glossary.md` |
| `04_journeys/` | `02_grounding/`, `brief.md`, `goals.md`, `glossary.md` |
| `10_blueprint/datamodel/` | `02_grounding/`, `brief.md`, `glossary.md`, `04_journeys/`, and `10_blueprint/techstack.md` · `architecture.md` when they exist |
| `05_features/` | the above, and `10_blueprint/datamodel/` |
| `06_behaviors/` | the above + `05_features/` |
| `07_screens/` | the above, and `10_blueprint/` when it exists |
| `08_dossiers/` | everything the feature loop touched |
| `09_mockup/` | `03_brand/`, `04_journeys/`, `05_features/`, `07_screens/`, `10_blueprint/datamodel/` |
| `10_blueprint/` (the rest) | everything above it |
| `11_build/` | everything |

`06_behaviors/` and `10_blueprint/architecture.md` are optional; a reader checks for
existence before reading.

## Dependency flow

```
02_grounding/ ─────────────────► read by everything, at any point

brief · goals · glossary
        │
        ├──► 03_brand/
        │
        └──► 04_journeys/ ──► 10_blueprint/datamodel/ ──► 05_features/ ──┬──► 06_behaviors/ ──┐
                                                                         │                    │
                                                                         └──► 07_screens/ ◄───┘
                                                                                    │
                                           09_mockup/ ◄─────────────────────────────┤
                                                                                    ▼
                                                           10_blueprint/ (techstack · architecture)
                                                                                    │
                                                                                    ▼
                                                                               11_build/
```

The data model is built from the journeys and the glossary, before any feature exists, so
every later skill reads entity names from it and none coins one. Brand runs in parallel with
the journeys→model→features track. Screens read behaviors when they exist. Everything before
`11_build/` is design; nothing under it is.

## `05_features/` — the permissions section

Each feature file carries its permissions in frontmatter and restates them as a table for
the reader:

```markdown
---
permissions:
  admin: [create, read, update, delete]
  member: [read, update]
  guest: [read]
---

## Permissions

| Role   | Actions                      |
| ------ | ---------------------------- |
| admin  | create, read, update, delete |
| member | read, update                 |
| guest  | read                         |
```

Implementation scaffolding reads it for the authorization policy. The data model does not: it
is built before the features exist and takes its roles from the journeys.

## `10_blueprint/datamodel/` — schema format

`model.dbml` and `model.json` are the canonical, stack-neutral model, and they are written
before the stack is chosen. The stack recorded in `techstack.md` decides only the translation
`build-database` makes from them:

| stack signal | stack-specific file |
|---|---|
| generic / unknown | none — `model.dbml` + `model.json` are the schema |
| Prisma | `schema.prisma` |
| PostXL / NestJS | `postxl-schema.json` |

`seed.json` is produced regardless. It holds named seed
scenarios — `empty`, `single_user`, `populated`, `edge_cases` — each independently runnable.

`architecture-datamodel` owns `model.dbml`, `model.json` and `seed.json`. The stack-specific
file is `build-database`'s alone: a translation of `model.json` for one migration tool, written
at the location the chosen template's `## Migration / ORM` section gives, and the canonical
files are never edited to match it.

The join between a feature and the models it uses is the feature spec's own `data_entities[]`
frontmatter list, written by `spec-feature`, each name a model in `model.json`. The model
holds no list of features.

## Dossiers

`08_dossiers/<feature_slug>/index.md` is the concept-side working record for one feature:
the framing, the questions, the scope line. `11_build/slices/<slice_id>/` is its build-side
counterpart. Both are **frozen** when their loop ends — indexed, closed, and kept as
documentation rather than deleted.

A dossier is one file. The per-phase handoffs the old collection wrote existed to survive a
session boundary that no longer breaks (ADR 0005).
