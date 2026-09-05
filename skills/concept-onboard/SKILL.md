---
name: concept-onboard
description: "Use at the start of a project to capture what the pipeline needs and the user already knows — technology preferences, an existing brand, the material they are bringing with them. Also when they say 'I have existing docs', 'use these files', or an answer needs someone who is not in the room. Triggers on 'onboard', 'set up the project', 'ingest my seeds'."
version: "0.1.0"
metadata:
  artifacts:
    requires:
      - { id: scope }
  prerequisites:
    files:
      - { path: "_concept/01_meta/scope.yaml", gate: soft }
    inputs_optional:
      - { id: framework, label: "Preferred framework or language", type: text, hint: "Skip if undecided" }
      - { id: database, label: "Database preference", type: text }
      - { id: ui_library, label: "UI component library", type: text }
      - { id: auth, label: "Authentication approach", type: text }
      - { id: has_brand, label: "Is there an existing brand?", type: boolean }
---

# concept-onboard

Fills `02_grounding/onboarding/` — the preferences, constraints and material a project
arrives with, before any artifact is designed against them. It collects and records; it
designs nothing. The vision is `concept-brief`'s, the sizing is `concept-scope`'s, and every
technology named here is a preference a later skill weighs, not a decision it inherits.

Paths are `contracts/concept_structure.md`'s. Everything this skill writes lands under
`02_grounding/`, which every skill may read at any point.

## Steps

1. **Resume before asking.** `02_grounding/onboarding/onboarding.yaml` present means this
   ran before: show what it holds and ask whether to continue with it, change specific
   answers, or start over. `answers.json` holds the raw per-field values a dialog collected
   and is what makes "change specific answers" cheap — carry it forward on every write.
   Read `01_meta/scope.yaml` for `project_type` and the flow; this skill confirms that value
   rather than collecting it again, and a project whose type is unset behaves as `web-app`
   everywhere downstream.
2. **Collect the technology preferences**, one question at a time per
   `contracts/agent_patterns.md § Questions Are Standalone Messages`: framework or language,
   data access and database, UI component library, authentication, and the overall
   architecture pattern. Each answer carries its confidence — **locked** (decided, not open
   to a recommendation), **preferred** (open to a better fit), **open** (recommend from the
   project's signals). That word is the whole point of the question: `architecture-techstack`
   can overrule *preferred* and must honour *locked*, and without it every answer reads as
   binding. Skip anything the user has not decided rather than recording a null.
3. **Ask what the project already has.** An existing brand — logo, palette, typography, a
   style guide — and where those files are, because `design-brand` extracts from them instead
   of proposing. On a flow that renders a walkthrough, which renderer the project wants
   (`static-html` for a zero-build page set, `astro` for a built site); that answer is read
   at render time and is the one place it is recorded.
4. **Inventory the seeds.** Scan `02_grounding/seeds/` — everything the user dropped in.
   For each file say which artifact it seeds and how far it gets there: **complete** (a later
   skill should adopt it and skip collecting that ground), **partial** (a starting point with
   named gaps), or **reference** (context only — code excerpts, competitor PDFs, anything
   unclassifiable). Show the table and let the user correct it before recording; a
   misclassified seed either gets ignored or gets treated as truth. Read the files where
   they sit and leave them there: a renamed seed breaks the citation of every skill that
   was going to quote it.
5. **Route the questions nobody in the room can answer.** Where an answer needs a person who
   is not here — a compliance owner, whoever holds the integration credentials, the client —
   write `02_grounding/onboarding/questions.md` instead of guessing or stalling. Aim each
   question at the gap between what that person knows and what this project needs, state the
   decision riding on it, order most-important-first, keep one idea per question, and leave a
   blank answer stub under each. Async usually gets one pass, so a compound question comes
   back half-answered.
6. **Write `onboarding.yaml`**, merging rather than replacing what step 1 loaded: the
   confirmed identity, the decisions with their confidence and any rationale given, the brand
   answer, the renderer under `mockup.renderer`, and the seed inventory. Report what was
   captured and which questions went out.

**Done when** `onboarding.yaml` and `answers.json` exist, every seed under
`02_grounding/seeds/` appears in the inventory, and any question for someone outside the
room is in `questions.md`.
