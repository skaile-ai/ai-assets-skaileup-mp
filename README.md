# ai-assets-skaileup-mp

[![ci](https://github.com/skaile-ai/ai-assets-skaileup-mp/actions/workflows/ci.yml/badge.svg)](https://github.com/skaile-ai/ai-assets-skaileup-mp/actions/workflows/ci.yml)

The skaileup skill collection, rebuilt small. Same product domains as
[`ai-assets-skaileup`](https://github.com/skaile-ai/ai-assets-skaileup) — design, spec,
mockups, build, quality — as roughly **9 domains and ~30 skills** instead of 17 and 95,
with one shared vocabulary ([`CONTEXT.md`](./CONTEXT.md)) and a flat tree.

This repo is built **in parallel** with the original. Nothing is cut over: projects opt
in by pointing `skaile.yaml` at `-mp`. The old collection keeps running untouched.

## Layout

```
skills/<name>/SKILL.md     one directory per skill; the directory name IS the name: field
flows/<id>/<id>.flow.yaml  the graph over skills — order lives here, not in the filesystem
contracts/                 the shared reference layer every skill reads
profiles/                  project-type data (web-app, api-service, cli-tool, …)
docs/                      skill template, worked examples, decision records
CONTEXT.md                 the collection's glossary — the words skills use with each other
```

No `NN_` prefixes anywhere, no domain folders: the domain is the first segment of the
skill's name (`concept-brief`, `mockup-walkthrough`, `build-implement`). The nine
domains are **concept · design · experience · spec · mockup · architecture · build ·
quality · ops**.

One skill carries no domain: [`skaileup`](./skills/skaileup/), the router. It is named for
the collection because it is the door into it rather than a step inside one domain — run it
when work arrives from outside a flow, or when a `_concept/` tree is opened cold and the
next skill is unclear.

## Writing a skill

Start from [`docs/skill-template.md`](./docs/skill-template.md) — a ceiling of 140 lines
and a set of defaults, not a form. For the shape in practice, read a landed skill;
[`docs/examples/WHY.md`](./docs/examples/WHY.md) records what the two ports that set the
shape cut, and what each `MUST` / `NEVER` line became.

## How a project moves through it

A **flow** is the unit a project is sized by: it names the skills and the order, so the
graph carries the sequence and no prose restates it. Four ship:

| Flow | For |
|---|---|
| [`appbuilder-mvp`](./flows/appbuilder-mvp/) | The lean end-to-end path — 9 skills, one featureset pass |
| [`appbuilder-standard`](./flows/appbuilder-standard/) | A multi-user app in full — 27 skills, discovery through review |
| [`skaileup-concept-only`](./flows/skaileup-concept-only/) | The conceptualization half alone, to hand a specified product on |
| [`skaileup-concept-reverse`](./flows/skaileup-concept-reverse/) | A concept built out of an existing repository |

A host picks the flow (in forge-concept the profile key *is* the flow id) and runs its
nodes; each writes into `_concept/`, the one artifact tree, described in
[`contracts/concept_structure.md`](./contracts/concept_structure.md).

## Status

Skeleton. Skills and flows land per domain; the migration map is in this repo at
[`.scratch/wayfinder/map.md`](./.scratch/wayfinder/map.md).

There is **no documentation site**. The old collection's Starlight site stays in
[`ai-assets-skaileup`](https://github.com/skaile-ai/ai-assets-skaileup) with the tree it
describes; here the flows are the pipeline, `docs/adr/` holds why the collection is shaped
as it is, and `scripts/check.py` answers whether it still hangs together.

**Green means `python scripts/check.py`** — it checks the collection and then runs its own
fixtures, so one command is the whole gate. The badge above is the same answer for anyone
who did not run it.
