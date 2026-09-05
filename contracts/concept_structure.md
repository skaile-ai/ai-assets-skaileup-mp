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
├── brief.md                        elevator pitch, audience, problem, hero flow
├── goals.md                        success criteria, KPIs, constraints, non-goals
├── comparable.md                   reference apps: borrow, avoid, positioning gap
│
├── 01_meta/
│   └── scope.yaml                  tier + profile; every skill reads its depth from here
│
├── 02_grounding/                   everything that came from outside — read by every skill
│   ├── onboarding/
│   │   ├── onboarding.yaml         project profile + collected answers
│   │   ├── answers.json            per-dialog field values, preserved for resume
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
│   └── findings/
│       ├── index.md                catalogue of raw findings with source and date
│       └── *.png · *.md            screenshots, page saves, excerpts
│
├── 03_brand/
│   ├── identity.md                 colours, fonts, tone — and copy guidelines when asked for
│   ├── tokens.json                 machine-readable design tokens
│   ├── brandbook.html              self-contained visual reference
│   └── references/                 screenshots from reference URLs
│
├── 04_journeys/
│   └── stories.yaml                personas, story map (hero/vital/hygiene/backlog), EARS criteria
│
├── 05_features/
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
│   └── <feature_slug>/index.md     the working record behind one feature; frozen when written
│
├── 09_mockup/
│   ├── walkthrough/                the clickable walkthrough — one output tree, renderer-agnostic
│   ├── storybook/                  the standalone Storybook project
│   └── feedback/                   sessions · triage · patches · applied · devlog.md
│
├── 10_blueprint/
│   ├── techstack.md                chosen technologies and why
│   ├── architecture.md             system architecture, modules, data flow, protocols
│   ├── glossary.md                 the project's ubiquitous language
│   ├── decisions.md                design-time decision records, append-only
│   └── datamodel/                  schema, seed data, feature cross-reference
│
└── 11_build/
    ├── slices/<slice_id>/          one vertical slice's dossier, frozen on commit
    └── decisions.md                build-time decision records, append-only
```

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
| `brief.md` · `goals.md` · `comparable.md` | `02_grounding/` |
| `03_brand/` | `02_grounding/`, `brief.md` |
| `04_journeys/` | `02_grounding/`, `brief.md`, `goals.md` |
| `05_features/` | the above |
| `06_behaviors/` | the above + `05_features/` |
| `07_screens/` | the above, and `10_blueprint/` when it exists |
| `08_dossiers/` | everything the feature loop touched |
| `09_mockup/` | `03_brand/`, `04_journeys/`, `05_features/`, `07_screens/` |
| `10_blueprint/` | everything above it |
| `11_build/` | everything |

`06_behaviors/` and `10_blueprint/architecture.md` are optional; a reader checks for
existence before reading.

## Dependency flow

```
02_grounding/ ─────────────────► read by everything, at any point

brief · goals · comparable
        │
        ├──► 03_brand/
        │
        └──► 04_journeys/ ──► 05_features/ ──┬──► 06_behaviors/ ──┐
                                             │                    │
                                             └──► 07_screens/ ◄───┘
                                                       │
                              09_mockup/ ◄─────────────┤
                                                       ▼
                                              10_blueprint/
                                          techstack → architecture → datamodel
                                                       │
                                                       ▼
                                                  11_build/
```

Brand runs in parallel with the journeys→features track. Screens read behaviors when they
exist. Everything before `11_build/` is design; nothing under it is.

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

`10_blueprint/datamodel/` reads it for auth rules; implementation scaffolding reads it for
the authorization policy.

## `10_blueprint/datamodel/` — schema format

The format follows the stack recorded in `techstack.md`:

| stack signal | file(s) |
|---|---|
| generic / unknown | `model.dbml` + `model.json` (canonical model + editor canvas) |
| Prisma | `schema.prisma` |
| PostXL / NestJS | `postxl-schema.json` |
| several needed | `model.dbml` first, then the stack-specific format |

`seed.json` and `feature-map.json` are produced regardless. `seed.json` holds named seed
scenarios — `empty`, `single_user`, `populated`, `edge_cases` — each independently runnable.
`feature-map.json` maps each model to the feature files it came from.

## Dossiers

`08_dossiers/<feature_slug>/index.md` is the concept-side working record for one feature:
the framing, the questions, the scope line. `11_build/slices/<slice_id>/` is its build-side
counterpart. Both are **frozen** when their loop ends — indexed, closed, and kept as
documentation rather than deleted.

A dossier is one file. The per-phase handoffs the old collection wrote existed to survive a
session boundary that no longer breaks (ADR 0005).
