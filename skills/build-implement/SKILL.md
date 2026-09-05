---
name: build-implement
description: "Use when a planned vertical slice is ready to build — implements it test-first, reviews it against its spec, then commits it and freezes its dossier. Triggers on 'build this slice', 'implement the next slice', 'land it'."
version: "0.1.0"
artifacts:
  requires:
    - { id: slice-plan, gate: hard }
    - { id: features, gate: hard }
    - { id: screens, gate: hard }
    - { id: datamodel, gate: soft }
prerequisites:
  files:
    - { path: "11_build/slices", gate: hard, min_entries: 1 }
    - { path: "05_features", gate: hard, min_entries: 1 }
    - { path: "07_screens", gate: hard, min_entries: 1 }
---

# build-implement

Builds one vertical slice and lands it. Everything it knows about the work comes from
`11_build/slices/<slice_id>/plan.md` and the artifacts that plan names; everything it knows
about how to build is `tdd` and `code-review`, which it calls rather than restates.

## Steps

1. **Load the slice.** Read `plan.md`, the feature spec it names, and the screens under
   `07_screens/<feature_slug>/`. Refuse to start while any `blocked_by` slice is unfrozen —
   its dossier has no `index.md`, so the thing this slice builds on does not exist yet.
   Resume from `progress.yaml` if one is there.
2. **Build the rows, one at a time, with `tdd`.** A row is done when its UI renders real
   data, its handler is callable from that UI, its data layer round-trips, and its tests are
   green — then the next row starts. Confirm the seams with the user before the first test,
   as `tdd` requires; the plan's test tags say which level, not where. Mark each finished row
   in `progress.yaml`.
3. **Review against the spec before reviewing the code.** Read the feature spec against what
   was actually built, assuming the implementer finished suspiciously quickly: every
   acceptance criterion present in the code, not merely implied by a passing test. Fix gaps
   and re-run before going further — a quality review of the wrong feature is wasted work.
   Then run `code-review`.
4. **Run the gate in `plan.md`.** Its manual checks are questions for the user, one at a
   time; its automated tests are commands. Add what using it felt like — awkward flow, hidden
   state, a screen doing too much — and close on **Done**, **Needs more work**, or
   **Blocked**, the last two naming what has to change and who owns it. Only Done continues.
5. **Recap** in the dossier: one to three sentences of what a user can now do, in their
   words rather than the code's; the files touched; and where the outcome differed from the
   plan, with the reason. This is what the next reader gets instead of this session.
6. **Propose one simplification pass.** One to three of the smallest behaviour-preserving
   improvements — a deletion, a simplification, a clarification — each with what verifies the
   behaviour survived, and let the user pick. Additions are proposals for the next slice, not
   for this one; the value here is subtraction while the code is still fresh.
7. **Commit atomically.** Propose the decomposition — migration, logic, UI, tests — and stage
   an explicit file list per commit after the user approves it, never `.` or `-A`. Each commit
   body names the slice and its feature spec; that trailer is how a commit is traced back to
   the artifact that asked for it.
8. **Freeze the dossier and back-link the spec.** Once every commit has landed, write
   `11_build/slices/<slice_id>/index.md` per `contracts/slice_loop.md` — the commits, the
   feature spec, the recap — and remove `progress.yaml`. Then patch the feature spec's
   frontmatter with the slice reference, the commit SHAs and the source files, per
   `contracts/feedback_loop.md`; leave that edit in the working tree for the next commit.
   Everything else under `_concept/` was read, not rewritten: this back-link and the slice's
   own dossier are the only things this skill writes there, and a spec quietly edited to
   match the code stops being the thing the code is checked against.

**Done when** the slice's commits are on the branch, `index.md` exists beside `plan.md`, and
the feature spec points back at both.
