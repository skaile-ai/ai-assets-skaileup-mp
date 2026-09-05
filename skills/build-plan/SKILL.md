---
name: build-plan
description: "Use when a frozen feature spec needs breaking into buildable work — cuts the feature into vertical slices, gives each its blocking edges, and writes one slice dossier per slice. Triggers on 'plan this feature', 'break it into slices', 'what do we build first'."
version: "0.1.0"
artifacts:
  requires:
    - { id: features, gate: hard }
    - { id: screens, gate: hard }
    - { id: techstack, gate: soft }
    - { id: datamodel, gate: soft }
prerequisites:
  files:
    - { path: "05_features", gate: hard, min_entries: 1 }
    - { path: "07_screens", gate: hard, min_entries: 1 }
    - { path: "10_blueprint/techstack.md", gate: soft }
    - { path: "10_blueprint/datamodel", gate: soft }
---

# build-plan

Turns one frozen feature spec into the set of **vertical slices** that build it, each with
the slices that block it, each in its own dossier under `11_build/slices/<slice_id>/`. It
plans and stops: `build-implement` takes one dossier and builds it.

Paths are `contracts/concept_structure.md`'s; `slice_id` and the dossier lifecycle are
`contracts/slice_loop.md`'s.

## Steps

1. **Read the feature, then the code.** Load
   `05_features/<featureset>/<feature_slug>.md`, every screen under
   `07_screens/<feature_slug>/`, and `10_blueprint/` for stack, architecture and data model
   where they exist. Then explore the codebase for what is already there. Slice titles and
   descriptions use `10_blueprint/glossary.md`'s vocabulary and respect the decisions in
   `10_blueprint/decisions.md` and `11_build/decisions.md` — a plan written in different
   words than the code is a plan the implementer has to translate. Look for prefactoring
   that makes the change easy first; it becomes the slice everything else is blocked by.
2. **Cut vertical slices.** Each slice is a **tracer bullet**: a narrow but complete path
   through every layer this feature crosses — UI renders real data, the handler is callable
   from it, the data layer round-trips, and its tests are green — demoable on its own and
   sized to fit one fresh context window. Every acceptance criterion in the spec lands in at
   least one slice. The pull to decompose by layer is strong and constant: "all the screens",
   "all the migrations", "wire it up after" each produce N half-finished slices and zero
   working ones, so a candidate slice you cannot describe as something a user can do is a
   layer wearing a slice's name — merge it into the slice that needs it, or split it by
   user-facing seam. Use the data model for slice *order* (parents before children), never
   to reshape a slice into an entity.
3. **Sequence a wide refactor as expand–contract, not as a slice.** A **wide refactor** is
   one mechanical change — rename a column, retype a shared symbol — whose blast radius fans
   across the codebase, so one edit breaks thousands of call sites and no vertical slice can
   land green. Expand first: add the new form beside the old, one slice, blocking the rest.
   Then migrate call sites in batches sized by blast radius (per package, per directory),
   each batch its own slice blocked by the expand, CI green batch to batch because the old
   form still exists. Contract last: delete the old form in a slice blocked by every batch.
   When even the batches cannot stay green alone, keep the sequence but let them share an
   integration branch, and promise green only at a final integrate-and-verify slice.
4. **Give each slice its blocking edges.** `blocked_by` lists the slices that genuinely gate
   it; a slice with none can start immediately. The edges are the whole ordering — the
   dossier directory carries no number, so an edge left off is a slice that will be picked up
   before the thing it needs exists.
5. **Quiz the user before writing anything.** Present the breakdown as a numbered list —
   title, blocked by, and what end-to-end behaviour the slice delivers. Ask whether the
   granularity is right, whether each edge is a real gate rather than a hunch, and what should
   merge or split. Iterate until they approve. This is the cheapest point at which a
   mis-cut slice costs a sentence instead of a rewrite.
6. **Write one dossier per approved slice** — `11_build/slices/<slice_id>/plan.md`, slug per
   `contracts/slice_loop.md`, with frontmatter naming the feature file and `blocked_by`, and
   a body carrying: the one-line slice scope; the rows of UI / logic / data it crosses, each
   citing the screen file, the symbol and the entity by name; the acceptance criteria from
   the spec it satisfies, copied verbatim; the manual checks and automated tests that prove
   it, each test tagged `[unit]`, `[integration]` or `[e2e]` by the smallest reliable seam;
   and the carry-overs it deliberately leaves open. Testing belongs here rather than after —
   a slice whose tests are decided later is a slice whose seams were never agreed.
7. **Report the frontier** — the slices whose blockers are all satisfied, in the order they
   can start. That list is what `build-implement` is handed.

**Done when** every acceptance criterion in the spec is claimed by a slice, every
`blocked_by` names a slice that exists, and each slice's `plan.md` is on disk.
