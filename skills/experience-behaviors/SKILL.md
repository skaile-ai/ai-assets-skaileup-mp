---
name: experience-behaviors
description: "Use when the featuresets are settled and an entity's lifecycle has enough states that prose stops being precise about it. Writes the state machines and rules the data model and the screens are built against. Triggers on 'state machine', 'behavioral rules', 'formalize the lifecycle', 'what states can this be in'."
version: "0.1.0"
metadata:
  requires:
    - contract:@skaile-ai/shared-contracts
  artifacts:
    requires:
      - { id: featuresets }
      - { id: research-behavioral-patterns }
  prerequisites:
    files:
      - { path: "_concept/05_features", gate: hard, min_entries: 1 }
      - { path: "_concept/02_grounding/research/behavioral-patterns.md", gate: soft }
---

# experience-behaviors

Writes `06_behaviors/<featureset>.md`: the states an entity can be in, what moves it between
them, and what has to hold on either side. It is the optional step — the pipeline runs
without it — and it earns its place when a lifecycle has enough states that a feature spec's
prose can no longer say precisely what is legal. `architecture-datamodel` and the feature
loop both read it where it exists.

Paths are `contracts/concept_structure.md`'s. Entity and enum naming are
`contracts/golden_principles.md`'s — the model is built from these tables, so a name that
disagrees with them gets renamed later and the reference breaks.

## Steps

1. **Read the featuresets and what has been specified so far.** `05_features/featuresets.md`
   for the grouping, every feature spec already written under it, and `brief.md` for the
   domain. `02_grounding/research/behavioral-patterns.md`, where it exists, carries how this
   domain already models these lifecycles — worth borrowing before inventing.
2. **Find the entities with a life.** For each featureset ask what things the features act
   on, which of them can be in more than one state, what moves them between states — a user
   action, a clock, another entity — and what must be true before and after each move. An
   entity with exactly one state is not a state machine and does not belong in this file.
3. **Write one markdown file per featureset**, named for it, at
   `06_behaviors/<featureset>.md`. Each entity gets its states listed and a transition table:

   | from | event | to | requires | ensures |
   |---|---|---|---|---|
   | active | failed login, count reaches the limit | locked | account is active | further attempts are refused |

   Plain markdown tables rather than a formal notation: every reader of this file is an
   agent or a person, and a grammar with no parser is a grammar that drifts from what it
   claims to describe without anything noticing.
4. **Give each entity its permissions and its constants.** Who can trigger which transition,
   as a role × transition table — the same roles the feature specs use. Then the values the
   rules quote: retry limits, lockout durations, session timeouts, page sizes. Naming them
   here is what stops the same number being re-guessed in a feature spec, a screen and the
   code.
5. **Record what formalising exposed.** Every ambiguity the feature specs left open goes in
   an `## Open questions` section, phrased as the decision it needs rather than as an
   observation. These are the highest-value output of this step: they are the rules that
   would otherwise be settled silently by whoever implements them first.
6. **Report the tables** — per featureset: entities, states, transitions, open questions —
   and put the open questions to the user. Their answers go back into the tables before this
   file is treated as settled.

**Done when** every featureset with a real lifecycle has a file, each entity in it has its
states and a transition table, and the open questions have been put to the user.
