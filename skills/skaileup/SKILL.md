---
name: skaileup
description: "Use when no flow is running and the next skill is unclear — work arriving from outside the collection, or a `_concept/` tree opened cold. Triggers on 'which skill', 'what do I run next', 'where do I start', 'I have a bug report', 'a feature was requested'."
version: "0.1.0"
metadata:
  requires:
    - contract:@skaile-ai/shared-contracts
---

# skaileup

The collection's front door: it names the one skill to run next and stops there. It writes
no artifact and enters no flow — a router that also did the work would be a second place
where a skill's job is defined.

It answers only where nothing else already does. **Which flow** a project is sized by
belongs to `concept-scope` step 4, and to the host's profile picker before that. **What
runs after a skill completes** belongs to `contracts/agent_patterns.md § Next-Step
Suggestion`, which every skill already follows. What is left is the two cold cases below.

Paths are `contracts/concept_structure.md`'s.

## Steps

1. **Pick the door.** Two cases, and they are told apart by where the work came from:

   | | door |
   |---|---|
   | Work the collection did not create — a request, a bug report, a feature ask | step 2 |
   | A `_concept/` tree opened with nothing running and no skill just finished | step 3 |

   Anything else is not this skill's. A flow is dispatching, or a skill just completed and
   suggested its own successors; routing it again would give the user two answers from two
   sources, and no way to tell which is stale.

2. **Intake — triage first, then one entry point.** Run the globally installed `/triage`
   before choosing. It decides whether the item is worth doing at all, and that judgement is
   not this collection's to make: skaileup builds what a project has decided to build.

   What survives triage enters at exactly one of two skills:

   | the item | enter at |
   |---|---|
   | A capability the product does not have, or one whose behaviour changes | `spec-feature` |
   | A defect in code already built — the spec was right, the code is not | `build-plan` |

   The line between them is whether the specification was wrong. A defect whose fix changes
   what the product promises is a changed capability, not a bug, and goes to `spec-feature`;
   sending it to `build-plan` gets the code corrected against a spec that still describes the
   old promise.

3. **Cold start — read the sizing, then walk the flow.** In order, stopping at the first
   that answers:

   1. **No `_concept/01_meta/scope.yaml`** — the project is unsized, so no flow is chosen and
      no order exists to walk. `concept-scope` is next, and nothing else can be.
   2. **A `flow:` in that file** — open `flows/<flow>/<flow>.flow.yaml` and walk its edges
      from the entry node. The first node whose artifacts are not yet in the tree is the
      answer. Read the graph; never restate it from memory, and never carry a remembered
      order between projects — the flow file is the only place the sequence lives, and a
      router that recites it becomes wrong the first time an edge moves.
   3. **A `flow:` naming no such file** — say so plainly rather than guessing a neighbour.
      A wrong flow re-sizes every skill after it.

4. **Answer with one name and its evidence.** Name a single skill, and the sentence that
   chose it: which file was absent, which edge was walked, which door the work came in
   through. A list of candidates hands the decision back, and the user came here because
   they did not have it.

**Done when** the user has one skill name and can see what chose it.
