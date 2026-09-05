---
name: concept-scope
description: "Use when a project has no _concept/01_meta/scope.yaml yet, or the recorded sizing is wrong. Records the flow the project is sized by and resolves its project type. Triggers on 'new project', 'scope this', 'how big is this', 're-scope'."
version: "0.1.0"
metadata:
  prerequisites:
    inputs_optional:
      - { id: project_description, label: "What are you building?", type: textarea, hint: "One or two sentences — the signals below can be inferred from it" }
      - { id: project_type, label: "Project type", type: select, options: [web-app, cli-tool, api-service, library, mobile-app, data-pipeline] }
---

# concept-scope

Writes `01_meta/scope.yaml`, the first file a project grows and the one eleven skills read
to decide how deep to go. Two values and the evidence behind them: the **flow** the project
is sized by, and its **project type**. It sizes and stops — every artifact after this is
some other skill's.

Paths are `contracts/concept_structure.md`'s. Ask each question as its own message per
`contracts/agent_patterns.md § Questions Are Standalone Messages`; a question buried under a
paragraph of status gets skimmed past, and a guessed answer here mis-sizes everything after.

## Steps

1. **Check for an existing scope.** `01_meta/scope.yaml` present means this is a re-scope,
   not a first run: load it and use its values as the defaults for every question below, so
   the user corrects a sizing rather than restating one. Its `chosen_at` is also the honest
   answer to "has anything changed since" — a re-scope days later against a grown tree is a
   different act from one five minutes after the first.
2. **Collect the signals.** How many distinct things a user can do; whether more than one
   role shares state; how data is persisted (none, one relational schema, or an external
   store the project does not own); which external services are named; and whether there is
   already a repository. Take what the description or the input dialog already answered and
   ask only for the rest. Record each answer as the user gave it — the reasoning in step 4
   quotes these numbers, and a rounded or normalised signal makes a re-scope argue with a
   sizing nobody can reconstruct.
3. **Resolve the project type** against `profiles/<project_type>.yaml` in this collection.
   The profile names the artifacts a project of that type is not expected to grow — a
   `cli-tool` grows no screens and no brand — so it is what stops a later skill from
   reporting a missing artifact that was never coming. When the description settles it,
   confirm rather than ask. `architecture-techstack` and `build-scaffold` both branch on
   this value, and unset it reads as `web-app`.
4. **Record the flow, and derive it only when nothing else has.** A flow *is* the sizing —
   one word, not two — so the project is sized by the flow it runs under. On a host that
   started the run from an onboarding profile the flow is already chosen and this step
   writes down which one. Where nothing has chosen, put the four to the user with your
   recommendation from the signals:

   | flow | fits |
   |---|---|
   | `appbuilder-mvp` | one capability, single user, no data layer to design |
   | `appbuilder-standard` | anything else that gets built |
   | `skaileup-concept-only` | the design is the deliverable; no code follows |
   | `skaileup-concept-reverse` | a repository already exists and the concept is extracted from it |

   The four names are the whole vocabulary — a fifth value is a flow that will not load.
5. **Show the decision, then write.** Present flow, project type, the signals literally, and
   two to six sentences of reasoning naming which signals decided it. On a re-scope show the
   diff against the loaded file and get a yes to overwriting: a silent re-size changes the
   depth of every skill still to run and leaves the artifacts already written at the old one.
   Then write `01_meta/scope.yaml`:

   ```yaml
   flow: appbuilder-standard
   project_type: web-app
   reasoning: |
     Nine user-facing capabilities with two roles sharing state, one relational
     schema, and no external store — standard rather than mvp on both counts.
   signals:
     features_estimate: 9
     multi_user: true
     persistence: structured
     integrations: [stripe]
     existing_repo: false
   chosen_at: "2026-09-05T14:22:00Z"
   ```

   `chosen_at` is ISO-8601 UTC. Nothing else belongs in this file: it records what was
   decided, and a file that also named the flow that wrote it would be naming its own caller.

**Done when** `01_meta/scope.yaml` exists, its `flow` is one of the four, its `project_type`
resolves to a `profiles/` file, and the user has seen the reasoning.
