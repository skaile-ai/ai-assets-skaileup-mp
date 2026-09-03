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
# ...and nothing else unless a machine reads it. Today that means:
#   artifacts.requires[].id + gate   — hard gates the flow engine enforces
#   prerequisites.files[]            — path gates
#   prerequisites.inputs_optional[]  — the input dialog forge-concept renders
#   requires                         — transitive install manifest
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

- **Ceiling 140 lines**, frontmatter included — mp's measured maximum. Both ports came in
  under 110. A skill that cannot fit is a signal about the skill, not about the ceiling.
- **The environment and the contracts are sources of truth; the body is not a cache of
  them.** No READS/WRITES path list (the frontmatter and the contracts have it), no
  CHECKLIST (the validator has it), no Context Budget table.
- **Constraints are stated positively, at the step they bind.** No `MUST`/`NEVER` block.
- **`## Depth Behavior`, `## Standalone Mode`, `## Context Budget`** describe how the
  collection works, not what the skill does. They belong in one place, once — `CONTEXT.md`
  or the router — not in 30-39 skills each.
