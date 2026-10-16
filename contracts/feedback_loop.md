# Feedback Loop — Cross-Reference Protocol

When a downstream skill creates or modifies an artifact that relates to an
upstream artifact, it must register the connection in both directions.
Every path below is `concept_structure.md`'s, relative to `_concept/`.

## The Rule

**Every link must exist in both files.** If screen X implements feature Y,
then feature Y must list screen X, and screen X must list feature Y.

## Registration Protocol

### When `experience-journeys` writes the stories:

1. Write `stories.yaml` to `04_journeys/`
2. Each journey includes `candidate_features` (slugs) and `candidate_entities` (PascalCase glossary terms)
3. `spec-featuresets` consumes them to seed the feature roster
4. No frontmatter updates needed — the roster discovers journeys by reading the file directly

```yaml
journeys:
  - id: onboarding_flow
    persona: new_user
    candidate_features: [registration, email_verification, profile_setup]
    candidate_entities: [User, Profile]
```

### When `spec-featuresets` reads the journeys:

1. Read `04_journeys/stories.yaml`
2. Use `candidate_features` from each journey to seed the roster
3. For each feature, set `story_refs` to the journey IDs that motivated it
4. Features may be added, merged, or split beyond what journeys suggest — `story_refs` traces the origin

```yaml
# 05_features/auth/registration.md
---
story_refs: [onboarding_flow, invite_flow]
---
```

### When `spec-feature` writes a screen:

1. Write the screen file with `implements:` listing the feature paths
2. For each referenced feature, read its frontmatter
3. Append the screen path to the feature's `screens:` array
4. Update `last_updated` on both files

```yaml
# 07_screens/login/login.md
---
implements:
  - 05_features/auth/login.md
  - 05_features/auth/registration.md
---
```

```yaml
# 05_features/auth/login.md — updated by the same run
screens:
  - path: 07_screens/login/login.md
```

### When `spec-feature` writes a feature spec:

1. Read `10_blueprint/datamodel/model.json` for the model names; a feature never coins one
2. Set `data_entities:` in the feature's frontmatter to the list of model names (PascalCase)
   that serve this feature, each one a model in `model.json`
3. Update `last_updated` on the feature file

The feature's `data_entities:` is the only feature↔entity join. To find the features that use
a model, search `05_features/*/*.md` for the model name in `data_entities`.

```yaml
# 05_features/auth/login.md
data_entities: [User, Session]
```

### When `experience-behaviors` writes behavioural specs (optional):

1. Write one markdown file per featureset to `06_behaviors/<featureset>.md`
2. No frontmatter updates needed — downstream skills discover them by checking the folder

### When `spec-feature` reads behavioural specs (optional):

1. Check whether `06_behaviors/*.md` exists
2. If present, use the transitions to inform the screen specs:
   - What a transition exposes → screen data requirements
   - What triggers it → screen user actions
   - Its `requires` guard → state-dependent UI elements

### When `build-implement` freezes a slice:

1. Read the recap in `11_build/slices/<slice_id>/` for the files the slice touched
2. Resolve the feature file by globbing `05_features/*/<feature_slug>.md`, per
   `contracts/slice_loop.md`
3. Set `slice_ref: 11_build/slices/<slice_id>/`, `commits:` (landed SHAs),
   `source_files:` (code paths from the recap, excluding everything under `_concept/`)
   in the feature frontmatter
4. Show the frontmatter diff before writing; update `last_updated` on the feature file

### When a screen is deleted or renamed:

1. Find all features that reference the old screen path
2. Remove or update the entry in their `screens:` array
3. Update `last_updated`

### When a feature is deleted:

1. Find all screens that reference the feature in `implements:`
2. Remove the entry (or flag for human review if the screen depends on it)
3. Nothing to update in the model: it holds no list of features, and the deleted spec's
   `data_entities` goes with the file

## mockup-feedback

`mockup-feedback` is the one place a stakeholder's comment becomes an edit to a spec. It
registers nothing new in either direction: no screen is created, deleted or renamed, so the
`implements:` / `screens:` links stay as they are.

### Screen edits

1. A session annotation routes by its `specRef` to one file, `07_screens/<group>/<screen>.md`.
   The patch edits that file alone, anchored to a heading, and nothing else under
   `07_screens/` or `05_features/`.
2. A feature spec is `spec-feature`'s artifact. Feedback never patches it: an annotation that
   asks for a different rule, scope line or permission becomes a `needs_manual` entry naming
   the screen's `implements:` feature file, and the human re-enters `spec-feature` for that
   feature. A journey annotation becomes `needs_manual` the same way; `stories.yaml` is
   `experience-journeys`' to re-enter.
3. The rendered walkthrough is derived from the screens, so it is stale after an apply;
   `mockup-walkthrough` re-renders it, reading the devlog so the applied edits survive.

### Id promotion

1. An element id the renderer auto-slugged is `provisional: true` in the screen's
   `elements:` frontmatter. The first time a human annotates it the id is worth keeping, so the
   promotion patch flips it to `provisional: false`. The id never changes; only its standing
   does.
2. A navigation annotation on an element with no `target:` is promoted to a `target:` only when
   the destination resolves to exactly one `screen_id` in the walkthrough manifest.
3. A session annotation id is unique within its session only. It becomes a tracked id as the
   `annotationId` of the patches derived from it (`p-<annotationId>-<kind>`) and again in
   `applied/<sid>.json`, which is the lasting record once `sessions/` rotates.

The patch and review-file formats are `mockup-feedback`'s `references/patch-format.md`.

## Validation

`ops-review` checks for broken cross-references:

- Screen references a feature that doesn't exist → ERROR
- Feature lists a screen that doesn't exist → ERROR
- Feature's `data_entities` names a model that is not in `model.json` → WARNING
- Model that no feature's `data_entities` lists → WARNING (an entity nobody asked for, or a feature nobody wrote down)
- Feature has `screens: []` but matching screens exist → WARNING (missing link)
- Feature has `story_refs` pointing to a journey ID not in `stories.yaml` → WARNING
