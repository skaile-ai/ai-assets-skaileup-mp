---
name: build-implement
description: "Use when a planned vertical slice is ready to build — implements it test-first, reviews it against its spec, then commits it and freezes its dossier. Triggers on 'build this slice', 'implement the next slice', 'land it'."
version: "0.1.0"
metadata:
  requires:
    - contract:@skaile-ai/shared-contracts
  artifacts:
    requires:
      - { id: slice-plan }
      - { id: acceptance-criteria }
      - { id: features }
      - { id: screens }
      - { id: datamodel }
      - { id: standards }
    produces:
      - { id: slice-index, path: "_concept/11_build/slices/<slice_id>/index.md" }
      - { id: acceptance-criteria, path: "_concept/11_build/acceptance-criteria/<featureset>/<feature_slug>.ac.md" }
      - { id: trace, path: "_concept/11_build/trace.yaml" }
  prerequisites:
    files:
      - { path: "_concept/11_build/slices", gate: hard, min_entries: 1 }
      - { path: "_concept/05_features", gate: hard, min_entries: 1 }
      - { path: "_concept/07_screens", gate: soft, min_entries: 1 }
      - { path: "_concept/02_grounding/standards/index.yml", gate: soft }
---

# build-implement

Builds one vertical slice and lands it. Everything it knows about the work comes from
`11_build/slices/<slice_id>/plan.md` and the artifacts that plan names; everything it knows
about how to build is `tdd` and `code-review`, which it calls rather than restates. Both
have to be installed: this skill stops and names the missing one rather than improvising a
test loop or a review.

## Steps

1. **Load the slice.** Read `plan.md`, the feature spec it names, and the screens under
   `07_screens/<feature_slug>/`. A project whose profile grows no screens has none: the spec
   alone is then the source of truth, and the plan's UI rows name the endpoint, command or
   public function to build instead. Refuse to start while any `blocked_by` slice is
   unfrozen — its dossier has no `index.md`, so the thing this slice builds on does not exist
   yet. Resume from `progress.yaml` if one is there.
2. **Build the rows, one at a time.** Where `02_grounding/standards/index.yml` exists, match
   its entries on `applies_to: build-implement` and the slice's keywords and load the hits
   before the first test, so the code written follows the conventions the codebase already has.
   Call the Skill tool with "tdd" for each row. A row is
   done when its UI renders real data, its handler is callable from that UI, its data layer
   round-trips, and its tests are green — then the next row starts. Confirm the seams with
   the user before the first test,
   as `tdd` requires; the plan's test tags say which level, not where. Mark each finished row
   in `progress.yaml`.
3. **Review the code.** Call the Skill tool with "code-review". Whether the finished feature
   conforms to its spec is `quality-review`'s verdict, the one place that question is asked;
   a second read here would be a second verdict on the same question. What guards this
   slice meanwhile is the ledger in step 7: a criterion with no check behind it stays untested.
4. **Run the gate in `plan.md`.** Its manual checks are questions for the user, one at a
   time; its automated tests are commands. Add what using it felt like — awkward flow, hidden
   state, a screen doing too much — and close on **Done**, **Needs more work**, or
   **Blocked**, the last two naming what has to change and who owns it. Only Done continues.
   Note which criterion ids (`contracts/acceptance_criteria.md § Criterion ids`) each check
   exercised and whether it passed; step 7 writes them to the ledger once there is a commit
   to stamp.
5. **Recap** in the dossier: one to three sentences of what a user can now do, in their
   words rather than the code's; the files touched; and where the outcome differed from the
   plan, with the reason. This is what the next reader gets instead of this session.
6. **Propose one simplification pass.** One to three of the smallest behaviour-preserving
   improvements — a deletion, a simplification, a clarification — each with what verifies the
   behaviour survived, and let the user pick. Additions are proposals for the next slice, not
   for this one; the value here is subtraction while the code is still fresh.
7. **Commit atomically, then record the slice in the trace.** Propose the decomposition —
   migration, logic, UI, tests — and stage an explicit file list per commit after the user
   approves it, never `.` or `-A`. Each commit body names the slice and its feature spec;
   that trailer is how a commit is traced back to the artifact that asked for it. Once the
   last commit has landed, write the slice into `11_build/trace.yaml` — the one
   feature→commit join, which `quality-review`, `quality-release` and `ops-review` read
   instead of rebuilding it from dossiers. Create the file with the first slice; a feature
   cut into several slices has one entry each, and an entry for the same slice id is
   replaced, not duplicated. `code` is the source files the commits touched, tests excluded.
   Then update the ledger at `11_build/acceptance-criteria/<featureset>/<feature_slug>.ac.md`
   per `contracts/acceptance_criteria.md § Ledger updates`, stamping the last commit's short
   sha: only the rows step 4's checks exercised, each carrying its check as the pointer.

   ```yaml
   features:
     <feature_slug>:
       featureset: <featureset>
       slices:
         - { id: <slice_id>, commits: [<sha>, ...], code: [<path>, ...] }
   last_updated: YYYY-MM-DD
   ```
8. **Freeze the dossier.** Once every commit has landed, write
   `11_build/slices/<slice_id>/index.md` per `contracts/slice_loop.md` — the commits, the
   feature spec, the recap — and remove `progress.yaml`. Everything else under `_concept/`
   was read, not rewritten: the ledger rows, the trace entry and the slice's own dossier are
   the only things this skill writes there, and a spec quietly edited to match the code
   stops being the thing the code is checked against. The spec carries no pointer to its
   commits; the trace is the one join.

**Done when** the slice's commits are on the branch, `index.md` exists beside `plan.md`, and
`trace.yaml` carries the slice's entry.
