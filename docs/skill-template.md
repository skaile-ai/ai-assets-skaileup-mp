# The `-mp` skill template

What the two ports converged on. Not a form to fill in — a ceiling and a set of defaults.
Sections come from the skill's own content, the way mp's do; a skill with nothing to say
under a heading does not carry the heading.

```markdown
---
name: <kebab-case; this is the skill's whole identity — install path, flow data.skill,
       produced_by, grounding path>
description: "Use when <trigger>, or when the user says '<phrase>'."
version: "0.1.0"
metadata:                            # everything a machine reads sits under this key —
  artifacts:                         # `parseSkillRequirements` and `extractSkillRequires`
    requires:                        # both read `metadata.` and never fall back to the root
      - { id: <artifact> }           # id only; no code has ever read a `gate:` here
  prerequisites:
    files:                           # the live gate: `_concept/`-prefixed, `hard` or `soft`
      - { path: "_concept/<tree entry>/...", gate: hard, min_entries: 1 }
    inputs_optional:                 # the input dialog forge-concept renders
      - { id: <field>, label: "...", type: text }
---

# <name>

<One paragraph: what this skill does, and where it stops. This replaces Overview,
When to Use, When NOT to Use and Integration — the description already carries the
triggers, so state the job and the boundary instead of restating them.>

<Where a shared contract owns the rules, point at it once and say this file covers only
the deviations. Then list the deviations.>

## Steps

1. **<Verb phrase>.** <What to do. Constraints that bind this step live in this step,
   stated as their consequence — "resolution never depends on parse order", "an invented
   competitor is indistinguishable from a real one downstream" — not as a MUST elsewhere
   in the file.>
2. ...

## <One section for a cluster of constraints, when they genuinely cluster>

<e.g. "The Astro config is load-bearing" — four settings that only make sense together.
Name the consequence of getting it wrong, and point at the file that already encodes it.>

**Done when** <a condition the agent can check, ideally one a command checks for it>.
```

Siblings, in `references/`:

- **A schema or format spec** the steps refer to but do not need inline (`specs-json.md`).
- **Real files the skill copies** rather than writes out from a fence (`scaffold/`).
  A file that is copied is a file that cannot drift from the prose describing it.

## The rules behind it

- **`metadata:` is where the readers look.** `resolver/src/parser.ts:45-46` reads
  `fm.metadata.prerequisites` with no root-level fallback, and
  `discovery/src/requires-graph.ts:236-238` returns early on a missing `metadata`. A block at
  the root parses, renders no error, and reports `satisfied: true` on an unmet gate.
  `name`, `description` and `version` stay at the root: those readers normalise both.
- **A declared path is joined to the *project* root** (`resolver/src/validator.ts:81`), not to
  `_concept/`, so every concept path carries the prefix. `scripts/check.py` enforces both
  halves: a path either starts with `_concept/` and names a real top-level entry of the
  artifact tree, or is one of the named project-root gates in `PROJECT_ROOT_PREREQUISITES`.
- **A `soft` gate renders nowhere** — it is excluded from `satisfied` and never warned on. If
  its absence changes what the skill does, the step says so; the frontmatter alone tells the
  human nothing.
- **Ceiling 140 lines**, frontmatter included — mp's measured maximum. Both ports came in
  under 110. A skill that cannot fit is a signal about the skill, not about the ceiling.
- **The environment and the contracts are sources of truth; the body is not a cache of
  them.** No READS/WRITES path list (the frontmatter and the contracts have it), no
  CHECKLIST (the validator has it), no Context Budget table.
- **Constraints are stated positively, at the step they bind.** No `MUST`/`NEVER` block.
- **`## Depth Behavior`, `## Standalone Mode`, `## Context Budget`** describe how the
  collection works, not what the skill does. They belong in one place, once —
  `contracts/agent_patterns.md`, which already carries `Standalone Mode` and
  `Next-Step Suggestion` — not in 30-39 skills each.
