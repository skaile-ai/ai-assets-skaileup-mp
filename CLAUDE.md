# ai-assets-skaileup-mp

The skaileup collection rebuilt small: ~9 domains, ~30 skills. Built in parallel with
[`ai-assets-skaileup`](https://github.com/skaile-ai/ai-assets-skaileup), which stays live
and untouched — projects opt in via `skaile.yaml`.

## The invariants

- **`skills/<name>/SKILL.md`, flat.** The directory name equals the `name:` field
  character for character. That one string is the install path, the flow node's
  `data.skill`, and the grounding input path. No `NN_` prefixes, no domain folders — the
  domain is the name's first segment.
- **Nine domains:** `concept · design · experience · spec · mockup · architecture ·
  build · quality · ops`. `quality` inspects `src/`; `ops` inspects `_concept/`.
- **Names are `domain-skill`** — 2 segments by default, 3 for a real sub-cluster, never 4.
  Separator `-`, never `_`.
- **Order lives in the flow graph**, never in the filesystem.
- **Skill bodies: 140 lines including frontmatter.** No `MUST`/`NEVER` block — constraints
  are stated positively at the step they bind, and a hard guardrail is a named failure with
  a check behind it. See [`docs/skill-template.md`](./docs/skill-template.md).
- **Frontmatter carries only what a machine reads**: `version`, `artifacts.requires[].id`,
  `prerequisites.*`, `requires`. Everything else is documentation and belongs in the body.
  The machine layer sits **under `metadata:`** and its paths start with **`_concept/`** —
  that is where the readers look, and neither failure raises ([ADR 0011](./docs/adr/0011-the-machine-layer-sits-under-metadata.md)).
- **Flow nodes declare `data.phase`** rather than relying on forge-concept's name-prefix
  fallback.

## The vocabulary

[`CONTEXT.md`](./CONTEXT.md) is the collection's glossary and nothing else — no paths, no
process. Use its words; don't redefine them locally. Where a thing *lives* is
[`contracts/concept_structure.md`](./contracts/concept_structure.md)'s job.

Two words that are easy to get wrong: an **asset** is shipped by this repo; an **artifact**
is written into a project. A **slice** is a vertical slice, implementation-side only — the
concept-side per-feature thing is a **feature dossier**.

## Contracts

[`contracts/`](./contracts/) is the shared reference layer. A file earns its place there
only if more than one skill reads it *at a step in its body*, or a machine reads it.
Citing a contract in passing is not reading it.

## Decisions

[`docs/adr/`](./docs/adr/) holds the decision records this collection was built from.
Read them before re-litigating shape questions.
