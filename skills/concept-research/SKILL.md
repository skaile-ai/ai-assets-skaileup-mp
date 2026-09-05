---
name: concept-research
description: "Use when a decision needs grounding in something other than the room's opinion — the domain, the competitors, the audience, or the visual references screens will be designed against. Runs beside any other step rather than after it. Triggers on 'research this', 'what do competitors do', 'find inspiration', 'who are the users really'."
version: "0.1.0"
metadata:
  artifacts:
    requires:
      - { id: brief }
  prerequisites:
    files:
      - { path: "_concept/brief.md", gate: soft }
    inputs_optional:
      - { id: research_scope, label: "What to research", type: multiselect, options: [domain, competitors, audiences, design, patterns, colors, behavioral], hint: "Leave empty for the four defaults" }
---

# concept-research

Fills `02_grounding/research/` with findings that other skills design against, and
`02_grounding/findings/` with the raw material behind them. It is not a pipeline step with a
place in the order — it runs alongside whichever step needs grounding, and nothing waits on
it. It writes findings only: no brief, no features, no tokens.

Paths are `contracts/concept_structure.md`'s; subagent dispatch is
`contracts/agent_patterns.md § Subagent Dispatch`.

## Steps

1. **Scope the research against the brief.** Read `brief.md`, `goals.md` and
   `comparable.md` where they exist, and pull out the domain, the audience segments and the
   products already named — the user's own comparables go on the list before anything you
   found. Present the plan as who and what you will investigate, and let them add or cut.
   Research that answers a question nobody asked spends the same tokens as research that
   does.
2. **Dispatch one background agent per topic** and keep working while they read. Each is
   pointed at **primary sources** — official documentation, the product itself, first-party
   pricing and changelogs, the spec — and follows every claim back to whoever owns it. A
   secondary write-up is a claim about a claim, and it is the one that turns out to be two
   years stale. Each agent returns its findings with a source against every factual claim.
3. **Write the findings**, one file per topic, each with the count it carries and
   `last_updated` in frontmatter per `contracts/artifact_frontmatter.md`:
   `domain.md` (terminology, regulations, trends, the workflows this domain already has),
   `competitors.md` (per product: features, strengths, the gaps users complain about,
   pricing, audience, and what it means for this product), `audiences.md` (per persona:
   real job title, current tools, pain points, and the design implications), and
   `design-inspiration.md`. Add `patterns.md`, `colors-fonts.md` or `behavioral-patterns.md`
   only when the scope asked for them. A persona like "busy professional" describes nobody
   and produces screens for nobody; a competitor feature that could not be verified is
   written as not publicly available rather than filled in.
4. **Always write `design-inspiration.md`.** `design-brand`, `experience-shell` and both
   mockup renderers read it, and it is the file that most often goes unwritten because the
   competitor work ran long. Layout patterns, colour directions, typography pairings and
   component patterns — each with its source, and each with where in *this* product it would
   apply. Once `03_brand/tokens.json` exists the references stay inside it: an off-palette
   reference collected after the brand is chosen is a reference nothing can be built from.
5. **Catalogue the raw material.** Screenshots, page saves and excerpts go under
   `02_grounding/findings/` with `index.md` listing each one's source and date. Research
   dispatched alongside one particular skill goes to `02_grounding/research/step/<skill
   name>/` instead — the directory is that skill's `name:` character for character, which is
   how it finds it again.
6. **Report what changed the picture**, not what was collected: the competitor gap, the
   persona nobody had in mind, the regulation that constrains the data model. Point at the
   skills that should now be re-run or run for the first time.

**Done when** every file the scope asked for exists, every factual claim in them names its
source, and `02_grounding/findings/index.md` accounts for the raw material.
