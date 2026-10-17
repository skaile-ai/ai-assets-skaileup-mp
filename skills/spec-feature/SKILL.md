---
name: spec-feature
description: "Use when one feature needs its permanent spec — grills the user, draws the in/out line, then writes the feature spec and every screen it needs. Triggers on 'spec this feature', 'design a new feature', 'lock down acceptance criteria', 'what is in vs out'."
version: "0.1.0"
metadata:
  requires:
    - contract:@skaile-ai/shared-contracts
  artifacts:
    requires:
      - { id: scope }
      - { id: brief }
      - { id: journeys }
      - { id: brand-tokens }
      - { id: datamodel }
      - { id: glossary }
      - { id: app-design }
    produces:
      - { id: features, path: "_concept/05_features/<featureset>/<feature>.md" }
      - { id: screens, path: "_concept/07_screens/<feature_slug>/<screen>.md" }
      - { id: dossier, path: "_concept/08_dossiers/<feature_slug>/index.md" }
      - { id: decisions, path: "_concept/10_blueprint/decisions.md" }
  prerequisites:
    files:
      - { path: "_concept/01_meta/scope.yaml", gate: hard }
      - { path: "_concept/brief.md", gate: hard }
      - { path: "_concept/glossary.md", gate: hard }
      - { path: "_concept/04_journeys/stories.yaml", gate: soft }
      - { path: "_concept/10_blueprint/datamodel", gate: soft }
      - { path: "APP-DESIGN.md", gate: soft }
---

# spec-feature

One feature, from a sentence to a spec somebody can build: the interview, the scope line,
then the two permanent artifacts — the feature spec and its screen specs — and the feature
dossier, opened with the grill and frozen last. This skill is the **only writer of screen
specs and their `elements:` blocks**; `experience-shell` writes the shell's nav elements in
`07_screens/shell.md`, nothing else under that tree. It handles **one** feature per run and
is re-entered once per feature in `05_features/featuresets.md`: the flow graph draws that
node once, because iteration is not something a flow edge can express, so the repetition
lives here.

Paths are `contracts/concept_structure.md § The tree`. Each step names the contract section
it writes to; read that section at the step, not before.

## Steps

1. **Resolve the feature and its slug.** Take a one-sentence title, derive `feature_slug`
   per `contracts/slice_loop.md § Slug rule`, and place it in exactly one featureset under
   `05_features/`. A glob that already resolves means this is a refinement of an existing
   spec: load it and say so before asking anything, so the user answers against what is
   written rather than from memory, and carry its existing `screens:` array through
   untouched — it was populated by a later step that is not running now, and a rewritten
   spec that drops it silently unlinks the feature from its screens. Two matches across
   featuresets is the collision the slug rule names — list both and ask which one this is.
2. **Grill.** Call the Skill tool with "grilling" against this feature. If it is not
   installed, run the rounds yourself: one frontier of unsettled questions per message, each
   with a recommended answer. Either way, what this feature adds is the ground the frontier
   has to cover before it can be empty: what the feature *is* and who triggers it, the
   happy path, state
   transitions, boundary inputs, concurrency, a role × action permissions table, persistence
   and recovery, error states, and the other features this one touches. The flow in
   `01_meta/scope.yaml` sets the depth — `appbuilder-mvp` settles the happy path and
   permissions in a round or two; `appbuilder-standard`, `skaileup-concept-only` and
   `skaileup-concept-reverse` work the tree until the frontier is genuinely empty. Read
   `brief.md`, `04_journeys/stories.yaml` and any sibling spec the feature touches first —
   no journeys and no data model means the interview carries both loads, so ask where the
   feature sits in a journey rather than assuming it stands alone:
   `grilling` makes finding facts your job, and asking the user something the tree already
   says spends the round you needed for a real question.
   Open the dossier as the grill starts: write `08_dossiers/<feature_slug>/index.md` with
   `status: open` and the framing, then append what each round settles — answers, rejected
   options — and, after every later step, what that step settled that the spec will not hold.
   A session that dies mid-feature leaves its reasons on disk; an `open` dossier already there
   is that interrupted run, so load it and continue.
3. **Use the glossary's words; pin decisions as they pass the gate.** Name every concept in
   the grill by its term in `glossary.md`, per `contracts/domain_model.md § Glossary format`
   — a synonym from the `_Avoid_` list is renamed to the term, not adopted. Entity names are
   read, never coined: from `10_blueprint/datamodel/model.json` when it exists, else from the
   glossary. A concept with no term stops the interview: name it and hand back, and the flow
   re-enters `concept-glossary`, which pins it before this feature goes on. A choice that
   passes the three-test gate appends to
   `10_blueprint/decisions.md`, cheap now and unrecoverable later: the reasoning is in the
   room only while the interview is running.
