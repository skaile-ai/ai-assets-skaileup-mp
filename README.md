# ai-assets-skaileup-mp

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
skill's name (`concept-brief`, `mockup-walkthrough`, `build-slice-implement`). The nine
domains are **concept · design · experience · spec · mockup · architecture · build ·
quality · ops**.

## Writing a skill

Start from [`docs/skill-template.md`](./docs/skill-template.md) — a ceiling of 140 lines
and a set of defaults, not a form. For the shape in practice, read a landed skill;
[`docs/examples/WHY.md`](./docs/examples/WHY.md) records what the two ports that set the
shape cut, and what each `MUST` / `NEVER` line became.

## Status

Skeleton. Skills and flows land per domain; see the migration map in the old repo at
`.scratch/skaileup-mp/map.md`.
