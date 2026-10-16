---
name: experience-behaviors
description: "Use when the featuresets are settled and an entity's lifecycle has enough states that prose stops being precise about it. Writes the state machines and rules the feature specs and the screens are built against. Triggers on 'state machine', 'behavioral rules', 'formalize the lifecycle', 'what states can this be in'."
version: "0.1.0"
metadata:
  requires:
    - contract:@skaile-ai/shared-contracts
  artifacts:
    requires:
      - { id: featuresets }
      - { id: research-behavioral-patterns }
      - { id: glossary }
      - { id: datamodel }
      - { id: journeys }
    produces:
      - { id: behaviors, path: "_concept/06_behaviors/<featureset>.md" }
  prerequisites:
    files:
      - { path: "_concept/05_features", gate: hard, min_entries: 1 }
      - { path: "_concept/02_grounding/research/behavioral-patterns.md", gate: soft }
      - { path: "_concept/glossary.md", gate: soft }
      - { path: "_concept/10_blueprint/datamodel", gate: soft }
      - { path: "_concept/04_journeys/stories.yaml", gate: soft }
---

# experience-behaviors

Writes `06_behaviors/<featureset>.md`: the states an entity can be in, what moves it between
them, and what has to hold on either side. It is the optional step — the pipeline runs
without it — and it earns its place when a lifecycle has enough states that a feature spec's
prose can no longer say precisely what is legal. The feature loop reads it where it exists.

Paths are `contracts/concept_structure.md`'s. Entity and enum naming are
`contracts/golden_principles.md`'s — the data model is built before this file, so these
tables name entities as the model does. Criterion ids are
`contracts/acceptance_criteria.md § Criterion ids`.

## Steps

1. **Read the featuresets and what has been specified so far.** `05_features/featuresets.md`
   for the grouping, every feature spec already written under it, `brief.md` for the
   domain, and `04_journeys/stories.yaml` for the criteria (by id) the lifecycles have to
   satisfy. `02_grounding/research/behavioral-patterns.md`, where it exists, carries how
   this domain already models these lifecycles — worth borrowing before inventing.
2. **Find the entities with a life.** Entity names are read, never coined: from
   `10_blueprint/datamodel/model.json` when it exists, else from `glossary.md`; a concept with
   neither is handed back, and the flow re-enters `architecture-datamodel` for a missing model
   or `concept-glossary` for a missing term. For each featureset ask what things the features act
   on, which of them can be in more than one state, what moves them between states — a user
   action, a clock, another entity — and what must be true before and after each move. An
   entity with exactly one state is not a state machine and does not belong in this file.
3. **Write one markdown file per featureset**, named for it, at
   `06_behaviors/<featureset>.md`. Each entity gets its states listed and a transition table.
   A transition that realises a criterion names it by id in `criteria`, never by its text:

   | from | event | to | requires | ensures | criteria |
   |---|---|---|---|---|---|
   | active | failed login, count reaches the limit | locked | account is active | further attempts are refused | AC-login-03 |

   Plain markdown tables rather than a formal notation: every reader of this file is an
   agent or a person, and a grammar with no parser is a grammar that drifts from what it
   claims to describe without anything noticing.
4. **Name the constants, and point at the permissions.** Who can trigger which transition is
   the feature spec's role × action table — `05_features/<featureset>/<feature>.md
   § Permissions` — so cite it per entity and never restate it; where that spec is not
   written yet, the roles for a transition go under `## Open questions`, and `spec-feature`
   settles them in its table. Then the values the rules quote: retry limits, lockout
   durations, session timeouts, page sizes. Naming them
   here is what stops the same number being re-guessed in a feature spec, a screen and the
   code.
5. **Record what formalising exposed.** Every ambiguity the feature specs left open goes in
   an `## Open questions` section, phrased as the decision it needs rather than as an
   observation. These are the highest-value output of this step: they are the rules that
   would otherwise be settled silently by whoever implements them first.
6. **Report the tables** — per featureset: entities, states, transitions, open questions —
   and put the open questions to the user. Their answers go back into the tables before this
   file is treated as settled. When an answer, or any later edit, changes a rule a written
   feature spec rests on, name that spec's file (`05_features/<featureset>/<feature>.md`)
   in the report: the flow re-enters `spec-feature` for it, and the spec's criteria are
   updated there, by id.

**Done when** every featureset with a real lifecycle has a file, each entity in it has its
states and a transition table, and the open questions have been put to the user.
