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
2. Each journey includes `candidate_features` (slugs) and `candidate_entities` (PascalCase names)
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

### When `architecture-datamodel` writes the model:

1. Write the schema file (format determined by the stack)
2. Write `10_blueprint/datamodel/feature-map.json` mapping each model to the features it serves
3. For each referenced feature, read its frontmatter
4. Set `data_entities:` to the list of model names (PascalCase) that serve this feature
5. Update `last_updated` on the feature file

```yaml
# 05_features/auth/login.md — updated by architecture-datamodel
data_entities: [User, Session]
```

### When `experience-behaviors` writes behavioural specs (optional):

1. Write one markdown file per featureset to `06_behaviors/<featureset>.md`
2. No frontmatter updates needed — downstream skills discover them by checking the folder

### When `architecture-datamodel` reads behavioural specs (optional):

1. Check whether `06_behaviors/*.md` exists
2. If present, use its state tables to pre-populate the data model:
   - Entity states → model enums
   - Entity relationships → model relationships
   - Named constants → field defaults and constraints
3. This is additive — the agent still reads features and applies its own analysis

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
3. Find all models in `feature-map.json` that reference the feature
4. Remove the reference

## Validation

`ops-review` checks for broken cross-references:

- Screen references a feature that doesn't exist → ERROR
- Feature lists a screen that doesn't exist → ERROR
- Model in `feature-map.json` references a feature that doesn't exist → WARNING
- Feature has `screens: []` but matching screens exist → WARNING (missing link)
- Feature has `story_refs` pointing to a journey ID not in `stories.yaml` → WARNING
