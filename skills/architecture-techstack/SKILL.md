---
name: architecture-techstack
description: "Use when a project has a brief but no technology decided — scans the stack templates on disk, asks what the project actually constrains, and records the winner as the one id every later skill resolves. Triggers on 'tech stack', 'what should we build this with', 'pick a framework', 'which template'."
version: "0.1.0"
metadata:
  artifacts:
    requires:
      - { id: brief }
      - { id: scope }
      - { id: features }
  prerequisites:
    files:
      - { path: "_concept/brief.md", gate: hard }
      - { path: "_concept/01_meta/scope.yaml", gate: soft }
      - { path: "_concept/05_features", gate: soft, min_entries: 1 }
    inputs_optional:
      - { id: framework_experience, label: "Framework experience", type: text, hint: "React, Vue, Svelte — or starting fresh?" }
      - { id: hosting, label: "Hosting", type: select, options: [self-hosted, managed] }
---

# architecture-techstack

Chooses the project's technology and resolves it to exactly one template, in one pass.
`tech_stack_skill` in `10_blueprint/techstack.md` is the single field every later skill
resolves — `templates/<that string>/TEMPLATE.md` is where the scaffold commands, theming,
auth and ORM recipes come from — so the abstract choice and the concrete template are one
decision under one approval, not two rounds over the same field.

Paths are `contracts/concept_structure.md`'s and the frontmatter is
`contracts/artifact_frontmatter.md § 10_blueprint/techstack.md`. The template set, its atoms
and its section headings are `templates/README.md`'s; read it before scoring.

## Steps

1. **Read the ground before asking anything.** `brief.md` for what is being built and for
   whom; `01_meta/scope.yaml` for `flow` and `project_type`, falling back to
   `02_grounding/onboarding/onboarding.yaml` when scope has not been written yet; every
   feature under `05_features/` that exists, for complexity signals. `project_type` decides
   which axes carry weight — `cli-tool`, `api-service`, `library` and `data-pipeline` grow no
   screens, so the UI-library axis is dead for them and the choice is a runtime and a data
   layer. A `techstack.md` that is already there is a handed-off or reverse-engineered
   concept: read it back to the user and confirm it instead of re-running the selection, since
   regenerating a stack the project was already built against invalidates everything
   downstream of it without saying so.
2. **Discover the candidates at runtime.** Scan `templates/*/TEMPLATE.md` and read only each
   one's `## Identity` table and `## When to Use`. The candidate set is whatever is on disk
   and the id is the directory name character for character — a list of ids written into this
   file is a list that goes wrong the day a template lands.
3. **Ask in plain language, one question per message**, per
   `contracts/agent_patterns.md § Questions Are Standalone Messages`: existing framework
   experience, web / mobile / desktop / API, how data-heavy the app is, whether it needs a CMS
   or admin panel, self-hosted or managed, and any budget constraint. Skip whatever the
   onboarding answers already settled and adjust each question to the last answer.
   `appbuilder-mvp` settles this in a round or two — one capability and a single user rarely
   argue with the default — while the other three flows work the whole list.
4. **Score every candidate on four weighted axes**: frontend framework ×3, UI library ×2,
   backend ×1, database ×1. Frontend dominates deliberately, because a Nuxt project never
   lands on a Next template whatever the other three score.
5. **Break a tie on the flow** from `01_meta/scope.yaml`. `appbuilder-mvp` takes the lighter
   `*-minimal` template; `appbuilder-standard`, `skaileup-concept-only` and
   `skaileup-concept-reverse` take the fuller UI-library one. Ties are the normal case rather
   than the exception — several templates share a frontend, and the tie-break is the only
   thing separating them.
6. **A top frontend score of zero is an answer, not a rounding problem.** Report the gap, then
   offer the closest framework match or `tech_stack_skill: custom`, which means no template
   and `build-scaffold` working from `techstack.md` alone with each command confirmed. Mapping
   Svelte onto a Next template costs the entire build; a stack with no template is a gap in
   `templates/`, recorded as one.
7. **Approve the stack and its template together, once.** Show it in the user's language —
   what the app will be built on, which outside services it will talk to and what for — with
   the technical line under it: frontend, UI library, backend, database, auth, the winning
   template id and its one-line identity, and the runner-up with the gap that lost it. One id
   is on the table, not two: a second checkpoint over the same field asks the same person the
   same question twice and lets the two answers disagree.
8. **Check the id resolves, then write.** `test -d templates/<id>` before anything is written
   — a `tech_stack_skill` naming a directory that is not there fails at `build-scaffold`,
   several steps and one approval later, with nothing to fall back on. Then write
   `10_blueprint/techstack.md`: the frontmatter fields from the contract plus
   `tech_stack_skill`, a short section per axis saying why that choice fits *this* project,
   `## Additional Integrations` covering payments, mail and SMS, file storage, analytics and
   error tracking, and anything domain-specific the features named — "None identified" when
   there are none — and `## Trade-offs Considered`, which is what a reader six months later
   opens this file for. Names and reasons only: a Prisma schema or a line of SQL here is
   `architecture-datamodel`'s output written in the wrong file, and stale as soon as it exists.

**Done when** `10_blueprint/techstack.md` exists, its `tech_stack_skill` names either a real
`templates/` directory or `custom`, and the user approved that one id.
