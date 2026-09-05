# Slice loop — slugs and freezing

The two per-feature loops share two rules: how a dossier is named, and when it stops being
working state. `spec-feature`, `build-plan` and `build-implement` read this file. Every path
below is `concept_structure.md`'s, relative to `_concept/`.

## Slug rule

Both slugs match `^[a-z][a-z0-9-]{1,47}$`. Derive one from a human title by lowercasing,
replacing each run of non-`[a-z0-9]` characters with a single `-`, trimming leading and
trailing `-`, and truncating to 48 characters.

**`feature_slug`** names three things at once — `05_features/<featureset>/<feature_slug>.md`,
`07_screens/<feature_slug>/`, and `08_dossiers/<feature_slug>/`. It resolves by globbing
`05_features/*/<feature_slug>.md`. Zero matches means the spec was never written; more than
one means two featuresets claim the slug, so name the matches and ask rather than picking.

**`slice_id`** names one vertical slice's dossier, `11_build/slices/<slice_id>/`, and is
derived from that slice's own title. A feature decomposes into several slices, so it is not
the feature slug: the slice's `plan.md` frontmatter carries `feature` and `blocked_by`
instead, and dependency order lives in those edges rather than in the directory name.

A slug that already exists is a resume, not a collision. Load what is there, show what would
change, and write after the user agrees — overwriting a dossier silently discards the
reasoning it holds, which is the only thing a dossier is for.

## Freeze lifecycle

A dossier is **frozen** by writing `index.md` into it. Frozen means indexed and closed: it
stops being working state and becomes the record of how the feature or slice got built.
Nothing in a dossier is deleted; the one removal is the transient
`11_build/slices/<slice_id>/progress.yaml`, dropped by the freeze that makes it moot.

| dossier | frozen by | when |
|---|---|---|
| `08_dossiers/<feature_slug>/` | `spec-feature` | every spec and screen write has landed |
| `11_build/slices/<slice_id>/` | `build-implement` | every commit for the slice has landed |

`index.md` carries `status: frozen` in its frontmatter and links forward to the canonical
artifacts — the spec and its screens for a feature, the commit SHAs and the feature spec for
a slice. An unfrozen slice dossier means work that was built and never committed, which is
why `build-branch` refuses to close a branch while one exists.

## Session boundaries

The boundaries inside both loops are answered once, at authoring time, in
`../docs/adr/0005-warm-and-cold-session-boundaries.md`: warm within a loop, cold on the way
out of one. That is why a frozen dossier has to stand on its own — the next reader of it may
be a different session, host or person.
