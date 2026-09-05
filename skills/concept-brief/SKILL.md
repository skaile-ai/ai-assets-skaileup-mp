---
name: concept-brief
description: "Use when a concept has no _concept/brief.md yet, or the user wants to redefine one. Writes the pitch, the goals and the comparables — the three root files everything downstream reads. Triggers on 'I have an app idea', 'new project', 'start from scratch', 'redo the brief'."
version: "0.1.0"
metadata:
  requires:
    - contract:@skaile-ai/shared-contracts
  artifacts:
    requires:
      - { id: scope }
  prerequisites:
    files:
      - { path: "_concept/01_meta/scope.yaml", gate: soft }
    inputs_optional:
      - { id: raw_description, label: "Describe your idea", type: textarea, hint: "Free-form — name, audience, problem and hero flow can all be mined from this" }
      - { id: elevator_pitch, label: "What does the app do?", type: text, hint: "One sentence: who it is for, what it does" }
      - { id: target_audience, label: "Who is the primary user?", type: text, hint: "Role, context, skill level" }
      - { id: problem_statement, label: "What problem does it solve?", type: text, hint: "The single most important one" }
      - { id: hero_flow, label: "Most important user action", type: text, hint: "The one thing every user must be able to do" }
      - { id: comparable_products, label: "Similar apps", type: text }
      - { id: success_criteria, label: "What does success look like?", type: text, hint: "Goals, constraints, deadlines" }
---

# concept-brief

The three root files of a concept — `brief.md`, `goals.md`, `comparable.md` — and nothing
else. Journeys, features, screens, brand and stack all read these, so a brief that guesses
sets the whole concept guessing. It writes what the user actually said and hands off.

Paths are `contracts/concept_structure.md`'s and the frontmatter shapes are
`contracts/artifact_frontmatter.md`'s. `02_grounding/` is readable at any point and is the
only thing upstream of this skill.

## Steps

1. **Read what already exists.** `02_grounding/onboarding/` for answers a dialog collected,
   and `02_grounding/research/{domain,competitors,audiences}.md` where research ran first —
   that file set is the deep pass, and this skill distils it rather than re-running it. The
   flow in `01_meta/scope.yaml` sets how hard steps 3 and 4 work: `appbuilder-mvp` takes one
   pass at each, `appbuilder-standard` and `skaileup-concept-only` work them until the user
   stops correcting.
2. **Get the pitch.** With a free-form description, mine it for everything it carries — name,
   pitch, audience, problem, hero flow, comparables, success criteria — and carry on with the
   gaps; step 5 is a cheaper place to fill one than an interview is. Otherwise ask, one at a
   time: what it does in a sentence, who the primary user is, the single most important
   problem, the one action every user must be able to take, similar apps, and what success
   looks like. Write `brief.md` — frontmatter per the contract, then the vision in plain
   language: who it serves, what problem it solves, the primary journey.
3. **Turn the vision into goals**, in `goals.md`: the one outcome that would mean this
   worked, the measurable signals behind it, hard constraints (deadline, budget, compliance,
   platform), and the explicit non-goals — what people will expect and this deliberately will
   not do. Every criterion ties back to the brief's problem or hero flow, and each one is a
   number, a threshold or a yes/no condition, because a goal nobody can settle is a goal
   nothing downstream can be checked against. A deadline or budget the user never implied is
   written `TBD`: an invented one gets planned around.
4. **Study the comparables**, in `comparable.md`: three to six products — at least one direct
   competitor, one indirect, one adjacent, since the best patterns cross domains. Each gets a
   concrete borrow and a concrete avoid, named as a specific pattern rather than "good UX",
   and the file closes on the positioning gap: where this product sits that none of them do,
   tied to the audience. If the user named none and no research exists, write that. A
   fabricated competitor is indistinguishable from a real one by the time features are being
   cut against it, and unverifiable claims about a real one are marked `unverified`.
5. **Show the brief and wait for a yes in words.** Apply changes, show it again, ask again.
   The brief is the root of every artifact after it, so an unapproved one propagates its
   mistakes into work that costs far more to redo than this conversation does.
6. **Pin the vocabulary the user settled**, per `contracts/domain_model.md` — a term they
   corrected you on goes into `10_blueprint/glossary.md` now, while the correction is still
   in the room. The whole downstream tree uses that word or drifts from it.

**Done when** `brief.md`, `goals.md` and `comparable.md` are on disk and the user has said
yes to the brief.
