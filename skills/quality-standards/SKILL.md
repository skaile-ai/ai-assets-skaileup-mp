---
name: quality-standards
description: "Use when work is starting against an existing codebase and its conventions have not been written down — scans the code for the patterns it already follows and records them as standards the build skills read. Triggers on 'discover standards', 'what conventions does this codebase use', 'analyse the codebase'."
version: "0.1.0"
---

# quality-standards

Reads an existing codebase and writes down the conventions it already follows, so anything
added to it looks like it belongs there. Discovery only — this skill applies nothing; the
skills that write code read `02_grounding/standards/index.yml` themselves when they need it.

It has no gates by design: it reads code, not `_concept/`, so it runs at any point, and it
is the one part of the pipeline that works on a repository with no concept at all.

## Steps

1. **Agree the scope.** Ask for the path to analyse — in a reverse-engineering run that is
   the repository you are already in — and which domains to cover: `api`, `database`, `ui`,
   `naming`, `testing`, `architecture`. Narrow beats complete: a domain nothing downstream
   writes into produces standards nothing reads.
2. **Scan broadly before concluding.** A convention is a pattern with several independent
   instances; one occurrence is somebody's choice on one afternoon, and recording it as a
   standard binds every future author to an accident. Where a pattern has two competing
   forms, record the dominant one and name the exception rather than picking a winner.
3. **Write one file per convention** to `02_grounding/standards/<domain>/<convention>.md`,
   with frontmatter and a body short enough to be read at the point of use:

   ```yaml
   ---
   domain: api
   keywords: [routing, rest, endpoints]     # what a reader greps for
   applies_to: [build-implement, build-plan]  # skill names, exactly as they install
   last_updated: YYYY-MM-DD
   ---
   ```

   The body is the rule in a sentence or two, then one example from this codebase that
   follows it and one that would not. Examples that are invented rather than lifted are how
   a standards file ends up describing a codebase nobody has.

   `applies_to` names skills by their `name:`, which is a skill's whole identity — a value
   that resolves to no installed skill matches nothing and silently narrows the standard to
   zero readers.
4. **Write the index** at `02_grounding/standards/index.yml`, one entry per file carrying
   `path`, `domain`, `keywords` and `applies_to`. This is the file readers actually open:
   they match on `applies_to` and `keywords` and load only the standards that hit, so a
   convention missing from the index is a convention that exists and is never applied.

   ```yaml
   standards:
     - path: api/route-naming.md
       domain: api
       keywords: [routing, rest, endpoints]
       applies_to: [build-implement, build-plan]
   ```
5. **Report** the count per domain and the conventions worth knowing about before anyone
   writes code — the ones that will surprise someone arriving from a different project.

**Done when** `index.yml` exists, every entry in it resolves to a file that exists, and
every `applies_to` value names a skill that is installed.
