---
name: spec-featuresets
description: "Use when the journeys are approved and nothing has decided what the app's features are or how they group. Derives the feature roster from the stories and cuts it into featuresets, one entry per feature the loop will then specify. Triggers on 'what features do we need', 'group the features', 'plan the feature set'."
version: "0.1.0"
metadata:
  artifacts:
    requires:
      - { id: brief }
      - { id: goals }
      - { id: journeys }
      - { id: research-competitors }
  prerequisites:
    files:
      - { path: "_concept/brief.md", gate: hard }
      - { path: "_concept/04_journeys/stories.yaml", gate: hard }
      - { path: "_concept/02_grounding/research/competitors.md", gate: soft }
    inputs_optional:
      - { id: feature_scope, label: "How broad should the feature set be?", type: select, options: ["must-have only", "must-have + nice-to-have", "comprehensive"] }
---

# spec-featuresets

Writes `05_features/featuresets.md`: the featuresets this product has, and the features in
each one, named and prioritised. It draws the boundaries; it writes no feature spec —
`spec-feature` takes one entry from this roster at a time and turns it into the spec and its
screens. A **featureset** is the only grouping level there is: a feature belongs to exactly
one, and nothing sits between them.

Paths are `contracts/concept_structure.md`'s; `story_refs` back to the journeys is
`contracts/feedback_loop.md`'s.

## Steps

1. **Start from the stories, not from the domain.** Read `04_journeys/stories.yaml` and
   collect every `candidate_features` hint across every journey; read `brief.md` and
   `goals.md` for what is in scope at all. A feature that traces to no story and no line of
   the brief is one you thought of rather than one the product needs — either find the
   journey it serves, or leave it out and let the user add it back deliberately.
2. **Let the competitor findings sharpen the list**, where research ran: a gap users complain
   about in `02_grounding/research/competitors.md` is a candidate with evidence behind it,
   and a feature every competitor has that no journey mentions is a question worth asking
   rather than a feature worth adding.
3. **Cluster into featuresets by what a user is doing**, not by which entity is touched.
   Aim for a handful: a featureset so large it has no single purpose will be re-cut the first
   time somebody looks for something in it, and one holding a single feature is a folder
   pretending to be a grouping. Names are lowercase, hyphenated slugs and become the
   directory each feature spec is written into, so renaming one later rewrites every
   cross-reference to it.
4. **Prioritise from the story stage.** Hero, vital and hygiene stories give must-have
   features; backlog stories give nice-to-have. The scope answer calibrates what survives:
   must-have only cuts everything backlog-derived, and comprehensive keeps it all. Whatever
   is cut is written down as cut rather than dropped, so the next reader can tell a decision
   from an oversight.
5. **Settle the role vocabulary once**, here: the roles this product has, across every
   featureset. Each feature spec restates its own role × action table, and they only line up
   if the words were agreed in one place first — `admin` in one spec and `owner` in the next
   describing the same person is a permissions bug that reaches the code.
6. **Write `05_features/featuresets.md`.** Per featureset: its slug, one sentence on what a
   user does in it, and its features as a table — feature slug, the outcome in one line,
   priority, and the story ids it came from. Then the role vocabulary and the cut list. This
   file is a roster, not a spec: no requirements, no acceptance criteria, no screens.
7. **Put the whole roster to the user as a table** with counts per featureset and per
   priority, and iterate until they approve. This is the cheapest point at which a
   mis-grouped feature costs a line instead of a directory rename. Then hand off: the loop
   runs `spec-feature` once per must-have entry.

**Done when** `05_features/featuresets.md` lists every featureset with its features,
priorities and `story_refs`, every feature traces to a story or an explicit line of the
brief, and the user has approved the roster.
