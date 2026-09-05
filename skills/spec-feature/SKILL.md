---
name: spec-feature
description: "Use when one feature needs its permanent spec — grills the user, draws the in/out line, then writes the feature spec and every screen it needs. Triggers on 'spec this feature', 'design a new feature', 'lock down acceptance criteria', 'what is in vs out'."
version: "0.1.0"
metadata:
  artifacts:
    requires:
      - { id: scope }
      - { id: brief }
      - { id: journeys }
      - { id: brand-tokens }
      - { id: datamodel }
  prerequisites:
    files:
      - { path: "_concept/01_meta/scope.yaml", gate: hard }
      - { path: "_concept/brief.md", gate: hard }
      - { path: "_concept/04_journeys/stories.yaml", gate: soft }
      - { path: "_concept/10_blueprint/datamodel", gate: soft }
---

# spec-feature

One feature, from a sentence to a spec somebody can build: the interview, the scope line,
then the two permanent artifacts — the feature spec and its screen specs — and the feature
dossier frozen behind them. This skill is the **only writer of screen specs and of the
`elements:` block**; `experience-shell` owns `07_screens/shell.md` and nothing else under
that tree.

Paths are `contracts/concept_structure.md`'s. The slug rule and the freeze are
`contracts/slice_loop.md`'s, the `elements:` schema is `contracts/elements_block.md`'s, the
frontmatter shapes are `contracts/artifact_frontmatter.md`'s, and the EARS grammar is
`contracts/acceptance_criteria.md § EARS template`. Read each at the step that uses it.

## Steps

1. **Resolve the feature and its slug.** Take a one-sentence title, derive `feature_slug`
   per `contracts/slice_loop.md`, and place it in exactly one featureset under
   `05_features/`. A glob that already resolves means this is a refinement of an existing
   spec: load it and say so before asking anything, so the user answers against what is
   written rather than from memory. Two matches across featuresets is the collision the slug
   rule names — list both and ask which one this is.
2. **Grill.** Run the global `grilling` skill against this feature. Its rounds and frontier
   are the interview; what this feature adds is the ground the frontier has to cover before
   it can be empty: what the feature *is* and who triggers it, the happy path, state
   transitions, boundary inputs, concurrency, a role × action permissions table, persistence
   and recovery, error states, and the other features this one touches. The tier in
   `01_meta/scope.yaml` sets the depth — `appbuilder-mvp` and `appbuilder-simple` settle the
   happy path and permissions in a round or two; `appbuilder-standard` and
   `appbuilder-complex` work the tree until the frontier is genuinely empty. Read
   `brief.md`, `04_journeys/stories.yaml` and any sibling spec the feature touches first —
   no journeys and no data model means the interview carries both loads, so ask where the
   feature sits in a journey rather than assuming it stands alone:
   `grilling` makes finding facts your job, and asking the user something the tree already
   says spends the round you needed for a real question.
3. **Pin the vocabulary as it crystallises**, per `contracts/domain_model.md` — a term the
   user settles goes into `10_blueprint/glossary.md`, a choice that passes the three-test
   gate appends to `10_blueprint/decisions.md`. Both are cheap now and unrecoverable later:
   the reasoning is in the room only while the interview is running.
4. **Draw the scope line.** Walk every edge case and open question the grill surfaced and
   put each one IN, OUT, or DEFER with a one-line rationale. IN items become acceptance
   criteria; OUT and DEFER become the spec's `## Out of Scope` section, which is where a
   later reader looks to find out whether something was considered or forgotten. A DEFER
   names the feature or slice that will pick it up, or it is an OUT wearing a friendlier word.
   An OUT that clears the three-test gate also appends to `10_blueprint/decisions.md` with
   Status `rejected`, per `contracts/domain_model.md` — `## Out of Scope` is this feature's
   and freezes with its dossier, so a refusal that binds the whole design stays invisible to
   the next feature unless it is also logged where that feature reads.
5. **Write the feature spec** to `05_features/<featureset>/<feature_slug>.md`: frontmatter
   per the contract (including the `permissions:` block and its restated table), the
   acceptance criteria in EARS, `## Out of Scope` from step 4, and the entities the feature
   reads or writes. Every criterion traces to something the user confirmed in the grill —
   an invented one reads exactly like a real one to the implementer, and gets built.
6. **Write one screen spec per screen the feature needs**, at
   `07_screens/<feature_slug>/<screen>.md`. Each carries `implements:` pointing back at the
   feature file and an `elements:` block per `contracts/elements_block.md` — that block is
   what the walkthrough renderers, the annotator and the feedback pass all read, so a screen
   without it renders as an auto-slugged guess. Name only screens the scope line put IN.
7. **Register both directions**, per `contracts/feedback_loop.md`: the feature's `screens:`
   lists the files just written, each screen's `implements:` names the feature. A
   one-directional link is a screen nothing can find from the feature it belongs to.
8. **Show the whole write set and get approval**, then write. An existing file gets its diff
   shown and its own answer — the user's earlier edits are the case this catches.
9. **Freeze the feature dossier.** Write `08_dossiers/<feature_slug>/index.md`: the framing,
   the questions the grill answered, the scope line with its rationales, and links forward to
   the spec and screens. It is written once, at the end, and frozen by existing — the working
   notes lived in this session's context, which is what the warm boundary inside the loop
   buys. Skip it and the next reader has the decisions without any of the reasons.

**Done when** the spec, every screen it names, and the frozen dossier are on disk, and the
feature's `screens:` and each screen's `implements:` resolve to each other.
