---
name: concept-brief
description: "Use when starting a new concept and no _concept/discovery/ exists, or when the user says 'I have an app idea', 'new project', 'start from scratch', or wants to redefine an existing brief."
version: '1.0.0'
prerequisites:
  inputs_optional:
    - { id: raw_description, label: 'Describe your idea', type: textarea, hint: 'Free-form — name, audience, problem and hero flow can all be inferred from this' }
    - { id: app_name, label: 'App name', type: text, hint: 'Working name' }
    - { id: elevator_pitch, label: 'What does the app do?', type: text, hint: 'One sentence: who is it for, what does it do' }
    - { id: target_audience, label: 'Who is the primary user?', type: text, hint: 'Role, context, skill level' }
    - { id: problem_statement, label: 'What problem does it solve?', type: text, hint: 'The single most important one' }
    - { id: hero_flow, label: 'Most important user action', type: text, hint: 'The one thing every user must be able to do' }
    - { id: comparable_products, label: 'Similar apps', type: text, hint: 'For reference' }
    - { id: success_criteria, label: 'What does success look like?', type: text, hint: 'Goals, constraints, deadlines' }
---

# concept-brief

The first step of a concept. It writes `_concept/discovery/` — the pitch, the goals, and
the comparables — and stops there. Everything downstream (features, screens, data model,
brand, stack) reads the brief, so a brief that guesses at them sets the whole concept
guessing. Write what the user actually said and hand off.

Nothing downstream exists yet, so there is nothing downstream to read. Your inputs are the
user, `_concept/_grounding/overview/user_input.json` if a dialog pre-collected answers, and
`_concept/_grounding/research/{domain,competitors}.md` if research ran first. All three are
optional.

## 1. Gather

Read `user_input.json` first and use whatever it holds.

If `raw_description` is present, mine it for every field you can — name, pitch, audience,
problem, hero flow, comparables, success criteria — and carry on with gaps. The user reviews
in step 3, which is a cheaper place to fill a gap than an interview.

Otherwise ask, one at a time, and wait for the answers:

1. What does the app do, in a sentence?
2. Who is the primary user — role, context, skill level?
3. What is the single most important problem it solves?
4. What is the one action every user must be able to take?
5. Are there apps that do something similar?
6. What does success look like? Constraints, deadlines?
7. How big is this — a focused tool, a moderate feature set, or a large system?

## 2. Write

Three files under `_concept/discovery/`, frontmatter per `contracts/frontmatter.md`:

- **`brief.md`** — frontmatter (`elevator_pitch`, `audience`, `problem`, `hero_flow`,
  `comparable_products`, `last_updated`) plus the vision in natural language: who it serves,
  what problem it solves, the primary journey.
- **`goals.md`** — success criteria, constraints, deadlines, known limitations.
- **`comparable.md`** — per app: what it does well, what to borrow, what to avoid. If the
  user named none, write that. A fabricated competitor is indistinguishable from a real one
  by the time `concept-comparable` and `product-spec-features` read this file.

Then size the project from the description — `small` (≤5 implied features, no custom
backend), `standard` (6–15), or `complex` (16+, or multi-tenant, or a significant custom
backend) — and write `{ "complexity", "complexity_rationale" }` into
`_concept/_grounding/overview/user_input.json`. It lives there rather than in `brief.md`
frontmatter because the frontmatter shape is pinned and downstream skills read the grounding
file. Tell the user your read of the size in a sentence; they may correct it, and their
answer wins.

## 3. Approve

Show the user `brief.md` and ask: "Does this capture your vision? Approve to continue, or
tell me what to change." Apply changes, show again, ask again — until they approve in words.
The brief is the root of every downstream artifact, so an unapproved brief propagates its
mistakes into work that costs far more to redo.

**Done when** all three files exist and the user has said yes to the brief.

## 4. Hand off

Point at what comes next: `research` to explore the domain (optional), `design-brand-visual`
for visual identity, `product-spec-features` to spec what the app does, or a flow to walk the
whole pipeline.
