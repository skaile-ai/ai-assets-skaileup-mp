# Frontmatter Schema — `_concept/` artifact files

> **Scope:** the YAML frontmatter of files a skill writes *into* `_concept/`. Every path
> below is `concept_structure.md`'s. A skill's own manifest frontmatter is a different
> object and lives in `docs/skill-template.md`.

All markdown files in `_concept/` use YAML frontmatter. Skills use these field names exactly.

## Universal Fields

Every markdown file in `_concept/`:

```yaml
---
last_updated: YYYY-MM-DD    # ISO date, updated on every write
---
```

---

## brief.md

```yaml
---
elevator_pitch: "One sentence"
audience: "Who it's for"
problem: "What it solves"
hero_flow: "The most important user action"
comparable_products: [app1, app2]
last_updated: YYYY-MM-DD
---
```

## goals.md

```yaml
---
success_criteria: []            # what "working" means, one line each
kpis: []                        # the measurable ones
constraints: []                 # budget, deadline, platform, compliance
non_goals: []                   # explicitly out, so nobody re-proposes them
last_updated: YYYY-MM-DD
---
```

## comparable.md

```yaml
---
last_updated: YYYY-MM-DD
---
```

---

## 02_grounding/research/competitors.md

```yaml
---
products_analyzed: 5
last_updated: YYYY-MM-DD
---
```

## 02_grounding/research/audiences.md

```yaml
---
personas_defined: 3
last_updated: YYYY-MM-DD
---
```

## 02_grounding/research/domain.md

```yaml
---
last_updated: YYYY-MM-DD
---
```

## 02_grounding/research/design-inspiration.md

```yaml
---
references_collected: 8
last_updated: YYYY-MM-DD
---
```

---

## 03_brand/identity.md

```yaml
---
mood: "calm | bold | professional | playful | ..."
mode: light | dark | both
last_updated: YYYY-MM-DD
---
```

---

## 04_journeys/stories.yaml

A data file, not a markdown artifact — no frontmatter. Structure:

```yaml
version: "1.0"
last_updated: YYYY-MM-DD
personas:
  - id: persona_id
    name: Persona Name
    role: role_name
    goals: ["..."]
journeys:
  - id: journey_id
    persona: persona_id
    title: Journey Title
    stage: hero | vital | hygiene | backlog
    steps:
      - action: What the user does
        system_response: What the system does
        acceptance: EARS-format acceptance criterion
    candidate_features: [feature_slug]
    candidate_entities: [EntityName]
```

---

## 05_features/\<featureset\>/\<feature\>.md

```yaml
---
priority: must-have | nice-to-have
roles: [all_users]              # or [admin, member, guest]
permissions:                    # role → allowed actions
  admin: [view, create, edit, delete]
  member: [view, create]
  guest: [view]
story_refs: []                  # journey IDs from stories.yaml that motivated this feature
agent_notes: |
  Free-form notes from the agent about this feature.
  Used for context across sessions.
screens: []                     # populated by spec-feature when it writes the screens
data_entities: []               # populated by architecture-datamodel
slice_ref: ""                   # populated by build-implement: 11_build/slices/<slice_id>/
commits: []                     # populated by build-implement: git SHAs that shipped this feature
source_files: []                # populated by build-implement: code files from the slice recap
last_updated: YYYY-MM-DD
---
```

### screens[] format (populated by the screen write)

```yaml
screens:
  - path: 07_screens/login/login.md
```

### data_entities[] format (populated by architecture-datamodel)

```yaml
data_entities: [User, Session]
```

### back-link format (populated by build-implement on freeze)

Forward-built features get code back-links when their slice is frozen — the same shape
`concept-reverse` writes for imported repos:

```yaml
slice_ref: 11_build/slices/login/
commits: [abc1234, deadbeef1234567]      # 7-40 hex chars each
source_files:
  - src/routes/login.ts
  - src/components/LoginForm.tsx
```

`ops-review`'s trace treats an empty `commits`/`source_files` on a frozen slice's feature as
a red trace row.

---

## 06_behaviors/\<featureset\>.md

```yaml
---
last_updated: YYYY-MM-DD
---
```

The states, transitions and constants are markdown tables in the body, not frontmatter —
`experience-behaviors` owns their shape.

---

## 07_screens/shell.md

```yaml
---
elements: []                    # carries the `kind: nav` block — see contracts/elements_block.md
last_updated: YYYY-MM-DD
---
```

## 07_screens/\<feature_slug\>/\<screen\>.md

```yaml
---
implements:
  - 05_features/auth/login.md
  - 05_features/auth/registration.md
data_entities: [User]
layout: 07_screens/shell.md
elements: []                    # OPTIONAL — see contracts/elements_block.md
last_updated: YYYY-MM-DD
---
```

For the optional `elements:` block (used by walkthrough renderers and the mockup-feedback
loop), see `contracts/elements_block.md`.

---

## 10_blueprint/techstack.md

```yaml
---
platform: web | mobile | desktop | api
framework: ""                   # e.g. PostXL, Laravel, Rails, custom
frontend: ""                    # e.g. Vite + React 19
ui_library: ""                  # e.g. @postxl/ui-components, shadcn/ui
backend: ""                     # e.g. NestJS + Fastify + tRPC
orm: ""                         # e.g. Prisma, TypeORM, Drizzle, Ecto
database: ""                    # e.g. PostgreSQL, SQLite
auth: ""                        # e.g. Keycloak, Auth.js, custom
package_manager: ""             # e.g. pnpm, bun, npm
tech_stack_skill: ""            # the winning template's directory name, or `custom`
last_updated: YYYY-MM-DD
---
```

`tech_stack_skill` is the field the rest of the collection resolves: `build-scaffold` and
`build-database` read `templates/<that string>/TEMPLATE.md` for their recipe sections and
atoms. `custom` means no template — the commands come from this file's own prose. Written by
`architecture-techstack`; the legal values are the directory names under `templates/`.

---

## 10_blueprint/architecture.md

```yaml
---
apps: []                        # deployable units, e.g. [api, web, worker]
custom_services: []             # runtime services outside the main app
custom_modules: []              # code-level module boundaries within the app
protocols: []                   # e.g. [http, trpc, websocket]
external_integrations: []       # third-party APIs, services
last_updated: YYYY-MM-DD
---
```

---

## 10_blueprint/datamodel/feature-map.json

JSON file — no frontmatter. Maps each model to its source feature files:

```json
{
  "last_updated": "YYYY-MM-DD",
  "models": {
    "User": {
      "source_features": [
        "05_features/auth/login.md",
        "05_features/auth/registration.md"
      ]
    }
  }
}
```
