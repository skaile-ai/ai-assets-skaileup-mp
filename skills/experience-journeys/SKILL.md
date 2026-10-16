---
name: experience-journeys
description: "Use when the brief is approved and nothing has mapped what users actually do yet. Defines the personas and the staged story map that features are derived from. Triggers on 'map the journeys', 'user stories', 'what do users do', 'story map'."
version: "0.1.0"
metadata:
  requires:
    - contract:@skaile-ai/shared-contracts
  artifacts:
    requires:
      - { id: brief }
      - { id: goals }
      - { id: research-audiences }
      - { id: glossary }
    produces:
      - { id: journeys, path: "_concept/04_journeys/stories.yaml" }
  prerequisites:
    files:
      - { path: "_concept/brief.md", gate: hard }
      - { path: "_concept/goals.md", gate: soft }
      - { path: "_concept/02_grounding/research/audiences.md", gate: soft }
      - { path: "_concept/glossary.md", gate: soft }
---

# experience-journeys

Writes `04_journeys/stories.yaml`: who the users are, and the staged map of what they are
trying to do. `spec-featuresets` derives the feature roster from this file rather than
inventing one, so a journey missing here is a feature nobody thinks to build. It maps
journeys and stops — no feature specs, no screens.

Paths are `contracts/concept_structure.md`'s; the EARS grammar is
`contracts/acceptance_criteria.md § EARS template` and the criterion ids are its
`§ Criterion ids`; the `candidate_*` handoff into features is `contracts/feedback_loop.md`'s.

## Steps

1. **Read the brief, and the audience research when it exists.** `brief.md` gives the
   audience and the `hero_flow`; `goals.md` gives what success means and therefore which
   journeys matter; `02_grounding/research/audiences.md` gives personas grounded in real job
   titles instead of inferred ones. Without research, derive the personas from the brief and
   say so — an invented persona reads exactly like a researched one to every skill after this.
2. **Define two to five personas**, each with a slug id, a human-readable label and what they
   are trying to achieve. Put the list to the user before going further: personas are the
   axis everything below is organised on, and adding one later re-cuts every journey.
3. **Map exactly one hero journey.** It comes from the brief's `hero_flow`, and it is the
   journey that, if it fails, leaves the product with no reason to exist. Three to eight
   sequential stories, each with a snake_case slug `id` (unique in the file — criterion ids
   are built from it), its persona, its outcome, and at least two acceptance
   criteria. Stop and get this one approved before mapping anything else — a hero journey the
   user disagrees with makes every other journey the wrong shape. Exactly one journey carries
   `stage: hero`; a second one means the product's core has not been decided.
4. **Map the rest, staged by what they are for, and write the `stages:` section.** The
   stage definitions live in `stories.yaml § stages` — one entry per stage id with a
   one-line definition — and nowhere else; every other skill cites them. `vital` — the other
   journeys that make the product usable day to day. `hygiene` — the operational flows
   nobody buys the product for and it cannot run without: onboarding, settings, roles,
   import and export. `backlog` — journeys deliberately out of this scope, sourced from the
   goals' non-goals and the gaps research found. The stage is what sets each story's
   priority, and what `spec-featuresets` and `experience-shell` read.
5. **Write acceptance criteria in EARS for every story** — at least two on a hero story, one
   everywhere else — using the pattern that fits: ubiquitous, event-driven, state-driven,
   optional-feature or complex. Give each criterion its id at write time, `AC-<story-id>-<nn>`
   per `contracts/acceptance_criteria.md § Criterion ids`, numbered per story from `01`. The
   feature specs, slice plans, ledger and e2e verdicts all cite these ids, so an id is never
   renumbered or reused after this step, and a vague criterion ("the system should work")
   is fixed here, once, rather than discovered by whoever has to test it.
6. **Give every story its downstream hints** — `candidate_features`, `candidate_entities`,
   `candidate_screens` — as plain strings. They are hints, not specs: `spec-featuresets` and
   `spec-feature` may add, merge or split beyond them, and `story_refs` is what traces the
   result back here. The data model is built from this file, so it does not exist yet:
   `candidate_entities` are read from `glossary.md`, never coined, and a concept with no term
   is handed back, with the flow re-entering `concept-glossary`.
7. **Write `04_journeys/stories.yaml`** — the project name, problem and success metrics from
   the brief, the personas, the `stages:` section (`hero`, `vital`, `hygiene`, `backlog`,
   each with its definition from steps 3 and 4), then the journeys — each journey is one
   story, its `id` the story id — with their stage, criteria and hints.
   Show the map as a table by stage with counts, and iterate until the user approves.

**Done when** `stories.yaml` exists with exactly one hero journey, every story has an `id` and
at least one EARS criterion carrying its `AC-<story-id>-<nn>` id plus its candidate hints, and
the user has approved the map.