4. **Draw the scope line.** Walk every edge case and open question the grill surfaced and
   put each one IN, OUT, or DEFER with a one-line rationale. IN items become acceptance
   criteria; the whole line becomes the spec's `## Scope` section (step 5), the one record of
   what was considered — a later reader looks there to tell a considered item from a forgotten
   one, and the dossier links to it rather than copying it. A DEFER names the feature or slice
   that will pick it up, or it is an OUT wearing a friendlier word. `10_blueprint/decisions.md`
   takes only decisions that pass `contracts/domain_model.md § The ADR gate — record
   sparingly`: an OUT that clears it appends with Status `rejected`, because a refusal that
   binds the whole design stays invisible to the next feature unless it is logged where that
   feature reads.
5. **Write the feature spec** to `05_features/<featureset>/<feature_slug>.md`: frontmatter per
   `contracts/artifact_frontmatter.md § 05_features/\<featureset\>/\<feature\>.md`,
   `## Permissions`, `## Scope` from step 4, and the acceptance criteria. `## Permissions`
   is the role × action table from the grill, in the form `contracts/concept_structure.md`
   gives for the `05_features/` permissions section, with roles from `featuresets.md`'s
   vocabulary. This spec is the one record of who may do what; `experience-behaviors`, the
   seed and scaffolding cite it, so none restates it. Criteria from `stories.yaml` are cited
   by id (`AC-…`, `contracts/acceptance_criteria.md § Criterion ids`), never retyped; one the
   feature needs that its journeys lack stops the write and hands back to
   `experience-journeys`. A criterion the grill adds that no story carries takes an id in
   the same grammar under the feature slug. Set `data_entities: [<ModelName>, …]` to the
   `model.json` models the feature reads or writes, each name copied from the model — the
   one feature↔entity join. An entity the model lacks stops the write and hands back to
   `architecture-datamodel`; with no `model.json`, hand back the same way when the flow has
   that node, otherwise leave the list empty and name entities by glossary term. Every
   criterion traces to something the user confirmed in the grill — an invented one reads
   exactly like a real one to the implementer, and gets built.
6. **Write one screen spec per screen the feature needs**, at
   `07_screens/<feature_slug>/<screen>.md`. Each carries `implements:` pointing back at the
   feature file and an `elements:` block per `contracts/elements_block.md § Schema` — the
   block the walkthrough renderers, the annotator and the feedback pass all read, so a screen
   without it renders as an auto-slugged guess. Name only screens the scope line put IN. Where
   `APP-DESIGN.md` exists, each editing surface is the OBJ `task → surface` row of the entity
   it edits (`contracts/app_design.md § Reading it`); a surface the floorplan lacks goes back
   to `experience-interaction`, not invented. Without the file the screen chooses and says so.
7. **Register both directions**, per `contracts/feedback_loop.md § Registration Protocol`:
   the feature's `screens:` lists the files just written, each screen's `implements:` names
   the feature. A one-directional link is a screen nothing can find from its feature.
8. **Show the whole write set and the blast radius, then write.** An existing file gets its
   diff shown and its own answer — the user's earlier edits are the case this catches. Beside
   the diffs, name which already-written artifacts this feature just invalidated and whose
   owner has to re-run: `04_journeys/stories.yaml` when it introduces a flow no story covers,
   `10_blueprint/techstack.md` for a new dependency, `architecture.md` for a new module or
   protocol, `10_blueprint/datamodel/` for new entities or fields, and `07_screens/shell.md`
   when it adds a top-level destination. Naming the owner is the whole of it — this skill
   edits none of them, and a cascade that reaches into five trees is the multi-writer tangle
   one writer per artifact exists to avoid. When the project is already built, `build-plan`
   is the next command: the feature is specified, not planned.
9. **Freeze the feature dossier.** Append the links forward to the spec (its `## Scope`
   included) and the screens, then set `status: frozen` per
   `contracts/slice_loop.md § Freeze lifecycle`. Steps 2–8 already put the framing and the
   grill's answers on disk; the scope line stays the spec's, linked rather than copied. Skip
   the dossier and the next reader has the decisions without any of the reasons.

**Done when** the spec, every screen it names, and the frozen dossier are on disk, and the
feature's `screens:` and each screen's `implements:` resolve to each other.
